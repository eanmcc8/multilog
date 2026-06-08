#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: Twitter/X cross-mention and reply trust builder."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, fail, ok, section, timestamp, warn
from mlx.env import ROOT, load_env, require_env
from mlx.human import human_delay, human_scroll, human_type

load_env()

MENTIONS_FILE = ROOT / "mentions.txt"


def load_targets() -> list[str]:
    if MENTIONS_FILE.exists():
        lines = [
            l.strip()
            for l in MENTIONS_FILE.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")
        ]
        if lines:
            return lines
    sample = "# @handle per line\n@elonmusk\n@OpenAI\n"
    MENTIONS_FILE.write_text(sample, encoding="utf-8")
    return ["@OpenAI"]


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    tweet_url = os.getenv("TWITTER_TWEET_URL", "")
    targets = load_targets()[: int(os.getenv("TWITTER_MENTION_COUNT", "3"))]

    banner("Twitter Mass Mention", f"Cross-tag trust builder  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Open X / Twitter")
            await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)

            if "login" in page.url.lower():
                warn("Not logged in — import cookies or login first")

            if tweet_url:
                section("Reply on tweet")
                await page.goto(tweet_url, wait_until="domcontentloaded", timeout=45000)
                await human_delay(2000, 4000)
                reply_box = page.locator('[data-testid="tweetTextarea_0"], div[role="textbox"]').first
                if await reply_box.count():
                    mentions = " ".join(random.sample(targets, min(2, len(targets))))
                    text = os.getenv("TWITTER_REPLY_TEXT", f"Great thread! {mentions}")
                    await human_type(page, '[data-testid="tweetTextarea_0"]', text)
                    await human_delay(1000, 2000)
                    post = page.locator('[data-testid="tweetButton"], button:has-text("Reply")')
                    if await post.count() and os.getenv("TWITTER_DRY_RUN", "true").lower() != "true":
                        await post.first.click()
                        ok("Reply posted")
                    else:
                        warn("Dry-run: set TWITTER_DRY_RUN=false to post")
                else:
                    fail("Reply box not found")
            else:
                section("Compose mention tweet")
                compose = page.locator('[data-testid="SideNav_NewTweet_Button"], a[href="/compose/tweet"]')
                if await compose.count():
                    await compose.first.click()
                    await human_delay(1500, 3000)
                mentions = " ".join(targets)
                text = os.getenv("TWITTER_TWEET_TEXT", f"Hello {mentions} #automation")
                box = '[data-testid="tweetTextarea_0"]'
                if await page.locator(box).count():
                    await human_type(page, box, text)
                    ok(f"Draft ready: {text[:60]}...")
                    warn("Set TWITTER_DRY_RUN=false to publish")

            await human_scroll(page, random.randint(200, 500))


if __name__ == "__main__":
    asyncio.run(main())
