import boto3
import json
import time
import requests
import urllib.request

ec2client = boto3.client('ec2')
ec2 = boto3.resource('ec2')

def runInstance():
    print('Create instance')
    instance = ec2client.run_instances(
        ImageId='ami-011fb52991425d8d8', 
        InstanceType='t2.micro',
        MaxCount=1, 
        MinCount=1,
        SecurityGroupIds=[
            'sg-0df908cef6dc9f063'
        ])
    return instance

def checkState(instance):
    print('Check State')
    instanceId = instance['Instances'][0]['InstanceId']
    
    check_flag = True

    while check_flag:
        try:
            instance_details = ec2.Instance(instanceId)
            if instance_details.state['Name'] == 'running':
                check_flag = False
                print(instance_details.state['Name'])
            
            #print(instance_details.state['Name'])
            time.sleep(1)
        except:
            pass

def checkSC(instance):
    instanceId = instance['Instances'][0]['InstanceId']
    instance_details = ec2.Instance(instanceId)

    print('Security groups')
    print(instance_details.security_groups)

def connectAndDownload(instance):
    instanceId = instance['Instances'][0]['InstanceId']
    instance_details = ec2.Instance(instanceId)

    instance_url = 'http://' + instance_details.public_ip_address

    print('Send request')

    check_flag = True

    while check_flag:
        try:
            r = requests.get(instance_url)
            print(r)
            check_flag = False
        except:
            #'Timeout exceeded'
            pass


    opener = urllib.request.FancyURLopener({})
    with opener.open(instance_url) as f:
        content = f.read()
        with open("page.html", "wb") as f1:
            f1.write(content)

def stopAndTerminate(instance):
    instanceId = instance['Instances'][0]['InstanceId']
    ec2.instances.filter(InstanceIds=[instanceId]).stop()
    ec2.instances.filter(InstanceIds=[instanceId]).terminate()

if __name__ == '__main__':
    start = time.time()
    
    instance = runInstance()
    checkState(instance)
    end = time.time()
    checkSC(instance)
    connectAndDownload(instance)
    stopAndTerminate(instance)

    print('Instance start time: ' + str(end - start) + 's')