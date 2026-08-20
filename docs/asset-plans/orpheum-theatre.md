# Orpheum Theatre — SF-SIM asset plan

B. Marcus Priteca's 1926 Pantages Theatre at 1192 Market Street: a Plateresque
(late Spanish Gothic) terra-cotta pile on the triangular block where Market, Hyde
and Grove meet, with the most encrusted theatre facade left on Market Street, a
red mission-tile eave, a dark-green blade sign eight storeys tall spelling
ORPHEUM down the front, and a flat-roofed 1998 stage house standing clear of
everything at the back. The sign and the marquee under it are the whole asset's
identity.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/orpheum-theatre/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `orpheum-theatre` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4146109, 37.7793187` (measured footprint AABB centre, OSM way/35115840) |
| Target height | **27.2 m** — stage-house roof (2010 city LiDAR `hgt_max` 27.19 m, corroborated by the published 75 ft grid); Market-block eave 23.3 m, blade-sign crown ~25.7 m |
| OSM footprint | 64.74 m E–W x 74.99 m N–S axis-aligned; 2,967 m² polygon; Market frontage bears **45.9°** cw from N, Hyde flank **171.5°** |
| Triangle cap | 24,000 |
| Category | `17` (theater / cinema) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Orpheum Theatre GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the Orpheum Theatre (1192 Market Street,
San Francisco) and deliver it as a downloadable, validated GLB.

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
7. `artifacts/civic-center-courthouse/` and `artifacts/sf-main-library/` — the two
   nearest reference implementations of this exact deliverable; the Main Library is
   the Orpheum's neighbour across Hyde Street and sets the scale it will be judged at
8. `docs/asset-plans/orpheum-theatre.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The **vertical ORPHEUM blade sign** — dark green, gold-edged, an ornate crown on
  top, white bulb letters reading down the facade, projecting from the entrance bay
  and rising clear of the tile eave. This is the single recognition cue and it must
  read at thumbnail size.
- The **marquee** below it: a dark-green boxed canopy with a lit soffit, a poster
  panel above it, and "ORPHEUM THEATRE" on its fascia.
- The **encrusted Plateresque entrance bay** the sign hangs on: a taller, more
  ornamented slice of the frontage with a crested gable above the eave.
- The **cream terra-cotta street front**: a ground-floor arcade of round arches on
  barley-twist columns, tall glazed upper storeys in ornamented piers, a heavy
  ornament band, and a projecting **red mission-tile pent roof** with a low parapet
  above it.
- The **step down along Market**: three glazed storeys plus arcade on the Hyde/Grove
  corner block, two plus arcade on the north-east wing.
- The **big hipped auditorium roof** filling the centre and north of the block, and
  the **flat-roofed stage house** standing highest at the north-east corner.
- A designed roof generally: tile eaves on the street sides, the hip, the plant-filled
  valley between them, and the stage house — the camera looks down.

## Research the Orpheum independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor and the real-world orientation,
and gather references covering:

- Market Street (south-east) elevation, the Hyde Street (west) flank, the Grove
  Street (north) side and the north-east party wall
- Aerial and roof/top views
- Ground-level views, day and night — the sign and marquee are lit
- The 1926 drawings: a set of Priteca blueprints is in the Gary Parks collection and
  about 30 images of the drawings are reproduced on the San Francisco Theatres blog
- Whether OSM's `height=46 m` is the building (it is **not** — see 2.15)
- Which element carries the LiDAR maximum: stage house, corner block, or blade sign

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

## Create a reference dossier

Write `artifacts/orpheum-theatre/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the 3-5 strongest recognition cues; features to preserve; features to
simplify; uncertainties and conflicting evidence. A contact sheet of attributed
reference thumbnails is welcome if legally permissible — do not commit copyrighted
full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade into
broad rhythms, deliberately design every surface visible from above, evaluate from the
app's high three-quarter aerial camera, then simplify again.

The finished asset must be immediately recognizable as the Orpheum, consistent with the
real building from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and
never accurate in one view while invented in the others.

The hard call here is ornament. The real facade is a continuous crust of Plateresque
relief; modelled literally it is 100k triangles of noise that dissolves to grey mush at
the app's altitude. Translate it into **rhythm and depth**, not detail: pier/bay
spacing, a proud ornament band under the eave, recessed window reveals, and the crested
gable on the entrance bay. Spend the whole personality budget on the blade sign, the
marquee and the tile roof. It has to sit convincingly beside `sf-main-library`,
`asian-art-museum` and `civic-center-courthouse`, which are already in the scene and
are all calm pale masses — the Orpheum is allowed to be the one with a sign on it, and
nothing else.

## Scope of the exported asset

Export the Orpheum block only: street-front wings, entrance bay, marquee, blade sign,
auditorium roof, stage house, tile eaves and roof plant.

Do not include unrelated surrounding city geometry: the City College building next door
at 1170 Market, the Main Library across Hyde, United Nations Plaza, Market/Hyde/Grove
streets, the Muni/BART station entrances, trees, people, vehicles, plinths, cameras or
lights. Temporary context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project palette;
`_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no cameras, lights,
animations, armatures or constraints; no external dependencies; at most 24,000
triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric`
in `app/src/assets.js` only scales and positions). The Market Street frontage bears
**45.9° cw from true north** and faces **south-east**; the Hyde Street flank bears
171.5°. The contract's "front faces −Y" rule therefore cannot be honoured literally on
this site — the front faces −Y+X at 135.9°. Record that decision and the measured
heading in `REPORT.md`.

**The blade sign must not be the tallest thing in the model.** Its crown sits at
~26.0 m; the stage-house roof at 27.2 m is the bbox top, so that the manifest's
`targetHeightM` is a measured building height and the loader's scale lands at 1.0.

## Reproducible Blender workflow

Headless only: `blender -b --python script.py -- args`; no GPU, so use Workbench or CPU
Cycles. Keep `artifacts/orpheum-theatre/build_orpheum_theatre.py` (deterministic build
script), `artifacts/orpheum-theatre/orpheum-theatre.blend`, and
`artifacts/orpheum-theatre/orpheum-theatre.glb`. The script must rebuild the model
reliably enough for future revision. Do not modify or rename an unrelated existing GLB
to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `orpheum-theatre-top.png`,
`-north.png`, `-east.png`, `-south.png`, `-west.png`, plus `-contact-sheet.png`, at
least one high three-quarter aerial beauty render `-aerial.png`, and a night render
`-night.png` showing the glow set.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation;
the top view must clearly show the tile eaves, the hipped auditorium roof, the roof
plant and the stage house; the aerial view uses the style bible's camera assumptions
(30-50 degrees down, long lens). Simple tabletop lighting, neutral warm background,
minimal depth of field, and every image must depict the same exported model.

## Validate the exported GLB

Re-import `orpheum-theatre.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Render at least one review image from the re-imported asset. Write
`artifacts/orpheum-theatre/validation.json` and `artifacts/orpheum-theatre/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "orpheum-theatre",
  "file": "orpheum-theatre.glb",
  "anchor": [
    -122.4146109,
    37.7793187
  ],
  "targetHeightM": 27.2,
  "cat": 17,
  "name": "Orpheum Theatre",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`,
or any app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in
`docs/asset-plans/orpheum-theatre.md`.
````

---

## Part 2 — Research and design dossier

Compiled 19 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify anything
it relies on.

### 2.1 Verified facts

| Fact | Value | Source |
|---|---|---|
| Official name | Orpheum Theatre (opened as the Pantages Theatre; the block is the Marshall Square Building) | Wikipedia, SF Theatres blog |
| Address | 1192 Market Street at Hyde, Grove and 8th, Civic Center | OSM, Wikipedia |
| OSM element | way/35115840, `name=Orpheum Building`, `building=commercial`, `heritage:ref=94`, wikidata Q121306407 | Overpass |
| Opened | 20 February 1926 | SF Theatres blog (Chronicle 1926), PCAD |
| Architect | B. Marcus Priteca, for Alexander Pantages; developer William Wagnon | SF Landmarks Final Case Report, PCAD |
| Style | Plateresque / late Spanish Gothic terra-cotta, facade patterned on a Spanish cathedral | Wikipedia, Final Case Report, Clio |
| Landmark status | San Francisco Designated Landmark **#94**, Final Case Report 20 Oct 1976, designated 1977 | NoeHill (quotes the Case Report), Wikipedia |
| Seating | 2,446 originally; 2,203 after the 1998 rebuild (Wikipedia says 2,197) | SF Theatres blog, Wikipedia |
| 1997–98 rebuild | Stagehouse largely demolished and rebuilt; **grid height 60 ft → 75 ft**, stage depth 30 ft → 39 ft 10 in, proscenium 48 ft → 50 ft, wall-to-wall 68 ft → 82 ft. Roger Morgan (consultant), Korth Sunseri Hagey (architect) | SF Theatres blog, historictheatrephotos |
| Owner / operator | BroadwaySF (ATG) | Wikipedia |
| Footprint (measured) | 64.74 m E–W x 74.99 m N–S AABB; 2,967 m² polygon; min-area OBB 69.13 x 61.52 m | OSM way/35115840 geometry, reprojected |
| DataSF footprint | `SF0351022`, 2,884 m² after `simplifyRing(0.6)` — agrees with OSM to within 3 % | DataSF `ynuv-fyni` |
| AABB centre (measured) | −122.4146109, 37.7793187 | same; equals the Overpass `center` for the way |
| Polygon centroid (measured) | (2009.26, −1033.61) local m vs AABB centre (2014.15, −1030.09) — 6.0 m apart, so the choice matters here (see 2.3) | same |
| Roof heights | LiDAR over 11,595 cells: `hgt_max` **27.19 m**, median 21.47 m, mean 20.61 m, sd 3.36 m, mode 16.80 m, min 7.86 m | DataSF `ynuv-fyni`, `SF0351022` |
| Ground elevation | 15.68 m NAVD88 min, 16.22 m median | same (`gnd_min_m`, `gnd_mediancm`) |
| Market frontage bearing | **45.9°** cw from N (59.63 m long), with a 13.04 m chamfer at the Hyde corner | OSM geometry |
| Hyde flank bearing | 171.5° cw from N (61.41 m long) | same |

### 2.2 Sources

- **OSM way/35115840** via the Overpass API — footprint geometry, tags, heritage refs.
  Nominatim (bounded to SF) resolved the address to node/11100318800 first; the theatre
  node is a POI, not the building, and had to be matched into the way by point-in-polygon.
- **DataSF *Building Footprints (with LiDAR-derived heights)*, resource `ynuv-fyni`,
  building `SF0351022`** — the authority for every height here, because no published
  architectural height for the Orpheum exists. Ground elevation, roof min/mode/median/max.
- **Wikipedia, *Orpheum Theatre (San Francisco)*** — name history, architect, opening,
  landmark status, capacity, the 1998 renovation.
- **NoeHill, *San Francisco Landmark 94: Orpheum Theater*** — quotes the Landmarks
  Preservation Advisory Board **Final Case Report, 20 October 1976** at length: "the most
  impressive theater façade surviving on Market Street", the Spanish Gothic turn in
  Priteca's work, the Pantages → RKO → Cinerama → SHN chain of custody.
- **San Francisco Theatres blog, *The Pantages / Orpheum Theatre: history + exterior
  views* (June 2017)** — the single richest source: the Marshall Square Building name, the
  developer, before/after stage dimensions including the 60 ft → 75 ft grid, and roughly
  30 reproductions of Priteca's 1926 drawings (Gary Parks collection).
- **historictheatrephotos.com, *Orpheum — San Francisco*** — independent confirmation of
  the 1997–98 stagehouse demolition and rebuild and the stage dimensions.
- **PCAD (U. Washington), building 1555** — architect firm attribution, opening date,
  capacity, use history.
- **Cinema Treasures #234, Clio #40678, Cinematour** — corroborating style descriptions
  (Spanish Baroque / Spanish Moorish / "patterned after a 12th-century cathedral").
- **Wikimedia Commons, Category:Orpheum Theatre (San Francisco)** — the photographic
  basis for §2.4. Used: `San Francisco Orpheum Theatre 01.jpg` (Joe Mabel, CC BY-SA — the
  full Market elevation from the Grove/Market corner, the key image), `…03.jpg` and
  `…04.jpg` (dusk and looking-up detail of the entrance bay), `Orpheum Theatre -
  panoramio.jpg` and `Orpheum Theater - panoramio.jpg` (street-level along Market from
  both directions), `Orpheum - theater facade.jpg`.
- **Google satellite imagery at z20**, tiled around the anchor — the roof plan: the hipped
  auditorium roof, the red tile eaves, the mechanical valley, the stage house.
- **Overture Maps + DataSF building extracts already in `pipeline/data/`** — used to
  measure the exclusion radius in 2.13 against the geometry the bake actually sees.

Photogrammetry note: the sub-element heights in 2.4 and 2.7 were measured off
`San Francisco Orpheum Theatre 01.jpg`, which has parallel verticals (so height is linear
in pixel row for a fixed depth), calibrated on two in-plane knowns — pedestrians at the
lobby line and a 4.1 m marquee soffit — and cross-checked against the LiDAR median. They
are *inferred*, good to roughly ±1 m, and they are the weakest numbers in this plan.

### 2.3 Orientation and placement

The site is a **trapezoid, not a rectangle**, and this is the main geometric fact of the
job. Market Street cuts the city grid at 45.9°, Hyde Street runs at 171.5°, and the block
between them closes with a north edge and a north-east party wall. The two street
frontages are 54° apart, so the model is a polygon prism — not a box, and not two boxes
at the same angle.

Working frame for 2.7 is Market-aligned: `u+` runs **north-east along Market at 45.9°**,
`v+` runs **north-west at 315.9°** (away from Market), origin at the frame-bbox centre.
In that frame the polygon is 77.68 m (u) x 57.26 m (v), and the Market face is a straight
line at `v = −28.6` running `u = −28.05 … +31.58`.

Export frame is world-aligned: Blender `+Y` = north, `+X` = east. The exported AABB is
therefore **64.74 m (E–W) x 74.99 m (N–S)**, and the manifest anchor must be the **AABB
centre**, `−122.4146109, 37.7793187` — not the polygon centroid, which sits 6.0 m
west-north-west of it. `placeGeneric` puts the GLB's *origin* at the anchor and the
contract puts the origin at the *bounding-box* base centre, so centroid and anchor are
not interchangeable on a trapezoid. (On the courthouse they agreed to 0.1 m and nobody
had to choose; here they do not.)

Sides: **south-east = Market Street** (the show face), **south-west = the 13 m chamfer**
at the Market/Hyde corner, **west = Hyde Street**, **north = Grove Street**, **north-east
= the party wall** against City College of San Francisco's Civic Center campus at
1170 Market.

### 2.4 What each side shows

- **South-east — Market Street (59.6 m of frontage plus the 13 m corner chamfer).** The
  show face, and it steps. From the Hyde corner to the entrance bay (~35 m) it is the tall
  block: a ground-floor **arcade of round arches on barley-twist terra-cotta columns**,
  then three storeys of large steel-sash glazing set in richly ornamented piers, then a
  deep relief frieze, then a projecting **red mission-tile pent roof**, then a low parapet
  pierced by oval oculi. Eave ~23.3 m, parapet ~24.3 m *(inferred)*. North-east of the
  entrance the same language drops to **two glazed storeys over the arcade**, eave ~16.5 m
  *(inferred)*. Between them the **entrance bay**: a taller, more encrusted slice with a
  crested gable rising above the eave to ~24.8 m *(inferred)*, carrying the blade sign, and
  the marquee at its foot.
- **The blade sign.** Projecting perpendicular to the facade, dark green with a gold
  bead-edge frame, an ornate finialled crown on top, and ORPHEUM reading downward in white
  bulb letters. Bottom ~8.5 m, crown ~25.7 m *(inferred)* — about 17 m of sign. It is the
  tallest thing on the street front and the only saturated colour on the building.
- **The marquee.** A dark-green boxed canopy over the pavement, soffit ~4.1 m, top ~7.0 m
  *(inferred)*, chase lights along the lower edge, "ORPHEUM THEATRE" in white on the
  fascia, and a lit rectangular poster panel standing above it against the facade.
- **West — Hyde Street (61.4 m).** The same terra-cotta wall, less ornamented, arcade
  continuing at street level; the tile eave and parapet run the whole length in the
  satellite. Storey count *inferred* to match the corner block for its southern half and
  drop toward the north.
- **North — Grove Street (~34.9 m) and the north-west jogs.** Plainer still; tile eave and
  parapet continue. This is the back of house.
- **North-east — the party wall.** Shared with City College at 1170 Market; blind, and the
  small 29 m² OSM sliver at 35 Fulton Street sits against this corner (see 2.13).
- **Above.** The most designed surface and the one the app camera actually sees. A **large
  low-pitch hipped roof** covers the auditorium across the centre and north of the block —
  grey, hipped at its west end, ridge running roughly SW–NE. Along the Market and Hyde
  edges, the red tile pent roof caps the parapet with a **flat roof strip behind it**. The
  valley between the wings and the hip is packed with **mechanical plant** — condenser
  banks, ducting, a long low penthouse, a stair penthouse on the west block. At the
  **north-east corner the stage house** stands clear of everything: a pale flat-roofed box
  with a small rigging penthouse and a flagpole, the highest element on the site at 27.2 m.

### 2.5 Recognition cues (ranked)

1. The vertical ORPHEUM blade sign — dark green, crowned, bulb-lit, projecting.
2. The marquee and its poster panel directly under the sign.
3. Cream terra-cotta over a round-arched ground arcade, under a red mission-tile eave.
4. The step down along Market: tall corner block, taller entrance bay, lower NE wing.
5. The big hipped auditorium roof with the pale stage house standing above its NE corner.

### 2.6 Miniature translation

Per §22 of the style bible. Keep 1–5; they all survive at thumbnail size, which is the
whole reason the ornament does not have to.

**Drop:** every literal Plateresque relief (rosettes, grotesques, colonnette shafts,
cartouches, the frieze figures), the barley-twist flutes on the arcade columns, the
window mullion grids (one flat `Toy_glass` pane per bay), the oculi in the parapet as
pierced holes (keep them as shallow recesses), the "1192" address plaque, the air
conditioners hanging in the windows, the Muni/BART furniture on the pavement.

**Keep as rhythm and depth, not detail:** the bay pitch on Market and Hyde, a proud
ornament band under the eave, recessed window reveals ~0.25 m deep, the arcade's arch
heads at 10 segments, the crested gable outline on the entrance bay.

**Exaggerate:** the blade sign (up ~15 % in width and depth so it reads from the aerial
camera, and its bulb letters as raised pucks rather than incised), the marquee projection,
the tile eave overhang, and the parapet cap thickness. Nothing else.

### 2.7 Massing recipe

Build in the Market frame `(u, v, z)`: `u+` NE along Market at 45.9°, `v+` NW at 315.9°,
origin at the frame-bbox centre; then rotate the whole assembly into the world frame
(`+Y` north) and re-centre on the **AABB** so the export contract holds. Footprint
outline, measured, in metres from the frame centre:

```
(-3.08, +28.63) (-38.84, -21.30) (-28.05, -28.61) (+31.58, -28.63)
(+31.58, -28.09) (+31.36,  +1.95) (+38.72,  +1.78) (+38.84,  +7.85)
(+10.59, +28.33) (+7.61, +26.63)  (+2.31,  +25.50)
```

The Market face is the straight `v = −28.6` edge from `u = −28.05` to `u = +31.58`; the
chamfer is the `(-38.84,-21.30) → (-28.05,-28.61)` edge; the Hyde flank is
`(-3.08,+28.63) → (-38.84,-21.30)`.

| Element | Extent | z range | Notes |
|---|---|---|---|
| Ground arcade | all street faces | 0 → 7.2 | round arches, pitch ~6.0 m, recessed 0.6 m; `Toy_cream` piers, `Toy_ink` reveals |
| Corner block wall | `u −28.0 … +2.0` on Market, all of Hyde, Grove | 7.2 → 21.6 | three glazed storeys, bay pitch ~6.0 m |
| NE wing wall | `u +11.0 … +31.6` on Market | 7.2 → 14.9 | two glazed storeys |
| Ornament band | both | eave −1.4 | proud +0.3, `Toy_sand` |
| Tile pent roof | both | corner 21.6 → 23.3; wing 14.9 → 16.5 | `Toy_brick`, overhang 1.2 m |
| Parapet | both | to 24.3 / 17.5 | plain cap, oval recesses on the corner block |
| Entrance bay | `u +2.0 … +11.0` | 0 → 24.8 | proud +0.5 from the Market face; crested gable above the eave |
| Marquee | centred `u +6.5` | 4.1 → 7.0 | 11 x 4.2 m, projects 4.0 m, `Toy_ink` box with `Toy_trim` edge |
| Poster panel | centred `u +6.5` | 7.0 → 12.0 | 4.5 x 5.0 m, flat against the bay |
| Blade sign | `u +6.5`, projecting 2.2 m | 8.5 → **26.0** | 3.4 m wide x 0.9 m thick, crown 8.5 % of its height, 7 bulb-letter pucks |
| Auditorium hip roof | `u −22 … +18`, `v −12 … +26` | eave 19.0 → ridge 22.0 | low pitch, hipped west end |
| Roof plant valley | between wings and hip | 21.6 → 24.0 | 2 condenser banks, 1 long penthouse, 1 stair penthouse |
| Stage house | `u +14 … +36`, `v +4 … +26` | 0 → **27.2** | flat roof; the rigging penthouse and flagpole are folded into the 27.2 m cap, not built above it |

Every z above the LiDAR line is *inferred* except the 27.2 m top. Normalize the assembled
bbox top to 27.2 m exactly so `targetHeightM / measuredHeight` lands at 1.0.

Bevel 0.12 m, 2 segments. Arch heads 10 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | terra-cotta walls, piers, arcade, entrance bay |
| `Toy_sand` | `#ece4d4` | ornament band, string courses, crested gable |
| `Toy_trim` | `#f3efe6` | parapet caps, eave fascia, sign frame, marquee edge |
| `Toy_brick` | `#c96f4a` | mission-tile pent roofs |
| `Toy_glass` | `#2a4d73` | all windows and arcade glazing |
| `Toy_ink` | `#3a3530` | arcade reveals, entrance recess, marquee box, blade-sign ground |
| `Toy_roofd` | `#45454a` | auditorium hip roof, flat roof strips, stage-house roof |
| `Toy_steel` | `#9aa0a6` | condenser banks, penthouses, flagpole |
| `Toy_stone` | `#d9d2c2` | stage-house walls (stucco, cooler than the terra-cotta) |
| `Toy_white_Glow` | `#f7f4ec` | the blade sign's bulb letters and crown lamps, and the marquee chase lights |
| `Toy_mustard_Glow` | `#d9a441` | the marquee soffit and the entrance recess under it |

Night glow: **hero = the blade sign**, which is the only correct answer for this building;
**supporting = the marquee chase line and its warm soffit**. Nothing else. The upper
storeys stay dark — a theatre's offices are dark at curtain, and 60 m of lit windows would
out-shout the Main Library across Hyde. Both glow day-colours (`f7f4ec`, `d9a441`) are
palette neighbours of the terra-cotta, so the daylight asset stays calm; the sign reads as
white bulbs on dark green by day and as white bulbs on dark green, lit, by night. Do not
build the sign as a closed glow shell — model the letters as separate raised pucks on a
non-glow `Toy_ink` ground.

The dark green of the real sign and marquee has no palette entry; `Toy_ink` is the nearest
and keeps the asset inside the palette. If the executing agent judges from the renders that
the green is a genuine recognition cue, `#2c4a70` navy is the wrong direction and an
off-palette green is a WARN, not a fail — record the choice either way.

### 2.9 Top surface

Designed, not blank (§10). Red tile eave strips down the Market and Hyde edges; a grey
hipped auditorium roof filling the centre and north; a plant-filled valley between them
with two condenser banks, a long penthouse and a stair penthouse; the pale stage house
standing clear at the north-east. From directly above, the read is: a warm tile L along
the two streets, a big grey hip, and one bright box at the top corner — plus the blade
sign's crown poking over the Market eave, which is what tells you which building it is.

### 2.10 Scope

The Orpheum block only. No City College, no Main Library, no UN Plaza, no street
furniture, no trees, no vehicles, no plinth.

### 2.11 Triangle budget

Cap 24,000; target 12,000–17,000. The arcade (roughly 30 arches x ~140 tris with 10-segment
heads ≈ 4,200), the window bays (~60 x 40 ≈ 2,400), the blade sign with its letter pucks
and crown (~1,800), the tile eaves with their overhang and fascia (~1,500), the hipped roof
and stage house (~600), and the roof plant (~1,200) dominate. If it runs over, the arcade
arch heads drop to 8 segments before anything else is touched.

### 2.12 Draft manifest entry

```json
{
  "id": "orpheum-theatre",
  "file": "orpheum-theatre.glb",
  "anchor": [-122.4146109, 37.7793187],
  "targetHeightM": 27.2,
  "cat": 17,
  "name": "Orpheum Theatre",
  "estimated": false,
  "loadRadius": 2500
}
```

`loadRadius`: the default rule is `max(2500, 27.2 x 30) = max(2500, 816) = 2500`. A 27 m
building is invisible past ~2 km and the procedural block under it is carved out, so 2500 m
is both the rule and the right answer. Not `alwaysLoaded` — that list is for skyline pieces.

`estimated: false` follows the precedent set by `civic-center-courthouse` and
`earl-warren-building`: the height is a measurement (city LiDAR), not a guess, even though
no architect ever published a figure.

### 2.13 Integration notes (for later, not this task)

New landmark — **Case B**. `orpheum-theatre` exists in neither `pipeline/lib/landmarks.mjs`
nor `app/src/landmarks.js`, so integration needs a manifest entry (2.12), a registry entry,
a tile re-bake, audit 1.6 and `node pipeline/landmark-streaming-check.mjs` against a build.

**Exclusion radius: `exclude: 20`.** Measured against the geometry the bake actually sees
(DataSF + Overture, projected, `simplifyRing(0.6)`), distances from the anchor:

| Ring | Source | Area | Centroid | Nearest vertex |
|---|---|---|---|---|
| Orpheum `SF0351022` | DataSF | 2,883 m² | **6.11 m** | 24.14 m |
| Orpheum `7ad3c2dc…` (OSM w35115840) | Overture | 2,967 m² | **7.28 m** | 28.27 m |
| Civic Center Station `837db0e8…` | Overture | 6,944 m² | 66.18 m | **24.55 m** |
| City College 1170 Market `SF0351051` | DataSF | 578 m² | 33.64 m | **25.65 m** |
| City College `e757eceb…` | Overture | 521 m² | 33.79 m | **28.27 m** |
| 35 Fulton St sliver `876a881a…` | Overture | 29 m² | 38.66 m | 34.90 m |

`excluded()` drops a ring when its centroid **or any vertex** is inside the radius, so the
window is `(7.28, 24.55)` — above 7.28 to catch both of our own rings on the centroid test,
below 24.55 to spare the Civic Center Station strip. **20 m** sits in the middle with 12.7 m
of margin on our side and 4.5 m on the neighbours'. Two rings drop, both ours; this is the
normal DataSF-plus-Overture double-trace, not collateral. The station polygon is a narrow
strip along Market and does **not** overlap the theatre footprint (point-in-polygon: zero
shared interior), so there is no unavoidable-collateral case here.

Residual: the 29 m² Overture sliver at 35 Fulton Street shares two vertices with the
Orpheum's north-east corner and survives at `exclude: 20` as a ~5 x 11 m, 11.6 m procedural
nub against the party wall. No single radius removes it without eating City College. If
stage-5 QA shows it poking through the asset, add

```js
extraExclusions: [{ lon: -122.4144084, lat: 37.7796474, r: 6 }],
```

which catches that ring on its own centroid (0 m) and reaches nothing else — the nearest
City College vertex is 10.8 m away and the nearest station vertex 19.3 m. Decide it from
the baked tile, not from this table.

Draft registry entry:

```js
{
  id: 'orpheumTheatre',
  name: 'Orpheum Theatre',
  lon: -122.4146109,
  lat: 37.7793187,
  height: 27.2,
  // Trapezoidal block, 64.7 x 75.0 m AABB. Both source rings (DataSF SF0351022,
  // Overture 7ad3c2dc) sit 6.1 and 7.3 m from the anchor on the centroid test;
  // the nearest neighbour vertex is the Civic Center Station strip at 24.55 m and
  // City College at 25.65 m. 20 m is the middle of that window.
  exclude: 20,
  camera: { distance: 380, yaw: 44, pitch: 20 },
}
```

`yaw: 44` puts the camera at bearing 136° — south-east of the block, square onto the Market
frontage and the sign. (`camera.js`: the offset is `(sin yaw, ·, cos yaw)`, and `+z` is
south, so the camera's compass bearing from the pivot is `(180 − yaw) mod 360`.)

Run `docs/asset-plans/INTEGRATION-PROMPT.md` for the full procedure. `BATCH: yes` applies —
throw the bake away and commit source only.

### 2.14 Validation checklist

`validation.json` must show: fresh-scene re-import; `min_z ≈ 0`; XY centre within 0.5 m;
dims ≈ 64.7 x 75.0 x 27.2 m; tris ≤ 24,000; zero image textures; zero transparent
materials; every material `Toy_*` and none named `Toy_body`; no cameras, lights, animation,
armatures or constraints; transforms applied; no negative scales; normals outward by the
per-object signed-volume test with the ray test as a supplementary metric; glow materials
present and shipping with emission strength 0; and the bbox top owned by the stage house,
not the blade sign.

### 2.15 Open questions and risks

1. **OSM's `height=46 m` is wrong and must not be used.** DataSF records
   `p2010_zmaxn88ft = 150.96 ft = 46.01 m` — the roof's **absolute NAVD88 elevation**.
   Someone converted that to metres and tagged it as building height. The real height above
   ground is 27.19 m. This is the one trap on this building and it is a 19 m error.
2. **No published architectural height exists.** 27.2 m is LiDAR, and it is only 1.96 sd
   above the mean, which is the zone where `hgt_max` sometimes turns out to be a parapet
   spike or a stray return. It survives four checks: the published 75 ft grid height implies
   a fly-tower roof at ~26–27 m; photographs show a distinctly taller stepped block behind
   the Market facade; the satellite shows a large elevated flat-roofed mass at the NE with
   its own walls and shadow; and `maxcm_1st − gnd_median` gives the same 27.0 m
   independently. It is a broad block, not a spike — that is what makes it trustworthy.
   Attribution of the max to the stage house rather than to the corner block's parapet is
   *inferred* from the photographs; the number is the same either way.
3. **Every sub-element height in 2.4 and 2.7 is photogrammetric**, ±1 m, from one photo with
   a scale calibrated on pedestrians and an assumed 4.1 m marquee soffit. The two that
   matter most — the 23.3 m corner-block eave and the 16.5 m NE-wing eave — bracket the
   LiDAR median of 21.47 m and the LiDAR mode of 16.80 m respectively, which is the only
   independent check available. Re-derive them if better sources turn up; the Priteca
   drawings reproduced on the SF Theatres blog would settle it outright.
4. **Ornament is the artistic risk.** Priteca's facade is the most ornamented on Market
   Street; a miniature that tries to keep it will read as grey noise from the app camera,
   and one that strips it entirely will read as a generic cream box with a sign. §2.6 draws
   the line at rhythm-and-depth, but it is a judgement call and the renders are the referee.
5. **The dark green** of the sign and marquee is off-palette. `Toy_ink` is the substitute
   proposed in 2.8; the alternative is an off-palette green, which is a WARN. Whichever the
   executing agent picks, it must be recorded in `REPORT.md` with the reason.
6. **The trapezoid.** Anchor and centroid are 6.0 m apart. Using the centroid would slide
   the whole building 6 m north-west of where it belongs, which on a 60 m frontage is
   visible. The AABB centre is the anchor; §2.3 says why.
7. **The 35 Fulton Street sliver** survives the exclusion by design (2.13). Whether it needs
   the `extraExclusions` circle is a stage-5 decision made from the baked tile.
