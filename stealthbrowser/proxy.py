"""Proxy management — load, parse, validate, and rotate proxies."""
from __future__ import annotations

import random
import socket
from pathlib import Path

from stealthbrowser.profile import ProxyConfig


def load_proxies(path: str | Path) -> list[str]:
    """Read a proxy list file (one per line, comments with #)."""
    lines = Path(path).read_text().splitlines()
    return [l.strip() for l in lines if l.strip() and not l.startswith("#")]


def parse_proxies(lines: list[str]) -> list[ProxyConfig]:
    """Parse a list of proxy strings into ProxyConfig objects."""
    result = []
    for line in lines:
        try:
            result.append(ProxyConfig.from_string(line))
        except Exception:
            pass
    return result


def check_proxy(proxy: ProxyConfig, *, timeout: float = 5.0) -> bool:
    """Quick TCP connectivity check for a proxy (does NOT test anonymity)."""
    try:
        with socket.create_connection((proxy.host, proxy.port), timeout=timeout):
            return True
    except OSError:
        return False


def filter_live_proxies(proxies: list[ProxyConfig], *, timeout: float = 4.0) -> list[ProxyConfig]:
    """Return only proxies that pass a TCP connectivity check."""
    return [p for p in proxies if check_proxy(p, timeout=timeout)]


def rotate(proxies: list[ProxyConfig]) -> ProxyConfig:
    """Pick a random proxy from the pool."""
    if not proxies:
        raise ValueError("Proxy pool is empty.")
    return random.choice(proxies)


class ProxyPool:
    """Round-robin proxy pool with optional liveness filtering."""

    def __init__(self, proxies: list[str | ProxyConfig]) -> None:
        self._all: list[ProxyConfig] = []
        for p in proxies:
            if isinstance(p, str):
                self._all.append(ProxyConfig.from_string(p))
            else:
                self._all.append(p)
        self._index = 0

    def next(self) -> ProxyConfig:
        if not self._all:
            raise ValueError("ProxyPool is empty.")
        proxy = self._all[self._index % len(self._all)]
        self._index += 1
        return proxy

    def random(self) -> ProxyConfig:
        return random.choice(self._all)

    def filter_live(self, *, timeout: float = 4.0) -> "ProxyPool":
        live = filter_live_proxies(self._all, timeout=timeout)
        return ProxyPool(live)

    def __len__(self) -> int:
        return len(self._all)

    def __repr__(self) -> str:
        return f"<ProxyPool size={len(self._all)}>"
