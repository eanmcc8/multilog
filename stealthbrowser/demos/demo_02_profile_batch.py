"""Demo 02 — Create a batch of randomized profiles and save them."""
from __future__ import annotations

import json
from pathlib import Path

from stealthbrowser.profile import BrowserProfile

profiles = BrowserProfile.batch(
    5,
    os="windows",
    driver="http",
    name_prefix="Demo",
)

output_dir = Path("output/profiles")
output_dir.mkdir(parents=True, exist_ok=True)

for p in profiles:
    path = p.save(output_dir / f"{p.name}.json")
    print(f"Saved  : {path}")
    print(f"  UA   : {p.fingerprint.user_agent[:55]}...")
    print(f"  Res  : {p.fingerprint.resolution_width}x{p.fingerprint.resolution_height}")
    print(f"  TZ   : {p.fingerprint.timezone}")
    print()

print(f"Total: {len(profiles)} profiles saved to {output_dir}/")
