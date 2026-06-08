#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Google Scholar research browser — academic paper search warmup."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, timestamp
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, human_type, random_mouse_wander

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    query = os.getenv("SCHOLAR_QUERY", "browser fingerprint detection")
    scrolls = int(os.getenv("SCHOLAR_SCROLLS", "5"))
    banner("Google Scholar Research", f"Query: {query}  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://scholar.google.com/", wait_until="domcontentloaded", timeout=60000)
            await human_delay(2000, 4000)
            box = page.locator('input[name="q"]')
            if await box.count():
                await human_type(page, 'input[name="q"]', query)
                await page.keyboard.press("Enter")
                await human_delay(3000, 6000)
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 5))
                await human_scroll(page, random.randint(250, 600))
                await human_delay(2000, 4000)
                ok(f"Papers {i + 1}/{scrolls}")
            ok("Scholar research browse complete")


if __name__ == "__main__":
    asyncio.run(main())
