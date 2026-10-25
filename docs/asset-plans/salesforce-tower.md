# Salesforce Tower — SF-SIM asset plan (v2 rebuild)

The tallest building in San Francisco and the anchor of the Transbay batch: a 326 m
rounded-square shaft of pale glass and white sunshades that tapers, rolls in at the
shoulders and ends in an open, perforated white crown carrying Jim Campbell's
"Day for Night" LED work. A v1 GLB has shipped since August 2026; this plan covers the
**v2 rebuild** to the batch standard (shared kit, pale skin, blunt crown, real entrance
faces). It replaces nothing but the GLB and its manifest numbers.

**Deliverable:** `artifacts/salesforce-tower/` (build script, GLB, renders, REFERENCE,
REPORT). Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `salesforce-tower` (already in the manifest) |
| Existing procedural builder | `salesforceTower` in `pipeline/lib/landmarks.mjs` — **Case A**, already replaced by the v1 GLB; v2 is a file swap |
| WGS84 anchor | `-122.3969300, 37.7897750` (OSM OBB centre via `tk.run`) |
| Target height | **326.0 m** architectural, crown rim (published, CTBUH / architect); roof ~297 m |
| Footprint | 54.5 × 54.1 m across the flats, rounded square, flats at 45°/135° (OSM way 431972186, 2,656 m²) |
| Triangle cap | 27,000 (built: 17,508) |
| Category | `3` (office) — the live entry's `16` (museum) should be corrected |

---

## Part 1 — Task prompt

````markdown
# Rebuild the Salesforce Tower GLB (v2) for SF-SIM

Work in artifacts/salesforce-tower/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first. Keep the v1 id, file name and 326 m height.

Must capture: the taper and shoulder roll-in to a BLUNT open crown (~55% of the base
width, not a point); the pale silvery skin with white horizontal sunshade bands; the
perforated white crown screen open at the top with the roof plant visible inside; the
LED crown floors as the night hero; lobby, canopies on Mission (NW face) and Fremont
(NE face) and the blue cloud by the Mission doors.

Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest
exactly 326.0 m, flat Toy_* materials (roughness 0.85), `_Glow` only as skins over
solid body, <= 27,000 tris, no textures/cameras/lights/animation. Build with
`tk.run(SLUG, build, HERE, (-122.396930, 37.789775), 326.0)`.

Run: build -> tools/landmark-kit/validate.py (--height 326 --anchor <tk.run anchor>,
must print "all checks pass") -> tools/landmark-kit/render.py (7 renders + contact
sheet). Write REFERENCE.md and REPORT.md (Gate 3 pending). Do not edit the manifest,
landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Architectural height | 326 m / 1,070 ft | published (CTBUH, Pelli Clarke & Partners) |
| Roof | ~296–297 m | published CTBUH roof; 297 used (estimated within band) |
| Floors / year | 61 / 2018 | published |
| Footprint | 54.5 × 54.1 m OBB, 2,656 m² | measured (OSM) |
| Heading | flats face 45/135/225/315° | measured (OSM OBB bearing 139.5°) |
| LED crown | six floors, ~11,000 LEDs | published (Campbell, owner) |
| Shoulder height ~215 m, rim ≈ 56% of base | | inferred (photographs) |
| LiDAR | none (2010 survey predates the tower) | — |

### 2.2 Sources

- OSM way 431972186 — https://www.openstreetmap.org/way/431972186
- CTBUH — https://www.skyscrapercenter.com/building/building/290
- Architect — https://pcparch.com/work/salesforce-tower
- Wikipedia — https://en.wikipedia.org/wiki/Salesforce_Tower
- Day for Night — https://www.jimcampbell.tv/portfolio/day-for-night
- Commons — https://commons.wikimedia.org/wiki/File:Salesforce_Tower_from_Sacramento_and_Davis_Street_2021.jpg ,
  https://commons.wikimedia.org/wiki/File:Salesforce_tower_facing_south.jpg
- DataSF footprints/LiDAR (https://data.sf.gov/resource/ynuv-fyni): no record usable (pre-construction).

### 2.3 Orientation

Rounded square rotated 44.6° (yaw) so its flats face the SoMa grid. Mission St = NW
face (315°), Fremont St = NE face (45°), First St = SW face (225°), Transit Center =
SE face (135°). Blender +Y = true north; the loader adds no rotation.

### 2.4 What each side shows

All four flats are the same curtain wall (glass + white sunshades) — published and
visible in every photo. Differences are at grade only: NW (Mission) has the main
entrance canopy and the cloud sign; NE (Fremont) a second entrance (inferred position);
SE faces the Transit Center bridge (not modelled — separate asset); SW is plain.

### 2.5 Recognition cues

1. Bullet silhouette with a blunt open top. 2. Pale silvery skin, white bands.
3. White perforated crown. 4. Glowing LED crown at night. 5. Mission entrance + cloud.

### 2.7 Massing recipe

- `half_width(z)`: 27.2 m at grade → 24.6 m at 215 m (power 1.15), then a
  quarter-ellipse roll-in to 15.2 m at 326 m. `corner_frac` 0.30 → 0.68.
- Shaft = one `tk.banded_loft` 15–297 m, pitch 8.3 m, band 1.15 m, 0.55 m proud.
- Crown = 11 hoops + vertical ribs 297–326 m, open top, cool glow skin inside.
- Roof deck at 297 m: 2 plant clusters, BMU + rail, four masts on a plinth.
- Lobby 0–15 m recessed 2.2 m behind white piers; canopies NW and NE; stone apron.

### 2.8 Palette

`Toy_glassg` shaft (documented off-palette extra), `Toy_white` bands/crown/piers,
`Toy_glassl` lobby, `Toy_roofd`/`Toy_steel` roof, `Toy_sky` cloud, `Toy_stone` apron,
`Toy_leaf`/`Toy_leafd` trees; glow: `Toy_white_Glow`, `Toy_sand_Glow`, `Toy_red_Glow`.

### 2.9 Roof

Designed for the downward camera: dark deck inside the white lattice, plant, BMU,
masts. Never a blank cap.

### 2.11 Triangle budget

17,508 total, of which the night-glow object is 1,648 faces; the shaft loft and the
crown lattice (11 hoops, 32 ribs) take most of the rest. Well under the 27,000 cap.

### 2.12 Draft manifest entry

```json
{
  "id": "salesforce-tower",
  "file": "salesforce-tower.glb",
  "anchor": [-122.39693, 37.789775],
  "targetHeightM": 326,
  "cat": 3,
  "name": "Salesforce Tower",
  "estimated": false,
  "dims": [78.9968, 78.9968, 326.0],
  "tris": 17508
}
```

### 2.13 Integration notes

Case A, already integrated: `assets.js` maps `salesforce-tower` to the baked
`salesforceTower` and hides the procedural tower on successful load; on failure the
procedural model stays (fallback). v2 needs no registry change and no re-bake — only
the GLB, `anchor`, `dims`, `tris` (and `cat`) in the manifest. The registry entry's
`exclude: 90` still covers the 79 m apron diagonal half-width (~56 m).

### 2.15 Open risks

- Shoulder height and rim width are photo-inferred; a published section would settle them.
- The 4.5 m stone apron widens `dims` to 79 m; harmless, but it overlaps the street
  edge on Mission/Fremont slightly at full scale.
- Changing `cat` from 16 to 3 alters the card/tone for this landmark in the app.
