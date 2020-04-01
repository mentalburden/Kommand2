#!/usr/bin/python3

import os, sys
import socket
import subprocess

targetports = ['22','25','80','443','4567']
cntlsubnet = "10.13."
cntl = "10.13.13.1"
uwst = "10.13.13.10"
uest = "10.13.13.20"
euro = "10.13.13.30"
afra = "10.13.13.40"
asia = "10.13.13.50"

def masscan(port):
        #os.system(masscan stuff here with port)
        print(port)

def get_zt_address():
        ips = []
        p = subprocess.Popen(["hostname", "-I"], stdout=subprocess.PIPE)
        term = p.stdout.read().decode('utf-8').replace("\n","chonker")
        out = term.split(" ")
        for x in out:
                if x.startswith(cntlsubnet):
                        return x

myname = socket.gethostname()

myztaddress = get_zt_address()
if get_zt_address() == cntl:
        print("i can haz cntrl")
elif get_zt_address() == uwst:
        masscan(targetports[0])
elif get_zt_address() == uest:
        masscan(targetports[1])
elif get_zt_address() == asia:
        masscan(targetports[2])
elif get_zt_address() == afra:
        masscan(targetports[3])
elif get_zt_address() == euro:
        masscan(targetports[4])
