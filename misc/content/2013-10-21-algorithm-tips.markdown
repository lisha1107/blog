UUID: 03a0e2cd-fce2-48ec-9fdd-4addcaad0021
Status: published
Author: Ben Chuanlong Du
Date: 2015-02-24 13:20:33
Slug: algorithm-tips
Title: Tips About Algorithms
Category: Software
Tags: tips, algorithm, error tolerance, numerical issue, overflow

**
Things on this page are fragmentary and immature notes/thoughts of the author. 
It is not meant to readers but rather for convenient reference of the author and future improvement.
**
 
1. comparing lots of values that are very close is not a good idea. p-values, permutation test statistics.
a better way is to work on integers instead, for example, permutation indexes ...
if you do have to compare real numbers, give an error tolerance. 

2. the error doesn't come from calculation but from storing numbers. 
I used to think that log(x) is problematic when x is small (I thought this can cause numeric problems).
acutally this won't cause problems at all as long as x is a positive double number.

3. overflow of double becomes inf, for arithematic calculating, this is probably not a problem
overflow of positive double (to left) becomes 0, for many arithematic calculation, this is not a problem.

4. use log and then exp is a good way to avoid overflowing problem,
this trick is used a lot in statistics but it seems that even boost libary don't use this trick.
so, don't trust these libraries totally, you own implementation might even be better.

