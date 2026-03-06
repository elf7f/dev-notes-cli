from pathlib import Path

from devnotes.config import CONFIG_FILENAME, init_config, load_config


def test_load_config_uses_defaults(tmp_path: Path) -> None:
    cfg = load_config(tmp_path)
    assert cfg["output_dir"] == "content/posts"
    assert cfg["default_template"] == "note"


def test_init_config_creates_file(tmp_path: Path) -> None:
    created = init_config(tmp_path)
    assert created.name == CONFIG_FILENAME
    assert created.exists()

    cfg = load_config(tmp_path)
    assert cfg["timezone"] == "+08:00"
