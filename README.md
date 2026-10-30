# comicbook

A dependency-free HTML comic project featuring **Magneton**.

## Read online

- [Chapters](https://mushfequr-rahman.github.io/ask-out-jessie/chapters.html): one available story, **Prologue**.
- [Read Prologue](https://mushfequr-rahman.github.io/ask-out-jessie/prologue.html): all twenty-four illustrated pages, including Rovan's rise, the five silver honour guards, and Auric Reach's response on page 12.
- [Glossary](https://mushfequr-rahman.github.io/ask-out-jessie/glossary.html): metals, ships, eight duchies and banners, people, and world terms.
- [Asset library](https://mushfequr-rahman.github.io/ask-out-jessie/assets.html): all 99 current artwork files; linked from the glossary.
- [Repository asset catalogue](ASSETS.md), [world.json](world.json) and [character.json](character.json): artwork inventory, world reference and character records.

Every page uses the same two navigation links: **Chapters** and **Glossary**. The Chapters menu is also the home page. There are no other published story entries yet. The Prologue's twenty-four pages contain 83 unique regenerated panel illustrations.

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
- `character.json`: all character records, including Rovan, Grievous, the five Silver Guard captains and Auric Reach’s unnamed ruler.
- `world.json`: world lore, metals, ships, duchies, chronology, story panels, unknown details, asset metadata and a `characters_file` reference to `character.json`.
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

Check the two shared navigation links and active states on all pages, the single Prologue entry, all twenty reader pages, the page selector, all 83 unique panel images, glossary section links and ship filters, eight distinct colours and banners, and mobile layouts. Old `index.html?page=7#reader`, `index.html#fleet`, and `magneton.html#type-c` bookmarks should forward to the new structure.

## World and asset maintenance

Edit comic pages in `chapters/prologue.json`; `script.js` renders their images at runtime and keeps the full source text in an accessible transcript. Both the browser and repository checks reject pages containing more than five panels. Keep `world.json` current when author-established lore changes. It separates established facts from provisional visual designs and explicitly records unknown details. Its story pages, captions, narration and asset references are derived from chapter JSON by the asset script. The glossary remains checked-in HTML; lore edits should also be reflected there and in `STORY.md`.

After changing artwork, refresh the metadata and catalogues:

```sh
python3 scripts/build_assets.py
python3 scripts/sync_layout.py
python3 scripts/validate_world.py
```

The asset script first validates and syncs each chapter JSON into the world reference, then inventories the actual files and records dimensions, file sizes, SHA-256 hashes, and comic usage in `world.json`. It also writes `ASSETS.md` and `assets.html`. Regeneration is optional for serving because the generated files are committed. It never changes image contents. The asset library uses the same two-tab header and is reached from the Glossary tab.

## Fixed comic pages

Every page has a 1,000 × 1,400 logical canvas. Each panel in chapter JSON has a `priority` from 1 to 5. `panel-layout.js` evaluates ordered row arrangements, allocates space by priority, measures the story text, and balances image proportions against the requested emphasis. Major reveals and action shots receive more area; smaller beats connect them without changing reading order. The algorithm supports up to five images on a page.

The current chapter stores fixed `holder` rectangles before generation. New artwork is composed for those rectangles, including its speech bubbles and lettering. The renderer fills each holder proportionally; a planned central aperture protects lettering where a provider cannot output the exact aspect ratio. Image loading never changes the holders. **Full size** shows the native canvas in a scrollable viewport; **Read page text** provides the complete story at normal text sizes. Click any panel image to open its uncropped original.

The Silver Guard have their own introduction on page 9. Page 10 follows the troops entering town, page 11 shows the captains’ assault, and page 12 contains the rival’s response.

The Silver Guard’s current armour includes restrained brass fittings and Veymarch’s silver broken-shield-and-star badge on crimson enamel. Chapter prose is edited for scene progression and natural dialogue; all lore and asset references remain in `world.json`.

## Character records

Edit character identities, appearances, motivations and equipment in `character.json`. It contains a `characters` array with stable IDs. `world.json` points to it through `characters_file`; references such as `ruler_id`, `target_character_id` and `exclusive_expert_id` still use those IDs. Character records are not duplicated in the world file. The Silver Guard have one group record with five visual profiles and five linked member records identified by their titles. Their personal names remain unestablished.

Run `python3 scripts/validate_world.py` after editing either file to check character IDs, duchy links, crafting experts, weapon references and artwork references.

## Image requests and visual references

`objects.json` stores 26 reusable visual specifications for metals, ships, uniforms, weapons and banners. `scenes/prologue.json` supplies individual shots, references and lettering. Build reviewable image requests with:

```sh
python3 scripts/build_image_requests.py
python3 scripts/test_image_requests.py
python3 scripts/validate_generation.py --require-outputs --banner-review generation/rule-banner-review.json
```

The request builder takes scene + world.json + character.json + objects.json. It writes prompts rather than calling a paid API. All 83 selected outputs are already committed under `assets/`. Earlier anchors are retained under `references/`; generation requests and run metadata record provenance. See [the generation workflow and official research sources](docs/image-generation.md) for reference conditioning, exact lettering, fixed apertures and the MongoDB assessment. JSON remains the storage layer for this static site.

## Banner consistency

The generation builder gives canonical house banners precedence over older scene references and uses dedicated cloth/emblem/trim palettes from `objects.json`. The map/UI colours remain separate. [Compare banners and panels side by side](generation/banner-review.html); the review tool saves decisions locally and exports versioned JSON. Regenerate the comparison with `python3 scripts/build_banner_review.py`. Future schema-2 artwork with house references requires a complete exported review during output validation. See [the workflow](docs/image-generation.md#banner-consistency-framework) for commands and review rules. Existing artwork is unchanged.

Page 13, **Three Bastions**, follows a schooner courier’s warning, Rovan’s council with Grievous and all five captains, and their decision to face the approaching enemy head-on. The battle itself remains ahead.

Page 15, **The Shattered Plains**, names Rovan’s capital ship the **Argonaut**, shows its departure under the city’s doubts, and reveals the difficult terrain he chooses to split the three enemy Bastions.

The [Argonaut refit illustration](assets/argonaut-refit.png) shows Rovan investing captured wealth in his flagship. Its canonical ship anchor is stored in `objects.json` and reserved before older scene references in future generation requests. The [glossary](glossary.html#argonaut-refit) describes the upgrades.

Page 14, **Fourteen Days**, shows Rovan and his engineers using captured resources to install huge heavy cannons during the Argonaut’s legendary fourteen-day refit. The former page 14 is now page 15. Page 16 introduces **Admiral Joseph**, who ignores crew warnings in pursuit of a duchy and sends all three Bastions after the Argonaut into the Shattered Plains.

Pages 17–18 show the Argonaut splitting Josephine, Serenity and Serendipity in the Shattered Plains, distracting Josephine and sending two boarding teams against the other ships. `character.json` now gives the same five captains individual title records: Stormlance, Windblade, Bulwark, Riftwalker and Hullbreaker. Their personal names remain unknown.

Page 19, **Three Prizes**, shows all three Bastions capitulating, their crews surrendering, Joseph’s overboard sentence, Rovan taking the ships in hand, and the soldiers celebrating the first-ever capture of enemy capitals. He now owns four capitals including Argonaut, with repairs still needed on the prizes.

Page 20, **New Frontier**, returns the four-ship fleet to the conquered harbour. Rovan names it his foothold for the Auric campaign, discusses the opportunity with Grievous, and welcomes volunteers from Auric Reach and Veymarch. Repair crews restore the prizes and repaint them crimson without changing their standard Bastion hulls. Captain Mara Voss commands Josephine, Captain Idris Vale commands Serenity, and Captain Tomas Kest commands Serendipity. These are naval commands, distinct from the five silver knights. The fleet departs for Oram, Auric Reach’s capital; it has not arrived there.

Page 21, **The Siege of Oram**, introduces Auric Reach’s capital as the largest and richest city in the world, with access to most farmland. Rovan’s four capital ships overlook it while supply convoys run between New Frontier and the siege fleet. The Argonaut opens fire and bewildered civilians take cover. Oram remains under Auric Reach’s control; no surrender or conquest is shown.

Page 22, **The Fall of Oram**, continues the four-ship bombardment, with the ships spread above the city and explosions among its buildings. Rovan sends a messenger to Duke Ferdinand, the previously unnamed ruler of Auric Reach. Ferdinand confers with his barons and surrenders Oram. The surrender is of the city; the fate of the rest of the duchy and any terms remain unestablished.

Page 23, **The Price of Rule**, follows Rovan’s quiet entry into Oram and the handover of keys. He exiles the older bald grey-bearded baron, brings dockworkers and farmers into a local council, and orders grain access, wages and paid repairs. These are first attempts at fairer government, with no guarantee of success.

Page 24, **Too Much to Hold**, shows the administrative strain and Ironveil and Glassmere moving toward exposed Auric mining rocks and trade moorings. Rovan meets Grievous and the three naval captains—Mara Voss, Idris Vale and Tomas Kest—to ask what they can defend. They have four capital ships; no response or new conquest is decided yet.
