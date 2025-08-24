# Lewin Fox - Personal Website

Built with [Zola](https://www.getzola.org/documentation/getting-started/installation/)

## Quick Start

Open in the devcontainer, run `zola serve` and the site will be served on `localhost:1111`.

## How Templates and Content Interact

### Content-to-Template Mapping

**Content Type → Template Used:**

- `content/_index.md` → `templates/index.html` (homepage)
- `content/blog/_index.md` → `templates/section.html` (blog listing)
- `content/about/_index.md` → `templates/section.html` (about page)
- `content/blog/hello-world.md` → `templates/page.html` (individual post)

### Template Hierarchy

**Base Template (`base.html`):**

```html
<html>
  <head>
    ...
  </head>
  <body>
    <header>...</header>
    <main>{% block content %}{% endblock content %}</main>
    <footer>...</footer>
  </body>
</html>
```

**Child Templates Extend Base:**

- `index.html` → `{% extends "base.html" %}`
- `section.html` → `{% extends "base.html" %}`
- `page.html` → `{% extends "base.html" %}`

### Data Flow

**From Content Files:**

```toml
+++
title = "Hello World"
description = "Welcome to my blog"
date = 2024-01-15
+++
# Markdown content here
```

**To Templates:**

- `{{ page.title }}` → "Hello World"
- `{{ page.description }}` → "Welcome to my blog"
- `{{ page.date }}` → 2024-01-15
- `{{ page.content | safe }}` → Rendered markdown HTML

### Key Variables

**For Pages (individual posts):**

- `page.title`, `page.content`, `page.date`
- `page.earlier` / `page.later` (navigation)
- `page.reading_time` (auto-calculated)

**For Sections (blog listing, about):**

- `section.title`, `section.content`, `section.pages`
- `section.pages` contains all posts in that section

**Global Config:**

- `config.extra.title` → "Lewin Fox"
- `config.extra.menu_items` → Navigation array

### Template Logic Examples

**Homepage Recent Posts:**

```html
{% for page in section.pages | slice(end=3) %}
<h3><a href="{{ page.permalink }}">{{ page.title }}</a></h3>
{% endfor %}
```

**Blog Listing:**

```html
{% for page in section.pages %}
<article>
  <h2>{{ page.title }}</h2>
  <time>{{ page.date | date(format="%B %d, %Y") }}</time>
</article>
{% endfor %}
```

The beauty is that content authors just write markdown with frontmatter, and templates handle all the presentation logic!
