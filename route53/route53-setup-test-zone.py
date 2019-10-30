#!/usr/bin/python

# (c) Thomas Bridge 2017
# Issued under the GPL.

import boto3
import configparser
import sys
import time

#from botocore.errorfactory import InvalidVPCId  

debug = False

try:
	Config = configparser.ConfigParser()
	Config.read("route53.ini")
	vpcid = Config.get("setup", "vpcid")
	domainname = Config.get("main", "domainname")
except:
	print("Cannot get setup settings")
	sys.exit()

try:
	region = Config.get("main", "region")
except ConfigParser.NoOptionError:
	region = boto3.session.Session().region_name

if not region:
	print("Cannot determine the region")
	sys.exit()
else:
	if debug:
		print("Region is: " + region)
		
client = boto3.client('route53')
call_ref = str(int(time.time()))

try:
	response = client.create_hosted_zone(Name = domainname, CallerReference=call_ref, VPC={'VPCRegion': region, 'VPCId': vpcid}, HostedZoneConfig = {'PrivateZone': True})
except Exception as ex:
	print("Couldn't create zone " + domainname + " in VPC " + vpcid + " (region is: " + region + ")")
	print("Error: " + ex.response["Error"]["Message"])
	sys.exit()
		
rr_name = Config.get("rrset1", "name") + '.' + domainname
rr_type = Config.get("rrset1", "type")
rr_ttl = int(Config.get("rrset1", "ttl"))
rr_value = Config.get("rrset1", "value")
	
zoneid = response.get("HostedZone").get("Id")

rr_set = [{"Action": "CREATE", "ResourceRecordSet": {
    "Name": rr_name,
    "Type": rr_type,
    "TTL": rr_ttl,
    "ResourceRecords": [{"Value": rr_value}] }}]		
    
create_action = client.change_resource_record_sets(HostedZoneId=zoneid, ChangeBatch={"Changes": rr_set })    
	

