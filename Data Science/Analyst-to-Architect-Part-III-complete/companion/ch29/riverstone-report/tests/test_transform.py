import pandas as pd
import pytest

from riverstone_report.errors import NoDataError
from riverstone_report.transform import MonthSummary, revenue_by_category, summarize, top_customers


def test_summarize_counts_orders_not_lines(lines):
    summary = summarize(lines, target=20000.0)
    assert summary.revenue == 25000.0
    assert summary.orders == 3
    assert summary.customers == 3
    assert summary.pct_of_target == 125.0


def test_no_target_gives_no_percentage(lines):
    assert summarize(lines, target=None).pct_of_target is None


def test_categories_are_sorted_and_shares_add_up(lines):
    result = revenue_by_category(lines)
    assert list(result["category"]) == ["Storage", "Furniture", "Kitchen"]
    assert list(result["net_revenue"]) == [16000.0, 5000.0, 4000.0]
    assert result["share_pct"].sum() == pytest.approx(100.0, abs=0.2)


@pytest.mark.parametrize("n, expected", [(1, ["Sharma Hardware"]), (2, ["Sharma Hardware", "Green Leaf Hotels"])])
def test_top_customers(lines, n, expected):
    assert list(top_customers(lines, n)["customer_name"]) == expected


def test_top_customers_rejects_zero(lines):
    with pytest.raises(ValueError, match="at least 1"):
        top_customers(lines, 0)


def test_empty_month_raises_no_data(lines):
    with pytest.raises(NoDataError):
        summarize(lines.iloc[0:0], target=300000.0)


def test_missing_column_is_reported(lines):
    with pytest.raises(ValueError, match="net_revenue"):
        summarize(lines.drop(columns="net_revenue"), target=None)


def test_zero_target_gives_no_percentage():
    assert MonthSummary(revenue=100.0, orders=1, customers=1, target=0.0).pct_of_target is None
