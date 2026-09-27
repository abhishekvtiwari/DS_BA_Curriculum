"""Settings for one report run, read from arguments and environment variables."""
from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from riverstone_report.errors import ConfigError


def parse_month(text: str) -> date:
    """Turn '2025-12' into date(2025, 12, 1). Raise ConfigError for anything else."""
    try:
        year, month = (int(part) for part in text.split("-"))
        return date(year, month, 1)
    except ValueError:
        raise ConfigError(f"month must look like YYYY-MM, got {text!r}") from None


@dataclass(frozen=True)
class ReportConfig:
    month: date
    database_url: str
    output_dir: Path = Path("reports")
    top_n: int = 5

    @classmethod
    def from_env(cls, month: str, env: Mapping[str, str] = os.environ) -> ReportConfig:
        url = env.get("RIVERSTONE_DATABASE_URL")
        if not url:
            raise ConfigError("set RIVERSTONE_DATABASE_URL to the database connection URL")
        return cls(
            month=parse_month(month),
            database_url=url,
            output_dir=Path(env.get("RIVERSTONE_OUTPUT_DIR", "reports")),
        )

    @property
    def next_month(self) -> date:
        if self.month.month == 12:
            return date(self.month.year + 1, 1, 1)
        return date(self.month.year, self.month.month + 1, 1)

    @property
    def output_path(self) -> Path:
        return self.output_dir / f"riverstone_monthly_{self.month:%Y-%m}.xlsx"
