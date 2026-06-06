#!/usr/bin/env python3
"""Demo: Yelp stealth reviewer — residential proxy + human mouse behavior."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import (
    human_delay,
    human_scroll,
    human_type,
    random_mouse_wander,
    random_page_activity,
)

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    yelp_url = os.getenv("YELP_BUSINESS_URL", "")
    review = os.getenv("YELP_REVIEW_TEXT", "Excellent experience, will come back!")
    dry_run = os.getenv("YELP_DRY_RUN", "true").lower() != "false"

    banner("Yelp Stealth Reviewer", f"Residential proxy + human sim  |  {timestamp()}")
    if not yelp_url:
        raise SystemExit("Set YELP_BUSINESS_URL in .env")

    warn("Use residential proxy on profile (demo 20) before running Yelp")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()

            section("Warm Yelp home")
            await page.goto("https://www.yelp.com", wait_until="domcontentloaded", timeout=45000)
            await random_page_activity(page, scrolls=4, clicks=2)
            await human_delay(3000, 6000)

            section("Business page")
            await page.goto(yelp_url, wait_until="domcontentloaded", timeout=60000)
            await random_mouse_wander(page, random.randint(8, 15))
            await human_scroll(page, random.randint(400, 900))
            await human_delay(4000, 8000)

            section("Write review")
            write = page.locator('a:has-text("Write a Review"), button:has-text("Write a Review")')
            if await write.count():
                if dry_run:
                    warn("Dry-run — set YELP_DRY_RUN=false to proceed")
                else:
                    await write.first.click()
                    await human_delay(2000, 4000)
                    stars = page.locator('[aria-label="5 star rating"], div[role="radio"]').last
                    if await stars.count():
                        await stars.click()
                    box = page.locator("textarea")
                    if await box.count():
                        await human_type(page, "textarea", review)
                    ok("Review draft ready — submit in browser if prompted")
            else:
                warn("Review CTA not found")

            ok("Yelp stealth session done")


if __name__ == "__main__":
    asyncio.run(main())
