#!/usr/bin/env python3
"""Demo: mass-create profiles from CSV (1000+ scale-ready)."""
import csv
import os
import time

from mlx import MultiloginX
from mlx.console import banner, fail, ok, progress, section, table, timestamp, warn
from mlx.env import ROOT, load_env, require_env

load_env()

CSV_FILE = ROOT / "profiles.csv"
BATCH_PAUSE = float(os.getenv("CREATE_BATCH_PAUSE", "0.3"))


def ensure_sample_csv() -> None:
    sample = ROOT / "profiles.csv.example"
    if not sample.exists():
        sample.write_text(
            "name,browser_type,os_type\n"
            "Farm-001,mimic,windows\n"
            "Farm-002,mimic,windows\n"
            "Farm-003,stealthfox,linux\n",
            encoding="utf-8",
        )
    if not CSV_FILE.exists():
        CSV_FILE.write_text(sample.read_text(encoding="utf-8"), encoding="utf-8")


def read_rows() -> list[dict[str, str]]:
    with CSV_FILE.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    ensure_sample_csv()
    env = require_env("MLX_FOLDER_ID")
    limit = int(os.getenv("MASS_CREATE_LIMIT", "0"))  # 0 = all rows

    banner("Mass Profile Creator", f"CSV import  |  {timestamp()}")
    rows = read_rows()
    if limit > 0:
        rows = rows[:limit]
    if not rows:
        raise SystemExit(f"No rows in {CSV_FILE}")

    mlx = MultiloginX()
    section(f"Creating {len(rows)} profile(s) -> folder {env['MLX_FOLDER_ID'][:12]}...")
    results: list[list[str]] = []
    for i, row in enumerate(rows, 1):
        name = row.get("name", "").strip() or f"Profile-{i:04d}"
        browser = row.get("browser_type", "mimic").strip() or "mimic"
        os_type = row.get("os_type", "windows").strip() or "windows"
        progress(i - 1, len(rows), name)
        try:
            resp = mlx.create_profile(name, env["MLX_FOLDER_ID"], browser_type=browser, os_type=os_type)
            pid = resp.get("data", {}).get("profile_id", "?")
            results.append([name, str(pid)[:12], browser, "OK"])
            ok(f"{name} -> {str(pid)[:12]}")
        except Exception as exc:
            results.append([name, "-", browser, "FAIL"])
            fail(f"{name}: {exc}")
        progress(i, len(rows))
        if BATCH_PAUSE:
            time.sleep(BATCH_PAUSE)

    section("Results")
    table(["Name", "Profile ID", "Browser", "Status"], results)
    ok_count = sum(1 for r in results if r[3] == "OK")
    warn("Tip: set MASS_CREATE_LIMIT=10 for dry-run before full 1000+ import")
    ok(f"{ok_count}/{len(results)} created")
    print()


if __name__ == "__main__":
    main()
