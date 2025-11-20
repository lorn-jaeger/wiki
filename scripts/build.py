#!/usr/bin/env python3
"""Build the GitHub Pages site using Pandoc.

This script converts every Markdown file in the repository into a standalone
HTML file in the `_site` directory. It also generates the home page table of
contents based on the Markdown files discovered across the tree.
"""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "_site"
INDEX_PATH = REPO_ROOT / "index.md"


def load_markdown_files() -> list[Path]:
    """Return sorted Markdown files excluding the build output and index file."""
    md_files: list[Path] = []
    for path in REPO_ROOT.rglob("*.md"):
        if OUTPUT_DIR in path.parents:
            continue
        if any(part.startswith(".") for part in path.parts):
            continue
        if path == INDEX_PATH:
            continue
        md_files.append(path)
    return sorted(md_files)


def extract_title(markdown_text: str, fallback: str) -> str:
    """Extract a title from YAML front matter or the first H1/H2 heading."""
    if markdown_text.startswith("---\n"):
        # Naive YAML front matter scan to find a title line before the closing ---.
        for line in markdown_text.splitlines()[1:]:
            if line.strip() == "---":
                break
            match = re.match(r"title:\s*(.+)", line, re.IGNORECASE)
            if match:
                return match.group(1).strip()
    # Look for the first markdown heading.
    heading_match = re.search(r"^#\s+(.+)$", markdown_text, flags=re.MULTILINE)
    if heading_match:
        return heading_match.group(1).strip()
    heading_match = re.search(r"^##\s+(.+)$", markdown_text, flags=re.MULTILINE)
    if heading_match:
        return heading_match.group(1).strip()
    return fallback


def render_markdown(content: str, output_html: Path, title: str) -> None:
    output_html.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "pandoc",
            "-f",
            "markdown",
            "-t",
            "html",
            "--standalone",
            "--metadata",
            f"title={title}",
        ],
        input=content.encode(),
        check=True,
        stdout=output_html.open("wb"),
    )


def build_index(titles_by_path: dict[Path, str]) -> None:
    index_template = INDEX_PATH.read_text(encoding="utf-8")
    toc_lines: list[str] = []
    for md_path in sorted(titles_by_path):
        relative_md = md_path.relative_to(REPO_ROOT)
        depth = len(relative_md.parts) - 1
        indent = "  " * depth
        link = relative_md.with_suffix(".html").as_posix()
        toc_lines.append(f"{indent}- [{titles_by_path[md_path]}]({link})")
    toc_markdown = "\n".join(toc_lines) if toc_lines else "_No pages yet._"
    index_markdown = index_template.replace("<!-- TABLE_OF_CONTENTS -->", toc_markdown)
    render_markdown(index_markdown, OUTPUT_DIR / "index.html", "Home")


def build_site() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    titles_by_path: dict[Path, str] = {}
    for md_file in load_markdown_files():
        markdown_text = md_file.read_text(encoding="utf-8")
        title = extract_title(markdown_text, md_file.stem.replace("-", " ").title())
        titles_by_path[md_file] = title
        output_html = OUTPUT_DIR / md_file.relative_to(REPO_ROOT).with_suffix(".html")
        render_markdown(markdown_text, output_html, title)

    build_index(titles_by_path)


if __name__ == "__main__":
    build_site()
