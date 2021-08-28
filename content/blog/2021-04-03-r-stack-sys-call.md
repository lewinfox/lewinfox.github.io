---
title: "The R call stack: sys.call()"
date: 2020-11-03T17:33:04+12:00
slug: "r-stack-sys-call"
description: "Tutorial on sys.call in R"
keywords: [R, tutorial, sys.call]
draft: true
tags: [R, tutorials]
math: false
---

This is the first in a series of posts in which I'm going to explore the R call stack and the tools
we have to manipulate it.

# `sys.call()`

Returns a call. What is a call? At a minimum a call is a `language` object pointing to a function.
If that function has arguments, the call object can optionally contain values to be passed to those
arguments.

``` r
get_call <- function(which = 0) {
  # All this function does is capture its own call and return it
  sys.call(which = which)
}
```

``` r
call_object <- get_call(0)
```

If we inspect `call_object` we just see the function call.

``` r
call_object
#> get_call(0)
```

We can see that the object has a length.

``` r
length(call_object)
#> [1] 2
```

And we can look at the data types of each element.

``` r
lapply(call_object, typeof)
#> [[1]]
#> [1] "symbol"
#>
#> [[2]]
#> [1] "double"
```

If we name the arguments in our function call we see that the entries
acquire names.

``` r
call_2 <- get_call(which = 0)

lapply(call_2, typeof)
#> [[1]]
#> [1] "symbol"
#>
#> $which
#> [1] "double"
```

We can access the elements using list subsetting syntax.

``` r
call_2$which
#> [1] 0

call_2[[2]] == call_2$which
#> [1] TRUE
```

However the function component has no name so has to be accessed using
`[[`.

``` r
call_2$``

call_2[[1]]
#> Error: attempt to use zero-length variable name
```

If we use single brackets every entry is treated as a `call`. This leads to some interesting output.

``` r
call_2[1]
#> get_call()

call_2[2]
#> 0()
```

# Exploring other levels

So far we’ve left `which` at the default value of zero. Referring to `help(sys.call)` we find the
following:

> `.GlobalEnv` is given number 0 in the list of frames. Each subsequent function evaluation
> increases the frame stack by 1 and the call, function definition and the environment for
> evaluation of that function are returned by `sys.call`, `sys.function` and `sys.frame` with the
> appropriate index.
>
> `sys.call`, `sys.frame` and `sys.function` accept integer values for the argument `which`.
> Non-negative values of which are frame numbers whereas negative values are counted back from the
> frame number of the current evaluation.

We can demonstrate this by defining a new function `wrapper()` that calls `get_call()` and passes in
a value for `which`. I think that `which` is not a very descriptive parameter name so I've renamed
it `frame_number`.

``` r
wrapper <- function(frame_number = 0) {
  get_call(which = frame_number)
}
```

The default behaviour (`which = 0`) returns the call to `get_call()` as seen from `wrapper()`. Note
how the call differs from what we obtained by calling `get_call()` directly.

``` r
wrapper()
#> get_call(which = frame_number)
```

Things get more interesting when we pass in a different value for `frame_number`. Referring to the
documentation again, we know that `.GlobalEnv` has a frame number of zero, and the number is
incremented with each function call. This means that `wrapper()` has a frame number of 1, and
`get_call()` has a frame number of 2.

![Diagram showing R call stack frame numbering](/img/r-call-stack-environment-frame-numbering.png)

Let’s test that!

``` r
wrapper(1)
#> wrapper(1)

wrapper(2)
#> get_call(which = frame_number)
```

Great, that’s what we expected. If we nested another function inside `get_call()` it would get a
frame number of 3, and so on.

Now let’s try negative numbers. Negative numbers count back from the frame in which `sys.call()`
was called, so we expect `frame_number = -1` to give us `wrapper()`.

``` r
wrapper(frame_number = -1)
#> wrapper(frame_number = -1)
```

What about `frame_number = -2`? That ought to take us back up to frame 0, which is `.GlobalEnv`.

``` r
wrapper(frame_number = -2)
#> NULL
```

`sys.call()` looks for `call` objects, and `.GlobalEnv` is an environment, not a call, so we don’t
get anything useful here.
