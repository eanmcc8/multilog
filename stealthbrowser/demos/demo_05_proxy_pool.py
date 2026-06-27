"""Demo 05 — ProxyPool: parse, rotate, and assign proxies to profiles."""
from __future__ import annotations

from stealthbrowser.proxy import ProxyPool
from stealthbrowser.profile import BrowserProfile

# Example proxies (replace with real ones)
sample_proxies = [
    "http://proxy1.example.com:8080",
    "socks5://proxy2.example.com:1080:user:pass",
    "http://10.0.0.1:3128",
]

pool = ProxyPool(sample_proxies)
print(f"Pool size: {len(pool)}")

# Assign proxies to profiles round-robin
profiles = BrowserProfile.batch(6, driver="http", name_prefix="ProxyTest")
for p in profiles:
    proxy = pool.next()
    p.proxy = proxy
    print(f"  {p.name} -> {proxy.host}:{proxy.port} ({proxy.type})")

print()
print("Random pick:", pool.random().url)
print()

# Show what a ProxyConfig looks like
from stealthbrowser.profile import ProxyConfig
pc = ProxyConfig.from_string("socks5://myuser:mypass@proxy.example.com:1080")
print("Parsed proxy URL:", pc.url)
print("Playwright dict :", pc.as_playwright_dict())
