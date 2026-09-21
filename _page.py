#!/usr/bin/env python3
"""Generates privacy + support pages per app into ./docs/<slug>/, in the app's own design language.
Static, system fonts only, no scripts, no trackers (a privacy page that phones home would be a joke).
Usage: _page.py <slug> "<App Name>" "<one-line what it is>" --theme nocturne|braun [--third-party "<credit line>"]"""
import os, sys, datetime
slug, name, blurb = sys.argv[1], sys.argv[2], sys.argv[3]
theme = sys.argv[sys.argv.index("--theme") + 1] if "--theme" in sys.argv else "braun"
third = sys.argv[sys.argv.index("--third-party") + 1] if "--third-party" in sys.argv else ""
today = datetime.date.today().strftime("%-d %B %Y"); email = "khzorif@gmail.com"
THEMES = {
 "nocturne": dict(  # visconti-atelier, Nocturne: rare-book on black, gold as rule and label
  css="""body{background:#0e0c09;color:#f4ecd8;font:18px/1.6 Georgia,'Iowan Old Style','Times New Roman',serif;max-width:620px;margin:0 auto;padding:64px 22px}
h1{font-weight:400;font-style:italic;font-size:2.6em;line-height:1.1;margin:0 0 .3em;color:#f4ecd8}
.eyebrow{font-family:-apple-system,system-ui,sans-serif;font-size:.7em;letter-spacing:.22em;text-transform:uppercase;color:#e4c97a;margin-bottom:1.2em}
.lead{color:#b8a26e;font-style:italic;font-size:1.05em}
h2{font-family:-apple-system,system-ui,sans-serif;font-size:.72em;letter-spacing:.2em;text-transform:uppercase;color:#e4c97a;margin:2.4em 0 .6em;font-weight:500}
h2:before{content:'';display:block;height:1px;background:rgba(176,138,62,.45);margin-bottom:1.4em}
a{color:#e0846e}p{margin:.5em 0}
.fleuron{text-align:center;color:#e4c97a;margin:2.4em 0;font-size:1.2em}.fleuron:before,.fleuron:after{content:'';display:inline-block;width:38%;height:1px;background:rgba(176,138,62,.45);vertical-align:middle;margin:0 12px}
footer{margin-top:3em;font-family:ui-monospace,Menlo,monospace;font-size:.78em;color:#6b5847}""",
  eyebrow_privacy="I — Privacy", eyebrow_support="II — Support", divider="<div class=fleuron>❦</div>"),
 "braun": dict(  # braun-rams: white housing, parting lines, one red, lowercase headings
  css="""body{background:#fff;color:#000;font:17px/1.55 -apple-system,system-ui,'Helvetica Neue',sans-serif;max-width:620px;margin:0 auto;padding:56px 22px}
h1{font-weight:500;font-size:2.2em;line-height:1.1;margin:0 0 .2em;text-transform:lowercase}
.eyebrow{font-size:.68em;letter-spacing:.08em;text-transform:uppercase;color:#666;margin-bottom:1.5em}
.lead{color:#666}
h2{font-size:.68em;letter-spacing:.08em;text-transform:uppercase;color:#666;font-weight:500;margin:2.2em 0 .5em;padding-top:1.2em;border-top:1px solid #c2c2c2}
a{color:#000}p{margin:.5em 0}
.fleuron{height:2px;background:#d72000;width:44px;margin:2.4em 0}
footer{margin-top:3em;font-size:.82em;color:#666;border-top:1px solid #c2c2c2;padding-top:1em}""",
  eyebrow_privacy="privacy", eyebrow_support="support", divider="<div class=fleuron></div>"),
}[theme]
def page(title, eyebrow, body):
    return f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>{title} · {name}</title><style>{THEMES['css']}</style></head><body>
<div class=eyebrow>{eyebrow}</div><h1>{name}</h1><p class=lead>{blurb}</p>{body}
<footer>Firoz Khan · <a href='mailto:{email}'>{email}</a> · {today}</footer></body></html>"""
privacy = page("Privacy", THEMES["eyebrow_privacy"], f"""
<h2>What {name.split(':')[0]} collects</h2><p>Nothing. There is no account, no analytics, no advertising and no tracking. Nothing you do in the app is sent anywhere. It stays on your device.</p>
<h2>Purchases</h2><p>In-app purchases are handled by Apple. We receive no personal information about you from a purchase.</p>
<h2>Apple services</h2><p>Where the app shows maps or street-level imagery, Apple Maps loads them under <a href='https://www.apple.com/legal/privacy/'>Apple's privacy policy</a>. Siri and Shortcuts, where offered, run on your device.</p>
{'<h2>Third-party content</h2><p>' + third + '</p>' if third else ''}
{THEMES['divider']}
<h2>Contact</h2><p>Questions about privacy? Email <a href='mailto:{email}'>{email}</a>.</p>""")
support = page("Support", THEMES["eyebrow_support"], f"""
<h2>Get help</h2><p>Email <a href='mailto:{email}'>{email}</a> and say which app and which iPhone. Replies within a few days.</p>
<h2>Purchases</h2><p>To restore a purchase on a new device, open the app's settings or paywall and tap <strong>Restore purchases</strong>. Refunds are handled by Apple at <a href='https://reportaproblem.apple.com'>reportaproblem.apple.com</a>.</p>
{THEMES['divider']}
<h2>Privacy</h2><p><a href='privacy.html'>Read the privacy policy</a>.</p>""")
os.makedirs(f"docs/{slug}", exist_ok=True)
open(f"docs/{slug}/privacy.html", "w").write(privacy); open(f"docs/{slug}/support.html", "w").write(support)
print(f"docs/{slug}/ ({theme})")
