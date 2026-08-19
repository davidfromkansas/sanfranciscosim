# Pier 15 (Exploratorium) — build report

**Asset:** `artifacts/pier-15/pier-15.glb` · built 19 Aug 2026 · Blender 5.2.0 LTS
(headless, deterministic script `build_pier_15.py`) · **stage-4 optimized**:
350,496 B raw (from 731,528 rebuilt), 315 → 12 draw submeshes, tris unchanged; original
archived at `optimize/input/pier-15.glb`, full metrics in `optimize/REPORT.md`.
The stage-2 validator re-ran PASS against the shipped packed file.

## Shipped numbers (fresh-scene validation of the exported GLB)

| Metric | Value | Gate |
|---|---|---|
| Overall validation | **PASS** (`validation.json`, all checks) | PASS |
| Triangles | **10,852** | ≤ 22,000 ✓ |
| Objects | 12 meshes after optimize (loader merges to ≤ 2 draw calls) | ✓ |
| Dimensions | 249.25 x 221.09 x **16.40** m | ✓ |
| min Z | 0.000 (waterline; pile feet touch it exactly) | ✓ |
| Bbox top | 16.400 = targetHeightM → loader scale **1.0** | ✓ |
| XY centre offset | (-4.95, -0.56) m — AABB centre vs the surveyed area-centroid origin; the deck flares at the seawall and carries the south apron, so this is honest, not misplacement | ✓ (documented tolerance 5.5) |
| Materials | 12 `Toy_*`, flat, no textures, no alpha; 3 `_Glow` sets (glassl/amber/glass) | ✓ |
| Normals | signed volume: 0 inverted; 31.5k visibility rays: 0.0% flipped | ✓ |
| Cameras/lights/animations/armatures | none | ✓ |

## Review renders (all from the exported GLB)

`pier-15-{north,east,south,west,frontage,top,water,aerial,aerial-night}.png` +
`pier-15-contact-sheet.png`. The water view is taken from the courtyard side —
the only image that proves the pile field, deck soffit and courtyard notch.

## Iteration log

1. **Review 1 (aerial + frontage, low samples):** monitor read as a plain steel
   bar from above → added glazed cap-slope strips. The "O" ring's upper interior
   showed cream wall — the fanlight arch topped out below the ring → fanlight
   enlarged (span 8.4, crown 9.6), "O" lowered and resized (⌀5.1/4.2, centre
   z 6.9).
2. **Review 2 (arch zoom):** the amber fanlight glow, a filled arch panel,
   washed the whole glazing warm at the app's 12% day alpha; its concave ring
   profile also ear-clipped into a filled cap. Rebuilt as an explicit quad-strip
   arch band (`arch_band_panel`) — night reads as a lit portal outline, day is
   near-invisible. Letter kerning tightened; "R" leg widened.
3. **Validation catch:** three terrace railings carried an unapplied
   `location.z` offset → `rail_chain` gained a `base` parameter; transforms now
   all identity. OVERALL PASS.
4. **Review 3 (post-bake tile decode):** the first re-bake left a 13.8 m baked
   block 23 m deep inside the deck at the bay end. Root cause: the plan mis-read
   the bay-end massing — the real Bay Observatory Gallery is OSM w738027034 on
   the NORTH APRON (t -45.4..-25.5), the shed runs near-full-width to s ≈ 106.6,
   and there is no deck-level terrace. Model rebuilt to match (10,852 tris,
   315 objects); the baked ring is taken by a 12 m `extraExclusions` circle
   (its 87.4 m gate from the anchor is past Pier 17's 84.9 m ceiling; from the
   circle's own centre Pier 17's nearest vertex is 29.1 m). Full render rig,
   stage-2 validation and the optimize gates re-ran clean on the rebuilt asset.

## Dossier corrections (REPORT beats plan)

- The plan's expected AABB "~250 x 178 m" was a rotation-math slip; the correct
  expectation for the 245 x 94.8 m OBB at 54.9° is **~249 x 221 m** (measured:
  249.3 x 221.1). `validate_pier_15.py` gates on the corrected numbers.
- Monitor centreline built at **t = +9.0** in the pier frame (7.5 m SE of the
  shed centreline, straight from the rectified aerial) rather than the plan's
  provisional t = 11.
- The flagpole is deliberately omitted (plan 2.15: at true height it would
  become the bbox top and shrink the pier ~27%). The 16.4 m crest cap is the
  architectural top.

## Approval (stage 3)

The pipeline invocation pre-approved all gates: **"APPROVE EVERYTHING DONT ASK
ME FOR PERMISSION"** — David, 19 Aug 2026, in the BATCH: yes invocation of
ADDRESS-TO-ASSET for this building. Recorded here verbatim per gate 3; no
separate design sign-off was requested or given.

## Draft manifest entry (verified values)

```json
{
  "id": "pier-15",
  "file": "pier-15.glb",
  "anchor": [
    -122.3974662,
    37.8016046
  ],
  "targetHeightM": 16.4,
  "cat": 25,
  "name": "Pier 15 (Exploratorium)",
  "estimated": false,
  "dims": [
    249.25,
    221.09,
    16.4
  ],
  "tris": 10852,
  "loadRadius": 2500
}
```

`targetHeightM` is photogrammetric (range 15.8-17.0, method in plan 2.16);
`estimated` stays `false` on the strength of the two-way camera verification,
with the range recorded here. Integration notes incl. the measured exclusion
window (70 m; ceiling 84 m — Pier 17's gate) are in `docs/asset-plans/pier-15.md`
§2.13. **Note for integration: `SF9900015` is one merged DataSF polygon covering
Piers 15 AND 17 — excluding it un-bakes Pier 17 too, and Pier 17's Overture ring
does NOT gap-fill (bbox occupancy 0.464 > the 0.25 gate — measured, see §2.13).
Pier 17's site bakes empty until a pier-17 asset lands; follow-up task flagged.**

## Stage 5 — integration QA (batch mode, 19 Aug 2026)

Local QA against the BUILT app (`app/dist`) in headless Chrome over CDP
(`qa_local.mjs`; screenshots in `artifacts/pier-15/qa/`):

| Check | Result |
|---|---|
| Re-validation of the shipped GLB (stage-2 validator) | PASS (10,852 tris, 12 objects) |
| Manifest entry loads / merge line | PASS — `sf-assets: pier-15 merged 12 objects / 12 materials -> batched (8180 tris body); uniform x1.0000 at 3523, -3494 on the water plane` |
| Uniform scale | PASS — x1.0000 |
| id round trip (`camelId('pier-15')` → `pier-15`) | PASS (digit segments don't camelise) |
| Case B registry + re-bake + audit 1.6 | PASS — 115 zones clear; verify-rebake: 584/585 cells unchanged, only 22_8 (21→20) |
| Exclusion proof from the tiles | PASS — decoded cells 22_8/22_9/23_8/23_9: zero surviving rings overlap the deck polygon (overlap area 0.0 m², penetration 0.00 m) |
| Single building / no baked block poking through | PASS |
| Terrain seating | PASS — `seaLevel: true`, seated at exactly y = 0 (the anchor samples a spurious 2.5 m Terrarium bump; the loader's water-plane datum from the pier-3 branch was ported verbatim, identical hunks for the batch merge) |
| Night glow | PASS — monitor lightband + amber arch + apron points only |
| Draw calls at the landmark | PASS — avg 85/frame (< 300) |
| Fallback drill (real 404) | PASS — boots, exactly one `pier-15 failed to load` warning, site empties inside the exclusion (Case B expected) |
| app `npm test` + `npm run build` + `npm run lint` | PASS |

**Known, documented collateral:** Pier 17's site bakes empty (the merged DataSF
record covered both piers; Pier 17's Overture ring fails the bbox-occupancy
gap-fill gate at 0.464 > 0.25). Follow-up pier-17 asset task flagged.

Batch mode: the bake was verified as above and then DISCARDED; this branch
commits source only (GLB, manifest entry, registry entry, seaLevel loader
patch, plan, artifacts). The city is re-baked once for the whole batch by
`docs/asset-pipeline/BATCH-INTEGRATE.md`. Note for the batch session: run
`node pipeline/landmark-streaming-check.mjs` against the batch build, and
this branch and `pipeline/pier-3` carry IDENTICAL `app/src/assets.js` seaLevel
hunks — they merge clean, but merge pier-3 first if git complains.
