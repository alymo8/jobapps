import fnmatch
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent

# Generic patterns, always on (spec section 3).
GENERIC = [
    ("artifact_url", re.compile(r"claude\.ai/(code/)?artifact/[0-9A-Za-z-]{10,}")),
    ("routine_id", re.compile(r"trig_[0-9A-Za-z]{10,}")),
    ("windows_user_path", re.compile(r"[A-Za-z]:[\\/]Users[\\/][^<%\s]")),
    ("home_path", re.compile(r"/home/[a-z]")),
    ("mac_user_path", re.compile(r"/Users/[a-z]")),
    (
        "email",
        re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"),
    ),
    ("phone", re.compile(r"\(?\d{3}\)?[-. ]\d{3}[-. ]\d{4}")),
]

# (path glob, regex matched against the hit line, one-line reason)
ALLOWLIST = []


def _email_ok(line):
    """True when every email on the line is an allowed placeholder."""
    for m in GENERIC[5][1].finditer(line):
        local, _, domain = m.group(0).rpartition("@")
        if domain.lower() in ("example.com", "example.org") or local == "noreply":
            continue
        return False
    return True


def load_terms(path):
    terms = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        t = line.strip()
        if t and not t.startswith("#"):
            terms.append(t)
    return terms


def term_pattern(term):
    return re.compile(
        r"(?:(?<![A-Za-z0-9])|(?<=\\[ntr]))" + re.escape(term) + r"(?![A-Za-z0-9])",
        re.IGNORECASE,
    )


def _allowlisted(path, line):
    return any(
        fnmatch.fnmatch(path, glob) and re.search(rx, line)
        for glob, rx, _reason in ALLOWLIST
    )


def scan(path, text, patterns):
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        for name, pat in patterns:
            if not pat.search(line):
                continue
            if name == "email" and _email_ok(line):
                continue
            if _allowlisted(path, line):
                continue
            hits.append(f"{path}:{n}: {name}")
    return hits


def is_binary(data):
    return b"\0" in data[:8192]


def tracked_files():
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True
    ).stdout
    return [p for p in out.decode("utf-8").split("\0") if p]


def _scan_repo(patterns):
    hits = []
    for rel in tracked_files():
        p = ROOT / rel
        if not p.is_file():
            continue
        data = p.read_bytes()
        if is_binary(data):
            continue
        hits += scan(rel, data.decode("utf-8", errors="replace"), patterns)
    return hits


class ScannerTest(unittest.TestCase):
    def test_generic_patterns_hit(self):
        samples = {
            "artifact_url": "https://claude.ai/artifact/" + "A" * 12,
            "routine_id": "trig_" + "B" * 12,
            "windows_user_path": "C:" + "\\" + "Users" + "\\" + "bob",
            "home_path": "/" + "home" + "/bob",
            "mac_user_path": "/" + "Users" + "/bob",
            "email": "bob" + "@" + "corp.io",
            "phone": "514" + "-555-" + "0199",
        }
        for name, sample in samples.items():
            with self.subTest(name):
                hits = scan("f.md", sample, GENERIC)
                self.assertIn(f"f.md:1: {name}", hits)

    def test_generic_patterns_skip_placeholders(self):
        samples = [
            "<repo-root>",
            "%USERPROFILE%" + "\\" + "x",
            "C:" + "\\" + "Users" + "\\" + "<name>",
            "x" + "@" + "example.com",
            "noreply" + "@" + "anthropic.com",
            "a" + "@" + "b.c",
            "https://claude.ai/artifact/<artifact-id>",
        ]
        for s in samples:
            with self.subTest(s):
                self.assertEqual(scan("f.md", s, GENERIC), [])

    def test_term_matches_next_to_underscore(self):
        pat = term_pattern("Zed")
        for text in ["Zed_Resume_Acme.tex", "zed.md", "ZED's", "Best,\\nZed"]:
            with self.subTest(text):
                self.assertTrue(pat.search(text))

    def test_term_ignores_inside_word(self):
        pat = term_pattern("Zed")
        for text in ["Zedekiah", "aZed"]:
            with self.subTest(text):
                self.assertIsNone(pat.search(text))

    def test_load_terms_skips_blank_and_comments(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "terms"
            p.write_bytes(b"Zed\r\n\r\n# note\n  Qux  \n")
            self.assertEqual(load_terms(p), ["Zed", "Qux"])

    def test_binary_detection(self):
        self.assertTrue(is_binary(b"a\0b"))
        self.assertFalse(is_binary(b"abc"))

    def test_allowlist_suppresses_hit(self):
        sample = "ask " + "bob" + "@" + "corp.io"
        self.assertEqual(len(scan("docs/a.md", sample, GENERIC)), 1)
        entry = [("docs/*.md", r"corp\.io", "test")]
        with mock.patch.object(sys.modules[__name__], "ALLOWLIST", entry):
            self.assertEqual(scan("docs/a.md", sample, GENERIC), [])
            self.assertEqual(len(scan("other/a.md", sample, GENERIC)), 1)


class RepoScanTest(unittest.TestCase):
    def test_tracked_files_have_no_generic_hits(self):
        hits = _scan_repo(GENERIC)
        self.assertEqual(hits, [], "\n".join(hits))

    def test_tracked_files_have_no_personal_terms(self):
        terms_file = ROOT / ".personal-terms"
        if not terms_file.exists():
            self.skipTest(".personal-terms not present (CI view)")
        patterns = [
            (f"term {i}", term_pattern(t))
            for i, t in enumerate(load_terms(terms_file))
        ]
        hits = _scan_repo(patterns)
        self.assertEqual(hits, [], "\n".join(hits))


if __name__ == "__main__":
    unittest.main()
