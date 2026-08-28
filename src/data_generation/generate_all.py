from .customers import generate_customers
from .customer_profiles import add_customer_profiles
from .products import generate_products
from .account_managers import generate_account_managers
from .contracts import generate_contracts
from .revenue import generate_monthly_revenue

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