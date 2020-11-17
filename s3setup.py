#Setup S3 bucket programmatically

import boto3

#start session on viren's AWS account

dev = boto3.session.Session(profile_name='viren_aws_access')

s3 = dev.resource('s3')

response = s3.create_bucket(Bucket = 'rav-viren-face-recognition')

for bucket in s3.buckets.all():
	print(bucket.name)



