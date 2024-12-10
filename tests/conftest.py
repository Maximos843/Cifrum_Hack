from src.lib.model.model import model
from src.app import app
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import torch
import numpy as np
import random
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))


DatabaseClient_instance = MagicMock()
DatabaseClient_instance.select_with_condition_query.return_value = None
DatabaseClient_instance.insert_query.return_value = None

model.predict = MagicMock(return_value=(["test"], ("positive", 0.9)))

get_db_client_patch = patch(
    'api.get_db_client', return_value=DatabaseClient_instance)
get_db_client_patch.start()

client = TestClient(app)


def teardown_module():
    get_db_client_patch.stop()


@pytest.fixture(scope="session", autouse=True)
def set_seeds():
    seed = 1
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    yield
