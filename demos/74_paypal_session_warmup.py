#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: PayPal session warmup — browse dashboard and activity."""
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
    hold_sec = int(os.getenv("PAYPAL_HOLD_SEC", "45"))
    banner("PayPal Session Warmup", f"Dashboard browse  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto("https://www.paypal.com/myaccount/summary", wait_until="domcontentloaded", timeout=60000)
            await human_delay(4000, 7000)
            if "signin" in page.url.lower() or "login" in page.url.lower():
                warn("Login manually or import cookies first")
            section(f"Session hold ~{hold_sec}s")
            elapsed = 0
            while elapsed < hold_sec:
                await random_mouse_wander(page, random.randint(2, 5))
                await human_scroll(page, random.randint(100, 300))
                await page.wait_for_timeout(5000)
                elapsed += 5
            ok("PayPal session warmup complete")


if __name__ == "__main__":
    asyncio.run(main())
