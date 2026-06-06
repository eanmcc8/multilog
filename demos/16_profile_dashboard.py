#!/usr/bin/env python3
"""Demo: full profile dashboard with formatted tables."""
import os

from mlx import MultiloginX
from mlx.console import banner, fail, ok, section, table, timestamp
from mlx.env import load_env
from mlx.profiles import normalize_folders, normalize_profiles, profile_id

load_env()


def main():
    banner("Profile Dashboard", f"Multilogin X overview  |  {timestamp()}")
    mlx = MultiloginX()

    section("Workspaces")
    workspaces = mlx.get_workspaces()
    table(
        ["Name", "ID"],
        [[str(w.get("name", "?")), str(w.get("id", w.get("workspace_id", "")))[:12]] for w in workspaces],
    )

    section("Folders")
    folders = normalize_folders(mlx.get_folders())
    table(
        ["Name", "Folder ID"],
        [[f.get("name", "?"), str(f.get("folder_id", f.get("id", "")))[:12]] for f in folders],
    )

    section("Profiles")
    folder_id = os.getenv("MLX_FOLDER_ID", "")
    result = mlx.search_profiles(limit=50, folder_id=folder_id)
    profiles = normalize_profiles(result)
    data = result.get("data", result)
    info_total = str(data.get("total", len(profiles)))
    table(
        ["Name", "Profile ID", "Browser"],
        [
            [
                p.get("name", "unnamed"),
                profile_id(p)[:12],
                p.get("browser_type", "?"),
            ]
            for p in profiles[:20]
        ],
    )
    if len(profiles) > 20:
        ok(f"Showing 20 of {info_total} profiles")

    section("Active Sessions")
    try:
        active = mlx.get_active_profiles()
        active_data = active.get("data", active)
        if isinstance(active_data, list):
            ok(f"{len(active_data)} profile(s) running")
        else:
            ok("Active profile data retrieved")
    except Exception as exc:
        fail(str(exc))

    section("Summary")
    try:
        summary = mlx.get_profile_summary()
        ok("Profile summary fetched")
        data = summary.get("data", summary)
        if isinstance(data, dict):
            for k, v in list(data.items())[:8]:
                print(f"    {k}: {v}")
    except Exception as exc:
        fail(str(exc))

    print()


if __name__ == "__main__":
    main()
