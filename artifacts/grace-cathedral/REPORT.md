# Grace Cathedral — build & validation report

**Status: PASS** (15/15 contract checks, fresh-scene re-import of the exported GLB).
Asset only — nothing integrated, no app code, manifest, or pipeline file touched.

| | |
|---|---|
| Deliverable | `grace-cathedral.glb` (772 KB) |
| Source | `build_grace_cathedral.py` → `grace-cathedral.blend` |
| Blender | 5.2.0 LTS, headless (`-b --python`) — see "Environment note" |
| Objects / triangles | 550 / **10,814** (budget 27,000; 40% used) |
| Dimensions (x, y, z m) | 109.094 × 48.169 × **75.300** |
| bbox min / max | (−54.547, −24.084, 0.0) / (54.547, 24.084, 75.3) |
| min Z / XY centre offset | 0.0 m / (0.0, 0.0) |
| Materials | 11, all `Toy_*`, flat, opaque, no textures |
| Glow set | `Toy_white_Glow` (rose tracery), `Toy_gold_Glow` (portal tympanum, flèche lantern), `Toy_mustard_Glow` (lit panes in all 49 windows) |

## Orientation decision (required by the task)

The asset is authored **world-true**: Blender `+Y` = true north, `+X` = east, so
`placeGeneric` (which only scales and positions — verified in
`app/src/assets.js:266`) drops it in at its real heading with no rotation.

**Measured heading: the nave long axis bears 81.03° cw from true north**,
computed by PCA over the 27 nodes of OSM way/32946942 (oriented extent
95.8 × 43.4 m, matching the published 329 × 162 ft). The twin-tower entrance
front and rose window therefore face ~ENE-to-E onto Taylor Street and the
polygonal apse closes the west end — the plan's "long axis nearly east-west,
entrance east" confirmed and made precise. The build works in a local (u, v)
frame rotated by that bearing and converts to world axes at mesh creation
(`W()` in the build script), so the heading is baked once and cannot drift.

## Where this build departs from the plan (and why)

1. **Height: 75.3 m, not 53 m.** The plan takes OSM `height=53` (the towers) as
   the top and never mentions the flèche. Wikipedia's own infobox gives the
   central spire as **247 ft / 75.3 m above street**, with the flèche measuring
   117 ft from the roof ridge — which also *derives* the nave ridge at
   ≈ 39.6 m. Photographs confirm a prominent verdigris flèche with a gold cross
   at the crossing. It is modelled, and `targetHeightM` is **75.3** so the app's
   `targetHeightM / size.y` scale lands on ×1.0000 and every published storey
   height stays true. Shipping the plan's 53 would squash the whole cathedral
   to 70% scale.
2. **Roofs are copper-brown, not dark gray.** The plan assigns `Toy_roofd`
   (#45454a) to all roofs; the close-up flèche photo and the flank views show
   brown standing-seam metal. Nave/transept/choir/apse use `Toy_roofc`
   (#7c6553, off-palette **WARN**), aisles use the palette `Toy_rust` for the
   value break the plan asks for in §2.9, and ridges are capped in the palette
   `Toy_verdigris` tying every slope to the flèche. This is also what saves the
   model from the all-gray deadness the plan warns about in §2.15.
3. **Buttresses are engaged stepped piers with pinnacle caps, not flyers.** The
   task asked this question explicitly; no photograph in the reference set shows
   a flying arch on the nave flanks, so the conservative reading is modelled and
   the uncertainty is recorded in REFERENCE.md.
4. **Anchor moved.** See below.

## Manifest draft (do not apply — integration is a separate job)

```json
{
  "id": "grace-cathedral",
  "file": "grace-cathedral.glb",
  "anchor": [
    -122.4134339,
    37.7918333
  ],
  "targetHeightM": 75.3,
  "cat": 8,
  "name": "Grace Cathedral",
  "estimated": false,
  "dims": [
    109.094,
    48.169,
    75.3
  ],
  "tris": 10814
}
```

**Anchor derivation** (the plan's `-122.4136014, 37.7918406` is ~13 m off for
this model): `placeGeneric` puts the model's ORIGIN on the anchor, and the
origin is the exported bounding-box centre — which includes the east entrance
steps and therefore sits 5.53 m east of the OSM footprint centroid. Measured
footprint bbox centre is `-122.4134968, 37.7918332`; the model origin projects
to **`-122.4134339, 37.7918333`** using the app's own projection constants
(`111320·cos 37.77°`, `110540`). `estimated: false` — both the height and the
anchor come from published/measured sources.

## Validation (fresh isolated scene, re-imported GLB)

`validate_grace_cathedral.py` factory-resets Blender, imports only the exported
GLB and reports on the re-import — never the authoring scene. Full machine
output in `validation.json`.

| Check | Result |
|---|---|
| Meters, plausible dimensions | PASS — 109.09 × 48.17 × 75.30 |
| Base at z = 0 | PASS — min Z exactly 0.0 |
| Centred in XY | PASS — offset (0.0, 0.0) |
| Triangle budget ≤ 27,000 | PASS — 10,814 |
| No image textures | PASS — 0 images, 0 textured materials |
| No transparency | PASS — every material alpha 1.0 |
| Materials follow contract | PASS — all `Toy_*`, no `Toy_body` |
| No cameras / lights | PASS — 0 / 0 |
| No animation, skinning, constraints | PASS — 0 / 0 / 0 |
| Transforms applied | PASS — all objects identity loc/rot/scale |
| No negative scales | PASS |
| Normals outward | PASS — 0 non-unit loop normals; 19,731 visibility-ray first hits, **0 flipped** |
| No degenerate triangles | PASS — 0 |
| No unexpected objects | PASS — 550 meshes, nothing else, no foreign geometry |
| Glow set is night-only | PASS — all three `_Glow` materials ship emission 0.0 |

**Normal method:** every source mesh runs `bmesh.ops.recalc_face_normals`
before export; the validator then fires 22,500 deterministic Fibonacci-sphere
rays inward at nine targets spread through the massing and requires that the
first face each ray meets opposes the ray.

## Night state

The app draws every `*_Glow` material as a separate **unlit overlay** whose
opacity is `0.12 + 0.95 · uNight` (`app/src/kit.js:199`), so a glow surface is
12% present in daylight. Nothing primary is authored as `_Glow`: the rose
glazing is opaque `Toy_glass` and the glow is a set of thin tracery rings 4 cm
proud of it, with the trim spokes standing prouder still and silhouetting over
them. Glow set:

- `Toy_mustard_Glow` — **lit panes in all 49 windows**: both aisle flanks, the
  clerestory, the transept great windows and arm flanks, the choir, the apse
  and the tower stages. Each is a second, smaller lancet 5 cm in front of its
  opaque `Toy_glass` pane, inset on all sides so a dark glazed reveal frames
  it and its back edge is buried in the wall. By day the window still reads as
  dark glazing with a faint warm centre — the pane never depends on the glow
  layer to exist (`lit_lancet()` in the build script).
- `Toy_white_Glow` — rose-window tracery rings + hub (the lit "Canticle of the
  Sun"), cool against the warm windows so the rose stays the hero.
- `Toy_gold_Glow` — portal tympanum over the Ghiberti doors, and the flèche
  lantern liner reading as a small warm beacon at the crossing.

This supersedes the plan's "keep it to two glow surfaces" (§2.8) at David's
request. It costs no draw calls — the loader merges every glow surface into a
single glow mesh — and 1,464 triangles.

**Render-script gotcha worth keeping:** the GLB ships emission at 0.0 per the
contract, so its glTF `emissiveFactor` is (0,0,0) and **the importer defaults
every material's Emission Color to white**. A night preview that only raises
Emission Strength therefore lights every glow surface white, whatever colour it
was authored. The app does not behave that way — its glow layer carries each
surface's own baked colour — so the night code copies Base Color into Emission
Color first. Without that fix the lit windows previewed as white instead of
amber.

`render_grace_cathedral.py` renders BOTH app states: day images force glow
alpha to 0.12, night images take alpha to 1.0 with emission on. The shipped GLB
is fully opaque either way — the transparency exists only inside the render
scene.

## Review renders

All eight are re-imports of the shipped GLB, so every image is the exact
exported geometry. The four elevations share one rig — same orthographic scale
(`span × 1.08`), framing, three-light tabletop setup, exposure and projection —
and differ only in azimuth; directions are true compass directions.

| File | What it shows |
|---|---|
| `grace-cathedral-east.png` | Entrance front: twin towers, rose over the gold doors, great steps |
| `grace-cathedral-north.png` / `-south.png` | Flanks: 6 aisle bays, buttress comb, clerestory, transept gable |
| `grace-cathedral-west.png` | Polygonal apse and choir gable under the flèche |
| `grace-cathedral-top.png` | Roofscape: ridge cresting cross, aisle value break, tower crown decks, buttress comb, apse fan |
| `grace-cathedral-aerial.png` | The app's camera — 38° down, 88 mm lens |
| `grace-cathedral-night.png` / `-night-east.png` | Dusk state; lit rose, portal, flèche lantern |
| `grace-cathedral-contact-sheet.png` | All eight, labelled |

## Design notes (style bible §22)

Recognition cues kept: twin flat-crowned towers over a full-width flight of
steps; the 7.6 m rose centred between them; the verdigris flèche and gold cross
on a long cruciform body; the buttress comb; warm gray stone against copper
roofs. Simplified away: all tracery (one recessed lancet per bay), crockets,
statuary, gargoyles and the clock; the rose becomes ring + 12 chunky spokes,
which is not an arbitrary count — the window's documented geometry is the
Chartres 12-fold scheme. Roofs are designed rather than left blank: ridge
cresting, an aisle-roof value break, tower crown decks with stair penthouses
and vents, and pierced parapet slots. The transept arms' east and west faces
got a full bay rhythm after the first aerial review showed them reading as
blank slabs — the app's camera looks straight at them.

## Integration notes (for the separate job, per `docs/asset-plans/INTEGRATION-PROMPT.md`)

- `graceCathedral()` already exists procedurally in `app/src/landmarks.js`
  with an 80 m exclusion zone; id `grace-cathedral` maps to it, so this is a
  Case-A replace.
- Use `targetHeightM: 75.3` (scale ×1.0000) and the anchor above, not the
  plan's values.
- `min Z = 0` is the **east street level at the foot of the steps**; the entry
  podium is 6.1 m above it. Nob Hill rises westward, so check the west end
  against `sampleElevation` — the apse may want the terrain sampled at the
  building centre rather than the anchor.
- Nothing here has been committed; the working tree is untouched apart from
  this artifacts directory.

## Environment note

The task text specifies Blender 4.5 LTS at `/opt/blender`. This machine has
**Blender 5.2.0 LTS** at `/Applications/Blender.app/Contents/MacOS/Blender`,
which is what every script was run with (headless, CPU Cycles, no GPU). The
scripts take `blender -b --python <script> -- [args]` exactly as specified and
are path-agnostic.

See `OPTIMIZATION.md`: this GLB is the size-optimized build (geometry-identical; objects joined per material). Figures above reflect the shipped file.
