# Markdown for Agents — GitHub Action

> Generate Markdown versions of your static pages (plus `llms.txt` and `llms-full.txt`) on every deploy, so AI agents and answer engines can read and cite your site.

Companion to [markdown-for-agents-worker](https://github.com/wu736139669/markdown-for-agents-worker).
This Action handles the **generation** half in CI; the worker (or the static `.md`
files themselves) handles **serving**.

## Usage

```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write        # only needed if you use the commit-back example
    steps:
      - uses: actions/checkout@v4

      # ... your build step that produces ./public ...

      - name: Generate agent-readable Markdown
        uses: wu736139669/markdown-for-agents-action@v1
        with:
          directory: ./public
          base-url: https://example.com
          site-name: Example Tools
          site-description: Free browser tools that never upload your files.

      # ... your deploy step (wrangler deploy, netlify deploy, rsync ...) ...
```

## Inputs

| Input | Required | Default | Description |
| --- | --- | --- | --- |
| `directory` | no | `./public` | Folder containing the built HTML files |
| `base-url` | **yes** | — | Canonical site URL (absolute links + llms.txt) |
| `site-name` | no | — | When set, `llms.txt` is generated |
| `site-description` | no | — | One-line description used in `llms.txt` |
| `full-txt` | no | `true` | Also generate `llms-full.txt` |

## What it produces

For every `page.html` in `directory`:

- `page.md` — clean Markdown (title, description, content; nav/forms/scripts stripped)
- `llms.txt` — index of all pages with descriptions (when `site-name` is set)
- `llms-full.txt` — every page concatenated (when `full-txt: true`)

Then pair it with `Accept: text/markdown` content negotiation
([worker repo](https://github.com/wu736139669/markdown-for-agents-worker)) or simply
link the `.md` files from your pages via
`<link rel="alternate" type="text/markdown" href="/page.md" />`.

## Commit the generated files back (optional)

```yaml
      - name: Commit generated markdown
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          git diff --cached --quiet || git commit -m "chore: regenerate agent markdown"
          git push
```

## Notes

- Review the generated Markdown the first time you enable this — the converter is
  deliberately conservative, and template-driven sites can do better by generating
  `.md` from their own data model.
- Only `GET`s the files it generates; no network calls, no telemetry.

## License

MIT
