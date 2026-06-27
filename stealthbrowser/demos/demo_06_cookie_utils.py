"""Demo 06 — Cookie utilities: save, load, merge, rotate."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from stealthbrowser.cookies import (
    cookies_from_header,
    cookies_to_header,
    filter_cookies,
    load_cookies,
    merge_cookies,
    save_cookies,
)

cookies_a = [
    {"name": "session_id", "value": "abc123", "domain": ".example.com", "path": "/"},
    {"name": "theme", "value": "dark", "domain": ".example.com", "path": "/"},
    {"name": "tracking", "value": "xyz", "domain": ".ads.com", "path": "/"},
]

cookies_b = [
    {"name": "session_id", "value": "NEW_SESSION", "domain": ".example.com", "path": "/"},
    {"name": "lang", "value": "en", "domain": ".example.com", "path": "/"},
]

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "cookies.json"
    save_cookies(cookies_a, path)
    loaded = load_cookies(path)
    print("Saved & loaded:", len(loaded), "cookies")

filtered = filter_cookies(cookies_a, "example.com")
print("Filtered (example.com):", [c["name"] for c in filtered])

merged = merge_cookies(cookies_a, cookies_b)
print("Merged:", {c["name"]: c["value"] for c in merged})

header = cookies_to_header(cookies_a)
print("Header:", header)

reparsed = cookies_from_header(header)
print("Reparsed:", [c["name"] for c in reparsed])
