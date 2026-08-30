# This is going to be used for churn modelling

import pandas as pd

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