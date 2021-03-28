# Grace McNamara
# 28-Mar-2021

from typing import Dict, List

import boto3
from botocore.exceptions import ClientError

client = boto3.client('s3')


def lambda_handler(event: Dict[str, any], context):

    bucket_encryption_status = {"buckets": {}}
    if buckets_specified_in(event):
        bucket_encryption_status = get_specified_bucket_status(buckets=event["buckets"])
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


def buckets_specified_in(event: Dict[str, str]) -> bool:
    """
    Check if buckets key exists in event and has buckets specified.

    :param event: The event object to check for buckets on.
    :return: True if buckets key exists and has one or more bucket names specified, else False.
    """
    return 'buckets' in event and len(event['buckets']) > 0


def get_specified_bucket_status(buckets: List[str]) -> Dict[str, Dict[str, str]]:
    """
    Get status of passed in buckets.

    :param buckets: A list of buckets to get the status of.
    :return: A dictionary containing the bucket names and their encryption status.
    """
    bucket_encryption_status = {"buckets": {}}

    for bucket in buckets:
        bucket_name = bucket
        result = retrieve_encryption_status(bucket_name)
        bucket_encryption_status['buckets'][bucket_name] = result

    return bucket_encryption_status


def retrieve_encryption_status(bucket_name):
    try:
        client.get_bucket_encryption(Bucket=bucket_name)
        return ("Encrypted")
    except ClientError as e:
        if e.response.get('Error').get('Code') == 'ServerSideEncryptionConfigurationNotFoundError':
            return ("Not Encrypted")
