# One Market Plaza — Spear Tower and Steuart Tower — SF-SIM asset plan

Welton Becket Associates, 1976: two white towers on a six-storey podium filling
the Mission Street half of the block at 1 Market Street. **Spear Tower**, 43
storeys and **172 m**, is the taller one and one of the pieces that makes the
Embarcadero skyline behind the Ferry Building; **Steuart Tower**, 27 storeys and
**111 m**, stands north-east of it across an elevated plaza. Both are the same
building in two sizes: a rectangular shaft with **canted corners**, wrapped in
**close-spaced white precast piers over dark recessed window slots** for their
whole height — no setbacks, no crown, no articulation at the top. The plaza
between them carries a **circular sunken garden** and a run of **glazed
barrel-vault canopies** over the retail below.

They are the third and fourth buildings of One Market Plaza. The first, the 1916
Southern Pacific Building, is a **separate asset on a separate branch**
(`docs/asset-plans/1-market.md`) and is explicitly out of scope here; so is the
glazed atrium in its courtyard, which that asset carries.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/one-market-plaza-towers/`.

| | |
|---|---|
| Manifest id | `one-market-plaza-towers` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3941803, 37.7933169` (envelope AABB centre, measured) |
| Target height | **177.6 m** (Spear Tower rooftop plant crest, LiDAR maximum); Spear roof **172.0 m**, Steuart roof **111.0 m**, podium **27.8 m** |
| Footprint | 7,521 m2 twelve-vertex envelope, AABB 120.7 x 126.5 m; Spear shaft 52.5 x 35.7 m, Steuart shaft 43.3 x 33.7 m |
| Triangle cap | 26,000 |
| Category | `3` (office) |
| Streaming | **resident — omit `loadRadius`** (see 2.13) |

---

## Part 1 — Task prompt

````markdown
# Create a production-ready One Market Plaza towers GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of **Spear Tower and Steuart Tower at One
Market Plaza**, San Francisco, with the six-storey podium and plaza they stand
on, and deliver it as a downloadable, validated GLB.

Do not integrate or deploy the model yet.

## Read the project sources first

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-miniature-style/SKILL.md`
5. `.agents/skills/sf-asset-check/SKILL.md`
6. `app/public/sf-assets/landmarks_manifest.json`
7. `artifacts/salesforce-tower/` — **the reference implementation.** The same
   problem at the same altitude of abstraction: a single tall office shaft that
   has to read as a skyline silhouette from kilometres away and still hold up at
   200 m. Its build script's shaft/mullion helpers are the skeleton to **adapt,
   not rewrite**. `artifacts/555-california/` is the secondary reference for a
   dark-slotted white tower.
8. `artifacts/1-market/` — the immediate neighbour, built in the same batch. Its
   `build_1_market.py` carries the footprint helpers (`poly_edge`,
   `offset_polygon`, `prism`, `ring_band`, `wall_box`, `uv_box`, `hip_roof`) and
   the shared-edge geometry the two assets must agree on.
9. `docs/asset-plans/one-market-plaza-towers.md` — this plan

## Must capture

- **Two white shafts of very different height on one podium** — 172 m and 111 m.
  The height contrast IS the composition; do not let the shorter one read as a
  stump or the taller one as a needle.
- **Canted corners on both shafts.** Each tower is a rectangle with its four
  corners cut, so it reads as an elongated octagon in plan and its silhouette
  has a soft chamfered edge instead of a hard 90 deg arris. This is the single
  most identifiable thing about them.
- **The pier rhythm**: close-spaced white precast piers running the FULL height
  of each shaft, unbroken from podium to roof, with dark recessed window slots
  between them. No spandrels, no horizontal banding, no crown. At miniature
  scale this is what makes them read as 1976 rather than as generic glass boxes.
- **The six-storey podium** filling the rest of the lot, in the same white
  language at a coarser rhythm, with a glazed retail level at plaza grade.
- **The elevated plaza between the towers**: the circular sunken garden, the run
  of glazed barrel-vault canopies, the paved deck.
- Designed roofs: light decks, parapets, plant enclosures on both towers (the
  taller Spear enclosure sets the 177.6 m crest).

## Research independently

Verify the dossier rather than trusting it. Re-check the architectural heights,
the two shaft footprints, the anchor and the real-world orientation. Gather
references for all four elevations of both towers, the plaza, and the roofs.

**Three source traps are already resolved in 2.1 — do not re-inherit them:**

1. **Steuart Tower has no footprint of its own in the DataSF survey.** It is
   inside the podium polygon (`mblr = SF3713007`, `sf16_bldgid`
   201006.0000212), whose `hgt_median` is the **podium's** 27.75 m. Its shaft
   footprint comes from OSM `way/132238431`, shifted into the DataSF frame.
2. **That podium polygon's LiDAR maximum is 163.58 m and is not Steuart Tower.**
   It is Spear Tower spilling over the shared boundary — the same artefact that
   put 114.92 m on the Southern Pacific Building's footprint next door.
3. **Floor counts disagree by one across sources** (Spear 42 or 43, Steuart 27
   or 28). The heights do not, and the heights are what the model needs.

## Scope

In: the podium, both shafts, the plaza and its garden and canopies, both roofs.

Out: **the Southern Pacific Building and the glazed atrium in its courtyard** —
those are `artifacts/1-market/`, built in the same batch, and the two assets abut
along the shared survey edge from `(3777.2, −2606.5)` to `(3814.4, −2569.9)` in
the app's local frame. Also out: Mission Street, Spear Street, Steuart Street,
Don Chee Way, the Embarcadero, street trees, vehicles, people.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full: binary `.glb`, real
metres, origin at base centre, min Z ~ 0, applied transforms, no negative scales,
outward normals, no textures, no transparency, flat `Toy_*` materials, `_Glow`
only where it lights at night, no `Toy_body`, no cameras/lights/animations, at
most **26,000** triangles.

**Orientation:** Blender `+Y` = true north, `+X` = east. The complex sits on the
45 deg downtown grid: the **Mission Street elevation faces south-east, 135.2 deg**;
the **Steuart Street / Don Chee Way elevation faces north-east, 45.2 deg**; the
north-west boundary is the shared edge with the Southern Pacific Building at
**315.2 deg**; the south-west return faces **225.2 deg**.

**Height normalization:** the tallest geometry (Spear Tower's plant cap) must
land at exactly **177.6 m**.

## Renders

`-top`, `-north`, `-east`, `-south`, `-west`, `-aerial`, `-aerial-night`, and a
contact sheet, all regenerated from the exported GLB. The **aerial** is the hero
here — place it low enough to see the height difference between the two shafts,
which a top view cannot show. The top view must show the plaza, the garden and
the two shaft footprints.

## Validate

Fresh-scene re-import of the exported GLB; write `validation.json` and
`REPORT.md`. The XY bounding box will be roughly **121 x 127 m** — that is the
45 deg envelope, not a scale error.

## Manifest draft

```json
{
  "id": "one-market-plaza-towers",
  "file": "one-market-plaza-towers.glb",
  "anchor": [-122.3941803, 37.7933169],
  "targetHeightM": 177.6,
  "cat": 3,
  "name": "One Market Plaza (Spear and Steuart Towers)",
  "estimated": false,
  "dims": [x, y, z],
  "tris": N
}
```

**No `loadRadius`** — this is a resident skyline piece. See 2.13.
````

---

## Part 2 — Research and design dossier

Compiled 19 August 2026. Values marked *inferred* are derived estimates.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Complex | **One Market Plaza**, alt. Del Monte Building; 1 Market Street, block **3713** lot **007** | Wikipedia; SF Planning ZA letter; SF Assessor — measured |
| Completed | **1976**; renovated 1996 (César Pelli) and 2014–16 | Wikipedia |
| Architect | **Welton Becket Associates** | Wikipedia (One Market Plaza and Steuart Tower articles) |
| **Spear Tower height** | **172 m (564 ft)** roof | Wikipedia, CTBUH/skyscrapercenter — two independent sources agree; **and DataSF LiDAR `hgt_median` 172.41 m**, i.e. the survey agrees to 0.4 m |
| Spear Tower floors | 43 (CTBUH says 42 above ground) | Wikipedia / CTBUH |
| Spear plant crest | **177.6 m** | DataSF LiDAR `hgt_maxcm` 177.56 on the shaft's own footprint — 5.2 m of rooftop plant over a 43-storey tower, which is normal |
| **Steuart Tower height** | **111 m (364 ft)** roof | Wikipedia, CTBUH — two independent sources agree; corroborated below |
| Steuart Tower floors | 27 (its own Wikipedia article says 28) | Wikipedia / CTBUH |
| Podium | **6 storeys**, roof **27.8 m** | SF Planning ZA letter ("27 stories with a 6-story podium"); DataSF LiDAR `hgt_median` 27.75 m on `SF3713007` / 201006.0000212 — measured |
| Complex floor area | 1,460,071 sq ft (Wikipedia); lot 007 roll 1,534,312 sq ft on a 113,198 sq ft lot | Wikipedia; SF Assessor (43 stories, built 1979) |
| Facade | **white** towers; the Wikipedia aerial caption names them "Steuart Tower (left, shorter white building), Spear Tower (center, taller white building)" | Wikipedia — measured for colour, *observed* for the pier detail |
| Envelope footprint | **7,521 m2**, AABB 120.7 x 126.5 m | DataSF podium ring ∪ Spear shaft ring, shared edge removed — measured |
| Spear shaft footprint | **52.5 x 35.7 m**, 1,868 m2, centred at local (3783.1, −2575.7) | DataSF `ynuv-fyni` 201006.0001309 — measured |
| Steuart shaft footprint | **43.3 x 33.7 m**, 1,460 m2, centred at local (3843.6, −2583.6) | OSM way/132238431 shifted +1.9, −2.0 into the DataSF frame — *inferred*, see 2.15 |
| Long axes | both shafts run **NW–SE** (135/315 deg), parallel to each other | measured from both rings; confirmed on the nadir imagery |

**Corroborating Steuart's 111 m without LiDAR.** Steuart has no footprint of its
own in the survey, so the published figure was checked against **Spear's**, which
does. On the z20 nadir tile both towers lean the same direction; the lean is
proportional to height. Measured roof-corner displacement from each shaft's
ground ring: Spear **26.7 m**, Steuart **17.6 m**, ratio **1.52**. Published
ratio 172/111 = **1.55**. Solving for Steuart from Spear's known height gives
**113 m** against a published 111 — inside the ±10 m that ±10 px of corner
reading buys. The published value stands.

### 2.2 Sources

- `https://en.wikipedia.org/wiki/One_Market_Plaza` — the complex, Spear 172 m /
  43 storeys, Steuart 111 m / 27 storeys, 1976, Welton Becket Associates, and the
  aerial caption that establishes both towers as white.
- `https://en.wikipedia.org/wiki/Steuart_Tower` — Steuart 111 m / 364 ft.
- `https://www.skyscrapercenter.com/complex/1071` (CTBUH) — independent
  confirmation of both heights; floor counts 42 and 27.
- `https://sfplanning.org/sites/default/files/za/1%20Market%20Street.pdf` — lot
  007, "Spear Tower 43 stories; Steuart Tower 27 stories with a 6-story podium".
- `https://data.sfgov.org/resource/ynuv-fyni` — the Spear shaft footprint and its
  172.41 / 177.56 m heights; the podium polygon and its 27.75 m.
- `https://data.sfgov.org/resource/wv5m-vpq2` — SF Assessor, block 3713 lot 007.
- OSM `way/132238423` (Spear Tower part, h=172, 43 levels), `way/132238431`
  (Steuart Tower part, h=111, 27 levels), `way/132238424` (One Market Plaza,
  h=28), `way/944977178` (podium part, 6 levels) — the only source that separates
  Steuart's shaft from the podium.
- Google satellite z20 — the canted corners, the pier rhythm, the plaza, the
  circular garden, the barrel-vault canopies, the roof plant, and the lean
  measurement above.

### 2.3 Orientation and placement

The complex holds the Mission Street half of the block bounded by Market (NW),
Steuart (NE), Mission (SE) and Spear (SW). Its north-west boundary is the shared
survey edge with the Southern Pacific Building.

Envelope simplified to twelve vertices, Blender coordinates (metres, `+X` east,
`+Y` north, **CCW**), centred on the anchor `-122.3941803, 37.7933169`:

```
( -50.850,  13.450)   W — shared edge with the Southern Pacific Building
( -60.350,   4.150)
( -22.950, -32.650)
( -18.550, -38.150)
(   6.350, -63.250)   S — Mission x Spear return
(  31.650, -38.350)
(  25.550, -32.150)
(  35.050, -23.050)
(  60.350,   2.150)   E — Don Chee Way
(  28.650,  33.150)
(  -1.350,  63.250)   N — toward Steuart Street
( -34.750,  29.050)
```

Encloses 7,521 m2 against the survey's 7,543 m2 (−0.3%).

**Shaft placement** in the same frame: **Spear Tower** centred at
`(−28.90, −1.75)`, 52.5 m (NW–SE) x 35.7 m; **Steuart Tower** centred at
`(+31.65, +6.18)`, 43.3 m (NW–SE) x 33.7 m. The 60.6 m between their centres is
the plaza.

### 2.4 What each side shows

All four elevations of both towers are **the same**: an unbroken run of white
precast piers over dark recessed slots, top to bottom, turning the canted corners
without interruption. That uniformity is the design, not an omission — Welton
Becket gave these towers no principal facade.

- **South-east (Mission Street), 135.2 deg** — the public front: the podium's
  glazed retail level, the plaza steps, and both shafts behind.
- **North-east (Steuart Street / Don Chee Way), 45.2 deg** — Steuart Tower's own
  street elevation, podium below.
- **South-west, 225.2 deg** — Spear Tower's flank over the podium.
- **North-west, 315.2 deg** — the party boundary with the Southern Pacific
  Building; the podium here is what the SP Building's courtyard looks out at.
- **The plaza** — an elevated deck between the shafts with a circular sunken
  garden, a run of glazed barrel-vault canopies along its south-east side, and
  paving. *Observed* from nadir imagery.
- **Above** — two flat light decks inside parapets, a plant enclosure on each
  (Spear's is the crest at 177.6 m), and the podium roof at 27.8 m around them.

### 2.5 Recognition cues (ranked)

1. **Two white shafts, one much taller than the other, on a shared base.**
2. **Canted corners** on both.
3. **Full-height white pier rhythm over dark slots** — no crown, no setback.
4. The elevated plaza with its circular garden between them.

### 2.6 Miniature translation

- **Keep** the height contrast, the canted corners, the pier rhythm, the podium,
  the plaza garden and canopies.
- **Simplify** the piers to applied strips at a coarser pitch than reality; the
  canopies to a run of half-round vaults; the garden to a shallow disc.
- **Drop** all facade detail below the pier grid, the ground-floor lobbies, the
  parapet coping profile.
- **Exaggerate** the canted corners slightly and the pier depth, so the shafts
  keep their vertical grain at skyline distance instead of flattening to slabs.

### 2.7 Massing recipe

| Element | From | To |
|---|---|---|
| Podium (six storeys) | 0.00 | **27.80** |
| Podium parapet | 27.80 | 28.80 |
| Plaza deck | — | 27.80 |
| **Steuart Tower** shaft | 27.80 | **111.00** |
| Steuart parapet / plant crest | 111.00 | **115.50** *(inferred)* |
| **Spear Tower** shaft | 27.80 | **172.00** |
| Spear parapet | 172.00 | 173.20 |
| Spear plant crest | 173.20 | **177.60** |

Both shafts run from the podium roof, not from the ground — they are read as
rising out of it, which is what the piers do in life.

### 2.8 Materials and palette

| Surface | Material |
|---|---|
| Tower piers, podium walls, parapets | `Toy_white` / `Toy_cream` |
| Window slots | `Toy_glass` (mid-dark blue) |
| Podium retail glazing | `Toy_glassl` |
| Roof decks | `Toy_slate` |
| Plant enclosures | `Toy_steel` |
| Plaza paving | `Toy_sand` |
| Garden | `Toy_mint` |
| Canopy glazing | `Toy_glassl` + `Toy_glassl_Glow` |

**Night.** Hero: a **sparse scatter of lit slots up both shafts**, denser low and
thinning with height, which is what a 1976 office tower actually looks like after
dark. Supports: the podium's retail band, and the plaza canopies. The roofs are
not lit. Glow surfaces sit **outside** the opaque glazing, coloured to match it —
a plate tucked behind opaque glass renders nothing.

### 2.9 Triangle budget

Cap **26,000**. Indicative: Spear shaft and piers ~8k; Steuart shaft and piers
~6k; podium ~4k; plaza, garden and canopies ~3k; roofs and plant ~2k; glow ~1.5k.

If it runs over, coarsen the podium's pier pitch before touching either shaft.

### 2.13 Integration notes

- **New landmark (Case B).** `pipeline/lib/landmarks.mjs` entry
  `id: 'oneMarketPlazaTowers'`, `height: 177.6`.
- **`exclude: 30`, measured against the real bake input** (DataSF + Overture,
  after `simplifyRing`, testing centroid **and** vertices as `excluded()` does):

  | Gate | Ring | Verdict |
  |---|---|---|
  | **3.3 m** | overture `One Market Plaza` h=28 | drop — caught by its centroid |
  | **10.4 m** | datasf `SF3713007` h=27.75 (podium + Steuart) | drop |
  | **10.4 m** | datasf `SF3713007` h=172.41 (Spear shaft) | drop |
  | **51.8 m** | datasf `SF3713006` h=46.12 and `SF3713007` h=39.71 | **must survive** — the Southern Pacific Building and its atrium |

  Safe window **(10.4, 51.8)**, 41 m wide; **30 m** sits mid-band. This is
  unusually comfortable — the opposite of the 1 Market case next door, whose
  window was only 19 m wide.
- **The two assets are complementary by construction.** The anchors are 78.2 m
  apart; 1 Market's `exclude: 20` reaches 35.4 m short of this complex's rings,
  and this one's `exclude: 30` reaches 51.8 m short of 1 Market's. Neither eats
  the other. Verify both together after the batch bake.
- **Resident, not streamed: omit `loadRadius`.** At 172 m Spear is over the
  ~150 m skyline-piece threshold, and it is one of the towers that makes the
  waterfront silhouette behind the Ferry Building — a hole there at 2.5 km would
  be visible from across the bay. The manifest has 18 residents and uses no
  `alwaysLoaded` key; follow that convention and simply omit the field.
- **This asset lands in a batch whose `BatchedMesh` is already 91.8% full.** A
  resident entry never leaves that buffer. `BATCH-INTEGRATE.md` must raise
  `BODY_VERTS` in `app/src/assets.js` before this and 1 Market land together —
  see `artifacts/1-market/REPORT.md` §8.7.
- **Batch mode applies**: source-only branch, bake discarded.

### 2.15 Open questions and risks

- **Steuart Tower's footprint is the weakest number here.** It has none in the
  DataSF survey, so the plan uses OSM `way/132238431` shifted by the +1.9, −2.0 m
  registration offset measured between OSM's and DataSF's Spear rings. Its area
  (1,460 m2) is 78% of Spear's, which matches the nadir imagery. Re-check before
  modelling.
- **Steuart's plant crest (115.5 m) is inferred**, by analogy with Spear's
  measured 5.6 m of rooftop plant. It does not set the export height, so an error
  there is cosmetic.
- **The podium is one flat 27.8 m mass in this plan, and reality is more
  complicated** — the LiDAR polygon's mean (54.5 m) is far above its median
  (27.75 m) with a 40 m sigma, because the polygon also contains both shafts.
  Parts of the lot at plaza grade and the Mission Street frontage may sit lower.
  If imagery shows a big step, model it; do not invent one.
- **Do not model the Southern Pacific Building.** It is the brick building on the
  same address and it is a separate asset in the same batch. Most photography of
  "One Market Plaza" shows all three buildings together.
