UUID: 21443057-903b-44ae-b806-756ae32eeafc
Status: published
Date: 2016-06-20 22:21:15
Slug: ssh-copy-id
Author: Ben Chuanlong Du
Title: Copy SSH Public Key Using "ssh-copy-id"
Category: Linux
Tags: Linux, SSH, server, remote, port, ssh-copy-id

You can use the following command to copy your SSH public key to a Linux server.
```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub host_machine
```
However, 
if a Linux server runs the SSH deamon on a non default port (default is 22), 
you have to specify the port with option `-p port`. 
In addition, 
the host machine and the port options must be in quotes 
(either single or double quotes), 
otherwise, 
you will get an error message.
Suppose sshd runs on port 323 on `host_machine`, 
the following command copies the ssh public key to it. 
```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub "host_machine -p 323"
```
You can of course SSH into the server 
and add your SSH public key(s) into the `~/.ssh/authorized_keys` file manually.
