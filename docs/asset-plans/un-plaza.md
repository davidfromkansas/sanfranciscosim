# United Nations Plaza — SF-SIM asset plan

Lawrence Halprin's 1975 gateway to the Civic Center: a 2.8-acre wedge of **red brick
herringbone** driven diagonally out of Market Street, up the closed Fulton Street
alignment, toward City Hall's dome. Two rows of eight inscribed granite light standards
march down its axis like a colonnade; a sunken pile of 673 Sierra granite blocks — the
fountain — sits at the Market end; the UN emblem is inlaid at the centre; Simón Bolívar's
bronze closes the west end at Hyde Street. Since November 2023 the middle of it has also
been the **UN Skate Plaza**.

This is the second plan in the set whose subject is a plaza rather than a building, and
the first whose recognition cue is a **colour**. Civic Center Plaza is a green carpet three
blocks west; UN Plaza is the red one. Seen from the app's aerial camera they must never be
confused, and the thing that separates them is that this one is brick.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/un-plaza/`. This document is the plan only: Part 1 is the runnable task prompt,
Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `un-plaza` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4138900, 37.7801415` (world-axis-aligned XY bbox centre of the plaza polygon, measured) |
| Target height | **16.4028 m** — the model's *vertical extent*, not a height: this shipped as a terrain-draped ground asset (see 2.16). The plaza's own height is 13.00 m, the crown of the tallest plane tree. Light standards 5.90 m; Bolívar 8.10 m; obelisk 5.18 m; fountain crest 4.03 m |
| Footprint | L-shaped, 220.8 m (along Fulton) × 150.3 m (across) in the plaza frame; 11,264 m² = **2.78 acres**, measured from OSM relation `1735771` / outer way `24588033` |
| Axis-aligned XY bbox | ~215.3 m × 158.0 m — expected; the plaza is a wedge between two grids 35.7° apart |
| Triangle cap | 18,000 |
| Category | `0` (Miscellaneous — the slot Civic Center Plaza, Palace of Fine Arts and Coit Tower use) |

> **This plan's building brief arrived as "UN Plaza, 355 McAllister St".** 355 McAllister is
> **Civic Center Plaza**, three blocks west, which is already integrated (`civic-center-plaza`,
> anchor `-122.41761, 37.7794895`, DataSF parcel `0788001`). United Nations Plaza is a
> different site 340 m east with no McAllister address at all. See 2.15 risk 1.

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready United Nations Plaza GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of **United Nations Plaza**, San Francisco — the
brick pedestrian plaza on the closed Fulton Street alignment between Market Street and
Hyde Street, plus the closed block of Leavenworth Street running north from it — and
deliver it as a downloadable, validated GLB.

Do not integrate or deploy the model yet. Create the asset, validate it, render review
images, and commit the deliverables to your working branch.

## Read the project sources first

Before any research or modeling, read in this order:

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-miniature-style/SKILL.md`
5. `.agents/skills/sf-asset-check/SKILL.md`
6. `app/public/sf-assets/landmarks_manifest.json`
7. `artifacts/civic-center-plaza/` — the closest reference implementation in *kind*: the
   other Civic Center plaza, built on the same street grid, in the same frame convention,
   with the same "the ground plane IS the asset" problem. Read its REPORT.md for what went
   wrong there before repeating it.
8. `artifacts/asian-art-museum/` and `artifacts/sf-main-library/` — the neighbourhood's
   scale and palette; this plaza has to read as the same world as those two.
9. `docs/asset-plans/un-plaza.md` — this plan, whose dossier is your research starting
   point, not a substitute for your own verification.

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules. Do not invent a new style and do not copy
visual instructions from unrelated prompts.

## Must capture

- **The red brick field.** Roughly 10,900 m² of herringbone brick paving is 80% of this
  asset and it is recognition cue #1. UN Plaza is the only large red plaza in the city.
  The brick must be a *designed* surface — a joint grid, a change of tone at the walks,
  a kerb line legible from the air — never a flat red slab.
- **The double colonnade of 16 light standards.** Two rows of eight square granite
  columns with white globe luminaires, 11.76 m apart across the axis and ~11.77 m apart
  along it (one wider 15.8 m bay at the centre, where the UN emblem sits). Measured
  positions are in 2.3. This is the second cue and the one that makes the plaza read as
  designed rather than as leftover paving.
- **The sunken granite fountain** at the Market end: an octagonal well ~40 × 21 m holding
  an asymmetric pile of pale grey Sierra granite slabs, crest 4.03 m above plaza grade,
  basin sunk about 2.4 m below it. Chunky, blocky, stacked — this is a Halprin object and
  it should look like a giant's game of jacks, not like a water feature.
- **The wedge.** The plaza's south-east boundary is Market Street at bearing 45.20°,
  cutting across a plaza whose own axis is 80.94°. The 35.74° wedge is the plan shape and
  it must survive at thumbnail size. Do not straighten it.
- **The two planting beds** flanking the promenade (decomposed granite, not lawn — this
  plaza has almost no grass), the **south stepped terrace** descending toward Market, and
  the **Walk of Great Ideas**: a broad pale granite band inlaid across the brick carrying
  the UN Charter preamble, with the 4.6 m **UN emblem** roundel on the centreline.
- **Simón Bolívar** (Adamo Tadolini, bronze equestrian on a pale pedestal, ~8.1 m overall)
  closing the west end at Hyde Street, and the 5.18 m black granite **obelisk**.
- **The UN Skate Plaza** (opened November 2023, expanded February 2025): a pale concrete
  skate surface with low ledges, banks and three geometric skateable art pieces, occupying
  the central paved area. Plus the plaza's current furniture — game tables, fitness
  station, café seating, festoon lighting, the Pit Stop toilet, bike racks.
- **The Leavenworth arm**: the fenced planted strip and dog run running north from the
  plaza along the Federal Building's east flank.

## Research United Nations Plaza independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the WGS84
anchor, the plaza polygon, the 80.94° / 45.20° bearings, the light-standard positions, and
the current state of the site, and gather references covering:

- **Aerial and satellite imagery, which is the primary reference** — the camera looks down
  and this asset is almost entirely a ground plane. Note that the current Google/Esri
  imagery of this block **predates the November 2023 renovation**; see 2.15 risk 2.
- The Market Street elevation (the plaza's front door and BART portal), the Hyde Street
  end, and the long north edge against the 1936 Federal Building at 50 UN Plaza.
- Ground-level views looking **west along the Fulton axis toward City Hall** — the
  composition the plaza was designed to create and the model's signature view.
- The fountain from several angles. It is a genuinely complicated object and every photo
  of it is different; simplify honestly rather than inventing blocks.
- Day and night appearance. The globes on the 16 standards are the plaza's night signature.
- Recent (2024–2026) photography of the skate plaza, the game tables and the seating, to
  place the 2023–25 layer correctly.

Prefer the Cultural Landscape Foundation, SF Planning's Civic Center Cultural Landscape
Inventory and its DPR 523B record for UN Plaza, SF Recreation & Parks, sf.gov's own
project pages, the SF Arts Commission's civic art record for the fountain, geolocated
photography and aerial imagery. Never rely on a single photograph, a single AI-generated
image, or a single unsourced 3D model. Separate verified facts from visual inference; if
sources disagree, document the disagreement and decide.

**Four source problems are already known and resolved in 2.1 and 2.15 — re-check them, do
not silently re-inherit the wrong value:**

1. **The brief's address, 355 McAllister Street, is Civic Center Plaza's, not this
   plaza's.** Confirm you are modelling the right site before anything else.
2. **OSM tags way `128534096` `leisure=pitch` + `sport=skateboard`, but every aerial
   available shows a decomposed-granite tree bed on that footprint.** The tag is newer
   than the imagery. Treat the polygon as the *bed* and place the skate surface from
   post-2023 photography, not from that outline.
3. **The plaza's own OSM ring is digitised ~0.5° off the street grid** (its long edges
   measure 80.3–80.4° where DataSF's McAllister centrelines measure 80.96° over seven
   consecutive blocks). Build on the grid, not on the ring's drift. See 2.3.
4. **There is no published height for the light standards.** 5.90 m is a photogrammetric
   measurement off a levelled photosphere, not a survey. It is not the height datum — the
   tree crowns are — but it is the number the colonnade is built from.

## Create a reference dossier

Write `artifacts/un-plaza/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the 3–5 strongest recognition cues; features to preserve; features to
simplify; uncertainties and conflicting evidence. A contact sheet of attributed reference
thumbnails is welcome if legally permissible — do not commit copyrighted full-resolution
imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22, adapted as
`artifacts/civic-center-plaza/` adapted it: there is no massing to rebuild, so the
equivalent moves are **§12 Landscaping**, **§13 Roads and Ground Plane** and **§17
Composition**.

This is a **hero landmark** in the style bible's detail budget (§21), and its detail must
go into *pattern, colour and rhythm*. Two style-bible rules carry unusual weight:

- **§13, last sentence.** Four fifths of this asset is paving. Give the brick a joint
  pattern and a tonal break where the granite bands cross it, or the plaza will read as a
  red parking lot from 600 m.
- **§15 and §16.** This is the most heavily used public space in the Civic Center. Place
  small clusters of people at four deliberate nodes — the skate surface, the fountain rim,
  the café seating, the Market/BART portal — never an even sprinkle.

The finished asset must be immediately recognizable as this plaza, consistent with the
real place from all four sides and above, credible as landscape architecture, and a
premium handcrafted miniature.

## Scope of the exported asset

Export the plaza only: the brick ground plate and its kerb, all paving and granite inlays
(the Walk of Great Ideas, the UN emblem, the coordinates cross), the two planting beds and
their trees, the south stepped terrace and its retaining walls, the 16 light standards,
the fountain and its octagonal well, Simón Bolívar and his pedestal, the obelisk, the two
flagpoles, the skate surface and its elements, the plaza's benches, game tables, fitness
station, planters, bins, bike racks, the Pit Stop kiosk, the BART/Muni portal heads and
elevator on the plaza, the Leavenworth arm with its fence, planting and dog run, and small
people clusters.

Do not include unrelated surrounding city geometry: **50 United Nations Plaza (the 1936
Federal Building), 1 United Nations Plaza, the Orpheum Theatre**, Civic Center Plaza, the
Main Library, the Asian Art Museum, Market/Hyde/Leavenworth/McAllister roadways or their
sidewalks, the Market Street transit lanes, street trees outside the plaza polygon, the
BART/Muni station box below, terrain, cameras or lights. Temporary context may appear in
review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ≈ 0; applied transforms; no
negative scales; outward normals; no duplicate or foreign geometry; no image textures; no
transparency; flat-color materials named `Toy_*` from the project palette; `_Glow` suffix
only on surfaces that glow at night; no `Toy_body`; no cameras, lights, animations,
armatures or constraints; no external dependencies; at most 18,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric`
in `app/src/assets.js` only scales and positions). Build directly in the measured `(e, n)`
plaza frame given in 2.3 and map to world X/Y once.

> **This plaza sits on TWO grids and both signs matter.** Its own axis is the Civic Center
> grid — **80.94° east / 260.94° west**, cross axis **350.94° north / 170.94° south** — the
> same frame `civic-center-plaza`, `sf-main-library` and `city-hall` are built in. Its
> south-east boundary is **Market Street at 45.20°**, measured on the Hyde→Larkin
> centreline that fronts the plaza. Those two differ by 35.74°, and mirroring either one
> about north produces a bounding box that measures identically while putting the plaza
> visibly out of true against its own block. `civic-center-plaza` shipped exactly that bug
> once (189.06 for 170.94). Check every bearing's SIGN against the neighbours, not against
> a bbox.

**Height normalization:** the tallest geometry in the export must land at exactly
**13.00 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0. The tallest
element is a tree crown, and 13.00 m is a *design* value, not a survey (2.15 risk 3) —
so drive it from a named constant, author exactly one crown to it, and assert it in the
validator. Every other vertical in the asset is an independently measured number and must
not be scaled to fit.

**Flatness caution:** every surface except the trees, the standards, the statue and the
obelisk is within 0.6 m of z = 0. Author the ground plate with real thickness (0.30 m to
the brick top, granite bands 0.32 m, beds 0.40 m) so the loader's merge does not z-fight
against the baked landcover, which sits at +0.06 m above terrain. The two OSM
`natural=sand` beds bake as landcover sand directly under this asset — the plate must
cover them.

**Ground-plane trap (this has cost a day before).** The app's loader seats an asset from
**one** terrain sample at its anchor, so a 220 m ground-plane asset on sloping terrain
floats at one end. Check the terrain drape across the whole footprint at integration and
record the result; do not discover it after approval. And note that `glb-optimize`'s weld
pass silently smooths flat shading on large coplanar faces — inspect the brick field after
stage 4, not just before it.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/un-plaza/build_un_plaza.py` (deterministic build script),
`artifacts/un-plaza/un-plaza.blend`, and `artifacts/un-plaza/un-plaza.glb`. The plaza
ring, the 16 light-standard positions, the fountain outline, the beds, the terrace, the
dog run and the UN emblem are **measured data, not invention** — they are already
committed at `artifacts/un-plaza/data/elements_en.json` with their OSM element ids, and
the script must read that file rather than eyeballing a grid. Tree positions are *not* in
OSM: digitise them from the aerial into `artifacts/un-plaza/data/trees_en.json` and commit
that alongside. Do not modify or rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `un-plaza-top.png`,
`-north.png`, `-east.png`, `-south.png`, `-west.png`, plus `un-plaza-contact-sheet.png`,
at least one high three-quarter aerial beauty render `un-plaza-aerial.png`, and a night
render `un-plaza-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation.

Two subject-specific requirements:

- **The top view is the primary review image for this asset.** It must clearly show the
  wedge, the brick field, the double colonnade, the two beds, the granite bands, the skate
  surface and the fountain. Render it larger than the elevations.
- Add one extra render, `un-plaza-axis.png`: a low three-quarter view looking **west along
  the Fulton axis** from the Market end. Frame it as if City Hall were at the far end.

Because the site is 221 m × 150 m and only 13 m tall, the elevations will be extremely
wide and mostly empty. Frame them to the plan dimension and accept the empty sky.

## Validate the exported GLB

Re-import `un-plaza.glb` into a fresh isolated Blender scene and validate the re-import,
not the source scene. Report object count, triangle count, dimensions, bounding-box
min/max, min Z, XY center offset, material names, image-texture count, camera count, light
count, animation count, applied-transform status, negative-scale status,
normal-orientation status, unexpected geometry, and per-material contract compliance.
Render at least one review image from the re-imported asset. Write
`artifacts/un-plaza/validation.json` and `artifacts/un-plaza/REPORT.md`.

Four subject-specific validator checks, in addition to the standard ones:

1. **`max_z == 13.00 ± 0.01`**, and the vertex achieving it belongs to a tree crown.
2. **Exactly 16 light standards**, at the `elements_en.json` positions within 0.05 m,
   globe tops at 5.90 m.
3. **XY bbox ≈ 215.3 × 158.0 m**, and the model's XY centre within 0.5 m of the origin.
   That bbox is the consequence of an L-shaped wedge across two grids, not a scale error.
4. **The Market-facing boundary measures 45.20° ± 0.15°** and the Fulton axis
   **80.94° ± 0.10°**, both signed.

The normals test needs care: this asset is a union of many separate closed solids (plate,
kerbs, bands, columns, crowns, blocks), so **per-object signed volume is the authoritative
check**; the whole-model ray test will show a small residual and ≤ 0.15% is the gate.

## Manifest draft

Verify the real WGS84 anchor yourself, then include this draft entry in `REPORT.md`. Do
not edit the production manifest in this task.

```json
{
  "id": "un-plaza",
  "file": "un-plaza.glb",
  "anchor": [
    -122.4138900,
    37.7801415
  ],
  "targetHeightM": 13.0,
  "cat": 0,
  "name": "United Nations Plaza",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`"estimated": true` is deliberate — the height datum is an authored tree crown, not a
published figure. See 2.15.

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`,
or any app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in
2.13 below.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Source | Confidence |
|---|---|---|---|
| Name | United Nations Plaza | OSM relation `1735771`, Wikidata `Q1311705` | verified |
| Location | Fulton Street alignment, Market Street to Hyde Street, plus closed Leavenworth Street north to McAllister | OSM; Wikipedia | verified |
| Address | none of its own; the brief's "355 McAllister St" is Civic Center Plaza (DataSF parcel `0788001`) | DataSF address point `288381-501940-325286`; manifest `civic-center-plaza` | verified — see 2.15 risk 1 |
| Created | 1975, dedicated for the UN Charter's 30th anniversary; constructed January–June 1975 | Wikipedia; TCLF | verified |
| Designers | Market Street Joint Venture Architects — Lawrence Halprin & Associates (Don Carter principal-in-charge, Angela Danadjieva landscape architect), Mario Ciampi and Associates, John Carl Warnecke & Associates | Wikipedia; TCLF | verified |
| Published area | 2.6 acres (Wikipedia infobox); 2.5 acres (TCLF) | Wikipedia; TCLF | verified, conflicting |
| Polygon area | 11,264 m² = **2.78 acres** | shoelace over OSM way `24588033` | measured |
| Plaza-frame extent | 220.81 m along the Fulton axis × 150.33 m across | this dossier, §2.3 | measured |
| World XY bbox | 215.27 m × 157.98 m | this dossier, §2.3 | measured |
| Anchor (XY bbox centre) | lon −122.4138900, lat 37.7801415 | reprojected from the ring | measured |
| Fulton axis | **80.94° / 260.94°** true; cross axis 350.94° / 170.94° | DataSF centrelines (McAllister reads 80.96° over 7 blocks); matches `civic-center-plaza` | measured |
| Market Street frontage | **45.20°** true | DataSF centreline `8752101` (Hyde→Larkin, 192.3 m), corroborated by the OSM ring's own 134.6 m Market edge at 45.18° | measured |
| Original paving | 117,000 ft² (10,900 m²) brick in a herringbone pattern, plus 20,000 ft² (1,900 m²) of lawn | Wikipedia | verified |
| Original planting | 192 London plane and black poplar trees along the Fulton promenade | Wikipedia | verified (1975 state) |
| Light standards | **16**, two rows of eight; rows 11.76 m apart, bays ~11.77 m with one 15.83 m centre bay | OSM `highway=street_lamp` nodes `13481539165`–`80` | measured (positions) |
| Light standard height | 5.90 m to the top of the globe | photogrammetry off a levelled photosphere, §2.3 | estimated ±0.5 m |
| Standards inscribed | names of UN member nations added 1995, updated 2005; original square semi-translucent luminaires replaced by frosted glass globes in 1995 | Wikipedia | verified |
| Fountain | Halprin with Ernest Born, 1975; 673 Sierra granite blocks; 165 ft (50 m) run; basin 100 ft (30 m) wide; cost $1.2 M | Wikipedia; SF Arts Commission accession `1975.29`; art&architecture-sf | verified |
| Fountain footprint | 40.1 × 21.5 m, 493 m² | OSM way `128534058` | measured |
| Fountain crest | **4.03 m** above plaza grade | DataSF LiDAR footprint `159394` (`hgt_maxcm` 403, `gnd_mediancm` 1349) | measured |
| Fountain status | still standing; repeatedly fenced (1978, 2003, 2018–19); removal proposed 1994 and 2003, rejected both times. **The 2025–26 SF fountain demolition is the Vaillancourt Fountain at Embarcadero Plaza, a different object** | Wikipedia; SF Chronicle Jan/Apr 2026 | verified |
| Obelisk | 17 ft (5.18 m) black granite, engraved 1995 with the preamble to the Universal Declaration of Human Rights | Wikipedia | verified |
| Walk of Great Ideas | 1995, $400,000; eight white granite paving stones inlaid in brass with the UN Charter preamble | Wikipedia; visible and legible in ground-level photography | verified |
| UN emblem | inlaid at the plaza centre, 1995; 4.6 m across at `(e −46.1, n −19.85)` — dead on the colonnade centreline, in the wide centre bay | OSM way `1470003860`; measured | measured |
| Coordinates cross | granite blocks inlaid with brass giving San Francisco's datum coordinates for distances to other cities, in the south-west of the plaza near Market | Wikipedia | verified |
| Simón Bolívar | bronze equestrian by Adamo Tadolini, gift of Venezuela; ~8.1 m overall on its pedestal, at `(e −101.15, n −20.17)` | OSM node `411095145`; TCLF; height photogrammetric | measured (position), estimated (height) |
| Farmers market | Heart of the City, Wednesdays and Sundays here 1981–2023; relocated to Fulton Plaza in 2023 | Wikipedia; SF Examiner Sep 2024 | verified |
| 2023 revitalization | $2 M, reopened 8 November 2023; Verde Design with SF Rec & Park, SF Public Works and the Civic Center CBD; CPRS Award of Excellence in Design 2024 | sfrecpark.org; SF Chronicle Nov 2023 | verified |
| Skate plaza | 13,000 ft² opened Nov 2023; +2,100 ft² in the north-east corner Feb 2025 with three geometric skateable art pieces by Alexis Sablone (with The Skatepark Project and Converse) | sf.gov Jan 2025; KQED; SFist | verified |
| Other 2023–25 additions | outdoor fitness station, chess and ping-pong tables, café seating, new trees, Tivoli/festoon lighting, dog run | sf.gov; sfrecpark.org; OSM `leisure=fitness_station`, `leisure=dog_park` | verified |
| Retained neighbours | only the Orpheum Theatre (1925), 1 United Nations Plaza (1932) and the Federal Building (1936) survived the plaza's construction | Wikipedia | verified |
| Historic status | contributes to the Civic Center NRHP district; independently eligible for the NRHP on design merit and for the California Register for its role in LGBTQ history | Wikipedia; SF Planning DPR 523B | verified |

### 2.2 Sources

- **OpenStreetMap, Overpass API** — the plaza multipolygon (relation `1735771`, outer way
  `24588033`, five inner rings), the 16 light-standard nodes, the fountain, both planting
  beds, the south terrace and its steps and retaining walls, the dog run, the UN emblem,
  Bolívar, the obelisk, the two flagpoles, the fitness station, the Pit Stop, the BART
  portals and the footway network. Everything marked *measured* above was computed from
  this pull. The raw pull and derived plaza-frame coordinates are committed under
  `artifacts/un-plaza/data/`.
- **DataSF** — street centrelines (`3psu-pn9h`) for the two grid bearings; LiDAR building
  footprints (`ynuv-fyni`) for the fountain's 4.03 m crest and the neighbours' heights;
  the address point and parcel (`ramy-di5m`, `acdm-wktn`) that identify 355 McAllister as
  Civic Center Plaza.
- **Wikipedia, *United Nations Plaza (San Francisco)*** — construction dates, designers,
  paving quantities, the 1995 and 2005 refurbishments, the Walk of Great Ideas, the
  obelisk, the fountain's block count and dimensions, the removal history, landmark status.
- **The Cultural Landscape Foundation** — *United Nations Plaza* and the Halprin Legacy
  microsite: the 1962–75 Market Street sequence, the tree-shaded inscribed columns, the
  Bolívar gift, the 1995 and 2005 rehabilitations.
- **SF Arts Commission**, civic art record `1975.29` — the fountain as an accessioned
  artwork, 165 ft long, granite.
- **sf.gov / SF Rec & Park / KQED / SFist / SF Chronicle / SF Examiner / NYT (May 2025)** —
  the 2023 revitalization and the 2023 and 2025 skate plaza phases.
- **SF Chronicle, January and April 2026** — the Vaillancourt Fountain removal, recorded
  here only to rule it out: it is a different fountain at a different plaza.
- **Google satellite imagery at z20** and a levelled Google photosphere at the plaza's
  Hyde end (`CIABIhBTIDVFCMu9Ia0rkJLR_mRK`) — the ground-plane layout, and the
  photogrammetric heights for the light standards and Bolívar.
- **The repo's own committed tiles** (`app/public/tiles/buildings/20_13.bin`) — the
  exclusion measurements in 2.13. This is the authoritative input, not OSM or DataSF.

### 2.3 Orientation and placement

The plaza is a wedge between two grids. All geometry is authored in a local `(e, n)` frame
on the **Civic Center grid** and mapped to world once:

```
e  = along the Fulton axis, POSITIVE TOWARD MARKET / EAST
     bearing  80.94 deg true    (west, toward City Hall, is 260.94)
n  = across the axis, POSITIVE TOWARD NORTH
     bearing 350.94 deg true    (south, toward Market, is 170.94)
e in [-108.7, +112.2]    n in [-76.5, +73.8]
world_x = e·sin(80.94°) + n·sin(350.94°)
world_y = e·cos(80.94°) + n·cos(350.94°)      (Blender +Y = north)
```

The origin is the **world-axis-aligned XY bbox centre**, `lon −122.4138900, lat 37.7801415`
— the point the asset contract requires the model to be centred on. It is *not* the area
centroid (`−122.4139525, 37.7799996`, 15.7 m south) and *not* a minimum-area OBB centre;
on an L-shaped wedge those three are different points and only the bbox centre satisfies
"origin at base center". Model Z = 0 is the surrounding sidewalk level; the brick top is
+0.30 m.

**Why 80.94° and not the ring's own 80.4°.** A least-squares fit over the OSM ring's long
edges gives 80.42°. DataSF's McAllister centrelines read **80.96°** across seven
consecutive blocks and Fulton (Hyde→Larkin) reads 81.12°; `civic-center-plaza`,
`sf-main-library` and `bill-graham-civic-auditorium` are all built on 80.94 / 350.94. The
0.5° gap is OSM digitising drift on this one polygon — 1.9 m of error at the plaza's east
end. Build on the grid. The Market edge is the opposite case: the ring's own 134.6 m
Market segment reads 45.18° against DataSF's 45.20° on the block that fronts the plaza, so
that boundary is trusted as drawn.

Measured plaza ring, in `(e, n)`, long edges only (the full 39-vertex ring, including the
Market-corner chamfers and the Leavenworth arm, is in `data/elements_en.json`):

```
(  38.83,  73.80) (  39.47,  18.24) (  58.97,  18.22) (  71.91,  19.64) (  81.19,  23.68)
( 112.16,  19.86) ( 107.24,  16.31) (  -1.99, -62.36) ( -21.70, -76.53) ( -27.63, -70.97)
( -47.46, -43.67) (-106.81, -44.31) (-108.65, -38.72) (-108.49,  -2.23) (-107.02,   3.34)
(   2.61,   4.32) (  30.72,  73.73)
```

Measured element layout, all in `(e, n)`:

| Element | Extent |
|---|---|
| Promenade block | n from +3.8 (Federal Building line) to −44.0 (Market-side walk), e −107 → +2.6 |
| **Colonnade centreline** | n = −19.83 |
| Light standards, north row | n = −13.95; e = −90.04, −78.26, −66.50, −54.73, −38.90, −27.12, −15.43, −3.55 |
| Light standards, south row | n = −25.71; e = −90.03, −78.25, −66.50, −54.73, −38.90, −27.11, −15.42, −3.55 |
| Planting bed, north-west | e ∈ [−94.7, −54.0], n ∈ [−10.5, 0.0] — 423 m², decomposed granite |
| Planting bed, south-west | e ∈ [−94.8, −53.8], n ∈ [−39.8, −29.9] — 400 m², decomposed granite |
| Planting bed, north-central | e ∈ [−37.7, +1.4], n ∈ [−10.2, +0.1] — 396 m² (OSM's mis-tagged "skate pitch") |
| South stepped terrace | e ∈ [−37.4, +0.6], n ∈ [−51.3, −28.7] — 652 m²; retaining walls at n −34.0 and n −48.9→−42.6; three step lines at n = −35.5, −37.0, −38.6 spanning e −37.4 → −18.1 |
| UN emblem roundel | centre (−46.1, −19.85), 4.6 m across |
| Simón Bolívar | (−101.15, −20.17) |
| Obelisk | (−74.65, −5.88) |
| Flagpole (UN) | (5.55, −30.69) |
| Flagpole (US) | (5.63, −7.98) |
| Fountain | e ∈ [22.7, 62.8], n ∈ [−7.4, +14.1] — 493 m², crest +4.03 m |
| Fitness station | (−58.36, −35.49) |
| Pit Stop toilet | (74.17, 1.85) |
| Bike share dock | (88.11, 9.96) |
| Bike racks | (−72.78, −31.02), (−34.59, −60.81), (37.10, −30.20), (79.63, 2.56) |
| BART/Muni elevator head | e ∈ [6.8, 10.2], n ∈ [−50.2, −46.7] |
| Leavenworth arm | e ∈ [21, 39], n ∈ [+16, +75]; dog run e ∈ [21.0, 30.7], n ∈ [28.6, 58.3] (275 m², fenced) |
| Mapped trees (NE corner only) | (70.45, 15.13), (81.71, 13.24), (69.53, 1.06), (74.40, −4.38) |

Note the composition this table describes, because it is the whole design: a 47.8 m deep
promenade block, symmetric about n = −19.9, with a 10 m planting bed along each long edge,
a 20 m brick corridor between them, and the two column rows set 4 m in from each bed. Then
the wedge opens out east of e ≈ 0 into the Market-facing forecourt, and the fountain sits
in it, off the axis to the north. The plaza is *not* symmetric end to end and should not
be built as if it were.

**The light standards carry real survey jitter** (rows read −13.85 to −14.07 and −25.62 to
−25.84; bays 11.69 to 11.88 m). Keep it. A perfectly ruled colonnade is the single easiest
way to make this asset look procedural rather than surveyed.

**Photogrammetric heights.** Measured off the levelled photosphere at the Hyde end
(equirect, horizon on the centre row, elevation = `(H/2 − y)/H × 180°`, per the repo's
Street View recipe). The camera resects to `(e −93.6, n −19.85)` from the 117.4° the
nearest column pair subtends at 11.76 m separation, i.e. 6.88 m to each column. That gives
a 0.74 m square shaft — the right order for a Halprin column — and a globe top 3.65 m
above the lens. The same pano puts Bolívar's overall height at 8.08 m from a 7.5 m
baseline, which matches the published order for that equestrian and is what validates the
camera solution. Column height is quoted as **5.90 m ± 0.5**; it is not the height datum,
so an error here does not rescale the plaza.

### 2.4 What each side shows

- **South-east (Market Street).** The plaza's front door: the 134.6 m diagonal frontage at
  45.20°, the BART/Muni portal heads and elevator, the coordinates cross in the paving, and
  the stepped terrace rising away from the street. Busiest edge, most people, most furniture.
- **South-west (Hyde Street).** The ceremonial end: Bolívar on his pedestal closing the
  axis, the two westernmost columns flanking him, the broad granite Walk band underfoot.
  Short, symmetric, and the elevation that explains the plaza's ceremonial claim.
- **North (50 UN Plaza).** A 110 m straight edge against the Federal Building's flank —
  a walk, the north planting bed, and the north column row behind it. The quietest edge.
  Nothing of the Federal Building belongs in this asset.
- **East / north-east (Leavenworth, 7th at Market).** The fountain, the Pit Stop, the bike
  dock, the four mapped trees, and the narrow planted Leavenworth arm running north.
- **Above.** The composition: a **red wedge** with a pale granite band across its waist, a
  dark-green bed along each side of the promenade, sixteen white dots in two ranks down
  the axis, a pale grey pile at the Market end, and a pale skate surface in the middle. If
  the top view does not read as red-with-a-white-colonnade at 600 m, the asset has failed.

### 2.5 Recognition cues (ranked)

1. **The red brick field.** A colour cue, not a shape cue, and the only one that works at
   any distance. Nothing else this size in San Francisco is red.
2. **The double colonnade of sixteen globe-topped columns** marching down the Fulton axis.
3. **The wedge** — a plaza that is visibly a leftover triangle between Market's grid and
   the Civic Center's, with the 35.74° cut on its Market side.
4. **The sunken granite fountain** at the Market end: a pale, blocky, deliberately
   chaotic pile in a dark octagonal well.
5. **The pale granite bands** — the Walk of Great Ideas across the brick and the UN emblem
   roundel dead on the centreline.
6. **Bolívar** closing the west end, and the double row of dark-green beds framing the walk.

### 2.6 Miniature translation

- **Brick, not texture.** `Toy_brick` flat, with the joint pattern cut as a shallow
  recessed grid (0.02 m) in two tones — never an image texture, never per-brick geometry.
  The herringbone reads at aerial distance as a directional grain; do it as a coarse
  diagonal joint grid at ~2.4 m pitch, not as bricks.
- **Chunky columns.** 0.75 m square shafts with a 0.12 m bevel, a plain cap, a 0.62 m
  sphere on top. Do not model the inscribed nation names; suggest them with one recessed
  band per shaft.
- **The fountain as a toy.** Nine to twelve chunky bevelled slabs at three or four
  heights, stacked asymmetrically inside a sunken octagon with a stepped rim. It should
  read as *deliberately blocky*, which is exactly what the real one is. Do not attempt 673
  blocks and do not attempt water jets.
- **Trees as pruned street planes**, in the ccplaza family: a knuckled trunk under a wide
  slightly flattened crown. `Toy_verdigris` crowns so they separate from the brick.
- **The skate surface as one pale concrete pad** with four or five low bevelled
  ledges/banks and three geometric art blocks in accent colour. It is a 2023 layer on a
  1975 plaza and should read as an inserted object, not as part of the paving.

### 2.7 Massing recipe

1. **Ground plate** — extrude the 39-vertex ring 0.30 m, bevel the top edge 0.06 m, kerb
   the perimeter in `Toy_stone`. This is the asset's floor and every other element sits on
   it.
2. **Joint grid** — inset the brick field into bays and recess the joints 0.02 m. Two
   tones of `Toy_brick` alternating by bay, ~8% apart in value.
3. **Granite inlays** — the Walk of Great Ideas as a 6 m wide `Toy_stone` band crossing
   the promenade near the Hyde end at +0.32 m, the UN emblem roundel at (−46.1, −19.85),
   the coordinates cross in the Market corner. Flush, not proud: these are inlays.
4. **Planting beds** — three slabs at +0.40 m in `Toy_sand`, kerbed in `Toy_stone`.
5. **South terrace** — the 652 m² platform with its retaining walls and three step lines,
   descending 1.5 m toward Market in three treads.
6. **Colonnade** — 16 columns from the measured table, shaft `Toy_stone`, globe
   `Toy_white` / `Toy_white_Glow`.
7. **Fountain** — sunken octagon (well floor at −2.4 m, rim at +0.45 m), 10–12 slabs to a
   crest of exactly 4.03 m, all `Toy_stone` with one `Toy_ink` shadow face.
8. **Monuments** — Bolívar (pedestal `Toy_stone`, figure `Toy_verdigris` bronze) at
   8.10 m; obelisk (`Toy_ink`) at 5.18 m; two flagpoles (`Toy_steel`) at 12.0 m with flat
   slab flags.
9. **Skate layer** — one `Toy_cream` pad, low ledges, three `Toy_teal` / `Toy_coral` /
   `Toy_mustard` geometric blocks.
10. **Trees** — from `data/trees_en.json`; exactly one crown authored to 13.00 m.
11. **Furniture and life** — benches, game tables, fitness frame, planters, bins, racks,
    the Pit Stop, portal heads, festoon-light catenaries, and four people clusters.
12. **Leavenworth arm** — raised planted strip at +0.40 m, fence, dog-run gate, five trees.

### 2.8 Materials and palette

All from the project palette in `.agents/skills/sf-asset-check/SKILL.md`.

| Material | Hex | Used for |
|---|---|---|
| `Toy_brick` | `c96f4a` | the brick field — the asset's dominant colour |
| `Toy_rust` | `a86444` | the second brick tone (alternating bays, joint recesses) and tree trunks |
| `Toy_stone` | `d9d2c2` | granite: kerbs, the Walk band, the emblem, column shafts, fountain slabs, Bolívar's pedestal, terrace walls |
| `Toy_cream` | `f2ede3` | the skate pad and the main cross-walks — a half-tone lighter than the granite so the 2023 layer reads as inserted |
| `Toy_sand` | `ece4d4` | the three decomposed-granite planting beds |
| `Toy_verdigris` | `9fb8a8` | tree crowns and the Bolívar bronze |
| `Toy_mint` | `8fd0a8` | the dog run's turf and the small lawn remnant |
| `Toy_white` | `f7f4ec` | the sixteen globe luminaires |
| `Toy_steel` | `9aa0a6` | flagpoles, fence, bike racks, festoon catenaries, railings |
| `Toy_ink` | `3a3530` | the obelisk, joint shadow, the fountain well's shaded faces |
| `Toy_roofd` | `45454a` | bench slats, bins, game-table tops, portal heads |
| `Toy_teal` / `Toy_coral` / `Toy_mustard` | `3fa8a0` / `e8735a` / `d9a441` | the three skateable art blocks — the plaza's only saturated accents |
| `Toy_navy` / `Toy_red` | `2c4a70` / `c4453c` | the two flags, as flat slabs with no devices |

**Night state** (`_Glow` variants, required by stage 2 of the pipeline):

- `Toy_white_Glow` — **the sixteen globes are the hero glow.** At night the plaza becomes
  two dotted lines of warm points running down the Fulton axis, which is precisely what
  the real place does and is unmistakable from the aerial camera.
- `Toy_cream_Glow` — a thin catenary of festoon lights over the promenade (the 2023
  Tivoli lighting), and a low wash on the skate pad.
- `Toy_teal_Glow` — one restrained accent on the BART/Muni portal head at the Market end.

Nothing else glows. The brick, the beds and the fountain go dark, and that contrast is the
point. Every `_Glow` surface is a **thin shell proud of its opaque parent**, never the
parent itself, and its day colour matches its non-glow neighbour — a closed glow shell is
two alpha layers and reads at roughly 23% by day, not 12%, which will tint the brick.

### 2.9 Top surface

The top surface *is* the asset, so §2.7 is the answer. The one rule worth restating: judged
from the app's high three-quarter camera at 400–800 m, the plaza must resolve into six
shapes — one red wedge, two dark-green bars, one pale granite band, one pale skate pad,
one pale grey pile. If any of those six merges into its neighbour, increase the tonal
separation before adding any detail.

### 2.10 Scope

**In:** the plaza polygon and everything standing on it, as listed in Part 1.

**Out:** 50 United Nations Plaza (the Federal Building), 1 United Nations Plaza, the
Orpheum Theatre, Civic Center Plaza, the Main Library, the Asian Art Museum, Market,
Hyde, Leavenworth and McAllister roadways with their sidewalks, transit lanes and street
trees, the BART/Muni station box below the plaza, terrain, cameras, lights.

**Deliberately omitted despite being on site:** the individual inscriptions on the columns
and on the Walk of Great Ideas (suggested as recessed bands, never lettered); the 673
individual fountain blocks; the farmers-market stalls, which left for Fulton Plaza in 2023
and would date the model; food trucks and event tents; individual hydrants, cabinets and
sign poles.

### 2.11 Triangle budget

| Group | Count | Tris each | Tris |
|---|---:|---:|---:|
| Ground plate + kerb + joint grid | 1 | — | 1,600 |
| Granite inlays (Walk band, emblem, cross, walks) | ~14 | ~40 | 560 |
| Planting beds + kerbs | 3 | ~120 | 360 |
| South terrace, walls and steps | 1 | — | 700 |
| Light standards (shaft 60 + cap 24 + globe 96) | 16 | 180 | 2,880 |
| Trees (trunk 20 + crown 28) | ~60 | 48 | 2,880 |
| Fountain (well, rim, 12 slabs) | 1 | — | 1,500 |
| Simón Bolívar + pedestal | 1 | — | 700 |
| Obelisk, 2 flagpoles + flags | 3 | ~90 | 270 |
| Skate pad, ledges, 3 art blocks | 1 | — | 900 |
| Benches, game tables, planters, bins, racks | ~40 | 30 | 1,200 |
| Pit Stop, portal heads, elevator | 4 | ~150 | 600 |
| Festoon catenaries | 6 | ~40 | 240 |
| Leavenworth arm (strip, fence, dog run) | 1 | — | 900 |
| People clusters | 4 | ~90 | 360 |
| | | **total** | **≈ 15,650** |

Cap 18,000; hard gate 30,000 (PERF-PLAN #9). The trees and the columns are 37% of the
budget together. If the count runs over, drop the globe from 96 tris to 60 (−576) and the
crowns from ten sides to eight before touching the ground plate — the plate's joint grid
is what stops the plaza reading as a red slab and is the last thing to cut.

### 2.12 Draft manifest entry

```json
{
  "id": "un-plaza",
  "file": "un-plaza.glb",
  "anchor": [
    -122.4138900,
    37.7801415
  ],
  "targetHeightM": 13.0,
  "cat": 0,
  "name": "United Nations Plaza",
  "estimated": true,
  "dims": [
    215.27,
    157.98,
    13.0
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`loadRadius` is the default rule's floor, `max(2500, 13 × 30) = 2500`. Beyond it the site
is empty ground — which for a plaza is the least illegible absence in the set, and the
fountain blocks that currently stand there will have been excluded. `alwaysLoaded` is not
justified: this is not a skyline piece.

### 2.13 Integration notes (for later, not this task)

**Case B — new landmark.** There is no `unPlaza` in `pipeline/lib/landmarks.mjs` or
`app/src/landmarks.js`, so integration needs a registry entry and a tile re-bake.

**The exclusion cannot be a circle at the anchor.** Measured against the committed bake
input (`app/public/tiles/buildings/20_13.bin`), the gate being
`dist(centroid, ZONE) < r || any dist(vertex, ZONE) < r`:

| From the ANCHOR | Distance | What it is |
|---|---:|---|
| nearest neighbour vertex | **4.76 m** | 50 UN Plaza, the Federal Building (7,586 m², baked 35.4 m tall) |
| farthest fountain block still needing to be dropped | **57.51 m** | the fountain's granite mass |

There is no radius that satisfies both, because the anchor is the bbox centre of an
L-shaped wedge and lands 4 m off the Federal Building's frontage. Use `extraExclusions`.

**Seven baked footprints stand inside the plaza and all seven are the fountain.** DataSF's
LiDAR captured the granite slabs as buildings; the procedural builder — with no
`hgt_medcm` to work from — extruded them to 3.1–8.5 m. Seven phantom blocks up to 8.5 m
tall stand in the plaza in the current build, and **the asset cannot be judged before the
re-bake**:

| Baked footprint | Area | Extruded height | Position `(e, n)` |
|---|---:|---:|---|
| `20_13#180` | 51 m² | 4.1 m | (31.0, 8.4) |
| `20_13#171` | 20 m² | 8.5 m | (40.7, −2.3) |
| `20_13#172` | 12 m² | 8.5 m | (40.4, 11.2) |
| `20_13#170` | 23 m² | 8.5 m | (49.0, −0.3) |
| `20_13#182` | 25 m² | 3.1 m | (53.2, 10.4) |
| `20_13#169` | 18 m² | 8.4 m | (59.2, 6.4) |
| `20_13#181` | 15 m² | 3.1 m | (58.7, 11.9) |

One circle clears all seven. Optimised over the tile, the centre that maximises the band is
`(e 48.10, n −14.80)` = **lon −122.4133237, lat 37.7800778**, with a band of
**(25.77, 34.76) m** — 9.0 m wide, which is roomy by this repo's standards. The ceiling is
`20_13#17` (1,171 m², 43.1 m tall) north-east of the fountain, at 34.76 m; the runner-up is
`20_13#36` at 34.81 m. **Ship r = 30.** It clears the last fountain block by 4.2 m and
spares the nearest real building by 4.8 m.

**No `exclude` at the anchor.** The anchor circle's ceiling is 4.76 m, which would drop
nothing and risk the Federal Building; omit the field, as `pipeline/lib/landmarks.mjs`
allows and as the vacant-parcel precedent established. Two footprints do overlap the plaza
ring by slivers — the Federal Building by 0.5 m and a Market-side neighbour by 0.3 m —
which is survey noise between two different polygon sources, not a building standing in
the plaza. Leave them.

**No `clearTrees`.** Checked, and worth recording because every other plaza in this set
needed it: `pipeline/landcover.mjs` scatters trees only on `KIND.trees` and `KIND.grass`.
UN Plaza's outer polygon is `highway=pedestrian` + `place=square`, which maps to no
landcover kind at all, and its inner rings are `natural=sand` and `leisure=pitch`. Nothing
scatters here. Confirm against the re-bake rather than taking it on trust.

Draft registry entry:

```js
{
  // An L-shaped wedge, not a building. The anchor is the bbox centre and lands
  // 4.76 m off the Federal Building's baked footprint, so there is no usable
  // radius at the anchor at all — `exclude` is omitted and the work is done by
  // one extra circle over the fountain. DataSF's LiDAR read the fountain's
  // granite slabs as seven buildings and the procedural builder extruded them
  // to 3.1-8.5 m; r = 30 at (-122.4133237, 37.7800778) drops all seven (band
  // 25.77-34.76 m, measured against buildings/20_13.bin) and spares the
  // 43 m neighbour north-east of it by 4.8 m.
  id: 'unPlaza',
  name: 'United Nations Plaza',
  lon: -122.4138900,
  lat: 37.7801415,
  height: 13.0,
  extraExclusions: [{ lon: -122.4133237, lat: 37.7800778, r: 30 }],
  camera: { distance: 520, yaw: 90, pitch: 28 },
}
```

The camera preset looks **west along the Fulton axis** (yaw 90, the same convention
`civic-center-plaza` uses for the same bearing) so the fly-to lands on the plaza's own
axis with City Hall beyond the far end — the composition the plaza was built to create,
and the NRHP nomination's own description of what it is for.

**Ground-plane seating.** The loader seats an asset from one terrain sample at its anchor.
This asset is 215 m across, and the anchor sits near its north-east corner rather than in
the middle of the promenade. Measure the terrain drape across the whole footprint during
local QA and record it; if the west end floats or sinks, that is a placement problem to
solve at integration, not an asset defect.

**Batch mode applies.** A Case B re-bake rewrites ~600 generated files; run the bake, do
the full Step 5/6 QA on it, then `git checkout -- app/public/tiles api/_data` and commit
source only, per `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

### 2.14 Validation checklist

- [ ] Binary GLB, real metres, applied transforms, no negative scales
- [ ] `min_z ≈ 0`, XY centre within 0.5 m of the origin
- [ ] `max_z == 13.00 ± 0.01`, achieved by a tree crown
- [ ] XY bbox ≈ 215.3 × 158.0 m (the two-grid wedge, not a scale error)
- [ ] Fulton axis 80.94° ± 0.10 and Market frontage 45.20° ± 0.15, both signed
- [ ] ≤ 18,000 triangles; ≤ 500 KB compressed
- [ ] Exactly 16 light standards at the `elements_en.json` positions within 0.05 m,
      globe tops at 5.90 m, row jitter preserved
- [ ] Fountain crest exactly 4.03 m; well floor −2.4 m
- [ ] Bolívar 8.10 m, obelisk 5.18 m
- [ ] All materials `Toy_*` and in the palette; no textures, no transparency, no `Toy_body`
- [ ] `_Glow` materials present, all thin shells proud of an opaque parent, day colours
      matching their non-glow neighbours
- [ ] No cameras, lights, animations, armatures, constraints, or foreign geometry
- [ ] Per-object signed-volume normals test clean; whole-model ray residual ≤ 0.15%
- [ ] Top view resolves into the six shapes of §2.9 and reads **red** at 600 m
- [ ] Night render shows two dotted lines of globes on a dark field, not a glowing slab
- [ ] After stage 4: the brick field's flat shading survived the optimizer's weld

### 2.16 What integration changed (added after the fact)

This section records the four things stage 5 found that this plan did not
predict. It is written here rather than only in `artifacts/un-plaza/REPORT.md`
because the next ground-plane plan in this set should start from it.

1. **The asset had to become terrain-draped, and the plan only flagged the risk
   rather than budgeting for it.** §2.13's "ground-plane seating" note said to
   measure the drape at integration. Measured: the terrain runs 13.06–16.64 m
   under the plaza while the anchor sits at 15.119 m, so a flat plate seated at
   the anchor is **buried 1.52 m at the Hyde end and floats 2.06 m** over the
   south side of the promenade. That is not a placement tweak — it is a rebuild,
   and it moved `targetHeightM` from an architectural height to a vertical
   extent. **A ground-plane plan should specify the drape up front**, as
   `424-brannan` does, not list it as a risk.
2. **Drape to a PLANE, not to the sampled grid.** The grid hugs the heightmap
   exactly but is piecewise-bilinear and therefore not affine, so draping a thin
   slab's vertices on it folds the slab: `skate_pad`, a 0.06 m inlay spanning
   50 m, came out with an inverted signed volume and the paving clearance
   spread to 0.37 m. A plane shear maps planes to planes and every prism stayed
   valid. Cost: a 0.373 m RMS residual in-ring, whose 2.0 m maximum is a single
   ~20 m Terrarium DEM dip over the Civic Center station excavation — a hole in
   the elevation data, not topography.
3. **`verify-rebake.mjs` had no model for a landmark with no anchor exclusion.**
   It compared `4.8 m vs undefined m radius` and reported FAIL. `unPlaza` is the
   first landmark whose work is done entirely by `extraExclusions`, so the tool
   gained a guard (one `if`), and the substantive question — is anything
   standing under the asset — was answered by point-in-polygon against the real
   footprint, which is what ADDRESS-TO-ASSET asks for anyway.
4. **The shared landmark `BatchedMesh` is at 91.2% with this landmark in it**
   (1,459,122 of 1,600,000 body vertices, all 103 generic landmarks resident;
   un-plaza contributes 26,730, i.e. 1.7%). A clean load places all 96 with
   `failed: 0`, but repeated release/re-add churn fragments the reserve and drops
   landmarks with `Reserved space request exceeds the maximum buffer size`.
   That is the pre-existing condition `sf3d-landmark-batch-full` records, not a
   defect in this asset — but **the batch integrator should re-check the reserve
   before adding many more**, and the headroom number above is the one to watch.

### 2.15 Open questions and risks

1. **The brief named the wrong site.** "UN Plaza, 355 McAllister St" conflates two
   different plazas: 355 McAllister is Civic Center Plaza (DataSF parcel `0788001`,
   centroid `−122.41760, 37.77948`), which is already integrated as `civic-center-plaza`
   at that exact anchor. United Nations Plaza is 340 m east and has no McAllister
   frontage. This plan builds United Nations Plaza, because the alternative reading is a
   landmark that already exists. If that is wrong, stop before stage 2 — nothing after
   Gate 1 is cheap to redo.
2. **The available imagery predates the site's current state.** Google's and Esri's z20
   imagery of this block both show the pre-November-2023 plaza: farmers-market ground,
   decomposed-granite beds where the skate plaza now is, no game tables. OSM's *tags* are
   current (`sport=skateboard`, `leisure=dog_park`, `leisure=fitness_station`) but its
   *geometry* for the skate area is the old bed outline, and 396 m² is far short of the
   published 13,000 ft² (1,208 m²). **The 1975 bones — brick, colonnade, beds, fountain,
   Walk, emblem, Bolívar — are measured and safe. The 2023–25 layer is placed from news
   photography and is the least certain part of this asset.** Re-check it against recent
   photography before building, and expect to revise it.
3. **The height datum is an authored tree crown, not a survey.** No element of this plaza
   has a published height. 13.00 m is a design value in the range mature London planes
   occupy, chosen so the tallest geometry is a *broad* object rather than a thin pole —
   the failure mode `civic-center-plaza` §2.15 risk 1 warns about, where a 1% error in a
   flagpole rescales the whole ground plane. Because `targetHeightM` is set equal to the
   model's authored maximum, the loader's scale is exactly 1.0 and the ground plane is
   correct *by construction*, whatever the real trees measure. The manifest is marked
   `"estimated": true` to say so.
4. **The light standards' 5.90 m is photogrammetric, ±0.5 m.** The camera was resected from
   the pano itself rather than trusted from its reported lat/lon, and the solution is
   corroborated by Bolívar coming out at 8.08 m from the same frame. It is good enough for
   a miniature and it is not load-bearing on scale. If a published figure surfaces, change
   the constant and re-export.
5. **Acreage disagrees across sources** (2.5 / 2.6 published, 2.78 measured). The model is
   built on the OSM polygon because that is the polygon the pipeline's landcover and
   exclusion already use, so the model and the baked city agree with each other even if
   they both differ slightly from the published figure. Recorded, not resolved.
6. **The fountain is politically live.** It has been proposed for removal in 1994, 2003 and
   2018, fenced off three times, and survives at the time of writing; the 2019 Civic Center
   Public Realm concept would partly fill it and plant it. Model it as it stands. Do not
   confuse it with the Vaillancourt Fountain at Embarcadero Plaza, whose disassembly began
   in April 2026 — a different artwork at a different plaza, and the first thing a search
   for "SF fountain removal" returns.
7. **The Leavenworth arm is 9 m wide and 56 m long, and it sets the model's Y bbox.**
   Including it costs 8 m of otherwise empty bounding box in each direction and moves the
   anchor north-east, off the promenade. It is included anyway because it is part of the
   polygon the pipeline uses and because the dog run is a real 2023 feature; but if a later
   pass wants a tighter asset, dropping the arm is the one scope cut available, and it
   would move the anchor.
8. **`docs/asset-plans/README.md` says parks are planned in `docs/plans/parks/`.** UN Plaza
   is treated as a landmark on the same argument the README already records for
   `civic-center-plaza`: a designed hardscape with a fixed surveyed layout and no natural
   component. Add its row to the README table with this plan.
