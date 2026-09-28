"""Does a deeper discount buy Riverstone more orders? One year, one answer."""
import pandas as pd

DATA = "../full"


def customer_year(year=2025, segment=None, min_orders=1):
    """One row per customer: orders placed, list revenue, net revenue, discount rate."""
    orders = pd.read_csv(f"{DATA}/orders.csv", parse_dates=["order_date"])
    items = pd.read_csv(f"{DATA}/order_items.csv")
    customers = pd.read_csv(f"{DATA}/customers.csv")

    orders = orders[(orders.status != "Cancelled") & (orders.order_date.dt.year == year)]
    lines = items.merge(orders[["order_id", "customer_id"]], on="order_id")
    lines["list_revenue"] = lines.quantity * lines.unit_price
    lines["net_revenue"] = lines.list_revenue * (1 - lines.discount_pct / 100)

    per_customer = (lines.groupby("customer_id")
                    .agg(orders=("order_id", "nunique"),
                         list_revenue=("list_revenue", "sum"),
                         net_revenue=("net_revenue", "sum"))
                    .reset_index()
                    .merge(customers[["customer_id", "segment"]], on="customer_id"))
    per_customer["discount_pct"] = 100 * (1 - per_customer.net_revenue / per_customer.list_revenue)

    if segment is not None:
        per_customer = per_customer[per_customer.segment == segment]
    return per_customer[per_customer.orders >= min_orders]


def discount_report(year=2025, segment=None, band_cut=5.0, min_orders=1):
    """Average orders and revenue for customers above and below one discount line."""
    people = customer_year(year=year, segment=segment, min_orders=min_orders)
    people = people.assign(
        band=people.discount_pct.ge(band_cut).map({True: f"{band_cut:g}% or deeper",
                                                   False: f"under {band_cut:g}%"}))
    return (people.groupby("band")
            .agg(customers=("customer_id", "size"),
                 avg_orders=("orders", "mean"),
                 avg_revenue=("net_revenue", "mean"))
            .round({"avg_orders": 1, "avg_revenue": 0}))


if __name__ == "__main__":
    print(discount_report())
