#!/usr/bin/env python3
"""Demo: accept Facebook Business Manager invitation link."""
import asyncio
import os

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import ensure_output, load_env, require_env
from mlx.human import human_click, human_delay

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    invite_url = os.getenv("FB_BM_INVITE_URL", "")
    if not invite_url:
        raise SystemExit("Set FB_BM_INVITE_URL in .env (Business Manager invite link)")

    banner("FB BM Invitation Accepter", f"Via / BM onboarding  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Open invite link")
            await page.goto(invite_url, wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)

            if "login" in page.url.lower():
                warn("Login required — complete sign-in then re-run")

            section("Accept invitation")
            for label in ("Accept", "Join", "Confirm", "Get Started", "Continue"):
                btn = page.locator(f'button:has-text("{label}"), div[role="button"]:has-text("{label}")')
                if await btn.count():
                    try:
                        await human_click(page, f'button:has-text("{label}")')
                        ok(f"Clicked: {label}")
                        break
                    except Exception:
                        continue
            else:
                warn("No accept button found — complete manually in open browser")

            await human_delay(5000, 8000)
            path = ensure_output() / "fb_bm_invite.png"
            await page.screenshot(path=str(path))
            ok(f"Screenshot -> {path.name}")


if __name__ == "__main__":
    asyncio.run(main())
