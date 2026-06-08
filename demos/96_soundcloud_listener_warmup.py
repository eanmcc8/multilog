#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: SoundCloud listener warmup — browse tracks and playlists."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, random_mouse_wander

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    url = os.getenv("SOUNDCLOUD_URL", "https://soundcloud.com/discover")
    listen_min = int(os.getenv("SOUNDCLOUD_LISTEN_MIN", "4"))
    banner("SoundCloud Listener Warmup", f"~{listen_min} min  |  {timestamp()}")
    warn("Personal listening only — stream inflation violates SoundCloud ToS")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await human_delay(4000, 7000)
            play = page.locator('button[aria-label*="Play"], button.sc-button-play')
            if await play.count():
                await play.first.click()
                ok("Playback started")
            elapsed = 0
            while elapsed < listen_min * 60:
                await page.wait_for_timeout(30_000)
                elapsed += 30
                await random_mouse_wander(page, random.randint(1, 3))
                ok(f"Listening {elapsed}s")


if __name__ == "__main__":
    asyncio.run(main())
