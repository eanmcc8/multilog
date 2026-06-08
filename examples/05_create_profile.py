#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Example: create one profile in your folder."""
import os

from mlx import MultiloginX
from mlx.console import banner, ok, promo_footer
from mlx.env import load_env, require_env

load_env()


def main() -> None:
    env = require_env("MLX_FOLDER_ID")
    name = os.getenv("EXAMPLE_PROFILE_NAME", "SDK-Example-Profile")
    banner("Example 05 — Create Profile")
    mlx = MultiloginX()
    resp = mlx.create_profile(name, env["MLX_FOLDER_ID"], browser_type="mimic", os_type="windows")
    pid = resp.get("data", {}).get("profile_id", "?")
    ok(f"Created {name} → {pid}")
    promo_footer()


if __name__ == "__main__":
    main()
