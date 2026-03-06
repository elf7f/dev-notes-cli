from __future__ import annotations

import argparse
from pathlib import Path

from .config import init_config, load_config
from .doctor import run_doctor
from .generator import NoteOptions, write_note
from .templates import TEMPLATES, list_template_names
from .utils import parse_csv_items


def cmd_new(args: argparse.Namespace) -> int:
    cwd = Path.cwd()
    try:
        cfg = load_config(cwd)
    except Exception as exc:
        print(f"Failed to load config: {exc}")
        return 1

    selected_template = args.template or str(cfg["default_template"])
    if selected_template not in TEMPLATES:
        print(f"Unknown template '{selected_template}'. Run 'devnotes list-templates'.")
        return 1

    categories = [args.category.strip()] if args.category and args.category.strip() else []
    final_overwrite = bool(cfg["overwrite"]) if args.overwrite is None else args.overwrite

    options = NoteOptions(
        title=args.title,
        template=selected_template,
        tags=parse_csv_items(args.tags),
        categories=categories,
        summary=(args.summary or "").strip(),
        output_dir=args.dir or str(cfg["output_dir"]),
        timezone=str(cfg["timezone"]),
        slugify=bool(cfg["slugify"]),
        overwrite=final_overwrite,
    )

    try:
        created = write_note(cwd, options)
    except Exception as exc:
        print(f"Failed to create note: {exc}")
        return 1

    print(f"Created: {created}")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    cwd = Path.cwd()
    try:
        path = init_config(cwd, force=args.force)
    except FileExistsError as exc:
        print(str(exc))
        return 1

    print(f"Initialized config: {path}")
    return 0


def cmd_list_templates(_: argparse.Namespace) -> int:
    for name in list_template_names():
        description = str(TEMPLATES[name]["description"])
        print(f"- {name}: {description}")
    return 0


def cmd_doctor(_: argparse.Namespace) -> int:
    checks, healthy = run_doctor(Path.cwd())
    for label, ok, detail in checks:
        state = "[OK]" if ok else "[FAIL]"
        print(f"{state} {label}: {detail}")

    if healthy:
        print("Doctor check passed.")
        return 0

    print("Doctor check failed.")
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="devnotes",
        description="Generate markdown notes for tech blogs and study logs.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_new = subparsers.add_parser("new", help="Create a new markdown note file")
    p_new.add_argument("title", help="Note title")
    p_new.add_argument("--tags", default="", help="Comma-separated tags, e.g. redis,java")
    p_new.add_argument("--category", default="", help="Single category")
    p_new.add_argument("--summary", default="", help="Short summary")
    p_new.add_argument("--dir", default=None, help="Output directory override")
    p_new.add_argument("--template", default=None, help="Template name")
    group = p_new.add_mutually_exclusive_group()
    group.add_argument("--overwrite", dest="overwrite", action="store_true", help="Overwrite file")
    group.add_argument("--no-overwrite", dest="overwrite", action="store_false", help="Do not overwrite file")
    p_new.set_defaults(overwrite=None, func=cmd_new)

    p_init = subparsers.add_parser("init", help="Initialize default config file")
    p_init.add_argument("--force", action="store_true", help="Overwrite existing .devnotes.yaml")
    p_init.set_defaults(func=cmd_init)

    p_list = subparsers.add_parser("list-templates", help="List built-in templates")
    p_list.set_defaults(func=cmd_list_templates)

    p_doctor = subparsers.add_parser("doctor", help="Check configuration and output directory health")
    p_doctor.set_defaults(func=cmd_doctor)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
