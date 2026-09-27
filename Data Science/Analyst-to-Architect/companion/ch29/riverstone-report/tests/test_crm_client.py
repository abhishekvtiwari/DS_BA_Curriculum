import random

import pytest
import requests

from riverstone_report.crm_client import CrmClient
from riverstone_report.errors import CrmApiError


class FakeResponse:
    def __init__(self, status_code, body=None, headers=None):
        self.status_code = status_code
        self._body = body or {}
        self.headers = headers or {}
        self.text = str(self._body)

    def json(self):
        return self._body


class FakeSession:
    """Plays back a list of responses (or exceptions) instead of calling a real server."""
    def __init__(self, replies):
        self.replies = list(replies)
        self.headers = {}
        self.calls = []

    def get(self, url, params, timeout):
        self.calls.append(params)
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return reply


def make_client(replies, sleeps):
    return CrmClient("https://crm.example", "test-key", session=FakeSession(replies),
                     sleep=sleeps.append, rng=random.Random(1))


def test_follows_pages_until_next_page_is_none():
    sleeps = []
    client = make_client([FakeResponse(200, {"items": [{"lead_id": 1}], "next_page": 2}),
                          FakeResponse(200, {"items": [{"lead_id": 2}], "next_page": None})], sleeps)
    assert [lead["lead_id"] for lead in client.iter_leads()] == [1, 2]
    assert sleeps == []


def test_retries_server_errors_then_succeeds():
    sleeps = []
    client = make_client([FakeResponse(503), requests.ConnectionError(),
                          FakeResponse(200, {"items": [], "next_page": None})], sleeps)
    assert list(client.iter_leads()) == []
    assert len(sleeps) == 2 and sleeps[1] > sleeps[0]


def test_honors_retry_after_on_429():
    sleeps = []
    client = make_client([FakeResponse(429, headers={"Retry-After": "7"}),
                          FakeResponse(200, {"items": [], "next_page": None})], sleeps)
    list(client.iter_leads())
    assert sleeps == [7.0]


def test_does_not_retry_a_bad_api_key():
    sleeps = []
    client = make_client([FakeResponse(401, {"error": "invalid key"})], sleeps)
    with pytest.raises(CrmApiError, match="401"):
        list(client.iter_leads())
    assert sleeps == []


def test_gives_up_after_max_attempts():
    sleeps = []
    client = make_client([FakeResponse(500)] * 4, sleeps)
    with pytest.raises(CrmApiError, match="after 4 attempts"):
        list(client.iter_leads())
    assert len(sleeps) == 3
