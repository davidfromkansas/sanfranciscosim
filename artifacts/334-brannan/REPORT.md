# 334 Brannan Street (Sherman and Clay Building) — build report

Asset: `artifacts/334-brannan/334-brannan.glb`
Plan: `docs/asset-plans/334-brannan.md`
Dossier: `artifacts/334-brannan/REFERENCE.md` (this report and that dossier beat
the plan wherever they disagree)
Built: 16 August 2026, Blender 5.2.0 LTS, headless, from
`build_334_brannan.py` (deterministic — re-running it reproduces the GLB).

## Numbers

| | Value |
|---|---|
| Triangles | **5,916** (cap 9,000) |
| Objects (shipped, after the optimize join) | 15 — 109 in the authored GLB |
| Dimensions (axis-aligned) | 30.176 x 30.648 x **13.400** m |
| Building along its own axes | 21.08 m (Brannan frontage) x 21.13 m deep |
| Min Z | 0.000 m |
| XY centre offset | 0.129, -0.073 m |
| Materials | 14, all `Toy_*`, flat, no textures, no alpha |
| Glow groups | 2 (`Toy_gold_Glow`, `Toy_glass_Glow`) |
| Anchor | -122.3930344, 37.7814147 |
| Front heading | 135.1° true (SE), Brannan Street |
| File, raw | **176,264 B** shipped (365,324 B authored, −51.8%) |
| Draw submeshes | **16** shipped (110 authored) |

Height stack as built: roof deck **12.15 m** (LiDAR median 12.14, measured),
parapet coping crest **13.10 m**, gold pier caps **13.40 m** = the bounding-box
top, so the loader's `targetHeightM / measuredHeight` lands on exactly 1.0.

## Validation

`validate_334_brannan.py` factory-resets Blender, imports **only the exported
GLB**, and validates the re-import. The committed `validation.json` is the run
against the **shipped** (stage-4, meshopt-packed) file — **overall PASS**, every
check true. The authored pre-optimize GLB passed the same run identically
(5,916 tris, 109 objects, 31,500 rays / 0 flipped, 109/109 positive volumes):

| Check | Result |
|---|---|
| meters and plausible dimensions | PASS |
| crest normalized to 13.40 m target | PASS (13.400) |
| base at z = 0 | PASS (0.000) |
| centred in XY | PASS (0.13, -0.07) |
| under triangle budget | PASS (5,916 / 9,000) |
| no image textures | PASS |
| no transparency | PASS |
| materials follow contract | PASS (14 `Toy_*`, no `Toy_body`) |
| no cameras or lights | PASS |
| no animation, skin or constraints | PASS |
| transforms applied | PASS |
| no negative scales | PASS |
| normals outward — per-object signed volume | PASS (15 / 15 positive; 109 / 109 before the join) |
| normals outward — ray test | PASS (31,500 first hits, **0** flipped, 0.000% residual) |
| stored loop normals finite and unit (the gltfpack trap) | PASS (0 invalid) |
| no degenerate geometry | PASS |
| no unexpected objects | PASS |

## Renders

All regenerated from the exported GLB, never from the authoring scene:
`334-brannan-north/east/south/west.png` (one ortho rig, identical scale, framing,
lighting, exposure; azimuth is the only difference), `334-brannan-top.png`,
`334-brannan-aerial.png` (85 mm, 38° down, azimuth 92° so the Brannan front and
the exposed northeast flank are both in frame), `334-brannan-aerial-night.png`,
and `334-brannan-contact-sheet.png`.

Because the building stands at 45° to the world axes, each axis-aligned elevation
shows two faces at once and compresses every horizontal dimension by cos 45°.
That is the real heading, not a camera error. The night render clips the glow
colours to white under the Standard view transform — it judges *which* surfaces
glow and how restrained the scatter is, not the night palette; the app draws
`_Glow` unlit at the material's own baked colour (warm gold frieze, blue sash).

## Dossier corrections made during the build

REPORT beats plan. These are the plan's numbers that did not survive contact with
the model; all of them are also recorded in `REFERENCE.md` §7.

1. **Footprint winding (plan §2.3).** The plan lists the corners `E, S, W, N` and
   calls that the build order. That winding is *clockwise* and inverts every
   outward normal. The script uses `S, E, N, W` (counter-clockwise), which also
   puts the Brannan front on edge 0. The corner coordinates themselves were
   correct and are unchanged.
2. **Body colour (plan §2.7 step 3, §2.8).** The plan applied a full-width greige
   "Brannan skin" and then cut sage recesses into it. Without booleans a recess
   cannot be cut out of an applied skin. Built as: **greige body**, sage recess
   panels applied flush per bay, greige piers and bands standing proud between
   them, and a separate sage skin on the northeast flank (which is genuinely
   painted sage). Same photographed result, fewer parts.
3. **Recess width.** 2.44 m as first built swallowed the piers and the whole
   facade read sage — the exact failure the plan warns about in §2.6. Narrowed to
   1.98 m against 0.95 m piers.
4. **Frieze projection.** At 0.07 m proud the gold band disappeared under the
   parapet coping from the aerial camera. Pushed to 0.13 m, proud of the coping.
5. **Living wall (plan §2.7 step 8).** Raised onto the plinth (0.40-3.30 m) and
   widened to 15.4 m; at the planned size it read as a green rectangle floating
   on a blank wall. `Toy_leaf` deepened `6d8558` → `5b7347` for separation.
6. **Roof furniture (plan §2.7 step 10).** Re-laid out after the first aerial:
   two tables with chairs plus three planters in the Brannan half, skylights
   beside the bulkhead, instead of the planned scatter of four tables.

Two dossier facts were re-verified and held: the **1929** construction date (against
five commercial listings that all say 1911 — that is 340 Brannan's date), and the
**15.63 m LiDAR maximum as neighbour bleed** from 340 Brannan's rooftop penthouse
across the shared property line, not a fourth storey here.

## Iteration log

| # | Change | Why |
|---|---|---|
| 1 | first build, sage body + greige applied frame | as planned |
| 1a | aerial review | facade read as a plain green box; the greige frame was invisible |
| 2 | inverted the two tones (greige body, sage recesses), widened piers to 0.95 m, coping greige instead of near-white, NE flank given its own sage skin, deeper `Toy_leaf`, roof re-laid out | fix the read |
| 2a | aerial review | better, but the 2.44 m recesses still swallowed the piers and the gold band hid under the coping |
| 3 | recesses 1.98 m, frieze proud 0.13 m, living wall raised and widened | final |
| 4 | full rig + night + validation | all PASS |

## Approval (pipeline gate 3)

Approved by David in the session brief of 16 August 2026, verbatim:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

Recorded here as the standing approval that advances this asset past gate 3. No
per-render feedback was given, because none was requested.

## Stage 4 — optimize

Full detail in `optimize/REPORT.md`. Summary: Phase B welded 8,980 coincident
vertex pairs and joined 109 objects into 15 (one per material); the limited
dissolve was **skipped by rule** because the parapet and coping are coplanar ring
bands; Phase C packed with `gltfpack@0.24 -c -km -kn -noq`. Result 365,324 →
**176,264 B** raw (−51.8%) and 110 → **16** draw submeshes, with triangles, bbox,
origin and the 14-material set all unchanged, and a maximum A/B pixel delta of
0.0067% across day/night × near/far. All gates G1-G6, G8 PASS (G7 n/a). The
optimized file is now the shipping `334-brannan.glb`; the authored original is
archived at `optimize/input/334-brannan.glb`.

## Draft manifest entry

```json
{
  "id": "334-brannan",
  "file": "334-brannan.glb",
  "anchor": [
    -122.3930344,
    37.7814147
  ],
  "targetHeightM": 13.4,
  "cat": 19,
  "name": "334 Brannan Street (Sherman and Clay Building)",
  "estimated": true,
  "dims": [
    30.1763,
    30.6477,
    13.4
  ],
  "tris": 5916,
  "loadRadius": 2500
}
```

`"estimated": true` because the parapet and pier-cap heights are photogrammetric,
not published; the 12.15 m roof deck under them is LiDAR-measured.
`loadRadius` takes the default: `max(2500, 13.4 × 30) = 2500` m.
