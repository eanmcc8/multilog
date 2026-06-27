"""Tests for BrowserProfile and related models."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from stealthbrowser.profile import (
    BrowserProfile,
    Fingerprint,
    ProxyConfig,
)


class TestProxyConfig:
    def test_from_string_simple(self):
        p = ProxyConfig.from_string("proxy.example.com:8080")
        assert p.host == "proxy.example.com"
        assert p.port == 8080
        assert p.type == "http"

    def test_from_string_with_auth(self):
        p = ProxyConfig.from_string("socks5://user:pass@proxy.example.com:1080")
        assert p.type == "socks5"
        assert p.username == "user"
        assert p.password == "pass"
        assert p.port == 1080

    def test_url_property(self):
        p = ProxyConfig(host="h.com", port=8080, type="http", username="u", password="p")
        assert "u:p@h.com:8080" in p.url

    def test_url_no_auth(self):
        p = ProxyConfig(host="h.com", port=3128, type="http")
        assert "@" not in p.url

    def test_playwright_dict(self):
        p = ProxyConfig(host="h.com", port=8080, type="http", username="u", password="p")
        d = p.as_playwright_dict()
        assert "server" in d
        assert d["username"] == "u"


class TestFingerprint:
    def test_random_windows(self):
        fp = Fingerprint.random("windows")
        assert "Windows" in fp.user_agent or "Win" in fp.platform
        assert fp.resolution_width > 0
        assert fp.resolution_height > 0
        assert fp.canvas_noise > 0
        assert fp.audio_noise > 0
        assert len(fp.fonts) > 0

    def test_random_macos(self):
        fp = Fingerprint.random("macos")
        assert "Macintosh" in fp.user_agent or fp.platform == "MacIntel"

    def test_random_linux(self):
        fp = Fingerprint.random("linux")
        assert "Linux" in fp.user_agent or "Linux" in fp.platform

    def test_fields_populated(self):
        fp = Fingerprint.random()
        assert fp.webgl_vendor
        assert fp.webgl_renderer
        assert fp.locale
        assert fp.timezone
        assert fp.hardware_concurrency in [2, 4, 6, 8, 12, 16]
        assert fp.device_memory in [2, 4, 8, 16, 32]


class TestBrowserProfile:
    def test_random_creates_valid_profile(self):
        p = BrowserProfile.random()
        assert p.id
        assert p.name
        assert p.fingerprint.user_agent
        assert p.driver == "playwright"

    def test_custom_driver(self):
        p = BrowserProfile.random(driver="selenium")
        assert p.driver == "selenium"

    def test_custom_os(self):
        p = BrowserProfile.random(os="macos")
        assert p.os == "macos"

    def test_proxy_assignment(self):
        p = BrowserProfile.random(proxy="http://user:pass@proxy.example.com:8080")
        assert p.proxy is not None
        assert p.proxy.host == "proxy.example.com"

    def test_randomize_fingerprint(self):
        p = BrowserProfile.random()
        old_ua = p.fingerprint.user_agent
        p.randomize_fingerprint()
        # New fingerprint should be a valid Fingerprint (may occasionally match, test type)
        assert isinstance(p.fingerprint, Fingerprint)

    def test_rotate_proxy(self):
        p = BrowserProfile.random()
        proxies = ["http://a.com:8080", "http://b.com:3128"]
        p.rotate_proxy(proxies)
        assert p.proxy is not None
        assert p.proxy.host in ("a.com", "b.com")

    def test_serialization_roundtrip(self):
        p = BrowserProfile.random(os="linux", driver="http")
        d = p.to_dict()
        p2 = BrowserProfile.from_dict(d)
        assert p2.id == p.id
        assert p2.name == p.name
        assert p2.os == p.os
        assert p2.fingerprint.user_agent == p.fingerprint.user_agent

    def test_json_roundtrip(self):
        p = BrowserProfile.random()
        j = p.to_json()
        p2 = BrowserProfile.from_json(j)
        assert p2.id == p.id

    def test_save_load(self):
        p = BrowserProfile.random()
        with tempfile.TemporaryDirectory() as tmp:
            path = p.save(Path(tmp) / "test_profile.json")
            p2 = BrowserProfile.load(path)
        assert p2.id == p.id
        assert p2.fingerprint.timezone == p.fingerprint.timezone

    def test_batch(self):
        profiles = BrowserProfile.batch(5, driver="http", name_prefix="Test")
        assert len(profiles) == 5
        ids = {p.id for p in profiles}
        assert len(ids) == 5  # all unique
        for p in profiles:
            assert p.name.startswith("Test-")
            assert p.driver == "http"

    def test_batch_with_proxies(self):
        proxies = ["http://a.com:8080", "http://b.com:3128", "http://c.com:9090"]
        profiles = BrowserProfile.batch(6, driver="http", proxies=proxies)
        for p in profiles:
            assert p.proxy is not None
