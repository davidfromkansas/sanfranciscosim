# Herbst Theatre / War Memorial Veterans Building — build report

Deliverable: `herbst-theatre.glb` — a validated toy-diorama miniature of the War
Memorial Veterans Building (401 Van Ness Avenue), the building that contains the
916-seat Herbst Theatre. Authored per `docs/styles/miniature-toy.md` (artistic
gate) and `.agents/skills/sf-asset-check/SKILL.md` (technical gate). Research
dossier: `REFERENCE.md`. Plan: `docs/asset-plans/herbst-theatre.md`.

Built as stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

## Files

| File | What |
|---|---|
| `build_herbst_theatre.py` | Deterministic build (headless Blender 5.2 LTS at `/Applications/Blender.app/Contents/MacOS/Blender`, no GPU) |
| `herbst-theatre.blend` / `.glb` | Source scene and the shipped export |
| `render_herbst_theatre.py` | Review renders — always re-imports the exported GLB |
| `validate_herbst_theatre.py` → `validation.json` | Fresh-scene re-import contract validation |
| `twin_test.py` | Places this GLB and the Opera House GLB at their real anchors and renders the pair (the plan's twin gate) |
| `make_contact_sheet.py` | Composes the review set |
| `herbst-theatre-{north,east,south,west,top,aerial,night,night-east,contact-sheet}.png` | Review set (one shared ortho rig for the four elevations) |
| `herbst-theatre-twin-{aerial,front}.png` | The twin test against the Opera House |

## Validated result (fresh-scene re-import of the GLB)

- **PASS** — `validation.json`, all 15 checks.
- **220 objects, 9,844 triangles** (budget 18,000), dims
  **92.53 × 70.71 × 31.00 m** (world-axis AABB of the building rotated 81.11°),
  min-z 0.0, XY centre offset 0.0 / 0.0.
- Normals: `inverted_solids: []`, **`ray_flipped_fraction` 0.0** across 22,500
  rays, 0 degenerate triangles, 0 non-unit loop normals. (Cleaner than the
  0.1%-tolerance the union-of-solids gate allows.)
- Materials (all palette, flat, textureless, opaque): `Toy_stone`, `Toy_sand`,
  `Toy_trim`, `Toy_glass`, `Toy_ink`, `Toy_roofd`, `Toy_steel`,
  `Toy_mustard_Glow`, `Toy_white_Glow` — the Opera House twin's set exactly.
  Glow ships with emission 0 (the night pass is the app's).
- 0 image textures, 0 cameras, 0 lights, 0 animations, 0 armatures, 0
  constraints, transforms applied, no negative scales.

## Orientation & placement (for the integration job)

- **Authored world-true**: the long axis bears **81.11° cw from true north**
  (OSM way/32865757 length-weighted dominant edge angle — the same bearing the
  Opera House twin measures); the colonnade front faces east onto Van Ness. The
  loader (`placeGeneric`) applies no rotation — none is needed.
- **Anchor (recomputed, use this): `-122.4210157, 37.7795789`** — the WGS84
  point under the exported bbox CENTRE. It sits ~2 m east and ~4 m north of the
  raw footprint oriented-bbox centre (−122.4210354, 37.7795452) because the
  model carries its own front steps and because the footprint is notched at the
  rear, so the AABB centre is not the polygon centre. `placeGeneric` puts the
  exported bbox CENTRE on the anchor, so this is the value that lands the
  building on its footprint.
- `targetHeightM` **31** = the exported max-z exactly, so the loader's
  `targetHeightM / measuredHeight` scale lands at **1.0000**.

## Design decisions

### The height (the number most likely to be wrong)

`targetHeightM = 31`, shipped **`"estimated": true`**. The OSM tag on this
building is `height=28`, and it is *not* the architectural top — it is the
parapet. Full reasoning in `REFERENCE.md`; in short: the Opera House dossier
derived its own main-block parapet from **this building's** 28 m tag, the twins
are officially "substantially identical", this building has no fly tower, and
the Opera House's front-block hip — the same element on the same cornice line —
peaks at 31.0 m. Adopting 31.0 m makes the pair share a base course, a cornice
line, a front attic parapet and a roof ridge. No published elevation or section
was found; a real one would supersede this.

### Twinning

Every z constant is lifted unchanged from
`artifacts/war-memorial-opera-house/build_war_memorial_opera_house.py`: base
course top 9.5, shafts 10.7–20.3, entablature 21.0–23.0, cornice 23.0–24.5,
front attic parapet 27.0, roof eaves 25.6. The palette and the glow scheme are
identical. This is deliberate and is the asset's main correctness requirement —
see the twin test below.

### Massing

Four-part scheme measured from the 37-node footprint (`REFERENCE.md` §
decomposition): 45.5 m front pavilion with stepped 52.2 m shoulders, full-width
67.38 m wings, 51.4 m main block, 41.15 m rear block on Franklin. Depth 83.06 m.
No fly tower, no stage house, no raised auditorium attic — the level silhouette
is the cue that tells this building from its twin at a glance from the air.

### Facade

Rusticated `Toy_stone` basement with 7 arched openings and a two-groove
rustication; giant-order colonnade of **7 open loggia bays separated by 8 PAIRS
of columns (16 shafts)**, bay pitch 4.843 m; a real 2.9 m loggia recess in front
of a solid front core (the Green Room loggia, SGH); one unbroken
entablature/cornice line at 24.5 m; attic parapet with inset panels; arched
windows in a regular rhythm on every visible elevation (8 per main-block flank,
2 per wing front, 2 per wing outer flank, 1 per shoulder flank). Service canopy
and doors on the **north** (McAllister) flank — the working side; the **south**
flank is the formal court-facing one, the opposite hand to the Opera House.

### Roofscape

With no tower, the roof carries the whole aerial read, so it is composed rather
than defaulted. Three *truncated* hips (hipped perimeter around a flat deck —
which is what "metal roof with skylights", SGH, actually describes) at one
~36–40° pitch, in a deliberate hierarchy: **wings 26.9 < main block 29.4 <
front block 31.0** (the summit). Six skylights on the main deck — four on the
court-facing south half, two north — plus two plant clusters and a stair
penthouse, all held below 31.0 m so the max-z stays exact.

### Night state

Per the app's dusk system (glow shells only, never primary surfaces):
`Toy_mustard_Glow` lit panes 5 cm proud behind every opaque `Toy_glass` arch
(7 basement + 7 loggia + 24 flank/wing/shoulder windows) and one thin
`Toy_white_Glow` soffit strip under the entablature as the floodlit-colonnade
cue. Rear service windows deliberately stay dark. Every glow surface's day
colour is a palette entry its non-glow neighbours already use, so nothing shifts
at noon. Matches the twin exactly.

## Corrections applied to the plan doc

The plan is a head start, not a citation — these are the places it was wrong.

1. **Roof form.** The plan specified two ridged hips. Built as truncated hips
   instead: better match to "metal roof with skylights", one shared pitch, and a
   deck to design on.
2. **Roof extent.** The plan implied the front hip could span the full 67.38 m
   wing width. It cannot — the pavilion is 45.5 m and the shoulders 52.2 m, so a
   full-width front roof hangs over open air at the front corners. This was
   visible in the first build's aerial and is fixed: the front hip is bounded to
   the 52.2 m shoulder width and the wings get their own low roofs.
3. **Loggia back wall.** The plan called for a wall; a wall alone left a void
   between it and the wings that only the roof hid. Built as a solid 52.2 m
   front core to the cornice, with the loggia as a real 2.9 m recess.
4. **Shoulders.** The plan made them an extension of the stone corner pavilions.
   Full-height stone merged the two into one blank slab corner that swallowed
   the colonnade's proportions; built in `Toy_sand` starting above the
   entablature instead.
5. **Wing roofs.** First build used flat decks that ended up buried inside the
   wing parapets — invisible dead geometry that made the wings read as pale sand
   terraces from above. Replaced with visible low dark hips at 26.9 m.

## The twin test (the plan's gate)

`twin_test.py` imports both shipped GLBs at scale 1.0 and places each so its
bbox centre sits on its manifest anchor, using the repo's own projection —
exactly what `placeGeneric` does. Renders: `herbst-theatre-twin-aerial.png`
(the pair across the memorial court from the app's camera) and
`herbst-theatre-twin-front.png` (an orthographic elevation along the shared
81.11° bearing, where a cornice mismatch of even a metre would be unmissable).

Result: see the QA table below.

## Draft manifest entry (do NOT apply in this task)

```json
{
  "id": "herbst-theatre",
  "file": "herbst-theatre.glb",
  "anchor": [-122.4210157, 37.7795789],
  "targetHeightM": 31,
  "cat": 17,
  "name": "Herbst Theatre (War Memorial Veterans Building)",
  "estimated": true,
  "dims": [92.532, 70.711, 31.0],
  "tris": 9844,
  "loadRadius": 2500
}
```

`dims`/`tris` are the pre-optimize numbers and are rewritten to the shipped
values by stage 4.

**Streaming decision (mandatory, PERF-PLAN #3):** `loadRadius: 2500` — the
skill's default `max(2500, targetHeightM * 30)`. At 2,500 m the whole Civic
Center is a small cluster on screen, so the swap to the baked stand-in is
illegible. Noted: the Opera House twin ships with no `loadRadius` (boot-loaded),
so beyond 2,500 m the pair is GLB + baked. That is acceptable at that distance
but is called out for the integration QA.

## Integration notes

- **New landmark (Case B).** Needs a `pipeline/lib/landmarks.mjs` entry
  (`id: 'herbstTheatre'`) **and a re-bake of the affected tiles**, or the baked
  procedural building will intersect the GLB.
- Manifest id `herbst-theatre` maps to `herbstTheatre`.
- Exclusion radius: the Opera House uses 62 for a 104 × 73 m footprint; 58 for
  this 83 × 67 m one.
- The model includes its own front steps; the memorial court, its planting and
  the streetscape are app-side.
- This closes the open item the Opera House's `REPORT.md` left behind: *"the
  near-identical Veterans Building stays procedural — check the pair still reads
  as twins."* It no longer stays procedural.

## QA per the plan's Part 1

| Item | Status |
|---|---|
| Fresh-scene re-import validation (not the authoring scene) | PASS (`validation.json`, 15/15) |
| min-z ≈ 0, XY centred | PASS (0.0 / 0.0, 0.0) |
| Max Z equals target height exactly (loader scale 1.0000) | PASS (31.000) |
| Real-metre dims consistent with the measured footprint | PASS |
| ≤ 18,000 triangles | PASS (9,844) |
| Materials `Toy_*`, flat, no textures/alpha, no `Toy_body` | PASS |
| `_Glow` only on lit panes + colonnade soffit, emission 0 | PASS |
| No cameras/lights/animations/armatures/constraints | PASS |
| Transforms applied, no negative scales, outward normals | PASS (flipped fraction 0.0) |
| No foreign/leaked geometry | PASS (fresh factory scene build, 220/220 objects) |
| 5 controlled views + aerial + night ×2 + contact sheet from the export | PASS |
| Twin test — cornice/base/roof aligned with the Opera House | PASS (see above) |
| Committed | PASS — stage-2 gate commit on `pipeline/herbst-theatre` |
