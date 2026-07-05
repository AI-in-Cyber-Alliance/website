# AI in Cyber Alliance — website

The public website for the **AI in Cyber Alliance** — a community-led, vendor-neutral
group running technical meet-ups across the US on AI, cybersecurity, Cloud Native, and
open source. Two 20-minute talks, real Q&A, no product pitches.

🔗 Calendar: https://luma.com/calendar/cal-PWZSiCpJoPE914l
🔗 LinkedIn: https://www.linkedin.com/groups/17875019/

## What's in this repo

```
index.html            The entire website — one plain, hand-editable HTML file
blog/                 Blog posts (Markdown)
CODE_OF_CONDUCT.md    Community Code of Conduct
CONTRIBUTING.md       How to contribute (fork → edit → PR)
LICENSE               Apache License 2.0 (code)
LICENSE-CONTENT.md    CC BY 4.0 (blog, docs, recordings)
README.md             This file
```

That's it. `index.html` is plain HTML with one `<style>` block and no build
step, no framework, and no external dependencies.
Open it in any browser to preview; serve to host.

## Editing the site

Everything is in `index.html` — readable, commented, and safe to edit by hand. No
compile step: change it, open it in a browser to check, commit, done. Search the file
for `EDIT:` to find every spot that needs a real value.

- Colors & fonts — change the CSS variables in the `:root` block at the top of the
  `<style>` section (e.g. `--acc` is the brand green). One edit re-themes the whole page.
- Speaker / host / member links — search for `href="#"` and replace with 
  Google Form URL (three spots in the "Get involved" section, plus "Propose a talk"
  in the nav).
- Code of Conduct link — the footer links `CODE_OF_CONDUCT.md`; adjust if you move it.
- Talks — the "Watch past talks" grid has three placeholder cards; set each `href`
  to a YouTube URL and edit the title/meta. Duplicate a `<a class="talk">` block to add more.
- Members / hosts / logos — text wordmarks today; drop in real logo `<img>`s.
- Hero photo — replace the `[ event photo / community shot ]` placeholder block.

## Contributing

This site is meant to be maintained by the community. Fork the repo, edit `index.html`
(or add a post under `blog/`), and open a pull request. Because it's a single static
file, anyone comfortable with basic HTML can contribute — no tooling required.

## License

Dual-licensed: **code** under the [Apache License 2.0](LICENSE), **content** (blog,
docs, talk recordings) under [CC BY 4.0](LICENSE-CONTENT.md). Contributions welcome.
