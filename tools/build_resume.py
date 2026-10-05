"""Compile a tailored resume .tex and report the checks sources/resume_prompt.md requires.

Usage: python tools/build_resume.py <path/to/resume.tex>

Writes <name>.pdf next to the .tex (only the .tex and .pdf are kept there), renders a
preview PNG into the temp dir, and prints a JSON report:
  errors          LaTeX errors (compile failed if non-empty)
  overfull        Overfull \\hbox warnings (fix any that push text into the margin)
  pages           page count (must be 1)
  fill            bottom of the last text line / page height (target 0.95-0.98)
  skills_lines    rendered lines in the Skills section (must be <= 5)
  png             rendered page (temp dir), to look at before delivering
  ok              all hard checks pass (the visual check is still on you)
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import fitz  # PyMuPDF

FILL_MIN, FILL_MAX = 0.95, 0.98
SKILLS_MAX_LINES = 5


def compile_tex(tex: Path) -> tuple[list[str], list[str]]:
    miktex = Path.home() / "scoop/apps/miktex/current/texmfs/install/miktex/bin/x64/pdflatex.exe"
    pdflatex = shutil.which("pdflatex") or str(miktex)
    cmd = [pdflatex, "-interaction=nonstopmode", "-halt-on-error", tex.name]
    subprocess.run(cmd, cwd=tex.parent, capture_output=True, text=True, errors="replace")
    log = tex.with_suffix(".log").read_text(errors="replace")
    errors = [m.group(0).strip() for m in re.finditer(r"^! .*$", log, re.M)]
    overfull = [m.group(0).strip() for m in re.finditer(r"^Overfull \\hbox.*$", log, re.M)]
    for ext in (".aux", ".out", ".log"):
        tex.with_suffix(ext).unlink(missing_ok=True)
    return errors, overfull


def preview_png(pdf: Path) -> Path:
    """Where to render the page-1 preview: the temp dir, so postings/ keeps only .tex and .pdf."""
    out = Path(tempfile.gettempdir()) / "jobapps-preview" / pdf.parent.name
    out.mkdir(parents=True, exist_ok=True)
    return out / pdf.with_suffix(".png").name


def text_lines(page) -> list[tuple[float, float, str]]:
    """(y0, y1, text) for each visual line, merging spans that share a baseline."""
    rows: dict[int, list] = {}
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            text = "".join(s["text"] for s in line["spans"]).strip()
            if not text:
                continue
            y0, y1 = line["bbox"][1], line["bbox"][3]
            key = round((y0 + y1) / 2 / 3)  # 3pt buckets
            row = rows.setdefault(key, [y0, y1, ""])
            row[0], row[1], row[2] = min(row[0], y0), max(row[1], y1), (row[2] + " " + text).strip()
    return sorted((r[0], r[1], r[2]) for r in rows.values())


def section_line_count(lines, start: str, ends: tuple[str, ...]) -> int:
    count, inside = 0, False
    for _, _, text in lines:
        upper = text.upper()
        if not inside and upper == start:
            inside = True
            continue
        if inside and upper in ends:
            break
        if inside:
            count += 1
    return count


def main(tex_path: str) -> int:
    tex = Path(tex_path).resolve()
    errors, overfull = compile_tex(tex)
    report = {"tex": str(tex), "errors": errors, "overfull": overfull}
    pdf = tex.with_suffix(".pdf")
    if errors or not pdf.exists():
        report["ok"] = False
        print(json.dumps(report, indent=2))
        return 1

    doc = fitz.open(pdf)
    page = doc[0]
    lines = text_lines(page)
    png = preview_png(pdf)
    page.get_pixmap(dpi=110).save(png)
    report.update(
        pages=doc.page_count,
        fill=round(max(y1 for _, y1, _ in lines) / page.rect.height, 3),
        skills_lines=section_line_count(
            lines, "SKILLS", ("EXPERIENCE", "EDUCATION", "RESEARCH", "PROJECTS")
        ),
        pdf=str(pdf),
        png=str(png),
    )
    doc.close()
    report["ok"] = (
        report["pages"] == 1
        and FILL_MIN <= report["fill"] <= FILL_MAX
        and report["skills_lines"] <= SKILLS_MAX_LINES
    )
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
