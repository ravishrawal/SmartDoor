from dbMethods import *
from s3methods import *
from rekognitionMethods import *
import base64
import json
import boto3
import sys
sys.path.insert(1, '/opt')
import cv2



def lambda_handler(event,context):

    # decode data
    isFace, faceid, imgid = parseEvent(event)
    # print(isFace, faceid, imgid)
    photo = 'NO FACE DETECTED'
  
    if isFace:
        #create file

        f = open('/tmp/bytestream12', 'ab')
        # write payload to file
        bytestream = get_byte_stream_from_kvs()
        chunks = bytestream.iter_chunks(chunk_size=1024)
        count = 1
        for chunk in chunks:
            if count>=100: break
            f.write(chunk)
            count+=1
        
        f = open('/tmp/bytestream12', 'rb')
        f.seek(0)
        # print('file contents', f.read())
        
        #extract photo
        cap = cv2.VideoCapture('/tmp/bytestream12')
        success, photo = cap.read()
        print(success)
        if success:
            bucket_name = 'rav-viren-face-recognition'
            cv2.imwrite('/tmp/img.jpg', photo)
            response = addToS3('/tmp/img.jpg', 'test323', bucket_name)
            print('S3 Response:', response)
        f.close()
        
        #if face not in collection, add face to collection ONLY IF APPROVED
        # if not faceid:
        #   bucket = 'rav-viren-face-recognition'
        #   collection_id = 'faceCollection'
        #   faceid = add_faces_to_collection(bucket, photo, collection_id)[0]

    
    return {
    'statusCode': 200,
    'body': ''
    }


def parseEvent(ev):
    data_raw = ev['Records'][0]['kinesis']['data']
    data_str = base64.b64decode(data_raw).decode('ASCII')
    data = json.loads(data_str)
    
    isFace = data['FaceSearchResponse']
    faceid = None
    imgid = None
    
    if isFace:
        faceMatch = data['FaceSearchResponse'][0]['MatchedFaces']
        if faceMatch:
            print('faceMatch', faceMatch)
            faceid = faceMatch[0]['Face']['FaceId']
            imgid = faceMatch[0]['Face']['ImageId']
    
    return isFace, faceid, imgid
  
def get_byte_stream_from_kvs():
    kvs = boto3.client('kinesisvideo', region_name='us-east-1')
    kvs_response = kvs.get_data_endpoint(
        StreamARN='arn:aws:kinesisvideo:us-east-1:961394851336:stream/face_recognition/1604277868692',
        APIName='GET_MEDIA',
        )
    video_client = boto3.client('kinesis-video-media', endpoint_url=kvs_response['DataEndpoint'], region_name='us-east-1')
    video_response = video_client.get_media(
        StreamARN='arn:aws:kinesisvideo:us-east-1:961394851336:stream/face_recognition/1604277868692',
        StartSelector={'StartSelectorType':'NOW'}
        )
        
    return video_response['Payload']
  

