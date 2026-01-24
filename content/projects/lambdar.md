+++
title = "lambdar"
description = "Tools to help you run R on AWS Lambda"
weight = 4

[extra]
github = "https://github.com/lewinfox/lambdar"
+++

Lambdar is an R package designed to simplify deploying R functions to AWS Lambda by providing a custom runtime environment. The package enables developers to write R code normally, then annotate handler functions with a `@lambda` tag.

**Key capabilities:**
- Automated Docker container creation for AWS Lambda
- Local testing via AWS's Runtime Interface Emulator
- Seamless deployment to AWS Elastic Container Registry
- Configuration management and dependency scanning
- Full deployment pipeline automation

The package streamlines the entire process from building Dockerfiles to uploading container images to ECR, eliminating the need for manual AWS Lambda setup.

See the [GitHub repository](https://github.com/lewinfox/lambdar) for installation and usage instructions.
