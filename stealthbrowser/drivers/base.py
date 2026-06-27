"""Base driver interface — all backends implement this contract."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseDriver(ABC):
    """Common interface for all StealthBrowser backends."""

    def __init__(self, profile) -> None:
        self.profile = profile
        self._started = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    @abstractmethod
    def start(self) -> "BaseDriver":
        """Launch / initialise the driver.  Returns self for chaining."""

    @abstractmethod
    def stop(self) -> None:
        """Tear down the driver cleanly."""

    def __enter__(self) -> "BaseDriver":
        return self.start()

    def __exit__(self, *_) -> None:
        self.stop()

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    @abstractmethod
    def get(self, url: str) -> None:
        """Navigate to *url*."""

    @abstractmethod
    def current_url(self) -> str:
        """Return the current page URL."""

    @abstractmethod
    def title(self) -> str:
        """Return the current page title."""

    @abstractmethod
    def source(self) -> str:
        """Return the raw page HTML / response body."""

    # ------------------------------------------------------------------
    # Interaction (best-effort — HTTP driver returns None)
    # ------------------------------------------------------------------

    def find(self, selector: str) -> Any:
        return None

    def click(self, selector: str) -> None:
        pass

    def type(self, selector: str, text: str) -> None:
        pass

    def screenshot(self, path: str) -> None:
        pass

    # ------------------------------------------------------------------
    # Cookies
    # ------------------------------------------------------------------

    def get_cookies(self) -> list[dict]:
        return []

    def set_cookies(self, cookies: list[dict]) -> None:
        pass

    def clear_cookies(self) -> None:
        pass

    # ------------------------------------------------------------------
    # JavaScript execution (no-op for HTTP driver)
    # ------------------------------------------------------------------

    def execute_js(self, script: str, *args) -> Any:
        return None

    # ------------------------------------------------------------------
    # Meta
    # ------------------------------------------------------------------

    @property
    def backend(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"<{self.backend} profile={self.profile.name!r} started={self._started}>"
