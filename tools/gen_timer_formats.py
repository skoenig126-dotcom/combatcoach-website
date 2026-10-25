#!/usr/bin/env python3
"""Erzeugt die Format-Seiten des Timers (Muay Thai, MMA, Tabata; DE + EN).

Basis sind die fertigen Seiten box-timer.html / en/boxing-timer.html - Footer, Logo, Schrift, Teilen-Link und
Timer-Logik kommen unveraendert von dort. Pro Format wird nur ersetzt: Meta, Schema, H1, Voreinstellung (data-preset),
Vorlagen-Buttons und der Inhalt zwischen Timer und CTA-Box.

ACHTUNG: Ueberschreibt die Zielseiten. Handaenderungen an den Format-Seiten gehen verloren - Inhalte hier pflegen.
Aufruf aus dem Repo-Root:  python3 tools/gen_timer_formats.py
"""
import html, io, json, re

BASE = {"de": "box-timer.html", "en": "en/boxing-timer.html"}
HOME = {"de": "/", "en": "/en/"}
LBL = {
  "de": dict(related="Weiterlesen:", faq="Häufige Fragen", sep=" · "),
  "en": dict(related="Read next:", faq="Frequently asked questions", sep=" · "),
}

TABLE_CSS = """    .workout{width:100%;border-collapse:collapse;margin:1.4rem 0 2rem;font-size:.9rem}
    .workout th,.workout td{text-align:left;padding:.7rem .9rem;border-bottom:1px solid var(--border);color:var(--cream-dim);vertical-align:top}
    .workout th{color:var(--cream);font-size:.78rem;letter-spacing:.08em;text-transform:uppercase}
    .workout td:first-child{color:var(--red);font-weight:600}
"""

# ---------------------------------------------------------------------------------------------------------------
FORMATS = [
 # ============================ MUAY THAI ============================
 dict(
  key="muaythai",
  de=dict(
   slug="muay-thai-timer.html", crumb="Muay-Thai-Timer",
   title="Muay-Thai-Timer: 5×3 Minuten mit Combo-Ansage (gratis)",
   desc="Kostenloser Muay-Thai-Timer: 5 Runden à 3 Minuten, 2 Minuten Pause – mit Combo-Ansage für Teep, Low Kick, Ellbogen und Knie. Direkt im Browser.",
   ogdesc="Kostenloser Muay-Thai-Timer mit 5×3-Minuten-Runden und Combo-Ansage. Ohne Anmeldung, direkt im Browser.",
   h1=("Muay-Thai-Timer mit ", "5×3-Minuten-Runden", ""),
   lead="Fünf Runden à drei Minuten, zwei Minuten Pause: So wird in Thailand gekämpft, und so trainierst du hier. Der Timer ist bereits eingestellt — die Combo-Ansage ruft dir Muay-Thai-Kombinationen mit Teep, Ellbogen und Knie zu. Kostenlos, ohne Anmeldung.",
   preset=dict(rounds=5, round=180, rest=120, prep=10, sport="muaythai", caller="on", speed=7),
   buttons=[("Profi 5×3 · 2 Min Pause", 5, 180, 120), ("Einsteiger 3×3 · 1 Min", 3, 180, 60), ("Technik 5×2 · 1 Min", 5, 120, 60)],
   h2_formats="Die Rundenformate im Muay Thai",
   intro="Muay Thai kennt ein festes Profiformat. Das Training orientiert sich daran, damit sich Tempo, Atmung und Pausen im Kampf vertraut anfühlen.",
   head=("Einsatz", "Format", "Pause"),
   rows=[("Profikampf (Thailand-Regeln)", "5 Runden à 3 Min", "2 Min"),
         ("Amateurkampf", "häufig 3 Runden à 3 Min", "ca. 1 Min – je nach Verband"),
         ("Training im Gym (Pads, Sack)", "5 Runden à 3 Min", "1–2 Min"),
         ("Einsteiger &amp; Technik", "3–5 Runden à 2 Min", "1 Min")],
   h2_train="So trainierst du mit dem Muay-Thai-Timer",
   train=["<strong>Pad- und Sackrunden (5×3)</strong> — pro Runde ein Schwerpunkt: Teep und Low Kick, Ellbogen und Knie, Clinch-Arbeit am Sack, freie Runde.",
          "<strong>Technikrunden (5×2)</strong> — dieselbe Technik eine Runde lang, erst sauber und langsam, dann schneller. Die Combo-Ansage kannst du dabei ausschalten.",
          "<strong>Finisher</strong> — nach den Runden ein <a href=\"/tabata-timer.html\">Tabata-Block</a> mit Knien und Schlagserien.",
          "<strong>Training im Team</strong> — mit „Link teilen“ schickst du den eingestellten Timer an deine Trainingsgruppe."],
   related=[("/muay-thai-training.html", "Muay Thai lernen"), ("/box-timer.html", "Box-Timer"), ("/tabata-timer.html", "Tabata-Timer")],
   faq=[("Wie lange dauert eine Runde im Muay Thai?",
         "Im Profikampf nach Thailand-Regeln dauert eine Runde 3 Minuten, gekämpft werden fünf Runden mit je 2 Minuten Pause. Im Amateurbereich sind kürzere Formate wie 3 × 3 Minuten üblich; die Details hängen vom Verband ab."),
        ("Welche Pause ist im Muay Thai üblich?",
         "Im Profibereich 2 Minuten. Im Training sind 1 bis 2 Minuten üblich: Kürzere Pausen steigern die Intensität, längere geben Raum für Technikkorrekturen."),
        ("Wie funktioniert die Combo-Ansage im Muay-Thai-Modus?",
         "Der Timer wählt im eingestellten Abstand zufällig eine Kombination aus dem Muay-Thai-Pool — darunter Teep, Low Kick, Ellbogen und Knie — und spricht sie aus. Sie erscheint zusätzlich groß im Display."),
        ("Kann ich den Timer im Gym auf dem Handy nutzen?",
         "Ja. Solange der Timer läuft, hält die Seite den Bildschirm wach, sofern dein Browser das erlaubt. Stell die Lautstärke so ein, dass du den Gong am Sack hörst.")]),
  en=dict(
   slug="en/muay-thai-timer.html", crumb="Muay Thai timer",
   title="Muay Thai Timer: 5×3 Rounds with Combo Callouts (Free)",
   desc="Free Muay Thai timer: 5 rounds of 3 minutes with 2 minutes rest — plus combo callouts for teeps, low kicks, elbows and knees. Runs in your browser.",
   ogdesc="Free Muay Thai timer with 5×3-minute rounds and combo callouts. No sign-up, runs in your browser.",
   h1=("Muay Thai timer with ", "5×3 minute rounds", ""),
   lead="Five rounds of three minutes with two minutes of rest: that is how it is fought in Thailand, and how you train here. The timer is already set up — the combo callouts shout Muay Thai combinations with teeps, elbows and knees at you. Free, no sign-up.",
   preset=dict(rounds=5, round=180, rest=120, prep=10, sport="muaythai", caller="on", speed=7),
   buttons=[("Pro 5×3 · 2 min rest", 5, 180, 120), ("Beginner 3×3 · 1 min", 3, 180, 60), ("Technique 5×2 · 1 min", 5, 120, 60)],
   h2_formats="Round formats in Muay Thai",
   intro="Muay Thai has a fixed professional format. Training follows it so pace, breathing and rest feel familiar when it counts.",
   head=("Use", "Format", "Rest"),
   rows=[("Pro fight (Thai rules)", "5 rounds × 3 min", "2 min"),
         ("Amateur fight", "often 3 rounds × 3 min", "about 1 min – depends on the federation"),
         ("Gym training (pads, bag)", "5 rounds × 3 min", "1–2 min"),
         ("Beginners &amp; technique", "3–5 rounds × 2 min", "1 min")],
   h2_train="How to train with the Muay Thai timer",
   train=["<strong>Pad and bag rounds (5×3)</strong> — one focus per round: teep and low kick, elbows and knees, clinch work on the bag, a free round.",
          "<strong>Technique rounds (5×2)</strong> — the same technique for a whole round, clean and slow first, then faster. You can switch the combo callouts off for these.",
          "<strong>Finisher</strong> — after the rounds, a <a href=\"/en/tabata-timer.html\">Tabata block</a> with knees and punch flurries.",
          "<strong>Training as a team</strong> — “Share link” sends the configured timer to your training group."],
   related=[("/en/muay-thai-training.html", "Muay Thai for beginners"), ("/en/boxing-timer.html", "Boxing timer"), ("/en/tabata-timer.html", "Tabata timer")],
   faq=[("How long is a round in Muay Thai?",
         "In a professional fight under Thai rules a round lasts 3 minutes, and five rounds are fought with 2 minutes of rest. Amateur bouts often use shorter formats such as 3 × 3 minutes; details depend on the federation."),
        ("What rest period is normal in Muay Thai?",
         "Two minutes in professional fights. In training, 1 to 2 minutes is common: shorter rest raises intensity, longer rest leaves room for technique corrections."),
        ("How do the combo callouts work in Muay Thai mode?",
         "At the interval you set, the timer picks a random combination from the Muay Thai pool — including teeps, low kicks, elbows and knees — and speaks it. It also appears in large type on the display."),
        ("Can I use the timer on my phone in the gym?",
         "Yes. While the timer runs, the page keeps your screen awake where your browser allows it. Set the volume so you can hear the bell at the bag.")]),
 ),
 # ============================ MMA ============================
 dict(
  key="mma",
  de=dict(
   slug="mma-timer.html", crumb="MMA-Timer",
   title="MMA-Timer: 3×5 und 5×5 Minuten Rundentimer (gratis)",
   desc="Kostenloser MMA-Timer: 3×5 oder 5×5 Minuten mit 1 Minute Pause wie im Käfig – plus Combo-Ansage für Striking-Runden. Direkt im Browser, ohne Anmeldung.",
   ogdesc="Kostenloser MMA-Rundentimer für 3×5 und 5×5 Minuten, mit Combo-Ansage für Striking. Ohne Anmeldung.",
   h1=("MMA-Timer für ", "3×5 und 5×5 Minuten", ""),
   lead="Drei Runden à fünf Minuten, bei Titelkämpfen und Main Events fünf Runden, dazwischen eine Minute Pause: Das ist das Format der großen Ligen. Der Timer bildet es nach — dazu eine Combo-Ansage für deine Striking-Runden. Kostenlos, ohne Anmeldung.",
   preset=dict(rounds=3, round=300, rest=60, prep=10, sport="kickboxing", caller="on", speed=6),
   buttons=[("Profi 3×5", 3, 300, 60), ("Titelkampf 5×5", 5, 300, 60), ("Amateur 3×3", 3, 180, 60)],
   h2_formats="Die Rundenformate im MMA",
   intro="Im MMA gelten je nach Veranstalter unterschiedliche Regeln. Die großen Ligen arbeiten nach den Unified Rules; wer sich auf einen Kampf vorbereitet, trainiert im selben Takt.",
   head=("Einsatz", "Format", "Pause"),
   rows=[("Profikampf (Unified Rules)", "3 Runden à 5 Min", "1 Min"),
         ("Titelkämpfe &amp; Main Events", "5 Runden à 5 Min", "1 Min"),
         ("Amateur-MMA", "häufig 3 Runden à 3 Min – je nach Veranstalter", "1 Min"),
         ("Training &amp; Sparring", "3–5 Runden à 3–5 Min", "1 Min")],
   h2_train="So trainierst du mit dem MMA-Timer",
   train=["<strong>Striking-Runden</strong> — Combo-Ansage an, Tempo 5–6 Sekunden: Kombinationen aus Boxen und Kicks, ohne nachzudenken.",
          "<strong>Grappling-Runden</strong> — Combo-Ansage aus; der Timer gibt nur Rundenstart, Ende und Pausen vor, etwa für 5-Minuten-Rolls.",
          "<strong>Gemischte Einheiten</strong> — eine Runde Striking, eine Runde Takedowns, eine Runde Bodenarbeit; der Gong trennt die Blöcke.",
          "<strong>Wettkampfsimulation</strong> — 3×5 mit 10 Sekunden Vorbereitung und ohne Zwischenstopps, so wie im Käfig.",
          "<strong>Wichtig zur Ansage</strong> — sie nutzt Kickbox-Kombinationen und deckt Striking ab, nicht Takedowns oder Bodenarbeit."],
   related=[("/kickboxen-training.html", "Kickboxen für Anfänger"), ("/box-timer.html", "Box-Timer"), ("/muay-thai-timer.html", "Muay-Thai-Timer")],
   faq=[("Wie lange ist eine MMA-Runde?",
         "Bei Profikämpfen nach den Unified Rules dauert eine Runde 5 Minuten, dazwischen gibt es 1 Minute Pause. Im Amateurbereich sind kürzere Runden von etwa 3 Minuten üblich."),
        ("Wie viele Runden hat ein MMA-Kampf?",
         "In der Regel drei. Titelkämpfe und Main Events gehen über fünf Runden."),
        ("Passt die Combo-Ansage zu MMA?",
         "Sie nutzt Kickbox-Kombinationen und eignet sich damit für Striking-Runden. Takedowns und Bodenarbeit deckt sie nicht ab — dafür schaltest du sie aus und nutzt den Timer nur als Rundenuhr."),
        ("Kann ich den Timer für Grappling und BJJ nutzen?",
         "Ja, als reine Rundenuhr: Combo-Ansage ausschalten, Rundenlänge und Pause einstellen — etwa 5 Minuten Rolling mit 1 Minute Pause.")]),
  en=dict(
   slug="en/mma-timer.html", crumb="MMA timer",
   title="MMA Timer: 3×5 and 5×5 Minute Round Timer (Free)",
   desc="Free MMA timer: 3×5 or 5×5 minutes with 1 minute rest like in the cage — plus combo callouts for striking rounds. In your browser, no sign-up.",
   ogdesc="Free MMA round timer for 3×5 and 5×5 minutes, with combo callouts for striking. No sign-up.",
   h1=("MMA timer for ", "3×5 and 5×5 minutes", ""),
   lead="Three rounds of five minutes, five rounds for title fights and main events, one minute of rest in between: that is the format of the major promotions. The timer recreates it — plus combo callouts for your striking rounds. Free, no sign-up.",
   preset=dict(rounds=3, round=300, rest=60, prep=10, sport="kickboxing", caller="on", speed=6),
   buttons=[("Pro 3×5", 3, 300, 60), ("Title fight 5×5", 5, 300, 60), ("Amateur 3×3", 3, 180, 60)],
   h2_formats="Round formats in MMA",
   intro="MMA rules differ by promotion. The major organisations work under the Unified Rules; if you are preparing for a fight, train at the same rhythm.",
   head=("Use", "Format", "Rest"),
   rows=[("Pro fight (Unified Rules)", "3 rounds × 5 min", "1 min"),
         ("Title fights &amp; main events", "5 rounds × 5 min", "1 min"),
         ("Amateur MMA", "often 3 rounds × 3 min – depends on the organiser", "1 min"),
         ("Training &amp; sparring", "3–5 rounds × 3–5 min", "1 min")],
   h2_train="How to train with the MMA timer",
   train=["<strong>Striking rounds</strong> — callouts on, pace 5–6 seconds: boxing and kick combinations without thinking.",
          "<strong>Grappling rounds</strong> — callouts off; the timer only marks round start, end and rest, for example for 5-minute rolls.",
          "<strong>Mixed sessions</strong> — one round of striking, one of takedowns, one of ground work; the bell separates the blocks.",
          "<strong>Fight simulation</strong> — 3×5 with 10 seconds of preparation and no stops, just like in the cage.",
          "<strong>Note on the callouts</strong> — they use kickboxing combinations and cover striking, not takedowns or ground work."],
   related=[("/en/kickboxing-training.html", "Kickboxing for beginners"), ("/en/boxing-timer.html", "Boxing timer"), ("/en/muay-thai-timer.html", "Muay Thai timer")],
   faq=[("How long is an MMA round?",
         "In professional fights under the Unified Rules a round lasts 5 minutes with 1 minute of rest in between. Amateur bouts commonly use shorter rounds of around 3 minutes."),
        ("How many rounds does an MMA fight have?",
         "Usually three. Title fights and main events go five rounds."),
        ("Do the combo callouts work for MMA?",
         "They use kickboxing combinations, which suits striking rounds. They do not cover takedowns or ground work — for those, switch them off and use the timer as a plain round clock."),
        ("Can I use the timer for grappling and BJJ?",
         "Yes, as a plain round clock: switch the callouts off and set round length and rest — for example 5 minutes of rolling with 1 minute of rest.")]),
 ),
 # ============================ TABATA ============================
 dict(
  key="tabata",
  de=dict(
   slug="tabata-timer.html", crumb="Tabata-Timer",
   title="Tabata-Timer: 8×20 Sek. Belastung, 10 Sek. Pause (gratis)",
   desc="Kostenloser Tabata-Timer: 8 Runden à 20 Sekunden Belastung und 10 Sekunden Pause – mit Gong und optionaler Combo-Ansage für Schlagserien. Im Browser.",
   ogdesc="Kostenloser Tabata-Timer mit 20/10-Intervallen, Gong und optionaler Combo-Ansage. Ohne Anmeldung.",
   h1=("Tabata-Timer mit ", "20/10-Intervallen", ""),
   lead="Acht Runden, 20 Sekunden alles geben, 10 Sekunden Pause: vier Minuten, die es in sich haben. Der Timer ist auf das klassische Tabata-Protokoll eingestellt; für Kampfsportler gibt es optional eine Combo-Ansage, die dir Schlagserien zuruft. Kostenlos, ohne Anmeldung.",
   preset=dict(rounds=8, round=20, rest=10, prep=10, sport="boxing", caller="on", speed=4),
   buttons=[("Klassisch 8×20/10", 8, 20, 10), ("Doppelt 16×20/10", 16, 20, 10), ("Einsteiger 8×20/20", 8, 20, 20)],
   h2_formats="Das Tabata-Protokoll",
   intro="Das Protokoll geht auf den japanischen Forscher Izumi Tabata zurück, der Intervalle aus 20 Sekunden maximaler Belastung und 10 Sekunden Pause in den 1990er-Jahren untersuchte. Entscheidend ist, dass die 20 Sekunden wirklich hart sind — sonst ist es ein gewöhnlicher Intervall.",
   head=("Variante", "Aufbau", "Dauer"),
   rows=[("Klassisch", "8 × 20 Sek. Belastung / 10 Sek. Pause", "ca. 4 Min"),
         ("Doppelt", "16 × 20 Sek. Belastung / 10 Sek. Pause", "ca. 8 Min"),
         ("Einsteiger", "8 × 20 Sek. Belastung / 20 Sek. Pause", "ca. 5 Min")],
   h2_train="So nutzt du den Tabata-Timer im Kampfsport",
   train=["<strong>Finisher nach dem Sack</strong> — ein bis zwei Blöcke Schlagserien (Jab–Cross–Haken–Cross) bringen am Ende der Einheit Kondition unter Ermüdung.",
          "<strong>Ganzkörper-Blöcke</strong> — pro Block eine Übung: Burpees, Sprawls, Kniehebelauf oder Seilspringen.",
          "<strong>Aufwärmen nicht auslassen</strong> — Tabata startet bei hoher Intensität; vorher 5–10 Minuten locker bewegen.",
          "<strong>Pausen zwischen den Blöcken</strong> — eine Minute Pause, dann der nächste Block; mehr als zwei bis drei Blöcke pro Einheit sind für die meisten zu viel."],
   related=[("/boxsack-training-anfaenger.html", "Boxsack-Training für Anfänger"), ("/box-timer.html", "Box-Timer"), ("/muay-thai-timer.html", "Muay-Thai-Timer")],
   faq=[("Was ist Tabata?",
         "Ein Intervallprotokoll aus 8 Runden mit je 20 Sekunden maximaler Belastung und 10 Sekunden Pause — insgesamt etwa vier Minuten."),
        ("Wie oft pro Woche sollte ich Tabata trainieren?",
         "Wegen der hohen Intensität reichen für die meisten zwei bis drei Einheiten pro Woche mit Erholungstagen dazwischen. Das ist eine allgemeine Orientierung, keine individuelle Trainingsempfehlung."),
        ("Ist Tabata für Anfänger geeignet?",
         "Mit der Einsteiger-Variante (20 Sekunden Belastung, 20 Sekunden Pause) ja. Wer Vorerkrankungen hat oder lange nicht trainiert hat, klärt hochintensive Intervalle vorher ärztlich ab."),
        ("Welche Übungen eignen sich für Tabata im Kampfsport?",
         "Schlagserien am Sack, Burpees, Sprawls, Kniehebelauf, Seilspringen und Medizinball-Würfe. Wichtig ist, dass du in 20 Sekunden wirklich Vollgas geben kannst.")]),
  en=dict(
   slug="en/tabata-timer.html", crumb="Tabata timer",
   title="Tabata Timer: 8×20 Sec Work, 10 Sec Rest (Free)",
   desc="Free Tabata timer: 8 rounds of 20 seconds work and 10 seconds rest — with a bell and optional combo callouts for punch flurries. Runs in your browser.",
   ogdesc="Free Tabata timer with 20/10 intervals, a bell and optional combo callouts. No sign-up.",
   h1=("Tabata timer with ", "20/10 intervals", ""),
   lead="Eight rounds, 20 seconds all-out, 10 seconds rest: four minutes that are not a joke. The timer is set to the classic Tabata protocol; for fighters there is an optional combo caller that shouts punch flurries at you. Free, no sign-up.",
   preset=dict(rounds=8, round=20, rest=10, prep=10, sport="boxing", caller="on", speed=4),
   buttons=[("Classic 8×20/10", 8, 20, 10), ("Double 16×20/10", 16, 20, 10), ("Beginner 8×20/20", 8, 20, 20)],
   h2_formats="The Tabata protocol",
   intro="The protocol goes back to the Japanese researcher Izumi Tabata, who studied intervals of 20 seconds of maximal effort and 10 seconds of rest in the 1990s. What matters is that the 20 seconds are truly hard — otherwise it is just an ordinary interval.",
   head=("Variant", "Structure", "Duration"),
   rows=[("Classic", "8 × 20 sec work / 10 sec rest", "about 4 min"),
         ("Double", "16 × 20 sec work / 10 sec rest", "about 8 min"),
         ("Beginner", "8 × 20 sec work / 20 sec rest", "about 5 min")],
   h2_train="How to use the Tabata timer in fight sports",
   train=["<strong>Finisher after the bag</strong> — one or two blocks of punch flurries (jab–cross–hook–cross) build conditioning under fatigue at the end of a session.",
          "<strong>Full-body blocks</strong> — one exercise per block: burpees, sprawls, high knees or jump rope.",
          "<strong>Do not skip the warm-up</strong> — Tabata starts at high intensity; move easily for 5–10 minutes first.",
          "<strong>Rest between blocks</strong> — one minute, then the next block; more than two to three blocks per session is too much for most people."],
   related=[("/en/heavy-bag-training-beginners.html", "Heavy bag drills for beginners"), ("/en/boxing-timer.html", "Boxing timer"), ("/en/muay-thai-timer.html", "Muay Thai timer")],
   faq=[("What is Tabata?",
         "An interval protocol of 8 rounds, each with 20 seconds of maximal effort and 10 seconds of rest — about four minutes in total."),
        ("How often per week should I do Tabata?",
         "Because of the high intensity, two to three sessions per week with recovery days in between are enough for most people. This is a general guideline, not an individual training recommendation."),
        ("Is Tabata suitable for beginners?",
         "With the beginner variant (20 seconds work, 20 seconds rest) yes. If you have health conditions or have not trained for a long time, check high-intensity intervals with a doctor first."),
        ("Which exercises work for Tabata in fight sports?",
         "Punch flurries on the bag, burpees, sprawls, high knees, jump rope and medicine-ball throws. What matters is that you can truly go all-out for 20 seconds.")]),
 ),
]

# ---------------------------------------------------------------------------------------------------------------
def url_of(slug): return "https://combatcoach.org/" + slug

def build(lang, F, other_slug):
    base = io.open(BASE[lang], encoding="utf-8").read()
    s = base
    def sub1(pattern, repl, label, flags=re.S):
        nonlocal s
        s, n = re.subn(pattern, lambda m: repl, s, count=1, flags=flags)
        assert n == 1, (lang, F["slug"], label)
    assert len(F["desc"]) <= 160, (F["slug"], len(F["desc"]))
    de_url = url_of(F["slug"] if lang == "de" else other_slug)
    en_url = url_of(other_slug if lang == "de" else F["slug"])
    url = url_of(F["slug"])
    title_html = html.escape(F["title"], quote=False)

    sub1(r"<title>.*?</title>", f"<title>{title_html}</title>", "title")
    sub1(r'<meta name="description" content="[^"]*" />', f'<meta name="description" content="{html.escape(F["desc"])}" />', "desc")
    sub1(r'<link rel="canonical" href="[^"]*" />\n  <link rel="alternate" hreflang="de"[^\n]*\n  <link rel="alternate" hreflang="en"[^\n]*\n  <link rel="alternate" hreflang="x-default"[^\n]*',
         f'<link rel="canonical" href="{url}" />\n  <link rel="alternate" hreflang="de" href="{de_url}" />\n  <link rel="alternate" hreflang="en" href="{en_url}" />\n  <link rel="alternate" hreflang="x-default" href="{de_url}" />', "canonical/hreflang")
    sub1(r'<meta property="og:title" content="[^"]*" />', f'<meta property="og:title" content="{html.escape(F["title"])}" />', "og:title")
    sub1(r'<meta property="og:description" content="[^"]*" />', f'<meta property="og:description" content="{html.escape(F["ogdesc"])}" />', "og:desc")
    sub1(r'<meta property="og:url" content="[^"]*" />', f'<meta property="og:url" content="{url}" />', "og:url")

    # JSON-LD
    m = re.search(r'<script type="application/ld\+json">\n(.*?)\n  </script>', s, re.S)
    ld = json.loads(m.group(1))
    app = ld["@graph"][0]
    app["name"] = F["title"].split(":")[0].strip(); app["url"] = url; app["description"] = F["ogdesc"]
    ld["@graph"][1]["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub(r"<[^>]+>", "", a))}} for q, a in F["faq"]]
    home = "https://combatcoach.org" + HOME[lang]
    base_slug = BASE[lang]
    base_name = "Box-Timer" if lang == "de" else "Boxing timer"
    ld["@graph"][2]["itemListElement"] = [
        {"@type": "ListItem", "position": 1, "name": "Combat Coach", "item": home},
        {"@type": "ListItem", "position": 2, "name": base_name, "item": url_of(base_slug)},
        {"@type": "ListItem", "position": 3, "name": F["crumb"], "item": url}]
    s = s.replace(m.group(0), '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + "\n  </script>")

    # Sprachumschalter, Breadcrumb, H1, Lead
    sub1(r'<a class="lang-btn" href="/[^"]*">(EN|DE)</a>', f'<a class="lang-btn" href="/{other_slug}">{"EN" if lang == "de" else "DE"}</a>', "lang switch")
    sub1(r'<nav class="crumb" aria-label="Breadcrumb">.*?</nav>',
         f'<nav class="crumb" aria-label="Breadcrumb"><a href="{HOME[lang]}">Combat Coach</a> / <a href="/{base_slug}">{base_name}</a> / {F["crumb"]}</nav>', "crumb")
    a, b, c = F["h1"]
    sub1(r"<h1>.*?</h1>", f'<h1>{a}<span class="accent">{b}</span>{c}</h1>', "h1")
    sub1(r'<p class="lead">.*?</p>', f'<p class="lead">{F["lead"]}</p>', "lead")

    # Timer: Voreinstellung + Vorlagen
    sub1(r'<section class="timer" id="timer" aria-label="[^"]*">',
         "<section class=\"timer\" id=\"timer\" aria-label=\"%s\" data-preset='%s'>" % (html.escape(F["crumb"]), json.dumps(F["preset"])), "timer section")
    label_presets = "Vorlagen" if lang == "de" else "Presets"
    btns = "\n".join(f'          <button class="preset" type="button" data-rounds="{r}" data-round="{d}" data-rest="{p}">{html.escape(t)}</button>' for t, r, d, p in F["buttons"])
    sub1(r'<div class="presets">.*?</div>', f'<div class="presets">\n          <span>{label_presets}</span>\n{btns}\n        </div>', "presets")

    # Inhalt zwischen Timer und CTA
    th = "".join(f"<th>{x}</th>" for x in F["head"])
    tr = "".join(f"          <tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>\n" for a, b, c in F["rows"])
    li = "".join(f"        <li>{x}</li>\n" for x in F["train"])
    rel = LBL[lang]["sep"].join(f'<a href="{h}">{t}</a>' for h, t in F["related"])
    faq = "".join('      <details>\n        <summary><h3>%s</h3><span class="chev" aria-hidden="true"></span></summary>\n        <div class="body"><p>%s</p></div>\n      </details>\n' % (q, a) for q, a in F["faq"])
    body = (f'</section>\n\n      <h2>{F["h2_formats"]}</h2>\n      <p>{F["intro"]}</p>\n'
            f'      <table class="workout">\n        <thead><tr>{th}</tr></thead>\n        <tbody>\n{tr}        </tbody>\n      </table>\n\n'
            f'      <h2>{F["h2_train"]}</h2>\n      <ul>\n{li}      </ul>\n      <p>{LBL[lang]["related"]} {rel}</p>\n\n'
            f'      <h2>{LBL[lang]["faq"]}</h2>\n{faq}\n      ')
    i = s.index("</section>", s.index('<section class="timer"'))
    j = s.index('<div class="cta-box">')
    s = s[:i] + body + s[j:]

    # Tabellen-CSS
    anchor = "    footer{"
    assert s.count(anchor) == 1, (lang, F["slug"], "css anchor")
    s = s.replace(anchor, TABLE_CSS + anchor)
    io.open(F["slug"], "w", encoding="utf-8").write(s)
    return len(s)

if __name__ == "__main__":
    for F in FORMATS:
        for lang in ("de", "en"):
            other = F["en" if lang == "de" else "de"]["slug"]
            n = build(lang, F[lang], other)
            print(f"  {F[lang]['slug']:<28} {n:>6} B   Titel {len(F[lang]['title'])} Z · Desc {len(F[lang]['desc'])} Z")
