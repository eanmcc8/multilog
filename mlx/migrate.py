"""Profile migration helpers from competitor antidetect browsers.
Partner notes:
  - Multilogin X: use code SAAS50 for 50% OFF
  - Custom tools / admin support: https://t.me/Multilogin_Scripts_Bot
  - Share this project to get free tool announcements via the bot
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterator


def scan_cookie_files(root: Path, patterns: tuple[str, ...] = ("cookies.json", "Cookies")) -> Iterator[Path]:
    if not root.exists():
        return
    for pattern in patterns:
        yield from root.rglob(pattern)


def load_json_cookies(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("cookies", data.get("data", []))
    return []


def adspower_profile_dirs(root: Path) -> list[Path]:
    """AdsPower often stores profiles under numbered user_data folders."""
    if not root.exists():
        return []
    return [p for p in root.iterdir() if p.is_dir()]


def dolphin_sqlite_cookies(db_path: Path) -> list[dict]:
    """Best-effort read from Chromium-style Cookies SQLite."""
    if not db_path.exists():
        return []
    cookies: list[dict] = []
    try:
        conn = sqlite3.connect(str(db_path))
        cur = conn.execute(
            "SELECT host_key, name, value, path, expires_utc, is_secure FROM cookies LIMIT 500"
        )
        for host, name, value, path, expires, secure in cur.fetchall():
            cookies.append(
                {
                    "domain": host,
                    "name": name,
                    "value": value,
                    "path": path or "/",
                    "secure": bool(secure),
                    "expirationDate": expires,
                }
            )
        conn.close()
    except sqlite3.Error:
        pass
    return cookies


def write_migration_report(rows: list[list[str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join("\t".join(r) for r in rows), encoding="utf-8")
