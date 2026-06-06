#!/usr/bin/env python3
"""Demo: Amazon search product and add to wishlist for purchase trust."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, fail, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, human_type

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    keyword = os.getenv("AMAZON_KEYWORD", "wireless mouse")
    dry_run = os.getenv("AMAZON_DRY_RUN", "true").lower() != "false"

    banner("Amazon Wishlist Adder", f"Shopping trust signal  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Amazon home")
            await page.goto("https://www.amazon.com", wait_until="domcontentloaded", timeout=45000)
            await human_delay(2000, 4000)

            section(f"Search: {keyword}")
            await human_type(page, "#twotabsearchtextbox", keyword)
            await page.keyboard.press("Enter")
            await human_delay(2500, 4000)

            section("Open product")
            item = page.locator('[data-component-type="s-search-result"] h2 a, .s-result-item h2 a').first
            try:
                await item.click(timeout=15000)
            except Exception as exc:
                fail(str(exc))
                return
            await human_delay(3000, 5000)
            await human_scroll(page, random.randint(300, 600))

            section("Add to wishlist")
            wishlist = page.locator(
                '#add-to-wishlist-button-submit, '
                'input[name="submit.add-to-wishlist"], '
                'span:has-text("Add to List")'
            )
            if await wishlist.count():
                if dry_run:
                    warn("Dry-run mode — set AMAZON_DRY_RUN=false to click")
                else:
                    await wishlist.first.click()
                    ok("Added to wishlist")
            else:
                warn("Wishlist button not found (login may be required)")


if __name__ == "__main__":
    asyncio.run(main())
