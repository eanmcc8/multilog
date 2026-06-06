#!/usr/bin/env python3
"""Demo: DataDome / Akamai bypass profile template for e-commerce scraping."""
import asyncio
import os

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.antibot import antibot_profile_parameters
from mlx.browser import profile_browser
from mlx.console import banner, info, ok, section, table, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, random_page_activity

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    target = os.getenv("ANTIBOT_TEST_URL", "https://www.guess.com")

    banner("DataDome / Akamai Bypass Template", f"Strict MLX profile flags  |  {timestamp()}")
    params = antibot_profile_parameters(strict=True)
    flags = params["flags"]
    rows = [[k, v] for k, v in list(flags.items())[:8]]
    section("Recommended profile flags")
    table(["Flag", "Value"], rows)

    warn("Apply via demo 22 or update_profile before scraping")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section(f"Probe: {target}")
            resp = await page.goto(target, wait_until="domcontentloaded", timeout=90000)
            status = resp.status if resp else "?"
            info(f"HTTP status: {status}")

            if await page.locator("text=Access Denied, text=blocked").count():
                warn("Blocked — rotate residential proxy (demo 20)")
            else:
                await random_page_activity(page, scrolls=3, clicks=1)
                ok("Page loaded — extend with your scrape selectors")

            await human_delay(2000, 4000)


if __name__ == "__main__":
    asyncio.run(main())
