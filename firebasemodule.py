#!/usr/bin/python3

import re, os, sys, requests, json, time
import shodan
import pprint
import socket
from datetime import datetime

sys.path.append('/home/serviceaccountname/')
import mblocalvarsmodule as mblocal

filepath = '/home/serviceaccountname/quad0out.json'
projectname = "noway"
#api = shodan.Shodan("SueperCoolNeAtAPIkey111")
telephone = {"no-info-for-host":"---none---"}
service = 'https://nope.firebaseio.com'
asnapi = 'http://yeahright:666/v1/as/ip/'

def store(ip,prt,ban,asn,geo,data):

        now = datetime.now()
        mytime = now.strftime("%d/%m/%Y, %H:%M:%S")
        if ban == None:
                ban = "script error"
        if asn == None:
                asn = "script error"
        if geo == None:
                geo = "script error"
        if data == None:
                data = "script error"
        octs = ip.split('.')
        thisdata = {"liveports": {str(prt):str(mytime)},"banners":{str(prt):str(ban)},"xtradata":str(data),"asninfo":str(asn),"geoinfo":str(geo),"scannedon":{str(mblocal.myhostname()):str(mytime)}}
        cleandata = json.dumps(thisdata)
        myurl = service+"/"+projectname+"/"+octs[0]+"/"+octs[1]+"/"+octs[2]+"/"+octs[3]+"/hostdata.json"
        chonker = requests.patch(myurl, data=cleandata)
