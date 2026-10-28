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
