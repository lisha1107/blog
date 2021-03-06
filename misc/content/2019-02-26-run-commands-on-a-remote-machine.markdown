Status: published
Date: 2019-06-26 18:39:12
Author: Benjamin Du
Slug: run-commands-on-a-remote-machine
Title: Run Commands on a Remote Machine
Category: Programming
Tags: programming, Shell, Python, SSH

**
Things on this page are fragmentary and immature notes/thoughts of the author.
It is not meant to readers but rather for convenient reference of the author and future improvement.
**

## SSH

1. The pipeline command is run locally.
    If you want the pipeline command to run remotely, 
    place the whole command to be run remotely in double/single quotes.
    For example, 
    the command below SSH into into a Hadoop client through a proxy configured by proxychains,
    prints the content of a text file and then count the number of lines in the file.

        proxychains ssh client_ip /apache/hadoop/bin/hdfs dfs -cat adset_id/adset_id_642.txt | wc -l

    The `wc -l` command is run locally instead of running on the Hadoop client.
    Since proxychains prints out some information too, 
    the `wc -l` will over count the number of lines in the text file.
    The correct way is count the number of lines on the Hadoop client instead of counting locally.
    A simple way is to place the whole command to be run on the Hadoop client in double/singls quotes.
    Below is an illustration.

        proxychains ssh client_ip '/apache/hadoop/bin/hdfs dfs -cat adset_id/adset_id_642.txt | wc -l'

https://stackoverflow.com/questions/305035/how-to-use-ssh-to-run-a-shell-script-on-a-remote-machine

## Python

### [paramiko/paramiko](https://github.com/paramiko/paramiko)
[paramiko/paramiko](https://github.com/paramiko/paramiko)
is a pure Python implementation of SSHv2. 
It is a great tool to interact with a remote server in Python.

### [parallel-ssh](https://github.com/ParallelSSH/parallel-ssh)

### [asyncssh](https://github.com/ronf/asyncssh)

### [fabric](https://github.com/fabric/fabric/)

### [ssh2-python](https://github.com/ParallelSSH/ssh2-python)

### [sshtunnel](https://github.com/pahaz/sshtunnel)


## References 

http://vozis.blogspot.com/2015/01/python-sftp-with-paramiko-via-socks.html

https://medium.com/@RyanHiebert/sftp-via-socks-proxy-using-paramiko-a736afe17b9e

https://adimian.com/blog/2014/10/paramiko-and-corporate-proxies

https://github.com/Anorov/PySocks

https://github.com/paramiko/paramiko/pull/508

https://gist.github.com/rubanm/5818236

https://medium.com/@keagileageek/paramiko-how-to-ssh-and-file-transfers-with-python-75766179de73

https://stackoverflow.com/questions/10488832/how-to-ssh-over-http-proxy-in-python/33767220

https://stackoverflow.com/questions/28411960/execute-a-command-on-remote-machine-in-python

https://python-for-system-administrators.readthedocs.io/en/latest/ssh.html
