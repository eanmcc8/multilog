#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Microsoft Outlook web warmup — inbox browse session."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, random_mouse_wander

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    hold_sec = int(os.getenv("OUTLOOK_HOLD_SEC", "60"))
    banner("Microsoft Outlook Warmup", f"Inbox session  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://outlook.live.com/mail/", wait_until="domcontentloaded", timeout=90000)
            await human_delay(5000, 9000)
            if "login" in page.url.lower():
                warn("Microsoft login required — use demo 10 Google or MS cookies")
            section(f"Inbox browse ~{hold_sec}s")
            elapsed = 0
            while elapsed < hold_sec:
                await random_mouse_wander(page, random.randint(2, 5))
                await human_scroll(page, random.randint(150, 400))
                await page.wait_for_timeout(5000)
                elapsed += 5
            ok("Outlook warmup complete")


if __name__ == "__main__":
    asyncio.run(main())
