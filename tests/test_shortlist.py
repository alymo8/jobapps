import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))
import shortlist  # noqa: E402

FIXTURE_KEYS = Path(__file__).resolve().parent / "fixtures" / "decision_keys.py"
FIXTURE_SHA256 = "d359f04c6f7f2dc873ab3f07528f7627f7d0bf7749b3a1f52b189ef1ffd7415d"
KEYS = shortlist.load_keys(FIXTURE_KEYS)


def row(rank, company, title, url, **kw):
    r = {
        "rank": rank, "tab": "main", "company": company, "title": title,
        "location": "Toronto, ON", "work_mode": "Hybrid", "company_type": "Startup",
        "priority": "No", "canada": "Confirmed", "new": "No", "status": "Open",
        "deadline": "", "fit_notes": "", "url": url, "score": 50.0,
    }
    r.update(kw)
    return r


def body(url, company, title, decision="applied", decided_at="2026-10-10T09:00:00-04:00", note=""):
    return {
        "schema_version": 1, "url": url, "url_norm": KEYS.norm_url(url),
        "company": company, "title": title, "match_key": KEYS.match_key(company, title),
        "decision": decision, "source": "user", "decided_at": decided_at,
        "week_seen": "2026-10-17", "note": note,
    }


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def week(self, rows, week="2026-10-17"):
        p = self.dir / f"{week}.json"
        p.write_text(json.dumps({"week": week, "rows": rows}), encoding="utf-8")
        return p

    def decisions_dir(self, docs, wrapped=True):
        d = self.dir / "dump"
        (d / "decisions").mkdir(parents=True, exist_ok=True)
        for i, b in enumerate(docs):
            doc_id = KEYS.doc_id(b["url"])
            obj = {"id": doc_id, "version": i + 1, "data": b} if wrapped else b
            (d / "decisions" / f"{doc_id}.json").write_text(json.dumps(obj), encoding="utf-8")
        return d

    def run_cli(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = shortlist.main([str(a) for a in args])
        text = out.getvalue()
        try:
            return code, json.loads(text)
        except json.JSONDecodeError:
            return code, text


class KeysAndInputsTest(Base):
    def test_fixture_sha256(self):
        self.assertEqual(hashlib.sha256(FIXTURE_KEYS.read_bytes()).hexdigest(), FIXTURE_SHA256)

    def test_load_keys_ok(self):
        self.assertEqual(KEYS.norm_url("https://www.X.com/a/"), "x.com/a")

    def test_load_keys_missing_function(self):
        p = self.dir / "bad_keys.py"
        p.write_text("def norm_url(u): return u\n", encoding="utf-8")
        with self.assertRaises(shortlist.KeysError) as ctx:
            shortlist.load_keys(p)
        self.assertIn("doc_id", str(ctx.exception))

    def test_load_keys_missing_function_cli(self):
        p = self.dir / "bad_keys.py"
        p.write_text("def norm_url(u): return u\n", encoding="utf-8")
        code, out = self.run_cli("list", "--keys", p, "--rows", self.week([]), "--decisions", self.dir)
        self.assertEqual(code, 1)
        self.assertFalse(out["ok"])
        self.assertIn("doc_id", out["error"])

    def test_load_keys_broken_module(self):
        sources = ("def norm_url(:\n", "raise SystemExit('boom')\n", "import not_a_module_xyz\n")
        for i, src in enumerate(sources):
            p = self.dir / f"broken{i}.py"
            p.write_text(src, encoding="utf-8")
            with self.assertRaises(shortlist.KeysError):
                shortlist.load_keys(p)

    def test_bad_decision_file_skipped(self):
        d = self.dir / "dump" / "decisions"
        d.mkdir(parents=True)
        (d / "u-bad.json").write_text("{not json", encoding="utf-8")
        (d / "u-b.json").write_text(json.dumps(body("https://b.com/1", "B", "T")))
        with contextlib.redirect_stderr(io.StringIO()):
            got = shortlist.load_decisions(self.dir / "dump")
        self.assertEqual([x["doc_id"] for x in got], ["u-b"])

    def test_load_rows_json(self):
        week, rows = shortlist.load_rows(self.week([row(1, "A", "T", "https://a.com/1")]))
        self.assertEqual(week, "2026-10-17")
        self.assertEqual(rows[0]["company"], "A")

    def test_load_rows_csv(self):
        p = self.dir / "2026-10-10.csv"
        p.write_text(
            "rank,tab,company,title,location,work_mode,company_type,priority,canada,new,url\n"
            "3,main,Okta,Engineer,Toronto,Remote,Public,Yes,Confirmed,No,https://okta.com/j/3\n",
            encoding="utf-8",
        )
        week, rows = shortlist.load_rows(p)
        self.assertEqual(week, "2026-10-10")
        self.assertEqual(rows[0]["rank"], 3)
        for k in ("deadline", "status", "fit_notes", "score"):
            self.assertEqual(rows[0][k], "")

    def test_load_decisions_wrapped_and_bare(self):
        d = self.dir / "dump" / "decisions"
        d.mkdir(parents=True)
        (d / "u-a.json").write_text(json.dumps({"id": "u-a", "version": 3, "data": body("https://a.com/1", "A", "T")}))
        (d / "u-b.json").write_text(json.dumps(body("https://b.com/1", "B", "T")))
        got = {x["doc_id"]: x for x in shortlist.load_decisions(self.dir / "dump")}
        self.assertEqual(got["u-a"]["version"], 3)
        self.assertIsNone(got["u-b"]["version"])
        self.assertEqual(got["u-b"]["body"]["company"], "B")

    def test_is_decided_by_url_and_by_match_key(self):
        decs = [
            {"doc_id": "x", "version": 1, "body": body("https://www.a.com/1/", "Other", "Other")},
            {"doc_id": "y", "version": 1, "body": body("https://elsewhere.com/9", "Acme Inc.", "Backend Engineer")},
        ]
        idx = shortlist.decided_index(decs)
        self.assertTrue(shortlist.is_decided(KEYS, row(1, "A", "T", "https://a.com/1"), idx))
        self.assertTrue(shortlist.is_decided(KEYS, row(2, "Acme", "Backend Engineer", "https://acme.com/2"), idx))
        self.assertFalse(shortlist.is_decided(KEYS, row(3, "Okta", "Engineer", "https://okta.com/3"), idx))


class ListTest(Base):
    def rows(self):
        return [
            row(1, "Mistral AI", "FDE", "https://m.com/1", new="Yes", priority="Yes", location="Montréal, QC"),
            row(2, "Acme", "Backend Engineer", "https://acme.com/2", tab="below_cut"),
            row(3, "Okta", "Engineer", "https://okta.com/3", deadline="2026-10-11"),
            row(4, "Cohere", "ML Engineer", "https://c.com/4", deadline="2026-10-31", canada="Confirmed (province-restricted)"),
            row(50, "Globex", "AI Engineer", "https://globex.com/50", deadline="2026-10-22"),
            row(80, "TD", "Data Scientist", "https://td.com/80", deadline="2026-10-20"),
            row(90, "Shopify", "Dev", "https://shop.com/90", deadline="2026-10-25"),
        ]

    def list(self, *extra, decisions=()):
        d = self.decisions_dir(list(decisions))
        return self.run_cli("list", "--keys", FIXTURE_KEYS, "--rows", self.week(self.rows()),
                            "--decisions", d, "--today", "2026-10-18", *extra)

    def ranks(self, out):
        return [r["rank"] for r in out["rows"]]

    def test_sort_deadlines_within_7_days_first(self):
        _, out = self.list()
        self.assertEqual(self.ranks(out), [80, 50, 90, 1, 2, 3, 4])

    def test_decided_rows_hidden_and_counts(self):
        _, out = self.list(decisions=[body("https://acme.com/2", "x", "y")])
        self.assertNotIn(2, self.ranks(out))
        self.assertEqual((out["total_rows"], out["decided_hidden"], out["shown"], out["week"]), (7, 1, 6, "2026-10-17"))

    def test_filters(self):
        self.assertEqual(self.ranks(self.list("--new")[1]), [1])
        self.assertEqual(self.ranks(self.list("--priority")[1]), [1])
        self.assertEqual(self.ranks(self.list("--location", "montreal")[1]), [1])
        self.assertEqual(len(self.list("--location", "montreal", "--location", "toronto")[1]["rows"]), 7)
        self.assertEqual(self.ranks(self.list("--company", "acme")[1]), [2])
        self.assertEqual(self.ranks(self.list("--title", "engineer", "--tab", "main")[1]), [50, 3, 4])
        self.assertEqual(self.ranks(self.list("--tab", "below_cut")[1]), [2])
        self.assertEqual(self.ranks(self.list("--top", "2")[1]), [80, 50])
        self.assertEqual(self.ranks(self.list("--top", "0")[1]), [])

    def test_chips(self):
        rows = {r["rank"]: r["chips"] for r in self.list()[1]["rows"]}
        self.assertEqual(rows[1], ["New", "Priority"])
        self.assertEqual(rows[4], ["Province-restricted", "Deadline 2026-10-31"])
        self.assertEqual(rows[50], ["Deadline 2026-10-22"])
        self.assertEqual(rows[3], ["Deadline 2026-10-11 (past)"])

    def test_table(self):
        _, text = self.list("--table", "--top", "1")
        self.assertIn("Week 2026-10-17: 1 shown, 0 decided hidden, 7 rows", text)
        self.assertIn("| Rank | Company | Title | Location | Chips | URL |", text)
        self.assertIn("| 80 | TD | Data Scientist |", text)


class FindDocDecisionsTest(Base):
    def test_find(self):
        newer = self.week([
            row(1, "Example", "Dev", "https://example.com/job/1"),
            row(3, "Globex", "Senior AI Engineer (Toronto)", "https://globex.com/3"),
            row(4, "Acme", "Backend", "https://acme.com/4"),
            row(5, "Acme", "Frontend", "https://acme.com/5"),
            row(6, "Brokta Inc", "Engineer", "https://brokta.com/6"),
        ])
        older = self.week([row(9, "Okta", "Engineer", "https://okta.com/9")], week="2026-10-10")
        f = ("find", "--keys", FIXTURE_KEYS, "--rows", newer, older)
        self.assertEqual(self.run_cli(*f, "--url", "https://www.Example.com/job/1/")[1][0]["rank"], 1)
        self.assertEqual(self.run_cli(*f, "--rank", "3")[1][0]["company"], "Globex")
        self.assertEqual(len(self.run_cli(*f, "--company", "Globex", "--title", "Senior AI Engineer")[1]), 1)
        self.assertEqual(self.run_cli(*f, "--company", "globex", "--title", "ai engineer")[1][0]["rank"], 3)
        self.assertEqual([m["rank"] for m in self.run_cli(*f, "--company", "acme")[1]], [4, 5])
        self.assertEqual(self.run_cli(*f, "--company", "brokta")[1][0]["rank"], 6)
        okta = self.run_cli(*f, "--company", "okta")[1]  # "okta" is not a word of "brokta"
        self.assertEqual((okta[0]["rank"], okta[0]["week"]), (9, "2026-10-10"))
        self.assertNotIn("decided", okta[0])
        d = self.decisions_dir([body("https://acme.com/4", "Acme", "Backend")])
        got = self.run_cli(*f, "--company", "acme", "--decisions", d)[1]
        self.assertEqual([m["decided"] for m in got], [True, False])

    def doc(self, *extra):
        return self.run_cli("doc", "--keys", FIXTURE_KEYS, "--url", "https://jobs.lever.co/x/1",
                            "--company", "Mistral AI", "--title", "FDE (Montreal)",
                            "--decision", "applied", "--week", "2026-10-17", *extra)[1]

    def test_doc_fields(self):
        out = self.doc("--note", "tailored resume")
        d = out["data"]
        self.assertEqual(set(d), {"schema_version", "url", "url_norm", "company", "title", "match_key",
                                  "decision", "source", "decided_at", "week_seen", "note"})
        self.assertEqual(out["doc_id"], KEYS.doc_id("https://jobs.lever.co/x/1"))
        self.assertEqual(d["url_norm"], KEYS.norm_url("https://jobs.lever.co/x/1"))
        self.assertEqual(d["match_key"], KEYS.match_key("Mistral AI", "FDE (Montreal)"))
        self.assertEqual((d["schema_version"], d["source"], d["note"]), (1, "claude_code", "tailored resume"))
        self.assertIsNotNone(datetime.fromisoformat(d["decided_at"]).tzinfo)
        self.assertIsNone(out["if_version"])

    def test_doc_date_and_empty_week(self):
        d = self.doc("--decided-at", "2026-10-17")["data"]
        self.assertTrue(d["decided_at"].startswith("2026-10-17T12:00:00"))
        self.assertIsNotNone(datetime.fromisoformat(d["decided_at"]).tzinfo)
        out = self.run_cli("doc", "--keys", FIXTURE_KEYS, "--url", "https://a.com/1", "--company", "A",
                           "--title", "T", "--decision", "not_interested", "--week", "")[1]
        self.assertEqual(out["data"]["week_seen"], "")

    def test_doc_existing_note(self):
        p = self.dir / "existing.json"
        p.write_text(json.dumps({"id": "u-x", "version": 7, "data": body("https://jobs.lever.co/x/1", "Mistral AI", "FDE", note="too senior")}))
        self.assertEqual(self.doc("--existing", p)["data"]["note"], "too senior")
        out = self.doc("--existing", p, "--note", "tailored resume")
        self.assertEqual(out["data"]["note"], "too senior; tailored resume")
        self.assertEqual(out["if_version"], 7)
        self.assertEqual(self.doc("--existing", p, "--note", "too senior")["data"]["note"], "too senior")

    def test_decisions(self):
        d = self.decisions_dir([
            body("https://acme.com/2", "Acme", "Backend Engineer", decided_at="2026-10-01T10:00:00-04:00"),
            body("https://okta.com/3", "Okta", "Engineer", decision="not_interested", decided_at="2026-10-15T10:00:00-04:00"),
            body("https://globex.com/4", "Globex", "AI Engineer", decided_at="2026-10-12T10:00:00-04:00"),
        ])
        base = ("decisions", "--keys", FIXTURE_KEYS, "--decisions", d)
        companies = lambda out: [x["body"]["company"] for x in out]  # noqa: E731
        self.assertEqual(companies(self.run_cli(*base)[1]), ["Okta", "Globex", "Acme"])
        self.assertEqual(companies(self.run_cli(*base, "--decision", "applied")[1]), ["Globex", "Acme"])
        self.assertEqual(companies(self.run_cli(*base, "--match", "acme")[1]), ["Acme"])
        self.assertEqual(companies(self.run_cli(*base, "--url", "https://www.globex.com/4/")[1]), ["Globex"])
        self.assertEqual(companies(self.run_cli(*base, "--company", "Okta Inc", "--title", "Engineer")[1]), ["Okta"])
        self.assertEqual(companies(self.run_cli(*base, "--company", "globex")[1]), ["Globex"])
        first = self.run_cli(*base)[1][0]
        self.assertEqual(first["doc_id"], KEYS.doc_id("https://okta.com/3"))
        self.assertIsNotNone(first["version"])


class PendingTest(Base):
    def add(self, pending, *extra, keys=True, decision="applied", url="https://a.com/1"):
        args = ["pending-add", "--file", pending, "--url", url, "--company", "A", "--title", "T",
                "--decision", decision, "--week", ""]
        if keys:
            args += ["--keys", FIXTURE_KEYS]
        return self.run_cli(*args, *extra)

    def lines(self, pending):
        return [json.loads(x) for x in pending.read_text(encoding="utf-8").splitlines() if x.strip()]

    def test_add_with_keys(self):
        pending = self.dir / "sub" / "pending.jsonl"
        self.add(pending)
        self.add(pending, url="https://a.com/2")
        lines = self.lines(pending)
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0]["doc_id"], KEYS.doc_id("https://a.com/1"))
        self.assertEqual(lines[0]["data"]["match_key"], KEYS.match_key("A", "T"))

    def test_add_without_keys(self):
        pending = self.dir / "pending.jsonl"
        self.add(pending, keys=False)
        line = self.lines(pending)[0]
        self.assertEqual((line["doc_id"], line["data"]["url_norm"], line["data"]["match_key"]), ("", "", ""))
        self.assertEqual(line["data"]["source"], "claude_code")

    def test_plan_and_clear(self):
        pending = self.dir / "pending.jsonl"
        self.add(pending, url="https://same.com/1")
        self.add(pending, url="https://diff.com/1", decision="not_interested")
        self.add(pending, url="https://new.com/1", keys=False)
        d = self.decisions_dir([body("https://same.com/1", "A", "T"), body("https://diff.com/1", "A", "T")])
        code, plan = self.run_cli("pending-plan", "--keys", FIXTURE_KEYS, "--file", pending, "--decisions", d)
        self.assertEqual(code, 0)
        self.assertEqual([p["action"] for p in plan], ["skip", "write", "write"])
        self.assertEqual(plan[1]["if_version"], 2)
        self.assertIsNone(plan[2]["if_version"])
        self.assertEqual(plan[2]["doc_id"], KEYS.doc_id("https://new.com/1"))
        self.assertEqual(plan[2]["data"]["url_norm"], "new.com/1")
        self.assertEqual(plan[2]["data"]["match_key"], "a|t")
        self.run_cli("pending-clear", "--file", pending)
        self.assertTrue(pending.exists())
        self.assertEqual(pending.stat().st_size, 0)

    def test_plan_dedupes_and_merges_notes(self):
        pending = self.dir / "pending.jsonl"
        self.add(pending, "--note", "first", decision="not_interested")
        self.add(pending, "--note", "applied on site")
        d = self.decisions_dir([body("https://a.com/1", "A", "T", decision="not_interested", note="too senior")])
        _, plan = self.run_cli("pending-plan", "--keys", FIXTURE_KEYS, "--file", pending, "--decisions", d)
        self.assertEqual(len(plan), 1)
        self.assertEqual((plan[0]["action"], plan[0]["data"]["decision"]), ("write", "applied"))
        self.assertEqual(plan[0]["data"]["note"], "too senior; applied on site")

    def test_plan_missing_file(self):
        code, plan = self.run_cli("pending-plan", "--keys", FIXTURE_KEYS, "--file", self.dir / "nope.jsonl",
                                  "--decisions", self.dir)
        self.assertEqual((code, plan), (0, []))


if __name__ == "__main__":
    unittest.main()
