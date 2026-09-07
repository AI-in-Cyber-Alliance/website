# Contributing

The AI Cyber Alliance website is **maintained by the community it describes**. Anyone can
propose a change; two maintainers review; one approval merges it and the live site updates.
No special tooling required.

## Two ways to contribute

**Open an issue (no HTML needed).** Use one of the forms under
[New issue](../../issues/new/choose): *List my city*, *Add my organization as a member*,
*Add a host*. A maintainer reviews it against the criteria below and, if approved, makes the
site change for you.

**Open a pull request (you edit the file).** Fork the repo, edit `index.html`, preview it in a
browser, open a PR. The whole site is one plain HTML file with **no build step and no
framework**; search it for `TEMPLATE:` to find a copy-paste block for each kind of listing.

Either way the review criteria are the same.

## Get listed

Listing is a statement that an organization or city is part of the alliance, so it is by
review, not by request. Maintainers check the criteria below and nothing else.

### Member organization

Members are equal peers who put in the work. To be listed, an organization has:

- co-organized, spoken at, sponsored, or hosted at least one AI Cyber Alliance event, **or**
  committed to one that is on the [Luma calendar](https://luma.com/aicyberalliance); and
- agreed to the community-first values: educational talks, no product pitches, vendor-neutral.

A logo without participation is not a listing. Members who go a year without participating
may be moved to the hosts row or removed; maintainers will reach out first.

### Host

Hosts have provided a venue for an event, or have a confirmed date for one. Space offered
without a date is welcome; it goes on the city card as "Venue secured" until the event exists.

### Meet-up city

A city card goes up when there is:

- a named local organizer with a way to reach them; and
- either a venue, or a target month for a first event.

Cards move through three states, each with its own `TEMPLATE:` block in `index.html`:
*Venue TBD* → *Date coming soon* → *Registration open* (once the event is on Luma).
Events themselves are submitted on Luma via **Submit Event** on the calendar page and approved
there by a calendar admin; the website card and the Luma event are separate approvals.

### Past talk

Any recorded talk from an alliance event, linked to its YouTube URL. Newest first.

## How a pull request works

1. **Fork** this repository.
2. **Edit** `index.html`. Copy the matching `TEMPLATE:` block rather than writing new markup so
   the result matches the rest of the page. Colors and fonts are CSS variables in the `:root`
   block at the top of `<style>`; you should not need to touch them.
3. **Logos** go in `assets/` as `member-<org>.png` or `host-<org>.png`: trimmed, transparent
   PNG or SVG, under 100 KB. Set the inline `height` so the mark sits at the same visual weight
   as its neighbours (members 30–50px, hosts 26–38px).
4. **Preview** by opening `index.html` in your browser, desktop and phone width.
5. **Check** with `python3 scripts/check.py` (optional; CI runs it on every PR). It validates
   HTML nesting, local links and anchors, image sizes, and asset naming.
6. **Open the PR.** The template asks for a short description and a checklist.

A maintainer reviews, requests changes if needed, and merges. The live site updates on merge.

## Common edits

| I want to… | Where |
|---|---|
| Add a contact / host form link | `index.html` — the `EDIT:` comments |
| Publish a meet-up for registration | `index.html` — the city's card in `#meetups`: switch to the `Registration open` template, set date, Luma URL and `data-luma-event-id` |
| Add a new city | `index.html` — `TEMPLATE: city` in `#meetups`; keep "Your city" last |
| Add a past talk | `index.html` — `TEMPLATE: talk`, set the YouTube `href` |
| Add a member or host | `index.html` — `TEMPLATE: member` / `TEMPLATE: host`, logo in `assets/` |
| Change a brand color | `index.html` — `--blue`, `--pink`, `--magenta` in `:root` |

## Maintainers

Current maintainers, listed in [`.github/CODEOWNERS`](.github/CODEOWNERS):

- Evan Powell ([@epowell101](https://github.com/epowell101))
- John Van Lowe ([@johnvanlowe](https://github.com/johnvanlowe))

Maintainers review against the criteria above. Disagreements about a listing are settled in
the PR thread, in the open. Adding a maintainer is itself a PR to `CODEOWNERS`, approved by an
existing maintainer.

**Branch protection** (repository Settings → Branches → rule for `main`) enforces the flow:
require a pull request before merging, require 1 approving review, require review from Code
Owners, require the "Site checks" status check to pass. With those four set, "one approval
merges it" is a GitHub guarantee rather than a convention.

## Ground rules

- Be respectful and constructive: see the [Code of Conduct](CODE_OF_CONDUCT.md).
- Keep the site **community-first**: no product pitches or marketing copy.
- Keep it simple. This is intentionally a dependency-free static site. Please do not add a
  build system, framework, or package manager.

## Licensing

By contributing, you agree that your contributions are licensed under the project's terms:
**code** under the [Apache License 2.0](LICENSE), and **content** (docs, logos as displayed,
recordings) under [CC BY 4.0](LICENSE-CONTENT.md).
