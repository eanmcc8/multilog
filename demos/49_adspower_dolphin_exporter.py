#!/usr/bin/env python3
"""Demo: export cookies from AdsPower / Dolphin and import into Multilogin X."""
import os
from pathlib import Path

from mlx import MultiloginX
from mlx.console import banner, fail, ok, progress, section, table, timestamp, warn
from mlx.cookies import save_cookies
from mlx.env import ROOT, ensure_output, load_env, require_env
from mlx.migrate import (
    adspower_profile_dirs,
    dolphin_sqlite_cookies,
    load_json_cookies,
    write_migration_report,
)
from mlx.profiles import normalize_profiles, profile_id

load_env()


def extract_cookies(source: Path, vendor: str) -> list[dict]:
    if vendor == "dolphin":
        db = source / "Default" / "Cookies"
        if not db.exists():
            db = source / "Cookies"
        return dolphin_sqlite_cookies(db)
    for name in ("cookies.json", "Cookies.json", "cookie.json"):
        p = source / name
        if p.exists():
            return load_json_cookies(p)
    for found in source.rglob("cookies.json"):
        return load_json_cookies(found)
    return []


def main():
    env = require_env("MLX_FOLDER_ID")
    vendor = os.getenv("EXPORT_VENDOR", "adspower").lower()
    source = Path(os.getenv("EXPORT_SOURCE_DIR", str(ROOT / "migration" / vendor)))
    limit = int(os.getenv("MIGRATE_LIMIT", "10"))

    banner("AdsPower / Dolphin Exporter", f"Import to MLX  |  {timestamp()}")
    warn("Large migrations require deep hardware fingerprint — see README Important Note")

    if not source.exists():
        source.mkdir(parents=True)
        raise SystemExit(f"Set EXPORT_SOURCE_DIR — place {vendor} profile folders in {source}")

    dirs = adspower_profile_dirs(source)[:limit]
    if not dirs:
        dirs = [source]

    mlx = MultiloginX()
    profiles = normalize_profiles(mlx.search_profiles(limit=limit, folder_id=env["MLX_FOLDER_ID"]))[:limit]
    if not profiles:
        raise SystemExit("Create MLX profiles first (demo 19)")

    section(f"Export {vendor} -> MLX ({min(len(dirs), len(profiles))} items)")
    rows: list[list[str]] = []
    out_dir = ensure_output() / "exported" / vendor
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, (src_dir, prof) in enumerate(zip(dirs, profiles, strict=False), 1):
        pid = profile_id(prof)
        name = prof.get("name", pid[:8])
        progress(i - 1, min(len(dirs), len(profiles)), name)
        try:
            cookies = extract_cookies(src_dir, vendor)
            if not cookies:
                rows.append([name, src_dir.name, "0", "EMPTY"])
                fail(f"No cookies in {src_dir.name}")
                continue
            backup = out_dir / f"{name}_{pid[:8]}.json"
            save_cookies(cookies, backup)
            mlx.import_cookies(pid, cookies)
            rows.append([name, src_dir.name, str(len(cookies)), "OK"])
            ok(f"{name} <- {src_dir.name} ({len(cookies)} cookies)")
        except Exception as exc:
            rows.append([name, src_dir.name, "-", "FAIL"])
            fail(str(exc))
        progress(i, min(len(dirs), len(profiles)))

    section("Export summary")
    table(["MLX Profile", "Source Dir", "Cookies", "Status"], rows)
    write_migration_report(rows, ensure_output() / f"{vendor}_export.txt")
    print()


if __name__ == "__main__":
    main()
