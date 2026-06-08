#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: Twitch live stream browser — watch session for profile warmup."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, random_mouse_wander

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    channel = os.getenv("TWITCH_CHANNEL_URL", "https://www.twitch.tv")
    watch_min = int(os.getenv("TWITCH_WATCH_MIN", "20"))
    banner("Twitch Stream Browser", f"Live watch session  |  {timestamp()}")
    warn("Viewbotting violates Twitch ToS — use for legitimate personal viewing only")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section(f"Open stream: {channel}")
            await page.goto(channel, wait_until="domcontentloaded", timeout=90000)
            await human_delay(5000, 10000)

            mature = page.locator('button[data-a-target="content-classification-gate-overlay-start-watching-button"]')
            if await mature.count():
                await mature.click()

            player = page.locator('[data-a-target="player-overlay-click-handler"]')
            if await player.count():
                await player.click()

            section(f"Watching ~{watch_min} min")
            elapsed = 0
            while elapsed < watch_min * 60:
                await page.wait_for_timeout(30_000)
                elapsed += 30
                await random_mouse_wander(page, random.randint(1, 3))
                ok(f"Watching {elapsed}s")

            ok("Twitch stream browse complete")


if __name__ == "__main__":
    asyncio.run(main())
