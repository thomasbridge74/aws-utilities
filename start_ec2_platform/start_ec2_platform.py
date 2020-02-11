#!/usr/bin/env python

import sys
import boto3
import argparse
from pprint import pprint

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--role", help="Rolename in configuration")
    parser.add_argument("-p", "--platform", help="Platform value in tag", default="Linux")
    parser.add_argument("-a", "--action", help="start|stop|status", default="status")
    parser.add_argument("-t", "--tag", help="Tag Name (defaults to Platform)", default="Platform")
    return(parser)

# if defined(role)
def main():
    args = createParser().parse_args()
    platform = args.platform
    role = args.role
    action = args.action
    tag = args.tag
    print("Action is " + action)
    if action not in ['start', 'stop', 'status']:
        print("Invalid action")
        sys.exit()

    try:
        if role:
            ec2 = boto3.Session(profile_name=role).client('ec2')
        else:
            ec2 = boto3.Session().client('ec2')
        filter = [{'Name': 'tag:' + tag, 'Values': [platform]}]
        instances = ec2.describe_instances(Filters=filter)
    except Exception as e:
        print("Error: ", e)
        sys.exit()

    if instances['ResponseMetadata']['HTTPStatusCode'] == 200:
        for x in instances['Reservations']:
            inst_id = x['Instances'][0]['InstanceId']
            state = x['Instances'][0]['State']
            if action == "status":
                print(inst_id, state)
            elif action == "stop":
                # Stop if running else warn and do nothing.
                if state['Code'] == 16:
                    print("Stopping instance ", inst_id)
                    ec2.stop_instances(InstanceIds=[inst_id])
                else:
                    print(inst_id, " has status ", state['Name'], " doing nothing")
            elif action == "start":
                if state['Code'] == 80:
                    print("Starting instance ", inst_id)
                    ec2.start_instances(InstanceIds=[inst_id])
                else:
                    print(inst_id, " has status ", state['Name'], " doing nothing")
    else:
        print("HTTP Response not correct")
# pprint(instances)

if __name__ == '__main__':
    main()
