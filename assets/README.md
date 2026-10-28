# Magneton panel artwork

Generated illustrations for this original fictional setting. The artwork uses dark teal, ochre, orange, and mint tones in an inked graphic novel style. Lettering is separate HTML, not baked into the images.

- `fracture.png`: shattered landmasses and magnetic fields.
- `survivors.png`: humanity surviving and adapting on floating islands.
- `ore.png`: discovery and extraction of Magneton.
- `polarity-engine.png`: two green Type B cores of opposing polarity inside a precision motor.
- `city.png`: a floating city supported by Magneton technology.

Every comic panel uses a different illustration. Ship images are shared between the home gallery and glossary as references. They are concept depictions of the world; character appearances and machine designs are not yet fixed story canon.

The retained designs explore the user-provided rigid metal Zeppelin and open-deck references. Each ship can be opened at full resolution from the fleet gallery.

## Current ship designs

- `mining-mole.png`: squat mining tug with a removable ore cassette and forward drill.
- `schooner-needle.png`: light teardrop commuter with articulated engine outriggers.
- `trader-caravan.png`: broad twin-hull merchant with connected freight decks.
- `capital-bastion.png`: armored three-keel capital fortress.
- `schooner-kestrel.png`: compact commuter with a boarding deck and hull-edge field rings.
- `trader-terrace.png`: broad merchant with passenger terraces and a raised aft bridge.

The last two designs draw on the user's second, open-deck airship reference. The glossary displays all six ships together. Names and qualitative handling notes for variants are proposed concepts, and illustrations are not to scale.

## Unique prologue scenes and materials

- `magnetic-islands.png`: magnetic currents between exposed island undersides.
- `human-adaptation.png`: three generations studying a magnetic instrument.
- `gravity-chamber.png`: ordinary local gravity inside a floating city.
- `city-street.png`: an inhabited street powered by green energy conduits.
- `mining-dock.png`: extraction, unloading, and control of trade.
- `ducal-assembly.png`: the former mining magnates ruling together.
- `magneton-types.png`: Type A bronze, Type B green polarity specimens, and a conceptual Type C forging sample. Type C is now established as silvery.

The thirty-seven comic images in `chapters/prologue.json` must have distinct source files and distinct file contents. The retired amber/green engine illustration has been replaced so both Type B cores are green.

The original ore carrier, city schooner, passenger trader, and ducal man-of-war designs have been removed. The prologue now uses the Mole mining ship.

## The Duke’s Due and world atlas

- `rovan-city-crimson.png`: Rovan Vey and General Grievous overlooking the small city.
- `unpaid-ledger-crimson.png`: the unpaid soldiers' accounts and pay chest.
- `duke-resolve-crimson.png`: Rovan's resentment becomes a decision.
- `caravan-boarding-crimson.png`: armoured Tesla-gun soldiers boarding an Auric Reach Caravan.
- `duke-seizure-crimson.png`: Rovan announces seizure for unpaid protection fees.
- `soldiers-cheer-crimson.png`: soldiers cheer while the sailors remain silent.
- `shattered-earth-atlas.png`: large-scale map backdrop for eight editable duchy labels in the glossary.

Character appearances are working designs. Map labels are HTML so names and locations can be refined without repainting the geography. All thirty-seven comic panels retain unique image sources and contents.

## His Own Future

- `rovan-future-crimson.png`: Rovan declares he will define his own future.
- `recruit-drill-crimson.png`: experienced veterans train recruits with seized resources.
- `single-bastion-departure.png`: departure with exactly one capital ship.
- `auric-raid-crimson.png`: the first organised inter-duchy invasion since the Fracture.
- `ships-confiscated-crimson.png`: ships seized at the captured docks.
- `city-captured-crimson.png`: the baron's city surrenders to the trained force.
- `type-c-seamless-forge-industrial.png`: Rovan privately crafts the stolen silver metal.
- `type-c-seamless-five-industrial.png`: exactly five seamless silver captains with a lance, broadsword, twin swords, war hammer and scythe, shown in full.
- Retired magnetic-boarding illustration: two of the five guards demonstrate field drifting between ships; their armour is not penetrated by weapons.

All thirty-seven comic panels must use distinct source images and file hashes. The five-guard line-up must show exactly five guards, not Rovan or the general as a sixth figure. The initial city capture uses bronze-armoured veterans, before the silver sets exist.

## Duchy banners

Eight individual heraldic banner images match the colour key and atlas labels in the consolidated glossary.

- `banner-veymarch.png`: Veymarch, crimson, silver broken shield and star.
- `banner-auric-reach.png`: Auric Reach, gold, merchant’s balance within a coin.
- `banner-ironveil.png`: Ironveil, steel, silver hammer and anvil.
- `banner-glassmere.png`: Glassmere, cyan, white crystal prism.
- `banner-stormholt.png`: Stormholt, violet, silver lightning bolt and ring.
- `banner-emberfall.png`: Emberfall, orange, dark flame and golden ember.
- `banner-verdant-crown.png`: Verdant Crown, emerald, golden crown of leaves.
- `banner-pale-meridian.png`: Pale Meridian, ivory, midnight compass star.

The atlas background remains the same geography; heraldic colours, names, and banner links are editable HTML. No ninth or tenth duchy was added.

## Complete inventory

See [ASSETS.md](../ASSETS.md) for the full repository catalogue, [assets.html](../assets.html) for the visual library, and [world.json](../world.json) for structured world facts and image metadata. Refresh the inventory with `python3 scripts/build_assets.py`, then shared layout with `python3 scripts/sync_layout.py`.

## Crimson uniform correction and next move

The Rovan scenes on pages 5–8 use `-crimson.png` replacements. Their military cloth underlayers, capes, and tabards match Veymarch crimson; bronze and silver armour retain their metal colours. The departure panorama has no legible soldier base layers and is unchanged. Retired teal-cloth files are removed from the current catalogue.

- `council-next-steps.png`: Rovan and General Grievous discuss what comes next.
- `auric-counterorder.png`: Auric Reach’s unnamed ruler dispatches three capital ships.
- `three-capital-ships.png`: exactly three enemy capital ships depart, with no battle outcome shown.

## Seamless Type C redesign

Pages 9 and 11 use seven unique illustrations: `type-c-seamless-forge-industrial.png`, `type-c-seamless-five-industrial.png`, `type-c-lance-assault-industrial.png`, `type-c-broadsword-breach-industrial.png`, `type-c-twin-sword-flight-industrial.png`, `type-c-warhammer-shield-industrial.png` and `type-c-scythe-city-seized-industrial.png`. The previous three page-9 illustrations are retired. The silver armour has continuous coverage, with brushed metal and restrained machined details and external crimson cloth. Each captain has a different magnetic weapon.

## Practical Silver Guard and the troop advance

The current Type C artwork uses the `-industrial.png` variants: restrained brushed silver, tool marks, simple closed helmets and distinct body silhouettes. The earlier grand armour concepts are retired. Page 10 adds `troops-dock-run.png`, `troops-gate-charge.png` and `troops-street-advance.png`. The Prologue has 12 fixed-size pages and 37 unique comic illustrations; all 52 current assets are catalogued in `ASSETS.md` and `assets.html`.
