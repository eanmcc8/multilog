#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: Google login automation via Multilogin profile."""
import asyncio
import os

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, fail, ok, section, timestamp, warn
from mlx.env import ensure_output, load_env
from mlx.human import human_click, human_delay, human_type

load_env()


async def main():
    folder_id = os.getenv("MLX_FOLDER_ID", "")
    profile_id = os.getenv("MLX_PROFILE_ID", "")
    email = os.getenv("GOOGLE_EMAIL", os.getenv("MLX_EMAIL", ""))
    password = os.getenv("GOOGLE_PASSWORD", "")

    if not all([folder_id, profile_id, email, password]):
        raise SystemExit("Set MLX_FOLDER_ID, MLX_PROFILE_ID, GOOGLE_EMAIL, GOOGLE_PASSWORD in .env")

    banner("Google Login", f"Stealth sign-in  |  {timestamp()}")
    mlx = MultiloginX()

    async with async_playwright() as pw:
        async with profile_browser(mlx, profile_id, folder_id, pw) as session:
            page = await session.new_page()
            section("Navigate")
            await page.goto("https://accounts.google.com/", wait_until="domcontentloaded")
            await human_delay(800, 1500)

            section("Credentials")
            email_sel = 'input[type="email"]'
            await human_type(page, email_sel, email)
            await human_click(page, "#identifierNext")
            await human_delay(1000, 2000)

            pass_sel = 'input[type="password"]'
            await page.wait_for_selector(pass_sel, timeout=15000)
            await human_type(page, pass_sel, password)
            await human_click(page, "#passwordNext")
            await page.wait_for_timeout(6000)

            if "challenge" in page.url or "signin/v2" in page.url:
                warn("2FA or challenge detected - complete manually (90s)")
                await page.wait_for_timeout(90_000)

            path = ensure_output() / "google_login.png"
            await page.screenshot(path=str(path))
            if "myaccount.google.com" in page.url or "mail.google" in page.url:
                ok(f"Login success -> {path.name}")
            else:
                fail(f"Check screenshot: {path.name}")


if __name__ == "__main__":
    asyncio.run(main())
