#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Telegram Web session warmup."""
import asyncio
import os

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    banner("Telegram Web Warmup", f"Web client  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://web.telegram.org/k/", wait_until="domcontentloaded", timeout=90000)
            await human_delay(4000, 8000)
            warn("Login via phone QR in profile if needed")
            for i in range(int(os.getenv("TG_WEB_SCROLLS", "4"))):
                await human_scroll(page, 300)
                await human_delay(3000, 6000)
                ok(f"Chat list scroll {i + 1}")


if __name__ == "__main__":
    asyncio.run(main())
