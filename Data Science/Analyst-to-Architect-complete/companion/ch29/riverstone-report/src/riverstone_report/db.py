"""Reading from the database. The only module that knows SQL."""
from __future__ import annotations

from datetime import date

import pandas as pd
from sqlalchemy import Engine, text

SALES_LINES_SQL = text("""
    SELECT sl.order_id, sl.order_date, c.customer_name, sl.category, sl.net_revenue
    FROM sales_lines AS sl
    JOIN customers AS c ON c.customer_id = sl.customer_id
    WHERE sl.order_date >= :month_start AND sl.order_date < :next_month
""")

TARGET_SQL = text("SELECT target_revenue FROM sales_targets WHERE target_month = :month_start")


def fetch_sales_lines(engine: Engine, month_start: date, next_month: date) -> pd.DataFrame:
    """One row per non-cancelled order line in the month, with net_revenue as a float."""
    with engine.connect() as conn:
        lines = pd.read_sql(SALES_LINES_SQL, conn, params={"month_start": month_start, "next_month": next_month})
    return lines.astype({"net_revenue": "float64"})


def fetch_target(engine: Engine, month_start: date) -> float | None:
    """The month's revenue target, or None if no target was set."""
    with engine.connect() as conn:
        value = conn.execute(TARGET_SQL, {"month_start": month_start}).scalar_one_or_none()
    return None if value is None else float(value)
