UUID: 775a72d6-f67a-4003-951f-b90be1dea2f8
Status: published
Date: 2017-10-22 12:32:25
Author: Ben Chuanlong Du
Slug: install-gnu-utils-using-macports
Title: Install GNU Utils Using MacPorts
Category: OS
Tags: Mac, Mac OSX, MacPorts

**
Things on this page are
fragmentary and immature notes/thoughts of the author.
It is not meant to readers
but rather for convenient reference of the author and future improvement.
**

## Configuration
Run the following command after installation.
```
export PATH=/opt/local/libexec/gnubin：/opt/local/bin:/opt/local/sbin:$PATH
export MANPATH=/opt/local/share/man:$MANPATH
```

## Installation
```
sudo port install file
sudo port install coreutils
```

## Issues

1. had issues to sync ports in office, not sure this is due to network issue or firewall in office
    rsync: failed to connect to rsync.macports.org: No route to host (65)
    exit code 10

