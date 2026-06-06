#!/usr/bin/env python3
"""Demo: YouTube search, watch video, simulate engagement."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, fail, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, human_type

load_env()


async def skip_ads(page) -> None:
    skip = page.locator(".ytp-ad-skip-button, .ytp-skip-ad-button")
    for _ in range(8):
        if await skip.count():
            await skip.first.click()
            ok("Skipped ad")
            break
        await page.wait_for_timeout(1500)


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    keyword = os.getenv("YOUTUBE_KEYWORD", "lofi hip hop")
    watch_sec = int(os.getenv("YOUTUBE_WATCH_SEC", "45"))

    banner("YouTube Video Watcher", f"Search + watch  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Open YouTube")
            await page.goto("https://www.youtube.com", wait_until="domcontentloaded", timeout=45000)
            await human_delay(2000, 4000)

            consent = page.locator('button:has-text("Accept all"), button:has-text("Agree")')
            if await consent.count():
                await consent.first.click()

            section(f"Search: {keyword}")
            search_box = 'input#search, input[name="search_query"]'
            try:
                await human_type(page, search_box, keyword)
                await page.keyboard.press("Enter")
            except Exception:
                await page.goto(
                    f"https://www.youtube.com/results?search_query={keyword.replace(' ', '+')}",
                    wait_until="domcontentloaded",
                )
            await human_delay(2500, 4000)

            section("Play first video")
            thumb = page.locator("ytd-video-renderer a#video-title, a#video-title").first
            try:
                await thumb.click(timeout=15000)
            except Exception as exc:
                fail(str(exc))
                return

            await human_delay(3000, 5000)
            await skip_ads(page)

            section(f"Watching ~{watch_sec}s")
            await page.wait_for_timeout(watch_sec * 1000)
            await human_scroll(page, random.randint(100, 300))

            like = page.locator('button[aria-label*="like"], button[aria-label*="Like"]')
            if await like.count() and random.random() < 0.4:
                await like.first.click()
                ok("Random like")
            else:
                warn("Like skipped or not found")

            ok("YouTube session complete")


if __name__ == "__main__":
    asyncio.run(main())
