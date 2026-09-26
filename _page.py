#!/usr/bin/env python3
"""Generates privacy + support pages per app into ./docs/<slug>/, in the app's own design language.
Static, system fonts only, no scripts, no trackers (a privacy page that phones home would be a joke).
Usage: _page.py <slug> "<App Name>" "<one-line what it is>" --theme nocturne|braun [--third-party "<credit line>"] [--access "<mic/camera/photos sentence>"] [--subscription]"""
import os, sys, datetime
slug, name, blurb = sys.argv[1], sys.argv[2], sys.argv[3]
theme = sys.argv[sys.argv.index("--theme") + 1] if "--theme" in sys.argv else "braun"
access = sys.argv[sys.argv.index("--access") + 1] if "--access" in sys.argv else ""
sub = "--subscription" in sys.argv
# Apple services paragraph only when the app really uses them (2026-09-26: it was on every page, true only for Keep)
maps, intents = "--maps" in sys.argv, "--intents" in sys.argv
apple = ("<h2>Apple services</h2><p>" + ("Maps and street-level imagery are loaded by Apple Maps under <a href='https://www.apple.com/legal/privacy/'>Apple's privacy policy</a>. " if maps else "")
         + ("Siri and Shortcuts run on your device. " if intents else "") + "</p>") if (maps or intents) else ""
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
}.get(theme)
if "--tokens" in sys.argv:
    # 2026-09-26 operator rule: pages must match the app's own aesthetic. tokens.json comes from the app's
    # theme file / DESIGN.md (handoff/metadata/en-US/pages_tokens.json). Fonts are self-hosted next to the
    # page (docs/<slug>/fonts/), never loaded from a third party.
    import json
    T = json.load(open(sys.argv[sys.argv.index("--tokens") + 1]))
    def fam(role):
        f = T.get("fonts", {}).get(role) or {}
        stack = {"serif": "Georgia,'Iowan Old Style',serif", "mono": "ui-monospace,Menlo,monospace",
                 "rounded": "ui-rounded,-apple-system,system-ui,sans-serif"}.get(f.get("fallback"), "-apple-system,system-ui,'Helvetica Neue',sans-serif")
        return (f"'{f['family']}'," if f.get("family") else "") + stack
    faces = "".join(f"@font-face{{font-family:'{f['family']}';src:url('fonts/{f['file']}');font-weight:{f.get('weight', 400)};font-style:{f.get('style', 'normal')};font-display:swap}}"
                    for f in T.get("fonts", {}).values() if f.get("file"))
    case = {"lower": "lowercase", "upper": "uppercase"}.get(T.get("heading_case"), "none")
    css = f"""{faces}body{{background:{T['bg']};color:{T['fg']};font:{T.get('body_size', 17)}px/1.6 {fam('body')};max-width:620px;margin:0 auto;padding:56px 22px}}
h1{{overflow-wrap:anywhere;font-family:{fam('heading')};font-weight:{T.get('heading_weight', 500)};font-style:{T.get('heading_style', 'normal')};font-size:{T.get('h1_size', '2.3em')};line-height:1.1;margin:0 0 .3em;text-transform:{case};color:{T.get('heading_color', T['fg'])}}}
.eyebrow,h2{{font-family:{fam('label')};font-size:.7em;letter-spacing:{T.get('label_tracking', '.12em')};text-transform:uppercase;color:{T.get('label_color', T['muted'])};font-weight:500}}
.eyebrow{{margin-bottom:1.4em}}.lead{{color:{T['muted']}}}
h2{{margin:2.3em 0 .6em;padding-top:1.2em;border-top:1px solid {T['line']}}}
a{{color:{T.get('link', T['accent'])}}}p{{margin:.5em 0}}strong{{color:{T['fg']}}}
.fleuron{{height:{T.get('divider_height', '3px')};background:{T['accent']};width:{T.get('divider_width', '44px')};margin:2.4em 0;border-radius:{T.get('radius', '0')}}}
footer{{margin-top:3em;font-family:{fam('label')};font-size:.78em;color:{T['muted']};border-top:1px solid {T['line']};padding-top:1em}}
{T.get('extra_css', '')}"""
    THEMES = dict(css=css, eyebrow_privacy=T.get("eyebrow_privacy", "privacy"), eyebrow_support=T.get("eyebrow_support", "support"),
                  divider=T.get("divider_html", "<div class=fleuron></div>"))
    theme = "tokens"
elif THEMES is None: sys.exit(f"unknown theme {theme!r}")
def page(title, eyebrow, body):
    return f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>{title} · {name}</title><style>{THEMES['css']}</style></head><body>
<div class=eyebrow>{eyebrow}</div><h1>{name}</h1><p class=lead>{blurb}</p>{body}
<footer>Firoz Khan · <a href='mailto:{email}'>{email}</a> · {today}</footer></body></html>"""
privacy = page("Privacy", THEMES["eyebrow_privacy"], f"""
<h2>What {name.split(':')[0]} collects</h2><p>Nothing. There is no account, no analytics, no advertising and no tracking. Nothing you do in the app is sent anywhere. It stays on your device.</p>
{f"<h2>What it uses on your iPhone</h2><p>{access} None of it is ever sent to us, and you can turn access off at any time in Settings.</p>" if access else ""}
<h2>Purchases</h2><p>In-app purchases are handled by Apple. We receive no personal information about you from a purchase.</p>
{apple}
{'<h2>Third-party content</h2><p>' + third + '</p>' if third else ''}
{THEMES['divider']}
<h2>Contact</h2><p>Questions about privacy? Email <a href='mailto:{email}'>{email}</a>.</p>""")
support = page("Support", THEMES["eyebrow_support"], f"""
<h2>Get help</h2><p>Email <a href='mailto:{email}'>{email}</a> and say which app and which iPhone. Replies within a few days.</p>
<h2>Purchases</h2><p>To restore a purchase on a new device, open the app's settings or paywall and tap <strong>Restore purchases</strong>. {"To cancel a subscription, open Settings → your name → Subscriptions on your iPhone; it stays active until the end of the period you paid for. " if sub else ""}Refunds are handled by Apple at <a href='https://reportaproblem.apple.com'>reportaproblem.apple.com</a>.</p>
{THEMES['divider']}
<h2>Privacy</h2><p><a href='privacy.html'>Read the privacy policy</a>.</p>""")
os.makedirs(f"docs/{slug}", exist_ok=True)
open(f"docs/{slug}/privacy.html", "w").write(privacy); open(f"docs/{slug}/support.html", "w").write(support)
print(f"docs/{slug}/ ({theme})")
