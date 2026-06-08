#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Example: authenticate and list account structure."""
import os

from mlx import MultiloginX
from mlx.console import banner, promo_footer, section, table
from mlx.env import load_env
from mlx.profiles import normalize_folders, normalize_profiles, profile_id

load_env()


def main() -> None:
    banner("Example 01 — Hello MLX")
    mlx = MultiloginX()

    section("Workspaces")
    table(["Name", "ID"], [[w.get("name", "?"), str(w.get("id", ""))[:20]] for w in mlx.get_workspaces()])

    section("Folders")
    rows = [[f.get("name", "?"), str(f.get("folder_id", f.get("id", "")))[:20]] for f in normalize_folders(mlx.get_folders())]
    table(["Name", "Folder ID"], rows)

    section("Profiles (first 10)")
    fid = os.getenv("MLX_FOLDER_ID", "")
    profs = normalize_profiles(mlx.search_profiles(limit=10, folder_id=fid))
    table(["Name", "ID"], [[p.get("name", "?"), profile_id(p)[:20]] for p in profs])
    promo_footer()


if __name__ == "__main__":
    main()
