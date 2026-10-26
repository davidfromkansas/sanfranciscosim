# PG&E General Office Building (245 Market Street) — SF-SIM asset plan

Pacific Gas and Electric's 1923–25 headquarters on the Market/Beale corner, by Bakewell &
Brown: seventeen storeys of cream terracotta with an arcaded two-storey base, a plain
punched shaft, a row of tall arched windows, a deep cornice, and setbacks over the top
storeys. Its design deliberately matches the Matson Building next door
(`matson-building`); together they are the Beaux-Arts pair at the foot of the Transbay
towers.

**Deliverable:** validated miniature GLB plus dossier, renders and report under
`artifacts/pge-general-office/`. Part 1 is the runnable task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `pge-general-office` |
| Existing procedural builder | none — new landmark, Case B (needs a `pipeline/lib/landmarks.mjs` entry, an exclusion and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3968490, 37.7923850` (OSM OBB centre, from `tk.run`) |
| Target height | **79.8 m** — DataSF 2010 LiDAR crest 79.77 m (measured), footprint `201006.0000848` |
| Footprint | 44.1 x 42.4 m OBB, edges at bearing 135.3° / 45.3°; 1,851 m² measured from OSM way 1279504251 |
| Triangle cap | 12,000 (built: 3936) |
| Category | `3` (office — same as `1-market`, `555-california`, `columbus-tower`) |

---

## Part 1 — Task prompt

````markdown
# Create a production-ready PG&E General Office Building GLB for SF-SIM

Work in the sanfranciscosim repo, BATCH mode (docs/asset-pipeline/ADDRESS-TO-ASSET.md).
Build a stylized miniature of the PG&E General Office Building, 245 Market Street,
with the shared kit in tools/landmark-kit/.

Must capture: cream terracotta block matched to the Matson Building; arcaded base; plain
punched shaft; a row of tall arched windows near the top; deep cornice; attic storey
with balustrade; set-back top storeys; lit windows at night.

Contract: metres, Z up, +Y north, base centre at origin, crest exactly 79.8 m, flat
Toy_* materials, _Glow as thin skins, <= 12,000 triangles. Build -> validate ("all
checks pass") -> render; write REFERENCE.md and REPORT.md. Do not integrate.
````

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Basis |
|---|---|---|
| Address / use | 245 Market St; PG&E headquarters (to 2022), offices | published (Wikipedia) |
| Architect, dates | Bakewell & Brown, 1923–25; matching annex 1945 | published (Wikipedia, NRHP) |
| Storeys | 17 | published (Wikipedia) |
| Composition | arcaded first two storeys, plain shaft, multiple setbacks at the top four storeys, all terra cotta | published (Wikipedia/NRHP text) |
| NRHP | 29 Nov 1995, ref 95001385 | published |
| Footprint | 44.1 x 42.4 m, 1,851 m² | measured (OSM way 1279504251) |
| Crest | 79.77 m above ground | measured (DataSF LiDAR 2010, `201006.0000848` hgt_max) |
| Other LiDAR stats | median 58.39 m, majority 22.80 m | measured, but the ring also covers the annex to the south, so these are not this tower's roof planes |
| Conflicting figure | 93.5 m / 18 floors | published (CTBUH "215-245 Market Street", which lists a 2025 Hines / Pickard Chilton retrofit) — not used, see 2.15 |

### 2.2 Sources

- OSM way 1279504251 — https://www.openstreetmap.org/way/1279504251 (annex: way 260291406)
- DataSF Building Footprints (2010 LiDAR), https://data.sf.gov/resource/ynuv-fyni — record `201006.0000848`
- Wikipedia — https://en.wikipedia.org/wiki/Pacific_Gas_and_Electric_Company_General_Office_Building_and_Annex
- Commons photo (infobox): File:Pacific Gas and Electric Co. General Office Building full view.JPG — Market facade
- CTBUH — https://www.skyscrapercenter.com/building/215-245-market-street/26532

### 2.3 Orientation

Authored true-world (+Y north). Local +X runs to bearing 135.3° (SE), +Y to 45.3° (NE).
Faces: **NW = Market Street** (local −X, hero, street trees in front), SW = Beale Street,
NE = party side toward Matson, SE = the 1945 annex.

### 2.4 What each side shows

- **NW, Market (photo):** a two-storey arcaded base (largely hidden by street trees in the
  photo), a plain shaft of paired punched windows, a band of eight-plus tall round-arched
  windows two storeys high between pilasters, a deep cornice with urns and balustrade, and
  above it a set-back attic/top block with small windows.
- **SW, Beale:** inferred to repeat the Market composition (corner building).
- **NE / SE:** inferred plainer (light court toward Matson, annex). Modelled alike.

### 2.5 Recognition cues (ranked)

1. Cream terracotta block, matching Matson in height and colour.
2. The row of tall arched windows under a heavy cornice.
3. Stepped top: attic with balustrade, then a smaller set-back block.
4. Arcaded base on Market.

### 2.7 Massing recipe

- Base 43 x 41 m terracotta 0–10 m, 3.6 m arches at 5.4 m pitch, cream cornice.
- Shaft: cream punched block 11–60 m, 3.9 m storeys, 2.9 m pitch.
- Arched storey: band at 60 m, cream 60.5–67 m with 3.0 m arched windows at 4.6 m pitch.
- Terracotta cornice 67–68.6 m (1.2 m projection), balustrade band.
- Attic 40 x 38 m, 68.6–72.5 m, punched windows, parapet.
- Top block 30 x 28 m, 72.5–77 m, cornice to 78 m, plant cluster to 79.8 m.

### 2.8 Palette

`Toy_cream`, `Toy_terracotta` (off-palette, documented), `Toy_glassd`, `Toy_roofd`,
`Toy_steel`, `Toy_stone` (plinth), `Toy_leaf` (trees), `Toy_sand_Glow` (night windows and
arches).

### 2.9 Roof

Two stepped roof decks (attic terrace ring and top block) and one plant cluster on top;
LiDAR crest 79.8 m is taken to include the rooftop plant.

### 2.11 Triangle budget

Cap 12,000; the build lands at 3936.

### 2.12 Draft manifest entry

```json
{
  "id": "pge-general-office",
  "file": "pge-general-office.glb",
  "anchor": [-122.396849, 37.792385],
  "targetHeightM": 79.8,
  "cat": 3,
  "name": "PG&E General Office Building (245 Market Street)",
  "estimated": false,
  "dims": [67.7332, 67.748, 79.8],
  "tris": 3936
}
```

### 2.13 Integration notes

- **Case B, new landmark**: `pipeline/lib/landmarks.mjs` entry, exclusion, re-bake.
- The exclusion must remove the tower ring but keep the **annex (OSM 260291406)**; the
  DataSF ring `201006.0000848` merges tower and annex, so do not exclude on it blindly.
  Measure the safe window against OSM, DataSF and Overture rings (Matson's ring is ~42 m
  centre to centre away).
- Integrate together with `matson-building`; judge the pair on Market.
- `loadRadius`: default 2500.

### 2.15 Open risks

1. **CTBUH 93.5 m / 18 floors vs LiDAR 79.8 m.** The 2010 LiDAR predates the 2025
   retrofit CTBUH lists; if that retrofit added a rooftop storey, the crest may now be
   higher. Kept the measured value; revisit if a post-retrofit photo shows an addition.
2. Side and rear elevations are inferred.
3. Setback depths are read from one photo, not measured.
