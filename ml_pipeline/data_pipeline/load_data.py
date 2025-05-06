import boto3
from botocore.client import Config
from data_pipeline.config import ACCESS_KEY, SECRET_KEY, ENDPOINT_URL, BUCKET_NAME, REGION_NAME
from io import BytesIO

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name=REGION_NAME
    )

def list_audio_files(s3_client):
    """
    Lists all .flac audio files in the bucket.
    """
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    contents = response.get("Contents", [])
    return [obj["Key"] for obj in contents if obj["Key"].endswith(".flac")]

def fetch_audio_stream(s3_client, key: str) -> BytesIO:
    """
    Fetches an audio file from R2 as an in-memory BytesIO stream.

    Args:
        key (str): The object key in the bucket.

    Returns:
        BytesIO stream of the file contents.
    """
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
    return BytesIO(response["Body"].read())