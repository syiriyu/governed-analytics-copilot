import numpy as np
import pandas as pd
from faker import Faker # this is used to generate realistic-looking fake information

from .config import N_ACCOUNT_MANAGERS, REGIONS, SEED


def generate_account_managers():
    fake = Faker("en_GB") # generate british style fake data
    Faker.seed(SEED)
    rng = np.random.default_rng(SEED)

    records = [] # we define an empty list, because we are about to populate it with our for loop. The list will contain several dictionaries

    for i in range(1, N_ACCOUNT_MANAGERS + 1): # our range here is saying take the 1st record and then take the number of account managers and add 1 bcos python's range will exclude the true final number
        records.append({
            "account_manager_id": f"AM{i:03d}", # this says take the AM prefix, format it as an int because of 'd', make it 3 digits wide because of '3', and fill it with 0's.
            "account_manager_name": fake.name(),
            "region": rng.choice(REGIONS), # we're randomly selecting regions using our random number generator and our list of regions from the config file
            "team": f"Team {rng.integers(1, 13):02d}", # this gives the team prefix and then assigns a number between the range of 1 and 13. e.g. Team 03
        })

    return pd.DataFrame(records)