#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Meta Ads Manager browser — browse ad account dashboard."""
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
    scrolls = int(os.getenv("META_ADS_SCROLLS", "4"))
    banner("Meta Ads Manager Browser", f"Ad account dashboard  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://www.facebook.com/adsmanager/", wait_until="domcontentloaded", timeout=90000)
            await human_delay(5000, 9000)
            if "login" in page.url.lower():
                warn("Facebook login required — use demo 11 warmup + cookies")
            section(f"Ads Manager browse ({scrolls}x)")
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 5))
                await human_scroll(page, random.randint(200, 500))
                await human_delay(3000, 6000)
                ok(f"Round {i + 1}/{scrolls}")
            ok("Meta Ads browse complete")


if __name__ == "__main__":
    asyncio.run(main())
