import contextlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))
HAS_FITZ = importlib.util.find_spec("fitz") is not None


@unittest.skipUnless(HAS_FITZ, "PyMuPDF not installed")
class PreviewPngTest(unittest.TestCase):
    def test_preview_goes_to_temp_dir_per_posting(self):
        import build_resume

        name = "Acme-test-preview-png"
        folder = Path(tempfile.gettempdir()) / "jobapps-preview" / name
        shutil.rmtree(folder, ignore_errors=True)
        self.addCleanup(shutil.rmtree, folder, True)

        pdf = Path("postings") / name / "Jordan_Lee_Resume_Acme.pdf"
        png = build_resume.preview_png(pdf)

        self.assertEqual(png, folder / "Jordan_Lee_Resume_Acme.png")
        self.assertTrue(folder.is_dir())


@unittest.skipUnless(HAS_FITZ, "PyMuPDF not installed")
class CompileFailureTest(unittest.TestCase):
    def setUp(self):
        import build_resume

        self.br = build_resume
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.tex = Path(self.tmp.name) / "r.tex"
        self.tex.write_text("\\documentclass{article}\\begin{document}x\\end{document}\n")

    def run_main(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = self.br.main(str(self.tex))
        return code, json.loads(out.getvalue())

    def test_pdflatex_missing_is_reported(self):
        with mock.patch.object(self.br, "find_pdflatex", return_value=None):
            code, report = self.run_main()
        self.assertEqual(code, 1)
        self.assertFalse(report["ok"])
        self.assertIn("pdflatex not found", report["errors"][0])

    def test_timeout_is_reported(self):
        timeout = subprocess.TimeoutExpired("pdflatex", self.br.COMPILE_TIMEOUT)
        with mock.patch.object(self.br, "find_pdflatex", return_value="pdflatex"), \
                mock.patch.object(self.br.subprocess, "run", side_effect=timeout):
            code, report = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("timed out", report["errors"][0])

    def test_no_log_is_reported(self):
        with mock.patch.object(self.br, "find_pdflatex", return_value="pdflatex"), \
                mock.patch.object(self.br.subprocess, "run"):
            code, report = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("no log", report["errors"][0])


if __name__ == "__main__":
    unittest.main()
