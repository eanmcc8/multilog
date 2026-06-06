#!/usr/bin/env python3
"""Demo: Twitter/X timeline warmup."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import ensure_output, load_env, require_env
from mlx.human import human_delay, human_scroll

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    scrolls = int(os.getenv("TW_SCROLLS", "6"))
    banner("Twitter / X Warmup", f"Timeline browsing  |  {timestamp()}")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Open X")
            await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=45000)
            await human_delay(2000, 4000)

            if "login" in page.url.lower():
                warn("Not logged in - complete login manually (60s)")
                await page.wait_for_timeout(60_000)

            section(f"Timeline scroll ({scrolls}x)")
            for i in range(scrolls):
                await human_scroll(page, random.randint(250, 600))
                await human_delay(1200, 3500)
                ok(f"Scroll {i + 1}/{scrolls}")

            path = ensure_output() / "twitter_warmup.png"
            await page.screenshot(path=str(path))
            ok(f"Screenshot -> {path.name}")


if __name__ == "__main__":
    asyncio.run(main())
