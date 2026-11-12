import contextlib
import datetime as dt
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import discover  # noqa: E402
import read_postings as rp  # noqa: E402

TODAY = dt.date(2026, 10, 10)


def p(url, title="AI Engineer", company="Acme", location="Montreal"):
    return {"company": company, "title": title, "location": location, "url": url}


class DiscoverTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.root = self.base / "jobapps"
        (self.root / "postings").mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def rows_json(self, *rows, bom=False):
        path = self.base / "rows.json"
        path.write_text(json.dumps(list(rows)), encoding="utf-8-sig" if bom else "utf-8")
        return path

    def run_main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = discover.main(["--root", str(self.root), *args], today=TODAY)
        return code, out.getvalue()

    def run_rows(self, *rows, extra=(), bom=False):
        return self.run_main("--input", str(self.rows_json(*rows, bom=bom)), *extra)

    def csvs(self):
        return sorted((self.root / "discovered").glob("*.csv"))

    def urls(self, path=None):
        return [x["url"] for x in rp.from_csv(path or self.csvs()[0])]

    def test_dedupe_sources(self):
        (self.root / "applications.md").write_text(
            "| x | https://d.example/1/?utm_source=li |\n", encoding="utf-8")
        (self.root / "dlq.md").write_text(
            "| 2026-10-10 | b | 1 | C | T | https://D.EXAMPLE/2/ | score | LOW-SCORE | d | n | open |\n",
            encoding="utf-8")
        d = self.root / "postings" / "Acme-3"
        d.mkdir()
        (d / "posting.md").write_text("# Acme: AI\n- URL: https://d.example/3\n", encoding="utf-8")
        (self.root / "discovered").mkdir()
        (self.root / "discovered" / "2026-10-01.csv").write_text(
            "Rank,Company,Title,Location,URL\n1,A,T,L,https://d.example/4\n", encoding="utf-8")
        ex = self.root / "list.txt"
        ex.write_text("https://d.example/5\n", encoding="utf-8")
        self.run_rows(*[p(f"https://d.example/{i}") for i in range(1, 7)], extra=("--exclude", str(ex)))
        new = [f for f in self.csvs() if f.name == "2026-10-10.csv"][0]
        self.assertEqual(self.urls(new), ["https://d.example/6"])

    def test_csv_round_trip_with_commas(self):
        self.run_rows(p("https://c.example/1", title="AI; ML Engineer", company="Acme, Inc"))
        got = rp.read_source(self.csvs()[0])[0]
        self.assertEqual((got["company"], got["title"]), ("Acme, Inc", "AI; ML Engineer"))

    def test_location_filter(self):
        self.run_rows(
            p("https://l.example/1", location="Montreal, QC"),
            p("https://l.example/2", location="San Francisco, CA"),
            p("https://l.example/3", location=""),
            p("https://l.example/4", location="Remote - Canada"),
            extra=("--location", "canada", "Montreal"),
        )
        self.assertEqual(self.urls(), ["https://l.example/1", "https://l.example/3", "https://l.example/4"])

    def test_missing_exclude_file(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_rows(p("https://a.example/1"), extra=("--exclude", str(self.root / "nope.csv")))
        self.assertIn("exclude", str(cm.exception.code))
        self.assertFalse((self.root / "discovered").exists())

    def test_applications_url_trailing_punctuation(self):
        (self.root / "applications.md").write_text(
            "| x | Applied via https://p.example/1. Thanks |\n", encoding="utf-8")
        self.run_rows(p("https://p.example/1"), p("https://p.example/2"))
        self.assertEqual(self.urls(), ["https://p.example/2"])

    def test_nothing_new_writes_nothing(self):
        code, out = self.run_rows()
        self.assertEqual(code, 0)
        self.assertIn("no new postings", out)
        self.assertFalse((self.root / "discovered").exists())

    def test_rank_is_input_order(self):
        self.run_rows(p("https://r.example/c"), p("https://r.example/a"), p("https://r.example/b"))
        got = rp.from_csv(self.csvs()[0])
        self.assertEqual([x["url"] for x in got],
                         ["https://r.example/c", "https://r.example/a", "https://r.example/b"])
        self.assertEqual([x["rank"] for x in got], [1, 2, 3])

    def test_duplicate_url_in_input_keeps_first(self):
        self.run_rows(p("https://www.x.example/1/?utm_source=li", title="First"),
                      p("https://x.example/1", title="Second"))
        got = rp.from_csv(self.csvs()[0])
        self.assertEqual(len(got), 1)
        self.assertEqual(got[0]["title"], "First")

    def test_second_run_dedupes_earlier_csv(self):
        self.run_rows(p("https://a.example/1"))
        _, out = self.run_rows(p("https://a.example/1"))
        self.assertIn("no new postings", out)
        self.run_rows(p("https://a.example/1"), p("https://a.example/9"))
        self.assertEqual([f.name for f in self.csvs()], ["2026-10-10-2.csv", "2026-10-10.csv"])

    def test_skipped_rows_counted(self):
        no_title = p("https://s.example/x")
        del no_title["title"]
        no_location = p("https://s.example/2")
        del no_location["location"]
        _, out = self.run_rows(
            p("https://s.example/1"),
            no_title,
            p(""),
            p("   "),
            p(None),
            "x",
            no_location,
        )
        got = rp.from_csv(self.csvs()[0])
        self.assertEqual([x["url"] for x in got], ["https://s.example/1", "https://s.example/2"])
        self.assertEqual(got[1]["location"], "")
        self.assertIn("skipped 5 rows", out)

    def test_malformed_json_exits_nonzero(self):
        bad = self.base / "rows.json"
        bad.write_text("[{", encoding="utf-8")
        with self.assertRaises(SystemExit) as cm:
            self.run_main("--input", str(bad))
        self.assertIsInstance(cm.exception.code, str)
        self.assertIn("not valid JSON", cm.exception.code)
        self.assertFalse((self.root / "discovered").exists())

    def test_top_level_object_exits_nonzero(self):
        bad = self.base / "rows.json"
        bad.write_text(json.dumps({"rows": []}), encoding="utf-8")
        with self.assertRaises(SystemExit) as cm:
            self.run_main("--input", str(bad))
        self.assertIsInstance(cm.exception.code, str)
        self.assertIn("JSON list", cm.exception.code)
        self.assertFalse((self.root / "discovered").exists())

    def test_missing_input_file(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_main("--input", str(self.base / "nope.json"))
        self.assertIsInstance(cm.exception.code, str)
        self.assertIn("not found", cm.exception.code)

    def test_input_required(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_main()
        self.assertEqual(cm.exception.code, 2)

    def test_input_utf8_bom_and_accents(self):
        self.run_rows(p("https://u.example/1", company="Société Générale", location="Montréal"), bom=True)
        got = rp.from_csv(self.csvs()[0])[0]
        self.assertEqual((got["company"], got["location"]), ("Société Générale", "Montréal"))

    def test_no_last_run_file(self):
        self.run_rows(p("https://a.example/1"))
        self.assertTrue(self.csvs())
        self.assertFalse((self.root / "discovered" / ".last-run").exists())

    def test_cli_round_trip_read_postings(self):
        (self.root / "applications.md").write_text("| x | https://r.example/2 |\n", encoding="utf-8")
        j = self.rows_json(p("https://r.example/1"), p("https://r.example/2"), p("https://r.example/3"))
        done = subprocess.run([sys.executable, str(REPO / "tools" / "discover.py"),
                               "--input", str(j), "--root", str(self.root)],
                              capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(done.returncode, 0, done.stderr)
        csv_path = self.csvs()[0]
        read = subprocess.run([sys.executable, str(REPO / "tools" / "read_postings.py"), str(csv_path), "--all"],
                              capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(read.returncode, 0, read.stderr)
        self.assertEqual([x["url"] for x in json.loads(read.stdout)],
                         ["https://r.example/1", "https://r.example/3"])


if __name__ == "__main__":
    unittest.main()
