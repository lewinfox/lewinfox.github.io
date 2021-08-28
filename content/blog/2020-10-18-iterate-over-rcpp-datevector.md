---
title: "How to iterate over an Rcpp DateVector (with example)"
date: 2020-10-10T17:33:04+12:00
slug: "iterate-over-rcpp-datevector-example" 
description: "Tutorial showing how to iterate over an Rcpp DateVector in R"
keywords: [R Rcpp DateVector tutorial] 
draft: false
tags: [R, Rcpp, tutorials]
math: false
---

In a recent Rcpp project I wanted (in C++) to iterate over the elements of a `DateVector`. It turns out that my naive approach didn't work, and it took me a fair bit of Googling to find the answer so I thought it was worth recording. If you're in a rush you can skip the preamble and [jump straight to the solution](#the-solution-create-a-date-object).

## Iterating over `DateVector`s doesn't work as expected

For the sake of this example let's say I was trying to duplicate [`lubridate::year()`](https://lubridate.tidyverse.org/reference/year.html), i.e. given a vector of dates, return a vector containing just the year of those dates. An `Rcpp::Date` object has a `getYear()` method, but a `DateVector` doesn't have an equivalent. No problem, just loop over the `DateVector` and call the `getYear()` method on each, right?

Here's my first attempt:

```cpp
#include <Rcpp.h>
using namespace Rcpp;

// [[Rcpp::export]]
IntegerVector get_years(const DateVector& dates) {
  auto n = dates.length();
  IntegerVector out(n);
  for (auto i = 0; i < n; i++) {
    out[i] = dates[i].getYear();  
  }
  return out;
}
```

To my surprise this yielded a compiler error saying that the `getYear()` method doesn't exist for `double` objects, which is confusing because I'm working with a vector of `Date`s, not `double`s, aren't I?

```
E> get-years.cpp: In function 'Rcpp::IntegerVector get_years(const DateVector&)':
   get-years.cpp:9:23: error: request for member 'getYear' in 
   [...looooong Rcpp class description...]
   which is of non-class type 'const type {aka const double}'
E>      out[i] = dates[i].getYear();
E>                        ^
```

## The solution: create a `Date` object

If we explicitly create a `Date` object first the compiler is perfectly happy; the code below works as expected:

```cpp
#include <Rcpp.h>
using namespace Rcpp;

// [[Rcpp::export]]
IntegerVector get_years(const DateVector& dates) {
  auto n = dates.length();
  IntegerVector out(n);
  for (auto i = 0; i < n; i++) {
    Date d = dates[i];
    out[i] = d.getYear();
  }
  return out;
}
```

An explanation for this behaviour is given in a [related StackOverflow question](https://stackoverflow.com/questions/55981439/rcpp-error-comparing-a-datevector-element-with-a-date). To quote [duckmayr](https://stackoverflow.com/users/8386140/duckmayr)'s answer:

> [...] an `Rcpp::DateVector` is not a vector of `Rcpp::Date`s, but is a class derived from `Rcpp::NumericVector` (see [here](https://github.com/RcppCore/Rcpp/blob/6062d561939e72a9a6bbf0d0b3a2311374be3552/inst/include/Rcpp/date_datetime/newDateVector.h#L29)). This makes sense considering R's own internal treatment of date vectors:
>
> ```r
> pryr::sexp_type(as.Date("2019/05/04"))
> # [1] "REALSXP"
> ```

To which [Dirk Eddelbuettel](https://stackoverflow.com/users/143305/dirk-eddelbuettel), the maintainer of Rcpp, added:

> [...] conversion[s] which do require to/from conversion to `SEXP` "generally work" but the compiler sometimes needs some help. As such the assigning of a `DateVector` element to a `Date` makes comparison easier.

This explains the compiler error, but for me it was not intuitive that a `DateVector` is not the same as a vector of `Date`s.

[duckmeyr's answer](https://stackoverflow.com/a/55981814) goes on to suggest an alternative:

> If what you actually want is a vector of `Rcpp::Date`s, that can be achieved easily as well using the member function `getDates()`:
>
> ```cpp
> // [[Rcpp::export]]
> bool dateProb(DateVector dateVec, Date date) {
>     Date date2 = dateVec(0);
>     std::vector<Date> newdates = dateVec.getDates();
>     Rcpp::Rcout << (newdates[0] < date) << "\n";
>     return (date2 < date);
> }
> ```

Hopefully this post was useful to someone, and you found your answer quicker than I did!

