UUID: 03a0e2cd-fce2-48ec-9fdd-4addcaad0021
Status: published
Date: 2014-09-05 01:22:21
Slug: environments-in-r
Author: Ben Chuanlong Du
Title: Environments in R
Category: Programming
Tags: R, programming, environment

**
Things on this page are
fragmentary and immature notes/thoughts of the author.
It is not meant to readers
but rather for convenient reference of the author and future improvement.
**

1. The option `pos=1` of the function `assign` refers to the global environment, 
i.e., the user's workspace. 
Containers in R are 1-based, 
so it is easy to understand (and remember) that R use 1 to stand for the global enviroment (user's workspace).
Notice that `..GlobalEnv` is a variable standing for the global environment and `globalenv()` returns the global environment,
`pos=1` is equivalent to say `pos=.GlobalEnv` or `pos=globalenv()`.
If you want to create a global variable in a function,
you can use the function `assign` by specifying `pos=1` (or `pos=.GlobalEnv` or `pos=globalenv`).
Another easier but less powerful way is to the `<<-` or `->>` to assign/create global variables. 
    
2. The function `new.env` creates a new environment. 
If you want to source in some code 
but would rather let the code in a new environment (so that the environment sourcing the code is not contaminated),
you can use `source(path_to_file, local=new.env())`.

3. The function `emptyenv` returns an immutable empty environment. 
The empty environment is not used to evaluate expressions or run code but rather to check whether nested environments end.
