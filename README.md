# Combat Coach – Website

Marketing landing page for the **Combat Coach** app — your smart martial arts workout pal
(Muay Thai, Kickboxing, Boxing).

Static site, no build step. Dark, high-contrast brand design matching the app
(red `#E42B24`, cream `#FFFDE4`, black background).

## Structure

| File | Purpose |
|------|---------|
| `index.html` | Landing page (hero, features, CTA, footer) |
| `privacy.html` | Privacy Policy |
| `legal.html` | Terms of Use (`#terms`) + Legal Notice / Imprint (`#imprint`) |
| `CombatCoach_Avata_Logo.png` | Boxer avatar logo |
| `Combat_Coach_FontLogo.png` | "Combat Coach" wordmark logo |

All links are relative — open `index.html` in a browser or serve the folder as-is.

## Fonts & images

- Fonts loaded from Google Fonts (Anton, Montserrat, Inter).
- Hero/showcase photos hotlinked from [Pexels](https://www.pexels.com) (free license; credited in the footer).

## Deployment (GitHub Pages)

1. Push to GitHub.
2. **Settings → Pages → Build and deployment → Branch: `main` / root**.
3. Optionally set a custom domain (`combatcoach.org`) under the same page.

## License

© Combat Coach. All rights reserved.

## Werkzeuge (`tools/`)

Reproduzierbare Helfer, nicht Teil der Website (per `robots.txt` von der Indexierung ausgenommen). Aufruf jeweils aus dem Repo-Root:

| Skript | Zweck |
|---|---|
| `tools/optimize_images.py` | erzeugt WebP-Screenshots und das 128-px-Logo aus den PNG-Originalen (nur Pillow) |
| `tools/add_toc.py` | Inhaltsverzeichnis mit Sprungmarken in den Ratgeberseiten (idempotent) |
| `tools/gen_timer_formats.py` | erzeugt die Format-Timer (Muay Thai, MMA, Tabata; DE+EN) aus den Basis-Timern — überschreibt die Zielseiten |
| `tools/update_sitemap.py` | setzt `lastmod` in `sitemap.xml` aus dem Git-Verlauf |
