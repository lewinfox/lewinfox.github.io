---
title: "Method dispatch in R - a letter to my younger self"
date: 2020-08-08T11:37:00+12:00
slug: "r-method-dispatch"
description: "An explanation of method dispatch in R for beginners"
keywords: ["R", "method-dispatch", "tutorial"]
draft: false
tags: ["R", "tutorials"]
math: false
toc: false
---

# The confusion

When I first started learning R, one of the things that I struggled to understand was method dispatch.

I was following a tutorial for the [`keras`](https://keras.rstudio.com/) package for image classification. After training the model, the code below generates the predictions:

```r
predictions <- predict(model, test_images, batch_size = 16)
```

I wanted to read up on other options in the `predict()` function besides `batch_size`, but found the documentation was extremely unhelpful:

```r
help(predict)
```
```
### Usage
`predict (object, ...)`

### Arguments
`object` a model object for which prediction is desired.
`...` additional arguments affecting the predictions produced.
```

<div style="font-weight: lighter;">
(Of course this is selective editing - the help page tells you exactly what's going on. I just lacked the background knowledge to understand it at the time.)
</div>

I thought the Keras team had been extremely lazy with their documentation! `object` makes sense, but fobbing me off with "additional arguments affecting the predictions produced" was pretty poor form. Annoyed, I thought maybe reading the source code for `predict()` would help:

```r
View(predict)
```

```r
function (object, ...)
UseMethod("predict")
```
_WUT!_ What's `UseMethod()`? Where's the code?! Even `batch_size` isn't in here, and I _know_ that exists.

At this point I was thoroughly confused and tempted to file this under "a wizard did it". It wasn't until some time, and much reading, later that it clicked for me.

# The explanation

> Note:<br> <div style="font-weight: lighter;">R actually has several different models for object-oriented programming, presumably because it doesn't want you getting cocky. This post only talks about "S3", which is the oldest and simplest. For a comprehensive explanation of OO programming in R I strongly recommend the relevant chapter of [Advanced R](https://adv-r.hadley.nz/oo.html).</div>

For someone coming from a more traditional object-oriented language, R's method dispatch system seems wilfully obscure. In a language like Python or Javascript, methods are defined in the classes on which they operate. For example, you might write a `Dog` class in Python like this:

```python
class Dog:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"A dog called {self.name}"

    def speak(self):
        print(f"{self.name} says 'Woof'")
```

You would then create a `Dog` like this:
```python
spot = Dog("Spot")
```

and call the `speak()` method using "object-dot-method" syntax:

```python
spot.speak()
```

```
Spot says 'Woof'
```

In R's S3 system things are done differently. Instead of methods belonging to objects, we have generic functions like `print()`, `predict()` etc. When one of these generics is called on an object, it checks the object's `class` attribute, looks for a function named `<generic>.<class>()` and calls it, passing in the object and any additional arguments (exactly as the documentation says). In the event that no matching function is found, a default function is called or an error is thrown.

It's probably easiest to show this with an example. Here's how we create an S3 class in R:

```r
# The data is not important here - S3 classes
# can be assigned to any object
fluffy <- 100
class(fluffy) <- "dog"
```

That's it! `fluffy` is now an instance of a `"dog"` object. For someone coming from another language this is already really freaking weird.

If we print the object we can see that all that's happened is that `fluffy` has some metadata attached to it, specifically an `attr`ibute called `"class"` that has a value of `dog`.

```r
print(fluffy)
```
```
[1] 100
attr(,"class")
[1] "dog"
```
That `class` attribute is what R will use to determine the appropriate method to call. When we call `print(dog)`, R sees that the `class` attribute is `"dog"` and searches for a function called `print.dog()`. Because that doesn't exist, a catch-all function called `print.default()` is used, which gives the output we see above.

This is what `UseMethod()` is doing in the `predict()` function - it tells R to search for a `predict.<something>()` function and call it.

Because predicting a dog doesn't make much sense, let's try printing instead. It's as simple as creating a `print.dog()` function:

```r
print.dog = function(x, ...) {
  # This is R's built-in `cat()` function,
  # nothing to do with our dogs
  cat("Woof\n")
}
```
Now when we call `print(fluffy)`, `print.dog()` will be found and called:

```r
print(fluffy)
```
```
Woof
```

This explains why `help(predict)` was so unhelpful. Although I was calling `predict()`, the function doing the actual work was `predict.keras.engine.training.Model()`, which has [much more helpful documentation](https://keras.rstudio.com/reference/predict.keras.engine.training.Model.html).

# Inheritance
The `class` attribute can contain multiple values. The inheritance hierarchy is determined by the order of the values, and successive methods can be called using the function `NextMethod()`, which tells R to move down the class list and try successive methods. When it runs out of methods it will call a default function (`print.default()`, in the case of `print()`) as a last resort, and fail with an error if that's not possible.

For example, if we want to print big and small dogs differently we can define two new `print()` methods:

```r
print.big.dog <- function(x, ...) {
  cat("---\n")
  cat("Woof woof, I'm hungry\n")
  cat("---\n")
  NextMethod()
}

print.small.dog <- function(x, ...) {
  cat("---\n")
  cat("I'm a fast runner!\n")
  cat("---\n")
  NextMethod()
}
```
If we create instances of these new classes and print them:

```r
biggie <- 100
class(biggie) <- c("big.dog", "dog")

skinny <- 200
class(skinny) <- c("small.dog", "dog")
```
We can see that the methods are called in order - `print.[big|small].dog()` first, then `print.dog()` and finally `print.default()`, which generates the output we saw initially

```r
print(biggie)
```

```
---
Woof woof, I'm hungry
---
Woof
[1] 100
attr(,"class")
[1] "big.dog" "dog"
```

```r
print(skinny)

```

```
---
I'm a fast runner!
---
Woof
[1] 200
attr(,"class")
[1] "small.dog" "dog"
```

Hopefully this gives you an idea of the flexibility of the system.

# Parallels with Python
We can actually see a similarity here between R and Python - our Python `Dog` class has a `__str__()` method that is called by the generic function `print()`.

```python
tiddles = Dog("Tiddles")
print(tiddles)
```

```
A dog called Tiddles
```
The idea is similar, it's just that in R the method that does the printing is defined _outside_ the class it relates to.

# Summary
I intended this post to be one that would have cleared up my confusion back in the day, to give me a toehold into the world of S3 methods. I've skipped a load of stuff (what if we wanted to create a generic `speak()` function so we could recreate our Python example above? How do you see what methods are defined for a class? Or what classes implement a certain generic?) but again, check out [Advanced R](https://adv-r.hadley.nz/oo.html) if you want to know more.
