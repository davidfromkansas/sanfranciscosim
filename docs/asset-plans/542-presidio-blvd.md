# 542 Presidio Boulevard — SF-SIM asset plan

One of the cream-stucco, terracotta-roofed officers' family quarters that line Presidio
Boulevard where it drops into the park. A quiet Mission Revival duplex from the WWI-era
build-out — not a hero landmark, but the archetype of the Presidio's residential roofscape,
and the first of that family in the scene.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/542-presidio-blvd/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `542-presidio-blvd` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4516862, 37.7971579` (measured, OBB centre) |
| Target height | **10.6 m** to the roof crest (*estimated*); eave **8.0 m** (corroborated) |
| OSM footprint | 14.01 x 19.37 m oriented bbox, 271.5 m2 (OSM way/288361188, measured) |
| Triangle cap | 8,000 |
| Category | `1` (House) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 542 Presidio Boulevard GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 542 Presidio Boulevard in San Francisco and deliver
it as a downloadable, validated GLB.

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
8. `docs/asset-plans/542-presidio-blvd.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Low-pitched terracotta tile **hipped** roof with deep overhanging eaves — the dominant surface
- Two-storey cream stucco box, quiet and near-symmetrical
- A tiled **pent roof / belt course** between the two floors, running over the porch
- Full-width recessed ground-floor porch behind chunky square columns, with a solid
  stucco balustrade wall (not spindles)
- Two front doors side by side — it is a duplex, not a single house
- Tall dark multi-pane casement windows on the upper floor, with small iron balconettes
- Two chimneys
- A raised base with entry steps — the house sits up on a green rise above the boulevard

## Research 542 Presidio Boulevard independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- **The crest height.** The OSM `height=8` tag is the EAVE, not the top (see 2.1). Do not
  model to 8 m. Establish the ridge height and record eave vs crest explicitly.
- Whether 542 specifically is a duplex or one of the four single-family houses in the row
- The roof pitch, which sets the crest — the single largest uncertainty in this plan

Prefer architect/engineer publications, owner or institutional material (Presidio
Trust / NPS), planning and permitting documents, architectural press, geolocated
photography, and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

Note that 540–547 Presidio Boulevard are near-identical siblings from one campaign;
references to the neighbours are legitimate evidence for the type, but the footprint,
anchor and orientation must come from 542 itself.

## Create a reference dossier

Write `artifacts/542-presidio-blvd/REFERENCE.md` containing: source links and what each
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

This is a small building: at 10.6 m it will be read almost entirely as a **roof** plus a
silhouette. Spend the budget accordingly — §10 of the style bible applies with full force.
Resist the urge to model interior-scale detail that will never be visible.

The finished asset must be immediately recognizable as a Presidio officers' quarters,
consistent with the real building from all four sides and above, architecturally credible,
and a premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the house itself: raised base, two storeys, porch, pent roof, main hipped roof and
chimneys.

Do not include unrelated surrounding city geometry: Presidio Boulevard or Sumner Avenue,
the neighbouring houses at 540/541/543/544, the detached garages, the retaining walls,
the surrounding cypress and eucalyptus, hedges, lawns, people, vehicles, plinths, cameras
or lights. Temporary context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 8,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The long axis and roof
ridge run **NNE–SSW at bearing ~31°**; the entrance front faces **ESE, bearing ~121°**,
onto Presidio Boulevard. This means the front does NOT face `-Y`: real-world orientation
wins (see the orientation note in `docs/asset-plans/README.md`). Record the deviation and
the measured heading in `REPORT.md`.

**Height normalisation:** normalise the bbox top to the verified crest height exactly, so
the loader's `targetHeightM / measuredHeight` scale lands at 1.0.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/542-presidio-blvd/build_542_presidio_blvd.py` (deterministic build script),
`artifacts/542-presidio-blvd/542-presidio-blvd.blend`, and
`artifacts/542-presidio-blvd/542-presidio-blvd.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`542-presidio-blvd-top.png`, `542-presidio-blvd-north.png`, `542-presidio-blvd-east.png`,
`542-presidio-blvd-south.png`, `542-presidio-blvd-west.png`, plus
`542-presidio-blvd-contact-sheet.png` and at least one high three-quarter aerial beauty
render `542-presidio-blvd-aerial.png`. A night render `542-presidio-blvd-night.png` is
required, and the night tile must appear on the contact sheet.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the hip roof's ridge, the four hip
planes, the eave overhang and the two chimneys; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `542-presidio-blvd.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/542-presidio-blvd/validation.json` and
`artifacts/542-presidio-blvd/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "542-presidio-blvd",
  "file": "542-presidio-blvd.glb",
  "anchor": [
    -122.4516862,
    37.7971579
  ],
  "targetHeightM": 10.6,
  "cat": 1,
  "name": "542 Presidio Boulevard",
  "estimated": true,
  "loadRadius": 2500,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or
any app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in
`docs/asset-plans/542-presidio-blvd.md`. **Read 2.13 before integrating: this landmark needs
an unusually small exclusion radius and its registry id cannot start with a digit.**
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* or *estimated* are
visual or derived, not published figures — the executing agent must re-verify anything it
relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 542 Presidio Blvd, San Francisco, CA 94129 | Nominatim, OSM tags |
| OSM way | `way/288361188`, 12 vertices | OSM API (measured) |
| Footprint | 14.01 x 19.37 m oriented bbox, area 271.5 m2 | measured from OSM geometry, min-area OBB |
| Anchor (OBB centre) | `-122.4516862, 37.7971579` | derived from the measured geometry |
| Long-axis / ridge bearing | ~31 deg (NNE–SSW) | measured from the OBB |
| Entrance front | faces ESE, bearing ~121 deg, onto Presidio Blvd | *inferred* from street layout + aerial |
| Built | 1912–1917 (sources disagree, see 2.15) | Presidio Trust / pres.house; address listing |
| Original use | Officers' family quarters, 4th Cavalry | pres.house (544, identical sibling) |
| Style | Mission Revival | Presidio Trust rental material |
| Storeys | 2 over a raised base | pres.house; street-level photography |
| Ground-floor ceiling | 10 ft 6 in (3.20 m) | pres.house (544) |
| Walls | Cream stucco | pres.house; photography |
| Roof | Low-pitch hipped, terracotta mission tile, deep eaves | OSM `roof:shape=hipped`, `roof:colour=red`; aerial; photography |
| Chimneys | Two | pres.house (544) |
| Windows | Multi-pane casements, dark frames | pres.house; photography |
| Unit type | Duplex (two front doors) | *inferred* from photography of the row; the group is 16 duplex units + 4 single-family homes |
| OSM `height` | `8` — this is the **EAVE**, not the crest | OSM tag; corroborated by storey arithmetic (2.3) |
| Eave height | 8.0 m | corroborated: OSM tag AND independent storey arithmetic agree |
| Crest height | **10.6 m** | *estimated* — eave + hip rise at an assumed 4.5:12 pitch (2.3) |
| Nearest neighbour | 543 Presidio Blvd, 25.1 m centre-to-centre | measured from OSM |
| District | Presidio of San Francisco National Historic Landmark District (designated 1962) | NRHP #66000232 |

### 2.2 Sources

- https://www.openstreetmap.org/way/288361188 — footprint, `height=8`, `roof:shape=hipped`, `roof:colour=red`
- https://nominatim.openstreetmap.org/ — address resolution within the SF bbox
- https://pres.house/ — 544 Presidio Boulevard, the identical sibling next door: 1912, 4th
  Cavalry officers' quarters, cream stucco, low terracotta roof, arched entry, two working
  chimneys, original casement windows, two floors, 10 ft 6 in ground-floor ceiling, restored
  2023. The strongest single source for the type; also carries a street-level elevation photo.
- https://www.nps.gov/prsf/learn/historyculture/presidio-architecture.htm — Presidio building
  families; 473 of ~790 buildings are contributing historic structures
- https://www.nps.gov/prsf/learn/historyculture/queen-anne.htm — the competing Queen Anne
  attribution for "Funston and Presidio Boulevards" quarters (see 2.15)
- https://presidio.gov/rent-a-home — Presidio Trust: the Presidio Boulevard homes are Mission
  Revival four-bedroom duplexes and single-family houses built for officers' families during WWI
- https://noehill.com/sf/landmarks/nat1966000232.aspx — NRHP #66000232, the NHL district
- Esri World Imagery (z20 aerial, retrieved 12 August 2026) — roof form, ridge orientation,
  eave overhang, tile colour

### 2.3 Height derivation (the key number)

OSM says `height=8`. Per the pipeline's standing correction, an OSM height tag is not the
architectural top; here it is demonstrably the eave, and independent arithmetic lands on the
same figure:

| Component | Value | Basis |
|---|---|---|
| Raised base above grade | 1.10 m | ~6 risers at 0.18 m, observed in street photography |
| Ground floor | 3.60 m | 3.20 m verified ceiling + 0.40 m structure |
| Second floor | 3.25 m | ~2.90 m ceiling + 0.35 m structure/plate (*estimated*) |
| **Eave above grade** | **7.95 m ≈ 8.0 m** | sum — matches the OSM tag exactly |
| Hip rise | 2.60 m | half-span 7.0 m at 4.5:12 (20.6 deg) (*estimated*) |
| **Crest above grade** | **10.55 m ≈ 10.6 m** | eave + hip rise |

The pitch is the only free parameter and the dominant uncertainty: 4:12 gives 10.3 m, 6:12
gives 11.5 m. Band the crest at **10.6 ±0.6 m** until the executing agent verifies the pitch.
Mission tile requires roughly 4:12 minimum, which floors the estimate.

Geometry cross-check: with equal pitch on all four sides, a full hip over a 14.01 x 19.37 m
plan gives a ridge of 19.37 − 14.01 = **5.36 m**, about a quarter of the length. The aerial is
consistent with that, which supports equal-pitch full hips rather than a cross-hip.

### 2.4 What each side shows

**ESE (Presidio Boulevard front)** — The hero elevation. Raised base with concrete entry
steps; a full-width recessed porch behind four chunky square stucco columns with simple
capitals; a solid stucco balustrade wall at porch-rail height; two front doors side by side
(duplex); above the porch a terracotta **pent roof / belt course** on a bracketed cornice;
then the upper storey with tall dark multi-pane casements and small iron balconettes at the
sills; then the deep eave and hip roof.

**WNW (rear)** — *inferred*: plainer, service side facing the rise; the aerial shows a small
projection on this face (rear porch or stair). No verified imagery.

**NNE / SSW (ends)** — *inferred*: the short gable-less hip ends, two window bays each,
chimneys emerging near the eave line. The aerial shows a small notch on each long side, read
here as a chimney breast and a bay.

**Top** — Low hipped terracotta tile roof, ridge on the long NNE–SSW axis, ridge ~5.4 m long,
four hip planes, deep overhanging eaves with a visible shadow line, two chimneys. This is the
surface the app camera actually sees.

### 2.5 Recognition cues (ranked)

1. The low terracotta hipped tile roof with deep overhanging eaves — the Presidio's
   signature roofscape, and at this scale the whole read
2. A quiet cream stucco two-storey box, restrained and near-symmetrical
3. The tiled pent roof / belt course splitting the two floors over a recessed porch
4. Chunky square porch columns above a solid stucco balustrade
5. Two chimneys and a raised base on a green rise

### 2.6 Miniature translation

**Preserve**

- The roof: pitch, hip form, deep eave overhang, terracotta colour
- The two-band facade split created by the pent roof
- The porch void — the shadow under it is what stops the box reading as a slab
- The raised base; the house sits above its ground

**Simplify / exaggerate**

- Exaggerate the eave overhang slightly (0.9 m rather than a scale ~0.6 m) — it is the
  single feature that makes the roof read from above
- Multi-pane casements become plain recessed rectangles; no muntin geometry
- Balconettes become a single thin bar each, or are dropped if they cost more than they read
- Porch balustrade becomes one clean stucco parapet volume
- Roof tile is a flat colour with, at most, a light course banding — no modelled tiles
- Two front doors kept as a deliberate cue: it reads as a duplex, not a villa

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render. Long axis on bearing 31 deg.

1. Base/plinth: 14.0 x 19.4 m, z=0 to z=1.1, `Toy_stone`, inset 0.1 m from the wall line.
2. Body: 13.8 x 19.2 m, z=1.1 to z=8.0, `Toy_cream`.
3. Pent roof / belt course: continuous band at z=4.7, projecting 0.5 m, 0.35 m thick,
   `Toy_brick`, on a thin `Toy_trim` cornice.
4. Porch: recess the ESE face 2.2 m deep from z=1.1 to z=4.7; 4 columns 0.45 x 0.45 m,
   `Toy_trim`; solid balustrade wall 1.1 m high, 0.3 m thick, `Toy_trim`.
5. Entry steps: 3.0 m wide, 6 risers, `Toy_stone`, centred on the ESE face.
6. Doors: two 1.0 x 2.1 m recessed panels, `Toy_ink`, under the porch.
7. Upper windows: recessed 0.15 m, 1.1 x 1.9 m, `Toy_glass` in `Toy_ink` reveals —
   4 bays on each long face, 2 on each short face.
8. Main roof: hipped, eave at z=8.0, crest at z=10.6, ridge 5.4 m on the long axis,
   eave overhang 0.9 m all round, `Toy_brick`; thin `Toy_trim` fascia at the eave.
9. Chimneys: 2, 0.9 x 0.6 m, rising to z=11.4, `Toy_cream` with a `Toy_ink` cap.
10. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | stucco walls, chimney shafts |
| `Toy_brick` | `#c96f4a` | main hip roof and pent roof — the terracotta tile |
| `Toy_trim` | `#f3efe6` | porch columns, balustrade, cornice, eave fascia |
| `Toy_stone` | `#d9d2c2` | raised base and entry steps |
| `Toy_glass` | `#2a4d73` | windows |
| `Toy_ink` | `#3a3530` | window reveals, doors, chimney caps |
| `Toy_glass_Glow` | `#2a4d73` | the 3 lit upper windows at night |
| `Toy_white_Glow` | `#f7f4ec` | the porch soffit / entry light |

Night glow: hero = the warm porch entry light under the pent roof; supporting = three lit
upper windows. Two glow materials, both of which share a hex with a non-glow palette
neighbour, so the day render is unaffected — `Toy_glass_Glow` windows are indistinguishable
from `Toy_glass` windows in daylight. A house is not a skyline piece: keep it to a lamp and a
few windows, and let the row read as quiet.

### 2.9 Top surface

At 10.6 m tall with a 271 m2 footprint, this asset is mostly roof. The roof is not decorated
with rooftop programme — a 1917 house has none, and inventing HVAC or solar would violate
rule 5 — so it must earn its read purely through form: a crisp ridge, four clean hip planes,
a deep eave with a real shadow line, a subtle tile course banding, and the two chimneys as
the only vertical incident. Get the eave shadow right and the asset works; get it wrong and
this is a red box.

### 2.10 Scope

**In the GLB:** the house — raised base, two storeys, porch, pent roof, main hipped roof,
chimneys.

**Not in the GLB:** Presidio Boulevard, Sumner Avenue, the neighbouring houses at
540/541/543/544, detached garages, retaining walls, cypress and eucalyptus, hedges, lawns,
people, vehicles, plinths, cameras or lights.

### 2.11 Triangle budget

Cap 8,000 — deliberately far below the 27,000 landmark ceiling, because this is a small
simple house and the shared batch is a common resource. Suggested split: body and window
recesses ~3k, roof and eave ~2k, porch and columns ~1.5k, base and steps ~0.8k, chimneys
~0.4k. If the first pass exceeds the cap, the fault is modelled detail that the aerial camera
cannot resolve — remove it rather than raising the cap.

### 2.12 Draft manifest entry

```json
{
  "id": "542-presidio-blvd",
  "file": "542-presidio-blvd.glb",
  "anchor": [
    -122.4516862,
    37.7971579
  ],
  "targetHeightM": 10.6,
  "cat": 1,
  "name": "542 Presidio Boulevard",
  "estimated": true,
  "loadRadius": 2500,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`"estimated": true` because the crest height is derived, not published — flip it to `false`
only if the executing agent finds a published or surveyed height.

`loadRadius` 2500 is the default rule's floor (`max(2500, 10.6 * 30)` = 2500). The far
stand-in is the baked procedural house; with the small exclusion radius below, the absence
past the radius is a single missing 14 x 19 m house in a wooded block, which is illegible
well before 2500 m.

### 2.13 Integration notes (for later, not this task)

Two traps here, both worth reading before touching the registry:

- **The exclusion radius must be small — 14 m.** Most landmarks use `exclude: 70–120`,
  which here would be destructive: an 80 m radius would delete six or seven baked
  neighbours that have no GLB to replace them, punching a hole in the middle of the row.
  Measured from the anchor against actual ring geometry (not centroids): 542's own
  footprint reaches **11.3 m**, the nearest neighbour vertex — 543 Presidio Blvd,
  `way/288361199` — is **18.1 m**, and 541 is 20.2 m. `excluded()` in
  `pipeline/buildings.mjs` tests every ring vertex, not just the centroid, so the safe
  band is 11.3–18.1 m; **14** leaves ~2.7 m over its own ring and ~4.1 m of clearance to
  543. This matches the tight-band precedent set by `380Brannan` (9) and `550Third` (8).
- **The registry id is `542PresidioBlvd`.** `camelId()` in `app/src/assets.js` is just
  `id.replace(/-([a-z])/g, ...)`, so the manifest's `542-presidio-blvd` maps to
  `542PresidioBlvd`, and that is what `pipeline/lib/landmarks.mjs` must use. Registry ids
  are quoted string values, not bare identifiers, so a leading digit is fine —
  `380Brannan`, `550Third` and `375Alabama` are already in there. (An earlier draft of
  this plan claimed a digit-leading id was illegal and proposed `presidioBlvd542`; that
  was wrong, and using it would have broken the id round trip.)
- **New landmark**: needs the `pipeline/lib/landmarks.mjs` entry and a re-bake of the affected
  tiles, plus audit 1.6 per `INTEGRATION-PROMPT.md`.
- No camera preset is warranted: a 10.6 m house does not deserve a search/fly-to preset of its
  own. Omit `camera` unless David asks for it.
- Terrain: the house sits on a rise above the boulevard. Confirm it seats on
  `sampleElevation` without floating or sinking — this slope is steeper than most landmark
  sites and is the likeliest local QA failure.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bbox top normalised to the verified crest so loader scale lands at 1.0
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 8,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the porch light and the three lit upper windows
- [ ] Glow materials' day colors match their non-glow palette neighbours
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + night render + contact sheet regenerated from the final export
- [ ] Real-world heading recorded, and the `-Y` front deviation documented
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **Roof pitch drives the crest.** 10.6 m is derived, not published. The band is 10.0–11.2 m.
  This is the number most likely to be wrong and the one the loader scales by.
- **Style attribution conflicts.** NPS describes the officers' quarters at "Funston and
  Presidio Boulevards" as Queen Anne (1880–1890); the Presidio Trust describes the Presidio
  Boulevard homes as Mission Revival built during WWI. The physical evidence for 542 —
  hipped red tile roof, cream stucco, casements, pent belt course — is decisively Mission
  Revival, and the Queen Anne reference almost certainly points at the older Funston Avenue
  row a few blocks away. Resolved in favour of Mission Revival, but flagged.
- **Build date conflicts**: 1912 (pres.house, for 544) vs 1917 (address listing, for 542).
  The row may have been built in phases. Not load-bearing for the model; do not assert a
  single year in `REPORT.md` without a better source.
- **Duplex vs single-family unverified for 542 specifically.** The group is 16 duplex units
  plus 4 single-family homes. The two-front-door cue is taken from photography of a sibling.
  If 542 turns out to be single-family, drop the second door.
- **No verified imagery of the rear or the two end elevations.** They are inferred from the
  type and the aerial and are labelled as such. 542 sits behind a wooded rise and is not
  usefully covered by street-level imagery; the neighbours are.
- **Sibling reuse.** 540–547 are near-identical. If this asset lands well, it is a strong
  candidate to become a small reusable Presidio-quarters kit piece rather than eight separate
  landmarks. Worth a decision from David before modelling the second one.
