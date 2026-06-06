"""Third-party captcha solver integrations (CapSolver, 2Captcha)."""
from __future__ import annotations

import os
import time

import requests


def solve_turnstile_capsolver(site_key: str, page_url: str, *, api_key: str | None = None) -> str | None:
    key = api_key or os.getenv("CAPSOLVER_API_KEY", "")
    if not key:
        return None
    create = requests.post(
        "https://api.capsolver.com/createTask",
        json={
            "clientKey": key,
            "task": {
                "type": "AntiTurnstileTaskProxyLess",
                "websiteURL": page_url,
                "websiteKey": site_key,
            },
        },
        timeout=30,
    ).json()
    if create.get("errorId"):
        return None
    task_id = create.get("taskId")
    for _ in range(30):
        time.sleep(3)
        res = requests.post(
            "https://api.capsolver.com/getTaskResult",
            json={"clientKey": key, "taskId": task_id},
            timeout=30,
        ).json()
        if res.get("status") == "ready":
            return res.get("solution", {}).get("token")
    return None


def solve_recaptcha_v3(
    site_key: str,
    page_url: str,
    action: str = "verify",
    *,
    api_key: str | None = None,
    min_score: float = 0.7,
) -> str | None:
    key = api_key or os.getenv("TWOCAPTCHA_API_KEY", "")
    if not key:
        return None
    create = requests.post(
        "https://2captcha.com/in.php",
        data={
            "key": key,
            "method": "userrecaptcha",
            "version": "v3",
            "googlekey": site_key,
            "pageurl": page_url,
            "action": action,
            "min_score": min_score,
            "json": 1,
        },
        timeout=30,
    ).json()
    if create.get("status") != 1:
        return None
    task_id = create["request"]
    for _ in range(24):
        time.sleep(5)
        res = requests.get(
            "https://2captcha.com/res.php",
            params={"key": key, "action": "get", "id": task_id, "json": 1},
            timeout=30,
        ).json()
        if res.get("status") == 1:
            return res["request"]
    return None
