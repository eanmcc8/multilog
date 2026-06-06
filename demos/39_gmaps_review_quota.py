#!/usr/bin/env python3
"""Demo: Google Maps review quota scheduler for Local SEO."""
import asyncio
import os
import random
from datetime import datetime

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, human_type, random_mouse_wander

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    maps_url = os.getenv("GMAPS_PLACE_URL", "")
    daily_quota = int(os.getenv("GMAPS_DAILY_QUOTA", "28"))
    review_text = os.getenv("GMAPS_REVIEW_TEXT", "Great service, highly recommend!")
    dry_run = os.getenv("GMAPS_DRY_RUN", "true").lower() != "false"

    banner("Google Maps Review Quota", f"Local SEO  |  {timestamp()}")
    if not maps_url:
        raise SystemExit("Set GMAPS_PLACE_URL in .env (Google Maps business link)")

    section(f"Daily quota target: {daily_quota} reviews/profile rotation")
    warn(f"Today slot 1/{daily_quota} — use demo 03 bulk farm for multi-profile rotation")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Open Maps place")
            await page.goto(maps_url, wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)
            await random_mouse_wander(page, random.randint(4, 10))
            await human_scroll(page, random.randint(200, 500))

            section("Write review flow")
            write_btn = page.locator('button:has-text("Write a review"), span:has-text("Write a review")')
            if await write_btn.count():
                if dry_run:
                    warn("Dry-run — set GMAPS_DRY_RUN=false to submit")
                else:
                    await write_btn.first.click()
                    await human_delay(2000, 4000)
                    stars = page.locator('[aria-label*="5 stars"], button[aria-label*="Star"]')
                    if await stars.count():
                        await stars.last.click()
                    textarea = page.locator("textarea")
                    if await textarea.count():
                        await human_type(page, "textarea", review_text)
                    submit = page.locator('button:has-text("Post"), button:has-text("Publish")')
                    if await submit.count():
                        await submit.first.click()
                        ok("Review submitted")
            else:
                warn("Write review button not found — login or import cookies first")

            ok(f"Quota log: {datetime.now():%Y-%m-%d} 1/{daily_quota}")


if __name__ == "__main__":
    asyncio.run(main())
