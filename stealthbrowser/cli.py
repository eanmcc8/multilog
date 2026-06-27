"""Command-line interface for StealthBrowser."""
from __future__ import annotations

import argparse
import json
import sys

from stealthbrowser.profile import BrowserProfile
from stealthbrowser import __version__


def cmd_profile(args: argparse.Namespace) -> int:
    if args.action == "create":
        p = BrowserProfile.random(
            os=args.os,
            driver=args.driver,
            headless=args.headless,
            name=args.name or "",
        )
        if args.proxy:
            from stealthbrowser.profile import ProxyConfig
            p.proxy = ProxyConfig.from_string(args.proxy)
        output = p.to_json()
        if args.output:
            import pathlib
            path = pathlib.Path(args.output)
            path.write_text(output)
            print(f"Saved profile to {path}")
        else:
            print(output)
        return 0

    elif args.action == "batch":
        profiles = BrowserProfile.batch(
            args.count,
            os=args.os,
            driver=args.driver,
            headless=args.headless,
            name_prefix=args.prefix,
        )
        data = [p.to_dict() for p in profiles]
        output = json.dumps(data, indent=2)
        if args.output:
            import pathlib
            path = pathlib.Path(args.output)
            path.write_text(output)
            print(f"Saved {len(profiles)} profiles to {path}")
        else:
            print(output)
        return 0

    elif args.action == "show":
        p = BrowserProfile.load(args.file)
        print(p.to_json())
        return 0

    print(f"Unknown profile action: {args.action}", file=sys.stderr)
    return 1


def cmd_fingerprint(args: argparse.Namespace) -> int:
    from stealthbrowser.profile import Fingerprint
    fp = Fingerprint.random(args.os)
    print(json.dumps({
        "user_agent": fp.user_agent,
        "platform": fp.platform,
        "webgl_vendor": fp.webgl_vendor,
        "webgl_renderer": fp.webgl_renderer,
        "resolution": f"{fp.resolution_width}x{fp.resolution_height}",
        "locale": fp.locale,
        "timezone": fp.timezone,
        "hardware_concurrency": fp.hardware_concurrency,
        "device_memory": fp.device_memory,
        "canvas_noise": fp.canvas_noise,
        "audio_noise": fp.audio_noise,
    }, indent=2))
    return 0


def cmd_fetch(args: argparse.Namespace) -> int:
    from stealthbrowser.profile import BrowserProfile
    from stealthbrowser.session import StealthSession

    profile = BrowserProfile.random(driver="http", os=args.os)
    if args.proxy:
        from stealthbrowser.profile import ProxyConfig
        profile.proxy = ProxyConfig.from_string(args.proxy)

    with StealthSession(profile) as s:
        s.get(args.url)
        if args.title:
            print("Title:", s.title())
        elif args.json:
            print(json.dumps(s.json(), indent=2))
        else:
            print(s.source()[:args.limit] if args.limit else s.source())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stealthbrowser",
        description=f"StealthBrowser v{__version__} — standalone multi-backend browser automation",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    # --- profile ---
    p_profile = sub.add_parser("profile", help="Create / inspect browser profiles")
    p_profile.add_argument("action", choices=["create", "batch", "show"], help="Action to perform")
    p_profile.add_argument("--os", default="windows", choices=["windows", "macos", "linux"])
    p_profile.add_argument("--driver", default="playwright", choices=["playwright", "selenium", "http"])
    p_profile.add_argument("--headless", action="store_true")
    p_profile.add_argument("--name", default="")
    p_profile.add_argument("--proxy", default="")
    p_profile.add_argument("--count", type=int, default=5, help="Number of profiles (batch)")
    p_profile.add_argument("--prefix", default="Profile", help="Name prefix (batch)")
    p_profile.add_argument("--output", "-o", default="", help="Output file path")
    p_profile.add_argument("--file", "-f", default="", help="Profile JSON file (show)")

    # --- fingerprint ---
    p_fp = sub.add_parser("fingerprint", help="Generate a random fingerprint")
    p_fp.add_argument("--os", default="windows", choices=["windows", "macos", "linux"])

    # --- fetch ---
    p_fetch = sub.add_parser("fetch", help="Fetch a URL using the HTTP driver")
    p_fetch.add_argument("url", help="URL to fetch")
    p_fetch.add_argument("--os", default="windows", choices=["windows", "macos", "linux"])
    p_fetch.add_argument("--proxy", default="")
    p_fetch.add_argument("--title", action="store_true", help="Print page title only")
    p_fetch.add_argument("--json", action="store_true", help="Parse response as JSON")
    p_fetch.add_argument("--limit", type=int, default=0, help="Truncate HTML output to N chars")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    handlers = {
        "profile": cmd_profile,
        "fingerprint": cmd_fingerprint,
        "fetch": cmd_fetch,
    }
    fn = handlers.get(args.command)
    if fn:
        sys.exit(fn(args))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
