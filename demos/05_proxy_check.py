#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: validate proxy before assigning to a profile."""
import os

from mlx import MultiloginX
from mlx.env import load_env

load_env()


def main():
    host = os.getenv("PROXY_HOST", "")
    port = int(os.getenv("PROXY_PORT", "0"))
    ptype = os.getenv("PROXY_TYPE", "http")
    user = os.getenv("PROXY_USER", "")
    pwd = os.getenv("PROXY_PASS", "")

    if not host or not port:
        raise SystemExit("Set PROXY_HOST and PROXY_PORT in .env")

    mlx = MultiloginX()
    print(f"Checking {ptype}://{host}:{port} ...")
    result = mlx.validate_proxy(host, port, ptype, user, pwd)
    data = result.get("data", result)
    print(f"Valid: {data.get('is_valid', False)} | IP: {data.get('ip', '?')} | Country: {data.get('country', '?')}")


if __name__ == "__main__":
    main()
