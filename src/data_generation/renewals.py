# This is going to be used for churn modelling

import pandas as pd
import numpy as np

from .config import SEED

def build_renewal_features(
    contracts: pd.DataFrame,
    product_usage: pd.DataFrame,
    support_cases: pd.DataFrame,
) -> pd.DataFrame:

    # we're only considering contracts eligible for review (so like SELECT * from contracts WHERE eligibility = TRUE)
    eligible_contracts = contracts[
        contracts["renewal_eligible"] == True
    ].copy()


    # this is just taking product usage and ordering it chronlogically
    sorted_usage = product_usage.sort_values(
        ["contract_id", "month"]
    )


    # this is essentially taking a summed count of active users using the first value for active users in a given month, then do the same for last value
    # reset index converts contract_id into a new column, as groupby can often turn the grouped column into the DF's index
    usage_summary = (
        sorted_usage
        .groupby("contract_id")
        .agg(
            first_active_users=("active_users", "first"),
            last_active_users=("active_users", "last"),
        )
        .reset_index()
    )

    # this calc is to workout the % change of active users from first to last month

    usage_summary["usage_change_pct"] = (
        (
            usage_summary["last_active_users"]
            - usage_summary["first_active_users"]
        )
        / usage_summary["first_active_users"]
    )


    # we're selecting one to one validation because we expect one eligible contract row is = to one usage summary row. So one summary row per contract
    renewal_features = eligible_contracts.merge(
        usage_summary,
        on="contract_id",
        how="left",
        validate="one_to_one",
    )

    
    # we use a many-to-many join here temporarily
    support_contracts = support_cases.merge(
        eligible_contracts[
            [
                "contract_id",
                "customer_id",
                "contract_start_date",
                "contract_end_date",
            ]
        ],
        on="customer_id",
        how="inner",
        validate="many_to_many"
    )

   # this is to essentially say where opened_date is between contract start date and contract end date. '&' syntax is the same as AND in pandas and | is the same as OR
    support_contracts = support_contracts[
        (
            support_contracts["opened_date"]
            >= support_contracts["contract_start_date"]
        )
        &
        (
            support_contracts["opened_date"]
            <= support_contracts["contract_end_date"]
        )
    ]

    # note, we can still calculate the avg on booleans because they are output as 1 or 0
    support_summary = (
        support_contracts
        .groupby("contract_id")
        .agg(
            support_case_count=(
                "case_id",
                "count",
            ),
            sla_breach_rate=(
                "sla_breached",
                "mean",
            ),
            average_satisfaction=(
                "satisfaction_score",
                "mean",
            ),
            average_resolution_hours=(
                "resolution_hours",
                "mean",
            ),
        )
        .reset_index()
    )

    renewal_features = renewal_features.merge(
        support_summary,
        on="contract_id",
        how="left",
        validate="one_to_one",
    )

    # some contracts may have no support cases, so we need to account for this, so we're basically performing COALESCE(case_count, 0)

    renewal_features[
        "support_case_count"
    ] = renewal_features[
        "support_case_count"
    ].fillna(0)

    return renewal_features

# this is a helper function that says, given a customer's usage trend, how much should we adjust churn probability?
def calculate_usage_adjustment(
    usage_change_pct,
):
    if pd.isna(usage_change_pct): # if the usage is not available, we're not going to penalise or reward the customer
        return 0

    if usage_change_pct <= -0.30:
        return 0.08

    elif usage_change_pct <= -0.10:
        return 0.04

    elif usage_change_pct >= 0.20:
        return -0.02

    else:
        return 0

# same as above but for SLAs
def calculate_sla_adjustment(
    sla_breach_rate,
):

    if pd.isna(sla_breach_rate):
        return 0

    if sla_breach_rate > 0.50:
        return 0.06

    elif sla_breach_rate > 0.25:
        return 0.03

    else:
        return 0

# same as above but for satisfaction information
def calculate_satisfaction_adjustment(
    average_satisfaction,
):

    if pd.isna(average_satisfaction):
        return 0

    if average_satisfaction < 3.0:
        return 0.06

    elif average_satisfaction < 3.5:
        return 0.03

    elif average_satisfaction >= 4.3:
        return -0.02

    else:
        return 0

def generate_renewal_outcomes(
    renewal_features: pd.DataFrame,
    customers: pd.DataFrame,
) -> pd.DataFrame:

    rng = np.random.default_rng(SEED)

    renewal_outcomes = renewal_features.copy()

    customer_risk = customers[
        [
            "customer_id",
            "customer_segment",
            "baseline_churn_probability",
        ]
    ]

    renewal_outcomes = renewal_outcomes.merge(
        customer_risk,
        on="customer_id",
        how="left",
        validate="many_to_one",
    )

    renewal_outcomes[
        "usage_risk_adjustment"
    ] = renewal_outcomes[
        "usage_change_pct"
    ].apply( # apply takes the function and applies it to every value in this column
        calculate_usage_adjustment
    )

    renewal_outcomes[
        "sla_risk_adjustment"
    ] = renewal_outcomes[
        "sla_breach_rate"
    ].apply(
        calculate_sla_adjustment
    )

    renewal_outcomes[
        "satisfaction_risk_adjustment"
    ] = renewal_outcomes[
        "average_satisfaction"
    ].apply(
        calculate_satisfaction_adjustment
    )

    # this takes all of our adjusted churn figures and applies our % changes to reveal the final churn probability. #example: enterprise baseline 5% -> usage grew 25% -2% churn -> low SLA breach rate 0% change -> satisfaction = 4.5 -2% churn -> final probability = 1%
    renewal_outcomes[
        "churn_probability"
    ] = (
        renewal_outcomes[
            "baseline_churn_probability"
        ]
        + renewal_outcomes[
            "usage_risk_adjustment"
        ]
        + renewal_outcomes[
            "sla_risk_adjustment"
        ]
        + renewal_outcomes[
            "satisfaction_risk_adjustment"
        ]
    )

    renewal_outcomes[
        "churn_probability"
    ] = renewal_outcomes[
        "churn_probability"
    ].clip( # clip constrains values in a range
        lower=0.01,
        upper=0.80
    )

    renewal_outcomes[
        "random_draw"
    ] = rng.random( # generates numbers between 0 and 1
        len(renewal_outcomes)
    )

    renewal_outcomes[
        "churned"
    ] = (
        renewal_outcomes["random_draw"]
        <
        renewal_outcomes["churn_probability"]
    )

    renewal_outcomes[
        "renewed"
    ] = ~renewal_outcomes[ # tilde means Boolean NOT.. so churned = True and renewed = False
        "churned"
    ]

    return renewal_outcomes