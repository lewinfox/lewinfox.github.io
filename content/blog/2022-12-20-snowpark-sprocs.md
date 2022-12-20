---
title: "How to deploy Snowflake stored procedures with Python"
date: 2022-12-20T19:24:21+13:00
slug: "deploy-snowflake-stored-procedures-python"
description: "How to deploy Snowflake stored procedures using Python"
keywords: ["snowflake", "snowpark", "python", "tutorial"]
draft: false
tags: ["python", "snowflake", "snowpark", "tutorials"]
math: false
toc: true
---

This post walks through an example of deploying a 
[Snowflake stored procedure](https://docs.snowflake.com/en/sql-reference/stored-procedures.html) 
using the 
[Snowpark Python library](https://docs.snowflake.com/en/developer-guide/snowpark/python/index.html).

Most of the examples online (including in the official 
documentation) assume you're doing this via a SnowSQL session. 
This guide assumes you want to have a deployment script to make 
the process automatable via GitHub Actions or your CI/CD tool of 
choice.

## Setup

We'll be using the `snowflake-snowpark-python` library to deploy 
our procedure. At the time of writing (December 2022) this only 
works with Python 3.8. If you're using 
[`conda`](https://www.anaconda.com/) you can create a virtual 
environment using Python 3.8 with the Snowpark library 
installed as follows:

``` shell
conda create --name my_env snowflake-snowpark-python python=3.8
```

## Creating a single-file Python function

First we need a Python function that will become our stored 
procedure. I'm using a simple `add_one()` function as an 
example, saved in a file called `main.py`.

``` python
# main.py
from snowflake.snowpark import Session

def add_one(session: Session, x: int) -> int:
    """Add one to an integer"""
    return x + 1
```

Some things to note here:

1) We're using [type hints](https://docs.python.org/3.8/library/typing.html). 
   This makes life easier later on as Snowpark will use these to 
   generate the appropriate input and return types for the 
   function. More on this later.
2) The first argument to the function _must_ be a 
   [`snowflake.snowpark.Session`](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/session.html) 
   object, even if we don't do anything with it in the function
   itself. When we call the generated stored procedure the
   `Session` will be automatically supplied by the Snowflake 
   runtime, i.e. our SQL call will look like:

   ``` sql
   CALL ADD_ONE(1)
   ```

   If the first argument to your function isn't a `Session`
   object, Snowpark will throw an error when you try and deploy.


## Writing a deployment script

The Snowpark API provides a 
[`register_from_file()`](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/api/snowflake.snowpark.stored_procedure.StoredProcedureRegistration.register_from_file.html)
function that we can use to deploy our procedure. Here's a super
simple deployment script.

For information on connecting to Snowflake see 
[the Snowpark docs](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/api/snowflake.snowpark.Session.html#snowflake.snowpark.Session).

``` python
# deploy.py
from snowflake.snowpark import Session

# Connection parameters shouldn't be hard-coded into the script 
# like this. Use environment variables, GitHub Actions secrets, 
# etc.
SF_CONNECTION_PARAMS = {
    "account": "my.snowflake.account",
    "user": "me@email.com",
    "password": "password123",
    "warehouse": "my_warehouse",
    "role": "my_role",
    "database": "my_database",
    "schema": "my_schema"
}

# Create a session that we will use to deploy our proc
session = Session.builder.configs(SF_CONNECTION_PARAMS).create()

# Create a Snowflake stage to hold the uploaded Python source
# files
session.sql(
    "CREATE STAGE IF NOT EXISTS PYTHON_SOURCE_CODE"
).collect()

# Deploy the procedure
session.sproc.register_from_file(
    name = "add_one", # Name of the procedure in Snowflake
    stage_location = "python_source_code",
    file_path = "main.py",
    func_name = "add_one", # Within `main.py`
    is_permanent = True,
    replace = True,
    packages = ["snowflake-snowpark-python"]
)

```

Running `python deploy.py` will deploy the stored procedure.

### Notes

* `name` is the name of the deployed procedure in Snowflake.
  This doesn't have to be the same as the name of the function.
* `is_permanent` should be `True`. If left as `False` the
  procedure will only exist for the duration of the `session`
  used to deploy it, i.e. it won't be useable once the
  deployment script has run.
* `replace = True` means that any pre-existing procedure with
  this name will be replaced. If this is `False` then trying to
  deploy a procedure whose name already exists will cause an
  error.
* `packages` _must_ contain `snowflake-snowpark-python` even if
  you're only using Python standard library packages.
* If we hadn't included type hints in our source code we'd also
  need to supply `input_types` and `return_type` arguments to
  `deploy_from_file()`.


## Using multiple Python files

If your Python code is split over multiple files you need to
tell Snowpark which files need to be included in the deployment
package. For example, if I have a custom module containing some
application code:

``` python
# my_module.py

def greater_than_ten(x: int) -> bool:
    """Is a number greater than ten?"""
    if x > 10:
        return True
    
    return False
```

and I want to import this module into my main procedure code:

``` python
# main.py
from snowflake.snowpark import Session

import my_module

def sometimes_add_one(session: Session: x: int) -> int:
    """Add one to integers that are greater than ten"""
    if my_module.greater_than_ten(x):
        return x

    return x + 1
```

the deployment command needs to refer to `my_module.py` to
ensure it's uploaded.

``` python
# deploy.py

# ... see above

session.sproc.register_from_file(
    name = "add_one", # Name of the procedure in Snowflake
    stage_location = "python_source_code",
    file_path = "main.py",
    func_name = "add_one", # Within `main.py`
    is_permanent = True,
    replace = True,
    packages = ["snowflake-snowpark-python"],
    imports = ["my_module.py"] # This becomes `import my_module`
)
```

This example demonstrated how to use a Python script to deploy a
single Snowflake stored procedure. You could easily expand this
to deploy multiple procedures, which may be more suitable for 
use in a CI/CD environment.
