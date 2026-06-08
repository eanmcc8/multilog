#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Shopee / Lazada SEA marketplace warmup."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, timestamp
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll

load_env()

SITES = [
    ("Shopee", "https://shopee.vn"),
    ("Lazada", "https://www.lazada.vn"),
]


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    site = os.getenv("SEA_SHOP", "shopee")
    url = next((u for n, u in SITES if site.lower() in n.lower()), SITES[0][1])
    banner("SEA E-commerce Warmup", f"{url}  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)
            for i in range(int(os.getenv("SEA_SCROLLS", "6"))):
                await human_scroll(page, random.randint(300, 700))
                await human_delay(2000, 5000)
                ok(f"Browse {i + 1}")


if __name__ == "__main__":
    asyncio.run(main())
