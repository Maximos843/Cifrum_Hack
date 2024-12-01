import pytest
import random
import numpy as np
import torch


@pytest.fixture(scope="session", autouse=True)
def set_seeds():
    seed = 1
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    yield
