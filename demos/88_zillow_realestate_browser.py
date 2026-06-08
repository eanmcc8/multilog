#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Zillow real estate browser — browse property listings."""
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
    location = os.getenv("ZILLOW_LOCATION", "Austin TX")
    scrolls = int(os.getenv("ZILLOW_SCROLLS", "5"))
    banner("Zillow Real Estate Browser", f"{location}  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://www.zillow.com/homes/", wait_until="domcontentloaded", timeout=90000)
            await human_delay(4000, 7000)
            search = page.locator('input[placeholder*="Address"], input[id*="search"]')
            if await search.count():
                await human_type(page, 'input[placeholder*="Address"], input[id*="search"]', location)
                await page.keyboard.press("Enter")
                await human_delay(4000, 8000)
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 6))
                await human_scroll(page, random.randint(350, 800))
                await human_delay(2500, 5000)
                ok(f"Listings {i + 1}/{scrolls}")


if __name__ == "__main__":
    asyncio.run(main())
