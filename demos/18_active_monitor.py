#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: monitor running profiles in a live loop."""
import json
import os
import time

from mlx import MultiloginX
from mlx.console import C, _c, banner, section, table, timestamp
from mlx.env import load_env

load_env()


def main():
    interval = int(os.getenv("MONITOR_INTERVAL", "5"))
    rounds = int(os.getenv("MONITOR_ROUNDS", "6"))
    banner("Active Profile Monitor", f"Refresh every {interval}s  |  {timestamp()}")

    mlx = MultiloginX()
    for r in range(1, rounds + 1):
        section(f"Poll {r}/{rounds}  ({timestamp()})")
        try:
            data = mlx.get_active_profiles()
            payload = data.get("data", data)
            if isinstance(payload, list):
                rows = [[str(p.get("id", p.get("profile_id", "")))[:12], str(p.get("port", "?"))] for p in payload]
                table(["Profile ID", "Port"], rows or [["-", "-"]])
                print(_c(f"  Running: {len(payload)}", C.GREEN if payload else C.DIM))
            else:
                print(json.dumps(payload, indent=2)[:500])
        except Exception as exc:
            print(_c(f"  Error: {exc}", C.RED))
        if r < rounds:
            time.sleep(interval)
    print()


if __name__ == "__main__":
    main()
