#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: export cookies from profile and save to JSON."""
import json

from mlx import MultiloginX
from mlx.env import ensure_output, load_env, require_env

load_env()


def main():
    profile_id = require_env("MLX_PROFILE_ID")["MLX_PROFILE_ID"]

    mlx = MultiloginX()
    print(f"Exporting cookies for {profile_id}...")
    result = mlx.export_cookies(profile_id)
    cookies = result.get("data", {}).get("cookies", result.get("data", []))

    path = ensure_output() / f"cookies_{profile_id[:8]}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=2)
    count = len(cookies) if isinstance(cookies, list) else "?"
    print(f"Saved {count} cookies -> {path}")


if __name__ == "__main__":
    main()
