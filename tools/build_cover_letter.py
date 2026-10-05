"""Check a cover_letter.md and, unless --check, build a one-page PDF from it.

Usage: python tools/build_cover_letter.py <postings/<dir>/cover_letter.md> [--check]

The .md is plain paste-ready text: paragraphs separated by blank lines, starting with
the greeting line and ending with the sign-off (see CoverLetter_prompt_v1.md).
Prints a JSON report:
  words           word count of the whole letter (target 300-400)
  greeting_ok     first line is the exact greeting (English or French form)
  signoff_ok      last two lines are the exact sign-off matching that greeting
  pages           page count of the PDF (must be 1; omitted with --check)
  pdf, png        Aly_Mohamed_Hussein_Cover_Letter_<Company>.pdf/.png next to the .md
  ok              all checks pass (looking at the PNG is still on you)
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

import fitz  # PyMuPDF

sys.path.insert(0, str(Path(__file__).parent))
from build_resume import compile_tex  # noqa: E402

WORDS_MIN, WORDS_MAX = 300, 400
FORMS = {  # greeting -> sign-off lines
    "Dear hiring team,": ["Best,", "Aly"],
    "Bonjour à l'équipe de recrutement,": ["Cordialement,", "Aly"],
}

PREAMBLE = r"""\documentclass[letterpaper,11pt]{article}
\usepackage[empty]{fullpage}
\usepackage[hidelinks]{hyperref}
\usepackage{fontawesome5}
\usepackage[english]{babel}
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}
\setlength{\parindent}{0pt}
\setlength{\parskip}{9pt}
\raggedright
\input{glyphtounicode}
\pdfgentounicode=1
\begin{document}
\begin{center}
    {\Huge \scshape <<name>>} \\ \vspace{1pt}
    \small \raisebox{-0.1\height}\faPhone\ <<phone>> ~
    {\raisebox{-0.2\height}\faHome\ {<<city>>}}  ~
    \href{mailto:<<email>>}{\raisebox{-0.2\height}\faEnvelope\  \underline{<<email>>}} ~
    \href{<<linkedin>>}{\raisebox{-0.2\height}\faLinkedin\ \underline{<<linkedin_bare>>}}  ~
    \href{<<github>>}{\raisebox{-0.2\height}\faGithub\ \underline{<<github_bare>>}}
\end{center}
\vspace{10pt}
"""

# Contact details live in the gitignored profile.md, not in the repo.
PROFILE = Path(__file__).resolve().parent.parent / "profile.md"
CONTACT_KEYS = {"name": "Full name", "phone": "Phone", "email": "Email",
                "city": "Location", "linkedin": "LinkedIn", "github": "GitHub"}  # fmt: skip

SPECIALS = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
            "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\^{}"}


def escape(text: str) -> str:
    return "".join(SPECIALS.get(c, c) for c in text)


def check(lines: list[str]) -> dict:
    greeting = lines[0] if lines else ""
    signoff = FORMS.get(greeting)
    words = len(re.findall(r"\S+", "\n".join(lines)))
    return {
        "words": words,
        "greeting_ok": signoff is not None,
        "signoff_ok": signoff is not None and lines[-2:] == signoff,
    }


def contact() -> dict:
    """Header fields from the "## Contact" bullets ("- Key: value") of profile.md."""
    text = PROFILE.read_text(encoding="utf-8")
    section = text.split("## Contact", 1)[1].split("\n## ", 1)[0]
    fields = dict(re.findall(r"^- ([^:\n]+): *(\S.*?) *$", section, re.M))
    c = {k: fields[v] for k, v in CONTACT_KEYS.items()}
    c["city"] = c["city"].split(",")[0]
    for k in ("linkedin", "github"):
        c[f"{k}_bare"] = re.sub(r"^https?://", "", c[k])
    return c


def preamble() -> str:
    out = PREAMBLE
    for k, v in contact().items():
        out = out.replace(f"<<{k}>>", v)
    return out


def to_tex(text: str) -> str:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text.strip())]
    body = []
    for p in paragraphs:
        body.append(r" \\ ".join(escape(line.strip()) for line in p.splitlines()))
    today = date.today()
    dated = f"{today:%B} {today.day}, {today.year}"
    return preamble() + dated + "\n\n" + "\n\n".join(body) + "\n\\end{document}\n"


def main(argv: list[str]) -> int:
    md = Path(argv[0]).resolve()
    text = md.read_text(encoding="utf-8")
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    report = {"md": str(md), **check(lines)}
    report["ok"] = (WORDS_MIN <= report["words"] <= WORDS_MAX
                    and report["greeting_ok"] and report["signoff_ok"])
    if "--check" not in argv:
        company = md.parent.name.split("-")[0]
        tex = md.with_name(f"Aly_Mohamed_Hussein_Cover_Letter_{company}.tex")
        tex.write_text(to_tex(text), encoding="utf-8")
        errors, overfull = compile_tex(tex)
        report.update(errors=errors, overfull=overfull)
        pdf = tex.with_suffix(".pdf")
        if errors or not pdf.exists():
            report["ok"] = False
        else:
            doc = fitz.open(pdf)
            png = tex.with_suffix(".png")
            doc[0].get_pixmap(dpi=110).save(png)
            report.update(pages=doc.page_count, pdf=str(pdf), png=str(png))
            doc.close()
            report["ok"] = report["ok"] and report["pages"] == 1
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
