#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: check 2Captcha / CapSolver account balance."""
import os

import requests

from mlx.console import banner, ok, section, table, timestamp, warn
from mlx.env import load_env

load_env()


def twocaptcha_balance(key: str) -> str:
    r = requests.get(
        "https://2captcha.com/res.php",
        params={"key": key, "action": "getbalance", "json": 1},
        timeout=30,
    ).json()
    if r.get("status") == 1:
        return f"${r['request']}"
    return r.get("request", "error")


def capsolver_balance(key: str) -> str:
    r = requests.post(
        "https://api.capsolver.com/getBalance",
        json={"clientKey": key},
        timeout=30,
    ).json()
    if r.get("errorId") == 0:
        return f"${r.get('balance', 0)}"
    return r.get("errorDescription", "error")


def main():
    banner("Captcha Balance Check", f"API wallet  |  {timestamp()}")
    tc = os.getenv("TWOCAPTCHA_API_KEY", "")
    cs = os.getenv("CAPSOLVER_API_KEY", "")
    rows: list[list[str]] = []
    section("Balances")
    if tc:
        rows.append(["2Captcha", twocaptcha_balance(tc)])
    else:
        warn("Set TWOCAPTCHA_API_KEY")
    if cs:
        rows.append(["CapSolver", capsolver_balance(cs)])
    else:
        warn("Set CAPSOLVER_API_KEY")
    if rows:
        table(["Provider", "Balance"], rows)
        ok("Top up before running demos 38/45/47")
    else:
        warn("No captcha API keys in .env")


if __name__ == "__main__":
    main()
