import boto3
import logging 


def send_message(phone, message):
    # Initialize logger and set log level
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Initialize SNS client for us east 1 region
    session = boto3.Session(region_name="us-east-1")
    sns_client = session.client('sns')

    if phone[0]=='+' and len(phone)==12:
        num = phone
    else:
        num = '+1'+ phone
    
    print(num,message)
    
    # Send message
    response = sns_client.publish(
        PhoneNumber=num,
        Message= message,
        MessageAttributes={
            'AWS.SNS.SMS.SenderID': {
                'DataType': 'String',
                'StringValue': 'SENDERID'
            },
            'AWS.SNS.SMS.SMSType': {
                'DataType': 'String',
                'StringValue': 'Promotional'
            }
        }
    )

    logger.info(response)
    print("message sent")  
