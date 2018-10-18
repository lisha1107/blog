UUID: 9fde8ad7-e1b6-420e-8db0-e0046f8eb529
Status: published
Date: 2017-06-25 12:10:31
Author: Ben Chuanlong Du
Slug: odbc-vs-jdbc-in-python
Title: ODBC vs JDBC in Python
Category: Programming
Tags: programming, Python, ODBC, JDBC, database, SQL

**
Things on this page are
fragmentary and immature notes/thoughts of the author.
It is not meant to readers
but rather for convenient reference of the author and future improvement.
**

Overall speaking, 
Python has better ODBC support than JDBC support. 
Most database related packages in Python support or rely on ODBC. 
Currently, ODBC packages also have richer feathers than JDBC packages.
However, 
it is not an easy job to install and configure ODBC drivers for a non-open source databases. 

## JDBC Packages in Python

1. `JayDeBeApi` is currently the first choice even thought it is not fully DB-API compliant.
It works on both Python 2 and Python 3.

2. `py4jdbc` (based on Py4j) is another JDBC package which claims to be faster than `JayDeBeApi` (based on JPype)
but it is relative young compared to JayDeBeApi.

3. Just ignore the JayDeBeApi3 package (for Python3 only). 

4. PyAthenaJDBC is a JDBC package specifically for Amazon Athena.

## ODBC Packages in Python

1. `pyodbc` and `SQLAlchemy` are general purpose packages relying on ODBC. 

2. There are lots of database specific packages relying on ODBC. 
For example, 
`teradata` is a Python package for Teradata SQL which relies on ODBC or RESTful.

## Misc


http://docs.python-guide.org/en/latest/scenarios/db/


the teradata package is weird, the file option can be used to run multiple statements in file ...
but if I manually pass a string, it doesn't work ... check the implementation ...
https://support.microsoft.com/en-us/help/3103282/teradata-odbc-configuration-on-linux
https://developer.teradata.com/tools/articles/teradata-sqlalchemy-introduction
https://github.com/Teradata/sqlalchemy-teradata
http://developer.teradata.com/tools/reference/teradata-python-module#Installing
http://stackoverflow.com/questions/34948453/read-teradata-query-into-pandas


## ORM

SQLalchemy, peewee (lightweight)


http://stackoverflow.com/questions/10797794/multiple-queries-executed-in-java-in-single-statement

https://wiki.vip.corp.ebay.com/pages/viewpage.action?pageId=327124647



http://stackoverflow.com/questions/4493614/sqlalchemy-equivalent-of-pyodbc-connect-string-using-freetds

https://developer.teradata.com/tools/articles/teradata-sqlalchemy-introduction

http://stackoverflow.com/questions/12047193/how-to-convert-sql-query-result-to-pandas-data-structure

http://stackoverflow.com/questions/29525808/sqlalchemy-orm-conversion-to-pandas-dataframe/29528804#29528804


## JDBC

https://analyticsanvil.wordpress.com/2016/06/08/python-jdbc-dyanmic-hive-scripting/

https://github.com/minatverma/pythonWorks/blob/master/DQM.py

https://www.fullstackpython.com/databases.html

http://docs.python-guide.org/en/latest/scenarios/db/

## DBAPI

the cursor obj has an member description which contains the column information and more ...

https://wiki.vip.corp.ebay.com/pages/viewpage.action?pageId=327124647
