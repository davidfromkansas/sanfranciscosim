# Salesforce Transit Center (and Salesforce Park) — SF-SIM asset plan

The four-block-long bus terminal between Mission and Howard, Beale and Second, wrapped in a
rippling white perforated-aluminium skin and topped by Salesforce Park, a 2.2 ha rooftop
garden. From the app's aerial camera it is the single biggest green shape downtown and it sits
directly at the foot of Salesforce Tower, so it is the base the whole Transbay cluster stands on.
Today the procedural city shows it as a generic long low block.

**Deliverable:** a validated miniature GLB plus reference, renders and report under
`artifacts/transit-center/`. Part 1 is the task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `transit-center` |
| Existing procedural builder | none — new landmark, Case B (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3968739, 37.7891093` (OSM footprint OBB centre after recentering) |
| Target height | **30 m** to the gondola head-house roof (OSM `height`, estimated); park deck **21.3 m** (~70 ft, published); skin parapet 23.2 m (inferred) |
| Footprint | 436 m x 56 m along bearing 45.3°, 21,984 m2 (OSM way 542375290, simplified to 64 points) |
| Triangle cap | 27,000 (built: 6,780) |
| Category | `25` (transit_station, as the Ferry Building) |

---

## Part 1 — task prompt

Build `artifacts/transit-center/transit-center.glb` with `build_transit_center.py` (shared kit in
`tools/landmark-kit/`). One long scalloped volume: glazed street level 0–6 m, dark glazed bus-deck
body behind a white wavy skin from 4.5 m to 23.2 m, and the park on top at 21.3 m. The park must
read at aerial distance as green with lighter lawn ovals, two pale meandering paths, tree rows
along both edges, the light-column oculus, the amphitheatre and two small white pavilions.
Night: lit street level, skin glowing softly, the oculus and cafe lit. Validate at 30 m with the
anchor above; render the standard 7-view set.

## Part 2 — dossier

### 2.1 Verified facts
- Opened 2018, Pelli Clarke Pelli Architects; about 1,400 ft (430 m) long (published). Our OSM
  footprint measures 436 m along its axis (measured).
- Park level about 70 ft above the street (published); used as 21.3 m.
- Overall height 30 m from OSM `height` tag (estimated; it covers the pavilions/gondola top).
- The DataSF 2010 LiDAR predates the building, so no measured height exists.

### 2.2 Sources
- OSM way 542375290 (footprint, height tag) — https://www.openstreetmap.org/way/542375290
- Wikipedia: https://en.wikipedia.org/wiki/Salesforce_Transit_Center
- Salesforce Park: https://www.salesforcetransitcenter.com/salesforce-park/
- No Commons photo was fetched (rate-limited); the model follows the well-known aerial look.

### 2.3 Orientation
Long axis at bearing 45.3° (true), running south-west (Second St / bus ramp end) to north-east
(Beale St). The footprint already holds the skin's scallops, so the model is lofted straight from it.

### 2.4 What each side shows
- North-west and south-east (long sides): the white wavy skin over a glazed base; slot rows of
  perforation read as pale bands (simplified).
- Ends: same skin wrapping round. The bus ramp to the Bay Bridge (south-west end) is omitted.
- Street-level storefront detail is inferred.

### 2.5 Recognition cues (ranked)
1. The long green roof park with lawns and paths.
2. The rippling white skin.
3. The light column (glass oculus ringed in white).
4. The pavilions and the amphitheatre.

### 2.7 Massing recipe
`street_glass` prism 0–6 m (inset 3.5 m) → `body` dark glass 6–20.7 m (inset 2.6 m, no top) →
`skin` ring band 4.5–23.2 m on the outline → `park_soil` 20.7–21.3 m → lawns (`mint`), stone paths
of short box segments, `tree_row` x2, four tree clumps, oculus, four amphitheatre steps, cafe
(18 x 9 m) and gondola head house (10 x 8 m, to 30 m), sidewalk plinth.

### 2.8 Palette
`white` skin and roofs, `glassd`/`glassl` glazing, `steel` slots, `leaf` deck, `mint` lawns,
`leaf`/`leafd` trees, `stone` paths. Glow: `sand_Glow` street and cafe, `white_Glow` skin and oculus.

### 2.9 Roof
The roof is the park (see 2.7). No plant equipment.

### 2.11 Triangle budget
6,780 tris (25% of cap); paths and trees are most of it. Kept low for the shared vertex budget.

### 2.12 Draft manifest entry
```json
{ "id": "transit-center", "file": "transit-center.glb", "anchor": [-122.3968739, 37.7891093],
  "targetHeightM": 30, "cat": 25, "name": "Salesforce Transit Center", "estimated": true,
  "dims": [342.49, 340.32, 30], "tris": 6780, "loadRadius": 2500 }
```

### 2.13 Integration notes
Case B. The footprint is 436 m long and thin, so a single `exclude` radius cannot cover it
without wiping neighbours: use a centre `exclude` of ~30 m plus `extraExclusions` circles
(~30 m radius) every ~50 m along the axis. Its south-west half overlaps Salesforce Tower's 90 m
exclusion, which is fine (both remove procedural buildings only). Check that 425 Mission,
Salesforce Tower and 50/100 First keep their own buildings.

### 2.15 Open risks
- Height 30 m is OSM-estimated; the park level is the reliable number.
- The bus ramp and the street-level arcades are left out.
- The park layout is stylised (lawn ovals, path loop), not surveyed.
