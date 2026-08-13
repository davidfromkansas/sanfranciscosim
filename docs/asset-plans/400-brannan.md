# 400 Brannan Street — SF-SIM asset plan

The 1905 corner block at Third and Brannan: a low two-storey commercial/industrial
building that holds the west corner of the intersection with two full street
elevations and nothing else. Not a monument and not even a character piece in the
380 Brannan sense — its job in the city is *corner*: a light stucco box with a dark
base, wide industrial sash upstairs, a row of black awnings over shopfronts on both
frontages, and a roll-up freight door at the far end. It is the building that makes
the 3rd/Brannan crossing read as a real intersection instead of a gap.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/400-brannan/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `400-brannan` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3946805, 37.7800981` |
| Target height | **8.8 m** to the roof bulkhead; parapet crest 8.6 m; roof deck 7.77 m (LiDAR median) |
| Footprint | 23.89 m (Third Street frontage, NE) x 23.07 m (Brannan frontage, SE); 489.4 m2, measured |
| Triangle cap | 8,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 400 Brannan Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 400 Brannan Street (also addressed
588–592 Third Street) in San Francisco and deliver it as a downloadable, validated GLB.

Do not integrate or deploy the model yet. Create the asset, validate it, render
review images, and commit the deliverables to your working branch.

## Read the project sources first

Before any research or modeling, read in this order:

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-miniature-style/SKILL.md`
5. `.agents/skills/sf-asset-check/SKILL.md`
6. `app/public/sf-assets/landmarks_manifest.json`
7. `artifacts/380-brannan/` — the closest reference implementation in scale, budget
   and character (two-storey SoMa masonry box at a 45° heading, designed flat roof,
   restrained night state). Its `build_380_brannan.py` is the script skeleton to
   adapt, not to rewrite.
8. `docs/asset-plans/400-brannan.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules.

## Must capture

- A low, chunky **two-storey** box with a flat roof and a continuous parapet, holding
  a street corner with **two finished elevations meeting at a sharp 90° corner**
- The **light upper wall over a dark base** — the building's whole tonal identity
- The **row of black shopfront awnings** running along both frontages
- Wide **horizontal industrial sash windows** upstairs (landscape, not portrait —
  this is what separates it from every residential neighbour)
- The white **roll-up freight door** at the southwest end of the Brannan elevation
- A designed flat roof: parapet ring, vent/mechanical scatter, one roof bulkhead

## Research 400 Brannan Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- Both street elevations (Third and Brannan) and, if any view exists, the two party
  flanks
- Aerial and roof views (vent layout, bulkhead, parapet)
- Ground-level views day and night
- The **paint scheme**, which is the one thing this dossier is least sure of: 2016
  street-level photography shows cream stucco with chocolate bands; 2019 photography
  of the same tenant frontage reads light-gray over charcoal. Decide from the most
  recent imagery you can find and record the decision in `REPORT.md`
- The bay count and window rhythm of both frontages — the dossier's readings are
  *inferred* from oblique photography

**Two source traps are already known and resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:** there is **no parcel numbered 400 Brannan** in
the SF parcel layer (Brannan's even numbers jump 376–380 → 414), and Nominatim's
"400 Brannan" is a POI node, not a building; the address resolves through the EAS
address layer to block 3776 lot 114, whose primary address is **590 Third Street**.
And the DataSF LiDAR `hgt_max` of 11.65 m on this footprint is **not** the crest —
it is a +6σ outlier over a roof whose height standard deviation is 0.64 m, almost
certainly the street tree that overhangs the Brannan kerb.

## Create a reference dossier

Write `artifacts/400-brannan/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3–5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. Do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade into
broad rhythms, deliberately design every surface visible from above, evaluate from
the app's high three-quarter aerial camera, then simplify again.

This is a **secondary building** in the style bible's detail budget (§21). Its one
spent exaggeration is the awning row: thickened so it survives at thumbnail size and
carried around the corner, because a continuous dark shelf at shopfront height is
what makes a corner building read as a corner building from the air.

The finished asset must be immediately recognizable as this corner, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single corner block: body, parapet, both street elevations' openings,
awnings, roll-up door, roof deck and roof furniture.

Do not include unrelated surrounding city geometry: Third Street, Brannan Street, the
neighbouring 566–586 Third Street complex behind it, traffic signals, the street tree
on the Brannan kerb, the sidewalk, parked cars, people, plinths, cameras or lights.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ≈ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project
palette; `_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no
cameras, lights, animations, armatures or constraints; at most 8,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The **Third Street
elevation faces northeast, bearing 45.2°**; the **Brannan Street elevation faces
southeast, bearing 135.2°**. Build directly on the measured footprint polygon in 2.3
rather than modelling an axis-aligned box and rotating it. Record the measured
headings in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the roof bulkhead) must
land at exactly **8.8 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/400-brannan/build_400_brannan.py` (deterministic build script),
`artifacts/400-brannan/400-brannan.blend`, and `artifacts/400-brannan/400-brannan.glb`.
The script must rebuild the model reliably enough for future revision.

## Required review renders

Render the exact final geometry from controlled cameras: `400-brannan-top.png`,
`400-brannan-north.png`, `400-brannan-east.png`, `400-brannan-south.png`,
`400-brannan-west.png`, plus `400-brannan-contact-sheet.png`, at least one high
three-quarter aerial beauty render `400-brannan-aerial.png`, and a night render
`400-brannan-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; the
top view must clearly show the parapet ring, the vent scatter and the bulkhead. Note
that the aerial camera should be placed to see the **corner**, not a flat elevation —
this building's whole subject is the corner.

## Validate the exported GLB

Re-import `400-brannan.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Write `artifacts/400-brannan/validation.json` and
`artifacts/400-brannan/REPORT.md`.

The axis-aligned XY bounding box will be roughly **31 x 33 m** even though the
building is 23.9 x 23.1 m — that is the expected consequence of a 45° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "400-brannan",
  "file": "400-brannan.glb",
  "anchor": [
    -122.3946805,
    37.7800981
  ],
  "targetHeightM": 8.8,
  "cat": 3,
  "name": "400 Brannan Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/400-brannan.md`.
````

---

## Part 2 — Research and design dossier

Compiled 13 August 2026 from the sources in 2.2. Values marked *inferred* are visual
or derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address resolution | `400 BRANNAN ST` → parcel **3776114** (block 3776, lot 114) | DataSF EAS address layer (`ramy-di5m`) — **measured**, see 2.15 |
| Other addresses on the same parcel | 406 and 410 Brannan St; primary assessor address **590 Third St** | EAS; SF Assessor roll |
| Built | 1905 | SF Assessor secured roll 2025, block 3776 lot 114 |
| Storeys | **2** | SF Assessor roll (`number_of_stories = 2`); confirmed by street-level photography on Brannan |
| Use | Industrial (`IND`), 1 unit, 22 rooms | SF Assessor roll — a shopfront-and-loft commercial block, not a factory |
| Lot area | 5,318 sq ft (494 m2) | SF Assessor roll — within 1% of the LiDAR footprint, i.e. full-lot coverage |
| Footprint | 489.4 m2; 23.89 m (NE, Third St) x 23.07 m (SE, Brannan) x 20.38 m (SW rear) | DataSF building footprints (`ynuv-fyni`, `mblr = SF3776114`), reprojected — **measured** |
| OSM footprint (cross-check) | 478 m2 | OSM way/124903637 (`source=Bing`, `height=8`) — agrees within 2.3% |
| Roof deck height | **7.77 m** above ground | DataSF LiDAR `hgt_median_m` (mode 7.82, mean 7.69, σ 0.64 over 1,946 cells) — **measured** |
| LiDAR maximum | 11.65 m | DataSF LiDAR `hgt_maxcm` — **rejected as the crest**, see 2.15 |
| Parapet crest | ~8.6 m | *inferred*, deck + ~0.85 m parapet |
| Ground elevation | 6.94–7.24 m (NAVD88) | DataSF LiDAR `gnd_min_m` / `gnd_mediancm` — the app's terrain handles this, not the asset |
| Frontage headings | Third St front faces **45.2°** (NE); Brannan front faces **135.2°** (SE) | measured from the footprint polygon |
| Current tenants | Avant Barre (studio, 400 Brannan), a gallery/retail unit at 406–410, Cafe Buenos Aires (590 Third) and Kinoko (592 Third) on the Third Street side | OSM POI nodes; DataSF registered-business file; street-level photography |

### 2.2 Sources

- `https://data.sfgov.org/resource/ramy-di5m` (DataSF EAS Addresses) — the only source that ties "400 Brannan" to a parcel at all
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — address ranges per block/lot; establishes that no parcel is *numbered* 400 Brannan
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — the authoritative footprint polygon and the 7.77 m / 11.65 m heights
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — 1905, 2 storeys, industrial use, lot area
- `https://www.openstreetmap.org/way/124903637` — cross-check footprint, `height=8`
- KartaView / OpenStreetCam sequence 7003 (frame `574e630a394a5`, capture 2016-05-31), Brannan Street approaching Third — the clearest single view of the Brannan elevation: address plates 410 / 406 / 400, black awnings, roll-up door, upper sash band
- KartaView sequence 1352479 (frames 34–36, capture 2019-03-14), Third Street at Brannan — the Third Street elevation and the current tonal scheme
- Esri World Imagery (z20 nadir, 2023 vintage) — roof: flat dark membrane, vent scatter, one light-roofed appendage at the north corner, street-tree canopy overhanging the Brannan kerb

### 2.3 Orientation and placement

The building holds the **west corner** of Third and Brannan: its northeast elevation
fronts Third Street, its southeast elevation fronts Brannan Street, its southwest side
is a party wall against the interior of block 3776, and its northwest side is a
stepped party wall against the 566–586 Third Street apartment complex
(`docs/asset-plans/574-third.md` — the two share a wall and are being built in the
same batch).

Measured DataSF footprint, in Blender coordinates (metres, `+X` east, `+Y` north),
already centred on the anchor `-122.3946805, 37.7800981` (the axis-aligned bounding-box
centre, which is what the loader's origin convention needs):

```
( -1.365,  16.605)   N corner
( 15.485,  -0.335)   E corner
( -0.875, -16.605)   S corner
(-15.485,  -2.395)   W corner
( -2.955,  11.195)   inner corner of the NW notch
```

That five-vertex simplification of the 13-vertex survey ring encloses 491.7 m2 against
the survey's 489.4 m2 (+0.5%); the discarded vertices are sub-1.5 m jogs in the
northwest party wall. Build on this polygon.

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| N→E | 23.89 m | NE 45.2° | **Third Street front** |
| E→S | 23.07 m | SE 135.2° | **Brannan Street front** |
| S→W | 20.38 m | SW 224.2° | rear party wall (block interior) |
| W→notch→N | 8.2 + 14.6 m | NW ~315.6° | party wall against 566–586 Third |

Because of the 45° heading the axis-aligned bounding box is ~31 x 33 m. That is correct.

### 2.4 What each side shows

**Southeast (Brannan Street)** — Documented in 2016 photography. A flat two-storey
stucco wall over a masonry base. Top to bottom: a plain parapet with no cornice; a
band of **wide horizontal steel/aluminium sash windows** on the upper floor, roughly
square-to-landscape, several with through-wall air-conditioners hanging out of them; a
horizontal band marking the floor line; then the shopfront level — a white roll-up
freight door at the southwest end, then a run of glazed shopfronts under **black
awnings**, with the address plates 410, 406 and 400 reading from southwest to
northeast. Two black gooseneck lamps are fixed to the upper wall. The whole elevation
is a light warm tone over a dark base band.

**Northeast (Third Street)** — The same two-storey composition turning the corner,
with a longer run of shopfronts (Cafe Buenos Aires at 590, Kinoko at 592) under the
same black awning line, and the same upper sash band. This face reads slightly more
"retail" than Brannan: more glass, no freight door.

**Southwest and northwest (party walls)** — Blank painted masonry with sparse
openings; the northwest wall is stepped where the 574 Third complex meets it. Neither
is visible from the street. They are visible from the app's aerial camera, so build
them as finished, quiet wall planes — no invented window grid.

**Top** — A flat, dark membrane roof inside a continuous parapet. Nadir imagery shows a
loose scatter of small vents and units grouped toward the middle of the deck, one
square skylight-sized element, and a light-roofed appendage at the north corner. The
big dark blob over the Brannan edge is the street tree, not a roof feature.

### 2.5 Recognition cues (ranked)

1. **The corner itself** — two finished elevations meeting at a sharp 90° corner on the
   city's diagonal grid, only two storeys tall where everything around it is three or
   more
2. Light upper wall over a dark base
3. The continuous **black awning line** carried around both frontages at shopfront height
4. Wide **horizontal** industrial sash windows upstairs
5. The white roll-up freight door at the southwest end of Brannan

### 2.6 Miniature translation

**Preserve**

- The single-volume box, the real 45° heading, and the notched party wall
- The two-tone split: light body, dark base
- The awning line as a continuous dark shelf turning the corner
- The landscape proportion of the upper windows

**Simplify / exaggerate**

- The upper sash band becomes 6 identical bays on Third and 6 on Brannan
- Air-conditioners, gooseneck lamps, signage lettering and address plates all disappear
- The awnings are thickened to ~0.45 m deep and 0.35 m tall so they survive at
  thumbnail size — this is the one place semantic exaggeration is spent
- Shopfronts become one recessed dark glazed band per frontage, divided by piers,
  rather than individually modelled units
- The roof vent scatter becomes three small units, one hatch and one bulkhead

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 footprint from z=0 to z=7.77, `Toy_sand`. Its top cap is the
   roof deck (`Toy_roofd`).
2. Base band: a 0.10 m proud skirt on both street edges, z=0 to z=0.75, `Toy_ink`.
3. Shopfront level, z=0.75 to z=3.55: on each street edge, a recessed glazed band
   (`Toy_glass`) inset 0.25 m, broken by 0.5 m piers in `Toy_sand`; on Brannan, replace
   the southwest-most 4.0 m of that band with the roll-up door (`Toy_trim`, horizontal
   ribbing implied by two shallow grooves, not modelled slat by slat).
4. Awning line: a continuous `Toy_ink` shelf at z=3.55–3.90, projecting 0.45 m, running
   the full length of both street edges and mitred round the corner.
5. Floor-line band: 0.22 m `Toy_stone` course at z=4.05, both street edges.
6. Upper floor, z=4.55 to z=6.95: 6 bays per street edge, openings 2.4 x 1.9 m
   (landscape), recessed 0.18 m, `Toy_glass` with `Toy_trim` frames.
7. Parapet: z=7.77 to z=8.6, following the footprint, 0.35 m thick, `Toy_sand` with a
   `Toy_stone` coping in the top 0.16 m.
8. Roof deck at z=7.77, `Toy_roofd`: three mechanical boxes (1.8 x 1.3 x 0.8 m,
   1.2 x 1.0 x 0.6 m, 0.9 x 0.9 x 1.0 m) in `Toy_steel`, one hatch 1.4 x 1.1 x 0.45 m,
   and the bulkhead 3.2 x 2.4 m from z=7.77 to **z=8.8** in `Toy_roofd` — this sets the
   bounding-box top and must land exactly on 8.8.
9. Bevel 0.12 m, 2 segments on the chunky solids; 0.05 m / 1 segment on window frames;
   none on fills and glow shells.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_sand` | `#ece4d4` | upper wall, piers, parapet |
| `Toy_stone` | `#d9d2c2` | floor-line course, parapet coping |
| `Toy_ink` | `#3a3530` | base band, awnings, shopfront reveals |
| `Toy_glass` | `#2a4d73` | shopfront glazing and upper sash |
| `Toy_trim` | `#f3efe6` | window frames, roll-up door |
| `Toy_roofd` | `#45454a` | roof deck, hatch, bulkhead |
| `Toy_steel` | `#9aa0a6` | roof mechanical units |
| `Toy_glass_Glow` | `#6f95b8` | a few lit upper windows at night |
| `Toy_trim_Glow` | `#f3efe6` | the shopfront band under the awnings at night |

Note on the paint scheme: 2016 photography shows cream stucco with chocolate-brown
bands; 2019 photography of the same frontage reads light-gray over charcoal. The
scheme above (warm light body, near-black base) is the common denominator and matches
the more recent evidence. If newer imagery settles it, follow the newer imagery and
record the change.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
glazing — the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a
primary surface must never be authored as glow. Hero glow: the shopfront band under
the awnings, on both frontages — this is a corner with cafés on it, and a lit ground
floor under a dark awning is exactly what that looks like at night. Supporting accent:
three or four lit upper windows, not the whole band.

### 2.9 Top surface

A 490 m2 flat roof only 7.8 m up, in a district the camera flies over constantly and
close to. Keep the deck clearly darker than the parapet coping so the ring reads from
above, group the mechanical units off-centre toward the block interior (matching the
nadir imagery) and leave the street-facing third of the deck comparatively clean — the
real roof is empty there.

### 2.10 Scope

**In the GLB:** the single corner block — body, base, shopfronts, awnings, roll-up
door, upper sash bays, parapet, roof deck and roof furniture

**Not in the GLB:** Third Street, Brannan Street, the 574 Third complex behind, the
street tree, traffic signals, sidewalk, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 8,000 — a secondary building with two finished elevations rather than one.
Suggested split: body, parapet and base ~1.5k, upper window bays (12) ~2.5k,
shopfront bands and piers ~1.5k, awnings ~0.6k, roof furniture ~1.2k.

### 2.12 Draft manifest entry

```json
{
  "id": "400-brannan",
  "file": "400-brannan.glb",
  "anchor": [
    -122.3946805,
    37.7800981
  ],
  "targetHeightM": 8.8,
  "cat": 3,
  "name": "400 Brannan Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark (Case B).** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: '400Brannan'`, lon/lat as above, `height: 8.8`) and re-bake the affected tiles,
  or the baked procedural building on this exact footprint will intersect the GLB.
- **Exclusion radius must be measured, not guessed.** This is a corner lot whose
  northwest party wall is shared with the 1,906 m2 complex at 566–586 Third — a
  neighbour so large that its footprint centroid is far away (30 m) while its nearest
  *vertex* is on this building's own wall. `excluded()` tests every ring vertex as well
  as the centroid, so size the radius against the real bake input
  (`data/buildings_datasf.geojson`) and expect the safe band to be narrow. Start the
  measurement at ~8 m and walk it up until a second building drops.
- `loadRadius`: the default formula gives `max(2500, 8.8 × 30) = 2500` m. Take the default.
- This is the third asset on this block face (with `550-third` and `574-third`) and the
  sixth in the Brannan family. Batch mode applies — see 2.15.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 8.8 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~31 x 33 m is expected)
- [ ] Triangles at or under 8,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the shopfront band and a few upper windows; glow shells proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual ≤ 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The address does not exist as a parcel.** SF's parcel layer has no lot numbered 400
  Brannan: even numbers run 376–380 (block 3775, the 380 Brannan lot) and then jump to
  414 (block 3776). Only the EAS address layer carries `400 BRANNAN ST`, on block 3776
  lot 114, together with 406 and 410 — and that lot's assessor address is 590 Third
  Street. This is the same class of failure as 350 Brannan (plans README): a geocoder
  will hand you a POI node or a roadway. Resolve address → EAS → parcel → footprint,
  and never trust a geocoder result whose `osm_type` is not a building.
- **The LiDAR maximum is not the crest.** 11.65 m sits +6σ above a roof whose height
  standard deviation is 0.64 m and whose minimum (2.40 m) is plainly vegetation; the
  nadir imagery shows a large street-tree canopy breaking over the Brannan parapet.
  The crest used here is the inferred parapet at 8.6 m, and the 8.8 m target is set by
  a modest roof bulkhead. If newer LiDAR or a photograph shows a real stair penthouse,
  raise the target to match it and re-normalize.
- **The paint scheme changed between 2016 and 2019** and may have changed again. See 2.8.
- The 6-bay window rhythm on each frontage is *inferred* from oblique photography and
  is the weakest number in this dossier.
- Whether the northwest party wall is truly shared (zero gap) with 566–586 Third or has
  a light gap is unresolved; the survey rings touch, so model both walls as finished and
  let the exclusion measurement decide the rest.
- No architect is recorded for the 1905 building in any source consulted.
- **Batch:** this asset is being built alongside `574-third`, which shares its northwest
  party wall. Stage 5 must run in batch mode (source-only branch, bake discarded) or the
  two landmarks' tile re-bakes will collide.
