# Grace McNamara
# 28-Mar-2021

from typing import Dict

import boto3
from botocore.exceptions import ClientError

client = boto3.client('s3')


def lambda_handler(event: Dict[str, str], context):
    """

    :param event:
    :param context:
    :return:
    """
    bucket_encryption_status = {"buckets": {}}
    if 'buckets' in event and len(event['buckets']) > 0:
        for bucket in event['buckets']:
            bucket_name = bucket
            result = retrieve_encryption_status(bucket_name)
            bucket_encryption_status['buckets'][bucket_name] = result
    else:
        buckets = client.list_buckets()
        print(buckets)
        print(buckets)
        for bucket in buckets['Buckets']:
            result = retrieve_encryption_status(bucket['Name'])
            bucket_encryption_status['buckets'][bucket['Name']] = result
    return {
        'statusCode': 200,
        'body': bucket_encryption_status
    }


def buckets_specified(event: Dict[str, str]) -> bool:
    """
    Check if buckets key exists in event and has buckets specified.

    :param event: The event object to check for buckets on.
    :return: True if buckets key exists and has one or more bucket names specified, else False.
    """
    return 'buckets' in event and len(event['buckets']) > 0

def retrieve_encryption_status(bucket_name):
    try:
        client.get_bucket_encryption(Bucket=bucket_name)
        return ("Encrypted")
    except ClientError as e:
        if e.response.get('Error').get('Code') == 'ServerSideEncryptionConfigurationNotFoundError':
            return ("Not Encrypted")
