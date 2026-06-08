#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: social warmup — visit sites to build account trust score."""
import asyncio
import os
import random

from dotenv import load_dotenv
from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.env import require_env
from mlx.human import human_delay, human_scroll

load_dotenv()

WARMUP_URLS = [
    "https://www.google.com",
    "https://www.youtube.com",
    "https://news.ycombinator.com",
    "https://www.reddit.com",
    "https://twitter.com",
    "https://www.facebook.com",
]


async def warmup(page, urls: list[str]) -> None:
    for url in urls:
        print(f"  -> {url}")
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await human_delay(2000, 5000)
            await human_scroll(page, random.randint(200, 600))
            await human_delay(1000, 3000)
        except Exception as exc:
            print(f"     skip: {exc}")


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    count = int(os.getenv("WARMUP_SITES", "4"))
    urls = random.sample(WARMUP_URLS, min(count, len(WARMUP_URLS)))

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            print(f"Warming up {len(urls)} sites...")
            await warmup(page, urls)
            print("Warmup complete.")


if __name__ == "__main__":
    asyncio.run(main())
