# 54-58 South Park — build report

Miniature GLB for SF-SIM, built 16-17 August 2026 from `docs/asset-plans/58-south-park.md`
via the address-to-asset pipeline (`docs/asset-pipeline/ADDRESS-TO-ASSET.md`), invoked with
`BUILDING: 58 S Park St, San Francisco, CA 94107`, `BATCH: yes`.

**This report beats the plan.** Where the dossier in the plan file and this report disagree,
this report and `REFERENCE.md` are correct.

## 1. Headline numbers

| | As built (pre-approval) |
|---|---|
| Triangles | **4,664** (cap 10,000) |
| Objects | 81 |
| Dimensions (AABB) | 28.3764 × 28.4853 × 16.90 m |
| Min Z | 0.0 |
| XY centre offset | (0.136, −0.124) m |
| Materials | 10, all `Toy_*`, flat, opaque, untextured |
| Glow materials | `Toy_glass_Glow` |
| File, raw | 281,428 B (pre-optimize) |
| Contract validation | **PASS on all 16 checks** (`validation.json`) |
| Anchor | `-122.3938881, 37.7821223` (assessor parcel centroid) |
| Target height | 16.9 m — bbox top normalized exactly, so loader scale = 1.0 |
| Parapet crest | 13.6 m |
| Front heading | 135.2° true (south-east, onto South Park) |

The AABB is ~28.4 × 28.5 m for a 9.73 × 30.10 m building. That is the expected consequence
of authoring at the real 45.2° SoMa heading, not a scale error.

## 2. Corrections to the dossier made during the build

**The plan's biggest open question is resolved: the low element is at the REAR.** The plan
left it conditional — rear step or mid-depth lightwell — and said the two give visibly
different silhouettes. It was settled by pulling the Google satellite tiles at z21 as raw
imagery (tile `x=335579 y=810539 z=21` and its 8-neighbourhood, 59 mm/px) and registering
them against the assessor parcel polygon: the roof's rear parapet sits about **3 m in from
the rear lot line**, with the strip behind it in permanent shadow from the four-storey block
in front. The asset drops the rear **4.5 m** to 4.0 m. That is 15% of the lot against the
17% a two-level fit to the LiDAR moments wants, and 4.5 m is the depth the imagery supports.

**The same registration gave the roof its programme**, which the plan could only guess at:
furniture cluster at the park end, a planting run along the south-west parapet, a glazed
element mid-depth, and a dark ~3.8 × 3.5 m structure with an adjoining raised block toward
the rear. All four are in the asset, and the dark structure is the roof office that carries
the crest. Full table in `REFERENCE.md`.

**The footprint source changed from OSM to the assessor parcel.** The plan quoted the parcel
(9.73 × 30.10 m, 292.8 m²) and it is what was built, but it is worth stating why: OSM way
`124884349` is 3% smaller and shifted ~2.3 m north-west, and the DataSF LiDAR footprint
`SF3775219` is smaller again (258.9 m²) because it is roof-derived and inset. The parcel
matches the marketed lot area to 0.5% and shares its edges vertex-for-vertex with both
neighbours' parcels, which is what a real party-wall row looks like. This matters at
integration: the exclusion radius has to be measured against the files the bake reads, not
against this polygon (see §6).

**Nothing moved the height.** 13.6 m parapet and 16.9 m crest both survived. The crest keeps
its ±1 m caveat and `estimated: true` — see `REFERENCE.md`, "The height caveat".

## 3. Design decisions, and the ones that were reversed

**The two-tone stack is built as geometry, not as colour.** The dark charcoal top storey
stands `CAP_PROUD = 0.15 m` out of the plaster on the front elevation, so the split throws a
real shadow line. Colour alone flattens at diorama scale; this is the one place semantic
exaggeration was spent (style bible §22).

**The palette roles were inverted after the first aerial.** The first build used `Toy_sand`
(`ece4d4`) for the plaster body and `Toy_stone` (`d9d2c2`) for the roof deck. That is the
wrong way round twice over: the real plaster is a light warm *gray* and the real deck is
paler than the walls, and the render showed a cream building with a slightly darker roof,
which killed the roof read. The two were swapped — body `Toy_stone`, deck `Toy_sand`,
furniture `Toy_trim` (`f3efe6`) — giving a clean value ladder walls < deck < furniture.

**The roof office's coping was coplanar with the office's own top cap** in the first build
and rendered as a black hole from above. The office box now stops at `Z_CREST − 0.16` and
the coping slab caps it.

**The roof stair block moved from `Toy_stone` to `Toy_roofd`** so it groups with the office
into one dark cluster instead of reading as a third pale object (style bible §10: organise
into clear clusters, not scattered props).

**Deck furniture was scaled up ~35%** after the first aerial, where it read as crumbs.
Semantic scale (§9), not accuracy.

**The single-storey rear roof was blank** in the first build — a pale tray with a coping and
nothing in it, directly under the app's downward camera. It now carries a rooflight, a
condenser and a planter. Four objects, 432 triangles.

**The night preview's emission strength dropped from 3.0 to 1.8.** This asset's only glow
colour is the pale blue `Toy_glass_Glow` (`6f95b8`); at the 3.0 that 101 South Park uses for
its warm oak, every lit opening clipped to flat white and the glazed bay read as a hole
punched in the facade rather than as lit glass. Render-script only — the shipped asset is
unchanged.

**Both flanks are deliberately blank.** 44-46 South Park and 70 South Park are attached at
0.00 m. Nothing on those 30 m walls is visible in the real world or in the app, and no
budget was spent there.

## 4. Contract deviations, recorded

**"Front faces −Y" is not honoured, on purpose.** The asset is authored at its real-world
heading — Blender `+Y` = true north, front outward normal **135.2°** — because
`placeGeneric()` in `app/src/assets.js` applies no rotation. This is the deviation the plans
README calls out for the 45°-rotated SoMa grid; real-world orientation wins.

**Everything is a union of closed solids and there are no booleans.** Openings are not cut
into walls: each is a dark border ring standing proud of the wall with the glass standing
proud again inside it, and the eye reads the ring as a reveal. The rear elevation of the
four-storey block is reached by placing panels on `EDGE_REAR` at a negative offset, because
that wall stands 4.5 m in front of the rear lot line.

All 81 objects pass the per-object signed-volume test outward, and the 31,500-ray cast test
returns 0 flipped visible faces.

## 5. Validation

`validation.json`, written by `validate_58_south_park.py` from a **fresh-scene re-import of
the exported GLB** (never the authoring scene). All 16 checks PASS:

| Check | Result |
|---|---|
| meters and plausible dimensions | PASS (16.9 m crest; 28.4 × 28.5 m AABB expected at 45°) |
| crest normalized to target | PASS (16.900 vs 16.9) |
| base at z = 0 | PASS (0.000) |
| centred in XY | PASS (0.136, −0.124) |
| under triangle budget | PASS (4,664 / 10,000) |
| no image textures | PASS |
| no transparency | PASS |
| materials follow contract | PASS (10, all `Toy_*`) |
| no cameras or lights | PASS |
| no animation, skin or constraints | PASS |
| transforms applied | PASS |
| no negative scales | PASS |
| normals outward, signed volume | PASS (81/81) |
| normals outward, ray residual | PASS (0.0%) |
| no degenerate geometry | PASS (0) |
| no unexpected objects | PASS |

## 6. Integration notes carried forward

- **Case B, new landmark.** Needs a `pipeline/lib/landmarks.mjs` entry and a tile re-bake.
- **Both flanks are exact party walls**, so the exclusion radius is the delicate part, and it
  must be measured against the two files the bake actually reads
  (`pipeline/data/buildings_datasf.geojson` and `overture_buildings.geojsonseq`) — not
  against the parcel polygon this asset is built on. `excluded()` drops a footprint when its
  centroid **or any ring vertex** is inside the radius, and both neighbours share vertices
  with this building's rings. Expect a radius of order 2 m, like 106 (`2.1`) and 132 (`2`)
  South Park, not the 16 m a free-standing building would take. Check *which* rings drop.
- **The procedural stand-in is the right height here** (OSM `height=14` against a 13.6 m
  parapet), so an unbaked local check will not reveal an exclusion mistake — the two will
  simply z-fight. Bake before judging.
- `loadRadius` = 2500 m (the default formula's floor).
- Batch mode: bake, QA the bake, then `git checkout -- app/public/tiles api/_data` and commit
  source only.

## 7. Draft manifest entry

```json
{
  "id": "58-south-park",
  "file": "58-south-park.glb",
  "anchor": [
    -122.3938881,
    37.7821223
  ],
  "targetHeightM": 16.9,
  "cat": 2,
  "name": "54-58 South Park",
  "estimated": true,
  "dims": [
    28.3764,
    28.4853,
    16.9
  ],
  "tris": 4664,
  "loadRadius": 2500
}
```

`cat` is `2` (apartments): two dwellings over one commercial condo. `name` is the building's
real name; the id keeps the requested address. `estimated` is `true` because no crest height
is published anywhere.

## 8. Approval

Presented at gate 3 on 17 August 2026: contact sheet, aerial day and night renders, and the
numbers line.

The owner's approval for this run was given **in advance**, in the session's opening
instruction, verbatim:

> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

That is a standing authorization for the pipeline's internal gates, and it is what advances
this asset to stage 4. It is recorded here rather than treated as silent consent, and it is
weaker evidence than a decision taken after seeing the renders — if the design is revised
later, that is a normal stage-2 loop, not a broken gate.

It does **not** cover push, PR or deploy. Stage 5 still ends at a local commit and asks.
