"""Structure of the tracked starting material in templates/ (used by /onboard)."""

import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests"))

import build_cover_letter  # noqa: E402
from test_shortlist import FIXTURE_SHA256  # noqa: E402

SOURCE_TEMPLATES = ("resume_prompt.md", "cover_letter_prompt.md", "mega-resume.tex",
                    "profile.md", "stories.md", "answers.md")  # fmt: skip
TEXT_SUFFIXES = {".md", ".tex", ".py", ".json", ".html", ".csv", ".txt", ".yml", ".yaml"}


def read(name: str) -> str:
    return (TEMPLATES / name).read_text(encoding="utf-8")


def section(text: str, heading: str) -> str:
    return text.split(heading + "\n", 1)[1].split("\n## ", 1)[0]


def bullets(text: str) -> dict[str, str]:
    return dict(re.findall(r"^- ([^:\n]+): *(.*?) *$", text, re.M))


class SourceTemplatesTest(unittest.TestCase):
    def test_source_templates_exist(self):
        for name in SOURCE_TEMPLATES:
            self.assertTrue((TEMPLATES / name).is_file(), name)

    def test_profile_contact_keys_are_ask(self):
        fields = build_cover_letter.contact_fields(TEMPLATES / "profile.md")
        for key in [*build_cover_letter.CONTACT_KEYS.values(), "Preferred first name"]:
            self.assertEqual(fields.get(key), "ASK", key)

    def test_profile_targeting_keys(self):
        targeting = bullets(section(read("profile.md"), "## Targeting"))
        self.assertEqual(
            list(targeting),
            ["Pay floor", "Score threshold", "Years of experience", "Target roles",
             "Locations", "Deal-breakers"],  # fmt: skip
        )
        self.assertEqual(set(targeting.values()), {"ASK"})

    def test_profile_job_search_keys(self):
        text = read("profile.md")
        self.assertEqual(
            bullets(section(text, "## Job search")),
            {"Target companies": "ASK", "Priority companies": "ASK"},
        )
        self.assertEqual(re.findall(r"^## .*$", text, re.M)[-1], "## Job search")

    def test_profile_has_sections(self):
        headings = re.findall(r"^## .*$", read("profile.md"), re.M)
        for h in ("## Contact", "## Eligibility", "## Compensation & availability",
                  "## Common questions", "## Voluntary self-identification (EEO / diversity)",
                  "## Free-text answers", "## Career goals and cover letters",
                  "## LinkedIn outreach", "## Targeting", "## Job search"):  # fmt: skip
            self.assertIn(h, headings)
        self.assertNotIn("## Workday work history", headings)

    def test_profile_has_no_placeholders(self):
        text = read("profile.md")
        self.assertIsNone(re.search(r"<[^>\n]+>", text))
        values = bullets(text)
        self.assertTrue(values)
        for key, value in values.items():
            self.assertEqual(value, "ASK", key)

    def test_mega_resume_sections(self):
        text = read("mega-resume.tex")
        self.assertIn(r"\section{Skills}", text)
        self.assertNotIn("Technical Skills", text)

    def test_mega_resume_examples_are_comments(self):
        call = re.compile(r"\\(resumeSubheading|resumeItem|resumeProjectHeading"
                          r"|resumeSubheadingDegree|resumeSubHeadingListStart"
                          r"|resumeSubHeadingListEnd|resumeItemListStart|resumeItemListEnd)\b")  # fmt: skip
        for n, line in enumerate(read("mega-resume.tex").splitlines(), 1):
            if "\\newcommand" in line or "\\renewcommand" in line:
                continue
            if "<" in line or call.search(line):
                self.assertTrue(line.lstrip().startswith("%"), f"line {n}: {line}")

    def test_prompt_templates_keep_sections(self):
        expected = {
            "resume_prompt.md": ["## Inputs", "## Task", "## Hard rules", "## Content selection",
                                 "## Skills section", "## Fitting the page",
                                 "## Compile and verify", "## What to report"],
            "cover_letter_prompt.md": ["## Inputs", "## Task", "## Hard rules", "## Structure",
                                       "## Voice", "## Verify before delivering",
                                       "## What to report"],
        }  # fmt: skip
        for name, headings in expected.items():
            found = re.findall(r"^## .*$", read(name), re.M)
            for h in headings:
                self.assertIn(h, found, f"{name}: {h}")

    def test_template_backtick_runs_are_short(self):
        files = [p for p in TEMPLATES.rglob("*") if p.is_file() and p.suffix in TEXT_SUFFIXES]
        self.assertTrue(files)
        for p in files:
            self.assertIsNone(re.search(r"`{4,}", p.read_text(encoding="utf-8")), str(p))

    def test_template_placeholders_are_single_line(self):
        # A "<word" with no ">" later on its line is a placeholder split by a line break, which
        # /onboard's re.findall(r"<[^>\n]+>") would miss. The page's HTML/JS is not a placeholder.
        files = [p for p in TEMPLATES.rglob("*") if p.is_file() and p.suffix in TEXT_SUFFIXES
                 and p != SHORTLIST / "index.html"]  # fmt: skip
        self.assertTrue(files)
        for p in files:
            for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                self.assertNotRegex(line, r"<[A-Za-z][^>]*$", f"{p.name} line {n}")

    def test_mega_resume_skill_lines_end_in_line_break(self):
        lines = re.findall(r"^%\s+\\textbf\{.*$", read("mega-resume.tex"), re.M)
        self.assertTrue(lines)
        for line in lines[:-1]:
            self.assertTrue(line.endswith(" \\\\"), line)


WEEKLY_PLACEHOLDERS = ("<target roles in priority order>", "<target companies>",
                       "<priority companies>", "<location scope>", "<shortlist artifact URL>",
                       "<sources list>")  # fmt: skip


class WeeklyPromptTemplateTest(unittest.TestCase):
    def test_weekly_prompt_placeholders(self):
        path = TEMPLATES / "weekly-search-prompt.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Weekly job search prompt"))
        for placeholder in WEEKLY_PLACEHOLDERS:
            self.assertIn(placeholder, text)
        self.assertRegex(text, r"(?m)^<sources list>$")
        self.assertNotIn("Claude Docs", text.split("## Target roles", 1)[0])
        self.assertRegex(text, r"(?m)^### Known board-access notes \(from past runs\)$")


SHORTLIST = TEMPLATES / "shortlist"
SHORTLIST_FILES = ("index.html", "capabilities.json", "data/CONTRACT.md", "data/decision_keys.py",
                   "data/index.json", "data/latest.json")  # fmt: skip
COUNT_KEYS = ("total", "ranked", "below_cut", "new", "new_in_ranked", "priority",
              "region_restricted", "unverified", "likely_live", "hidden_applied",
              "hidden_not_interested")  # fmt: skip


class ShortlistTemplateTest(unittest.TestCase):
    def load(self, name):
        return json.loads((SHORTLIST / name).read_text(encoding="utf-8"))

    def test_shortlist_files_exist(self):
        for name in SHORTLIST_FILES:
            self.assertTrue((SHORTLIST / name).is_file(), name)

    def test_shortlist_capabilities(self):
        self.assertEqual(self.load("capabilities.json"), {"db": {}, "user": {}})

    def test_shortlist_keys_match_fixture(self):
        data = (SHORTLIST / "data" / "decision_keys.py").read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), FIXTURE_SHA256)

    def test_shortlist_empty_data(self):
        latest = self.load("data/latest.json")
        self.assertEqual(latest["schema_version"], 1)
        self.assertIsNone(latest["week"])
        self.assertEqual(latest["rows"], [])
        self.assertEqual(latest["coverage"], [])
        self.assertEqual(latest["flags"], [])
        self.assertEqual(latest["counts"], dict.fromkeys(COUNT_KEYS, 0))
        index = self.load("data/index.json")
        self.assertEqual(index, {"schema_version": 1, "latest": None, "weeks": []})


SAMPLE_RESUME = ROOT / "tests" / "fixtures" / "sample-resume.md"


class SampleResumeFixtureTest(unittest.TestCase):
    def test_sample_resume_shape(self):
        self.assertTrue(SAMPLE_RESUME.is_file())
        text = SAMPLE_RESUME.read_text(encoding="utf-8")
        for h in ("## Experience", "## Education", "## Projects", "## Skills"):
            self.assertRegex(text, rf"(?m)^{re.escape(h)}$", h)
        jobs = re.split(r"(?m)^### ", section(text, "## Experience"))[1:]
        self.assertEqual(len(jobs), 2)
        for job in jobs:
            self.assertGreaterEqual(len(re.findall(r"(?m)^- ", job)), 7, job.splitlines()[0])
        emails = re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", text)
        self.assertTrue(emails)
        for email in emails:
            self.assertTrue(email.endswith("@example.com"), email)


SKILLS = ROOT / ".claude" / "skills"


class SkillsTest(unittest.TestCase):
    def test_skills_name_existing_templates(self):
        skill_files = sorted(SKILLS.glob("*/SKILL.md"))
        self.assertTrue(skill_files)
        for skill in skill_files:
            text = skill.read_text(encoding="utf-8")
            paths = {m.rstrip(".,;:)") for m in re.findall(r"(?<![\w/>.-])templates/[\w./-]+", text)}
            for rel in paths:
                self.assertTrue((ROOT / rel).exists(), f"{skill.parent.name}: {rel}")

    def test_discover_skill_removed(self):
        self.assertFalse((SKILLS / "discover").exists())
        self.assertTrue((SKILLS / "scan-jobs" / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
