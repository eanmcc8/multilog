#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Shopify store warmup — organic browse pattern."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, random_page_activity

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    store = os.getenv("SHOPIFY_STORE_URL", "")
    if not store:
        raise SystemExit("Set SHOPIFY_STORE_URL in .env")
    banner("Shopify Store Warmup", f"Store browse  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Shopify home first")
            await page.goto("https://www.shopify.com", wait_until="domcontentloaded", timeout=45000)
            await random_page_activity(page, scrolls=2, clicks=1)
            section("Target store")
            await page.goto(store, wait_until="domcontentloaded", timeout=60000)
            await human_delay(4000, 8000)
            for _ in range(random.randint(3, 6)):
                await human_scroll(page, random.randint(300, 650))
                await human_delay(random.randint(5, 12) * 1000, random.randint(5, 12) * 1000)
            ok("Shopify visit complete")


if __name__ == "__main__":
    asyncio.run(main())
