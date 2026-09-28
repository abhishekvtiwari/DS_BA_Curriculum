from datetime import date
from pathlib import Path

import pytest

from riverstone_report.config import ReportConfig, parse_month
from riverstone_report.errors import ConfigError


@pytest.mark.parametrize("text, expected", [("2025-12", date(2025, 12, 1)),
                                            ("2026-01", date(2026, 1, 1))])
def test_parse_month(text, expected):
    assert parse_month(text) == expected


@pytest.mark.parametrize("bad", ["Dec 2025", "2025-13", "2025", ""])
def test_parse_month_rejects_bad_input(bad):
    with pytest.raises(ConfigError):
        parse_month(bad)


def test_from_env_needs_database_url():
    with pytest.raises(ConfigError, match="RIVERSTONE_DATABASE_URL"):
        ReportConfig.from_env("2025-12", env={})


def test_december_rolls_into_next_year():
    env = {"RIVERSTONE_DATABASE_URL": "postgresql://example"}
    config = ReportConfig.from_env("2025-12", env=env)
    assert config.next_month == date(2026, 1, 1)
    assert config.output_path == Path("reports/riverstone_monthly_2025-12.xlsx")
