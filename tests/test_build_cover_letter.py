import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))
HAS_FITZ = importlib.util.find_spec("fitz") is not None

LETTER = "Dear hiring team,\n\n" + " ".join(["word"] * 316) + "\n\nBest,\nAly\n"
CONTACT = """# Application profile

## Contact

- Full name: A B
- Phone: 1
- Email: a@b.c
- Location: Montreal, QC, Canada
- LinkedIn: https://www.linkedin.com/in/x
- GitHub: https://github.com/y

## Eligibility

- Legally authorized to work in Canada: Yes
"""


@unittest.skipUnless(HAS_FITZ, "PyMuPDF not installed")
class BuildCoverLetterTest(unittest.TestCase):
    def setUp(self):
        import build_cover_letter

        self.bcl = build_cover_letter
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        self.letter = self.dir / "Acme-1" / "cover_letter.md"
        self.letter.parent.mkdir()
        self.letter.write_text(LETTER, encoding="utf-8")

    def run_main(self, argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = self.bcl.main(argv)
        return code, json.loads(out.getvalue())

    def test_profile_path(self):
        self.assertTrue(self.bcl.PROFILE.as_posix().endswith("sources/profile.md"))

    def test_contact_reads_contact_section(self):
        profile = self.dir / "profile.md"
        profile.write_text(CONTACT, encoding="utf-8")
        with mock.patch.object(self.bcl, "PROFILE", profile):
            self.assertEqual(self.bcl.contact(), {
                "name": "A B", "phone": "1", "email": "a@b.c", "city": "Montreal",
                "linkedin": "https://www.linkedin.com/in/x", "github": "https://github.com/y",
                "linkedin_bare": "linkedin.com/in/x", "github_bare": "github.com/y"})

    def test_contact_drops_trailing_notes(self):
        profile = self.dir / "profile.md"
        profile.write_text(CONTACT.replace(
            "https://www.linkedin.com/in/x", "https://www.linkedin.com/in/x (www form; note, 2026-10-05)"),
            encoding="utf-8")
        with mock.patch.object(self.bcl, "PROFILE", profile):
            c = self.bcl.contact()
        self.assertEqual(c["linkedin"], "https://www.linkedin.com/in/x")
        self.assertEqual(c["linkedin_bare"], "linkedin.com/in/x")

    def test_missing_profile_is_json_error(self):
        with mock.patch.object(self.bcl, "PROFILE", self.dir / "missing.md"):
            code, report = self.run_main([str(self.letter)])
        self.assertEqual(code, 1)
        self.assertFalse(report["ok"])
        self.assertEqual(report["error"], self.bcl.MISSING_PROFILE)
        self.assertIn("words", report)
        self.assertEqual(list(self.letter.parent.glob("*.tex")), [])

    def test_check_needs_no_profile(self):
        with mock.patch.object(self.bcl, "PROFILE", self.dir / "missing.md"):
            code, report = self.run_main([str(self.letter), "--check"])
        self.assertEqual(code, 0)
        self.assertNotIn("error", report)


if __name__ == "__main__":
    unittest.main()
