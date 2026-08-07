def calculate_total_orders(merged):
    return merged["order_id"].nunique()


def calculate_total_quantity(merged):
    return merged["quantity"].sum()


def calculate_total_sales(merged):
    return merged["item_amount"].sum()


def calculate_average_order_amount(merged):
    order_totals = (
        merged.groupby("order_id")["item_amount"]
        .sum()
    )
    return order_totals.mean()


def get_category_sales(merged):
    return (
        merged
        .groupby("category", as_index=False)["item_amount"]
        .sum()
        .sort_values("item_amount", ascending=False)
    )


def get_status_counts(merged):
    return (
        merged[["order_id", "order_status"]]
        .drop_duplicates()
        .groupby("order_status", as_index=False)["order_id"]
        .nunique()
        .rename(columns={"order_id": "order_count"})
        .sort_values("order_count", ascending=False)
    )


def get_monthly_sales(merged):
    return (
        merged
        .groupby("order_month", as_index=False)["item_amount"]
        .sum()
        .sort_values("order_month")
    )