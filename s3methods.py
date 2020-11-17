import logging
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal


def addToS3(photo, photo_name, bucket_name):
    #get s3 bucket
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    #upload to bucket
    try:
        response = bucket.upload_file(photo, f'{photo_name}.jpg')
    except ClientError as e:
        logging.error(e)
        return False
    print('successfully added to S3')
    return response