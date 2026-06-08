#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Example: validate every proxy in proxies.txt."""
from mlx import MultiloginX
from mlx.console import banner, ok, promo_footer, table
from mlx.env import ROOT, load_env
from mlx.proxy_utils import parse_proxy

load_env()
PROXY_FILE = ROOT / "proxies.txt"


def main() -> None:
    banner("Example 03 — Proxy Validate")
    if not PROXY_FILE.exists():
        raise SystemExit("Copy proxies.txt.example to proxies.txt first")

    mlx = MultiloginX()
    rows: list[list[str]] = []
    for line in PROXY_FILE.read_text(encoding="utf-8").splitlines():
        parsed = parse_proxy(line)
        if not parsed:
            continue
        host, port, ptype, user, pwd = parsed
        try:
            r = mlx.validate_proxy(host, port, ptype, user, pwd)
            data = r.get("data", r)
            rows.append([f"{host}:{port}", "OK" if data.get("is_valid") else "DEAD", str(data.get("ip", "?"))])
        except Exception as exc:
            rows.append([f"{host}:{port}", "ERR", str(exc)[:30]])

    table(["Proxy", "Status", "IP"], rows)
    ok(f"Checked {len(rows)} proxy(s)")
    promo_footer()


if __name__ == "__main__":
    main()
