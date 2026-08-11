# Fairmont San Francisco asset report

## Result

**PASS** — `fairmont-san-francisco.glb` meets the repository's landmark contract
and was validated after fresh-scene re-import in Blender 5.2.0 LTS. All 15
machine checks in `validation.json` pass; that file is the authority for every
metric below. The exact exported GLB was re-imported before all seven review
renders were produced, so every image depicts the shipping geometry.

Nothing was integrated or deployed: the production manifest, `pipeline/lib/landmarks.mjs`
and all app code are untouched, and nothing was committed. Integration is a
separate job (`docs/asset-plans/INTEGRATION-PROMPT.md`).

## Deliverables

- `REFERENCE.md` — research dossier and design decisions
- `build_fairmont_san_francisco.py` — deterministic model build/export script
- `render_fairmont_san_francisco.py` — fresh-GLB controlled render script
- `validate_fairmont_san_francisco.py` — isolated re-import validator
- `make_contact_sheet.py` — contact-sheet composer
- `fairmont-san-francisco.blend` — reproducible authoring scene (asset only)
- `fairmont-san-francisco.glb` — final binary deliverable (851 KB, self-contained)
- `validation.json` — full object-level machine report
- `fairmont-san-francisco-{north,east,south,west,top,aerial}.png`
- `fairmont-san-francisco-contact-sheet.png`
- `fairmont-san-francisco-night.png`, `fairmont-san-francisco-night-west.png`

Rebuild from this directory with:

```bash
blender -b --python build_fairmont_san_francisco.py && blender -b --python validate_fairmont_san_francisco.py && blender -b --python render_fairmont_san_francisco.py && blender -b --python render_fairmont_san_francisco.py -- --night && python3 make_contact_sheet.py
```

## Scope decision — both buildings

The GLB contains the **1907 Beaux-Arts block and the 1961/62 tower**, plus the
ballroom podium that physically joins them. Research settled this: on Nob Hill
the pair is how the Fairmont reads from any distance, every aerial and
street-level reference shows them as one massing, and the mapped OSM relation
covers both. Modelling the block alone would have produced an asset that is
accurate from Mason Street and wrong from every other approach.

Consequence, exactly as `docs/asset-plans/fairmont-san-francisco.md` §2.13
anticipated: `targetHeightM` is the tower's published **99.06 m**, not the
historic block's unpublished ~33 m, and the anchor moves to the centre of the
combined composition (below).

## Orientation — the plan's dossier was wrong, and this corrects it

The plan states the entrance faces **east** onto Mason Street with the tower
west of the block. Street data and imagery show the reverse, and the model
follows the evidence:

- Overpass places Mason Street ~65 m **west** of the complex centroid, Powell
  ~76 m east, California south, Sacramento north.
- The mapped footprint spans −52 m to +73 m east of the centroid, so Mason runs
  along the block's **west** edge, and the 1961 tower stands **east**
  (downhill, toward Powell) — confirmed against satellite imagery.

**Measured heading:** the Nob Hill grid runs **9.05° counter-clockwise from
cardinal** (ten long OSM edges bear 80.95°/170.9° true, agreeing within 0.4°).
The whole composition is yawed +9.05° so it drops into the city at its real
heading; Blender **+Y = true north, +X = east**, and the loader's `placeGeneric`
applies no rotation. The Mason Street entrance front therefore faces west, its
outward normal at **≈261° true**.

One consequence is visible in the review renders: because the asset carries its
true 9° yaw, a true-west orthographic elevation also shows a foreshortened
sliver of the north flank. That is correct behaviour, not a modelling error.

## Contract results

| Rule | Result | Evidence |
|---|---|---|
| Binary GLB, no external dependencies | PASS | 813 KB self-contained `fairmont-san-francisco.glb` |
| Plausible real-world meters | PASS | 124.73 × 98.31 × 99.06 m; footprint matches the mapped 117.9 × 84.1 m complex plus the 9° yaw and the porte-cochère projection |
| Origin / base | PASS | bounding-box min Z **0.0 m**; XY centre offset **[0.0, 0.0] m** |
| Orientation | PASS | authored true-world: +Y north, +X east, +9.05° grid yaw; entrance normal ≈261° |
| Triangle budget | PASS | **13,380 / 24,000** triangles |
| Applied transforms | PASS | all 17 imported mesh objects at location 0, rotation 0, scale 1 |
| Negative scales | PASS | none |
| Normals | PASS | 0 invalid/non-unit loop normals; **0 flipped visible first-hits across 19,470 of 22,500 deterministic rays** |
| Unexpected / leaked geometry | PASS | 17 mesh objects only; no studio floor, context, camera or light in the GLB |
| Image textures / PBR maps | PASS | 0 images, 0 texture nodes |
| Transparency | PASS | every material alpha 1.0, opaque (the app, not the asset, fades the glow buffer) |
| Flat material contract | PASS | 15 `Toy_*` materials, roughness 0.85, no `Toy_body` |
| Glow naming | PASS | `Toy_white_Glow` and `Toy_gold_Glow` only, on 16 declared night surfaces (see below) |
| Cameras / lights | PASS | 0 / 0 |
| Animations / armatures / constraints | PASS | 0 / 0 / 0 |
| Degenerate geometry | PASS | 0 degenerate triangles |
| Fresh isolated re-import | PASS | validator factory-resets then imports the final GLB; the render script repeats that isolation independently |

### Normals: what the first pass got wrong

Worth recording, because it is a trap for anything built from open shells. The
first export had **7,071 flipped visible faces**. `recalc_face_normals`
guarantees only that an open shell is *consistent*, not that it faces outward,
so the punched facade panels and the capless cornice/parapet rings came out
inside-out. The build now winds every face against an explicitly derived
outward direction (`wind()`), reading each loft's rings as a profile traversal:
rising strips are outer walls, falling strips are inner walls, and a horizontal
strip is a top surface when the plan steps inward and a soffit when it steps
outward.

That removed all but 118 hits. The remainder were **real holes, not bad
normals**: the facade panels stood 0.45 m proud of their core, leaving an open
notch at every building corner through which a grazing view saw the panels'
backs, and the cornice, podium rail and pool rim were single-sided ribbons. The
panels now close their perimeter back to the core, the cornice profile returns
down to the roof deck as a solid parapet, and the rail and rim are two-sided.
The last 3 hits were a coincident-face seam where the podium rail met its deck,
fixed by sinking the rail 0.4 m into the podium. Final count: **0**.

## Night state, and what actually triggers it

**Nothing in the GLB switches, and the asset holds no night mesh, timer or
flag.** The material-name suffix `_Glow` is the entire contract; the app owns
the trigger:

1. `app/src/env.js` computes the real sun elevation for the live San Francisco
   clock and sets `shared.uNight = ramp(elevation, −10°, 0°)` — exactly 0 while
   the sun is above the horizon, exactly 1 once it is 10° below, smooth through
   dusk.
2. `app/src/assets.js` splits the imported GLB into two merged buffers by that
   suffix: everything else becomes one lit `MeshLambertMaterial` body, while
   `Toy_*_Glow` faces become one unlit `MeshBasicMaterial` mesh
   (`userData.nightOnly`). That is why the whole asset still costs two draw
   calls.
3. `updateLandmarkGlow` in `app/src/kit.js` sets, every frame,
   `opacity = min(1, 0.12 + uNight × 0.95)`.

So the hotel lights up because the sun set over the real city, on the same
ramp that drives the street lamps and the procedural windows — not because
anything in this file said so.

**The constraint that shape falls out of:** a glow face is still drawn at
daytime, at 12% opacity — 88% transparent. A glow surface must therefore be a
thin veneer with solid body geometry directly behind it, never the only skin at
that spot, or the building would go see-through at noon. Every glow surface
here obeys that: the lit-room panes hover 0.03 m in front of the recessed
window glass, the cornice line and colonnade bands ride 0.06–0.07 m proud of
solid trim, and the Crown Room band sits just outside the tower's glazing with
the core behind it.

The night design, 16 objects across two glow colours:

| Surface | Material | Reads as |
|---|---|---|
| `glow_win_{w,n,s,e}`, `glow_win_pav_*` | `Toy_gold_Glow` | occupied guest rooms on the historic block — a deterministic ~1/3 scatter, not a switchboard |
| `glow_rooms_{w,e}` | `Toy_gold_Glow` | the same scatter per storey inside the tower's glass strips |
| `glow_cornice_line` | `Toy_white_Glow` | the floodlit cornice — the building's brightest line, and the cue that survives to city distance |
| `glow_colonnade_{plinth,entab}` | `Toy_white_Glow` | the giant order uplit from its plinth and downlit from the entablature |
| `pc_fascia`, `glow_pc_doors` | `Toy_white_Glow`, `Toy_gold_Glow` | the porte-cochère canopy and warm light spilling from the lobby doors |
| `twr_crown_fascia`, `glow_crown_room` | `Toy_white_Glow`, `Toy_gold_Glow` | the lit crown ring and the Crown Room band below it |

This is deliberately more than the asset plan's §2.8 note ("keep it to two
surfaces"), on David's explicit request for a full night state. The restraint
is kept in the palette instead: two glow colours, no coloured accent lighting,
and the roof and body stay dark so the lit cornice and windows carry the image.

The night renders reproduce the app's pass rather than flattering the asset:
`_Glow` materials become emission at strength 1.6 (the app draws flat unlit
colour with no bloom, so a hot value would be a lie), everything else drops to
a dim cool moon key. The day renders correspondingly put alpha 0.12 on the same
materials, which is why the lit panes read there as only a faint warm tint.

## Geometry and materials

- Object count: **17 mesh objects**
- Triangle count: **13,380** (the night state cost 542)
- Dimensions: **[124.7346, 98.395, 99.06] m**
- Bounding box: min **[−62.3673, −49.1975, 0.0]**, max **[62.3673, 49.1975, 99.06]**
- Minimum Z: **0.0 m**; XY centre offset **[0.0, 0.0] m**
- Materials: `Toy_cream`, `Toy_glass`, `Toy_gold_Glow`, `Toy_ink`, `Toy_mint`,
  `Toy_mustard`, `Toy_red`, `Toy_roofd`, `Toy_sand`, `Toy_sky`, `Toy_steel`,
  `Toy_stone`, `Toy_teal`, `Toy_trim`, `Toy_white_Glow`

The 124.7 × 98.3 m axis-aligned bounds exceed the 117.9 × 84.1 m facade-aligned
footprint because the composition carries its true 9.05° yaw and the Mason
porte-cochère projects west of the block face.

## Visual design

The miniature preserves the five cues ranked in `REFERENCE.md`: the pale
symmetrical block on the hill, the porte-cochère with its arc of international
flags, the crested cornice with corner parapets and rooftop flags, the regular
window grid with its giant centre colonnade, and the plain picket-crowned tower
standing east of the block.

Per `docs/styles/miniature-toy.md` §22 and §26, roughly 200 ornamented windows
became one clean recessed grid, all classical ornament collapsed into three
horizontals (grooved base, string course, cornice), and the tower's curtain wall
became seven recessed glass strips crossed by floor bands grouped one per two
storeys so the rhythm survives the city camera. The colonnade, flags and
entrance openings are semantically enlarged (§9).

The roof was designed as a second facade (§10): the mapped interior courtyard
carries a garden terrace one storey below the roof deck — legible from the
app's downward camera rather than reading as a 20 m shaft — with lawn, pool,
hedge blocks, three penthouse volumes with light caps, two mechanical clusters,
planters and the two rooftop flagpoles.

The night state is described in its own section above.

The four elevations share one camera rig — same orthographic scale, 1500 × 1200
resolution, camera height, warm tabletop lighting, exposure and projection —
differing only in azimuth. The aerial uses a 40° downward, 105 mm restrained-
perspective camera per style bible §18.

## Draft manifest entry (not applied)

```json
{
  "id": "fairmont",
  "file": "fairmont-san-francisco.glb",
  "anchor": [
    -122.4100666,
    37.7924244
  ],
  "targetHeightM": 99.06,
  "cat": 7,
  "name": "Fairmont San Francisco",
  "estimated": false,
  "dims": [
    124.7346,
    98.395,
    99.06
  ],
  "tris": 13380
}
```

Two values differ from the plan's draft, both deliberately:

- **`anchor`** is the centre of the exported composition, not the OSM relation
  centroid. The build recentres the model's bounding box, which sits 8.267 m
  east and 7.633 m north of the mapped centroid `-122.4101606, 37.7924935`;
  placing the asset at the raw centroid would offset it by ~11 m. The build
  script prints this anchor on every run, so it stays correct if the massing
  changes.
- **`targetHeightM` is 99.06**, the published architectural height of the
  tower, which is the asset's tallest point — so the loader's
  `targetHeightM / measuredHeight` scale is exactly 1.0. The plan's rounded 99
  would shrink the asset by 0.06%.

`estimated: false` is justified: the anchor derives from measured OSM geometry
and the height from the published tower figure. Note that the historic block's
~33 m is an *estimate* (see `REFERENCE.md`) — it is not what the manifest
depends on, but any future block-only variant must be marked estimated.

## Scope confirmation

The GLB contains only the hotel complex: the 1907 block with its porte-cochère,
colonnade, cornice, parapets, roof garden and penthouses; the ballroom podium;
and the 1961/62 tower. No Huntington Park, Grace Cathedral, Mark Hopkins,
California or Mason Street, cable car line, terrain, trees, people, vehicles,
plinth, camera or light is present. The studio floor and lights exist only
inside the render process and are never exported — confirmed by the re-import
object count of 307 meshes and zero cameras/lights.

See `OPTIMIZATION.md`: this GLB is the size-optimized build (geometry-identical; objects joined per material). Figures above reflect the shipped file.
