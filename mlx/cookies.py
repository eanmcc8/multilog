"""Cookie format conversion (JSON <-> Netscape)."""
from __future__ import annotations

import json
from pathlib import Path


def load_cookies(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8").strip()
    if path.suffix.lower() == ".json":
        data = json.loads(text)
        if isinstance(data, dict) and "cookies" in data:
            return data["cookies"]
        if isinstance(data, list):
            return data
        raise ValueError("JSON must be a cookie list or {cookies: [...]}")
    return parse_netscape(text)


def parse_netscape(text: str) -> list[dict]:
    cookies: list[dict] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 7:
            continue
        domain, _flag, path, secure, expiry, name, value = parts[:7]
        cookies.append(
            {
                "domain": domain,
                "path": path,
                "name": name,
                "value": value,
                "secure": secure.upper() == "TRUE",
                "httpOnly": False,
                "expirationDate": int(expiry) if expiry.isdigit() else None,
            }
        )
    return cookies


def to_netscape(cookies: list[dict]) -> str:
    lines = ["# Netscape HTTP Cookie File"]
    for c in cookies:
        domain = c.get("domain", "")
        if domain and not domain.startswith("."):
            domain = f".{domain.lstrip('.')}"
        path = c.get("path", "/")
        secure = "TRUE" if c.get("secure") else "FALSE"
        expiry = str(int(c.get("expirationDate") or c.get("expires") or 0))
        name = c.get("name", "")
        value = c.get("value", "")
        lines.append(f"{domain}\tTRUE\t{path}\t{secure}\t{expiry}\t{name}\t{value}")
    return "\n".join(lines) + "\n"


def save_cookies(cookies: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".json":
        path.write_text(json.dumps(cookies, indent=2), encoding="utf-8")
    else:
        path.write_text(to_netscape(cookies), encoding="utf-8")
