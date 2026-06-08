#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Binance web warmup — login prep and market browse."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    banner("Binance Warmup", f"Exchange browse  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://www.binance.com/en/markets", wait_until="domcontentloaded", timeout=90000)
            await human_delay(4000, 8000)
            for i in range(int(os.getenv("BINANCE_SCROLLS", "5"))):
                await human_scroll(page, random.randint(300, 600))
                await human_delay(2500, 5000)
                ok(f"Market scroll {i + 1}")
            warn("Complete KYC/login manually in profile")


if __name__ == "__main__":
    asyncio.run(main())
