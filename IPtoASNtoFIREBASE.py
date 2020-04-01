#!/usr/bin/python3

#for each json in quad0 masscan output, do asn lookup at wrangler:9996, ship json to firestore

import re, os, sys, requests, json, time
import shodan
import pprint
import socket
import dns.resolver

filepath = '/home/SUPERcoolUSER123/quad0out.json'
#api = shodan.Shodan("aSuperCoolAPIkey")
#testarray = []
vpsname = 'uswest'
telephone = {"no-info-for-host":"---none---"}
service = 'https://womblechonks-fake-firebase-db.firebaseio.com'
asnapi = 'http://your-ip-to-asn-docker:666/v1/as/ip/'

def asnlookup(address):
        myurl = asnapi + str(address)
        chonker = requests.get(myurl)
        jason = json.loads(chonker.text)
        anounced = str(jason['announced'])
        if anounced == "True":
                country = str(jason['as_country_code'])
                asndesc = str(jason['as_description']).replace(',',' ').replace("-"," ").replace(':',' ')
                asnnum = str(jason['as_number'])
                asnjson = {"ccod":country,"asnd":asndesc,"asnn":asnnum}
                return asnjson
        else:
                failjson = {'noasn':'noasn'}
                return failjson

def gofirebase(ip):
        octs = ip.split('.')
        #cleandata = {'a': str(octs[0]), 'b': str(octs[1]), 'c': str(octs[2]), 'd': str(octs[3]) ,'asni':json }
        cleandata = json.dumps(asnlookup(ip))
        myurl = service+"/"+vpsname+"/"+octs[0]+"/"+octs[1]+"/"+octs[2]+"/"+octs[3]+"/asn.json"
        print(str(myurl) + " ----- " + str(cleandata))
        chonker = requests.patch(myurl, data=cleandata)
        print(chonker.text)


#main starts here
with open(filepath) as fp:
        line = fp.readline()
        while line:
                ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)
                print(ip)
                try:
                        gofirebase(ip[0])
                except:
                        print("nope")
                line = fp.readline()
