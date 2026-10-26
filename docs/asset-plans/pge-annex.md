# PG&E General Office Building Annex — SF-SIM asset plan

The 1945 annex of the PG&E General Office Building (Bakewell & Brown, 245 Market Street), built behind the 1925 tower on Beale Street and designed to match it. It is part of the NRHP listing "Pacific Gas and Electric Company General Office Building and Annex". The miniature copies the general office's cream terracotta palette, arcaded base, punched shaft and cornice (artifacts/pge-general-office/).

**Deliverable:** `artifacts/pge-annex/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `pge-annex` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3965063, 37.7921155` (from `tk.run`: OSM OBB centre + recentre shift) |
| Target height | **55.8 m** — DataSF 2010 LiDAR max of ring 201006.0003729, which covers the annex footprint (measured). The facts file's 83 m is the OSM `height=83` tag, which is taller than the 79.8 m general office and inconsistent with the annex's 13 storeys (`building:levels=13` ≈ 52–56 m); rejected |
| Footprint | OSM way 260291406: 8 nodes (4 collinear, dropped), 1,715 m², OBB 42.2 × 40.9 m, bearing 45° |
| Triangle cap | 3,000 (built: 2,200) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest | 55.8 m | measured (LiDAR ring max); consistent with 13 storeys |
| Storeys | 13 | OSM `building:levels` |
| Year / architects | 1945 / Bakewell & Brown (designed to match the 1925 building) | published (Wikipedia, NRHP) |
| Footprint | 42.2 × 40.9 m, 1,715 m² | measured (OSM) |
| Cladding, base, cornice | match the general office | inferred (NRHP text), not photographed |

### Sources

- OSM way 260291406 — https://www.openstreetmap.org/way/260291406
- Wikipedia — https://en.wikipedia.org/wiki/Pacific_Gas_and_Electric_Company_General_Office_Building_and_Annex
- Commons photo of the main building (annex not visible) — https://commons.wikimedia.org/wiki/File:Pacific_Gas_and_Electric_Co._General_Office_Building_full_view.JPG
- DataSF 2010 LiDAR rings 201006.0003729 / 0000848 / 0000581 (all mblr SF3711014A) — https://data.sf.gov/resource/ynuv-fyni
- Lead's existing landmark: artifacts/pge-general-office/ and docs/asset-plans/pge-general-office.md

### Orientation

Plan rotated 45° like the general office. NW face = party wall with the 1925 tower (no windows modelled); SW = Beale Street; SE toward 77 Beale's plaza; NE toward the Matson annex.

### What each side shows

- SW (Beale), SE, NE: cream terracotta, arcaded base, punched shaft — **inferred** from the NRHP description; no photo of the annex was found.
- NW: hidden party wall against the general office (it is lower than the 1925 tower).

### Recognition cues (ranked)

1. Same cream terracotta and arcaded base as the general office, a storey-height lower block behind it.
2. Terracotta cornice and balustrade with a set-back attic.
3. Punched-window grid at the general office's storey pitch.

### Massing recipe

- 0–9 m `Toy_terracotta` base, round arches at 5.4 m (as pge-general-office), lit; cream cornice.
- 9.9–48.6 m `tk.punched_block`: 10 storeys at 3.87 m, `Toy_cream`, panes at 2.9 m (general office spacing).
- 48.6–50 m terracotta cornice + balustrade; attic inset 2 m to 53.6 m; attic cornice; deck and low plant to 55.8 m.
- Party face (NW) gets no windows.

### Palette

`Toy_cream`, `Toy_terracotta`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, `Toy_stone`; glow `Toy_sand_Glow`. Same set as pge-general-office (terracotta off-palette, documented there).

### Roof

Set-back attic with a dark deck and a low plant cluster; the balustrade rings the main roof.

### Triangle budget

2,200 tris (body 1,862, night glow 338) against a 3,000 cap.

### Draft manifest entry

```json
{"id": "pge-annex", "file": "pge-annex.glb", "anchor": [-122.3965063, 37.7921155], "targetHeightM": 55.8, "cat": 3, "name": "PG&E General Office Building Annex", "estimated": false, "dims": [65.7542, 65.3062, 55.8], "tris": 2200, "loadRadius": 2500}
```

### Integration notes

Case B. The DataSF ring for the 1925 tower (201006.0000848) also covers part of the annex, so exclude by this OSM way only, radius ~24 m, and confirm pge-general-office, Matson and 77 Beale survive. loadRadius 2,500 m.

### Open risks

- **No photograph of the annex**: every facade is inferred from "designed to match". If the annex is plainer (likely for 1945), the arcade and balustrade overstate it.
- Height rests on one LiDAR ring statistic (max 55.8 m); the ring is small and its median (18.9 m) shows it also covers low structures.
- OSM footprint touches the general office's footprint along the NW face (≈0.5 m overlap).
