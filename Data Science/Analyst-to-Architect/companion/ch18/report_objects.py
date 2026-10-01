"""Analyst to Architect · Chapter 18 · report_objects.py
Section 18.17's finished code: the monthly report organised as objects rather than loose functions.

Use:     from report_objects import ReportConfig, MonthlyReport, ExcelWriterStep, MarkdownWriterStep
         report = MonthlyReport(ReportConfig(month="2025-12"))
         report.run()
Reads:   ../full/orders.csv, order_items.csv, customers.csv, products.csv, sales_targets.csv
Tested:  Python 3.12.0, pandas 3.0.2 (1 October 2026)

Riverstone Supplies is fictional; every name and number is invented.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

log = logging.getLogger("report_objects")


@dataclass(frozen=True)
class ReportConfig:
    """Every setting the report needs, in one named bundle.

    frozen=True makes it read-only after it is built, so no step can quietly change a setting
    that a later step depends on.
    """
    month: str
    data_dir: Path = Path("../full")
    out_dir: Path = Path("reports")
    tolerance_pct: float = 50.0

    @property
    def start(self) -> pd.Timestamp:
        return pd.Timestamp(self.month + "-01")

    @property
    def end(self) -> pd.Timestamp:
        return self.start + pd.offsets.MonthBegin(1)


class SalesData:
    """Loads Riverstone's order lines and nothing else. One job."""

    def __init__(self, config: ReportConfig):
        self.config = config
        self._lines: pd.DataFrame | None = None

    def lines(self) -> pd.DataFrame:
        """The month's order lines, loaded once and remembered."""
        if self._lines is None:
            self._lines = self._load()
        return self._lines

    def _load(self) -> pd.DataFrame:
        d = self.config.data_dir
        orders = pd.read_csv(d / "orders.csv", parse_dates=["order_date"])
        items = pd.read_csv(d / "order_items.csv")
        customers = pd.read_csv(d / "customers.csv")
        products = pd.read_csv(d / "products.csv")

        window = orders[(orders.order_date >= self.config.start)
                        & (orders.order_date < self.config.end)
                        & (orders.status != "Cancelled")]
        lines = (window
                 .merge(items, on="order_id", validate="one_to_many")
                 .merge(customers[["customer_id", "customer_name", "segment"]],
                        on="customer_id", validate="many_to_one")
                 .merge(products[["product_id", "product_name", "unit_cost"]],
                        on="product_id", validate="many_to_one"))
        lines["net_revenue"] = (lines.quantity * lines.unit_price
                                * (1 - lines.discount_pct / 100)).round(2)
        lines["cost"] = (lines.quantity * lines.unit_cost).round(2)
        log.info("loaded %s lines for %s", f"{len(lines):,}", self.config.month)
        return lines

    def target(self) -> float:
        """The month's revenue target. The file dates each month as its first day."""
        targets = pd.read_csv(self.config.data_dir / "sales_targets.csv")
        wanted = self.config.start.strftime("%Y-%m-%d")
        row = targets[targets.target_month == wanted]
        return float(row.target_revenue.iloc[0]) if len(row) else float("nan")


@dataclass
class Check:
    """One named check and whether it passed."""
    name: str
    passed: bool
    detail: str


class WriterStep:
    """What every writer must do. Subclasses say how."""

    suffix = ""

    def write(self, report: "MonthlyReport") -> Path:
        raise NotImplementedError("a writer must implement write()")

    def path_for(self, report: "MonthlyReport") -> Path:
        report.config.out_dir.mkdir(parents=True, exist_ok=True)
        return report.config.out_dir / f"riverstone-{report.config.month}{self.suffix}"


class ExcelWriterStep(WriterStep):
    suffix = ".xlsx"

    def write(self, report: "MonthlyReport") -> Path:
        path = self.path_for(report)
        with pd.ExcelWriter(path, engine="xlsxwriter") as xl:
            report.by_segment().to_excel(xl, sheet_name="By segment", index=False)
            report.lines().head(1000).to_excel(xl, sheet_name="Lines", index=False)
        return path


class MarkdownWriterStep(WriterStep):
    suffix = ".md"

    def write(self, report: "MonthlyReport") -> Path:
        path = self.path_for(report)
        h = report.headlines()
        rows = "\n".join(
            f"| {r.segment} | {r.net_revenue:,.0f} |"
            for r in report.by_segment().itertuples())
        path.write_text(
            f"# Riverstone · {report.config.month}\n\n"
            f"Net revenue Rs {h['net_revenue']:,.0f} from {h['orders']:,} orders.\n\n"
            f"| Segment | Net revenue |\n|---|---|\n{rows}\n",
            encoding="utf-8")
        return path


class MonthlyReport:
    """The report. It owns its settings, its data, and its writers."""

    def __init__(self, config: ReportConfig, writers: list[WriterStep] | None = None):
        self.config = config
        self.data = SalesData(config)
        self.writers = writers if writers is not None else [MarkdownWriterStep()]

    def lines(self) -> pd.DataFrame:
        return self.data.lines()

    def headlines(self) -> dict:
        lines = self.lines()
        return {
            "net_revenue": float(lines.net_revenue.sum()),
            "orders": int(lines.order_id.nunique()),
            "margin_pct": float((1 - lines.cost.sum() / lines.net_revenue.sum()) * 100),
        }

    def by_segment(self) -> pd.DataFrame:
        return (self.lines()
                .groupby("segment", as_index=False)["net_revenue"]
                .sum()
                .sort_values("net_revenue", ascending=False)
                .round(2))

    def checks(self) -> list[Check]:
        lines = self.lines()
        h = self.headlines()
        target = self.data.target()
        out = [
            Check("some lines were loaded", len(lines) > 0, f"{len(lines):,} lines"),
            Check("no negative revenue", bool((lines.net_revenue >= 0).all()),
                  f"min Rs {lines.net_revenue.min():,.2f}"),
            Check("segments reconcile to the total",
                  abs(self.by_segment().net_revenue.sum() - h["net_revenue"]) < 0.01,
                  "segment sum matches the headline"),
        ]
        if target == target:                       # not NaN
            gap = (h["net_revenue"] / target - 1) * 100
            out.append(Check("within tolerance of target",
                             abs(gap) <= self.config.tolerance_pct, f"{gap:+.1f}% vs target"))
        return out

    def run(self) -> list[Path]:
        failed = [c for c in self.checks() if not c.passed]
        if failed:
            raise ValueError("checks failed: " + "; ".join(c.name for c in failed))
        return [w.write(self) for w in self.writers]
