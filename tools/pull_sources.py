"""Write the one code block of a downloaded Claude Doc to its local source file.

Usage: python tools/pull_sources.py <downloaded.md> <target path>

The doc (exported as Markdown, see .claude/skills/pull-sources.md) must hold exactly one
fenced code block: an unindented line of 3+ backticks plus an optional info string, closed by
a line of the same backticks (trailing spaces allowed). Its content is written to the target
as UTF-8 with LF line endings. Prints a JSON report and exits 0, or 1 on any error:
  path            the target argument as given
  status          created | changed | unchanged (unchanged: the file is not rewritten)
  sha256          hex digest of the target's bytes after the call
  lines           content lines written
  error           what went wrong (nothing is written); code_blocks when the count is off
"""

import hashlib
import json
import re
import sys
from pathlib import Path

FENCE = re.compile(r"^(`{3,})[^`]*$")


def extract_block(text: str) -> str:
    """The content of the single fenced code block in `text`, each line ending in a newline."""
    blocks: list[list[str]] = []
    fence, current = None, []
    for line in text.replace("\r\n", "\n").split("\n"):
        if fence is None:
            m = FENCE.match(line)
            if m:
                fence, current = m.group(1), []
        elif line.rstrip(" ") == fence:
            blocks.append(current)
            fence = None
        else:
            current.append(line)
    if fence is not None:
        raise ValueError("unclosed fence")
    if len(blocks) != 1:
        err = ValueError(f"expected exactly one code block, found {len(blocks)}")
        err.code_blocks = len(blocks)
        raise err
    return "".join(line + "\n" for line in blocks[0])


def pull(src: Path, target: Path) -> dict:
    report: dict = {"path": str(target)}
    try:
        content = extract_block(src.read_text(encoding="utf-8")).encode("utf-8")
        if target.exists() and target.read_bytes() == content:
            status = "unchanged"
        else:
            status = "changed" if target.exists() else "created"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    except ValueError as e:
        report["error"] = str(e)
        if hasattr(e, "code_blocks"):
            report["code_blocks"] = e.code_blocks
        return report
    except OSError as e:
        report["error"] = f"{type(e).__name__}: {e}"
        return report
    report.update(status=status, sha256=hashlib.sha256(content).hexdigest(),
                  lines=content.count(b"\n"))
    return report


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 1
    report = pull(Path(argv[0]), Path(argv[1]))
    report["path"] = argv[1]  # as given, not as Path renders it (backslashes on Windows)
    print(json.dumps(report))
    return 1 if "error" in report else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
