# 543 Presidio Blvd — SF-SIM asset plan

A World War I–era officers' family residence on the west side of Presidio Boulevard,
where the boulevard drops away from Lombard Gate into the park. Two storeys of pale
stucco over a raised basement, under a low red clay-tile hipped roof with deep eaves —
one of a row of near-identical Mission Revival houses (540 · 541 · 542 · 543 · 544 ·
545 · 546 · 547 · 548 · 549) that step down the hillside together.

It is the second **Presidio** plan in this set (after `1008-general-kennedy`) and the
first for a *single detached house*. The design brief is therefore "the most legible
house in a row of near-identical houses", not "monument" and not "background block":
the recognition rests entirely on the silhouette of a compact near-square block under a
near-pyramidal tile hip, and on the way that hip reads as one clean red shape from the
app's aerial camera.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/543-presidio-blvd/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `543-presidio-blvd` |
| Existing procedural builder | none — new landmark, **Case B** (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4515779, 37.7973711` (footprint OBB centre, measured) |
| Target height | **9.55 m** to the chimney crest; roof ridge 9.15 m; eave 7.0 m (see 2.1 — OSM's `height=8` is the LiDAR *median*, not the crest) |
| Footprint | 13.72 m (front, along bearing 10.7°) × 12.79 m (depth), 165.8 m²; a 2.70 × 3.45 m notch cut from the rear NNE corner — measured |
| Triangle cap | 9,000 |
| Category | `1` (House) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 543 Presidio Blvd GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the house at 543 Presidio Boulevard, in the
Presidio of San Francisco, and deliver it as a downloadable, validated GLB.

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
7. `artifacts/1008-general-kennedy/` — the nearest reference implementation: the other
   Presidio building in this set, same stucco-and-tile-hip vocabulary, same
   "one of a near-identical row" design problem
8. `artifacts/salesforce-tower/` — the canonical reference implementation of this
   deliverable (dossier, deterministic build script, validator, renders, report)
9. `docs/asset-plans/543-presidio-blvd.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A compact, almost square two-storey block of pale stucco, standing on a raised
  basement above a terraced lawn
- A low **red clay-tile hipped roof** with only a very short ridge — nearly pyramidal
  over this near-square plan — and deep overhanging eaves that throw a hard shadow line
- Deep eave fascia: at this scale the eave shadow is what makes the roof read as tile
- A symmetrical street elevation facing east-southeast onto Presidio Boulevard, with a
  projecting one-storey entry porch under its own small hip
- Regular double-hung windows in two tiers, quiet and evenly spaced
- One masonry chimney, which is the only vertical incident and sets the 9.55 m crest
- The rear corner notch: the back of the house is 11.0 m wide, not the full 13.7 m

## Research 543 Presidio Blvd independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- All four elevations, and aerial / roof views
- Day and night appearance
- The Presidio's WWI-era officers' family housing type generally (Presidio Boulevard,
  Liggett Avenue and Simonds Loop neighbourhoods), since published material on this
  individual house is thin
- Whether this house is a single-family residence or a duplex — the DataSF footprint is
  165 m² where its immediate neighbours at 541 and 545 are ~248 m², which is evidence
  it is the smaller single-family type
- Whether the roof carries dormers (the aerial suggests it does not)
- The detached garage: it is a **separate** OSM/DataSF footprint and is out of scope

Prefer Presidio Trust and National Park Service material, National Historic Landmark
District documentation, planning and permitting documents, geolocated photography, and
aerial/satellite imagery. Never rely on a single photograph, a single AI-generated
image, or a single unsourced 3D model. Separate verified facts from visual inference;
if sources disagree, document the disagreement and decide.

**Do not use the OSM `height=8` tag as the target height.** It reproduces the DataSF
LiDAR *median* height over the footprint (8.21 m), which for a hipped roof falls
between the eave and the ridge. The LiDAR *maximum* — 9.55 m — is the crest.

## Create a reference dossier

Write `artifacts/543-presidio-blvd/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3–5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. A contact sheet of
attributed reference thumbnails is welcome if legally permissible — do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

This is a **secondary building** in the style bible's §21 detail budget, not a hero:
clear massing, facade rhythm, a designed roof, one or two identity cues. Resist the
temptation to add hero detail — the house's charm is its quietness, and the roof is
90% of the read. The finished asset must be immediately recognizable as one of the
Presidio's officers' houses, consistent with the real building from all four sides and
above, architecturally credible, and a premium handcrafted miniature.

## Scope of the exported asset

Export the house only: raised basement, two storeys, entry porch, hipped tile roof,
eaves and chimney.

Do not include unrelated surrounding city geometry: the detached garage, the terraced
lawn, the retaining wall and its stair, Presidio Boulevard, the neighbouring houses at
541 and 545, trees, people, vehicles, plinths, cameras or lights. A shallow base band
that hides the terrain seam is part of the building (it is the raised basement) and is
allowed; a display plinth is not. Temporary context may appear in review renders but
must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ≈ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 9,000 triangles.

**Normalize the bounding-box top to 9.55 m exactly**, so the loader's
`targetHeightM / measuredHeight` scale lands at 1.0.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The street front
faces **east-southeast, bearing 100.7° true**, onto Presidio Boulevard; the long axis
of the front wall runs at bearing 10.7°. This is a deliberate deviation from the
contract's "front faces −Y" rule, which real-world orientation overrides
(`docs/asset-plans/README.md`, AGENTS rule 5). Record the decision and the measured
heading in `REPORT.md`.

## Night state (required)

Design a `_Glow` set for the app's dusk pass. This is a house, so the night state is
domestic and sparse: a handful of warm-lit windows spread across at least two
elevations (the camera orbits the city — a night state confined to one facade is
invisible from half the orbit), plus a lit porch soffit at the entry. Glow surfaces
must be thin shells proud of the opaque glazing, never the primary surface: the app
renders `_Glow` in a separate layer that is ~12% alpha by day. Day colors of glow
materials must match their non-glow palette neighbours.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless only: `blender -b --python script.py -- args`; no GPU, so
use Workbench or CPU Cycles.

Keep `artifacts/543-presidio-blvd/build_543_presidio_blvd.py` (deterministic build
script), `artifacts/543-presidio-blvd/543-presidio-blvd.blend`, and
`artifacts/543-presidio-blvd/543-presidio-blvd.glb`. The script must rebuild the model
reliably enough for future revision. Do not modify or rename an unrelated existing GLB
to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`543-presidio-blvd-top.png`, `543-presidio-blvd-north.png`, `543-presidio-blvd-east.png`,
`543-presidio-blvd-south.png`, `543-presidio-blvd-west.png`, plus
`543-presidio-blvd-contact-sheet.png`, a high three-quarter aerial beauty render
`543-presidio-blvd-aerial.png`, and its night counterpart
`543-presidio-blvd-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions as true compass directions
(north = Blender `+Y`), which is how the asset is authored. The top view must clearly
show the hip's four planes, the short ridge, the eave overhang and the chimney. The
aerial view uses the style bible's camera assumptions (30–50° down, long lens). Simple
tabletop lighting, neutral warm background, minimal depth of field, and every image
must depict the same exported model.

## Validate the exported GLB

Re-import `543-presidio-blvd.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Include the normals test: per-object signed volume
is authoritative for a union of solids; the ray test must show ≤ 0.15% residual (zero
for single shells). Render at least one review image from the re-imported asset. Write
`artifacts/543-presidio-blvd/validation.json` and `artifacts/543-presidio-blvd/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "543-presidio-blvd",
  "file": "543-presidio-blvd.glb",
  "anchor": [
    -122.4515779,
    37.7973711
  ],
  "targetHeightM": 9.55,
  "cat": 1,
  "name": "543 Presidio Blvd",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`,
or any app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes
in `docs/asset-plans/543-presidio-blvd.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent must
re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 543 Presidio Boulevard, San Francisco, CA 94129 | Nominatim (single unambiguous result), OSM `addr:*` tags |
| OSM way | `way/288361199` | Overpass, geometry pulled 12 Aug 2026 |
| DataSF LiDAR building | `201006.0038392` | DataSF `ynuv-fyni`; centroid 0.8 m from the OSM centroid, area 165.0 m² vs OSM 165.8 m² — the same building |
| Footprint | 13.72 m × 12.79 m OBB; 165.8 m² actual; rear NNE corner notched 2.70 × 3.45 m | **measured** from OSM geometry, reprojected with the repo's tangent projection, reduced to a minimum-area oriented bounding box |
| Anchor (OBB centre) | `-122.4515779, 37.7973711` | **measured** |
| Front-wall bearing | 10.7° true; the street elevation faces 100.7° true (ESE) | **measured** from the OSM polygon edges; the nearest Presidio Boulevard centreline node lies 32.6 m away in the +v (100.7°) direction |
| Ground elevation | 34.51 m NAVD88 min, 34.83 m median | DataSF `gnd_mincm` / `gnd_mediancm` |
| **Crest height** | **9.55 m** above grade | DataSF `hgt_maxcm` = 955 (2010 LiDAR, 50 cm cells) |
| Median roof height | 8.21 m | DataSF `hgt_median_m` — this is what OSM's `height=8` tag reproduces |
| Roof shape / colour | hipped, red | OSM `roof:shape=hipped`, `roof:colour=red` |
| Era and use | built for officers' families during World War I; four-bedroom duplexes and single-family houses | Presidio Trust residential leasing material (Presidio Boulevard neighbourhood) |
| Style | Mission Revival | Presidio Trust neighbourhood description; consistent with the Presidio's NHL District stucco-and-tile vocabulary |
| Type | single-family, *inferred* | 165 m² footprint against ~248 m² at 541 and 545 (DataSF `201006.0016579` and `201006.0016699`) — this is the smaller of the two types on the street |

### 2.2 Sources

- https://www.openstreetmap.org/way/288361199 — footprint geometry, address, `height=8`, `roof:shape=hipped`, `roof:colour=red`
- https://data.sfgov.org/resource/ynuv-fyni — DataSF LiDAR building footprints; building `201006.0038392` supplies every height figure used here
- https://www.rentcafe.com/apartments/ca/san-francisco/presidio-boulevard-neighborhood/default.aspx — Presidio Trust leasing description of the Presidio Boulevard neighbourhood: Mission Revival, built for officers' families during World War I, four-bedroom duplex or single-family, basement, detached garage
- https://www.presidio-residences.com/apartments/ca/san-francisco/simonds-loop-neighborhood/index — the adjacent Simonds Loop neighbourhood: Mission-style duplexes and single-family houses built as officer housing before WWII, attached garages, basements
- https://www.nps.gov/articles/presidio-architecture.htm — the Presidio's architectural inventory: 473 historic contributing buildings in the National Historic Landmark District
- https://noehill.com/sf/landmarks/nat1966000232.aspx — National Register listing #66000232 for the Presidio, with the officers'-family-housing inventory
- Google Maps aerial and street-level imagery at 37.79737, −122.45158 — used for visual observation only (roof form, eave depth, porch, window rhythm, terracing); no imagery is reproduced or committed

### 2.3 Height derivation (the number that matters most)

There is no published architectural height for an individual Presidio residence, so the
crest is taken from the 2010 LiDAR and the storey breakdown is inferred to fit it:

| Level | Height | Basis |
|---|---|---|
| Exposed raised basement | 0.90 m | *inferred* — the house stands above a terraced lawn; the plinth also hides the terrain seam |
| Ground floor | 3.10 m → 4.00 m | *inferred* |
| Second floor | 3.00 m → 7.00 m (eave line) | *inferred* |
| Hip roof, 4:12 over the 12.79 m cross span | +2.15 m → **9.15 m ridge** | *inferred* |
| Chimney | → **9.55 m crest** | **measured** (`hgt_maxcm` = 955) |

This set is self-checking. A hipped roof whose surface runs from 7.00 m to 9.15 m has a
median surface height of roughly 8.1–8.2 m over the footprint — and DataSF's measured
`hgt_median_m` for this building is **8.21 m**. The eave/ridge split is inferred, but it
is the split that reproduces the one independent measurement available. Record it as
*inferred* anyway; only 9.55 m and 8.21 m are measured.

### 2.4 What each side shows

Local frame used throughout: **u** along bearing 10.7° (the front wall's long axis,
positive toward the NNE), **v** along bearing 100.7° (positive toward Presidio
Boulevard). Origin at the OBB centre. Footprint in this frame:

```
 (+6.86, +6.40) ---------------- (-6.83, +6.39)      <- street front (ESE), 13.72 m
       |                               |
 (+6.84, -2.94)                        |
       |___(+4.17, -2.94)              |
              |                        |
       (+4.16, -6.39) ---------- (-6.86, -6.39)      <- rear (WNW), 11.02 m
```

**East-southeast (Presidio Boulevard front, bearing 100.7°)** — The hero elevation:
13.72 m of symmetrical pale stucco in two tiers of double-hung windows, a projecting
one-storey entry porch on the centre line under its own small hip, and the deep eave
shadow above. The whole thing stands on the exposed raised basement, above a terraced
lawn reached by a concrete stair (out of scope).

**North-northeast flank (bearing 10.7°)** — 12.79 m deep at the front, stepping back
2.70 m at the rear where the corner is notched. Quieter: two tiers of windows, no
entrance. The chimney rises on this flank.

**West-northwest (rear, bearing 280.7°)** — 11.02 m wide, plainer, service side.

**South-southwest flank (bearing 190.7°)** — Full 12.79 m depth, faces the neighbouring
house at 541; two tiers of windows.

**Top** — This is the surface that matters. A near-pyramidal red tile hip: over an
11.02 × 12.79 m main block the ridge is only ~0.9 m long, so the roof reads as four
large triangles meeting almost at a point, with a subordinate lower hip over the
2.70 × 9.34 m front wing. Deep overhang all round. One chimney. No dormers observed.

### 2.5 Recognition cues (ranked)

1. **The near-pyramidal red tile hip** — from the app's camera this is the building
2. A compact, almost square pale block, standing slightly proud of its lawn
3. Deep eaves throwing a hard shadow line all the way round
4. The projecting entry porch on the street front
5. The single chimney breaking the roof plane

### 2.6 Miniature translation

**Preserve**

- The near-square plan and its 13.72 × 12.79 m proportion — do not stretch it
- The rear corner notch: it is 6% of the footprint and it is what distinguishes this
  house from its neighbours in plan
- The hip's four-plane geometry as real geometry, not a bevelled plane
- The eave overhang, exaggerated if anything — it is the tile-roof cue at 20 px
- Restraint. This is a quiet house; §21's "secondary building" budget applies

**Simplify / exaggerate**

- Individual tiles → one flat `Toy_red` surface; the shape carries the read
- ~20 double-hung windows → 12 identical recessed openings on a regular grid
- Porch columns and rails → two chunky posts and a flat canopy
- Terracing, retaining wall, garage, planting → omitted entirely (out of scope)
- Eave overhang enlarged to 0.55 m with a 0.35 m fascia so the shadow reads

### 2.7 Massing recipe

Build order for the deterministic script. All coordinates in the (u, v) frame of 2.4,
relative to the OBB centre; z from grade.

1. **Basement band** — full footprint (main block + front wing), z 0 → 0.90,
   `Toy_stone`, inset 0 (it is the widest element at ground level).
2. **Main block** — u −6.86…+4.16, v −6.39…+6.40, z 0.90 → 7.00, `Toy_white`.
3. **Front wing** — u +4.16…+6.86, v −2.94…+6.40, z 0.90 → 7.00, `Toy_white`.
   (2 and 3 together are the notched footprint; keeping them separate keeps each a
   closed solid for the signed-volume normals test.)
4. **Eave fascia** — closed band around the whole envelope grown 0.55 m outward,
   z 6.65 → 7.00, `Toy_trim`.
5. **Main hip** — over u −6.86…+4.16, v −6.39…+6.40 grown by the 0.55 m overhang,
   eave 7.00 → ridge 9.15, ridge along **v**, `Toy_red`.
6. **Wing hip** — over the front wing's overhung rectangle, eave 7.00 → ridge 8.35,
   ridge along **v**, `Toy_red`. Lower than the main hip so the wing reads subordinate.
7. **Chimney** — 0.85 × 0.70 m section on the NNE flank at u ≈ +2.6, v ≈ −1.5, rising
   from z 7.6 to **9.55** (the bbox top), `Toy_brick` — deliberately not `Toy_red`, so
   the stack reads as a separate object from above.
8. **Entry porch** — projecting 1.9 m from the front wall on the centre line, 4.2 m
   wide; slab z 0.90, two `Toy_trim` posts, flat canopy z 3.30 → 3.65, its own small
   hip above to 4.30, `Toy_red`. Door recess in `Toy_ink`.
9. **Windows** — 12 recessed `Toy_glass` openings, 1.10 × 1.65 m, sills at z 2.10 and
   z 4.90, with 0.10 m `Toy_trim` sills. Front: 3 per tier flanking the porch. Each
   flank: 2 per tier. Rear: 1 per tier.
10. **Glow set** — thin `Toy_glass_Glow` shells over 4 of the 12 windows, spread across
    the front and the SSW flank, plus a `Toy_trim_Glow` porch soffit.
11. **Bevel** — 0.12 m / 2 segments on the massing volumes; 0.05 m / 1 on sills, posts
    and thin bands; none on window fills and glow shells.
12. **Recentre** — shift so the XY bbox centre is the origin, and carry the same shift
    into the manifest anchor (the eave overhang is symmetric, so this should be small;
    the notch makes it non-zero).

### 2.8 Materials and palette

| Material | Hex | Used for |
|---|---|---|
| `Toy_white` | `f7f4ec` | stucco walls |
| `Toy_stone` | `d9d2c2` | exposed raised basement |
| `Toy_red` | `c4453c` | clay-tile hips (main, wing, porch) |
| `Toy_trim` | `f3efe6` | eave fascia, window sills, porch posts and canopy |
| `Toy_glass` | `2a4d73` | window fills |
| `Toy_brick` | `c96f4a` | chimney |
| `Toy_ink` | `3a3530` | door recess |
| `Toy_glass_Glow` | `6f95b8` | lit windows (night) |
| `Toy_trim_Glow` | `f3efe6` | porch soffit (night) |

All nine are project-palette colours. No off-palette warnings expected.

### 2.9 Top surface

The roof is the asset. Four large hip planes meeting at a ~0.9 m ridge, a subordinate
lower hip over the front wing, a continuous eave shadow, one brick chimney. Nothing
else — no vents, no solar, no roof clutter. §10's "never leave prominent roofs blank"
is satisfied by the hip geometry itself, which is a designed surface, not a blank slab.

### 2.10 Scope

In: raised basement, two storeys, entry porch, hipped tile roofs, eaves, chimney,
windows, glow set.

Out: the detached garage (a separate DataSF footprint), the terraced lawn, the
retaining wall and stair, Presidio Boulevard, the neighbouring houses, all planting,
vehicles, people, display plinths, cameras and lights.

### 2.11 Triangle budget

| Group | Estimate |
|---|---|
| Basement, two wall volumes, eave band | ~900 |
| Two hips + porch hip | ~450 |
| Chimney, porch posts, canopy, door | ~600 |
| 12 windows (fill + sill) | ~1,700 |
| 4 glow shells + porch soffit | ~300 |
| Bevel overhead (0.12/2 on the massing) | ~2,500 |
| **Total** | **~6,500** |

Cap 9,000 — well under the contract's 27,000 and the PERF-PLAN hard limit of 30,000.
This is a small house; a number near 6k is the right answer and a number near 20k means
something was over-detailed.

### 2.12 Draft manifest entry

```json
{
  "id": "543-presidio-blvd",
  "file": "543-presidio-blvd.glb",
  "anchor": [-122.4515779, 37.7973711],
  "targetHeightM": 9.55,
  "cat": 1,
  "name": "543 Presidio Blvd",
  "estimated": true,
  "dims": [x, y, z],
  "tris": N,
  "loadRadius": 2500
}
```

`estimated: true` because the eave/ridge split is inferred; the anchor and the 9.55 m
crest are measured. `loadRadius` uses the default rule `max(2500, 9.55 × 30)` = 2500.
`alwaysLoaded` is emphatically not appropriate — this is a 9.5 m house.

### 2.13 Integration notes (Case B)

No `543-presidio-blvd` id exists in `pipeline/lib/landmarks.mjs` or `app/src/landmarks.js`,
so integration is **Case B**:

1. Add a registry entry to `pipeline/lib/landmarks.mjs` — id `543-presidio-blvd`,
   `lon -122.4515779`, `lat 37.7973711`, height 9.55, exclusion radius ~11 m (large
   enough to clear the baked procedural building on this footprint, small enough not to
   punch a hole in the neighbouring houses at 541 and 545, whose footprints start
   ~7 m away — this is the tightest exclusion radius in the set and must be checked
   against the re-baked tile visually).
2. Re-bake the affected tiles, or the baked procedural building will intersect the GLB.
3. Run audit 1.6.
4. The far stand-in beyond `loadRadius` is the baked procedural house, which is present
   and appropriate here — unlike a carved-out hero site, nothing goes missing at range.

### 2.14 Validation checklist

- [ ] Binary GLB, real metres, applied transforms, no negative scales
- [ ] min Z ≈ 0, XY bbox centre ≈ (0, 0)
- [ ] **bbox top = 9.55 m exactly** (loader scale must land at 1.0)
- [ ] ≤ 9,000 triangles
- [ ] Materials all `Toy_*` from the table in 2.8; no textures, no transparency
- [ ] `_Glow` present, and only on thin shells proud of opaque surfaces
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Normals: per-object signed volume positive for every closed solid; ray test
      ≤ 0.15% residual
- [ ] Fresh-scene re-import validated, not the source `.blend`
- [ ] Renders: top, N, E, S, W, contact sheet, aerial day, aerial night
- [ ] Front elevation reads at thumbnail size from the aerial camera

### 2.15 Open questions and risks

- **The eave/ridge split is inferred.** Only the 9.55 m crest and the 8.21 m median are
  measured. The split chosen reproduces the measured median, which is the strongest
  available check, but it is not a published figure. Labelled *inferred* throughout.
- **Single-family vs duplex is inferred** from the 165 m² footprint against ~248 m² at
  541 and 545. It changes the window count slightly and nothing else; the model does not
  depend on it.
- **Whether `hgt_maxcm` = 955 is the chimney or the ridge.** The plan assumes chimney,
  putting the ridge at 9.15 m. If the 9.55 m is actually the ridge, the roof is one
  storey-fraction steeper and the chimney rises above it — but the *bbox top* is 9.55 m
  either way, so `targetHeightM` is unaffected. This is a shape question, not a scale one.
- **Dormers.** None observed in the aerial. If ground-level research finds them, they
  belong on the street elevation only.
- **The exclusion radius is unusually tight** (§2.13). This is the first plan in the set
  where neighbouring buildings sit within ~7 m of the subject, and a careless radius will
  delete 541 and 545 from the baked city. Verify visually after the re-bake.
- **2010 LiDAR is 16 years old.** For a house in a National Historic Landmark District
  under Presidio Trust stewardship, the massing is very unlikely to have changed, but the
  data is not current.
