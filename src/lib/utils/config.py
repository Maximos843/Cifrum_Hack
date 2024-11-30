import os
from dataclasses import dataclass


@dataclass
class Consts:
    id2label = {
        0: 'негативный',
        1: 'нейтральный',
        2: 'положительный'
    }
    ACCESS_KEY_ID = os.environ.get('ACCESS_KEY_ID')
    SECRET_KEY_ID = os.environ.get('SECRET_KEY_ID')
    ENDPOINT_URL = 'https://s3.gis-1.storage.selcloud.ru'
    BUCKET_NAME = 'grinatom-model'
    MODEL_KEY = '/model/bert_model_rubert_DeepPavlov.pkl'
