Status: published
Date: 2019-08-26 23:40:57
Author: Benjamin Du
Slug: spark-issue-cannot-create-a-path-from-an-empty-string
Title: Spark Issue Cannot Create a Path from An Empty String
Category: Programming
Tags: programming, Spark, issue, empty string, path

**
Things on this page are fragmentary and immature notes/thoughts of the author.
It is not meant to readers but rather for convenient reference of the author and future improvement.
**

## Issue

java.lang.IllegalArgumentException: Can not create a Path from an empty string

## Possible Causes

The error you are seeing could be from number of things:

1. parameters , check for ${param} in the code and make sure it has value

2. create external table with invalid path (path containing spaces or parameter that is null)

3. insert overwrite directory statement with invalid path. 

## Solutions

Identify the root cause and fix accordingly.


## References

https://forums.aws.amazon.com/thread.jspa?threadID=132895
