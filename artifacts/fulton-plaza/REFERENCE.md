# Fulton Plaza — reference dossier

The pedestrianised block of Fulton Street between Larkin and Hyde, in San Francisco's
Civic Center: a 120 m × 49 m right-of-way lying between the Asian Art Museum and the Main
Library, closed to traffic since spring 2020, with the 1894 Pioneer Monument standing on
its exact centre and two 20-metre koi painted around the monument on the black asphalt.

This file is the research behind `build_fulton_plaza.py`. Where it disagrees with
`docs/asset-plans/fulton-plaza.md`, this file and `REPORT.md` win — the plan was written
before the model existed and two of its numbers moved (see "Corrections to the plan").

| | |
|---|---|
| Manifest id | `fulton-plaza` |
| Manifest anchor | `-122.4159308, 37.7796961` (model XY bbox centre) |
| Right-of-way OBB centre | `-122.4159189, 37.7796904`, measured; the model sits 1.05 m west / 0.63 m north of it |
| `targetHeightM` | **13.1999 m** — the model's VERTICAL EXTENT, not an architectural height. See "The terrain drape" |
| Monument crest | 11.698 m above local grade (apron 1.03 + 10.668 m of monument) |
| Right-of-way | 120.04 m × 48.59 m oriented, 5,805 m² = 1.435 acres, heading 81.15° |
| Axis-aligned XY bbox | 128.49 × 67.63 m — the 8.85° rotation, plus the beds' overhang and the tree crowns |
| Triangles | 13,364 (cap 16,000) |
| Category | `0` (Miscellaneous), `loadRadius` 2500 |

## Sources, and what each establishes

| Source | Establishes | Confidence |
|---|---|---|
| DataSF parcels `acdm-wktn`, blklots `0354001` (library block) and `0353001` (museum block) | The right-of-way polygon. Fulton Plaza has no parcel of its own — it is a street — so its outline is the gap between the two block faces it lies between | **measured** |
| `app/public/tiles/buildings/19_13.bin` footprint #101 | The Pioneer Monument's plan, as a 17-vertex cruciform 16.76 × 11.39 m. DataSF traces the monument as a *building*, which is both why the landmark needs an exclusion and why we have a survey-grade outline of it | **measured** |
| SF Arts Commission, Civic Art Collection, accession 1894.4.a-o | Pioneer Monument: 1894, Frank Happersberger, bronze and granite on marble; **420 × 488 × 676 in** overall (10.668 × 12.40 × 17.17 m); base alone 294 in = 7.468 m; "the *Early Days* component was removed and placed into storage in 2018" | verified |
| Wikipedia, *Pioneer Monument (San Francisco)* | The four cardinal piers — Plenty (N), Commerce (S), In '49 (W), Early Days (E) — and the Minerva-with-grizzly crown; the 1993 move from the City Hall forecourt | verified |
| SFGate, 14 Sep 2018 | *Early Days* removed before dawn; the east pier has stood empty since | verified |
| Illuminate (`illuminate.org/projects/fulton-plaza/`), Feb 2024 | Two white-and-orange koi by Jeremy Novy, painted on the blacktop, circling the Pioneer Monument; completed spring 2024 | verified |
| Illuminate news, 22 Feb 2024; UnderscoreSF | Each koi about 65–70 ft (20–21 m) | verified |
| KQED, *Ever Seen A Koi Fish on the Sidewalk?* | Painted in 5 ft grid sections over two months with exterior primer, paint and a sealant carrying **retroreflective glass beads that glow when light hits them** — this is the evidence behind the night state | verified |
| SFMTA board item, 16 Jul 2024, and the MOU of 17 Jun 2024 | The closure: Fulton between Hyde and Larkin, 24 h daily, 1 Sep 2024 → 31 Aug 2027; closed continuously since spring 2020; Rec & Park activates, Public Works maintains, SFMTA owns the closure | verified |
| Illuminate / SF Rec & Park / SF Standard, Apr 2025 | SPECTRA: 1,271 programmable LEDs strung roof-to-roof between the library and the museum over 1.6 acres, debut 5 Apr 2025, approved for two years. **Deliberately not modelled** — see "SPECTRA" below | verified |
| OSM ways 1469745032 / 1469745033 | The two raised planting beds on the museum side (`area=yes`, `highway=pedestrian`, `surface=dirt`) | **measured** |
| OSM ways 399142439 / 696627437 | The south and north sidewalk centrelines | **measured** |
| OSM nodes 6465902729, 13481001521, 13480967445/6 | Ashurbanipal (1988); the 1996 "California Native Americans" plaque, which sits on the monument's **east** pier and corroborates which pier is empty; two plaza lamps | **measured** |
| Esri World Imagery (`World_Imagery/MapServer/export`) at 0.110 m/px | The primary visual reference: the koi positions, the monument's pale apron (~21 m), the two flanks, the tree rows. The parcel-derived right-of-way quad overlays exactly onto the visible plaza in this imagery, which is what validates both | **measured**, ±2 m |
| `app/public/tiles/terrain.bin` via `manifest.terrain` | The drape. Anchor 17.788 m; the plaza falls 2.37 m and cross-falls up to 0.87 m | **measured** |

**Rejected.** Wikidata Q14683658 gives the Pioneer Monument at `-122.4181304, 37.779701` —
its **pre-1993** site in Civic Center Plaza, 180 m west. Nominatim resolves "147 Fulton
Street" to OSM way `33789581`, which is a *cycleway segment*, not a footprint: the same
"the geocoder returned `osm_type: way`, so it must be a building" trap that 350 Brannan
and 10 South Park document.

## Orientation and placement

The plaza's long axis runs **81.15°** (toward Hyde Street, east); its cross axis
**171.15°** (toward the Main Library, south). The Civic Center grid leans **8.85° east of
north**, which agrees with every neighbour already shipped — Main Library 9.06°, Asian Art
Museum 9.06°, City Hall 9.62°, Civic Center Plaza 9.06°.

> The cross-axis bearing is 171.15 = 180 − 8.85, **not** 188.85. Those two are mirror
> images about north and every bounding-box measurement reads the same 8.85° for both.
> `civic-center-plaza` shipped the wrong sign once and came out 18° crooked against its own
> block with every number in its report still validating.

Right-of-way corners, from DataSF, and the same corners in the plaza's own `(u, v)` frame
(`+u` east toward Hyde, `+v` south toward the library):

| Corner | lon | lat | u | v |
|---|---|---|---|---|
| SW — Larkin × library line | −122.4165461 | 37.7793902 | −59.64 | +24.30 |
| SE — Hyde × library line | −122.4152008 | 37.7795570 | +60.17 | +24.29 |
| NE — Hyde × museum line | −122.4152951 | 37.7799901 | +59.34 | −24.29 |
| NW — Larkin × museum line | −122.4166336 | 37.7798241 | −59.87 | −24.28 |

**The Pioneer Monument is the plaza's geometric centre.** The area centroid of its traced
footprint lands at `(u −0.34, v −0.68)` — **0.76 m** from the right-of-way's own oriented
bounding-box centre. The 1993 relocation put it on the crossing of the two axes, and that
is why the model is built symmetric about it.

**The two flanks are not symmetric, and the model keeps them different.** The north
(museum) side carries two raised soil beds from `v = −19.2` to `v = −26.3`, i.e. they start
5 m inside the property line and *overhang it by up to 2.0 m*. That overhang is real — the
beds are cut into the museum's forecourt — and harmless, because the Asian Art Museum GLB's
own wall stands another ~5 m north of it. The south (library) side has no bed at all: a
pale terrace, a low wall on its plaza edge, and a thinner row of smaller trees.

## The terrain drape — read this before changing anything

**This asset is draped on the baked terrain, and that is why `min_z` is −1.50 m and
`targetHeightM` is 13.20 m.** Both are deliberate, both are asserted by
`validate_fulton_plaza.py`, and neither is a contract slip.

`placeGeneric()` in `app/src/assets.js` seats a landmark from a single terrain sample:

```js
const y = Math.max(0, data.sampleElevation(x, z));   // at the anchor, once
```

Correct for a building; wrong for an asset that IS the ground. Fulton falls **2.37 m**
across this block — 18.9 m at the Larkin end, 16.7 m at Hyde, with the anchor at 17.788 m —
and unlike South Park the fall is genuinely two-dimensional: the **cross-fall reaches
0.87 m**, so `dy` is sampled on a 4 m grid rather than reduced to a profile of `u`.

Consequences:

- **z = 0 is the anchor's ground**, which is exactly where the loader puts it. `min_z` is
  −1.50 m (the deck's flat underside, 0.34 m below the lowest terrain it covers). The check
  that replaces "min_z ≈ 0" is that the deck stands `Z_DECK` above the terrain everywhere:
  measured by ray-casting onto the deck at 32 points across the right-of-way, **max
  standoff error 0.0039 m**.
- **`targetHeightM` is the vertical extent**, 13.1999 m, because the loader's scale is
  `targetHeightM / bbox height` and it must be 1.0.
- `sample_terrain.mjs` reads `app/public/tiles/terrain.bin` through `manifest.terrain` —
  the shipped copy of the bake output and the exact array `app/src/data.js` indexes at
  runtime — so the sampler agrees with the loader by construction.

A long thin prism is **not** draped just because its corners are. `prism_verts_faces()` puts
a plane through the four corners, and with 0.87 m of cross-fall a 45 m scored joint modelled
as one box rose 0.6 m above the deck in the middle and drew straight across the monument's
apron (measured in the exported GLB: `joint_u5` spanned z +0.40 to +1.19 where the apron
topped out at +0.77). Every long bar in the model — the joints, the terrace wall, the bed
kerbs — is segmented along its own length by `draped_bar()` or gridded by `draped_slab()`.

## The street that is still baked underneath

`exclusionZones()` is consumed by `pipeline/buildings.mjs`, `audit.mjs` and
`verify-rebake.mjs` — **not** by `pipeline/streets.mjs`. One DataSF centreline survives the
closure and still bakes: `streets/19_13.bin` line 44, class index 4 = `residential`, 16
points of which 12 lie inside the plaza quad. In toy mode that renders, under this asset, a
9 m `#3c3c40` road ribbon on the terrain, 3 m pale sidewalk plinths lifted `TOY_CURB_H =
0.35 m` at the kerb, and a 0.5 m centre dash at `TOY_MARK_LIFT = 0.03 m`.

**The deck top is at +0.95 m above local grade, and that number was measured in the running
app, not chosen.** 0.55 m — nominally 0.20 m of clearance over the kerb — was not enough,
and the reason is two effects that stack:

- the ribbon's `y` is quantised to decimetres and rounds **up** to 0.20 m above the terrain
  sample in places, so the sidewalk top actually reaches terrain + 0.55 m;
- `createGroundMaterial()` in `app/src/materials.js` runs the whole ground mesh with
  `polygonOffsetFactor = polygonOffsetUnits = -2`, which pulls it toward the camera in
  depth so that draped geometry wins ties.

Measured station by station along the block, the clearance at 0.55 m was **0.06–0.15 m**,
the offset won, and in the running app two pale stone stripes drew straight over the deck,
across both koi and across the monument's apron. **Nothing upstream can see this**: the
Blender renders are of a file that does not contain the street, and the contract validator
only knows about the file. It is a depth-bias fight against geometry that is not in the
asset. At 0.95 m the worst station has 0.40 m of clearance.

The cost is a plaza that stands a little proud of the crossings at Larkin and Hyde. That is
semantic exaggeration in authoring, which the style bible allows; nothing has been moved or
rescaled, so AGENTS rule 5 is untouched. Verify it in the app from a low camera at both ends
as well as from above — the failure shows as a charcoal stripe or a pale plinth bleeding
through the deck.

## What each side shows

- **From above** — the review image that matters. A black asphalt field; a pale circular
  apron dead centre with the cruciform monument on it; two large pale-and-orange koi
  orbiting it, one 33 m west and one 27 m east, lying across the axis; a dark green band of
  mature crowns in raised soil down the north edge; a pale terrace with a thinner, lighter
  tree row down the south edge; bollards ruling both ends.
- **West (Larkin) end** — the grand end, aimed at Civic Center Plaza and City Hall's dome.
- **East (Hyde) end** — 2.4 m lower, opening onto UN Plaza and Market Street; the farmers
  market stages here.
- **South (library) elevation** — long low pale wall and terrace, younger trees, more
  paving. Reads bright.
- **North (museum) elevation** — two raised soil beds, mature planes, deep shade,
  Ashurbanipal standing in it. Reads dark and green.

## Recognition cues (ranked)

1. **The two koi** on black asphalt, circling the monument. Nothing else in San Francisco
   looks like this from the air.
2. **The Pioneer Monument on its pale round apron**, dead centre, **with one empty pier**.
3. **The axis** — 120 m of open route between two civic buildings, bollarded at both ends.
4. **The asymmetric flanks** — dark planted bed north, pale terrace south.
5. **The grade** — the plaza visibly runs downhill to the east.

## Z stack

Every level is a distinct closed solid; the gaps are what keep the model free of coplanar
surfaces. All heights are **above local grade**, with the drape added per vertex.

| z | element |
|---|---|
| −1.50 | deck underside (flat; 0.34 m below the lowest terrain it covers) |
| 0.95 | asphalt field top — 0.40 m clear of the baked street's sidewalk plinths |
| 0.97 | scored joints |
| 0.98 → 1.01 | koi bodies and pectorals |
| 1.01 → 1.025 | koi markings |
| 1.025 → 1.052 | koi `_Glow` shells (white body, then the markings on top of it) |
| 1.03 | the monument's granite apron |
| 1.10 | south terrace, north sidewalk |
| 1.35 | north planting beds (kerb 1.41) |
| 1.42 | terrace low wall |
| 2.18 | monument platform (apron + 1.15) |
| 3.78 | the four cardinal piers |
| 8.50 | central pedestal top (apron + 7.468) |
| 11.70 | **Minerva's finial** (apron + 10.668) — the crest |

## Palette

`Toy_tarmac` (`6f7076`) asphalt field · `Toy_stone` (`d9d2c2`) kerb, terrace, sidewalks,
monument granite · `Toy_cream` (`f2ede3`) the monument's apron · `Toy_seam` (`5f5f68`)
scored joints · `Toy_steel` (`9aa0a6`) lamp poles, bollards, tree trunks ·
`Toy_verdigris` (`9fb8a8`) tree crowns · `Toy_soil` (`7d6a55`) beds · `Toy_bronze`
(`6d6448`) Minerva, the three surviving groups, Ashurbanipal · `Toy_koiWhite` (`f4e9dc`)
and `Toy_koiOrange` (`e8733c`) the mural · `Toy_ink` (`3a3530`) bollard bands ·
`Toy_roofd` (`45454a`) bench slats and bins · `Toy_navy` (`2c4a70`) people.
Glow: `Toy_koiWhite_Glow`, `Toy_koiOrange_Glow`, `Toy_gold_Glow` (`caa64a`).

Two palette decisions worth keeping:

- **The asphalt is `6f7076`, not `Toy_roofd`.** Measured in the running app on
  `92-south-park`, `Toy_roofd` (`45454a`) on a large up-facing surface comes back
  **rgb(9,9,12)** — below what the diorama's ambient can lift — and the whole asset reads
  as a hole. `6f7076` is ~2.7× its linear luminance, still the darkest large surface in the
  model, and still unmistakably asphalt against the pale edges. **This one has to be judged
  in the app at stage 5, not from these renders**, where anything dark looks fine.
- **The bronze is `6d6448`, not a gilt.** Authored at `7a6f52` first and the figures read as
  gold pagoda finials next to the granite.

## Night state

The **koi are the hero glow**, and that is not a licence: the real mural is sealed with
retroreflective glass beads specifically so that it lights up. The white body glows through
a shell inset to 55% of the body's half-width, and the three markings glow **on top of that
shell in their own colour** — authored the other way round first, and the night render gave
two pure-white fish, because the white shell was simply covering the orange. Supporting
glow: the lamp lenses (a plate *under* the housing, not inside it — the first build buried
the glow box within the opaque head and the night render showed a row of unlit poles) and a
warm wash up the monument's pedestal.

Glow surfaces are thin shells proud of the opaque solid beneath them, never the solid
itself: the app draws `_Glow` in a separate unlit layer at `0.12 + 0.95 × uNight` alpha, so
a primary surface authored as glow reads translucent at noon.

## SPECTRA — why it is not here

The 1,271-LED array strung between the library's and the museum's roofs is the most
photographed thing about this plaza right now, and it is deliberately absent. Three reasons,
in order of weight:

1. **The app's camera looks down.** A canopy stretched across the plaza at ~28 m would
   occlude the koi and the monument from the only view this asset is judged from, and
   destroy the composition it exists to deliver.
2. **It hangs from two other assets.** Anything holding it up inside this footprint is a
   fiction; the roofs that carry it belong to `sf-main-library` and `asian-art-museum`.
3. **It is temporary** — approved for a two-year run from April 2025 — so baking it in dates
   the asset.

Its effect is already in the night state: this is a plaza that is brightly lit from above,
which is why the koi glow.

## Simplifications, and what they cost

- **Tree heights are estimated.** No source consulted measures them. The crowns are modelled
  at 7.80 m (north) and 5.60 m (south) above local grade so that the Pioneer Monument stays
  the tallest thing on its own plaza once the 2.37 m drape is added. A measured plane taller
  than 11.27 m would be a real conflict; the honest resolution is to keep the monument as the
  datum and record the trees as deliberately restrained, not to move the datum onto a
  lollipop. `validate_fulton_plaza.py` asserts that the crest belongs to `monument`.
- **Tree positions are counted from aerial imagery, not surveyed.** 12 in the north beds at
  8.6 m centres, 10 on the south terrace at 11.4 m.
- **The koi outlines are authored.** Their published length and their positions are solid;
  their silhouettes come from one aerial image at 0.110 m/px of a mural that has been on the
  ground since 2024 and wears. See REPORT.md's open risks.
- **The bronze groups are chunky silhouettes**, not figures: a tapered body and a head,
  turned to their own cardinal rather than to the paving grid.
- **The farmers market and the concert stage are not modelled.** Both are twice-weekly
  temporary set-ups; their traces — the staging space kept clear at the Hyde end, the people
  clusters — are.
- **The library's forecourt sculptures are out of scope.** The Maya Angelou monument
  (`−122.416468, 37.779140`) and Rickey's *Double L Excentric Gyratory*
  (`−122.416520, 37.779355`) both stand south of the right-of-way, on library land.

## Corrections to the plan

`docs/asset-plans/fulton-plaza.md` was written before the model existed. Two of its numbers
moved, and REPORT.md beats the plan:

1. **`targetHeightM` is 13.1999 m, not 10.67 m.** The plan set the target to the Pioneer
   Monument's catalogue height and asked the validator to assert `max_z == 10.67`. That is
   incompatible with the drape the same plan mandates: once z = 0 means the anchor's ground,
   the export spans −1.50 to +11.70 and the loader's scale is `targetHeightM / 13.20`. The
   monument crest is still the model's crest, and is still 10.668 m of monument — it now
   stands on a 0.63 m apron on a draped deck. This follows the convention `64-south-park`
   and `424-brannan` already ship under.
2. **The expected XY bbox is 128.5 × 67.6 m, not 126.1 × 66.3 m.** The plan's figure was the
   right-of-way alone; the planting beds overhang the property line by up to 2.0 m and the
   tree crowns add another 2.3 m beyond that.

Everything else in the plan held, including the exclusion measurements, the "no
`clearTrees`" finding and the street-under-the-deck hazard.
