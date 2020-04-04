#!/usr/bin/python3
#banner knocks every /24 for every .txt in your country range lists dir
#get global local info from hostname to change port and socket send data

from netaddr import IPNetwork
import asyncio
import socket
import glob
import sys
import os

countrydir = "/home/paramiko/countries/"
thisport = 80
targets = []
targetsubnets = []
grabtasks = []
grabdata = []
loop = asyncio.get_event_loop()

def cleandata(ip,input):
	cleaninput = input.splitlines()
	thisdata = {'ip':str(ip),'bannerlines':str(cleaninput)}
	return thisdata

async def grab(ip):
	global grabdata
	try:
		reader, writer = await asyncio.open_connection(str(ip),thisport)
		writer.write(b'GET / HTTP/1.1\n Banner grab test, dont mind me.\n\n')
		await writer.drain()
		chonk = await reader.read(4096)
#		thisdata = {'ip':ip,'banner':chonk}
#		grabdata.append(cleandata(ip,chonk))
		print(cleandata(ip,chonk))
	except:
		return

async def asyncloopmanager():
	for x in range(len(targets)):
		try:
			grabtasks[x] = loop.create_task(grab(targets[x]))
		except IndexError:
			pass
	await asyncio.sleep(0.5)

def handlesubnet(subnet):
	global targets
	mysubnet = IPNetwork(str(subnet))
	mysubnets = list(mysubnet.subnet(24))
	for sub in mysubnets:
		for ip in IPNetwork(str(sub)):
			targets.append(str(ip))
		print(targets)
		chonker = loop.run_until_complete(asyncloopmanager())
		targets = []

def handlefiles():
	for filename in glob.glob(os.path.join(countrydir, '*.txt')):
		with open(filename, 'r') as f:
			lines = f.readlines()
			for x in lines:
				if len(x) > 1:
					targetsubnets.append(str(x).replace("\n",""))

#main starts here
if __name__ == '__main__':
	handlefiles()
	for x in targetsubnets:
		handlesubnet(x)
