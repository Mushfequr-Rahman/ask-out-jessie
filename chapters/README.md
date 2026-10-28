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
          "caption": "The last war.",
          "priority": 5
        }
      ]
    }
  ]
}
```

Page numbers must start at 1 and run consecutively. Every page must have **1–5 panels**. `image_src` and `caption` are required; captions may be empty. The reader and repository validator enforce this limit. All text is rendered as text, so HTML tags in captions are displayed literally.

Every current panel declares a `priority` integer from **1 to 5**: 1 is a small connective beat, 3 is a normal story beat, and 5 is the page’s main reveal or action. Higher priorities receive more page area, not a new reading position. Older files without the field default to 3; invalid values are rejected.

Optional panel fields:

- `narration`: story prose or dialogue inset over the artwork; use `\n` for a paragraph or a change of speaker. Lines such as `Rovan: “Hold the line.”` render as dialogue balloons.
- `holder`: fixed `{x, y, width, height}` in the 952 × 1,268 panel region. A page with `layout_mode: "fixed"` requires a holder for every panel.
- `lettering_mode`: `baked` for lettering generated in the artwork; `editable_html` for the older text overlay mode. Baked panels hide duplicate HTML text but preserve the transcript.
- `scene_id`: stable generation scene ID.
- `image_fit`: legacy `contain` mode for older artwork. Clicking any image opens the full original.
- `image_alt`: accessible image description (defaults to the caption).
- Legacy `layout` values are accepted for compatibility but no longer position panels. The automatic fixed-canvas algorithm uses image proportions and measured text instead.
- Legacy `full_size_link` is accepted; every illustration now links to its original for full-size viewing.

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

Each page uses the same 1,000 × 1,400 canvas. The priority algorithm can author 1–5 holders; the current chapter locks those rectangles before artwork generation. Runtime uses the saved geometry, independent of image dimensions. New art includes lettering and is composed for the holder aperture. See [the generation workflow](../docs/image-generation.md). The canvas scales uniformly in **Fit width** mode; **Full size** enables native-size scrolling. The separate **Read page text** transcript always uses normal readable text sizes.
