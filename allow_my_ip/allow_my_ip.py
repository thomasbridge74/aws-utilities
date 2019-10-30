#!/usr/bin/python

# (c) Thomas Bridge 2017
 
# Licenced under GPL v2 or v3
# See https://www.gnu.org/ 

import pycurl
import sys
import boto3
from botocore.exceptions import ClientError  
from io import BytesIO
import configparser

debug = True

try:
	Config = configparser.ConfigParser()
	Config.read("allow_my_ip.ini")
	sgid = Config.get("Main", "sgid")
except:
	print("Cannot find sgid in ini file")
	sys.exit()
	
try:
	region = Config.get("Main", "region")
except ConfigParser.NoOptionError:
	region = boto3.session.Session().region_name

if debug:
	print("Sgid is: " + sgid)

if not region:
	print("Cannot determine the region")
	sys.exit()
else:
	if debug:
		print("Region is: " + region)

ip = BytesIO()

try:
	c = pycurl.Curl()
	c.setopt(c.URL, 'http://checkip.amazonaws.com/')
	c.setopt(c.WRITEDATA, ip)
	c.perform()
	
	ipaddress = ip.getvalue().rstrip().decode() + "/32"
except:
	print("Couldn't get the local ip address")
	sys.exit()
	
security_group = boto3.resource('ec2', region_name=region).SecurityGroup(sgid)

try:
	response = security_group.authorize_ingress(IpProtocol = 'tcp', FromPort=22, ToPort=22, CidrIp=ipaddress)
	print("Added " + ipaddress + " to " + sgid)
except ClientError as ex:
	print("Couldn't add " + ipaddress + " to " + sgid)
	print("Error: " + ex.response["Error"]["Message"])
