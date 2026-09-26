#!/bin/bash
# publish.sh <app-dir> — generate an app's privacy + support pages, push them to kzorif/apps
# (GitHub Pages), and wait until both URLs answer 200. Run automatically by every app's
# scripts/handoff.sh (operator, 2026-09-23: "make sure to do it automatically").
#
# Inputs, all from the app's handoff/metadata/en-US/:
#   name.txt, subtitle.txt       → page title and one-liner
#   privacy_access.txt           → the "What it uses on your iPhone" sentence; REQUIRED when the app
#                                  declares any NS…UsageDescription (mic, camera, photos, …)
#   pages_theme.txt (optional)   → braun (default) | nocturne
# A StoreKit config with an auto-renewable subscription adds the how-to-cancel line.
set -e
APP="$(cd "${1:-.}" && pwd)"; SLUG=$(basename "$APP"); M="$APP/handoff/metadata/en-US"
PAGES="$HOME/Apps/_kit/pages"; source "$HOME/Apps/_kit/scripts/env.sh"
NAME=$(cat "$M/name.txt"); BLURB=$(cat "$M/subtitle.txt")
# Operator rule 2026-09-26: the pages must match the app's aesthetic. pages_tokens.json (colours + the app's
# own fonts, from its theme file / DESIGN.md) is the normal path; pages_theme.txt names a hand-made theme.
# No silent default any more: ten apps shipped generic white Braun pages that way.
if [ -f "$M/pages_tokens.json" ]; then ARGS=(--tokens "$M/pages_tokens.json")
elif [ -f "$M/pages_theme.txt" ]; then ARGS=(--theme "$(cat "$M/pages_theme.txt")")
else echo "pages: write $M/pages_tokens.json from the app's theme (bg, fg, muted, accent, line, fonts) — pages must match the app's look"; exit 1; fi
if [ -f "$M/privacy_access.txt" ]; then ARGS+=(--access "$(cat "$M/privacy_access.txt")")
elif grep -rqs "UsageDescription" "$APP/project.yml" "$APP"/Sources/*/Info.plist; then
  echo "pages: app declares a permission (UsageDescription) but $M/privacy_access.txt is missing — write one sentence saying what it uses and why"; exit 1
fi
grep -qs "recurringSubscriptionPeriod" "$APP"/Sources/*/*.storekit && ARGS+=(--subscription)
grep -rqsE "^import MapKit|Map\(|MKMapView|LookAround" "$APP/Sources" && ARGS+=(--maps)
grep -rqsE "^import AppIntents|AppShortcutsProvider" "$APP/Sources" && ARGS+=(--intents)

# one publisher at a time (parallel drills); a separate lock from the ledger lock, because
# handoff.sh already runs under that one
exec 9>"$PAGES/.publish.lock"; /usr/bin/python3 -c 'import fcntl; fcntl.flock(9, fcntl.LOCK_EX)'
cd "$PAGES"
git pull -q --rebase
python3 _page.py "$SLUG" "$NAME" "$BLURB" "${ARGS[@]}" >/dev/null
# self-host the fonts the tokens name (copied from the app's own bundle; OFL/licensed with the app)
if [ -f "$M/pages_tokens.json" ]; then
  for f in $(/usr/bin/python3 -c "import json,sys; print(' '.join(v['file'] for v in json.load(open(sys.argv[1])).get('fonts',{}).values() if v.get('file')))" "$M/pages_tokens.json"); do
    src=$(find "$APP/Sources" "$APP/Resources" -name "$f" 2>/dev/null | head -1)
    [ -n "$src" ] || { echo "pages: font $f named in pages_tokens.json not found in the app"; exit 1; }
    mkdir -p "docs/$SLUG/fonts"; cp "$src" "docs/$SLUG/fonts/"
  done
fi
git add "docs/$SLUG"
if git diff --cached --quiet; then echo "pages: $SLUG unchanged"
else git commit -qm "pages: $SLUG" && git push -q && echo "pages: $SLUG pushed"; fi

# wait for GitHub Pages (usually under a minute), up to ~4 min
for i in $(seq 1 24); do
  P=$(curl -s -o /dev/null -w '%{http_code}' "$URL_BASE/$SLUG/privacy"); S=$(curl -s -o /dev/null -w '%{http_code}' "$URL_BASE/$SLUG/support")
  [ "$P$S" = 200200 ] && { echo "pages: live $URL_BASE/$SLUG/privacy + /support"; exit 0; }
  /bin/sleep 10
done
echo "pages: pushed but not live yet ($P/$S) — re-check $URL_BASE/$SLUG/privacy in a few minutes"; exit 2
