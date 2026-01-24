+++
title = "icecream"
description = "Never use print() to debug again"
weight = 2

[extra]
github = "https://github.com/lewinfox/icecream"
tags = ["R", "debugging", "developer-tools"]
+++

The icecream package is an R debugging tool designed to simplify print debugging. It provides an `ic()` function that displays expressions alongside their evaluated values, along with optional context information like file location and function name.

**Key features:**
- Variable inspection with automatic value printing
- Execution tracking showing file, line number, and function context
- Support for complex data structures (data frames, lists) with smart summarization
- Enable/disable functionality for conditional debugging output
- Customizable output formatting through R options

This project is an R port of the original Python icecream library by Ansgar Grunseid.

See the [GitHub repository](https://github.com/lewinfox/icecream) for installation and usage details.
