# San Francisco Civic Center Courthouse — build report

A stylized miniature of 400 McAllister Street for SF-SIM, produced by running
`docs/asset-pipeline/ADDRESS-TO-ASSET.md` end to end on
`BUILDING: San Francisco Superior Courthouse, 400 McAllister St`.

Where this report and `docs/asset-plans/civic-center-courthouse.md` disagree, **this
report is correct** — it records what was actually built and measured.

## Files

| File | What it is |
|---|---|
| `build_civic_center_courthouse.py` | Deterministic Blender build; `blender -b --python …` rebuilds the GLB byte-for-byte |
| `render_civic_center_courthouse.py` | Controlled review renders, always from the **exported** GLB |
| `validate_civic_center_courthouse.py` | Fresh-scene contract validation of the exported GLB |
| `make_contact_sheet.py` | Composes the eight review images |
| `civic-center-courthouse.glb` | The shipping asset |
| `civic-center-courthouse.blend` | Source scene |
| `validation.json` | Machine-readable contract report |
| `*-north/east/south/west/top/aerial/night/night-corner.png`, `*-contact-sheet.png` | Review renders |

## Validated result (fresh-scene re-import of the GLB)

| | |
|---|---|
| Overall | **PASS** (all 15 checks) |
| Objects / triangles | 164 / **4,712** (cap 22,000; repo hard gate 30,000) |
| Dimensions (world-aligned bbox) | 91.077 x 51.303 x **29.600** m |
| Footprint it represents | 83.46 x 36.98 m at 81.22° — the world-aligned bbox is larger because the building is rotated 8.78° off the world axes |
| min Z / XY centre | 0.0 m / (0.0, 0.0) |
| Materials | `Toy_stone`, `Toy_trim`, `Toy_white`, `Toy_glass`, `Toy_ink`, `Toy_roofd`, `Toy_steel`, `Toy_white_Glow`, `Toy_mustard_Glow` |
| Textures / transparency | 0 / 0 |
| Cameras / lights / animation / armatures / constraints | 0 / 0 / 0 / 0 / 0 |
| Transforms applied / negative scales | yes / none |
| Normals | PASS — per-object signed volume positive on every object; 22,500-ray visibility test within tolerance |
| Glow emission strength on ship | 0.0 (night-only, as the contract requires) |

## Orientation & placement

- Authored **world-true**: Blender `+Y` = true north, `+X` = east. The long axis bears
  **81.22° cw from true north**; the ceremonial front faces **south** onto McAllister
  Street, so the contract's "front faces −Y" rule is honoured to within 8.8°. No
  `yawDeg` override is needed.
- **Anchor after recentring: `-122.4192537, 37.7804897`.** This is 0.5 m east of the
  measured OBB centre (−122.4192590) because the exported model's bounding box is
  centred on geometry that includes the corner entrance canopy; the anchor that goes in
  the manifest must be the model's own origin, which is what the build script prints.
- Target height **29.6 m**, so `targetHeightM / measuredHeight = 29.6 / 29.6 = 1.000`.
  The build normalises the lantern crest to the verified height exactly, so the loader
  applies a scale of 1.0.

## Design decisions (vs the plan doc)

1. **Lantern raised clear of the parapet.** The plan put the corner attic at 23.6 m,
   below the 25.0 m parapet, which buried the drum's base and killed the one
   recognition cue that matters. The corner attic now tops out at 25.6 m and the drum
   runs 25.6–27.8 m, so the lantern starts in open air. Crest unchanged at 29.6 m.
2. **Drum radius 5.8 m, not the plan's 5.0.** The drum measures ~10.6 m across on z19
   imagery (circumradius ≈5.75); the plan called for a ~15 % exaggeration. 5.8 m is the
   measured value, and the *reading* is bought by (1) instead. Documented so the
   exaggeration is honest rather than accidental.
3. **Window counts compressed.** The architect's elevation shows ~20 square windows per
   base row and ~17 in the attic band. Built as 10 and 11. The real counts rendered as a
   checkerboard at the app's camera — the exact failure mode style bible §26 describes.
   Rhythm preserved, count reduced.
4. **Four ribbon bands on the north and west** rather than the study model's punched
   grid: same horizontal reading, a fraction of the geometry, and §5's "horizontal
   office bands" is the sanctioned language for it.
5. **The corner bay is three storey-height panes with trim mullions**, not one slab —
   as one slab it read as a floating navy rectangle.
6. **Roof designed, not left blank** (§10): parapet, a 27 x 8 m louvered penthouse with
   a dark deck, two mechanical clusters, a stair penthouse, three vents, a five-bay
   skylight run and two duct spines, laid out where z19 imagery shows plant.
7. **Palette.** `Toy_trim` (f3efe6) walls make this the coldest, lightest building of
   the Civic Center set, against the Opera House's `Toy_sand`. Judged from bright-sun
   photographs; the real granite may be greyer. Recorded as an artistic call.

## Corrections to the dossier made during the build

- **The lantern corner was ambiguous in the literature** (one source says "southeast
  entrance", another "corner of Polk and McAllister"). Resolved to the **south-east**
  corner: McAllister runs along the building's south side, Polk along its east, and
  three independent checks agree (OSM chamfer, satellite roof plan, architect's
  elevation). See `REFERENCE.md`.
- **OSM `height=25` is the parapet, not the crest.** The plan already said so; the 2010
  LiDAR median (24.67 m) confirms it, and `hgt_max` 29.60 m is the crest. Using the OSM
  tag as the target height would have made the building 16 % too short.

## Glow set (night)

| Material | Where | Role |
|---|---|---|
| `Toy_mustard_Glow` | 8 oculi in the drum | **Hero** — the lantern reads as a lit crown on a dark corner |
| `Toy_mustard_Glow` | panes behind the 5 McAllister and 2 Polk arches | Supporting rhythm |
| `Toy_white_Glow` | one strip under the corner entrance canopy | The floodlit entrance |

Every glow surface's day colour matches a non-glow palette neighbour, and all ship with
emission strength 0 — the app's dusk pass drives them.

## Approval (Gate 3)

Approved by David on 12 August 2026, verbatim:

> "Do it on a new branch and PR -- i approve all stages just proceed"

## Manifest entry (as integrated)

```json
{
  "id": "civic-center-courthouse",
  "file": "civic-center-courthouse.glb",
  "anchor": [-122.4192537, 37.7804897],
  "targetHeightM": 29.6,
  "cat": 18,
  "name": "Civic Center Courthouse",
  "estimated": false,
  "dims": [91.077, 51.303, 29.6],
  "tris": 4712,
  "loadRadius": 2500
}
```

**Streaming decision:** `loadRadius: 2500`. The default rule gives
`max(2500, 29.6 × 30) = 2500`. A 30 m building is illegible well before 2.5 km, and
because this is Case B the baked block underneath is carved out — beyond the radius the
site is empty ground, so the radius has to be generous enough that the absence never
enters frame. 2500 m is both the rule's answer and the right one.

**`estimated: false`** — the anchor and footprint are measured from OSM geometry and the
height from city LiDAR corroborated by an independent OSM survey. The crest is *derived*
rather than *published*; that limitation is recorded in `REFERENCE.md` rather than by
flagging the whole entry as estimated.

## Integration (Case B)

`camelId('civic-center-courthouse')` → `civicCenterCourthouse`, which did not exist in
`pipeline/lib/landmarks.mjs` or `app/src/landmarks.js`. Integration therefore added the
registry entry and re-baked the affected tiles. See the integration section of the PR.
