"""
Your module description
"""
import boto3
import sys
sys.path.insert(1, '/opt')
import cv2

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

def save_img_to_tmp(stream_tmp_file,photo_tmp_file):
	print('in save img to tmp')
	#save stream to file
	num_chunks = 100
	with open(stream_tmp_file, 'wb') as f:
		# write payload to file
		bytestream = get_byte_stream_from_kvs()
		chunks = bytestream.iter_chunks(chunk_size=1024)
		count = 1
		for chunk in chunks:
			if count>=num_chunks: 
				break
			f.write(chunk)
			count+=1
	
	# capture frame	from video (stream) file
	with open(stream_tmp_file, 'rb') as f:
		f.seek(0)
		print('file contents', f.read())
		# extract photo
		cap = cv2.VideoCapture(stream_tmp_file)
		success, photo = cap.read()
		print(f"succesfully caputred image from stream {success}")
		if success:
			cv2.imwrite(photo_tmp_file, photo)
		return success, photo
