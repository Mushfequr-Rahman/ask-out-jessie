# comicbook

An HTML comic project featuring **Magneton** (working story title).

A dependency-free HTML comic book starter. Includes a responsive four-page world-building prologue plus five pages following Duke Rovan Vey, twenty-seven unique comic panel illustrations, all six ships visible on the home page, a comparison glossary, and a Magneton materials guide, accessible reader controls, and keyboard navigation. No build tools, accounts, API keys, or external services are required.

## Run locally

From the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open the site in your local browser on port 8000.

## GitHub hosting

[Read the comic on GitHub Pages](https://mushfequr-rahman.github.io/ask-out-jessie/).

GitHub Pages publishes the `master` branch from the repository root. The `.nojekyll` file serves the HTML and assets directly, with no build tools. Pushing to `master` triggers GitHub's Pages deployment. In repository Settings → Pages, keep **Deploy from a branch**, **master**, and **/ (root)** selected. If the repository is renamed, update this link to the new repository path.

[Compare all six ship designs in the glossary](https://mushfequr-rahman.github.io/ask-out-jessie/glossary.html).

To read the comic, select **Read the Comic** (or open the hosted site at `#reader`), scroll through the panels, then select **Next Page** at the bottom. Previous and arrow keys work too.

The fleet section links each ship image to its full-resolution, GitHub-hosted PNG. Images can also be viewed directly from the repository's `assets/` folder.

## Magneton materials

[Explore Types A, B and C](https://mushfequr-rahman.github.io/ask-out-jessie/magneton.html).

- **Type A:** common, durable, bronze-like metal used for ship hulls.
- **Type B:** glowing green metal in opposing polarities, used in delicate machinery and hull components.
- **Type C:** recently discovered, silvery, most malleable, and hardest to find; impervious to weapons and able to drift through magnetic fields. Rovan secretly crafts exactly five honour-guard armour-and-sword sets.

## Current fleet

The four original ship designs have been retired. The six current designs are:

| Mining | Commuter schooners | Traders | Capital |
| --- | --- | --- | --- |
| [Mole](assets/mining-mole.png) | [Needle](assets/schooner-needle.png), [Kestrel](assets/schooner-kestrel.png) | [Caravan](assets/trader-caravan.png), [Terrace](assets/trader-terrace.png) | [Bastion](assets/capital-bastion.png) |

[Browse all six designs together](https://mushfequr-rahman.github.io/ask-out-jessie/glossary.html).

## Story and world atlas

[Read Chapter One: The Duke’s Due](https://mushfequr-rahman.github.io/ask-out-jessie/?page=5#reader).

[Read Chapter Two: His Own Future](https://mushfequr-rahman.github.io/ask-out-jessie/?page=7#reader).

[Explore the eight-duchy atlas](https://mushfequr-rahman.github.io/ask-out-jessie/glossary.html#world-atlas).

[STORYBOARD-IDEAS.md](STORYBOARD-IDEAS.md) records the selected campaign, first city capture, and five silver honour guards. Unchosen earlier proposals are not story events.

## Make it your comic

- `index.html`: comic title, description, story panels, and page articles.
- `styles.css`: colors, typography, responsive layout, and artwork presentation.
- `script.js`: previous/next controls and arrow-key navigation.
- `glossary.html`: all six ship designs, comparison table, and design notes.
- `glossary.js`: optional ship-class filters; all designs remain visible without JavaScript.
- `magneton.html`: Types A, B, and C, material specimens, properties, and uses.
- `assets/`: place your own artwork here and reference it with relative image paths. Include descriptive alt text.

To add a page, add another `article.comic-page` before the reader controls with a unique ID, a heading connected with `aria-labelledby`, and the `hidden` attribute. Update the initial page count in the HTML; JavaScript calculates subsequent counts automatically. Keep the first page visible so the comic remains readable without JavaScript.

## Verify changes

Serve the root folder and check all nine comic pages, boundary button states, keyboard navigation, and a narrow mobile viewport. Check the browser console for errors. This starter has no package installation, build command, or test runner.

## Story reference

See [STORY.md](STORY.md) for the world premise and details still to develop. Each of the twenty-seven comic panels has its own image. The asset collection also includes the other ship designs and a materials specimen illustration; ship images are intentionally shared between the home gallery and glossary for comparison. Captions stay in HTML so they remain readable and editable. See [assets/README.md](assets/README.md) for the artwork inventory.
