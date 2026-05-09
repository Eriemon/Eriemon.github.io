# Contributing

Thank you for helping keep this academic homepage accurate, readable, and easy to maintain.

## Contribution Scope

Good contributions include:

- Updating publications, projects, news, experience, awards, or contact links.
- Improving bilingual English/Chinese wording while preserving factual accuracy.
- Fixing responsive layout, theme/style behavior, accessibility, or broken links.
- Updating repository documents such as `README.md`, `README-CN.md`, `SECURITY.md`, or `CITATION.cff`.

Please keep changes focused. Avoid broad visual rewrites unless the change has been discussed first.

## Content Guidelines

- Keep public facts current and verifiable.
- Update both English and Chinese text when the same content appears in both languages.
- Use `README-CN.md` for the Chinese README. Do not add `README-CH.md`.
- Do not commit private drafts, tokens, credentials, unpublished personal data, local machine paths, browser cache files, or generated files that are not part of the site.
- External links should use public, stable destinations intended for visitors.

## Style Guidelines

- Preserve the static deployment model: `index.html`, `style-natural.css`, `style-academic.css`, and `script.js`.
- Keep Natural as the default style and Academic as the alternative style.
- Preserve Light/Dark, Academic/Natural, and English/Chinese toggles.
- Use semantic CSS classes for shared UI treatments instead of inline styles when possible.
- Check desktop and mobile layouts after visual changes.

## Local Preview

Run a local static server from the repository root:

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:8765/
```

## Validation Checklist

Before submitting changes, check:

- The homepage loads without console errors.
- There is no horizontal scrolling on desktop or mobile.
- Projects and News display correctly in both Natural and Academic styles.
- English and Chinese language switching updates the edited text.
- Light and Dark modes remain readable.
- External links open as expected.
- Markdown links in `README.md` and `README-CN.md` point to existing files or public URLs.

Run:

```powershell
git diff --check
git status --short
```

## License

By contributing, you agree that your contribution is provided under the repository license, [Apache License 2.0](LICENSE).
