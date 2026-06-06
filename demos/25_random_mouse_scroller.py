#!/usr/bin/env python3
"""Demo: random mouse scroll, move, and click to mimic human behavior."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp
from mlx.env import load_env, require_env
from mlx.human import human_delay, random_page_activity

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    url = os.getenv("MOUSE_DEMO_URL", "https://www.wikipedia.org")
    rounds = int(os.getenv("MOUSE_ROUNDS", "5"))

    banner("Random Mouse & Scroller", f"Anti-bot behavior sim  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section(f"Target: {url}")
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            await human_delay(1500, 3000)

            for i in range(rounds):
                section(f"Activity round {i + 1}/{rounds}")
                await random_page_activity(
                    page,
                    scrolls=random.randint(3, 8),
                    clicks=random.randint(1, 3),
                )
                ok(f"Round {i + 1} complete")
            ok("Human-like session finished")


if __name__ == "__main__":
    asyncio.run(main())
