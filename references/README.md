# Generation references

`panels/` preserves the prior panel art as stable scene/character anchors for the regeneration pipeline. These files are inputs, not the current comic illustrations. `iterations/` preserves a first pass when a focused correction is needed. Keep references stable; update a scene's reference role explicitly when a visual design is approved.

Current selected art lives in `assets/panels/` and is listed in the asset catalogue. Reusable object appearances live in `objects.json`; character anchors are declared in `character.json`.
