#!/usr/bin/python3

import json
import time
import socket
import requests
import subprocess

def getcontroljson():
        get = requests.get("http://awebsite/control.json")
        jason = json.loads(get.text)
        return jason

def myvars():
        jayson = getcontroljson()
        for key in jayson.keys():
                if key == myhostname():
                        if isinstance(jayson[key], dict)== False:
                                for x in jayson[key]:
                                        jason = json.dumps(x)
                                        jout = json.loads(jason)
                                        myport = jout['port']
                                        myban = jout['banner']
                                        mycont = jout['continent']
        return myport, myban, mycont

def mycountries():
        countrycodes = []
        ccjson = requests.get("http://awebsite/cc.json")
        jason = json.loads(ccjson.text)
        for x in jason:
                if x['Continent_Name'] == myvars()[2]:
                        countrycodes.append(x['Two_Letter_Country_Code'] )
        return countrycodes

def subnetlookup(cc):
        #!!!!!!!!!!!!!!!!!!!!dockerize this and bring it internal later on!!!!!!!!!!!!!!!!!!!!!
        ranges = []
        cctoasnapi = "http://www.cc2asn.com/data/"
        cctoasnapiend = "_ipv4"
        cleanurl = cctoasnapi + str(cc).lower() + cctoasnapiend
        print(cleanurl)
        req = requests.get(cleanurl)
        for subnet in req.text.splitlines():
                ranges.append(subnet.replace("\n",""))
        time.sleep(1)
        return ranges

def mysubnets():
        for cc in mycountries():
                return subnetlookup(cc)

def myhostname():
        myhostname = str(socket.gethostname())
        return myhostname

def myztaddress():
        ztsubnet = "10.13.13"
        ips = []
        p = subprocess.Popen(["hostname", "-I"], stdout=subprocess.PIPE)
        term = p.stdout.read().decode('utf-8').replace("\n","chonker")
        out = term.split(" ")
        for x in out:
                if x.startswith(ztsubnet):
                        return x

def buildlvfile():
        file = open("/home/serviceaccountname/localvars.txt","w+")
        file.write(str(myvars())+"\n")
        file.write(str(myhostname())+"\n")
        file.write(str(myztaddress())+"\n")
        file.write(str(mycountries())+"\n")
        file.close()

def getranges():
        for x in mycountries():
                thisfilename = "/home/paramiko/countries/" + str(x).lower() + "-ranges.txt"
                file = open(thisfilename, "w+")
                chonk = subnetlookup(x)
                if len(str(chonk)) >= 7:
                        file.write('\n'.join(chonk))
                file.close()
