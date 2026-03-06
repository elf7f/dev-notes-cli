from __future__ import annotations

import os
from pathlib import Path

from .config import CONFIG_FILENAME, load_config


def run_doctor(cwd: Path) -> tuple[list[tuple[str, bool, str]], bool]:
    checks: list[tuple[str, bool, str]] = []

    config_file = cwd / CONFIG_FILENAME
    checks.append((
        "Config file",
        config_file.exists(),
        str(config_file),
    ))

    try:
        cfg = load_config(cwd)
        checks.append(("Config parse", True, "Configuration is valid"))
    except Exception as exc:  # pragma: no cover
        checks.append(("Config parse", False, str(exc)))
        return checks, False

    out_dir = (cwd / str(cfg["output_dir"]))

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        checks.append(("Output dir exists", out_dir.exists(), str(out_dir)))
    except OSError as exc:
        checks.append(("Output dir exists", False, str(exc)))

    writable = os.access(out_dir, os.W_OK)
    checks.append(("Output dir writable", writable, str(out_dir)))

    healthy = all(ok for _, ok, _ in checks)
    return checks, healthy
