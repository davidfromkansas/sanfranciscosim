# Ferry Station Post Office Building — SF-SIM asset plan

The **Agriculture Building** of 1915, on the water at the foot of Mission Street,
one block south of the Ferry Building: San Francisco's central post office from
1915 to 1925, built so that mail could come off the boats and go out by streetcar.
It is the only Mediterranean-Revival *palazzo* on the Embarcadero — a two-storey
riveted-steel frame standing on a timber-pile wharf, clad in long red pressed
brick laid in Flemish bond, trimmed in trompe-l'œil terracotta cut to look like
ashlar, on a granite base, under a copper cornice and a **low-pitched clay-tile
hip roof**. Three things make it: the **wide tiled hip roof wrapping the
Embarcadero front**, the **light terracotta piers** that break the brick front
into three pavilions, and the **central entrance** with its cast-iron phoenix,
shield and out-thrust flagstaff over the doors.

Behind that two-storey front the building drops away in steps to a one-storey
work-room block with a flat roof and roof monitors, and ends in an open concrete
wharf apron over the ferry slips. From the app's aerial camera that stepped
profile — tall tiled band, mid flat deck, low flat deck, water — is as much of
the identity as the facade is.

It contributes to the **Port of San Francisco Embarcadero Historic District**
(NRHP 2006) and is individually listed (NRHP #78000756, 1 December 1978).

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/ferry-station-post-office/`. This document is the plan only: Part 1 is
the runnable task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `ferry-station-post-office` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3921505, 37.7941368` (footprint AABB centre, measured) |
| Target height | **12.65 m** (clay-tile hip ridge, DataSF LiDAR maximum); cornice/eave **10.8 m**, measured photogrammetrically |
| Footprint | 2,069.3 m2 six-vertex ring; 50.74 m Embarcadero front (SW) x 38.97 m NW flank x 47.20 m SE flank, with an 8.22 x 11.20 m wharf bump-out on the NE (bay) side |
| Triangle cap | 15,000 |
| Category | `18` (Government) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Ferry Station Post Office Building GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the **Ferry Station Post Office Building**
(the **Agriculture Building**), 101 The Embarcadero at Mission Street, San
Francisco — and deliver it as a downloadable, validated GLB.

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
7. `artifacts/300-brannan/` — **the reference implementation for the facade.** Same
   altitude of abstraction: a masonry block on a rotated SoMa/Embarcadero heading,
   built from a measured footprint polygon rather than an axis-aligned box, with a
   pilaster/bay rhythm and a designed roof. Its `build_300_brannan.py` footprint and
   elevation helpers (`poly_edge`, `offset_polygon`, `wall_box`, `bay_spans`,
   `pilasters`, `window_unit`, `glazed_elevation`) are the script skeleton to
   **adapt, not rewrite**.
8. `artifacts/95-jack-london-alley/` — secondary reference for a *sloped-roof*
   masonry landmark at this scale, i.e. how a pitched roof plane is built and
   bevelled without blowing the triangle budget.
9. `docs/asset-plans/ferry-station-post-office.md` — this plan, whose dossier is
   your research starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules.

## Must capture

- The **low-pitched clay-tile hip roof** over the Embarcadero front: a band
  ~17 m deep running the full 50.74 m frontage, hipped at both ends, eave at
  10.8 m, ridge at 12.65 m. This is the single most identifying feature from the
  app's aerial camera and the one place semantic exaggeration is spent — the real
  measured band depth and eave-to-ridge rise give **12.3°** on their own, which is
  enough for the hip to read as a *tile hip roof* from above; no further
  steepening is needed and none should be applied.
- The **stepped section**: tiled two-storey front band → flat two-storey deck at
  ~9.8 m over the middle of the frontage only → flat one-storey work-room deck at
  ~6.6 m with roof monitors, running from the tile straight back to the bay at
  both ends → the 1918/19 tiled wing along the SE flank. Seen from above the
  building is a set of descending terraces, not one box.
- The **three-pavilion Embarcadero front**: full-height light terracotta piers
  set in from each end mark off end pavilions, and the same terracotta frames the
  central entrance. Between them, red brick.
- The **two-band fenestration**: a high first floor of tall rectangular windows in
  recessed brick architraves, a horizontal terracotta string course, and a squat
  second floor of near-square windows with decorative brick panels between them.
- The **central entrance**: terracotta surround, a grilled transom over double
  iron-framed doors, the cast **phoenix-and-shield ornament** above it and an
  **out-thrust flagstaff** angling down over the sidewalk. Simplify the ornament
  to a readable toy shield; keep the flagstaff — it is the silhouette's one
  gesture off the wall plane.
- The **terracotta shield panels** on the second floor either side of the centre.
- The **granite base** as a distinct darker plinth band around the whole building.
- The **dark copper cornice** as a continuous projecting eave line under the tile.
- The **1918/19 south (SE) addition**: a narrower two-storey tiled-hip wing along
  the SE flank, separated from the central block by a recessed light-well slot,
  carrying the same brick and cornice, and stepping out over the former driveway.
- The **roof monitors** (three raised, light-topped clerestory boxes) on the
  one-storey rear deck, plus a restrained scatter of vents and mechanical cubes.
- The **bump-out on the NE (bay) side** is *built on*, not an open apron: the
  1918/19 wing's tiled hip roof covers it out to 47.2 m and hips at the end.
  (This corrects an earlier reading of this plan — see 2.15 risk 9.)

## Research the Ferry Station Post Office Building independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor and the real-world
orientation, and gather references covering:

- The Embarcadero (SW) principal elevation, the NW flank facing Harry Bridges
  Plaza and the Ferry Building, the SE flank facing the ferry gangways, and the
  NE rear over the water
- Aerial/roof views — the tile-roof plan shape, where tile stops and flat deck
  begins, the roof monitors and the light-well slot
- Ground-level views day and night
- The **bay count** of the Embarcadero front. The dossier reads it as a wide
  centre pavilion flanked by two end pavilions from the 2025 Street View
  panorama, and that is the single number most worth re-counting

**Three source traps are already known and resolved in 2.1 and 2.15 — re-check
them, do not silently re-inherit the wrong value:**

1. OSM way/104599975 tags `height=15 m` and `roof:shape=flat`. **Both are wrong.**
   The roof over the front block is a clay-tile *hip*, stated by the NRHP
   nomination, by the Port's own historic-resource description and visible in
   nadir imagery. 15 m is ~2.4 m above the LiDAR crest.
2. The building's height must **not** be taken as a single number. `hgt_maxcm`
   (12.65 m) is the tile ridge over the front band only; the LiDAR median
   (9.80 m) and modal (6.66 m) values are the two flat decks behind it, and the
   published "two-story" description covers only the front 25.9 m of a 38.97 m
   deep building. The reconciliation is worked in 2.7 — model the steps.
3. The building **stands on a pile-supported wharf over the Bay**, not on land.
   Its base is the wharf deck; there is no grade change across the footprint and
   no basement. Do not model piles, water or a plinth — the app's terrain seats
   the asset (see 2.13 for the seating check).

## Create a reference dossier

Write `artifacts/ferry-station-post-office/REFERENCE.md` containing: source links
and what each establishes; verified dimensions and location; orientation;
observations from all four sides and above; the 3–5 strongest recognition cues;
features to preserve; features to simplify; uncertainties and conflicting
evidence. Do not commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

This is a **secondary building with landmark presence** in the style bible's
detail budget (§21). It sits 150 m from the Ferry Building, which is a monument
with a 74.7 m tower; this asset must read as its handsome low neighbour and must
not compete with it. Spend the budget on the roof and the front elevation; keep
the NE rear plain.

Watch the warm-value budget. Brick, clay tile and terracotta are all warm, and a
building made only of them turns into an orange blob at aerial distance. The
separation comes from **value**, not hue: keep the tile roof clearly darker than
the brick, and the terracotta trim clearly lighter than both, and check that
three-step ladder in the aerial render before committing.

The finished asset must be immediately recognizable as this building,
consistent with the real one from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel
art, not generic low-poly, and never accurate in one view while invented in the
others.

## Scope of the exported asset

Export the single building: body, granite base, all four elevations, terracotta
piers and trim, window bays, entrance ensemble with flagstaff, cornice, tile hip
roofs, flat roof decks with parapets, roof monitors, roof furniture, the SE
addition and the light-well slot, and the low wharf apron on the NE side.

Do not include unrelated surrounding city geometry: the Embarcadero roadway,
Muni/F-line tracks and overhead, the ferry gangways, canopies and pontoons at
the Downtown Ferry Terminal, the Ferry Building, Harry Bridges Plaza, palms,
street lights, traffic signals, the bike lane, sidewalks, water, piles, parked
cars, people, plinths, cameras or lights.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ≈ 0; applied
transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; at most
15,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The
**Embarcadero (principal) elevation faces south-west, bearing 234.0°**; the
**NW flank faces 324.3°**; the **SE flank faces 144.3°**; the **NE rear faces
54.0°**. Build directly on the measured footprint polygon in 2.3 rather than
modelling an axis-aligned box and rotating it.

Derive "outward" from the ring's **winding**, never from the centroid: this
footprint has a re-entrant step on the NE side (edge V4→V5), and the centroid
test returns the wrong normal there. Record the measured headings in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the clay-tile hip
ridge over the front band) must land at exactly **12.65 m** so the loader's
`targetHeightM / measuredHeight` scale is 1.0. The flagstaff must not exceed it —
angle it downward as the real one is, so the ridge stays the bounding-box top.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/ferry-station-post-office/build_ferry_station_post_office.py`
(deterministic build script),
`artifacts/ferry-station-post-office/ferry-station-post-office.blend`, and
`artifacts/ferry-station-post-office/ferry-station-post-office.glb`. The script
must rebuild the model reliably enough for future revision.

## Required review renders

Render the exact final geometry from controlled cameras:
`ferry-station-post-office-top.png`, `-north.png`, `-east.png`, `-south.png`,
`-west.png`, plus `-contact-sheet.png`, at least one high three-quarter aerial
beauty render `-aerial.png`, and a night render `-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection.
The **top view is the important one here** — it must clearly show the tile hip
band and its hipped ends, the two flat deck levels, the light-well slot, the roof
monitors and the wharf apron. Place the aerial camera to the south-west so it
sees the Embarcadero front and the SE flank at once, with the roof steps in
profile.

## Validate the exported GLB

Re-import `ferry-station-post-office.glb` into a fresh isolated Blender scene and
validate the re-import, not the source scene. Report object count, triangle
count, dimensions, bounding-box min/max, min Z, XY center offset, material names,
image-texture count, camera count, light count, animation count, applied-transform
status, negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Write
`artifacts/ferry-station-post-office/validation.json` and `REPORT.md`.

The axis-aligned XY bounding box will be roughly **69.8 x 65.2 m** even though no
elevation is longer than 50.7 m — that is the expected consequence of a ~54°
real-world heading plus the tile eave overhang, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

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
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`,
`pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a
separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md`
for that, together with the integration notes in
`docs/asset-plans/ferry-station-post-office.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent
must re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Historic name | **Ferry Station Post Office Building** | NRHP nomination (1978) — measured |
| Current name | **Agriculture Building** (a.k.a. "AG Building") | NRHP nomination; Port of SF property listings; OSM `old_name=AG Building` |
| Address | **101 The Embarcadero**, at the foot of Mission Street | Wikipedia infobox; NoeHill; the "101" is cast over the central entrance and legible in Street View — measured |
| Coordinates (published) | 37.79417, −122.39111 | Wikipedia. **Longitude is ~90 m off**; use the measured anchor below |
| Architect | **A. A. Pyle**, Architectural Division, California State Department of Engineering; structural drawings R. T. Alden | NRHP nomination and NRHP asset metadata — measured |
| Client | State Board of Harbor Commissioners | NRHP nomination |
| Contractor | Teichert and Ambrose | NRHP nomination |
| Dates | Contract 22 Oct 1914; construction begun 30 Apr 1915; completed **1915** (NRHP nomination says August; the district nomination says 6 May); second-storey rear addition **1918**; dolphin extension between ferry slips 7 and 8 begun 31 Jan 1919 | NRHP nomination; Embarcadero Historic District nomination §7 pp. 59, 150–51 |
| Construction cost | $31,981.50 | Embarcadero Historic District nomination |
| Style | **Mediterranean / Mediterranean Revival**, palazzo-like | NRHP nomination; Wikipedia; Port RFI |
| Structure | Two-storey **riveted steel frame**, reinforced-concrete deck on a **timber-pile wharf** built at the same time | Port of SF Historic Piers RFI (2018); Wikipedia — measured |
| Exterior | Long red pressed **brick in Flemish bond** with light mortar; **granite base**; **terracotta / "artificial stone" trim of cement coloured French ochre** rendered as trompe-l'œil ashlar; **copper cornice**; **wood casement windows**; cast- and wrought-iron doors; **clay-tile hip roof** | NRHP nomination §7; NoeHill; Port RFI — measured |
| Storeys | **Two** at the Embarcadero front; the rear work-room block is **one** tall storey (plus a mezzanine, later removed) | NRHP nomination; Port RFI ("one-story east portion") — measured |
| Original plan dimensions | First floor **167 ft x 125 ft** (50.9 x 38.1 m); second floor same width, **85 ft** (25.9 m) deep | NRHP nomination §7 — measured, and the key to the massing (2.7) |
| Footprint (measured) | **2,069.3 m2**, six-vertex ring, 50.74 x 38.97 m main block + an 8.22 x 11.20 m NE bump-out | OSM way/104599975 geometry, projected — measured; DataSF `ynuv-fyni` `sf16_bldgid` 201006.0001038 agrees (8,886 x 0.25 m2 cells = 2,221 m2 incl. eaves) |
| **Height — tile ridge** | **12.65 m** above the wharf deck | DataSF LiDAR `hgt_maxcm = 1265`; corroborated by `peak_1st_m 15.83` − `gnd_meancm 3.07` = 12.76 m — measured |
| **Height — cornice / eave** | **10.8 m** ±0.3 | Photogrammetric solve on Street View pano `PJ2Y60ERa8pqvq0e-Pwxlw`, 152 silhouette samples over 60° of azimuth, rms 0.32° (2.15 risk 2) — measured |
| Height — mid flat deck | **9.80 m** *inferred* | DataSF LiDAR `hgt_median_m` |
| Height — low flat deck | **6.66 m** *inferred* | DataSF LiDAR `hgt_majoritycm` (modal); independently the residual that balances the LiDAR mean (2.7) |
| LiDAR spread | mean 8.72 m, σ 2.67 m over 8,886 cells, min 0.42 m, max 12.65 m | DataSF `ynuv-fyni` — a wide spread, i.e. a genuinely multi-level roof, not an outlier spike |
| Ground | Wharf deck **3.07 m** NAVD88 mean (median 3.11, σ 0.32) | DataSF LiDAR `gnd_*` — the app's terrain handles this, not the asset |
| Frontage headings | Embarcadero front **234.0°** (SW); NW flank **324.3°**; SE flank **144.3°**; NE rear **54.0°** | measured from the footprint polygon by winding |
| NRHP status | Individually listed **#78000756**, 1 Dec 1978; also a contributor to the Port of SF **Embarcadero Historic District** (NRHP 2006) | NPS NRHP; California OHP listing N712; NoeHill — measured |
| Wikidata | **Q38251704** (no height, no coordinates beyond the imprecise pair above) | Wikidata entity dump |
| History of use | Central post office 1915–1925 → transportation-company offices (Southern Pacific, Oakland–Alameda Ferry) 1925–1933 → California Department of Agriculture from 1933 → **Amtrak's San Francisco bus terminal until March 2015** | NRHP nomination; Wikipedia; RailPAC |
| Current use | **Port of San Francisco** property; small-suite office (310–6,000 sq ft at $4.05 psf/mo) and interior storage (300–2,000 sq ft at $2.00) | Port of SF Availability Report, May 2025 — *observed (listing data)* |
| Future | Repeatedly proposed for adaptive reuse (hotel, or office/retail with a one-storey glass addition) and for being **raised ~8 ft** for sea-level rise; nothing built as of this plan | Port Historic Piers RFI 2018 and responses; SF Chronicle, Nov 2018 — **not** to be modelled |

### 2.2 Sources

- `https://npgallery.nps.gov/NRHP/GetAsset/feff6419-1b0b-49e6-ba3c-9bcb8d6a6ff4` —
  **National Register nomination form** (Pamela McGuire, 8 Feb 1978). The primary
  source: architect, dates, contractor, the 167 x 125 ft / 85 ft plan dimensions,
  the Flemish-bond brick, granite base, artificial-stone trim, copper cornice and
  tile hip roof, the pier/pavilion composition of the principal facade, the
  phoenix-and-shield ornament and flagstaff, and the 1918/1919 additions. Quoting
  Charles Hall Page & Associates, *Survey of Cultural Resources*, 14 Nov 1977.
- `https://npgallery.nps.gov/NRHP/AssetDetail?assetID=feff6419-...` — NRHP asset
  metadata: reference #78000756, architect `Pyle, A.A.`, significant year 1915.
- `https://en.wikipedia.org/wiki/Ferry_Station_Post_Office_Building` — address
  101 The Embarcadero, 1915, cost, the 1918 enlargement, the Amtrak terminal until
  March 2015. Its infobox coordinates are imprecise; see 2.15 risk 1.
- `https://noehill.com/sf/landmarks/nat1978000756.asp` — the materials list and,
  importantly, the note that **the "stone" trim is trompe-l'œil, not real stone**.
  Also three 26 May 2008 photographs of the Embarcadero elevation.
- `https://ohp.parks.ca.gov/ListedResources/Detail/N712` — California OHP listing.
- `https://www.sfport.com/sites/default/files/Planning/082018_SFPort-HistoricPiersRFI.pdf` —
  Port of San Francisco, *Historic Piers Request for Interest*, Aug 2018. The
  building description ("two-story, pile-supported … riveted steel frame,
  reinforced concrete deck, beams, girders … brick-clad, terracotta-trimmed façade
  with a granite base, copper cornice, wood casement windows … iron door and clay
  tile roof") and the phrase **"one-story east portion"**, which is what fixes the
  rear massing.
- `https://www.sfport.com/sites/default/files/2025-05/availability_report_may_2025.pdf` —
  current leasing state. *Observed (listing data)*.
- `https://www.sfchronicle.com/business/article/New-SF-hotels-WeWork-backed-waterfront-school-13392845.php`
  and the Pacific Waterfront Partners RFI response — the unbuilt hotel/office
  schemes. Recorded so a future reader does not mistake a rendering for the
  building.
- `https://www.openstreetmap.org/way/104599975` — the footprint ring used for the
  measured geometry in 2.3. Tags `height=15 m` and `roof:shape=flat` are **wrong**
  (2.15 risk 3); `wikidata=Q38251704` is right.
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints,
  LiDAR-derived), `sf16_bldgid` **201006.0001038**, `mblr` **SF9900278** — the
  height statistics that carry this plan, and the polygon the bake actually uses
  (2.13).
- Google Street View, **capture 2025**, panorama `PJ2Y60ERa8pqvq0e-Pwxlw` at
  `37.79393616, −122.39254082` in the Embarcadero/Mission intersection, labelled
  "101 The Embarcadero" — the principal elevation end to end, the entrance
  ensemble, the terracotta piers, the shield panels, the two window bands and the
  cornice. This is the pano the 10.8 m eave was solved from. Two more used for the
  flanks: `PX-RCbub6-akkld2ohlZGA` (`37.79439703, −122.39235567`, on the plaza NW
  of the building — shows the low rear block's brick parapet against the tall
  front block) and `32-vZMNCrEPriUP4k5vL2g` (`37.79390835, −122.39174352`, on the
  ferry gangway SE of the building — shows the SE flank, the tile hip roof in
  profile and the lower rear).
- Google satellite imagery z20 (`https://mt1.google.com/vt/lyrs=s&x=&y=&z=20`),
  stitched and overlaid with the OSM ring — the roof plan: the tile hip band
  wrapping the Embarcadero front and hipping at both ends, the two flat decks
  behind it, the three light-topped roof monitors on the low deck, the light-well
  slot inboard of the SE wing, the mechanical scatter, and the open concrete
  wharf apron on the bay side. ~55% of the ring's plan area reads as tile.

Photos were not downloaded into the repo; the URLs and the observations above are
the record, per the plan-set convention.

### 2.3 Orientation and placement

The building stands on the **bay side of the Embarcadero**, on its own
pile-supported wharf, at the foot of Mission Street — one short block south-east
of the Ferry Building, immediately north-west of the Downtown Ferry Terminal's
gangways. Its principal elevation faces the Embarcadero roadway to the
**south-west**; its rear faces the Bay to the **north-east**; the NW flank looks
across to Harry Bridges Plaza and the Ferry Building; the SE flank looks at the
ferry slips.

Measured OSM footprint, six vertices, in **Blender coordinates** (metres,
`+X` east, `+Y` north, **CCW**, signed area +2,069.3 m2), already centred on the
anchor `-122.3921505, 37.7941368` (the axis-aligned bounding-box centre, which is
what the loader's origin convention needs):

| Vertex | X (east, m) | Y (north, m) | note |
|---|---|---|---|
| V0 | −2.43 | +31.87 | north corner |
| V1 | −34.10 | +9.15 | west corner |
| V2 | −4.25 | −31.87 | south corner |
| V3 | +34.10 | −4.36 | east corner (outer end of the wharf bump-out) |
| V4 | +27.51 | +4.70 | inner end of the bump-out |
| V5 | +20.83 | −0.10 | re-entrant step back to the rear wall line |

Edges, with outward normals derived from the winding:

| Edge | Length | Outward bearing | What it is |
|---|---|---|---|
| V0→V1 | 38.97 m | 324.3° (NW) | NW flank, toward Harry Bridges Plaza |
| V1→V2 | **50.74 m** | **234.0° (SW)** | **the Embarcadero principal elevation** |
| V2→V3 | 47.20 m | 144.3° (SE) | SE flank, toward the ferry slips |
| V3→V4 | 11.20 m | 53.9° (NE) | outer face of the wharf bump-out |
| V4→V5 | 8.22 m | **324.3° (NW)** | **re-entrant** step — the centroid test gets this one wrong |
| V5→V0 | 39.54 m | 54.0° (NE) | main rear (bay) wall line |

Axis-aligned extents: 68.21 m east–west by 63.74 m north–south. The 167 ft
(50.9 m) frontage published in the NRHP nomination and the measured 50.74 m agree
to 0.3%; the 125 ft (38.1 m) original depth and the measured 38.97 m agree to 2%.

### 2.4 What each side shows

**South-west — the Embarcadero (principal) elevation, 50.74 m.** The subject.
A granite base band; above it a high first floor of tall rectangular windows set
in brick architraves outlined by a recessed course of brick; a horizontal
terracotta string course; then a squat second floor of near-square windows with
decorative brick panels between them, and two carved **terracotta shield panels**
flanking the centre. Full-height **terracotta piers** set in from each end mark
off end pavilions with their own lesser entrances under bracketed lintels. The
**central entrance** is a terracotta surround around a grilled transom over double
iron-framed doors with the cast street number **101**; above it the cast
**phoenix-and-shield** ornament carries an **out-thrust flagstaff**. A dark copper
cornice runs the whole length, and the clay-tile roof rises behind it. Wall-mounted
lanterns and a small "THE EMBARCADERO" street blade are present but are street
furniture, not building.

**North-west flank, 38.97 m.** The finished front design is carried around this
side for the depth of the two-storey block, then drops to the one-storey rear:
plain brick with a simple corbelled parapet band, service doors and a fire
escape, looking onto the plaza. The step from two storeys to one is plainly
visible from here and is the most useful reference for the section.

**South-east flank, 47.20 m.** Similar: the finished design returns for the depth
of the front block, then the 1918/19 addition runs back along the flank as a
narrower two-storey tiled-hip wing over what was a driveway, with a recessed
light-well slot between it and the central block. Beyond that, plain brick with
tall segmental-headed openings at deck level.

**North-east rear, over the water.** Utilitarian. The one-storey work-room block's
brick rear wall, roll-up and service doors, and the open concrete wharf apron with
bollards, rails and stacked equipment. This is the side the aerial camera sees
least; keep it plain.

**Above.** The reason this asset is worth building. A **clay-tile hip roof band
~17 m deep runs the full frontage and hips at both ends**; behind it a flat deck
at ~9.8 m; behind that a larger flat deck at ~6.6 m carrying **three raised,
light-topped roof monitors** in a row and a scatter of vents, ducts and mechanical
cubes; a **narrow tiled hip** along the SE flank with a dark light-well slot
inboard of it; and finally the open concrete apron on the bay side. Terraces, not
a box.

### 2.5 Recognition cues (ranked)

1. **The wide clay-tile hip roof** over a long brick two-storey block, on the
   water, one block from the Ferry Building. Nothing else on the Embarcadero has
   it.
2. **The three-pavilion terracotta-and-brick front** — light full-height piers
   dividing a red-brick wall, with the terracotta-framed central entrance.
3. **The stepped roof section** falling away from the tile band to two flat decks
   and then to an open wharf apron.
4. **The entrance ensemble**: grilled transom, phoenix-and-shield, out-thrust
   flagstaff.
5. **The two-band fenestration** — tall first-floor windows over a string course,
   squat second-floor windows with brick panels between.

### 2.6 Miniature translation

- **Keep:** the tile hip band and its hipped ends; the three-pavilion rhythm; the
  granite base; the cornice line; the two window bands; the shield panels; the
  entrance with flagstaff; the roof monitors; the light-well slot; the apron.
- **Exaggerate (a little):** the roof pitch, from ~8° to at most ~12°, so the hip
  reads as a *roof* from the aerial; the depth of the terracotta piers, so the
  three-pavilion break survives at aerial distance; the cornice projection.
- **Simplify:** Flemish bond → flat brick colour; the trompe-l'œil ashlar → plain
  terracotta blocks at the piers and surrounds; the ornamental brick panels
  between second-floor windows → a single recessed band or a simple diamond motif;
  the phoenix-and-shield → one chunky shield plaque; wood casement muntins → flat
  dark glass panes; the cast-iron door frames → a simple frame.
- **Drop:** the fire escape's fine members (a solid stair box instead, or nothing);
  wall lanterns; downpipes; the ferry-terminal gangways and canopies; signage
  other than the entrance number, if it is even legible at scale.

### 2.7 Massing recipe

The section is the thing this plan exists to get right, so here is how the four
numbers were reconciled. DataSF LiDAR over 8,886 cells gives max **12.65 m**,
median **9.80 m**, mode **6.66 m**, mean **8.72 m**, σ 2.67 m. A two-level model
cannot produce a median of 9.80 with a mode of 6.66; a three-level model can, and
it is the model the documents independently describe:

| Level | Plan area | Height | Contribution |
|---|---|---|---|
| Tiled front band (hipped, eave 10.8 → ridge 12.65) | ~842 m2 (50.74 x 16.6) | mean ≈ 11.7 m | 41% |
| Flat deck behind it, still two storeys | ~256 m2 (s 9.0–36.5 only) | **9.80 m** | 12% |
| One-storey work-room deck + the 1918/19 SE wing | ~970 m2 | **6.60 m** / wing 9.9–11.05 | 47% |

That set reproduces the reported **median 9.80** exactly (the 50th percentile lands
in the middle band) and the reported **mode 6.66** (the largest single flat area),
and its area-weighted mean of ~9.6 m sits above the reported 8.72 m — the
balance being the 50 cm edge cells that catch the wharf deck (`hgt_mincm = 42`;
the DataSF polygon is 2,221 m2 against the ring's 2,069 m2, so ~7% of its cells
are eave-overhang cells) and the sloped tile spreading across bins rather than
concentrating in one. Independently, the NRHP nomination says the **second floor
was only 85 ft (25.9 m) deep** against a 125 ft (38.1 m) first floor, and the Port
describes a **"one-story east portion"**. 16.6 m of tile + ~9.3 m of flat deck =
25.9 m of two-storey block. Three lines of evidence, none tuned to the others.

Build order:

1. **Base plinth.** Granite band, the full six-vertex ring, 0 → 1.0 m, inset 0.
2. **Two-storey front block.** From edge V1→V2 inward 25.9 m over s 9.0–36.5 and
   16.6 m elsewhere, full 50.74 m width,
   walls to the cornice at 10.8 m. Cornice: a projecting band 10.4 → 10.8 m,
   ~0.5 m proud, returning around both flanks for the block's depth.
3. **Tile hip roof.** Over the front 16.6 m of that block: eave at 10.8 m at the
   outer face, ridge at **12.65 m** 8.3 m in from the frontage and running
   parallel to it, hipped at both ends at the same pitch, which puts the ridge
   ends ~8.3 m in from each corner.
4. **Mid flat deck.** The remaining ~8.9 m of the two-storey block: deck at 9.80 m,
   brick parapet to 10.40 m, coping a lighter terracotta.
5. **One-storey block.** The rest of the main ring (to the V5→V0 rear line): deck
   at **6.60 m**, brick parapet to **7.30 m** with a terracotta coping band (the
   NRHP's "artificial stone band" crowning the original rear).
6. **SE addition.** A wing **10.74 m** wide along edge V2→V3, running the full
   depth from the tiled front band out to the bump-out (30.6 m): walls to 9.40 m,
   cornice to 9.90 m, its own tile hip to a ridge at **11.05 m** on the wing's
   centre line, hipped at the bay end. Between it and the central block, a
   **light-well slot** 3.5 m wide dropped to 5.40 m.
7. **Roof monitors.** Three boxes on the one-storey deck, in a row parallel to the
   frontage, each ~7 x 2.5 m, rising 1.5 m above the deck, with a light-toned top
   and a dark glazed side band.
8. **Roof furniture.** A restrained scatter of low vents, two duct runs and one
   mechanical cube on the mid and low decks. Nothing on the tile.
9. **No wharf apron.** The V3–V4–V5 bump-out is roofed by the SE wing (step 6),
   not open deck. Nothing inside the footprint ring is at ground level.
10. **Facade detail.** Terracotta piers at ~8.5 m and ~17 m in from each end of
    the frontage, full height and ~0.35 m proud; a string course at 6.6 m; two
    window bands; the central entrance bay 6 m wide with a terracotta surround,
    transom grille, doors, shield plaque and a flagstaff angled ~35° down and
    ~2.5 m out at 8.5 m.

Bevel everything with the project's 0.10–0.15 m, 2-segment convention. Do **not**
bevel the hairline reveals — per the applied-band convention, hairline strips are
built as thin proud boxes without bevels.

### 2.8 Materials and palette

All flat, roughness ~0.85, from the project palette in
`.agents/skills/sf-asset-check/SKILL.md`:

| Surface | Material | Hex | Note |
|---|---|---|---|
| Brick walls | `Toy_brick` | `c96f4a` | the dominant field |
| Clay-tile roofs | `Toy_rust` | `a86444` | **must stay clearly darker than the brick** — this is the value step that keeps the aerial legible |
| Terracotta piers, surrounds, string course, copings, shields | `Toy_sand` | `ece4d4` | the light step; the real trim is a warm cement ochre, and `Toy_sand` is the palette's nearest light warm |
| Granite base plinth | `Toy_steel` | `9aa0a6` | cool grey against the warm field |
| Copper cornice | `Toy_ink` | `3a3530` | the real cornice reads near-black in 2025 imagery — do **not** invent a verdigris patina it does not have |
| Windows, transom grille, light-well slot | `Toy_glass` | `2a4d73` | the style bible's dark blue-grey graphical window |
| Flat roof decks, wharf apron | `Toy_steel` | `9aa0a6` | **not** `Toy_roofd` — `Toy_roofd` renders near-black (rgb 9,9,12) on a horizontal deck under the app's lighting and swallows the roof |
| Roof monitor tops | `Toy_stone` | `d9d2c2` | the light caps that make the monitors read from above |
| Roof furniture, doors, flagstaff | `Toy_roofd` / `Toy_ink` | `45454a` / `3a3530` | small vertical objects, where `Toy_roofd` behaves |
| Lit ground-floor windows at night | `Toy_glass_Glow` | `2a4d73` | see below |
| Entrance transom at night | `Toy_gold_Glow` | `caa64a` | the hero |

**Night state.** Restrained, and required. Hero: the **entrance transom and door
glass** glow warm gold — one small, bright, unmistakable point at the centre of the
frontage. Supporting: a sparse, irregular row of **first-floor windows** on the
Embarcadero elevation only, using `Toy_glass_Glow`, roughly one in three lit, none
on the second floor, none on the rear. Nothing on the roof glows.

Build the glow surfaces as **flat inset panels**, never as closed shells around the
window recesses: a closed `_Glow` shell is two alpha layers and reads at ~23%
opacity in daylight, which tints the whole facade. And remember that a `_Glow`
material's **base colour is its unlit daytime appearance** — pick a colour that is
already right by day, then let the night pass make it emit.

### 2.9 Top surface

Restated because the camera looks down and this roof is the asset:

- Tile hip band, front 17 m, hipped both ends, ridge parallel to the Embarcadero.
- Flat deck at 9.80 m behind it, inside a parapet, empty except two vents.
- Flat deck at 6.60 m behind that, inside a parapet, carrying the three monitors,
  two duct runs and one mechanical cube.
- Narrow tile hip along the SE flank; a dark recessed light-well slot inboard of it.
- Open concrete apron on the bay side, kerbed, empty.
- Nothing on the tile roofs — no vents, no aerials. The tile planes must stay clean.

### 2.10 Scope

**In:** the building and its wharf apron, as listed in Part 1's scope section.

**Out:** the Embarcadero roadway and its F-line tracks and overhead, the ferry
gangways/canopies/pontoons of the Downtown Ferry Terminal, the Ferry Building,
Harry Bridges Plaza and its palms, street lights, traffic signals, the protected
bike lane, sidewalks, water, piles, parked vehicles, people, and any of the
unbuilt hotel/office/glass-addition proposals.

### 2.11 Triangle budget

| Element | Budget |
|---|---|
| Base plinth + main wall masses (3 blocks) | 900 |
| Cornice bands and parapet copings | 900 |
| Tile hip roofs (front + SE wing), bevelled | 700 |
| Terracotta piers (6) and string course | 900 |
| First-floor window band (~22 openings, recess + pane) | 3,200 |
| Second-floor window band (~22 openings) | 2,600 |
| Entrance ensemble (surround, transom grille, doors, shield, flagstaff) | 1,400 |
| End-pavilion entrances (2) | 500 |
| Shield panels (2) and brick panel motif | 500 |
| Roof monitors (3) | 700 |
| Roof furniture | 700 |
| Light-well slot, wharf apron and kerb | 600 |
| Bevel overhead | ~1,200 |
| **Total** | **~14,800 of 15,000** |

If it overruns, take it from the second-floor window band first (merge the
recess and pane into one inset box), then from the brick panel motif.

### 2.12 Draft manifest entry

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
    69.8386,
    65.2024,
    12.65
  ],
  "tris": 11596,
  "loadRadius": 2500
}
```

`loadRadius` by the default rule: `max(2500, 12.65 x 30) = 2500`. This is not an
`alwaysLoaded` skyline piece; it must stream.

### 2.13 Integration notes (for later, not this task)

**Case B — new landmark.** There is no `ferryStationPostOffice` in
`pipeline/lib/landmarks.mjs` or `app/src/landmarks.js`, so integration needs a
registry entry *and* a tile re-bake, and must run `pipeline/verify-rebake.mjs`
(audit 1.6).

Draft registry entry:

```js
{
  id: 'ferryStationPostOffice',
  name: 'Ferry Station Post Office Building',
  lon: -122.3921505,
  lat: 37.7941368,
  exclude: 39,
  camera: { distance: 260, yaw: 290, pitch: 22 },
},
```

The camera's `yaw` is **not** the frontage bearing: the offset is
`(sin yaw, ·, cos yaw)` with `+z` south, so the camera's compass bearing from the
building is `180 − yaw`. Standing the eye at bearing 250° — just off the
frontage's 234° normal, so the SE flank rakes away behind the front — needs
`yaw: 290`.

**Sizing `exclude` — measured, not guessed.** `excluded()` in
`pipeline/buildings.mjs` drops a source footprint if its centroid **or any ring
vertex** falls within `exclude` metres of the registry anchor. Measured from this
anchor against the DataSF footprints the bake actually reads:

- this building's own DataSF ring spans **18.24 m → 37.34 m** from the anchor, so
  anything below 37.4 m leaves part of the procedural block standing;
- the nearest neighbouring DataSF footprint (`mblr CN9900002`, the ferry-terminal
  gangway kiosk) has its closest vertex at **41.45 m**.

So the window is **37.4 ≤ r < 41.5 m** and **39 m** sits comfortably in it —
1.7 m of clearance below, 2.5 m above.

**Predicted collateral that did not happen.** Overture also carries two OSM
`building=roof` rings — way/979811981 and way/979811987, the gangway canopies at
the Downtown Ferry Terminal — whose nearest vertices are **29.93 m** and
**32.87 m** from the anchor, i.e. *inside* any radius that can clear this
building's own footprint, so on paper they read as unavoidable collateral.

They are not. Measured from the baked tile rather than from the source data
(18 August 2026), neither ring reaches the baked city at all — the cross-source
gap-fill in `pipeline/buildings.mjs` does not emit them. In cell `23_10`,
`origin/main`'s nearest footprint vertex *after* this building's own is 80.31 m
from the anchor; `24_10`'s nearest is the DataSF gangway kiosk at 41.45 m, and
the exclusion leaves it untouched. **The exclusion drops exactly one baked
footprint — this building's own, 12.2 m tall.** Rings penetrating the asset
footprint go 1 → 0; per-cell counts go 49 → 48 in `23_10` and are unchanged in
all 584 other cells.

This is why the check is "which rings disappear", not "how many": the source-data
answer (four rings at risk) and the baked answer (one ring dropped, no
collateral) are different, and only the tile settles it.

**Terrain seating is the risk to check first.** This building stands on a wharf
over the Bay, so its base is the wharf deck at ~3.07 m NAVD88 while the app's
terrain at that point may sample much closer to water level (y = 0). The loader
seats a landmark from a single terrain sample at the anchor. At local QA, confirm
the asset is not floating over, or sunk into, the Embarcadero edge; if it is,
that is a manifest/anchor conversation, not a reason to re-export the GLB.

Everything else follows `docs/asset-plans/INTEGRATION-PROMPT.md` unchanged:
re-validation, the manifest entry with its explicit `loadRadius`, the re-bake,
audit 1.6, local verification (single building, scale ≈ 1.0, orientation, terrain
seating, night glow, draw calls < 300) and the mandatory fallback drill.

### 2.14 Validation checklist

- [ ] Binary `.glb`, real metres, applied transforms, no negative scales
- [ ] `min_z` ≈ 0, XY centre ≈ (0, 0)
- [ ] Bounding-box **Z = 12.65 m exactly** (the tile ridge; the flagstaff below it)
- [ ] Bounding box ≈ 68.2 x 63.7 m in XY — the expected consequence of the ~54° heading
- [ ] Embarcadero elevation faces **234.0°**, i.e. its outward normal is −X−Y
- [ ] ≤ 15,000 triangles
- [ ] Materials all `Toy_*`, flat, no textures, no transparency, no `Toy_body`
- [ ] `_Glow` present on the entrance transom and a sparse first-floor window set only
- [ ] `_Glow` base colours look correct in the **day** render, not only at night
- [ ] Outward normals: per-object signed volume for the union of solids; ray test
      ≤ 0.15% residual
- [ ] Fresh-scene re-import validated, not the source scene
- [ ] No cameras, lights, animation, armatures, constraints, foreign geometry
- [ ] Top render shows tile band, both flat decks, monitors, slot and apron
- [ ] Night render shows one hero glow and a restrained supporting set

### 2.15 Open questions and risks

1. **Wikipedia's coordinates are wrong by ~90 m.** The infobox gives
   37.79417, −122.39111; the building is at −122.3921. Use the measured anchor
   `-122.3921505, 37.7941368` (the footprint AABB centre). *Resolved.*
2. **The eave height is photogrammetric, not published.** Nobody publishes a height
   for this building; Wikidata has none. 10.8 m comes from a least-squares fit of
   the roofline silhouette in Street View pano `PJ2Y60ERa8pqvq0e-Pwxlw` — 152
   samples across 60° of azimuth against the known 18.63 m perpendicular standoff,
   rms 0.32°, with the camera height cross-checked at 2.16 m against three
   pedestrians in frame. It is corroborated at the NW corner independently
   (8.69 m above camera at D = 31.33 m vs 8.60 m from the fit). Confidence: ±0.3 m.
   **The shipped height is the LiDAR ridge, 12.65 m, which does not depend on it** —
   the eave only sets where the roof starts.
3. **OSM `height=15 m` and `roof:shape=flat` are both wrong.** 15 m is 2.4 m above
   the LiDAR crest and 4.2 m above the measured eave; the roof is a clay-tile hip,
   per the NRHP nomination, the Port's description and nadir imagery. Do not
   re-inherit either tag. *Resolved.*
4. **The 9.80 m mid deck is inferred.** It is the LiDAR median and it is what makes
   the three-level model reproduce both the median and the mode (2.7), and it
   matches the documented 85 ft second-floor depth — but no photograph in the
   source set looks straight down on it. If the executing agent finds a view that
   contradicts it, the report wins over this plan.
5. **The SE wing's dimensions are estimated.** Its ~9 m width and ~30 m run come
   from the nadir tile mask, which suffers parallax on a 12.65 m building. The
   narrow (~3 m) tile strip measured right at the SE ring edge may be an eave
   overhang rather than a separate roof plane. Re-read it from imagery before
   committing.
6. **The building may be raised ~8 ft.** Several Port schemes propose lifting it
   for sea-level rise, and one adds a one-storey glass floor. None is built. Model
   the building as it stands; if a future re-bake finds it changed, that is a new
   revision, not this one.
7. **Warm-value collapse.** Brick, tile and terracotta are all warm; at aerial
   distance the building can turn into one orange mass. The mitigation is the
   three-step value ladder in 2.8 (tile darker than brick, trim lighter than both)
   plus the cool grey base and decks. Check it in the aerial render specifically —
   the Blender review rig is more forgiving than the app's flatter lighting.
9. **Corrections made during the build**, all of which this plan has been updated
   for and all of which are argued in
   `artifacts/ferry-station-post-office/REFERENCE.md` §8: the NE bump-out is
   roofed by the 1918/19 wing rather than being an open apron; the two-storey
   block is 25.9 m deep only over the middle of the frontage; the clay tile is
   *lighter and more saturated* than the brick, not darker; and the registry
   camera's `yaw` had been written as the frontage bearing rather than
   `180 − bearing`.
10. **It must not out-shout the Ferry Building** 150 m away. If the two are ever
   framed together and this one draws the eye first, the tile is too saturated or
   the roof pitch has been pushed too far.
