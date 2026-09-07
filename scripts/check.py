#!/usr/bin/env python3
"""Lightweight checks for pull requests. No dependencies beyond the standard library.

  1. index.html and code-of-conduct.html parse with balanced tags.
  2. Every local href/src (assets/, #anchors, .html) resolves.
  3. Images in assets/ stay under the size cap.
  4. Nothing left at href="#" outside a known EDIT: placeholder.

Run locally:  python3 scripts/check.py
"""
import os, re, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html", "code-of-conduct.html"]
IMAGE_CAP = 120 * 1024          # bytes; hero photo is exempt below
IMAGE_EXEMPT = {"event-photo.jpg"}
VOID = {"meta", "link", "img", "br", "input", "hr", "source", "wbr"}

errors = []

class Checker(HTMLParser):
    def __init__(self, name):
        super().__init__()
        self.name, self.stack, self.ids, self.refs = name, [], set(), []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for k in ("href", "src"):
            if k in a:
                self.refs.append((a[k], self.getpos()[0]))
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))
    def handle_endtag(self, tag):
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        else:
            errors.append(f"{self.name}:{self.getpos()[0]} unexpected </{tag}> (open: {[t for t,_ in self.stack[-3:]]})")

for page in PAGES:
    path = os.path.join(ROOT, page)
    if not os.path.exists(path):
        errors.append(f"{page} missing"); continue
    src = open(path, encoding="utf-8").read()
    c = Checker(page); c.feed(src)
    for tag, line in c.stack:
        errors.append(f"{page}:{line} <{tag}> never closed")
    for ref, line in c.refs:
        if ref.startswith(("http://", "https://", "mailto:", "data:")):
            continue
        if ref == "#":
            # allowed only when the preceding lines carry an EDIT: marker
            window = "\n".join(src.splitlines()[max(0, line-3):line])
            if "EDIT:" not in window:
                errors.append(f"{page}:{line} dead link href=\"#\" without an EDIT: comment")
            continue
        if ref.startswith("#"):
            if ref[1:] not in c.ids:
                errors.append(f"{page}:{line} anchor {ref} has no matching id")
            continue
        target = ref.split("#")[0].split("?")[0]
        if not os.path.exists(os.path.join(ROOT, target)):
            errors.append(f"{page}:{line} local path not found: {ref}")

assets = os.path.join(ROOT, "assets")
for f in sorted(os.listdir(assets)):
    size = os.path.getsize(os.path.join(assets, f))
    if f in IMAGE_EXEMPT:
        continue
    if size > IMAGE_CAP:
        errors.append(f"assets/{f} is {size//1024} KB; cap is {IMAGE_CAP//1024} KB (trim, compress, or use SVG)")
    if not re.match(r"^(aca|member|host|event)-[a-z0-9-]+\.(png|svg|jpg)$", f):
        errors.append(f"assets/{f}: name it member-<org>.png, host-<org>.png, or aca-*.*")

if errors:
    print("\n".join(errors)); print(f"\n{len(errors)} problem(s)"); sys.exit(1)
print("All checks passed.")
