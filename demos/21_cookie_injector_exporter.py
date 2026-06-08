#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: bulk cookie export/import (JSON + Netscape) without opening browser."""
import os

from mlx import MultiloginX
from mlx.console import banner, fail, ok, progress, section, table, timestamp, warn
from mlx.cookies import load_cookies, save_cookies
from mlx.env import ROOT, ensure_output, load_env, require_env
from mlx.profiles import normalize_profiles, profile_id

load_env()

COOKIE_DIR = ROOT / "cookies"
MODE = os.getenv("COOKIE_BULK_MODE", "export")  # export | import


def main():
    env = require_env("MLX_FOLDER_ID")
    limit = int(os.getenv("COOKIE_BULK_LIMIT", "5"))
    fmt = os.getenv("COOKIE_BULK_FORMAT", "json")  # json | netscape

    banner("Cookie Injector / Exporter", f"Bulk {MODE}  |  {timestamp()}")
    mlx = MultiloginX()
    COOKIE_DIR.mkdir(parents=True, exist_ok=True)

    search = mlx.search_profiles(limit=limit, folder_id=env["MLX_FOLDER_ID"])
    profiles = normalize_profiles(search)[:limit]
    if not profiles:
        raise SystemExit("No profiles found")

    rows: list[list[str]] = []
    if MODE == "export":
        section(f"Exporting cookies for {len(profiles)} profile(s)")
        for i, prof in enumerate(profiles, 1):
            pid = profile_id(prof)
            name = prof.get("name", pid[:8])
            ext = "json" if fmt == "json" else "txt"
            out = COOKIE_DIR / f"{name}_{pid[:8]}.{ext}"
            progress(i - 1, len(profiles), name)
            try:
                result = mlx.export_cookies(pid)
                cookies = result.get("data", {}).get("cookies", result.get("data", []))
                save_cookies(cookies if isinstance(cookies, list) else [], out)
                rows.append([name, str(len(cookies)), out.name, "OK"])
                ok(f"{name} -> {out.name}")
            except Exception as exc:
                rows.append([name, "-", "-", "FAIL"])
                fail(str(exc))
            progress(i, len(profiles))
    else:
        section(f"Importing cookies into {len(profiles)} profile(s)")
        files = sorted(COOKIE_DIR.glob("*.*"))
        if not files:
            raise SystemExit(f"No cookie files in {COOKIE_DIR}")
        for i, prof in enumerate(profiles, 1):
            pid = profile_id(prof)
            name = prof.get("name", pid[:8])
            src = files[(i - 1) % len(files)]
            progress(i - 1, len(profiles), name)
            try:
                cookies = load_cookies(src)
                mlx.import_cookies(pid, cookies)
                rows.append([name, str(len(cookies)), src.name, "OK"])
                ok(f"{name} <- {src.name} ({len(cookies)} cookies)")
            except Exception as exc:
                rows.append([name, "-", src.name, "FAIL"])
                fail(str(exc))
            progress(i, len(profiles))

    section("Summary")
    table(["Profile", "Cookies", "File", "Status"], rows)
    warn("Set COOKIE_BULK_MODE=import and place files in ./cookies/")
    backup = ensure_output() / "cookie_bulk_report.txt"
    backup.write_text("\n".join("\t".join(r) for r in rows), encoding="utf-8")
    ok(f"Report -> {backup}")
    print()


if __name__ == "__main__":
    main()
