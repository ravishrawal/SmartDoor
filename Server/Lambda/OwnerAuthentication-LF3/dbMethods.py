"""
Your module description
"""
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import logging

def get_visitor(faceid):
	db_resource = boto3.resource('dynamodb')
	visitors_table = db_resource.Table('Visitors')
	response = visitors_table.scan(FilterExpression = Attr('faceid').eq(faceid))
	print("visitor response: ", response)
	visitor = response['Items']	
	return visitor

def update_status(visitor_in):
    faceid = visitor_in['faceid']
    approval_status = 'approved'
    visitor = get_visitor(faceid)
    if len(visitor)>0:
        visitor = visitor[0]
        db_resource = boto3.resource('dynamodb')
        visitors_table = db_resource.Table('Visitors')
        #update status
        try:
            response_as = visitors_table.update_item(
                Key={
                    'faceid': faceid,
                },
                UpdateExpression="set approval_status=:approval_status",
                ExpressionAttributeValues={
                    ':approval_status': approval_status
                },
                ReturnValues="UPDATED_NEW"
            )
            
            response_ph = visitors_table.update_item(
                Key={
                    'faceid': faceid,
                },
                UpdateExpression="set phone_number=:phone_number",
                ExpressionAttributeValues={
                    ':phone_number': visitor_in['phone_number']
                },
                ReturnValues="UPDATED_NEW"
            )
            
            response_na = visitors_table.update_item(
                Key={
                    'faceid': faceid,
                },
                UpdateExpression="set visitor_name=:visitor_name",
                ExpressionAttributeValues={
                    ':visitor_name': visitor_in['visitor_name']
                },
                ReturnValues="UPDATED_NEW"
            )
            
        except ClientError as e:
            logging.error(e)
            return False
        return [response_as, response_ph, response_na]

def delete_visitor(faceid):
    db_resource = boto3.resource('dynamodb')
    visitors_table = db_resource.Table('Visitors')
    visitors = get_visitor(faceid)
    if len(visitors)>0:
        visitor = visitors[0]
        #delete
        try:
            db_response = visitors_table.delete_item(Key={'faceid': faceid})
            print('deleted:', db_response)
        
            s3 = boto3.resource('s3')
            for item in visitor['photos']:
                s3_response = s3.Object(item['bucket'], item['objectKey']).delete()
            
            rek = boto3.client('rekognition')
            collectionId = 'faceCollection'
            rek_response = rek.delete_faces(CollectionId=collectionId,FaceIds=[faceid])
            
            print("RESPONSES:", db_response,s3_response,rek_response)
    
        except ClientError as e:
            logging.error(e)
            print('couldnt delete item from db,s3, or rekognition')
            return False
        return True
        
       
    
    
            
    
        
   
