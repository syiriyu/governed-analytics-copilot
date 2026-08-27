import numpy as np
import pandas as pd

# retrieves seed from the config file we've got in our SRC folder (importance of the seed is to retain the same information, such as customers, so testing can be conducted reliably)
from .config import SEED

# def allows us to define a reusable function, so we can reuse add_customer_profiles if we call just that. It's also expecting the customers argument to be a dataframe.
# embed the random number generator inside the function
def add_customer_profiles(customers: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)

#
customers = customers.copy()


# create a tuple for each customer, so these can then our function can generate a random figure for each type
employee_ranges = {
    "Small Business": (10, 249),
    "Mid-Market": (250, 1999),
    "Enterprise": (2000, 20000),
}


# this is an empty list, as we intend to fill it out
employee_counts = []

# high + 1 is important because NumPy's upper limit is exclusive - this means that it won't include the absolute highest limit we've set unless we add one to it
# for every value in the customer_segment column, do the following functions
for segment in customers["customer_segment"]:
    low, high = employee_ranges[segment]
    employee_count = rng.integers(low, high +1)
    employee_counts.append(employee_count)

customers["employee_count"] = employee_counts


# now to repeat the same for product count ranges too

product_count_ranges = {
    "Small Business": (1, 2),
    "Mid-Market": (1, 3),
    "Enterprise": (2, 5).
}

expected_product_counts = []

for segment in customers["customer_segment"]:
    low, high = product_count_ranges[segment]
    product_count = rng.integers(low, high + 1)
    expected_product_counts.append(product_count)

customers["expected_product_count"] = expected_product_counts


# adding in plausible churn numbers but not realistic statistics
churn_probabilities = {
    "Small Business": 0.12,
    "Mid-Market": 0.08,
    "Enterprise": 0.05,
}


# map here is saying, take every value in the customer segment column and replace/map it according to this dictionary
customers["baseline_churn_probability"] = (
    customers["customer_segment"].map(churn_probabilities)
)

return customers