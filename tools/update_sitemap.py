#!/usr/bin/env python3
"""Setzt <lastmod> in sitemap.xml auf das tatsaechliche Aenderungsdatum jeder Seite.

Quelle: letzter Git-Commit der Datei; Dateien mit uncommitteten Aenderungen bekommen das heutige Datum.
Falsche lastmod-Werte lernt Google zu ignorieren - deshalb nicht von Hand pflegen.
Aufruf aus dem Repo-Root:  python3 tools/update_sitemap.py
"""
import datetime, io, re, subprocess

def sh(*a): return subprocess.run(a, capture_output=True, text=True).stdout.strip()

today = datetime.date.today().isoformat()
dirty = {l[3:].strip().strip('"') for l in sh("git", "status", "--porcelain").splitlines()}
s = io.open("sitemap.xml", encoding="utf-8").read()

def file_of(url):
    p = url.replace("https://combatcoach.org/", "")
    return "index.html" if p == "" else (p + "index.html" if p.endswith("/") else p)

def fix(m):
    f = file_of(m.group(1))
    d = today if f in dirty else (sh("git", "log", "-1", "--format=%cs", "--", f) or today)
    return f"{m.group(0).rsplit('<lastmod>', 1)[0]}<lastmod>{d}</lastmod>"

s2 = re.sub(r"<loc>(https://combatcoach\.org/[^<]*)</loc>\s*<lastmod>[^<]*</lastmod>", fix, s)
io.open("sitemap.xml", "w", encoding="utf-8").write(s2)
for m in re.finditer(r"<loc>https://combatcoach\.org/([^<]*)</loc>\s*<lastmod>([^<]*)</lastmod>", s2):
    print(f"  {m.group(2)}  /{m.group(1)}")
