# 140 New Montgomery (Pacific Telephone Building) — SF-SIM asset plan

San Francisco's first skyscraper south of Market (Miller & Pflueger, 1925), the Pacific Telephone & Telegraph headquarters: a 26-storey Art Deco tower of mottled pale grey terracotta on an L-shaped plan, unbroken vertical piers, two stepped shoulders after Saarinen's Tribune Tower entry, a parapet of pinnacles and a small central lantern under the flagpole. In the miniature it is the pale ribbed ziggurat beside SFMOMA.

**Deliverable:** `artifacts/140-new-montgomery-street/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `140-new-montgomery-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4000285, 37.7866863` (from `tk.run`, OSM OBB centre + recentre shift) |
| Target height | **132.7 m** — published architectural top 132.7 m (Wikipedia; roof 132.6 m, tip/flagpole 140.2 m not modelled); DataSF LiDAR max 137.6 m (flagpole), majority 116.1 m = main roof |
| Footprint | OSM way 80296766: 21 nodes, 1,434 m², L-shaped, OBB 48.9 × 44.8 m, bearing 134.7°; simplified to its 7-node L |
| Triangle cap | 5,000 (built: 4,792) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Architectural top / roof / top floor | 132.7 / 132.6 / 125.9 m | published (Wikipedia) |
| Main parapet | 116.1 m | measured (LiDAR majority plane) |
| Floors / year / architects | 26 / 1925 / Miller & Pflueger (J. R. Miller, T. L. Pflueger) | published |
| Footprint | L, arms ≈ 14.6 m deep, bearing 134.7° | measured (OSM) |
| Setbacks at ≈ 66 m and ≈ 91 m; lantern 9 × 8 m |  | inferred (photo) |

### Sources

- OSM way 80296766 — https://www.openstreetmap.org/way/80296766
- Wikipedia — https://en.wikipedia.org/wiki/140_New_Montgomery
- Commons photo — https://commons.wikimedia.org/wiki/File:140_New_Montgomery_from_Salesforce_Park.jpg (April 2021, from the east)
- DataSF footprints / 2010 LiDAR — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Footprint used directly; yaw −44.7° (bearing 134.7°, along New Montgomery). The L's long NE face fronts New Montgomery St; the NW arm runs toward Minna/Natoma; the inner corner opens SW toward SFMOMA. +Y = true north.

### What each side shows

- NE (New Montgomery): the photographed face — piers, two symmetric shoulders, pinnacled parapet, central lantern.
- NW and SE ends: same piers and setbacks (photo shows the shoulders in profile).
- Inner (court) faces: same skin assumed (**inferred**).

### Recognition cues (ranked)

1. Pale grey ribbed Art Deco verticality.
2. Stepped shoulders (ziggurat silhouette).
3. Pinnacled parapet and small central lantern.
4. L-shaped plan read from above.

### Massing recipe

- Plan = OSM L simplified to 7 nodes.
- 0–10 m stone base with dark shopfront glass; band to 11 m.
- 11–66 m, 66.8–91 m, 91.8–116 m: three `tk.shaft` sections (7/3/3 two-storey groups) of `Toy_glassd` with `Toy_stone` spandrels and `Toy_white` piers every 3.6 m, each stepping in (offset −3.0, −4.8 m); lit panes cut per storey.
- Parapet ring 116–117.6 m with `Toy_white` pinnacles every ~7 m.
- Lantern 9 × 8 m over the New Montgomery arm to 130.7 m, crown ring to 132.7 m, white light line.

### Palette

`Toy_white`, `Toy_stone`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`; glow `Toy_sand_Glow`, `Toy_white_Glow`.

### Roof

Dark decks on each setback; pinnacled parapet; a hollow lantern crown; small plant cluster on the main roof.

### Triangle budget

4,792 tris (body 3,986, night glow 806) against a 5,000 cap.

### Draft manifest entry

```json
{"id": "140-new-montgomery-street", "file": "140-new-montgomery-street.glb", "anchor": [-122.4000285, 37.7866863], "targetHeightM": 132.7, "cat": 3, "name": "140 New Montgomery (Pacific Telephone Building)", "estimated": false, "dims": [74.6329, 59.8669, 132.7], "tris": 4792, "loadRadius": 3981}
```

### Integration notes

Case B. Tight lot beside SFMOMA's expansion and the St. Regis; clear only this L footprint (the OBB half-diagonal is ~33 m, but the court is open to the SW—check SFMOMA survives). loadRadius 3,981 m.

### Open risks

- Setback heights are read from one frontal photo (perspective).
- The light-court notches of the OSM outline are dropped; the inner edge of the L is a straight diagonal.
- Lantern position (over the New Montgomery arm) is inferred; the 7.5 m flagpole is omitted.
