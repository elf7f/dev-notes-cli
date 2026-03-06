from __future__ import annotations

from pathlib import Path
import yaml

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


def load_config(cwd: Path) -> dict[str, object]:
    path = config_path(cwd)
    data: dict[str, object] = {}

    if path.exists():
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        if raw is None:
            raw = {}
        if not isinstance(raw, dict):
            raise ValueError(f"Invalid config in {path}: expected a key-value mapping")
        data = raw

    merged = dict(DEFAULT_CONFIG)
    merged.update(data)
    return merged


def dump_default_config() -> str:
    return yaml.safe_dump(DEFAULT_CONFIG, sort_keys=False, allow_unicode=True)


def init_config(cwd: Path, force: bool = False) -> Path:
    path = config_path(cwd)
    if path.exists() and not force:
        raise FileExistsError(f"{CONFIG_FILENAME} already exists")

    path.write_text(dump_default_config(), encoding="utf-8")
    return path
