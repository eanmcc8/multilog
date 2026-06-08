#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Instagram feed warmup — scroll, explore, build trust."""
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
    scrolls = int(os.getenv("IG_SCROLLS", "8"))
    banner("Instagram Warmup", f"Feed + explore  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Instagram home")
            await page.goto("https://www.instagram.com/", wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)
            if "login" in page.url.lower():
                warn("Import cookies or login manually")
            section(f"Scrolling ({scrolls}x)")
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 6))
                await human_scroll(page, random.randint(300, 700))
                await human_delay(1500, 4000)
                ok(f"Scroll {i + 1}/{scrolls}")
            path = ensure_output() / "instagram_warmup.png"
            await page.screenshot(path=str(path))
            ok(f"Done -> {path.name}")


if __name__ == "__main__":
    asyncio.run(main())
