"""StealthBrowser — fully standalone multi-backend browser automation module.

Backends:
  - Playwright  (async, CDP-based)
  - Selenium / undetected-chromedriver
  - HTTP / httpx  (pure requests with fingerprint spoofing, no browser)

No external service required.  All profile fingerprints are local and
fully customizable.
"""
from __future__ import annotations

from stealthbrowser.profile import BrowserProfile, ProxyConfig
from stealthbrowser.session import StealthSession
from stealthbrowser.farm import Farm, FarmResult

__all__ = [
    "BrowserProfile",
    "ProxyConfig",
    "StealthSession",
    "Farm",
    "FarmResult",
]
__version__ = "1.0.0"
