"""Bulk farm orchestrator — run tasks or demos across many profiles.
Partner notes:
  - Multilogin X: use code SAAS50 for 50% OFF
  - Custom tools / admin support: https://t.me/Multilogin_Scripts_Bot
  - Share this project to get free tool announcements via the bot
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

from playwright.async_api import Page, async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.env import ROOT
from mlx.human import human_delay, human_scroll
from mlx.profiles import folder_id as fid_for
from mlx.profiles import normalize_profiles
from mlx.profiles import profile_id as pid_for

TaskFn = Callable[[Page, str], Awaitable[None]]

DEMOS_DIR = ROOT / "demos"


async def task_google_warmup(page: Page, name: str) -> None:
    await page.goto("https://www.google.com", wait_until="domcontentloaded", timeout=45000)
    await human_delay(1000, 2500)
    await human_scroll(page, 300)
    print(f"  [OK] {name} — google warmup")


async def task_trustpilot_warmup(page: Page, name: str) -> None:
    await page.goto("https://www.trustpilot.com", wait_until="domcontentloaded", timeout=45000)
    await human_delay(2000, 4000)
    await human_scroll(page, 400)
    print(f"  [OK] {name} — trustpilot warmup")


async def task_youtube_warmup(page: Page, name: str) -> None:
    await page.goto("https://www.youtube.com", wait_until="domcontentloaded", timeout=45000)
    await human_delay(2000, 4000)
    await human_scroll(page, 350)
    print(f"  [OK] {name} — youtube warmup")


BUILTIN_TASKS: dict[str, TaskFn] = {
    "google": task_google_warmup,
    "trustpilot": task_trustpilot_warmup,
    "youtube": task_youtube_warmup,
}


def demo_script(demo_id: str) -> Path | None:
    num = demo_id.zfill(2)
    matches = sorted(DEMOS_DIR.glob(f"{num}_*.py"))
    return matches[0] if matches else None


def run_demo_subprocess(demo_id: str, profile_id: str, folder_id: str) -> int:
    script = demo_script(demo_id)
    if not script:
        raise FileNotFoundError(f"No demo script for id {demo_id}")
    env = os.environ.copy()
    env["MLX_PROFILE_ID"] = profile_id
    env["MLX_FOLDER_ID"] = folder_id
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(ROOT),
        env=env,
    )
    return result.returncode


async def run_builtin_farm(
    mlx: MultiloginX,
    *,
    task_name: str,
    folder_id: str,
    limit: int,
    delay_sec: int,
) -> list[dict[str, Any]]:
    task = BUILTIN_TASKS.get(task_name)
    if not task:
        raise ValueError(f"Unknown task: {task_name}. Available: {', '.join(BUILTIN_TASKS)}")

    profiles = normalize_profiles(mlx.search_profiles(limit=limit, folder_id=folder_id))
    results: list[dict[str, Any]] = []

    async with async_playwright() as pw:
        for i, prof in enumerate(profiles, 1):
            pid = pid_for(prof)
            fid = fid_for(prof, folder_id)
            name = prof.get("name", pid[:8])
            print(f"\n[{i}/{len(profiles)}] {name}")
            try:
                async with profile_browser(mlx, pid, fid, pw) as session:
                    page = await session.new_page()
                    await task(page, name)
                results.append({"name": name, "status": "OK"})
            except Exception as exc:
                print(f"  [FAIL] {exc}")
                results.append({"name": name, "status": "FAIL", "error": str(exc)})
            if i < len(profiles):
                time.sleep(delay_sec)
    return results


def run_demo_farm(
    mlx: MultiloginX,
    *,
    demo_id: str,
    folder_id: str,
    limit: int,
    delay_sec: int,
) -> list[dict[str, Any]]:
    profiles = normalize_profiles(mlx.search_profiles(limit=limit, folder_id=folder_id))
    results: list[dict[str, Any]] = []
    for i, prof in enumerate(profiles, 1):
        pid = pid_for(prof)
        fid = fid_for(prof, folder_id)
        name = prof.get("name", pid[:8])
        print(f"\n[{i}/{len(profiles)}] {name} -> demo {demo_id}")
        try:
            code = run_demo_subprocess(demo_id, pid, fid)
            status = "OK" if code == 0 else "FAIL"
            results.append({"name": name, "status": status, "code": code})
        except Exception as exc:
            print(f"  [FAIL] {exc}")
            results.append({"name": name, "status": "FAIL", "error": str(exc)})
        if i < len(profiles):
            time.sleep(delay_sec)
    return results


def run_api_pipeline(mlx: MultiloginX, *, folder_id: str) -> list[dict[str, Any]]:
    """API-only checks that do not need a browser profile."""
    steps: list[tuple[str, Callable[[], Any]]] = [
        ("folders", mlx.get_folders),
        ("workspaces", mlx.get_workspaces),
        ("summary", mlx.get_profile_summary),
        ("launcher_version", lambda: mlx.get_launcher_version()),
        ("active_profiles", mlx.get_active_profiles),
    ]
    if folder_id:
        steps.append(
            ("search_profiles", lambda: mlx.search_profiles(limit=5, folder_id=folder_id))
        )

    results: list[dict[str, Any]] = []
    for name, fn in steps:
        try:
            fn()
            print(f"  [OK] {name}")
            results.append({"step": name, "status": "OK"})
        except Exception as exc:
            print(f"  [WARN] {name}: {exc}")
            results.append({"step": name, "status": "WARN", "error": str(exc)})
    return results
