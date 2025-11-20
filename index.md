# Project wiki

This site renders all Markdown files in the repository into a simple GitHub Pages site using Pandoc and GitHub Actions. Add new Markdown files anywhere in the tree—they will be built automatically on the next push.

## Table of contents

<!-- TABLE_OF_CONTENTS -->

## How it works

* Every Markdown file in the repo (except this index) is converted to HTML with Pandoc.
* A GitHub Actions workflow builds the site and publishes it with GitHub Pages on each push to the `main` branch.
* Use front matter (`---` blocks) in your Markdown files to set titles or other metadata.

## Creating new pages

1. Create a new Markdown file anywhere in the repository. Use a front matter block to set the page title:

   ```markdown
   ---
   title: New page title
   ---

   Your content here.
   ```
2. Commit and push to `main`. The workflow will rebuild and deploy the site.
3. Your new page automatically appears in the table of contents above, indented based on its folder depth.
