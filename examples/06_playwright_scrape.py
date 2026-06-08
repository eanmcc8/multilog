#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Example: CDP scrape page title from antidetect profile."""
import asyncio
import os

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, promo_footer
from mlx.env import load_env, require_env

load_env()


async def main() -> None:
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    url = os.getenv("SCRAPE_URL", "https://www.google.com")
    banner("Example 06 — Playwright Scrape")
    mlx = MultiloginX()

    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            title = await page.title()
            ok(f"Title: {title}")
    promo_footer()


if __name__ == "__main__":
    asyncio.run(main())
