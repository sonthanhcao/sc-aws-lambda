import json
import urllib.parse
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import csv
# from prettytable import PrettyTable
# from tabulate import tabulate
print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    # csv_file_name = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    # csv_object = s3_client.get_object(Bucket=bucket,Key=csv_file_name)
    try:
        local_file_name = '/tmp/report.csv'
        csv_object = s3.get_object(Bucket=bucket, Key=key)
        s3.download_file(bucket, key, local_file_name)



        client = boto3.client('sns')
        snsArn = 'arn:aws:sns:eu-central-1:226275233641:soncao-test-sns'

        with open(local_file_name,'r') as f, open('/tmp/report.txt', 'w') as w:
            next(f) # Skip first line
            rowReader = csv.reader(f, delimiter=',')

            for values in rowReader:
                TEXT = 'Instance %s( %s ) can be resized to %s | %s | %s estimated saving is %s$ | %s$ | %s$' % ( values[0], values[1], values[3], values[4], values[5], values[8], values[9], values[10] )
                w.writelines(TEXT + '\n')

        with open("/tmp/report.txt", "r") as txt_file:
            output = txt_file.read() # might need .readlines() or .read().splitlines(). Whatever works for you

        response = client.publish(
            TopicArn = snsArn,
            Message = output ,
            Subject='Hello This is recommendation report from AWS'
        )
        print("Send successfully")
        return output # csv_object['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
