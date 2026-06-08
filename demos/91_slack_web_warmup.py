#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Slack web warmup — workspace browse and channel scroll."""
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
    workspace = os.getenv("SLACK_URL", "https://app.slack.com/client")
    scrolls = int(os.getenv("SLACK_SCROLLS", "5"))
    banner("Slack Web Warmup", f"Workspace browse  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto(workspace, wait_until="domcontentloaded", timeout=90000)
            await human_delay(5000, 9000)
            if "signin" in page.url.lower():
                warn("Slack login required")
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 5))
                await human_scroll(page, random.randint(200, 500))
                await human_delay(2500, 5000)
                ok(f"Channel browse {i + 1}/{scrolls}")


if __name__ == "__main__":
    asyncio.run(main())
