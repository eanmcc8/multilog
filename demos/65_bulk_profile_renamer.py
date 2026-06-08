#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: bulk rename profiles with prefix/suffix."""
import os

from mlx import MultiloginX
from mlx.console import banner, ok, progress, section, table, timestamp
from mlx.env import load_env, require_env
from mlx.profiles import normalize_profiles, profile_id

load_env()


def main():
    env = require_env("MLX_FOLDER_ID")
    prefix = os.getenv("RENAME_PREFIX", "Farm")
    limit = int(os.getenv("RENAME_LIMIT", "10"))
    dry = os.getenv("RENAME_DRY_RUN", "true").lower() != "false"

    banner("Bulk Profile Renamer", f"prefix={prefix}  |  {timestamp()}")
    mlx = MultiloginX()
    profs = normalize_profiles(mlx.search_profiles(limit=limit, folder_id=env["MLX_FOLDER_ID"]))[:limit]
    section(f"Renaming {len(profs)} profile(s)")
    rows: list[list[str]] = []
    for i, p in enumerate(profs, 1):
        pid = profile_id(p)
        old = p.get("name", pid[:8])
        new = f"{prefix}-{i:03d}"
        progress(i - 1, len(profs), old)
        if dry:
            rows.append([old, new, "DRY-RUN"])
        else:
            try:
                mlx.update_profile(pid, name=new)
                rows.append([old, new, "OK"])
                ok(f"{old} -> {new}")
            except Exception:
                rows.append([old, new, "FAIL"])
        progress(i, len(profs))

    table(["Old", "New", "Status"], rows)
    if dry:
        ok("Set RENAME_DRY_RUN=false to apply")


if __name__ == "__main__":
    main()
