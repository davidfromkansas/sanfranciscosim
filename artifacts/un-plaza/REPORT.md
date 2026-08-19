# United Nations Plaza — build report

Deliverable of stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md` for the
building brief *"UN Plaza, 355 McAllister St"*. Built from
`docs/asset-plans/un-plaza.md`; every correction to that plan is recorded here,
and **REPORT beats plan**.

## 1. Numbers

| | |
|---|---|
| File | `un-plaza.glb` |
| Triangles | **16,778** shipping / 16,934 pre-optimize (cap 18,000; hard gate 30,000) |
| Bytes | **452,532** shipping (meshopt, stage 4); pre-optimize 911,264 |
| Draw submeshes | **26** shipping / 62 pre-optimize |
| Dimensions | **215.22 × 157.94 × 13.00 m** |
| min Z | 0.0000 |
| XY centre offset | 0.0000, 0.0000 |
| Mesh objects | 22 shipping / 57 pre-optimize |
| Materials | 19 `Toy_*`, three of them `_Glow` |
| Anchor | −122.4138900, 37.7801415 |
| Height datum | tallest tree crown, exactly 13.00 m |
| Light standards | 16, max position error **0.00 m** against the measured survey |
| Colonnade bearing (both rows) | 81.03° / 81.03° true |
| Market frontage bearing | 45.20° true |
| Normals | signed volume outward on **57/57** objects; ray-test flipped fraction **0.000000** |
| Validation | `validation.json` — **overall PASS**, 21/21 checks (authoring side); `optimize/gates.json` — G1–G5 all PASS (shipping side) |

## 2. What was verified before modelling, and what changed

**The brief named the wrong site.** "355 McAllister St" is Civic Center Plaza
(DataSF parcel `0788001`), which is already integrated as `civic-center-plaza`
at that exact anchor. United Nations Plaza is 340 m east. This asset is United
Nations Plaza. Recorded in the plan's §2.15 risk 1 and in REFERENCE.md §1.

**Both grid bearings were re-derived from DataSF, not inherited.** A
least-squares fit over the OSM plaza ring's own long edges gives 80.42°;
McAllister's centrelines read 80.96° over seven consecutive blocks and
`civic-center-plaza` is built on 80.94. The 0.5° gap is OSM digitising drift and
is worth 1.9 m at the plaza's east end. The model is built on **80.94 / 350.94**.
The Market frontage is the opposite case: the ring's own 134.6 m Market edge
reads 45.18° against DataSF's 45.20°, so it is trusted as drawn — the model uses
**45.20**.

**The fountain's heights are surveyed, and the plan did not know it.** DataSF's
LiDAR building layer (`ynuv-fyni`) captured nine of the fountain's granite
masses as buildings, with footprints *and* `hgt_maxcm`. Those nine are modelled
at their surveyed positions and heights, crest **4.03 m**. This is the only
fully surveyed element in the asset and it is asserted in the validator.

## 3. The height datum — a deliberate choice, recorded

`targetHeightM = 13.00 m` is the **authored** height of the tallest London plane
crown, not a survey. No element of this plaza has a published height.

That is safe here, and the reasoning matters because `civic-center-plaza` §2.15
risk 1 warns about exactly the opposite case. Because `targetHeightM` is set
**equal to the model's authored maximum**, the loader's
`targetHeightM / measuredHeight` scale is exactly 1.0 and the 215 m ground plane
is correct *by construction*, whatever the real trees measure. The datum was
deliberately put on a **broad** object rather than a thin pole so that a future
correction moves one crown rather than rescaling the plaza. Every other vertical
in the asset — the 4.03 m fountain crest, the 5.18 m obelisk, the 5.90 m
standards, the 8.10 m Bolívar — is an independently sourced number and is
authored at that number, not scaled to fit.

The manifest entry is marked `"estimated": true` to say so.

## 4. Tree positions are inferred, not surveyed

The plaza's trees are not in OSM — only four, at the 7th-and-Market corner. The
54 positions in `data/trees_en.json` are derived from the three measured bed
outlines and from canopy positions read off the z20 aerial, with a deterministic
hash jitter, and are written out by the build script so the inference is
reviewable in a diff rather than buried in code. Wikipedia records 192 London
plane and black poplar trees along the promenade in 1975; far fewer stand today.
**This is the largest visual assumption in the asset** and it should be
re-checked against recent photography if the asset is ever revised.

## 5. Defects found and fixed during the build

Every one of these was found by looking at a render or at `validation.json`, and
each is the kind of thing that ships silently:

1. **The UN emblem rendered as a black square.** The first Z ladder put the
   granite inlays at 0.32 and the walks at 0.34, which enclosed the emblem
   *inside* the walk solid. Fixed by putting inlays above walks (0.36 / 0.33).
2. **The fountain read as a pale octagonal plateau** with the granite pile
   buried inside it, because its rim was a filled prism rather than a kerb.
   Fixed by adding `ring_prism()` and building kerb + bench + sunken floor.
   The basin floor then had to be lifted to +0.32, *above* the brick plate,
   because the plate covers the whole ring and a floor at +0.04 is invisible.
3. **Market-aligned paving bands ran clean off the plate** at both ends. Fixed
   by adding `clip_span()`, which walks each band against the ring and emits
   only the contiguous run that is inside it.
4. **The Market direction had its sign flipped** (`HEADING_MARKET − HEADING_E`
   instead of `HEADING_E − HEADING_MARKET`), which sent the frontage band out of
   the plaza within a few metres and left `walk_market` unbuilt entirely — and
   the validator caught it as a missing bearing, not as a wrong one.
5. **256 degenerate triangles** in `columns`: the shaft top and the globe's
   underside were both at 5.28 m, so the neck frustum collapsed to zero height —
   16 zero-area side quads per column. Fixed by lowering the shaft to 5.05.
6. **The night state was two light-sabres.** The festoon lighting was authored
   as one 86 m glowing rail per column row, which buried the sixteen globes the
   night state is supposed to be about, and it sat on the column rows so the two
   glow families interleaved into one indistinguishable line. Fixed twice: to
   0.34 m bulbs at 2.4 m pitch, and moved to the promenade centreline.
7. **A 46 m lit strip on the skate pad read as a runway.** Replaced with four
   bollard-scale pools.
8. **The crowns cost 22,134 triangles** — the bevel pass caught them because
   `crowns` was not in `UNBEVELLED`. Also `bike_racks` and `fitness`. Total went
   40,082 → 17,340.
9. **Two closed frusta stacked on a shared ring bury a pair of coincident,
   opposite-facing caps** — invisible in every render, but stage 4's weld
   collapses them and the coplanar dissolve merges them into one face, breaking
   the shell. `globes_glow` came out of Phase B at signed volume **−1.620**
   against **+1.365** in the source. Fixed at source with a `profile()` helper
   that emits a solid of revolution in one piece with no internal caps; the
   globes, tree crowns and obelisk were rewired onto it, which also removed 838
   buried triangles (17,772 → 16,934). Full write-up in `optimize/REPORT.md`.
10. **The studio floor in the review rig was sized off the model's HEIGHT**
   (65 m), so it appeared as a beige rectangle inside the frame of a 215 m
   asset. Now sized off the plan.

## 6. Integration notes measured during this build

Measured against `app/public/tiles/buildings/20_13.bin`, so they are against
what is actually baked rather than against OSM:

- **Seven baked footprints stand inside the plaza and all seven are the
  fountain.** DataSF's LiDAR slabs, extruded by the procedural builder to
  3.1–8.5 m. The asset cannot be judged before the re-bake.
- **There is no usable exclusion radius at the anchor.** The nearest neighbour
  vertex is 4.76 m away (50 UN Plaza, the Federal Building), and the farthest
  fountain block needing to be dropped is 57.51 m. `exclude` is omitted.
- **One `extraExclusions` circle clears all seven**: centre
  `(−122.4133237, 37.7800778)`, band (25.77, 34.76) m, **ship r = 30**. Nearest
  protected neighbour `20_13#17` (1,171 m², 43.1 m) at 34.76 m.
- **`clearTrees` is not needed.** `pipeline/landcover.mjs` scatters trees only
  on `KIND.trees` and `KIND.grass`; this plaza's outer polygon is
  `highway=pedestrian` + `place=square`, which maps to no landcover kind, and
  its inners are `natural=sand` and `leisure=pitch`.

Full working in `docs/asset-plans/un-plaza.md` §2.13.

## 7. Draft manifest entry

```json
{
  "id": "un-plaza",
  "file": "un-plaza.glb",
  "anchor": [
    -122.4138900,
    37.7801415
  ],
  "targetHeightM": 13.0,
  "cat": 0,
  "name": "United Nations Plaza",
  "estimated": true,
  "dims": [
    215.22,
    157.94,
    13.0
  ],
  "tris": 16778,
  "loadRadius": 2500
}
```

`dims` and `tris` are the **shipped** figures, measured after stage 4.

## 8. Files

| File | What it is |
|---|---|
| `build_un_plaza.py` | deterministic build; `blender -b --python build_un_plaza.py` |
| `render_un_plaza.py` | controlled review renders from the **exported GLB**; `-- --night` for the dusk pass |
| `validate_un_plaza.py` | fresh-scene contract validation of the exported GLB |
| `make_contact_sheet.py` | composes the eight review images |
| `data/elements_en.json` | every measured element in the plaza `(e, n)` frame |
| `data/trees_en.json` | the inferred tree positions, written by the build |
| `data/osm_raw.json`, `data/frame.json` | the raw Overpass pull and the frame definition |
| `validation.json` | machine-readable validation, **overall PASS** |

## 9. Approval

Stage 3 gate, satisfied by a standing pre-authorisation given with the building
brief on **2026-08-19**, quoted verbatim:

> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

The contact sheet, the day and night aerials and the top view were presented at
the same time rather than held for a reply, per that instruction. The numbers
presented were those in §1.
