# dev-notes-cli

一个轻量的命令行工具，用于快速生成结构化技术博客/学习笔记 Markdown 模板。

English README: [README.md](./README.md)

## 项目背景

写 Hugo 或其他静态博客时，常常要重复手写 front matter 和文章骨架（标题、日期、tags、分类、摘要等），效率低且容易漏字段。`dev-notes-cli` 用一条命令生成规范化笔记文件。

## 功能特性

- 命令行创建 Markdown 技术笔记
- 自动生成 YAML front matter
- 支持 `tags`、`category`、`summary`
- 内置三种模板：`note`、`project`、`interview`
- 支持 `.devnotes.yaml` 默认配置
- 内置 `doctor` 健康检查命令

## 技术栈

- Python 3.11+
- Typer
- pathlib / datetime / re / unicodedata
- PyYAML

## 目录结构

```text
dev-notes-cli/
├── README.md
├── README.zh-CN.md
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

## 安装

```bash
python3 -m venv .venv
.venv/bin/pip install ".[dev]"
```

或者使用 Makefile：

```bash
make venv
make install
```

## 快速开始

```bash
devnotes init
devnotes new "Redis缓存击穿总结" --tags redis,java --category 面试笔记 --template interview
```

## 命令说明

### `devnotes new`

创建新文章：

```bash
devnotes new "JWT登录实现" \
  --tags java,spring,jwt \
  --category 面试笔记 \
  --summary "JWT 登录流程与踩坑总结" \
  --template interview
```

### `devnotes init`

初始化配置文件：

```bash
devnotes init
```

### `devnotes list-templates`

列出内置模板：

```bash
devnotes list-templates
```

示例输出：

```text
- interview: Interview Q&A template.
- note: General technical note template.
- project: Project review template.
```

### `devnotes doctor`

检查配置和输出目录：

```bash
devnotes doctor
```

示例输出：

```text
[OK] Config file: /path/to/.devnotes.yaml
[OK] Config parse: Configuration is valid
[OK] Output dir exists: /path/to/content/posts
[OK] Output dir writable: /path/to/content/posts
Doctor check passed.
```

## 配置文件

文件名：`.devnotes.yaml`

```yaml
output_dir: "content/posts"
default_template: "note"
default_author: ""
timezone: "+08:00"
slugify: true
overwrite: false
```

## 生成结果示例

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

## Makefile 快捷命令

```bash
make test
make templates
make smoke
```

## Roadmap

- [x] 基础模板生成
- [x] YAML front matter 支持
- [ ] 自定义模板支持
- [ ] 交互式模式
- [ ] Hugo 专项集成
