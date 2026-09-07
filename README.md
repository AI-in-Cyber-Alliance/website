# AI Cyber Alliance — website

The public website for the **AI Cyber Alliance** — a community-led, vendor-neutral
group running technical meet-ups on AI, cybersecurity, Cloud Native, and open source.
Two 20-minute talks, real Q&A, no product pitches.

🔗 Site: https://ai-cyber-alliance.org/
🔗 Calendar (follow for every event): https://luma.com/aicyberalliance
🔗 LinkedIn: https://www.linkedin.com/groups/17875019/
🔗 YouTube: https://www.youtube.com/@AICyberAlliance

## What's in this repo

```
index.html            The entire website — one plain, hand-editable HTML file
code-of-conduct.html  Code of Conduct, rendered for the site
assets/               Logos (alliance, members, hosts) and the hero event photo
scripts/check.py      PR checks: HTML nesting, links, image size, asset naming
.github/              Issue forms (list a city, add a member, add a host),
                      PR template, CODEOWNERS, and the "Site checks" workflow
CODE_OF_CONDUCT.md    Community Code of Conduct (source)
CONTRIBUTING.md       How to contribute (fork → edit → PR)
LICENSE               Apache License 2.0 (code)
LICENSE-CONTENT.md    CC BY 4.0 (docs, recordings)
README.md             This file
```

`index.html` is plain HTML with one `<style>` block: no build step, no framework, no
package manager. Open it in any browser to preview; serve the folder to host.

## Page map

| Section | `id` | Theme | What lives there |
|---|---|---|---|
| Hero | `#top` | dark | Headline, CTAs, event photo, stats |
| About | `#what` | light | What the alliance is and isn't |
| Format | `#format` | dark | Talk format, cities, audience, topics |
| **Meet-ups** | `#meetups` | light | City cards, Luma follow, live calendar embed |
| Members | `#members` | dark | Founding member logos |
| Hosts | `#hosts` | light | Host logos |
| Talks | `#talks` | dark | Past talk cards → YouTube |
| Get involved | `#start` | dark | Speak / Host / Join |

Large sections alternate charcoal and off-white via `class="section light"`.

## Editing the site

Everything is in `index.html`: readable, commented, and safe to edit by hand. Change it,
open it in a browser, commit, done. Search the file for `EDIT:` to find every spot that
takes a real value.

### Colors and fonts

Brand tokens are CSS variables in the `:root` block at the top of `<style>`:

| Token | Value | Use |
|---|---|---|
| `--charcoal` | `#2B292A` | Dark section background |
| `--offwhite` | `#EFEFEF` | Light section background |
| `--blue` | `#839CF8` | Cloud Blue, primary (buttons, links, "registration open") |
| `--pink` | `#EAA4A4` | Pulse Pink, secondary (eyebrows, accents, "date coming soon") |
| `--magenta` | `#ED58F5` | Highlight, used sparingly (hover, focus, selected) |

Light sections override the text/line/link tokens inside `.section.light` so the same
components render correctly on both backgrounds.

### Meet-ups (`#meetups`)

Events are run on Luma. The site never stores registrations; it links out.

- **Follow the whole calendar:** `https://luma.com/aicyberalliance`. Luma's Follow
  notifies people of every event in every city. This is the primary CTA in the section.
- **Calendar ID:** `cal-PWZSiCpJoPE914l` (used by the embed and the long-form URL
  `https://luma.com/calendar/cal-PWZSiCpJoPE914l`).
- **One card per city.** Each card has a status pill and a button. Three states:

  | State | Markup | Button |
  |---|---|---|
  | Registration open | `class="city live"` + `<span class="status open">` | `Register →` pointing at the event |
  | Date coming soon (venue secured) | `class="city"` + `<span class="status soon">` | `Get notified →` → follow the calendar |
  | Venue TBD | `class="city"` + `<span class="status">` | `Get notified →` → follow the calendar |

- **To publish an event on a card:** create it on Luma, then on the card add class
  `live`, switch the pill to `status open`, set the date line, and give the Register
  button both the event URL (`href`, the no-JS fallback) and the event ID
  (`data-luma-event-id="evt-…"`). The event ID is under the event's
  **Manage → More → Embed**. With the ID set, Register opens Luma's checkout in an
  overlay without leaving the page (`embed.lu.ma/checkout-button.js`, loaded once at the
  bottom of the file).
- **After an event passes:** either point the card at the next event or drop it back to
  `status soon`. Keep registerable events first, then venue-secured cities, then TBD,
  then the dashed **Your city** card last.
- **Your city card:** lists candidate cities (New York, Charlotte, Dublin, Denver,
  South Bay, elsewhere) and links to the contact form. Edit the list as chapters launch.
- **Live calendar embed:** the `<iframe>` at the bottom of the section is Luma's
  calendar embed and updates itself as events are added. Confirm or refresh the `src`
  from Luma → calendar → **Settings → Embed**. `?lt=light` matches the light section.

### Everything else

- **Forms.** Two Google Forms. Speaker proposals: `https://forms.gle/dih1br2x3Vrxh4fo6`.
  Hosting and new cities ("Get in touch", "Host us", "Your city"):
  `https://docs.google.com/forms/d/e/1FAIpQLSfZF3G4AfSoCuAK0vVwZnNinjJtrq1DSPBQqOhtVkXWKuuRHA/viewform`
  (fields: Email, City, Experience & fit).
- **Following on Luma** requires a free Luma account; the same account is needed to register
  for any event, so the site links straight to the calendar page and says so under the button.
- **Talks.** The "Watch past talks" grid has three placeholder cards. Set each `href` to
  a YouTube URL and edit the title and meta. Duplicate an `<a class="talk">` block to add more.
- **Members and hosts.** Logo images live in `assets/`; heights are set inline per logo so
  wordmarks of different proportions sit at the same visual weight. Copy a `.member` or
  `.host` block to add one.
- **Cities chips** in the Format section are a general list; the Meet-ups section is the
  source of truth for what is actually scheduled.
- **Code of Conduct.** The footer links `code-of-conduct.html`; the Markdown source is
  `CODE_OF_CONDUCT.md`.

## Getting listed

Members, hosts, and meet-up cities are added by pull request or by one of the issue forms
under **New issue**, reviewed by a maintainer against the criteria in
[CONTRIBUTING.md](CONTRIBUTING.md#get-listed), and merged with one approval. Search
`index.html` for `TEMPLATE:` to find the copy-paste block for each kind of listing.

## Contributing

This site is maintained by the community. Fork the repo, edit `index.html`, open a pull
request. Because it's a single static file, anyone comfortable with basic HTML can
contribute. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Dual-licensed: **code** under the [Apache License 2.0](LICENSE), **content** (docs, talk
recordings) under [CC BY 4.0](LICENSE-CONTENT.md). Contributions welcome.
