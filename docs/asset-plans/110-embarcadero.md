# 110 The Embarcadero (The Commonwealth Club of California) — SF-SIM asset plan

A 1910 waterfront warehouse that became the permanent home of the nation's oldest
public-affairs forum. Leddy Maytum Stacy gutted it in 2015–17, kept the rendered
two-storey **Steuart Street** front, and hung a **three-storey glass curtain wall**
on the **Embarcadero** end — so the building is two completely different buildings
depending on which street you stand in. Between them, on top, is a planted roof
terrace that the app's downward camera sees more of than either facade.

It is a through-lot: 41.9 m deep, only 13.9 m wide, with party walls on both long
sides (the Audiffred Building to the north-west, a seven-storey brick office to the
south-east). Both short ends are hero elevations; neither long side is ever seen.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/110-embarcadero/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `110-embarcadero` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3926624, 37.7932325` (footprint vertex mean = AABB centre; the polygon is a true parallelogram, measured) |
| Target height | **17.4 m** (roof fascia over the Embarcadero curtain wall; the Steuart end steps down to 11.6 m — see 2.1 and 2.15) |
| OSM footprint | 41.87 x 13.91 m parallelogram on the 44.8 deg waterfront grid, 582.1 m2 (OSM way/256969674, measured; DataSF parcel 3715002 agrees to ~1 m) |
| Triangle cap | 13,000 |
| Category | `17` (theater_cinema — an auditorium venue; night profile 1, evening-lit) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 110 The Embarcadero GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 110 The Embarcadero — the Commonwealth
Club of California headquarters — in San Francisco and deliver it as a
downloadable, validated GLB.

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
8. `artifacts/500-third/` and `artifacts/2-south-park/` — two nearby brick-and-
   glass neighbours already built; this asset must look like it came out of the
   same toy box and must not out-detail them
9. `docs/asset-plans/110-embarcadero.md` — this plan, whose dossier is your
   research starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The **long thin through-lot block**: 41.9 m deep by 13.9 m wide, running from
  The Embarcadero (north-east) back to Steuart Street (south-west), with blind
  party walls on both long sides. The narrowness is the building's condition —
  the press called it "a narrow 45-foot-wide building" and that is exactly the
  measured 13.91 m
- **Two utterly different short ends.** The whole design idea is that the
  building is historic on one street and modern on the other. Do not blend them
- **The Embarcadero end (north-east, the address face):** a three-storey glass
  curtain wall filling the full 13.9 m width, slender white mullions in about
  five structural bays each subdivided into three panes, pale horizontal spandrel
  bands at the floor lines, and a projecting flat roof fascia / brise-soleil
  eyebrow across the top. At ground level a recessed dark glazed lobby with the
  entrance toward the north-west (Audiffred) half, a thin flat canopy, a white
  signage band reading **COMMONWEALTH CLUB**, and the numerals **110**
- **The Steuart Street end (south-west, the historic face):** a two-storey pale
  grey rendered 1910 front with a strong bracketed cornice that steps up into a
  wide, shallow **triangular pediment**; four tall white-framed upper windows in
  a 2 + blank centre + 2 rhythm inside recessed moulded panels; a continuous sill
  band; and a ground-floor run of large storefront windows with a doorway at the
  south-east end
- **The step in the massing.** The Embarcadero end stands full height (17.4 m);
  the Steuart end stops at the historic parapet (11.6 m, pediment apex 12.3 m)
  with the new glazed third floor **set back behind it**, topping out around
  14.0 m, plus a solid pale-grey clad stair/lift over-run box at ~14.8 m on the
  south-east side. This step is what a preservation-led vertical addition looks
  like and it is visible from every aerial angle
- **The roof as a designed terrace**, because the app's camera looks down on it:
  a planted roof garden across the middle of the roof, an open paved deck at the
  Embarcadero end, a low penthouse/plant volume near the centre, a square
  skylight or roof feature near the north-east end, and a parapet all round
- Both long sides as **plain blind party walls** — no windows, no articulation
  beyond a flat rendered surface. They are invisible in the city and must not be
  decorated

## Research 110 The Embarcadero independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North-east (The Embarcadero) and south-west (Steuart Street) elevations
- Aerial and roof views — the roof carries most of what the app's camera sees
- Ground-level views of the entrance, canopy and signage
- Day and night appearance
- Publicly available drawings, plans or diagrams (Leddy Maytum Stacy, Tipping
  Structural Engineers and Salter all publish project pages)
- **The height, which this dossier derives from Street View photogrammetry, not
  from a published figure.** The 2010 DataSF LiDAR for this footprint measures
  the *pre-renovation two-storey* building (median 10.33 m) and must never be
  used as the target height. See 2.15 for the full argument and the two
  independent checks. A measured elevation, a planning drawing or a dated
  photograph against a known neighbour beats what is written here
- **How far the third floor is set back at the Steuart end,** and whether the
  stair over-run box sits on the south-east or north-west side. This dossier
  reads both from one Street View frame

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/110-embarcadero/REFERENCE.md` containing: source links and what
each establishes; verified dimensions and location; orientation; observations
from all four sides and above; the 3-5 strongest recognition cues; features to
preserve; features to simplify; uncertainties and conflicting evidence. A contact
sheet of attributed reference thumbnails is welcome if legally permissible — do
not commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

This building's job is to be a **hinge**: old city on one street, new city on the
other, in one 42-metre-long object. §5 (facade rhythm over mullion count) governs
the curtain wall, §10 (roofs as secondary facades) governs the terrace, and §8
(semantic exaggeration) applies to exactly two things — the pediment on Steuart
and the roof fascia on the Embarcadero. §11 (landmark silhouette geometry) does
not apply: there is no crown and no tower here. Resist inventing one.

The finished asset must be immediately recognizable as 110 The Embarcadero,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel
art, not generic low-poly, and never accurate in one view while invented in the
others.

## Scope of the exported asset

Export the 110 The Embarcadero building itself, including its parapets, roof
terrace decking and planters, penthouse and stair over-run, the Embarcadero
curtain wall with its entrance canopy and signage, and the Steuart Street
historic front with its pediment and cornice.

Do not include unrelated surrounding city geometry: The Embarcadero, Steuart
Street, the Audiffred Building, the seven-storey office to the south-east, the
F-line tracks, street furniture, street trees, people, vehicles, plinths,
cameras or lights. Temporary context may appear in review renders but must not
leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 13,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The long axis
runs 135.2 / 315.2 deg true; the Embarcadero front faces north-east (outward
normal 44.8 deg true), so the contract's "front faces −Y" cannot be honoured
literally. Real-world orientation wins (AGENTS rule 5). Record the decision and
the measured heading in `REPORT.md`.

**Height normalization:** make the exported bounding-box top land exactly on the
verified architectural height, so the loader's `targetHeightM / measuredHeight`
scale is 1.0. The bbox top is the Embarcadero roof fascia, **not** the Steuart
parapet and **not** the stair over-run.

## Reproducible Blender workflow

Blender 4.5 LTS or newer, headless only: `blender -b --python script.py -- args`;
no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/110-embarcadero/build_110_embarcadero.py` (deterministic build
script), `artifacts/110-embarcadero/110-embarcadero.blend`, and
`artifacts/110-embarcadero/110-embarcadero.glb`. The script must rebuild the model
reliably enough for future revision. Do not modify or rename an unrelated existing
GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`110-embarcadero-top.png`, `110-embarcadero-north.png`, `110-embarcadero-east.png`,
`110-embarcadero-south.png`, `110-embarcadero-west.png`, plus
`110-embarcadero-contact-sheet.png`, at least one high three-quarter aerial beauty
render `110-embarcadero-aerial.png`, and a night render
`110-embarcadero-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection;
use orthographic or long-lens cameras; label directions from the researched
orientation; the aerial view uses the style bible's camera assumptions (30-50
degrees down, long lens) and must be taken from the **north-east**, looking down
the long axis over the glass front and across the roof terrace to the Steuart
pediment beyond — that view is the hero view for this asset, because it is the
only one that shows both faces and the step between them at once. Simple tabletop
lighting, neutral warm background, minimal depth of field, and every image must
depict the same exported model.

## Validate the exported GLB

Re-import `110-embarcadero.glb` into a fresh isolated Blender scene and validate
the re-import, not the source scene. Report object count, triangle count,
dimensions, bounding-box min/max, min Z, XY center offset, material names,
image-texture count, camera count, light count, animation count, applied-transform
status, negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Normals are checked two ways: per-object signed
volume (authoritative for a union of closed solids) and a deterministic
visibility-ray test (≤ 0.15% residual, zero for single shells). Render at least
one review image from the re-imported asset. Write
`artifacts/110-embarcadero/validation.json` and
`artifacts/110-embarcadero/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "110-embarcadero",
  "file": "110-embarcadero.glb",
  "anchor": [
    -122.3926624,
    37.7932325
  ],
  "targetHeightM": 17.4,
  "cat": 17,
  "name": "The Commonwealth Club (110 The Embarcadero)",
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
`docs/asset-plans/110-embarcadero.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent
must re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 110 The Embarcadero / 115 Steuart Street, San Francisco, CA 94105 | Club press release (both addresses given); DataSF parcel carries the Steuart address |
| Occupant | The Commonwealth Club of California — the nation's oldest and largest public-affairs forum, founded 1903 | Club, LMS, Salter |
| Parcel | Block 3715, lot 002 (`mapblklot 3715002`), zoning C-3-O "Downtown — Office", Financial District/South Beach | DataSF parcels `acdm-wktn` (measured) |
| Original building | 1910, two storeys; International Longshoremen's Association union hall; site of the 1934 Bloody Thursday shootings during the Pacific Coast dock strike; owned by the Accornero family for 70+ years until the Club bought it in 2012 | LMS, Club "Our Building Story", Club press release |
| Renovation | Groundbreaking 11 June 2014; construction 2015–2017; opened 12 September 2017 | Club press releases (both events) |
| Architect | Leddy Maytum Stacy Architects; lead Marsha Maytum (1954–2024). AIA National Firm Award 2017 | LMS project page, Club press release |
| Consultants | Tipping Structural Engineers (structure/seismic); Salter (acoustics, AV, telecom, security); Gensler (space planning) | respective project pages |
| Storeys | **3 above grade** plus basement and roof deck — the permit for the works reads "add 1 story", existing 2 → proposed 3 | DBI PA 201312174360 (measured); later 2017 permits all list "3 existing stories". *OSM tags `building:levels=3`… see 2.15 for the OSM level discrepancy* |
| Area | 22,600 sq ft (LMS) / "24,000 square feet of interior space" (the Club) | LMS, Club |
| Program | 299-seat auditorium, 135-person multipurpose room, library lounge, boardroom, three catering kitchens, roof garden and a publicly accessible roof terrace | Tipping, Club, Hoodline |
| Sustainability | LEED Gold; designed for a 70 % energy-use reduction | LMS |
| Construction move | Historic Steuart Street façade retained and shored (permit: "temporary shoring of 2 story facade and 2 walls"); a **light-weight glass third floor** added so the original wooden piles in Bay mud could be reused | DBI PA 201601288257; Tipping; Club press release |
| Footprint | 41.87 x 13.91 m parallelogram, 582.1 m2 | OSM way/256969674 reprojected with the app's tangent projection (measured) |
| Footprint cross-check | DataSF parcel 3715002 polygon agrees with the OSM ring to ≤ 1.0 m at every vertex | DataSF `acdm-wktn` (measured) |
| Width cross-check | 13.91 m = 45.6 ft, against the press release's "narrow 45-foot-wide building" | Club press release + measurement |
| Anchor | -122.3926624, 37.7932325 | footprint vertex mean; a true parallelogram, so this equals the AABB centre exactly (measured) |
| Long-axis heading | 135.2 / 315.2 deg true; frontage normals 44.83 deg (Embarcadero) and 224.94 deg (Steuart) | OSM geometry (measured) |
| **Height (Embarcadero end)** | **17.4 m** to the top of the roof fascia; curtain-wall head 16.9 m | Street View photogrammetry, rectified elevation at 60 px/m, D = 16.73 m (measured — see 2.15) |
| Height (Steuart end) | historic cornice 11.5 m, pediment apex 12.3 m, set-back glass volume ~14.0 m, stair over-run box ~14.8 m | same method from the Steuart pano, D = 15.73 m (measured, ±0.4 m) |
| Storey datums | ground 0 → 4.2 m; level 2 4.2 → 11.7 m (double-height auditorium volume); level 3 11.7 → 16.9 m | spandrel-band positions read off the rectified Embarcadero elevation (measured) |
| Pre-renovation height | 10.33 m median over this footprint | SF **2010** LiDAR `SF3715002`, `hgt_median_m` — this is the *old two-storey building* and is not the target height (see 2.15) |
| Ground | 3.43 m NAVD88 mean over the footprint (`gnd_min` 3.33 m) | same LiDAR record — flat made ground on the old waterfront |
| Lot condition | Through-lot. Party walls on **both** long sides: Audiffred Building (`SF3715001`, 4 storeys + mansard, LiDAR max 19.18 m) to the NW; an unnamed 7-storey brick office (OSM way/193054135, `SF3715003`, LiDAR median 26.82 m) to the SE. Both share footprint vertices with this building | OSM + DataSF (measured) |
| Nearest landmark already in the scene | `ferry-building`, 261 m north | repo manifest + measured bearing |

### 2.2 Sources

- https://www.openstreetmap.org/way/256969674 — footprint geometry (`building=commercial`, `roof:shape=flat`). The Club is tagged separately as amenity node 9659886917, which falls inside this ring — that is how the address resolves to this polygon and not to one of the three other "110 The Embarcadero" address objects Nominatim returns
- https://data.sfgov.org/resource/acdm-wktn.json — DataSF parcels: `mapblklot 3715002`, address 115 STEUART ST, C-3-O. The parcel polygon matches the OSM building ring to within 1 m, i.e. the building is built lot-line to lot-line
- https://data.sfgov.org/resource/i98e-djp9.json — DBI permits at 110 The Embarcadero. The load-bearing ones: **PA 201312174360** (2013-12-17, "structural upgrade of (e) foundation … add 1 story to accomodate assembly", existing 2 → proposed 3); **201601288257** (2016, "temporary shoring of 2 story facade and 2 walls"); **201705197169** (2017, "provide card readers to roof deck"); **201708074118** (2017, assembly occupant-load permit). Every 2017 record lists 3 existing storeys
- https://data.sfgov.org/resource/ynuv-fyni.json — SF 2010 LiDAR building footprints, record `SF3715002`: 2,499 half-metre cells (625 m2), ground mean 3.43 m NAVD88, height median 10.33 m, height mean 11.45 m, **height max 24.43 m with σ = 3.38 m**. The maximum is rejected — see 2.15
- https://lmsarch.com/projects/commonwealth-club-california/ — architect's project page: 22,600 sq ft, LEED Gold, "the existing two story structure, built in 1910, was renovated and a new floor added", "the historic Steuart Street façade was restored", California Heritage Council Award, photography by Bruce Damonte
- https://tippingstructural.com/projects/commonwealth-club/ — structural engineer: 299-seat auditorium, 135-person multipurpose room, library lounge, roof garden, publicly accessible roof terrace; "a new glass curtain facade alongside the historic facade"; reuse of the existing foundation
- https://www.commonwealthclub.org/visit/building-story and .../press-release/commonwealth-club-new-headquarters — owner: opening date, 24,000 sq ft, the 1910 purchase from the Accornero family, "110 The Embarcadero/115 Steuart Street", Gensler's "narrow 45-foot-wide building", Tipping's pile solution and the "light-weight glass third floor"
- https://www.salter-inc.com/case_stories/case-commonwealth-club-of-california/ — 22,000 sq ft, 300-seat auditorium with a Meyer Sound Constellation system, reclaimed-wood acoustic walls
- https://hoodline.com/2018/04/a-look-inside-the-commonwealth-club-s-new-home-for-ideas/ — "a berth at 110 The Embarcadero, next to the Audiffred Building"; "an expansive roof deck"; three catering kitchens
- Google Street View panoramas `yo5P5pi5QKGaa2I7JTPGvQ` (The Embarcadero, opposite the entrance, 16.73 m out and 0.24 m off the facade centreline) and `cGw3lu-Usr6Mdz7aiLS_2w` (Steuart Street, 15.73 m out) — the primary elevation references and the source of every dimension in 2.4 and of the height in 2.1
- Bing/Vexcel near-nadir aerial at z20 and Google aerial at z22 — roof reading in 2.4 "Top". The Google imagery here is a strong oblique in which a 17 m roof displaces several metres, so only the Bing frame was used for position; treat the pattern as real and the coordinates as free

### 2.3 Orientation and placement

The east side of Steuart Street between Mission and Howard, on the Embarcadero
waterfront. The grid here is rotated ~45 deg from true north: The Embarcadero and
Steuart Street both run 135.2 / 315.2 deg, and this lot runs straight through from
one to the other.

Measured footprint, reprojected with the app's tangent projection and recentred on
the anchor (x east, y north, metres):

```
v0 ( +19.790,  +9.833)   Embarcadero end, SE corner
v1 (  -9.935, -19.648)   Steuart end, SE corner
v2 ( -19.781,  -9.821)   Steuart end, NW corner
v3 (  +9.926, +19.637)   Embarcadero end, NW corner
```

| Edge | Length | Outward normal (true) | What it is |
|---|---|---|---|
| v3 → v0 | 13.908 m | 44.83 deg (NE) | **The Embarcadero front** — the glass curtain wall, the address face |
| v0 → v1 | 41.865 m | 135.24 deg (SE) | party wall to the 7-storey office (OSM way/193054135) — blind |
| v1 → v2 | 13.911 m | 224.94 deg (SW) | **Steuart Street front** — the restored 1910 face |
| v2 → v3 | 41.837 m | 315.24 deg (NW) | party wall to the Audiffred Building — blind |

Author `+Y` = north and place the polygon exactly as measured. The contract's
"front faces −Y" cannot be met — there are two fronts and neither faces −Y — so
real-world orientation wins per the README orientation note and AGENTS rule 5.

The two shared long edges are literal party walls: the Audiffred ring and this
ring share the vertices at v2 and v3, and the south-east neighbour's ring shares
v0 and v1. Nothing on those faces will ever be visible in the city.

### 2.4 What each side shows

**North-east (The Embarcadero) — the address face, 13.9 m wide.** A full-width,
full-height **glass curtain wall** rising three storeys from a recessed ground
floor to a projecting roof fascia. Slender white/light metal mullions divide it
into about **five structural bays of ~2.6 m**, each subdivided into three glazed
panes of ~0.87 m; pale opaque **spandrel bands** cross the whole width at the
floor lines (measured at 3.6–4.8 m and 11.0–12.4 m above the pavement). The glass
reads mid blue-grey with a green cast. At the top, at 16.9 m, the curtain wall
meets a **flat projecting eyebrow / fascia about 0.5 m deep**, whose outer edge is
the building's 17.4 m crest and whose dark soffit is visible from the street.

At ground level the wall steps back into a dark glazed lobby with clear-glass
doors; above the doors a **white fascia band carries COMMONWEALTH CLUB** in
spaced letters, with the numerals **110** on a small plate below it, and a thin
flat canopy over the doorway. The entrance sits toward the **north-west (Audiffred)
half** of the frontage, not on the centreline. Pale plaster returns close the
curtain wall at both jambs. *(All of the above measured directly off a rectified
60 px/m elevation built from Street View pano `yo5P5pi5QKGaa2I7JTPGvQ`.)*

**South-west (Steuart Street) — the historic face, 13.9 m wide.** Two storeys of
pale grey / off-white rendered wall, the restored 1910 front:

- a strong **cornice** across the top, which steps up in the middle into a wide,
  shallow **triangular pediment** — the whole crown is one gesture and it is the
  single strongest cue on this side. Cornice line ~11.5 m, apex ~12.3 m;
- under the cornice, a row of about **six console brackets / modillions** over a
  recessed frieze panel;
- an upper storey of **four tall white-framed windows** in a **2 + blank centre
  bay + 2** rhythm, each window two lights wide, each set inside a recessed
  moulded panel with a broad plain pilaster strip between;
- a continuous **sill band / string course** under those windows at ~5.0 m;
- a ground storey of large **storefront windows** — roughly three wide bays of
  three lights with a transom above — and a recessed **doorway at the south-east
  end**;
- a plain plinth at the base.

Behind and above this front, **set back**, the new third floor appears as a band
of teal glazing with the roof garden's planting visible through it (top ~14.0 m),
and at the south-east side a **solid pale-grey clad box** — the stair / lift
over-run — rising to ~14.8 m. *(Measured off a rectified elevation from Street View
pano `cGw3lu-Usr6Mdz7aiLS_2w`; the setback distance itself is* inferred*.)*

**North-west and south-east (both 41.9 m) — party walls.** Blind rendered walls
against the Audiffred Building and the seven-storey office respectively. Both
neighbours are taller than this building along most of the length, so these faces
are never seen. Model them flat, with nothing on them but the parapet return.
*Observed (both neighbours share footprint vertices with this building).*

**Top — the roof terrace.** The largest surface the app's camera ever sees of this
building, and the one the Club actually markets: "roof garden", "publicly
accessible roof terrace", "an expansive roof deck". Reading the near-nadir Bing
frame along the long axis from Steuart (SW) to Embarcadero (NE):

1. a pale flat roof strip at the extreme **Steuart end**, behind the historic
   parapet and beside the stair over-run box;
2. a **planted band** — dense green, the roof garden — occupying roughly the
   middle third of the roof;
3. a low **penthouse / plant volume** near the centre-south of the roof;
4. an open **paved deck** across the north-east third;
5. a **square roof feature near the Embarcadero end** reading as a skylight or a
   radial paving pattern;
6. a parapet all round, stepping down at the Steuart end.

*(The pattern is observed; the exact positions are* inferred*, and the Google z22
frame that would resolve them is a strong oblique. Do not chase pixel positions.)*

### 2.5 Recognition cues (ranked)

1. **Two-faced.** A three-storey glass box on one street and a rendered 1910
   pedimented front on the other, 42 m apart in the same building. Nothing else on
   this block does that, and from the app's aerial camera both are in frame at
   once.
2. **The pediment on Steuart Street** — a shallow triangle stepping up out of a
   bracketed cornice, on an otherwise flat waterfront street wall.
3. **The glass front with its fascia eyebrow and the COMMONWEALTH CLUB band** —
   the address face, and the one piece of lettering on the building.
4. **The step in the roofline**: full height at the Embarcadero end, dropping to
   the historic parapet at the Steuart end with the new floor set back behind it.
5. **The planted roof terrace** — green on a downtown roof, between two blank
   grey neighbours.

### 2.6 Miniature translation

**Preserve**

- The 41.87 x 13.91 m parallelogram and its 135.2 deg heading — the narrowness
  *is* the building
- Both hero ends, fully designed, completely different from one another
- The step: 17.4 m at the Embarcadero end, 11.6 m parapet at Steuart with a
  set-back volume behind
- The pediment-over-cornice crown on Steuart
- The green roof terrace

**Simplify / exaggerate**

- The curtain wall becomes **five `Toy_glass` bays in `Toy_trim` mullions**, one
  pane per bay per storey (rhythm, not mullion count — §5). Do not model the
  ~0.87 m sub-panes; five bays x three storeys is the reading
- The roof fascia is **thickened to ~0.35 m and projected ~0.6 m** past the glass
  so it survives at city distance (§9) — it is the top edge of the whole asset
- **COMMONWEALTH CLUB** becomes one chunky extruded `Toy_trim` band; do not model
  letterforms. The **110** becomes a small `Toy_ink` plate. At city scale the band
  is the sign
- The Steuart pediment is **exaggerated: raise the apex ~0.3 m above measured**
  and give the cornice a 0.25 m projection, so the crown still reads from 200 m
  (§8). This is the one place on the asset where exaggeration is licensed
- The six modillions become six beveled `Toy_trim` blocks; the frieze becomes one
  recessed panel
- The four upper windows keep their **2 + gap + 2** rhythm exactly — the blank
  centre bay is what makes the face read as 1910 rather than generic
- The ground-floor storefront becomes three `Toy_glass` panels in a `Toy_trim`
  frame plus one `Toy_ink` door recess at the south-east end
- The roof becomes four zones, not a survey: `Toy_stone` deck at the NE third, a
  `Toy_mint` planted band across the middle with three or four `Toy_sand`
  planter kerbs, a `Toy_trim` penthouse box, and a `Toy_glassl` square skylight
  near the NE end
- Party walls are flat `Toy_trim` with a parapet return and nothing else

**Do not add** a tower, a crown, a corner turret, windows on the party walls, or a
curve to the Embarcadero curtain wall. That wall is planar — it only appears bowed
in equirectangular panoramas, and the rectilinear frames confirm the spandrels are
dead straight.

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render. Local axes: **u** along
the long axis (0 at the anchor, +u toward The Embarcadero, ±20.93 m at the ends),
**t** across the width (±6.95 m).

1. **Main body:** extrude the measured footprint from z=0 to **z=16.60**,
   `Toy_trim` (pale rendered wall). This is the volume that stands full height at
   the Embarcadero end.
2. **Steuart step-down:** cut the body back to **z=11.20** for the last 8.0 m at
   the Steuart end (u from −20.93 to −12.9), so the historic front reads two
   storeys with the new floor set back behind it.
3. **Steuart historic front (SW end):**
   - Parapet/cornice: a `Toy_trim` band from z=11.20 to **z=11.60**, projecting
     0.25 m, running the full 13.9 m width, capped with a 0.08 m `Toy_ink` line.
   - Pediment: a shallow triangle centred on the face, 9.0 m base, apex at
     **z=12.60**, sitting on the cornice, same `Toy_trim`, with the cornice
     moulding carried up its rakes.
   - Modillions: six `Toy_trim` blocks 0.35 x 0.30 x 0.55 m under the cornice at
     z=10.4, spaced 2.0 m.
   - Frieze: a 1.0 m recessed panel, 0.10 m deep, between z=9.6 and z=10.6.
   - Upper windows: four `Toy_glass` panels 1.5 x 2.6 m at z=5.4, at
     t = −4.9, −3.0, +3.0, +4.9, each in a 0.14 m `Toy_trim` frame recessed 0.12 m.
   - Sill band: `Toy_trim`, 0.25 m tall, projecting 0.12 m, at z=5.0.
   - Storefront: three `Toy_glass` panels 3.0 x 3.2 m at z=1.0 in a `Toy_trim`
     frame, plus a 1.2 x 2.6 m `Toy_ink` door recess at the south-east end.
   - Plinth: `Toy_stone`, 0.5 m tall, projecting 0.08 m.
4. **Set-back third floor at the Steuart end:** a `Toy_glass` band from z=11.20 to
   **z=13.90**, inset 1.6 m from the Steuart face, with a solid `Toy_trim`
   **stair over-run box** 3.2 x 3.6 m rising to **z=14.80** on the south-east side.
5. **Embarcadero curtain wall (NE end):**
   - Recessed ground floor: pull the face back 0.5 m from grade to z=3.6,
     `Toy_ink` back plane with a `Toy_glass` lobby wall and clear `Toy_glass`
     doors 2.8 x 3.0 m placed toward the north-west half of the frontage.
   - Signage band: `Toy_trim`, 0.9 m tall, z=3.6 to z=4.5, full width, projecting
     0.10 m; a 0.5 x 0.35 m `Toy_ink` **110** plate below it toward the doors.
   - Entrance canopy: `Toy_trim` slab 4.5 x 1.4 x 0.18 m at z=4.4 over the doors.
   - Curtain wall: from z=4.8 to **z=16.60**, five bays of `Toy_glass` in 0.18 m
     `Toy_trim` mullions, with 0.55 m `Toy_glassl` spandrel bands at z=11.0–11.6.
   - Jamb returns: 0.6 m `Toy_trim` strips at both ends of the frontage, full
     height.
6. **Roof fascia:** a `Toy_trim` slab 13.9 x 1.2 x 0.35 m across the Embarcadero
   end, top at **z=17.40**, projecting 0.60 m beyond the glass, with a `Toy_ink`
   soffit face. **This is the bbox top.**
7. **Main parapet:** 0.25 m thick `Toy_trim`, from z=16.60 to z=17.10, round the
   NE two-thirds of the perimeter; it steps down to the 11.60 m historic parapet
   at the Steuart end.
8. **Roof deck field:** `Toy_stone` slab, top at z=16.70, over the NE third
   (u from +4 to +20.5).
9. **Roof garden:** a `Toy_mint` planted band 12.0 x 10.5 m centred at u=−3, with
   four `Toy_sand` planter kerbs 0.35 m tall around and through it.
10. **Roof penthouse / plant:** `Toy_trim` box 5.0 x 4.0 m from z=16.70 to
    **z=17.30**, centred near u=0. Cap it below the 17.40 m fascia so the fascia
    stays the unambiguous crest and the loader's scale factor lands on 1.0.
11. **Roof skylight:** one `Toy_glassl` square 2.4 x 2.4 m, 0.30 m proud, at
    u=+13 on the deck.
12. Bevel 0.1 m, 2 segments, on everything.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_trim` | `#f3efe6` | rendered walls, cornice, pediment, modillions, mullions, signage band, fascia, penthouse, party walls |
| `Toy_stone` | `#d9d2c2` | Steuart plinth, roof deck field |
| `Toy_glass` | `#2a4d73` | curtain-wall panes, Steuart upper windows and storefront, set-back third floor |
| `Toy_glassl` | `#6f95b8` | curtain-wall spandrel bands, roof skylight |
| `Toy_ink` | `#3a3530` | lobby back plane, door recesses, parapet cap line, fascia soffit, the 110 plate |
| `Toy_mint` | `#8fd0a8` | roof-garden planting |
| `Toy_sand` | `#ece4d4` | planter kerbs |
| `Toy_glass_Glow` | `#2a4d73` | the curtain wall at night — the hero |
| `Toy_trim_Glow` | `#f3efe6` | the COMMONWEALTH CLUB signage band and the entrance canopy underside |
| `Toy_glassl_Glow` | `#6f95b8` | the roof skylight and the set-back third-floor glazing |

**Night state.** This is an events building: it is dark all day and full at 6 pm,
which is exactly what `cat 17`'s night profile says. The composition is
**one hero and two supports**: the Embarcadero curtain wall lit as a single warm
lantern across all three storeys (the hero — it is a glass box with an auditorium
behind it, so light it evenly rather than as a scatter), the signage band and
canopy as the ground-level cue, and the roof skylight plus the set-back glazing as
the faint aerial cue. The Steuart historic front stays **dark except for its
ground-floor storefront** — a rendered 1910 wall does not glow.

Glow shells must be thin surfaces proud of the opaque glazing behind them — the app
renders `_Glow` in a separate layer by day, and a closed shell counts twice, so keep
them open single-sided planes and choose the base colour on the assumption that
**the base colour is the night look**. Drive `_Glow` emission from Base Color at
strength 1.0 in the render rig (see the README's note on re-imported GLBs).

### 2.9 Top surface

At 17.4 m over a 41.9 x 13.9 m plan, and hemmed in by two taller neighbours, the
roof is the only part of this building the app's camera sees uninterrupted. It is
also the part the Club sells: a public roof terrace on the waterfront. A blank grey
membrane would sink it into the baked block between two blank grey membranes.

The design is a **gradient along the long axis**: hard paving at the Embarcadero
end where the public deck is, planting through the middle, and the quiet strip
behind the historic parapet at the Steuart end. That gradient also does the
narrative work of the whole asset — new at one end, old at the other — in the one
view the app actually gives you. The penthouse is the only vertical event and must
stay **below** the 17.4 m fascia so the bbox top is unambiguous.

### 2.10 Scope

**In the GLB:** the building, both street fronts, both party walls, parapets,
cornice and pediment, the set-back third floor and stair over-run, roof deck,
roof garden and planters, penthouse, skylight, entrance canopy and signage band

**Not in the GLB:** The Embarcadero, Steuart Street, the F-line tracks, the
Audiffred Building, the seven-storey office to the south-east, street trees,
street furniture, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 13,000 — below 599 Third's 15,000 because this building has half the plan area
and two blind faces, and well below the 27,000 contract ceiling. Suggested split:
shell, step, parapets and roof field ~2k; Embarcadero curtain wall (bays,
mullions, spandrels, lobby, canopy, signage, fascia) ~4k; Steuart historic front
(cornice, pediment, modillions, windows, storefront) ~4k; set-back volume and
over-run ~1k; roof garden, planters, penthouse, skylight ~1.5k; spare ~0.5k.

### 2.12 Draft manifest entry

```json
{
  "id": "110-embarcadero",
  "file": "110-embarcadero.glb",
  "anchor": [
    -122.3926624,
    37.7932325
  ],
  "targetHeightM": 17.4,
  "cat": 17,
  "name": "The Commonwealth Club (110 The Embarcadero)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`loadRadius` is the skill's default `max(2500, targetHeightM * 30)` = 2500; at
17.4 m the building is illegible long before 2,500 m, so the carved hole left
beyond the radius costs nothing.

### 2.13 Integration notes (for later, not this task)

- **New landmark (Case B).** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: '110Embarcadero'`, lon/lat as above, `height: 17.4`) and re-bake the
  affected tiles, or the baked block will sit inside the model. Manifest id
  `110-embarcadero` maps to registry id `110Embarcadero`.
- **Exclusion radius — measured, unusually comfortable.** `excluded()` in
  `pipeline/buildings.mjs` drops a footprint when its ring **centroid** *or* **any
  vertex** falls inside the radius. Measured against the DataSF footprints the bake
  actually reads (`ynuv-fyni`, streamed and centroided the same way):

  | Ring | Gate | Via |
  |---|---|---|
  | `SF3715002` — this building | **1.83 m** | centroid (its own nearest vertex is 20.40 m) |
  | `SF3715003` — 7-storey office, SE party wall | 14.27 m | centroid |
  | `SF3715001` — Audiffred Building, NW party wall | 14.55 m | centroid |
  | `SF3715025` — next lot SE | 28.35 m | centroid |

  The Overture/OSM traces of the same three buildings gate at 0.0 m (this
  building — its OSM ring centroid *is* the anchor), 13.95 m (Audiffred) and
  ~15.6 m (the office). Combining both traces, the window that drops exactly this
  building and nothing else is **1.83 < r ≤ 13.95 m**. Every ring here is
  centroid-gated because these lots are long and thin, so their corners are all
  20 m+ from the anchor.

  **Start at `exclude: 5`** — 2.7× above this building's gate and 2.8× below the
  first neighbour's, near the geometric middle of the band. Re-measure against the
  real bake input before committing the number (memory: sizing an exclusion from
  the wrong trace has been the recurring failure here), and check `verify-rebake`
  by penetration depth rather than per-cell counts, which can report "dropped
  nothing" for a working exclusion.
- **Camera preset.** `camera: { distance: 190, yaw: 135, pitch: 26 }`. Camera
  offset is `(sin yaw, ., cos yaw)` with +z south, so camera bearing = `180 − yaw`;
  yaw 135 stands the eye at bearing 45 — north-east, on The Embarcadero, looking
  back down the long axis over the glass front and across the roof to the Steuart
  pediment. That is the only view that carries both faces. 190 m suits a 17.4 m
  building (cf. `181SouthPark` at 190 for 16.5 m). **No `key`** — at 17.4 m this is
  block texture, not a destination.
- **Terrain.** Flat made ground on the old waterfront (LiDAR ground mean 3.43 m
  NAVD88, range 0.36 m across the footprint). Seating should be uneventful; check
  it anyway.
- **Batch note.** This landmark is being built in a batch. Follow batch mode in
  `docs/asset-pipeline/ADDRESS-TO-ASSET.md`: run the bake and the full QA on it,
  then `git checkout -- app/public/tiles api/_data` and commit **source only**
  (GLB, manifest entry, `landmarks.mjs` entry, this plan, `artifacts/`). Verify
  with `git diff --name-only origin/main` before handing off.
- **Shared BatchedMesh pressure.** The landmark batch is close to full in this
  quadrant of the city, and an overflow drops a *different* landmark on every
  reload rather than this one. Check the merge line's vertex total during local QA
  before blaming this asset for anything missing nearby.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] bbox top exactly 17.4 m (the Embarcadero roof fascia) so the loader's scale
      factor is 1.0 — confirm nothing on the roof pokes above it
- [ ] Dimensions plausible in meters and consistent with 2.1 (≈ 41.9 x 13.9 plan,
      on the 135.2 deg heading, so the AABB is roughly 39 x 39 m)
- [ ] Triangles at or under 13,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the curtain wall, the signage band and canopy, the roof
      skylight and the set-back third-floor glazing — never on the Steuart
      rendered wall
- [ ] Glow shells are open single-sided planes proud of the opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume + deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + night render + contact sheet regenerated from the final
      export, with the aerial taken from the north-east
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

1. **The height is measured, not published, and the LiDAR actively lies here.**
   No source gives a height for this building. DataSF's footprint record
   `SF3715002` is **2010 LiDAR** — five years before the works began — so its
   median (10.33 m) describes the *old two-storey warehouse*, and its maximum
   (24.43 m, σ 3.38 m over the footprint) is an outlier of the kind this project
   has learned to refuse. The 17.4 m in 2.1 comes instead from a rectified
   60 px/m elevation built from Street View pano `yo5P5pi5QKGaa2I7JTPGvQ`, with:
   - the pano's position independently corroborated — the two facade corners,
     projected to true bearings 203.05 deg and 248.5 deg, land on the building's
     actual edges in the rectilinear frame, and the 45.5 deg angular span
     sine-rules back to 13.93 m against a measured 13.91 m frontage;
   - the vertical zero pinned on the pavement line rather than assumed from a
     camera height (which solves to 1.93 m above the pavement, not the nominal
     2.5 m — the difference is the kerb);
   - the perpendicular distance D = 16.73 m, whose ±0.4 m uncertainty is the
     dominant residual and puts the quoted height at **17.4 ± 0.6 m**.

   Two independent checks agree: (a) the storey ladder read off the same
   elevation — ground floor to 4.2 m, a 7.5 m double-height auditorium volume,
   a 5.2 m third floor — sums to the same crest; (b) the 2010 LiDAR's 10.33 m
   median is exactly where the *old* roof should be if the new third floor was
   built on top of it, and the Steuart-side measurement puts the retained
   historic parapet at 11.5 m, right above it. If a drawing or a published figure
   turns up, it beats all of this.

2. **The Steuart end is genuinely lower than the Embarcadero end (11.6 m vs
   17.4 m), and that is the plan's biggest single claim.** It is supported by two
   separate rectified elevations and by the preservation logic (retain the
   two-storey front, set the addition back). But the setback *distance* — how far
   in from the Steuart face the new floor starts — is inferred from one oblique
   Street View frame, and 2.7's 1.6 m is a guess. Getting it wrong changes the
   aerial silhouette more than any other number in this plan.

3. **OSM tags this building `building:levels` inconsistently with the permits.**
   Every DBI record from 2017 says three storeys and PA 201312174360 records the
   2 → 3 change explicitly. Three is right; treat any higher OSM level count as
   stale.

4. **The Embarcadero curtain wall is planar, not curved.** In the equirectangular
   panorama its spandrel bands bow strongly, which reads as a segmental bow in
   plan. They are dead straight in Google's rectilinear frames of the same pano.
   This is projection, not architecture — do not model a curve.

5. **Roof-object placement is inferred.** Google's z22 imagery over this block is a
   strong oblique in which a 17 m roof displaces several metres; only the Bing z20
   near-nadir frame was used, and at 0.118 m/px it resolves zones, not objects. The
   *pattern* (deck at the Embarcadero end, planting through the middle, one
   penthouse, one square feature) is well supported by that frame and by the Club's
   own description of a roof garden plus a public terrace. The coordinates are not.

6. **The address is ambiguous in OSM.** Nominatim returns four objects for "110 The
   Embarcadero"; three are stray address points up the waterfront. The correct
   polygon is way/256969674, identified by the Commonwealth Club amenity node
   9659886917 falling inside it and by DataSF parcel 3715002 matching its ring to
   1 m. The parcel's own official address is **115 Steuart Street** — do not let a
   Steuart-addressed record be mistaken for a different building.

7. **The rectified elevations in this research are mirrored relative to the
   photographs** on the Embarcadero side (the COMMONWEALTH CLUB lettering reads
   backwards in them) and un-mirrored on the Steuart side. Every left/right claim
   in 2.4 has been restated in NW/SE terms against the raw photographs to avoid
   inheriting that flip — but re-check the entrance side and the stair-over-run
   side against a photograph before trusting them.
