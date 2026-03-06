# dev-notes-cli

A lightweight CLI tool for generating structured Markdown notes for technical blogs and study logs.

中文说明见：[README.zh-CN.md](./README.zh-CN.md)

## Why

When writing technical notes for Hugo or other static blogs, creating front matter and article structure repeatedly is tedious and error-prone. `dev-notes-cli` generates a clean note file in one command.

## Features

- Create Markdown notes from the command line
- Generate YAML front matter automatically
- Support `tags`, `category`, and `summary`
- Support templates: `note`, `project`, `interview`
- Configurable defaults via `.devnotes.yaml`
- Built-in `doctor` command for setup checks

## Minimal Dependencies

Runtime dependency downloads: **none** (standard library only).

## Project Structure

```text
dev-notes-cli/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── setup.py
├── Makefile
├── devnotes/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── generator.py
│   ├── templates.py
│   ├── utils.py
│   └── doctor.py
└── .gitignore
```

## Install (Minimal Download)

1. Check Python is available:

```bash
python3 --version
```

2. Create virtual environment:

```bash
python3 -m venv .venv
```

3. Activate environment:

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Windows CMD:

```bat
.\.venv\Scripts\activate.bat
```

4. Install project only:

```bash
pip install .
```

5. Verify:

```bash
devnotes --help
```

## Remove / Uninstall

If you installed with virtual environment:

1. Exit environment if active:

```bash
deactivate
```

2. Remove `.venv`:

macOS / Linux:

```bash
rm -rf .venv
```

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force .venv
```

If you installed globally, also uninstall package:

```bash
pip uninstall dev-notes-cli
```

## Quick Start

```bash
devnotes init
devnotes new "Redis缓存击穿总结" --tags redis,java --category 面试笔记 --template interview
devnotes doctor
```

## Commands

### `devnotes new`

```bash
devnotes new "JWT登录实现" \
  --tags java,spring,jwt \
  --category 面试笔记 \
  --summary "JWT 登录流程与踩坑总结" \
  --template interview
```

### `devnotes init`

```bash
devnotes init
```

### `devnotes list-templates`

```bash
devnotes list-templates
```

### `devnotes doctor`

```bash
devnotes doctor
```

## Config

File: `.devnotes.yaml`

```yaml
output_dir: "content/posts"
default_template: "note"
default_author: ""
timezone: "+08:00"
slugify: true
overwrite: false
```
