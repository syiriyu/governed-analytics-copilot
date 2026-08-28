from .customers import generate_customers
from .customer_profiles import add_customer_profiles


customers = generate_customers()
customers = add_customer_profiles(customers)

# testing customers dataset
print(customers.head())