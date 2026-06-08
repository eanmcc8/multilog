#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Spotify web listener warmup — browse playlists and hold session."""
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
    playlist = os.getenv("SPOTIFY_URL", "https://open.spotify.com/")
    listen_min = int(os.getenv("SPOTIFY_LISTEN_MIN", "5"))
    banner("Spotify Listener Warmup", f"~{listen_min} min session  |  {timestamp()}")
    warn("Stream manipulation violates Spotify ToS — personal listening only")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto(playlist, wait_until="domcontentloaded", timeout=60000)
            await human_delay(4000, 7000)
            play = page.locator('button[data-testid="play-button"], button[aria-label="Play"]')
            if await play.count():
                await play.first.click()
                ok("Playback started")
            section(f"Listening ~{listen_min} min")
            elapsed = 0
            while elapsed < listen_min * 60:
                await page.wait_for_timeout(30_000)
                elapsed += 30
                await random_mouse_wander(page, random.randint(1, 3))
                ok(f"Listening {elapsed}s")
            ok("Spotify warmup complete")


if __name__ == "__main__":
    asyncio.run(main())
