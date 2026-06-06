"""Human-like interaction helpers for stealth automation."""
from __future__ import annotations

import asyncio
import random


async def human_delay(min_ms: int = 80, max_ms: int = 220) -> None:
    await asyncio.sleep(random.uniform(min_ms, max_ms) / 1000)


async def human_type(page, selector: str, text: str, *, clear_first: bool = True) -> None:
    await page.click(selector)
    await human_delay(100, 300)
    if clear_first:
        await page.fill(selector, "")
    for char in text:
        await page.keyboard.type(char, delay=random.randint(40, 120))
        if random.random() < 0.08:
            await human_delay(150, 400)


async def human_click(page, selector: str) -> None:
    loc = page.locator(selector)
    box = await loc.bounding_box()
    if box:
        x = box["x"] + box["width"] * random.uniform(0.25, 0.75)
        y = box["y"] + box["height"] * random.uniform(0.25, 0.75)
        await page.mouse.move(x, y, steps=random.randint(8, 18))
        await human_delay(50, 150)
        await page.mouse.click(x, y)
    else:
        await loc.click()
    await human_delay(200, 500)


async def human_scroll(page, pixels: int = 400) -> None:
    steps = random.randint(3, 7)
    per_step = pixels // steps
    for _ in range(steps):
        await page.mouse.wheel(0, per_step + random.randint(-20, 20))
        await human_delay(80, 200)


async def random_mouse_wander(page, moves: int = 8) -> None:
    viewport = page.viewport_size or {"width": 1280, "height": 720}
    w, h = viewport["width"], viewport["height"]
    for _ in range(moves):
        x = random.randint(40, max(41, w - 40))
        y = random.randint(40, max(41, h - 40))
        await page.mouse.move(x, y, steps=random.randint(6, 16))
        await human_delay(120, 350)


async def random_page_activity(page, *, scrolls: int = 5, clicks: int = 2) -> None:
    await random_mouse_wander(page, random.randint(4, 10))
    for _ in range(scrolls):
        await human_scroll(page, random.randint(150, 550))
        await human_delay(400, 1200)
    for _ in range(clicks):
        viewport = page.viewport_size or {"width": 1280, "height": 720}
        x = random.randint(80, viewport["width"] - 80)
        y = random.randint(120, viewport["height"] - 80)
        await page.mouse.click(x, y)
        await human_delay(300, 900)
