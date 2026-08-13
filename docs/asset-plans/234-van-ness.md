# 234 Van Ness Avenue — The Kelsey Civic Center

WRNS Studio + Santos Prescott & Associates' 2025 disability-forward affordable
housing block, directly across Van Ness from City Hall. An eight-storey L that
wraps an open-air courtyard, striped in white and grey fibre-cement with
copper-anodized aluminium fins, and — the thing nobody else in the Civic Center
does — a courtyard whose eight storeys of inner wall are a **candy-coloured
patchwork** of sky blue, coral, mustard, olive and cream panels, wide open to the
app's downward camera.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/234-van-ness/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `234-van-ness` |
| Existing procedural builder | none — new landmark (Case B: needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.12) |
| WGS84 anchor | `-122.4193071, 37.7780541` (footprint AABB centre, measured) |
| Target height | **30.12 m** (mechanical-penthouse crest; main roof 25.73 m = the published "84 feet", parapet 26.80 m — all three read off the architect's dimensioned south elevation) |
| Footprint | L-shaped ring, 55.60 m (E–W) x 44.80 m (N–S), **1,304 m²** measured — the geotechnical report's 13,815 sq ft (1,283 m²) confirms it to 1.6 % |
| Triangle cap | 24,000 |
| Category | `2` (Apartments) |

> **Identity note, read this first.** The building is marketed and published as
> **240 Van Ness Avenue**; the assessor addresses the assembled lot as **165
> Grove Street** (block 0811, lot 0811204, created 2022-09-17 out of lots
> 0811016/018/019/021); the requested **234 Van Ness** is the Van Ness street
> number of the same parcel's frontage, and SF YIMBY files it under
> "234 Van Ness Avenue". All four names are one building. Slug and manifest id
> stay `234-van-ness` to match the request; every alias is recorded in
> REFERENCE.md so search finds it.

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh agent session.

````markdown
# Create a production-ready 234 Van Ness Avenue (The Kelsey Civic Center) GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of The Kelsey Civic Center, 234–240 Van Ness
Avenue, and deliver it as a downloadable, validated GLB.

Do not integrate or deploy the model yet. Create the asset, validate it, render
review images, and commit the deliverables to your working branch.

## Read the project sources first

Before any research or modeling, read in this order:

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-asset-check/SKILL.md`
5. `app/public/sf-assets/landmarks_manifest.json`
6. `artifacts/380-brannan/` — the reference implementation of this exact
   deliverable: four deterministic scripts, the same headless invocation, the
   same report structure
7. `artifacts/101-grove/` — the nearest sibling in the scene, one lot east on
   the same block, and the closest thing to a neighbour this asset has
8. `docs/asset-plans/234-van-ness.md` — this plan, whose dossier is your
   research starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules.

**Re-verify §2.2–2.6 of this dossier before modelling.** Plans in this repo have
been wrong before; if the model and the plan disagree, REPORT.md wins and the
correction is written up prominently.

## Must capture

- The **L-shaped eight-storey massing**: a 54 m bar along Dr. Tom Waddell Place
  with a 15 m head on Van Ness, and a wing running north to a 22 m frontage on
  Grove Street, wrapping the neighbouring corner lot
- The **open-air courtyard** cut through the wing — the identity feature, and the
  only one the app's downward camera can see
- The **candy-coloured courtyard walls**: full-height vertical panel stripes in
  sky blue, coral, mustard, olive-green, pale blue and cream, against the calm
  white/grey street elevations. This contrast *is* the building
- The **vertical striping** of the street elevations: broad white fibre-cement
  bands alternating with charcoal window-wall bays and slim **copper-anodized
  fins**, capped by a copper fascia band at the parapet
- The **projecting glazed corner bay** stacked up the Van Ness/Waddell corner
- The **green rooftop deck** facing City Hall: pale paver field, dark bronze
  raised planters with vivid planting, a perimeter picket guardrail, wood benches
- The **mechanical penthouse** at 30.12 m that sets the crest
- The ground floor: a **textured-concrete base** with storefront glazing and a
  wood-slat trellis canopy at the Van Ness/Waddell corner, and the arched
  courtyard portal

## Research the building independently

Verify the dossier rather than trusting it. Re-check at minimum the architectural
height, the footprint ring, the WGS84 anchor, the courtyard's position and size,
and the real-world orientation. §2.7 flags the courtyard's position as the
largest inference in the plan — any published floor plan, site plan or aerial
beats it.

Prefer architect/owner publications, planning and permitting documents,
architectural press, geolocated photography, and aerial imagery. Never rely on a
single photograph or a single AI-generated image. Separate verified facts from
visual inference.

## Create a reference dossier

Write `artifacts/234-van-ness/REFERENCE.md`: source links and what each
establishes; verified dimensions and location; every address alias; orientation;
observations from all four sides and above; the 3–5 strongest recognition cues;
features to preserve; features to simplify; uncertainties and conflicting
evidence.

## Make your own design decisions

Follow §22 of the style bible. This is a **secondary building with one loud
interior**. Its job in the scene is to be the crisp modern block that makes City
Hall across the street look monumental — it must not compete with City Hall,
Davies, or the Opera House. Spend the budget on the courtyard, the vertical
striping rhythm, the corner bay, and the roof deck. Resist modelling individual
mullions, balcony pickets, panel joints or fin profiles — they become noise two
hundred metres up.

## Scope of the exported asset

Export the building itself, including its courtyard, roof deck, planters,
guardrail, penthouse, corner bay, canopy and ground-floor base.

Do not include Van Ness Avenue, Grove Street, Dr. Tom Waddell Place, the
neighbouring 171 Grove corner building, 101 Grove, City Hall, street furniture,
street trees, vehicles, people, plinths, cameras or lights.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world metres; origin at base centre; minimum geometry Z ≈ 0; applied
transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-colour materials named
`Toy_*`; `_Glow` suffix only on night-glow surfaces; no `Toy_body`; no cameras,
lights, animations, armatures or constraints; at most 24,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation.
The Van Ness front faces west (outward normal 261.8° true). The contract's
"front faces −Y" cannot be honoured literally; real-world orientation wins
(AGENTS rule 5). Record the decision and the measured heading in REPORT.md.

**Height normalization:** the exported bounding-box top must land exactly on
**30.120 m** so the loader's `targetHeightM / measuredHeight` scale is 1.000. The
penthouse is the only thing allowed to touch it.

## Reproducible Blender workflow

Blender 4.5 LTS or newer, headless only: `blender -b --python script.py -- args`;
no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/234-van-ness/build_234_van_ness.py` (deterministic build script),
`234-van-ness.blend`, and `234-van-ness.glb`.

## Required review renders

`234-van-ness-top.png`, `-north.png`, `-east.png`, `-south.png`, `-west.png`,
`234-van-ness-contact-sheet.png`, a high three-quarter aerial hero
`234-van-ness-aerial.png`, and `234-van-ness-aerial-night.png`.

The four elevations share scale, framing, lighting, exposure and projection.
**The aerial is the hero image** and must be framed from the south-west, high
enough that the courtyard and the roof deck both read in one frame — that is the
only angle from which this asset's identity is visible.

Drive `_Glow` night renders from Base Color, not from the imported emission.

## Validate the exported GLB

Re-import into a fresh isolated Blender scene and validate the re-import, not the
source scene. Report object count, triangle count, dimensions, bbox min/max,
min Z, XY centre offset, material names, image-texture count, camera count, light
count, animation count, applied-transform status, negative-scale status,
normal-orientation status (per-object signed volume **and** a deterministic
visibility-ray test, ≤ 0.15 % residual), unexpected geometry, and per-material
contract compliance. Write `validation.json` and `REPORT.md`.

## Manifest draft

Verify the anchor and height yourself, then include this draft in REPORT.md. Do
not edit the production manifest in this task.

```json
{
  "id": "234-van-ness",
  "file": "234-van-ness.glb",
  "anchor": [-122.4193071, 37.7780541],
  "targetHeightM": 30.12,
  "cat": 2,
  "name": "The Kelsey Civic Center (234 Van Ness Avenue)",
  "estimated": false,
  "dims": [55.60, 44.80, 30.12],
  "tris": N,
  "loadRadius": 2500
}
```
````

---

## Part 2 — Research and design dossier

Compiled 13 August 2026. Values marked *inferred* or *estimated* are visual or
derived, not published figures.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Names | The Kelsey Civic Center; 234 Van Ness Ave; 240 Van Ness Ave (published); 165 Grove St (assessor) | SF YIMBY, WRNS Studio, Rockridge Geotechnical, DataSF parcels — *measured/verified* |
| Parcel | Block 0811, lot 0811204, 13,815 sq ft, created 2022-09-17 from lots 0811016/018/019/021 | DataSF `acdm-wktn` (measured); Rockridge Geotechnical (site footprint) |
| Architects | WRNS Studio with Santos Prescott & Associates | WRNS Studio project page, SF YIMBY |
| Developers | Mercy Housing California + The Kelsey | Mercy Housing, thekelsey.org |
| Contractor | Cahill Contractors; broke ground mid-2023, topped out Aug 2024 | SF YIMBY |
| Opened | October 2025 | SF YIMBY "Grand Opening", Mercy Housing |
| Programme | 112 affordable apartments (80 studios, 32 two-bedroom) at 20–60 % AMI; 25 % reserved for people with disabilities; ~1,400 sq ft Disability Cultural Center; ground-floor retail; 62 bike spaces | SF YIMBY, The Kelsey |
| Cost | $88.3 M | Rockridge Geotechnical, SF YIMBY |
| Storeys | 8, at grade, **no basement** (the previous building's basement was filled) | Rockridge Geotechnical |
| Courtyard | 3,450 sq ft (320 m²), open-air, ground level | WRNS Studio / SF YIMBY |
| Cladding | textured fibre-cement panel rainscreen in vertical bands; vertical copper-anodized aluminium fins; charcoal-painted aluminium window wall; copper-anodized fascia panel at the parapet; textured concrete base | WRNS Studio south-elevation drawing (material keynotes) — *measured from the drawing* |
| Structure | mat foundation on drilled displacement columns; all-electric, low-carbon | Rockridge Geotechnical, The Kelsey |
| OSM | ways `1547771521` + `1547771522`, both `building=yes`, traced 2026-08-06 by user *pootriarch*; together 1,302 m² | OSM API — *measured* |

### 2.2 Sources

- https://wrnsstudio.com/projects/the-kelsey-civic-center/ — architect's project page
- https://sfyimby.com/2025/10/grand-opening-for-kelsey-civic-center-at-240-van-ness-avenue-san-francisco.html — completion, "84 feet tall", L-shape, cladding description, unit mix; carries four Bruce Damonte photographs (establishing view, corner view, courtyard, rooftop deck) that are the primary visual reference for §2.5
- https://sfyimby.com/2021/01/renderings-for-the-kelsey-civic-center-at-240-van-ness-avenue-civic-center-san-francisco.html — **the dimensioned architect's `SOUTH ELEVATION - TOM WADDELL` at 1/8" = 1'-0"**, with the full level schedule and material keynotes. This is the single most valuable source in the plan and every height in §2.3 comes off it.
- https://www.rockridgegeo.com/projects/affordable-senior-housing/the-kelsey-civic-center/ — 13,815 sq ft site footprint, 8 levels at grade, no basement, mat foundation
- https://thekelsey.org/projects/civic-center/ and https://www.mercyhousing.org/2025/11/… — programme, AMI bands, disability-forward design process
- https://data.sfgov.org/resource/acdm-wktn.json — SF parcels, block 0811; the lot assembly and its geometry
- https://data.sfgov.org/resource/ynuv-fyni.json (as bundled in `pipeline/data/buildings_datasf.geojson`) — the 2010 LiDAR footprints the bake actually reads; the basis of §2.12's exclusion arithmetic
- OSM Overpass API — ways 1547771521 / 1547771522 (the built footprint), way 8917756 (Dr. Tom Waddell Place), parcels and neighbours

### 2.3 Height — *measured*

Read directly off the architect's dimensioned south elevation:

| Datum | Drawing | Metres |
|---|---|---|
| Level 1 (grade) | 0'-0" | 0.000 |
| Level 2 | 15'-0" | 4.572 |
| Levels 3–8 | +9'-11" each | 7.595 / 10.617 / 13.640 / 16.662 / 19.685 / 22.708 |
| **ROOF** | **84'-5"** | **25.730** — the published "84 feet above Van Ness" |
| Copper fascia / parapet top | +3'-6" | 26.797 |
| **Mechanical penthouse crest** | **+14'-5" over roof** | **30.124 → normalize to 30.120** |

`estimated: false`. The 15'-0" ground floor and the 9'-11" residential floor are
the whole facade rhythm and must be built on these lines, not on a uniform
division.

### 2.4 Anchor, footprint and orientation — *measured*

Ways 1547771521 + 1547771522 unioned along their shared edge, reprojected with
the app's tangent projection (`LON0 −122.4375`, `LAT0 37.77`). Union area
**1,304 m²** against the geotechnical report's 1,283 m² — 1.6 %, which is what
confirms the two untagged 2026 traces are this building and not two others.

- Axis-aligned extent **55.60 m (E–W) x 44.80 m (N–S)**
- Minimum-area OBB 54.10 x 36.58 m at **170.75°** — the Civic Center grid
- **Anchor (model origin = ring AABB centre): `lon −122.4193071, lat 37.7780541`**
- Furthest vertex from the anchor: 34.02 m

Modelled ring, metres, x east / y north, origin at the anchor, **CCW in plan**:

```
v0 (-25.60, -22.40)   v1 (-27.80,  -7.10)   v2 (  3.30,  -2.00)
v3 (  2.20,   4.30)   v4 ( -0.30,  18.60)   v5 ( 21.90,  22.40)
v6 ( 24.20,   8.20)   v7 ( 25.90,  -2.60)   v8 ( 27.80, -13.70)
```

| Edge | Length | Outward normal (true) | What it is |
|---|---|---|---|
| v8 → v0 | **54.10 m** | 170.7° (S) | **Dr. Tom Waddell Place** — the long public face |
| v0 → v1 | **15.46 m** | 261.8° (W) | **Van Ness Avenue** — the address frontage |
| v1 → v2 | 31.52 m | 350.7° (N) | lot line against 244 Van Ness / the corner lot |
| v2 → v3, v3 → v4 | 6.40 + 14.52 m | 260.1° (W) | lot line against the 171 Grove corner building |
| v4 → v5 | **22.52 m** | 350.3° (N) | **Grove Street** frontage |
| v5 → v6, v6 → v7, v7 → v8 | 14.39 + 10.93 + 11.26 m | ~80.8° (E) | party line against 101 Grove |

Three public faces (Waddell, Van Ness, Grove) and two party/lot lines. The
building wraps the 171 Grove corner lot rather than holding the corner itself —
that is why photograph 2 shows a low old stucco building immediately north of the
white block.

Dr. Tom Waddell Place (OSM way 8917756) runs ENE from Van Ness at z ≈ −861 to
−881, about 6.4 m clear of the south wall: a one-way service alley, which is what
the "DO NOT ENTER" sign in the corner photograph is standing in.

### 2.5 What each side shows — *observed from photographs and the architect's elevation*

**South (Dr. Tom Waddell Place), 54.1 m — the long face.** A 15'-0" **textured
concrete base** with storefront glazing, painted aluminium vents, a coiling
garage door and hollow-metal service doors. Above it seven residential floors in
a strict vertical rhythm: broad white fibre-cement panel bands alternating with
narrower charcoal window-wall bays, each bay a stack of vision glass over opaque
glass infill, divided by **slim copper-anodized fins** that run the full seven
storeys. Fibre-cement spandrels close the bays at each floor line. The wall
terminates in a **copper-anodized fascia band** at 25.73 → 26.80 m — the one warm
line on an otherwise cool elevation. Behind it, set back, the fibre-cement-clad
penthouse and its darker anodized mechanical screen.

**West (Van Ness Avenue), 15.5 m — the address face.** The same system, only 15 m
wide, so it reads as a narrow white end wall with two or three punched bays and a
scatter of coral/salmon accent panels. At the south-west corner a **projecting
glazed bay** stacks six storeys of large charcoal-framed windows and cantilevers
over the ground floor on a copper-toned soffit — the strongest street-level move
on the building. Under it, glazed lobby/retail with a **wood-slat trellis canopy**
on charcoal steel outriggers. The **arched courtyard portal** opens here.
*(Portal position inferred — see §2.11.)*

**North (Grove Street), 22.5 m.** *Inferred from the same facade system.* The
wing's end wall facing City Hall's block: white bands, charcoal bays, fins,
fascia. No photograph of it was located.

**East and the two west lot lines.** Party walls against 101 Grove and the corner
lot: the same white fibre-cement field, far fewer openings, no fins, plain
parapet. *Inferred.*

**The courtyard — the identity.** An open-air court cut through the wing.
Its walls are the opposite of the street: eight storeys of **full-height vertical
panel stripes in sky blue, coral, mustard, olive-green, pale blue, cream and
charcoal**, arranged as an irregular patchwork with no two adjacent bays alike.
One wall carries **open-air access galleries** — a stack of cream decks behind
light metal picket railings, with warm orange-red perforated screens at one end.
The ground plane is pale plank paving and grey unit pavers with planted beds,
small trees, loose seating and a festoon of catenary lights; one end wall is a
flat **mustard-yellow** plane. A big **soft segmental arch** frames the passage
into it under a concrete soffit.

**The roof.** An occupied deck facing City Hall: pale concrete paver field,
**dark bronze raised planters** with vivid mixed planting, wood-topped benches, a
perimeter guardrail of fine vertical pickets, and the fibre-cement penthouse with
its anodized mechanical screen at the west end. Nothing else. This is the surface
the app's camera spends the most time looking at, and it is genuinely handsome —
build it properly.

### 2.6 Recognition cues (ranked)

1. **The open courtyard with candy-coloured walls** — visible only from above,
   which is exactly where the app's camera is. Nothing else in the Civic Center
   looks like this.
2. **The white-and-charcoal vertical stripe** of the street elevations with the
   thin copper fins and the copper fascia lid.
3. **The L that wraps a corner it does not own** — the notch at the Van
   Ness/Grove corner is a real, checkable piece of the city.
4. **The projecting glazed corner bay** at Van Ness and Waddell.
5. **The planted roof deck** facing City Hall.

### 2.7 Massing recipe

Dimensions are the starting point, not a straitjacket — adjust after the first
aerial review render.

1. **Base:** extrude the measured ring from z=0 to **4.572** in `Toy_stone`
   (textured concrete), pulled 0.12 m proud of the body above so the base reads
   as a plinth.
2. **Body:** extrude the ring from 4.572 to **25.730**, `Toy_white`.
3. **Courtyard void:** cut an open shaft of ~**16 x 17 m** (≈ 272 m² at the
   opening, 320 m² at ground with the recessed base) through the wing, centred
   near (x 12.5, y 8.5), from z=**2.6** (the arched soffit) to the roof. Its four
   inner faces are the colour patchwork.
4. **Vertical striping (all three public faces):** alternate `Toy_white` panel
   bands ~2.8 m wide with `Toy_ink` window-wall bays ~2.0 m wide from 4.572 to
   25.730. Per bay per floor, a `Toy_glass` vision slab over a `Toy_glassl`
   opaque infill; `Toy_rust` fin strips 0.18 m wide, 0.10 m proud, at every band
   joint, running the full seven storeys uninterrupted.
5. **Coral accents:** replace ~8 scattered `Toy_white` panels on the Van Ness and
   Waddell faces with `Toy_coral` — the building really does this, and it is what
   keeps the street elevations from reading as grey.
6. **Fascia:** a `Toy_rust` ring band 25.730 → 26.797, 0.22 m proud, on all
   faces. The single warm horizontal.
7. **Corner bay (Van Ness/Waddell corner):** a 6.5 x 3.2 m projecting box from
   z=**7.6** to **25.0**, 1.1 m proud, faced almost entirely in `Toy_glass` with
   `Toy_ink` frames and a `Toy_rust` soffit slab under it.
8. **Ground floor:** storefront glazing (`Toy_glass` inside `Toy_ink` reveals)
   along Van Ness and the west half of Waddell; a `Toy_roofd` coiling door and
   two `Toy_ink` service doors on the east half; a `Toy_sand` wood-slat canopy
   (a plate plus six slats, not thirty) on `Toy_ink` outriggers at the corner.
9. **Arched portal:** a segmental-arched recess 5.4 m wide, springing at 3.4 m,
   crest 4.4 m, in the Van Ness face, `Toy_ink` behind a `Toy_trim` archivolt.
10. **Courtyard walls:** the four inner faces divided into ~1.6 m vertical
    stripes, each a full-height `Toy_sky` / `Toy_coral` / `Toy_mustard` /
    `Toy_mint` / `Toy_cream` / `Toy_glassl` / `Toy_ink` panel from a fixed
    deterministic sequence (no randomness — the script must rebuild identically).
    One face carries six stacked `Toy_cream` gallery decks 0.9 m proud with a
    `Toy_steel` rail band, and a `Toy_ioorange` screen panel at its north end.
11. **Courtyard floor:** a `Toy_sand` paver pad at z=0.15, four `Toy_roofd`
    planter boxes with `Toy_mint` tops, and three chunky trees (trunk + one
    crown volume each).
12. **Roof deck:** `Toy_trim` paver field at 25.73 → 25.95; five `Toy_roofd`
    planters 0.55 m tall with `Toy_mint` planting caps; four `Toy_sand` bench
    blocks; a perimeter guardrail = a `Toy_steel` bottom rail, 0.10 m pickets at
    1.1 m pitch, and a top rail at 26.80 so the rail and the fascia agree.
13. **Penthouse:** a `Toy_white` block ~14 x 9 m at the west end, 25.73 → 28.9,
    with a `Toy_roofd` anodized mechanical screen on top setting the crest at
    exactly **30.120**; two `Toy_steel` units and a hatch beside it.

### 2.8 Palette map

The street elevations are the neutral kind (style bible §7): one warm accent (the
copper fins and fascia) and a handful of coral panels. Every saturated colour in
this asset is spent inside the courtyard, where it belongs.

| Element | Material | Hex |
|---|---|---|
| Fibre-cement panel field, penthouse | `Toy_white` | f7f4ec |
| Concrete base, canopy slats, benches, courtyard pavers | `Toy_stone` / `Toy_sand` | d9d2c2 / ece4d4 |
| Roof paver field, archivolt | `Toy_trim` | f3efe6 |
| Window-wall bays, reveals, frames, service doors | `Toy_ink` | 3a3530 |
| Vision glazing, corner bay | `Toy_glass` | 2a4d73 |
| Opaque glass infill, courtyard blue stripes | `Toy_glassl` | 6f95b8 |
| Copper-anodized fins, fascia, bay soffit | `Toy_rust` | a86444 |
| Coral accent panels, courtyard coral stripes | `Toy_coral` | e8735a |
| Courtyard sky-blue stripes | `Toy_sky` | 6db3d9 |
| Courtyard mustard stripes, the yellow end wall | `Toy_mustard` | d9a441 |
| Courtyard olive stripes, planting caps | `Toy_mint` | 8fd0a8 |
| Courtyard cream stripes, gallery decks | `Toy_cream` | f2ede3 |
| Gallery screen | `Toy_ioorange` | c0402a |
| Guardrail, rails, roof plant | `Toy_steel` | 9aa0a6 |
| Planters, mechanical screen, coiling door | `Toy_roofd` | 45454a |
| Night: lit apartment windows | `Toy_glassl_Glow` | 6f95b8 |
| Night: courtyard festoon + ground-floor lobby | `Toy_trim_Glow` | f3efe6 |

### 2.9 Night state

Required. **Hero:** the courtyard — a warm `Toy_trim_Glow` wash at its floor and
a line of festoon points, so the one thing that identifies this building from
above still identifies it after dusk. **Supporting:** an irregular scatter of lit
apartment windows (roughly a third of the bays, never a full grid) plus the
ground-floor lobby glazing on Van Ness. Nothing on the roof glows. Glow shells
are thin panels proud of the opaque glazing — the app draws `_Glow` at ~12 %
alpha by day, so a coincident face reads as a smear.

### 2.10 Triangle budget

Cap **24,000**.

| Group | Est. tris |
|---|---|
| Base + body prisms + courtyard shaft + fascia ring | ~2,200 |
| Vertical striping: ~34 bays x 7 floors x (glass + infill) | ~6,500 |
| Fins: ~36 full-height strips | ~1,700 |
| Courtyard: ~40 colour stripes + 6 galleries + rails + screen | ~4,200 |
| Ground floor: storefronts, doors, canopy, arched portal | ~1,400 |
| Corner bay | ~600 |
| Roof: pavers, 5 planters, benches, guardrail (~90 pickets) | ~3,200 |
| Penthouse + plant | ~700 |
| Glow shells | ~800 |
| Bevel overhead | the balance |

If it overshoots: thin the guardrail pickets first, then the fin count, then the
window bays on the two party walls. Never the courtyard.

### 2.11 Open risks / what is not verified

1. **The courtyard's exact position and size is the largest inference in the
   plan.** 3,450 sq ft is published; *where* it sits in the L is read off the
   photographs and the massing, not off a plan. Any published floor or site plan
   overrides §2.7 step 3.
2. **The arched portal is placed on Van Ness by inference.** The courtyard
   photograph proves the arch exists and that it is big; it does not prove which
   street it opens off. The south elevation's ground floor is service-heavy,
   which argues against Waddell.
3. **North (Grove) elevation and both party walls are inferred** from the
   photographed system. No photograph of any of them was located.
4. **The colour sequence of the courtyard panels is designed, not surveyed.** The
   palette is read off one photograph of two walls; the sequence is the modeller's
   and must be deterministic in the script.
5. **OSM ways 1547771521/1547771522 are untagged, one week old and unverified by
   a second mapper.** The 1.6 % agreement with the geotechnical report's site
   area is what makes them trustworthy; if they are ever retagged or corrected,
   re-measure.
6. **The 171 Grove corner building is collateral in the re-bake** — see §2.12.
   This is a real, standing 9.7 m building that this landmark's exclusion radius
   removes from the scene, and it is the one thing in this plan that makes the
   city *less* accurate.

### 2.12 Integration — Case B, and the exclusion problem

**Case B.** No `234-van-ness` id exists in `pipeline/lib/landmarks.mjs` or
`app/src/landmarks.js`, so integration needs a registry entry **and** a re-bake,
or the baked procedural blocks will intersect the GLB.

`excluded()` in `pipeline/buildings.mjs` drops a footprint when its centroid **or
any ring vertex** falls inside the radius. Measured against the file the bake
actually reads (`pipeline/data/buildings_datasf.geojson`, the 2010 LiDAR
footprints), sorted by nearest vertex to the anchor:

| DataSF `mblr` | nearest vertex | centroid | height | what it is |
|---|---|---|---|---|
| `SF0811019` | **6.14 m** | 11.83 m | 10.27 m | on the site — demolished 2023 |
| `SF0811020` | **6.14 m** | 16.10 m | 9.71 m | **171 Grove — still standing** |
| `SF0811018` | 11.67 m | 15.07 m | 9.24 m | on the site — demolished 2023 |
| `SF0811001` | 17.49 m | 50.83 m | 19.77 m | 101 Grove — already a landmark (`exclude: 22`) |
| next | 30.11 m | | | 200–214 Van Ness |

Radius bands (footprints dropped): `r < 7` → 0 · `7–11` → 2 · `12–17` → 3 ·
`18–30` → 4 · `31+` → 6.

**Shipping `exclude: 14`** — the middle of the 12–17 band. It drops exactly the
three footprints on and beside the site and touches nothing else; 101 Grove stays
outside it and remains governed by its own entry.

**The unavoidable collateral is `SF0811020`, the 171 Grove corner building.** It
shares a party-wall vertex with the site at exactly the same 6.14 m, so *no*
radius removes the two demolished footprints without removing it too. The choices
are the same three as at 1008 General Kennedy: accept the drop, model the
neighbour as well, or build the `excludePoly` clipping mechanism that would
actually fix this. **This plan ships the drop and flags it** — a 9.7 m one-storey
commercial shed is a far smaller loss than the twelve-building Letterman campus,
and the alternative is leaving two demolished buildings standing inside a 2025
landmark. A follow-up asset for 171 Grove would close the gap cleanly.

Draft registry entry:

```js
{
  // The Kelsey Civic Center, 2025. L-shaped, wraps the 171 Grove corner lot.
  // exclude 14 sits in the 12-17 m band that drops exactly the three DataSF
  // footprints on and beside the site (SF0811018/019 demolished for this
  // building, SF0811020 unavoidable collateral - see the plan, 2.12) without
  // reaching 200-214 Van Ness at 30.1 m. 101 Grove at 17.5 m stays outside it.
  id: '234VanNess',
  name: 'The Kelsey Civic Center (234 Van Ness Avenue)',
  lon: -122.4193071,
  lat: 37.7780541,
  height: 30.12,
  exclude: 14,
  camera: { distance: 320, yaw: 225, pitch: 30 },
}
```

The camera preset looks down from the south-west at 30° — the only angle from
which the courtyard and the roof deck both read.

Then run `docs/asset-plans/INTEGRATION-PROMPT.md` in full: manifest entry with
the explicit `loadRadius`, registry entry, tile re-bake, audit 1.6, local
verification (single building, scale 1.0, orientation, terrain seating, night
glow, draw calls < 300), and the mandatory fallback drill. `BATCH: yes` applies —
run the bake, QA on it, then `git checkout -- app/public/tiles api/_data` and
commit source only.

### 2.13 Streaming

`loadRadius` follows the default rule `max(2500, 30.12 x 30)` = **2500 m**. A
30 m block in a dense district is illegible well before that, and its procedural
stand-in has been carved out, so the radius must be comfortably larger than the
distance at which the empty lot would be noticed. No case for `alwaysLoaded`.

### 2.14 Validation checklist

- Fresh-scene re-import of the exported GLB, not the source scene
- `dims.z` exactly **30.120** so `targetHeightM / measuredHeight` = 1.000
- `min_z` within 0.5 m of 0; XY centre within 1 m of origin
- ≤ 24,000 triangles
- No image textures, no transparency, no cameras/lights/animation/armatures
- Every material `Toy_*`, no `Toy_body`
- `_Glow` only on the lit-window scatter, the courtyard wash and the lobby
- Per-object signed volume positive for every object; ray residual ≤ 0.15 %
- No degenerate triangles — leave the fins, pickets, panel stripes and glow
  shells unbevelled; they are thinner than twice the bevel width
- Aerial render reviewed **before** the formal rig, and again after
