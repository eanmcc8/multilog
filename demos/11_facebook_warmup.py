#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: Facebook feed warmup - scroll and simulate reading."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import ensure_output, load_env, require_env
from mlx.human import human_delay, human_scroll

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    scrolls = int(os.getenv("FB_SCROLLS", "8"))
    banner("Facebook Warmup", f"Feed activity simulation  |  {timestamp()}")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Open Facebook")
            await page.goto("https://www.facebook.com/", wait_until="domcontentloaded", timeout=45000)
            await human_delay(2000, 4000)

            if "login" in page.url.lower():
                warn("Not logged in - login manually or import cookies first")
                await page.wait_for_timeout(30_000)

            section(f"Scrolling feed ({scrolls}x)")
            for i in range(scrolls):
                await human_scroll(page, random.randint(300, 700))
                await human_delay(1500, 4000)
                ok(f"Scroll {i + 1}/{scrolls}")

            path = ensure_output() / "facebook_warmup.png"
            await page.screenshot(path=str(path))
            ok(f"Screenshot -> {path.name}")


if __name__ == "__main__":
    asyncio.run(main())
