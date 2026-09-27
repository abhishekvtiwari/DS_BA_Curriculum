"""Exceptions the report can raise. Callers catch ReportError to handle any of them."""


class ReportError(Exception):
    """Base class for every expected failure of the monthly report."""


class ConfigError(ReportError):
    """A setting is missing or invalid."""


class NoDataError(ReportError):
    """The requested month has no sales, so a report would be misleading."""


class CrmApiError(ReportError):
    """The CRM API kept failing after all retries, or refused the request."""
