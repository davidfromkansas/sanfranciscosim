# San Francisco Civic Center Courthouse — SF-SIM asset plan

The 1997 Superior Court building at 400 McAllister Street: a six-storey light-granite
block that answers Beaux-Arts Civic Center on two sides and the modern city on the other
two, and turns its chamfered McAllister/Polk corner into an octagonal lantern with round
oculi under a shallow dome. That corner lantern is the whole asset's identity.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/civic-center-courthouse/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `civic-center-courthouse` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4192590, 37.7804897` (measured OBB centre, OSM way/108389188) |
| Target height | **29.6 m** — crest of the corner lantern dome (2010 city LiDAR `hgt_max`); main parapet 25.0 m (OSM `height=25`, LiDAR median 24.7 m) |
| OSM footprint | 83.46 x 36.98 m oriented bbox, 3,073 m² polygon, long axis bearing **81.22°** cw from N |
| Triangle cap | 22,000 |
| Category | `18` (government / courthouse) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready San Francisco Civic Center Courthouse GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the San Francisco Civic Center Courthouse
(400 McAllister Street) and deliver it as a downloadable, validated GLB.

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
7. `artifacts/war-memorial-opera-house/` — the nearest reference implementation of this
   exact deliverable, three blocks away and on the same street grid (dossier,
   deterministic build script, validator, renders, report)
8. `docs/asset-plans/civic-center-courthouse.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The chamfered McAllister/Polk corner: recessed glazed entrance under a tall flat arch,
  a projecting glazed bay above it, and an **octagonal lantern with large round oculi
  under a shallow dome** — the single recognition cue
- A giant round-arched arcade over a two-storey rusticated base on the McAllister (south)
  and Polk (east) elevations
- The attic band of small square windows and the projecting cornice that runs the whole
  classical frontage
- The plainer, contemporary north (Golden Gate Avenue) and west elevations: a flat
  punched/banded window grid, no arcade
- A designed roof: perimeter parapet, long louvered mechanical penthouse, two HVAC
  clusters, and the lantern rising clear of everything

## Research the courthouse independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams — the architect (Mark Cavagnero
  Associates) publishes a McAllister Street elevation, a site plan, an upper floor plan
  and study-model photographs
- Which corner carries the lantern, and how far the lantern rises above the parapet
- Whether the OSM `height=25` tag is the parapet or the crest (it is the parapet)

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/civic-center-courthouse/REFERENCE.md` containing: source links and what
each establishes; verified dimensions and location; orientation; observations from all
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

The finished asset must be immediately recognizable as the Civic Center Courthouse,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel art,
not generic low-poly, and never accurate in one view while invented in the others.

It also has to sit convincingly beside `city-hall`, `opera-house` and
`st-marys-cathedral`, which are already in the scene: same slab thicknesses, same
bevel weight, same restrained palette. This building is the greyest and flattest of
the Civic Center set — let it be a calm neutral next to City Hall's dome, and spend the
personality budget entirely on the corner lantern.

## Scope of the exported asset

Export the courthouse block only: base, arcade, attic, cornice, parapet, roof plant and
the corner lantern.

Do not include unrelated surrounding city geometry: the Earl Warren Building next door,
the State Building, Civic Center Plaza, McAllister/Polk/Golden Gate streets, trees,
people, vehicles, plinths, cameras or lights. Temporary context may appear in review
renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 22,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The long axis bears
**81.22° cw from true north**; the ceremonial front faces **south** onto McAllister
Street, so the contract's "front faces −Y" rule is honoured almost literally here.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Headless only: `blender -b --python script.py -- args`; no GPU, so use Workbench or
CPU Cycles. Keep `artifacts/civic-center-courthouse/build_civic_center_courthouse.py`
(deterministic build script),
`artifacts/civic-center-courthouse/civic-center-courthouse.blend`, and
`artifacts/civic-center-courthouse/civic-center-courthouse.glb`. The script must rebuild
the model reliably enough for future revision. Do not modify or rename an unrelated
existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`civic-center-courthouse-top.png`, `-north.png`, `-east.png`, `-south.png`, `-west.png`,
plus `-contact-sheet.png`, at least one high three-quarter aerial beauty render
`-aerial.png`, and a night render `-night.png` showing the glow set.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the parapet, the louvered
penthouse, the HVAC clusters and the corner lantern; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `civic-center-courthouse.glb` into a fresh isolated Blender scene and validate
the re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/civic-center-courthouse/validation.json` and
`artifacts/civic-center-courthouse/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "civic-center-courthouse",
  "file": "civic-center-courthouse.glb",
  "anchor": [
    -122.4192590,
    37.7804897
  ],
  "targetHeightM": 29.6,
  "cat": 18,
  "name": "Civic Center Courthouse",
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
`docs/asset-plans/civic-center-courthouse.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Fact | Value | Source |
|---|---|---|
| Official name | San Francisco Civic Center Courthouse | OSM `name`, Superior Court of California |
| Address | 400 McAllister Street, San Francisco, CA 94102 | OSM `addr:*`, court website |
| OSM element | way/108389188, `amenity=courthouse`, `building=government`, surveyed 2026-02-23 | Overpass |
| Opened | 9 December 1997 (construction 1995–98) | architect / court sources |
| Architects | Lee/Timchula Architects with Mark Cavagnero Associates (local architect) | Cavagnero project page |
| Size / program | 224,000 sq ft, 44 courtrooms plus administration | Cavagnero project page |
| Storeys | six | courthouse references |
| Footprint (measured) | 83.46 x 36.98 m minimum-area oriented bbox; 3,073 m² polygon area | OSM geometry, reprojected |
| Long-axis bearing (measured) | **81.22°** cw from true north | same |
| OBB centre (measured) | −122.4192590, 37.7804897 | same |
| Polygon centroid (measured) | (1605.03, −1159.57) local m; OBB centre (1605.13, −1159.54) — they agree to 0.1 m, so the OBB centre is a safe anchor | same |
| Parapet height | 25 m | OSM `height=25`; 2010 city LiDAR median 24.67 m, mean 25.19 m over 12,618 cells |
| **Crest height** | **29.6 m** | 2010 city LiDAR `hgt_max` 29.60 m (mblr SF0766002) |
| Ground elevation | ~20.2 m NAVD88 | LiDAR `gnd_min_m` |
| Corner treatment | SE corner chamfered ~6.1 m across (the OSM polygon carries the chamfer explicitly) | OSM geometry |

### 2.2 Sources

- OSM way/108389188 via the Overpass API — footprint geometry, tags, `height`, survey date.
- Nominatim (bounded to the SF bbox) — address resolution, bounding box.
- DataSF *Building Footprints (with LiDAR-derived heights)*, resource `ynuv-fyni`,
  building `SF0766002` — `hgt_min/mean/median/max`, ground elevation. This is the
  authority for the crest, because no published architectural height exists.
- Mark Cavagnero Associates, project page for the San Francisco Civic Center Courthouse —
  **McAllister Street elevation drawing (with a 0–40 ft scale bar), site plan, upper floor
  plan, study-model photographs and a colour exterior photograph of the McAllister/Polk
  corner.** This is the single most useful source and it is the architect's own.
- Esri World Imagery (z19, ~0.24 m/px), rotated to the building axis — the roof plan:
  parapet, the two mechanical clusters, the louvered penthouse, the octagonal lantern.
- Superior Court of California, County of San Francisco — location page, program.

### 2.3 Orientation and placement

Long axis bears 81.22° cw from N — the standard Civic Center grid, identical to the War
Memorial Opera House's 81.11° three blocks south-west. Build frame: `u+` runs ENE along
McAllister, `v+` runs NNW (north). The ceremonial front faces **south** onto McAllister;
Polk Street is the **east** flank; Golden Gate Avenue is the **north** rear; the west
flank abuts the mid-block neighbour.

Two published descriptions conflict on the corner. Courthouse references call the angled
entrance "southeast"; a court-directory page calls the building "the corner of Polk and
McAllister". Both are the same corner: McAllister runs along the building's **south** side
(the courthouse sits north of McAllister, i.e. north of City Hall's block) and Polk is the
east side, so McAllister × Polk **is** the south-east corner. The OSM polygon's 6.1 m
chamfer sits there, and the satellite roof plan puts the octagonal lantern there. Resolved:
**lantern at the SE corner.**

### 2.4 What each side shows

- **South — McAllister Street (the ceremonial front, 83.5 m).** Two-storey rusticated
  granite base with a grid of square punched windows in two rows. Above it a giant order of
  **five round-arched windows** (≈6.0 m wide, ≈9.5 m pitch) set in wide flat piers with
  narrow slot windows; the arcade is centred roughly one third in from the west end. Above
  the arches a plain frieze, then an attic band of ~18 small square windows, then a
  projecting cornice, then a plain parapet. A louvered mechanical penthouse is set back
  behind the parapet. Measured from the architect's elevation (40 ft = 178 px):
  base top ≈7.6 m, arcade sill ≈8.4 m, arch spring ≈15.2 m, arch crest ≈17.9 m,
  attic band 19.3–20.7 m, cornice 20.7–21.6 m, parapet 25.0 m.
- **East — Polk Street (37 m).** The same language, compressed: rusticated base, two giant
  arches, attic band, cornice. Cavagnero: the south and east sides carry the traditional
  materials and detailing.
- **North — Golden Gate Avenue.** The contemporary face. No arcade; a flat granite wall with
  a regular grid of banded/louvered ribbon windows over four storeys above the base
  (clearly visible in the study-model photographs). *Inferred* window counts.
- **West.** Contemporary, plainest of the four, partly blind where it meets the neighbour.
- **SE corner.** Chamfered at 45°, full height. Ground level: a recessed glazed entrance
  under a tall flat arch, flanked by flagpoles. Above: a projecting three-storey glazed bay.
  Above the cornice: a square attic block, then an **octagonal drum carrying large circular
  oculi**, then a shallow segmental dome. Crest 29.6 m.
- **Above.** A bright flat membrane roof inside a continuous parapet; a long louvered
  penthouse running east–west near the south edge; one HVAC cluster centre-west and a
  second at the east end; the lantern clear of everything at the SE.

### 2.5 Recognition cues (ranked)

1. The octagonal lantern with round oculi and a shallow dome on the chamfered corner.
2. The giant round-arched arcade over a heavy rusticated base — five arches on McAllister.
3. Near-white granite: the coldest, lightest wall value in the Civic Center set.
4. The attic band of small square windows under a projecting cornice, running the whole
   classical frontage.
5. The two-faced parti — classical south/east, flat modern north/west.

### 2.6 Miniature translation

Per §22 of the style bible. Keep 1–4; they survive at thumbnail size. Cue 5 survives as a
value/rhythm change only (arcade vs. band), not as a materials change. Drop: the Albert
Paley entrance doors, the granite panel joint pattern, the window mullion grids inside the
arches (one flat `Toy_glass` pane per arch instead), the slot windows in the piers (keep
them as a single narrow recess), the sixth-storey setback on the north.

Exaggerate: the lantern (drum diameter and dome rise both up ~15 % from measured, so the
silhouette reads from the app camera), the cornice projection, and the depth of the
rustication.

### 2.7 Massing recipe

Build frame `(u, v, z)`: `u+` ENE along McAllister at bearing 81.22°, `v+` north,
origin at the OBB centre. `u ∈ [−41.75, +41.75]`, `v ∈ [−18.5, +18.5]`.
South face `v = −18.5`, north `v = +18.5`, east `u = +41.75`, west `u = −41.75`.
SE chamfer: a 6.1 m face at 45°, cutting 4.3 m off each of the south and east faces.

| Element | z range | Notes |
|---|---|---|
| Rusticated base | 0 → 7.6 | proud +0.35 all round; two courses; two rows of square windows |
| String course | 7.6 → 8.0 | proud +0.5 |
| Main granite wall | 8.0 → 19.2 | arcade cut into south and east |
| Giant arches | sill 8.6, spring 15.2, crest 17.9 | 5 on south (pitch 9.5 m, w 6.0), 2 on east |
| Attic band | 19.3 → 20.7 | ~18 small square windows south, 8 east |
| Cornice | 20.7 → 21.7 | proud +0.9 |
| Parapet | 21.7 → 25.0 | plain, capped |
| Roof deck | 24.2 | `Toy_roofd` |
| Louvered penthouse | 24.2 → 28.6 | set back 4 m from the south parapet, ~38 x 9 m |
| HVAC clusters | 24.2 → 26.4 | two, `Toy_steel` |
| Corner attic block | 21.7 → 23.6 | square, chamfered, over the corner bay |
| Octagonal drum | 23.6 → 27.0 | R ≈ 5.0 m, three oculi facing S, SE and E |
| Dome cap | 27.0 → **29.6** | shallow octagonal segmental dome |

### 2.8 Materials and palette

| Surface | Material | Hex |
|---|---|---|
| Rusticated base, string course | `Toy_stone` | d9d2c2 |
| Main granite wall, piers, drum | `Toy_trim` | f3efe6 |
| Cornice, parapet cap, dome | `Toy_white` | f7f4ec |
| All windows, glazed corner bay | `Toy_glass` | 2a4d73 |
| Entrance recess, arch reveals | `Toy_ink` | 3a3530 |
| Roof deck | `Toy_roofd` | 45454a |
| Penthouse louvers, HVAC, flagpoles | `Toy_steel` | 9aa0a6 |
| Lit arch and oculus panes (night) | `Toy_mustard_Glow` | d9a441 |
| Entrance canopy soffit strip (night) | `Toy_white_Glow` | f7f4ec |

The building is deliberately the coldest, lightest of the Civic Center set: `Toy_trim`
walls against the Opera House's `Toy_sand`.

### 2.9 Top surface

Designed, not blank (§10): parapet band, the long louvered penthouse, two HVAC clusters
laid out as the satellite shows them, a stair penthouse, and the lantern. The dome is
`Toy_white` so the corner reads from directly above as a bright disc on a grey field.

### 2.10 Scope

The courthouse block only. No Earl Warren Building, no State Building, no plaza, no street
furniture, no trees, no vehicles, no plinth.

### 2.11 Triangle budget

Cap 22,000; target 10,000–14,000. The arcade (7 arches × ~120 tris with the 10-segment
head), the drum and dome (~1,200), and the window grids dominate.

### 2.12 Draft manifest entry

```json
{
  "id": "civic-center-courthouse",
  "file": "civic-center-courthouse.glb",
  "anchor": [-122.4192590, 37.7804897],
  "targetHeightM": 29.6,
  "cat": 18,
  "name": "Civic Center Courthouse",
  "estimated": false,
  "loadRadius": 2500
}
```

`loadRadius`: the default rule is `max(2500, 29.6 × 30) = max(2500, 888) = 2500`.
A 30 m building is invisible past ~2 km anyway, and the baked procedural block is carved
out under it, so 2500 m is both the rule and the right answer.

### 2.13 Integration notes (for later, not this task)

New landmark — **Case B**. `civic-center-courthouse` exists in neither
`pipeline/lib/landmarks.mjs` nor `app/src/landmarks.js`, so integration needs:

1. a manifest entry (2.12);
2. a registry entry in `pipeline/lib/landmarks.mjs` with id, lon/lat, height and an
   exclusion radius large enough to clear the 83.5 x 37 m footprint (≈50 m);
3. a re-bake of the affected 500 m tiles, or the baked procedural block will intersect the
   GLB;
4. audit 1.6 and `node pipeline/landmark-streaming-check.mjs` against a build.

Run `docs/asset-plans/INTEGRATION-PROMPT.md` for the full procedure.

### 2.14 Validation checklist

`validation.json` must show: fresh-scene re-import; `min_z ≈ 0`; XY centre within 0.5 m;
dims ≈ 83.5 x 37.0 x 29.6 m; tris ≤ 22,000; zero image textures; zero transparent
materials; every material `Toy_*` and none named `Toy_body`; no cameras, lights,
animation, armatures or constraints; transforms applied; no negative scales; normals
outward by the per-object signed-volume test with the ray test as a supplementary metric;
glow materials present and shipping with emission strength 0.

### 2.15 Open questions and risks

- **No published architectural height.** 29.6 m is 2010 LiDAR, not a citation. The building
  has not changed since, and OSM's independently surveyed `height=25` agrees with the same
  dataset's median, which is a good cross-check — but it is still *derived*, and the
  manifest entry should say so if the executing agent cannot do better.
- **North and west elevations are *inferred*** from study-model photographs; window counts
  and band positions there are design decisions, not measurements.
- **Arch count on Polk is *inferred*** (two) from the corner photograph; the architect
  publishes only the McAllister elevation.
- The 2010 LiDAR predates any rooftop plant added since; the penthouse height 28.6 m is
  *inferred* to sit below the 29.6 m crest.
- Facade colour is judged from photographs taken in bright sun; the real granite may read
  slightly greyer than `Toy_trim`. This is an artistic call, recorded here so it can be
  revisited.
