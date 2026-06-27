"""Human-like interaction helpers — backend-agnostic where possible.

Async functions work with PlaywrightDriver pages.
Sync functions work with SeleniumDriver instances.
"""
from __future__ import annotations

import asyncio
import random
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stealthbrowser.drivers.playwright_driver import PlaywrightDriver
    from stealthbrowser.drivers.selenium_driver import SeleniumDriver


# ---------------------------------------------------------------------------
# Async helpers (Playwright)
# ---------------------------------------------------------------------------

async def human_delay(min_ms: int = 80, max_ms: int = 300) -> None:
    """Pause for a realistic human-range duration."""
    await asyncio.sleep(random.uniform(min_ms, max_ms) / 1000)


async def human_type(page, selector: str, text: str, *, clear_first: bool = True) -> None:
    """Type text character-by-character with randomized inter-key delays."""
    await page.click(selector)
    await human_delay(100, 350)
    if clear_first:
        await page.fill(selector, "")
    for char in text:
        await page.keyboard.type(char, delay=random.randint(35, 130))
        if random.random() < 0.07:
            await human_delay(200, 500)


async def human_click(page, selector: str) -> None:
    """Click at a random point within the element bounding box."""
    loc = page.locator(selector)
    box = await loc.bounding_box()
    if box:
        x = box["x"] + box["width"] * random.uniform(0.2, 0.8)
        y = box["y"] + box["height"] * random.uniform(0.2, 0.8)
        steps = random.randint(8, 20)
        await page.mouse.move(x, y, steps=steps)
        await human_delay(40, 120)
        await page.mouse.click(x, y)
    else:
        await loc.click()
    await human_delay(150, 400)


async def human_scroll(page, pixels: int = 400, *, direction: str = "down") -> None:
    """Scroll in natural-feeling chunks."""
    sign = 1 if direction == "down" else -1
    steps = random.randint(3, 8)
    per_step = (pixels // steps) * sign
    for _ in range(steps):
        await page.mouse.wheel(0, per_step + random.randint(-15, 15))
        await human_delay(70, 180)


async def random_mouse_wander(page, moves: int = 8) -> None:
    """Move the mouse randomly around the viewport."""
    vp = page.viewport_size or {"width": 1280, "height": 720}
    w, h = vp["width"], vp["height"]
    for _ in range(moves):
        x = random.randint(40, max(41, w - 40))
        y = random.randint(40, max(41, h - 40))
        await page.mouse.move(x, y, steps=random.randint(5, 15))
        await human_delay(100, 300)


async def random_page_activity(
    page, *, scrolls: int = 5, wander_moves: int = 4
) -> None:
    """Combine scrolling and mouse movement for realistic page dwell."""
    for _ in range(scrolls):
        await human_scroll(page, random.randint(200, 600))
        await human_delay(500, 1500)
    await random_mouse_wander(page, moves=wander_moves)


async def human_hover(page, selector: str) -> None:
    """Move the mouse over an element without clicking."""
    loc = page.locator(selector)
    box = await loc.bounding_box()
    if box:
        x = box["x"] + box["width"] * random.uniform(0.3, 0.7)
        y = box["y"] + box["height"] * random.uniform(0.3, 0.7)
        await page.mouse.move(x, y, steps=random.randint(6, 14))
        await human_delay(200, 600)


async def slow_read(page, seconds: float = 3.0) -> None:
    """Simulate someone reading the page (occasional small scrolls + pauses)."""
    end = asyncio.get_event_loop().time() + seconds
    while asyncio.get_event_loop().time() < end:
        await human_delay(800, 2000)
        if random.random() < 0.4:
            await human_scroll(page, random.randint(50, 200))


# ---------------------------------------------------------------------------
# Sync helpers (Selenium)
# ---------------------------------------------------------------------------

def sync_delay(min_ms: int = 80, max_ms: int = 300) -> None:
    time.sleep(random.uniform(min_ms, max_ms) / 1000)


def sync_type(element, text: str) -> None:
    element.clear()
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.04, 0.13))
        if random.random() < 0.07:
            time.sleep(random.uniform(0.2, 0.5))


def sync_scroll(driver, pixels: int = 400) -> None:
    steps = random.randint(3, 7)
    per_step = pixels // steps
    for _ in range(steps):
        driver.execute_script(f"window.scrollBy(0, {per_step + random.randint(-15, 15)});")
        time.sleep(random.uniform(0.07, 0.18))


def sync_random_activity(driver, *, scrolls: int = 4) -> None:
    for _ in range(scrolls):
        sync_scroll(driver, random.randint(200, 500))
        time.sleep(random.uniform(0.5, 1.5))
