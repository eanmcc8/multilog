#!/usr/bin/env python3
"""Demo: validate multiple proxies from proxies.txt."""

from mlx import MultiloginX
from mlx.console import banner, fail, ok, progress, section, table, timestamp
from mlx.env import ROOT, load_env

load_env()

PROXY_FILE = ROOT / "proxies.txt"


def parse_proxy(line: str) -> tuple[str, int, str, str, str] | None:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    # host:port or host:port:user:pass or type://host:port
    ptype = "http"
    if "://" in line:
        ptype, line = line.split("://", 1)
    parts = line.split(":")
    if len(parts) < 2:
        return None
    host = parts[0]
    port = int(parts[1])
    user = parts[2] if len(parts) > 2 else ""
    pwd = parts[3] if len(parts) > 3 else ""
    return host, port, ptype, user, pwd


def main():
    banner("Bulk Proxy Checker", f"Launcher API validate  |  {timestamp()}")

    if not PROXY_FILE.exists():
        PROXY_FILE.write_text(
            "# host:port or host:port:user:pass\n"
            "# 127.0.0.1:8080\n"
            "# socks5://proxy.example.com:1080:user:pass\n",
            encoding="utf-8",
        )
        raise SystemExit(f"Created sample {PROXY_FILE} - add proxies and re-run")

    lines = [l for l in PROXY_FILE.read_text(encoding="utf-8").splitlines() if parse_proxy(l)]
    if not lines:
        raise SystemExit(f"No proxies in {PROXY_FILE}")

    mlx = MultiloginX()
    section(f"Checking {len(lines)} proxy(s)")
    rows = []
    for i, line in enumerate(lines, 1):
        parsed = parse_proxy(line)
        if not parsed:
            continue
        host, port, ptype, user, pwd = parsed
        progress(i - 1, len(lines), host)
        try:
            result = mlx.validate_proxy(host, port, ptype, user, pwd)
            data = result.get("data", result)
            valid = data.get("is_valid", False)
            ip = data.get("ip", "?")
            country = data.get("country", "?")
            rows.append([f"{host}:{port}", "OK" if valid else "DEAD", ip, country])
            ok(f"{host}:{port} -> {ip} ({country})") if valid else fail(f"{host}:{port} dead")
        except Exception as exc:
            rows.append([f"{host}:{port}", "ERR", "-", "-"])
            fail(str(exc))
        progress(i, len(lines))

    section("Summary")
    table(["Proxy", "Status", "IP", "Country"], rows)
    live = sum(1 for r in rows if r[1] == "OK")
    ok(f"{live}/{len(rows)} proxies alive")
    print()


if __name__ == "__main__":
    main()
