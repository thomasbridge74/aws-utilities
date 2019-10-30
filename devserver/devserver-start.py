#!/usr/bin/python

# (c) Thomas Bridge 2017
 
# Licenced under GPL v2 or v3
# See https://www.gnu.org/ 

import boto3
import configparser
import sys
from time import sleep

verbose = 1
# First, get the server information.

try:
	Config = configparser.ConfigParser()
	Config.read("devserver.ini")
	ec2_instance_id = Config.get("Main", "devserver")
	region = Config.get("Main", "region")
	hostname = Config.get("Main", "hostname")
	zone = Config.get("Main", "hostedzone")
except:
	print("Cannot get required information")
	sys.exit()

fqdn = hostname + "." + zone

print("Server " + ec2_instance_id + " in region " + region + " has fqdn " + fqdn)

# Next, see if the server is running and if not, start it.

client = boto3.client('ec2')

response = client.describe_instance_status( InstanceIds = [ ec2_instance_id, ], IncludeAllInstances=True)
status = response[u'InstanceStatuses'][0][u'InstanceState'][u'Name']

if status == "stopped":
	if verbose >= 1:
		print("Starting instance now...")
	start_response = client.start_instances(InstanceIds = [ec2_instance_id, ])
	while client.describe_instance_status( InstanceIds = [ ec2_instance_id, ], IncludeAllInstances=True)[u'InstanceStatuses'][0][u'InstanceState'][u'Name'] != "running":
		if verbose >= 2:
			print("Waiting...")
		sleep(0.1)
elif status == "running":
	if verbose >= 1:
		print("Instance already running")
else:
	print("Status is " + status)
	print("Exiting")
	sys.exit()

server_info = client.describe_instances( InstanceIds = [ec2_instance_id, ])
public_ip_address = server_info[u'Reservations'][0][u'Instances'][0][u'PublicIpAddress']

print("Server has been started and has public IP " + public_ip_address)

# Now we need to update the DNS record

# First get the zone id for the zone
nsclient = boto3.client('route53')

zoneid = nsclient.list_hosted_zones_by_name(DNSName=zone)[u'HostedZones'][0][u'Id']

rr_set = [{"Action": "UPSERT", "ResourceRecordSet": {
    "Name": fqdn,
    "Type": "A",
    "TTL": 15,
    "ResourceRecords": [{"Value": public_ip_address}] }}]		

create_action = nsclient.change_resource_record_sets(HostedZoneId=zoneid, ChangeBatch={"Changes": rr_set })    



