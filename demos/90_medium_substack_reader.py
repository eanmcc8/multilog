#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Medium + Substack reader warmup — article browse pattern."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, timestamp
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, random_mouse_wander

load_env()

SITES = {"medium": "https://medium.com/", "substack": "https://substack.com/home"}


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    site = os.getenv("READER_SITE", "medium").lower()
    url = SITES.get(site, SITES["medium"])
    scrolls = int(os.getenv("READER_SCROLLS", "6"))
    banner("Medium / Substack Reader", f"{site.title()}  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 5))
                await human_scroll(page, random.randint(350, 750))
                await human_delay(2500, 5000)
                ok(f"Article browse {i + 1}/{scrolls}")


if __name__ == "__main__":
    asyncio.run(main())
