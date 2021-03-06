UUID: 03a0e2cd-fce2-48ec-9fdd-4addcaad0021
Status: published
Author: Ben Chuanlong Du
Date: 2017-04-22 14:56:23
Slug: oracle-sql-tips
Title: Oracle SQL Tips
Category: Programming
Tags: programming, Oracle SQL, tips

**
Things on this page are fragmentary and immature notes/thoughts of the author. 
It is not meant to readers but rather for convenient reference of the author and future improvement.
**
 

0. Unlike Teradata SQL, 
a `select` statement in Oracle must have the `from` keyword. 
The `dual` table can be used if you do not really want to select from a table.
```SQL
select 'example' from dual
```

1. insert multiple records/tuples into a table/tables
```SQL
insert all
into t1(f1, f2) values (v1, v2)
into t1(f1, f2) values (v3, v4)
into t2(n1, n2) values (w1, w2)
select * from t1;
```
Note that you must issue a `select` clause at the end.
Fields declaration can be omitted. 

2. Show user tables
```SQL
select * FROM user_tables;
```

3. rownum vs rownumber() over() 

3. how to drop if exists?

4. it's strange that I cannot insert multiple records into an empty table!
be careful! you previous conclusion about fields might be wrong!

## Data Type

1. `varchar` is reserved by Oracle to support distinction 
between NULL and empty string in future, 
as ANSI standard prescribes.
`varchar2` does not distinguish between a NULL and empty string, 
and never will.
If you rely on empty string and NULL being the same thing, 
you should use `varchar2`.

## Regular Expression
```SQL
select
    regexp_substr('Programming', '(\w).*?\1', 1, 1, 'i')
from
    dual
;
```

## Trick and Traps

Oracle sql: it seems that {} in /* ... */ causes issues ...
