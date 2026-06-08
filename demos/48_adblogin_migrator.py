#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: migrate cookies/profiles from ADBLogin folders into Multilogin X."""
import os
from pathlib import Path

from mlx import MultiloginX
from mlx.console import banner, fail, ok, progress, section, table, timestamp, warn
from mlx.cookies import load_cookies, save_cookies
from mlx.env import ROOT, ensure_output, load_env, require_env
from mlx.migrate import scan_cookie_files, write_migration_report

load_env()


def main():
    env = require_env("MLX_FOLDER_ID")
    source = Path(os.getenv("ADBLOGIN_DATA_DIR", str(ROOT / "migration" / "adblogin")))
    limit = int(os.getenv("MIGRATE_LIMIT", "10"))

    banner("ADBLogin → Multilogin Migrator", f"Bulk cookie import  |  {timestamp()}")
    warn("Large migrations require deep hardware fingerprint — see README Important Note")

    if not source.exists():
        source.mkdir(parents=True)
        sample = source / "profile_001" / "cookies.json"
        sample.parent.mkdir(parents=True, exist_ok=True)
        sample.write_text('[{"domain":".example.com","name":"sid","value":"demo","path":"/"}]', encoding="utf-8")
        raise SystemExit(f"Created sample at {source} — add ADBLogin exports and re-run")

    cookie_files = list(scan_cookie_files(source))[:limit]
    if not cookie_files:
        raise SystemExit(f"No cookie files under {source}")

    mlx = MultiloginX()
    search = mlx.search_profiles(limit=limit, folder_id=env["MLX_FOLDER_ID"])
    from mlx.profiles import normalize_profiles, profile_id

    profiles = normalize_profiles(search)[:limit]
    if not profiles:
        raise SystemExit("Create target profiles in MLX folder first (demo 19)")

    section(f"Migrating {min(len(cookie_files), len(profiles))} profile(s)")
    rows: list[list[str]] = []
    for i, (cf, prof) in enumerate(zip(cookie_files, profiles, strict=False), 1):
        pid = profile_id(prof)
        name = prof.get("name", pid[:8])
        progress(i - 1, min(len(cookie_files), len(profiles)), name)
        try:
            cookies = load_cookies(cf)
            mlx.import_cookies(pid, cookies)
            backup = ensure_output() / "migrated" / f"{name}_{pid[:8]}.json"
            save_cookies(cookies, backup)
            rows.append([name, cf.name, str(len(cookies)), "OK"])
            ok(f"{name} <- {cf.name}")
        except Exception as exc:
            rows.append([name, cf.name, "-", "FAIL"])
            fail(str(exc))
        progress(i, min(len(cookie_files), len(profiles)))

    section("Migration report")
    table(["Profile", "Source", "Cookies", "Status"], rows)
    report = ensure_output() / "adblogin_migration.txt"
    write_migration_report(rows, report)
    ok(f"Report -> {report}")
    print()


if __name__ == "__main__":
    main()
