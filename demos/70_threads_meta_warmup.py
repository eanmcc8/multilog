#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Meta Threads feed warmup — scroll timeline and explore."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import ensure_output, load_env, require_env
from mlx.human import human_delay, human_scroll, random_mouse_wander

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    scrolls = int(os.getenv("THREADS_SCROLLS", "7"))
    banner("Meta Threads Warmup", f"Feed scroll  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://www.threads.net/", wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)
            if "login" in page.url.lower():
                warn("Import cookies or login manually")
            section(f"Scrolling ({scrolls}x)")
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 5))
                await human_scroll(page, random.randint(250, 650))
                await human_delay(1500, 3500)
                ok(f"Scroll {i + 1}/{scrolls}")
            path = ensure_output() / "threads_warmup.png"
            await page.screenshot(path=str(path))
            ok(f"Done -> {path.name}")


if __name__ == "__main__":
    asyncio.run(main())
