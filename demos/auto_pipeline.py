#!/usr/bin/env python3
"""One-click automation pipeline — API health + optional farm (no interaction)."""
from __future__ import annotations

import os
import sys

from mlx import MultiloginX
from mlx.console import banner, fail, ok, section, table, timestamp, warn
from mlx.env import load_env
from mlx.farm import run_api_pipeline

load_env()

API_STEPS = [
    "folders",
    "workspaces",
    "summary",
    "launcher_version",
    "active_profiles",
    "search_profiles",
]


def main() -> int:
    banner("Auto Pipeline", f"Full API health check  |  {timestamp()}")
    folder_id = os.getenv("MLX_FOLDER_ID", "")

    if not os.getenv("MLX_EMAIL") and not os.getenv("MLX_TOKEN"):
        warn("No MLX credentials — copy .env.example to .env and fill in values")
        return 1

    mlx = MultiloginX()
    section("Phase 1: Cloud + Launcher API")
    results = run_api_pipeline(mlx, folder_id=folder_id)
    rows = [[r["step"], r["status"], r.get("error", "")[:40]] for r in results]
    table(["Step", "Status", "Note"], rows)

    ok_count = sum(1 for r in results if r["status"] == "OK")
    if ok_count == 0:
        fail("All API steps failed — check .env and Multilogin X launcher")
        return 1

    section("Phase 2: Ready checks")
    checks = [
        ("profiles.csv", "Mass create (demo 19)"),
        ("proxies.txt", "Proxy rotator (demo 20)"),
        ("keywords.txt", "Google farmer (demo 26)"),
    ]
    for fname, label in checks:
        path = os.path.join(os.path.dirname(__file__), "..", fname)
        if os.path.exists(path):
            ok(f"{label} — {fname} found")
        else:
            warn(f"{label} — copy {fname}.example -> {fname}")

    if folder_id and os.getenv("AUTO_FARM", "").lower() in ("1", "true", "yes"):
        section("Phase 3: Bulk farm (AUTO_FARM=true)")
        warn("Run: set FARM_DEMO=24 && python demos/03_bulk_farm.py")

    ok(f"Pipeline complete ({ok_count}/{len(results)} API steps OK)")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
