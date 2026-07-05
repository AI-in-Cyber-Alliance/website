# AI in Cyber Alliance — website

The public website for the **AI in Cyber Alliance** — a community-led, vendor-neutral
group running technical meet-ups across the US on AI, cybersecurity, Cloud Native, and
open source. Two 20-minute talks, real Q&A, no product pitches.

🔗 Calendar: https://luma.com/calendar/cal-PWZSiCpJoPE914l
🔗 LinkedIn: https://www.linkedin.com/groups/17875019/

## What's in this repo

```
index.html            The entire website — one self-contained file (fonts + code inlined)
blog/                 Blog posts (Markdown)
CODE_OF_CONDUCT.md    Community Code of Conduct
LICENSE               Apache License 2.0 (code)
LICENSE-CONTENT.md    CC BY 4.0 (blog, docs, recordings)
README.md             This file
```

That's it. `index.html` has **no external dependencies** — open it in any browser and it
just works. Hosting is as simple as serving this folder.

## Editing the site

Everything is in `index.html`. Common edits:

- **Speaker / host / member links** — search for `href="#"` and replace with your
  Google Form URL (three spots in the "Get involved" section, plus "Propose a talk"
  in the nav).
- **Code of Conduct link** — the footer links `#`; point it at `CODE_OF_CONDUCT.md`.
- **Talks** — the "Watch past talks" grid has three placeholder cards; swap the
  `href="#"` for YouTube URLs and edit the titles.
- **Members / hosts / logos** — text wordmarks today; drop in real logo `<img>`s.
- **Hero photo** — replace the `[ event photo / community shot ]` placeholder block.

Save, commit, push — the change is live.

> Note: `index.html` is a compiled bundle. The editable source lives in the design
> project; regenerate the bundle there if you make large structural changes. Small
> content/link edits are safe to make directly in `index.html`.

## Hosting

Any static host works (Cloudflare Pages, Cloudflare Workers static assets, GitHub
Pages, Netlify, S3…). Point it at this folder and serve `index.html`.

## License

Dual-licensed: **code** under the [Apache License 2.0](LICENSE), **content** (blog,
docs, talk recordings) under [CC BY 4.0](LICENSE-CONTENT.md). Contributions welcome.
