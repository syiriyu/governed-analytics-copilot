from pathlib import Path

SEED = 42

N_CUSTOMERS = 10_000
N_ACCOUNT_MANAGERS = 120

START_DATE = "2023-01-01"
END_DATE = "2026-06-30"

DATA_DIR = Path("data/generated")

CUSTOMER_SEGMENTS = [
    "Small Business",
    "Mid-Market",
    "Enterprise",
]

REGIONS = [
    "UK & Ireland",
    "Northern Europe",
    "Southern Europe",
    "Central Europe",
]

INDUSTRIES = [
    "Technology",
    "Financial Services",
    "Retail",
    "Manufacturing",
    "Professional Services",
    "Healthcare",
    "Media",
    "Travel",
]