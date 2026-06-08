#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: Facebook account initializer — cookie session + 5min feed warmup."""
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
    minutes = float(os.getenv("FB_INIT_MINUTES", "5"))
    scrolls = int(os.getenv("FB_SCROLLS", "12"))

    banner("FB Account Initializer", f"Anti-checkpoint warmup  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Load Facebook (cookies from profile)")
            await page.goto("https://www.facebook.com/", wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)

            if "login" in page.url.lower():
                warn("Not logged in — import cookies (demo 15/21) or login manually")
                await page.wait_for_timeout(20_000)

            section(f"Feed warmup ~{minutes} min ({scrolls} scrolls)")
            deadline = minutes * 60
            elapsed = 0.0
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(3, 8))
                await human_scroll(page, random.randint(350, 800))
                wait = random.uniform(8, 25)
                await human_delay(int(wait * 1000), int(wait * 1000))
                elapsed += wait
                ok(f"Scroll {i + 1}/{scrolls} ({int(elapsed)}s)")
                if elapsed >= deadline:
                    break

            path = ensure_output() / "fb_initializer.png"
            await page.screenshot(path=str(path))
            ok(f"Done -> {path.name}")


if __name__ == "__main__":
    asyncio.run(main())
