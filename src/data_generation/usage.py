# this is to generate monthly product engagement for every active customer-product contract

# if revenue tells us what this customer is worth commercially speaking, usage tells us how engaged the customer is with the product

import numpy as np
import pandas as pd

from .config import SEED, END_DATE


# we're using two datasets this time because contracts has various IDs (customer, product, contract start date), but it doesn't know customer_segment or employee_count
def generate_product_usage(
    contracts: pd.DataFrame,
    customers: pd.DataFrame,
) -> pd.DataFrame:

    rng = np.random.default_rng(SEED)

    usage_records = []

    data_end_month = (
        pd.Timestamp(END_DATE)
        .to_period("M")
        .to_timestamp()
    )

    # now need to perform a join on both datasets

    contract_context = contracts.merge(
        customers[
            [
                "customer_id",
                "customer_segment",
                "employee_count",
            ]
        ],
        on="customer_id",
        how="left",
        validate="many_to_one"
    )

    adoption_rates = {
        "Small Business": 0.35,
        "Mid-Market": 0.22,
        "Enterprise": 0.12,
    }

    #these are assumptions about how frequently users might interact with the products i.e. Atlas core frequently used, while Atlas secure is lower frequency
    events_per_user = {
        "P001": 18,
        "P002": 10,
        "P003": 8,
        "P004": 15,
        "P005": 5,
        "P006": 3,
    }

    usage_patterns = [
        "stable",
        "growing",
        "declining"
    ]

# these need to add up to 100%
    usage_pattern_probabilities = [
        0.55,
        0.25,
        0.20,
    ]


# iterate through each row in the contract_context dataset
    for _, contract in contract_context.iterrows():
        
        # works like a CASE statement... says if the row is a given customer segment, return its associated adoption_rates number
        adoption_rate = adoption_rates[
            contract["customer_segment"]
        ]

        # we don't want it to return 0 active users, so we set max to be 1 - so pick whatever your calc is or at minimum the value 1
        base_active_users = max(
            1,
            round(
                contract["employee_count"]
                * adoption_rate
            ),
        )

        # this is to generate a usage pattern once per contract, so it gives us the idea of the trend over 12 months
        usage_pattern = rng.choice(
            usage_patterns,
            p=usage_pattern_probabilities,
        )

        start_month = (
            pd.Timestamp(contract["contract_start_date"])
            .to_period("M")
            .to_timestamp()
        )

        # starting from the contract's start month, generate 12 monthly dates
        contract_months = pd.date_range(
            start=start_month,
            periods=12,
            freq="MS",
        )

        contract_months = contract_months[
            contract_months <= data_end_month
        ]

        # enumerate turns the month name into the numerical representative value (so 0 = Jan)
        
        for month_number, month in enumerate(
            contract_months
        ):

            if usage_pattern == "growing":
                trend_multiplier = (
                    1 + (0.04 * month_number)
                )

            elif usage_pattern == "declining":
                trend_multiplier = max(
                    0.30,
                    1 - (0.07 * month_number),
                )

            else:
                trend_multiplier = 1

            noise = rng.normal(
                loc=1.0,
                scale=0.05,
            )

            
            # this combines company sizw * adoption rate * usage trend * monthly randomness
            active_users = max(
                1,
                round(
                    base_active_users
                    * trend_multiplier
                    * noise
                ),
            )

            product_intensity = events_per_user[
                contract["product_id"]
            ]

            usage_events = max(
                active_users,
                round(
                    active_users
                    * product_intensity
                    * rng.normal(
                        loc=1.0,
                        scale=0.08,
                    )
                ),
            )

            usage_records.append({
                    "month": month,
                    "contract_id": contract["contract_id"],
                    "customer_id": contract["customer_id"],
                    "product_id": contract["product_id"],
                    "active_users": active_users,
                    "usage_events": usage_events,
                })

    return pd.DataFrame(usage_records)



