# 370 Brannan Street — reference dossier

Compiled 12 August 2026 for the SF-SIM miniature asset. Everything here was
re-verified for the build; where this dossier disagrees with
`docs/asset-plans/370-brannan.md`, this file and `REPORT.md` win.

## What the building is

A 1937 two-storey stucco-over-wood-frame infill building on the northwest side
of Brannan Street in SoMa, between 372–374 to the southwest and 362–366 to the
northeast, with its back on the Varney Place alley. 3,700 sq ft over two floors
on a 1,760 sq ft lot. Assessor use class Industrial; permitted "public assembly
other" since a 2013 tenant improvement; occupied in recent years by software and
design firms (Typeform US, Spherecast, radiantgraph, ARRIS Design Partners).

It is 60 m northeast along the same block face from
[380 Brannan Street](../380-brannan/), which is already in the manifest.

## Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM way/124890321](https://www.openstreetmap.org/way/124890321) | address, `building=yes`, `height=7`, `source=Bing`. Footprint **rejected** — see conflicts. |
| DataSF Building Footprints `ynuv-fyni`, `mblr=SF3775020` | the authoritative footprint polygon; `hgt_median_m` 7.07, `hgt_majoritycm` 745, `hgt_maxcm` 763, `hgt_stdcm` 33, `gnd_min_m` 9.34 |
| DataSF Assessor roll `wv5m-vpq2` (2025), block 3775 lot 020 | built **1937**, 2 storeys, 3,700 sq ft, Industrial |
| DataSF Building Permits `i98e-djp9`, lot 020 (4 permits, 2009–2014) | 2 storeys existing and proposed on every one; `existing_construction_type_description = "wood frame (5)"`; 2009 office fit-out (B→M occupancy change); 2013 T.I.; Dec 2013 "install 1 non-illuminated channel letter sign" |
| Google Street View pano `QGmjHr1j26kBQJg4CIIlyQ` (Brannan St, 2025) | the entire front-elevation description below |
| Esri World Imagery + Google satellite, z20–21 (2026) | roof: membrane deck, two square skylights, one small roof light, one hatch, no plant |
| OSM highway geometry (Overpass) | Varney Place centreline is **4.7 m** from the rear wall — the rear is an exposed elevation |
| DataSF `ynuv-fyni` for `SF3775021` / `SF3775018` | neighbour crests 8.80 m and 8.58 m — 370 is the lowest of the three |

Commercial listing pages (LoopNet, Crexi, Cityfeet) return 403 to automated
fetches; their figures (3,700 sq ft, 1,760 sq ft lot, 1937, "high ceilings,
natural light, skylights") were read from search-result summaries and are only
relied on where the assessor roll independently agrees, which it does.

## Verified dimensions and location

| | |
|---|---|
| WGS84 anchor | `-122.3938572, 37.7807602` (footprint centre) |
| Footprint | 7.00 m frontage × 23.83 m deep, 166.9 m², a clean rectangle |
| Roof deck | 7.05 m above ground (LiDAR median 7.07, majority 7.45, std 0.33) |
| Parapet crest | **7.63 m** (LiDAR max) — the asset's target height |
| Ground elevation | 9.34 m NAVD88 (the app's terrain handles this, not the asset) |
| Brannan front heading | 134.9° true (SE) |
| Rear heading | 315.0° true (NW), onto Varney Place |

The LiDAR standard deviation of 0.33 m over 707 cells is the number that settles
the massing: this is one uniform flat roof at a single level. There is no lower
rear wing, no penthouse and no stepped section. The `hgt_mincm` of 5.65 m is a
handful of edge cells, not a real feature.

## Orientation

Footprint in Blender coordinates (metres, +X east, +Y north), CCW, centred on
the anchor — this is verbatim what `build_370_brannan.py` extrudes:

```
(-10.946,   5.907)
(  5.999, -10.863)
( 10.941,  -5.901)
( -5.994,  10.857)
```

| Edge | Length | Outward normal | Elevation |
|---|---|---|---|
| 0 | 23.84 m | SW 224.7° | party wall, 372–374 Brannan |
| 1 | 7.00 m | SE 134.9° | **Brannan Street front** |
| 2 | 23.82 m | NE 44.7° | party wall, 362–366 Brannan |
| 3 | 7.00 m | NW 315.0° | **Varney Place rear** |

Authored in true-world orientation (`+Y` = north) per
`docs/asset-plans/README.md`: `placeGeneric()` never rotates an asset, so the
contract's "front faces −Y" cannot be honoured literally for a building whose
front faces southeast. Real-world orientation wins (AGENTS rule 5).

Because of the ~45° heading the axis-aligned XY bounding box is 21.87 × 21.71 m
for a building that is 7.00 × 23.83 m. That is expected, not a scale error.

## What each side shows

**Southeast — Brannan Street front.** One composition: a raised flat stucco
frame — a pilaster at each end, a wide band across the middle — enclosing the
elevation. Inside it, top to bottom: a wide black steel-sash window band filling
most of the upper storey, deeply set, roughly a 4×3 pane grid with a darker
transom row behind; the mid-band itself, plain, carrying the painted numerals
**"370"** at its southwest end; then the ground floor, a **cobalt-blue solid
door with a six-light window** at the southwest end and a large dark
plate-glass storefront window filling the rest, with a small tenant decal.
Above the upper window the wall runs up into a plain parapet — no cornice, no
coping course, no ornament of any kind. The wall is a mid warm gray; the frame
reads one step lighter. A young street tree stands directly in front of the
door (not part of the asset).

**Northwest — Varney Place rear. NOT SOURCED.** No Street View coverage of the
alley was found; satellite imagery shows only the roof edge. The rear is 4.7 m
from the alley and fully visible to the app's aerial camera, so it could not be
left blank — it is built as the minimum a 1937 wood-frame back wall must have
(a service door and two small high windows) and **every number on it is
inferred**. This is the asset's one real gap. See `REPORT.md`.

**Northeast and southwest flanks.** Party walls, built hard against neighbours
that are ~1 m taller. Modelled blank. Inventing a window grid on a party wall
would be a straightforward lie, and the real walls have none.

**Top.** A pale flat membrane roof inside a plain parapet. Two square skylights
— raised pale curbs with dark glazing, ~2.6 m square — sit on the centre line,
one about a third of the way in from the rear and one just past the middle. A
smaller rectangular roof light, ~1.6 × 1.0 m, sits between the second skylight
and the street. A small pale hatch box sits near the southwest edge two-thirds
of the way back. **No HVAC plant, no penthouse, no masts.** This is a small
wood-frame building and its roof is genuinely empty; the two skylights are the
only things on it that read from above, which is exactly why they were kept at
full size and given light `Toy_glassl` caps.

## Recognition cues, ranked

1. **The proportion** — 7 m wide, 23.8 m deep, 7.6 m tall, visibly narrower and
   lower than both neighbours. At city scale this is the whole recognition.
2. **The framed front panel** — raised border with a wide mid-band.
3. **The cobalt-blue door** — the only saturated colour on the block face, and
   the only thing besides the silhouette that survives at thumbnail size.
4. The black steel-sash upper window band.
5. The two square skylights on an otherwise empty roof.

## Preserved

- The measured footprint and the real 45° heading, exactly
- Being lower than both neighbours — 7.63 m is not rounded up to match the block
- The framed-panel composition and the mid-band's vertical position
- The blue door as the single accent
- Blank flanks

## Simplified

- The upper window's ~12-pane grid → one recessed glazed panel with three
  mullions; individual panes are sub-pixel at city scale
- The frame thickened to 0.55 m wide and 0.10 m proud so it survives at
  thumbnail size — the one place semantic exaggeration is spent
- The painted "370" numerals are **not modelled**: the contract forbids
  textures, and glyph geometry on a 7 m frontage is noise. The band that carries
  them is the cue that survives. Recorded as a decision, not an oversight.
- Storefront decal, street tree, sidewalk grate, wall meter: dropped
- Roof membrane seam lines: dropped
- A true pyramid skylight cap → a shallow tapered frustum (`tapered_box`), which
  reads identically from a 38° camera at a fraction of the triangles

## Conflicting evidence, resolved

**OSM's footprint is 1.2 m too narrow — rejected.** Way/124890321 traces
5.83 × 24.24 m. The DataSF LiDAR footprint says 7.00 × 23.83 m and the
assessor's 1,760 sq ft lot (163.5 m²) agrees with DataSF's 166.9 m² to 2%. The
OSM way is `source=Bing` — a rooftop trace from oblique imagery on a building
whose neighbours are a metre taller on both sides, exactly the case where such a
trace loses the eaves. **Built on DataSF.** A 1.2 m error on a 7 m frontage is
17%, so this one matters more than the usual OSM/DataSF disagreement.

**`height=7` on the OSM way is the roof deck, not the crest.** It matches
`hgt_median_m` 7.07 to within 1%. The crest is 7.63 m. This is the same trap as
380 Brannan's `height=11` and the standing warning in
`docs/asset-plans/README.md`.

**Storey count: no conflict.** Unlike 380 Brannan, the assessor roll and all
four building permits agree on 2, and the floor area (3,700 sq ft ≈ 2.06× the
footprint) confirms two full floors with no mezzanine.

**Construction type.** Permits say wood frame (Type V), not the unreinforced
brick of its 1908 neighbours. The elevation is stucco, not masonry, and it is
modelled as a painted stucco slab — no brick material appears in this asset.

## Remaining uncertainties

- **The rear elevation is inferred in full** (see above). Highest-value future
  correction.
- **Vertical band positions are inferred** from photogrammetric estimates off a
  single oblique pano, scaled against the measured 7.63 m crest: mid-band
  3.40–4.50 m, upper window band 4.60–6.45 m, storefront head 3.20 m. The three
  are mutually consistent and consistent with the overall height, but none is a
  published figure.
- **The upper window's 4×3 pane grid is inferred** from one capture partly
  occluded by a street tree — but since it is simplified to one panel with three
  mullions, being wrong about it costs almost nothing.
- No architect is recorded for the 1937 building in any source consulted.
