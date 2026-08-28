from .customers import generate_customers
from .customer_profiles import add_customer_profiles
from .products import generate_products
from .account_managers import generate_account_managers
from .contracts import generate_contracts

customers = generate_customers()
customers = add_customer_profiles(customers)

products = generate_products()
account_managers = generate_account_managers()

contracts = generate_contracts(
    customers,
    products,
    account_managers,
)



print("\nCustomers")
print(customers.head())

print("\nContracts")
print(contracts.head())

print(f"\nNumber of contracts: {len(contracts):,}")

print(
    contracts["renewal_eligible"].value_counts()
)

