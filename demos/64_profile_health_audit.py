#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: profile health audit — proxy, cookies, fingerprint flags."""
from mlx import MultiloginX
from mlx.console import banner, ok, section, table, timestamp, warn
from mlx.env import load_env, require_env
from mlx.profiles import normalize_profiles, profile_id

load_env()


def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    banner("Profile Health Audit", f"Pre-flight check  |  {timestamp()}")
    mlx = MultiloginX()
    pid = env["MLX_PROFILE_ID"]
    rows: list[list[str]] = []

    section("Cloud API")
    try:
        mlx.get_profile_summary()
        rows.append(["Cloud API", "OK", "Authenticated"])
    except Exception as exc:
        rows.append(["Cloud API", "FAIL", str(exc)[:40]])

    section("Launcher")
    try:
        ver = mlx.get_launcher_version()
        rows.append(["Launcher", "OK", str(ver.get("data", ver))[:30]])
    except Exception as exc:
        rows.append(["Launcher", "WARN", str(exc)[:40]])
        warn("Start Multilogin X app")

    section("Profile lookup")
    search = mlx.search_profiles(limit=50, folder_id=env["MLX_FOLDER_ID"])
    profs = normalize_profiles(search)
    match = next((p for p in profs if profile_id(p) == pid), None)
    if match:
        rows.append(["Profile", "OK", match.get("name", pid[:12])])
        proxy = match.get("parameters", {}).get("proxy", {})
        if proxy.get("host"):
            rows.append(["Proxy set", "OK", f"{proxy.get('host')}:{proxy.get('port')}"])
        else:
            rows.append(["Proxy set", "WARN", "No proxy on profile"])
    else:
        rows.append(["Profile", "FAIL", "ID not in folder"])

    section("Cookies")
    try:
        c = mlx.export_cookies(pid)
        n = len(c.get("data", {}).get("cookies", c.get("data", [])))
        rows.append(["Cookies", "OK" if n else "EMPTY", str(n)])
    except Exception as exc:
        rows.append(["Cookies", "WARN", str(exc)[:40]])

    table(["Check", "Status", "Detail"], rows)
    ok("Audit complete — fix WARN before scale runs")


if __name__ == "__main__":
    main()
