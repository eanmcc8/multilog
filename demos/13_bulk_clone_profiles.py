#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: bulk clone profiles via Cloud API."""
import os

from mlx import MultiloginX
from mlx.console import banner, fail, ok, progress, section, table, timestamp
from mlx.env import load_env

load_env()


def main():
    source_id = os.getenv("CLONE_SOURCE_ID", os.getenv("MLX_PROFILE_ID", ""))
    folder_id = os.getenv("MLX_FOLDER_ID", "")
    count = int(os.getenv("CLONE_COUNT", "3"))
    prefix = os.getenv("CLONE_PREFIX", "Clone")

    if not source_id or not folder_id:
        raise SystemExit("Set MLX_PROFILE_ID (source) and MLX_FOLDER_ID in .env")

    banner("Bulk Profile Clone", f"Cloud API  |  {timestamp()}")
    mlx = MultiloginX()
    section(f"Cloning {count} profile(s) from {source_id[:12]}...")

    created = []
    for i in range(1, count + 1):
        progress(i - 1, count, "cloning")
        name = f"{prefix}-{i:03d}"
        try:
            result = mlx.clone_profile(source_id, folder_id, name)
            pid = result.get("data", {}).get("profile_id", "?")
            created.append([name, str(pid)[:12], "OK"])
            ok(f"{name} -> {pid[:12]}")
        except Exception as exc:
            created.append([name, "-", "FAIL"])
            fail(str(exc))
        progress(i, count)

    section("Results")
    table(["Name", "New ID", "Status"], created)
    print()


if __name__ == "__main__":
    main()
