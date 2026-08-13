# 362 Brannan Street — build report

Stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md` for `BUILDING: 362 Brannan St,
San Francisco, CA 94107`, `BATCH: yes`. Plan: `docs/asset-plans/362-brannan.md`.
Research: `REFERENCE.md` in this folder.

**Where the report disagrees with the plan, the report wins.**

## Deliverables

| File | What it is |
|---|---|
| `build_362_brannan.py` | deterministic build; `blender -b --python build_362_brannan.py` reproduces the GLB |
| `362-brannan.blend` | authoring scene |
| `362-brannan.glb` | the shipping asset |
| `render_362_brannan.py` | controlled review renders, always of the re-imported GLB |
| `validate_362_brannan.py` | fresh-scene contract validation |
| `make_contact_sheet.py` | composes the contact sheet |
| `362-brannan-{north,east,south,west}.png` | four elevations, one rig, identical everything but azimuth |
| `362-brannan-top.png` | plan view |
| `362-brannan-aerial.png` | the app's high three-quarter aerial, from the SE |
| `362-brannan-aerial-night.png` | night state |
| `362-brannan-contact-sheet.png` | all seven |
| `validation.json` | machine-readable contract results |

## Measured numbers

| | |
|---|---|
| Objects | 13 shipped (83 as built, joined per material at stage 4) |
| Triangles | **5,904** (cap 8,000) |
| Dimensions (x, y, z) | 31.227 x 30.835 x **8.600** m |
| Min Z | 0.000 |
| XY centre offset | (−0.21, +0.28) m |
| File size | **155,844 bytes raw** / 112,206 gzipped (shipped, post-optimize; 344,668 / 61,949 as built) |
| Materials | 11, all `Toy_*` |
| Textures / animations / cameras / lights / skins | 0 / 0 / 0 / 0 / 0 |

The XY bounding box is ~31 m for a 20.1 x 24.8 m building. That is the expected
consequence of the ~45° SoMa heading, not a scale error.

## Corrections to the dossier

None of the plan's verified facts changed under re-verification. Two things it
left open were resolved by the build, and one modelling decision departs from it:

1. **The bay's extent stayed *inferred*.** No source was found that pins it. The
   model uses 9.0 m of frontage x 8.5 m deep (76 m2, 16% of the roof), which is
   where the LiDAR area statistics and the oblique photography agree. Anyone who
   finds a measured source should override it — it is the one number here that
   could be materially wrong.
2. **The water table does not run the full frontage.** The plan said it did.
   Modelled unbroken, it drew a green line straight across the doorway, which the
   building does not do. It now stops 0.15 m short on each side of the entrance.
3. **The entrance moved.** The plan put it 0.85 m past the height step; its 2.3 m
   reveal then ran back under the two-storey bay. It is now 1.45 m past the step,
   entirely on the low wall, where the photography puts it.

## Deliberate contract deviations

**`Toy_bottle` (`#2f4f3f`) is a palette extension.** Off-palette colours are a
WARN, not a FAIL (`sf-asset-check` §7), and this one is deliberate. The palette's
nearest green is `Toy_verdigris` `#9fb8a8`, a pale sage. This building is cream
stucco and dark bottle-green joinery and nothing else — rendered in verdigris the
window band, the two frieze diamonds, the water table and the freight doors all
sink into the stucco and the building has no identity left. The extension buys the
entire recognition read for one colour.

**The front faces southeast, not −Y.** The contract's "front faces −Y" can only be
honoured literally by buildings whose front faces south. Real-world orientation
wins (AGENTS rule 5, and the orientation note in `docs/asset-plans/README.md`):
the asset is authored with `+Y` = true north so `placeGeneric()` — which scales and
positions but never rotates — drops it in at its real heading. **Brannan front
135.9° true; Varney back 315.2°.**

**A 0.25% Z-only normalization.** The 0.12 m bevel rounds the ridge of the bay
roof and takes ~21 mm off the apex, so the raw build tops out at 8.579 m and the
loader's `targetHeightM / measuredHeight` would land at 1.0025 rather than 1.0.
`normalize_height()` scales Z about z=0 to put the top exactly on 8.600. Z-only
rather than uniform on purpose: a uniform scale would move the footprint ~80 mm,
which is real-world placement accuracy and belongs to AGENTS rule 5.

## Iteration log

Every change below came from looking at a render, in the order the plan requires
(aerial first, formal rig last).

1. **Rear parapet step removed.** A 0.22 m raised strip along the Varney parapet,
   modelling the real wall's slight step, rendered as a thin white blade floating
   over the back. At the app's camera distance a step that shallow is noise, not
   information.
2. **Seven ribs and a ridge cap on the bay roof.** The sloped roof was the largest
   unmodulated surface on the model — a pale slab that read as a lid. The real
   roof is ribbed galvanized sheet; the ribs also now set the crest, and the ridge
   cap stops the plane ending in a cut.
3. **Stair bulkhead added.** The Varney third of the deck was empty in the first
   aerial. Its cap is `Toy_steel`, not `Toy_sand` — in cream it read from straight
   overhead as a bright slab competing with the skylight field.
4. **Parapet and coping pulled 20 mm inside the wall plane.** Flush, the parapet
   ring's outward face is coplanar with the two-storey bay's front face over 9 m,
   and an oversailing coping would have drawn a wrong horizontal ledge across the
   bay at 5.95 m. The coping earns its read from its material and its inward
   overhang over the dark deck, which is the only place it is seen from.
5. **The bay stands 40 mm proud of the street wall.** This is the one defect the
   fast preview renders missed and the full Cycles pass caught: flush, the bay's
   front face and the one-storey block's front face are exactly coplanar over the
   same 9 m, and the z-fight showed up as a soft diagonal X across the stucco
   under the window band — the two quads triangulate differently, so the seam runs
   corner to corner. 40 mm also gives the step at the entrance a real reveal.
6. **Water table broken at the entrance; entrance moved onto the low wall.** See
   "Corrections" above.

## Night state

Restrained on purpose: this is a working sheet-metal shop, not an office floor.
Two of the three sash units carry one lit pane each — bottom-left of the unit —
and the entrance sign panel glows. Nothing else. The frieze diamonds and the water
table stay dark: they are daylight identity features and lighting them would read
as signage.

Both `_Glow` surfaces are thin shells proud of the opaque glazing behind them, as
the app requires — it renders `_Glow` in a separate unlit layer at
`opacity = 0.12 + 0.95·uNight`, so a primary surface authored as glow would be
~12% alpha all day. The day renders preview that by dropping the glow shells to
0.12 alpha, so what you see is what the app shows.

## Draft manifest entry

Not applied here — stage 5 owns the manifest.

```json
{
  "id": "362-brannan",
  "file": "362-brannan.glb",
  "anchor": [-122.3937450, 37.7808430],
  "targetHeightM": 8.6,
  "cat": 19,
  "name": "362 Brannan Street",
  "estimated": false,
  "dims": [31.227, 30.835, 8.6],
  "tris": 5904,
  "loadRadius": 2500
}
```

`dims` and `tris` above are measured from the **shipped (optimized)** GLB — stage 4
is complete and `362-brannan.glb` in this folder is the optimized file. The
pre-optimize original is archived at `optimize/input/362-brannan.glb`. Stage 4's own
report is `optimize/REPORT.md`.

`estimated: false` — the height is DataSF LiDAR `hgt_maxcm`, a measurement, not an
inference. The 7.1 m eave beneath it is inferred, but it is not the manifest's
number.

`loadRadius: 2500` — the default rule gives `max(2500, 8.6 × 30) = 2500` m.
Explicitly taken rather than defaulted into (AGENTS: every new manifest entry
declares its streaming decision). Beyond that radius the carved-out site is a gap,
but at 2.5 km an 8.6 m building is far below a pixel and the absence is illegible.

## Stage 5 notes carried forward

- **Case B.** Registry id `362Brannan` (verified: `camelId('362-brannan')` →
  `362Brannan`), `exclude: 8`. The band was measured by streaming
  `pipeline/data/buildings_datasf.geojson` and applying `excluded()` from
  `pipeline/buildings.mjs` — which tests every ring **vertex**, not just the
  centroid. Radii 6/8/9/10 drop exactly one ring (this building, centroid 3.49 m);
  11 and up also drop 370 Brannan, whose nearest vertex is 10.00 m away. Safe band
  `3.5 < r <= 10`; 8 m is the middle. **Do not raise past 10** — on a party-wall
  site the neighbours' vertices are much closer than their centroids (370 Brannan:
  centroid 13.33 m, nearest vertex 10.00 m), so a centroid-only reading of the
  band is far too optimistic. That mistake was in this plan's first draft.
  `camera: { distance: 200, yaw: 45, pitch: 24 }`, mirroring `380Brannan` four
  doors down. A `camera` is mandatory, not optional — `context.mjs` bakes it into
  `context/landmarks.json` and `camera.js` reads `preset.yaw` unconditionally.
- **Batch mode.** Stage 5 runs the bake and does the full QA on it, then discards
  it (`git checkout -- app/public/tiles api/_data`) and commits source only.

## Validation (gate 2)

`validate_362_brannan.py` re-imports the exported GLB into a fresh isolated scene
and judges the re-import, never the authoring scene. **16/16 PASS.**

| Check | Result |
|---|---|
| meters and plausible dimensions | PASS |
| crest normalized to target (8.600) | PASS |
| base at z = 0 | PASS |
| centred in XY | PASS |
| under triangle budget (5,904 / 8,000) | PASS |
| no image textures | PASS |
| no transparency | PASS |
| materials follow contract | PASS |
| no cameras or lights | PASS |
| no animation, skin or constraints | PASS |
| transforms applied | PASS |
| no negative scales | PASS |
| normals outward (per-object signed volume) | PASS |
| normals outward (ray residual within tolerance) | PASS |
| no degenerate geometry | PASS |
| no unexpected objects | PASS |

**One validator bug found and fixed.** `validate_362_brannan.py` was seeded from
`380-brannan`'s copy, and two of its constants are per-asset: the dimensional
plausibility window was still `12.4 <= z <= 12.8` (380 Brannan's crest) and
`anchor_lonlat` still pointed at 380 Brannan. The first produced a genuine FAIL on
a correct asset; the second would have shipped a wrong anchor into the record
silently. Both retargeted. Worth knowing before copying this validator again:
`TRI_BUDGET`, the plausibility window, `target_height_m`, `front_heading_deg_true`
and `anchor_lonlat` all need retargeting, and only the first two announce
themselves.
