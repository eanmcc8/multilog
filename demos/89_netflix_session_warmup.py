#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Netflix session warmup — browse catalog and hold session."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, random_mouse_wander

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    scrolls = int(os.getenv("NETFLIX_SCROLLS", "6"))
    hold_min = int(os.getenv("NETFLIX_HOLD_MIN", "3"))
    banner("Netflix Session Warmup", f"Catalog browse  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://www.netflix.com/browse", wait_until="domcontentloaded", timeout=60000)
            await human_delay(4000, 7000)
            if "login" in page.url.lower():
                warn("Login or import cookies for full catalog")
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 5))
                await human_scroll(page, random.randint(300, 650))
                await human_delay(2000, 4000)
                ok(f"Browse {i + 1}/{scrolls}")
            section(f"Session hold ~{hold_min} min")
            await page.wait_for_timeout(hold_min * 60 * 1000)
            ok("Netflix warmup complete")


if __name__ == "__main__":
    asyncio.run(main())
