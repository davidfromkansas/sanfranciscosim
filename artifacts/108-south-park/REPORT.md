# 108-110 South Park — build report

Miniature GLB for the SF toy-diorama city, built from
`docs/asset-plans/108-south-park.md` under
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`. **REPORT beats plan**: where this file
and the plan disagree, this file is what shipped.

## Shipped numbers

| | |
|---|---|
| File | `108-south-park.glb` — **shipped = the stage-4 optimized build**, 96,196 B (93.9 KB) raw |
| Triangles | **3,516** (cap 9,000; validator budget 6,000) |
| Objects | 11 shipped (53 as authored; joined per material at stage 4) |
| Dimensions | 26.159 x 25.719 x **8.450** m |
| min Z / XY centre offset | 0.000 m / (0.000, 0.000) |
| Materials | 10, all `Toy_*` (`verdigris` `mint` `gold` `trim` `ink` `glass` `stone` `steel` + 2 `_Glow`), no textures, no alpha |
| Manifest anchor | **−122.3944817, 37.7816789** |
| targetHeightM | **8.45** (front cornice crest) |
| Front / rear heading | 135.35° / 315.35° true |
| Draw submeshes | 13 shipped (58 as authored) |
| Validation | `validation.json` — **overall PASS**, all 16 checks, re-run on the shipped file |

The axis-aligned XY box is 26.2 x 25.7 m for a building that is 6.43 x 29.75 m.
That is the ~135° real-world heading plus the awnings' 0.80 m projection, not a
scale error. It is expected and the validator asserts it explicitly.

## Contract deviations, declared

1. **Front does not face −Y.** The asset-check contract's rule 3 says the front
   faces −Y in Blender. It cannot here: the building is authored at its real
   heading so the loader (`placeGeneric` in `app/src/assets.js`, which only
   scales and positions) drops it onto its real footprint. The shopfront faces
   **135.35° true**. This is the case `docs/asset-plans/README.md` calls out;
   real-world orientation wins.
2. **Two off-palette hexes, both keeping palette names.**
   `Toy_verdigris = #35493e` (body) and `Toy_mint = #4f6858` (cornice, belt,
   casings). The project palette has no dark green at all. The style bible's SF
   exception — painted facades are saturated identity in this city — covers it,
   and 165 South Park set the precedent of overriding the hex while keeping the
   NAME so the contract check and the loader's merge path are unaffected.
   **WARN, not FAIL.**
3. **The body green is lighter than the real paint.** See "Corrections and
   judgment calls" below.

## Dossier verification

Everything in the plan's 2.1 was re-checked against the sources before modelling.
**Nothing in the dossier had to be corrected.** Specifically re-derived:

- **Height.** LiDAR median 7.76 m over 853 cells (`SF3775059`), OSM `height=8`,
  assessor 2 storeys — three independent sources agree on a ~7.8 m deck. Model
  deck **7.80 m**. The LiDAR maximum of 11.88 m is *not* used: it is 2.2σ above
  the mean and the attached Gran Oriente next door reads 11.02 m, so it is
  party-wall bleed across a shared line. Crest **8.45 m** = deck + 0.65 m of
  boxed cornice, estimated from the Jan 2025 pano at ±0.4 m. **This is the one
  estimated number in the asset**, hence `"estimated": true`.
- **Footprint.** OSM way/124884358 reprojects to an exact 6.433 x 29.750 m
  parallelogram, 191.37 m2. The assessor's lot is 199.3 m2; DataSF's LiDAR ring
  is 218.8 m2 over 14 ragged vertices. OSM is the only one consistent with a
  21 x 100 ft parcel, so the model is authored on it.
- **Anchor.** Area centroid −122.3944841, 37.7816792; the model's bbox centre
  lands 0.209 m east / 0.029 m south of it (the awnings), so the manifest anchor
  is **−122.3944817, 37.7816789**.
- **Orientation.** Front normal 135.35°, verified against the park polygon
  (OSM way/24052083, nearest vertex 31.7 m at bearing 103.6°) and against the
  two attached neighbours' centroids, which lie north-east and south-west.
- **Party walls.** Both neighbours share footprint vertices at **0.00 m**. This
  is recorded here because it is the single most consequential fact for
  integration — see "Integration warning".

## Build iterations

Every pass was reviewed from the high three-quarter aerial first, per the style
bible §18 and the pipeline's stage-2 override.

| Pass | Problem seen | Fix |
|---|---|---|
| 1 | The aerial camera (78 mm at 2.15 x span, aimed at the bbox centre) put the shopfront — the only designed elevation — off the bottom edge of frame and filled the picture with roof. The night render was unreadable for the same reason. | 62 mm at 2.85 x span, aim point pushed 7 m from the bbox centre toward the shopfront and down to 0.42 x height. |
| 1 | The rear carriage door rendered as a flat 3.6 x 3.4 m black rectangle. `prism()` makes a **solid**, so an ink "frame" spanning the opening is a filled panel and the green leaf and glazing authored behind it were invisible. | Ink block moved behind and oversized so it shows only as a shadow border; leaf and glazing authored **proud** of the wall in front of it — 165 South Park's gate arrangement. |
| 1 | The recessed entry had the same bug and read as a black hole punched in the corner of the facade. | Same fix. |
| 1 | The roof carried four small skylights in the middle third and 8 m of blank deck at the street end — the end the app's camera actually looks at. Style bible §10 failure. | Skylights enlarged to 1.80 x 1.25 m and moved forward, plus a pale stair hatch near the street end, a mechanical block in the rear third and two vent stacks. |
| 2 | With the black hole fixed, the entry became a green door on a green wall and vanished. | Leaf in `Toy_ink`, with a lighter-green casing (two jambs + head) drawing it as an object. The pale transom band already runs across the top of the bay, so no separate fanlight. |
| 2 | The gold sign and the cornice overhung the party lines by 3-5 cm, showing as slivers outside the silhouette in the flank elevations. | Both trimmed flush to the frontage; the cornice dies are what wrap the corners. |
| **3 (in-app)** | **The whole building rendered as a literal black slab in the running app.** The Blender studio rig said the dark green was fine; the diorama's low-ambient lighting said otherwise. Measured in the local build at 1 PM from 70 m: front wall `rgb(5,5,6)`, roof `rgb(4,4,6)`, gold band `rgb(4,5,6)`, against `rgb(118,117,111)` on the neighbour's wall. Only the skylights and the transom survived. | Body `#35493e -> #587a66`, trim `#4f6858 -> #7f9d8b` (~3x luminance, still the darkest building on the rim). |
| **3 (in-app)** | The roof was `Toy_roofd` #45454a on the assumption that a flat SoMa roof is dark. It rendered black, swallowed the skylight line and turned the asset into a silhouette from the app's camera — **and it was also wrong about the reference**: the 2026 satellite imagery shows a LIGHT membrane roof on this row. | Roof deck `Toy_roofd -> Toy_stone` #d9d2c2; skylight frames and roof hatch `Toy_trim -> Toy_steel` so they still read against a light deck. |

Nothing above 8.45 m at any pass — the crest normalization was asserted by the
validator on every run.

**Pass 3 is the lesson worth carrying forward: the Blender review rig is not the
app.** A colour that reads correctly under a three-sun tabletop rig with 0.30
ambient can be gone entirely in the diorama. Judge dark assets in the running
app before believing the renders.

## Corrections and judgment calls

- **The body green is two steps lighter than the building.** The real paint reads
  near-black in shade. A near-black 6.4 m sliver, standing between an 11 m pale
  stucco neighbour and a navy one, reads from the app's camera as a *gap in the
  row* rather than as a building — and at one step up (`#35493e`) it still did,
  measurably, in the running app. `#587a66` is the same colour at ~3x the
  luminance and still leaves this the darkest building on the rim, which is the
  cue. Style bible §29: readability over realism. **Do not correct it back toward
  the photograph.**
- **The roof is a light membrane, not dark.** Corrected against the satellite
  imagery during stage-5 QA; the original dark deck was both a reference error
  and a rendering failure.
- **Green trim, not cream trim.** The palette's cream `Toy_trim` was the easy
  choice and would have been wrong — every piece of trim on this building is
  green. A lighter green does the same legibility job truthfully.
- **The sign has no lettering.** Flat-colour contract, and "SOUTH PARK CAFE" is
  sub-pixel from the aerial camera. The band itself is the identity cue.
- **The night state shows the shopfront lit although the unit was vacant** in the
  January 2025 pano (papered glazing), and a July 2026 Mission Local piece
  implies the café is gone. Glowing the transom band and one display bay is a
  §16 storytelling choice on a building whose entire identity is its shopfront —
  it is not a claim about current tenancy. Recorded so it is not mistaken for a
  research error.
- **The third upper window is inferred** from the bay rhythm; only two are
  clearly visible past the ficus.

## Night state

Hero glow: the **transom band**, a warm `Toy_trim_Glow` shell the width of the
shopfront. Supporting: **one display bay** and **two of the three upper windows**
in `Toy_glass_Glow`. Every glow surface is a thin shell proud of an opaque
surface — the app renders `_Glow` in a separate layer at ~12% alpha by day, so no
primary surface is authored as glow. Both glow materials' day colours match
their non-glow neighbours (`f3efe6` / `6f95b8` beside `Toy_trim` and
`Toy_glass`).

## Validation

`validation.json`, written by `validate_108_south_park.py` from a **fresh-scene
re-import of the exported GLB** (never the authoring scene). Blender 5.2.0 LTS.

**overall: PASS** — 16/16 checks, including:

- crest normalized to 8.450 m (loader scale lands at exactly 1.0)
- min Z 0.000, XY centre (0.000, 0.000)
- 3,516 triangles against a 6,000 budget
- 10 materials, all `Toy_*`, none textured, none transparent, no `Toy_body`
- no cameras, lights, animations, armatures, constraints; transforms applied;
  no negative scales
- **normals**: 53/53 objects enclose positive signed volume (authoritative for a
  union of solids); 0 non-unit loop normals; the 31,500-ray visibility test
  returned **0 flipped visible faces**, residual 0.000%
- no degenerate triangles, no unexpected or leaked geometry

## Renders

All regenerated from the final export. The four elevations share one rig and
differ only in azimuth; they are named for the nearest compass direction to each
building-aligned face:

| File | Face |
|---|---|
| `108-south-park-south.png` | shopfront, faces 135.35° (South Park) |
| `108-south-park-north.png` | rear, faces 315.35° (Taber Place) |
| `108-south-park-east.png` | party flank toward 104-106, faces 45.35° |
| `108-south-park-west.png` | party flank toward 112, faces 225.35° |
| `108-south-park-top.png` | roof, rolled so the shopfront is at the top of frame |
| `108-south-park-aerial.png` | the app's high three-quarter camera |
| `108-south-park-aerial-night.png` | the same camera, dusk pass |
| `108-south-park-contact-sheet.png` | all seven |

## Draft manifest entry

```json
{
  "id": "108-south-park",
  "file": "108-south-park.glb",
  "anchor": [-122.3944817, 37.7816789],
  "targetHeightM": 8.45,
  "cat": 5,
  "name": "108-110 South Park (South Park Cafe)",
  "estimated": true,
  "dims": [26.159, 25.719, 8.45],
  "tris": 3516,
  "loadRadius": 2500
}
```

`loadRadius`: the default rule `max(2500, 8.45 * 30)` gives 2500 m. Taken as-is.

## Stage 4 — optimize

Full detail in `optimize/REPORT.md`. Headline: 215,656 → **96,196 B raw
(−55.4%)**, 53 → **11 objects**, 58 → **13 draw submeshes**, triangles and bbox
unchanged, all eight gates PASS, worst A/B pixel delta 0.13% against a 2%/4%
limit. The pre-optimize original is archived at
`optimize/input/108-south-park.glb`. The numbers in this report and in
`validation.json` are the **shipped** numbers.

## Integration warning (Case B)

Neither `pipeline/lib/landmarks.mjs` nor `app/src/landmarks.js` knows this id, so
integration needs a registry entry **and a tile re-bake**.

**Both neighbours share this footprint's party-wall vertices at 0.00 m**, and
`excluded()` drops a footprint when its centroid *or any ring vertex* falls
inside the radius. This is the 165 South Park situation, where the only workable
circle centre turned out to be the DataSF ring's area centroid rather than the
manifest anchor, and the safe window was 0.4 m wide. **Measure the radius against
`pipeline/data/buildings_datasf.geojson` and the Overture gap-fill — not against
OSM, and never from the half-diagonal.** Getting this wrong deletes a real,
standing, historically significant neighbour from the baked city and nothing
crashes to tell you.

The procedural stand-in on this footprint is ~7.8 m and the asset is 8.45 m, so
an **unbaked** local check shows a near-perfect overlap and proves nothing. Bake
before judging.

## Approval

Stage 3 gate — user's approval, quoted verbatim with date:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION" — David, 16 August 2026
> (given up front, in the pipeline invocation, covering every gate in this run)


## Stage 5 — local integration QA

Case B. Registry entry `108SouthPark` (`exclude: 2.7`), manifest entry, GLB in
`app/public/sf-assets/landmarks/`, full twelve-stage re-bake run and QA'd, then
**discarded per batch mode** — this branch ships source only.

### Exclusion radius, measured

`excluded()` drops a footprint when its centroid OR any ring vertex is inside the
radius, and the bake reads DataSF first then gap-fills from Overture, so both
sources bind. Measured from the manifest anchor against
`pipeline/data/buildings_datasf.geojson` and `overture_buildings.geojsonseq`:

| polygon | vertex | centroid | trigger |
|---|---|---|---|
| this building, Overture `86058388` | 15.04 m | 0.21 m | **0.21 m** |
| this building, DataSF `SF3775059` | 4.09 m | 0.71 m | **0.71 m** |
| 104-106 South Park, DataSF `SF3775058` | 4.64 m | 7.91 m | **4.64 m** ← the ceiling |
| 112 South Park, Overture `0675706c` | 9.62 m | 6.28 m | 6.28 m |
| 112 South Park, DataSF `SF3775060` | 10.71 m | 6.62 m | 6.62 m |
| 104-106 South Park, Overture `aa14bd23` | 10.43 m | 6.74 m | 6.74 m |

Safe band **(0.71, 4.64)**; a sweep confirms every radius from 0.8 to 4.6 drops
exactly this building's two rings and nothing else. Shipped **2.7**, the middle,
with ~2 m of margin at both ends. At 4.7 the Gran Oriente Filipino — National
Register-nominated, no hand-built replacement — vanishes from the baked city.

### Re-bake outcome

Twelve stages (`terrain … muni-shapes`) against a warm `pipeline/data` snapshot,
2 min 20 s. `node audit.mjs` check **1.6 PASS** (66 zones over 65 landmarks
clear); 1.2b, 1.3c and 1.7b fail on `main` already and are unrelated.
`node verify-rebake.mjs`: **584 of 585 cells unchanged**, `23_13 217 -> 215`.

Decoding the tile before and after, exactly **one** footprint disappeared within
26 m of the anchor — this building's, centroid 1.0 m away. Both party-wall
neighbours survive (104-106 at 8.48 m, 112 at 6.42 m). The second dropped
footprint in the cell sits **93.5 m away**, 3.1 m from `188SouthPark`'s anchor
and inside its 5 m radius: 188 South Park was merged source-only in batch mode
(`0ce3c647`), so `main`'s tiles are stale against its registry entry and this
bake caught it up. Not caused by this change, and discarded with the rest of the
bake.

### QA table

| item | result | evidence |
|---|---|---|
| Re-validation of the shipped GLB | **PASS** | fresh-scene re-import, 16/16 checks, 3,516 tris, crest 8.450 m |
| Manifest entry | **PASS** | 59 entries, valid JSON, served by the dev server |
| id mapping | **PASS** | `camelId('108-south-park')` → `108SouthPark`, matches the registry |
| Case B registry + re-bake | **PASS** | `exclude: 2.7` measured, above |
| audit 1.6 | **PASS** | 66 zones clear |
| Single building on the site | **PASS** | tile decode: own footprint dropped, both neighbours standing; screenshot shows one building |
| Scale factor | **PASS** | console `uniform x1.0000 at 3785, -1291` |
| Orientation | **PASS** | shopfront faces the park; camera preset yaw 45 (bearing 135) lands square on it |
| Terrain seating | **PASS** | no float, no sink; ground pivot 9.5 m vs DataSF `gnd_min` 8.77 m |
| Night glow | **PASS** | transom band + one display bay + two upper windows; nothing else lights |
| Draw calls | **PASS** | 99 with 53 landmarks live (budget < 300) |
| Streaming | **PASS** | `loadRadius` 2500 m; 41 far / 18 live on boot, 53 live at the site, 0 failed |
| Fallback drill | **PASS** | GLB moved aside → app boots, `failed: 1`, one console warning, empty ground on the lot (Case B expected), both neighbours intact. Vite answers the missing file with `index.html` at 200, so the warning is a parse failure, not a 404 |
| `npm run lint` | **PASS** | eslint clean |
| `npm run build` | **PASS** | built in 1.68 s |
| Batch-mode sanity | **PASS** | `git diff --name-only origin/main` lists **nothing** under `app/public/tiles/` or `api/_data/` |
| Deployed QA | **not run** | stage 5 ends at a local verification and a ship decision (ADDRESS-TO-ASSET §5) |

### One finding worth recording

While the **unoptimized** 53-object / 58-primitive build was staged in `app/`
for a quick colour check, 25 landmarks — including this one — failed with
`THREE.BatchedMesh: Reserved space request exceeds the maximum buffer size` once
53 assets were resident at once. With the **shipped** 11-object / 13-primitive
build, the identical camera and pump gives `failed: 0`. The shared batch reserves
by geometry count, so one asset carrying 45 extra primitives is enough to
exhaust it for everybody. That is the concrete reason stage 4's submesh collapse
is not cosmetic, and the reason the optimized file is the one that ships.
