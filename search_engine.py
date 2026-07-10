import pandas as pd
from rapidfuzz import fuzz
from config import CSV_FILE, MAX_RESULTS

# Load CSV
df = pd.read_csv(CSV_FILE).fillna("")

# Convert important columns to string
columns = [
    "product_name",
    "description",
    "main_category",
    "sub_category",
    "color_options"
]

for col in columns:
    if col in df.columns:
        df[col] = df[col].astype(str)


def search_products(query):
    query = query.lower()
    results = []

    for _, row in df.iterrows():

        score = 0

        search_text = " ".join([
            row.get("product_name", ""),
            row.get("description", ""),
            row.get("main_category", ""),
            row.get("sub_category", ""),
            row.get("color_options", "")
        ]).lower()

        score = fuzz.partial_ratio(query, search_text)

        if score > 55:
            results.append((score, row))

    results.sort(reverse=True, key=lambda x: x[0])

    return [x[1] for x in results[:MAX_RESULTS]]
