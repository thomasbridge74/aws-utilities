# Devserver Start up

These scripts help manage a development server where the intention isn't to keep the server on 24x7.    It essentially does two 
things:

1. Start the server up.
2. Update the DNS entry in Route 53 with the public IP address.

## Why would I want these scripts?

This script assumes you're already created the development server.   It helps keep costs down by only letting the server run 
when you need it to.   The DNS update allows you to use a hostname - which is particularly useful if the IP addresses change as
your browser will use the hostname history to access the server.   This avoids the costs that would come with using an Elastic IP 
- either you need to keep the server on or you get charged for reserving an Elastic IP when the associated instance isn't running.

The DNS TTL is set to 15 seconds - this is currently hardcoded.


## setup

You need to have configured (in ~/.aws/) a setup with an access key/secret pair with authorisation to make changes in your Route53
structure.    Python will use the boto3 library.    It is possible that this can work on an AWS EC2 instance with the appropriate role
attached, but I've not tried that.

This is developed on a Mac.   I expect it will work on Linux with no changes, but this has not been tried.

## What's in this directory?

There are two files.

### devserver.ini

devserver.ini has just a main section.   The settings here are

1. EC2 ID
2. Region (the AWS region hosting the EC2 instance)
3. The hostname.
4. The name of the hosted zone the server should be in.


### devserver-start.py

This script checks to see if the server is running, and if it isn't, starts it up.   Once the server is running, the public IP address of the
server is obtained and then used to update the zone in route 53.

