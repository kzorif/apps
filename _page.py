#!/usr/bin/env python3
"""Generates privacy + support pages per app into ./docs/<slug>/. Static, no scripts, no trackers.
Usage: _page.py <slug> "<App Name>" "<one-line what it is>" [--third-party "<credit line>"]"""
import os, sys, datetime
slug, name, blurb = sys.argv[1], sys.argv[2], sys.argv[3]
third = sys.argv[sys.argv.index("--third-party") + 1] if "--third-party" in sys.argv else ""
today = datetime.date.today().isoformat(); email = "mr.firozkhan57@gmail.com"
css = "body{font:17px/1.55 -apple-system,system-ui,sans-serif;max-width:640px;margin:48px auto;padding:0 20px;color:#111}h1{font-weight:600}h2{font-size:1.05em;margin-top:2em}a{color:#111}footer{margin-top:3em;color:#666;font-size:.9em}"
def page(title, body):
    return f"<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>{title} · {name}</title><style>{css}</style></head><body><h1>{title}</h1><p><em>{name}</em> — {blurb}</p>{body}<footer>Firoz Khan · <a href='mailto:{email}'>{email}</a> · updated {today}</footer></body></html>"
privacy = page("Privacy Policy", f"""
<h2>What {name} collects</h2><p>Nothing. {name} has no account, no analytics, no advertising, no tracking, and never sends your data anywhere. Everything you do in the app stays on your device.</p>
<h2>Purchases</h2><p>In-app purchases are handled by Apple. We receive no personal information about you from a purchase.</p>
<h2>Apple services</h2><p>Where the app shows maps or street-level imagery, those are loaded by Apple Maps under <a href='https://www.apple.com/legal/privacy/'>Apple's privacy policy</a>. Siri and Shortcuts, where offered, run on your device.</p>
{'<h2>Third-party content</h2><p>' + third + '</p>' if third else ''}
<h2>Contact</h2><p>Questions: <a href='mailto:{email}'>{email}</a>.</p>""")
support = page("Support", f"""
<h2>Get help</h2><p>Email <a href='mailto:{email}'>{email}</a> and say which app and which iPhone. Replies within a few days.</p>
<h2>Purchases</h2><p>To restore a purchase on a new device, open the app's settings or paywall and tap <strong>Restore purchases</strong>. Refunds are handled by Apple at <a href='https://reportaproblem.apple.com'>reportaproblem.apple.com</a>.</p>
<h2>Privacy</h2><p><a href='privacy.html'>Privacy policy</a>.</p>""")
os.makedirs(f"docs/{slug}", exist_ok=True)
open(f"docs/{slug}/privacy.html", "w").write(privacy); open(f"docs/{slug}/support.html", "w").write(support)
print(f"docs/{slug}/privacy.html docs/{slug}/support.html")
