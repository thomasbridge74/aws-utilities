# Route 53 test zone setup

These scripts help set up a test zone for experimenting in Route 53.   

## Why would I want these scripts?

Thess can be useful when wanting to play around
with the Route53 service - and in particular are written in mind to avoid getting charged.   (Amazon charge 50c for each hostzone per
month, but this is not pro rata.   However, they do not charge for zones that exist for less than 12 hours, so if you're
just experimenting, you can do so without incurring a charge).

These scripts are useful for creating a private (not public) hosted zone.   I'm not entirely sure it would be useful for
the scripts to have a public zone option.    Because they are private zones, you need to associate the zone with a VPC.

## setup

You need to have configured (in ~/.aws/) a setup with an access key/secret pair with authorisation to make changes in your Route53
structure.    Python will use the boto3 library.    It is possible that this can work on an AWS EC2 instance with the appropriate role
attached, but I've not tried that.

This is developed on a Mac.   I expect it will work on Linux with no changes, but this has not been tried.

## What's in this directory?

There are four files.

### route53.ini

route53.ini has three sections

1. setup - just one entry required here - vpc representing the VPC ID of the VPC you're associating the zone with.
2. main - settings that are general to the zone - including the zone name itself and the region setting.   (If not defined, the 
script will attempt to get the default region instead).
3. rrset1 - has just a single RR record to add to the zone (eg if you want to add a dns server to the zone).   The 1 is appended
as I may then expand the script to allow multiple DNS records to be created at setup time.

### route53-setup-test-zone.py

This sets up the domain in AWS, including with the RR record defined in the ini file.

### route53-delete-test-zone.py

This deletes the zone.   First, it needs to delete any RRs defined within the zone, and then the zone itself.   (The script uses
a function that only returns a maximum of 100 RRs - I'm assuming that a test zone won't have more than 100 RRs but if your zone does,
this won't work.

### route53-list-zone.py

A very simple script that lists all the zones in your route53 account.

