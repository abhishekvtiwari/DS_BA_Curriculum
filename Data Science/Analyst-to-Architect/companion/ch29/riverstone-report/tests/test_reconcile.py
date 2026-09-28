"""Integration test: runs only when RIVERSTONE_DATABASE_URL points at riverstone_2025."""
import os

import pytest
from sqlalchemy import create_engine

from riverstone_report import db, transform
from riverstone_report.config import ReportConfig

pytestmark = pytest.mark.skipif(not os.environ.get("RIVERSTONE_DATABASE_URL"),
                                reason="no database configured")


def test_december_2025_matches_the_book():
    config = ReportConfig.from_env("2025-12")
    engine = create_engine(config.database_url)
    lines = db.fetch_sales_lines(engine, config.month, config.next_month)
    summary = transform.summarize(lines, db.fetch_target(engine, config.month))
    assert summary.revenue == 439823.50
    assert summary.pct_of_target == 115.7
    categories = transform.revenue_by_category(lines)
    assert categories["net_revenue"].sum() == pytest.approx(summary.revenue)
