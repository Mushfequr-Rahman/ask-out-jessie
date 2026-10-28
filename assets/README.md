# Magneton artwork

The current Prologue uses 40 unique illustrations in `panels/`, named by page and panel. All speech bubbles and lettering are generated directly inside the artwork. Complete readable source text remains in chapter JSON and the reader transcript.

Panel holders are fixed before generation; each illustration is composed for its assigned aperture. No image loading can resize those holders. The five Type C captains retain sealed silver armour, restrained brass fittings and crimson Veymarch crests; ordinary allies wear bronze over crimson.

The other 16 current assets are six Zeppelin-like ship designs, eight duchy banners, the shattered-Earth atlas and Magneton specimens. The current inventory has 56 images. See [ASSETS.md](../ASSETS.md) or [the asset library](../assets.html) for every file and its usage.

Earlier comic artwork is preserved as generation anchors under [references/](../references/README.md), outside the published current-asset inventory. See [the generation workflow](../docs/image-generation.md) for scene requests, visual bibles, lettering, provenance, review and research sources.

Refresh metadata after changing artwork:

```sh
python3 scripts/build_assets.py
python3 scripts/sync_layout.py
python3 scripts/validate_world.py
python3 scripts/validate_generation.py --require-outputs
```
