# Ferry Station Post Office Building — build report

`artifacts/ferry-station-post-office/` — the miniature GLB of the **Agriculture
Building**, 101 The Embarcadero at Mission Street, San Francisco (A. A. Pyle,
1915; NRHP #78000756).

Built 18 August 2026 from `docs/asset-plans/ferry-station-post-office.md`.
**REPORT beats plan**: where this file and the plan disagree, this file and
`REFERENCE.md` §8 are right.

## Deliverables

| File | What |
|---|---|
| `build_ferry_station_post_office.py` | deterministic Blender build, world-space metres, Z up, +Y north |
| `ferry-station-post-office.blend` | the source scene |
| `ferry-station-post-office.glb` | **the shipping asset** |
| `render_ferry_station_post_office.py` | controlled review renders of the exported GLB |
| `validate_ferry_station_post_office.py` | fresh-scene contract validation |
| `make_contact_sheet.py` | the review montage |
| `validation.json` | machine-readable validation, `overall: PASS` |
| `REFERENCE.md` | the research dossier and every correction to the plan |
| `*-aerial/top/night/southwest/northwest/southeast/northeast.png`, `-contact-sheet.png` | review renders |

## Numbers

| | |
|---|---|
| Triangles | **11,596** of a 15,000 cap |
| Objects | 285 |
| Dimensions | 69.84 x 65.20 x **12.650** m |
| Bounding-box top | **12.650 m** — the clay-tile hip ridge |
| `targetHeightM / measuredHeight` | **1.000000** |
| min Z | 0.0 |
| XY centre offset | (−0.158, −0.253) m — the tile eave overhangs the front and both flanks but not the rear |
| Materials | `Toy_brick`, `Toy_rust`, `Toy_sand`, `Toy_stone`, `Toy_steel`, `Toy_ink`, `Toy_roofd`, `Toy_glass`, `Toy_gold`, `Toy_glassl_Glow`, `Toy_gold_Glow` — all on-palette |
| Glow groups | 2 (`Toy_gold_Glow` entrance hero, `Toy_glassl_Glow` scattered first-floor bays) |
| Textures / transparency / cameras / lights / animation | 0 / 0 / 0 / 0 / 0 |
| Normals | 0 objects with inverted signed volume; ray residual **0.0%** over 31,500 rays (gate 0.15%) |
| Anchor | −122.3921505, 37.7941368 |
| Frontage normal | 234.0° true; NW flank 324.3°, SE flank 144.3°, rear 54.0° |

## The heights it is built on

| Level | Value | Confidence |
|---|---|---|
| Clay-tile hip ridge | **12.65 m** | measured — DataSF LiDAR `hgt_maxcm`, corroborated by `peak_1st_m` − ground |
| Cornice / tile eave | **10.80 m** | measured — photogrammetric fit, 152 samples, rms 0.32°, ±0.3 m |
| Two-storey flat deck | 9.80 m | inferred — LiDAR median + the NRHP's 85 ft second-floor depth |
| SE wing ridge / eave | 11.05 / 9.90 m | estimated — see `REFERENCE.md` §8.6 |
| Work-room deck / parapet | 6.60 / 7.30 m | inferred — LiDAR mode + the Port's "one-story east portion" |
| Granite base | 1.00 m | measured off the rectified elevation |

## Dossier corrections made during the build

Five, all in `REFERENCE.md` §8, and three of them changed geometry:

1. The wharf bump-out is **not** an open concrete apron — the 1918/19 SE wing's
   tiled hip roof covers it out to 47.2 m with a hipped end. The apron the plan
   called for was removed.
2. The two-storey block runs 25.9 m deep only over the **middle** of the
   frontage (s 9.0–36.5); at both ends the work-room deck runs from the tile
   straight back to the bay. That is where the three roof monitors sit, and the
   plan had put them inside solid geometry.
3. The plan's "tile must be clearly darker than the brick" is backwards. The
   clay tile is the *lighter, more saturated* terracotta; the separation that
   works is brick / tile / light trim with the dark copper cornice between wall
   and roof.
4. Wikipedia's coordinates are ~90 m off in longitude. Not used.
5. OSM's `height=15 m` and `roof:shape=flat` are both wrong. Not used.

## Iteration log

| Pass | Change | Why |
|---|---|---|
| 1 | first build, 10,936 tris | massing from the plan |
| 2 | exact height normalisation added | bevelling the ridge shaved 12 mm; the loader scale must be 1.000 |
| 3 | two-storey mid block cut back to s 9.0–36.5; monitors and mechanical moved onto the deck that actually exists; deck materials split (`Toy_stone` mid / `Toy_steel` work room); shield panels and lozenges pushed proud of the pavilion faces; the three-bar "diamonds" replaced with a real lozenge on a recessed panel; cornice projection raised to 0.72 m and the eave overhang cut to 0.42 m so the copper cornice is not swallowed | the first top view showed the monitors buried inside the mid block, both decks reading as one grey mass, and no cornice line |
| 4 | mid block rebuilt as a solid to 9.80 m with its own parapet and coping, not a solid to 10.20 m | the mid deck was hidden under the block's own top face |
| 5 | end-pavilion doors recessed into a light reveal and shortened to 2.90 m; entrance glow widened to the full transom and a doorway glow added | the doors read as black slabs, and the night hero was a speck |

## Style judgement

Reviewed from the high three-quarter aerial first, as the style bible requires.
The building reads as a set of descending terraces with the tiled hip band as
the subject; the three-pavilion front survives at aerial distance because the
terracotta blocks are a full value step lighter than the brick; the roof carries
designed content (monitors, ducts, plant, the dark light-well slot) without
clutter, and nothing sits on the tile. Night state is one warm gold entrance
plus four scattered first-floor bays — restrained, and the glow plates are flat
and proud of opaque glazing, never shells.

It is deliberately quieter than the Ferry Building 150 m away: no crown, no
tower, no saturated accent beyond the small gold plaque over the doors.

## Approval

Gate 3 was carried by the session's standing instruction, quoted verbatim:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

— David, 18 August 2026, in the invocation of this pipeline run. No per-render
approval was solicited; the renders and this report are the record.

## Manifest draft

```json
{
  "id": "ferry-station-post-office",
  "file": "ferry-station-post-office.glb",
  "anchor": [
    -122.3921505,
    37.7941368
  ],
  "targetHeightM": 12.65,
  "cat": 18,
  "name": "Ferry Station Post Office Building (Agriculture Building)",
  "estimated": false,
  "dims": [
    69.84,
    65.2,
    12.65
  ],
  "tris": 11596,
  "loadRadius": 2500
}
```

## Gate 2 — PASS

`validation.json` `overall: PASS`, every check true, on a fresh-scene re-import
of the exported GLB.
