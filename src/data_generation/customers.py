import numpy as np
import pandas as pd
from faker import Faker

from .config import (
    CUSTOMER_SEGMENTS,
    INDUSTRIES,
    N_CUSTOMERS,
    REGIONS,
    SEED,
)


def generate_customers():
    fake = Faker("en_GB")
    Faker.seed(SEED)
    rng = np.random.default_rng(SEED)

    segments = rng.choice(
        CUSTOMER_SEGMENTS,
        size=N_CUSTOMERS,
        p=[0.55, 0.30, 0.15],
    )

    regions = rng.choice(
        REGIONS,
        size=N_CUSTOMERS,
        p=[0.45, 0.20, 0.15, 0.20],
    )

    industries = rng.choice(
        INDUSTRIES,
        size=N_CUSTOMERS,
    )

    records = []

    for i in range(N_CUSTOMERS):
        records.append({
            "customer_id": f"C{i + 1:05d}",
            "customer_name": fake.company(),
            "customer_segment": segments[i],
            "industry": industries[i],
            "region": regions[i],
        })

    return pd.DataFrame(records)