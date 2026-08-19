# 50 United Nations Plaza — build report

**Deliverable:** `50-united-nations-plaza.glb`, a validated miniature of the
Federal Office Building at 50 United Nations Plaza (Arthur Brown Jr., 1934–36),
built for the SF-SIM toy-diorama city.

REPORT beats plan. Where this file and
`docs/asset-plans/50-united-nations-plaza.md` differ, this file is the record of
what was actually built; `REFERENCE.md` is the record of what was measured.

## Numbers

| | |
|---|---|
| Triangles | **13,624** / 24,000 cap (27,000 repo landmark ceiling) |
| Dimensions (axis-aligned, m) | **122.73 × 84.90 × 33.00** |
| Oriented footprint | 112.53 × 66.93 m at bearing 80.92 deg, + 0.90 m cornice |
| `targetHeightM` | **33.0** — bbox top normalised to it exactly, loader scale = 1.000 |
| min Z / XY centre offset | 0.0000 m / (0.0000, 0.0000) m |
| Objects | 548 (the loader merges them to 2 draw calls in the shared batch) |
| Materials | 11, all `Toy_*`, flat, opaque, no textures |
| Glow set | `Toy_gold_Glow` (6 arched entrances) + `Toy_white_Glow` (attic window band) |
| GLB on disk | see `ls -l` below; the stage-4 optimize pass has not run yet |
| Anchor | **−122.4144853, 37.7804351** (see "Corrections") |
| Category | 18 (Government) |

## Validation — `validation.json`, overall **PASS**

Fresh factory-reset Blender scene, re-importing the exported GLB. The authoring
`.blend` was not inspected.

| Check | Result |
|---|---|
| meters and plausible dimensions | PASS |
| base at z = 0 | PASS (min Z 0.0000) |
| centred in XY | PASS (0.0000, 0.0000) |
| under triangle budget | PASS (13,624 / 24,000) |
| no image textures | PASS (0 images, 0 textured materials) |
| no transparency | PASS |
| materials follow contract | PASS (11 × `Toy_*`, no `Toy_body`) |
| no cameras or lights | PASS |
| no animation, skinning or constraints | PASS |
| transforms applied | PASS |
| no negative scales | PASS |
| **normals outward** | PASS |
| no degenerate geometry | PASS (0) |
| no unexpected objects | PASS |

**Normals method.** Every source mesh runs `bmesh.ops.recalc_face_normals` before
export. Because this asset is a *union of solids*, the authoritative test is
**per-object signed volume**: all 548 objects enclose a positive volume
(`negative_signed_volume_objects: []`). Backing that up, 22,500 deterministic
visibility rays over 15 targets (the four wings and the courtyard at three heights)
produced 22,467 first hits and **0 flipped visible faces** — a 0.000% residual
against the 0.15% allowance.

## What was built

Authored in Blender directly in world metres, Z up, +X east, +Y north, then the
whole assembly rotated **+9.08 deg about Z** so it drops into the city at its real
heading with no loader rotation. The hero front faces south onto United Nations
Plaza, so the contract's "front faces −Y" and the real-world heading agree to
within 9 degrees.

- **The ring.** Four abutting bars (south / north / west / east) tile the plan
  exactly, which is what makes the 72.2 × 27.1 m courtyard a real void while
  keeping every piece a closed convex solid.
- **The two south corners are concave scoops** — 8-segment arcs of R 10.4 m bowing
  6.9 m into the building, each carrying an arched entrance. The north corners are
  square. This asymmetry is the plan-level recognition cue.
- **Vertical composition, all four sides:** plinth; rusticated `Toy_stone` base to
  11.0 m with three reveal courses; belt course; a two-storey order to 22.1 m; a
  0.90 m projecting cornice at 23.2 m; a set-back attic behind a balustrade; a top
  cornice at 29.0 m; a hipped metal roof cresting at 33.0 m.
- **South front:** 18 free-standing Doric columns standing 0.85 m proud under that
  cornice, with a continuous balustrade band between them and three arched
  entrances at the centre. West, east and north get proud pilaster strips on the
  same 5.3 m rhythm.
- **North central wing** (|x| < 31 m) stops four storeys up: parapet at 24.7 m,
  flat deck at 23.4 m carrying a `Toy_mint` green roof, two `Toy_navy` PV banks,
  three white mechanical boxes and a `Toy_stone` gravel margin. Its two end
  pavilions stay full height, so the north side reads as a low centre between two
  taller granite pavilions.
- **Roof:** five hip bars of equal pitch (35 deg) and equal eave height. Where two
  meet at a right angle their planes intersect exactly on the 45-degree diagonal,
  which *is* the correct hip line, so the union needs no boolean.
- **Courtyard:** paved floor with a `Toy_sand` walk cross, two planting beds, eight
  tree pucks, light glazed-brick liners with vertical window slots on all four
  walls, and the 2013 elevator bulkhead on the east side.
- **Night:** six `Toy_gold_Glow` arched entrances (three south, one per concave
  corner, one north) and a continuous `Toy_white_Glow` attic window band that
  traces the cornice line all the way round — which is what gives this low, wide
  building a readable silhouette from the app's aerial camera after dark. Two glow
  sets, nothing else, no invented facade floodlighting.

## Palette

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `f2ede3` | main granite walls, attic storey |
| `Toy_stone` | `d9d2c2` | rusticated base, plinth, courtyard floor, gravel margin, bulkhead |
| `Toy_trim` | `f3efe6` | columns, pilasters, belt course, cornices, balustrades, parapets |
| `Toy_sand` | `ece4d4` | courtyard brick liners and walkways |
| `Toy_glass` | `2a4d73` | all windows and the arched openings |
| `Toy_steel` | `9aa0a6` | the standing-seam metal hip roof and its dormers |
| `Toy_navy` | `2c4a70` | the two photovoltaic banks |
| `Toy_mint` | `8fd0a8` | the green roof and courtyard trees — the one saturated accent |
| `Toy_white` | `f7f4ec` | rooftop mechanical boxes |
| `Toy_white_Glow` | `f7f4ec` | the attic window band (night) |
| `Toy_gold_Glow` | `caa64a` | the six arched entrances (night) |

`Toy_roofd` was deliberately **not** used for the metal roof: it renders as
rgb(9,9,12) on a roof deck in the app and would have turned the building's largest
visible surface black. `Toy_steel` is both the correct zinc colour and safe.

## Corrections and decisions

1. **The anchor moved 0.7 m.** The plan anchored on the OSM OBB centre
   (−122.4144797, 37.7804306). The model centres on its own bounding box, and
   because the two south corners are scooped while the north corners are square,
   that box centre sits 0.49 m east and 0.49 m south. **Shipped anchor:
   `−122.4144853, 37.7804351`**, reported by the build script.
2. **"Roof outline" in plan §2.4 means the CORNICE outline.** With the wall plane
   at 112.53 × 66.93 and a 0.90 m cornice projection, the cornice outline is
   114.33 × 68.73 m against DataSF's LiDAR box of 114.10 × 68.96 — agreement to
   0.25 m, which is the cross-check the plan intended. The metal roof itself sits
   inboard of that.
3. **Height confirmed, not corrected.** 33.0 m crest / 29.0 m parapet / 24.7 m
   north wing all re-derived independently in `REFERENCE.md` §3.
4. **18 columns, not ~26.** A deliberate rhythm reduction; the real count is read
   from photography and is itself *inferred*.
5. **No facade floodlighting.** A targeted search found no documented night scheme,
   so none was invented.

## Defects found and fixed during the build

Each of these shipped once in an intermediate render and was caught in review:

1. **Self-intersecting south outline.** The two concave corner arcs were spliced in
   the wrong order, so the south bar's polygon crossed itself and the whole base
   rendered as broken backfaces. Fixed by walking the outline CCW: west edge → SW
   scoop forward → south wall → SE scoop reversed → east edge.
2. **Black patches on the roof corners.** Overlapping hip bars had *coplanar* flat
   tops which z-fought to black. Each bar now crests a few centimetres below the
   one that hides it (south wins at the south corners, west/east over the
   pavilions).
3. **Whole window rows invisible.** Panes were placed at a single plane offset
   while the rusticated base stands 0.25 m proud of the body, so both base rows
   were buried inside the wall. Every storey now carries its own plane offset, and
   the clearance was raised from 0.01 m to 0.07 m — at 0.01 m a pane only showed
   where a rustication course happened to recess the wall behind it.
4. **Entrance arches invisible, then transparent.** First they were recessed behind
   the proud base (there are no booleans here, so anything behind that face never
   renders). Then, built as one solid whose outward face carried the glow material,
   they went see-through: at the loader's 12% day opacity the ray does *not* land
   on the solid's far cap but on the wall behind it (verified in Cycles with the
   glass recoloured red). The fix, applied to the attic windows too: **an opaque
   dark pane with a thin glow plate standing on its outer face**, so the day read
   is the pane's own colour and depends on nothing behind it.
5. **Corner arches edge-on.** `arch_prism` extrudes along `(-sin yaw, cos yaw)`, so
   the two concave corner entrances needed 135 deg, not the 45 deg their faces sit
   at. The yaw is now derived from the outward normal so it cannot be wrong again.
6. **Pilasters and windows floating in the scooped corners.** The west and east
   walls stop at the concave corners; their rhythms now start north of the scoop.
7. **The courtyard read as a striped billboard.** Horizontal storey bands on the
   courtyard walls became a barcode from the app's three-quarter camera. Replaced
   with vertical slots on the courtyard's own bay rhythm, which read as windows.
8. **Black square in the courtyard.** Two coplanar paving slabs, z-fighting.

## Files

```
artifacts/50-united-nations-plaza/
  build_50_united_nations_plaza.py     deterministic build (Blender headless)
  render_50_united_nations_plaza.py    controlled review renders of the EXPORT
  validate_50_united_nations_plaza.py  fresh-scene contract validation
  make_contact_sheet.py                composes the seven renders
  50-united-nations-plaza.blend
  50-united-nations-plaza.glb          the shipping asset
  50-united-nations-plaza-{north,east,south,west}.png   four elevations, one rig
  50-united-nations-plaza-top.png      courtyard, hip roof, green roof, PV
  50-united-nations-plaza-aerial.png   the app's high three-quarter camera
  50-united-nations-plaza-night.png    the glow set
  50-united-nations-plaza-contact-sheet.png
  REFERENCE.md  REPORT.md  validation.json
```

Rebuild: `blender -b --python build_50_united_nations_plaza.py`
Re-render: `blender -b --python render_50_united_nations_plaza.py`
Re-validate: `blender -b --python validate_50_united_nations_plaza.py`

## Draft manifest entry

```json
{
  "id": "50-united-nations-plaza",
  "file": "50-united-nations-plaza.glb",
  "anchor": [
    -122.4144853,
    37.7804351
  ],
  "targetHeightM": 33.0,
  "cat": 18,
  "name": "50 United Nations Plaza Federal Office Building",
  "estimated": false,
  "dims": [
    122.7264,
    84.8953,
    33.0
  ],
  "tris": 13624,
  "loadRadius": 2500
}
```

`loadRadius` is the default rule `max(2500, 33.0 × 30)` = 2500. The production
manifest was not edited by this stage.

## Approval

_(stage 3 — pending)_
