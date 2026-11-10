# Combat Coach – Website

Statische Website von **Combat Coach** (Boxen, Kickboxen, Muay Thai), live auf https://combatcoach.org
(GitHub Pages, Branch `main`, Push = live). Zweisprachig: Deutsch im Root, Englisch unter `/en/`.
Dunkles Hochkontrast-Design passend zur App (Rot `#E42B24`, Creme `#FFFDE4`, Schwarz).

- **Neu auf einem Rechner?** → `HANDOVER.md` (Setup, Stand, Erkenntnisse, offene Aufgaben)
- **Arbeitsregeln für Claude Code** → `CLAUDE.md`

## Technik in Kürze

- Kein Build-Schritt, kein Framework; CSS inline pro Seite.
- Schrift Roboto Mono lokal in `fonts/`, keine Drittanbieter-Requests (Ausnahme: Formspree für die Warteliste).
- SEO: `canonical`, `hreflang` (DE/EN), JSON-LD, `sitemap.xml`, `robots.txt`, `llms.txt`.
- Lokale Vorschau: `python3 -m http.server 8766` im Repo-Root.

## Werkzeuge (`tools/`)

Reproduzierbare Helfer, nicht Teil der Website (per `robots.txt` von der Indexierung ausgenommen). Aufruf jeweils aus dem Repo-Root:

| Skript | Zweck |
|---|---|
| `tools/optimize_images.py` | erzeugt WebP-Screenshots und das 128-px-Logo aus den PNG-Originalen (nur Pillow) |
| `tools/add_toc.py` | Inhaltsverzeichnis mit Sprungmarken in den Ratgeberseiten (idempotent) |
| `tools/gen_timer_formats.py` | erzeugt die Format-Timer (Muay Thai, MMA, Tabata; DE+EN) aus den Basis-Timern — überschreibt die Zielseiten |
| `tools/update_sitemap.py` | setzt `lastmod` in `sitemap.xml` aus dem Git-Verlauf |
