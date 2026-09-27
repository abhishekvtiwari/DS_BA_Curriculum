"""A careful client for the CRM's leads API: pagination, timeouts, retries with backoff, and rate limits."""
from __future__ import annotations

import logging
import random
import time
from collections.abc import Callable, Iterator
from typing import Any

import requests

from riverstone_report.errors import CrmApiError

log = logging.getLogger(__name__)

RETRY_STATUSES = {429, 500, 502, 503, 504}


class CrmClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        *,
        session: requests.Session | None = None,
        max_attempts: int = 4,
        backoff_seconds: float = 0.5,
        timeout: tuple[float, float] = (3.05, 10.0),
        sleep: Callable[[float], None] = time.sleep,
        rng: random.Random | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.session.headers["X-API-Key"] = api_key
        self.max_attempts = max_attempts
        self.backoff_seconds = backoff_seconds
        self.timeout = timeout
        self.sleep = sleep
        self.rng = rng or random.Random()

    def _wait_time(self, attempt: int, response: requests.Response | None) -> float:
        if response is not None and response.status_code == 429:
            retry_after = response.headers.get("Retry-After", "")
            if retry_after.isdigit():
                return float(retry_after)
        base: float = self.backoff_seconds * 2 ** (attempt - 1)
        return round(base + self.rng.uniform(0, base / 2), 3)

    def get_json(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        for attempt in range(1, self.max_attempts + 1):
            response: requests.Response | None = None
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
            except (requests.ConnectionError, requests.Timeout) as exc:
                problem = type(exc).__name__
            else:
                if response.status_code == 200:
                    data: dict[str, Any] = response.json()
                    return data
                if response.status_code not in RETRY_STATUSES:
                    raise CrmApiError(f"{url} returned {response.status_code}: {response.text[:100]}")
                problem = f"HTTP {response.status_code}"
            if attempt == self.max_attempts:
                raise CrmApiError(f"{url} failed after {attempt} attempts (last: {problem})")
            wait = self._wait_time(attempt, response)
            log.warning("attempt %d for %s failed (%s); retrying in %.3f s", attempt, params, problem, wait)
            self.sleep(wait)
        raise AssertionError("unreachable")

    def iter_leads(self, page_size: int = 10) -> Iterator[dict[str, Any]]:
        page = 1
        while True:
            data = self.get_json("/leads", {"page": page, "page_size": page_size})
            yield from data["items"]
            if data["next_page"] is None:
                return
            page = data["next_page"]
