# 101 South Park — build report

Miniature GLB for SF-SIM, built 12–13 August 2026 from `docs/asset-plans/101-south-park.md`
via the address-to-asset pipeline (`docs/asset-pipeline/ADDRESS-TO-ASSET.md`), invoked with
`BUILDING: 101 S Park St, San Francisco, CA 94107`, `BATCH: yes`. The session was
opened with `STOP_AFTER: 3`; at gate 3 the owner approved, asked for the Kleiner Perkins
identity to be modelled, and lifted the remaining approval gates, so the run continues
through stages 4 and 5.

**This report beats the plan.** Where the dossier in the plan file and this report disagree,
this report and `REFERENCE.md` are correct.

## 1. Headline numbers

Both columns are real: the asset was built, approved, then optimized in stage 4
(`optimize/REPORT.md`). **The shipped column is what the manifest describes.**

| | As built | **Shipped (post-optimize)** |
|---|---|---|
| Triangles | 7,534 (cap 9,000) | **7,502** |
| Objects | 86 | 11 |
| Draw submeshes | 87 | **12** |
| Dimensions (AABB) | 30.5306 x 29.8696 x 10.90 m | identical |
| Min Z | 0.0 | 0.0 |
| XY centre offset | (−0.003, −0.172) m | identical |
| Materials | 11, all `Toy_*`, flat, opaque, untextured | 11, identical set |
| Glow materials | `Toy_rust_Glow`, `Toy_glass_Glow` | identical |
| File, raw | 479,732 B | **191,700 B (−60.0%)** |
| Contract validation | PASS on all 16 checks | **PASS on all 16 checks** |
| Anchor | `-122.3937582, 37.7812624` (footprint OBB centre) | unchanged |
| Target height | 10.9 m — bbox top normalized exactly, so loader scale = 1.0 | unchanged |
| Parapet crest | 10.0 m | unchanged |
| Front heading | 318.3° true (northwest, onto South Park) | unchanged |

The AABB is ~30.5 x 29.9 m for a 13.1 x 29.7 m building. That is the expected consequence of
authoring at the real 44.5° SoMa heading, not a scale error.

Compression is `EXT_meshopt_compression` without `KHR_mesh_quantization`, matching
`pipeline/compress-assets.mjs`. Full stage-4 detail in `optimize/REPORT.md`.

## 2. Corrections to the dossier made during the build

**The plan's single 10.0 m figure is split into two.** 10.0 m is the **parapet crest** — what
the photogrammetric read off the January 2025 pano actually measures, and the height the
building presents to the street. The asset's bounding box has to reach the tallest *feature*,
and the 2010 LiDAR maximum over this footprint is 10.92 m. Treating 10.0 as the parapet and
10.9 as the crest makes both measurements consistent instead of forcing a choice between
them, and it is the same parapet/crest split `380-brannan` uses. `targetHeightM` is
therefore **10.9**, not 10.0. The plan file, the plans README table and the draft manifest
entry were all updated to match.

**The footprint is simplified from eight vertices to four.** The DataSF survey draws the
southwest boundary as four segments and puts a 0.077 m chamfer at the west corner. Those
points are collinear to within 0.18 m. Merging them gives a clean quadrilateral of 378.2 m2
against the survey's 380.1 m2 — 0.5% — which is far inside the contract's tolerances and much
healthier for the bevel pass than four near-parallel walls would have been. The four corners
as built are in `REFERENCE.md` §3.

**No mass step was modelled.** The plan's §2.7 carried a conditional step-down for the rear
of the building, pending evidence. That evidence was not found: the 2010 LiDAR predates the
current second storey and says nothing useful about today's massing, and the 2026 satellite
roof appears to change level partway along but not clearly enough at the available resolution
to place a step. The build takes the conservative reading — **one clean volume at full
height** — and this is a decision, not a finding. It is the item most worth a second look
before integration, and it is called out again in §6.

**No brick and no arches**, despite the architect's project copy describing the building as
"brick-clad" with "large, arched metal-clad windows". Every current photograph of the front
shows charcoal stucco and rectangular oak-framed openings. See `REFERENCE.md` §6.

## 3. Design decisions

- **The oak shopfront row is the entire identity, and it is over-framed on purpose.** This is
  a dark, deliberately plain building; the failure mode is a grey slab that reads as
  untextured procedural geometry rather than an authored asset. The oak frames are widened to
  a 0.28 m read and stand proud of the wall so they catch light from the app's aerial camera.
  This is the one place semantic exaggeration is spent (style bible §7, §22).

- **Palette extension: `Toy_charcoal` `#4a4540`.** The real wall is a dark warm gray. The
  palette's `Toy_ink` (`#3a3530`) is near-black and turns the whole building into a
  silhouette; `Toy_roofd` (`#45454a`) is too cool. Off-palette is a WARN, not a FAIL, and the
  style bible's §7 architectural base explicitly includes medium-to-dark warm gray. Recorded
  here as a deliberate extension, the same way `380-brannan` extended with `Toy_slate`.

- **Pale glazing on the ground floor, navy everywhere else.** The first aerial proved that
  `Toy_glass` navy behind a thin oak frame collapses into one dark hole, which defeats the
  only identity cue this building has. The real shopfront lights are frosted or shaded and
  read almost white from the street, so the ground-floor fills use `Toy_glassl`. The upper
  ribbon and both flanks keep `Toy_glass`.

- **The upper storey's recess is built, not drawn.** The asset is a union of closed solids
  with no booleans, so an opening cannot be cut out of a wall. The ribbon's 0.35 m reveal is
  made by building the *rest* of the front proud of it — a sill panel, a header panel and two
  end piers forming a picture frame, with the glass sitting back near the body plane. The
  shadow that throws is the whole upper half of the elevation. The front's own coping is
  carried out to the skin face so the parapet line does not disappear behind it.

- **The southwest flank is blank, and stays blank.** It is a party wall against 117 South
  Park. The first build added two shallow pilaster strips to break up 29.6 m of flat wall;
  they did not read at all in the aerial and they are not on the real building, so they were
  removed. A blank party wall against an attached neighbour is the honest answer.

- **A near-white roof deck.** `Toy_white` on the deck, against charcoal walls. This is not a
  stylistic flourish: the 2014 permit is a four-ply "cool" Title-24 re-roof over the entire
  building, and the 2026 satellite shows exactly that. It is also what makes this building
  legible from a camera that spends most of its time looking down.

- **Roof furniture spread over the full depth.** The first top view had everything clustered
  in the front two thirds and the rear third reading as an empty tray. Six skylights, three
  mechanical blocks, a duct, a hatch, two vent stubs and the penthouse are now distributed
  down all 29.6 m, still weighted to the front third where the satellite shows the real
  density. The penthouse sets the 10.9 m crest.

- **The Kleiner Perkins wordmark is real geometry, and it is deliberately
  oversized.** The pipeline has no textures, so a wordmark either exists as
  extruded letterforms or it does not exist at all. What is faithful: SF permit
  2018 records exactly one single-faced, **non-illuminated** wall sign reading
  "kleiner perkins", and KP's published brand assets are monochrome wordmarks
  with no brand colour — so the sign is off-white `Toy_trim` on charcoal and it
  does **not** glow at night. What is exaggerated: the real sign is a small
  plaque beside the entrance, which at city scale is far under a pixel. It is
  moved up onto the header band between the ribbon and the parapet and set at a
  0.75 m cap height so it reads from the app's downward camera. Exaggerating an
  identity feature in *authoring* is what AGENTS rule 5 and style bible §22
  permit; the building itself is not moved or rescaled. The street number over
  the entrance is modelled at its real position and size.

- **Glyph cost is welded, not decimated.** Font outlines are far denser than a
  three-quarter-metre letter needs, and the cost is driven entirely by the
  outline vertex count — a limited dissolve does nothing, because a triangulated
  simple polygon already costs exactly n−2 triangles for n outline vertices.
  Welding at a fixed *fraction* of cap height (9%) is the lever that works, and
  keeping it proportional makes glyph cost scale-invariant: the wordmark can be
  resized without re-tuning the budget.

- **Orientation deviates from the contract's "front faces −Y", deliberately.** The asset is
  authored in true-world orientation (`+Y` = north) because `placeGeneric()` in
  `app/src/assets.js` applies no rotation. The South Park front faces **318.3°**. This is the
  deviation the plans README requires to be recorded here.

## 4. Build iterations

| # | What the render showed | What changed |
|---|---|---|
| 1 | Upper ribbon and every flank window invisible; the building read as a blank slab | Openings were authored as solids sunk *into* the wall, which with no booleans just adds more wall. All openings rebuilt standing proud; the ribbon recess rebuilt as a proud surround |
| 2 | Aerial cropped the 29.7 m depth; ground-floor bays collapsed into dark holes | Beauty camera 105→78 mm at radius ×3.4; ground-floor glazing navy → `Toy_glassl` |
| 3 | Camera square onto the front hid both 29.6 m flanks edge-on | Beauty azimuth 318° → 5°, pitch 38° → 32° — between the front normal and the alley-flank normal, so both read |
| 4 | Rear third of the roof was an empty tray; flank windows read as flat pasted-on rectangles; night glow blew out to pure white | Roof furniture redistributed over the full depth; flank openings given a `Toy_ink` ring; night-rig emission strength 6.0 → 3.0 so the warm oak survives |
| 5 | Kleiner Perkins lettering added on request. First pass cost 6,312 triangles — over budget on its own; the `101` plate exported inside-out | Glyph outlines welded at 9% of cap height; glyph sheets now explicitly oriented outward before extruding (a sheet whose normals happened to face into the wall extruded backwards and inverted the solid), sliver faces dropped after triangulation |
| 6 | Wordmark legible but too small to earn its place | Cap height 0.50 → 0.75 m; weld made proportional so the enlargement cost nothing |

## 5. Validation

`validation.json`, written from a fresh factory-reset Blender scene with only the exported
GLB imported — never the authoring scene.

| Check | Result |
|---|---|
| Meters, plausible dimensions | PASS |
| Crest normalized to 10.9 m target | PASS (loader scale = 1.0) |
| Base at z = 0 | PASS (min Z 0.0) |
| Centred in XY | PASS (−0.003, −0.172) |
| Under triangle budget | PASS (7,502 / 9,000) |
| No image textures | PASS |
| No transparency | PASS |
| Materials follow contract | PASS (10 materials, all `Toy_*`, no `Toy_body`) |
| No cameras or lights | PASS |
| No animation, skinning or constraints | PASS |
| Transforms applied | PASS |
| No negative scales | PASS |
| Normals outward — per-object signed volume | PASS (authoritative for a union of solids) |
| Normals outward — 31,500-ray visibility test | PASS (residual within 0.15%) |
| No degenerate geometry | PASS |
| No unexpected or foreign objects | PASS |

## 6. Open risks carried into approval

1. **The height is an estimate, ±0.8 m.** No published figure exists. 10.0 m parapet /
   10.9 m crest is a photogrammetric read reconciled with the 2010 LiDAR maximum. It is the
   number most likely to move.
2. **Whether the second storey runs the full 29.7 m depth is unresolved** and the build made
   a conservative call rather than a finding. See §2.
3. **Three of the four elevations are inferred.** Only the northwest front has usable
   ground-level photography. The northeast flank faces an open paved strip and is genuinely
   visible from the app's camera, so its window rhythm is the most consequential invention in
   the asset. Street View coverage on Jack London Alley and Varney Place could not be reached
   during this pass.
4. **The four-bay rhythm on the front** is read from a single January 2025 pano with part of
   the elevation outside the frame.
5. **The published 16,420 sq ft does not fit on this lot**, and the roof in satellite imagery
   may run through to Varney Place further than either OSM or DataSF records. Both surveys
   agree on 13.07 x 29.7 m to within 1%, and AGENTS rule 5 says the survey wins, so that is
   what was built — but if the real structure is a through-block building, this asset is
   short at the rear.

## 7. Manifest entry (applied in stage 5)

```json
{
  "id": "101-south-park",
  "file": "101-south-park.glb",
  "anchor": [
    -122.3937582,
    37.7812624
  ],
  "targetHeightM": 10.9,
  "cat": 3,
  "name": "Kleiner Perkins (101 South Park)",
  "estimated": true,
  "dims": [
    30.53,
    29.87,
    10.9
  ],
  "tris": 7502,
  "loadRadius": 2500
}
```

`estimated: true` because the target height is not a published figure.

Integration is **Case B**: no entry exists in `pipeline/lib/landmarks.mjs` or
`app/src/landmarks.js`, so stage 5 needs a registry entry and a tile re-bake. **The
exclusion radius is 4 m, not the ~16 m the plan guessed** — see §9. Note that the baked procedural stand-in here is **6 m tall and this asset is
10.9 m** — the asset is *taller* than what it replaces, which is the inverse of the usual
case and will hide an exclusion-zone mistake rather than reveal it. Do the bake before
judging. `BATCH: yes` applies: bake, QA the bake, then discard the bake and commit source
only.

## 8. Stage 5 — integration QA (batch mode, source-only branch)

Bake run 13 August 2026 on this branch: `terrain → bridges → buildings → streets →
landcover → validate → lore → toy → notables → context → muni-shapes`, with
`pipeline/data/` symlinked from a sibling worktree (removed again before committing —
note that `.gitignore` lists `pipeline/data/` with a trailing slash, which does **not**
match a symlink, so git offers it as untracked).

| Check | Result |
|---|---|
| `verify-rebake.mjs` — only new landmarks' cells moved | **PASS** — 584 of 585 cells unchanged; cell `23_13` went 233 → 232 |
| `verify-rebake.mjs` — nothing surviving inside the radius | **PASS** — nearest surviving footprint 6.4 m vs the 4 m radius (that is 117 South Park, the attached neighbour, correctly kept) |
| `audit.mjs` check 1.6 — no procedural footprint inside a bespoke exclusion zone | **PASS** — 42 landmarks clear |
| Loader merge line | **PASS** — `sf-assets: 101-south-park merged 12 objects / 11 materials -> batched (3686 tris body); uniform x1.0000 at 3849, -1245` |
| Uniform scale ≈ 1.0 | **PASS** — exactly `x1.0000`, so the authored crest matches `targetHeightM` |
| Placed at the real anchor | **PASS** — `3849, -1245` is the projection of `-122.3937582, 37.7812624` |
| `camelId()` round trip | **PASS** — `101-south-park` → `101SouthPark`, which is the registry id, so no double building |
| Draw calls | **PASS by construction** — the log says `batched`, i.e. it joined the shared landmark `BatchedMesh` pair, so it adds **0** draw calls no matter how many landmarks exist |
| Single building on the footprint, correct seating and orientation | **PASS** — day screenshots show one building on the site, front onto the park, no procedural block poking through |
| Night `_Glow` layer renders | **PASS (partial)** — the glow layer is live and emissive in-app; see the honest note below |
| Fallback drill | **PASS** — see below |

**Fallback drill.** With `app/public/sf-assets/landmarks/101-south-park.glb` moved aside
and the page reloaded, the app logged exactly one warning —
`sf-assets: 101-south-park failed to load (...)` — `stats()` reported `failed: 1` with
every other landmark unaffected, and the app kept rendering with no crash and no error
cascade. Restoring the file and reloading brought the asset straight back. Note that with
Case B the site degrades to a **gap**, not to a procedural building, because the re-bake
deliberately removed the procedural footprint. That is the documented consequence of an
exclusion zone, not a fallback failure.

### Honest limitations of this QA pass

- **Frame rate and draw-call totals were not measurable here.** The browser pane runs
  hidden in this environment, so `requestAnimationFrame` is throttled to a few frames per
  screenshot; the in-app stats overlay consequently reads `fps 0 · draw calls 1`. The
  draw-call claim above rests on the architecture (the asset batches, adding zero calls),
  not on a measurement. **A real fps/draw-call reading against AGENTS rule 2 still has to
  be taken on a visible browser**, and it is the one QA item this session could not close.
- **The night state was confirmed to render but not fully judged in-app.** The glow layer
  is emissive and the rear elevation is correctly dark, but the diorama camera locks to a
  42° downward view, so the front elevation — where all the glow lives — is hard to see
  square-on. The full night appearance was judged from the authoring rig
  (`101-south-park-aerial-night.png`) instead.
- The dev server initially came up in the shared main checkout rather than this worktree,
  which made the served manifest look like it had 6 entries. Worth knowing before
  concluding an integration has failed.

## 9. Approval

Granted 13 August 2026: *"can you update the 3d model to reflect that including its
lettering and design? … you can proceed without any approvals needed from me moving
forward."* — David, in session. The approval came with the revision request recorded in §3
and §4 (iterations 5–6); the wordmark was added before the pipeline advanced past gate 3.

## 10. Exclusion radius — measured, and much tighter than the plan assumed

The plan's §2.13 proposed `exclude: ~16`, reasoning from the footprint's half-diagonal.
That is the wrong model of what `excluded()` in `pipeline/buildings.mjs` does: it drops a
procedural footprint when its ring centroid **or any of its ring vertices** falls inside the
radius. 117 South Park is *attached* to this building, so the two footprints share their
party-wall vertices — and those shared vertices sit **6.40 m** from this anchor. A 16 m
radius would have deleted a real neighbour that has no hand-built replacement, leaving a
hole in the block face.

Measured against the DataSF footprints:

| | Distance from anchor |
|---|---|
| This building's ring **area** centroid (DataSF) | 0.26 m |
| This building's ring area centroid (OSM cross-check) | 1.54 m |
| Nearest shared party-wall vertex, 117 South Park | **6.40 m** |
| 117 South Park's own centroid | 10.59 m |
| Next nearest neighbour vertex (123 South Park) | 13.17 m |

So the safe band is **1.6 m – 6.4 m**, and the exclusion has to work through the *centroid*
test — the building's own ring vertices are at 6.40 m, outside any radius that spares the
neighbour. **`exclude: 4`** sits in the middle with ~2.4 m of margin either side.

This is the same structural situation 550 Third documents ("through lot with party walls on
both long sides, so the exclusion window is narrow"), and the reason both it and 380 Brannan
use single-digit radii. `pipeline/verify-rebake.mjs` is what proves it after the bake:
it reports the distance from each new landmark's anchor to the nearest *surviving* footprint
vertex and fails if anything survives inside the radius, or if any cell outside the new
landmarks changed its building count.
