# comicbook

A dependency-free HTML comic project featuring **Magneton**.

## Read online

- [Chapters](https://mushfequr-rahman.github.io/ask-out-jessie/chapters.html): one available story, **Prologue**.
- [Read Prologue](https://mushfequr-rahman.github.io/ask-out-jessie/prologue.html): all ten existing illustrated pages, including Rovan's rise, the five silver honour guards, and Auric Reach's response on page 10.
- [Glossary](https://mushfequr-rahman.github.io/ask-out-jessie/glossary.html): metals, ships, eight duchies and banners, people, and world terms.
- [Asset library](https://mushfequr-rahman.github.io/ask-out-jessie/assets.html): all 45 original artwork files; linked from the glossary.
- [Repository asset catalogue](ASSETS.md) and [world.json](world.json): artwork inventory and structured world reference.

Every page uses the same two navigation links: **Chapters** and **Glossary**. The Chapters menu is also the home page. There are no other published story entries yet. The Prologue's ten pages retain all 30 unique panel illustrations.

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
- `prologue.html`: ten-page reader with a page selector, previous/next controls, and keyboard navigation.
- `glossary.html`: the consolidated reference page and all eight duchy banners.
- `magneton.html`: legacy link forwarding to the metals section of the glossary.
- `assets.html` / `ASSETS.md`: browsable website and repository artwork catalogues.
- `world.json`: all current lore, metals, ships, duchies, characters, chronology, story panels, unknown details, and asset metadata.
- `scripts/build_assets.py`: refreshes asset metadata and both catalogues without changing artwork.
- `partials/header.html` and `partials/footer.html`: shared site navigation and footer.
- `scripts/sync_layout.py`: refreshes shared layout in the checked-in static HTML.
- `site.js`: preserves old bookmarks; `script.js`: comic reader; `glossary.js`: ship-class filters.
- `styles.css`: shared visual design; `assets/`: illustrations and banners.
- `STORY.md`: current lore; `STORYBOARD-IDEAS.md`: selected story direction and open decisions.

After editing a shared layout partial, run:

```sh
python3 scripts/sync_layout.py
```

The generated HTML is checked in, so serving or publishing does not require this command. Add future stories to the Chapters menu only when they are ready to read.

## Verification

Check the two shared navigation links and active states on all pages, the single Prologue entry, all ten reader pages, the page selector, all 30 unique panel images, glossary section links and ship filters, eight distinct colours and banners, and mobile layouts. Old `index.html?page=7#reader`, `index.html#fleet`, and `magneton.html#type-c` bookmarks should forward to the new structure.

## World and asset maintenance

Keep `world.json` current when author-established lore changes. It separates established facts from provisional visual designs and explicitly records unknown details. It includes all ten story pages, their captions and narration, and asset references. The glossary remains checked-in HTML; lore edits should also be reflected there and in `STORY.md`.

After changing artwork, refresh the metadata and catalogues:

```sh
python3 scripts/build_assets.py
python3 scripts/sync_layout.py
python3 scripts/validate_world.py
```

The asset script inventories the actual files and records dimensions, file sizes, SHA-256 hashes, and comic usage in `world.json`. It also writes `ASSETS.md` and `assets.html`. Regeneration is optional for serving because the generated files are committed. It never changes image contents. The asset library uses the same two-tab header and is reached from the Glossary tab.
