+++
title = "foodwebr"
description = "Function dependency graphs in R"
weight = 1

[extra]
github = "https://github.com/lewinfox/foodwebr"
tags = ["R", "visualization", "code-analysis"]
+++

The foodwebr package enables developers to visualize how functions call each other within R codebases. It makes it easy to visualise the dependency graph of a set of functions (i.e. who calls who).

**Key applications:**
- Exploring unfamiliar codebases to understand function relationships
- Documenting internal function dependencies within packages
- Aiding code comprehension and maintenance

The package generates directed graphs showing which functions depend on which others, displaying results through graphviz-based visualizations that can be printed, plotted, or converted to tidy graph objects for advanced analysis.

Available on CRAN. See the [GitHub repository](https://github.com/lewinfox/foodwebr) for more details.
