

### Filtering like a WHERE clause

print(
    product_usage[
        product_usage["contract_id"] == "CT000001"
    ]
)


| Pandas/Python              | SQL mental equivalent                     |
| -------------------------- | ----------------------------------------- |
| `df["column"]`             | `SELECT column`                           |
| `df[["a", "b"]]`           | `SELECT a, b`                             |
| `df[df["x"] == 1]`         | `WHERE x = 1`                             |
| `.merge()`                 | `JOIN`                                    |
| `how="left"`               | `LEFT JOIN`                               |
| `.groupby()`               | `GROUP BY`                                |
| `.sort_values()`           | `ORDER BY`                                |
| `.head(10)`                | `LIMIT 10`                                |
| `.isna()`                  | `IS NULL`                                 |
| `.drop_duplicates()`       | `DISTINCT` / deduplication                |
| `.map(dictionary)`         | often similar to `CASE WHEN` / lookup     |
| `pd.date_range()`          | date series/calendar generation           |
| `.to_period("M")`          | monthly date grain / `DATE_TRUNC` concept |
| `for row in df.iterrows()` | row-by-row procedural processing          |
