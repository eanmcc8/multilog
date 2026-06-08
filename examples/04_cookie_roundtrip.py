#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Example: export cookies to JSON (import via mlx.import_cookies)."""
import json

from mlx import MultiloginX
from mlx.console import banner, ok, promo_footer
from mlx.env import ensure_output, load_env, require_env

load_env()


def main() -> None:
    pid = require_env("MLX_PROFILE_ID")["MLX_PROFILE_ID"]
    banner("Example 04 — Cookie Export")
    mlx = MultiloginX()
    result = mlx.export_cookies(pid)
    cookies = result.get("data", {}).get("cookies", result.get("data", []))
    path = ensure_output() / f"example_cookies_{pid[:8]}.json"
    path.write_text(json.dumps(cookies, indent=2), encoding="utf-8")
    ok(f"Exported {len(cookies)} cookies → {path}")
    ok("Re-import: mlx.import_cookies(profile_id, cookies)")
    promo_footer()


if __name__ == "__main__":
    main()
