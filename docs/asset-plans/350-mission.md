# 350 Mission Street (Salesforce East) — SF-SIM asset plan

A 30-storey blue glass office tower (SOM, 2015) on the Mission × Fremont corner, the
first of the three Salesforce buildings around the Transit Center. Its facade panels are
canted so the glass reads as a shimmering pixel pattern. It stands on a very tall,
see-through lobby with a giant LED media wall inside. In the miniature it is the
compact, glassy "little sister" next to Salesforce Tower and Millennium Tower.

**Deliverable:** `artifacts/350-mission/`. Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `350-mission` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3967200, 37.7908720` (OSM OBB centre via `tk.run`) |
| Target height | **129.0 m** roof (Wikipedia 424 ft, published). No LiDAR: the 2010 survey predates the 2015 tower |
| Footprint | OSM way 226514310: OBB 39.4 × 37.2 m, 1,459 m², 5 nodes, long axis bearing 135.0° |
| Triangle cap | 27,000 (built: 3,048) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`, as used by `555-california`, `4-embarcadero-center`) |

---

## Part 1 — Task prompt

````markdown
# Create the 350 Mission Street (Salesforce East) GLB for SF-SIM

Work in artifacts/350-mission/. Read AGENTS.md, docs/styles/miniature-toy.md and
tools/landmark-kit/toykit.py first; Part 2 of this plan is your research start.

Must capture: a near-square blue glass prism on the OSM heading; a tall (~17 m),
light, see-through lobby under a thin steel transfer band; two-tone blue banding
standing in for the canted pixel panels; a glass crown screen hiding a roof plant;
the LED media wall and the blue Salesforce cloud on the Mission (SE) face.

Contract: binary GLB, metres, +Y = true north, origin at base centre, min Z 0, crest
exactly 129.0 m, flat Toy_* materials, `_Glow` only as outward skins, no degenerate
triangles, <= 27,000 tris (aim for under 6,000). Build with
`tk.run(SLUG, build, HERE, (-122.396720, 37.790872), 129.0)`.

Run build -> kit validate.py (--height 129 --anchor <tk.run anchor>, "all checks
pass") -> kit render.py. Write REFERENCE.md and REPORT.md. Do not edit the manifest,
landmarks.mjs or app code.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 129 m (424 ft) | published (Wikipedia infobox, CTBUH 2929) |
| Floors / year / architect | 30 / 2015 / Skidmore, Owings & Merrill | published |
| Floor area | 455,350 sq ft | published (Kilroy Realty) |
| Footprint | OBB 39.4 × 37.2 m, 1,459 m², 5 nodes | measured (OSM) |
| Heading | long axis 135.0° (along Mission St) | measured (OSM) |
| OSM tags | `height=129`, `building:levels=27` | OSM (levels disagree with the published 30) |
| Lobby height ≈ 17 m | | estimated (photo: the base glass spans about four office floors) |
| DataSF LiDAR | none | the 2010 survey predates construction |

### 2.2 Sources

- OSM way 226514310 — https://www.openstreetmap.org/way/226514310
- DataSF footprints + 2010 LiDAR — https://data.sf.gov/resource/ynuv-fyni (no record for this tower)
- Wikipedia — https://en.wikipedia.org/wiki/350_Mission_Street
- CTBUH — https://www.skyscrapercenter.com/building/350-mission/2929 (via the Wikipedia infobox)
- Commons photo (Wikipedia lead image) — https://commons.wikimedia.org/wiki/File:Salesforce_East_2021.jpg

### 2.3 Orientation

Square-ish plan, long axis 135° (NW–SE). Model yaw = 90 − 135 = −45°; +Y = true north.
Local +x faces 135° = **Mission St (SE)**; local −y faces 225° = **Fremont St (SW)**; the
Mission × Fremont corner (where the photo is taken) is the south corner. Wikipedia
calls this the "northeast corner of Fremont and Mission" in street-grid terms; the
coordinates agree (Salesforce Tower sits across both streets to the SSW).

### 2.4 What each side shows

- SE (Mission) and SW (Fremont): the photographed faces — canted blue glass over the
  tall clear lobby; the Salesforce cloud on the shaft near the corner (photo).
- NE and NW: party sides toward 45 Fremont and the Blue Shield building; same glass
  skin assumed (**inferred**, not photographed).
- LED media wall: inside the lobby behind the glass (published widely; its exact face
  is **inferred** as Mission).

### 2.5 Recognition cues

1. A compact, almost cubic blue glass prism, darker and bluer than its neighbours.
2. The tall see-through lobby that makes the shaft look lifted.
3. The shimmering canted-panel texture (two-tone banding in the miniature).
4. The Salesforce cloud and the glowing media wall at street level.

### 2.7 Massing recipe

- Plan `tk.rect(38.5, 36.5)` on yaw −45°.
- Lobby 0–17 m: `Toy_glassl` prism inset 1.2 m, steel mullions 0.6 m proud of it, a
  `Toy_sand_Glow` ring behind them; LED screen (`Toy_sky` + `Toy_sky_Glow`) on the
  Mission face.
- Steel transfer band 17–18.2 m.
- Shaft 18.2–124.5 m: `tk.shaft` with 25 whole storey-groups (4.25 m), `Toy_glass`
  with `Toy_glassl` bands and fins every 4.6 m; lit panes aligned to the fin bays.
- Crown 124.5–129 m: glass screen ring, roof deck, plant, `Toy_white_Glow` crown line.
- Cloud (three `Toy_sky` lobes, ~10 m wide) on the Mission face at 22 m; stone apron,
  three street trees on Fremont.

### 2.8 Palette

`Toy_glass`, `Toy_glassl`, `Toy_steel`, `Toy_sky`, `Toy_roofd`, `Toy_stone`, `Toy_leaf`,
`Toy_leafd`, `Toy_rust` (trunks); glow `Toy_sand_Glow`, `Toy_sky_Glow`, `Toy_white_Glow`.
All core palette.

### 2.9 Roof

A glass screen ring around a dark deck with a tidy plant cluster; the crown light line
outlines it at night. Not blank from the aerial camera.

### 2.11 Triangle budget

3,048 tris (body 2,556, night glow 492). Deliberately lean; nothing to cut.

### 2.12 Draft manifest entry

```json
{
  "id": "350-mission",
  "file": "350-mission.glb",
  "anchor": [-122.39672, 37.790872],
  "targetHeightM": 129,
  "cat": 3,
  "name": "350 Mission Street (Salesforce East)",
  "estimated": false,
  "dims": [61.3769, 61.3769, 129.0],
  "tris": 3048
}
```

```js
{ id: '350Mission', name: '350 Mission Street (Salesforce East)', lon: -122.39672, lat: 37.790872,
  height: 129, exclude: 22, camera: { distance: 420, yaw: 200, pitch: 20 } }
```

### 2.13 Integration notes

Case B: registry entry, exclusion, batch re-bake. The OBB half-diagonal is ≈ 27 m, but
45 Fremont's centroid is ≈ 55 m away and the Blue Shield building abuts on the NE, so
keep the radius ~22 m and confirm at bake time that only this footprint is cleared.
`dims` is the axis-aligned box of the 45°-rotated plan plus the 3 m apron. Load radius:
none (skyline tower).

### 2.15 Open risks

- Lobby height (17 m) is read from the photo, not published.
- The LED wall's face is inferred; it is shown outside the glass as a screen because
  the model's opaque glass would hide an interior wall (a deliberate toy liberty).
- OSM says 27 levels, Wikipedia 30; the height (129 m) is what matters to the loader.
- The canted "pixel" panels are only suggested by banding; a closer look would need
  per-panel geometry, which is not worth the triangles.
