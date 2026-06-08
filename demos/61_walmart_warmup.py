#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Walmart.com browsing warmup."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, timestamp
from mlx.env import ensure_output, load_env, require_env
from mlx.human import human_delay, human_scroll

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    banner("Walmart Warmup", f"US retail browse  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://www.walmart.com", wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)
            for i in range(int(os.getenv("WALMART_SCROLLS", "5"))):
                await human_scroll(page, random.randint(250, 600))
                await human_delay(2000, 4000)
                ok(f"Scroll {i + 1}")
            await page.screenshot(path=str(ensure_output() / "walmart_warmup.png"))


if __name__ == "__main__":
    asyncio.run(main())
