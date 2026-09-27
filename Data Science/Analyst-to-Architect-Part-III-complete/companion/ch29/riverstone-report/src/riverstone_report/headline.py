"""A one-line headline for emails (section 29.6)."""
from riverstone_report.transform import MonthSummary


def headline(summary: MonthSummary) -> str:
    if summary.pct_of_target is None:
        return f"Revenue ₹{summary.revenue:,.0f} (no target set)"
    gap = summary.pct_of_target - 100
    return f"Revenue ₹{summary.revenue:,.0f}, {gap:+.1f} points against target"
