#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Discord web warmup — channels browse."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    invite = os.getenv("DISCORD_INVITE_URL", "https://discord.com/channels/@me")
    banner("Discord Warmup", f"Web client activity  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto(invite, wait_until="domcontentloaded", timeout=90000)
            await human_delay(4000, 8000)
            if "login" in page.url.lower():
                warn("Scan QR or login in open profile")
            for i in range(int(os.getenv("DISCORD_SCROLLS", "5"))):
                await human_scroll(page, random.randint(200, 500))
                await human_delay(3000, 7000)
                ok(f"Activity {i + 1}")


if __name__ == "__main__":
    asyncio.run(main())
