# Contributing

Thanks for helping build the AI in Cyber Alliance website! This site is **maintained by
the community**, and contributions are welcome from anyone — no special tooling required.

## What you can contribute

- Fix a typo, link, or piece of copy
- Add a past talk (title + YouTube link)
- Add or update a member / host
- Add a blog post
- Improve the design, accessibility, or responsiveness

## How it works

The whole site is a single, plain HTML file: [`index.html`](index.html). There's **no
build step and no framework** — just open it in a browser to preview your change.

1. **Fork** this repository.
2. **Edit** the files:
   - Site content, links, colors → `index.html` (search for `EDIT:` to find the spots
     that need real values; colors/fonts are CSS variables in the `:root` block at the
     top of the `<style>` section).
   - Blog posts → add a Markdown file under [`blog/`](blog/).
3. **Preview** by opening `index.html` in your browser.
4. **Open a pull request** with a short description of your change.

A maintainer will review and merge. Once merged, the live site updates automatically.

## Common edits

| I want to… | Where |
|---|---|
| Add the speaker / host Google Form link | `index.html` — the `EDIT:` comments (nav + "Get involved") |
| Add a past talk | `index.html` — duplicate an `<a class="talk">` card, set the YouTube `href` |
| Add a member or host | `index.html` — copy a `.member` / `.host` block |
| Change the brand color | `index.html` — `--acc` in the `:root` CSS variables |
| Write a blog post | new `.md` file in `blog/` |

## Ground rules

- Be respectful and constructive — see our [Code of Conduct](CODE_OF_CONDUCT.md).
- Keep the site **community-first**: no product pitches or marketing copy.
- Keep it simple — this is intentionally a dependency-free static site. Please don't add
  a build system, framework, or package manager.

## Licensing

By contributing, you agree that your contributions are licensed under the project's
terms: **code** under the [Apache License 2.0](LICENSE), and **content** (blog, docs)
under [CC BY 4.0](LICENSE-CONTENT.md).
