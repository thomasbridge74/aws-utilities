#!/usr/bin/python

# (c) Thomas Bridge 2017
# Issued under the GPL.

import boto3  
import configparser
import sys

debug = False

try:
	Config = configparser.ConfigParser()
	Config.read("route53.ini")
	domainname = Config.get("main", "domainname") + "."
except:
	print("Cannot get setup settings")
	sys.exit()
	
zoneid = ""

client = boto3.client('route53')

response = client.list_hosted_zones()

for hosted_zone in response.get("HostedZones"):
	if debug:
		print(hosted_zone.get("Name"))
	if hosted_zone.get("Name") == domainname:
		zoneid = hosted_zone.get("Id")

if zoneid == "":
	print("Couldn't find zoneid for " + domainname)
	sys.exit()
	
if debug:		
	print("zone id for", domainname, "is", zoneid)
	print("First, we delete all the resource records")

# This is a small subdomain where we don't expect the limitation of 100 records being
# returned in the script as an issue

zone = client.list_resource_record_sets(HostedZoneId = zoneid)

delete_records = []
    
for rr_set in zone.get("ResourceRecordSets"):
	if (rr_set.get("Name") != domainname) or ((rr_set.get("Type") != "NS") and (rr_set.get("Type") != "SOA")):
		delete_records.append({"Action": "DELETE", "ResourceRecordSet": rr_set})
		if debug:
			print(rr_set)
			
delete_action = client.change_resource_record_sets(HostedZoneId=zoneid, ChangeBatch={"Changes": delete_records })	
				
if debug:
	print("Attempting to delete")

delete_response = client.delete_hosted_zone(Id = zoneid)

if delete_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
	print("Domain " + domainname + " successfully deleted")
else:
	print("An unknown error occured deleting the domain " + domainname)
	print("Make sure it's deleted in the console")
	
		
		