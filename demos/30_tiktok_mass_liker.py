#!/usr/bin/env python3
"""Demo: TikTok For You scroll, like, and follow script."""
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
    videos = int(os.getenv("TIKTOK_VIDEOS", "8"))
    like_rate = float(os.getenv("TIKTOK_LIKE_RATE", "0.35"))
    follow_rate = float(os.getenv("TIKTOK_FOLLOW_RATE", "0.15"))

    banner("TikTok Mass Liker", f"FYP farming  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Open TikTok FYP")
            await page.goto("https://www.tiktok.com/foryou", wait_until="domcontentloaded", timeout=60000)
            await human_delay(4000, 7000)

            likes = follows = 0
            for i in range(videos):
                section(f"Video {i + 1}/{videos}")
                await random_mouse_wander(page, random.randint(2, 6))
                await human_scroll(page, random.randint(400, 900))
                await human_delay(3000, 8000)

                if random.random() < like_rate:
                    like_btn = page.locator('[data-e2e="like-icon"], button[aria-label*="Like"]')
                    if await like_btn.count():
                        await like_btn.first.click()
                        likes += 1
                        ok("Liked")

                if random.random() < follow_rate:
                    follow_btn = page.locator('[data-e2e="follow-button"], button:has-text("Follow")')
                    if await follow_btn.count():
                        await follow_btn.first.click()
                        follows += 1
                        ok("Followed")

                await page.keyboard.press("ArrowDown")
                await human_delay(2000, 5000)

            ok(f"Session done: {likes} likes, {follows} follows")
            warn("Adjust TIKTOK_LIKE_RATE / TIKTOK_FOLLOW_RATE in .env")


if __name__ == "__main__":
    asyncio.run(main())
