 # this is to give the fake company an operational/customer-experience dataset.
import numpy as np
import pandas as pd

from .config import SEED, START_DATE, END_DATE

 # we're only bringing in customers because the support cases are being modelled at the customer level, rather than for a specific product contract.
 # e.g. a customer could raise a support case related to their entire experience
def generate_support_cases(
    customers: pd.DataFrame,
 ) -> pd.DataFrame:

    rng = np.random.default_rng(SEED)

    support_records = []

    data_start_date = pd.Timestamp(START_DATE)
    data_end_date = pd.Timestamp(END_DATE)

    # assumption - larger customers tend to have more support demand
    annual_case_rates = {
        "Small Business": 1.5,
        "Mid-Market": 3.0,
        "Enterprise": 6.0,
    }

    priorities = [
        "P1",
        "P2",
        "P3",
        "P4",
    ]

    priority_probabilities = [
        0.05,
        0.15,
        0.45,
        0.35,
    ]

    sla_targets = {
        "P1": 4,
        "P2": 8,
        "P3": 24,
        "P4": 48,
    }

    case_types = [
        "Technical Issue",
        "Access Issue",
        "Billing Query",
        "Integration Issue",
        "Product Guidance",
    ]

    case_counter = 1

    for _, customer in customers.iterrows():

        active_days = (
            data_end_date - data_start_date
        ).days

        # 365.25 to approximately account for leap years
        active_years = active_days / 365.25

        # this is saying, for a given customer segment, give us the annual case rate
        annual_rate = annual_case_rates[
            customer["customer_segment"]
        ]

        expected_cases = annual_rate * active_years

        # poisson distribution is useful for generating counts of events over time, instead of being entirely random, it centres around an expected number of occurances
        number_of_cases = rng.poisson(
            expected_cases
    )

        # this is saying, repeat this block 4 times
        for _ in range(number_of_cases):
            for _ in range(4):
                random_days = int(
                    rng.integers(
                        0,
                        active_days + 1,
                    )
                )
                
                opened_date = (
                    data_start_date
                    + pd.Timedelta(days=random_days)
                )

                priority = rng.choice(
                    priorities,
                    p=priority_probabilities,
                )

                # so if priority target is a given priority, then retrive the SLA target
                sla_target = sla_targets[
                    priority
                ]

                # suppoer resolution should cluster around a sensible range, but occassionally have a long tail - hence the lognormal distribution
                resolution_multiplier = rng.lognormal(
                    mean=0,
                    sigma=0.55,
                )

                resolution_hours = round(
                    sla_target
                    * resolution_multiplier,
                    1,
                )

                sla_breached = (
                    resolution_hours > sla_target
                )

                base_satisfaction = 4.3

                
                # '-=' says take the instance of base_satisfaction and subtract 1.3
                if sla_breached:
                    base_satisfaction -= 1.3

                satisfaction_score = (
                    base_satisfaction
                    + rng.normal(
                        loc=0,
                        scale=0.5,
                    )
                )

                # constrain the score to be at minimum 5, and at most 1
                satisfaction_score = round(
                    min(
                        5,
                        max(
                            1,
                            satisfaction_score,
                        ),
                    ),
                    1,
                )

                case_type = rng.choice(
                    case_types
                )

                closed_date = (
                    opened_date
                    + pd.Timedelta(
                        hours=resolution_hours
                    )
                )

                support_records.append({
                "case_id": f"SC{case_counter:07d}",
                "customer_id": customer["customer_id"],
                "opened_date": opened_date,
                "closed_date": closed_date,
                "priority": priority,
                "case_type": case_type,
                "resolution_hours": resolution_hours,
                "sla_target_hours": sla_target,
                "sla_breached": sla_breached,
                "satisfaction_score": satisfaction_score,
            })

    return pd.DataFrame(support_records)

