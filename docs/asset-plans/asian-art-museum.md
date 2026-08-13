# Asian Art Museum (Old Main Library) — SF-SIM asset plan

George Kelham's 1917 Main Library, converted by Gae Aulenti in 2003 and crowned by
wHY's terracotta pavilion in 2023. A pale granite Beaux-Arts block that faces City
Hall across Civic Center Plaza — and, from the app's aerial camera, a designed roof
with a sculpture terrace on it.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/asian-art-museum/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `asian-art-museum` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4159859, 37.7802817` (oriented-bounding-box centre, measured) |
| Target height | **28.1 m** crest (raised central monitor); main cornice/roof plane **23.2 m** |
| OSM footprint | 106.60 x 54.71 m oriented box, 4,893 m2 polygon (OSM way/24588037, measured) |
| Long-axis bearing | 81.68 deg — the Civic Center grid, 8.32 deg north of due east |
| Triangle cap | 24,000 |
| Category | `16` (Museum) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Asian Art Museum GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the Asian Art Museum of San Francisco
(200 Larkin Street, the 1917 Old Main Library) and deliver it as a downloadable,
validated GLB.

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
8. `docs/asset-plans/asian-art-museum.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A pale granite Beaux-Arts block, long east–west, low and wide, not a tower
- The Larkin Street (west) ceremonial front: rusticated base, a giant-order
  colonnade, the incised frieze inscription, eight steps up to three double doors
- The long arched arcade of the Fulton Street (south) facade — the Civic Center
  axis elevation
- A heavy cornice and low attic wrapping the whole block
- The designed roof: two light courts, a raised central monitor, and the 2023
  terracotta pavilion + sculpture terrace occupying the eastern third
- Night: the facade uplight that washes the Larkin colonnade

## Research the Asian Art Museum independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views — the roof is a major surface here, and it changed in 2023
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- **The height.** The OSM `height=46` tag on way/24588037 is NOT a height: it is the
  NAVD88 roof *elevation* (152.93 ft). Do not use it. Establish the crest and the
  cornice line separately and say which is which.
- Whether wHY's 2023 pavilion rises above the historic parapet (the architect says
  it "fits within the datum lines of the historic structure" — check that visually)

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/asian-art-museum/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3-5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. A contact sheet of
attributed reference thumbnails is welcome if legally permissible — do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

The finished asset must be immediately recognizable as the Asian Art Museum,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel art,
not generic low-poly, and never accurate in one view while invented in the others.

This building is 106 m long and only 28 m tall. It will be read mostly from above
and at a shallow angle. Spend the budget on the roof, the cornice line, and the
facade rhythm; do not spend it on column flutes nobody will see.

## Scope of the exported asset

Export the museum block only: the historic 1917 mass, its base, colonnade, arcade,
cornice, attic, roof courts and central monitor, plus the 2023 rooftop pavilion and
sculpture terrace, and the Larkin entrance steps.

Do not include unrelated surrounding city geometry: Civic Center Plaza, City Hall,
the Pioneer Monument, the new Main Library, Larkin / Fulton / Hyde / McAllister
Streets, street trees, people, vehicles, plinths, cameras or lights. Temporary
context may appear in review renders but must not leak into the GLB.

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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The building's
long axis runs at bearing **81.68 deg**; the main entrance faces **west** onto
Larkin Street. The contract's "front faces −Y" cannot be honoured literally here;
real-world orientation wins (AGENTS rule 5). Record the decision and the measured
heading in `REPORT.md`.

**Height normalisation:** normalise the bbox top to the verified crest exactly, so
the loader's `targetHeightM / measuredHeight` scale lands at 1.0.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/asian-art-museum/build_asian_art_museum.py` (deterministic build script),
`artifacts/asian-art-museum/asian-art-museum.blend`, and
`artifacts/asian-art-museum/asian-art-museum.glb`. The script must rebuild the model
reliably enough for future revision. Do not modify or rename an unrelated existing
GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`asian-art-museum-top.png`, `asian-art-museum-north.png`, `asian-art-museum-east.png`,
`asian-art-museum-south.png`, `asian-art-museum-west.png`, plus
`asian-art-museum-contact-sheet.png`, at least one high three-quarter aerial beauty
render `asian-art-museum-aerial.png`, and a night render `asian-art-museum-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the two light courts, the
central monitor, the pavilion and the sculpture terrace; the aerial view uses the
style bible's camera assumptions (30-50 degrees down, long lens). Simple tabletop
lighting, neutral warm background, minimal depth of field, and every image must
depict the same exported model. The night render must show the `_Glow` set driven
from Base Color (see the note at the end of `docs/asset-plans/README.md`).

## Validate the exported GLB

Re-import `asian-art-museum.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/asian-art-museum/validation.json` and
`artifacts/asian-art-museum/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "asian-art-museum",
  "file": "asian-art-museum.glb",
  "anchor": [
    -122.4159859,
    37.7802817
  ],
  "targetHeightM": 28.1,
  "cat": 16,
  "name": "Asian Art Museum",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/asian-art-museum.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | 1915–1917, opened 15 February 1917 | Wikipedia, SFPL history |
| Architect | George W. Kelham (Q5545664) | Wikidata Q111931359 P84 |
| Style | Beaux-Arts / Classical Revival, closely modelled on Cass Gilbert's Detroit Public Library | noehill (SF Point of Historical Interest) |
| Converted | Gae Aulenti, base-isolation seismic upgrade; reopened 20 March 2003 | Wikipedia |
| Rooftop addition | wHY (Kulapat Yantrasast): Akiko Yamazaki & Jerry Yang Pavilion, 8,500 sq ft gallery, opened July 2023; East West Bank Art Terrace, 7,200 sq ft, August 2023 | ArchDaily, wHY, museum press |
| Footprint (polygon) | 4,893 m2 | OSM way/24588037, reprojected + shoelace (measured) |
| Footprint (oriented box) | 106.60 x 54.71 m | min-area OBB over the OSM polygon (measured) |
| Long-axis bearing | 81.68 deg (8.32 deg north of due east) | derived from the OBB (measured) |
| OBB centre | −122.4159859, 37.7802817 | derived (measured) |
| Polygon centroid | −122.4160441, 37.7802533 | derived (measured) — 5 m west of the OBB centre |
| Crest above grade | **28.10 m** | DataSF Building Footprints `hgt_maxcm` = 2810 (2010 LiDAR, measured) |
| Main roof plane above grade | **23.22 m** | DataSF `hgt_median_m` (measured) |
| Roof elevation NAVD88 | 41.66 m median / 47.16 m peak | DataSF `median_1st_m`, `peak_1st_m` |
| Site grade NAVD88 | 15.15–19.80 m (18.05 m median) | DataSF `gnd_*` — the block falls ~4.7 m across |
| Levels | 3 signed in OSM; historic building had four stack levels | OSM `building:levels`, Calisphere 1917 photo |
| Contributor to | SF Civic Center Historic District, NRHP #78000757, National Historic Landmark | noehill |
| Main entrance | **Larkin Street (west)** — eight steps with flanking ramps, three sets of double doors | Destination Accessible |
| Fulton Street (south) | "the long arcade of the Fulton Street facade ... defines the principal planning axis of the Civic Center" | noehill |
| Larkin Street (west) | "reflects the design of the City Hall in its main features" | noehill |

### 2.2 Sources

- https://www.openstreetmap.org/way/24588037 — footprint geometry, address, wikidata link
- https://data.sfgov.org/resource/ynuv-fyni.json (`mblr=SF0353001`, `area_id=255`) — 2010 LiDAR heights: `hgt_maxcm` 2810, `hgt_median_m` 23.22, ground 15.15–19.80 m
- https://en.wikipedia.org/wiki/Asian_Art_Museum_(San_Francisco) — Kelham 1917, Aulenti 2003, Yamazaki/Yang Pavilion 2023, 200,000 sq ft
- https://www.wikidata.org/wiki/Q111931359 — "The Old Main Library": Kelham, 1917, Beaux-Arts
- https://noehill.com/sf/landmarks/poi_asian_art_museum.asp — Detroit Public Library model, Fulton arcade, Larkin facade vs City Hall, historic-district status
- https://www.archdaily.com/880551/why-unveils-90-dollars-million-san-francisco-asian-art-museum-addition — pavilion programme, "rusticated gray terracotta facade"
- https://why-site.com/work/the-asian-art-museum-in-san-francisco/ — "the pavilion as a whole fits within the datum lines of historic structure"; terracotta as "a reinterpretation of the rusticated granite on the original façade"
- https://destinationaccessible.org/asian-art-museum/ — eight steps, ramps, three double doors on Larkin
- https://commons.wikimedia.org/wiki/File:Asianartmuseumnight.jpg — the Larkin night elevation (colonnade, inscription, uplight)
- https://commons.wikimedia.org/wiki/File:Asian_Art_Museum_(6000548677).jpg — the Hyde/east side: modern granite retaining walls, glass railings, glazed bay
- Esri World Imagery nadir aerial over the block — roof layout, light courts, pavilion and terrace

### 2.3 The height correction (read this before modelling)

OSM way/24588037 carries `height=46`. That figure is **not a height** — it is the
building's NAVD88 roof *elevation*, 152.927 ft = 46.61 m, which appears verbatim as
`p2010_zmaxn88ft` in the DataSF LiDAR record. Extruding 46 m would produce a museum
half the height of City Hall's dome, which is wrong by roughly a factor of 1.6.

The measured values are:

- **Crest 28.10 m** — the raised central monitor over the old delivery hall, visible
  in the aerial as a square hipped mass rising out of the flat roof. This is
  `targetHeightM`.
- **Cornice / main roof plane 23.22 m** — where the flat roof and the parapet sit.

The 2010 LiDAR predates the 2023 pavilion, but wHY state the pavilion "fits within
the datum lines of historic structure", so the crest is unchanged. Treat the
pavilion top as level with the historic attic (~24.2 m), not above it. *Inferred* —
worth one more visual check from an oblique aerial.

### 2.4 Orientation and placement

The block is bounded by Larkin (west), McAllister (north), Hyde (east) and Fulton
(south, the pedestrianised Fulton Mall with the Pioneer Monument). Its long axis
runs at bearing 81.68 deg — the Western Addition grid, 8.32 deg counter-clockwise
from due east. In Blender that is a +8.32 deg rotation about Z from an axis-aligned
box, with `+Y` = true north.

The main entrance faces **west** onto Larkin, across Civic Center Plaza from City
Hall. Anchor on the OBB centre, not the polygon centroid: the polygon has small
service notches on the north and south edges that pull the centroid 5 m west of the
mass the model actually centres on.

### 2.5 What each side shows

**West (Larkin Street) — the hero elevation.** Rusticated pale-granite base about a
third of the facade height, carrying tall rectangular windows. Above it a giant
order of engaged columns on a stylobate, with recessed glazed bays and small
balustraded balconies between them. End pavilions terminate the colonnade, each with
a tall arched opening filled by a geometric lattice grille. Above the columns: a full
entablature whose architrave carries the incised inscription ASIAN ART MUSEUM /
CHONG-MOON LEE CENTER FOR ASIAN ART AND CULTURE, then a dentil cornice and a low
attic. Eight steps and ramps lead to three double doors. At night the whole
colonnade is uplit and the cornice reads as a bright band.

**South (Fulton Street).** The long arcade — the Civic Center axis elevation, a
repeated run of arched openings above the rusticated base, quieter than Larkin but
the longest continuous rhythm on the building.

**North (McAllister Street).** The matching long flank; same base and cornice, plainer
rhythm, service notches in the footprint. A small separate structure stands off the
north-east corner (a distinct LiDAR record, ~8.6 m tall — not part of this asset).

**East (Hyde Street).** The modern face. Aulenti-era pale granite retaining walls and
a raised planted terrace with glass railings, a bronze relief panel, and a glazed
metal-framed bay projecting from the historic wall. Above it, the 2023 pavilion.

**Top.** The most important surface for this asset. Reading the nadir aerial: a light
parapet band around the whole block; a dark low-slope roof ring inside it; **two
rectangular light courts** in the western two-thirds separated by a cross-wing; a
**raised square monitor with a hipped roof** between them (the 28.1 m crest); and, over
the **eastern third**, the pale terracotta pavilion as a low box along the north edge
with a glazed clerestory strip, and beside it the pale open **sculpture terrace** with
scattered round sculptures and planters.

### 2.6 Recognition cues (ranked)

1. A long, low, pale block with an unbroken heavy cornice — reads as "the civic
   twin of City Hall" from across the plaza
2. The giant-order colonnade and inscribed frieze on the Larkin front
3. The arched arcade rhythm along Fulton
4. From above: two dark light courts + a raised central monitor in the west, a pale
   terracotta pavilion and sculpture terrace in the east — old and new split across
   one roof
5. The rusticated granite base wrapping all four sides

### 2.7 Miniature translation

**Preserve**

- The 106 x 55 m proportion and the 8.32 deg grid rotation — this building is a slab,
  not a block, and the rotation is what makes it sit in Civic Center rather than float
- The cornice/attic line as one continuous silhouette element
- The colonnade as the west front's whole identity
- The roof's east/west split — historic courts vs modern terrace

**Simplify / exaggerate**

- Dozens of columns become ~10 chunky ones on the west front only; north and south
  get pilaster strips, not free-standing columns
- The Fulton arcade becomes one repeated arched recess band, ~14 bays
- All ornament collapses into three horizontal bands: base cap, entablature, attic
- The inscription becomes a slightly proud `Toy_trim` frieze band, not letterforms
- Rooftop clutter becomes: two clean court voids, one hipped monitor, one pavilion
  box, one terrace deck, three sculpture pucks, two planter strips
- The eight entrance steps become one chunky three-tread plinth, semantically enlarged

### 2.8 Massing recipe

Build order for the deterministic script; author axis-aligned then rotate the whole
assembly +8.32 deg about Z. Dimensions are the starting point, not a straitjacket —
adjust after the first aerial review render.

1. Base: 106.6 x 54.7 m block, z=0 to z=6.5, `Toy_stone`, with four deep horizontal
   rustication grooves and a `Toy_trim` cap course at z=6.2.
2. Body: same plan, z=6.5 to z=19.5, `Toy_cream`, carrying the per-face rhythms of 5.
3. Entablature: `Toy_trim` band z=19.5 to z=22.6, projecting 0.9 m — the continuous
   cornice, the strongest silhouette line on the model.
4. Attic: `Toy_trim` parapet z=22.6 to z=24.2, inset 0.3 m from the cornice face.
5. Roof deck at z=23.2, `Toy_roofd`, with two light-court voids (each ~26 x 18 m)
   in the western two-thirds and a 3 m wide cross-wing between them.
6. Central monitor: 16 x 16 m, z=23.2 to z=27.0 `Toy_cream`, capped by a hipped
   `Toy_roofd` pyramid to the 28.1 m crest.
7. West colonnade: 10 columns radius 0.85 m from z=6.5 to z=19.5, standing 1.1 m proud
   of the body, `Toy_trim`; recessed `Toy_glass` bays between them; two solid end
   pavilions each pierced by one tall arched `Toy_glass` opening.
8. South arcade: 14 arched recesses 3.0 m wide, z=8.0 to z=17.5, `Toy_glass` in
   `Toy_cream` reveals. North flank: the same rhythm as flat window slots, no arches.
9. East third roof: `Toy_sand` pavilion box 34 x 16 x 5.0 m along the north edge with
   a `Toy_glass` clerestory strip; `Toy_sand` terrace deck beside it at z=23.6 with a
   low `Toy_trim` railing, three `Toy_coral` sculpture pucks and two `Toy_mint` planter
   strips.
10. West steps: 22 m wide, three treads, z=0 to z=1.5, `Toy_stone`, with three
    `Toy_glass` doorways behind.
11. Bevel 0.12 m, 2 segments.

### 2.9 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | main granite walls, monitor |
| `Toy_stone` | `#d9d2c2` | rusticated base, entrance steps |
| `Toy_trim` | `#f3efe6` | columns, entablature, cornice, attic, terrace railing |
| `Toy_glass` | `#2a4d73` | windows, arcade openings, doorways, clerestory |
| `Toy_roofd` | `#45454a` | roof deck, light-court floors, hipped monitor cap |
| `Toy_sand` | `#ece4d4` | the 2023 terracotta pavilion and terrace deck |
| `Toy_mint` | `#8fd0a8` | rooftop planter strips |
| `Toy_coral` | `#e8735a` | rooftop sculpture pucks — the one saturated accent |
| `Toy_white_Glow` | `#f7f4ec` | the Larkin colonnade uplight band |
| `Toy_gold_Glow` | `#caa64a` | the three entrance doorways at night |

Night glow: hero = the uplit west colonnade (documented in the night reference);
supporting = the entrance doorways. Two glow surfaces, nothing else. Their day
colors must match non-glow palette neighbours so the daylight asset stays calm.

### 2.10 Top surface

106 x 55 m of roof under a camera that looks down: this is the asset's largest single
surface and the place the 2023 work is legible. It must not be a flat gray rectangle.
The design is the real one, compressed: dark low-slope ring, two court voids, one
raised hipped monitor, then the pale pavilion and sculpture terrace filling the
eastern third. The value contrast between the dark historic roof and the pale modern
terrace is the point — it tells the building's story from the air in one read.

### 2.11 Scope

**In the GLB:** the historic 1917 block (base, colonnade, arcade, cornice, attic,
roof, courts, central monitor), the 2023 pavilion and sculpture terrace, the Larkin
entrance steps and doorways

**Not in the GLB:** Civic Center Plaza, City Hall, the Pioneer Monument, the new Main
Library, the small structure off the north-east corner, Larkin / Fulton / Hyde /
McAllister Streets, street trees, people, vehicles, plinths, cameras or lights

### 2.12 Triangle budget

Cap 24,000. Suggested split: body and facade rhythms ~8k, colonnade and arcade ~6k,
base rustication and cornice/attic ~4k, roof, courts, monitor, pavilion and terrace
~5k, steps ~1k.

### 2.13 Draft manifest entry

```json
{
  "id": "asian-art-museum",
  "file": "asian-art-museum.glb",
  "anchor": [
    -122.4159859,
    37.7802817
  ],
  "targetHeightM": 28.1,
  "cat": 16,
  "name": "Asian Art Museum",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`loadRadius` is the default rule `max(2500, 28.1 x 30)` = 2500.

### 2.14 Integration notes (for later, not this task)

- **New landmark (Case B).** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: 'asian-art-museum'`, lon/lat as above, height 28.1, `exclude: ~70` — the
  OBB half-diagonal is 59.9 m) **and re-bake the affected tiles**, or the baked
  procedural building will intersect the GLB.
- Civic Center is dense with already-integrated landmarks (`city-hall`,
  `opera-house`) and more in flight. Check the exclusion radius does not eat the
  Fulton Mall or the plaza edge.
- Manifest id `asian-art-museum` maps to `asianArtMuseum` under the registry's
  camel conversion — confirm against `app/src/landmarks.js` before wiring.

### 2.15 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bbox Z normalised to 28.10 m exactly, so the loader's scale lands at 1.0
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 24,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the colonnade uplight band and the entrance doorways
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume authoritative; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Seven review renders + night render + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.16 Open questions and risks

- **The height tag is a trap.** OSM `height=46` is the NAVD88 roof elevation. Anyone
  re-deriving the height from OSM without reading 2.3 will build it 1.6x too tall.
- The 28.10 m crest comes from 2010 LiDAR. wHY's "fits within the datum lines"
  statement is the only evidence the 2023 pavilion did not raise it; that is
  *inferred* from a marketing text and deserves one oblique-aerial check.
- The site falls ~4.7 m across the block (grade 15.15–19.80 m NAVD88). The app seats
  assets on sampled terrain at a single anchor, so the model's base will be level
  while the real building's is stepped. Accept it; do not model a stepped base.
- The exact column count and arcade bay count on the real elevations were read from
  photography, not drawings — they are *inferred* and chosen for rhythm, not census.
- Civic Center already has several landmarks; this one is low and wide, so it must
  not be allowed to visually compete with City Hall. Keep it calm.
