"""
Your module description
"""
import boto3
from boto3.dynamodb.conditions import Key, Attr
import random
import logging 
import time
from sendSMS import *

def createPasscode(faceid):
    #create 5 digit passcode
    passcode = round(10000+89999*random.random())
    expiry_time = int(time.time())+300
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
    response = passcodes_table.scan( FilterExpression= Attr('faceid').eq(faceid) & Attr('expiry_time').gt(int(time.time())))
    return response['Items']['passcode']
    

def open_door(visitor):
	phone = visitor['phone_number']
	name = visitor['visitor_name']
	faceid = visitor['faceid']
	new_passcode = createPasscode(faceid)
	url = f'http://smartdoorfrontend.s3-website-us-east-1.amazonaws.com/passcode?faceid={faceid}'
	message = f"Your OTP for SmartDoor is {new_passcode['passcode']}.\nIt expires in 5 minutes.\nVisit {url} to validate it."
	print(f"message: {message}")
	send_message(phone,message)
