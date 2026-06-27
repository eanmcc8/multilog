"""
Multilogin X Python SDK — Entry Point

This project is the Multilogin X Python SDK for browser automation.
Run demos with: python3 demos/<demo_name>.py
Or use the CLI:  mlx --help

Setup:
  1. Copy .env.example to .env and fill in your credentials.
  2. Run any demo: python3 demos/01_auth_check.py

Documentation: README.md
"""

import sys

from mlx import MultiloginX, __version__
from mlx.constants import PARTNER_NOTE


def main() -> None:
    print(f"Multilogin X Python SDK v{__version__}")
    print(PARTNER_NOTE)
    print()
    print("Usage:")
    print("  python3 demos/<demo_name>.py   — run a specific demo")
    print("  mlx --help                      — CLI interface")
    print()
    print("Setup:")
    print("  1. Copy .env.example to .env")
    print("  2. Fill in MLX_EMAIL and MLX_PASSWORD")
    print("  3. Run: python3 demos/01_auth_check.py")
    print()

    try:
        from mlx.env import get_env
        email = get_env("MLX_EMAIL", required=False)
        if email:
            print(f"Detected credentials for: {email}")
        else:
            print("No .env credentials found — copy .env.example to .env to get started.")
    except Exception:
        print("No .env credentials found — copy .env.example to .env to get started.")


if __name__ == "__main__":
    main()
    sys.exit(0)
