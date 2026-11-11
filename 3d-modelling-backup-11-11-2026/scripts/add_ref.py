#!/usr/bin/env python3
"""Add BibTeX entries to references.bib from a DOI or an arXiv ID.

Metadata is fetched from doi.org (Crossref/DataCite), never typed by hand.

Usage:
    python3 scripts/add_ref.py 10.1016/j.autcon.2025.106303
    python3 scripts/add_ref.py 2503.11651 https://arxiv.org/abs/2406.09414
    python3 scripts/add_ref.py --bib other.bib <id> ...
"""

import argparse
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_BIB = Path(__file__).resolve().parent.parent / "references.bib"

# Fields kept in the output, in this order. Everything else is dropped.
FIELDS = ["author", "title", "journal", "booktitle", "volume", "number",
          "pages", "month", "year", "publisher", "howpublished", "doi", "url"]

MONTHS = {"jan", "feb", "mar", "apr", "may", "jun",
          "jul", "aug", "sep", "oct", "nov", "dec"}

STOPWORDS = {"a", "an", "the", "on", "of", "for", "in", "to", "and", "with",
             "towards", "toward", "via", "from", "by", "is", "are"}

ARXIV_RE = re.compile(r"(?:arxiv[:/]|arxiv\.org/(?:abs|pdf)/)?(\d{4}\.\d{4,5})(?:v\d+)?",
                      re.IGNORECASE)
DOI_RE = re.compile(r"(10\.\d{4,9}/\S+)")


def parse_identifier(raw):
    """Return (doi, arxiv_id). arxiv_id is None for regular DOIs."""
    raw = raw.strip()
    if "doi.org/" not in raw and not raw.startswith("10."):
        m = ARXIV_RE.fullmatch(raw)
        if not m and "arxiv" in raw.lower():
            m = ARXIV_RE.search(raw)
        if m:
            return f"10.48550/arXiv.{m.group(1)}", m.group(1)
    m = DOI_RE.search(raw)
    if m:
        doi = m.group(1).rstrip(".,;")
        arxiv = re.fullmatch(r"10\.48550/arxiv\.(\d{4}\.\d{4,5})", doi, re.IGNORECASE)
        return doi, arxiv.group(1) if arxiv else None
    raise ValueError(f"not a DOI or arXiv ID: {raw}")


def fetch_bibtex(doi):
    req = urllib.request.Request(
        f"https://doi.org/{doi}",
        headers={"Accept": "application/x-bibtex; charset=utf-8",
                 "User-Agent": "add_ref.py (academic reference script)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_entry(text):
    """Parse one BibTeX entry into (entry_type, {field: value})."""
    m = re.search(r"@(\w+)\s*\{[^,]*,", text)
    if not m:
        raise ValueError("response is not a BibTeX entry")
    entry_type, i, fields = m.group(1).lower(), m.end(), {}
    while i < len(text):
        fm = re.compile(r"\s*([\w-]+)\s*=\s*").match(text, i)
        if not fm:
            break
        name, i = fm.group(1).lower(), fm.end()
        if text[i] == "{":
            depth, start = 0, i
            while True:
                depth += {"{": 1, "}": -1}.get(text[i], 0)
                i += 1
                if depth == 0:
                    break
            value = text[start + 1:i - 1]
        elif text[i] == '"':
            end = text.index('"', i + 1)
            value, i = text[i + 1:end], end + 1
        else:
            vm = re.compile(r"[^,}\s]+").match(text, i)
            value, i = vm.group(0), vm.end()
        fields[name] = " ".join(value.split())
        i = text.find(",", i) + 1 or len(text)
    return entry_type, fields


def ascii_fold(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def make_key(fields):
    """Key format: <first author last name><year><first title word>."""
    first_author = fields.get("author", "anon").split(" and ")[0]
    last = first_author.split(",")[0] if "," in first_author else first_author.split()[-1]
    last = re.sub(r"[^a-z]", "", ascii_fold(last).lower())
    words = re.findall(r"[a-z0-9]+", ascii_fold(fields.get("title", "")).lower())
    word = next((w for w in words if w not in STOPWORDS and not w[0].isdigit()), "")
    return f"{last}{fields.get('year', '')}{word}"


def protect_acronyms(title):
    """Brace words like VGGT, IFC, V2, 3D, NeRF so IEEEtran keeps their case."""
    if "{" in title:
        return title

    def brace(m):
        w = m.group(0)
        if any(c.isupper() for c in w[1:]) or (any(c.isupper() for c in w)
                                               and any(c.isdigit() for c in w)):
            return f"{{{w}}}"
        return w

    return re.sub(r"[A-Za-z0-9]+", brace, title)


def normalize(entry_type, fields, doi, arxiv_id):
    fields = dict(fields)
    if "title" in fields:
        fields["title"] = protect_acronyms(fields["title"])
    fields["doi"] = doi
    if arxiv_id:
        entry_type = "misc"
        fields["howpublished"] = f"arXiv:{arxiv_id}"
        fields["url"] = f"https://arxiv.org/abs/{arxiv_id}"
        fields.pop("publisher", None)
    else:
        # IEEEtran.bst ignores the doi field, so the DOI is printed via url.
        fields["url"] = f"https://doi.org/{doi}"
    if "pages" in fields:
        fields["pages"] = re.sub(r"\s*(?:–|—|-+)\s*", "--", fields["pages"])
    month = fields.get("month", "")[:3].lower()
    if month in MONTHS:
        fields["month"] = month
    else:
        fields.pop("month", None)
    return entry_type, fields


def format_entry(entry_type, key, fields):
    lines = [f"@{entry_type}{{{key},"]
    for name in FIELDS:
        if name in fields:
            # month is a BibTeX macro (sep), so it stays unbraced.
            value = fields[name] if name == "month" else f"{{{fields[name]}}}"
            lines.append(f"  {name:<12} = {value},")
    lines.append("}")
    return "\n".join(lines) + "\n"


def existing_keys_and_dois(bib_text):
    keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib_text))
    dois = {d.lower() for d in re.findall(r"\bdoi\s*=\s*\{([^}]*)\}", bib_text, re.IGNORECASE)}
    return keys, dois


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("ids", nargs="+", help="DOIs, arXiv IDs, or their URLs")
    parser.add_argument("--bib", type=Path, default=DEFAULT_BIB,
                        help=f"BibTeX file to append to (default: {DEFAULT_BIB})")
    args = parser.parse_args()

    bib_text = args.bib.read_text(encoding="utf-8") if args.bib.exists() else ""
    keys, dois = existing_keys_and_dois(bib_text)
    failed = False

    for raw in args.ids:
        try:
            doi, arxiv_id = parse_identifier(raw)
            if doi.lower() in dois:
                print(f"skip   {raw}: already in {args.bib.name}")
                continue
            entry_type, fields = normalize(*parse_entry(fetch_bibtex(doi)), doi, arxiv_id)
        except (ValueError, urllib.error.URLError) as e:
            print(f"error  {raw}: {e}", file=sys.stderr)
            failed = True
            continue

        key = base = make_key(fields)
        suffix = ord("b")
        while key in keys:
            key, suffix = f"{base}{chr(suffix)}", suffix + 1

        entry = format_entry(entry_type, key, fields)
        with args.bib.open("a", encoding="utf-8") as f:
            f.write(("\n" if bib_text.strip() or keys else "") + entry)
        keys.add(key)
        dois.add(doi.lower())
        print(f"added  {key}: {fields.get('title', '')}")
        if arxiv_id:
            print(f"       note: preprint; cite the published version (conference/journal DOI) if one exists")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
