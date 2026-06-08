#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: session keepalive — periodic mouse/scroll while profile stays open."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, random_mouse_wander

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    minutes = float(os.getenv("KEEPALIVE_MIN", "10"))
    url = os.getenv("KEEPALIVE_URL", "https://www.google.com")
    banner("Session Keepalive", f"~{minutes} min  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            deadline = minutes * 60
            elapsed = 0.0
            tick = 0
            while elapsed < deadline:
                tick += 1
                section(f"Pulse {tick} ({int(elapsed)}s)")
                await random_mouse_wander(page, random.randint(2, 5))
                await human_scroll(page, random.randint(100, 400))
                wait = random.uniform(25, 45)
                await human_delay(int(wait * 1000), int(wait * 1000))
                elapsed += wait
                ok(f"Session alive {int(elapsed)}s / {int(deadline)}s")


if __name__ == "__main__":
    asyncio.run(main())
