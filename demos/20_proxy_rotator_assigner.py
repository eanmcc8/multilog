#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: validate proxies and assign live ones to profiles (rotator)."""
import os

from mlx import MultiloginX
from mlx.console import banner, fail, ok, progress, section, table, timestamp, warn
from mlx.env import ROOT, load_env, require_env
from mlx.profiles import normalize_profiles, profile_id
from mlx.proxy_utils import parse_proxy, proxy_payload

load_env()

PROXY_FILE = ROOT / "proxies.txt"


def main():
    require_env("MLX_FOLDER_ID")
    assign_limit = int(os.getenv("PROXY_ASSIGN_LIMIT", "10"))

    banner("Proxy Rotator & Assigner", f"Validate + assign  |  {timestamp()}")
    if not PROXY_FILE.exists():
        raise SystemExit("Create proxies.txt from proxies.txt.example first (demo 14)")

    lines = [l for l in PROXY_FILE.read_text(encoding="utf-8").splitlines() if parse_proxy(l)]
    if not lines:
        raise SystemExit("No proxies in proxies.txt")

    mlx = MultiloginX()
    section(f"Checking {len(lines)} proxy(s)")
    live: list[tuple] = []
    for i, line in enumerate(lines, 1):
        host, port, ptype, user, pwd = parse_proxy(line)  # type: ignore[misc]
        progress(i - 1, len(lines), host)
        try:
            result = mlx.validate_proxy(host, port, ptype, user, pwd)
            data = result.get("data", result)
            if data.get("is_valid"):
                live.append((host, port, ptype, user, pwd))
                ok(f"{host}:{port} live")
            else:
                fail(f"{host}:{port} dead")
        except Exception as exc:
            fail(str(exc))
        progress(i, len(lines))

    if not live:
        raise SystemExit("No live proxies found")

    section(f"Assigning to up to {assign_limit} profile(s)")
    search = mlx.search_profiles(limit=assign_limit, folder_id=os.getenv("MLX_FOLDER_ID", ""))
    profiles = normalize_profiles(search)[:assign_limit]
    if not profiles:
        raise SystemExit("No profiles in folder to assign")

    rows: list[list[str]] = []
    for i, prof in enumerate(profiles):
        host, port, ptype, user, pwd = live[i % len(live)]
        pid = profile_id(prof)
        name = prof.get("name", pid[:8])
        payload = {"parameters": {"proxy": proxy_payload(host, port, ptype, user, pwd)}}
        try:
            mlx.update_profile(pid, **payload)
            rows.append([name, f"{host}:{port}", ptype, "OK"])
            ok(f"{name} <- {host}:{port}")
        except Exception as exc:
            rows.append([name, f"{host}:{port}", ptype, "FAIL"])
            fail(str(exc))

    section("Assignment summary")
    table(["Profile", "Proxy", "Type", "Status"], rows)
    warn("Rotate pool by re-running; uses round-robin over live proxies")
    print()


if __name__ == "__main__":
    main()
