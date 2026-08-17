# 44–46 South Park — build report

Stage 2–4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run 16–17 August 2026
against `docs/asset-plans/46-south-park.md`. **This report beats the plan**
wherever they disagree.

| | |
|---|---|
| Shipping asset | `artifacts/46-south-park/46-south-park.glb` |
| Manifest id | `46-south-park` |
| Manifest anchor | `-122.3938219, 37.7821864` |
| Target height | **16.15 m** (front parapet / roof screen crest) |
| Footprint | 9.47 m frontage x 29.43 m depth, front face bearing **135.2°** |
| Triangles | **4,505** shipped (4,532 as authored; cap 6,000) |
| Objects | **10** shipped (71 as authored, joined per material at stage 4) |
| File size | **124,584 B** raw (272,832 B pre-optimize, −55.4%) |
| Validator | Blender 5.2.0 LTS, fresh-scene re-import — **16 / 16 PASS** |

---

## 1. What was built

A miniature of the 2008 four-level mixed-use infill house at 44–46 South Park:
one public face carrying a white gridded glazed wall in a grey stucco surround,
two blind party walls, a rear block stepping down to 8 m, and a flat roof with
the building's 2012 photovoltaic array on it.

Deliverables in this directory:

```
build_46_south_park.py      deterministic build (Blender 5.2 LTS, headless)
render_46_south_park.py     the review rig (elevations, top, aerial, night)
validate_46_south_park.py   fresh-scene contract validation
make_contact_sheet.py       composes the contact sheet
46-south-park.blend         authoring scene
46-south-park.glb           the shipping asset
46-south-park-{facade,south,north,west,east,top,aerial,aerial-night}.png
46-south-park-contact-sheet.png
validation.json             machine-readable contract report
REFERENCE.md                the research dossier this was built from
optimize/                   stage-4 shrink pass (see §7)
```

## 2. Dossier corrections — what the plan got wrong or under-specified

The plan was re-verified from primary sources before modelling, per the
pipeline's stage-2 override. Findings:

1. **Anchor moved 0.24 m east / 0.11 m south.** The plan's `-122.3938249,
   37.7821869` is the DataSF LiDAR footprint's area centroid; the model's own XY
   bounding-box centre lands 0.26 m from it once the parapet, pier and awning are
   included. The shipped anchor is **`-122.3938219, 37.7821864`**. This does not
   move the exclusion window materially — recomputed against the real bake input
   it becomes (1.42, 4.95) m instead of (1.21, 4.99) m, and `exclude: 3` still
   sits near its middle. See §6.

2. **The rear elevation is not blind, and the plan implied it was.** The plan's
   2.4 describes the two party walls as blind and leaves the rear "not observed".
   Modelling it blind as well would give a four-flat building with no daylight at
   all: both long sides *are* party walls, so the rear is the only elevation
   these flats can see out of, and the 8 m step down exists precisely to get
   light into the middle of a 29 m deep plan. Ten plain punched openings are
   modelled on the rear. **All of it is inferred** and is labelled as such here
   and in `REFERENCE.md` §4.

3. **The service doors and the flat door are glazed and white, not dark.** The
   plan's 2.7 specified a `Toy_ink` panel for the double-door bay and the entry.
   The January 2025 panorama shows white-framed glazed double doors and a white
   door in the purple recess. Built as glazed/white; the ink reading also turned
   the building's one colour into a black slot with a purple edge.

4. **The plan's "one grey stucco" is not buildable as one grey.** See §4.

Nothing in the plan's measured values needed correcting: the footprint, the
bearing, the 16.15 m crest, the 13.90 m deck and the ~24%-at-8 m rear fraction
all survived re-verification.

## 3. Height, and how it was settled

The plan's headline open question (its 2.15) was what the 2.25 m between the
13.90 m roof deck and the 16.15 m LiDAR maximum actually is. It is settled here
as a **solid front parapet / terrace screen**, on three independent grounds:

- **Photogrammetry off the Jan 2025 panorama puts the top of the stucco band at
  15.9 ± 0.5 m** — 0.25 m from the LiDAR maximum. The panorama is levelled
  equirectangular, so elevation angles read straight off pixel rows; the
  camera's reported position is unusable (it puts the lens 6.9 m from the OSM
  front edge but 3.8 m from the surveyed parcel's, a 3.1 m disagreement that
  condemns the position rather than either survey), so distance was solved from
  the panorama itself: the 9.47 m frontage subtends 56.9°, which by the sine rule
  against the known 45.2° frontage bearing puts the lens 8.5 m out. Full working
  in `REFERENCE.md` §3.
- **The nadir aerial shows nothing tall anywhere on the roof.** No penthouse box,
  no side face, no cast shadow. Whatever the extra height is, it is at the edge.
- **Both immediate neighbours have the identical bimodal LiDAR signature** —
  54–58 South Park at median 13.50 / max 16.94 / std 3.89, and 70 South Park (the
  Gallery House) at 12.87 / 16.35 / 3.57, against this building's 13.52 / 16.15 /
  2.47. 70 South Park's permits explicitly reconfigure a roof-level penthouse
  serving a terrace. Three consecutive 2005–2009 infill houses with the same
  profile is a typology.

The alternative — a set-back top floor whose front wall is flush — is not
excluded by anything observed, and would change the roof composition. **It would
not change the crest**, so the loader's scale is 1.0 either way and the risk is
contained.

**The Gallery House attribution trap was closed before modelling.** Two sources
place Ogrydziak Prillinger's latticed "Gallery House" at 44–46 South Park. It is
at **70 South Park** — parcel 3775-053, permit 200510064957, 5,418 sq ft, 2009,
which is the exact area the architecture press quotes for it. No lattice was
modelled. Full evidence in `REFERENCE.md` §2.

## 4. Design decisions, and the iteration log

Four review passes from the high three-quarter aerial before the formal rig, per
the pipeline's stage-2 rule.

**Pass 1 — the glazing was invisible.** The window wall was authored 0.35 m
*behind* the stucco plane, as a real recess. But every object here is a closed
prism and none of them has an opening cut in it — that is what keeps the
per-object signed-volume normal test meaningful — so the glass plane sat inside
the solid body and the first aerial rendered a blank grey slab with a white
picture frame on it. Rebuilt with the glass a few centimetres *proud* of the
stucco and the frame and grid proud of that, which is how the reference
implementation (`artifacts/106-south-park/`) handles openings and is the only
way a solid-prism asset can show one.

**Pass 2 — a single mid grey turned the asset into a grey box.** The real
building's stucco is one colour all over. Authored that way, at `Toy_steel`
(`9aa0a6`), the aerial read as a featureless grey block: the white grid and the
grey surround were too close in value to separate, and the whole recognition of
this building is *white grid in a darker frame*. The two elements that **frame**
the grid — the 2.25 m screen band above it and the 0.48 m pier beside it — were
moved to `Toy_roofd` (`45454a`). Deliberately **not** applied to the body, the
party walls or the rear: a dark palette that looks right in this rig renders
near-black in the app, and 2.25 m of band plus a 0.48 m pier is as much darkness
as this asset can carry. Logged as a knowing departure from observation.

**Pass 2 — the day preview of the night state was wrong, and it was the rig's
fault.** The build script leaves every `_Glow` material emitting at strength 1.0
so the night pass only has to scale it, and the render rig's `fade_glow()` (which
previews the app's day state at 12% alpha) was inherited from 106 South Park
unchanged — it drops the alpha but left the emission on. On a punched-window
asset that is invisible; on a 5 m wide hero shopfront shell it washed the whole
ground floor out to flat pale grey and would have had me judging a facade the app
never shows. `fade_glow()` now zeroes emission as well. Note also that a closed
glow shell is **two** alpha layers, so it reads ~23% by day, not 12%; the
ground-floor shell was cut from the full 4.2 m storey to a 2.7 m band for the
same reason.

**Pass 3 — the doors.** Corrected to glazed/white, per §2.3.

**Pass 4 — the rear roof was a blank lid.** A quarter of the plan, seen from
directly above, with nothing on it. A hatch and two vents added — the style bible
treats roofs as facades and the camera looks down.

**Pass 4 — aerial framing.** At 37° down, the near (street) corner projects well
below the bbox centroid, and a centre-aimed frame clipped the building's own base
off the bottom edge. The hero camera now aims at `min_z + 0.34 × height`.

**Night emission.** 3.2 (the 106 South Park value) clipped the ground-floor hero
glow to flat white — that shell is 5 m of near-white `Toy_trim_Glow`, an order
more area than a punched window. 1.8 keeps it the brightest thing in frame while
the four cool upper panes still read as separate lights.

**The pane grid.** The real wall is roughly five panes by twelve. It is modelled
as **three structural bays by four floor bands of raised trim on one glass
plane**. A faithful grid is ~60 framed openings and roughly 4,000 triangles on
its own, none of which resolves at the app's camera; the cue is the whiteness and
the regularity, not the count. This is the single decision the triangle budget
turns on.

**Off-palette material, declared.** `Toy_plum` (`6b4270`) is not in the
`sf-asset-check` palette. It is the residential entry's surround and awning — the
only colour on the building and its fifth recognition cue — and no palette entry
is anywhere near purple. `sf-asset-check` scores an off-palette colour as a WARN,
not a failure. This one is knowing.

**Deliberate omissions.** No tenant signage (the `MGV` neon, the `46` numerals);
no street tree, utility pole, overhead wires or streetlight bracket; no
neighbours, vehicles or people.

## 5. Validation — `validation.json`

Fresh factory-reset Blender scene, importing only the exported GLB. **16 / 16
checks PASS.**

| Check | Result |
|---|---|
| meters and plausible dimensions | PASS — 27.93 x 27.62 x 16.15 m |
| crest normalized to target | PASS — bbox top 16.150 m exactly |
| base at z = 0 | PASS — min Z 0.0000 |
| centered XY | PASS — offset (0.0000, 0.0000) |
| under triangle budget | PASS — 4,505 / 6,000 |
| no image textures | PASS |
| no transparency | PASS |
| materials follow contract | PASS — all `Toy_*`, no `Toy_body` |
| no cameras or lights | PASS |
| no animation, skin or constraints | PASS |
| transforms applied | PASS |
| no negative scales | PASS |
| normals outward (signed volume) | PASS — all 10 shipped solids positive |
| normals outward (ray residual) | PASS |
| no degenerate geometry | PASS |
| no unexpected objects | PASS |

**On the 27.93 x 27.62 m XY bounding box:** that is the exact 45° rotation of a
9.47 x 29.43 m sliver, not a 28 m building. The loader scales by
`targetHeightM / measuredHeight`, which is 16.15 / 16.15 = **1.0000**.

Materials shipped: `Toy_glass`, `Toy_glassl_Glow`, `Toy_ink`, `Toy_navy`,
`Toy_plum`, `Toy_roofd`, `Toy_steel`, `Toy_stone`, `Toy_trim`, `Toy_trim_Glow`.

The table above is the **post-optimize** run: the same 16 checks were run and
passed on the pre-optimize 71-object / 4,532-triangle build as well, and were
re-run after the stage-4 shipping swap. That second run is the one that matters —
it is the only place a dissolve-manufactured sliver ever shows up, because
gltfpack re-emits stored normals (precedent: `350-brannan`). It reports
`invalid_or_nonunit_loop_normal_count: 0`.

## 6. Manifest entry and integration notes

```json
{
  "id": "46-south-park",
  "file": "46-south-park.glb",
  "anchor": [
    -122.3938219,
    37.7821864
  ],
  "targetHeightM": 16.15,
  "cat": 2,
  "name": "44-46 South Park",
  "estimated": false,
  "dims": [
    27.9295,
    27.6198,
    16.15
  ],
  "tris": 4505,
  "loadRadius": 2500
}
```

**Case B — new landmark.** `pipeline/lib/landmarks.mjs` needs
`id: '46SouthPark'`, `lon: -122.3938219`, `lat: 37.7821864`, `height: 16.15`,
`exclude: 3`, `camera: { distance: 130, yaw: 45, pitch: 24 }`.

**Exclusion, re-measured from the shipped anchor against the real bake input.**
`excluded()` in `pipeline/buildings.mjs` drops a footprint when its centroid *or
any ring vertex* falls inside the circle. The bake reads
`buildings_datasf.geojson` first and gap-fills from
`overture_buildings.geojsonseq`; because `addBuilding()` returns null on
exclusion, `markOccupied()` never runs, so the Overture twin of an excluded
DataSF footprint is re-attempted and has to be caught by the same circle.

| Polygon | Triggers at | Via |
|---|---|---|
| this building, DataSF SF3775217 | **0.26 m** | its own centroid |
| this building, Overture/OSM way 124884347 (`height=14`) | **1.42 m** | its centroid — **the FLOOR** |
| 26–28 South Park, DataSF SF3775049 (h 8.35) | **4.95 m** | nearest ring vertex — **the CEILING**, and a vertex it *shares* with this building's ring |
| 22–24 South Park rear wing, Overture (h 7.7) | 8.79 m | centroid |
| 54–58 South Park, DataSF SF3775219 (h 13.5) | 9.26 m | centroid |
| 54–58 South Park, Overture (h 14) | 9.36 m | centroid |
| 22–24 South Park, Overture (h 12) | 13.53 m | nearest vertex |
| 22–24 South Park, DataSF SF3775048 | 14.50 m | nearest vertex |

Safe window **(1.42, 4.95) m**; `exclude: 3` sits with 1.58 m of margin below and
1.95 m above. A correct exclusion here drops **exactly two rings** — the DataSF
footprint and its Overture twin. If `verify-rebake.mjs` reports one or three,
something is wrong. Do not raise past 4.5: at 4.95 this starts deleting 26–28
South Park, whose LiDAR ring shares a party-wall vertex with this one.

Do **not** set `clearTrees`: at 3 m the radius clears nothing, which is correct —
the street tree in front of the south-west end belongs to the park's rim
planting.

`loadRadius`: the default formula gives `max(2500, 16.15 × 30) = 2500` m.

## 7. Stage 4 — optimize

Full report: `optimize/REPORT.md`. **All gates PASS.**

| | Input | Shipped | Δ |
|---|---|---|---|
| raw bytes | 279,332 | **124,584** | −55.4% |
| gzip -9 bytes | 45,963 | 87,807 | +91.0% (qualified — see optimize §G6) |
| nodes | 71 | **10** | −85.9% |
| draw submeshes | 73 | **11** | −84.9% |
| triangles | 4,532 | 4,505 | −0.6% |
| bbox / origin / materials | — | identical | 0 |
| appearance, mean abs RGB Δ | — | 0.008–0.079% | gates 2% far / 4% near |

Phase B welded 6,916 coincident vertex pairs and joined 71 objects into 10 per
material. The limited dissolve was **run** here, not skipped: §3.3's warning is
about closed annulus ring bands and this asset has none — every parapet and band
is an independent four-sided prism. It returned zero triangles and manufactured
no slivers. Curve retessellation was skipped: halving the five 10-segment
cylinders would clear the one-pixel chord test by only 30% and they are the
asset's only round forms.

## 8. Gate 3 — approval

Approval for this asset was given in advance, in the session's opening
instruction, verbatim:

> **"APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"**
> — David, 16 August 2026

That is a standing pre-approval covering the whole run, not a per-render look, so
it is recorded here as such: the contact sheet, the aerial day and night renders
and the numbers in §5 were produced and presented, but **no reviewer looked at
them before the pipeline advanced to stage 4**. Anyone re-reviewing this asset
should treat the visual gate as un-exercised.

Push, PR and deploy were **not** covered by that instruction and were not done —
this session ends at a local, source-only branch, which is what `BATCH: yes`
prescribes regardless (`ADDRESS-TO-ASSET.md`, "Batch mode").
