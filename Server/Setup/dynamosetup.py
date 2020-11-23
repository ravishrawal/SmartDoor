# RUN this script to delete & create Passcodes & Visitors table

import boto3
from botocore.exceptions import ClientError

#start session on AWS account

dev = boto3.session.Session(profile_name='viren_aws_access')

#get dynamodb resource

dynamo = dev.resource('dynamodb')

#DROP table IF exists
table = dynamo.Table('Passcodes')

try:
	response = table.delete()
	print('great success\n', response)
except ClientError as e:
	print('table does not exist\n\n', e.response['Error']['Message'])

#DROP table IF exists
table = dynamo.Table('Visitors')

try:
	response = table.delete()
	print('great success\n', response)
except ClientError as e:
	print('table does not exist\n\n', e.response['Error']['Message'])

#create passcodes table
#TTL attribute with a timeout of 5 minutes

AttributeDefinitions = [
	{
		'AttributeName': 'visitor_name',
		'AttributeType': 'S',
	},
]

KeySchema = [
	{
		'AttributeName': 'visitor_name',
		'KeyType': 'HASH',
	},
]

ProvisionedThroughput = {
	'ReadCapacityUnits':10,
	'WriteCapacityUnits': 10,
}

create_table_response = dynamo.create_table(
	AttributeDefinitions=AttributeDefinitions,
	KeySchema=KeySchema,
	ProvisionedThroughput=ProvisionedThroughput,
	TableName='Passcodes')

#create visitors table
# photos is list type object format 
		
AttributeDefinitions = [
	{
		'AttributeName': 'faceid',
		'AttributeType': 'S',
	}, 
]

KeySchema = [
	{
		'AttributeName': 'faceid',
		'KeyType': 'HASH',
	},
]

ProvisionedThroughput = {
	'ReadCapacityUnits':10,
	'WriteCapacityUnits': 10,
}

create_table_response = dynamo.create_table(
	AttributeDefinitions=AttributeDefinitions,
	KeySchema=KeySchema,
	ProvisionedThroughput=ProvisionedThroughput,
	TableName='Visitors')
print(create_table_response)
