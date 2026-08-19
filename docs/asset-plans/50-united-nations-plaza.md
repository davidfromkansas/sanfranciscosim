# 50 United Nations Plaza (Federal Office Building) — SF-SIM asset plan

Arthur Brown Jr.'s 1936 Federal Office Building, the last piece of the Civic Center
and the one that closes the axis from City Hall down United Nations Plaza. A whole
city block of light grey granite wrapped around an open courtyard, with a 99 m
Doric colonnade on the plaza front — and, from the app's aerial camera, a C-shaped
metal hip roof around a green roof and a solar array.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/50-united-nations-plaza/`. This document is the plan only: Part 1 is the
runnable task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `50-united-nations-plaza` (registry `50UnitedNationsPlaza`) |
| Existing procedural builder | none — new landmark, **Case B** (needs a `pipeline/lib/landmarks.mjs` entry and a tile re-bake, see 2.14) |
| WGS84 anchor | `-122.4144797, 37.7804306` (OSM oriented-bounding-box centre, measured) |
| Target height | **33.0 m** crest (flat top of the hipped roof); main parapet **29.0 m**; north wing **24.7 m** |
| Footprint | 112.53 x 66.93 m oriented box; 7,447 m2 outer polygon less a 1,939 m2 courtyard = **5,508 m2 built** (OSM relation/19309896, measured) |
| Long-axis bearing | 80.92 deg — the Civic Center grid, 9.08 deg north of due east |
| Triangle cap | 24,000 |
| Category | `18` (Government) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 50 United Nations Plaza GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the Federal Office Building at 50 United
Nations Plaza, San Francisco (Arthur Brown Jr., 1934–36; since renamed the Senator
Dianne Feinstein Federal Building) and deliver it as a downloadable, validated GLB.

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
8. `docs/asset-plans/asian-art-museum.md` — the closest sibling: the same Civic
   Center grid, the same pale-granite Beaux-Arts language, the same "low, wide,
   read from above" problem
9. `docs/asset-plans/50-united-nations-plaza.md` — this plan, whose dossier is your
   research starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- One whole city block of pale granite: a 112 x 67 m rectangular RING with an open
  courtyard in the middle — the courtyard is the building's plan idea and its
  strongest read from the app's downward camera
- The south (United Nations Plaza) hero front: two-storey rusticated base, then a
  99 m run of free-standing two-storey Doric columns, then cornice, balustrade and
  a set-back attic storey
- The three arched double-height main entrances at the centre of the south front,
  and the two **concave** (scooped-in) corner entrances at the south-west and
  south-east corners
- The north (McAllister) side is a storey LOWER than the rest — four storeys and a
  flat roof between two taller granite end pavilions. Do not build a uniform box.
- The roof: a C-shaped, low-pitch standing-seam metal hip with a flat top over the
  south, east and west wings; a flat roof over the north wing carrying the 2013
  green roof and photovoltaic array
- Night: the arched entrances and the attic-storey window band

## Research 50 United Nations Plaza independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views — the roof is more than half of what this asset shows
- Ground-level views and the courtyard
- Day and night appearance
- Publicly available drawings, plans or diagrams
- **The height.** OSM `height=29` on relation/19309896 and the DataSF LiDAR median
  (29.02 m) both describe the **parapet**, not the crest. The metal roof rises
  about 4 m above it. Establish parapet and crest separately and say which is
  which — see 2.3.
- **The date of your photographs.** The public-domain Carol Highsmith rooftop
  photographs are from 2010 and predate the $122 M 2013 renovation: they show the
  old patched lead-coated copper roof and a bare north roof. The current state is
  standing-seam zinc plus a green roof and PV array. Model the current state.

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/50-united-nations-plaza/REFERENCE.md` containing: source links and
what each establishes; verified dimensions and location; orientation; observations
from all four sides and above; the 3-5 strongest recognition cues; features to
preserve; features to simplify; uncertainties and conflicting evidence. A contact
sheet of attributed reference thumbnails is welcome if legally permissible — do not
commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

The finished asset must be immediately recognizable as 50 UN Plaza, consistent
with the real building from all four sides and above, architecturally credible,
and a premium handcrafted miniature — not photorealistic, not voxel art, not
generic low-poly, and never accurate in one view while invented in the others.

This building is 112 m long and 33 m tall — a slab read from above and at a
shallow angle, next to City Hall's 94 m dome. Spend the budget on the ring plan,
the cornice line, the colonnade rhythm and the roof. Do not spend it on column
flutes, dentils or mascarons nobody will resolve.

## Scope of the exported asset

Export the building only: the granite ring (base, colonnade, pilasters, cornice,
balustrade, attic), the concave corner entrances, the courtyard void with its
floor and planting, the C-shaped metal hip roof with its dormers, the north wing's
flat roof with the green roof, PV array and mechanical plant, and the courtyard
elevator bulkhead.

Do not include unrelated surrounding city geometry: United Nations Plaza itself
(paving, fountain, trees, farmers' market), the Civic Center BART/Muni entrances,
the Asian Art Museum, the Main Library, Hyde / McAllister / Leavenworth Streets,
street trees, the flagpole, the sunken east service plaza's fencing, people,
vehicles, plinths, cameras or lights. Temporary context may appear in review
renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 24,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions; `yawDeg` exists
in the manifest but is not used here). The building's long axis runs at bearing
**80.92 deg**, i.e. build the assembly axis-aligned and then rotate it **+9.08 deg
about Z**. The hero entrance front faces **south** onto United Nations Plaza. The
contract's "front faces −Y" is therefore honoured almost exactly here, but
real-world orientation wins either way (AGENTS rule 5). Record the decision and
the measured heading in `REPORT.md`.

**Height normalisation:** normalise the bbox top to the verified crest (33.0 m
unless your research corrects it) exactly, so the loader's
`targetHeightM / measuredHeight` scale lands at 1.0.

**Courtyard:** the courtyard floor is real geometry inside the ring, not a hole in
the mesh. Keep the ring a closed union of solids so the normals test passes on
signed volume.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/50-united-nations-plaza/build_50_united_nations_plaza.py`
(deterministic build script),
`artifacts/50-united-nations-plaza/50-united-nations-plaza.blend`, and
`artifacts/50-united-nations-plaza/50-united-nations-plaza.glb`. The script must
rebuild the model reliably enough for future revision. Do not modify or rename an
unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`50-united-nations-plaza-top.png`, `-north.png`, `-east.png`, `-south.png`,
`-west.png`, plus `50-united-nations-plaza-contact-sheet.png`, at least one high
three-quarter aerial beauty render `-aerial.png`, and a night render `-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; **the top view must clearly show the courtyard, the
C-shaped metal hip roof, and the north wing's green roof and PV array**; the
aerial view uses the style bible's camera assumptions (30-50 degrees down, long
lens). Simple tabletop lighting, neutral warm background, minimal depth of field,
and every image must depict the same exported model. The night render must show
the `_Glow` set driven from Base Color (see the note at the end of
`docs/asset-plans/README.md`).

## Validate the exported GLB

Re-import `50-united-nations-plaza.glb` into a fresh isolated Blender scene and
validate the re-import, not the source scene. Report object count, triangle count,
dimensions, bounding-box min/max, min Z, XY center offset, material names,
image-texture count, camera count, light count, animation count, applied-transform
status, negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/50-united-nations-plaza/validation.json` and
`artifacts/50-united-nations-plaza/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "50-united-nations-plaza",
  "file": "50-united-nations-plaza.glb",
  "anchor": [
    -122.4144797,
    37.7804306
  ],
  "targetHeightM": 33.0,
  "cat": 18,
  "name": "50 United Nations Plaza Federal Office Building",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/50-united-nations-plaza.md`.
````

---

## Part 2 — Research and design dossier

Compiled 19 August 2026 from the sources in 2.2. Values marked *inferred* are visual
or derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Historic name | Federal Office Building; "50 UNP" | NRHP nomination (2017) |
| Current name | Senator Dianne Feinstein Federal Building | GSA historic-buildings page |
| Built | Designed 1933, constructed 1934–1936; the last building of the Civic Center | NRHP, Wikipedia, GSA |
| Architect | Arthur Brown, Jr. (Q4798105), under Supervising Architect Louis A. Simon | Wikidata Q5440315 P84, Wikipedia |
| Style | Second Renaissance Revival / Beaux Arts | NRHP §7, Wikidata P149 |
| Status | NRHP-listed 2017 (#100001018); contributing property to the SF Civic Center National Historic Landmark district | NRHP, Wikidata P1435, HKS |
| Renovation | $122 M GSA/HKS/Hathaway Dinwiddie historic renovation + seismic retrofit, dedicated 6 Nov 2013; LEED Platinum | The Registry (2013-11-07), HKS, Hathaway Dinwiddie |
| Gross area | 350,000 sq ft (32,516 m2) | GSA monograph, HKS |
| Storeys | **Five storeys plus an attic on the south, west and east; FOUR storeys on the north** (McAllister), except its two projecting end portions | NRHP §7 (twice, verbatim) |
| Block | Bounded by United Nations Plaza (S), Hyde St (W), McAllister St (N), Leavenworth St (E) | NRHP §7; confirmed against DataSF street centrelines (measured) |
| Footprint (outer polygon) | 7,447 m2 | OSM relation/19309896 outer way/32865027, reprojected + shoelace (measured) |
| Courtyard (inner polygon) | 1,939 m2 (OSM way/1411159971); 24,000 sq ft = 2,230 m2 as published | measured / The Registry |
| Built footprint | 5,508 m2 | outer − inner (measured); DataSF LiDAR counted 22,235 cells at 50 cm = 5,559 m2 |
| Footprint (oriented box) | 112.53 x 66.93 m (OSM) / 114.10 x 68.96 m (DataSF) | min-area OBB over each polygon (measured) — see 2.4 |
| Courtyard (oriented box) | 72.66 x 27.20 m | min-area OBB over the OSM inner ring (measured) |
| Wing depth | N 21.4 m, S 18.2 m, W 22.4 m, E 18.3 m | outer minus inner ring in the building's own frame (measured) |
| Long-axis bearing | 80.92 deg (9.08 deg north of due east) | derived from the OSM OBB (measured); DataSF gives 9.09 deg, the McAllister/UN Plaza centrelines 9.0 deg |
| OBB centre | −122.4144797, 37.7804306 | derived (measured) |
| **Parapet above grade** | **29.0 m** | three independent agreements: OSM `height=29`, DataSF `hgt_median_m` 29.02, Overture `height` 29, facaderetrofit.org "97 feet" (29.57 m) |
| **Crest above grade** | **33.0 m** | 2010 photogrammetric surface max 47.26 m NAVD88 − 14.14 m median grade = 33.1 m (DataSF `p2010_zmaxn88ft`, `gnd_mediancm`); independently, the LiDAR height mean/median/mode decomposition in 2.3 |
| North wing roof | 24.7 m | DataSF `hgt_majoritycm` 2473 — the modal roof height, and the north wing is 41% of the roof area (measured) |
| Site grade NAVD88 | 12.54–17.23 m (14.14 m median) | DataSF `gnd_*`; the block falls ~4.7 m, and the east service plaza is sunken |
| Walls | Light grey granite on S, W and E below the fifth-floor balustrade; Gladding, McBean glazed terra cotta *tooled to imitate granite* above, and on most of the north elevation | NRHP §7 |
| Roof | C-shaped low-pitch hip clad in standing-seam zinc (2013; replaced the original lead-coated copper) with arched dormers and a flat top, over S/E/W; flat roof over the north four-storey section | NRHP §7 |
| Green roof | 14,000 sq ft converted to garden surrounding a new photovoltaic array; first GSA building with a green roof; gravel drain fields keep soil off mechanical plant and historic parapets | GSA monograph, rooflite, Henry |
| Green roof location | the **north wing's flat roof** | Esri World Imagery nadir, z19 (measured against the projected footprint — see 2.5 Top) |
| South entrance | three arched double-height openings at the centre, keystones with eagle-and-shield cartouches, four lamp sconces | NRHP §7, Wikipedia |
| Corner entrances | south-west and south-east corners are **concave arc** reentrants with arched entrances, eagle cartouches and Doric porticos above the second storey | NRHP §7; confirmed in the OSM ring (four short segments per corner turning through 90 deg over ~6.9 x 6.9 m) |
| North entrance | one arched double-height opening at the centre, reached by a granite bridge over sunken areaways | NRHP §7 |
| Windows | paired four-over-four white-painted wood double-hung, recessed in their openings; four-lite transoms at the first floor | NRHP §7 |

### 2.2 Sources

- https://www.openstreetmap.org/relation/19309896 — multipolygon footprint (outer way/32865027, inner way/1411159971), `height=29`, `start_date=1933`, wikidata link
- https://npgallery.nps.gov/GetAsset/2a46e6cb-74e7-4320-b96d-5870c139903d — **the NRHP registration form (2017), the authoritative elevation-by-elevation description.** Everything in 2.5 that is not marked *inferred* comes from its §7.
- https://en.wikipedia.org/wiki/50_United_Nations_Plaza_Federal_Office_Building_(San_Francisco) — history, the 504 Sit-in, the AIDS Memorial Quilt origin, "hipped roof covered with light grey lead-coated copper"
- https://www.gsa.gov/real-estate/find-a-historic-federal-building/senator-dianne-feinstein-federal-building-san-francisco-ca — GSA's own description; the current building name
- https://www.gsa.gov/system/files/50_UNP_Monograph_MASTER_508.pdf — GSA Design Excellence monograph (Sept 2020): 350,000 sq ft, the rooftop garden around the PV array, the plant palette
- https://data.sfgov.org/resource/ynuv-fyni.json (`mblr=SF0351035`, `area_id=225`) — 2010/2023 LiDAR: `hgt_median_m` 29.02, `hgt_majoritycm` 2473, `hgt_maxcm` 3840, `hgt_meancm` 2849, `hgt_stdcm` 370, `p2010_zmaxn88ft` 155.07, `gnd_mediancm` 1414, 22,235 cells
- http://www.facaderetrofit.org/projects/50-united-nations-plaza — "97 feet"; the 2013 window restoration
- https://news.theregistrysf.com/san-franciscos-50-united-nations-plaza-renovation-ready-unveiling-official-dedication-ceremony/ — $122 M, LEED Platinum, 24,000 sq ft courtyard, dedicated 6 Nov 2013
- https://www.hksinc.com/what-we-do/projects/50-united-nations-plaza/ — architect of record for the renovation, NRHP #100001018
- https://www.rooflitesoil.com/project/50-u-n-plaza/ and https://www.henry.com/knowledge-center/project-profiles/henry-green-roof-system-federal-office-building/ — green-roof build-up, 8-inch media, gravel drain fields
- https://commons.wikimedia.org/wiki/File:2017_50_United_Nations_Plaza_Federal_Office_Building.jpg (CC BY-SA 4.0) — the south-east three-quarter street view: colonnade, corner arch, cornice/balustrade/attic stack
- https://commons.wikimedia.org/wiki/File:2017_50_United_Nations_Plaza_Federal_Office_Building_from_Hyde_Street.jpg (CC BY-SA 4.0) — the south-west corner: the plainer Hyde elevation, the corner hip cap
- https://commons.wikimedia.org/wiki/File:Exterior_from_rooftop,_Federal_Building,_San_Francisco,_California_LCCN2010718894.tif (public domain, Carol M. Highsmith, 2010) — the aerial that shows the whole roof plan and the axis to City Hall
- https://commons.wikimedia.org/wiki/File:Exterior_from_rooftop,_Federal_Building,_San_Francisco,_California_LCCN2010718899.tif and `...LCCN2010718907.tif` (public domain, Highsmith, 2010) — the roof surface, the corner pavilion, the entablature/balustrade/attic stack in close-up
- Esri World Imagery nadir tiles at z19 over the block (0.24 m/px) — the post-2013 roof: courtyard trees, the two PV banks, the green roof, the concave south corners

Exa queries that produced these: `"50 United Nations Plaza Federal Office Building San Francisco height stories granite facade"` (yielded gsa.gov, npgallery.nps.gov, facaderetrofit.org), `"50 United Nations Plaza San Francisco Federal Building aerial rooftop photo courtyard solar array green roof"` (yielded the GSA monograph, rooflite, henry.com, Commons), `"50 United Nations Plaza San Francisco federal building at night illuminated facade lighting"` (yielded nothing on night lighting — see 2.9).

### 2.3 The height (read this before modelling)

Three numbers matter and they are not the same number.

- **29.0 m — the parapet.** OSM `height=29`, Overture `height=29`, DataSF LiDAR
  `hgt_median_m` = 29.02, and facaderetrofit.org's "97 feet" (29.57 m) all land
  here independently. This is the top of the fifth-floor balustrade / main
  cornice line, i.e. the eave of the metal roof.
- **33.0 m — the crest**, and therefore `targetHeightM`. Derived two ways:
  1. DataSF `p2010_zmaxn88ft` = 155.0667 ft = 47.263 m NAVD88, minus the site's
     median grade `gnd_mediancm` = 14.14 m, gives **33.1 m**.
  2. The LiDAR height statistics decompose cleanly. Mode 24.73 m, median 29.02 m,
     mean 28.49 m, sd 3.70 m. The north wing is 21.4/(21.4+18.2+22.4+18.3) ≈ 41%
     of the roof area; put 41% of the area at 24.7 m and the remaining 59%
     spread uniformly between a 29 m eave and a ~33 m top, and the predicted mean
     is 0.41·24.7 + 0.59·31 = **28.4 m** against a measured 28.49, with the median
     landing just above 29 as observed. No other three-level split fits.
- **38.4 m — do NOT use this.** `hgt_maxcm` = 3840 is the 2013 elevator bulkhead
  on the east courtyard side plus rooftop mechanical plant, on 22,235 cells with
  sd 3.70 m. It is a fitting, not the architecture. (Compare
  `docs/asset-plans/500-third.md`, where the bulkhead *was* the right answer —
  there the bulkhead is the silhouette; here it is a box behind a 4 m roof.)

The north wing's roof is **24.7 m**, and that step is a required feature, not a
simplification to be smoothed away.

### 2.4 Orientation and placement

The block is bounded by United Nations Plaza (south), Hyde Street (west),
McAllister Street (north) and Leavenworth Street (east). Measured against the
DataSF street centrelines (`3psu-pn9h`) from the anchor: McAllister 44.1 m north,
UN Plaza 60.3 m south, Hyde 68.7 m west, Leavenworth 77.3 m east — and every one
of those centrelines runs at 9.0 deg off cardinal, the Civic Center grid.

The long axis runs at bearing **80.92 deg**. In Blender with `+Y` = true north,
build the assembly axis-aligned and rotate it **+9.08 deg about Z**.

**The hero front faces south.** This is unusually convenient: the contract's
"front faces −Y" and the real-world heading agree to within 9 deg.

Anchor on the **OSM OBB centre**, `−122.4144797, 37.7804306`. Two notes:

- The DataSF OBB centre is 1.60 m away (`−122.4144646, 37.7804226`) and its box is
  1.6–2.0 m larger in both directions. That is the usual DataSF-vs-OSM offset (see
  `sf3d-parcel-vs-footprint-offset`), and here it is also *informative*: the DataSF
  outline is LiDAR tracing the cornice, the OSM outline is the wall plane. Build
  the wall plane at 112.53 x 66.93 and give the main cornice a ~0.9 m projection
  and the CORNICE outline lands at ~114.3 x 68.7 — DataSF's box to within 0.3 m
  (the metal roof itself sits inboard of that). Use it as a free cross-check on
  the cornice depth.
- The area centroid of the built annulus is only 1.2 m from the OBB centre
  (2024.87, −1153.87 vs 2025.69, −1153.00 in local metres), so there is no
  centroid-vs-box argument here; the box centre is what the model centres on.

The courtyard is NOT centred: in the building's own frame its centre sits 2.05 m
east and 1.65 m south of the building centre, which is what makes the north wing
21.4 m deep and the south wing 18.2 m.

The site falls ~4.7 m across the block and the east service plaza is sunken a
further storey. The app seats assets on sampled terrain at one anchor, so the
model's base will be level while the real building's is stepped. Accept it; do not
model a stepped base or the sunken east plaza.

### 2.5 What each side shows

All four elevations share one tripartite composition: a two-storey rusticated
granite base, a two-storey order above it (columns on the south, pilasters
elsewhere) topped by a projecting dentil cornice, and a set-back fifth floor
behind a balustrade. The differences below are what make each side legible.

**South (United Nations Plaza) — the hero elevation.** 98.7 m of wall between the
two concave corners. Massive rusticated granite base for two storeys, capped by a
slightly projecting belt course. Above it the signature: a colonnade of
**free-standing** two-storey Doric columns standing clear of a recessed wall, with
granite-balustraded balconies at the third floor between them. Projecting dentil
cornice over the colonnade. The fifth floor is set back further again behind a
full-length balcony with a granite balustrade. Three arched double-height entrances
at the centre with eagle-and-shield cartouche keystones and four lamp sconces.
Granite mascarons over every other first-floor window lintel.

**West (Hyde Street).** The quiet side: no entrances at all, no basement access.
Same tripartite composition, but two-storey **pilasters** instead of columns and
balustrades directly in front of the third-floor windows rather than balconies.
The two ends of the elevation are **slightly recessed** from the central portion —
a shallow plane change, well under 1 m (OSM records the wall as one straight
60.0 m segment), so express it as a plane articulation, not a mass.

**North (McAllister Street) — the one that is different.** Almost entirely glazed
terra cotta tooled to imitate granite; only the two **projecting end portions** are
real granite. The central section is **four storeys with a flat roof** — no fifth
floor, no metal roof. The two end portions do carry the fifth floor and the hip
roof, so the north side reads as a low centre between two taller pavilions. One
arched double-height entrance at the centre, reached across a granite bridge over
the sunken areaways, with a carved shield cartouche and two sconces.

**East (Leavenworth Street).** Same as the west (pilasters, recessed ends,
balustrades at the third floor) with one difference: the basement is fully exposed,
so the rusticated base reads as **three** storeys here, and three service entrances
sit at basement level in a sunken plaza with curving ramps. Out of scope for the
GLB — model the elevation, not the plaza.

**Corners.** South-west and south-east are **concave arc** reentrants, roughly
6.9 x 6.9 m of corner scooped inward, each with an arched entrance and a Doric
portico above the second storey. North-west and north-east are square. This
asymmetry is a strong plan-level recognition cue and cheap to build.

**Top — more than half of what this asset shows.** Reading the Esri nadir against
the projected footprint:

- A **C-shaped low-pitch hip roof** in mottled grey standing-seam metal wraps the
  south, east and west wings and the two north end pavilions. It rises from the
  29 m eave to a flat top at 33 m, edged with a patinated-copper gutter line, and
  carries small arched dormers on the slopes.
- The **north wing's flat roof** sits ~8 m lower at 24.7 m and is the 2013 work:
  two long banks of dark blue-grey **photovoltaic panels** running east–west, a
  **green roof** of mid-green planting wrapping around them, white mechanical
  units, and a red-brown gravel margin along the north parapet.
- The **courtyard** (72.7 x 27.2 m) is open to the sky, paved, and planted with two
  rows of trees along its long sides. A glazed-brick elevator bulkhead rises
  through the roof on its east side (2013).

That contrast — historic grey metal hip around a modern green-and-blue flat roof,
around an open green courtyard — is the whole reason this building is worth an
asset. It tells the 1936-plus-2013 story from the air in one read.

### 2.6 Recognition cues (ranked)

1. **The ring plan with the open courtyard** — from the app's camera this is the
   first and strongest read, and nothing else in Civic Center has it
2. The 99 m south colonnade of free-standing columns above a heavy rusticated base
3. The stepped roofline: 24.7 m north wing / 29 m parapet / 33 m metal crest, with
   the two taller granite pavilions bracketing the low north side
4. From above: grey metal hip roof around a green roof and two solar arrays
5. The two concave scooped corners on the plaza front, each with an arched entrance

### 2.7 Miniature translation

**Preserve**

- The 112 x 67 m ring and the 72.7 x 27.2 m courtyard, and the uneven wing depths
  that put the courtyard off-centre
- The 9.08 deg grid rotation — it is what makes the building sit in Civic Center
  rather than float in it
- The north wing's lower flat roof, and the two end pavilions that stay tall
- One continuous cornice line all the way round: the strongest silhouette element
- The concave south corners

**Simplify / exaggerate**

- ~26 real column bays become **18 chunky columns**, diameter semantically enlarged
  to 1.6 m; the third-floor balconies become one continuous balustrade band
- West, east and north pilasters become shallow proud strips, not modelled orders
- The concave corners become 8-segment quarter-scoops (the style bible's low-seg
  curve rule), not smooth arcs
- Every dentil, mascaron, cartouche and sconce is dropped; the entablature becomes
  two clean bands
- Paired four-over-four windows become single recessed `Toy_glass` slots on a
  regular rhythm, ~34 bays long by ~20 bays deep
- Arched dormers become six small `Toy_steel` bumps per long roof slope
- The green roof becomes two `Toy_navy` PV rectangles in a `Toy_mint` field with a
  `Toy_stone` gravel margin and three white plant boxes
- The courtyard's trees become eight `Toy_mint` pucks on a `Toy_stone` floor

### 2.8 Massing recipe

Build order for the deterministic script. Author axis-aligned in the building's own
frame (`u` = long axis, `v` = short axis), then rotate the whole assembly
**+9.08 deg about Z**. `+v` is south. Dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render.

1. **Ring solid.** Outer box 112.53 (u) x 66.93 (v), inner void 72.66 x 27.20 with
   its centre at u +2.05, v +1.65. Scoop the two south corners as 8-segment
   concave quarter-rounds, 6.9 m in each direction. Chamfer the courtyard's two
   south corners ~5 m. Ring height to z = 23.2 everywhere for now.
2. **Plinth / water table:** z 0 → 0.9, `Toy_stone`, 0.25 m proud of the wall.
3. **Rusticated base (floors 1–2):** z 0.9 → 11.0, `Toy_stone`, with four deep
   horizontal rustication grooves (0.12 m deep, not applied bands — cut them).
4. **Belt course:** z 11.0 → 11.7, `Toy_trim`, projecting 0.45 m, all round.
5. **Order zone (floors 3–4):** z 11.7 → 20.6, `Toy_cream`. On the south, set the
   wall back 1.3 m and stand **18 columns** (radius 0.8 m, 10 segments) at the base
   plane, evenly spaced across the 98.7 m front; a continuous `Toy_trim` balustrade
   band z 11.7 → 12.9 runs between them. On the west, east and north, use 0.25 m
   proud `Toy_trim` pilaster strips on the same 5.48 m rhythm and the same
   balustrade band flat against the wall.
6. **Entablature:** architrave/frieze `Toy_cream` z 20.6 → 22.1; cornice `Toy_trim`
   z 22.1 → 23.2 projecting **0.9 m** (this is what makes the roof outline match
   the DataSF box — see 2.4).
7. **Attic (floor 5):** z 23.2 → 27.6, `Toy_cream`, set back 2.2 m from the cornice
   face, on the south/west/east and on the two north end pavilions ONLY. Continuous
   band of small `Toy_glass_Glow` windows (see 2.9). Balustrade `Toy_trim`
   z 23.2 → 24.6 standing at the cornice edge in front of it.
8. **Top cornice + coping:** z 27.6 → 29.0, `Toy_trim`, projecting 0.6 m.
9. **Hip roof:** over the south, east and west wings and the two north end
   pavilions. Eave at z 29.0 at the outer wall line and at the courtyard line,
   rising at ~35 deg to a flat top at **z 33.0** running the length of each wing.
   `Toy_steel`. Six small dormer bumps per long slope. **Do not use `Toy_roofd`
   here** — it reads near-black in the app (see `sf3d-toy-roofd-reads-black`).
10. **North wing:** stop the walls at the cornice z 23.2; parapet `Toy_trim`
    z 23.2 → 24.7; flat deck at z 23.4. On it: `Toy_stone` gravel margin 3 m wide
    along the north edge; a `Toy_mint` green-roof field filling the rest; two
    `Toy_navy` PV banks 34 x 5 m, raised 0.4 m, running along the wing; three
    `Toy_white` mechanical boxes 4 x 2.5 x 1.8 m.
11. **Courtyard:** floor at z 1.0, `Toy_stone`, with a `Toy_sand` walkway cross and
    eight `Toy_mint` tree pucks (radius 2.2 m, z 1.0 → 5.5) in two rows. Courtyard
    walls `Toy_sand` (the glazed light-grey brick). One `Toy_stone` elevator
    bulkhead 6 x 5 x 4 m on the east side, rising to z 27.
12. **Entrances:** six arched openings — three on the south centre (3.6 m wide,
    z 0.9 → 10.0), one on each concave corner, one on the north centre. Fill with
    `Toy_gold_Glow`, recessed 0.6 m. Do **not** build a solid "recess frame" prism
    in front of them (see `sf3d-applied-panel-recess-trap`): cut the reveal, or use
    a lintel band, never a box that swallows the opening.
13. Bevel 0.12 m, 2 segments, last.

### 2.9 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | main granite walls, attic storey |
| `Toy_stone` | `#d9d2c2` | rusticated base, plinth, courtyard floor, gravel margin, elevator bulkhead |
| `Toy_trim` | `#f3efe6` | columns, pilaster strips, belt course, cornices, balustrades, parapets |
| `Toy_sand` | `#ece4d4` | courtyard brick walls, courtyard walkways |
| `Toy_glass` | `#2a4d73` | windows on floors 1–4 |
| `Toy_steel` | `#9aa0a6` | the standing-seam metal hip roof and its dormers |
| `Toy_navy` | `#2c4a70` | the two photovoltaic banks |
| `Toy_mint` | `#8fd0a8` | the green roof and the courtyard trees — the one saturated accent |
| `Toy_white` | `#f7f4ec` | rooftop mechanical boxes |
| `Toy_glass_Glow` | `#2a4d73` | the attic-storey window band — the supporting night accent |
| `Toy_gold_Glow` | `#caa64a` | the six arched entrances — the night hero |

Night: hero = the six arched entrances, warm gold, the only bright points at street
level. Supporting = the continuous attic-storey window band, which traces the
cornice line all the way round and is what gives this low wide building a readable
silhouette from the app's aerial camera at night. Two glow sets, nothing else.
Both glow materials carry the **same base colour as their daytime palette
neighbours**, because that base colour IS the night look (see
`sf3d-glow-colour-is-unlit`); check the night render's colour directly rather than
trusting emission strength in the Blender rig.

**No facade floodlighting.** A targeted search found no documented night lighting
scheme for this building, and none of the sourced photography is nocturnal. Do not
invent an uplit colonnade. If the executing agent finds a credible night reference
showing one, add a shallow recessed `Toy_white_Glow` strip behind the columns —
never a closed shell around them (see `sf3d-glow-shell-day-alpha`).

### 2.10 Top surface

112 x 67 m of roof under a camera that looks down. It must not be a grey rectangle,
and it will not be, because the real roof is already a three-part composition: the
grey metal hip ring at 29–33 m, the green-and-blue flat roof at 24.7 m across the
whole north side, and the open planted courtyard in the middle. Build all three at
their real levels and the aerial read is finished. The value and hue contrast
between the grey historic roof, the mint green roof and the dark blue PV is the
point — resist flattening it toward one neutral.

### 2.11 Scope

**In the GLB:** the granite ring (plinth, rusticated base, belt course, order zone,
entablature, attic, balustrades, cornices), the 18-column south colonnade, the
concave south corners and the six arched entrances, the C-shaped metal hip roof
with dormers, the north wing's flat roof with green roof / PV / mechanical plant,
the courtyard floor, walls, walkways, trees and elevator bulkhead

**Not in the GLB:** United Nations Plaza (paving, fountain, trees, market stalls),
the Civic Center transit entrances, the flagpole, the east sunken service plaza and
its fences and gates, the McAllister areaway railings, the Asian Art Museum, the
Main Library, any street, street trees, people, vehicles, plinths, cameras or
lights

### 2.12 Triangle budget

Cap 24,000. Suggested split: ring solid, courtyard void and concave corners ~5k;
window rhythm on four elevations plus the courtyard ~5k; colonnade and pilaster
strips ~3k; base rustication, belt course, entablature, balustrades and cornices
~4k; hip roof, flat top and dormers ~3k; north flat roof, green roof, PV, plant
~2k; courtyard floor, walkways, trees, bulkhead ~2k.

### 2.13 Draft manifest entry

```json
{
  "id": "50-united-nations-plaza",
  "file": "50-united-nations-plaza.glb",
  "anchor": [
    -122.4144797,
    37.7804306
  ],
  "targetHeightM": 33.0,
  "cat": 18,
  "name": "50 United Nations Plaza Federal Office Building",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`loadRadius` is the default rule `max(2500, 33.0 x 30)` = 2500.

### 2.14 Integration notes (for later, not this task)

**New landmark (Case B).** Add a `pipeline/lib/landmarks.mjs` entry and re-bake, or
the baked procedural block will fight the GLB.

```js
{
  id: '50UnitedNationsPlaza',
  name: '50 United Nations Plaza Federal Office Building',
  lon: -122.4144797,
  lat: 37.7804306,
  height: 33.0,
  exclude: 40,
  camera: { distance: 600, yaw: 268, pitch: 20 },
},
```

`camelId('50-united-nations-plaza')` = `50UnitedNationsPlaza` — confirm against
`app/src/assets.js` line 37 before wiring.

**`exclude: 40` is measured, not guessed.** `excluded()` in `pipeline/buildings.mjs`
drops a footprint when its ring centroid OR any ring vertex falls inside the radius,
measured from the anchor against the rings the bake actually consumes (DataSF and
Overture, projected and `simplifyRing`'d at 0.6 m). From this anchor:

- **DataSF SF0351035 / area_id 225** — this building — centroid **1.64 m**
- **Overture `…7285e5e8827e`** (`height=29`, 10 vertices) — this building again,
  centroid **0.27 m**. Both datasets trace it, so a correct exclusion drops **two**
  rings, not one (see `sf3d-exclusion-two-rings`). Only the DataSF ring is a baked
  building; the Overture one would otherwise gap-fill straight back into the hole.
- Nearest **neighbour**: DataSF SF0348007 / area_id 2493 (across McAllister),
  nearest vertex **54.54 m**; the nearest Overture neighbour vertex is 55.47 m.

So the window is **(1.70, 54.54) m** and 40 sits comfortably inside it with 14.5 m
of headroom. Note that the OBB half-diagonal is 65.46 m — **the half-diagonal rule
would eat a neighbour here.** Do not use it.

The courtyard ring never reaches the bake: `outerRings()` in
`pipeline/lib/geojsonStream.mjs` discards inner rings, so the courtyard was never
baked as a solid and no exclusion is needed for it.

Verify after the bake by decoding the tile rather than trusting
`pipeline/verify-rebake.mjs`'s per-cell counts, which can report "dropped nothing"
for a working exclusion (`sf3d-verify-rebake-count-blindspot`).

**Neighbours.** Civic Center is crowded with landmarks already integrated
(`cityHall`, `asianArtMuseum`, `sfMainLibrary`, `civicCenterPlaza`,
`earlWarrenBuilding`, `civicCenterCourthouse`, `billGrahamCivicAuditorium`,
`101Grove`, `234VanNess`, `500VanNess`, `505VanNess`) and more in flight. Two
consequences:

- The shared landmark `BatchedMesh` is the constraint, not this asset. Check the
  buffer headroom before blaming a new file for a missing neighbour
  (`sf3d-landmark-batch-full`, `sf3d-batch-reserve-overflow`).
- Visually this building must not compete with City Hall, which is three times its
  height 400 m to the west and is the axis's focal point. 50 UNP is the axis's
  *east end*: calm, horizontal, and heavy at the base.

**Batch mode.** If other landmarks are in flight, still run the bake and the full
QA on it, then `git checkout -- app/public/tiles api/_data` and commit source only.

### 2.15 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bbox Z normalised to 33.0 m exactly, so the loader's scale lands at 1.0
- [ ] Bbox X/Y consistent with a 112.53 x 66.93 m box rotated 9.08 deg
      (≈ 114.6 x 83.9 m axis-aligned) plus the 0.9 m cornice projection
- [ ] The courtyard is an actual void in plan and the ring is a closed union of
      solids (per-object signed volume is the authoritative normals test)
- [ ] The north wing is visibly lower than the rest, with its two end pavilions tall
- [ ] Triangles at or under 24,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the six arched entrances and the attic window band
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (ray test residual
      <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Seven review renders + night render + contact sheet regenerated from the
      final export; the top view shows courtyard, hip roof, green roof and PV
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.16 Open questions and risks

- **The 29 m trap.** Four independent sources say 29 m and they are all describing
  the parapet. Anyone who takes 29 m as `targetHeightM` will build the building 4 m
  short and flat-topped, losing the metal roof entirely. Read 2.3 first.
- **The 38.4 m trap in the other direction.** `hgt_maxcm` is the 2013 elevator
  bulkhead. It is 5.4 m above the crest and would make the building taller than
  Bill Graham Civic Auditorium.
- The 33.0 m crest is *derived*, not published: one photogrammetric difference and
  one statistical decomposition, agreeing to 0.1 m. It deserves one oblique-aerial
  sanity check against the neighbouring Asian Art Museum (28.1 m crest, one block
  west) — 50 UNP should read clearly taller.
- The north wing's roof at 24.7 m is the LiDAR *mode*, assigned to the north wing
  on an area argument plus the nadir imagery. High confidence, but *inferred*.
- **The photographs are from two eras.** The public-domain rooftop set is 2010
  (old copper roof, bare north roof); the Commons street views are 2017
  (post-renovation). The Esri nadir is post-2013. Build the current state.
- The column count (~26 real, 18 modelled) and the window bay counts are read from
  photography, not drawings — *inferred*, and chosen for rhythm rather than census.
- The green roof's exact layout (two PV banks, planting around them, gravel to the
  north) is read off one nadir image at 0.24 m/px. The *presence* of a green roof
  and PV array on the north wing is well sourced; the arrangement is *inferred*.
- No night lighting reference exists. See 2.9 — the night state here is a design
  decision, documented as such, not an observation.
