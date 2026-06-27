"""StealthSession — unified sync/async entry point.

Automatically picks the right driver backend based on BrowserProfile.driver.

Async (Playwright):
    async with StealthSession(profile) as s:
        await s.get("https://example.com")
        print(await s.title())

Sync (Selenium or HTTP):
    with StealthSession(profile) as s:
        s.get("https://example.com")
        print(s.title())
"""
from __future__ import annotations

import asyncio
from typing import Any

from stealthbrowser.profile import BrowserProfile


class StealthSession:
    """Unified session wrapper — delegates to the right backend driver."""

    def __init__(self, profile: BrowserProfile) -> None:
        self.profile = profile
        self._driver = None

    # ------------------------------------------------------------------
    # Driver resolution
    # ------------------------------------------------------------------

    def _make_driver(self):
        d = self.profile.driver
        if d == "playwright":
            from stealthbrowser.drivers.playwright_driver import PlaywrightDriver
            return PlaywrightDriver(self.profile)
        elif d == "selenium":
            from stealthbrowser.drivers.selenium_driver import SeleniumDriver
            return SeleniumDriver(self.profile)
        elif d == "http":
            from stealthbrowser.drivers.http_driver import HTTPDriver
            return HTTPDriver(self.profile)
        else:
            raise ValueError(f"Unknown driver: {d!r}. Choose 'playwright', 'selenium', or 'http'.")

    # ------------------------------------------------------------------
    # Sync context manager (Selenium / HTTP)
    # ------------------------------------------------------------------

    def __enter__(self) -> "StealthSession":
        self._driver = self._make_driver()
        if hasattr(self._driver, "start"):
            self._driver.start()
        return self

    def __exit__(self, *_) -> None:
        if self._driver and hasattr(self._driver, "stop"):
            self._driver.stop()

    # ------------------------------------------------------------------
    # Async context manager (Playwright)
    # ------------------------------------------------------------------

    async def __aenter__(self) -> "StealthSession":
        self._driver = self._make_driver()
        if hasattr(self._driver, "__aenter__"):
            await self._driver.__aenter__()
        return self

    async def __aexit__(self, *args) -> None:
        if self._driver and hasattr(self._driver, "__aexit__"):
            await self._driver.__aexit__(*args)

    # ------------------------------------------------------------------
    # Proxied attribute access — forward everything to the driver
    # ------------------------------------------------------------------

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        driver = object.__getattribute__(self, "_driver")
        if driver is None:
            raise RuntimeError("StealthSession not started.  Use it as a context manager.")
        return getattr(driver, name)

    # ------------------------------------------------------------------
    # Convenience: run an async playwright task synchronously
    # ------------------------------------------------------------------

    @staticmethod
    def run_async(coro) -> Any:
        """Run a coroutine in a new event loop (helper for sync contexts)."""
        return asyncio.run(coro)

    # ------------------------------------------------------------------
    # Quick factory helpers
    # ------------------------------------------------------------------

    @classmethod
    def playwright(cls, **profile_kwargs) -> "StealthSession":
        p = BrowserProfile.random(driver="playwright", **profile_kwargs)
        return cls(p)

    @classmethod
    def selenium(cls, **profile_kwargs) -> "StealthSession":
        p = BrowserProfile.random(driver="selenium", **profile_kwargs)
        return cls(p)

    @classmethod
    def http(cls, **profile_kwargs) -> "StealthSession":
        p = BrowserProfile.random(driver="http", **profile_kwargs)
        return cls(p)
