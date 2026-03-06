# dev-notes-cli

A lightweight CLI tool for generating structured Markdown notes for technical blogs and study logs.

中文说明见：[README.zh-CN.md](./README.zh-CN.md)

## Why

When writing technical notes for Hugo or other static blogs, creating front matter and article structure repeatedly is tedious and error-prone. `dev-notes-cli` generates a clean note file in one command and keeps your posts consistent.

## Features

- Create Markdown notes from the command line
- Generate YAML front matter automatically
- Support `tags`, `category`, and `summary`
- Support multiple templates: `note`, `project`, `interview`
- Configurable defaults via `.devnotes.yaml`
- Built-in `doctor` command for setup checks

## Tech Stack

- Python 3.11+
- Typer
- pathlib / datetime / re / unicodedata
- PyYAML

## Project Structure

```text
dev-notes-cli/
├── README.md
├── LICENSE
├── pyproject.toml
├── Makefile
├── docs/
│   └── plan.md
├── devnotes/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── generator.py
│   ├── templates.py
│   ├── utils.py
│   └── doctor.py
├── tests/
│   ├── test_slug.py
│   ├── test_generator.py
│   └── test_config.py
└── examples/
    ├── example-note.md
    ├── example-project.md
    └── example-interview.md
```

## Install

```bash
python3 -m venv .venv
.venv/bin/pip install ".[dev]"
```

Or use Makefile:

```bash
make venv
make install
```

## Quick Start

```bash
devnotes init
devnotes new "Redis缓存击穿总结" --tags redis,java --category 面试笔记 --template interview
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

Example output:

```text
- interview: Interview Q&A template.
- note: General technical note template.
- project: Project review template.
```

### `devnotes doctor`

```bash
devnotes doctor
```

Example output:

```text
[OK] Config file: /path/to/.devnotes.yaml
[OK] Config parse: Configuration is valid
[OK] Output dir exists: /path/to/content/posts
[OK] Output dir writable: /path/to/content/posts
Doctor check passed.
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

## Generated Markdown Example

```markdown
---
title: "Redis缓存击穿总结"
date: 2026-03-06T21:00:00+08:00
draft: false
tags: ["redis", "java"]
categories: ["面试笔记"]
summary: "缓存击穿场景分析与常见方案。"
---

## 问题

## 回答思路

## 延伸问题

## 总结
```

## Makefile Shortcuts

```bash
make test
make templates
make smoke
```

## Roadmap

- [x] Generate basic note templates
- [x] Support YAML front matter
- [ ] Custom template support
- [ ] Interactive mode
- [ ] Hugo-specific integrations
