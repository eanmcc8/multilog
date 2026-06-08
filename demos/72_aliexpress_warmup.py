#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: AliExpress warmup — product search and category browse."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, random_mouse_wander

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    query = os.getenv("ALIEXPRESS_QUERY", "phone case")
    scrolls = int(os.getenv("ALIEXPRESS_SCROLLS", "6"))
    banner("AliExpress Warmup", f"Search: {query}  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://www.aliexpress.com/", wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 5000)
            search = page.locator('input[type="search"], input[name="searchWords"]')
            if await search.count():
                await search.first.fill(query)
                await page.keyboard.press("Enter")
                await human_delay(4000, 7000)
            section(f"Product browse ({scrolls}x)")
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 5))
                await human_scroll(page, random.randint(300, 700))
                await human_delay(2000, 4000)
                ok(f"Scroll {i + 1}/{scrolls}")
            ok("AliExpress warmup complete")


if __name__ == "__main__":
    asyncio.run(main())
