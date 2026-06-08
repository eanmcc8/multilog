#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Bluesky feed warmup — scroll AT Protocol social feed."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, random_mouse_wander

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    scrolls = int(os.getenv("BLUESKY_SCROLLS", "7"))
    banner("Bluesky Feed Warmup", f"AT feed browse  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://bsky.app/", wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)
            if "login" in page.url.lower():
                warn("Bluesky login for personalized feed")
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 5))
                await human_scroll(page, random.randint(250, 600))
                await human_delay(2000, 4000)
                ok(f"Scroll {i + 1}/{scrolls}")


if __name__ == "__main__":
    asyncio.run(main())
