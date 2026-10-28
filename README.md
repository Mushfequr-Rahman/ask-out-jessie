# comicbook

A dependency-free HTML comic project featuring **Magneton**.

## Read online

- [Chapters](https://mushfequr-rahman.github.io/ask-out-jessie/chapters.html): one available story, **Prologue**.
- [Read Prologue](https://mushfequr-rahman.github.io/ask-out-jessie/prologue.html): all twelve existing illustrated pages, including Rovan's rise, the five silver honour guards, and Auric Reach's response on page 12.
- [Glossary](https://mushfequr-rahman.github.io/ask-out-jessie/glossary.html): metals, ships, eight duchies and banners, people, and world terms.
- [Asset library](https://mushfequr-rahman.github.io/ask-out-jessie/assets.html): all 52 current artwork files; linked from the glossary.
- [Repository asset catalogue](ASSETS.md) and [world.json](world.json): artwork inventory and structured world reference.

Every page uses the same two navigation links: **Chapters** and **Glossary**. The Chapters menu is also the home page. There are no other published story entries yet. The Prologue's twelve pages retain all 37 unique panel illustrations.

## Run locally

From this repository:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

No package installation, API keys, or build tools are required. GitHub Pages publishes the `master` branch from `/ (root)` using `.nojekyll`. Pushing to `master` triggers deployment.

## Duchy colours and banners

| Duchy | Colour | Banner emblem |
| --- | --- | --- |
| Veymarch | Crimson | Silver broken shield and star |
| Auric Reach | Gold | Merchant's balance within a coin |
| Ironveil | Steel | Silver hammer and anvil |
| Glassmere | Cyan | White crystal prism |
| Stormholt | Violet | Silver lightning bolt and ring |
| Emberfall | Orange | Dark flame and golden ember |
| Verdant Crown | Emerald | Golden crown of leaves |
| Pale Meridian | Ivory | Midnight compass star |

The map and banner key use the same colour assignments, with names and numbers so identification does not depend on colour alone. Full-size banners open from the glossary. The eight duchies are listed in `data/duchies.json`.

## Project structure

- `index.html`: home alias of the Chapters menu, with support for old reader links.
- `chapters.html`: story menu; only Prologue is available.
- `prologue.html`: reader shell that loads `chapters/prologue.json`, with a page selector, previous/next controls, and keyboard navigation.
- `chapters/*.json`: one source per chapter; page number, title and up to five panels per page. See [chapter format](chapters/README.md).
- `scripts/sync_chapters.py`: validates chapter JSON and syncs its derived story records into `world.json`.
- `glossary.html`: the consolidated reference page and all eight duchy banners.
- `magneton.html`: legacy link forwarding to the metals section of the glossary.
- `assets.html` / `ASSETS.md`: browsable website and repository artwork catalogues.
- `world.json`: all current lore, metals, ships, duchies, characters, chronology, story panels, unknown details, and asset metadata.
- `scripts/build_assets.py`: refreshes asset metadata and both catalogues without changing artwork.
- `partials/header.html` and `partials/footer.html`: shared site navigation and footer.
- `scripts/sync_layout.py`: refreshes shared layout in the checked-in static HTML.
- `site.js`: preserves old bookmarks; `script.js`: comic reader; `glossary.js`: ship-class filters.
- `panel-layout.js`: fixed-canvas panel packing algorithm; tested with `node scripts/test_panel_layout.cjs`.
- `styles.css`: shared visual design; `assets/`: illustrations and banners.
- `STORY.md`: current lore; `STORYBOARD-IDEAS.md`: selected story direction and open decisions.

After editing a shared layout partial, run:

```sh
python3 scripts/sync_layout.py
```

The shared layout is checked in; chapter content is rendered in the browser from its JSON. Serving or publishing needs no build step. Add future stories to the Chapters menu only when they are ready to read.

## Verification

Check the two shared navigation links and active states on all pages, the single Prologue entry, all twelve reader pages, the page selector, all 37 unique panel images, glossary section links and ship filters, eight distinct colours and banners, and mobile layouts. Old `index.html?page=7#reader`, `index.html#fleet`, and `magneton.html#type-c` bookmarks should forward to the new structure.

## World and asset maintenance

Edit comic pages in `chapters/prologue.json`; `script.js` renders their images and text at runtime. Both the browser and repository checks reject pages containing more than five panels. Keep `world.json` current when author-established lore changes. It separates established facts from provisional visual designs and explicitly records unknown details. Its story pages, captions, narration and asset references are derived from chapter JSON by the asset script. The glossary remains checked-in HTML; lore edits should also be reflected there and in `STORY.md`.

After changing artwork, refresh the metadata and catalogues:

```sh
python3 scripts/build_assets.py
python3 scripts/sync_layout.py
python3 scripts/validate_world.py
```

The asset script first validates and syncs each chapter JSON into the world reference, then inventories the actual files and records dimensions, file sizes, SHA-256 hashes, and comic usage in `world.json`. It also writes `ASSETS.md` and `assets.html`. Regeneration is optional for serving because the generated files are committed. It never changes image contents. The asset library uses the same two-tab header and is reached from the Glossary tab.

## Fixed comic pages

Every page has a 1,000 × 1,400 logical canvas. Each panel in chapter JSON has a `priority` from 1 to 5. `panel-layout.js` evaluates ordered row arrangements, allocates space by priority, measures the story text, and balances image proportions against the requested emphasis. Major reveals and action shots receive more area; smaller beats connect them without changing reading order. The algorithm supports up to five images on a page.

Every image is proportionally resized and centred within its assigned panel, with space left for cream narration boxes and dialogue balloons. A uniform scale-and-translate transform preserves the entire illustration without cropping or stretching. **Full size** shows the native canvas in a scrollable viewport; **Read page text** provides the complete story at normal text sizes. Click any panel image to open its uncropped original.

The Silver Guard have their own introduction on page 9. Page 10 follows the troops entering town, page 11 shows the captains’ assault, and page 12 contains the rival’s response.

The Silver Guard’s current armour includes restrained brass fittings and Veymarch’s silver broken-shield-and-star badge on crimson enamel. Chapter prose is edited for scene progression and natural dialogue; all lore and asset references remain in `world.json`.
