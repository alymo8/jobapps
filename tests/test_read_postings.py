import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import read_postings as rp  # noqa: E402

HEAD = "| Date | Batch | Rank | Company | Title | URL | Stage | Reason | Detail | Needs | Status |\n"
SEP = "|---|---|---|---|---|---|---|---|---|---|---|\n"


def dlq_row(rank, url, reason, status="open"):
    return f"| 2026-10-10 | b | {rank} | Co{rank} | T{rank} | {url} | score | {reason} | d | n | {status} |\n"


class ReadPostingsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "dlq.md").write_text(
            HEAD + SEP
            + dlq_row(1, "https://a.example/1", "LOW-SCORE")
            + dlq_row(2, "https://a.example/2", "BLOCKED"),
            encoding="utf-8",
        )
        self.patches = [
            mock.patch.object(rp, "ROOT", self.root),
            mock.patch.object(rp, "DLQ", self.root / "dlq.md"),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.tmp.cleanup()

    def run_main(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rp.main(list(args))
        return json.loads(out.getvalue())

    def test_low_score_skipped_from_dlq_source(self):
        urls = [x["url"] for x in self.run_main(str(self.root / "dlq.md"))]
        self.assertEqual(urls, ["https://a.example/2"])

    def test_low_score_selected_with_reason(self):
        urls = [x["url"] for x in self.run_main(str(self.root / "dlq.md"), "--reason", "low-score")]
        self.assertEqual(urls, ["https://a.example/1"])

    def test_low_score_url_held_unless_all(self):
        self.assertEqual(self.run_main("https://a.example/1"), [])
        kept = self.run_main("https://a.example/1", "--all")
        self.assertEqual([x["url"] for x in kept], ["https://a.example/1"])
        self.assertEqual(kept[0]["dlq"], "LOW-SCORE")

    def test_resolved_low_score_not_held(self):
        (self.root / "dlq.md").write_text(
            HEAD + SEP + dlq_row(1, "https://a.example/1", "LOW-SCORE", status="resolved")
            + dlq_row(3, "https://a.example/3", "CLOSED", status="resolved"),
            encoding="utf-8",
        )
        self.assertEqual([x["url"] for x in self.run_main("https://a.example/1")], ["https://a.example/1"])
        self.assertEqual(self.run_main("https://a.example/3"), [])

    def test_dlq_rows_takes_a_path(self):
        other = self.root / "other.md"
        other.write_text(HEAD + SEP + dlq_row(5, "https://b.example/5", "CLOSED"), encoding="utf-8")
        self.assertEqual([r["url"] for r in rp.dlq_rows(other)], ["https://b.example/5"])
        self.assertEqual(len(rp.dlq_rows()), 2)

    def test_read_source_txt_ranks_from_start(self):
        f = self.root / "list.txt"
        f.write_text("https://x.example/1\nnot a url\nhttps://x.example/2\n", encoding="utf-8")
        got = rp.read_source(f, start_rank=4)
        self.assertEqual([(x["rank"], x["url"]) for x in got],
                         [(4, "https://x.example/1"), (5, "https://x.example/2")])

    def test_main_txt_ranks_continue_after_url_args(self):
        f = self.root / "list.txt"
        f.write_text("https://x.example/9\n", encoding="utf-8")
        got = self.run_main("https://x.example/8", str(f))
        self.assertEqual([x["rank"] for x in got], [1, 2])

    def test_read_source_csv(self):
        f = self.root / "list.csv"
        f.write_text('"Rank","Company","Title","Location","URL"\n"1","Acme, Inc","AI Eng","Montreal","https://x.example/c"\n',
                     encoding="utf-8")
        got = rp.read_source(f)
        self.assertEqual((got[0]["company"], got[0]["url"]), ("Acme, Inc", "https://x.example/c"))

    def test_normalize_url(self):
        n = rp.normalize_url
        self.assertEqual(n("HTTPS://Jobs.Lever.co/Acme/123/?utm_source=x"), "https://jobs.lever.co/Acme/123")
        self.assertEqual(n("https://x.example/jobs?gh_jid=42&utm=1"), "https://x.example/jobs?gh_jid=42")
        self.assertEqual(n("https://x.example/a#frag"), "https://x.example/a")
        self.assertEqual(n(" https://x.example/a/ "), "https://x.example/a")


if __name__ == "__main__":
    unittest.main()
