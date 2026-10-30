import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))
import pull_sources  # noqa: E402

LATEX_DOC = "# Mega resume\n\nnote\n\n```latex\n\\a{1}\n```\n"


class PullSourcesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def doc(self, text: str, name: str = "doc.md", newline: str = "\n") -> Path:
        p = self.dir / name
        p.write_bytes(text.replace("\n", newline).encode("utf-8"))
        return p

    def test_latex_block_extracted(self):
        target = self.dir / "out.tex"
        report = pull_sources.pull(self.doc(LATEX_DOC), target)
        self.assertEqual(target.read_bytes(), b"\\a{1}\n")
        self.assertEqual(report["status"], "created")
        self.assertEqual(report["lines"], 1)

    def test_longer_fence_keeps_inner_fences(self):
        inner = "```\nBest,\nJordan\n```"
        target = self.dir / "out.md"
        pull_sources.pull(self.doc(f"# T\n\n````markdown\n{inner}\n````\n"), target)
        self.assertEqual(target.read_text(encoding="utf-8"), inner + "\n")

    def test_whitespace_and_escapes_kept(self):
        body = " \n      \n\\% \\_ \\& \\# $|$ ·\n"
        target = self.dir / "out.tex"
        pull_sources.pull(self.doc(f"```latex\n{body}```\n"), target)
        self.assertEqual(target.read_bytes(), body.encode("utf-8"))

    def test_crlf_input_written_as_lf(self):
        target = self.dir / "out.tex"
        pull_sources.pull(self.doc(LATEX_DOC, newline="\r\n"), target)
        self.assertNotIn(b"\r", target.read_bytes())
        self.assertEqual(target.read_bytes(), b"\\a{1}\n")

    def test_zero_blocks_is_error(self):
        target = self.dir / "out.tex"
        report = pull_sources.pull(self.doc("# T\n\nno code here\n"), target)
        self.assertIn("error", report)
        self.assertEqual(report["code_blocks"], 0)
        self.assertFalse(target.exists())

    def test_two_blocks_is_error(self):
        target = self.dir / "out.tex"
        report = pull_sources.pull(self.doc("```\na\n```\n\n```\nb\n```\n"), target)
        self.assertIn("error", report)
        self.assertEqual(report["code_blocks"], 2)
        self.assertFalse(target.exists())

    def test_empty_block_is_error(self):
        target = self.dir / "out.tex"
        report = pull_sources.pull(self.doc("```latex\n \n```\n"), target)
        self.assertIn("error", report)
        self.assertFalse(target.exists())

    def test_write_failure_is_error(self):
        target = self.dir / "isdir"
        target.mkdir()
        report = pull_sources.pull(self.doc(LATEX_DOC), target)
        self.assertIn("error", report)

    def test_unclosed_fence_is_error(self):
        target = self.dir / "out.tex"
        report = pull_sources.pull(self.doc("```latex\n\\a{1}\n"), target)
        self.assertIn("error", report)
        self.assertFalse(target.exists())

    def test_second_run_unchanged(self):
        src, target = self.doc(LATEX_DOC), self.dir / "out.tex"
        pull_sources.pull(src, target)
        before = target.stat().st_mtime_ns
        report = pull_sources.pull(src, target)
        self.assertEqual(report["status"], "unchanged")
        self.assertEqual(target.stat().st_mtime_ns, before)

    def test_changed_when_content_differs(self):
        target = self.dir / "out.tex"
        target.write_bytes(b"old\n")
        report = pull_sources.pull(self.doc(LATEX_DOC), target)
        self.assertEqual(report["status"], "changed")
        self.assertEqual(target.read_bytes(), b"\\a{1}\n")

    def test_creates_parent_folder(self):
        target = self.dir / "sources" / "x.tex"
        report = pull_sources.pull(self.doc(LATEX_DOC), target)
        self.assertEqual(report["status"], "created")
        self.assertTrue(target.exists())

    def test_missing_input_is_error(self):
        report = pull_sources.pull(self.dir / "nope.md", self.dir / "out.tex")
        self.assertIn("error", report)

    def test_cli_exit_codes(self):
        script = str(TOOLS / "pull_sources.py")
        good = subprocess.run(
            [sys.executable, script, str(self.doc(LATEX_DOC)), str(self.dir / "a.tex")],
            capture_output=True, text=True)
        self.assertEqual(good.returncode, 0)
        self.assertEqual(json.loads(good.stdout)["status"], "created")
        target = self.dir.as_posix() + "/sub/c.tex"
        named = subprocess.run(
            [sys.executable, script, str(self.doc(LATEX_DOC)), target], capture_output=True, text=True)
        self.assertEqual(json.loads(named.stdout)["path"], target)
        bad = subprocess.run(
            [sys.executable, script, str(self.doc("no code\n", "bad.md")), str(self.dir / "b.tex")],
            capture_output=True, text=True)
        self.assertEqual(bad.returncode, 1)
        self.assertIn("error", json.loads(bad.stdout))


class LocalPullTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def raw(self, data: bytes, name: str = "src.md") -> Path:
        p = self.dir / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        return p

    def pulled(self, data: bytes) -> tuple[dict, bytes]:
        target = self.dir / "out.md"
        report = pull_sources.pull(self.raw(data), target, local=True)
        return report, target.read_bytes()

    def assert_error(self, src: Path):
        target = self.dir / "out.md"
        report = pull_sources.pull(src, target, local=True)
        self.assertIn("error", report)
        self.assertFalse(target.exists())

    def test_local_copied_verbatim(self):
        data = "\\a{1}\n```\nx\n```\n".encode("utf-8")
        report, out = self.pulled(data)
        self.assertEqual(out, data)
        self.assertEqual(report["status"], "created")
        self.assertEqual(report["lines"], 4)

    def test_local_crlf_written_as_lf(self):
        self.assertEqual(self.pulled(b"a\r\nb\r\n")[1], b"a\nb\n")

    def test_local_lone_cr_written_as_lf(self):
        self.assertEqual(self.pulled(b"a\rb\n")[1], b"a\nb\n")

    def test_local_bom_stripped(self):
        self.assertEqual(self.pulled(b"\xef\xbb\xbf# P\n")[1], b"# P\n")

    def test_local_final_newline_added(self):
        report, out = self.pulled(b"a\nb")
        self.assertEqual(out, b"a\nb\n")
        self.assertEqual(report["lines"], 2)

    def test_local_missing_file_is_error(self):
        self.assert_error(self.dir / "nope.md")

    def test_local_empty_file_is_error(self):
        self.assert_error(self.raw(b""))

    def test_local_whitespace_only_is_error(self):
        self.assert_error(self.raw(b" \n\t\r\n"))

    def test_local_invalid_utf8_is_error(self):
        self.assert_error(self.raw(b"a\xff\n"))

    def test_local_second_run_unchanged(self):
        src, target = self.raw(b"a\n"), self.dir / "out.md"
        pull_sources.pull(src, target, local=True)
        before = target.stat().st_mtime_ns
        report = pull_sources.pull(src, target, local=True)
        self.assertEqual(report["status"], "unchanged")
        self.assertEqual(target.stat().st_mtime_ns, before)

    def test_local_changed_overwrites(self):
        src, target = self.raw(b"a\n"), self.dir / "out.md"
        pull_sources.pull(src, target, local=True)
        src.write_bytes(b"b\n")
        report = pull_sources.pull(src, target, local=True)
        self.assertEqual(report["status"], "changed")
        self.assertEqual(target.read_bytes(), b"b\n")

    def test_local_error_keeps_existing_target(self):
        src, target = self.raw(b"a\n"), self.dir / "out.md"
        pull_sources.pull(src, target, local=True)
        src.write_bytes(b"")
        report = pull_sources.pull(src, target, local=True)
        self.assertIn("error", report)
        self.assertEqual(target.read_bytes(), b"a\n")

    def test_local_cli(self):
        script = str(TOOLS / "pull_sources.py")
        src = self.raw(b"# P\n", "my sources/profile.md")
        target = self.dir.as_posix() + "/jobapps sources/p.md"
        good = subprocess.run(
            [sys.executable, script, "--local", str(src), target], capture_output=True, text=True)
        self.assertEqual(good.returncode, 0)
        report = json.loads(good.stdout)
        self.assertEqual(report["status"], "created")
        self.assertEqual(report["path"], target)
        missing = subprocess.run(
            [sys.executable, script, "--local", str(self.dir / "nope.md"), target],
            capture_output=True, text=True)
        self.assertEqual(missing.returncode, 1)
        self.assertIn("error", json.loads(missing.stdout))
        one = subprocess.run(
            [sys.executable, script, "--local", str(src)], capture_output=True, text=True)
        self.assertEqual(one.returncode, 1)


if __name__ == "__main__":
    unittest.main()
