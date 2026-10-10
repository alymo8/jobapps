import contextlib
import datetime as dt
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import discover  # noqa: E402
import read_postings as rp  # noqa: E402

TODAY = dt.date(2026, 10, 10)
HEADER = "url\tfirst_seen\tportal\ttitle\tcompany\tstatus\tlocation\n"


def row(url, day, title="AI Engineer", company="Acme", status="added", location="Montreal", extra=0):
    cells = [url, day, "greenhouse-api", title, company, status, location] + ["x"] * extra
    return "\t".join(cells) + "\n"


class DiscoverTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.root = base / "jobapps"
        self.co = base / "career-ops"
        (self.root / "postings").mkdir(parents=True)
        (self.co / "data").mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def history(self, *rows):
        (self.co / "data" / "scan-history.tsv").write_text(HEADER + "".join(rows), encoding="utf-8")

    def run_main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        argv = ["--root", str(self.root), "--career-ops", str(self.co), "--no-scan", *args]
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = discover.main(argv, today=TODAY)
        return code, out.getvalue()

    def csvs(self):
        return sorted((self.root / "discovered").glob("*.csv"))

    def test_filters_status_cutoff_and_collapses(self):
        self.history(
            row("https://a.example/1", "2026-10-09"),
            row("https://a.example/1/", "2026-10-10"),
            row("https://a.example/2", "2026-09-01"),
            row("https://a.example/3", "2026-10-09", status="skipped_title"),
            row("https://a.example/7", "2026-10-09", status=""),
            row("https://a.example/8", "2026-06-14"),
            row("https://a.example/8", "2026-10-09"),
            row("https://a.example/4", "2026-10-08", extra=7),
            "https://a.example/short\t2026-10-09\n",
        )
        code, _ = self.run_main("--since", "7")
        self.assertEqual(code, 0)
        got = rp.from_csv(self.csvs()[0])
        self.assertEqual([x["url"] for x in got],
                         ["https://a.example/4", "https://a.example/1", "https://a.example/7"])
        self.assertEqual([x["rank"] for x in got], [1, 2, 3])

    def test_formula_escape_undone(self):
        self.history(row("https://a.example/5", "2026-10-09", title="'=SUM AI", company="'@Corp"))
        self.run_main("--since", "7")
        got = rp.from_csv(self.csvs()[0])[0]
        self.assertEqual((got["title"], got["company"]), ("=SUM AI", "@Corp"))

    def test_dedupe_sources(self):
        self.history(*[row(f"https://d.example/{i}", "2026-10-09") for i in range(1, 7)])
        (self.root / "applications.md").write_text(
            "| x | https://d.example/1/?utm_source=li |\n", encoding="utf-8")
        (self.root / "dlq.md").write_text(
            "| 2026-10-10 | b | 1 | C | T | https://D.EXAMPLE/2/ | score | LOW-SCORE | d | n | open |\n",
            encoding="utf-8")
        p = self.root / "postings" / "Acme-3"
        p.mkdir()
        (p / "posting.md").write_text("# Acme: AI\n- URL: https://d.example/3\n", encoding="utf-8")
        (self.root / "discovered").mkdir()
        (self.root / "discovered" / "2026-10-01.csv").write_text(
            "Rank,Company,Title,Location,URL\n1,A,T,L,https://d.example/4\n", encoding="utf-8")
        ex = self.root / "list.txt"
        ex.write_text("https://d.example/5\n", encoding="utf-8")
        self.run_main("--since", "7", "--exclude", str(ex))
        new = [f for f in self.csvs() if f.name == "2026-10-10.csv"][0]
        self.assertEqual([x["url"] for x in rp.from_csv(new)], ["https://d.example/6"])

    def test_csv_round_trip_with_commas(self):
        self.history(row("https://c.example/1", "2026-10-09", title="AI; ML Engineer", company="Acme, Inc"))
        self.run_main("--since", "7")
        got = rp.read_source(self.csvs()[0])[0]
        self.assertEqual((got["company"], got["title"]), ("Acme, Inc", "AI; ML Engineer"))

    def test_nothing_new_writes_nothing(self):
        self.history(row("https://a.example/1", "2026-01-01"))
        code, out = self.run_main("--since", "7")
        self.assertEqual(code, 0)
        self.assertIn("no new postings", out)
        self.assertFalse((self.root / "discovered").exists())

    def test_last_run_cutoff_and_default(self):
        self.history(row("https://a.example/1", "2026-10-05"), row("https://a.example/2", "2026-10-02"))
        (self.root / "discovered").mkdir()
        (self.root / "discovered" / ".last-run").write_text("2026-10-05\n", encoding="utf-8")
        self.run_main()
        self.assertEqual([x["url"] for x in rp.from_csv(self.csvs()[0])], ["https://a.example/1"])
        self.assertEqual((self.root / "discovered" / ".last-run").read_text().strip(), "2026-10-10")

    def test_default_cutoff_seven_days(self):
        self.history(row("https://a.example/1", "2026-10-03"), row("https://a.example/2", "2026-10-02"))
        self.run_main()
        self.assertEqual([x["url"] for x in rp.from_csv(self.csvs()[0])], ["https://a.example/1"])

    def test_second_run_dedupes_earlier_csv(self):
        self.history(row("https://a.example/1", "2026-10-09"))
        self.run_main("--since", "7")
        code, out = self.run_main("--since", "7")
        self.assertIn("no new postings", out)
        self.history(row("https://a.example/1", "2026-10-09"), row("https://a.example/9", "2026-10-10"))
        self.run_main("--since", "7")
        self.assertEqual([f.name for f in self.csvs()], ["2026-10-10-2.csv", "2026-10-10.csv"])

    def test_missing_career_ops(self):
        with self.assertRaises(SystemExit) as cm:
            discover.main(["--root", str(self.root), "--career-ops", str(self.co / "nope")], today=TODAY)
        self.assertNotEqual(cm.exception.code, 0)

    def test_missing_node(self):
        self.history(row("https://a.example/1", "2026-10-09"))
        with mock.patch.object(discover.shutil, "which", return_value=None):
            with self.assertRaises(SystemExit) as cm:
                discover.main(["--root", str(self.root), "--career-ops", str(self.co)], today=TODAY)
        self.assertIn("node", str(cm.exception.code))
        self.assertFalse((self.root / "discovered").exists())

    def test_scan_failure(self):
        self.history(row("https://a.example/1", "2026-10-09"))
        done = mock.Mock(returncode=1)
        with mock.patch.object(discover.shutil, "which", return_value="node"), \
                mock.patch.object(discover.subprocess, "run", return_value=done) as run:
            with self.assertRaises(SystemExit):
                discover.main(["--root", str(self.root), "--career-ops", str(self.co)], today=TODAY)
        self.assertEqual(run.call_args.args[0][1:], ["scan.mjs", "--quiet"])
        self.assertFalse((self.root / "discovered").exists())


    def test_location_filter(self):
        self.history(
            row("https://l.example/1", "2026-10-09", location="Montreal, QC"),
            row("https://l.example/2", "2026-10-09", location="San Francisco, CA"),
            row("https://l.example/3", "2026-10-09", location=""),
            row("https://l.example/4", "2026-10-09", location="Remote - Canada"),
        )
        self.run_main("--since", "7", "--location", "canada", "Montreal")
        urls = [x["url"] for x in rp.from_csv(self.csvs()[0])]
        self.assertEqual(urls, ["https://l.example/1", "https://l.example/3", "https://l.example/4"])

    def test_missing_exclude_file(self):
        self.history(row("https://a.example/1", "2026-10-09"))
        with self.assertRaises(SystemExit) as cm:
            self.run_main("--since", "7", "--exclude", str(self.root / "nope.csv"))
        self.assertIn("exclude", str(cm.exception.code))
        self.assertFalse((self.root / "discovered").exists())

    def test_applications_url_trailing_punctuation(self):
        self.history(row("https://p.example/1", "2026-10-09"), row("https://p.example/2", "2026-10-09"))
        (self.root / "applications.md").write_text(
            "| x | Applied via https://p.example/1. Thanks |\n", encoding="utf-8")
        self.run_main("--since", "7")
        self.assertEqual([x["url"] for x in rp.from_csv(self.csvs()[0])], ["https://p.example/2"])

    def test_scan_history_env_override(self):
        other = self.root.parent / "elsewhere.tsv"
        other.write_text(HEADER + row("https://e.example/1", "2026-10-09"), encoding="utf-8")
        with mock.patch.dict(discover.os.environ, {"CAREER_OPS_SCAN_HISTORY": str(other)}):
            self.run_main("--since", "7")
        self.assertEqual([x["url"] for x in rp.from_csv(self.csvs()[0])], ["https://e.example/1"])

if __name__ == "__main__":
    unittest.main()
