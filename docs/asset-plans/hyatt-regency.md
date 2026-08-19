# Hyatt Regency San Francisco — SF-SIM asset plan

John Portman's 1973 concrete wedge at the foot of Market Street: a triangular plan
that comes to a point on Embarcadero Plaza, a full-height fin wall along Market,
and fifteen guest-room terraces marching down and back to the north-west over a
two-storey podium — crowned at the Market/Drumm end by the Equinox drum under its
cantilevered concrete frame. The only stepped wedge in the landmark set.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/hyatt-regency/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `hyatt-regency` |
| Existing procedural builder | none — new landmark (Case B: needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3957275, 37.7942899` (bbox centre of the simplified footprint) |
| Target height | **80.8 m** (265 ft, CTBUH architectural top; DataSF LiDAR max 80.64 m) |
| OSM footprint | OSM way/28319370, 6,672 m2; 130.97 x 87.31 m oriented box, long axis 45.8 deg true |
| Triangle cap | 27,000 |
| Category | `7` (Hotel — same as `fairmont`) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Hyatt Regency San Francisco GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the Hyatt Regency San Francisco (5
Embarcadero Center) and deliver it as a downloadable, validated GLB.

Do not integrate or deploy the model yet. Create the asset, validate it, render
review images, and commit the deliverables to your working branch.

## Read the project sources first

Before any research or modeling, read in this order:

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-miniature-style/SKILL.md`
5. `.agents/skills/sf-asset-check/SKILL.md`
6. `app/public/sf-assets/landmarks_manifest.json`
7. `artifacts/salesforce-tower/` — the reference implementation of this exact
   deliverable (dossier, deterministic build script, validator, renders, report)
8. `docs/asset-plans/hyatt-regency.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules.

## Must capture

- The **stepped wedge**: a vertical fin wall the full 95.6 m of the Market Street
  frontage, from which fifteen guest-room terraces march down and back to the
  north-west until they meet the podium. This is the asset.
- The **triangular plan** that comes to a 23.6 m point on Embarcadero Plaza —
  from the plaza the building reads as a tall blank prow, from Drumm Street as a
  giant staircase.
- The **deep vertical precast fins** with narrow window slots on every full-height
  face: the brutalist rhythm that makes the concrete read as concrete.
- The **Equinox rooftop pavilion** at the Market/Drumm end: a drum under a big
  cantilevered rectangular concrete frame — the crown and the height datum.
- A two-storey **podium** with a recessed glazed arcade and a projecting eave,
  continuous with the Embarcadero Center promenade.
- Night: the podium lobby glass is the hero glow (the world's largest hotel
  atrium is behind it); the Equinox crown carries one restrained warm accent.

## Research the Hyatt Regency independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, the real-world orientation,
and — above all — **which way the wedge falls** (2.15 risk 1). Gather references
covering:

- The Market Street (south-east), plaza (north-east), Embarcadero Center
  (north-west) and Drumm Street (west) elevations
- Aerial and roof/top views — the camera looks down and this roof is a wedge
- Ground-level views of the podium arcade and the Drumm Street entrance
- Day and night appearance
- The Equinox pavilion: drum diameter, frame extent, how far it oversails
- The three published height figures (2.1) and what each measures

Prefer architect/engineer publications, owner or institutional material,
planning documents, architectural press, geolocated photography, and
aerial/satellite imagery. Never rely on a single photograph. Separate verified
facts from visual inference; if sources disagree, document the disagreement and
decide.

## Create a reference dossier

Write `artifacts/hyatt-regency/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3-5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22. The finished
asset must be immediately recognizable as the Hyatt Regency, consistent with the
real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature.

This building's silhouette from the app's aerial camera is a **wedge**, and the
wedge's terraced upper surface is the largest thing the camera sees. Budget
accordingly (§10, "roofs are secondary facades") — the terraces ARE the roof.

## Scope of the exported asset

Export the hotel volume only: podium, the stepped guest-room mass, the fin walls,
the wing roof and its mechanical ridge, and the Equinox pavilion.

Do not include: Embarcadero Plaza, the Vaillancourt Fountain, Market Street, Drumm
Street, the California Street cable car turntable, Embarcadero Center 4 or its
podium, the elevated pedestrian bridges, trees, people, vehicles, plinths, cameras
or lights. Temporary context may appear in review renders but must not leak into
the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied
transforms; no negative scales; outward normals; no duplicate or foreign geometry;
no image textures; no transparency; flat-color materials named `Toy_*` from the
project palette; `_Glow` suffix only on surfaces that glow at night; no `Toy_body`;
no cameras, lights, animations, armatures or constraints; at most 27,000 triangles.

**Normalize the bbox top to 80.8 m exactly** so the loader's
`targetHeightM / measuredHeight` scale lands at 1.0.

**Orientation:** author with Blender `+Y` = true north, `+X` = east. The Market
Street frontage runs 45.8 deg true and faces 135.8 deg; the plaza prow faces
45.8 deg. Do not rotate the plan to "look better".

## Reproducible Blender workflow

Blender 4.5 LTS or newer, headless only: `blender -b --python script.py -- args`;
assume no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/hyatt-regency/build_hyatt_regency.py`, `hyatt-regency.blend`, and
`hyatt-regency.glb`.

## Required review renders

`hyatt-regency-top.png`, `-north.png`, `-east.png`, `-south.png`, `-west.png`,
`-contact-sheet.png`, at least one high three-quarter aerial `-aerial.png`, and a
night render `-night.png`. The four elevations must share scale, framing, lighting,
exposure and projection. The top view must clearly show the terrace field, the wing
roof ridge and the Equinox frame. Put a night tile on the contact sheet.

## Validate the exported GLB

Re-import into a fresh isolated Blender scene and validate the re-import. Report
object count, triangle count, dimensions, bbox min/max, min Z, XY center offset,
material names, image-texture count, camera/light/animation counts, applied
transforms, negative scales, normal orientation, and per-material contract
compliance. Normals: per-object signed volume is authoritative for a union of
solids; a ray test may show <= 0.15% residual. Write `validation.json` and
`REPORT.md`.

## Manifest draft

```json
{
  "id": "hyatt-regency",
  "file": "hyatt-regency.glb",
  "anchor": [-122.3957275, 37.7942899],
  "targetHeightM": 80.8,
  "cat": 7,
  "name": "Hyatt Regency San Francisco",
  "estimated": false,
  "loadRadius": 2500,
  "dims": [x, y, z],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`,
or any app code in this task.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026. Values marked *inferred* are visual or geometric
deduction, not a cited source.

### 2.1 Verified facts

| Fact | Value | Source |
|---|---|---|
| Name | Hyatt Regency San Francisco | OSM, Wikidata Q5952911 |
| Address | 5 Embarcadero Center, SF CA 94111 | OSM `addr:*`, PCAD |
| Architect | John C. Portman Jr. / John Portman & Associates | Wikipedia, PCAD, portmanarchitects.com |
| Built | constructed 1971, opened May 1973 | PCAD |
| Structure | all-steel frame | CTBUH / Skyscraper Center |
| Rooms | 802–804 | Portman Architects (802), Wikipedia (804) |
| Gross area | 837,382 sf (77,795 m2); site 84,000 sf (7,804 m2) | Portman Architects |
| Atrium | 300 x 170 x 170 ft (91.4 x 51.8 x 51.8 m) — long the Guinness record holder | PCAD; Wikipedia quotes 107 x 49 x 52 m |
| Height (architectural top) | **80.8 m / 265 ft** | CTBUH Skyscraper Center |
| Height (LiDAR max) | 80.64 m | DataSF `ynuv-fyni`, footprint at 37.79424,-122.39585 |
| Height (other) | 77 m / 253 ft (Wikipedia); 83 m (OSM tag) | — |
| Floors | 20 above ground (CTBUH, OSM); "17 stories" (Portman Architects) | — |
| OSM way | 28319370, 33 nodes, 6,672 m2 | Overpass |

**Height decision.** CTBUH's 80.8 m "height to architectural top" and DataSF's
LiDAR maximum of 80.64 m agree to 0.16 m — two independent measurements of the
same crest, which is the Equinox pavilion frame. **Target height = 80.8 m**, and
the model's bbox top is the top of that frame. Wikipedia's 77 m and OSM's 83 m are
both rejected: 77 m is the roof deck of the guest-room wing plus parapet
(*inferred*), 83 m is an OSM estimate with no cited basis. Eave (wing roof deck)
is modelled at 72.0 m, crest at 80.8 m — recorded explicitly per the pipeline's
non-negotiable.

**Floor-count discrepancy.** CTBUH/OSM say 20, the architect says 17. Both are
true of a wedge: 20 levels exist at the Market Street face, 17 guest-room levels
sit in the stepped mass. Neither is used as a height input.

### 2.2 Sources

- Wikipedia, *Hyatt Regency San Francisco* — height 77 m, 20 floors, 804 rooms, opening 1973, owner Blackstone, atrium record, `Eclipse` sculpture by Charles O. Perry, former Equinox revolving restaurant.
- CTBUH Skyscraper Center, building 16108 — **80.8 m / 265 ft to architectural top**, 20 floors, all-steel structure. The height figure used.
- portmanarchitects.com project page — "wedge-shaped design **steps back to open the plaza to the bay**", 17 stories, 802 rooms, site 84,000 sf, GBA 837,382 sf. The single most load-bearing sentence in this dossier: it fixes the direction of the wedge.
- PCAD (U. Washington) entry 3413 — constructed 1971, opened May 1973, Portman + Howard Hirsch interiors, "Piranesian" triangular atrium 300 x 170 x 170 ft.
- OSM way/28319370 via Overpass — footprint geometry, `height=83`, `building:levels=20`, `tourism=hotel`, `wikidata=Q5952911`.
- DataSF LiDAR building heights (`ynuv-fyni`) — two footprints cover this building; see 2.3.
- Wikimedia Commons: `Hyatt Regency San Francisco (110103874).jpg` (2021-05-08, from Embarcadero Plaza — the definitive long elevation), `Hyatt Regency San Francisco 01.JPG` (Drumm/California corner — the Equinox pavilion and the stepped corner), `Five Embarcardero Center.jpg` (telephoto from the bay — the wedge silhouette), `160205-G-XX113-060.jpg` (USCG aerial from the bay — the terrace field), `...(Unsplash).jpg` (facade detail: balcony bands and vertical-bar railings), `2008 Olympic Torch Relay ... Justin Herman Plaza 69.JPG` (podium arcade at ground level).
- Google and Esri satellite imagery, z19–z20, stitched and overlaid with the OSM ring (see 2.3).

### 2.3 Orientation and placement

The site is a quadrilateral bounded by **Market Street** (south-east), **Drumm
Street** (west), **Embarcadero Plaza** (east/north-east) and the **Embarcadero
Center 4 podium** (north-west). California Street ends at Drumm at the site's
north-west corner (the California cable-car turntable is there).

Building axes used throughout this plan: **u** runs along the Market frontage at
bearing **45.8 deg true**; **v** is perpendicular, positive toward Market
(bearing 135.8 deg). Origin at OSM node lon `-122.3958136`, lat `37.7944765`.

The 33-node OSM ring reduces to a 7-point polygon with **6,663 m2** against the
surveyed 6,672 m2 (0.13% error):

| P | east (m) | north (m) | u | v | edge to next | length | outward normal |
|---|---|---|---|---|---|---|---|
| P0 | -1.70 | -56.20 | -40.40 | +39.11 | Market frontage | 95.61 m | 135.8 |
| P1 | 66.86 | 10.44 | +55.21 | +39.13 | plaza prow (a) | 9.95 m | 45.8 |
| P2 | 59.92 | 17.57 | +55.21 | +29.18 | plaza prow (b) | 13.63 m | 45.8 |
| P3 | 50.42 | 27.35 | +55.21 | +15.54 | north-west frontage | 102.23 m | 351.2 |
| P4 | -50.59 | 11.63 | -28.16 | -43.61 | Drumm upper | 20.52 m | 273.2 |
| P5 | -51.72 | -8.86 | -43.26 | -29.71 | Drumm lower | 61.49 m | 257.5 |
| P6 | -38.41 | -68.89 | -75.56 | +22.61 | Market/Drumm end | 38.84 m | 160.9 |

The Market frontage and the north-west frontage **converge at P1–P3**, so the plan
is a wedge in plan as well as in section: 23.6 m deep at the plaza prow, 82.7 m
deep at the Drumm end. Axis-aligned bbox 118.58 m (E–W) x 96.24 m (N–S); bbox
centre = **anchor `-122.3957275, 37.7942899`**.

**DataSF splits this building into two LiDAR footprints**, and the split is the
evidence for the section:

| DataSF ring | area | max | median | min | position |
|---|---|---|---|---|---|
| `201006.0000636` | 3,211 m2 | 80.64 m | 60.22 m | 11.07 m | south (Market half) |
| `201006.0000477` | 3,730 m2 | 74.78 m | 39.72 m | 0.27 m | north (terraced half) |

The southern half's median roof is **60.2 m**; the northern half's is **39.7 m**
with returns down to ground. That is a wedge falling from Market towards the
north-west, and it is an entirely independent confirmation of the architect's own
"steps back to open the plaza to the bay". A shadow measurement on the Google
z20 imagery (sun azimuth ~130 deg, shadow ~15 m past the north-west frontage)
puts that outer edge at **~11 m**, which is the southern ring's LiDAR minimum
to 0.1 m.

### 2.4 What each side shows

**South-east — Market Street (95.6 m, faces 135.8).** The full-height face: a
vertical wall of **deep precast fins**, roughly 3.2 m on centre, each flanking a
narrow recessed window slot, running unbroken from the podium eave to the roof
parapet at ~73 m. No setbacks, no balconies, no crown. Above and behind it the
terraces step away, so from an oblique view down Market the roofline reads as a
long diagonal — this is what the 2021 plaza photograph shows.

**North-east — the plaza prow (23.6 m, faces 45.8).** The wedge's point. A tall,
almost blank pale concrete end wall meeting the fin wall at a sharp arris; the
podium below carries the Embarcadero Center promenade and its escalators. The
USCG aerial shows this prow as the one large unfenestrated surface on the
building.

**North-west — the Embarcadero Center frontage (102.2 m, faces 351.2).** The
terrace field: fifteen guest-room floor plates stepping down and back, each
slab edge a pale horizontal band over a dark recessed balcony. This face is only
partly public — Embarcadero Center 4's podium is a few metres away — but it is
what the app's aerial camera sees.

**West — Drumm Street (20.5 m + 61.5 m, faces 273.2 / 257.5).** The cut end of
the wedge: a giant staircase of slab edges, each floor stepping back from the one
below, with the service core rising past them to the Equinox pavilion. The hotel
entrance and the `HYATT` lettering are on this side, under the podium eave.

**South-west — the Market/Drumm end (38.8 m, faces 160.9).** Full-height fin
wall, matching Market. The Equinox pavilion sits directly above this corner.

**Top.** From above the building is a triangular field of stepped slabs bounded
by the flat wing roof along Market. The wing roof carries a long clerestory ridge
and round mechanical units; the Equinox frame oversails the roof at the Drumm end.
Measured from Google z20 imagery, the wing roof band is ~18–25 m deep and runs the
full Market frontage.

### 2.5 Recognition cues (ranked)

1. The stepped wedge — fifteen terraces falling from a full-height Market wall to
   a two-storey podium. Nothing else in the city does this.
2. The triangular plan with the sharp prow on Embarcadero Plaza.
3. The Equinox pavilion: a drum under a cantilevered rectangular concrete frame,
   sitting off-centre at the Drumm end.
4. Deep vertical precast fins with narrow window slots — brutalist grey concrete.
5. The continuous podium eave tying it into the Embarcadero Center promenade.

### 2.6 Miniature translation

- Keep the wedge; **exaggerate the terrace slab edges** (0.55 m band, 0.35 m
  proud) so the staircase reads at thumbnail size. The real slabs are thinner.
- Compress the real ~3.0 m fin pitch to 3.2 m and deepen the fins to 0.75 m so
  the fin rhythm survives at 30-50 deg down. 30 fins on Market, not 32.
- Reduce 17 guest levels to **15 terraces** at 4.0 m — semantic scale, not
  literal (§9). The wedge angle is preserved.
- The podium becomes one clean two-storey volume with a recessed glazed arcade and
  a 1.0 m eave; the real podium's ramps, bridges and planters are dropped (§22.2).
- The Equinox frame is simplified to two stacked rectangular rings over a drum,
  oversailing 6 m — the real thing has more members but reads the same.
- No people, vehicles, trees or plaza paving in the GLB (scope).

### 2.7 Massing recipe

All heights in metres above the model's z=0.

1. **Podium** — the 7-point plan extruded 0 -> 12.0. A recessed glazed arcade
   band 1.4 -> 7.2, inset 1.3 m (`Toy_glassl_Glow`, the hero night surface). A
   projecting eave 10.9 -> 12.0, proud 1.1 m (`Toy_trim`).
2. **Stepped mass** — fifteen slabs, n = 0..14. Slab n spans z = 12.0 + 4.0n to
   16.0 + 4.0n, and its plan is the site polygon clipped to `v >= v_n` where
   `v_n = 13.12 - 3.0 * (14 - n)`. So the top slab (n = 14) is exactly the Market
   wing (v >= 13.12, i.e. 26.0 m deep), and the bottom slab (n = 0) reaches
   v = -28.88. Each slab is 3.0 m shorter than the one below it — this single
   rule produces the whole wedge, and the site polygon clips it, which is why the
   terrace count falls from fifteen at the Drumm end to three at the prow.
3. **Terrace band** — each slab carries a 0.55 m pale fascia proud 0.35 m along
   its exposed north-west edge, over a dark recess (`Toy_glass`).
4. **Fin wall** — on the Market frontage, the plaza prow and the Market/Drumm
   end, vertical fins 1.1 m wide x 0.75 m deep at 3.2 m centres from z = 12.0 to
   the local slab top, with `Toy_glass` between them.
5. **Wing roof** — 72.0 m deck with a 1.4 m parapet (73.4 m), a clerestory ridge
   3.5 m wide running the length of the Market frontage, and four round
   mechanical units.
6. **Equinox pavilion** — centred at u = -38.0, v = +18.0 (measured off the z20
   imagery). Square core 14 x 14 from 12.0 to 73.4; drum d = 20 m, 16 segments,
   73.4 -> 77.6, with a shallow cap; a lower frame ring 28 x 24 at 77.0 -> 78.4
   and an upper frame ring 32 x 27 at 79.4 -> **80.8** (the bbox top), both
   hollow, both oversailing the drum.
7. Bevel modifier 0.12 m / 2 segments on everything (contract rule 6).

### 2.8 Materials and palette

| Material | Hex | Where |
|---|---|---|
| `Toy_stone` | d9d2c2 | main concrete: podium, slabs, fin wall, prow |
| `Toy_trim` | f3efe6 | podium eave, terrace fascias, Equinox frame — the lit planes |
| `Toy_steel` | 9aa0a6 | fins, parapet cap, mechanical units |
| `Toy_glass` | 2a4d73 | window slots between fins, terrace recesses |
| `Toy_glassl_Glow` | 6f95b8 | podium arcade glazing — **hero night glow** (the atrium behind it) |
| `Toy_gold_Glow` | caa64a | a 0.5 m band under the Equinox upper frame — supporting accent |

Two glow groups only, matching non-glow neighbours by day: `Toy_glassl` reads as
a lighter glass than `Toy_glass`, `Toy_gold` as a warm metal trim. Per
`sf3d-glow-colour-is-unlit`, the base colour IS the night look — no closed glow
shells, no day-time alpha stacking.

### 2.9 Top surface

The terrace field is the roof. It is designed by construction (fifteen stepped
plates with fascias) and needs no props. The wing roof gets the clerestory ridge,
four mechanical drums and the parapet; the Equinox frame reads from directly
above as a rectangular ring around a circle, which is exactly what the satellite
shows.

### 2.10 Scope

In: podium, stepped mass, fin walls, wing roof and mechanical, Equinox pavilion.
Out: plaza, fountain, streets, cable-car turntable, Embarcadero Center 4 and its
podium, pedestrian bridges, trees, people, vehicles, plinth, cameras, lights.

### 2.11 Triangle budget

| Element | est. tris (post-bevel) |
|---|---|
| Podium + arcade + eave | 900 |
| 15 stepped slabs + fascias | 3,600 |
| Fin wall (~50 fins) + glass | 5,400 |
| Wing roof, parapet, ridge, mechanical | 1,800 |
| Equinox pavilion | 1,600 |
| **Total** | **~13,300** (cap 27,000) |

### 2.12 Draft manifest entry

```json
{
  "id": "hyatt-regency",
  "file": "hyatt-regency.glb",
  "anchor": [-122.3957275, 37.7942899],
  "targetHeightM": 80.8,
  "cat": 7,
  "name": "Hyatt Regency San Francisco",
  "estimated": false,
  "loadRadius": 2500,
  "dims": [118.6, 96.2, 80.8],
  "tris": 0
}
```

`loadRadius` = `max(2500, 80.8 * 30)` = 2500 m.

### 2.13 Integration notes (Case B)

New landmark: needs an entry in `pipeline/lib/landmarks.mjs` and a tile re-bake.

**Exclusion radius — measured, not guessed.** `excluded()` in `pipeline/buildings.mjs`
drops a footprint when its ring centroid OR any ring vertex falls inside the
circle. Measured from the OSM polygon centroid (`-122.3958308, 37.7943469`)
against the real bake inputs (`buildings_datasf.geojson` + `overture_buildings.geojsonseq`):

```
TARGET rings (three — Overture traces the whole building, DataSF splits it in two):
  overture 2121409a  h 83   6672 m2   centroid  0.00   nearest vertex 31.21
  datasf   ...0636   h 63.2 3211 m2   centroid 12.91   nearest vertex 19.62
  datasf   ...0477   h 36.7 3730 m2   centroid 15.54   nearest vertex 19.62

nearest NEIGHBOUR (Embarcadero Center 4 podium):
  datasf   ...0734   h 10.0 3164 m2   centroid 65.30   nearest vertex 41.11
  overture be43e192  h 17.0 3090 m2   centroid 61.72   nearest vertex 46.75

sweep:  r=13 -> 2 rings   r=16..41 -> 3 rings (correct)   r=42 -> 4 (eats the podium)
```

The safe window is **16–41 m**; `exclude: 28` sits in the middle with 12.4 m of
headroom over the last target and 13.1 m under the neighbour. THREE rings is the
correct answer against the raw inputs — but **the bake drops TWO**, because
`buildings.mjs` dedupes Overture against DataSF before excluding, so the Overture
copy was never baked as its own footprint. Settled from the tile, not from the
counts: in `origin/main`'s `23_10.bin` three footprints reach within 60 m of this
anchor (centroids 5.23 / 29.33 / 59.38 m); after the re-bake only the 59.38 m one
survives, nearest vertex 40.83 m — 12.8 m clear of the radius. The two that went
were 7.4 m and 6.1 m tall: the baked Hyatt was a podium block, not a tower.

`verify-rebake` also reports cell **23_13** changing (169 → 182 footprints). That
is **not** this radius. The control the tool itself prescribes was run — remove
the entry from `landmarks.mjs`, re-run `buildings.mjs` — and 23_13 still differs
from `origin/main` by exactly the same amount, as the *only* cell that differs.
It is the `pipeline/data/` snapshot vintage, not the exclusion. In batch mode the
bake is discarded anyway, so nothing about 23_13 ships from this branch.

Registry entry:

```js
{
  id: 'hyattRegency',
  name: 'Hyatt Regency San Francisco',
  lon: -122.3958308,
  lat: 37.7943469,
  height: 80.8,
  exclude: 28,
  camera: { distance: 420, yaw: 160, pitch: 28 },
}
```

`camera.yaw` is `180 - true bearing` of the eye. Bearing 20 deg (NNE) is the one
quarter that shows both recognition cues at once: the plaza prow (outward normal
45.8) and the terrace field on the north-west frontage (351.2). Pitch 28 at 420 m
puts the eye 197 m up, clear of Embarcadero Center 4's ~171 m roof, which stands
directly across the north-west site line.

### 2.14 Validation checklist

Binary GLB; metres; min Z 0 +/- 0.01; XY centre 0 +/- 0.05; bbox top exactly
80.8; applied transforms; no negative scale; outward normals (signed volume per
object; ray residual <= 0.15%); no textures/alpha/cameras/lights/animation; only
the six `Toy_*` names in 2.8; tris <= 27,000; renders from the re-imported file.

### 2.15 Open questions and risks

1. **Which way the wedge falls** was the single hardest question in this research,
   and three independent lines settle it the same way: the architect's own
   "steps back to open the plaza to the bay"; the DataSF LiDAR split (south median
   60.2 m vs north median 39.7 m); and a shadow measurement past the north-west
   frontage that puts that edge at ~11 m against the southern ring's LiDAR
   minimum of 11.07 m. Photographs alone were *not* sufficient — several
   plausible camera solutions gave opposite answers. If a future pass finds
   evidence against this, the whole massing flips and must be rebuilt, not patched.
2. **Terrace count** is a design decision (15 at 4.0 m), not a survey. The real
   building has 17 guest levels at ~3.5 m in a wedge whose top three levels are
   the wing. The silhouette angle is preserved; the step count is semantic scale.
3. **The Equinox pavilion's plan position** (u -38.0, v +18.0) was measured off
   Google z20 imagery to about +/- 4 m. Its frame dimensions (32 x 27 m upper
   ring, 6 m oversail) are *inferred* from the Drumm/California photograph and
   are the least-sourced numbers in the model. They set the bbox top, so an error
   here is an error in the shipped height — flagged, not hidden.
4. **The atrium is not modelled.** The world's largest hotel lobby is invisible
   from outside except through the podium glass, which is why that glass is the
   hero glow. Modelling a void inside a toy landmark would cost geometry the
   camera never sees.
5. **The podium is shared** with Embarcadero Center's promenade in reality; the
   asset cuts it at the site line. The exclusion radius of 28 m deliberately does
   NOT reach the EC4 podium footprint (41.1 m away), so that neighbour keeps its
   procedural block and the join is a hard edge. Accepted.
6. The 7-point simplified plan drops six sub-4 m jogs on the Drumm frontage
   (OSM nodes 25–28) and a 6.9 m stub at the Market/Drumm corner (node 0). Area
   error 0.13%.
