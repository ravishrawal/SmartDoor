import json
from dbMethods import *

def lambda_handler(event, context):
    #get faceid from event
    faceid = event['faceid']
    #get unexpired passcode from db
    db_passcode = getValidPasscode(faceid)
    print(event)
    
    #compare event passcode with db passcode
    event_passcode = event['passcode']
    
    #return success, wrong passcode, or expired passcode.
    passcode_validation = False
    if db_passcode: 
        if int(event_passcode) == int(db_passcode):
            print('passcodes match!')
            passcode_validation = True
    visitor_name = getVisitor(faceid)
    
    return {
        'statusCode': 200,
        'body': {
                'passcode_validation': passcode_validation,
                'visitor_name': visitor_name
            }
    }

