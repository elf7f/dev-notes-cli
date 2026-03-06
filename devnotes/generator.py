from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .templates import get_template
from .utils import format_yaml_list, iso_now, quote_yaml_str, slugify_title


@dataclass
class NoteOptions:
    title: str
    template: str
    tags: list[str]
    categories: list[str]
    summary: str
    output_dir: str
    timezone: str
    slugify: bool
    overwrite: bool


def render_markdown(options: NoteOptions) -> str:
    template_data = get_template(options.template)
    sections = template_data["sections"]

    front_matter = "\n".join(
        [
            "---",
            f"title: {quote_yaml_str(options.title)}",
            f"date: {iso_now(options.timezone)}",
            "draft: false",
            f"tags: {format_yaml_list(options.tags)}",
            f"categories: {format_yaml_list(options.categories)}",
            f"summary: {quote_yaml_str(options.summary)}",
            "---",
            "",
        ]
    )

    body = "\n\n".join(f"## {section}" for section in sections)
    return f"{front_matter}{body}\n"


def write_note(cwd: Path, options: NoteOptions) -> Path:
    filename = f"{slugify_title(options.title, options.slugify)}.md"
    output_path = (cwd / options.output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    note_path = output_path / filename
    if note_path.exists() and not options.overwrite:
        raise FileExistsError(f"File already exists: {note_path}")

    content = render_markdown(options)
    note_path.write_text(content, encoding="utf-8")
    return note_path
