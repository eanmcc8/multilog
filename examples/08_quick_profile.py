#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Example: launch a disposable quick profile (v3 API)."""
import asyncio

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import connect_playwright
from mlx.console import banner, ok, promo_footer
from mlx.env import load_env

load_env()


async def main() -> None:
    banner("Example 08 — Quick Profile")
    mlx = MultiloginX()
    payload = mlx.build_quick_profile_payload()
    session = mlx.start_quick_profile(payload)

    async with async_playwright() as pw:
        browser, context = await connect_playwright(mlx, session, pw)
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto("https://example.com", wait_until="domcontentloaded")
        ok(f"Quick profile running — port {session.port}")
        await browser.close()

    mlx.stop_profile(session.profile_id)
    promo_footer()


if __name__ == "__main__":
    asyncio.run(main())
