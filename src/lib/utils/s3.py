import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError, BotoCoreError

from src.lib.utils.config import Consts


def get_s3_client() -> BaseClient | None:
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=Consts.ACCESS_KEY_ID,
            aws_secret_access_key=Consts.SECRET_KEY_ID,
            endpoint_url=Consts.ENDPOINT_URL
        )
        return s3_client
    except BotoCoreError as e:
        print(f"BotoCoreError occurred in get_s3_client: {e}")
        return None


def handle_s3_errors(func):
    """Decorator to handle S3 errors."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "NoSuchBucket":
                print("Bucket does not exist.")
            elif error_code == "AccessDenied":
                print("Access denied to the bucket.")
            else:
                print(f"ClientError occurred: {e}")
        except BotoCoreError as e:
            print(Consts.ACCESS_KEY_ID, Consts.SECRET_KEY_ID)
            print(f"BotoCoreError occurred: {e}")
        return None

    return wrapper


@handle_s3_errors
def get_model_weights() -> bytes | None:
    s3_client = get_s3_client()
    response = s3_client.get_object(Bucket=Consts.BUCKET_NAME, Key=Consts.MODEL_KEY)
    model_bytes = response['Body'].read()
    return model_bytes
