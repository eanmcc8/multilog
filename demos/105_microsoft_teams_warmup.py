#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Microsoft Teams web warmup — browse teams and chat."""
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
    scrolls = int(os.getenv("TEAMS_SCROLLS", "5"))
    banner("Microsoft Teams Warmup", f"Teams browse  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://teams.microsoft.com/", wait_until="domcontentloaded", timeout=120000)
            await human_delay(6000, 10000)
            if "login" in page.url.lower():
                warn("Microsoft login required")
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 5))
                await human_scroll(page, random.randint(200, 500))
                await human_delay(3000, 6000)
                ok(f"Channel {i + 1}/{scrolls}")


if __name__ == "__main__":
    asyncio.run(main())
