#!/usr/bin/python3

import sys
import paramiko

usernm = 'c00luser'
passwd = 'KewlPassWordThatISNTREAL'
hostslist = ['10.13.13.10','10.13.13.20','10.13.13.30','10.13.13.40','10.13.13.50']

def connect(host,cmd):
        cleancmd = "hostname && echo \"---\" && " + cmd + "\n"
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=420, username=usernm, password=passwd)
        stdin, stdout, stderr = client.exec_command(cleancmd)
        for line in stdout.readlines():
                print(line.replace("\n",""))
        print('\n')
        client.close()


#main starts here
thiscmd = sys.argv[1]
for x in hostslist:
        connect(x,thiscmd)
