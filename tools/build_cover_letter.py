"""Check a cover_letter.md and, unless --check, build a one-page PDF from it.

Usage: python tools/build_cover_letter.py <postings/<dir>/cover_letter.md> [--check] [--profile <path>]

The .md is plain paste-ready text: paragraphs separated by blank lines, starting with
the greeting line and ending with the sign-off (see sources/cover_letter_prompt.md).
--profile defaults to sources/profile.md; its "## Contact" section gives the sign-off
name, the letter header and the output file name.
Prints a JSON report:
  words           word count of the whole letter (target 300-400)
  greeting_ok     first line is the exact greeting (English or French form)
  signoff_ok      last two lines are the closing word for that greeting and the
                  profile's "Preferred first name" (else the first word of "Full name")
  pages           page count of the PDF (must be 1; omitted with --check)
  pdf             <Full_Name>_Cover_Letter_<Company>.pdf next to the .md
  png             rendered page preview, in the temp dir
  ok              all checks pass (looking at the PNG is still on you)
  error           sources/profile.md (or --profile) is missing, or its ## Contact lacks Full name,
                  Phone, Email or Location (LinkedIn and GitHub are optional), in either mode
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

import fitz  # PyMuPDF

sys.path.insert(0, str(Path(__file__).parent))
from build_resume import compile_tex, preview_png  # noqa: E402

WORDS_MIN, WORDS_MAX = 300, 400
FORMS = {  # greeting -> closing word
    "Dear hiring team,": "Best,",
    "Bonjour à l'équipe de recrutement,": "Cordialement,",
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
    \href{mailto:<<email_url>>}{\raisebox{-0.2\height}\faEnvelope\  \underline{<<email>>}}<<links>>
\end{center}
\vspace{10pt}
"""
LINK = r"""  ~
    \href{<<url>>}{\raisebox{-0.2\height}\fa<<icon>>\ \underline{<<bare>>}}"""

# Contact details come from the pulled Profile doc (gitignored sources/), not the repo.
PROFILE = Path(__file__).resolve().parent.parent / "sources/profile.md"
MISSING_PROFILE = "sources/profile.md missing: pull the sources first (.claude/skills/pull-sources.md)"
CONTACT_KEYS = {"name": "Full name", "phone": "Phone", "email": "Email",
                "city": "Location", "linkedin": "LinkedIn", "github": "GitHub"}  # fmt: skip
OPTIONAL_KEYS = ("linkedin", "github")  # the header leaves out a link the profile lacks

SPECIALS = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
            "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\^{}"}


def escape(text: str) -> str:
    return "".join(SPECIALS.get(c, c) for c in text)


def escape_url(url: str) -> str:
    """A URL for \\href: hyperref takes it verbatim except for %, # and backslash."""
    return url.replace("\\", "/").replace("%", r"\%").replace("#", r"\#")


def check(lines: list[str], name: str) -> dict:
    greeting = lines[0] if lines else ""
    closing = FORMS.get(greeting)
    words = len(re.findall(r"\S+", "\n".join(lines)))
    return {
        "words": words,
        "greeting_ok": closing is not None,
        "signoff_ok": closing is not None and lines[-2:] == [closing, name],
    }


def contact_fields(profile: Path) -> dict[str, str]:
    """Every "## Contact" bullet ("- Key: value") of the profile, trailing note dropped."""
    text = profile.read_text(encoding="utf-8")
    if "## Contact" not in text:
        raise ValueError(f"{profile}: no ## Contact section")
    section = text.split("## Contact", 1)[1].split("\n## ", 1)[0]
    fields = dict(re.findall(r"^- ([^:\n]+): *(\S.*?) *$", section, re.M))
    # Values may carry a trailing note for the user, e.g. "https://... (www form; ...)": drop it.
    return {k: re.sub(r"\s*\([^()]*\)$", "", v) for k, v in fields.items()}


def contact(profile: Path) -> dict:
    """Header fields from the profile's "## Contact" bullets; ValueError names missing ones."""
    fields = contact_fields(profile)
    missing = [v for k, v in CONTACT_KEYS.items() if k not in OPTIONAL_KEYS and v not in fields]
    if missing:
        raise ValueError(f"{profile}: ## Contact lacks {', '.join(missing)}")
    c = {k: fields[v] for k, v in CONTACT_KEYS.items() if v in fields}
    c["city"] = c["city"].split(",")[0]
    for k in OPTIONAL_KEYS:
        if k in c:
            c[f"{k}_bare"] = re.sub(r"^https?://(www\.)?", "", c[k])
    return c


def signoff_name(profile: Path) -> str:
    fields = contact_fields(profile)
    preferred = fields.get("Preferred first name", "")
    if preferred.strip().upper() == "ASK":
        preferred = ""
    return preferred or fields["Full name"].split()[0]


def letter_tex_path(md: Path, profile: Path) -> Path:
    full = "_".join(contact_fields(profile)["Full name"].split())
    company = md.parent.name.split("-")[0]
    return md.with_name(f"{full}_Cover_Letter_{company}.tex")


def preamble(profile: Path) -> str:
    c = contact(profile)
    links = ""
    for k, icon in (("linkedin", "Linkedin"), ("github", "Github")):
        if k in c:
            links += (LINK.replace("<<url>>", escape_url(c[k])).replace("<<icon>>", icon)
                      .replace("<<bare>>", escape(c[f"{k}_bare"])))
    out = PREAMBLE.replace("<<links>>", links).replace("<<email_url>>", escape_url(c["email"]))
    for k in ("name", "phone", "city", "email"):
        out = out.replace(f"<<{k}>>", escape(c[k]))
    return out


def to_tex(text: str, profile: Path) -> str:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text.strip())]
    body = []
    for p in paragraphs:
        body.append(r" \\ ".join(escape(line.strip()) for line in p.splitlines()))
    today = date.today()
    dated = f"{today:%B} {today.day}, {today.year}"
    return preamble(profile) + dated + "\n\n" + "\n\n".join(body) + "\n\\end{document}\n"


def main(argv: list[str]) -> int:
    profile = PROFILE
    if "--profile" in argv:
        i = argv.index("--profile")
        profile = Path(argv[i + 1])
        rest = argv[:i] + argv[i + 2:]
    else:
        rest = argv
    md = Path(next(a for a in rest if a != "--check")).resolve()
    text = md.read_text(encoding="utf-8")
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    has_profile, profile_error = profile.exists(), MISSING_PROFILE
    if has_profile:
        try:
            contact(profile)  # every required ## Contact key, before anything is written
        except ValueError as e:
            has_profile, profile_error = False, str(e)
    report = {"md": str(md), **check(lines, signoff_name(profile) if has_profile else "")}
    report["ok"] = (has_profile and WORDS_MIN <= report["words"] <= WORDS_MAX
                    and report["greeting_ok"] and report["signoff_ok"])
    if not has_profile:
        report.update(ok=False, signoff_ok=False, error=profile_error)
    elif "--check" not in argv:
        tex = letter_tex_path(md, profile)
        tex.write_text(to_tex(text, profile), encoding="utf-8")
        errors, overfull = compile_tex(tex)
        report.update(errors=errors, overfull=overfull)
        pdf = tex.with_suffix(".pdf")
        if errors or not pdf.exists():
            report["ok"] = False
        else:
            doc = fitz.open(pdf)
            png = preview_png(pdf)
            doc[0].get_pixmap(dpi=110).save(png)
            report.update(pages=doc.page_count, pdf=str(pdf), png=str(png))
            doc.close()
            report["ok"] = report["ok"] and report["pages"] == 1
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
