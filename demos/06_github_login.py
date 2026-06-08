#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: GitHub login via Multilogin X + Playwright."""
import asyncio

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.env import ensure_output, require_env
from mlx.human import human_click, human_delay, human_type

SELECTORS = {
    "username": "#login_field",
    "password": "#password",
    "submit": 'input[type="submit"][value="Sign in"]',
}


async def login(page, username: str, password: str) -> bool:
    await page.goto("https://github.com/login", wait_until="domcontentloaded")
    await human_delay(500, 1200)
    await human_type(page, SELECTORS["username"], username)
    await human_delay(300, 700)
    await human_type(page, SELECTORS["password"], password)
    await human_delay(400, 900)
    await human_click(page, SELECTORS["submit"])
    await page.wait_for_timeout(5000)
    if "sessions/two-factor" in page.url:
        print("[WARN] 2FA required — complete manually in browser (120s wait)")
        await page.wait_for_timeout(120_000)
    return "github.com" in page.url and "login" not in page.url


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID", "GITHUB_USERNAME", "GITHUB_PASSWORD")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            ok = await login(page, env["GITHUB_USERNAME"], env["GITHUB_PASSWORD"])
            path = ensure_output() / "github_login.png"
            await page.screenshot(path=str(path))
            print("SUCCESS" if ok else f"FAILED — check {path}")


if __name__ == "__main__":
    asyncio.run(main())
