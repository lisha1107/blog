UUID: c9c53a46-c8ca-4b4c-a5fd-b40f76478ead
Status: published
Date: 2018-04-30 18:17:41
Author: Ben Chuanlong Du
Slug: package-management-in-linux
Title: Package Management in Linux
Category: Linux
Tags: Linux, package management, wajig, apt-get, dpkg

**
Things on this page are
fragmentary and immature notes/thoughts of the author.
It is not meant to readers
but rather for convenient reference of the author and future improvement.
**

1. apt-get
2. wajig (my favourite Debian/Ubuntu package management command)
3. Software Center (A fancy GUI for managing packages on Ubuntu/Debian)
4. Software Management (Linux Mint)

## Debian 

wajig apt-get, dpkg,


use alien or rpm to install rpm packages, wajig install alien; sudo alien -i *.rpm
```
dpkg -S $(which free)
```
Apt-get有问题时可以试试dpkg,
apt-get worries about dependencies but dpkg not,
so then dependency is broken,
you can use dpkg to install/remove packages

$ aptitude why libpng12-0

apt-mark manual

## [Nix](https://nixos.org/nix/)

sounds interesting

## RedHat

https://www.digitalocean.com/community/tutorials/package-management-basics-apt-yum-dnf-pkg

https://pkgs.org/
