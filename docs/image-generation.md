# Consistent comic image generation

The page is designed first. Its panel holders and lettering coordinates are saved before any image is generated. Artwork is then composed for those immutable apertures; loading a new image must never trigger a new layout.

## Request contract

The reusable template is [`templates/image-request.json`](../templates/image-request.json). The builder accepts the scene, `world.json` and `character.json`, plus the new reusable visual-object bible `objects.json`:

```sh
python3 scripts/build_image_requests.py \
  --scene scenes/prologue.json \
  --world world.json \
  --characters character.json \
  --objects objects.json
```

A scene file may contain one scene or a `scenes` array. Each scene specifies an action, character/object IDs, a fixed holder, reference-image roles, and exact lettering blocks. The output is one reviewable JSON request per panel in `generation/requests/`. `index.json` lists them. Scene descriptions are shot instructions; published captions and dialogue stay in chapter JSON.

Requests include:

- the target holder dimensions and aspect ratio;
- a model-size hint and the visible aperture within a native output;
- selected world, character and object facts, rather than the entire unrelated asset catalogue;
- explicitly numbered visual references and what each preserves;
- exact caption, narration and speech text, with holder-space and source-space positions;
- count, clothing, heraldry, material and weapon invariants;
- visual-review checks and hashes of the source bibles.

`world.json` remains the source of world lore. `character.json` owns character records. `objects.json` owns reusable visual specifications and reference images, with `world_reference` JSON pointers back to technical lore where applicable. It covers materials, ships, weapons, uniforms and all eight banners.

## Lettering is part of the image

The requested mode is **baked lettering**: speech balloons, captions and their words are generated directly in the artwork. The renderer hides its duplicate HTML lettering for those panels. The complete source text is still available in the accessible “Read page text” transcript.

Speech text is supplied literally, separately from the shot description. Speaker prefixes used in the transcript are not printed inside the balloon. Text position is part of the request. For a wide aperture, source-space positions must account for the model's native aspect ratio so a later aperture display cannot remove the lettering.

## Research and the choices used here

Primary sources were read from the providers' official GitHub repositories because direct documentation hosts were blocked by the environment's network policy. These are practical prompting recommendations, not a guarantee of identical results between runs.

1. **Reuse a character anchor.** OpenAI's [image-model prompting guide, character-consistency workflow](https://github.com/openai/openai-cookbook/blob/a8132ca2f7a5de3a6cf15d9e79d172787b42b697/examples/multimodal/image-gen-models-prompting-guide.ipynb) recommends establishing appearance, proportions, outfit and tone, then reusing that anchor for new actions. This project supplies stable archived Rovan/Grievous and Silver Guard references alongside each previous scene.
2. **State what changes and what stays.** The same guide recommends explicit composition, body framing, object interactions and invariant lists. Every request repeats the metal colours, house crest, ordinary-troop uniforms and exact ship/guard counts relevant to the shot. The silver lineup reference is a wardrobe anchor; it is not permission to add five guards to a single-captain scene.
3. **Use clear visual beats.** OpenAI's [GPT Image 1.5 guide, story-to-comic section](https://github.com/openai/openai-cookbook/blob/a8132ca2f7a5de3a6cf15d9e79d172787b42b697/examples/multimodal/image-gen-1.5-prompting_guide.ipynb) recommends one concrete action per panel. The scene records describe framing and action; plot narration is not used as a vague substitute for a shot.
4. **Specify literal lettering and placement.** Both guides recommend quoting exact text and constraining typography and layout. The requests distinguish source transcript text from the words printed in a speech balloon, reserve its position, and ask for readable dark lettering on pale backgrounds. Generated spelling, punctuation and tails still require visual review.
5. **Iterate on a narrow defect.** The guides recommend focused corrections over repeatedly rewriting an overloaded prompt. `generation/requests/corrections/` and `references/iterations/` retain corrective passes, for example moving lettering inside a panoramic aperture.
6. **Respect the provider's size limits.** The newer official guide documents flexible GPT Image 2 sizes: edges in multiples of 16, long/short ratio at most 3:1, under 3,840 pixels per edge and between 655,360 and 8,294,400 pixels total. The builder uses a roughly one-megapixel hint within those constraints. The available image tool does not expose a separate `size` argument, so a prompt's pixel request is a hint, not an asserted output size. Native PNG dimensions and aperture fit are checked after generation. A holder wider than 3:1 needs a correctly planned central aperture with all lettering and essential action inside it.

Useful starting point: use the same model/style, the same approved anchor files and stable descriptions; change the scene, pose and camera deliberately. Do not assume a seed or a phrase such as “same character” guarantees identity. Review the resulting picture.

## Review and provenance

`scenes/prologue.json` and the chapter's `holder` values record the pre-generation layout. `generation/runs/` records attempts and their source hashes. `generation/review.json` selects the published run for each panel with actual dimensions and a content hash. Pre-migration input bibles are retained in `generation/source-snapshots/`; current root files include the final publication metadata. Build future drafts with `--output generation/drafts` to preserve reviewed requests. The saved original image files in the execution workspace are retained, and the selected copies are checked into `assets/panels/`. See [the provenance notes](../generation/README.md) for pilot and corrective passes.

Before publishing, compare the rendered panel with its request: faces/outfits, the full five-captain lineup, weapon effects, Type B green cores, exactly three opposing capital ships, and literal lettering. Geometric and reference tests cannot prove the spelling of pixels or artistic identity; the source transcript remains authoritative.

## MongoDB assessment

For the current workload, **keep the checked-in JSON files**. The comic is a static GitHub Pages site with versioned lore and artwork, not a shared writing application. A database would require a separately hosted API, authentication and an editing workflow; GitHub Pages cannot run that server. No MongoDB credentials or client connection belong in the static reader.

MongoDB's official [Identify Application Workload](https://github.com/mongodb/docs/blob/d486fe3554401973c692d2859a11678cd7d4c696/content/manual/manual/source/data-modeling/schema-design-process/identify-workload.txt) guidance says schema design should follow actual frequent operations. This project's current operations are chapter reads, reviewed file edits and generated-asset commits. A database is not needed to support them.

If a shared editor or generation queue is added, MongoDB would be a reasonable authoring backend:

| Collection | Data and access pattern |
| --- | --- |
| `worlds` | A versioned world bible, read when creating requests. |
| `characters` | Stable character IDs, approved appearance and references. |
| `objects` | Stable IDs and reusable visual specifications. |
| `chapters` | Embedded pages/panels with at most five panels; fixed holders and lettering. |
| `generation_jobs` | Scene/version, request and source hashes, status, image path and review result. |

Use unique IDs per world, a unique scene/version or request-hash key for jobs, and an index on job status/update time for a worker queue. Store image files in object storage/CDN, with their paths and hashes in MongoDB. Publish a validated static JSON snapshot to this repository so reading the comic does not depend on the authoring database. This is a future architecture recommendation; no database service has been provisioned for the static site.

## Banner consistency framework

Future requests use schema version 2. Published requests and their historical source snapshots remain intact; new requests default to `generation/drafts/`.

1. **Reference precedence.** The builder resolves house affiliations from explicit banner objects, characters and uniform objects. It reserves the first image slots for every relevant canonical banner, before scene, character and ship references. Each input has an explicit role: canonical banners override older scene/character heraldry. The four-reference budget supports two houses plus scene and character anchors; a larger house cast fails with instructions to split the shot or author a combined reference sheet, rather than silently dropping a banner. A house reference does not instruct the model to insert a flag into an unrelated shot.
2. **Material palettes.** All eight banner objects in `objects.json` have `canonical_reference` and `palette`: sRGB cloth, emblem and trim swatches, named colours, and a lighting rule. Emberfall also has a golden-ember accent. These are neutral-light art-direction targets chosen to match the existing banner designs, not sampled pixel measurements. Map/UI `color` values stay in `world.json` and are excluded from the generation duchy context. Highlights and shadows are allowed; changing a house's hue family or emblem is not. Hex values guide generation but cannot enforce exact output pixels.
3. **Side-by-side review.** Run `python3 scripts/build_banner_review.py`, serve the site, and open [`generation/banner-review.html`](../generation/banner-review.html). It puts the canonical banner and swatches beside every candidate panel associated with that house, with links to full-size art. Review cloth hue, emblem, trim and scene lighting. Choose Matches reference, Needs correction, or No visible house marking and add notes. Pending is the default; nothing is automatically approved. Houses without scenes still show their reference and palette.

Decisions save in browser-local storage and can be exported as JSON. The review revision includes output-image hashes, canonical-reference hashes, palettes, candidate assignments and review criteria. Replacing an image or reference, editing a palette, or changing assignments invalidates the previous version's decisions. Rebuild the comparison after those changes. This is manual visual review, not an automated colour detector; a hidden banner requires an explanatory note.

```sh
python3 scripts/build_image_requests.py
python3 scripts/build_banner_review.py
# Review in the browser; export banner-review-decisions.json.
python3 scripts/validate_banner_review.py /path/to/banner-review-decisions.json
python3 scripts/validate_generation.py --require-outputs --banner-review /path/to/banner-review-decisions.json
```

Validation rejects unresolved, missing, duplicate or stale decisions. A newly selected output whose generation request uses schema 2 and house references requires the exported banner review in `validate_generation.py --require-outputs`. Previously published schema-1 artwork remains readable and unchanged; it is not retroactively labelled as passing the new banner review. The generated comparison starts with the current images for reference, including any existing inconsistencies. The review tool does not itself publish or modify artwork.

For publication checks, only the selected schema-2 scenes require passing banner decisions; unchanged schema-1 images can remain pending. Every report entry still needs current hashes. This preserves the earlier illustrations without falsely approving their known inconsistencies. The standalone review validator checks the complete comparison by default.

Named ships can also declare `canonical_reference` in `objects.json`. The request builder reserves that geometry anchor immediately after house banners, ahead of old scene references. The Argonaut’s refit illustration controls its wedge prow, crimson armour and machinery in future scenes. Older generic Bastion art supplies ancestry only.
