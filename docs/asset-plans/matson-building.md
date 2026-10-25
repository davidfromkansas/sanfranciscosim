# Matson Building (215 Market Street) — SF-SIM asset plan

The Matson Navigation Company's 1922–24 headquarters on the Market/Main corner: sixteen
storeys of cream terracotta by Bliss & Faville, composed as a classical column — an
ornate two-storey arcaded base with a tall central entrance arch on Market, a plain
punched shaft, and an ornate capital of paired arched windows under a deep bracketed
cornice, with a small arcaded penthouse on the roof. It is the twin of the PG&E General
Office Building next door (`pge-general-office`), and the pair should read as one
matched Beaux-Arts frontage among the 1960s–80s towers of the Transbay batch.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/matson-building/`. Part 1 is the runnable task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `matson-building` |
| Existing procedural builder | none — new landmark, Case B (needs a `pipeline/lib/landmarks.mjs` entry, an exclusion and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3965080, 37.7926550` (OSM OBB centre, from `tk.run`) |
| Target height | **73.0 m — ESTIMATED** (16 storeys + cornice + penthouse; no published or measurable height, see 2.1) |
| Footprint | 44.7 x 42.5 m OBB, edges at bearing 135.4° / 45.4°; 1,864 m² measured from OSM way 1279504249 |
| Triangle cap | 12,000 (built: 4114) |
| Category | `3` (office — same as `1-market`, `555-california`, `columbus-tower`) |

---

## Part 1 — Task prompt

````markdown
# Create a production-ready Matson Building GLB for SF-SIM

Work in the sanfranciscosim repo, BATCH mode (docs/asset-pipeline/ADDRESS-TO-ASSET.md).
Build a stylized miniature of the Matson Building, 215 Market Street, San Francisco,
with the shared kit in tools/landmark-kit/ (toykit.py, validate.py, render.py).

Must capture: the three-part "column" (arcaded base, plain punched shaft, arched top
storey under a deep cornice); the tall entrance arch centred on the Market (NW) face;
cream terracotta throughout; the small arcaded rooftop penthouse; lit windows at night.

Contract: metres, Z up, +Y north, base centre at origin, crest exactly 73.0 m, flat
Toy_* materials only, _Glow as thin skins over solid faces, <= 12,000 triangles.
Run build -> validate (must print "all checks pass") -> render; write REFERENCE.md and
REPORT.md in artifacts/matson-building/. Do not integrate.
````

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Basis |
|---|---|---|
| Address / use | 215 Market St; Matson Navigation Co. HQ, offices | published (Wikipedia, NRHP) |
| Architect, dates | Bliss & Faville, 1922–24; matching annex 1945–47 | published (Wikipedia) |
| Storeys | 16 | published (Wikipedia, NRHP summary, Structurae, SKYDB) |
| Style / cladding | Renaissance Revival, terra cotta, "column-like" three sections | published (Wikipedia) |
| NRHP | listed 29 Nov 1995, ref 95001384 | published |
| Footprint | 44.7 x 42.5 m, 1,864 m², near-square, edges 135.4° / 45.4° | measured (OSM way 1279504249) |
| Height | **73.0 m** | **estimated** — see below |

**Height.** No source found gives the Matson Building's height. Wikipedia, Structurae and
SKYDB give only 16 floors. The CTBUH entry "215-245 Market Street" (93.5 m, 18 floors,
completed 1925, "PG&E Headquarters") is the neighbouring PG&E General Office, not Matson.
OSM `height=83` is unsourced. The DataSF 2010 LiDAR footprint covering Matson
(`201006.0000581`, mblr SF3711014A) merges the tower with the annex and the plaza to the
south-east (max 94.69 m, majority 6.07 m), so its maximum cannot be attributed to the
tower. A direct DataSF query (intersects a box around the anchor, 2026-10-25) returned no
separate Matson footprint. The 73.0 m estimate scales the twin: PG&E's 17 storeys measure
79.8 m to the crest (LiDAR), ~4.2 m a storey with a double-height base, giving ~70 m to
the Matson balustrade and ~73 m to the penthouse cornice. The manifest entry is therefore
`"estimated": true`.

### 2.2 Sources

- OSM way 1279504249 — https://www.openstreetmap.org/way/1279504249 (annex: way 260291407)
- DataSF Building Footprints (2010 LiDAR), https://data.sf.gov/resource/ynuv-fyni — record `201006.0000581` (merged, unusable for height)
- Wikipedia, "Matson Building" — https://en.wikipedia.org/wiki/Matson_Building
- Commons photo (infobox lead image): File:Matson Building & Annex (San Francisco).jpg — Market facade from street level
- CTBUH "215-245 Market Street" — https://www.skyscrapercenter.com/building/215-245-market-street/26532 (PG&E, used only to rule out)
- Structurae / SKYDB entries (16 floors only)

### 2.3 Orientation

Authored true-world (+Y north). The plan is a near-square rotated 45°: local +X runs to
bearing 135.4° (SE), local +Y to 45.4° (NE). Faces: **NW = Market Street** (local −X,
hero), NE = Main Street, SW = party wall to PG&E (`pge-general-office`), SE = the annex.

### 2.4 What each side shows

- **NW, Market (photo):** two-storey base of tall arched openings between fluted pilasters,
  a grand central arch over the entrance, a frieze; twelve-plus bays of plain punched
  windows; an ornate band, the top storey of paired round-headed windows; bracketed
  cornice; balustrade; a small arcaded penthouse visible above.
- **NE, Main:** inferred to repeat the Market treatment without the grand arch (corner
  building; photo shows the return of the top arches).
- **SW / SE:** inferred plainer — SW abuts PG&E across a light court, SE meets the annex.
  The model treats all four faces alike except the portal (a toy simplification).

### 2.5 Recognition cues (ranked)

1. Cream terracotta block, the same height and colour as its PG&E twin.
2. Three-part column: arcaded base / plain shaft / arched capital storey.
3. Deep cornice with balustrade — a heavy lid, unlike the glass towers around it.
4. Tall central entrance arch on Market.
5. Small arcaded penthouse on the roof.

### 2.7 Massing recipe

- Base: 43.5 x 41.5 m terracotta prism 0–11 m, arcade of 3.0 m arches at 4.6 m pitch on
  every face, cream cornice at 11 m.
- Portal: cream frame 9 x 1.2 m standing proud of the NW face to 12.5 m, 6.2 m arch.
- Shaft: cream punched block 12–62 m, 3.85 m storeys, 2.8 m window pitch.
- Capital: terracotta band at 62 m, terracotta top storey 62.4–68 m with 1.9 m arched
  windows at 2.8 m, cream cornice 68–70 m projecting 1.6 m, balustrade to 71.4 m.
- Roof: dark deck at 70 m, penthouse 10 x 18 m (long axis parallel to Market) set toward
  Market, arched windows, cornice to 73.0 m; one small plant cluster to the SE.

### 2.8 Palette

`Toy_cream` (shaft, portal, cornices), `Toy_terracotta` (base, capital, balustrade —
off-palette warm cream, documented), `Toy_glassd` (windows), `Toy_roofd`, `Toy_steel`
(plant), `Toy_stone` (plinth), `Toy_sand_Glow` (night windows, arches, portal).

### 2.9 Roof

Dark deck inside the balustrade, the cream arcaded penthouse and a two-box plant cluster.
Penthouse position is inferred from the street photo (it sits behind the Market cornice).

### 2.11 Triangle budget

Cap 12,000; the build lands at 4114. Punched windows are the bulk; nothing to cut.

### 2.12 Draft manifest entry

```json
{
  "id": "matson-building",
  "file": "matson-building.glb",
  "anchor": [-122.396508, 37.792655],
  "targetHeightM": 73.0,
  "cat": 3,
  "name": "Matson Building",
  "estimated": true,
  "dims": [68.4374, 68.4571, 73.0],
  "tris": 4114
}
```

### 2.13 Integration notes

- **Case B, new landmark**: needs a `pipeline/lib/landmarks.mjs` entry, an exclusion and a
  re-bake. The exclusion must remove the Matson tower ring but **keep the Matson annex
  (OSM 260291407)** and the PG&E GLB's neighbour rings; the plan half-diagonal (~31 m)
  reaches the PG&E footprint, so measure the safe window against OSM, DataSF and Overture
  rings before choosing a radius (DataSF merges tower + annex into one ring here — the
  `sf3d-exclusion-two-rings` trap).
- Integrate together with `pge-general-office`; judge the pair side by side on Market.
- `loadRadius`: default `max(2500, 73 x 30) = 2500`.

### 2.15 Open risks

1. **Height is an estimate** (73.0 m). If a survey or published figure appears, rebuild
   with `H_TOP` changed; the capital and penthouse scale with it.
2. NE/SW/SE elevations are inferred; only the Market face is photographed here.
3. Penthouse size and position are read from one street-level photo.
4. Rooftop elements on the merged LiDAR footprint (94.7 m max) are unexplained.
