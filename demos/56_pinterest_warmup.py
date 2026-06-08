#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Pinterest pin browsing warmup."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, timestamp, warn
from mlx.env import ensure_output, load_env, require_env
from mlx.human import human_delay, human_scroll, random_mouse_wander

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    scrolls = int(os.getenv("PIN_SCROLLS", "7"))
    banner("Pinterest Warmup", f"Pin discovery  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://www.pinterest.com/", wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 5000)
            if "login" in page.url.lower():
                warn("Login required for full feed")
            for i in range(scrolls):
                await random_mouse_wander(page, 3)
                await human_scroll(page, random.randint(350, 800))
                await human_delay(2000, 4500)
                ok(f"Pin scroll {i + 1}/{scrolls}")
            await page.screenshot(path=str(ensure_output() / "pinterest_warmup.png"))


if __name__ == "__main__":
    asyncio.run(main())
