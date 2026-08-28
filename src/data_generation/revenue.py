# we're looking to establish for each contract, the monthly revenue, the active months filtered by end of data, and then append revenue records

import pandas as pd
# no numpy this time because we're not randomly generating info - it's gonna be derived from our other data we've already generated

from .config import END_DATE

# create a function that receives our contracts DataFrame and returns another DataFrame containing monthly revenue
def generate_monthly_revenue(
    contracts: pd.DataFrame,
) -> pd.DataFrame:

    revenue_records = []

    # revenue grain is gonna be monthly, rather than daily hence to_period("M")
    data_end_month = (
        pd.Timestamp(END_DATE)
        .to_period("M")
        .to_timestamp()
    )

    for _, contract in contracts.iterrows():
        contract["contract_value"]
        contract["contract_start_date"]

        # works out the monthly revenue by dividing the annual contract figure by 12
        monthly_revenue = round(
            contract["contract_value"] / 12,
            2,
        )

        start_month = (
            pd.Timestamp(contract["contract_start_date"])
            .to_period("M")
            .to_timestamp()
        )

# ms = month start, so it anchors it to the start of the month, rather than a random date
        contract_months = pd.date_range(
            start=start_month,
            periods=12,
            freq="MS",
        )

# we shouldn't have future revenue, so we need this to only run til the end of our dataset
        contract_months = contract_months[
            contract_months <= data_end_month
        ]

        for month in contract_months:

            revenue_records.append({
                "month": month,
                "contract_id": contract["contract_id"],
                "recognised_revenue": monthly_revenue,
            })

    return pd.DataFrame(revenue_records)

