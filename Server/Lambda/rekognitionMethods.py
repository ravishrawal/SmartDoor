import boto3

def add_faces_to_collection(bucket,photo_name,collection_id):
    
    client=boto3.client('rekognition')
    
    response=client.index_faces(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket,'Name':photo_name}},
                                ExternalImageId=photo_name,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])

    print ('Results for ' + photo_name)  
    print('Faces indexed:')
    faceidArr = []
    for faceRecord in response['FaceRecords']:
        
         print('  Face ID: ' + faceRecord['Face']['FaceId'])
         faceidArr.append(faceRecord['Face']['FaceId'])
         print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
            
    return faceidArr