# 540 Presidio Boulevard — SF-SIM asset plan

A 1912 Colonial Revival officers' quarters in the Presidio of San Francisco, now a two-unit
residence. It is not a skyline landmark and it never will be: it is one house in a short row of
four near-identical houses on a wooded rise above Presidio Boulevard. That is exactly what makes
it worth authoring carefully — the model has to earn its place by being *the house*, not *a*
house, when the camera comes down to it.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/540-presidio-blvd/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `540-presidio-blvd` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4519267, 37.7966669` |
| Target height | **11.5 m** to the chimney caps (*estimated*; eave 8.0 m is the only measured datum — see 2.1). Ridge as built is 10.5 m — see `artifacts/540-presidio-blvd/REPORT.md` |
| OSM footprint | way/288360343, 247.6 m², oriented bounding box 14.47 x 19.72 m at +6.49° |
| Triangle cap | 6,000 |
| Category | `1` (House) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 540 Presidio Boulevard GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 540 Presidio Boulevard, San Francisco (a 1912
Colonial Revival officers' quarters in the Presidio) and deliver it as a downloadable,
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
7. `artifacts/fairmont-san-francisco/` — the closest reference implementation of this exact
   deliverable, and the one whose REPORT.md explains the night-glow constraint properly
8. `docs/asset-plans/540-presidio-blvd.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Low-pitched hipped **terracotta tile roof** with wide overhanging eaves — the row's signature
  and, from the app's downward camera, the whole building
- Two-storey **cream stucco** box on a raised base, calm and symmetrical
- A **full-width covered porch** with square columns across the east (street) front — the
  building's one projecting mass, mapped in OSM as a 9.8 x 1.74 m bump-out
- **Two chimneys** — the tallest elements, and a named identity feature of the row
- A regular grid of tall, dark, graphical windows; no interiors
- The raised foundation with entry steps up to the porch

## Research 540 Presidio Boulevard independently

Verify the dossier in this plan rather than trusting it. The height in particular is a
derivation, not a published figure: re-check it, and if you find a measured architectural
height, use it and say so loudly. Re-check at minimum the architectural height, the
footprint, the WGS84 anchor, and the real-world orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views (the roof is the hero surface)
- Ground-level views
- Day and night appearance
- Presidio Trust / NPS historic building inventory records for the 500-block of Presidio
  Boulevard, which is the most likely source of a measured height or an elevation drawing
- The neighbouring houses 541, 542, 543 Presidio Boulevard and 544 (Presidio House): the row
  is a family, and any one of them is legitimate evidence for the shared elements

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/540-presidio-blvd/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3-5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. Every number that is a
derivation rather than a published figure must be labelled *estimated* with its derivation
shown. A contact sheet of attributed reference thumbnails is welcome if legally permissible —
do not commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

This is a *small* building, so §21's detail budget puts it near "secondary building": clear
massing, facade rhythm, a designed roof, one or two identity cues. Resist the urge to spend
the triangle budget just because it is there. The failure mode to avoid is a generic
low-poly house — the fix for that is architectural specificity (eave depth, porch column
rhythm, chimney placement, tile roof reading), not more polygons.

The finished asset must be immediately recognizable as a Presidio officers' quarters,
consistent with the real building from all four sides and above, architecturally credible,
and a premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the house: main block, porch, roof, chimneys, foundation base, entry steps, and at
most a pair of clipped hedges flanking the entry as scale cues.

Do not include unrelated surrounding city geometry: Presidio Boulevard itself, the
neighbouring houses at 541/542/543, Lovers' Lane, the cypress and eucalyptus stand, the
detached garage, terrain, lawns, fences, people, vehicles, plinths, cameras or lights.
Temporary context may appear in review renders but must not leak into the GLB. In
particular: **no ground pad.** The loader seats the asset on baked terrain, and a pad would
either float or sink.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 6,000 triangles.

**Normalize the bbox top to the verified height exactly.** The loader scales by
`targetHeightM / measuredHeight`, so the model's maximum Z must equal the height you put in
the manifest — the chimney cap. Scale must land at 1.000.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The porch and main
entrance face **east**, onto the walk that descends to Presidio Boulevard. The building's
plan is yawed **+6.49° CCW** from the cardinal grid; author that yaw into the geometry.
Record the decision and the measured heading in `REPORT.md`.

**Night state is required.** Read the "Night state, and what actually triggers it" section of
`artifacts/fairmont-san-francisco/REPORT.md` before designing it. The binding constraint: a
`_Glow` face is still drawn in daylight at 12% opacity, so every glow surface must be a thin
veneer with solid body geometry directly behind it. Keep the composition restrained — one
hero glow plus a few supporting accents — and make sure the day colours of the glow
materials match non-glow palette neighbours.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless only: `blender -b --python script.py -- args`; no GPU, so use
Workbench or CPU Cycles. Keep `artifacts/540-presidio-blvd/build_540_presidio_blvd.py`
(deterministic build script), `artifacts/540-presidio-blvd/540-presidio-blvd.blend`, and
`artifacts/540-presidio-blvd/540-presidio-blvd.glb`. The script must rebuild the model
reliably enough for future revision. Do not modify or rename an unrelated existing GLB to
satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`540-presidio-blvd-top.png`, `540-presidio-blvd-north.png`, `540-presidio-blvd-east.png`,
`540-presidio-blvd-south.png`, `540-presidio-blvd-west.png`, plus
`540-presidio-blvd-contact-sheet.png` and at least one high three-quarter aerial beauty
render `540-presidio-blvd-aerial.png`, plus a night render `540-presidio-blvd-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the hipped roof's ridge and four hips,
the eave overhang, the porch roof and both chimneys; the aerial view uses the style bible's
camera assumptions (30-50 degrees down, long lens). Simple tabletop lighting, neutral warm
background, minimal depth of field, and every image must depict the same exported model.
The day renders must put alpha 0.12 on the `_Glow` materials, matching what the app actually
draws at noon.

## Validate the exported GLB

Re-import `540-presidio-blvd.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/540-presidio-blvd/validation.json` and
`artifacts/540-presidio-blvd/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "540-presidio-blvd",
  "file": "540-presidio-blvd.glb",
  "anchor": [
    -122.4519267,
    37.7966669
  ],
  "targetHeightM": 11.5,
  "cat": 1,
  "name": "540 Presidio Boulevard",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or
any app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in
`docs/asset-plans/540-presidio-blvd.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *estimated* are visual or
derived, not published figures — the executing agent must re-verify anything it relies on.
This dossier is unusually honest about its gaps because the subject is a minor historic
residence, not a documented landmark: there is no Wikidata height, no architect monograph,
and no published elevation drawing that this research could reach.

### 2.1 Verified facts

| Fact | Value | Confidence |
|---|---|---|
| Address | 540 Presidio Boulevard, San Francisco, CA 94129 | verified (Nominatim, OSM `addr:*`) |
| OSM feature | way/288360343, `building=yes` | verified |
| Anchor (OBB centre) | −122.4519267, 37.7966669 | verified (derived from OSM geometry) |
| Footprint area | 247.6 m² | verified (OSM polygon, local tangent projection) |
| Oriented bounding box | 14.47 m (E–W) × 19.72 m (N–S) | verified (min-area rectangle over OSM geometry) |
| Plan yaw | +6.49° CCW from the cardinal grid | verified (min-area rectangle) |
| Roof shape | hipped | verified (OSM `roof:shape=hipped`) |
| Roof colour | red | verified (OSM `roof:colour=red`); terracotta tile per the row's description |
| OSM `height` | 8 m | verified as a *tag*; read here as the **eave**, not the top — see below |
| Year built | 1912 | verified (Presidio House, the same row; NPS/Presidio Trust material on the ~1912 officers' row) |
| Original use | US Army officers' family quarters (4th Cavalry era) | verified |
| Current use | two-unit residence (units A and B), 4 bed / 2.5 bath, ~1,620 sq ft per unit | verified (rental listings) |
| Storeys | 2 over a raised basement | verified for the row (Presidio House: "Two floors", 10' 6" ground-floor ceilings) |
| Wall finish | cream stucco | verified for the row |
| Chimneys | two | verified for the row |
| Entry | arched entry behind a covered porch | verified for the row |
| Windows | original casement | verified for the row |
| Architectural height | **11.5 m to the chimney caps** | ***estimated*** — derivation below |

**The height derivation, in full, because it is the weakest number in this plan.**
No published architectural height was found. The chain is:

1. OSM tags `height=8` on 540 *and identically on 541, 542 and 543* — a uniform tag across the
   row, which is how eave/gutter heights usually get entered for a repeated housing type.
   AGENTS' iron rule and the pipeline doc both warn that an OSM `height` on a pitched-roof
   building describes a low shell and must never be the target height.
2. That 8 m reconciles exactly with the storey stack the row's own documentation gives:
   1.1 m raised basement/plinth to the first floor + 3.7 m first floor (10' 6" ceiling plus
   structure) + 3.2 m second floor = **8.0 m to the eave**. Two independent routes agreeing on
   8.0 m is the reason this plan treats 8 m as the eave rather than the top.
3. Hip rise: the main block is 11.44 m across its short (E–W) span, so a 4:12 pitch — the
   normal range for a low Mission/Colonial Revival tile roof — rises 5.72 × 0.3333 = 1.91 m
   over the half-span. Ridge ≈ **9.9 m**. *(Pitch is the estimate; ±1:12 moves the ridge
   ±0.5 m.)* **As built this became 10.5 m**: the roof springs from the overhang edge, not
   the wall face, and 4:12 read as a flat plate from the app camera. The 11.5 m top is
   unchanged. See REPORT.md "Corrections made to the plan".
4. Chimneys clear the ridge by ~1.6 m. Architectural top = **11.5 m**.

5. **External check.** `1008-general-kennedy`, researched independently for this same repo from
   a different evidence base (DataSF LiDAR + Overture), landed on eave 7.8 m, ridge 10.9 m,
   chimney crest 11.9 m for the same Presidio type. Every level of that stack agrees with this
   one to within 0.4 m. Two buildings of a type is not a survey, but it is a great deal better
   than one derivation standing alone.

The manifest entry therefore ships with `"estimated": true`. If a Presidio Trust or NPS
inventory record with a measured height surfaces later, it supersedes this entirely, and the
correction is a one-line manifest edit plus a rebuild with the new `Z_CREST`.

### 2.2 Sources

| Source | Establishes |
|---|---|
| OpenStreetMap way/288360343 (+ 541/542/543 and the surrounding ways) | footprint geometry, address, roof shape and colour, the `height=8` tag, the row's uniformity, the position of Presidio Boulevard and the entry footways |
| Nominatim geocode of "540 Presidio Blvd, San Francisco, CA 94129" | address → OSM feature resolution |
| [Presidio House, 544 Presidio Boulevard](https://pres.house/) | the row's architecture in the owner's own words: "Cream stucco, a low terracotta roof, a pair of chimneys, and an arched entry"; 1912 construction as officers' quarters, 4th Cavalry; two floors; 10' 6" ground-floor ceilings; original casement windows; and a photograph of the front elevation |
| [NPS — Presidio of San Francisco Architecture](https://www.nps.gov/articles/presidio-architecture.htm) | Colonial Revival as the Presidio's early-1900s design language |
| [FoundSF — Presidio Officers Row](https://www.foundsf.org/Presidio_Officers_Row) | the ~1912 officers' quarters row, and that it mixes single units, duplexes and quadruplexes |
| Rental listings for 540 Presidio Blvd units A and B | duplex, 4 bed / 2.5 bath, ~1,620 sq ft per unit, detached single-car garage, basement |
| [`docs/asset-plans/1008-general-kennedy.md`](./1008-general-kennedy.md) and `artifacts/1008-general-kennedy/` | the closest built precedent: another Presidio two-storey stucco building under a red tile hipped roof with terracotta chimneys through the ridge. Its independently researched numbers — **eave 7.8 m, ridge 10.9 m, chimney crest 11.9 m** — corroborate this plan's derivation (8.0 / 9.9 / 11.5) to within 0.4 m at every level, which is the strongest external check available for the height |

Not reached, and worth trying again: the Presidio Trust / NPS historic building inventory
record for this building number, which is the most likely home of a measured height or an
elevation drawing. Google Street View and Bing Bird's Eye were both unavailable in this
session's browser, so the four-side observation in 2.4 leans on the row rather than on
direct imagery of 540 itself. That is a real limitation and is called out again in 2.15.

### 2.3 Orientation and placement

- **Anchor:** −122.4519267, 37.7966669 — the centre of the oriented bounding box, not the
  polygon centroid. The two bump-outs are on opposite sides and roughly balance, so the two
  differ by well under a metre here, but the OBB centre is the point the massing is built
  around and therefore the correct anchor.
- **Yaw:** the plan's long axis bears +6.49° CCW of true north. Authored into the geometry;
  manifest `yawDeg` stays absent (0).
- **Front:** **east.** Three independent signals agree — the 9.8 m porch bump-out is on the
  east face; the OSM footways that serve the house approach from the east; and Presidio House
  next door describes its living room as facing east for the morning light off the bay. The
  row sits on a rise *above* Presidio Boulevard, which runs below it to the east.
- The house is on Presidio Trust land inside the Presidio, on a wooded slope. The terrain the
  loader samples matters more here than for a downtown asset: at 11.5 m tall, a metre of
  terrain error is 9% of the building.

### 2.4 What each side shows

Confidence note: **east** is the well-evidenced side (photograph of the row's front elevation,
plus the OSM bump-out). North, south and west are read from the footprint plus the type, and
are *inferred*.

| Side | Reads as |
|---|---|
| **East (front)** | The full-width covered porch: square columns on a solid rail, the arched entry behind it, steps down to the walk. Two storeys of tall casement windows above, symmetrical about the entry. The hipped roof's long slope with a deep eave over the whole thing. |
| **North (gable-less end)** | A plain 11.4 m end wall, two storeys, a modest window pair per floor, the roof hipping back from this end. One chimney rides near this end of the ridge. |
| **South** | The mirror of the north end; the second chimney. *inferred* |
| **West (rear)** | The service side: the small 3.96 × 1.3 m bump-out (rear porch or bay), fewer and smaller openings, the ground falling away up the rise. *inferred* |
| **Top** | The hero surface. A hipped tile roof: a short ridge running N–S with four slopes falling away from it, a deep overhang all round casting a hard shadow line onto the walls, the lower porch roof stepping down on the east, and two chimneys breaking the ridge. Terracotta red against cream — the single strongest cue at city distance. |

### 2.5 Recognition cues (ranked)

1. **The low hipped terracotta roof with a deep overhang.** From the app's camera this is 80%
   of the building. Red-orange against a cream box, with a hard eave shadow.
2. **The two chimneys.** They break the ridge and give the silhouette its only vertical
   incident; the row's own marketing names them.
3. **The full-width east porch** with square columns — the one projecting mass, and what says
   "officers' quarters" rather than "house".
4. **Cream stucco, calm and symmetrical**, with a regular grid of tall dark windows.
5. **The raised base and entry steps**, which lift the house off the ground and read at any
   distance as a plinth line.

### 2.6 Miniature translation

Per style bible §22, the compression is:

- Roof pitch and eave depth get the **semantic exaggeration** (§9), not the building height.
  The real eave overhang is perhaps 0.6 m; the model uses **0.9 m**, so the shadow line and
  the tile edge survive at city distance. Nothing else is exaggerated — the massing stays at
  the measured footprint and the derived height.
- Windows become **graphical dark plates in a regular grid** (§5), recessed 0.08 m, no
  mullions, no interiors. Eight per long face per storey is too many at this scale; four
  reads better and stays honest to the rhythm.
- The porch becomes **five square columns** on a solid rail — the count is a rhythm decision,
  not a survey.
- The tile roof is **not** modelled as tiles. It is one clean beveled hipped solid in
  `Toy_brick`, with a thin fascia band under the eave in `Toy_trim`. Tile texture at this size
  is exactly the "microscopic facade geometry" §4 forbids.
- Two clipped hedges flank the steps as the only landscaping — scale cues (§15/§12), 12
  triangles each, and the one piece of environmental storytelling (§16) the budget allows.

### 2.7 Massing recipe

All coordinates in metres, local, before the +6.49° yaw; x east, y north, z up.
Derived directly from the OSM plan de-yawed about the OBB centre:

| Element | Extent | Height |
|---|---|---|
| Foundation plinth | main block footprint, +0.15 m proud | 0.0 → 1.10 |
| Main block | x −5.94…+5.50, y −9.86…+9.86 (11.44 × 19.72) | 1.10 → 8.00 |
| Storey band (floor line) | inset 0.06 m, 0.18 m tall | 4.80 |
| East porch | x +5.50…+7.24, y −4.80…+5.00 (1.74 × 9.80) | 1.10 → 3.60 (roof) |
| West service bay | x −7.24…−5.93, y −1.77…+2.19 (1.31 × 3.96) | 1.10 → 5.20 |
| Hipped main roof | main block + 0.9 m overhang all round | 8.00 → 9.91 (ridge) |
| Eave fascia | the overhang's edge band | 7.80 → 8.10 |
| Porch roof (hipped, shallower) | porch + 0.5 m overhang | 3.60 → 4.35 |
| Chimney N | 0.9 × 0.9, on the ridge at y = +5.6 | → 11.50 |
| Chimney S | 0.9 × 0.9, on the ridge at y = −5.6 | → 11.50 |
| Entry steps (4) | 2.6 m wide, off the porch's east face | 0.0 → 1.10 |
| Hedges (2) | 1.2 × 0.8 each, flanking the steps | 0.0 → 0.9 |

The ridge is a true ridge, not a point: hipped roofs on a 11.44 × 19.72 block hip in from
both ends, leaving a ridge of 19.72 − 11.44 = 8.28 m running N–S. Model it as a six-vertex
solid (four eave corners, two ridge ends), which is both correct and cheap.

### 2.8 Materials and palette

**This building belongs to a family.** `artifacts/1008-general-kennedy/` is the same Presidio
type — two-storey stucco under a red tile hipped roof with terracotta chimneys through the
ridge — and it is already built and shipped. Style bible §24 says families share palette,
window language, slab thickness and roof style, and vary in massing. So the palette below is
1008's palette, changed in exactly one place: the walls are `Toy_cream`, not `Toy_white`,
because the row's own documentation says cream stucco where 1008 is bare concrete.

| Material | Hex | Used on |
|---|---|---|
| `Toy_cream` | `f2ede3` | stucco walls, main block and service bay |
| `Toy_red` | `c4453c` | main roof, porch roof — the tile, matching 1008 |
| `Toy_trim` | `f3efe6` | eave fascia, storey band, porch columns and rail, window sills |
| `Toy_stone` | `d9d2c2` | foundation plinth, entry steps |
| `Toy_brick` | `c96f4a` | the two chimneys — deliberately NOT `Toy_red`, so the stacks read as separate objects from above (1008's reasoning, and it works) |
| `Toy_glass` | `2a4d73` | window plates |
| `Toy_ink` | `3a3530` | the arched front door |
| `Toy_mint` | `8fd0a8` | the two clipped hedges |
| `Toy_glass_Glow` | `6f95b8` | **supporting glow:** lit window panes |
| `Toy_gold_Glow` | `caa64a` | **hero glow:** the porch lantern over the front door |

Ten materials, all from the project palette, no off-palette colours.

**Night design.** Small building, small night state — five glow objects, not sixteen:

| Surface | Material | Reads as |
|---|---|---|
| `glow_lantern` | `Toy_gold_Glow` | the porch lantern over the arched entry — the hero, and the only warm point |
| `win_*_glow` ×4 | `Toy_glass_Glow` | four lit rooms out of sixteen windows, split across two elevations so the night state is not invisible from half the camera's orbit |

Note the glow colour: `6f95b8` (palette `glassl`), not the `2a4d73` of the glass behind it —
a lit pane has to be *lighter* than the dark glass to read as lit, and 1008 established this.
Every glow face is a thin pane 0.04 m proud of the recessed window fill or the porch soffit,
so it always has solid body geometry directly behind it. That is the constraint from
`artifacts/fairmont-san-francisco/REPORT.md` ("a glow face is still drawn in daylight at 12%
opacity") satisfied by construction rather than by hope.

### 2.9 Top surface

The roof *is* the design here (§10). It gets: a genuine hipped solid with a real ridge and
four hips; a 0.9 m overhang reading as a hard shadow line; a `Toy_trim` fascia band at the
eave so the roof edge is a drawn line rather than a colour change; the porch roof stepping
down on the east; and the two chimneys as the only rooftop objects. No vents, no dormers, no
solar — none of them are on this building, and inventing them would break iron rule 5.

### 2.10 Scope

In: the house, its porch, roof, chimneys, plinth, steps, two hedges.
Out: terrain, lawn, the cypress/eucalyptus stand, the detached garage, fences, the boulevard,
the neighbouring houses, and any ground pad whatsoever.

### 2.11 Triangle budget

6,000 cap; the recipe above should land near 3,500. The chunky solids all carry a 0.10 m
2-segment bevel (§4), which is where most of the count goes. If the build comes in under
2,500 the bevel is probably missing.

### 2.12 Draft manifest entry

```json
{
  "id": "540-presidio-blvd",
  "file": "540-presidio-blvd.glb",
  "anchor": [-122.4519267, 37.7966669],
  "targetHeightM": 11.5,
  "cat": 1,
  "name": "540 Presidio Boulevard",
  "estimated": true,
  "dims": [x, y, z],
  "tris": N,
  "loadRadius": 2500
}
```

`estimated: true` because the height is derived, not published (2.1).

`loadRadius: 2500` is the default rule `max(2500, targetHeightM × 30)` = `max(2500, 345)`.
The skill's absence-illegibility test — "beyond the radius the site is empty, so pick a radius
at which that absence is illegible" — passes trivially at any radius past ~600 m for an 11.5 m
house, so there is no reason to tune below the default. `alwaysLoaded` would be absurd here.

`cat: 1` (House). `cat: 2` (Apartments) is defensible for a two-unit rental and the call could
go either way; House matches the built form the model actually shows.

### 2.13 Integration notes (for later, not this task)

**Case B — new landmark.** `540-presidio-blvd` does not exist in `pipeline/lib/landmarks.mjs`
or `app/src/landmarks.js` (the only Presidio entry there is the `presidio` POI label at
−122.4662, 37.7989, which is unrelated). Integration therefore needs the registry entry, the
exclusion zone that carves the baked procedural box out of the tile, and a tile re-bake —
follow `docs/asset-plans/INTEGRATION-PROMPT.md` and its audit step 1.6.

The exclusion zone must cover this footprint **only**. Its neighbours 541, 542 and 543 are
separate OSM buildings a few metres away and must keep their baked versions; a radius tuned by
eye will eat them. Use the footprint, not a generous circle.

### 2.14 Validation checklist

- Re-import the exported GLB into a fresh scene; validate the re-import.
- Max Z = 11.50 exactly, min Z = 0.00, XY centre offset = (0, 0) — so the loader's scale is
  1.000.
- Dimensions ≈ 16.7 × 22.8 × 11.5 as built (the roof overhang widens the footprint bbox
  past the 14.47 × 19.72 walls; the yaw widens it again).
- ≤ 6,000 triangles.
- Materials exactly the nine in 2.8; no textures, no alpha < 1, no `Toy_body`.
- No cameras, lights, animation, armatures, constraints; transforms applied; no negative
  scales.
- Normals outward: every solid here is closed, so the per-object signed-volume test is
  authoritative and must be positive for all of them, with the ray test at zero residual.
- Renders: five elevations + top + aerial + night + contact sheet, all from the re-imported
  GLB, day renders at glow alpha 0.12.

### 2.15 Open questions and risks

1. **The height is derived, not measured.** This is the plan's one real weakness and it is
   labelled everywhere it appears. Two independent routes agree on the 8.0 m eave, which is
   reassuring; the 4:12 pitch and the 1.6 m chimney clearance above the ridge are not
   independently corroborated. Worst case the top is off by ~0.7 m (6%).
2. **Three of the four elevations are inferred** from the footprint and the building type.
   Street-level imagery of 540 itself was not reachable in this session (Google Maps, Bing
   Maps and Mapillary all failed to load in the available browser). The east front is well
   evidenced; north, south and west are honest reconstructions of a type, not observations.
   Anyone with Street View access should spend five minutes checking them before the model is
   treated as settled.
3. **The row is four near-identical houses.** Building this one and not 541/542/543 leaves a
   bespoke house standing next to three baked boxes. That is a visible inconsistency at close
   range, and the honest fix is either to build the row as a family later (§24) or to accept
   it. It is not a reason to skip the exclusion zone — a doubled building is worse.
4. **A duplex, not a mansion.** This is the smallest bespoke landmark in the set by a wide
   margin. It earns its place as a Presidio character piece, not a skyline one, and the
   budgets in this plan are set accordingly.
5. **Terrain sensitivity.** On a wooded rise, at 11.5 m tall, terrain sampling error is
   proportionally large. Verify the seating at street level during integration QA, not just
   from the air.
