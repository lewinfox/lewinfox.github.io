+++
title = "ACC"
date = 2024-01-15
description = "Designing an MLOps pipeline"
+++


## Building Scalable MLOps and LLM Solutions at ACC

Between 2022 and 2024, I worked with the Accident Compensation Corporation (ACC) in Wellington,
supporting their Data Engineering team. The engagement began with a need to modernise how machine
learning models were deployed, monitored, and integrated into business systems. While ACC had a
strong data foundation, they lacked an end-to-end MLOps framework to move models from notebooks into
production safely and efficiently.

I co-designed and implemented an MLOps architecture using MLflow, Docker, Python, and R. This system
allowed data scientists to containerise their models, capture inputs and outputs for auditability,
and serve predictions via REST APIs. We supported both batch and on-demand use cases, which meant
teams could deploy a wider variety of models to production. As a result, ACC was able to
operationalise its machine learning work more reliably and at lower risk.

In parallel, I led a stream of work around Large Language Models (LLMs). Using Ollama, vector
databases, and Retrieval-Augmented Generation (RAG), we built a prototype that let staff query
ACC-specific documents via a conversational interface. I also wrote a custom middleware layer to
integrate these components cleanly. This proof of concept demonstrated the potential of LLMs for
surfacing institutional knowledge in a user-friendly way.

Alongside this, I delivered a number of developer productivity improvements. I wrote a Python CLI
tool that automated dbt documentation, saving engineers hours each week, and built a GUI for editing
dbt models. I also established reusable ingestion pipelines in dbt, ensuring consistency across
projects. Finally, I helped ACC scale their Snowflake infrastructure by deploying Terraform
frameworks for file ingestion, UDFs, and security policies.

This combination of MLOps, LLM experimentation, and infrastructure automation gave ACC both
immediate value — in the form of faster, more reliable model deployments — and a foundation for
future data science innovation.
