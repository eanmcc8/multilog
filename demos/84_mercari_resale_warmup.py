#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Mercari + Poshmark resale warmup — browse marketplace listings."""
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

MARKETS = {"mercari": "https://www.mercari.com/", "poshmark": "https://poshmark.com/"}


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    market = os.getenv("RESALE_MARKET", "mercari").lower()
    url = MARKETS.get(market, MARKETS["mercari"])
    scrolls = int(os.getenv("RESALE_SCROLLS", "5"))
    banner("Resale Marketplace Warmup", f"{market.title()} browse  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)
            section(f"Listings browse ({scrolls}x)")
            for i in range(scrolls):
                await random_mouse_wander(page, random.randint(2, 5))
                await human_scroll(page, random.randint(300, 700))
                await human_delay(2000, 4000)
                ok(f"Round {i + 1}/{scrolls}")
            ok(f"{market.title()} warmup complete")


if __name__ == "__main__":
    asyncio.run(main())
