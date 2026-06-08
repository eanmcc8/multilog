#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: YouTube watch-time booster — multi-tab, resolution change, ad skip."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll

load_env()


async def skip_ads(page) -> None:
    skip = page.locator(".ytp-ad-skip-button, .ytp-skip-ad-button")
    for _ in range(6):
        if await skip.count():
            await skip.first.click()
            ok("Ad skipped")
            return
        await page.wait_for_timeout(1500)


async def watch_video(page, video_url: str, minutes: float) -> None:
    await page.goto(video_url, wait_until="domcontentloaded", timeout=60000)
    await human_delay(3000, 5000)
    await skip_ads(page)

    # Toggle quality (simulate human settings change)
    settings = page.locator(".ytp-settings-button")
    if await settings.count() and random.random() < 0.5:
        await settings.click()
        await human_delay(500, 1200)
        quality = page.locator('div.ytp-menuitem:has-text("Quality")')
        if await quality.count():
            await quality.click()
            await human_delay(500, 1200)

    watch_ms = int(minutes * 60 * 1000)
    section(f"Watching ~{minutes} min")
    chunk = 30_000
    watched = 0
    while watched < watch_ms:
        await page.wait_for_timeout(chunk)
        watched += chunk
        if random.random() < 0.3:
            await human_scroll(page, random.randint(50, 150))
        await skip_ads(page)
    ok(f"Watch time +{minutes} min")


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    video = os.getenv("YOUTUBE_VIDEO_URL", "https://www.youtube.com/watch?v=jfKfPfyJRdk")
    minutes = float(os.getenv("YOUTUBE_BOOST_MINUTES", "10"))
    tabs = int(os.getenv("YOUTUBE_BOOST_TABS", "1"))

    banner("YouTube Watch-Time Booster", f"4000h strategy  |  {timestamp()}")
    warn("Use unique profile + proxy per channel — avoid policy violations")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            pages = []
            for t in range(tabs):
                p = await session.context.new_page() if t else await session.new_page()
                pages.append(p)

            for i, page in enumerate(pages, 1):
                section(f"Tab {i}/{tabs}")
                await watch_video(page, video, minutes / tabs)

            ok("Watch-time boost session complete")


if __name__ == "__main__":
    asyncio.run(main())
