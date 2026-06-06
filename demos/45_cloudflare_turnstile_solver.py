#!/usr/bin/env python3
"""Demo: Cloudflare Turnstile solver via CapSolver API."""
import asyncio
import os

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.captcha import solve_turnstile_capsolver
from mlx.console import banner, fail, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    target = os.getenv("TURNSTILE_TEST_URL", "https://demo.turnstile.workers.dev")

    banner("Cloudflare Turnstile Solver", f"CapSolver integration  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section(f"Load page: {target}")
            await page.goto(target, wait_until="domcontentloaded", timeout=60000)
            await human_delay(2000, 4000)

            widget = page.locator("[data-sitekey], .cf-turnstile")
            if not await widget.count():
                fail("No Turnstile widget found")
                return

            site_key = await widget.first.get_attribute("data-sitekey")
            if not site_key:
                fail("Missing data-sitekey")
                return

            section("Solve via CapSolver")
            token = solve_turnstile_capsolver(site_key, page.url)
            if not token:
                warn("Set CAPSOLVER_API_KEY in .env")
                return

            await page.evaluate(
                """(t) => {
                    const el = document.querySelector('[name="cf-turnstile-response"]');
                    if (el) el.value = t;
                }""",
                token,
            )
            ok("Turnstile token injected — submit form or continue scrape")


if __name__ == "__main__":
    asyncio.run(main())
