import boto3
from botocore.client import Config
from io import BytesIO
from .config import ACCESS_KEY, SECRET_KEY, ENDPOINT_URL, BUCKET_NAME, REGION_NAME

def get_s3_client():
    '''
    Read data from s3 based on creds and create a client.
    '''
    return boto3.client(
        's3',
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name=REGION_NAME
    )

def list_audio_files(s3_client):
    '''
    Get all the audio files from the bucket and get the content of each audio file which ends with flac. 
    '''
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    return [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(".flac")]

def fetch_audio_stream(s3_client, key):
    '''
    The audio files are response objects and we need their bodies, so use the get object and io streaming to get the response body. 
    '''
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
    return BytesIO(response['Body'].read())
