"""Pure-HTTP backend — no real browser, maximum speed and stealth.

Uses httpx (with optional HTTP/2) and injects realistic headers derived from
the BrowserProfile fingerprint.  Ideal for scraping, API testing, and cookie
farming where a DOM isn't needed.

Falls back to the stdlib `urllib` if httpx is not installed.
"""
from __future__ import annotations

import json
import random
import re
from http.cookiejar import CookieJar
from typing import Any
from urllib.parse import urlparse

from stealthbrowser.drivers.base import BaseDriver


class HTTPDriver(BaseDriver):
    """Stateful HTTP session that looks like a real browser."""

    def __init__(self, profile) -> None:
        super().__init__(profile)
        self._session = None
        self._last_response = None
        self._last_url: str = ""
        self._use_httpx: bool = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> "HTTPDriver":
        try:
            import httpx
            self._session = self._build_httpx_session()
            self._use_httpx = True
        except ImportError:
            import requests
            self._session = self._build_requests_session()
            self._use_httpx = False
        self._started = True
        return self

    def stop(self) -> None:
        if self._session:
            try:
                self._session.close()
            except Exception:
                pass
        self._started = False

    def __enter__(self) -> "HTTPDriver":
        return self.start()

    def __exit__(self, *_) -> None:
        self.stop()

    # ------------------------------------------------------------------
    # Session builders
    # ------------------------------------------------------------------

    def _common_headers(self) -> dict[str, str]:
        fp = self.profile.fingerprint
        ua = fp.user_agent
        # Determine Accept header style (Chrome vs Firefox vs Safari)
        if "Firefox" in ua:
            accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            sec_ch = {}
        else:
            accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            sec_ch = {
                "sec-ch-ua": f'"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": f'"{fp.platform}"',
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
            }
        headers = {
            "User-Agent": ua,
            "Accept": accept,
            "Accept-Language": f"{fp.locale},{fp.locale.split('-')[0]};q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            **sec_ch,
        }
        if fp.do_not_track:
            headers["DNT"] = "1"
        return headers

    def _build_httpx_session(self):
        import httpx
        proxies = None
        if self.profile.proxy:
            proxies = {"http://": self.profile.proxy.url, "https://": self.profile.proxy.url}
        return httpx.Client(
            headers=self._common_headers(),
            follow_redirects=True,
            verify=True,
            http2=True,
            proxies=proxies,
            timeout=30.0,
        )

    def _build_requests_session(self):
        import requests
        s = requests.Session()
        s.headers.update(self._common_headers())
        if self.profile.proxy:
            s.proxies = {"http": self.profile.proxy.url, "https": self.profile.proxy.url}
        return s

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def get(self, url: str, **kwargs) -> None:
        self._last_response = self._session.get(url, **kwargs)
        self._last_url = url

    def post(self, url: str, **kwargs) -> Any:
        resp = self._session.post(url, **kwargs)
        self._last_response = resp
        self._last_url = url
        return resp

    def request(self, method: str, url: str, **kwargs) -> Any:
        resp = self._session.request(method, url, **kwargs)
        self._last_response = resp
        self._last_url = url
        return resp

    def current_url(self) -> str:
        if self._last_response is None:
            return self._last_url
        if hasattr(self._last_response, "url"):
            return str(self._last_response.url)
        return self._last_url

    def title(self) -> str:
        body = self.source()
        m = re.search(r"<title[^>]*>(.*?)</title>", body, re.IGNORECASE | re.DOTALL)
        return m.group(1).strip() if m else ""

    def source(self) -> str:
        if self._last_response is None:
            return ""
        return self._last_response.text

    def status_code(self) -> int:
        return self._last_response.status_code if self._last_response else 0

    def json(self) -> Any:
        return self._last_response.json() if self._last_response else None

    def headers(self) -> dict:
        return dict(self._last_response.headers) if self._last_response else {}

    # ------------------------------------------------------------------
    # Cookies
    # ------------------------------------------------------------------

    def get_cookies(self) -> list[dict]:
        jar = self._session.cookies
        cookies = []
        for name, value in jar.items():
            cookies.append({"name": name, "value": value})
        return cookies

    def set_cookies(self, cookies: list[dict]) -> None:
        for c in cookies:
            self._session.cookies.set(c.get("name", ""), c.get("value", ""),
                                      domain=c.get("domain", ""), path=c.get("path", "/"))

    def clear_cookies(self) -> None:
        self._session.cookies.clear()

    # ------------------------------------------------------------------
    # Fingerprint probe helpers
    # ------------------------------------------------------------------

    def fingerprint_report(self) -> dict:
        """Return a dict of what this session claims to be."""
        fp = self.profile.fingerprint
        return {
            "user_agent": fp.user_agent,
            "platform": fp.platform,
            "locale": fp.locale,
            "timezone": fp.timezone,
            "resolution": f"{fp.resolution_width}x{fp.resolution_height}",
            "webgl_vendor": fp.webgl_vendor,
            "proxy": self.profile.proxy.url if self.profile.proxy else None,
        }

    # ------------------------------------------------------------------
    # No-op overrides
    # ------------------------------------------------------------------

    def screenshot(self, path: str) -> None:
        pass

    def execute_js(self, script: str, *args) -> Any:
        return None
