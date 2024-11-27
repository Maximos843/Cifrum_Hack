import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError, BotoCoreError
from config import settings


def get_s3_client() -> BaseClient | None:
    try:
        s3_session = boto3.Session(
            aws_access_key_id=settings.S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
            region_name=settings.S3_REGION,
        )
        s3_client = s3_session.client("s3", endpoint_url=settings.S3_ENDPOINT)
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
            print(f"BotoCoreError occurred: {e}")
        return None

    return wrapper