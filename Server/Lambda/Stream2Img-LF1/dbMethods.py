import logging
import boto3
import time
from decimal import Decimal
from s3methods import *
from rekognitionMethods import *
from boto3.dynamodb.conditions import Key, Attr
import random

def get_visitor(faceid):
	db_resource = boto3.resource('dynamodb')
	visitors_table = db_resource.Table('Visitors')
	response = visitors_table.scan(FilterExpression = Attr('faceid').eq(faceid))
	print("visitor response: ", response)
	visitor = response['Items']	
	return visitor

def createVisitorOrAddPhoto(photo_tmp_file, photo):
    #get dynamodb
    db_client =  boto3.client('dynamodb')
    db_resource = boto3.resource('dynamodb')
    visitors_table = db_resource.Table('Visitors')
    
    #format photo for dynamodb
    name = photo_tmp_file.split('/')[-1][:-4] #extract file name without path or extension
    t = str(time.time())
    photo_name = name + t + '.jpg' 
    print(name, photo_name)
    new_photo = {
            'objectKey':photo_name, 
            'bucket': 'rav-viren-face-recognition', 
            'createdTimestamp': t,
        }

    #upload photo to S3
    s3_response = addToS3(photo_tmp_file, photo_name)
    photo_url = f"https://rav-viren-face-recognition.s3.amazonaws.com/{photo_name}"
    print('successfully added to S3. photo_url: ', photo_url)
    # index faces
    face_id_arr = add_faces_to_collection(photo_name)
    print('successfully added face to collection')
    print("face_id_arr: ", face_id_arr)
    #ASSUME only one face
    if face_id_arr:
        faceid = face_id_arr[0]
        response = visitors_table.scan(FilterExpression = Attr('faceid').eq(faceid))
        print('DB RESPONSE:', response)
        # check if visitor exists in dynamodb 
        visitor = response['Items']
        print('visitor: ', visitor)
        if len(visitor)==1:
            print("known visitor")
            # if so, add photo to user array
            response_add_photo = addPhoto(faceid, new_photo)
            print(f"response_add_photo: {response_add_photo}")
        else:
            #if not, create visitor
            print("unknown visitor")
            new_visitor = {
                    'faceid': faceid,
                    # 'name':  name,  
                    # 'phone_number': phone_number,
                    'photos': [new_photo],
                    'approval_status': 'pending',
                    'last_texted': ''
                }
                
            #add to dynamoDB table
            try:
                response_new_visitor = visitors_table.put_item(Item=new_visitor)
                print(f"response_new_visitor: {response_new_visitor}")
                print('successfully updated db')
            except ClientError as e:
                logging.error(e)
                print('failed to create visitor')
                return False 
        return faceid, visitor, photo_url
    else: 
        return None, None, None

def addPhoto(faceid, new_photo):
    db_resource = boto3.resource('dynamodb')
    visitors_table = db_resource.Table('Visitors')
    visitor = get_visitor(faceid)
    
    #add photo to array
    if len(visitor)>0:
        photosArr = visitor[0]['photos'].append(new_photo)
    
    #update user
    try:
        response = visitors_table.update_item(
            Key={
                'faceid': faceid,
            },
            UpdateExpression="set photos=:photos",
            ExpressionAttributeValues={
                ':photos': photosArr
            },
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        logging.error(e)
        print('failed to add photo to list in ')
        return False
        
    return response
    
def set_texted_user_time(faceid):
    print('setting texted time ...')
    db_resource = boto3.resource('dynamodb')
    visitors_table = db_resource.Table('Visitors')
    visitors_table.update_item(
            Key={
                'faceid': faceid,
            },
            UpdateExpression="set last_texted=:last_texted",
            ExpressionAttributeValues={
                ':last_texted': Decimal(time.time())
            },
            ReturnValues="UPDATED_NEW"
        )
    
def get_texted_user_time(faceid):
    db_resource = boto3.resource('dynamodb')
    visitors_table = db_resource.Table('Visitors')
    visitor = get_visitor(faceid)
    print('VISITOR INFO:', visitor)
    time_last_texted = visitor[0]['last_texted']
    return time_last_texted
    
def recently_texted_user(faceid):
    last_texted = get_texted_user_time(faceid)
    if not last_texted:
        return False
    elif (Decimal(time.time()) -  last_texted > 60):
        return False
    print('recently texted user')
    return True
