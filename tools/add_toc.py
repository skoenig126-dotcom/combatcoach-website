#!/usr/bin/env python3
"""Fuegt Ratgeberseiten ein Inhaltsverzeichnis mit Sprungmarken ein (idempotent).

- vergibt IDs an alle H2 vor der CTA-Box und an nummerierte H3 ("1. ...") -> Sprungmarken
- Nummerierte H3 erscheinen als Unterpunkte (z. B. die 10 Uebungen) - listenartig, snippet-freundlich
Aufruf aus dem Repo-Root:  python3 tools/add_toc.py
"""
import html, io, re

PAGES = {
  "de": ["boxen-alleine-trainieren.html", "boxsack-training-anfaenger.html", "schattenboxen-kombinationen.html",
         "kickboxen-training.html", "muay-thai-training.html"],
  "en": ["en/train-boxing-alone.html", "en/heavy-bag-training-beginners.html", "en/shadowboxing-combinations.html",
         "en/kickboxing-training.html", "en/muay-thai-training.html"],
}
TITLE = {"de": "In diesem Ratgeber", "en": "In this guide"}
LABEL = {"de": "Inhaltsverzeichnis", "en": "Table of contents"}

CSS = """    .toc { border: 1px solid var(--border-2); border-radius: var(--radius); background: var(--glass); padding: 1.1rem 1.4rem 1rem; margin: 0 0 2.4rem; }
    .toc__title { font-size: .72rem; letter-spacing: .14em; text-transform: uppercase; color: var(--cream-faint); margin: 0 0 .6rem; font-weight: 600; }
    .toc ol { margin: 0; padding-left: 1.2rem; color: var(--cream-faint); }
    .toc li { margin: .25rem 0; font-size: .88rem; }
    .toc ol ol { list-style: none; margin: .3rem 0 .5rem; padding-left: .9rem; }
    .toc ol ol li { font-size: .82rem; margin: .12rem 0; }
    @media (min-width: 640px) { .toc ol.toc__many { columns: 2; column-gap: 1.6rem; } .toc ol.toc__many li { break-inside: avoid; } }
    .toc a { color: var(--cream-dim); }
    .toc a:hover { color: var(--red); }
    h2[id], h3[id] { scroll-margin-top: 84px; }
"""

def slug(text, used):
    t = html.unescape(re.sub(r"<[^>]+>", "", text)).lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"), ("×", "x"), ("&", "und")):
        t = t.replace(a, b)
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:56].rstrip("-") or "abschnitt"
    base, n = t, 2
    while t in used:
        t = f"{base}-{n}"; n += 1
    used.add(t); return t

def build(path, lang):
    s = io.open(path, encoding="utf-8").read()
    if 'class="toc"' in s:
        return "uebersprungen (TOC vorhanden)"
    head, sep, tail = s.partition('<div class="cta-box">')
    assert sep, (path, "keine CTA-Box")
    used, items = set(), []          # items: (id, label, [subitems])
    def h2(m):
        label = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        i = slug(label, used); items.append([i, label, []])
        return f'<h2 id="{i}">{m.group(1)}</h2>'
    def h3(m):
        label = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        if not re.match(r"\d+\.\s", label) or not items:
            return m.group(0)
        i = slug(label, used); items[-1][2].append((i, label))
        return f'<h3 id="{i}">{m.group(1)}</h3>'
    # <details>-Bereiche (FAQ) nicht anfassen: H3 dort sind Fragen, keine Abschnitte
    parts = re.split(r"(<details>.*?</details>)", head, flags=re.S)
    for k, part in enumerate(parts):
        if part.startswith("<details>"): continue
        part = re.sub(r"<h2>(.*?)</h2>", h2, part, flags=re.S)
        parts[k] = re.sub(r"<h3>(.*?)</h3>", h3, part, flags=re.S)
    head = "".join(parts)
    esc = lambda t: html.escape(t, quote=False)
    li = ""
    for i, label, subs in items:
        li += f'          <li><a href="#{i}">{esc(label)}</a>'
        if subs:
            li += ("\n            <ol class=\"toc__many\">\n" if len(subs) >= 6 else "\n            <ol>\n") + "".join(f'              <li><a href="#{j}">{esc(t)}</a></li>\n' for j, t in subs) + "            </ol>\n          "
        li += "</li>\n"
    toc = (f'      <nav class="toc" aria-label="{LABEL[lang]}">\n        <p class="toc__title">{TITLE[lang]}</p>\n'
           f'        <ol>\n{li}        </ol>\n      </nav>\n\n')
    m = re.search(r'<p class="lead">.*?</p>\n\n', head, re.S)
    assert m, (path, "kein lead-Absatz")
    head = head[:m.end()] + toc + head[m.end():]
    assert s.count("    .lead {") == 1 or "    .lead{" in s, (path, "CSS-Anker")
    anchor = "    .lead {" if "    .lead {" in head else "    .lead{"
    head = head.replace(anchor, CSS + anchor, 1)
    io.open(path, "w", encoding="utf-8").write(head + sep + tail)
    return f"{len(items)} Abschnitte, {sum(len(x[2]) for x in items)} Unterpunkte"

if __name__ == "__main__":
    for lang, files in PAGES.items():
        for f in files:
            print(f"  {f:<42} {build(f, lang)}")
