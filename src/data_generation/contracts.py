# notebook structure goes: for customers, determine the product count, choose products, choose account manager, determine the billing type,  
# then for products: generate contract value and create contract


# Contracts is to represent the business relationship between customers, products, and account managers. Contracts can relate to revenue, usage, and renewals.
# One customer can have many contracts

import numpy as np
import pandas as pd

from .config import SEED, START_DATE, END_DATE

# this takes the three existing tables and returns a new contracts table
def generate_contracts(
    customers: pd.DataFrame,
    products: pd.DataFrame,
    account_managers: pd.DataFrame,
) -> pd.DataFrame:

    rng = np.random.default_rng(SEED)

    # converting the string date into timestamp data
    data_start_date = pd.Timestamp(START_DATE)
    data_end_date = pd.Timestamp(END_DATE)
    date_range_days = (data_end_date - data_start_date).days

    contracts = []

# underscores just make the number easier to read for humans, but it still represents the same number without the underscore.
    contract_value_ranges = {
        "Small Business": (5_000, 30_000),
        "Mid-Market": (25_000, 150_000),
        "Enterprise": (100_000, 750_000),
    }

    contract_counter = 1

# iterrows allows you to loop through one row at a time in a dataframe
    for _, customer in customers.iterrows():
        
        product_count = int(customer["expected_product_count"])

    # choose products for the customers & .sample() will randomly select rows from the product table.. replace false means they don't choose the same product twice
        selected_products = products.sample(
            n=product_count,
            replace=False,
            random_state=SEED + contract_counter,
        )

    # this ensures that account managers are based in the same region as the customer
        regional_managers = account_managers[
            account_managers["region"] == customer["region"]
        ]

    # sample with n=1 will return a one row dataframe, and .iloc[0] turns it into a single row that is easier for us to use
        account_manager = regional_managers.sample(
            n=1,
            random_state=SEED + contract_counter,
        ).iloc[0]

        billing_types = {
            "Small Business": "Monthly",
            "Mid-Market": "Monthly",
            "Enterprise": "Annual", 
        }

        # we're saying the billing type becomes the specified type from our above dictionary, based on the respective segment
        billing_type = billing_types[customer["customer_segment"]]

        # this is now a nested loop as we're saying... for each customer, choose products, and for each selected product, create a contract
        for _, product in selected_products.iterrows():
            low, high = contract_value_ranges[
                customer["customer_segment"]
            ]
            contract_value = rng.integers(low, high + 1)

            # rounds the contract value so it gives more natural looking commercial values
            contract_value = round(contract_value / 1000) * 1000

            random_days = int(
                rng.integers(0, date_range_days + 1)
            )

            # If timestamp represents a point in time, timedelta represents an amount of time - so we're deciding on how much after the data start data did the contract begin
            contract_start_date = (
                data_start_date + pd.Timedelta(days=random_days)
            )

            contract_end_date = (
                contract_start_date + pd.DateOffset(years=1)
            )

            renewal_eligible = contract_end_date <= data_end_date

            # we're using an f-string, in our case saying we want 6 digits, padding with zeroes
            contracts.append({
                "contract_id": f"CT{contract_counter:06d}",
                "customer_id": customer["customer_id"],
                "product_id": product["product_id"],
                "account_manager_id": account_manager["account_manager_id"],
                "contract_value": contract_value,
                "billing_type": billing_type,
                "contract_start_date": contract_start_date,
                "contract_end_date": contract_end_date,
                "renewal_eligible": renewal_eligible,
            })

        contract_counter += 1

    return pd.DataFrame(contracts)