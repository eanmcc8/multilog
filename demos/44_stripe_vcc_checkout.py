#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: Stripe checkout with VCC — unique fingerprint per profile."""
import asyncio
import os

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_type, random_mouse_wander

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    checkout_url = os.getenv("STRIPE_CHECKOUT_URL", "")
    card = os.getenv("VCC_NUMBER", "")
    exp = os.getenv("VCC_EXP", "")
    cvc = os.getenv("VCC_CVC", "")
    dry_run = os.getenv("STRIPE_DRY_RUN", "true").lower() != "false"

    banner("Stripe VCC Checkout", f"Anti-decline checkout  |  {timestamp()}")
    if not checkout_url:
        raise SystemExit("Set STRIPE_CHECKOUT_URL in .env")
    warn("Requires deep hardware fingerprint — see README Important Note")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Open checkout")
            await page.goto(checkout_url, wait_until="domcontentloaded", timeout=90000)
            await human_delay(3000, 6000)
            await random_mouse_wander(page, 5)

            if not card:
                warn("Set VCC_NUMBER, VCC_EXP, VCC_CVC in .env")
                return

            section("Fill payment fields")
            fields = [
                ('input[name="cardNumber"], input[autocomplete="cc-number"]', card),
                ('input[name="cardExpiry"], input[autocomplete="cc-exp"]', exp),
                ('input[name="cardCvc"], input[autocomplete="cc-csc"]', cvc),
            ]
            for selector, value in fields:
                if value and await page.locator(selector).count():
                    await human_type(page, selector.split(",")[0], value)

            pay = page.locator('button:has-text("Pay"), button[type="submit"]')
            if await pay.count():
                if dry_run:
                    warn("Dry-run — set STRIPE_DRY_RUN=false to submit")
                else:
                    await pay.first.click()
                    ok("Payment submitted")
            ok("Checkout flow ready")


if __name__ == "__main__":
    asyncio.run(main())
