# Generation records

`layout-lock.json` records all published panel rectangles before generation. Runtime uses the identical rectangles in chapter JSON.

`requests/` contains resolved scene requests and focused corrective edits. `runs/` records generation attempts; an attempt is not necessarily the final selected image. `review.json` identifies the selected run, actual PNG dimensions and SHA-256 hash for every published panel.

`source-snapshots/` preserves the input bibles used during generation, before the final asset paths and metadata were installed. Their hashes match the initial run records. The request builder has since gained stronger early-era exclusions and explicit speaker metadata; rebuilding with current inputs may change a prompt. Size hints and request coordinates are planning inputs, not a guarantee of native output dimensions or pixel placement. Early pilot requests informed the source-space lettering correction; corrective requests record the final changes.

Old illustrations used as conditioning references are in `references/panels/`. Intermediate images for corrective edits are in `references/iterations/`. Selected artwork is in `assets/panels/`; full generated originals were also retained in the execution workspace.

Build a new draft without overwriting the reviewed requests:

```sh
python3 scripts/build_image_requests.py --output generation/drafts
```

See [the workflow and research](../docs/image-generation.md).

## House colours and comparisons

New requests default to `drafts/` and reserve canonical house references first. Palette values in `objects.json` are separate from map/UI colours. Use the [banner comparison page](banner-review.html) to review current images beside their house reference and swatches. Rebuild it with `python3 scripts/build_banner_review.py` after changing candidate images, scene affiliations, references or palettes. Export decisions and validate them using `scripts/validate_banner_review.py`; pending and stale decisions cannot pass. No current images were regenerated or automatically marked as matching. See the workflow for the schema-2 publication check.

Page 13 adds three shots to the existing Prologue. Their pre-generation input bibles are archived in `page13-source-snapshots/`. The comparison report for that page records only its new images as reviewed; older panels remain pending under the newer banner-specific criteria.

Page 14 adds the Argonaut’s departure and Shattered Plains strategy. Its pre-generation bibles are in `page14-source-snapshots/`; `page14-banner-review.json` carries forward the checked page-13 decisions and adds page 14.

The Argonaut refit is a standalone reference scene in `scenes/argonaut-refit.json`, with its resolved request in `refit-requests/`. The page-14 before-refit images and original requests are archived under `references/iterations/` and `requests/archives/`; their historical run records point to those archived requests. New selected runs use the completed refit design.

The insertion of **Fourteen Days** shifts the former page14 to page15; renamed scenes and published image paths are recorded through `*-renumber.json` runs that retain their source-run links. New page14 uses the canonical refit image as its second comic panel. Page16 introduces Joseph and the pursuit. Historical page14 records remain archival. `fourteen-days-banner-review.json` is the current banner review; input bibles are preserved in `fourteen-days-source-snapshots/` and `fourteen-days-fleet-source-snapshots/`.

Pages17–18 add nine fixed-holder illustrations for the Josephine diversion and Serenity/Serendipity boarding attacks. `boarding-source-snapshots/` preserves the input bibles. `boarding-banner-review.json` adds their reviewed house markings while retaining older decisions only where hashes still match. The individual captain records are members of `honour-guard`, not extra knights.

Page19 adds five fixed-holder surrender/victory images. `surrender-source-snapshots/` preserves the generation inputs. The ownership change is explicit: earlier ship objects retain their pre-surrender Auric appearance, while `captured-bastions` supplies post-surrender Veymarch prize markings. Plain white flags are surrender signals, not altered house colours. `surrender-banner-review.json` is the current comparison review.

The opening surrender shot was redesigned at the user’s request: more engine smoke and the Argonaut looming over the three white-flag prizes. The earlier shot/request remain archived; the redesign is recorded in `prologue-p19-panel01-smoke-redesign.json`, followed by the selected crop-safe lettering pass `prologue-p19-panel01-lettering.json`.
