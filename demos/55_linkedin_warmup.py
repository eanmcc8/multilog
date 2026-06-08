#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: LinkedIn feed warmup for B2B account trust."""
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
    scrolls = int(os.getenv("LI_SCROLLS", "6"))
    banner("LinkedIn Warmup", f"B2B feed activity  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)
            if "login" in page.url.lower():
                warn("Login or import cookies first")
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 5))
                await human_scroll(page, random.randint(250, 600))
                await human_delay(2000, 5000)
                ok(f"Scroll {i + 1}/{scrolls}")
            await page.screenshot(path=str(ensure_output() / "linkedin_warmup.png"))
            ok("LinkedIn warmup complete")


if __name__ == "__main__":
    asyncio.run(main())
