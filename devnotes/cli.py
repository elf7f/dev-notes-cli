from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from .config import init_config, load_config
from .doctor import run_doctor
from .generator import NoteOptions, write_note
from .templates import TEMPLATES, list_template_names
from .utils import parse_csv_items

app = typer.Typer(help="Generate markdown notes for tech blogs and study logs.")


@app.command()
def new(
    title: str = typer.Argument(..., help="Note title"),
    tags: str = typer.Option("", "--tags", help="Comma-separated tags, e.g. redis,java"),
    category: str = typer.Option("", "--category", help="Single category"),
    summary: str = typer.Option("", "--summary", help="Short summary"),
    output_dir: Optional[str] = typer.Option(None, "--dir", help="Output directory override"),
    template: Optional[str] = typer.Option(None, "--template", help="Template name"),
    overwrite: Optional[bool] = typer.Option(
        None,
        "--overwrite/--no-overwrite",
        help="Whether to overwrite if file exists",
    ),
) -> None:
    """Create a new markdown note file."""
    cwd = Path.cwd()

    try:
        cfg = load_config(cwd)
    except Exception as exc:
        typer.secho(f"Failed to load config: {exc}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    selected_template = template or str(cfg["default_template"])
    if selected_template not in TEMPLATES:
        typer.secho(
            f"Unknown template '{selected_template}'. Run 'devnotes list-templates'.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    categories = [category.strip()] if category.strip() else []
    final_overwrite = bool(cfg["overwrite"]) if overwrite is None else overwrite

    options = NoteOptions(
        title=title,
        template=selected_template,
        tags=parse_csv_items(tags),
        categories=categories,
        summary=summary.strip(),
        output_dir=output_dir or str(cfg["output_dir"]),
        timezone=str(cfg["timezone"]),
        slugify=bool(cfg["slugify"]),
        overwrite=final_overwrite,
    )

    try:
        created = write_note(cwd, options)
    except Exception as exc:
        typer.secho(f"Failed to create note: {exc}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho(f"Created: {created}", fg=typer.colors.GREEN)


@app.command()
def init(
    force: bool = typer.Option(False, "--force", help="Overwrite existing .devnotes.yaml"),
) -> None:
    """Initialize default config file."""
    cwd = Path.cwd()
    try:
        path = init_config(cwd, force=force)
    except FileExistsError as exc:
        typer.secho(str(exc), fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho(f"Initialized config: {path}", fg=typer.colors.GREEN)


@app.command("list-templates")
def list_templates() -> None:
    """List built-in templates."""
    for name in list_template_names():
        description = str(TEMPLATES[name]["description"])
        typer.echo(f"- {name}: {description}")


@app.command()
def doctor() -> None:
    """Check configuration and output directory health."""
    checks, healthy = run_doctor(Path.cwd())

    for label, ok, detail in checks:
        state = "[OK]" if ok else "[FAIL]"
        typer.echo(f"{state} {label}: {detail}")

    if healthy:
        typer.secho("Doctor check passed.", fg=typer.colors.GREEN)
        return

    typer.secho("Doctor check failed.", fg=typer.colors.RED)
    raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
