```py
#!/usr/bin/python3

import boto3
import os
import subprocess as sp

def STOP_INSTANCES(REGION, TAG_KEY, TAG_VALUE):
    ec2 = boto3.client('ec2', region_name=REGION)
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:'+TAG_KEY,
                'Values': [TAG_VALUE]
            }
        ]
    )

    instancelist = []
    for reservation in (response["Reservations"]):
        for instance in reservation["Instances"]:
            if instance["State"]['Name'] == "running":
                instancelist.append(instance["InstanceId"])

    if instancelist != []:
        ec2.stop_instances(InstanceIds=instancelist)
    
    return instancelist




TARGET_SERVER = "google.com"
status,result = sp.getstatusoutput("ping -c1 -w2 " + TARGET_SERVER)

if status == 0: 
    print("System " + ip + " is UP !")
else:
    # three times iteration
    print("System " + ip + " is DOWN !")
    STOP_INSTANCES("us-east-1", "OWNER", "MAHESH")


```
