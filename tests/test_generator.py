from pathlib import Path

from devnotes.generator import NoteOptions, render_markdown, write_note


def make_options() -> NoteOptions:
    return NoteOptions(
        title="JWT登录实现",
        template="interview",
        tags=["java", "spring", "jwt"],
        categories=["面试笔记"],
        summary="JWT 登录实现与注意事项",
        output_dir="content/posts",
        timezone="+08:00",
        slugify=True,
        overwrite=False,
    )


def test_render_markdown_contains_sections() -> None:
    content = render_markdown(make_options())
    assert "title: \"JWT登录实现\"" in content
    assert "## 问题" in content
    assert "## 回答思路" in content


def test_write_note_creates_file(tmp_path: Path) -> None:
    out = write_note(tmp_path, make_options())
    assert out.exists()
    assert out.suffix == ".md"
