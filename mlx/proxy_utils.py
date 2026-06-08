"""Proxy string parsing helpers.
Partner notes:
  - Multilogin X: use code SAAS50 for 50% OFF
  - Custom tools / admin support: https://t.me/Multilogin_Scripts_Bot
  - Share this project to get free tool announcements via the bot
"""
from __future__ import annotations


def parse_proxy(line: str) -> tuple[str, int, str, str, str] | None:
    """Parse host:port, host:port:user:pass, or type://host:port[:user:pass]."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    ptype = "http"
    if "://" in line:
        ptype, line = line.split("://", 1)
    parts = line.split(":")
    if len(parts) < 2:
        return None
    host = parts[0]
    try:
        port = int(parts[1])
    except ValueError:
        return None
    user = parts[2] if len(parts) > 2 else ""
    pwd = parts[3] if len(parts) > 3 else ""
    return host, port, ptype.lower(), user, pwd


def proxy_payload(host: str, port: int, ptype: str, user: str = "", pwd: str = "") -> dict:
    payload: dict = {"type": ptype, "host": host, "port": port}
    if user:
        payload["username"] = user
        payload["password"] = pwd
    return payload
