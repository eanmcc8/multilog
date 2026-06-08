#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Notion workspace warmup — browse pages and sidebar."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, random_mouse_wander

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    scrolls = int(os.getenv("NOTION_SCROLLS", "5"))
    banner("Notion Workspace Warmup", f"Page browse  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://www.notion.so/", wait_until="domcontentloaded", timeout=90000)
            await human_delay(5000, 9000)
            if "login" in page.url.lower():
                warn("Notion login required for workspace")
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 5))
                await human_scroll(page, random.randint(250, 550))
                await human_delay(3000, 6000)
                ok(f"Page {i + 1}/{scrolls}")


if __name__ == "__main__":
    asyncio.run(main())
