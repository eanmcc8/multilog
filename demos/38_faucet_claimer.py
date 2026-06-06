#!/usr/bin/env python3
"""Demo: testnet faucet claimer with optional 2Captcha integration."""
import asyncio
import os

import requests
from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, fail, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_type

load_env()


def solve_2captcha(site_key: str, page_url: str) -> str | None:
    api_key = os.getenv("TWOCAPTCHA_API_KEY", "")
    if not api_key:
        return None
    create = requests.post(
        "https://2captcha.com/in.php",
        data={
            "key": api_key,
            "method": "userrecaptcha",
            "googlekey": site_key,
            "pageurl": page_url,
            "json": 1,
        },
        timeout=30,
    ).json()
    if create.get("status") != 1:
        fail(f"2Captcha submit failed: {create}")
        return None
    task_id = create["request"]
    for _ in range(24):
        import time

        time.sleep(5)
        res = requests.get(
            "https://2captcha.com/res.php",
            params={"key": api_key, "action": "get", "id": task_id, "json": 1},
            timeout=30,
        ).json()
        if res.get("status") == 1:
            return res["request"]
    fail("2Captcha timeout")
    return None


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    faucet_url = os.getenv(
        "FAUCET_URL",
        "https://sepoliafaucet.com",
    )
    wallet = os.getenv("FAUCET_WALLET_ADDRESS", "")

    banner("Faucet Claimer Bot", f"Testnet tokens + captcha  |  {timestamp()}")
    if not wallet:
        warn("Set FAUCET_WALLET_ADDRESS in .env")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section(f"Open faucet: {faucet_url}")
            await page.goto(faucet_url, wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)

            addr_input = page.locator('input[name="address"], input[placeholder*="address"], input[type="text"]').first
            if wallet and await addr_input.count():
                await human_type(page, 'input[name="address"], input[placeholder*="address"]', wallet)

            site_key_el = page.locator("[data-sitekey]")
            if await site_key_el.count():
                site_key = await site_key_el.first.get_attribute("data-sitekey")
                if site_key and os.getenv("TWOCAPTCHA_API_KEY"):
                    section("Solving captcha via 2Captcha")
                    token = solve_2captcha(site_key, page.url)
                    if token:
                        await page.evaluate(
                            """(t) => {
                                const el = document.querySelector('[name="g-recaptcha-response"], textarea[name="g-recaptcha-response"]');
                                if (el) el.value = t;
                            }""",
                            token,
                        )
                        ok("Captcha token injected")
                else:
                    warn("Set TWOCAPTCHA_API_KEY for auto-captcha or solve manually")

            submit = page.locator('button:has-text("Send"), button:has-text("Request"), button[type="submit"]')
            if await submit.count():
                if os.getenv("FAUCET_AUTO_SUBMIT", "false").lower() == "true":
                    await submit.first.click()
                    ok("Faucet submitted")
                else:
                    warn("Set FAUCET_AUTO_SUBMIT=true to submit (manual review recommended)")


if __name__ == "__main__":
    asyncio.run(main())
