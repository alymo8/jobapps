import contextlib
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))
HAS_FITZ = importlib.util.find_spec("fitz") is not None

FIXTURE = Path(__file__).parent / "fixtures" / "profile.md"
LETTER = "Dear hiring team,\n\n" + " ".join(["word"] * 316) + "\n\nBest,\nJordan\n"
FRENCH = ("Bonjour à l'équipe de recrutement,\n\n" + " ".join(["mot"] * 316)
          + "\n\nCordialement,\nJordan\n")


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

    def temp_profile(self, text):
        profile = self.dir / "profile.md"
        profile.write_text(text, encoding="utf-8")
        return profile

    def fixture_text(self):
        return FIXTURE.read_text(encoding="utf-8")

    def test_contact_reads_contact_section(self):
        self.assertEqual(self.bcl.contact(FIXTURE), {
            "name": "Jordan Avery Lee", "phone": "555-0100", "email": "jordan@example.com",
            "city": "Springfield", "linkedin": "https://www.linkedin.com/in/jordan-example",
            "github": "https://github.com/jordan-example",
            "linkedin_bare": "linkedin.com/in/jordan-example",
            "github_bare": "github.com/jordan-example"})

    def test_contact_drops_trailing_notes(self):
        profile = self.temp_profile(self.fixture_text().replace(
            "in/jordan-example", "in/jordan-example (www form; note, 2026-10-05)"))
        c = self.bcl.contact(profile)
        self.assertEqual(c["linkedin"], "https://www.linkedin.com/in/jordan-example")
        self.assertEqual(c["linkedin_bare"], "linkedin.com/in/jordan-example")

    def test_contact_keeps_inner_parentheses(self):
        profile = self.temp_profile(self.fixture_text().replace(
            "- Full name: Jordan Avery Lee", "- Full name: Jordan (Jo) Lee (note)"))
        self.assertEqual(self.bcl.contact(profile)["name"], "Jordan (Jo) Lee")

    def test_signoff_name_prefers_preferred_first_name(self):
        self.assertEqual(self.bcl.signoff_name(FIXTURE), "Jordan")

    def test_signoff_name_drops_trailing_note(self):
        profile = self.temp_profile(self.fixture_text().replace(
            "Preferred first name: Jordan", "Preferred first name: Jordan (on forms)"))
        self.assertEqual(self.bcl.signoff_name(profile), "Jordan")

    def test_signoff_name_falls_back_to_full_name(self):
        profile = self.temp_profile(self.fixture_text().replace(
            "- Preferred first name: Jordan\n", ""))
        self.assertEqual(self.bcl.signoff_name(profile), "Jordan")

    def test_check_signoff_uses_profile_name(self):
        code, report = self.run_main([str(self.letter), "--check", "--profile", str(FIXTURE)])
        self.assertEqual(code, 0)
        self.assertTrue(report["signoff_ok"])
        self.letter.write_text(LETTER.replace("Best,\nJordan", "Best,\nSam"), encoding="utf-8")
        code, report = self.run_main([str(self.letter), "--check", "--profile", str(FIXTURE)])
        self.assertEqual(code, 1)
        self.assertFalse(report["signoff_ok"])

    def test_check_french_form(self):
        self.letter.write_text(FRENCH, encoding="utf-8")
        code, report = self.run_main([str(self.letter), "--check", "--profile", str(FIXTURE)])
        self.assertEqual(code, 0)
        self.assertTrue(report["greeting_ok"])
        self.assertTrue(report["signoff_ok"])

    def test_profile_flag_before_md(self):
        code, report = self.run_main(["--profile", str(FIXTURE), str(self.letter), "--check"])
        self.assertEqual(code, 0)
        self.assertEqual(report["md"], str(self.letter.resolve()))

    def test_check_requires_profile(self):
        code, report = self.run_main(
            [str(self.letter), "--check", "--profile", str(self.dir / "missing.md")])
        self.assertEqual(code, 1)
        self.assertFalse(report["ok"])
        self.assertEqual(report["error"], self.bcl.MISSING_PROFILE)
        self.assertIn("words", report)

    def test_missing_profile_is_json_error(self):
        code, report = self.run_main([str(self.letter), "--profile", str(self.dir / "missing.md")])
        self.assertEqual(code, 1)
        self.assertFalse(report["ok"])
        self.assertEqual(report["error"], self.bcl.MISSING_PROFILE)
        self.assertIn("words", report)
        self.assertFalse(report["signoff_ok"])
        self.assertEqual(list(self.letter.parent.glob("*.tex")), [])

    def test_default_profile_used_without_flag(self):
        with mock.patch.object(self.bcl, "PROFILE", FIXTURE):
            code, report = self.run_main([str(self.letter), "--check"])
        self.assertEqual(code, 0)

    def test_preamble_escapes_contact_values(self):
        profile = self.temp_profile(self.fixture_text()
                                    .replace("Jordan Avery Lee", "Jordan & Lee_Co")
                                    .replace("github.com/jordan-example", "github.com/jo_dev#a%b"))
        tex = self.bcl.preamble(profile)
        self.assertIn(r"\scshape Jordan \& Lee\_Co}", tex)
        self.assertIn(r"\href{https://github.com/jo_dev\#a\%b}", tex)
        self.assertIn(r"\underline{github.com/jo\_dev\#a\%b}", tex)

    def test_github_and_linkedin_are_optional(self):
        profile = self.temp_profile(self.fixture_text()
                                    .replace("- GitHub: https://github.com/jordan-example\n", "")
                                    .replace("- LinkedIn: https://www.linkedin.com/in/jordan-example\n", ""))
        self.assertNotIn("github", self.bcl.contact(profile))
        tex = self.bcl.preamble(profile)
        self.assertNotIn(r"\faGithub", tex)
        self.assertNotIn(r"\faLinkedin", tex)
        self.assertIn(r"\faEnvelope", tex)

    def test_missing_required_contact_is_json_error(self):
        profile = self.temp_profile(self.fixture_text().replace("- Email: jordan@example.com\n", ""))
        code, report = self.run_main([str(self.letter), "--profile", str(profile)])
        self.assertEqual(code, 1)
        self.assertFalse(report["ok"])
        self.assertIn("Email", report["error"])
        self.assertEqual(list(self.letter.parent.glob("*.tex")), [])

    @unittest.skipUnless(shutil.which("pdflatex"), "pdflatex not on PATH")
    def test_underscore_handle_compiles(self):
        profile = self.temp_profile(self.fixture_text().replace(
            "github.com/jordan-example", "github.com/jo_dev"))
        code, report = self.run_main([str(self.letter), "--profile", str(profile)])
        self.assertEqual(report["errors"], [])
        self.assertEqual(code, 0)

    def test_letter_tex_path_from_full_name(self):
        md = self.dir / "Acme-1" / "cover_letter.md"
        self.assertEqual(self.bcl.letter_tex_path(md, FIXTURE).name,
                         "Jordan_Avery_Lee_Cover_Letter_Acme.tex")


if __name__ == "__main__":
    unittest.main()
