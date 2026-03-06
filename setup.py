from setuptools import setup

setup(
    name="dev-notes-cli",
    version="0.1.0",
    description="A lightweight CLI tool for generating structured Markdown notes for technical blogs and study logs.",
    author="wenzy",
    python_requires=">=3.9",
    packages=["devnotes"],
    entry_points={
        "console_scripts": [
            "devnotes=devnotes.cli:main",
        ]
    },
)
