UUID: 03a0e2cd-fce2-48ec-9fdd-4addcaad0021
Status: published
Author: Ben Chuanlong Du
Title: Tips for JavaScript
Date: 2019-03-14 23:47:42
Slug: javascript-tips
Category: Programming
Tags: tips, programming, JavaScript, JS, web

**
Things on this page are fragmentary and immature notes/thoughts of the author. 
It is not meant to readers but rather for convenient reference of the author and future improvement.
**


## Node.js

[Node.js](https:/nodejs.org/en/) is a JavaScript runtime environment outside browsers.

https://github.com/sindresorhus/awesome-nodejs

https://github.com/bnb/awesome-awesome-nodejs
 
[JavaScript Libraries](http://javascriptlibraries.com/)
[JavaScript WikiBooks](http://en.wikibooks.org/wiki/JavaScript)
[W3Schools JavaScript Tutorial](http://www.w3schools.com/js/default.asp)

## Build Tools

https://arstechnica.com/civis/viewtopic.php?f=20&t=1432661

https://www.tutorialsteacher.com/typescript/typescript-build-tools

## Install & Import a Package

This is a common misunderstanding in Node.js and npm. Installing a package globally doesn't ensure that the package can be required. A global install is meant to be used to install executable files. For example, if you want to install the latest version of npm, then you could run the command: npm install -g npm. This command would install the npm package in {prefix}/lib/node_modules and the executable file in {prefix}/bin (that usually is in your PATH).

In your case, I'd suggest the following:

$ mkdir my-project

$ cd my-project

$ npm init -y
[...]

$ npm install web3
[...]

$ npm install ethereum.js

$ jupyter notebook
[so that your notebook is created in the folder where the npm packages have been installed]

https://github.com/n-riesco/ijavascript/issues/118

## Testing & Debugging

https://github.com/Microsoft/vscode-recipes/tree/master/Docker-TypeScript

## Docker Client API

https://github.com/AgustinCB/docker-api

https://github.com/apocas/dockerode


1. case sensi tive

2. you don't have to write every line of code in HTML,
    you can save JavaScript code in another file and then load it.


3. alert vs confirm vs prompt

An alert box is often used if you want to make sure information comes through to the user.

When an alert box pops up, the user will have to click "OK" to proceed.

A confirm box is often used if you want the user to verify or accept something.

When a confirm box pops up, the user will have to click either "OK" or "Cancel" to proceed.

If the user clicks "OK", the box returns true. If the user clicks "Cancel", the box returns false.

A prompt box is often used if you want the user to input a value before entering a page.

When a prompt box pops up, the user will have to click either "OK" or "Cancel" to proceed after entering an input value.

If the user clicks "OK" the box returns the input value. If the user clicks "Cancel" the box returns null.

## Electron
For desktop UI.

## Libraries

1. D3

2. jQuery

3. AJAX relationship between jQuery? seems that jQuery can make AJAX calls

4. plotly, phantomjs

angularJS

## Visulization
1. Google Visualization APIs


[Underscore](http://underscorejs.org/)
is a JavaScript library that provides a whole mess of useful functional programming helpers without extending any built-in objects. 
It's the answer to the question: 
"If I sit down in front of a blank HTML page, 
and want to start being productive immediately, 
what do I need?" ... and the tie to go along with jQuery's tux and Backbone's suspenders. 

## References

https://github.com/jashkenas/coffeescript/wiki/list-of-languages-that-compile-to-js
