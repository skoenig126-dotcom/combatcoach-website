# Übergabe: Combat-Coach-Website

Stand: 10.11.2026 · Live: https://combatcoach.org · Repo: https://github.com/skoenig126-dotcom/combatcoach-website

## 1. Setup auf einem neuen Rechner (z. B. MacBook)

```bash
# 1. Werkzeuge (einmalig)
brew install git gh node python3
gh auth login                      # GitHub, HTTPS, Browser-Login
git config --global user.name  "<Name>"
git config --global user.email "<E-Mail>"

# 2. Repo holen — in einen EIGENEN Ordner, nie in einen Sammelordner mit anderen Dateien
mkdir -p ~/Projects && cd ~/Projects
gh repo clone skoenig126-dotcom/combatcoach-website
cd combatcoach-website

# 3. Optional für tools/ (nur Bildkonvertierung braucht es)
python3 -m pip install pillow

# 4. Lokale Vorschau
python3 -m http.server 8766        # → http://localhost:8766

# 5. Claude Code im Projektordner starten — liest CLAUDE.md automatisch
claude
```

Veröffentlichen = `git push origin main`. GitHub Pages baut automatisch (1–2 Min). **Vor jeder Arbeit `git pull`** (zwischendurch haben andere Sitzungen gepusht).

**Nicht mitgenommen und neu aufzubauen:** Claudes Gedächtnis (liegt lokal pro Rechner), die Sitzungs-Skripte aus dem Chat (relevante liegen jetzt in `tools/`), Blender- und FlutterFlow-Projekte (separat, nicht Teil dieses Repos).

## 2. Aufbau

| Bereich | Dateien |
|---|---|
| Startseiten | `index.html` (DE), `en/index.html` (EN) — Wörterbuch-i18n, EN-Text ist in die EN-Seite eingebacken |
| Ratgeber (je DE + EN) | `boxen-alleine-trainieren` / `train-boxing-alone`, `boxsack-training-anfaenger` / `heavy-bag-training-beginners`, `schattenboxen-kombinationen` / `shadowboxing-combinations`, `kickboxen-training` / `kickboxing-training`, `muay-thai-training` / `muay-thai-training` |
| Timer (je DE + EN) | `box-timer` / `boxing-timer`, `muay-thai-timer`, `mma-timer`, `tabata-timer` (EN unter `/en/`) |
| Sonstiges | `ratgeber.html` / `en/guides.html` (Hub), `ueber-uns.html` / `en/about.html`, `privacy.html` (clientseitig DE/EN), `legal.html` (Impressum + Nutzungsbedingungen) |
| Technik | `sitemap.xml`, `robots.txt`, `llms.txt`, `CNAME`, `.nojekyll`, `fonts/`, `assets/`, `screenshots/` (PNG-Originale + ausgelieferte WebP), `og-image.png`, `reveal.html` (Intro-Animation, per robots gesperrt) |
| Werkzeuge | `tools/optimize_images.py`, `add_toc.py`, `gen_timer_formats.py` (überschreibt die 6 Format-Timer-Seiten!), `update_sitemap.py` |

Seitenpaare sind **statische Einzeldateien je Sprache** (außer den Startseiten). Der Sprachumschalter navigiert zwischen den URLs; `localStorage cc_lang` merkt die Wahl (nur `privacy.html` schaltet clientseitig).

Hosting/DNS: GitHub Pages, Custom Domain `combatcoach.org` (Datei `CNAME`), HTTPS erzwungen. DNS bei IONOS: Apex und `www` → GitHub-IPs `185.199.108–111.153`. **Mail-Einträge nie anfassen.** `privacy.combatcoach.org` und `legal.combatcoach.org` haben keine DNS-Einträge mehr (tot).

## 3. Entscheidungen und Fakten

- **Design:** dunkel, Rot `#E42B24`, Creme `#FFFDE4`, Schwarz `#050505`, Schrift Roboto Mono (lokal, Variable Font `fonts/`), Logos `CombatCoach_Avata_Logo.png` / `Combat_Coach_FontLogo.png`.
- **Positionierung:** „Von Kampfsportlern. Für Kampfsportler." App nicht nur für Anfänger, sondern auch Fortgeschrittene, Profis, Coaches (Pläne erstellen/managen, Timer teilen).
- **Gründer-Story:** seit über 10 Jahren im Kampfsport, aktuell Schwerpunkt Muay Thai, dazu Boxen/Kickboxen. Name nur in JSON-LD, nicht sichtbar.
- **Kontakt:** info@combatcoach.org · Instagram `combat.coach_app` · Bluesky `combatcoach.bsky.social`. Postanschrift nur im Impressum.
- **Warteliste:** Formular im CTA beider Startseiten → Formspree `https://formspree.io/f/maeyrnnj` (Konstante `WAITLIST_ENDPOINT` am Ende der Startseiten-Skripte). Einwilligungshinweis am Formular, Abschnitt 4 in `privacy.html`. Die Datenschutz-Zusage „Löschung nach der Start-Mail" ist vom Betreiber zu bestätigen.
- **Launch-Wortlaut:** datumsneutral („Bald verfügbar"/„Coming soon"). Store-Buttons zeigen noch auf `#`. Sobald die App im Store ist: Buttons verlinken, Texte auf „Jetzt verfügbar" umstellen.
- **Intro (`reveal.html`):** läuft nur bei Direktaufruf ohne Referrer, einmal pro Sitzung (Besucher aus Google sehen sofort Inhalt).
- **Timer:** Browser-only (Web Audio, Web Speech, Wake Lock). Voreinstellung per URL (`?rounds=5&round=180&rest=120&prep=10&sport=muaythai&caller=on&speed=7`), „Link teilen"-Button. Schleife über `setInterval` (nicht `requestAnimationFrame` — das hält in Hintergrund-Tabs an).

## 4. SEO-Erkenntnisse (Search Console, Stand 23./26.10.2026)

- 3 Monate: 93 Klicks, 3.792 Impressionen, Ø-Position von ~21 auf ~10 gestiegen. Mobil 59 % der Impressionen und viel besser (Pos. 9,4) als Desktop (22,8). Deutschland ~41 % der Impressionen, USA/UK zusammen ~25 %.
- Wichtigste Seiten: `/en/` (28 Klicks, Pos. 7), Schattenboxen-DE (23 Klicks), `boxen-alleine-trainieren` (9). Größte ungenutzte Fläche: EN Heavy-Bag-Cluster (~700 Impressionen, Pos. ~29, fast keine Klicks).
- Beste Einzelanfrage: „schattenboxen für anfänger" (106 Impr., Pos. 8,9). Timer-Seiten haben hohe Klickrate (9 %), stehen aber schlecht.
- Wirksame Hebel bisher: Titel in der echten Suchsprache („drills", „Boxsack-Training", „für Anfänger", „combos"), eigene Seiten je Suchintention, FAQ passend zu belegten Anfragen, Inhaltsverzeichnis mit Sprungmarken.
- **FAQ-Rich-Snippets erscheinen nicht** (Google zeigt sie seit 2023 praktisch nur Behörden/Gesundheit) — FAQ bleibt trotzdem als Inhalt sinnvoll.
- Ignorieren: „schattenboxen rätsel", „chinesisches schattenboxen" (Kreuzworträtsel/Tai Chi), „coach a fighter calculator" (fremdes Produkt).
- Indexierungsbericht: 19 indexiert, 8 nicht — alle erklärbar (http/www-Weiterleitungen, `/index.html`-Duplikat, tote Subdomains, `privacy.html` noch nicht gecrawlt). Der einzige echte Fehler (`/en/boxen-alleine-trainieren.html`, 404) ist behoben.
- Marke „combat coach" Pos. ~4, CTR niedrig; hilft nur externe Reichweite (Instagram, Store-Eintrag, Erwähnungen), kein weiterer Code.
- Search-Console-Zugriff ging über „Claude in Chrome" im eingeloggten Browser (Sitemap einreichen, URL-Prüfung → „Indexierung beantragen", ~10/Tag). Eingereicht: Sitemap am 25.10., Indexierung für `muay-thai-timer`, `mma-timer`, `ratgeber`.

## 5. Offene Aufgaben (nach Priorität)

1. **Store-Release nachziehen:** Datum/„Jetzt verfügbar", echte Store-Links in den Buttons (beide Startseiten, `cta`), Schema ggf. wieder mit `releasedEvent`.
2. **Datenschutz-URL in App Store Connect / Google Play** muss `https://combatcoach.org/privacy.html` sein (alte Subdomains tot). Optional IONOS-Weiterleitung der Subdomains.
3. **Formspree:** Auftragsverarbeitungsvertrag abschließen, Eingänge prüfen; Datenschutz-Abschnitt 4 vom Betreiber prüfen lassen.
4. **Search Console:** Indexierung beantragen für `/privacy.html`, `/tabata-timer.html`, englische Seiten; nach 2–4 Wochen Daten erneut auswerten (Export „Leistung" + „Seiten") und Titel/Inhalte nachziehen.
5. **App-Screens einbauen:** zwei neue Screens (Drills, Digital Sparring) als WebP in Telefonrahmen; die Platzhalter „Screenshot folgt" (Combat Camp, KI-Plan) warten auf Bilder (`screenshots/combat_camp`, `ai_plan`; `python3 tools/optimize_images.py`).
6. **Ideen, noch offen:** installierbare Timer-PWA (Manifest + vorsichtiger Service Worker, offline im Gym); Technik-Grafiken aus den Blender-Animationen für die Ratgeber (Schlagnummern-System); weitere Ratgeber nach Suchdaten (z. B. „Kickbox-Kombinationen"); Backlinks/Reichweite.

## 6. Gelernte Stolpersteine

- Startseiten: Markup **und** Wörterbuch pflegen (siehe `CLAUDE.md`); relative Links im Wörterbuch → 404 auf `/en/`.
- Einfüge-Skripte mit `str.replace`/Regex: Trefferzahl asserten; gleiche Links kommen mehrfach vor (Byline vs. Footer).
- `.format()` mit Dict-Schlüsseln und lokalen Variablen kollidiert → Namen trennen.
- GitHub Pages: nach dem Push ist der Build für den **neuen** Commit abzuwarten, vorher zeigt `built` noch den alten. Remote-Commits durch Pages-Toggles → `git pull --rebase`.
- PageSpeed-API ohne Key hat kein nutzbares Kontingent; stattdessen Gewicht/Hosts statisch prüfen.
- Vorschau-Browser cached hartnäckig; Test mit `cache:'reload'`.
- Screenshot-Pane hinkt beim Scrollen hinterher — Werte per JS auslesen.
