# allow-my-ip.py

This is a script to automate the process of adding your IP to a security group so you can directly 
ssh to EC2 instances in AWS.

When setting up an EC2 instance, it is not uncommon to allow ssh from a remote location.   Even if you do not do it
for all hosts, but just to a single bastion host, you ideally do not want to leave the bastion host open to all IP addresses.
On the other hand, if you are moving around a lot or using a domestic broadband connection you cannot always plan the IP 
address you will be connecting from.    This script can be used from the CLI to determine your current public IP address
and add it to the security-group.    It was developed on a MacBook but I imagine it can be easily used on a Linux system 
as well.

To use this script effectively you need to do the following:

1. Ensure the boto3 package is installed.
2. Run "aws configure" with an access key pair that has permission to modify the security-group
3. Edit allow-my-ip.ini and enter the name of the security-group and optionally the region.    If there is no region defined, the
script will use the default region defined under the aws configure command.    If there is no default region, then the script
will simply exit.

## Note

This is a useful utility that has worked well for me on my MacBook.   I am putting it out here as I hope it may be useful
for others.  It's the first time I've released python code for that purpose onto Github, so I'm naturally a little nervous!
