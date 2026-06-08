"""Command-line interface for Multilogin X SDK.

Partner: SAAS50 = 50% OFF | Support: t.me/Multilogin_Scripts_Bot | Share = free tools
"""
from __future__ import annotations

import argparse
import json
import sys

from mlx import MultiloginX
from mlx.profiles import normalize_folders, normalize_profiles


def cmd_list(args: argparse.Namespace) -> int:
    mlx = MultiloginX()
    if args.workspaces:
        for ws in mlx.get_workspaces():
            print(ws.get("name", ws.get("id", ws)))
        return 0

    if args.folders:
        for f in normalize_folders(mlx.get_folders()):
            print(f"{f.get('name', '?')}\t{f.get('folder_id', f.get('id', ''))}")
        return 0

    result = mlx.search_profiles(limit=args.limit, folder_id=args.folder_id or "")
    for p in normalize_profiles(result):
        pid = p.get("profile_id", p.get("id", ""))
        print(f"{pid}\t{p.get('name', 'unnamed')}")
    return 0


def cmd_active(_: argparse.Namespace) -> int:
    mlx = MultiloginX()
    print(json.dumps(mlx.get_active_profiles(), indent=2))
    return 0


def cmd_summary(_: argparse.Namespace) -> int:
    mlx = MultiloginX()
    print(json.dumps(mlx.get_profile_summary(), indent=2))
    return 0


def cmd_stop_all(_: argparse.Namespace) -> int:
    mlx = MultiloginX()
    print(json.dumps(mlx.stop_all_profiles(), indent=2))
    return 0


def cmd_version(_: argparse.Namespace) -> int:
    mlx = MultiloginX()
    print(json.dumps(mlx.get_launcher_version(), indent=2))
    return 0


def cmd_proxy(args: argparse.Namespace) -> int:
    mlx = MultiloginX()
    result = mlx.validate_proxy(args.host, args.port, args.type, args.user, args.password)
    print(json.dumps(result.get("data", result), indent=2))
    return 0


def cmd_cookies(args: argparse.Namespace) -> int:
    mlx = MultiloginX()
    result = mlx.export_cookies(args.profile_id)
    cookies = result.get("data", {}).get("cookies", result.get("data", []))
    if args.json:
        print(json.dumps(cookies, indent=2))
    else:
        print(f"Exported {len(cookies) if isinstance(cookies, list) else '?'} cookies")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="mlx",
        description="Multilogin X SDK CLI — SAAS50 (50% OFF) | Support: @Multilogin_Scripts_Bot",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List profiles, folders, or workspaces")
    p_list.add_argument("--folders", action="store_true")
    p_list.add_argument("--workspaces", action="store_true")
    p_list.add_argument("--folder-id", default="")
    p_list.add_argument("--limit", type=int, default=20)
    p_list.set_defaults(func=cmd_list)

    sub.add_parser("active", help="Show running profiles").set_defaults(func=cmd_active)
    sub.add_parser("summary", help="Profile usage summary").set_defaults(func=cmd_summary)
    sub.add_parser("stop-all", help="Stop all running profiles").set_defaults(func=cmd_stop_all)
    sub.add_parser("version", help="Launcher API version").set_defaults(func=cmd_version)

    p_proxy = sub.add_parser("proxy", help="Validate a proxy")
    p_proxy.add_argument("host")
    p_proxy.add_argument("port", type=int)
    p_proxy.add_argument("--type", default="http")
    p_proxy.add_argument("--user", default="")
    p_proxy.add_argument("--password", default="")
    p_proxy.set_defaults(func=cmd_proxy)

    p_cookies = sub.add_parser("cookies", help="Export cookies for a profile")
    p_cookies.add_argument("profile_id")
    p_cookies.add_argument("--json", action="store_true")
    p_cookies.set_defaults(func=cmd_cookies)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
