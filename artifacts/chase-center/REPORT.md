# Chase Center — build report

`artifacts/chase-center/chase-center.glb`, produced by
`build_chase_center.py` (deterministic, headless Blender 5.2.0 LTS) for the
address-to-asset pipeline run on `BUILDING: 1 Warriors Wy, San Francisco, CA 94158`.

**This report beats the plan.** Where `docs/asset-plans/chase-center.md` and this
file disagree, this file is what was built and why — §4 lists every correction.

## 1. Shipped numbers

| | |
|---|---|
Numbers below are the **shipped** file — post stage-4 optimize. The
pre-optimize authored export is archived at `optimize/input/chase-center.glb`
and its figures are in brackets.

| | |
|---|---|
| Triangles | **11,289** (cap 27,000) [authored 11,660] |
| Mesh objects | 11 [authored 40] |
| Dimensions | 164.364 × 159.127 × **40.803** m [40.800] |
| Min Z | 0.000 |
| Bbox top | 40.803 — so `targetHeightM / measuredHeight` = **0.999936** |
| Draw submeshes | 14 [authored 43] |
| Materials | 10, all `Toy_*`, flat, opaque, no textures |
| Glow materials | `Toy_sky_Glow` (video board), `Toy_white_Glow` (atrium lobby + west parapet cove) |
| File | **98,220 B raw / 64,174 B gzip** [581,884 / 143,720] |
| Validation | `validation.json` — **overall PASS**, all 15 checks |
| Optimize | `optimize/REPORT.md` — gates G1–G6, G8 **PASS**, G7 n/a |

## 2. What was built

A pale aluminium drum on the arena's real 155 m plan, with:

- a stone plinth, a recessed dark glazed retail band and a concourse band, so
  the drum reads as floating;
- 40 vertical panel bands (0.70 m deep, ~12 m pitch) — the compressed stand-in
  for ~7,500 real mega-panels;
- one ledge at 20 m, the "stacked drums" cue from the Enclos description;
- the **sail**: the whole upper skin rises from 32.9 m on the bay side to the
  40.8 m crest over the west entry, following
  `32.9 + 7.9·((1+cos(θ−270°))/2)^2.2`;
- a crest course oversailing 0.25 m, carrying Warriors gold on its outer face
  and top through ±20° of the entry axis, and the night cove light on its
  exposed underside through ±45°;
- the west entry: a glazed slot in the skin with a pale reveal (two cheeks and a
  head), four steel fins, a pale canopy and the lit lobby band behind it;
- the video board on the WNW facade at 26 × 13 m in a navy frame — the
  night-glow hero;
- the roof: pale membrane, the raised bowl deck, a perimeter catwalk, one
  central mechanical cluster and twelve panel pads on a 61 m ring.

## 3. The plan shape — the one substantive research finding

The plan called the footprint a rounded square with a 34 m corner radius. That
implies 22,800 m²; the surveyed polygon is **19,465 m²**. Fitting alternatives
against the 66 OSM vertices:

| Candidate | Result |
|---|---|
| rounded square, R = 34 m | area off by +17% |
| ellipse | area −4%, radial residual to 13 m |
| best-fit superellipse (n = 1.889) | radial rms 5.3 m, max 13.6 m |
| **6-harmonic radial curve about the centroid** | **radial rms 2.03 m, area within 0.1%** |

The real plan is a lobed blob — r = 85.6 m to the north-east, 71.8 m to the
north-west — so the asset is driven by the harmonic fit (`R0` and `HARM` in the
build script), not by an idealised primitive. This is what makes the top view,
the surface the app's camera actually sees, read as Chase Center.

The **anchor** moved with it: the model centres on the polygon centroid, 3.4 m
from the oriented-box centre the plan quoted. The pipeline requires the anchor to
come from the geometry the model centres on, so the manifest anchor is the
centroid.

## 4. Dossier corrections made during the build

Each came out of a review render; all are also recorded in `REFERENCE.md` §8.

| # | Plan said | Built | Trigger |
|---|---|---|---|
| 1 | anchor `−122.387433, 37.767883` | `−122.3873962, 37.7678739` | anchor must be the centroid the model centres on |
| 2 | rounded square, R 34 m | 6-harmonic fit to the surveyed outline | §3 |
| 3 | 60 bands × 0.55 m | 40 bands × 0.70 m | first aerial read as corrugated tin, not mega-panels |
| 4 | swooping **parapet** on a flat drum | the whole upper **skin** swoops | the parapet version was invisible from the aerial camera — the swoop has to be in the silhouette |
| 5 | navy entry canopy | pale `Toy_trim` canopy; navy moved to the board frame | `Toy_navy` canopy over `Toy_glass` glazing merged into one dark blob |
| 6 | atrium projecting 15 m | a glazed slot 0.3 m proud + pale reveal + 6.5 m canopy | the projecting box read as a shed bolted to an arena |
| 7 | 6 roof units on a 46 m ring | 4 units flanking one block + 12 ring pads | scattered props; style bible §10 asks for clusters |

## 5. Iteration log

1. **Build 1** (9,604 tris) — first aerial. The entire roof rendered **black**:
   the drum's top cap and the roof deck were both at exactly z = 31.8, and
   Cycles z-fought the coplanar pair. Fixed by burying the drum cap and lifting
   the membrane; every stacked element now overlaps by 0.2–0.5 m rather than
   meeting flush. Also: roof props scattered, bands too fine.
2. **Build 2** (12,940 tris) — roof reads. Entry still a blue shed; the swoop
   still invisible. Corrections 3, 5, 6, 7.
3. **Build 3** (11,552 tris) — the swoop moved from the parapet into the skin.
   Silhouette now carries it. West elevation showed the entry reveal missing:
   dark glazing butted straight into dark retail band.
4. **Build 4** (11,660 tris, shipped) — pale reveal, canopy narrower than the
   slot, larger roof plant cluster.
5. **Validator fix** — the first run reported every object non-manifold. The
   check was wrong, not the geometry: the glTF importer splits vertices at
   flat-shaded edges, so index-based edge pairing calls a perfect cube
   non-manifold. Re-keyed by position; signed volumes were positive throughout
   and the ray residual was 0.000 on both runs.
6. **Night render fix** — the video board rendered as a pure white slab. Two
   causes: emission strength 6.0 clipped through the Standard view transform,
   and more importantly glTF writes `emissiveFactor = 0` when the authored
   emission strength is 0, so a **re-imported `_Glow` material carries a default
   white emission**. The night rig now drives emission from Base Color at
   strength 1.0, which is exactly what the app's unlit night overlay does. Worth
   knowing for every future asset's night render.

## 6. Orientation — recorded contract deviation

The contract's nominal "front faces −Y" cannot be honoured. Chase Center's main
entrance faces **west**, onto the Thrive City plaza (OSM "West Entrance" node,
76 m west of the centroid; Box Office NW, Bayfront Park E). Per
`docs/asset-plans/README.md`'s orientation note, real-world orientation wins
(AGENTS rule 5) and the model is authored with Blender +Y = true north,
+X = east. `placeGeneric()` applies no rotation, so it drops in at its real
heading. The plan's oriented box sits 169.9° from east — ~10° off axis, not a
visible rotation on a lobed blob, and not applied.

## 7. XY centring

`xy_center_offset_m` is `[−3.9, 1.85]`, not `[0, 0]`. The **origin** is the
surveyed footprint centroid, which is what `placeGeneric()` positions and what
the manifest anchor names; the bbox centre sits west of it because the entry
canopy and fins project onto the plaza. Palace of Fine Arts ships with the same
asymmetry (`[39.0, 14.2]`). The drum itself is centred on the origin.

## 8. Review renders

All rendered from the **re-imported exported GLB**, never the authoring scene:

`chase-center-north/east/south/west.png` (one ortho rig, identical scale,
framing, lighting, exposure — azimuth only differs), `-top.png`, `-aerial.png`
(105 mm, 38° down, WNW, the app's camera), `-night.png`, `-night-entry.png`,
and `chase-center-contact-sheet.png`.

## 9. Gate 3 — approval

Approved by David on 12 August 2026, verbatim:

> "hey just checking in please proceed to finish the entire pipeline. i approve
> it all. dont wait for me"

Given in a single message covering the remaining stages, so no per-iteration
approval was collected. The contact sheet, aerial, night renders and the numbers
in §1 are the evidence this approval stands on; they are presented alongside it
in the session summary.

## 10. Manifest entry (draft — not written by this stage)

```json
{
  "id": "chase-center",
  "file": "chase-center.glb",
  "anchor": [
    -122.3873962,
    37.7678739
  ],
  "targetHeightM": 40.8,
  "cat": 0,
  "name": "Chase Center",
  "estimated": false,
  "loadRadius": 2500,
  "dims": [
    164.3642,
    159.1272,
    40.8026
  ],
  "tris": 11289
}
```

`loadRadius` follows the default rule `max(2500, 40.8 × 30) = 2500`.
`cat 0` matches Oracle Park, the set's other sports venue.

## 11. Integration notes carried forward

- **Case B**: no `chase-center` in `pipeline/lib/landmarks.mjs` or
  `app/src/landmarks.js`. Needs a registry entry and a tile re-bake.
- Suggested `exclude` ≈ 115 m. The footprint's max radius is 85.6 m and the
  nearest neighbours (Uber HQ Buildings 3 and 4) are 109 and 112 m out — the
  tightest exclusion/neighbour margin in the landmark set. Verify at integration
  that the Uber blocks survive the re-bake.
- Mission Bay is flat fill at ~2–3 m; a 164 m footprint spans several terrain
  samples, so check seating.
