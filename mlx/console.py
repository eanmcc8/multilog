"""Pretty terminal output for demos and CLI tools."""
from __future__ import annotations

import os
import shutil
import sys
from datetime import datetime


class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"


def _supports_color() -> bool:
    return sys.stdout.isatty() and (sys.platform != "win32" or "ANSICON" in os.environ)


USE_COLOR = _supports_color()


def _c(text: str, code: str) -> str:
    if not USE_COLOR:
        return text
    return f"{code}{text}{C.RESET}"


def banner(title: str, subtitle: str = "") -> None:
    width = min(shutil.get_terminal_size((80, 20)).columns, 72)
    line = "=" * width
    print(_c(line, C.CYAN))
    print(_c(f"  {title}", C.BOLD + C.CYAN))
    if subtitle:
        print(_c(f"  {subtitle}", C.DIM))
    print(_c(line, C.CYAN))
    print()


def section(title: str) -> None:
    print(_c(f"\n>> {title}", C.BOLD + C.BLUE))
    print(_c("-" * 40, C.DIM))


def ok(msg: str) -> None:
    print(_c("  [OK] ", C.GREEN) + msg)


def fail(msg: str) -> None:
    print(_c("  [FAIL] ", C.RED) + msg)


def warn(msg: str) -> None:
    print(_c("  [WARN] ", C.YELLOW) + msg)


def info(msg: str) -> None:
    print(_c("  [i] ", C.CYAN) + msg)


def table(headers: list[str], rows: list[list[str]], max_col: int = 28) -> None:
    if not rows:
        info("(empty)")
        return
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], min(len(str(cell)), max_col))
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    print(_c(fmt.format(*headers), C.BOLD))
    print(_c("  ".join("-" * w for w in widths), C.DIM))
    for row in rows:
        clipped = [str(c)[:max_col] for c in row]
        print(fmt.format(*clipped))


def progress(current: int, total: int, label: str = "") -> None:
    bar_len = 30
    filled = int(bar_len * current / total) if total else 0
    bar = "#" * filled + "-" * (bar_len - filled)
    pct = int(100 * current / total) if total else 0
    suffix = f" {label}" if label else ""
    print(f"\r  [{bar}] {pct:3d}% ({current}/{total}){suffix}", end="", flush=True)
    if current >= total:
        print()


def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
