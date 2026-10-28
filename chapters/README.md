# Chapter sources

Each published chapter has one JSON file. `prologue.json` is the source for all Prologue pages. Its HTML shell loads `script.js` and declares `data-chapter-src="chapters/prologue.json"` on `#reader`. Image paths are relative to that HTML shell at the repository root.

```json
{
  "title": "Prologue",
  "pages": [
    {
      "Page Number": 1,
      "Title": "The fracture",
      "panels": [
        {
          "image_src": "assets/fracture.png",
          "caption": "THE NUCLEAR WAR DID NOT END WITH RUINS."
        }
      ]
    }
  ]
}
```

Page numbers must start at 1 and run consecutively. Every page must have **1–7 panels**. `image_src` and `caption` are required; captions may be empty. The reader and repository validator enforce this limit. All text is rendered as text, so HTML tags in captions are displayed literally.

Optional panel fields:

- `narration`: text below the caption; use `\n` for a line break.
- `image_alt`: accessible image description (defaults to the caption).
- `layout`: CSS class names, such as `["chapter-panel", "wide"]`. Without it, panels use the default two-column grid; the first panel spans both columns when the count is odd.
- `full_size_link`: `true` wraps the image in a link to the original.

Optional page field `footer` sets the printed footer label. Otherwise the reader uses the chapter and page titles.

After editing chapter JSON, run from the repository root:

```sh
python3 scripts/build_assets.py
python3 scripts/sync_layout.py
python3 scripts/validate_world.py
```

The asset script automatically syncs chapter pages into `world.json` before refreshing the catalogues. Edit the chapter JSON rather than the derived `world.json` story pages. To sync only those story records, run `python3 scripts/sync_chapters.py`.

For a future chapter, copy the Prologue HTML shell, update its title/description and `data-chapter-src`, create its JSON, and register its `json_file` and `reader` in `world.json` under `publication.stories`. Add the chapter to the Chapters menu and the shared-layout script when it is ready to publish.

Serve the site over HTTP (for example, `python3 -m http.server 8000`). Fetching chapter JSON requires HTTP; opening the HTML directly from disk is unsupported. GitHub Pages serves these JSON files without a build step.
