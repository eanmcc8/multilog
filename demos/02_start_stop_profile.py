#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: start profile, open URL, screenshot, stop."""
import asyncio
import os

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.env import ensure_output, load_env

load_env()


async def main():
    folder_id = os.getenv("MLX_FOLDER_ID", "")
    profile_id = os.getenv("MLX_PROFILE_ID", "")
    url = os.getenv("DEMO_URL", "https://bot.sannysoft.com/")

    if not folder_id or not profile_id:
        raise SystemExit("Set MLX_FOLDER_ID and MLX_PROFILE_ID in .env")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, profile_id, folder_id, pw) as session:
            page = await session.new_page()
            print(f"Opening {url} ...")
            await page.goto(url, wait_until="domcontentloaded")
            path = ensure_output() / "demo_screenshot.png"
            await page.screenshot(path=str(path))
            print(f"Saved {path}")


if __name__ == "__main__":
    asyncio.run(main())
