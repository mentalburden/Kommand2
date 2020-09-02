#!/usr/bin/python3

import sys
import paramiko

usernm = 'root'
iplist = 'workerlist'
privatekey = '/root/paramiko/testkey2'
hostslist = []
handleprikey = paramiko.ecdsakey.ECDSAKey(filename=privatekey)

def connect(host,cmd):
        cleancmd = "hostname && echo \"---\" && " + cmd + "\n"
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=usernm, pkey=handleprikey)
        stdin, stdout, stderr = client.exec_command(cleancmd)
        for line in stdout.readlines():
                print(line.replace("\n",""))
                print('\n')
        client.close()


#main starts here
thiscmd = sys.argv[1]
with open(iplist, 'r+') as hostsfile:
        for row in hostsfile:
                hostslist.append(row.rstrip('\n'))
print(hostslist)

for x in hostslist:
        connect(x,thiscmd)
