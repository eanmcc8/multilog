#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: WhatsApp Web session warmup."""
import asyncio
import os

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    hold = int(os.getenv("WA_HOLD_SEC", "60"))
    banner("WhatsApp Web Warmup", f"Keep session {hold}s  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://web.whatsapp.com/", wait_until="domcontentloaded", timeout=90000)
            await human_delay(5000, 10000)
            warn("Scan QR in open profile if not linked")
            await page.wait_for_timeout(hold * 1000)
            ok("WhatsApp Web session held")


if __name__ == "__main__":
    asyncio.run(main())
