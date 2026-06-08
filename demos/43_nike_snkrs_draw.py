#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: Nike SNKRS draw entry — login, captcha hook, join draw."""
import asyncio
import os

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.captcha import solve_recaptcha_v3
from mlx.console import banner, fail, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_type

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    snkrs_url = os.getenv("SNKRS_URL", "https://www.nike.com/launch")
    email = os.getenv("SNKRS_EMAIL", os.getenv("MLX_EMAIL", ""))
    dry_run = os.getenv("SNKRS_DRY_RUN", "true").lower() != "false"

    banner("Nike SNKRS Draw Enterer", f"Launch / draw flow  |  {timestamp()}")
    warn("Requires deep hardware fingerprint — see README Important Note")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Open SNKRS launch")
            await page.goto(snkrs_url, wait_until="domcontentloaded", timeout=90000)
            await human_delay(4000, 8000)

            login = page.locator('a:has-text("Sign In"), button:has-text("Sign In")')
            if await login.count() and email:
                section("Sign in")
                await login.first.click()
                await human_delay(2000, 4000)
                email_box = page.locator('input[type="email"], input[name="emailAddress"]')
                if await email_box.count():
                    await human_type(page, 'input[type="email"]', email)
                    warn("Complete password / OTP in open profile")

            site_key_el = page.locator("[data-sitekey]")
            if await site_key_el.count():
                site_key = await site_key_el.first.get_attribute("data-sitekey")
                if site_key:
                    section("reCAPTCHA v3 token")
                    token = solve_recaptcha_v3(site_key, page.url, action="snkrs")
                    if token:
                        ok("Captcha token obtained")
                    else:
                        warn("Set TWOCAPTCHA_API_KEY for auto-solve")

            section("Join draw")
            enter = page.locator('button:has-text("Enter Draw"), button:has-text("Buy")')
            if await enter.count():
                if dry_run:
                    warn("Dry-run — set SNKRS_DRY_RUN=false to click")
                else:
                    await enter.first.click()
                    ok("Draw entry clicked")
            else:
                fail("Draw button not found — check launch URL")


if __name__ == "__main__":
    asyncio.run(main())
