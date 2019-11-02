import os
import sys
import json
import base64
import boto3

with open(sys.argv[1]) as file:
    command = file.read()

payload = json.dumps(command)

client = boto3.client('lambda')
response = client.invoke(
    FunctionName='LAMBDA_ARN', # use your own lambda ARN here
    Payload=payload,
    LogType='Tail'
)

result = response['Payload'].read().decode('utf-8')
print(result)
