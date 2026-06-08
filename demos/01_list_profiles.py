#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: list folders and search profiles."""
import os

from mlx import MultiloginX
from mlx.console import banner, section, table, timestamp
from mlx.env import load_env
from mlx.profiles import normalize_folders, normalize_profiles, profile_id

load_env()


def main():
    banner("Profile Explorer", f"Quick list view  |  {timestamp()}")
    mlx = MultiloginX()

    section("Workspaces")
    table(
        ["Name", "ID"],
        [[str(w.get("name", "?")), str(w.get("id", ""))[:16]] for w in mlx.get_workspaces()],
    )

    section("Folders")
    table(
        ["Name", "Folder ID"],
        [[f.get("name", "?"), str(f.get("folder_id", f.get("id", "")))[:16]] for f in normalize_folders(mlx.get_folders())],
    )

    section("Profiles")
    folder_id = os.getenv("MLX_FOLDER_ID", "")
    result = mlx.search_profiles(limit=30, folder_id=folder_id)
    profiles = normalize_profiles(result)
    table(
        ["Name", "ID", "OS"],
        [[p.get("name", "?"), profile_id(p)[:16], p.get("os_type", "?")] for p in profiles],
    )
    print()


if __name__ == "__main__":
    main()
