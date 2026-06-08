#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: sync Incogniton backup data into new Multilogin profiles."""
import os
from pathlib import Path

from mlx import MultiloginX
from mlx.console import banner, ok, progress, section, table, timestamp, warn
from mlx.cookies import load_cookies, save_cookies
from mlx.env import ROOT, ensure_output, load_env, require_env
from mlx.migrate import scan_cookie_files, write_migration_report
from mlx.profiles import normalize_profiles, profile_id

load_env()


def main():
    env = require_env("MLX_FOLDER_ID")
    backup_dir = Path(os.getenv("INCOGNITON_BACKUP_DIR", str(ROOT / "migration" / "incogniton")))
    limit = int(os.getenv("MIGRATE_LIMIT", "10"))

    banner("Incogniton Backup Sync", f"Restore to MLX  |  {timestamp()}")
    warn("Large migrations require deep hardware fingerprint — see README Important Note")

    if not backup_dir.exists():
        backup_dir.mkdir(parents=True)
        sample = backup_dir / "profile_backup_001.json"
        sample.write_text(
            '[{"domain":".incogniton.test","name":"session","value":"1","path":"/"}]',
            encoding="utf-8",
        )
        raise SystemExit(f"Place Incogniton backups in {backup_dir} and re-run")

    files = list(scan_cookie_files(backup_dir, ("*.json",)))[:limit]
    if not files:
        files = list(backup_dir.glob("*.json"))[:limit]
    if not files:
        raise SystemExit("No backup JSON files found")

    mlx = MultiloginX()
    profiles = normalize_profiles(mlx.search_profiles(limit=limit, folder_id=env["MLX_FOLDER_ID"]))[:limit]

    section(f"Syncing {min(len(files), len(profiles))} backup(s)")
    rows: list[list[str]] = []
    sync_dir = ensure_output() / "incogniton_sync"
    sync_dir.mkdir(parents=True, exist_ok=True)

    for i, (bf, prof) in enumerate(zip(files, profiles, strict=False), 1):
        pid = profile_id(prof)
        name = prof.get("name", pid[:8])
        progress(i - 1, min(len(files), len(profiles)), name)
        try:
            cookies = load_cookies(bf)
            mlx.import_cookies(pid, cookies)
            save_cookies(cookies, sync_dir / f"{name}.json")
            rows.append([name, bf.name, str(len(cookies)), "OK"])
            ok(f"{name} synced")
        except Exception as exc:
            rows.append([name, bf.name, "-", "FAIL"])
            warn(str(exc))
        progress(i, min(len(files), len(profiles)))

    section("Sync report")
    table(["Profile", "Backup", "Cookies", "Status"], rows)
    write_migration_report(rows, ensure_output() / "incogniton_sync.txt")
    print()


if __name__ == "__main__":
    main()
