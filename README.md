# Simple GitHub Pages wiki (Pandoc edition)

This repository turns Markdown into a lightweight wiki. Every push to `main` runs a GitHub Actions workflow that builds the site with **Pandoc** and deploys it to GitHub Pages.

## Usage

1. Add Markdown files anywhere in the repository. If you want a custom title, include simple YAML front matter:
   ```markdown
   ---
   title: Page title
   ---
   ```
2. Commit and push to `main`.
3. The workflow builds the site and deploys it. The home page shows a table of contents that indents entries based on folder depth, so deeply nested notes remain readable.

## Local preview

If you want to preview locally without GitHub Actions:

```bash
sudo apt-get update && sudo apt-get install pandoc
python3 scripts/build.py
python3 -m http.server --directory _site 8000
```

Then open [http://localhost:8000](http://localhost:8000) to see the generated site.
