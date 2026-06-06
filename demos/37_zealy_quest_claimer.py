#!/usr/bin/env python3
"""Demo: Zealy (Crew3) daily quest claimer across profiles."""
import asyncio
import os

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    community = os.getenv("ZEALY_COMMUNITY_URL", "https://zealy.io")

    banner("Zealy Quest Claimer", f"Daily crew tasks  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Open Zealy community")
            await page.goto(community, wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)

            login = page.locator('button:has-text("Connect"), button:has-text("Log in")')
            if await login.count():
                warn("Connect wallet or Discord in open profile")

            section("Quest board")
            await human_scroll(page, 800)
            await human_delay(3000, 5000)

            tasks = page.locator('button:has-text("Claim"), button:has-text("Verify"), a:has-text("Start")')
            count = await tasks.count()
            ok(f"Found {count} actionable task(s)")
            if count and os.getenv("ZEALY_AUTO_CLAIM", "false").lower() == "true":
                await tasks.first.click()
                ok("First task triggered")
            else:
                warn("Set ZEALY_AUTO_CLAIM=true for auto-click; use demo 03 for multi-profile farm")


if __name__ == "__main__":
    asyncio.run(main())
