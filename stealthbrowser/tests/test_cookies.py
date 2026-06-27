"""Tests for cookie utilities."""
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from stealthbrowser.cookies import (
    cookies_from_header,
    cookies_to_header,
    filter_cookies,
    load_cookies,
    merge_cookies,
    save_cookies,
)

SAMPLE = [
    {"name": "session", "value": "abc", "domain": ".example.com", "path": "/"},
    {"name": "theme", "value": "dark", "domain": ".example.com", "path": "/"},
    {"name": "ad", "value": "xyz", "domain": ".ads.com", "path": "/"},
]


def test_save_load():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "cookies.json"
        save_cookies(SAMPLE, p)
        loaded = load_cookies(p)
    assert len(loaded) == 3
    assert loaded[0]["name"] == "session"


def test_filter():
    filtered = filter_cookies(SAMPLE, "example.com")
    assert len(filtered) == 2
    assert all("example.com" in c["domain"] for c in filtered)


def test_merge_overrides():
    extra = [{"name": "session", "value": "NEW", "domain": ".example.com"}]
    merged = merge_cookies(SAMPLE, extra)
    session = next(c for c in merged if c["name"] == "session")
    assert session["value"] == "NEW"
    assert len(merged) == 3


def test_to_header():
    h = cookies_to_header(SAMPLE[:2])
    assert "session=abc" in h
    assert "theme=dark" in h
    assert ";" in h


def test_from_header():
    h = "session=abc; theme=dark; lang=en"
    cookies = cookies_from_header(h)
    assert len(cookies) == 3
    names = [c["name"] for c in cookies]
    assert "session" in names
    assert "lang" in names


def test_roundtrip_header():
    cookies = [{"name": "a", "value": "1"}, {"name": "b", "value": "2"}]
    header = cookies_to_header(cookies)
    reparsed = cookies_from_header(header)
    values = {c["name"]: c["value"] for c in reparsed}
    assert values["a"] == "1"
    assert values["b"] == "2"
