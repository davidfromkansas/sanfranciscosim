# 8 Mission Street (1 Hotel San Francisco / Hotel Vitale) — SF-SIM asset plan

The waterfront hotel that fills the whole block between Mission Street, Steuart Street,
The Embarcadero and Don Chee Way — directly across the Embarcadero from the Ferry
Building, and the first building the city shows anyone walking off a ferry. Eight
storeys of brown brick on a rough limestone base, with a **circular brick turret** at
the Mission/Embarcadero corner carrying seven round suites and a metal lantern crown,
and a **concave curved notch** cut into the Mission/Steuart corner. Behind that street
wall the building terraces down to the north-west, and the stepped roofs are planted
green decks with the rooftop spa on them.

It is the only bespoke asset in the set whose brief is *stepped massing*. 501 Second is
bigger in plan and Fairmont is far taller, but both are single prisms with a flat
parapet. This one is a 25 m block on the Mission end that descends across two setbacks
to about 14 m at the plaza end, and the descent is visible from the app's aerial camera
in a way it is not from any street. Get the steps and the turret and it is unmistakable;
build it as one box with a bump on the corner and it is a brick slab next to the Ferry
Building.

John King's 2005 Chronicle review is unusually useful as a source precisely because he
disliked it: he inventories the materials (Jerusalem limestone base, brown brick,
yellowish plaster upper storeys), the setbacks (eight storeys on Mission descending to
six- and four-storey wings toward the plaza), and both corner events, in a way no
marketing copy does.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/8-mission/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `8-mission` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3932805, 37.7937365` |
| Target height | **28.66 m** to the turret crown (LiDAR max, measured); main Mission-end parapet **25.10 m** (LiDAR mode, measured); middle-wing parapet **19.64 m** (LiDAR median, measured); north-west wing **14.18 m** (derived — see `artifacts/8-mission/REFERENCE.md`) |
| Footprint | 64.08 m (Steuart / Embarcadero long axis, bearing 135.4°) x 42.07 m (Mission axis); L-shaped, 2,133 m2 measured from OSM way 193054134 |
| Triangle cap | 26,000 |
| Category | `7` (hotel) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 8 Mission Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 8 Mission Street — 1 Hotel San Francisco,
formerly Hotel Vitale — in San Francisco and deliver it as a downloadable, validated
GLB.

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
7. `artifacts/ferry-building/` — the neighbour across the Embarcadero, 220 m away. This
   asset will be seen in the same frame as that one in almost every aerial; check its
   scale, its palette and how it reads at distance before choosing yours
8. `artifacts/501-second/` — the closest precedent for a large multi-storey block with a
   tripartite composition and a big designed roof; reuse its bay/opening/cornice-ring and
   roof-plant helpers rather than reinventing them
9. `artifacts/49-south-park/` — the set's existing **rounded corner turret**. Do not
   re-solve the cylinder-meets-orthogonal-wall junction from scratch; start from what
   that build script does and check its segment count against the triangle budget here
10. `artifacts/2-south-park/` and `artifacts/524-second/` — the palette precedents for
    `Toy_brick` masonry, including 2 South Park's note on not darkening brick toward
    `Toy_rust`
11. `docs/asset-plans/8-mission.md` — this plan, whose dossier is your research
    starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The **stepped massing**. This is the whole brief and the thing that fails silently.
  Three plateaus, from the Mission (south-east) end down toward the Harry Bridges Plaza
  (north-west) end: **25.10 m**, **19.64 m**, and **14.18 m**. The tall end is on
  Mission, the low end is at the plaza, and the roofs in between are terraces, not
  leftovers. Read 2.7 before laying the first box.
- The **circular turret** at the Mission/Embarcadero corner: about **9.0 m** across
  (r ≈ 4.5 m), centred 4.5 m in from both faces, brick below with glazed upper storeys,
  rising past the parapet to a dark metal crown at **28.66 m** — the crest, and the
  night hero. It is the only feature of this building that any source calls
  distinctive, and it is what makes it legible from the aerial camera.
- The **concave notch** at the Mission/Steuart corner: a curve of radius **8.2 m** cut
  *into* the plan, not a chamfer and not a bulge. The two corner events are opposites
  and the building is unrecognisable if they are both convex.
- The **three-part facade**: a rough pale limestone base about 1.5 m tall, brown brick
  for most of the height, and **light warm plaster on the top two storeys**, which reads
  as a distinctly paler cap on every elevation.
- The **arched ground floor**: tall round-arched openings along Mission and Steuart, and
  a **barrel-vaulted metal-and-glass canopy** over the porte-cochere in the middle of
  the Mission elevation — the entrance, and the second night cue.
- The **projecting glazed bays** on The Embarcadero elevation: tall steel-framed window
  bays standing proud of the brick piers, running the full height of the shaft. That
  elevation is glass-dominant where Mission is brick-dominant.
- The **planted roof terraces** on the two lower plateaus, and the rooftop spa. The
  camera looks down; on this building the roof is a designed garden and must not be a
  grey membrane with vents on it.

## Research 8 Mission Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation,
and gather references covering:

- All four elevations. Mission (south-east) and The Embarcadero (north-east) are the
  hero elevations; Steuart (south-west) is the long one at 58 m; the Don Chee Way
  (north-west) end is the plain brick slab King complains about and must still be built
- Aerial and roof views — the terraces, the spa, the bamboo, the plant, and **where each
  setback actually falls**. This is the weakest number in this dossier (2.15)
- The turret: its diameter, how far it projects, how its crown is shaped, and where it
  tops out relative to the main parapet
- Ground-level views, day and night. The night state matters here: this is a hotel on a
  dark waterfront edge
- The storey count on each wing, and the two setback heights

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**Two known source traps, already resolved in 2.1 — re-check them, do not silently
re-inherit a wrong value:** OSM way 193054134 carries **no `height` and no
`building:levels` tag at all**, so there is no tag to be misled by and equally no
independent cross-check on the LiDAR; and the DataSF LiDAR record for this footprint is
**deliberately multi-modal** (mode 25.10 m, median 19.64 m, mean 19.65 m, σ 6.01 m) —
that spread is the building's real setbacks, not noise, and collapsing it to one number
is the single easiest way to get this asset wrong.

## Create a reference dossier

Write `artifacts/8-mission/REFERENCE.md` containing: source links and what each
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

Spend the detail on the **turret**, the **three roof plateaus** and the **pale attic
band**. Spend nothing on the fake arches' archivolts, individual window muntins, the
balcony railings, the bamboo pots or the limestone's rustication texture; at city scale
they are sub-pixel and they will eat the budget the turret needs.

Semantic exaggeration is allowed and wanted in exactly two places (style bible §22):
make the turret read slightly bolder than its true 9 m diameter if the aerial silhouette
needs it, and make the setbacks slightly crisper than the real terraces. Do not
exaggerate the height, the footprint or the position — AGENTS rule 5.

The finished asset must be immediately recognizable as 8 Mission Street, consistent with
the real building from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and
never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single hotel building: all four elevations, the turret, the notch, the
limestone base, the arched ground floor and entrance canopy, the Embarcadero glazed
bays, all three roof plateaus with their terraces, the spa and the roof plant.

**Do not include the Muni subway vent-shaft pavilion** that sits in the notch on the
north corner of the block (OSM way 260290226, roughly 20 x 15 m and 5.4 m tall, with the
circular louvred grille on its roof). It is a separate structure, it stays procedural,
and the integration exclusion radius in 2.13 is sized specifically to spare it.

Do not include unrelated surrounding city geometry: Mission Street, Steuart Street, The
Embarcadero, Don Chee Way, the Audiffred Building, Harry Bridges Plaza, the restaurant
marquee tent on the Embarcadero sidewalk, street trees, the sidewalk, parked cars,
people, plinths, cameras or lights. Temporary context may appear in review renders but
must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project palette;
`_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no cameras, lights,
animations, armatures or constraints; no external dependencies; at most 26,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric`
in `app/src/assets.js` only scales and positions). The Mission Street front faces
**south-east, bearing 135.4°**; The Embarcadero elevation faces **north-east, 45.4°**;
the Steuart Street elevation faces **south-west, 225.4°**; the Don Chee Way end faces
**north-west, 315.4°**. The building is rotated about 45° off the world axes, so build
directly on the measured footprint polygon in 2.3 rather than modelling an axis-aligned
box and rotating it.

**Height normalization:** the tallest geometry in the export (the turret crown) must
land at exactly **28.66 m** so the loader's `targetHeightM / measuredHeight` scale is
1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/8-mission/build_8_mission.py` (deterministic build script),
`artifacts/8-mission/8-mission.blend`, and `artifacts/8-mission/8-mission.glb`.
The script must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `8-mission-top.png`,
`8-mission-north.png`, `8-mission-east.png`, `8-mission-south.png`, `8-mission-west.png`,
plus `8-mission-contact-sheet.png`, at least one high three-quarter aerial beauty render
`8-mission-aerial.png`, and a night render `8-mission-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show **all three roof plateaus, the terraces, the turret and the
notch**, because the top view is the only one that proves the massing. The aerial view
uses the style bible's camera assumptions (30-50 degrees down, long lens), from **due
east**, so that the Mission and Embarcadero elevations and the turret between them are
seen together — that is the app's own preset (2.12).

**Add a fifth render the other plans do not need:** an orthographic elevation from the
**north-east** at a low angle, `8-mission-steps.png`, whose only job is to show the
three parapet heights as three distinct horizontal lines. If they do not read as three
lines there, the massing has collapsed.

Note that the axis-aligned elevation renders will each show the building at 45°. That is
the expected consequence of the real heading, not a camera error.

## Validate the exported GLB

Re-import `8-mission.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Render at least one review image from the re-imported asset. Write
`artifacts/8-mission/validation.json` and `artifacts/8-mission/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **74.1 x 56.5 m** (an L, not a rotated rectangle: the missing north quadrant shortens one world diagonal) even though the
building is 64.08 x 42.07 m — that is the expected consequence of a ~45° real-world
heading, not a scale error.

**Normals on this asset need the per-object signed-volume test, not the ray test alone.**
The turret is a cylinder intersecting two orthogonal walls and the notch is a concave
cut; both are the shapes that produce ray-test residuals on a union of solids. The
contract is: per-object signed volume authoritative, ray-test residual ≤ 0.15%.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "8-mission",
  "file": "8-mission.glb",
  "anchor": [
    -122.3932805,
    37.7937365
  ],
  "targetHeightM": 28.66,
  "cat": 7,
  "name": "1 Hotel San Francisco (8 Mission Street)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/8-mission.md`.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Source and confidence |
|---|---|---|
| Address | 8 Mission Street, San Francisco, CA 94105 | OSM `addr:*` on way 193054134 — **verified** |
| Current name | 1 Hotel San Francisco | OSM `name`, `website`; the hotel's own site — **verified** |
| Original name | Hotel Vitale (2005–2020) | Heller Manus, LDA Architects, SF Chronicle — **verified** |
| Architect | Heller Manus Architects (Clark Manus, FAIA). LDA Architects = record architect; interiors by Colum McCartan | Heller Manus project page; LDA project page; SF Chronicle 2005 — **verified** |
| Completed / opened | 2005 (approved 2000, opened March 2005) | LA Times 13 Mar 2005; LDA; SKYDB — **verified** |
| Storeys | **8** on the Mission Street end, terracing down to six- and four-storey wings toward Harry Bridges Plaza | Heller Manus ("eight-story"); SF Chronicle 2005 (the setbacks) — **verified** |
| Rooms | 199–200 | LA Times (199); Heller Manus (200) — **verified**, immaterial to the model |
| Gross area | 143,960 sq ft (13,374 m2) | LDA Architects — **verified**. Divided by the 2,133 m2 footprint that is 6.3 average floors, which is an independent corroboration of a terraced 8/6/4 building rather than a flat 8 |
| Crest (turret crown) | **28.66 m** above local ground | DataSF LiDAR `hgt_maxcm` 2866 on footprint `201006.0001079` — **measured**, corroborated visually (2.4) |
| Main parapet, Mission end | **25.10 m** | DataSF LiDAR `hgt_majoritycm` 2510 — **measured** (the modal roof plane) |
| Middle-wing parapet | **19.64 m** | DataSF LiDAR `hgt_mediancm` 1964 — **measured** |
| North-west wing parapet | **14.18 m** | *estimated* — a four-storey wing at the derived storey heights; see 2.15 risk 1 |
| Storey heights | ground ~6.0 m, typical ~2.73 m | *derived*: the 25.10 / 19.64 pair over an 8 / 6 storey difference gives 2.73 m per floor; the residual ground floor is 6.0 m, which matches a double-height arcaded lobby/restaurant |
| Ground elevation | 3.20 m min, 3.57 m mean | DataSF LiDAR `gnd_mincm` / `gnd_meancm` — **measured**. The app samples its own terrain; this is only a sanity bound |
| Footprint | L-shaped, 2,133 m2; OBB **64.08 x 42.07 m** at bearing 135.4° | OSM way 193054134 geometry via the OSM API, reprojected and reduced to a minimum-area OBB — **measured**. DataSF footprint `201006.0001079` (8,649 cells x 0.25 m2 = 2,162 m2) agrees to 1.4% |
| WGS84 anchor | `-122.3932805, 37.7937365` | OBB centre — **measured**. The true polygon centroid is 4.92 m away at `-122.3932618, 37.7936945`; the OBB centre is the correct anchor because the model is base-centred on the bounding rectangle |
| Turret | circle centre (u,v) = (27.6, −16.5), r ≈ **4.5 m** | least-squares fit to OSM arc nodes 2–15 — **measured** |
| Mission/Steuart notch | concave arc, r ≈ **8.2 m**, centred outside the plan at (u,v) = (34.3, 22.4) | fit to OSM arc nodes 29–35 — **measured** |
| Materials | rough Jerusalem limestone base (~5 ft), smooth brown brick above, yellowish plaster on the upper storeys | SF Chronicle 2005 (John King), corroborated by Street View — **verified** |
| Site history | Muni bus yard under the Embarcadero Freeway; MTA-owned land on a 65-year lease from 1998; Prop K shadow limits on the plaza drove the setbacks | SF Chronicle 2005 — **verified**, and it is the *reason* for the massing |

**No OSM `height` and no `building:levels` tag exists on this way.** That removes the
usual trap and also the usual cross-check: the tier heights rest on the LiDAR summary
plus published storey counts, and nothing else.

### 2.2 Sources

Exa (`web_search_advanced_exa`) queries actually run, and what each yielded:

1. `"Hotel Vitale 8 Mission Street San Francisco architect building height stories"`,
   8 results, summaries on — the load-bearing search. Yielded:
   - `hellermanus.com/projects/hotel-vitale` and `hellermanus.com/1-hotel-san-francisco` —
     architect, eight storeys, 200 rooms, **the circular turret with seven suites**, the
     rooftop spa. *Confirmed: architect, storey count, the turret's existence and role.*
   - `ldaarch.com/hotel-vitale` — record architect, 2005, 143,960 sq ft, $30M,
     "200 guest rooms in **a series of stepped floors, topped by accessible terraces**",
     "decks that bring the public out onto **the cascade of roofs** overlooking the
     Plaza". *Confirmed: the terracing, independently of King.*
   - `sfchronicle.com` / `sfgate.com`, John King, 21 Apr 2005 — **the single most useful
     source**. Materials (Jerusalem limestone base "after five feet or so gives way to
     smooth brown brick", "yellowish plaster on the upper stories"), the massing ("eight
     stories along Mission Street but uses terraces to descend to four-story and
     six-story wings facing Harry Bridges Plaza"), "tallest where it faces the
     three-story Audiffred, and shortest on Steuart Street", **"a circular bay where
     Mission meets the Embarcadero"**, **"the inwardly curved notch where Steuart and
     Mission streets meet"**, the porte-cochere entrance with its column, and "the brown
     slab facing the northern plaza". *Confirmed: every massing and material claim in
     2.4 and 2.7.*
   - `skydb.net` — 8 floors, 2005, no height. *Confirmed storeys; no height anywhere.*
   - `latimes.com` 13 Mar 2005 — opening date, 199 rooms, $53M.
   - `archello.com/project/hotel-vitale` — five Heller Manus project photographs.
2. `"Hotel Vitale San Francisco rooftop Spa Vitale terrace penthouse turret photos
   Embarcadero"`, 8 results, highlights on — roof and turret material.
   `cntraveler.com` ("the Spa Vitale takes up **a rooftop corner** … a rooftop terrace
   … overlook the Ferry Building"), `oceanhomemag.com` ("a **penthouse-level spa set in
   a tranquil bamboo garden**"), `wanderwithwonder.com` (penthouse terrace, rooftop
   event spaces), `justluxe.com` and `timeout.com` (the circular suites' 180°/360°
   views), `1hotels.com/san-francisco` (reclaimed-timber interiors — interior only).
   *Confirmed: the spa is a rooftop corner pavilion in a bamboo garden, not a full
   penthouse floor.* Labelled **observed (marketing photography)** — these show the
   hotel as marketed.

Non-Exa sources:

- OSM API way `193054134` — footprint geometry, 37 nodes, and the surrounding block
  (Audiffred Building 193054136, Steuart Place 193054132, Hotel Griffon 193054133, the
  vent pavilion 260290226) and the four street centrelines.
- DataSF Building Footprints (LiDAR-derived), `https://data.sfgov.org/resource/ynuv-fyni`
  — record `201006.0001079` (`mblr` SF3714019): the height statistics in 2.1, and the
  separate record `201006.0017562` for the vent pavilion (mode 4.49 m, max 6.28 m) that
  2.13's exclusion radius has to spare.
- Google satellite imagery (`mt1.google.com/vt/lyrs=s`, z21) stitched and overlaid with
  the OSM ring — the roof composition in 2.9: the green terrace decks, the white
  mechanical roof at the Mission end, the turret's circular roof, the spa deck at the
  notch, and the vent pavilion's circular louvre in the notch. **Observed.**
- Google Street View panoramas, keyless via `streetviewpixels-pa.googleapis.com` — the
  four elevations in 2.4. Panoids used: `5PjWOJB0thBrZhZJcrczXA` (Mission, yaw 315),
  `zXBL9q5JhlYVXn7nZUrCrQ` (Embarcadero, yaw 225), `NLmEUwDtUklmyMct15R5FA` (Steuart,
  yaw 45), `yPQsEQlbilZVbI4250XrJw` (the east corner and the turret, yaw 285),
  `fee0fFoI73P9eoY8ahIbrw` (Embarcadero oblique showing the step-down, yaw 291),
  `dWxwJrZ7v60AQHfr5ZELPw` (from Harry Bridges Plaza, yaw 187 — the north-west end).
  **Observed.**

### 2.3 Orientation and placement

Local frame used throughout this dossier: **u** runs along the 64.08 m axis, positive
toward bearing **135.4°** (south-east, toward Mission Street); **v** runs along the
42.07 m axis, positive toward bearing **225.4°** (south-west, toward Steuart Street).
The origin is the OBB centre, which is the anchor.

The plan is an **L**: a full-width bar plus a rectangular bite out of the north corner.

| Element | Extent | Faces | Length |
|---|---|---|---|
| Mission Street elevation | u = +32, v from −11.3 to +15.1 | south-east, 135.4° | 26.4 m straight |
| Turret | circle centre (27.6, −16.5), r 4.5 | the east corner | ~9.0 m across |
| Notch | concave arc r 8.2, centre (34.3, 22.4) | the south corner | ~8.5 m of arc |
| Steuart Street elevation | v = +21.0, u from −32.0 to +26.3 | south-west, 225.4° | **58.3 m — the long one** |
| Don Chee Way end | u = −32.0, v from +3.3 to +21.0 | north-west, 315.4° | 17.7 m |
| Notch return (inner) | v = +3.3, u from −31.9 to −11.5 | north-east, 45.4° | 20.4 m |
| Notch return (inner) | u = −11.4, v from +3.3 to −20.8 | north-west, 315.4° | 24.1 m |
| The Embarcadero elevation | v = −20.8, u from −11.2 to +22.8 | north-east, 45.4° | 34.0 m |

Street setbacks, measured from the OSM/DataSF centrelines: Mission ~11 m from the u=+32
face; Steuart ~12.5 m from the v=+21 face; The Embarcadero ~21 m from the v=−20.8 face;
Don Chee Way ~8 m from the u=−32 face. Nothing on this block is a party wall — the
building stands free on four sides, and all four elevations are public.

Neighbours, for scale judgement in the aerial: the Audiffred Building (3 storeys, 15.4 m
LiDAR mode) 57 m away across Mission; Hotel Griffon and Steuart Place (5 and 7 storeys)
beyond it; One Market Plaza's 42-storey Spear Tower 50 m away across Steuart; the Ferry
Building 220 m north-north-west across the Embarcadero. King's point — that the hotel is
tallest where it faces the three-storey Audiffred and lowest where it faces the
42-storey tower — is exactly backwards from good urbanism and exactly what the model has
to reproduce.

### 2.4 What each side shows

**South-east — Mission Street (hero, 26.4 m + turret + notch).** The tall end. Rusticated
pale limestone plinth about 1.5 m high under brick piers; a tall arcaded ground floor of
three big round-arched openings — a recessed service/porte-cochere bay at the west end, the
entrance bay in the middle, a further arched bay at the east; over the middle bay a
**barrel-vaulted metal-and-glass canopy** springing off the brick, which is the entrance
marker (and, per King, the entrance is behind a fat column under it). Above the arcade,
five storeys of brown brick with paired rectangular windows between flat piers and small
square dark vents in the spandrels; then the top two storeys in **light warm plaster**,
recessed very slightly, with darker horizontal window bands. Parapet 25.10 m. The turret
closes the east end; the notch cuts the west end.

**North-east — The Embarcadero (hero, 34.0 m).** The glassy elevation. Brick piers with
**tall steel-framed glazed bays projecting between them**, running from the second floor
to the attic, so the wall reads as vertical glass ribbons on brick rather than punched
windows. Same pale plaster attic above, here clearly set back behind a terrace. The
ground floor is the Americano restaurant frontage with an outdoor patio (currently under
a clear marquee tent — **do not model the tent**, it is temporary). Toward the north-west
the elevation **steps down**, twice.

**South-west — Steuart Street (58.3 m, the longest).** Round-arched glazed openings at
ground level with limestone quoins at the pier bases, then brick with square punched
windows and two- and three-storey projecting steel-and-glass bays. Visibly the lowest
street wall on the block — about five storeys where the Mission end is eight — with a
roof-deck railing on top. This is the elevation that proves the setbacks from the
street.

**North-west — Don Chee Way / Harry Bridges Plaza (17.7 m + the notch returns).** King's
"drab brown slab": a largely blind brown brick end wall with few openings, the lowest
plateau, facing the plaza and the F-line streetcar. Build it plainly and do not invent a
window grid to make it interesting — its blankness is a documented feature.

**The turret.** Full-height brick cylinder at the east corner projecting slightly past
both faces, brick for the lower storeys, progressively more glazed above, capped by a
**dark metal drum with radiating fin canopies** — a lantern, not a cone and not a dome.
It tops out about 3.6 m above the main parapet, which agrees with the LiDAR max (28.66 m)
being one storey above the LiDAR mode (25.10 m).

**Above.** See 2.9.

### 2.5 Recognition cues (ranked)

1. **The circular turret at the east corner** with its metal lantern crown. Every source
   that says anything distinctive about this building says this.
2. **The stepped roofline** descending north-west across three plateaus, with planted
   terraces on the lower two.
3. **The pale plaster attic over brown brick over pale limestone** — a three-band
   horizontal reading that survives to thumbnail size.
4. **The concave notch** at the Mission/Steuart corner, opposing the convex turret.
5. **The arched ground floor and the barrel-vault entry canopy** on Mission.
6. Its position: the low brick block standing between the Ferry Building and the
   Financial District towers, filling a whole waterfront block.

### 2.6 Miniature translation

Style bible tier: **secondary** — a full-block, well-known building, but not a skyline
piece. The budget and the treatment sit between 501 Second (a big plain block) and the
Ferry Building (a hero).

What survives the translation: the three plateaus; the turret; the notch; the three
material bands; the arcade rhythm at ground level; the glazed-bay rhythm on the
Embarcadero; the planted decks.

What is deliberately dropped: the fake arch archivolts and keystones; window muntins and
operable sashes; the balcony rails on individual rooms; the rustication texture of the
limestone; the bamboo as individual plants (it becomes two or three massed clumps); the
marquee tent; the porte-cochere column.

The trap specific to this building is that **the street views flatter it and the aerial
does not**. From Mission it looks like an ordinary eight-storey brick block, and a
modeller working from the hero elevation alone will build a box. The massing evidence is
in the roof, so the top view is the review render that decides whether this asset is
right.

### 2.7 Massing recipe

Build order for the deterministic script. Coordinates are in the (u, v) frame of 2.3;
dimensions are the starting point, not a straitjacket — adjust after the first aerial
review render.

1. **Plateau A — the Mission block.** Extrude the footprint region u ∈ [+6, +32]
   (full depth, v −20.8 … +21.0, with the turret arc at the east corner and the concave
   notch at the south corner) from z=0 to **z=25.10**. `Toy_brick` walls.
2. **Plateau B — the middle block.** Region u ∈ [−11.4, +6], v −20.8 … +21.0, from z=0
   to **z=19.64**. `Toy_brick`.
3. **Plateau C — the plaza end.** Region u ∈ [−32.0, −11.4], v +3.3 … +21.0 (this is the
   only part of the plan west of the notch), from z=0 to **z=14.18**. `Toy_brick`.
4. **Limestone plinth.** 0.12 m proud band on all elevations, z=0 to z=1.5,
   `Toy_stone`.
5. **Arcade, Mission and Steuart.** Round-arched recessed openings, z=1.5 to z=5.4,
   about 5.0 m wide on 7.5 m centres; reveal 0.35 m; `Toy_glass` behind `Toy_stone`
   arch rings. On the Embarcadero the ground floor is a plain glazed frontage, not an
   arcade.
6. **Entrance canopy.** Over the middle Mission bay: a half-cylinder barrel vault,
   radius 2.6 m, 6.0 m wide, springing at z=5.4, projecting 2.2 m, `Toy_slate` ribs with
   `Toy_glassl` infill. The night hero's support (2.8).
7. **Shaft piers.** On all four elevations, 1.0 m `Toy_brick` piers projecting 0.12 m at
   every bay boundary, from z=5.4 to each plateau's parapet.
8. **Punched windows** (Mission, Steuart, Don Chee end): one pair per bay per floor at
   z = 5.4 + k·2.73, each 1.9 m tall, `Toy_glass` in a 0.15 m `Toy_stone` reveal. On the
   Don Chee end use **at most one column of openings** — that wall is meant to be blank.
9. **Glazed bays** (Embarcadero, and two on Steuart): 3.2 m wide, projecting 0.5 m,
   running z=5.4 to the plateau parapet, `Toy_glass` panels in a `Toy_slate` frame.
   These are what make the north-east elevation read as glass on brick.
10. **Attic band.** On plateau A only, the top two storeys (z = 19.64 to 25.10) in
    `Toy_sand`, recessed 0.30 m behind the brick below, with a `Toy_stone` sill course
    at the transition. This is the single strongest horizontal move on the building.
11. **Parapets.** A 0.9 m `Toy_brick` ring with a `Toy_stone` coping on each plateau, and
    a `Toy_steel` railing line on B and C (the terrace decks).
12. **The turret.** Cylinder, centre (27.6, −16.5), radius 4.5 m, 24 segments, from z=0
    to **z=28.66**. `Toy_brick` to z=14.18, then alternating `Toy_glass` bands and
    `Toy_brick` piers to z=25.6; then the **crown**: a `Toy_slate` drum z=25.6 to 27.6
    (radius 4.7 m, slightly proud) and eight radiating `Toy_slate` fin canopies at
    z=27.6 to **28.66**, tips at radius 6.2 m. This block sets the bounding-box top and
    must land exactly on 28.66.
13. **Roof terraces.** On plateaus B and C: `Toy_leaf` deck panels laid as three or four
    large rectangles with `Toy_stone` paths between them, inset 1.2 m from the parapet.
    Do **not** cover the whole plateau — the real decks are a grid of planted panels with
    circulation between.
14. **Spa pavilion.** A 9 x 6 m, 3.2 m tall `Toy_sand` box with a `Toy_glassl` band, on
    plateau A's roof near the notch corner, with two `Toy_sage` bamboo clumps beside it.
    Nothing here may out-top the turret.
15. **Roof plant.** On plateau A's Mission end: four or five `Toy_steel` blocks (max
    2.0 m), two `Toy_slate` vents, one hatch. This is where the satellite imagery shows
    the mechanical field; keep it grouped there and leave the terraces clean.
16. Bevel 0.10 m, 2 segments on the plateau masses and the turret; 0.04 m, 1 segment on
    applied bands, piers, copings and reveals.

**The notch and the turret are the two junctions worth care.** Cut the notch as part of
the plateau-A profile curve, not as a boolean; build the turret as a cylinder unioned
into the wall profile at authoring time so no interior faces survive. Both rules exist
because this repo's optimize pass and normals gates punish leftover interior geometry.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_brick` | `c96f4a` | the whole masonry mass on all three plateaus, piers, parapets, turret shaft — **the identity colour** |
| `Toy_sand` | `ece4d4` | the two-storey plaster attic band on plateau A, the spa pavilion |
| `Toy_stone` | `d9d2c2` | limestone plinth, arch rings, copings, window reveals, roof paths |
| `Toy_glass` | `2a4d73` | all punched windows and the glazed bays |
| `Toy_glassl` | `6f95b8` | the entrance canopy glazing and the spa band |
| `Toy_slate` | `39434f` | the turret crown drum and fins, bay-window frames, canopy ribs, roof vents |
| `Toy_steel` | `9aa0a6` | roof plant blocks, terrace railings |
| `Toy_leaf` | `6d8558` | the planted roof-terrace decks |
| `Toy_sage` | `8f9b86` | the bamboo clumps by the spa |
| `Toy_glassl_Glow` | `6f95b8` | **the turret's glazed bands — the night hero** |
| `Toy_gold_Glow` | `caa64a` | the entrance canopy's underside strip |
| `Toy_glass_Glow` | `6f95b8` | scattered lit guest-room windows |

**Brick note.** `Toy_brick` at `c96f4a`, following `2-south-park`'s recorded lesson: do
not darken it toward `Toy_rust` to chase King's word "brown". The real brick is a muted
red-brown, `c96f4a` is the palette's brick, and the building's job in the aerial is to
read warm against the Ferry Building's grey-cream and One Market's dark glass. If the
first aerial says it is too orange, record the deviation rather than inventing a colour.

**Roof note.** The lower plateaus are *gardens*, not membrane. `Toy_leaf` decks with
`Toy_stone` paths, and the grey plant grouped on plateau A only. A pale membrane on the
terraces would be both wrong and, per the `524-second`/`501-second` findings, the wrong
value under the app's lighting.

**Night state (required).** Glow surfaces must be **thin shells proud of the opaque
surface behind them** — the app draws `_Glow` as a separate overlay that is visible by
day, and a closed glow shell is two alpha layers, so it will tint the facade beneath it.
Never author a primary surface as glow, and never wrap the turret in a closed glow
cylinder: use proud glazing *bands*.

Hero glow: **the turret's glazed bands**, so the corner reads as a lantern on the
waterfront — which is exactly what the seven circular suites are. Supporting: the
`Toy_gold_Glow` strip under the entrance canopy, and a scatter of lit guest-room windows
across the three plateaus. This is a 200-room hotel, so an irregular scatter over roughly
a fifth of the openings is the truthful pattern — not a uniform grid, not one lit floor,
and not nine-tenths lit.

The `_Glow` material's **base colour is its night appearance** (the app's night layer is
unlit and draws the material's own baked colour). Do not rely on a Blender emission
strength to make a too-dark glow look right in the night render — check the base colour
itself.

### 2.9 Top surface

2,133 m2 across three levels, and the only view that proves this asset is right.

The composition, from the satellite imagery: **plateau A** (the Mission end, 25.10 m) is
the working roof — pale membrane with the mechanical field grouped on it, the turret
rising off its east corner, and the spa pavilion and its bamboo tucked at the notch
corner overlooking Steuart. **Plateau B** (19.64 m) and **plateau C** (14.18 m) are the
garden: large rectangular planted decks in a grid with paved circulation between them,
edged by railings, stepping down and away to the north-west. The vent pavilion's circular
louvre sits in the notch beside plateau C but is **not part of this asset**.

Design intent: the eye should read *one tall block with a lantern, and a cascade of green
going down toward the plaza*. Keep the terraces green and open, keep the plant confined
to plateau A, and keep the three parapet lines crisp — from directly above, the three
parapet rings are what encode the massing.

### 2.10 Scope

**In the GLB:** the hotel — three plateau masses, the turret and its crown, the notch,
the limestone plinth, the arcaded ground floor, the entrance canopy, the punched windows
and glazed bays on all four elevations, all three parapets, the planted terraces, the
spa pavilion and bamboo, the roof plant.

**Not in the GLB:** the Muni vent-shaft pavilion in the notch (OSM 260290226); Mission,
Steuart, The Embarcadero, Don Chee Way; the Audiffred Building; Harry Bridges Plaza; the
Embarcadero marquee tent; street trees; sidewalk; vehicles; people; plinths; cameras or
lights.

### 2.11 Triangle budget

Cap **26,000** — above 501 Second's 20,000, justified by 155 m of public elevation across
four public faces, three separate parapet rings and a 24-segment cylinder with a
radiating crown. Suggested split: three plateau masses, parapets and the attic band ~4.5k;
piers ~2.5k; arcade and openings ~2.0k; punched windows ~7.0k; glazed bays ~3.0k; the
turret and crown ~3.5k; terraces, spa and plant ~2.5k; entrance canopy ~1.0k.

**The punched windows are the risk**, as always. If the first build lands over budget,
cut window bays before cutting anything on the list of five recognition cues — and cut
the Don Chee end first, since that wall is supposed to be blank.

### 2.12 Draft manifest entry

```json
{
  "id": "8-mission",
  "file": "8-mission.glb",
  "anchor": [
    -122.3932805,
    37.7937365
  ],
  "targetHeightM": 28.66,
  "cat": 7,
  "name": "1 Hotel San Francisco (8 Mission Street)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`"estimated": false` because the crest (28.66 m) and both upper roof planes (25.10 m,
19.64 m) are LiDAR measurements; only the lowest plateau is derived. `cat: 7` is the
hotel category — the same one `fairmont` and `22-south-park` carry.

Draft `pipeline/lib/landmarks.mjs` entry:

```js
{
  id: '8Mission',
  name: '1 Hotel San Francisco (8 Mission Street)',
  lon: -122.3932805,
  lat: 37.7937365,
  height: 28.66,
  exclude: 10,
  // Camera bearing = 180 - yaw with +z south, so yaw 90 stands the eye due EAST
  // — the bisector of the Mission elevation (135.4 deg) and the Embarcadero
  // elevation (45.4 deg), with the turret on the corner between them. Both are
  // hero elevations and the turret only reads from the corner. 320 m suits a
  // 28.66 m crest (cf. 181SouthPark 190 for 16.5 m, 49SouthPark 165 for 13 m).
  // No `key`: the waterfront's numbered destination is the Ferry Building.
  camera: { distance: 320, yaw: 90, pitch: 24 },
}
```

### 2.13 Integration notes (for later, not this task)

- **New landmark, Case B.** The id exists in neither `app/public/sf-assets/landmarks_manifest.json`
  nor `pipeline/lib/landmarks.mjs`, so integration needs a registry entry **and a re-bake
  of the affected tiles**, or the baked procedural block on this footprint will intersect
  the GLB. The cell is **`23_10`** (local x 3891.1, z −2623.8).
- **What the bake currently puts here.** `app/public/tiles/ctx/23_10.json` records
  procedural pick record id `103461` at the anchor: a 64.4 x 41.8 m block **24.2 m tall**.
  That is 4.5 m shorter than the asset's crest but it fills the whole footprint, so
  without the exclusion the GLB and the procedural block interpenetrate over the entire
  plan. This asset cannot be judged before the re-bake.
- **Exclusion radius: `exclude: 10`.** The safe window is **4.92 < r < 17.30 m**, measured
  against `excluded()`'s real test in `pipeline/buildings.mjs` (ring **centroid** inside
  the circle **or any ring vertex** inside it), against both bake sources:

  | Ring | centroid distance | nearest vertex |
  |---|---|---|
  | The hotel, OSM 193054134 | **4.92 m** | 11.93 m |
  | The hotel, DataSF `201006.0001079` | **4.37 m** | 10.94 m |
  | Muni vent pavilion, OSM 260290226 | 26.23 m | **17.30 m** |
  | Muni vent pavilion, DataSF `201006.0017562` | 26.82 m | 17.35 m |
  | Audiffred Building, OSM 193054136 | 63.90 m | 60.36 m |

  The lower bound is our own **centroid** (4.92 m), not our nearest vertex, because the
  anchor is the OBB centre and the L-shaped plan puts its centroid 4.92 m off it. The
  upper bound is the vent pavilion's nearest **vertex** (17.30 m), which is what fires
  the test. `r = 10` sits with 5.1 m of margin below and 7.3 m above. **The footprint
  half-diagonal is 38.32 m and would delete the pavilion, so do not use it** — this is
  the same trap 150 South Park and the Earl Warren Building document.
- **Verify against Overture before committing the radius.** The two rings above are OSM
  and DataSF; the bake's actual input is
  `pipeline/data/overture_buildings.geojsonseq`, which traces some SF buildings
  independently and can contribute a *second* ring for the same building (see
  `sf3d-exclusion-two-rings`). Re-measure both bounds against it, and prove the result
  from **penetration depth** into the asset's own (u, v) rectangle before and after the
  bake, not from a changed-file count.
- **The vent pavilion must survive.** It is a real Muni subway vent structure on the same
  parcel, it is not in the GLB, and if the re-bake removes it the north corner of the
  block becomes an empty lot.
- `loadRadius`: the default formula gives `max(2500, 28.66 × 30) = 2500` m. Take the
  default. `alwaysLoaded` is not warranted — this is not a skyline piece.
- **Judge it against `ferry-building`.** They face each other across 220 m of the
  Embarcadero and will be in the same frame constantly. If the hotel reads as tall as or
  busier than the Ferry Building, the massing or the palette is wrong.
- **`BATCH: yes` applies.** Run the bake and the full QA on it, then
  `git checkout -- app/public/tiles api/_data` before committing, and commit source only.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 28.66 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~74.1 x 56.5 m is expected)
- [ ] Footprint proportion preserved: the building must measure 64.08 x 42.07 m along its own axes, and the **L** must be present — a full rectangle is a failure
- [ ] Three parapet planes land at 25.10 m, 19.64 m and 14.18 m and are separately visible from directly above
- [ ] Turret present, ~9.0 m across, crown at 28.66 m; notch present and **concave**
- [ ] Triangles at or under 26,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the turret glazing bands, the canopy strip and scattered windows; every glow shell proud of the opaque surface, none closed
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual ≤ 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes; **no vent pavilion**
- [ ] Six review renders + `8-mission-steps.png` + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

1. **Where the two setbacks fall in plan — the weakest number here.** The three *heights*
   are measured (LiDAR mode 25.10, median 19.64, and a fourth-storey derivation for the
   lowest), and the *fact* of terracing is confirmed twice over (King; LDA's "series of
   stepped floors … cascade of roofs"). What no source states is the u-coordinate of each
   setback. The boundaries in 2.7 (u = +6 and u = −11.4) come from reading the roof
   composition off z21 satellite imagery — the extent of the white mechanical roof versus
   the green decks — plus the constraint that the LiDAR mean (19.65 m) and σ (6.01 m) must
   come out right. Treat them as **estimated**, re-derive them from a better aerial or an
   oblique before modelling, and note in REPORT.md what you changed. A wrong step
   *position* is a much cheaper error than a wrong step *count*, so keep three plateaus
   even if you move them.
2. **The lowest plateau's height (14.18 m) is derived, not measured.** King says
   "four-story wings", the derived storey heights (ground 5.99 m, typical 2.73 m) give 14.18 m, and the LiDAR summary is
   consistent with a substantial area well below the median — but no statistic isolates
   it. If a rectified elevation from Don Chee Way disagrees, believe the elevation.
3. **`hgt_maxcm` = 28.66 m is being taken as the crest, which this repo's own history says
   to distrust.** The check applied: it is only 1.5σ above the mean (contrast 592 Third,
   where the equivalent figure was a 6σ street-tree artifact), it sits 3.56 m — almost
   exactly one storey — above the modal roof plane, this footprint has **no party wall**
   for a neighbouring tower to bleed into (contrast the Earl Warren Building), and the
   Street View panoramas show a turret crown standing roughly one storey proud of the
   parapet at that corner. Four independent reasons, so it is recorded as measured. If
   the executing agent's own photogrammetry puts the crown elsewhere, the photogrammetry
   wins.
4. **Storey heights (ground 6.0 m, typical 2.73 m) are derived from two LiDAR planes and
   two published storey counts**, and the ground floor is unusually tall as a result. It
   is consistent with the arcaded double-height restaurant and lobby in the photographs,
   but it is arithmetic, not measurement. Verify against a rectified Mission Street
   elevation before spacing the window rows.
5. **`Toy_brick` may read too orange.** King's "brown brick" and the palette's `c96f4a`
   are not the same colour. Follow 2 South Park's precedent, keep `Toy_brick`, and record
   the deviation rather than inventing a hex.
6. **The Embarcadero ground floor is currently under a temporary clear marquee tent** in
   every recent photograph and in the satellite imagery. It is not architecture. Model
   the restaurant frontage behind it.
7. **The building is a lease on Muni land with a subway vent shaft carved out of its
   block.** That is why the plan is an L rather than a rectangle. Anyone tempted to
   "clean up" the footprint into a rectangle is deleting a real, surveyed, still-standing
   structure — and the integration exclusion in 2.13 is sized around it.
8. **This asset will always be seen next to the Ferry Building.** That is a harder test
   than the SoMa blocks face, where the neighbours are procedural. Judge every aerial
   render with `ferry-building` in mind.
