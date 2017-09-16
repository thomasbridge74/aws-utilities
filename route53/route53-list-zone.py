#!/usr/bin/python

# (c) Thomas Bridge 2017
# Issued under the GPL.

# This script does very little - it just lists the zones and the associated ID.

import boto3  

connection = boto3.client('route53')

response = connection.list_hosted_zones()

for hosted_zone in response.get("HostedZones"):
	print hosted_zone.get("Name") + " has ID " + hosted_zone.get("Id")

		