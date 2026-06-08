#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Example: bulk farm google warmup on first N profiles."""
import asyncio
import os

from mlx import MultiloginX
from mlx.console import banner, promo_footer, section, table
from mlx.env import load_env
from mlx.farm import run_builtin_farm

load_env()


async def main() -> None:
    folder_id = os.getenv("MLX_FOLDER_ID", "")
    limit = int(os.getenv("FARM_LIMIT", "3"))
    banner("Example 07 — Bulk Farm")
    if not folder_id:
        raise SystemExit("Set MLX_FOLDER_ID in .env")

    mlx = MultiloginX()
    section(f"google warmup × {limit} profiles")
    results = await run_builtin_farm(mlx, task_name="google", folder_id=folder_id, limit=limit, delay_sec=2)
    table(["Profile", "Status"], [[r["name"], r["status"]] for r in results])
    promo_footer()


if __name__ == "__main__":
    asyncio.run(main())
