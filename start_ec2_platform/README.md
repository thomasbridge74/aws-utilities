# start_ec2_platform

This is a very simple script to start all the EC2 instances in a specific account based on
how they are tagged.   The script requires that the AWS Python module (boto3) is installed.

## Usage

The script can either start, stop or do a status report on all instances matching the tags.
By default, it does a status report - the decision to start or stop can be made by using
the ```-a``` tag.      Before attempting to start or stop an instance, the script
does sanity check the current status of each instance and reports what it does for
each instance.

### Details
```
usage: start_ec2_platform.py [-h] [-r ROLE] [-p PLATFORM] [-a ACTION] [-t TAG]

optional arguments:
  -h, --help            show this help message and exit
  -r ROLE, --role ROLE  Rolename in configuration
  -p PLATFORM, --platform PLATFORM
                        Platform value in tag
  -a ACTION, --action ACTION
                        start|stop|status
  -t TAG, --tag TAG     Tag Name (defaults to Platform)

```

As written, no AWS credentials are either hardcoded into the script or supplied on the CLI.  
This means the script relies on the AWS Configuration typically stored in ```~/.aws/config```
and ```~/.aws/credentials``` files.    I wrote this in an environment where I had to switch
IAM roles after logging in.    The script as written may prompt for a MFA code if
that's required to login/switch roles.
 
## Setting up the AWS files.

Create an Access Key for accessing your account.    Then run ```aws configure``` to set up the 
default files.     If you need to switch roles, update the files so they look like the below:

### ```~/.aws/config```
```
[default]
region = <region>
output = json

[profile rolename]
region = <region>
```

### ```~/.aws/credentials```

```
[default]
aws_access_key_id = <ACCESS KEY ID>
aws_secret_access_key = <ACCESS KEY SECRET>

[devvpc]
source_profile = default
# This line is required if you use MFA authentication
mfa_serial = arn:aws:iam::<masteraccountid>:mfa/<masteraccountusername>
role_arn = arn:aws:iam::<roleaccountid>:role/<roleaccountname>
```

# Hints on running

## Behind corporate proxy
If you're in an environment (such as a corporate network) where your HTTP connections
are transparently intercepted by the proxy server, you may get an SSL verification error.
One work around I've found is to explicitly set the HTTP_PROXY and HTTPS_PROXY environment
variable.

## Running on Windows in Git Bash
As mentioned above, the script may prompt for a token as part of the authentication 
process to AWS.   For this to work in Git Bash on Windows, the script should be run
through the `winpty` command:

```buildoutcfg
winpty py -3 ./start_ec2_platform.py <arguments>
```
