# Combat Coach – Website (combatcoach.org)

Statische Website auf **GitHub Pages** (Repo `skoenig126-dotcom/combatcoach-website`, Branch `main`, Push = live).
**Zuerst `HANDOVER.md` lesen** — dort stehen Stand, Erkenntnisse, Entscheidungen und offene Aufgaben.

## Harte Regeln
- Immer **zweisprachig**: jede Änderung in DE **und** EN (DE liegt im Root, EN unter `/en/`).
- **Kein Build-Schritt**, kein Framework. Jede Seite hat ihr CSS inline.
- **Keine Drittanbieter-Requests** (keine Google Fonts, keine CDNs, keine Tracker). Schrift liegt lokal in `/fonts`. Einzige Ausnahme: Formspree (Warteliste) — im Datenschutz dokumentiert.
- **Der Klarname des Gründers erscheint nicht im sichtbaren Text** (nur in JSON-LD und im Impressum `legal.html`). Rollenbezeichnung verwenden („Gründer & Entwickler").
- **Kein konkretes Launch-Datum** auf der Seite, solange der Store-Termin nicht feststeht („Bald verfügbar" / „Coming soon"). Kein `releasedEvent` im Schema.
- **Nie DNS-Einträge für Mail anfassen** (MX/SPF/DKIM). DNS pflegt der Nutzer bei IONOS selbst.
- Impressum-Daten stehen nur in `legal.html` — nicht duplizieren oder ändern ohne Auftrag.
- Keine erfundenen Qualifikationen, Zahlen oder Zertifikate. Aussagen zum Gründer nur aus `HANDOVER.md` (10+ Jahre Kampfsport, Schwerpunkt Muay Thai).
- Daten aus der Search Console sind **Messwerte, keine Zusagen** — nie Rankings versprechen.

## Qualitäts-Checkliste vor jedem Push
- `<title>` ≤ 60 Zeichen, Meta-Description ≤ 160, `&` im Title als `&amp;`.
- JSON-LD parsebar; FAQPage-Fragen stehen wörtlich sichtbar auf der Seite.
- hreflang reziprok (DE ↔ EN, plus `x-default` = DE-Seite); jede Seite hat `canonical`.
- Neue Seite → in `sitemap.xml` (beide Sprachen, mit `xhtml:link`) und im Ratgeber-Hub (`ratgeber.html` / `en/guides.html`).
- Interne Links **absolut** (`/en/...`), nie relativ — relative Links in `/en/` zeigen sonst auf nicht vorhandene Seiten (das hat bereits einen 404 in der Search Console verursacht).
- Startseiten (`index.html`, `en/index.html`): jeder `data-i18n`-Schlüssel muss in **beiden** Wörterbüchern stehen; JS-Syntax mit `node --check` prüfen. Das Skript überschreibt beim Laden den Markup-Text aus dem Wörterbuch — Änderungen immer in **Markup und Wörterbuch** machen.
- Nach dem Push: Pages-Build abwarten (`gh api repos/skoenig126-dotcom/combatcoach-website/pages/builds/latest`) und die Live-URL per `curl` prüfen.

## Arbeitsweise
- Commit-Nachrichten über eine UTF-8-Datei schreiben (`git commit -F datei`) — Umlaute/ß in Heredocs wurden schon verstümmelt. Trailer wie in der aktuellen Claude-Code-Vorgabe.
- Größere HTML-Änderungen per Python-Skript mit Assertions (Anzahl der Treffer prüfen), nicht per fehleranfälligem Mehrfach-Edit. Vorsicht bei Mehrfachtreffern: ein Einfüge-Skript hat schon einmal den falschen von zwei gleichen Links getroffen.
- Lokale Vorschau: `python3 -m http.server 8766` im Repo-Root. Browser-Cache kann alte Fassungen liefern (`fetch(url,{cache:'reload'})` bzw. Hard-Reload).
- Hilfsskripte in `tools/` (siehe README).
