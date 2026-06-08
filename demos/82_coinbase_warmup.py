#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Coinbase warmup — browse markets and portfolio pages."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, random_mouse_wander

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    scrolls = int(os.getenv("COINBASE_SCROLLS", "5"))
    banner("Coinbase Warmup", f"Market browse  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://www.coinbase.com/", wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)
            if "login" in page.url.lower():
                warn("Login for portfolio view — browse works without auth")
            section(f"Market scroll ({scrolls}x)")
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 5))
                await human_scroll(page, random.randint(300, 600))
                await human_delay(2000, 4000)
                ok(f"Scroll {i + 1}/{scrolls}")
            ok("Coinbase warmup complete")


if __name__ == "__main__":
    asyncio.run(main())
