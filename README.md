# comicbook

An HTML comic project featuring **Magneton** (working story title).

A dependency-free HTML comic book starter. Includes a responsive four-page world-building prologue, generated panel illustrations, accessible reader controls, and keyboard navigation. No build tools, accounts, API keys, or external services are required.

## Run locally

From the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open the site in your local browser on port 8000. Any static hosting service can serve this folder, including GitHub Pages (select the branch containing this project and the root folder).

## Make it your comic

- `index.html`: comic title, description, story panels, and page articles.
- `styles.css`: colors, typography, responsive layout, and artwork presentation.
- `script.js`: previous/next controls and arrow-key navigation.
- `assets/`: place your own artwork here and reference it with relative image paths. Include descriptive alt text.

To add a page, add another `article.comic-page` before the reader controls with a unique ID, a heading connected with `aria-labelledby`, and the `hidden` attribute. Update the initial page count in the HTML; JavaScript calculates subsequent counts automatically. Keep the first page visible so the comic remains readable without JavaScript.

## Verify changes

Serve the root folder and check all four comic pages, boundary button states, keyboard navigation, and a narrow mobile viewport. Check the browser console for errors. This starter has no package installation, build command, or test runner.

## Story reference

See [STORY.md](STORY.md) for the world premise and details still to develop. The panels use six generated illustrations in a consistent graphic novel style, with selected scenes reused across the four-page prologue. Captions stay in HTML so they remain readable and editable. See [assets/README.md](assets/README.md) for the artwork inventory.
