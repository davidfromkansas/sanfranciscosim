# 132 The Embarcadero (Jewish Community Federation Building) — SF-SIM asset plan

A 1984 red-brick office block on the seawall lots between Mission and Howard, one
of four narrow deep lots that run the full 43 m from Steuart Street through to the
Embarcadero. Seven storeys, a measured 27.4 m parapet, and a 13.75 x 42.95 m
footprint — **the narrowest street frontage in the bespoke set**, 13.75 m against
524 Second's 42 m and 501 Second's 42.2 m.

It is a two-frontage building with no flanks: both long sides are party walls, so
the entire asset is two 13.75 m-wide elevations, a 43 m roof, and the top of one
brick side wall where the neighbour to the northwest falls away. That is the design
problem. There is almost no silhouette to work with, the building is one storey
taller than everything around it, and the only things that make it recognisable
from the air are its **red brick in a row that is otherwise cream, glass and
grey**, its **deep pale crown band**, and the fact that it is a **slab on edge** —
13.75 m wide and 43 m deep, pointed at the water.

The Embarcadero elevation is the address and the public face (a storefront base
under a full-width second-floor glazed ribbon, six bays of punched windows above);
the Steuart elevation is the institution's front door, with `JEWISH COMMUNITY
FEDERATION` incised across the brick above a deeply recessed entrance and a line of
security bollards at the kerb.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/132-embarcadero/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `132-embarcadero` |
| Existing procedural builder | none — new landmark (Case B: needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3925476, 37.7931482` (measured OBB centre, see 2.3) |
| Target height | **29.57 m** to the lift/stair bulkhead crest; **parapet 27.4 m (measured)**; roof deck 26.82 m (LiDAR median) |
| Footprint | 13.75 m (street frontages, bearing 134.95°/314.95°) x 42.95 m (depth, bearing 44.95°/224.95°); 590.6 m2, measured |
| Triangle cap | 14,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 132 The Embarcadero GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 132 The Embarcadero (the Jewish Community
Federation Building, also addressed 121 Steuart Street) in San Francisco and deliver
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
7. `artifacts/524-second/` — the closest brick reference implementation: same
   `Toy_brick` body, same party-wall problem, and a build script whose footprint,
   bay, opening, band and parapet helpers this asset should reuse rather than
   reinvent
8. `artifacts/300-brannan/` and `artifacts/501-second/` — the two precedents for a
   MULTI-STOREY block with a designed crown and a roof bulkhead that sets the
   bounding-box top; check their triangle split before designing the window rhythm
9. `docs/asset-plans/132-embarcadero.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## What is already observed, and what is not

The dossier in Part 2 is unusually strong on geometry and height and unusually weak
on the roof. Specifically:

- **Observed** (Street View, both frontages, February 2025 and August 2024 imagery):
  the Embarcadero elevation in full, the Steuart elevation in full, the entrance,
  the storefront base, the six-bay window grid, the crown band, and the parapet line.
- **Measured** (photogrammetry from a levelled panorama, 40 samples across the
  frontage, sigma 0.08 m): the parapet at **27.4 m ± 0.4**, and every window head
  and sill on the Embarcadero elevation (2.4).
- **NOT observed**: the roof. No aerial source available to this plan resolves it —
  Google's z22 tiles lean far enough at 27 m that the roof cannot be attributed to
  the footprint with confidence, and Esri's z20 is worse. The 29.57 m LiDAR maximum
  is read here as a lift/stair bulkhead (2.9), and that reading is an **inference**.
  Resolve it before you commit to the roof layout — see 2.15 risk 1.

## Must capture

- A **narrow deep slab**: 13.75 m of street frontage, 42.95 m deep, seven storeys,
  parapet at a measured 27.4 m. It is one storey taller than both party-wall
  neighbours and it must read that way. Do not widen it toward a comfortable
  proportion — the 1:3.1 frontage-to-depth ratio *is* the building
- **Red brick.** It is the only brick in its stretch of the row: cream and glass to
  the northwest (110–116 The Embarcadero), a darker painted block to the southeast
  (Steuart Place). At city scale the colour is the first recognition cue
- The **deep pale crown band** under a dark coping, running the full width of both
  frontages at roughly 24.4–26.9 m — the one strong horizontal on an otherwise even
  facade, and the thing that stops the model reading as a plain brick box
- The **six-bay punched-window grid**: six wide horizontal windows per floor on both
  frontages, floors 3–7, on a regular 2.29 m bay
- The **Embarcadero base**: a brick storefront band with three blue-grey glazed bays,
  a brick spandrel course with small wall lights at ~3.4 m, and a **full-width
  second-floor glazed ribbon** at 4.4–6.1 m. This is the only place the building
  opens up, and it is where the night glow belongs
- The **Steuart entrance**: a deeply recessed bay under a projecting brick lintel,
  with `JEWISH COMMUNITY FEDERATION` incised in metal letters across the brick and
  `121` beside the doors, flanked by two blue-grey steel service doors, planters,
  and a row of steel bollards along the kerb. The second floor on this side is
  **blind brick** — no ribbon
- Both **party walls**, as plain brick. The southeast wall is fully concealed by
  Steuart Place; the northwest wall is exposed above roughly 18 m and is visible
  from the aerial camera

## Research 132 The Embarcadero independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- Both frontages. A model built from the Embarcadero photograph alone will have an
  invented institutional entrance
- **Aerial and roof views** — this is the weak axis. The bulkhead, the mechanical
  plant, the cellular antenna platform (DBI records an AT&T array and a 2024 DISH
  installation with a roof equipment platform), and whether the roof steps
- Ground-level views, day and night
- Whether the northwest neighbour at 110–116 The Embarcadero has been rebuilt since
  the 2010 LiDAR — the Assessor still says three storeys and 10.5 m, the current
  Street View shows a glass building of roughly 18 m, and this changes how much of
  our northwest party wall is exposed (2.4)

Prefer architect/engineer publications, owner or institutional material, planning
and permitting documents, architectural press, geolocated photography, and
aerial/satellite imagery. Never rely on a single photograph, a single AI-generated
image, or a single unsourced 3D model. Separate verified facts from visual
inference; if sources disagree, document the disagreement and decide.

**Three source conflicts are already resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:** OpenStreetMap places the Angler restaurant
node (which carries `addr:housenumber=132`) inside a *different* building two lots
southeast, and OSM is wrong — every DBI permit filed at 132 The Embarcadero since
2014 carries block 3715 **lot 003**, which is this building, and the EAS address
point falls inside its Embarcadero frontage; SKYDB says six floors while the
Assessor and every permit say **seven**, and seven is right (the count is confirmed
window row by window row in 2.4); and the DataSF LiDAR **maximum** of 29.57 m is
2.75 m above the median roof deck and is NOT the parapet — the parapet is measured
independently at 27.4 m (2.9).

## Create a reference dossier

Write `artifacts/132-embarcadero/REFERENCE.md` containing: source links and what
each establishes; verified dimensions and location; orientation; observations from
both frontages, both party walls and above; the 3-5 strongest recognition cues;
features to preserve; features to simplify; uncertainties and conflicting evidence.
A contact sheet of attributed reference thumbnails is welcome if legally
permissible — do not commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade into
broad rhythms, deliberately design every surface visible from above, evaluate from
the app's high three-quarter aerial camera, then simplify again.

This is a **secondary-tier** building in the style bible's hierarchy (§21) — a good
neighbour, not a hero. Spend the detail on the three things that carry it: the
**crown band**, the **six-bay rhythm**, and the **Embarcadero glazed ribbon**. Spend
nothing on the window frames, the brick coursing, the incised lettering's letterforms
(a single readable strip is enough), the bollards individually, or the storefront
mullions. At city scale they are sub-pixel and they will eat the budget the crown
needs.

Because the roof is 43 m long and 13.75 m wide and the camera looks down on it, the
roof is the largest single surface in this asset. Design it: deck, parapet return,
bulkhead, a small number of mechanical blocks, and the antenna platform read as one
clean composition rather than scattered boxes.

The finished asset must be immediately recognizable as 132 The Embarcadero,
consistent with the real building from both frontages and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel art,
not generic low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1984 building: both frontages, both party walls, the crown band,
the parapet, the roof and its bulkhead and plant.

Do not include unrelated surrounding city geometry: the Embarcadero, Steuart Street,
the neighbours at 110–116 The Embarcadero and 131 Steuart Street (Steuart Place),
the Embarcadero promenade, the F-line tracks, street trees, the sidewalk, bollards
standing free of the building, parked cars, people, plinths, cameras or lights.
Temporary context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project
palette; `_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no
cameras, lights, animations, armatures or constraints; no external dependencies; at
most 14,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The Embarcadero
front faces **northeast, bearing 44.95°**; the Steuart front faces **southwest,
224.95°**; the party wall to Steuart Place faces **southeast, 134.95°**; the party
wall to 110–116 The Embarcadero faces **northwest, 314.95°**. The building is
rotated about 45° off the world axes, so build directly on the measured footprint
rectangle in 2.3 rather than modelling an axis-aligned box and rotating it.

**Height normalization:** the tallest geometry in the export (the roof bulkhead) must
land at exactly **29.57 m** so the loader's `targetHeightM / measuredHeight` scale is
1.0. The parapet must land at 27.4 m — it, not the bulkhead, carries the silhouette,
so verify it in the render rather than only checking the bounding box.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/132-embarcadero/build_132_embarcadero.py` (deterministic build
script), `artifacts/132-embarcadero/132-embarcadero.blend`, and
`artifacts/132-embarcadero/132-embarcadero.glb`. The script must rebuild the model
reliably enough for future revision. Do not modify or rename an unrelated existing
GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`132-embarcadero-top.png`, `132-embarcadero-north.png`, `132-embarcadero-east.png`,
`132-embarcadero-south.png`, `132-embarcadero-west.png`, plus
`132-embarcadero-contact-sheet.png`, at least one high three-quarter aerial beauty
render `132-embarcadero-aerial.png`, and a night render
`132-embarcadero-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection;
use orthographic or long-lens cameras; label directions from the researched
orientation; the top view must clearly show the full 13.75 x 42.95 m roof — its
bulkhead, mechanical layout and antenna platform; the aerial view uses the style
bible's camera assumptions (30–50 degrees down, long lens). Simple tabletop lighting,
neutral warm background, minimal depth of field, and every image must depict the same
exported model.

Because the building is rotated 45° from the world axes, the four compass renders
will each show two faces at 45°. That is correct and expected — do not rotate the
model to make the elevations square on.

## Validate the exported GLB

Re-import `132-embarcadero.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Render at least one review image from the re-imported asset. Write
`artifacts/132-embarcadero/validation.json` and `artifacts/132-embarcadero/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **40 x 40 m** even though
the building is 13.75 x 42.95 m — that is the expected consequence of a 45°
real-world heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "132-embarcadero",
  "file": "132-embarcadero.glb",
  "anchor": [
    -122.3925476,
    37.7931482
  ],
  "targetHeightM": 29.57,
  "cat": 3,
  "name": "132 The Embarcadero (Jewish Community Federation Building)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/132-embarcadero.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* are visual
or derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

**A note on the evidence quality of this dossier.** Geometry and height are strong:
the footprint is corroborated by three independent surveys (OSM trace 590.6 m2,
DataSF LiDAR footprint 617 m2, Assessor floor area implying 585 m2/floor), and the
parapet height comes from a photogrammetric solve with 40 samples and a 0.08 m
standard deviation that agrees with the LiDAR roof-deck median to 0.6 m. The
identification is strong: 12 DBI permits, the EAS address point, the Assessor's roll
and the building's own incised lettering all agree. **The roof is the weak axis and
the only real gap** — no usable orthophoto was obtained, and the 29.57 m LiDAR
maximum is interpreted rather than observed. See 2.15.

### 2.1 Verified facts

| Fact | Value | Source | Confidence |
|---|---|---|---|
| Name | Jewish Community Federation Building | incised lettering on the Steuart elevation, observed | verified |
| Addresses | 132 The Embarcadero (waterfront frontage); 121 Steuart Street (institutional entrance) | DataSF EAS; Assessor roll; DBI permits | verified |
| Assessor parcel | block 3715, lot 003 (`3715003`, MBLR `SF3715003`) | DataSF parcels `acdm-wktn`; Assessor roll `wv5m-vpq2` | verified |
| Year built | 1984 | Assessor roll; DBI permit 1982-03-02 "bldg use: offices" on lots 003/004 | verified |
| Storeys | 7 | Assessor roll; 10 of 12 DBI permits at 132 The Embarcadero; counted window row by row in 2.4 | verified |
| Floor area | 44,107 sq ft (4,097 m2) → 585 m2/floor over 7 floors | Assessor roll | verified |
| Use | Commercial Office; ground and second floor food/beverage on the Embarcadero side | Assessor roll; DBI permits | verified |
| Occupant | Jewish Community Federation and Endowment Fund of San Francisco (main office) | jewishfed.org contact page; "Koret boardroom" in DBI permit 2019-11-08 | verified |
| OSM building | way `193054135` — `building=office`, `building:levels=7`, `roof:shape=flat`, unnamed | OSM API | verified |
| DataSF footprint | `201006.0005323`, MBLR `SF3715003` | DataSF `ynuv-fyni` | verified |
| Footprint (OBB) | 13.75 m x 42.95 m, 590.6 m2 | min-area OBB of OSM way 193054135 | measured |
| Anchor (OBB centre) | −122.3925476, 37.7931482 | derived, 2.3 | measured |
| Long-axis bearing | 44.95° / 224.95° (depth); frontages 134.95° / 314.95° | derived from the OBB | measured |
| Roof deck | 26.82 m (LiDAR median), mode 26.68, mean 26.38, sigma 3.85, ground 3.46 m NAVD88 | DataSF `ynuv-fyni` | verified |
| **Parapet crest** | **27.4 m ± 0.4** | photogrammetry, 2.9 | measured |
| LiDAR maximum | 29.57 m | DataSF `ynuv-fyni` `hgt_maxcm` | verified (interpretation *inferred*) |
| Facade | red brick, six-bay punched-window grid, deep pale crown band under a dark coping | Street View, observed | verified |
| Party walls | both long sides — 110–116 The Embarcadero (NW), Steuart Place / 131 Steuart (SE) | OSM + DataSF footprint adjacency; observed | verified |

**Two identification conflicts, both resolved.**

1. **OpenStreetMap puts the Angler restaurant in the wrong building.** OSM node
   `2840137601` (`name=Angler`, `addr:housenumber=132`, `addr:street=The Embarcadero`)
   falls inside way `193054137` — two lots southeast, on parcel 3715-025 (141 Steuart
   Street). It is a misplaced POI. Everything else points at lot 003: the DataSF EAS
   address point for `132 THE EMBARCADERO` (−122.3924234, 37.7932441) falls inside
   this footprint near its Embarcadero frontage; all 12 DBI permits filed at
   132 The Embarcadero carry block 3715, and 10 of them carry lot 003 (the two that
   carry lot 004 are from 1982 and 2000, before lots 004 and 005 merged into 025);
   and the permits describe exactly this building's history — a `food/beverage
   hndlng` tenant on the ground floor since at least 2000, an awning dismantled in
   2017, the Angler wall sign in 2018, and a pergola filed in January 2026. Do not
   "correct" the plan back toward the OSM node.
2. **SKYDB says six floors.** The Assessor says seven, ten DBI permits say seven, and
   the Embarcadero elevation shows six window rows above a storefront base (2.4).
   Seven.

### 2.2 Sources

| Source | What it establishes |
|---|---|
| DataSF Addresses (`ramy-di5m`) | the EAS point for `132 THE EMBARCADERO`; the neighbouring `100 THE EMBARCADERO` = The Audiffred Building |
| DataSF Parcels (`acdm-wktn`) | block 3715 lot geometry; lot 003 = 121 Steuart; lot 025 = 131–141 Steuart |
| DataSF Assessor secured roll (`wv5m-vpq2`) | 1984, 7 storeys, 44,107 sq ft, Commercial Office; the whole block's ownership pattern |
| DataSF Building Permits (`i98e-djp9`) | 12 permits at 132 The Embarcadero; the lot-003 attribution; roof antennas (AT&T 2016/2018/2021, DISH 2024 with a roof equipment platform); lift machine rooms and hoistways; the 2026 pergola |
| DataSF Building Footprints (`ynuv-fyni`) | LiDAR footprint `201006.0005323`, MBLR SF3715003; the height distribution in 2.9; and the same for all six neighbours in 2.4 |
| OpenStreetMap API + Overpass | way `193054135` geometry and tags; the full block; the Angler node error |
| Google Street View (`streetviewpixels-pa`, panoramas `OLku-hi1dEEvbjsiBr8EWw`, `yo5P5pi5QKGaa2I7JTPGvQ`, `35oWNxHtxVyAvhUceWPuVA`, `CZDneEIDtQW66UdbfLSsgw`) | both elevations, the entrance, the base, the crown; the photogrammetric solve in 2.9 |
| Exa search — saisonhospitality.com, hoodline.com, michelin.com, en.wikipedia.org (Angler) | the restaurant tenancy history: Chaya Brasserie → Angler (2018), designed by Arcanum Architecture; *observed (press)* |
| Exa search — jewishfed.org, causeiq.com, bizprofile.net, skydb.net | the occupant; SKYDB's incorrect floor count |

Photographs are referenced by URL and description, not committed. Exa returned **no
architectural publication for the 1984 building** — no architect is attributed
anywhere reachable; that is an open question, not an omission (2.15 risk 3).

### 2.3 Orientation and placement

Local tangent projection (`AGENTS.md`): `x=(lon+122.4375)·111320·cos 37.77°`,
`z=−(lat−37.77)·110540`.

The four lots on this half-block are narrow and deep: each takes about 14 m of the
Embarcadero frontage and runs the full 43 m block depth through to Steuart Street.
Ours is the third from Mission Street.

Minimum-area oriented bounding box of OSM way `193054135`:

| | |
|---|---|
| Frontage extent | **13.75 m**, along bearing 134.95° (the Embarcadero / Steuart street line) |
| Depth extent | **42.95 m**, along bearing 44.95° |
| OBB centre | x 3955.62, z −2558.80 → **−122.3925476, 37.7931482** |
| Ring area | 590.6 m2 (OSM), 617 m2 (DataSF LiDAR), 585 m2 (Assessor floor area / 7) |

**Face bearings** (outward normals, true):

| Face | Bearing | What is there |
|---|---|---|
| Northeast | **44.95°** | The Embarcadero. 13.75 m. The address, the storefront, the glazed ribbon |
| Southwest | **224.95°** | Steuart Street. 13.75 m. The institutional entrance |
| Southeast | **134.95°** | party wall with Steuart Place (131 Steuart). Concealed |
| Northwest | **314.95°** | party wall with 110–116 The Embarcadero. Exposed above ~18 m |

**Why the OBB centre and not a ring centroid.** The OSM ring carries two sub-metre
jogs at its Embarcadero end, which pull a vertex mean 6.8 m off the true rectangle
centre; the DataSF LiDAR ring's area centroid sits 1.42 m from the OBB centre and
the OSM ring's sits 0.17 m from it. The OBB centre is the point the model actually
centres on, and it is within 1.5 m of both surveys.

**Distance check.** The Embarcadero frontage sits 16.5 m from the Embarcadero
centreline and 54.5 m from the Steuart centreline; the Steuart frontage sits 11.7 m
from the Steuart centreline. Both elevations are on the back of a sidewalk, not set
back.

### 2.4 What each side shows

**Northeast — The Embarcadero (13.75 m, the address).** Bottom to top, with heights
measured photogrammetrically (2.9):

| Element | Height | Notes |
|---|---|---|
| Storefront base | 0 → ~3.4 m | brick piers with three blue-grey framed glazed bays; a poster/exhibit panel in the middle bay |
| Brick spandrel course | ~3.4 m | a projecting brick band carrying three small square wall lights |
| **Second-floor glazed ribbon** | **4.37 → 6.11 m** | a full-width horizontal window band, deeply reveal-set — the only continuous glazing on the building |
| Floor 3 windows | 7.45 → 9.10 m | six bays |
| Floor 4 windows | 10.70 → 12.60 m | six bays |
| Floor 5 windows | 14.37 → 16.00 m | six bays |
| Floor 6 windows | 17.87 → 19.45 m | six bays |
| Floor 7 windows | 21.37 → 22.93 m | six bays |
| Brick above | 22.93 → ~24.4 m | plain |
| **Pale crown band** | ~24.4 → ~26.9 m | a deep light-cream/grey band, full width; the strongest horizontal on the building |
| Coping | ~26.9 → 27.4 m | dark, thin, projecting slightly |

Sill-to-sill spacing runs 3.08, 3.25, 3.67, 3.50, 3.50 m — mean floor-to-floor
**3.40 m**. Windows are wide horizontals, roughly 1.55–1.6 m tall, in light metal
frames set in plain brick reveals, six per floor on a **2.29 m bay**.

**Southwest — Steuart Street (13.75 m, the front door).** The same brick, the same
six-bay grid, the same crown band and coping — but a completely different base:

- A **deeply recessed entrance bay** roughly in the middle of the frontage, under a
  projecting brick lintel with a soldier course.
- **`JEWISH COMMUNITY FEDERATION`** in incised metal letters across the brick above
  the recess, and **`121`** to the right of the doors.
- Aluminium-framed glass entrance doors, flanked left and right by **blue-grey steel
  service doors**, with planters either side of the entrance.
- A continuous row of **steel security bollards** along the kerb — a real and visible
  characteristic of this building, and worth one simplified row in the miniature.
- **The second floor is blind brick on this side** — no ribbon. The ground floor
  reads as a double-height lobby: plain brick from the entrance lintel up to the
  floor-3 window row.

**Southeast — party wall with Steuart Place (131 Steuart Street).** Concealed. The
neighbour's LiDAR mode is 24.99 m and its maximum 27.77 m, so it reaches within
about 2.4 m of our deck and this wall is effectively invisible from any angle,
including the aerial camera. Model it plain.

**Northwest — party wall with 110–116 The Embarcadero.** Partly exposed, and the
size of the exposure is uncertain. The Assessor says lot 002 is three storeys, and
its 2010 LiDAR mode is 10.47 m — which would leave 17 m of our brick wall bare. But
current Street View shows a glass-clad building there of roughly 18 m, and the same
LiDAR record carries a 24.43 m maximum which is edge bleed from *our* wall. The
honest reading is **that the neighbour was rebuilt or reclad after 2010 and now
stands at roughly 18 m, leaving the top ~9 m of our northwest wall exposed.**
Verify this at stage 2 — from the aerial camera it decides how much plain brick the
model shows on that side (2.15 risk 2).

**Above.** Not observed. See 2.9 and 2.15 risk 1.

### 2.5 Recognition cues (ranked)

1. **Red brick between cream/glass and a darker block.** From the aerial camera this
   is the whole identification: a single warm-red 43 m slab in a row of pale ones.
2. **The narrow deep slab proportion** — 13.75 m wide, 42.95 m deep, pointed at the
   bay, one storey above both neighbours.
3. **The deep pale crown band** under a dark coping, wrapping both frontages.
4. **The six-bay punched-window grid**, even and regular on both fronts.
5. **The Embarcadero glazed ribbon** at the second floor — the one horizontal cut in
   the brick, and the night hero.

### 2.6 Miniature translation

- Brick reads as one flat `Toy_brick` field. No coursing, no relief, no colour
  variation. The building earns its identity from *being* brick next to *not* brick.
- Windows become plain recessed `Toy_glass` panes in `Toy_trim` reveals, one box per
  opening. Thirty on each frontage. No mullions, no frames beyond the reveal.
- The crown band is the one place to spend geometry: give it a real 0.15 m
  projection, a chamfered underside, and a distinct `Toy_trim` colour so it holds at
  thumbnail size.
- The Steuart lettering becomes **one `Toy_gold` strip** 0.5 m tall across the
  entrance lintel — semantic scale per the style bible §26, not legible letterforms.
- The bollards become one row of eight short `Toy_steel` cylinders, or a single
  chamfered plinth strip if the triangle budget tightens. They are the only thing
  that says "institution" at street level.
- The roof gets a real composition (2.9), not scattered boxes.
- Both party walls are flat brick planes with a single subtle bevel at the parapet.

### 2.7 Massing recipe

All heights are metres above the base plane at z = 0. Build directly on the OBB
rectangle (13.75 x 42.95 m, long axis 44.95°); do not model axis-aligned and rotate.

1. **Body**: extrude the 2.3 rectangle from z = 0 to z = 26.82 in `Toy_brick`; the
   top cap is the roof deck (`Toy_roofd`).
2. **Parapet**: a ring on the footprint, z = 26.82 → 27.40, 0.40 m thick,
   `Toy_brick` with a `Toy_ink` coping in the top 0.12 m.
3. **Crown band**: a `Toy_trim` band on both frontages **and returned 1.0 m onto both
   party walls**, z = 24.40 → 26.90, projecting 0.15 m, with a chamfered underside.
4. **Window grid**, both frontages: six bays at 2.29 m centres, openings 1.50 m wide
   x 1.58 m tall, recessed 0.22 m — `Toy_roofd` reveal, `Toy_glass` pane, `Toy_trim`
   sill 0.08 m proud. Rows at the sills listed in 2.4 (7.45, 10.70, 14.37, 17.87,
   21.37).
5. **Embarcadero glazed ribbon**: a single continuous recess z = 4.37 → 6.11 across
   the full 13.75 m, 0.28 m deep, `Toy_glassl` pane in a `Toy_trim` frame.
6. **Embarcadero base**: three glazed bays z = 0.30 → 3.10 in `Toy_glassl` with
   `Toy_navy` frames, separated by 0.9 m `Toy_brick` piers; a `Toy_brick` spandrel
   course z = 3.10 → 3.55 projecting 0.10 m, carrying three 0.25 m `Toy_trim_Glow`
   wall-light squares.
7. **Steuart entrance**: a recess 5.6 m wide x 4.4 m tall, 1.1 m deep, `Toy_ink`
   walls, with a `Toy_glassl` door plane at its back; a projecting `Toy_brick`
   lintel z = 4.40 → 4.90 out 0.25 m; a `Toy_gold` lettering strip z = 5.05 → 5.55
   across it. Two `Toy_navy` service doors 1.2 x 2.4 m flanking, and two `Toy_trim`
   planter boxes.
8. **Steuart blind second floor**: no openings between z = 4.90 and the floor-3 sill
   at 7.45 — plain `Toy_brick`. This asymmetry against the Embarcadero side is
   deliberate and must survive simplification.
9. **Bollards**: eight `Toy_steel` cylinders, 0.25 m diameter x 0.95 m, on a 1.5 m
   pitch along the Steuart frontage, 1.6 m out from the wall.
10. **Roof bulkhead**: 5.5 x 4.0 m in `Toy_slate` from z = 26.82 to **z = 29.57**,
    with a `Toy_trim` cap — this sets the bounding-box top and must land exactly on
    29.57. Place it toward the Steuart (southwest) third of the roof, over the lift
    core (2.9), set back at least 3 m from both frontages so it stays hidden behind
    the parapet from the street.
11. **Roof plant**: three `Toy_steel` blocks (max 1.5 m tall), two `Toy_roofd` vents,
    and one 4.0 x 2.0 x 0.4 m `Toy_steel` antenna platform with three 1.8 m
    `Toy_steel` masts — the DISH/AT&T array the permits record.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Where |
|---|---|---|
| `Toy_brick` | `#c96f4a` | the whole body, piers, spandrel course, parapet, both party walls, the entrance lintel — **the identity colour** |
| `Toy_trim` | `#f3efe6` | the crown band, window sills and reveal frames, the bulkhead cap, planters |
| `Toy_roofd` | `#45454a` | window reveals, roof deck, roof vents |
| `Toy_ink` | `#3a3530` | the parapet coping and the recessed Steuart entrance |
| `Toy_glass` | `#2a4d73` | all floor 3–7 windows |
| `Toy_glassl` | `#6f95b8` | the second-floor ribbon, the Embarcadero storefront, the entrance doors |
| `Toy_navy` | `#2f4763` | storefront and service-door frames — the observed blue-grey joinery |
| `Toy_slate` | `#6f7883` | the roof bulkhead walls |
| `Toy_steel` | `#9aa0a6` | bollards, roof plant, antenna platform and masts |
| `Toy_gold` | `#caa64a` | the Steuart lettering strip |
| `Toy_glassl_Glow` | `#6f95b8` | the second-floor ribbon and the Embarcadero storefront at night |
| `Toy_glass_Glow` | `#6f95b8` | lit upper windows at night |
| `Toy_trim_Glow` | `#f3efe6` | the three storefront wall lights |
| `Toy_gold_Glow` | `#caa64a` | the Steuart lettering strip at night — the entrance beacon |

**On the brick colour.** Sampled from sunlit Street View the wall reads about
`#c39373` in full sun and `#8a5f3f` in shade — browner than `Toy_brick`'s `#c96f4a`
and close to `Toy_rust`'s `#a86444`. `Toy_brick` is chosen anyway, for the same
reason 524 Second, 2 South Park and 168 South Park chose it: this building's whole
job in the row is *to be the red one*, and the family colour is what makes that read
from the aerial camera. If the day render shows it fighting the Audiffred two lots
northwest, `Toy_rust` is the fallback — record the swap in REPORT.md.

**Night composition.** One hero and two supports, per the style bible: the hero is
the **second-floor glazed ribbon plus storefront on the Embarcadero** — a continuous
bright horizontal at the waterfront, which is what the building actually does after
dark; the supports are the **`Toy_gold_Glow` lettering strip** on the Steuart
entrance and a **scattered subset (about a third) of the upper windows**. The crown
band does not glow. Keep the glow shells open-faced, not closed boxes — a closed
`_Glow` shell reads at roughly 23% by day and will tint the brick.

### 2.9 Top surface, and how the heights were established

**The measurement.** Google Street View panorama `OLku-hi1dEEvbjsiBr8EWw` sits at
−122.3922925, 37.7934067 — 15.2 m from the Embarcadero frontage, 17° off its normal.
Detecting the sky/building boundary column by column and intersecting each ray with
the measured facade plane gives the parapet crest at 40 sample points spanning
s = 0.3 → 13.9 m along the 13.22 m frontage, with a **standard deviation of 0.08 m**:
the parapet is dead level. Calibrating the camera height against the facade's base
line in a second, pitched-down view of the same panorama brackets it at 1.9–2.5 m,
which is the dominant residual, so the parapet is quoted as **27.4 m ± 0.4**.

**The LiDAR, read against it.** DataSF's 2010 return statistics for this footprint
are median 26.82 m, mode 26.68 m, mean 26.38 m, sigma 3.85 m, minimum 0.20 m,
maximum **29.57 m**. Mean below median with a 0.20 m minimum is the signature of
edge bleed — the 50 cm raster mask covers 625 m2 against a 617 m2 ring, so its rim
cells catch the sidewalk. That accounts for the low tail and the large sigma, and it
means **26.8 m is the roof deck** and the maximum is real geometry on our own roof
(both neighbours are lower: 24.99 m and 10.47 m by mode).

**What the 29.57 m is.** *Inferred.* The building is a 1984 seven-storey office with
traction lifts — DBI records "machine room & hoist ways" (2020-12-11) and
"neighboring building elevator machine rooms" (2021-03-15). A lift/stair bulkhead
2.75 m above the deck is exactly what that produces, and it is invisible from both
frontages because the sight line to the parapet is 60° at 15 m. That reading is
adopted here and drives `targetHeightM`. It is not observed. See 2.15 risk 1.

**What else is up there.** Cellular plant, documented rather than seen: AT&T antenna
swaps in 2016, 2018 and 2021, and a 2024 DISH permit for three antennas plus a roof
equipment platform. One simplified platform with three short masts is both accurate
and good miniature practice.

**The deck itself.** 13.75 x 42.95 m, flat, `Toy_roofd`, with the parapet returning
0.58 m above it. This is the single largest surface in the asset and the camera looks
straight down on it — the bulkhead, the plant blocks and the antenna platform should
be composed as one group toward the Steuart third, leaving the Embarcadero end of the
deck clean so the crown band reads uninterrupted from the water.

### 2.10 Scope

**In:** the 1984 building — both frontages, both party walls, the crown band, the
parapet, the roof deck, the bulkhead, the roof plant and antenna platform, the
Steuart entrance recess and its lettering strip, the bollard row.

**Out:** the Embarcadero roadway and promenade, the F-line tracks and overhead,
Steuart Street, both neighbours, street trees, sidewalk, traffic signals, the
Angler pergola and any restaurant furniture on the neighbouring lot, parked cars,
people, plinths, cameras, lights.

### 2.11 Triangle budget

| Element | Budget |
|---|---|
| Body, party walls, roof deck | 400 |
| Parapet ring + coping | 900 |
| Crown band with returns and chamfer | 1,200 |
| 60 punched windows (30 per frontage) | 5,400 |
| Second-floor ribbon | 400 |
| Embarcadero base: bays, piers, spandrel, wall lights | 1,400 |
| Steuart entrance: recess, lintel, doors, lettering, planters | 1,500 |
| Bollards (8) | 800 |
| Roof bulkhead + cap | 300 |
| Roof plant, vents, antenna platform and masts | 1,200 |
| Bevels and slack | 500 |
| **Total** | **~14,000** |

### 2.12 Draft manifest entry

```json
{
  "id": "132-embarcadero",
  "file": "132-embarcadero.glb",
  "anchor": [
    -122.3925476,
    37.7931482
  ],
  "targetHeightM": 29.57,
  "cat": 3,
  "name": "132 The Embarcadero (Jewish Community Federation Building)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`loadRadius` follows the default rule in `AGENTS.md`: `max(2500, 29.57 × 30)` =
**2500**. This is not an `alwaysLoaded` skyline piece.

### 2.13 Integration notes (for later, not this task)

**This is Case B** — there is no procedural builder with a matching id in
`pipeline/lib/landmarks.mjs` or `app/src/landmarks.js`. Integration therefore needs a
registry entry, an exclusion radius, and a tile re-bake, per
`docs/asset-plans/INTEGRATION-PROMPT.md`.

**Exclusion.** `excluded()` in `pipeline/buildings.mjs` drops a baked footprint when
its ring centroid **or any ring vertex** falls inside the radius. Measured from the
2.3 anchor against the actual bake input (DataSF footprints primary, Overture/OSM
gap-fill):

```
 0.17 m  this building's own OSM/Overture way 193054135, via centroid
 1.42 m  this building's own DataSF footprint SF3715003, via centroid
         -> the FLOOR: below this the procedural twin survives
13.74 m  OSM way 256969674 (110-116 The Embarcadero), centroid
         -> the CEILING, and the binding constraint
13.92 m  OSM way 193054132 (Steuart Place, 131 Steuart), centroid
14.13 m  DataSF SF3715002 (110-116 The Embarcadero), centroid
14.62 m  DataSF SF3715025 (Steuart Place), centroid
20.70 m  DataSF SF3715002, nearest ring vertex
20.70 m  this building's own DataSF footprint, nearest ring vertex
21.17 m  DataSF SF3715025, nearest ring vertex
21.46 m  OSM way 256969674, nearest ring vertex
27.69 m  OSM way 193054136 (The Audiffred Building), centroid
```

Safe window **(1.42, 13.74) m**. **`exclude: 7`** sits near the middle with 5.58 m of
margin below and 6.74 m above.

Note what this table says about vertices: this building's own nearest ring vertex is
20.70 m out and both party-wall neighbours' nearest vertices are 20.70 and 21.17 m
out — **the vertex test is unusable here**, because a party-wall row shares its
corners and no radius can catch ours without catching theirs. The centroid test is
the only lever, which is normal for a 7 m circle around the middle of a 14 x 43 m
building but means the radius must stay well under 13.74 m. Do not "round up for
safety": 14 would delete 110–116 The Embarcadero from the bake and leave a hole
against our northwest party wall.

**Registry entry** for `pipeline/lib/landmarks.mjs`:

```js
{
  id: '132Embarcadero',
  name: '132 The Embarcadero',
  lon: -122.3925476,
  lat: 37.7931482,
  height: 29.57,
  exclude: 7,
  // camera.js apply() puts the eye at pivot + (sin yaw, sin pitch, cos yaw)*distance
  // with +z south, so camera.yaw = 180 - the true bearing you want to look down.
  // This building wants the Embarcadero elevation, outward normal 44.95 deg true,
  // so 180 - 45 = 135. yaw 45 would stare at the Steuart entrance instead — which
  // is the better-looking elevation but not the address. Verify from a rendered
  // frame, not from the arithmetic.
  camera: { distance: 240, yaw: 135, pitch: 26 },
},
```

**Batch mode.** Other landmarks are in flight on this block. If `BATCH: yes`, run the
bake and the full QA on it, then `git checkout -- app/public/tiles api/_data` before
committing, and commit source only — see `docs/asset-pipeline/ADDRESS-TO-ASSET.md`
"Batch mode" and `docs/asset-pipeline/BATCH-INTEGRATE.md`.

**Collision warning.** A parallel branch `pipeline/121-steuart` exists. **121 Steuart
Street and 132 The Embarcadero are the same building** — this parcel, 3715-003.
Whichever session reaches integration first should claim the id; the other must be
retired rather than merged, or the manifest will carry the same GLB twice at the same
anchor and the shared landmark `BatchedMesh` will pay for it twice.

### 2.14 Validation checklist

- [ ] Re-import into a fresh Blender scene; validate the re-import, not the source
- [ ] Bounding-box top exactly **29.57 m**; minimum Z ~ 0; origin at base centre in XY
- [ ] Parapet lands at 27.40 m and roof deck at 26.82 m in the re-imported model
- [ ] Axis-aligned XY bbox ≈ 40 x 40 m (a 45° heading, not a scale error)
- [ ] Footprint measures 13.75 x 42.95 m along bearings 134.95° / 44.95°
- [ ] ≤ 14,000 triangles; ≤ 500 KB compressed
- [ ] Materials all `Toy_*`, flat colour, no textures, no transparency, no `Toy_body`
- [ ] `_Glow` only on the ribbon, storefront, wall lights, lettering strip and the lit
      window subset; glow shells open-faced
- [ ] Normals outward — per-object signed volume for the union of solids, ray test
      ≤ 0.15% residual
- [ ] No cameras, lights, animations, armatures, constraints, or foreign geometry
- [ ] Day and night aerials rendered from the high three-quarter camera; the brick
      reads red against its neighbours and the crown band reads at thumbnail size

### 2.15 Open questions and risks

1. **The roof is inferred, not observed — the one real gap.** No orthophoto obtained
   for this plan resolves a 27 m roof at this latitude: Google's z22 tiles lean far
   enough that the roof cannot be attributed to the footprint, and Esri's z20 is
   worse. The 29.57 m LiDAR maximum is read as a lift/stair bulkhead on the strength
   of the building's traction lifts and the 2.75 m offset above the deck, and that
   reading sets `targetHeightM`. **Resolve it at stage 2** — an oblique aerial, a
   drone photograph, a rooftop-antenna site survey in the DISH permit file, or a view
   from a taller neighbour would all settle it. If the 29.57 m turns out to be an
   antenna mast rather than a bulkhead, drop `targetHeightM` to the parapet at
   **27.4 m** and put the plant below it. The parapet is measured independently, so
   this risk is contained to the roof: it cannot mis-scale the building.
2. **The northwest neighbour's height is unresolved**, and it decides how much plain
   brick party wall the model shows. The Assessor and the 2010 LiDAR say 110–116 The
   Embarcadero is three storeys / 10.5 m; current Street View shows a glass building
   of roughly 18 m. If it really is 10.5 m, 17 m of our brick flank is bare and needs
   deliberate design rather than a flat plane.
3. **No architect is attributed.** Exa found nothing — no architectural press, no
   Wikipedia or Wikidata entry, no owner history for the 1984 building. This is a
   working office block, not a published one. Do not invent an attribution; if the
   executing agent finds one, record it in REFERENCE.md.
4. **The crown band's exact depth is measured off a single panorama** at 24.4–26.9 m
   and is the least certain of the facade dimensions, because the top of the wall was
   in shadow when the imagery was captured. It is a 2.5 m band; if it turns out to be
   1.5 m the building loses its main horizontal, so check it against a second source.
5. **The number of window bays is six from photographs and never from a drawing.**
   Both frontages were counted independently and agree, but the Steuart elevation
   shows a stepped edge at its southeast end that may be a shallow setback rather
   than an oblique-view artefact — worth one more look before the bay module is
   fixed at 2.29 m.
6. **Angler.** The restaurant that carries this address in press and in OSM appears
   in photographs to occupy the *neighbouring* colonnaded ground floor to the
   southeast, while every permit at 132 The Embarcadero since 2000 describes a
   food/beverage tenant on **this** lot. Both can be true — restaurants routinely
   spill across a party wall — and it does not affect the massing. It does affect the
   name: the asset is named for the building, not the tenant.
