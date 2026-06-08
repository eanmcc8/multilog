#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Example: start profile, visit URL, save screenshot."""
import asyncio
import os

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, promo_footer
from mlx.env import ensure_output, load_env, require_env

load_env()


async def main() -> None:
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    url = os.getenv("DEMO_URL", "https://example.com")
    banner("Example 02 — Screenshot")
    mlx = MultiloginX()

    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            path = ensure_output() / "example_screenshot.png"
            await page.screenshot(path=str(path))
            ok(f"Saved {path}")
    promo_footer()


if __name__ == "__main__":
    asyncio.run(main())
