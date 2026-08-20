# 169 Steuart Street — Army & Navy YMCA Building — SF-SIM asset plan

The 1924 Army & Navy YMCA — today the **Embarcadero YMCA** (169 Steuart) and the
**Harbor Court Hotel** (161–165 Steuart) inside one building — filling a whole 42 x 42 m
block-through parcel between The Embarcadero and Steuart Street, three doors south of the
Audiffred Building. Clay brick and terra cotta over a rusticated cast-stone base, two
eight-storey wings around a light court, and a **ten-storey arcaded tower with a red clay
tile hipped roof** over the middle of the bay-facing wing. LiDAR crest **46.64 m**.

It is the only asset in the Embarcadero batch whose identity is a *roof*. Every other
building on this block — the Audiffred, 110 and 132 The Embarcadero, 121 and 131 Steuart —
is a flat-topped street wall, and the whole reason this one is legible from the app's
aerial camera is the red tile pyramid and the flagpole standing 18 m above its neighbours'
parapets. Get the tile roof right and the model is finished; get it wrong and this is a
brown box.

It is also a **one-parcel-many-addresses** case, settled at stage 0: DataSF condo lots
`3715028` (161/165 Steuart) and `3715029` (169 Steuart) share one `mapblklot` `3715028`,
one polygon and one physical building; OSM traces that building as **three** ways. The
asset is the whole parcel. See 2.3 and 2.13 — only one asset per parcel can own the
exclusion.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/169-steuart/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `169-steuart` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3919821, 37.7926993` |
| Target height | **46.64 m** to the tile-roof apex; tower eave / arcade parapet 35.0 m; eight-storey wing roof 28.1 m; Embarcadero crest parapet 30.9 m; Steuart street wall 14.0 m (estimated); flagpole tip 50.4 m (not the target) |
| Footprint | 42.35 x 41.84 m oriented bounding box; a 1,766.9 m2 pentagon (a 45°-rotated square with a 5.84 m chamfer at the east corner), measured |
| Triangle cap | 22,000 |
| Category | `7` (hotel) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 169 Steuart Street (Army & Navy YMCA) GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the Army & Navy YMCA Building (Embarcadero YMCA /
Harbor Court Hotel), 169 Steuart Street / 166 The Embarcadero, San Francisco, and deliver
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
7. `artifacts/501-second/` — the closest reference implementation in the set: a 1925
   multi-storey block on a ~45°-rotated footprint of comparable size, with a tripartite
   base/shaft/cornice composition and a roof crest above a level parapet. Reuse its
   footprint, bay, opening and cornice-ring helpers rather than reinventing them
8. `artifacts/300-brannan/` — the nearest precedent for RED BRICK over a light stone base
   with a raised crest; check its brick/stone colour split and its triangle allocation
   before designing the window rhythm
9. `docs/asset-plans/169-steuart.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The **red tile roof**, which is the whole identity. A hipped, steeply pitched clay-tile
  roof with a finial and a flagpole, crowning a tower that **tops the middle portion** of
  the bay-facing wing. Apex at **46.64 m**, eave at **35.0 m** — an 11.6 m rise. It is the
  only sloped roof and the only saturated red on this block; from the app's aerial camera
  it is what says "YMCA" while every neighbour says "parapet"
- Under it, the **arcaded tower storey**: a band of small round-headed openings running
  around the tower immediately below the eave. "Arcaded tower" is the phrase the historic
  survey uses; it is the second recognition cue and it must survive simplification
- **Two eight-storey wings** of clay brick at a **28.1 m** roof, separated by a light
  court, over a **podium that covers the full block-through footprint** — the survey is
  explicit that the building fills the block on its lowest floors and divides into wings
  above
- The **bay-facing (northeast) entry elevation** — the hallmark front. A two-storey
  rusticated **light cast-stone base** to ~10.5 m, capped by a **corbelled bracket
  frieze**; six storeys of brick above it; a **top storey of tall arched windows** with
  terra-cotta surrounds and a **balustraded balcony**; and a **decorative crest parapet at
  30.9 m** with brick diaper panels. Polychrome terra-cotta shields flank the arched entry
- The **Steuart Street (southwest) elevation at 169** — the address on the manifest. A
  **three-storey street wall only**, ~14 m: cream stucco with round-arched openings and
  projecting bay windows at the Harbor Court end (165), dark red-brown brick with recessed
  bay windows and the "Embarcadero YMCA" entrance at the YMCA end (169). The eight-storey
  mass sits well behind it — do not run the tall block out to Steuart Street
- **Colour contrast is half the read.** Red-brown brick body, pale cast-stone base and
  trim, terracotta-red tile roof, cream stucco on the Steuart front. Against the batch's
  grey and tan neighbours this must be the warm building

## Research the Army & Navy YMCA independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation,
and gather references covering:

- All four sides. Two are public streets (The Embarcadero, Steuart) and two are party
  edges; a model built from the Embarcadero photograph alone will have three invented walls
- Aerial and roof views — the tile roof's plan shape and size, the light court's size and
  position, and where the podium roof steps down toward Steuart Street. **These are the
  weakest numbers in this dossier (see 2.15) and the aerial is where you fix them**
- Ground-level views, day and night
- The storey heights: the two-storey stone base, the eight-storey wings, and how the
  "ten-storey" tower count is made up
- The architect attribution and the 2013–2018 facade restoration's scope

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**Three source conflicts are already known and resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:** the published height is **35 m** and the DataSF
LiDAR maximum is **46.64 m**, and both are right about different things (35 m is the
ten-storey tower's eave, 46.64 m is the tile-roof apex — see 2.1 and 2.15 risk 1); the
architect is credited to **Frederick H. Meyer** by NoeHill and the AIA lists but the
original plans held by the YMCA are **signed by Carl Werner**; and the completion date is
given as **1924** by the architects, the survey and SKYDB while Historic Hotels and the
hotel's own site say the building **opened in 1926** — 1924 built, 1926 opened is the
reading used here.

**Do not model 169 Steuart as a separate small building.** DataSF condo lots `3715028`
and `3715029` share one `mapblklot`, one polygon and one structure; OSM's three ways
(`32862485`, `193054138`, `193054131`) are one surveyed outline drawn in pieces. The
asset is the whole parcel. See 2.3.

## Create a reference dossier

Write `artifacts/169-steuart/REFERENCE.md` containing: source links and what each
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

This building sits in the style bible's secondary tier but its **roof is hero-tier work**
(§21). Spend the triangles on the **tile roof, the arcaded tower band, the crest parapet
and the two-storey stone base**. Spend nothing on the corbel brackets individually, the
terra-cotta shields' heraldry, the balcony balusters, the window muntins or the lobby —
at city scale they are sub-pixel and they will eat the budget the roof needs.

Semantic exaggeration is licensed and wanted on exactly two features (§7 of the style
bible): make the **tile roof's pitch and colour** slightly stronger than life, and make
the **stone base read distinctly lighter** than the brick. Everything else stays literal.

The finished asset must be immediately recognizable as the Embarcadero YMCA, consistent
with the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1924 building on parcel `3715028`: the Embarcadero and Steuart
elevations, both party edges, the podium, both eight-storey wings and their light court,
the tower with its arcade and tile roof, the flagpole, and the roof plant.

Do not include unrelated surrounding city geometry: The Embarcadero, Steuart Street, the
F-line tracks, the Hotel Griffon at 155 Steuart, 177 Steuart / 188 The Embarcadero, the
open yard on the northwest side, street trees, palms, the sidewalk, parked cars, people,
plinths, cameras or lights. Temporary context may appear in review renders but must not
leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project palette;
`_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no cameras, lights,
animations, armatures or constraints; no external dependencies; at most 22,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric`
in `app/src/assets.js` only scales and positions). The Embarcadero entry front faces
**northeast, bearing 45.1°**; the Steuart Street elevation (the 169 address) faces
**southwest, 225.1°**; the party edge to 177 Steuart faces **southeast, 134.9°**; the
party edge and yard to 155 Steuart face **northwest, 314.9°**. The building is rotated
about 45° off the world axes, so build directly on the measured footprint pentagon in 2.3
rather than modelling an axis-aligned box and rotating it.

**Height normalization:** the tallest geometry in the export must land at exactly
**46.64 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0. If you model
the flagpole, it is **decorative geometry that must NOT set the bounding box** — either
keep its tip at or below 46.64 m or drop it; a 50.4 m flagpole tip would rescale the whole
building down by 7%.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/169-steuart/build_169_steuart.py` (deterministic build script),
`artifacts/169-steuart/169-steuart.blend`, and `artifacts/169-steuart/169-steuart.glb`.
The script must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `169-steuart-top.png`,
`169-steuart-north.png`, `169-steuart-east.png`, `169-steuart-south.png`,
`169-steuart-west.png`, plus `169-steuart-contact-sheet.png`, at least one high
three-quarter aerial beauty render `169-steuart-aerial.png`, and a night render
`169-steuart-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the tile roof's hips and ridge, the arcade band, the crest
parapet, the light court and the podium step-down toward Steuart Street; the aerial view
uses the style bible's camera assumptions (30-50 degrees down, long lens), from the
**northeast** so that the entry elevation and the tile roof are seen together.

Note that the axis-aligned elevation renders will each show the building at 45°. That is
the expected consequence of the real heading, not a camera error.

## Validate the exported GLB

Re-import `169-steuart.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Render at least one review image from the re-imported asset. Write
`artifacts/169-steuart/validation.json` and `artifacts/169-steuart/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **59.5 x 59.5 m** even though
the building is 42.35 x 41.84 m — that is the expected consequence of a ~45° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "169-steuart",
  "file": "169-steuart.glb",
  "anchor": [
    -122.3919821,
    37.7926993
  ],
  "targetHeightM": 46.64,
  "cat": 7,
  "name": "Army & Navy YMCA Building (169 Steuart Street)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/169-steuart.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* or *estimated*
are visual or derived, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Fact | Value | Source | Confidence |
|---|---|---|---|
| Name (historic) | Army & Navy Y.M.C.A. Building | OSM way `32862485`; NoeHill; historic survey text | measured/published |
| Name (today) | Embarcadero YMCA (169 Steuart) + Harbor Court Hotel (161–165 Steuart) | YMCA of SF; Harbor Court Hotel; McGinnis Chen Associates | published |
| Addresses | 169 Steuart St (YMCA), 161 & 165 Steuart St (hotel), 166 The Embarcadero | DataSF EAS `ramy-di5m`; NoeHill; SKYDB | measured |
| Parcel | block 3715, condo lots 028 (161–165) and 029 (169), one `mapblklot` **3715028** | DataSF parcels `acdm-wktn` | measured |
| Built | **1924** completed; opened **1926** | McGinnis Chen Associates; SKYDB; NoeHill (1924) vs Historic Hotels / harborcourthotel.com (1926) | published, conflicting — see 2.15 |
| Architect | **Carl Werner** (original plans, signed, held by the YMCA); **Frederick H. Meyer** credited by NoeHill and the AIA lists | historic survey text via sftrajan; NoeHill | published, conflicting |
| Storeys | full-footprint podium on the lowest floors; **two wings of 8 storeys**; a **10-storey arcaded tower** over the middle | historic survey text; McGinnis Chen ("10-story structure") | published |
| Structure / cladding | clay brick masonry and terra cotta over a rusticated cast-stone base; clay tile roof | McGinnis Chen Associates; Historic Hotels | published |
| Style | Spanish Colonial / Renaissance Revival eclectic, with late Italian Gothic and Moorish detailing | historic survey text; SKYDB ("spanish revival"); Historic Hotels | published |
| Published height | **35 m**, 10 floors | SKYDB | published — this is the tower EAVE, see below |
| LiDAR crest | **46.64 m** above ground (`hgt_maxcm` 4664) | DataSF `ynuv-fyni` `sf16_bldgid` 201006.0001651 | measured |
| LiDAR modal roof | **28.14 m** (`hgt_majoritycm` 2814); median 26.09 m; mean 24.90 m; sd **7.40 m** over 6,312 cells at 50 cm | DataSF `ynuv-fyni` | measured |
| LiDAR first-return peak | **50.35 m** (`peak_1st_m`) — the flagpole | DataSF `ynuv-fyni` | measured |
| Ground | 3.62 m NAVD88 median, range 0.62 m — flat | DataSF `ynuv-fyni` `gnd_*` | measured |
| Footprint | 42.35 x 41.84 m OBB; 1,766.9 m2 pentagon; DataSF LiDAR footprint 1,619 m2 | DataSF `acdm-wktn` + `ynuv-fyni`; OSM | measured |
| Anchor | `-122.3919821, 37.7926993` (parcel centroid; the OBB centre agrees to 0.01 m) | derived from the parcel polygon | measured |
| Rooms (hotel part) | 131 | OSM `193054138`; Harbor Court Hotel | published |
| Status | San Francisco Point of Historical Interest; a Historic Resource requiring a Certificate of Appropriateness | NoeHill; McGinnis Chen Associates | published |
| Restoration | 2013 conditions assessment; terra-cotta crack and spall repair, central balcony restoration, window sealants; completed 2018 | McGinnis Chen Associates | published |

**Why 35 m and 46.64 m are both right.** Four independent numbers land on one coherent
three-level building and none of them has to be discarded:

- `hgt_majoritycm` **28.14 m** is the modal roof plane. Divided by the survey's **8
  storeys** that is 3.52 m floor-to-floor — normal for a 1924 building with a tall ground
  floor. The wings.
- SKYDB's **35 m / 10 floors** is 28.14 m plus two more storeys of the same rhythm
  (28.14 + 2 x 3.5 = 35.1). The tower's eave, i.e. the top of its wall.
- `hgt_maxcm` **46.64 m** is 11.64 m above that eave. The tile roof reads ~18 m across in
  the z21 aerial, so an 11.6 m rise over a ~9 m half-span is a **~52° hip** — steep, which
  is exactly what a Spanish tile hipped roof is and what the photographs show.
- `peak_1st_m` **50.35 m** is 3.7 m above the crest, and there is a **visible flagpole** at
  the roof apex in every Embarcadero photograph. The first-return peak is the pole, not
  a tree; nothing overhangs this roof.

The standard-deviation test (`docs/asset-plans/README.md`; `92 South Park`, `592 Third`)
passes rather than fails here: **sd 7.40 m over a 46.2 m range** is a genuinely
multi-level building, not a flat roof with an outlier. A three-level illustrative fit —
28% of cells at ~14 m, 65% at 28.14 m, 7% spread across a 35→46.64 m pyramid —
reproduces the observed mean (24.9 m) and sd (7.40 m) to two decimals. That fit is a
**consistency check on the massing story, not a measurement**: the area fractions are not
uniquely invertible from three moments, and the modelling agent should size the tower and
the court from imagery, not from this arithmetic.

**Independent Street View check.** From the levelled equirectangular panorama
`FWxuTLcC1ZB4mrrB42U-3w` on The Embarcadero (34.65 m perpendicular to the entry facade,
solved from the parcel geometry), the sidewalk line falls **47 px below the image centre
row**, which puts the horizon at exactly row 1024 of 2048 for a 2.5 m camera — the pano
and the surveyed parcel agree to within 5 cm on the distance, so the elevation angles are
trustworthy. Read off that calibration: the Embarcadero crest parapet is **30.9 m** and
the tile-roof ridge is **35.3 m *if it stood on the facade plane***. It does not — it is
set back over the middle of the wing, and a setback of 12–13 m (about half the tower's
depth) puts the ridge at **45–47 m**, bracketing the LiDAR's 46.64 m. Photogrammetry
corroborates the crest to ~2 m; the LiDAR number is the one to ship.

### 2.2 Sources

| Source | Establishes | Note |
|---|---|---|
| DataSF EAS addresses (`ramy-di5m`) | 155 / 161 / 165 / 169 / 177 Steuart and their parcel numbers | the query that split 169 (lot 029) from 165 (lot 028) |
| DataSF parcels (`acdm-wktn`) | both lots share `mapblklot` 3715028, one polygon, address range 161–169 | the one-parcel-many-addresses check |
| DataSF building footprints (`ynuv-fyni`), `sf16_bldgid` 201006.0001651 | all LiDAR heights and the ground plane | 2010 Sanfran_Orig_0845 flight, 6,312 cells |
| DataSF assessor (`wv5m-vpq2`) | **nothing usable** — lots 028/029 are tax-exempt and record 0 storeys, 0 area | do not cite it as a storey count |
| OSM ways `32862485`, `193054138`, `193054131`, `193054133`, `32862467` | the three sub-outlines of our building and the neighbours; `roof:shape=pyramidal` on the main way | Bing-era traces, cross-check only |
| `mcaia.com/portfolio/embarcadero-ymca/` (McGinnis Chen Associates) | "10-story structure clad in clay brick masonry and terra cotta", completed 1924, Historic Resource, 2013–2018 restoration scope | the engineers who surveyed the facade — the strongest single source |
| `noehill.com/architects/meyer/embarcadero_ymca.asp` and `noehill.com/sf/landmarks/poi_embarcadero_ymca.asp` | 1924, 165 Steuart, Frederick H. Meyer, SF Point of Historical Interest | |
| `flickr.com/photos/sftrajan/14300648310` | the historic survey description quoted in 2.4 — wings, tower, arcade, tile roof, Carl Werner attribution, the Moorish lobby | verbatim survey text; the best description of the massing anywhere |
| `historichotels.org/us/hotels-resorts/harbor-court-hotel/history` | opened 1926, Spanish Colonial Revival, arched entries, terracotta carvings, clay tile roofing, 400 original rooms | marketing copy — dates conflict with the 1924 sources |
| `skydb.net/building/340008031/` | 35 m, 10 floors, 1924, Spanish Revival, "165 Steuart Street, 166 The Embarcadero" | the tower eave, not the crest |
| `ymcasf.org/about/history/` | the Army Navy YMCA lineage (the 1908 date there is the predecessor institution, not this building) | do not read 1908 as a construction date |
| Google Street View panos `FWxuTLcC1ZB4mrrB42U-3w`, `TuYMi4-QojLiDd-oC9Dv0Q`, `NDWWz4KU4P14-5Ai7OfXPw` (Embarcadero), `22UuCDNweuX1HZv-SgvwxQ`, `G8fvDCDD0sBmDoPfbEjThA` (Steuart) | the four elevations, the crest photogrammetry, the three-storey Steuart street wall | keyless, per `sf3d-streetview-photogrammetry` |
| Google satellite tiles z20/z21 over `37.79265,-122.39195` | the tile roof's plan shape, the light court, the podium step-down | near-nadir; the tile roof is parallax-stretched, do not scale it off the tile naively |

Exa `web_search_advanced_exa` was the primary photo/fact research tool (three passes:
building history, facade/roof photos, architect attribution). Domains that yielded
usable material: `mcaia.com`, `noehill.com`, `flickr.com`, `historichotels.org`,
`skydb.net`, `ymcasf.org`, `jimsteinhart.com`, `phgcdn.com`. Photographs were not
downloaded; URLs and descriptions are recorded here for the modeller.

### 2.3 Orientation and placement

The building fills a whole block-through parcel between The Embarcadero and Steuart
Street. It is rotated about 45° from the world axes, like the whole Financial District
South grid.

**Scope was settled at stage 0.** DataSF condo lots `3715028` (from_address 161, to 165)
and `3715029` (169–169) return **identical geometry and the same `mapblklot` 3715028**.
There is one parcel, one DataSF LiDAR footprint (1,619 m2) and one continuous facade;
OSM's three ways — `32862485` "Army and Navy Y.M.C.A. Building" (810 m2), `193054138`
"Harbor Court Hotel" (453 m2) and `193054131` "YMCA" (200 m2) — sum to 1,463 m2 and are
the same outline drawn in pieces. The asset is the whole parcel. No sibling in the
Embarcadero batch falls inside the 161–169 range (`121-steuart` and `131-steuart` are
other parcels), so there is no duplicate to reconcile.

Footprint pentagon, in Blender coordinates (metres, `+X` east, `+Y` north), already
centred on the anchor `-122.3919821, 37.7926993`, listed clockwise (reverse for a
counter-clockwise ring):

```
A ( 0.15,  29.76)   north corner   — Embarcadero x Hotel Griffon party line
B ( 29.69,  0.16)   east corner
C ( 25.56, -3.97)   chamfer end
D (-0.15, -29.76)   south corner   — Steuart x 177 Steuart party line
E (-29.69, -0.17)   west corner    — Steuart x Hotel Griffon party line
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `A -> B` | 41.81 m | NE 45.1° | **The Embarcadero** (the hallmark entry front, 166) |
| `B -> C` | 5.84 m | SE 135.0° | corner chamfer |
| `C -> D` | 36.42 m | SE 134.9° | party edge to 177 Steuart / 188 The Embarcadero |
| `D -> E` | 41.81 m | SW 225.1° | **Steuart Street** (161–169 — the address) |
| `E -> A` | 42.27 m | NW 314.9° | party edge and open yard to 155 Steuart (Hotel Griffon) |

Because of the 45.1° heading the axis-aligned bounding box is ~59.5 x 59.5 m for a
building that is 42.35 x 41.84 m. That is correct.

The parcel polygon and the DataSF LiDAR footprint agree on the outline; the LiDAR ring is
1,619 m2 against the parcel's 1,767 m2 because it traces the built face inside the
property line. Where they differ, follow the LiDAR ring for the walls and the parcel for
the exclusion arithmetic (2.13). Expect the usual ~1.25 m parcel-vs-footprint offset.

### 2.4 What each side shows

The historic survey (quoted in the sftrajan Flickr caption) is the authority for the
massing and is worth reading in full before modelling:

> "This structure covers the width of the block from the Embarcadero to Steuart Street on
> the 1st 2 floors. In its higher elevations it is divided into 2 wings, each 8 stories
> high. The entry wing, facing the bay, is the hallmark of the structure with its handsome
> brick facade, arched windows, and ornate balconies and decorative concrete crests.
> Decorative details abound at the base and at the 8th floor. ... A typical renaissance
> feature is the 10 story arcaded tower, with red tiled roof, that tops the building's
> middle portion."

**Northeast — The Embarcadero (41.81 m, the hallmark front).** Bottom-up, as measured off
the calibrated panorama:

- **0 – ~10.5 m**: a two-storey **rusticated light cast-stone base**, coursed in large
  blocks. Ground floor: tall rectangular shopfront-scale openings with dark bronze frames,
  and a **round-arched main entry** flanked by polychrome terra-cotta shields carrying the
  YMCA triangle. Second level: small round-arched windows with decorative surrounds.
- **~10.5 m**: a **corbelled bracket frieze** — a continuous row of heavy round corbels
  under a moulded band carrying the "ARMY AND NAVY Y.M.C.A." inscription. This is the
  strongest horizontal on the building after the roof.
- **~10.5 – ~26 m**: six storeys of **clay brick**, regular punched windows, three shallow
  bays (a wide centre and two ends).
- **~26 – 30 m**: the ornamented top storey — **tall round-arched windows** with
  terra-cotta archivolts, a **balustraded balcony** across the centre, brick diaper
  panels and roundels in the end bays.
- **30.9 m**: the **crest parapet** — a curved, arcaded decorative crown over each end bay,
  above the general 28.1 m roof line.

**Centre of that wing — the tower.** Rising above the 28.1 m roof: a band of small
round-headed **arcade** openings to an eave at **35.0 m**, then the **red clay tile hipped
roof** to **46.64 m**, finial and **flagpole** on the apex.

**Southwest — Steuart Street (41.81 m, the 169 address).** A **three-storey street wall
only**, ~14 m, in two halves:

- the **northwest half (161–165, Harbor Court)** — cream/off-white stucco, a gently curved
  parapet, large round-arched openings at the second level, projecting three-sided bay
  windows, small paired arched windows in the attic band, a dark restaurant frontage and a
  canopied hotel entrance at grade;
- the **southeast half (169, Embarcadero YMCA)** — dark red-brown brick, projecting bay
  windows set in deep square recesses, a flat parapet, and the "Embarcadero YMCA" entrance
  under a black fascia with a projecting "YMCA" blade sign.

The eight-storey mass sits **behind** this street wall, not on it. From the Steuart
sidewalk the tower is barely visible; from the aerial the step is obvious.

**Southeast (36.42 m + a 5.84 m chamfer).** A party edge against 177 Steuart / 188 The
Embarcadero, a 1986 blue-glass office block that stands 32.9 m. Brick, minimally
fenestrated, with a light well between the two buildings. *Inferred.*

**Northwest (42.27 m).** A party edge against the 26.4 m Hotel Griffon (155 Steuart), but
only partly built against: an **open yard with surface parking** occupies the middle of
that boundary, so a real, plain brick flank is exposed at the wing's full 28 m for part of
its length. Visible in the z20 aerial and from the Steuart panorama. *Inferred* in detail.

**Roof (the camera looks down — this is a facade).** From the z21 aerial: the **red tile
hipped roof** with a finial, sitting over the middle of the bay-facing wing; the light
grey flat roofs of the two eight-storey wings; a **light court** between them with visible
white plaster walls and window ranks; a lower **podium roof** across the Steuart third
carrying mechanical plant, roof hatches, a stair bulkhead and a panel array; and the
crest parapets standing proud along the Embarcadero edge.

### 2.5 Recognition cues (ranked)

1. **The red clay tile hipped roof with its flagpole**, standing 18 m above every parapet
   on the block. The only sloped roof and the only saturated red for two blocks.
2. **The arcaded tower storey** immediately under that roof — a band of small round-headed
   openings that reads as a texture change at thumbnail size.
3. **Red-brown brick over a pale two-storey stone base**, split by the corbelled bracket
   frieze. The tripartite reading is what makes it a 1920s civic building rather than a
   warehouse.
4. **The 42 x 42 m block-through square** — it fills the parcel corner to corner, which no
   other bespoke asset in the Embarcadero batch does.
5. **The three-storey Steuart street wall** stepping down from the eight-storey mass, with
   the cream-stucco / dark-brick split between the hotel and the YMCA entrances.

### 2.6 Miniature translation

- Keep four volumes: podium, two wings, tower. Everything else is surface treatment.
- The tile roof gets the exaggeration budget — a slightly steeper pitch and a slightly
  warmer red than life, with chunky beveled hips (Bevel 0.1–0.15, 2 segments per the
  contract) so the four hip lines catch the light from the aerial camera.
- The arcade band becomes a **repeating notched strip**, not modelled arches: a recessed
  band with regularly spaced square-cut reveals reads as an arcade at 40 px and costs a
  tenth of the triangles.
- The corbel frieze becomes **one moulded band with a shadow reveal**. Do not model the
  individual corbels.
- Windows are geometric recesses in the brick, not frames — the style bible's dark
  blue-grey graphical windows (`Toy_glass`). One rhythm per elevation, not per bay.
- The Steuart bay windows are worth keeping as **simple three-sided projections** because
  they are the only relief on that elevation and they carry the "169" read.
- The light court can be a shallow notch. It matters from directly above and nowhere else;
  do not model its interior walls in detail.
- Terra-cotta shields, balustrades, diaper panels, the inscription and the heraldry are
  colour and a 2–3 cm relief at most. At city scale they are one tone.

### 2.7 Massing recipe

Depths are measured from the Embarcadero (northeast) face along the parcel's 42.27 m
northeast→southwest axis. Levels are heights above ground (ground = 3.62 m NAVD88;
the model's z=0 is that ground).

| # | Volume | Plan | Top |
|---|---|---|---|
| 1 | **Podium** | the full pentagon A–B–C–D–E | **14.0 m** *(estimated — three storeys as built on Steuart today; the survey says "the 1st 2 floors")* |
| 2 | **Stone base band** | the full pentagon, as a material change and a projecting cornice, not a volume | 10.5 m *(photogrammetric)* |
| 3 | **Northeast wing** (the entry wing) | a bar on the A–B frontage, 41.81 m x ~15 m deep | **28.14 m** roof; **30.9 m** crest parapet on the northeast face *(measured / photogrammetric)* |
| 4 | **Light court** | a notch between the wings, ~10 x 14 m, floor at the podium roof | 14.0 m *(estimated — size and position must be verified from the aerial)* |
| 5 | **Southwest wing** | a parallel bar, ~41 m x ~12 m deep, ending ~29.6 m back from the Embarcadero face | **28.14 m** |
| 6 | **Steuart street wall** | the remaining ~12.7 m of depth to the D–E face | **14.0 m** — this band stays at podium height |
| 7 | **Tower** | centred on the A–B frontage over volume 3, ~17 x 17 m *(estimated)* | walls / arcade eave **35.0 m**; the arcade band occupies roughly 31–35 m |
| 8 | **Tile roof** | hipped, four faces, over volume 7 | **46.64 m** apex — the target height |
| 9 | **Flagpole + finial** | on the apex | decorative only; keep the export's bounding box at 46.64 m (see Part 1) |
| 10 | **Roof plant** | low bulkheads and units on the podium and wing roofs | +1.5–3 m over their roof, chunky boxes |

The 12.7 m depth of volume 6 and the 15 m depth of volume 3 are the numbers most worth
re-deriving from the aerial. Everything above 28.14 m is well constrained; everything
between the wings is not.

### 2.8 Materials and palette

All flat, roughness ~0.85, names from the `sf-asset-check` palette.

| Surface | Material | Hex | Note |
|---|---|---|---|
| Main brick body, wings and tower walls | `Toy_brick` | `c96f4a` | the warm red-brown that makes this the warm building on the block |
| Steuart YMCA half (169) brick | `Toy_rust` | `a86444` | visibly darker than the main body — that split is a recognition cue |
| Two-storey rusticated base, cornices, window surrounds, crest parapet | `Toy_stone` | `d9d2c2` | must read distinctly lighter than the brick |
| Steuart Harbor Court half (161–165) stucco | `Toy_cream` | `f2ede3` | the palest thing on the building |
| Clay tile roof | `Toy_red` | `c4453c` | if it reads brown next to `Toy_brick` in the day render, step to `Toy_ioorange` `c0402a` rather than desaturating the brick |
| Windows | `Toy_glass` | `2a4d73` | the style bible's dark blue-grey graphical windows |
| Terra-cotta shields, roundels, finial | `Toy_gold` | `caa64a` | the only warm accent; use it sparingly, it is 1% of the surface |
| Roof plant, bulkheads, flagpole | `Toy_steel` | `9aa0a6` | **not `Toy_roofd`** — `45454a` renders as near-black (rgb 9,9,12) on a roof deck under the app's lighting |

**Night (`_Glow`).** One hero plus two supporting accents, per the style bible:

- hero — **the arcade band under the tile roof** (`Toy_gold_Glow`, base colour `caa64a`),
  a lit loggia ring that is visible from every direction and is the same feature that
  identifies the building by day;
- supporting — **the Embarcadero entry arch** (`Toy_gold_Glow`) and a **scattered subset
  of hotel windows** (`Toy_glass_Glow`, base colour `2a4d73` lightened toward `6f95b8`);
- supporting — the **"Embarcadero YMCA" fascia** on Steuart (`Toy_white_Glow`, `f7f4ec`),
  a thin strip only.

A `_Glow` material's **base colour is its night appearance** — the app's night layer is an
unlit overlay drawn at the baked colour, so pick the colour you want to see at night and
check it in the night render, not the emission strength. Keep glow shells proud of the
opaque surface; a closed shell reads as two alpha layers and tints the facade by day.

### 2.9 Top surface

Designed, because the camera looks down:

- the tile roof's four hips and its short ridge, with a beveled eave overhang;
- the crest parapets along the Embarcadero edge, standing 2.8 m above the wing roof;
- the light court as a clean rectangular notch with a visible floor;
- the podium roof over the Steuart third: two or three chunky mechanical boxes, a stair
  bulkhead, a dark panel array, and a parapet all round;
- the northwest flank's exposed brick, visible over the open yard;
- no clutter that is not one of the above. The roof is the second-most-looked-at surface
  on this asset.

### 2.10 Scope

**In:** the 1924 building on parcel 3715028 — podium, both wings, light court, tower,
arcade, tile roof, flagpole, crest parapets, roof plant, all four edges.

**Out:** The Embarcadero and its F-line tracks, Steuart Street, the sidewalk and its
palms, the Hotel Griffon, 177 Steuart / 188 The Embarcadero, the northwest yard and its
parked cars, street furniture, people, plinths, cameras, lights.

### 2.11 Triangle budget

Cap **22,000**. Indicative split:

| Element | Triangles |
|---|---|
| Podium + street wall, beveled | 2,000 |
| Two wings, beveled masses | 2,500 |
| Stone base band + corbel frieze band | 1,800 |
| Embarcadero window rhythm + arched top storey | 4,500 |
| Steuart elevation: bays, arches, entrances | 3,000 |
| Crest parapets | 1,200 |
| Tower walls + arcade notch band | 2,500 |
| Tile roof + eave + finial + flagpole | 2,000 |
| Roof plant, court, party-edge relief | 1,500 |
| **Total** | **21,000** |

If the budget binds, cut the southeast party edge first, then the Steuart attic windows,
then the wing window rhythm. Never cut the tile roof, the arcade band or the stone base.

### 2.12 Draft manifest entry

```json
{
  "id": "169-steuart",
  "file": "169-steuart.glb",
  "anchor": [
    -122.3919821,
    37.7926993
  ],
  "targetHeightM": 46.64,
  "cat": 7,
  "name": "Army & Navy YMCA Building (169 Steuart Street)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`"estimated": false` because the 46.64 m crest is a LiDAR measurement corroborated by
Street View photogrammetry and by the roof's own pitch geometry, and the anchor is a
surveyed parcel centroid. The *interior* levels (podium at 14.0 m, court, tower plan) are
estimated and are called out in 2.15 — they do not reach the manifest.

`cat: 7` (hotel) is the building's dominant program — 131 hotel rooms against a gym and
pool — and matches OSM's `building=hotel` on the main way. `cat: 24` (gym) was considered
because 169 Steuart is specifically the YMCA door; the name carries that reading instead.

### 2.13 Integration notes (for later, not this task)

- **New landmark (Case B).** Add a `pipeline/lib/landmarks.mjs` entry (`id: '169Steuart'`)
  and re-bake the affected tiles, or the baked procedural building on this footprint will
  intersect the GLB.
- **Exclusion radius — measured, and the window is comfortable.** `excluded()` in
  `pipeline/buildings.mjs` drops a footprint when its **centroid OR any ring vertex** falls
  within `r` of the anchor, so the radius has to reach our own rings and miss every
  neighbour's vertex.

  | | distance from anchor |
  |---|---|
  | our DataSF LiDAR ring (centroid / nearest vertex) | 2.05 m / 7.67 m |
  | our OSM ring `32862485` (centroid / nearest vertex) | 8.34 m / 6.44 m |
  | our OSM ring `193054138` (centroid / nearest vertex) | 15.58 m / 6.44 m |
  | our OSM ring `193054131` (centroid / nearest vertex) | 19.63 m / **9.11 m** |
  | **nearest neighbour vertex** — Hotel Griffon, OSM `193054133` | **21.44 m** |
  | nearest neighbour vertex — 177 Steuart, DataSF `SF3715013` | 21.58 m |
  | 188 The Embarcadero, OSM `32862467` | 22.10 m |

  Safe window **9.11 m < r < 21.44 m**. Take **`exclude: 15`** — 5.9 m of margin over the
  worst of our own sub-rings and 6.4 m to the nearest neighbour vertex, which absorbs the
  usual ~1.25 m parcel-vs-footprint disagreement. **Re-measure against the real bake input**
  (`pipeline/data/overture_buildings.geojsonseq`) before committing: Overture may split this
  building differently from OSM, and a sub-ring stranded in one corner is the one thing
  that would move the lower bound.
- `loadRadius`: the default formula gives `max(2500, 46.64 * 30) = 2500` m. Take the
  default; this is not an `alwaysLoaded` skyline piece.
- **Verify-rebake's count check is blind here.** Our building is one DataSF polygon but
  three OSM/Overture rings, so a per-cell count comparison can report "nothing dropped"
  while the exclusion is working. Settle it from the tile: decode the cell and measure
  penetration, do not trust the count.
- **Judge it against the batch.** `audiffred-building`, `110-embarcadero`,
  `132-embarcadero`, `121-steuart` and `131-steuart` are all in flight on the same two
  blocks. If this one does not read as the tall warm building with the red roof among a
  row of flat grey and tan street walls, the tower has collapsed into the mass.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 46.64 m (loader scale lands at 1.0) — the flagpole must not set it
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~59.5 x 59.5 m is expected)
- [ ] Footprint proportion preserved: the building must measure 42.35 x 41.84 m along its own axes, with the 5.84 m chamfer at the east corner
- [ ] Wing roofs land at 28.1 m; tower eave at 35.0 m; Embarcadero crest parapet at 30.9 m; Steuart street wall at ~14 m
- [ ] The tile roof reads as a hipped, tiled, saturated-red volume from directly above
- [ ] Triangles at or under 22,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`; no `Toy_roofd`
- [ ] `_Glow` only on the arcade band, the entry arch, scattered hotel windows and the YMCA fascia; glow shells proud of the opaque surface
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

1. **`hgt_maxcm` 46.64 m is real here, and that is the opposite call from 592 Third and
   250 Van Ness.** There the maximum was street-tree canopy over a flat roof with a sub-metre
   standard deviation. Here the standard deviation is **7.40 m over 6,312 cells**, the
   footprint is a documented three-level building, the aerial shows a large tiled hipped roof
   at exactly that spot, and `peak_1st_m` (50.35 m) is explained by a **flagpole that is
   visible in the photographs**. Nothing overhangs this roof. Model the tower. If a later
   source contradicts 46.64 m, the number to fall back to is 35 m *for the eave* — not for
   the building.
2. **The podium height of 14.0 m is estimated.** It comes from counting three storeys on
   the Steuart street wall in Street View and from the LiDAR distribution's low mode; no
   source publishes it. The survey text says "the 1st 2 floors" cover the block, which
   suggests something nearer 10–11 m, while the built condition on Steuart today is
   unambiguously three storeys. Re-derive it before modelling — it sets the whole Steuart
   elevation.
3. **The light court's size and position are estimated.** "Divided into 2 wings" is
   published; the court's 10 x 14 m and its placement are read off a nadir satellite tile
   in which the tall walls are parallax-displaced. Verify from the aerial and be willing to
   make it a shallow notch.
4. **The tower's plan size is estimated and the two available methods disagree.** The z21
   tile puts the tile roof at ~18 m across; inverting the LiDAR moments for a three-level
   model puts the 35 m+ zone nearer 11–13 m across. Parallax inflates the first, and three
   moments cannot uniquely invert the second. **Size it from imagery**, take ~17 m as the
   starting point, and record what you measured.
5. **Two architects and two dates.** Frederick H. Meyer is credited by NoeHill and the AIA
   lists; the original plans held by the YMCA are signed by **Carl Werner**. Completed 1924
   (architects, survey, SKYDB) but opened 1926 (Historic Hotels, the hotel's own site).
   Record both attributions in `REFERENCE.md`; neither changes any geometry.
6. **The northwest flank is exposed but unphotographed.** An open yard interrupts the party
   line with the Hotel Griffon, leaving real brick wall visible up to 28 m for part of its
   length. It is visible in the z20 aerial and glimpsed from Steuart, but there is no
   straight-on photograph. Give it the plainest credible treatment — brick, sparse windows,
   no ornament — and mark it inferred.
7. **The assessor is useless here.** Lots 028 and 029 are tax-exempt and record 0 storeys,
   0 units and 0 area. Do not reach for `wv5m-vpq2` to settle the storey count, as several
   plans in this set legitimately do.
8. **The Steuart-side panorama does not calibrate.** `G8fvDCDD0sBmDoPfbEjThA` puts its own
   horizon ~34 px off the equirect centre row and disagrees with the surveyed geometry by a
   factor of two on distance — its reported position cannot be trusted (the failure mode
   `sf3d-streetview-photogrammetry` warns about). Every metric statement in this plan comes
   from the **Embarcadero** panorama, which self-calibrates to 5 cm. If you need a measured
   Steuart height, solve the camera distance from the panorama rather than from its
   reported lat/lon.
