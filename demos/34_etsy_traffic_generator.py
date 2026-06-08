#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: Etsy store traffic generator from clean profiles."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, fail, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, random_page_activity

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    store_url = os.getenv("ETSY_STORE_URL", "")
    if not store_url:
        raise SystemExit("Set ETSY_STORE_URL in .env (your Etsy shop or listing URL)")

    visits = int(os.getenv("ETSY_VISIT_PAGES", "4"))
    banner("Etsy Traffic Generator", f"Organic visit pattern  |  {timestamp()}")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()

            section("Browse Etsy home first")
            await page.goto("https://www.etsy.com", wait_until="domcontentloaded", timeout=45000)
            await random_page_activity(page, scrolls=3, clicks=1)
            await human_delay(2000, 4000)

            section(f"Visit store: {store_url[:50]}...")
            await page.goto(store_url, wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)

            for i in range(visits):
                await human_scroll(page, random.randint(250, 650))
                await human_delay(random.randint(4, 12) * 1000, random.randint(4, 12) * 1000)
                link = page.locator("a.listing-link, a[data-listing-id]").nth(random.randint(0, 2))
                if await link.count():
                    try:
                        await link.first.click()
                        ok(f"Viewed listing {i + 1}")
                        await human_delay(5000, 10000)
                        await page.go_back()
                    except Exception as exc:
                        fail(str(exc))
                else:
                    warn("No listing links on page")

            ok("Etsy traffic session complete")


if __name__ == "__main__":
    asyncio.run(main())
