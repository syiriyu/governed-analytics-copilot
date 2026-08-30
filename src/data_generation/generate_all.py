from .customers import generate_customers
from .customer_profiles import add_customer_profiles
from .products import generate_products
from .account_managers import generate_account_managers
from .contracts import generate_contracts
from .revenue import generate_monthly_revenue
from .usage import generate_product_usage
from .support import generate_support_cases
from .renewals import build_renewal_features

customers = generate_customers()
customers = add_customer_profiles(customers)

products = generate_products()
account_managers = generate_account_managers()

contracts = generate_contracts(
    customers,
    products,
    account_managers,
)

monthly_revenue = generate_monthly_revenue(
    contracts
)

product_usage = generate_product_usage(
    contracts,
    customers,
)

support_cases = generate_support_cases(
    customers
)

renewal_features = build_renewal_features(
    contracts,
    product_usage,
    support_cases,
)

#print("\nCustomers")
#print(customers.head())

#print("\nContracts")
#print(contracts.head())

#print(f"\nNumber of contracts: {len(contracts):,}")

#print(
#    contracts["renewal_eligible"].value_counts()
#)

#print("\nMonthly Revenue")
#print(monthly_revenue.head(10))

#print(
#    f"\nRevenue records: {len(monthly_revenue):,}"
#)

#print("\nProduct Usage")
#print(product_usage.head(10))

#print(
#    f"\nUsage records: {len(product_usage):,}"
#)

# to check for one record only
#print(
#    product_usage[
#        product_usage["contract_id"] == "CT000001"
#    ]
#)

# print("\nSupport Cases")
# print(support_cases.head(10))

# print(
#     f"\nSupport cases: {len(support_cases):,}"
# )

# print(
#     support_cases[
#         "sla_breached"
#     ].value_counts(
#         normalize=True
#     )
# )

# print(
#     support_cases.groupby(
#         "sla_breached"
#     )["satisfaction_score"].mean()
# )

# print(
#     support_cases.groupby(
#         "priority"
#     )["resolution_hours"].mean()
# )

print("\nRenewal Features")

print(
    renewal_features[
        [
            "contract_id",
            "usage_change_pct",
            "support_case_count",
            "sla_breach_rate",
            "average_satisfaction",
        ]
    ].head(20)
)

#-------------------------------------

# my first attempt to understand if higher breach rates result in lower satisfaction rates
# print(
#     renewal_features[
#         [renewal_features[average_satisfaction].mean()
#         renewal_features[sla_breach_rate] > renewal_features[sla_breach_rate].mean()
#         ]
#     ]
# )

# this is the correct approach

# takes a global avg of the SLA breach rate
average_breach_rate = renewal_features[
    "sla_breach_rate"
].mean()

# then uses that global SLA breach rate avg and returns contracts whose sla rate is higher than the global avg
high_breach_contracts = renewal_features[
    renewal_features["sla_breach_rate"]
    > average_breach_rate
]

# then printing the resultant high breach contracts' avg satisfaction score
print(
    high_breach_contracts[
        "average_satisfaction"
    ].mean()
)

#-------------------------------------

# len is equivalent to count(*), so count all over the number of rows in df. other methods are df.shape[0] for num of rows and df.shape[1] for num of columns
# print(
#     len(
#         renewal_features[
#         renewal_features["usage_change_pct"] < 0
#         ]
#     )
# )


# .duplicated() syntax will create an output where subsequent dupes are logged with a boolean.. so
# print(
#     "Duplicate contract IDs:",
#     contracts["contract_id"].duplicated().sum()
# )

# duplicate_contracts = contracts[
#     contracts["contract_id"].duplicated(
#         keep=False
#     )
# ].sort_values("contract_id")

# print(duplicate_contracts.head(20))