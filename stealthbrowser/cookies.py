"""Cookie utilities — import / export / rotate across profiles."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def save_cookies(cookies: list[dict], path: str | Path) -> Path:
    """Save a cookie list to a JSON file."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(cookies, indent=2))
    return p


def load_cookies(path: str | Path) -> list[dict]:
    """Load cookies from a JSON file."""
    return json.loads(Path(path).read_text())


def filter_cookies(cookies: list[dict], domain: str) -> list[dict]:
    """Return only cookies matching *domain* (partial match)."""
    return [c for c in cookies if domain in c.get("domain", "")]


def merge_cookies(base: list[dict], extra: list[dict]) -> list[dict]:
    """Merge two cookie lists, with *extra* taking precedence."""
    index = {c["name"]: c for c in base}
    for c in extra:
        index[c["name"]] = c
    return list(index.values())


def cookies_to_header(cookies: list[dict]) -> str:
    """Format cookies as a Cookie header string."""
    return "; ".join(f"{c['name']}={c['value']}" for c in cookies)


def cookies_from_header(header: str) -> list[dict]:
    """Parse a Cookie header string into a list of dicts."""
    result = []
    for part in header.split(";"):
        part = part.strip()
        if "=" in part:
            name, _, value = part.partition("=")
            result.append({"name": name.strip(), "value": value.strip()})
    return result
