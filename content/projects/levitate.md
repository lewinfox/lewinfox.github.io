+++
title = "levitate"
description = "Fuzzy string matching in R"
weight = 3

[extra]
github = "https://github.com/lewinfox/levitate"
+++

The levitate package provides fuzzy string matching capabilities entirely in R, with no dependencies on Python or the reticulate package. Inspired by Python's thefuzz library (formerly fuzzywuzzy), it enables developers to:

- Calculate string similarity and distance metrics
- Perform tokenized comparisons that handle word order variations
- Weight specific tokens to influence matching results
- Rank candidates by similarity to find best matches

The package implements multiple matching algorithms including basic ratio calculations, partial ratios, token-sorted comparisons, and token-set approaches—offering vectorized functions for efficient batch processing of string comparisons.

See the [GitHub repository](https://github.com/lewinfox/levitate) for more information.
