#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Steam store browser — browse games and community pages."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, random_mouse_wander

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    store_url = os.getenv("STEAM_STORE_URL", "https://store.steampowered.com/")
    scrolls = int(os.getenv("STEAM_SCROLLS", "6"))
    banner("Steam Store Browser", f"Game browse  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto(store_url, wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)
            section(f"Store browse ({scrolls}x)")
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 6))
                await human_scroll(page, random.randint(300, 700))
                await human_delay(2000, 4500)
                ok(f"Scroll {i + 1}/{scrolls}")
            ok("Steam browse complete")


if __name__ == "__main__":
    asyncio.run(main())
