#!/usr/bin/env python3
"""Update the meet-up city cards in index.html from the Luma calendar's iCal feed.

The Luma iframe lower in the section is already self-updating. This script keeps the
*cards* above it honest: when a city's next event is on Luma, its card flips to
"Registration open" with the real date and a Register button; when no upcoming event
exists, it falls back to "Date coming soon".

Only two blocks inside a card are touched: the status pill and everything from
<div class="when"> onward. The venue paragraph, the city name, and the card's position
are left exactly as a human wrote them.

Usage
  python3 scripts/sync_events.py            # rewrite index.html in place
  python3 scripts/sync_events.py --check    # exit 1 if the file is out of date (no writes)
  python3 scripts/sync_events.py --ics FILE # read a local .ics instead of fetching

Environment
  ACA_ICS_URL   override the calendar feed URL
"""
import argparse, os, re, sys, urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Luma calendar iCal feed. Confirm from the calendar page's Subscribe / Add to Calendar link.
# `or` rather than a get() default: CI passes an empty string when the repository variable
# is unset, and an empty string must fall back too.
DEFAULT_ICS = "https://api.lu.ma/ics/get?entity=calendar&id=cal-PWZSiCpJoPE914l"
ICS_URL = (os.environ.get("ACA_ICS_URL") or "").strip() or DEFAULT_ICS
CALENDAR = "https://luma.com/aicyberalliance?utm_source=website"
PAGE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "index.html")

# Which words in an event's title or location mean "this is that city's meet-up".
# Order matters: the first city whose tokens match wins, so put the more specific first.
CITY_TOKENS = {
    "Austin":         ["austin"],
    "Washington DC":  ["washington dc", "tysons", " dc:", " dc ", "vienna, va"],
    "SF Bay Area":    ["bay area", "sf bay", "snowflake", "san jose", "santa clara", "menlo park"],
    "San Francisco":  ["san francisco"],
    "Boston":         ["boston", "cambridge, ma"],
}


def fetch(path=None):
    if path:
        return open(path, encoding="utf-8").read()
    if not ICS_URL.startswith(("http://", "https://")):
        raise SystemExit("Feed URL looks wrong: %r. Set the ACA_ICS_URL repository variable "
                         "to the calendar's Subscribe link." % ICS_URL)
    print("Feed: %s" % ICS_URL)
    req = urllib.request.Request(ICS_URL, headers={"User-Agent": "ai-cyber-alliance-site"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:
        raise SystemExit("Could not read the calendar feed (%s). Nothing was changed. If the "
                         "address is wrong, set the ACA_ICS_URL repository variable from the "
                         "calendar's Subscribe link." % e)


def parse_ics(text):
    """Minimal VEVENT reader: enough for Luma's feed, no dependencies."""
    text = re.sub(r"\r?\n[ \t]", "", text)          # unfold continuation lines
    events = []
    for block in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", text, re.S):
        ev = {}
        for line in block.strip().splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            name = key.split(";")[0].upper()
            params = dict(
                p.split("=", 1) for p in key.split(";")[1:] if "=" in p
            )
            if name in ("DTSTART", "DTEND"):
                ev[name] = (value.strip(), params.get("TZID"))
            else:
                ev[name] = value.strip().replace("\\,", ",").replace("\\n", " ")
        if "DTSTART" in ev:
            events.append(ev)
    return events


def to_dt(raw):
    value, tzid = raw
    if value.endswith("Z"):
        return datetime.strptime(value, "%Y%m%dT%H%M%SZ").replace(tzinfo=ZoneInfo("UTC"))
    if "T" in value:
        dt = datetime.strptime(value, "%Y%m%dT%H%M%S")
        return dt.replace(tzinfo=ZoneInfo(tzid)) if tzid else dt.replace(tzinfo=ZoneInfo("UTC"))
    return datetime.strptime(value, "%Y%m%d").replace(tzinfo=ZoneInfo(tzid or "UTC"))


def match_city(ev):
    hay = (ev.get("SUMMARY", "") + " " + ev.get("LOCATION", "")).lower()
    for city, tokens in CITY_TOKENS.items():
        if any(t in hay for t in tokens):
            return city
    return None


def next_events(events, now):
    """Earliest upcoming event per city."""
    best = {}
    for ev in events:
        start = to_dt(ev["DTSTART"])
        if start < now:
            continue
        city = match_city(ev)
        if not city:
            continue
        if city not in best or start < to_dt(best[city]["DTSTART"]):
            best[city] = ev
    return best


def when_line(ev):
    start = to_dt(ev["DTSTART"])
    end = to_dt(ev["DTEND"]) if "DTEND" in ev else start + timedelta(hours=2)
    local = ZoneInfo(ev["DTSTART"][1]) if ev["DTSTART"][1] else start.tzinfo
    start, end = start.astimezone(local), end.astimezone(local)

    def clock(d):
        h = d.strftime("%I").lstrip("0") or "12"
        return h + (":%s" % d.strftime("%M") if d.minute else "") + d.strftime(" %p").replace(" AM", " AM").replace(" PM", " PM")

    date = "%s, %s %d, %d" % (start.strftime("%a"), start.strftime("%b"), start.day, start.year)
    times = "%s–%s %s" % (clock(start).replace(" AM", "").replace(" PM", ""), clock(end), start.strftime("%Z"))
    return "<strong>%s</strong> · %s<br>Two to three talks, Q&amp;A, networking" % (date, times)


def event_url(ev):
    for key in ("URL", "X-ALT-DESC", "DESCRIPTION"):
        m = re.search(r"https?://(?:lu\.ma|luma\.com)/[A-Za-z0-9\-_]+", ev.get(key, ""))
        if m:
            return m.group(0).replace("lu.ma", "luma.com")
    return CALENDAR


def event_id(ev):
    m = re.search(r"evt-[A-Za-z0-9]+", ev.get("UID", "") + " " + ev.get("URL", ""))
    return m.group(0) if m else None


def render(city, ev, venue_tbd=False):
    """Return (opening_tag, status_span, tail) for a card.

    With no upcoming event the card falls back to its resting state, which depends on
    whether a venue is secured: "Venue TBD" for cities still looking for space,
    "Date coming soon" for cities that have a host.
    """
    if not ev:
        resting = ('<span class="status"><span class="dot"></span>Venue TBD</span>'
                   if venue_tbd else
                   '<span class="status soon"><span class="dot"></span>Date coming soon</span>')
        return (
            '<div class="city" data-city="%s">' % city,
            resting,
            '<div class="when"><strong>Next date TBA</strong><br>Followers hear first when it lands on Luma</div>\n'
            '        <div class="acts">\n'
            '          <a class="btn btn-ghost btn-sm" href="%s" target="_blank" rel="noopener">Follow on Luma →</a>\n'
            '        </div>' % CALENDAR,
        )
    url, eid = event_url(ev), event_id(ev)
    attrs = ' data-luma-action="checkout" data-luma-event-id="%s" data-luma-utm-source="website"' % eid if eid else ""
    return (
        '<div class="city live" data-city="%s">' % city,
        '<span class="status open"><span class="dot"></span>Registration open</span>',
        '<div class="when">%s</div>\n'
        '        <div class="acts">\n'
        '          <a class="btn btn-primary btn-sm" href="%s" target="_blank" rel="noopener"%s>Register →</a>\n'
        '          <a class="more" href="%s" target="_blank" rel="noopener">Event details ↗</a>\n'
        '        </div>' % (when_line(ev), url, attrs, url),
    )


CARD = re.compile(
    r'(<div class="city[^"]*" data-city="(?P<city>[^"]+)">)\s*\n'
    r'\s*(?P<status><span class="status[^>]*>.*?</span>)\s*\n'
    r'(?P<middle>.*?)'
    r'(?P<tail><div class="when">.*?</div>\s*\n\s*<div class="acts">.*?</div>)\s*\n\s*</div>',
    re.S,
)


def apply(html, upcoming):
    changed = []

    def sub(m):
        city = m.group("city")
        middle = m.group("middle").rstrip()
        opening, status, tail = render(city, upcoming.get(city), venue_tbd='class="tbd"' in middle)
        new = "%s\n        %s\n%s\n        %s\n      </div>" % (opening, status, middle, tail)
        if new != m.group(0):
            changed.append(city)
        return new

    return CARD.sub(sub, html), changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ics")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    events = parse_ics(fetch(args.ics))
    if not events:
        print("No events found in the feed; leaving index.html alone.", file=sys.stderr)
        return 0
    upcoming = next_events(events, datetime.now(ZoneInfo("UTC")))
    html = open(PAGE, encoding="utf-8").read()
    new, changed = apply(html, upcoming)

    listed = ", ".join("%s → %s" % (c, to_dt(e["DTSTART"]).strftime("%b %d")) for c, e in sorted(upcoming.items()))
    print("Upcoming on Luma: %s" % (listed or "none"))
    if not changed:
        print("Cards already match the calendar.")
        return 0
    if args.check:
        print("Out of date: %s" % ", ".join(changed), file=sys.stderr)
        return 1
    open(PAGE, "w", encoding="utf-8").write(new)
    print("Updated: %s" % ", ".join(changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
