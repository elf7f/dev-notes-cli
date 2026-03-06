# dev-notes-cli

一个轻量的命令行工具，用于快速生成结构化技术博客/学习笔记 Markdown 模板。

English README: [README.md](./README.md)

## 项目背景

写 Hugo 或其他静态博客时，常常要重复手写 front matter 和文章骨架（标题、日期、tags、分类、摘要等），效率低且容易漏字段。`dev-notes-cli` 用一条命令生成规范化笔记文件。

## 功能特性

- 命令行创建 Markdown 技术笔记
- 自动生成 YAML front matter
- 支持 `tags`、`category`、`summary`
- 支持模板：`note`、`project`、`interview`
- 支持 `.devnotes.yaml` 默认配置
- 内置 `doctor` 健康检查命令

## 最小依赖

运行时依赖下载：**0 个第三方包**（只用 Python 标准库）。

## 项目结构

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

## 安装（最少下载）

1. 先确认 Python 可用：

```bash
python3 --version
```

2. 在项目目录创建虚拟环境：

```bash
python3 -m venv .venv
```

3. 激活虚拟环境：

macOS / Linux：

```bash
source .venv/bin/activate
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
```

Windows CMD：

```bat
.\.venv\Scripts\activate.bat
```

4. 仅安装项目本体：

```bash
pip install .
```

5. 验证是否安装成功：

```bash
devnotes --help
```

## 移除/卸载

如果是虚拟环境安装：

1. 先退出虚拟环境（如果已激活）：

```bash
deactivate
```

2. 删除 `.venv` 目录：

macOS / Linux：

```bash
rm -rf .venv
```

Windows PowerShell：

```powershell
Remove-Item -Recurse -Force .venv
```

如果你做过全局安装，再执行：

```bash
pip uninstall dev-notes-cli
```

## 快速开始

```bash
devnotes init
devnotes new "Redis缓存击穿总结" --tags redis,java --category 面试笔记 --template interview
devnotes doctor
```

## 命令说明

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
