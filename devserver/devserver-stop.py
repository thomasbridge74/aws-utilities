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

# Now, lets see about stopping the server.

client = boto3.client('ec2')

status = client.describe_instance_status( InstanceIds = [ ec2_instance_id, ], IncludeAllInstances=True)[u'InstanceStatuses'][0][u'InstanceState'][u'Name']

if status == "running":
	if verbose >= 1:
		print("We need to stop the server")
	client.stop_instances(InstanceIds = [ ec2_instance_id, ])
	print("Attempting to stop instance.   Status is " +
		  client.describe_instance_status( InstanceIds = [ ec2_instance_id, ], IncludeAllInstances=True)[u'InstanceStatuses'][0][u'InstanceState'][u'Name'])
else:
	print("Status is " + status)
	print("Nothing to do here")
	sys.exit()
