import boto3
import time
from botocore.exceptions import ClientError

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client('s3')

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print(e)

def read_file(object_name, bucket):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, object_name)
    body = obj.get()['Body'].read()

if __name__ == '__main__':
    start = time.time()
    #upload_file('LargeFile.zip', 'lsc-jj-bucket')
    read_file('LargeFile.zip', 'lsc-jj-bucket')
    end = time.time()
    print('Read time: ' + str(end - start) + 's')
