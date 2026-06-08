#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Google Maps listing browser — view business page for Local SEO research."""
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
    maps_url = os.getenv("GMAPS_PLACE_URL", "")
    scroll_rounds = int(os.getenv("GMAPS_SCROLL_ROUNDS", "5"))

    banner("Google Maps Listing Browser", f"Local SEO research  |  {timestamp()}")
    warn("Browse-only demo — do not post fake reviews (violates Google & FTC rules)")
    if not maps_url:
        raise SystemExit("Set GMAPS_PLACE_URL in .env (Google Maps business link)")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Open Maps place")
            await page.goto(maps_url, wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)
            for i in range(scroll_rounds):
                await random_mouse_wander(page, random.randint(3, 8))
                await human_scroll(page, random.randint(200, 500))
                await human_delay(1500, 3500)
                ok(f"Browse round {i + 1}/{scroll_rounds}")
            section("Reviews tab (read-only)")
            reviews = page.locator('button:has-text("Reviews"), [data-tab-index="1"]')
            if await reviews.count():
                await reviews.first.click()
                await human_delay(2000, 4000)
                await human_scroll(page, random.randint(300, 600))
            ok("Listing browse complete — use insights for legitimate SEO only")


if __name__ == "__main__":
    asyncio.run(main())
