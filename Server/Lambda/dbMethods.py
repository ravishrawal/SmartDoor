import logging
import boto3
from botocore.exceptions import ClientError
import time
from decimal import Decimal
from s3methods import *
import random
from boto3.dynamodb.conditions import Attr


def createOrUpdateUser(faceid, name, phone_number, photo):

    #get dynamodb
    db = boto3.resource('dynamodb')
    visitors_table = db.Table('Visitors')
    
    #format photo for dynamodb
    bucket_name = 'rav-viren-face-recognition'
    photo_name = name + str(time.time())    
    new_photo = {
            'objectKey':photo_name, 
            'bucket': bucket_name, 
            'createdTimestamp': str(time.time()),
        }

    #upload photo to S3
    addToS3(photo, photo_name, bucket_name)
    
    
    response = db.get_item( TableName='Visitors', Key={ 'faceid': { 'S': faceid, } }, AttributesToGet=['name', 'faceid', 'photos'],)
    user = response['Item']
    
    #check if user exists
    if user:
        #if so, add photo to user array
        response = updateUser(user, photo)
    else:
        #if not, create user
        new_visitor = {
                'faceid': faceid,
                'name':  name,  
                'phone_number': phone_number,
                'photos': [new_photo]
            }

        #add to dynamoDB table
        try:
            response = visitors_table.put_item(Item=new_visitor)
            print('successfully updated visitor in db')
        except ClientError as e:
            logging.error(e)
            return False
        
    return response


def updateUser(user, photo):
    db = boto3.client('dynamodb')
    visitors_table = db.Table('Visitors')
    
    #add photo to array
    photosArr = user['photos'].append(photo)
    
    #update user
    try:
        response = visitors_table.update_item(
            Key={
                'faceid': user['faceid'],
            },
            UpdateExpression="set photos=:photos",
            ExpressionAttributeValues={
                ':photos': photosArr
            },
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        logging.error(e)
        return False
        
    return response


def createPasscode(visitor_name, faceid=None):
    #create 5 digit passcode
    passcode = round(10000+89999*random.random())
    db = boto3.client('dynamodb')
    passcodes_table = db.Table('Passcodes')

    #expiry time = 2 minutes (in seconds)
    new_passcode = {
                'visitor_name': visitor_name,
                'passcode':  passcode,
                'expiry_time': int(time.time())+120
            }

    try:    
        response = passcodes_table.put_item(Item=new_passcode)
        print('successfully updated passcode in db')
    except ClientError as e:
        logging.error(e)
        return False

    return response

def getValidPasscode(visitor_name, faceid=None):
    db = boto3.client('dynamodb')
    passcodes_table = db.Table('Passcodes')

    response = passcodes_table.scan( FilterExpression= Attr('visitor_name').eq(visitor_name) & Attr('expiry_time').gt(int(time.time())) )
    return response['Items']['passcode']


