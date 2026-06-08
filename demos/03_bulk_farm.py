#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: bulk farm — run builtin task or any demo (01-120) across profiles."""
import asyncio
import os

from mlx import MultiloginX
from mlx.console import banner, ok, section, table, timestamp, warn
from mlx.env import load_env
from mlx.farm import BUILTIN_TASKS, run_api_pipeline, run_builtin_farm, run_demo_farm

load_env()


async def main():
    folder_id = os.getenv("MLX_FOLDER_ID", "")
    limit = int(os.getenv("FARM_LIMIT", "5"))
    delay = int(os.getenv("FARM_DELAY_SEC", "3"))
    demo_id = os.getenv("FARM_DEMO", "").strip()
    task = os.getenv("FARM_TASK", "google").strip().lower()
    api_only = os.getenv("FARM_API_ONLY", "").lower() in ("1", "true", "yes")

    banner("Bulk Farm Orchestrator", f"Multi-profile runner  |  {timestamp()}")
    mlx = MultiloginX()

    if api_only or (not folder_id and not demo_id):
        section("API pipeline (no browser)")
        warn("Set MLX_FOLDER_ID + FARM_DEMO for per-profile browser runs")
        rows = [[r["step"], r["status"]] for r in run_api_pipeline(mlx, folder_id=folder_id)]
        table(["Step", "Status"], rows)
        print()
        return

    if not folder_id:
        raise SystemExit("Set MLX_FOLDER_ID in .env")

    if demo_id:
        section(f"Running demo {demo_id.zfill(2)} on {limit} profile(s)")
        results = run_demo_farm(
            mlx, demo_id=demo_id.zfill(2), folder_id=folder_id, limit=limit, delay_sec=delay
        )
    else:
        section(f"Builtin task '{task}' on {limit} profile(s)")
        if task not in BUILTIN_TASKS:
            warn(f"Unknown FARM_TASK. Available: {', '.join(BUILTIN_TASKS)}")
            raise SystemExit(1)
        results = await run_builtin_farm(
            mlx, task_name=task, folder_id=folder_id, limit=limit, delay_sec=delay
        )

    section("Farm summary")
    table(["Profile", "Status"], [[r.get("name", "?"), r["status"]] for r in results])
    ok_count = sum(1 for r in results if r["status"] == "OK")
    ok(f"{ok_count}/{len(results)} succeeded")
    print()


if __name__ == "__main__":
    asyncio.run(main())
