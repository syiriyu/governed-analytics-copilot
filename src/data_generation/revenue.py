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