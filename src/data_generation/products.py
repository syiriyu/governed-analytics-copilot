import pandas as pd


def generate_products():
    products = [
        {
            "product_id": "P001",
            "product_name": "Atlas Core",
            "product_category": "Platform",
        },
        {
            "product_id": "P002",
            "product_name": "Atlas Insights",
            "product_category": "Analytics",
        },
        {
            "product_id": "P003",
            "product_name": "Atlas Automate",
            "product_category": "Automation",
        },
        {
            "product_id": "P004",
            "product_name": "Atlas Connect",
            "product_category": "Integration",
        },
        {
            "product_id": "P005",
            "product_name": "Atlas Secure",
            "product_category": "Compliance",
        },
        {
            "product_id": "P006",
            "product_name": "Atlas Support+",
            "product_category": "Premium Service",
        },
    ]

    return pd.DataFrame(products)