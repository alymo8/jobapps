"""Reference key functions for the user's Job Shortlist decisions. Must match the page's JS exactly."""
import hashlib, re, unicodedata
from urllib.parse import urlsplit
CO_SUFFIX = {"inc","ltd","llc","corp","corporation","canada","group","co","the"}
def norm_url(u):
    u = (u or "").strip()
    try:
        x = urlsplit(u)
        if not x.scheme or not x.netloc: raise ValueError
        host = (x.hostname or "").lower()
        host = host[4:] if host.startswith("www.") else host
        p = x.path or "/"
        if len(p) > 1: p = p.rstrip("/") or "/"
        return host + p + (("?" + x.query) if x.query else "")
    except Exception:
        return u.lower()
def norm_text(s):
    s = re.sub(r"\([^)]*\)", " ", s or "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not ("̀" <= c <= "ͯ"))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
def norm_company(s):
    t = [w for w in norm_text(s).split(" ") if w]
    while len(t) > 1 and t[-1] in CO_SUFFIX: t.pop()
    return " ".join(t)
def match_key(company, title): return norm_company(company) + "|" + norm_text(title)
def doc_id(url): return "u-" + hashlib.sha256(norm_url(url).encode()).hexdigest()[:24]
