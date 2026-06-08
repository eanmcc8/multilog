#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Fiverr freelancer browser — browse gigs and seller dashboard."""
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


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    category = os.getenv("FIVERR_CATEGORY", "programming-tech")
    scrolls = int(os.getenv("FIVERR_SCROLLS", "5"))
    banner("Fiverr Freelancer Browser", f"Category: {category}  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            url = f"https://www.fiverr.com/categories/{category}"
            await page.goto(url, wait_until="domcontentloaded", timeout=90000)
            await human_delay(4000, 7000)
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 5))
                await human_scroll(page, random.randint(300, 650))
                await human_delay(2500, 5000)
                ok(f"Gig browse {i + 1}/{scrolls}")


if __name__ == "__main__":
    asyncio.run(main())
