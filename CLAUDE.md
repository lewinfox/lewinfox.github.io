# Overview

This website is build with [`zola`](https://www.getzola.org/documentation) and
is a business sire promoting my data engineering consultancy.

A development server is always running at `localhost:1111`; use `curl` if you
need to inspect a page or test anything.

Site CSS is defined in `sass/style.scss`. Any styling changes should be applied
this file rather than in any CSS or HTML files.

My CV is available at `cv.md`. Refer to this to find my skills and experience.

# Site contents

- Homepage
- Blog

## Headers and footers

All pages contain a header and footer. The header contains a link to my github,
LinkedIn, and a mailto:lewin.a.f@gmail.com. The footer contains the same plus a
copyright notice.

## Homepage

Aims to give the reader a clear and immediate overview of the services I offer.
My elevator pitch is that I am a full-stack data developer, meaning I can do
everything from building dashboards, spreadsheet wrangling, ETL pipeline
development, data warehouse design, and system architecture.

Core technologies:

- Python
- SQL
- dbt
- Snowflake
- AWS
- Docker
- Terraform

## Blog

Contains blog posts on various technical topics likely to be of interest to
someone searching for data engineering topics. For now this can be a bullet point
list of topics relevant to my skills.

## Design principles

The website should be as light as possible, content-first. Minimal JS, maximum
simplicity, clear navigation, simple tech stack. I am not a web developer and
want something simple and maintainable.

## Notes for Claude

The `Makefile` contains targets for `build` and `serve`. Don't run these, but
be aware that we are using a Docker container to make the developer experience
as clean as possible. Assume there is always a live server running during
development; you do NOT need to build or serve the site at any point.
