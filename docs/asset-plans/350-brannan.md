# 350 Brannan Street — SF-SIM asset plan

A 1929 reinforced-concrete industrial building at the corner of Brannan Street, Jack London
Alley and Varney Place, one lot northeast of South Park. Not a monument and — importantly —
**not another brick warehouse**: it is a white-painted concrete box whose Brannan elevation
is a colonnade of storefront bays *bookended by two round-arched portals*, under two floors
of big multi-light steel-sash industrial windows. It is a corner building on three sides,
which is why the leasing copy sells "window lines on 3 sides", and it is the second plan in
this set for an ordinary street building rather than a civic landmark.

Its immediate neighbour `380-brannan` is already in the manifest. The two are the same block
and the same era and they must not end up looking like the same asset: 380 is raw red brick
with a coral band, 350 is white painted concrete with arched portals. Build the difference.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/350-brannan/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `350-brannan` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3935234, 37.7810229` |
| Target height | **13.85 m** to the roof penthouse crest; main parapet ~12.9 m; roof deck 12.02 m |
| Footprint | 21.60 m (Brannan frontage, SE) x 24.22 m (Jack London Alley, NE); 537.3 m2, measured |
| Triangle cap | 10,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 350 Brannan Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 350 Brannan Street in San Francisco and deliver it
as a downloadable, validated GLB.

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
7. `artifacts/380-brannan/` — the closest reference implementation in scale, era and site
   (same block, same 45° heading, same secondary-building detail budget). Read it for the
   *method*, not the *look*: 350 must not come out as a recolour of 380.
8. `docs/asset-plans/350-brannan.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A three-storey white-painted concrete box, flat roof, continuous parapet, on a
  45°-rotated corner lot with **three finished elevations** and one blind party wall
- The **two round-arched portals** at the two ends of the Brannan Street ground floor,
  with their pale cast-stone surrounds — this is the building's whole identity
- The ground-floor colonnade between them: square piers with recessed storefront glazing
- Two upper floors of **large multi-light steel-sash industrial windows**
- The black zig-zag **fire escape** on the Jack London Alley elevation
- A designed flat roof: the large raised central penthouse/monitor, skylights, a
  mechanical cluster, and the parapet ring

## Research 350 Brannan Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- All three exposed elevations (Brannan SE, Jack London Alley NE, Varney Place NW) plus
  the blind southwest party wall
- Aerial and roof/top views (the raised penthouse, skylight and mechanical layout)
- Ground-level views
- Day and night appearance
- The bay count and window rhythm of the Brannan elevation — the dossier's reading of
  **two arched portals plus five rectangular bays** is *inferred* from photography partly
  screened by street trees and must be confirmed
- The Varney Place (northwest) elevation, which this dossier never observed directly —
  see 2.15, it is the largest gap in the research
- Whether the LiDAR maximum of 13.85 m is the roof penthouse or a raised parapet element

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**Two source traps are already known and resolved in 2.1 — re-check them, do not silently
re-inherit the wrong value:** OSM `height=12` is the LiDAR *roof-deck median*, not the
crest, and must never be the target height; and the neighbourhood's "brick warehouse"
reputation (plus the South End Historic District literature, which describes brick
warehouses and does **not** cover this lot) will push you toward a brick building — the
assessor records construction class **C** and every photograph shows painted concrete.

## Create a reference dossier

Write `artifacts/350-brannan/REFERENCE.md` containing: source links and what each
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

This is a **secondary building** in the style bible's detail budget (§21), not a hero
landmark: clear massing, one strong facade rhythm, a simple designed roof, and exactly
one identity cue carried hard — the paired arched portals. Resist adding hero-tier
ornament, and in particular resist modelling the cast-stone voussoirs as individual
stones; they are sub-pixel at city scale.

The finished asset must be immediately recognizable as 350 Brannan Street, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1929 building: concrete body, parapet, all elevations' openings, the two
arched portals, the Jack London Alley fire escape, and the roof furniture.

Do not include unrelated surrounding city geometry: Brannan Street, Jack London Alley,
Varney Place, the neighbouring buildings on the southwest party wall, South Park, street
trees, the sidewalk, parked cars, people, plinths, cameras or lights. Temporary context may
appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 10,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The Brannan Street
entrance front faces **southeast, bearing 135.8°**; the building is rotated roughly 45°
off the world axes, so build directly on the measured footprint polygon in 2.3 rather
than modelling an axis-aligned box and rotating it. Record the measured heading in
`REPORT.md`.

**Height normalization:** the tallest geometry in the export (the roof penthouse) must
land at exactly **13.85 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/350-brannan/build_350_brannan.py` (deterministic build script),
`artifacts/350-brannan/350-brannan.blend`, and `artifacts/350-brannan/350-brannan.glb`.
The script must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`350-brannan-top.png`, `350-brannan-north.png`, `350-brannan-east.png`,
`350-brannan-south.png`, `350-brannan-west.png`, plus `350-brannan-contact-sheet.png`,
at least one high three-quarter aerial beauty render `350-brannan-aerial.png`, and a
night render `350-brannan-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the parapet ring, the raised
penthouse, skylights and mechanical cluster; the aerial view uses the style bible's camera
assumptions (30-50 degrees down, long lens). Simple tabletop lighting, neutral warm
background, minimal depth of field, and every image must depict the same exported model.

Aim the hero aerial from the **east**, so the Brannan and Jack London Alley elevations and
the roof are all in frame at once — that is the view the app's camera actually gets, and
the southwest party wall is the one face the city never shows.

## Validate the exported GLB

Re-import `350-brannan.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/350-brannan/validation.json` and
`artifacts/350-brannan/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **33 x 33 m** even though the
building is 21.6 x 24.2 m — that is the expected consequence of a ~45° real-world heading,
not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "350-brannan",
  "file": "350-brannan.glb",
  "anchor": [
    -122.3935234,
    37.7810229
  ],
  "targetHeightM": 13.85,
  "cat": 3,
  "name": "350 Brannan Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/350-brannan.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | 1929 | SF Assessor secured roll, block 3775 lot 016 (consistent 2020-2025) |
| Storeys | **3** | SF Assessor roll AND every building permit 1985-2026 (`number_of_existing_stories = 3`) — no conflict |
| Construction | Assessor construction class **C** (reinforced concrete); painted, not brick | SF Assessor roll; confirmed visually — every elevation is smooth painted wall, no brick coursing anywhere |
| Property class | Industrial (`IND`); in continuous **office** use since ~1990 | SF Assessor roll (class) vs permits 1990-2026 (`existing_use = office`) |
| Block / lot (APN) | 3775 / 016 | SF Assessor; DataSF parcels; DataSF footprints (`mblr = SF3775016`) |
| Lot area | 5,797 sq ft = 538.6 m2 | SF Assessor — matches the footprint, so the building covers the whole lot |
| Footprint | 537.3 m2; 21.60 m (SE, Brannan) x 24.22 m (NE, Jack London Alley) | DataSF LiDAR building footprint, reprojected — **measured** |
| OSM footprint (cross-check) | 534.2 m2 | OSM way/113545692 — agrees with DataSF within 0.6% |
| Parcel polygon (cross-check) | 577 m2, 22.05 x 26.15 m | DataSF parcel `acdm-wktn` — the lot, slightly larger than the building |
| Building area | 18,055 sq ft (assessor) / 19,662 sq ft (listing) | ~3.1x the footprint either way — confirms 3 full floors |
| Roof deck height | 12.02 m above ground | DataSF LiDAR `hgt_median_m` — **measured** |
| Maximum feature height | 13.85 m above ground | DataSF LiDAR `hgt_maxcm` — **measured** |
| Main parapet crest | ~12.9 m | *inferred*, roof deck + ~0.9 m parapet |
| Ground elevation | 10.55 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Frontage heading | Brannan front faces 135.8° (SE); Jack London Alley 44.5° (NE); Varney Place 315.9° (NW); party wall 225.3° (SW) | measured from the footprint polygon |
| Exposed elevations | **three** (SE, NE, NW); SW is a party wall | measured site geometry, corroborated by listing copy "window lines on 3 sides" |
| Parapet | Present, braced 1993 | permit 1993-02-11 "add blocks & straps per parapet plans" |
| Freight elevator | Removed 2023 | permit 2023-12-13 — evidence of the industrial original, gone from the exterior |
| No vertical additions | none 1985-2026 | full permit history is interior work, reroofing (1990, 2010), elevator and parapet bracing — so the 2010 LiDAR crest is still current |

### 2.2 Sources

- https://www.openstreetmap.org/way/113545692 — footprint, `building=yes`, `height=12`. **The way carries no address tags**; it was identified as 350 Brannan by parcel, see 2.15
- `https://data.sfgov.org/resource/ramy-di5m` (DataSF Addresses with Units) — 350 BRANNAN ST -> parcel 3775016, point 37.780947 / -122.393435
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — lot polygon, `from_address_num`/`to_address_num` = 350, zoning CMUO
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — authoritative footprint polygon and the 12.02 m / 13.85 m heights
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — 1929, block/lot, 3 storeys, class C, lot area
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits, 25 permits 1985-2026) — storey count, parapet bracing, use history, Jack London Alley entry
- Google Street View, Brannan Street panos (capture May 2025), several headings — SE elevation: white paint, twin arched portals, storefront colonnade, steel-sash upper windows, parapet
- Google Street View, Brannan/Jack London Alley corner pano (capture May 2025) — the three-quarter view showing the SE and NE elevations together, and the fire escape
- Google Maps satellite (Airbus / Maxar / Vexcel imagery, 2026) — light membrane roof, raised central penthouse, skylights, mechanical cluster, parapet ring
- Commercial listing copy (LoopNet / Showcase / Tandem) — 19,662 sq ft, 1929, "high ceilings", "window lines on 3 sides"
- https://noehill.com/sf/landmarks/sf_south_end.asp — South End Historic District (1867-1935, brick warehouses). Consulted and **rejected as context**: the district is bounded by Stillman/First/Ritch/King and does not reach this lot, see 2.15

### 2.3 Orientation and placement

The building occupies its entire lot at the junction of three streets: Brannan Street to
the southeast, Jack London Alley to the northeast, and Varney Place to the northwest —
the latter two meet at the building's north corner. Only the southwest side is shared,
with 358 Brannan Street and one untagged neighbour. It is rotated about 45° from the
world axes, like the whole SoMa grid.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
counter-clockwise, already centred on the anchor `-122.3935234, 37.7810229`:

```
(  1.094, -15.780)
( 16.574,  -0.721)
( -0.716,  16.241)
(-16.502,   0.922)
(-16.205,   0.630)
(  1.048, -16.797)
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(1.094,-15.780) -> (16.574,-0.721)` | 21.60 m | SE 135.8° | **Brannan Street front** |
| `(16.574,-0.721) -> (-0.716,16.241)` | 24.22 m | NE 44.5° | **Jack London Alley** |
| `(-0.716,16.241) -> (-16.502,0.922)` | 22.00 m | NW 315.9° | **Varney Place** |
| `(-16.205,0.630) -> (1.048,-16.797)` | 24.52 m | SW 225.3° | southwest party wall (blind) |

The two remaining 0.42 m and 1.02 m segments are corner jogs; keep them, they cost nothing
and they keep the model honest to the survey.

Because of the 45° heading the axis-aligned bounding box is ~33 x 33 m. That is correct.

### 2.4 What each side shows

**Southeast (Brannan Street front)** — The hero elevation. A white/off-white painted wall,
three storeys, organised top to bottom as: a plain parapet with small raised attic panels
over the pier positions; a blank frieze band; a top floor of **large multi-light steel-sash
industrial windows** with dark frames; a blank spandrel; a middle floor of the same
windows, read as a more horizontal band; and a tall ground floor of **square piers framing
recessed storefront glazing**, pale blue-green and slightly reflective, with solid spandrel
panels below. The ground floor is closed at **both ends by a round-arched portal** with a
pale, lightly textured cast-stone surround — the southwest one a recessed entry, the
northeast one the main "350" address entrance with its tenant signage. Those two arches
against a plain colonnade are the building's signature.

**Northeast (Jack London Alley)** — The same white wall and the same window rhythm,
uninterrupted by the arched portals, with the **black zig-zag fire escape** hung off the
upper two floors — the single strongest secondary cue. Ground-floor openings here are
service doors and a secondary accessible entrance (the 2008 permits moved the ground-floor
suite's designated entry to this side). The alley is narrow, so this face is only ever seen
obliquely in the real world — but the app's aerial camera sees it plainly, so build it
properly.

**Northwest (Varney Place)** — *Not directly observed; see 2.15.* Expected to continue the
same painted wall and window bays, with service openings at ground level. Model it as a
plainer version of the Jack London Alley elevation — regular bays, no arch, no fire escape
— and say so in `REPORT.md`.

**Southwest** — Party wall against 358 Brannan Street, whose nearest footprint vertex is
1.15 m away. Blind, unpainted, no openings. Model it as a flat wall in the body colour; it
is never visible in the app.

**Top** — A bright light-gray membrane roof inside a continuous parapet. Visible from
satellite: a **large raised rectangular penthouse/monitor** roughly centred on the roof and
set slightly toward the Varney Place side (this is almost certainly what the 13.85 m LiDAR
maximum measures), a row of small rectangular **skylights** on the deck southwest of it, a
second small skylight cluster, and a **mechanical/HVAC cluster** toward the Jack London
Alley edge. Diagonal seams run across the membrane. This is the surface the app's camera
sees most — design it, do not leave it flat.

### 2.5 Recognition cues (ranked)

1. **The two round-arched portals bookending the Brannan colonnade** — nothing else on the
   block does this, and it survives to thumbnail size
2. A white-painted three-storey concrete box on a 45° corner site, finished on three sides
3. Two floors of large multi-light steel-sash industrial windows
4. The black zig-zag fire escape on the Jack London Alley elevation
5. The big raised roof penthouse, centred and clearly proud of the parapet

### 2.6 Miniature translation

**Preserve**

- The single chunky box and its real 45° heading
- Both arched portals, as real arches, at the two ends of the Brannan ground floor
- The three-finished-sides / one-blind-side asymmetry
- The white body against dark glazing — the value contrast *is* the building

**Simplify / exaggerate**

- The Brannan ground floor becomes exactly 2 arches + 5 pier-framed bays; the upper floors
  become 5 clean window bays per long elevation, all identical
- Cast-stone voussoirs become one flat, slightly warmer arch surround band 0.3 m proud
- Steel-sash mullion grids become a single flat glazing panel recessed 0.2 m — no muntins
- The arches are widened and heightened slightly so they still read at thumbnail size; this
  is the one place semantic exaggeration is spent
- The fire escape becomes two chunky balcony slabs plus rails and one diagonal stair slab —
  no individual treads
- Roof clutter becomes one penthouse block, four skylight boxes, and one HVAC cluster of
  two blocks
- The tenant signage, "350" numerals and lease banners are dropped — sub-pixel, and dated

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 footprint from z=0 to z=12.02, `Toy_cream`.
2. Ground floor, z=0 to z=4.40, SE elevation: two round-arched portals 3.0 m wide,
   rise 1.1 m, 10-segment arcs, at the two ends; between them five bays 2.6 x 3.0 m
   recessed 0.25 m, `Toy_glassl`, separated by 0.7 m square piers left in body colour.
   Arch surrounds: 0.3 m proud band, `Toy_trim`. Arch reveals `Toy_ink`.
3. Ground floor on the NE (Jack London Alley) and NW (Varney Place) elevations: five plain
   bays each, same size, no arches; one 2.6 m service door `Toy_roofd` on each.
4. String course: 0.18 m `Toy_trim` band at z=4.40, SE/NE/NW only.
5. Middle floor, z=4.90 to z=7.90: 5 bays per finished elevation, openings 2.4 x 2.4 m,
   recessed 0.2 m, `Toy_glass`.
6. Top floor, z=8.20 to z=11.40: 5 bays per finished elevation, openings 2.4 x 2.8 m,
   recessed 0.2 m, `Toy_glass` — taller than the middle floor, which is what makes the
   industrial sash read.
7. Frieze: blank body-colour band z=11.40 to z=12.02.
8. Parapet: z=12.02 to z=12.90, following the footprint, 0.35 m thick, `Toy_cream` with a
   `Toy_trim` cap; small raised attic panels 0.25 m proud and 0.3 m higher over the five
   pier positions on the SE elevation only.
9. Roof deck at z=12.02, `Toy_stone` (the real membrane is light — do not default to a dark
   deck). Roof penthouse 9.0 x 6.0 m, centred and offset ~2 m toward Varney Place, from
   z=12.02 to **z=13.85** `Toy_cream` — this sets the bounding-box top and must land exactly
   on 13.85. Four skylight boxes 2.4 x 1.6 x 0.35 m `Toy_glassl` southwest of the penthouse;
   two HVAC blocks (2.2 x 1.6 x 1.0 m and 1.6 x 1.2 x 0.8 m) `Toy_steel` toward the NE edge.
10. Fire escape on the NE elevation, right of centre: two balcony slabs 3.2 x 0.9 x 0.15 m at
    z=5.2 and z=8.5, `Toy_ink`, with 1.0 m rails and one diagonal stair slab between them.
11. Southwest party wall: flat `Toy_cream`, no openings.
12. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | the painted body on all four elevations, parapet, roof penthouse |
| `Toy_trim` | `#f3efe6` | arch surrounds, string course, parapet cap |
| `Toy_glass` | `#2a4d73` | middle- and top-floor steel-sash windows |
| `Toy_glassl` | `#6f95b8` | ground-floor storefront glazing, roof skylights |
| `Toy_stone` | `#d9d2c2` | roof deck membrane |
| `Toy_roofd` | `#45454a` | service doors |
| `Toy_steel` | `#9aa0a6` | HVAC blocks |
| `Toy_ink` | `#3a3530` | fire escape, arch reveals |
| `Toy_glass_Glow` | `#2a4d73` | lit upper windows at night |
| `Toy_glassl_Glow` | `#6f95b8` | the two lit arched portals at night |

Note on the body colour: the real paint reads warm white in sun and cool light gray in
shade. `Toy_cream` is the closest palette entry; `Toy_white` (`#f7f4ec`) is a defensible
alternative if the aerial render looks chalky against the `Toy_stone` roof. Decide from the
render and record the decision in `REPORT.md`. Do **not** reach for `Toy_brick` — see 2.15.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a primary surface
must never be authored as glow. Hero glow: the two arched portals, lit as entrances — they
are the identity feature and lighting them is honest, not signage. Supporting accent: a
scatter of lit upper windows on the Brannan and Jack London Alley elevations (not all of
them — five or six across both faces is plenty). The roof penthouse does not glow.

### 2.9 Top surface

A flat roof 12 m up in a district the camera flies over constantly, and this one has a real
piece of geometry on it: the penthouse is roughly 9 x 6 m and stands 1.8 m proud, so it is
legible from the aerial camera and it is what sets the model's height. Group four skylight
boxes in a row on the southwest half, the HVAC pair off-centre toward the alley edge, and
keep the parapet ring continuous so the deck never reads as an open tray. Because the real
membrane is light, get separation from the *cap* (lighter `Toy_trim`) and from the *clutter*
(darker `Toy_steel`), not by darkening the deck.

### 2.10 Scope

**In the GLB:** the single 1929 building — concrete body, parapet, all elevations' openings,
both arched portals, the Jack London Alley fire escape, roof deck and roof furniture

**Not in the GLB:** Brannan Street, Jack London Alley, Varney Place, the neighbouring
buildings, South Park, street trees, sidewalk, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 10,000 — a secondary building, but with three finished elevations and two arches rather
than 380 Brannan's one-and-a-half, so slightly above that asset's 9,000. Suggested split:
body and parapet ~2k, upper window bays (two floors x three elevations) ~3.5k, ground-floor
bays and the two arched portals ~2.5k, roof furniture and penthouse ~1.5k, fire escape ~0.5k.

### 2.12 Draft manifest entry

```json
{
  "id": "350-brannan",
  "file": "350-brannan.glb",
  "anchor": [
    -122.3935234,
    37.7810229
  ],
  "targetHeightM": 13.85,
  "cat": 3,
  "name": "350 Brannan Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark, Case B.** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: '350Brannan'`, `lon: -122.3935234`, `lat: 37.7810229`, `height: 13.85`,
  `exclude: 8`, `camera: { distance: 230, yaw: 55, pitch: 26 }`) and re-bake the affected
  tiles, or the baked procedural building on this exact footprint will intersect the GLB.
- **Exclusion radius, measured.** `excluded()` in `pipeline/buildings.mjs` drops a footprint
  when its centroid **or any ring vertex** falls inside the radius. Measured from this
  anchor:
  - our own footprint's centroid sits at ~0 m, so any radius > ~1 m drops this building;
  - the nearest **neighbour** ring vertex is at **13.79 m** (358 Brannan Street and the
    untagged party-wall neighbour, both southwest);
  - the next neighbours are at 19.6 m and 20.0 m.

  So the safe band is roughly 1 m to 13.8 m and **8 m sits in the middle of it**. Do not
  raise it past 12 without re-running the check — this is a full-lot corner building with a
  party wall 1.15 m away, and a generous radius eats the neighbour. Re-verify against the
  actual baked footprint source before committing, then run `pipeline/audit.mjs` 1.6 and
  `pipeline/verify-rebake.mjs`.
- `loadRadius`: the skill's default formula gives `max(2500, 13.85 * 30) = 2500` m. Take the
  default; at 2.5 km a 14 m building is far below a pixel, so the carved-out gap is
  illegible.
- **Batch mode applies.** `380-brannan`, `362-brannan` and `370-brannan` are the same block
  and in flight in parallel sessions. Follow "Batch mode" in
  `docs/asset-pipeline/ADDRESS-TO-ASSET.md`: run the bake and do the full QA on it, then
  `git checkout -- app/public/tiles api/_data` before committing, and let
  `docs/asset-pipeline/BATCH-INTEGRATE.md` bake the city once for the whole batch.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 13.85 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~33 x 33 m is expected)
- [ ] Triangles at or under 10,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the two arched portals and the scattered lit windows; glow shells proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The OSM way carries no address.** Nominatim resolves "350 Brannan St" onto the *Brannan
  Street roadway* by TIGER interpolation, and no building on this block is tagged
  `addr:housenumber=350`. The identification here runs address -> DataSF parcel APN
  3775-016 -> parcel centroid -> the OSM/DataSF footprint that contains it, cross-checked by
  area (537 m2 building vs 5,797 sq ft = 538.6 m2 lot). It is solid, but it is a derivation,
  not a tag: confirm it against a photograph of the "350" address plate before modelling.
- **OSM `height=12` is the roof-deck median, not the crest.** It matches the LiDAR median
  (12.02 m) almost exactly, which makes it look trustworthy. The crest is ~12.9 m at the
  parapet and 13.85 m at the penthouse. This is the trap the plans README warns about,
  again, in a building where the tag looks plausible.
- **Whether 13.85 m is the penthouse or a raised parapet element is *inferred*.** The
  satellite view shows a clearly raised central block and that is the natural candidate, but
  the LiDAR maximum is a single cell. Either way the bounding-box top lands on 13.85; only
  the shape of what tops out is at stake.
- **The brick trap.** Everything around this building is a brick warehouse, the South End
  Historic District literature describes brick warehouses, and the neighbour asset
  `380-brannan` *is* brick. This one is not: the assessor records construction class C and
  every photograph shows smooth painted concrete with no coursing. Also note the historic
  district is bounded by Stillman/First/Ritch/King and does **not** contain this lot, so
  district-level descriptions are not evidence about this building.
- **The Varney Place (northwest) elevation was never directly observed.** Neither Varney
  Place nor Jack London Alley has Street View car coverage, and the satellite view only
  shows the roof edge. The dossier's treatment of that face in 2.4 is entirely *inferred*
  from the Jack London Alley elevation. This is the largest research gap and the executing
  agent should attack it first — pedestrian panoramas, listing photography, or planning
  documents.
- **The bay count is *inferred*.** The Brannan elevation reading of two arched portals plus
  five rectangular bays comes from photography partly screened by mature street trees; the
  five upper-floor bays per elevation are a regularisation of that. Confirm before
  committing to the facade.
- The assessor calls the property Industrial while every permit since 1990 calls it office,
  and it is leased as creative office. `cat: 3` (office) is the recommendation and matches
  the neighbour `380-brannan`; `19` (industrial) or `20` (warehouse) are defensible if the
  runtime label should reflect the building's origin rather than its use.
- No architect is recorded for the 1929 building in any source consulted.
