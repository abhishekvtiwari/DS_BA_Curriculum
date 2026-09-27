"""Pure calculations: DataFrames in, results out. No database, no files, so they are easy to test."""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from riverstone_report.errors import NoDataError

REQUIRED_COLUMNS = {"order_id", "customer_name", "category", "net_revenue"}


@dataclass(frozen=True)
class MonthSummary:
    revenue: float
    orders: int
    customers: int
    target: float | None

    @property
    def pct_of_target(self) -> float | None:
        if not self.target:
            return None
        return round(100 * self.revenue / self.target, 1)


def check_lines(lines: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(lines.columns)
    if missing:
        raise ValueError(f"sales lines are missing columns: {sorted(missing)}")
    if lines.empty:
        raise NoDataError("no sales lines for this month")


def summarize(lines: pd.DataFrame, target: float | None) -> MonthSummary:
    check_lines(lines)
    return MonthSummary(
        revenue=round(float(lines["net_revenue"].sum()), 2),
        orders=int(lines["order_id"].nunique()),
        customers=int(lines["customer_name"].nunique()),
        target=target,
    )


def revenue_by_category(lines: pd.DataFrame) -> pd.DataFrame:
    check_lines(lines)
    result = (lines.groupby("category", as_index=False)
                   .agg(net_revenue=("net_revenue", "sum"))
                   .sort_values(["net_revenue", "category"], ascending=[False, True], ignore_index=True))
    result["share_pct"] = (100 * result["net_revenue"] / result["net_revenue"].sum()).round(1)
    return result


def top_customers(lines: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    if n < 1:
        raise ValueError("n must be at least 1")
    check_lines(lines)
    totals = lines.groupby("customer_name", as_index=False).agg(net_revenue=("net_revenue", "sum"))
    ranked = totals.sort_values(["net_revenue", "customer_name"], ascending=[False, True], ignore_index=True)
    return ranked.head(n)
