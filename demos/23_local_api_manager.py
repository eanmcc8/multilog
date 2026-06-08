#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: Multilogin X local Launcher API manager (ports, active, stop-all)."""
import os

from mlx import MultiloginX
from mlx.console import banner, info, ok, section, table, timestamp, warn
from mlx.env import load_env

load_env()


def main():
    banner("Local API Manager", f"Launcher health  |  {timestamp()}")
    mlx = MultiloginX()
    launcher = os.getenv("MLX_LAUNCHER_URL", "https://launcher.mlx.yt:45001")

    section("Launcher")
    info(f"URL: {launcher}")
    try:
        ver = mlx.get_launcher_version()
        data = ver.get("data", ver)
        ok(f"Version: {data.get('version', data)}")
    except Exception as exc:
        warn(f"Launcher unreachable: {exc}")
        warn("Start Multilogin X app before running browser demos")

    section("Active profiles")
    try:
        active = mlx.get_active_profiles()
        items = active.get("data", active)
        if isinstance(items, dict):
            items = items.get("profiles", [])
        rows = []
        for item in items or []:
            pid = item.get("profile_id", item.get("id", "?"))
            port = item.get("port", item.get("automation_port", "?"))
            name = item.get("name", pid[:12])
            rows.append([name, str(pid)[:12], str(port)])
        if rows:
            table(["Name", "Profile ID", "Port"], rows)
        else:
            info("No profiles running")
    except Exception as exc:
        warn(str(exc))

    section("Cloud summary")
    try:
        summary = mlx.get_profile_summary()
        data = summary.get("data", summary)
        for key in ("profiles_count", "profiles_limit", "running_profiles"):
            if key in data:
                ok(f"{key}: {data[key]}")
    except Exception as exc:
        warn(str(exc))

    if os.getenv("API_MANAGER_STOP_ALL", "").lower() in ("1", "true", "yes"):
        section("Stop all")
        mlx.stop_all_profiles()
        ok("All profiles stopped")
    else:
        warn("Set API_MANAGER_STOP_ALL=true to stop all running profiles")

    print()


if __name__ == "__main__":
    main()
