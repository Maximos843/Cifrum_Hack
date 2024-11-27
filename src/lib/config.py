import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    S3_ENDPOINT: str = "https://storage.yandexcloud.net"
    S3_ACCESS_KEY_ID: str = os.getenv(
        "S3_ACCESS_KEY_ID", "default"
    )  # will fail during bentoml build without defaul value
    S3_SECRET_ACCESS_KEY: str = os.getenv("S3_SECRET_ACCESS_KEY", "default")
    S3_BUCKET_NAME: str = ""
    S3_REGION: str = "ru-central1"
    S3_CLASSIFIER_DIR_TEMPLATE: str = "classifier/"

    BASE_UUID: str = ""

    PROJECT_NAME: str = "Classifier"

    LOCAL_MODEL_DIR: str = ""


settings = Settings()