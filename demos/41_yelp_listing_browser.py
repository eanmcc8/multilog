#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: Yelp business listing browser — human browse pattern for market research."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, random_mouse_wander, random_page_activity

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    yelp_url = os.getenv("YELP_BUSINESS_URL", "")

    banner("Yelp Listing Browser", f"Market research browse  |  {timestamp()}")
    warn("Browse-only — fake Yelp reviews violate Yelp ToS and may be illegal")
    if not yelp_url:
        raise SystemExit("Set YELP_BUSINESS_URL in .env")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()

            section("Warm Yelp home")
            await page.goto("https://www.yelp.com", wait_until="domcontentloaded", timeout=45000)
            await random_page_activity(page, scrolls=4, clicks=2)
            await human_delay(3000, 6000)

            section("Business listing")
            await page.goto(yelp_url, wait_until="domcontentloaded", timeout=60000)
            await random_mouse_wander(page, random.randint(8, 15))
            await human_scroll(page, random.randint(400, 900))
            await human_delay(4000, 8000)
            ok("Yelp listing browse complete")


if __name__ == "__main__":
    asyncio.run(main())
