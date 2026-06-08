#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: restore cookies from JSON backup into a profile."""
import json
import os
from pathlib import Path

from mlx import MultiloginX
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import ensure_output, load_env, require_env

load_env()


def main():
    env = require_env("MLX_PROFILE_ID")
    profile_id = env["MLX_PROFILE_ID"]
    backup = os.getenv("COOKIE_BACKUP", "")

    if not backup:
        out = ensure_output()
        candidates = sorted(out.glob("cookies_*.json"))
        if not candidates:
            raise SystemExit("No backup found in output/ - run 04_cookie_backup.py first")
        backup = str(candidates[-1])

    path = Path(backup)
    if not path.exists():
        raise SystemExit(f"Backup not found: {path}")

    banner("Cookie Restore", f"Import session to profile  |  {timestamp()}")
    cookies = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(cookies, list):
        warn("Unexpected format - wrapping as list")
        cookies = [cookies]

    section(f"Import {len(cookies)} cookies")
    section(f"Target profile: {profile_id[:12]}...")
    section(f"Source file: {path.name}")

    mlx = MultiloginX()
    mlx.import_cookies(profile_id, cookies)
    ok(f"Imported {len(cookies)} cookies into profile {profile_id[:12]}")


if __name__ == "__main__":
    main()
