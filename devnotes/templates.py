from __future__ import annotations

TEMPLATES: dict[str, dict[str, object]] = {
    "note": {
        "description": "General technical note template.",
        "sections": [
            "背景",
            "核心概念",
            "实践或示例",
            "总结",
        ],
    },
    "project": {
        "description": "Project review template.",
        "sections": [
            "项目背景",
            "功能设计",
            "技术选型",
            "实现过程",
            "问题与优化",
            "总结",
        ],
    },
    "interview": {
        "description": "Interview Q&A template.",
        "sections": [
            "问题",
            "回答思路",
            "延伸问题",
            "总结",
        ],
    },
}


def list_template_names() -> list[str]:
    return sorted(TEMPLATES.keys())


def get_template(template_name: str) -> dict[str, object]:
    if template_name not in TEMPLATES:
        available = ", ".join(list_template_names())
        raise ValueError(f"Unknown template '{template_name}'. Available: {available}")
    return TEMPLATES[template_name]
