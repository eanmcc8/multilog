#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Temu + Shein shop warmup — browse deals and categories."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, random_mouse_wander

load_env()

SHOPS = {"temu": "https://www.temu.com/", "shein": "https://www.shein.com/"}


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    shop = os.getenv("DISCOUNT_SHOP", "temu").lower()
    url = SHOPS.get(shop, SHOPS["temu"])
    scrolls = int(os.getenv("DISCOUNT_SCROLLS", "6"))
    banner("Discount Shop Warmup", f"{shop.title()} browse  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=90000)
            await human_delay(4000, 7000)
            section(f"Deals browse ({scrolls}x)")
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 6))
                await human_scroll(page, random.randint(300, 700))
                await human_delay(2000, 4000)
                ok(f"Round {i + 1}/{scrolls}")
            ok(f"{shop.title()} warmup complete")


if __name__ == "__main__":
    asyncio.run(main())
