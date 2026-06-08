#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: launch a one-time quick profile (v3 API) and open a URL."""
import asyncio
import os

from dotenv import load_dotenv
from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import connect_playwright
from mlx.env import ensure_output

load_dotenv()


async def main():
    url = os.getenv("DEMO_URL", "https://bot.sannysoft.com/")
    mlx = MultiloginX()
    payload = mlx.build_quick_profile_payload(
        automation="playwright",
        parameters={"custom_start_urls": [url]},
    )
    print("Starting quick profile...")
    session = mlx.start_quick_profile(payload)
    print(f"CDP port: {session.port}")

    try:
        async with async_playwright() as pw:
            browser, context = await connect_playwright(mlx, session, pw)
            page = context.pages[0] if context.pages else await context.new_page()
            await page.goto(url, wait_until="domcontentloaded")
            path = ensure_output() / "quick_profile.png"
            await page.screenshot(path=str(path))
            print(f"Saved {path}")
            await browser.close()
    finally:
        mlx.stop_profile(session.profile_id)
        print("Quick profile stopped.")


if __name__ == "__main__":
    asyncio.run(main())
