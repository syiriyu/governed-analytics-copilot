import numpy as np
import pandas as pd
from faker import Faker

from .config import N_ACCOUNT_MANAGERS, REGIONS, SEED


def generate_account_managers():
    fake = Faker("en_GB")
    Faker.seed(SEED)
    rng = np.random.default_rng(SEED)

    records = []

    for i in range(1, N_ACCOUNT_MANAGERS + 1):
        records.append({
            "account_manager_id": f"AM{i:03d}",
            "account_manager_name": fake.name(),
            "region": rng.choice(REGIONS),
            "team": f"Team {rng.integers(1, 13):02d}",
        })

    return pd.DataFrame(records)