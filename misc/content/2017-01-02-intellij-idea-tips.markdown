Status: published
Date: 2019-12-01 17:15:04
Author: Ben Chuanlong Du
Slug: intellij-idea-tips
Title: IntelliJ IDEA Tips
Category: Software
Tags: software, IDE, IntelliJ IDEA, tips

**
Things on this page are
fragmentary and immature notes/thoughts of the author.
It is not meant to readers
but rather for convenient reference of the author and future improvement.
**

## Installation in Ubuntu 

https://itsfoss.com/install-intellij-ubuntu-linux/

You can use ubuntu-make to install IntelliJ IDEA in Docker.



1. The first scala project might very long time to generate the directories
    depending on your network speed.
    SBT needs to download some JARs and when the download is complete,
    it will generate the `src` directory.
    It suggests that you work in environment with good network connection
    when using IntelliJ.


2. sbt (rather than Maven) is required if you want to use Scala worksheet in IntelliJ IDEA.
    You might see the following error if Maven is use.

        scalac error: bad option: '-make:transitive' on mvn package via command line

As a matter of fact,
sbt is recommended over Maven for developing Scala,
generally speaking.
First,
sbt is better supported in IntelliJ IDEA.
The Maven archetype for Scala is too old in IntelliJ.
You have to update the file pom.xml immediately after you create a Maven based Scala project in IntelliJ IDEA.

## Install Plugins from Command-line

https://stackoverflow.com/questions/24044513/intellij-idea-install-plugins-from-command-line

## Tricks & Traps 

1. Close your project and quit IntelliJ IDEA.

2. Rename the project directory to match the name of your project if they don't match.

3. Restart IntelliJ.

4. Go to the menu `File -> Invalidate Caches/Restart -> Invalidate and Restart`.


## General Tips

1. Close IntelliJ IDEA if you don't use it.
    First, 
    this save memory and make your machine run faster.
    Second, 
    this helps avoiding some tricky issues that happens when IntelliJ IDEA runs for a long time 
    (especially on Mac where people typically don't quit applications and don't restart for a long time).
    Some of the tricky issues can be resolved simplify by restarting IntelliJ IDEA,
    so closing IntelliJ IDEA if you don't use it helps preventing these tricky issues from happening.

2. If you encounter some tricky issues in IntellIJ IDEA that doesn't seem to be caused by coding errors,
    you can first restart IntelliJ IDEA, 
    and then do a clean build to see whether the issue is resolved.

## Scala Project Using Maven in IntelliJ

https://www.ivankrizsan.se/2016/03/27/creating-a-scala-project-with-maven-dependency-management-for-gatling-testing-in-intellij-idea/



## Reload Dependencies

https://stackoverflow.com/questions/20413605/how-to-force-intellij-idea-to-reload-dependencies-from-build-sbt-after-they-chan

## Rename Project

https://stackoverflow.com/questions/21177495/renaming-a-project-in-intellij-idea

## Use ScalaTest

http://www.scalatest.org/user_guide/using_scalatest_with_intellij

https://stackoverflow.com/questions/21353128/running-individual-scalatest-test-methods-in-intellij-idea

## Issues & Solutions


I just had this issue, also. It turned out that IntelliJ hadn't marked my src/main/scala folder as a "source" folder.

To do this: Project Structure -> Modules -> right click folder and Mark as "Source" (blue)

Similarly the src/main/test folder wasn't marked as a test folder. I was able to add scala classes after those folders were appropriately marked.



https://stackoverflow.com/questions/5905896/intellij-inspection-gives-cannot-resolve-symbol-but-still-compiles-code



First of all you should try File | Invalidate Caches and if it doesn't help, delete IDEA system directory. Then re-import the Maven project and see if it helps.

In some weird cases compiled classes may report wrong info and confuse IDEA. Verify that the classes from this jar report correct names using javap.


## Questions

1. how to port intellij configuration files from one machine to another one?

2. how to pop up auto completion suggestions while typing?


## References 

https://stackoverflow.com/questions/39282282/class-not-found-empty-test-suite-in-intellij/40400136
