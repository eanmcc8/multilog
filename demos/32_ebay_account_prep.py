#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: eBay account registration environment prep (clean fingerprint + browse)."""
import asyncio
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import ensure_output, load_env, require_env
from mlx.human import human_delay, human_scroll, random_page_activity

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    banner("eBay Stealth Account Prep", f"Clean env before reg  |  {timestamp()}")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()

            section("Warm generic sites first")
            for url in ("https://www.google.com", "https://www.ebay.com"):
                await page.goto(url, wait_until="domcontentloaded", timeout=45000)
                await random_page_activity(page, scrolls=random.randint(2, 5), clicks=1)
                await human_delay(2000, 4000)

            section("eBay registration page")
            await page.goto("https://signup.ebay.com/pa/crte", wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)
            await human_scroll(page, random.randint(200, 500))

            path = ensure_output() / "ebay_reg_prep.png"
            await page.screenshot(path=str(path), full_page=True)
            ok(f"Environment ready -> {path.name}")
            warn("Complete registration manually or extend with your signup flow")


if __name__ == "__main__":
    asyncio.run(main())
