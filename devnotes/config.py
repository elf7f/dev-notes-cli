from __future__ import annotations

from pathlib import Path

CONFIG_FILENAME = ".devnotes.yaml"

DEFAULT_CONFIG: dict[str, object] = {
    "output_dir": "content/posts",
    "default_template": "note",
    "default_author": "",
    "timezone": "+08:00",
    "slugify": True,
    "overwrite": False,
}


def config_path(cwd: Path) -> Path:
    return cwd / CONFIG_FILENAME


def _parse_scalar(raw: str) -> object:
    text = raw.strip()
    if text in {"true", "True"}:
        return True
    if text in {"false", "False"}:
        return False
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        return text[1:-1]
    return text


def _parse_simple_yaml(text: str) -> dict[str, object]:
    result: dict[str, object] = {}
    for idx, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"Invalid config line {idx}: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"Invalid empty key at line {idx}")
        result[key] = _parse_scalar(value)
    return result


def load_config(cwd: Path) -> dict[str, object]:
    path = config_path(cwd)
    data: dict[str, object] = {}

    if path.exists():
        data = _parse_simple_yaml(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"Invalid config in {path}: expected a key-value mapping")

    merged = dict(DEFAULT_CONFIG)
    merged.update(data)
    return merged


def _dump_scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value)
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def dump_default_config() -> str:
    lines = [f"{key}: {_dump_scalar(value)}" for key, value in DEFAULT_CONFIG.items()]
    return "\n".join(lines) + "\n"


def init_config(cwd: Path, force: bool = False) -> Path:
    path = config_path(cwd)
    if path.exists() and not force:
        raise FileExistsError(f"{CONFIG_FILENAME} already exists")

    path.write_text(dump_default_config(), encoding="utf-8")
    return path
