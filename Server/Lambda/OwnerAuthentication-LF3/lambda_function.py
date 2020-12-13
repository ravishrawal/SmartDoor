import json
import otpMethods 
import sendSMS
import dbMethods


def lambda_handler(event, context):
    if event['approval_status']=='denied':
        dbMethods.delete_visitor(event['faceid'])
        
    elif event['approval_status']=='approved':
        visitor = {
            'faceid': event['faceid'],
            'phone_number': event['phone_number'],
            'visitor_name': event['visitor_name']
        }
        otpMethods.open_door(visitor)
        
        response = dbMethods.update_status(visitor)
        print('status response', response)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    


