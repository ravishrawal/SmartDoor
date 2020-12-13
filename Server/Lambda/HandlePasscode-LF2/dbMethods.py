import logging
import boto3
from botocore.exceptions import ClientError
import time
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr
import random

def createPasscode(faceid):
    #create 5 digit passcode
    passcode = round(10000+89999*random.random())
    expiry_time = int(time.time())+360
    db = boto3.resource('dynamodb')
    passcodes_table = db.Table('Passcodes')

    #expiry time = 2 minutes (in seconds)
    new_passcode = {
                'faceid': faceid,
                'passcode':  passcode,
                'expiry_time': expiry_time
            }

    try:    
        response = passcodes_table.put_item(Item=new_passcode)
        print('successfully updated passcode in db')
    
    except ClientError as e:
        print("Error: ", e)
        logging.error(e)
        return False

    return new_passcode

def getValidPasscode(faceid):
    db = boto3.resource('dynamodb')
    passcodes_table = db.Table('Passcodes')
    response = passcodes_table.scan( FilterExpression= Attr('faceid').eq(faceid) & Attr('expiry_time').gt(int(time.time())) )
    passcode = None
    
    if response["Items"]: 
        passcode = response['Items'][0]['passcode']
        
    return passcode
    
def getVisitor(faceid):
    db = boto3.resource('dynamodb')
    visitors_table = db.Table('Visitors')
    response = visitors_table.scan(FilterExpression=Attr('faceid').eq(faceid))
    visitor_name = 'Invalid User'
    if response['Items']: visitor_name = response['Items'][0]['visitor_name']
    return visitor_name
