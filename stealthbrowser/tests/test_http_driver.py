"""Tests for HTTPDriver — no real browser required."""
from __future__ import annotations

import pytest

from stealthbrowser.profile import BrowserProfile
from stealthbrowser.drivers.http_driver import HTTPDriver


@pytest.fixture
def profile():
    return BrowserProfile.random(driver="http", os="windows")


@pytest.fixture
def driver(profile):
    drv = HTTPDriver(profile)
    drv.start()
    yield drv
    drv.stop()


def test_start_stop(profile):
    drv = HTTPDriver(profile)
    drv.start()
    assert drv._started
    drv.stop()
    assert not drv._started


def test_context_manager(profile):
    with HTTPDriver(profile) as drv:
        assert drv._started


def test_get_and_source(driver):
    driver.get("https://httpbin.org/html")
    html = driver.source()
    assert len(html) > 0
    assert "<html" in html.lower() or "<!doctype" in html.lower()


def test_title(driver):
    driver.get("https://httpbin.org/html")
    t = driver.title()
    assert isinstance(t, str)


def test_status_code(driver):
    driver.get("https://httpbin.org/status/200")
    assert driver.status_code() == 200


def test_json_response(driver):
    driver.get("https://httpbin.org/json")
    data = driver.json()
    assert isinstance(data, dict)


def test_user_agent_forwarded(driver, profile):
    driver.get("https://httpbin.org/user-agent")
    data = driver.json()
    sent_ua = profile.fingerprint.user_agent
    reported = data.get("user-agent", "")
    assert sent_ua == reported


def test_fingerprint_report(driver, profile):
    report = driver.fingerprint_report()
    assert report["user_agent"] == profile.fingerprint.user_agent
    assert report["locale"] == profile.fingerprint.locale


def test_cookies(driver):
    driver.get("https://httpbin.org/cookies/set?foo=bar")
    cookies = driver.get_cookies()
    names = [c["name"] for c in cookies]
    assert "foo" in names


def test_clear_cookies(driver):
    driver.get("https://httpbin.org/cookies/set?foo=bar")
    driver.clear_cookies()
    assert driver.get_cookies() == []


def test_current_url(driver):
    driver.get("https://httpbin.org/get")
    url = driver.current_url()
    assert "httpbin.org" in url
