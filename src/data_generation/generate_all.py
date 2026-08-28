from .customers import generate_customers
from .customer_profiles import add_customer_profiles
from .products import generate_products
from .account_managers import generate_account_managers
from .contracts import generate_contracts
from .revenue import generate_monthly_revenue
from .usage import generate_product_usage
from .support import generate_support_cases

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

print("\nSupport Cases")
print(support_cases.head(10))

print(
    f"\nSupport cases: {len(support_cases):,}"
)

print(
    support_cases[
        "sla_breached"
    ].value_counts(
        normalize=True
    )
)

print(
    support_cases.groupby(
        "sla_breached"
    )["satisfaction_score"].mean()
)

print(
    support_cases.groupby(
        "priority"
    )["resolution_hours"].mean()
)