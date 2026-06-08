#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: randomize Canvas/WebGL/UA flags on existing profiles."""
import os

from mlx import MultiloginX
from mlx.console import banner, fail, ok, progress, section, table, timestamp
from mlx.env import load_env, require_env
from mlx.fingerprint import random_fingerprint_update
from mlx.profiles import normalize_profiles, profile_id

load_env()


def main():
    env = require_env("MLX_FOLDER_ID")
    limit = int(os.getenv("FINGERPRINT_LIMIT", "10"))

    banner("Fingerprint Randomizer", f"Refresh UA + noise flags  |  {timestamp()}")
    mlx = MultiloginX()
    search = mlx.search_profiles(limit=limit, folder_id=env["MLX_FOLDER_ID"])
    profiles = normalize_profiles(search)[:limit]
    if not profiles:
        raise SystemExit("No profiles in folder")

    section(f"Randomizing {len(profiles)} profile(s)")
    rows: list[list[str]] = []
    for i, prof in enumerate(profiles, 1):
        pid = profile_id(prof)
        name = prof.get("name", pid[:8])
        update = random_fingerprint_update()
        ua = update["parameters"]["fingerprint"]["navigator"]["user_agent"]
        progress(i - 1, len(profiles), name)
        try:
            mlx.update_profile(pid, **update)
            rows.append([name, ua[50:80] + "...", "OK"])
            ok(f"{name} refreshed")
        except Exception as exc:
            rows.append([name, "-", "FAIL"])
            fail(str(exc))
        progress(i, len(profiles))

    section("Results")
    table(["Profile", "UA (snippet)", "Status"], rows)
    print()


if __name__ == "__main__":
    main()
