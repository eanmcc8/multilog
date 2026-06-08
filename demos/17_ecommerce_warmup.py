#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: e-commerce browsing warmup (Amazon, eBay)."""
import asyncio
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, fail, ok, section, timestamp
from mlx.env import ensure_output, load_env, require_env
from mlx.human import human_delay, human_scroll

SITES = [
    ("Amazon", "https://www.amazon.com/"),
    ("eBay", "https://www.ebay.com/"),
]

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    banner("E-commerce Warmup", f"Shopping site activity  |  {timestamp()}")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            for name, url in SITES:
                section(name)
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    await human_delay(2000, 4000)
                    for _ in range(random.randint(3, 6)):
                        await human_scroll(page, random.randint(200, 500))
                        await human_delay(1000, 2500)
                    safe = name.lower()
                    path = ensure_output() / f"ecommerce_{safe}.png"
                    await page.screenshot(path=str(path))
                    ok(f"{name} done -> {path.name}")
                except Exception as exc:
                    fail(str(exc))


if __name__ == "__main__":
    asyncio.run(main())
