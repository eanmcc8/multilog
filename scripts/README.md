# Windows utilities (user-facing helpers only)

## Setup & run demos

```powershell
.\AUTO-SETUP.bat       # pip + playwright + copy .env templates
.\AUTO-PIPELINE.bat    # API health check (no browser)
.\RUN-DEMOS.bat        # 120 tools menu

powershell -ExecutionPolicy Bypass -File scripts\run-demo.ps1 -Demo 39
```

## GitHub About box (manual, one-time)

Paste from repo admin settings:

| Field | File |
| :--- | :--- |
| Description | `.github/DESCRIPTION` |
| Website | `.github/WEBSITE` |
| Topics | `.github/TOPICS` |
