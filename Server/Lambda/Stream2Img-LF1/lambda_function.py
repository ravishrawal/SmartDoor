from dbMethods import *
from s3methods import *
from rekognitionMethods import *
from otpMethods import *
from sendSMS import *
from videoMethods import *
import base64
import json
import boto3

def lambda_handler(event,context):
	# decode data
	isFace, faceid, imgid = parseEvent(event)
	# print(isFace, faceid, imgid)
	photo = 'NO FACE DETECTED'
	if isFace:
			stream_tmp_file = '/tmp/bytestream12'
			photo_tmp_file = '/tmp/img.jpg'
			success,photo = save_img_to_tmp(stream_tmp_file,photo_tmp_file)
			 # rekogntion recognized face
			print("FACEID:", faceid)
			# print(event)
			visitor = get_visitor(faceid)
			if len(visitor)>0:
				print("RECOGONIZED: ")
				visitor = visitor[0]
				if visitor['approval_status'] == 'approved':
					print(f'opening door for {visitor}')
					createVisitorOrAddPhoto(photo_tmp_file, photo)
					open_door(visitor)
			else:
				# unknown face
				print('unknown face')
				faceid, visitor, photo_url  = createVisitorOrAddPhoto(photo_tmp_file, photo)
				if faceid:
					print('created visitor')
					if not recently_texted_user(faceid):
						authenticate_by_owner(faceid,photo_url)
						# handle response in different lambda function
					else: 
						print('recently texted user - will not text again')
				else:
					print('no faceid')
	else: 
		print('no face!')
	
	return {
	'statusCode': 200,
	'body': ''
	}


def parseEvent(ev):
	data_raw = ev['Records'][0]['kinesis']['data']
	data_str = base64.b64decode(data_raw).decode('ASCII')
	data = json.loads(data_str)
	confidenceThreshold = 99
	isFace = data['FaceSearchResponse']

	if isFace:
		faceConfidence = data['FaceSearchResponse'][0]['DetectedFace']['Confidence']
		print('face confidence: ', faceConfidence)
		if faceConfidence < confidenceThreshold: 
			return None, None, None 
	
	faceid = None
	imgid = None
	if isFace:
		faceMatch = data['FaceSearchResponse'][0]['MatchedFaces']
		if faceMatch:
			print('faceMatch', faceMatch)
			faceid = faceMatch[0]['Face']['FaceId']
			imgid = faceMatch[0]['Face']['ImageId']
	print('end parse event')
	return isFace, faceid, imgid
  

def authenticate_by_owner(faceid, photo_url):
	url = f'http://smartdoorfrontend.s3-website-us-east-1.amazonaws.com/visitors/new/?faceid={faceid}&photo_url={photo_url}'
	owner_phone = '4127374028'
	message = f'You have a visitor.\n Please authenticate by visiting {url}.'
	send_message(owner_phone,message)
	set_texted_user_time(faceid)
	
