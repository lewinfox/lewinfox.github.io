---
title: "An unexpected use case for Python"
date: 2020-07-18T10:31:00+12:00
slug: "unexpected-use-case-python"
description: ""
keywords: [python, scraping]
draft: false
tags: [python]
math: false
toc: false
---

My partner recently discovered that her blog had been hacked (some time ago) due to a [vulnerability in a WordPress plugin](https://nakedsecurity.sophos.com/2018/11/13/wordpress-gdpr-compliance-plugin-hacked/).

Fortunately the damage was minimal - the attacker had just shoehorned a load of affiliate links into some of her older posts. The attacker had made an effort to incorporate the links with her existing content, which meant that she needed to read through ALL her old posts to identify and remove the links by hand.

I thought this was an interesting challenge - could I write something to help her pick out these bogus links? I usually work in R, but I ran through a web scraping tutorial in Python a few years ago and decided to dust off those skills.

I used a Jupyter notebook so there was a nice quick feedback loop, which was handy for the exploratory phase.

First, some imports:

```python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd
import lxml
```

Then I grabbed the sitemap and parsed it into a navigable object with `BeautifulSoup`:

```python
sitemap_url = "http://the-blog.com/post-sitemap.xml"
sitemap_xml = requests.get(sitemap_url).text
sitemap_soup = BeautifulSoup(sitemap_xml, "xml")
```

I wasn't familiar with the structure of a sitemap, so I needed to read through it to identify the structures that contain blog post links.

```
<url>
  <loc>http://the-blog.com/post-title/</loc>
  <lastmod>2018-06-29T08:47:18+00:00</lastmod>
  <image:image>
    <image:loc>https://some-cdn.net/big-long-url</image:loc>
    <image:title>Some stuff</image:title>
    <image:caption>Some more stuff</image:caption>
  </image:image>
</url>
```

Cool, so it looks like we need these `<loc><\loc>` tags.

```python
tag_list = sitemap_soup.find_all("loc")
```

The `tag_list` object now contains all the nodes matching `loc`, which also included `<image:loc>` entries - I don't want these. Fortunately this is an easy fix with a list comprehension:

```python
url_list = [
    tag.getText() for tag in tag_list 
    if not "image" in tag.getText()
    ]
```

At this point I had a nice clean list of URLs:

```python
['http://the-blog.com/',
 'http://the-blog.com/the-handmade-fair-wiltshire-press-launch/',
 'http://the-blog.com/bits-pieces-may-favourites/',
 # ...
]
```

At this point I had to think about how to flag potentially bogus links. I made the assumption that each bogus domain was unlikely to have been linked to more than once or twice, so I wanted to get a count of the unique domains (e.g. instagram.com, facebook.com) linked to, then filter out those that occurred more than once.

I wrote this function which:

  * Downloads each URL
  * Extracts all the anchor tags
  * Grabs the link text, url and domain (`netloc`) from each URL
  * Creates an object containing that info and appends it to an output list
  * Returns the list

```python
def get_links(urls):
    res = []
    for url in urls:
        html = requests.get(url).text
        soup = BeautifulSoup(html)
        for link in soup.find_all("a"):
            href = str(link["href"])
            text = str(link.getText())
            domain = urlparse(href).netloc
            res.append({
                "page": url,
                "link_domain": domain,
                "link_text": text
            })
    return res
```

The object returned from this function can then be converted directly to a Pandas `DataFrame`.

```python
link_table = pd.DataFrame(get_links(url_list))
```

This took a little while to run - to give you an idea of the size of the data the first ten pages contained over 1,500 URLs. Most of these were sidebars, images etc. rather than the links we were looking for.

At this point the dataset looked something like this:

| `page` | `link_domain` | `link_text` |
|:-------|:--------------|:------------|
| http://the-blog.com/some-post | www.instagram.com  | A few shots from a recent walk |
| http://the-blog.com/some-other-post | www.instagram.com | Sunny lake Tekapo |
| ... many more rows||

At this point I identified the domains that only appeared once, and filtered the result set to only include those domains.

```python
counts_df = link_table.groupby("link_domain").count()
one_shots = counts_df[counts_df["link_text"] == 1].index.tolist()
link_table = link_table[link_table["link_domain"].isin(one_shots)]
```

I ended up iterating on this a bit, including whitelisting some domains to cut down the size of the data. In the end we identified just over 100 domains that only had a single outgoing link, many of which did indeed prove to be fakes!

I enjoyed hacking on this for an evening, and it did end up helping my partner identify some links that weren't obvious the first time round. It was a fun little project, and an unexpected application of some old knowledge.
