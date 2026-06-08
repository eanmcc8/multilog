#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: Trustpilot business page browser — referer warmup for reputation research."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, random_page_activity

load_env()

WARMUP_SITES = [
    "https://www.google.com",
    "https://www.trustpilot.com",
]


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    target = os.getenv("TRUSTPILOT_URL", "")
    referer = os.getenv("TRUSTPILOT_REFERER", "https://www.google.com/")

    banner("Trustpilot Page Browser", f"Reputation research  |  {timestamp()}")
    warn("Browse-only — fake reviews violate consumer protection laws in many regions")
    if not target:
        raise SystemExit("Set TRUSTPILOT_URL (business profile page)")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()

            section("Cookie warmup")
            for url in WARMUP_SITES:
                await page.goto(url, wait_until="domcontentloaded", timeout=45000)
                await random_page_activity(page, scrolls=random.randint(2, 5), clicks=1)
                await human_delay(2000, 4000)

            section(f"Open target with referer: {referer[:40]}...")
            await page.goto(target, referer=referer, wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)
            await human_scroll(page, random.randint(300, 700))
            ok("Trustpilot page browse complete")


if __name__ == "__main__":
    asyncio.run(main())
