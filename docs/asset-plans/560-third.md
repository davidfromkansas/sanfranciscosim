# 560 Third Street — SF-SIM asset plan

A 1941 two-storey light-industrial infill on a 30 x 80 ft SoMa lot, re-skinned in
2015–16 into a charcoal-black storefront-and-loft office (the Poppin showroom, and
since then a small-tenant office building). The narrowest landmark in the Third
Street set — a 9.4 m frontage between the chocolate-brown 1907 block at 574 and the
cream 1921 warehouse at 550 — and the *lowest*, which is the whole point: it is the
notch in the block, a 7 m roof sunk four metres below the walls on either side.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/560-third/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `560-third` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3951188, 37.7804142` (footprint oriented-bbox centre, measured) |
| Target height | **7.2 m** (parapet crest; roof plane 6.66 m measured, parapet *derived*) |
| OSM footprint | 9.98 x 24.06 m bar on the 43.9 deg SoMa grid, 233 m2 (OSM way/124903642, measured) |
| Triangle cap | 8,000 |
| Category | `3` (Office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 560 Third Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 560 Third Street in San Francisco and
deliver it as a downloadable, validated GLB.

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
8. `artifacts/550-third/` — the immediate neighbour, and the closest match in
   scale, palette and detail budget. This asset stands shoulder to shoulder with
   it; they must look like pieces from one toy box.
9. `docs/asset-plans/560-third.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The narrow proportion: a 9.4 m wide, 24 m deep, two-storey bar wedged between
  two taller neighbours — the low notch in the block
- The **charcoal-black painted street front**, the single strongest cue and the
  only elevation anyone will ever see from the street
- The upper-floor **glazed band**: one wide window running nearly the full
  frontage, divided by dark mullions into four tall panes, set in a dark reveal
- The ground-floor dark glazed shopfront with its full-height glass door at the
  574 (south-east) end and a display window beside it
- The plain flat parapet with a thin cap — no cornice, no ornament
- The **roof**, which is the asset's real facade: pale membrane field, two large
  rectangular skylights, low parapet all round, a small mechanical cluster
- The **night state**: the upper glazed band as one warm lantern, the way it
  reads in the dusk reference (2.2), with a small ground-floor cue and nothing
  else

## Research 560 Third Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The north-east (3rd Street) elevation — the only public face
- Aerial and roof views — **the roof is the primary facade for this asset**, and
  the dossier's reading of it (§2.4 "Top") comes from a single oblique satellite
  frame in which the roof leans off its footprint. Better imagery beats it.
- Day and night appearance
- **The parapet crest height, which this dossier derives rather than measures.**
  The roof plane at 6.66 m is measured (2010 city LiDAR, `SF3776007`); 7.2 m
  assumes a 0.55 m parapet above it. OSM's Bing-traced `height=7` corroborates
  the order of magnitude but is not independent. Any better source — a planning
  drawing, a measured elevation, a dated photograph scaled against 574's known
  11.05 m — beats the derivation. Document what you find.
- Whether the two bright rectangles on the roof are skylights, roof hatches or
  mechanical housings (this dossier infers skylights from the "loft-style office
  with abundant natural light" description in the tenant's own copy)
- Any change since 2017: the newest usable street-level frame in the sources
  below is from March 2019, and the newest close facade view from February 2017.

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/560-third/REFERENCE.md` containing: source links and what each
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

This building has no skyline silhouette and only one public elevation. §10 (roofs
as secondary facades) is the governing section, not §11 (landmark geometry). The
entire budget goes into two surfaces — the roof and the 9.4 m street front — and
into the *contrast* between this building's dark, low, quiet mass and the pale
and brown volumes standing over it. Resist inventing articulation for the three
party walls; nobody can see them, and detail spent there is detail stolen from
the two that matter.

The finished asset must be immediately recognizable as 560 Third Street,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel
art, not generic low-poly, and never accurate in one view while invented in the
others.

## Scope of the exported asset

Export the 560 Third Street building itself, including its parapets, roof
membrane, skylights and rooftop mechanical plant.

Do not include unrelated surrounding city geometry: 3rd Street, the neighbouring
buildings at 550 3rd and 574 (566–586) 3rd, the large street tree at the kerb,
street furniture, parking meters, people, vehicles, plinths, cameras or lights.
Temporary context may appear in review renders but must not leak into the GLB.

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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The building's
long axis runs 43.9 deg / 223.9 deg true; the 3rd Street front faces north-east
(outward normal 44.1 deg true), so the contract's "front faces −Y" cannot be
honoured literally. Real-world orientation wins (AGENTS rule 5). Record the
decision and the measured heading in `REPORT.md`.

**Height normalization:** make the exported bounding-box top land exactly on the
verified architectural height, so the loader's `targetHeightM / measuredHeight`
scale is 1.0.

## Reproducible Blender workflow

Blender 4.5 LTS or newer, headless only: `blender -b --python script.py -- args`;
no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/560-third/build_560_third.py` (deterministic build script),
`artifacts/560-third/560-third.blend`, and `artifacts/560-third/560-third.glb`.
The script must rebuild the model reliably enough for future revision. Do not
modify or rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`560-third-top.png`, `560-third-north.png`, `560-third-east.png`,
`560-third-south.png`, `560-third-west.png`, plus `560-third-contact-sheet.png`,
at least one high three-quarter aerial beauty render `560-third-aerial.png`, and
a night render `560-third-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; **the top view and the north-east elevation are the two
hero images for this asset** — the top must clearly show the two skylights, the
parapet ring and the mechanical cluster, and the north-east must show the upper
glazed band, the shopfront and the entry; the aerial view uses the style bible's
camera assumptions (30-50 degrees down, long lens). Simple tabletop lighting,
neutral warm background, minimal depth of field, and every image must depict the
same exported model.

## Validate the exported GLB

Re-import `560-third.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Normals are checked two ways: per-object signed
volume (authoritative for a union of closed solids) and a deterministic
visibility-ray test (≤ 0.15% residual, zero for single shells). Render at least
one review image from the re-imported asset. Write
`artifacts/560-third/validation.json` and `artifacts/560-third/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "560-third",
  "file": "560-third.glb",
  "anchor": [
    -122.3951188,
    37.7804142
  ],
  "targetHeightM": 7.2,
  "cat": 3,
  "name": "560 Third Street",
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
for that, together with the integration notes in `docs/asset-plans/560-third.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* or
*derived* are visual or computed, not published figures — the executing agent
must re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 560 3rd Street, San Francisco, CA 94107 | OSM `addr:*` (`addr:source:housenumber=survey`), DBI permits, assessor roll |
| Parcel | Block 3776, Lot 007 (APN 3776007) | SF Assessor roll (measured) |
| Built | 1941 | SF Assessor roll, `year_property_built` |
| Storeys | 2 | SF Assessor roll; DBI permits reference a 2nd floor and a walkway between two 2nd-floor areas |
| Construction | Wood frame (Type V) per DBI 2015–16 permits; the assessor codes the parcel `C`. **Conflict — see 2.15.** | DBI PA 201511233289 / 201602099129 / 201602190008; assessor `construction_type` |
| Use | Assessor: Industrial (zoning SLI). Actual: office / showroom | assessor roll; DBI use fields flip office ↔ "warehouse, no furniture"; tenant listings |
| Footprint | 9.98 x 24.06 m bar, 233 m2 (shoelace) / 240 m2 (oriented bbox) | OSM way/124903642, reprojected + oriented bbox (measured) |
| Lot | 30 x 80 ft (9.14 x 24.38 m), 2,400 sq ft | SF Assessor roll — `lot_depth` 80 ft; frontage derived from lot area |
| Building area | 3,390 sq ft (assessor); "approximately 4,200 sq ft" as marketed in 2016 | assessor roll; Poppin lease press release |
| Roof plane height | 6.66 m above grade | SF 2010 LiDAR building footprint `SF3776007`, `hgt_median_m` 6.66 over 993 half-metre cells (measured) |
| Parapet crest | **7.2 m** — roof plane + ~0.55 m parapet | *derived*, corroborated by OSM `height=7` |
| OSM `height` tag | 7 m (source: Bing) | OSM — a stereo-traced figure that lands on the parapet edge; consistent, not independent |
| Anchor | -122.3951188, 37.7804142 | footprint oriented-bbox centre (measured) |
| Long-axis heading | 43.9 deg / 223.9 deg true | OSM geometry (measured) |
| Lot condition | **Not a through lot.** 3rd Street front (NE) only; party walls on both long sides and across the rear — 550 3rd wraps behind it | OSM footprint geometry + assessor lot depth (measured) |
| Neighbour heights | 550 3rd = 7.23 m roof / 11.0 m post-2025 crest (NW); 574 3rd = 11.05 m roof / 15.4 m crest (SE) | LiDAR `SF3776005`, `SF3776008`; `docs/asset-plans/550-third.md`, `574-third.md` |
| 2015–16 works | Demolition of partitions, new accessible toilets, new stairs and handrails, a new walkway joining two 2nd-floor areas, new finishes, Title-24 lighting; occupancy corrected office → warehouse | DBI PA 201511233289 + revisions 201602099129, 201602190008, 201604205205 |
| Earlier works | Reroofing 1993 and 2013; a 1-hour gas-meter enclosure 2003 | DBI PA 9320950, 201306210217, 200311180486 |
| Tenancy | Poppin SF showroom from January 2017 (~4,200 sq ft, street-level access plus a second floor for ~35 people); later Strandberg Engineering and other small offices | Poppin press release; business listings |

### 2.2 Sources

- https://www.openstreetmap.org/way/124903642 — footprint geometry, `addr:housenumber=560` (survey-sourced), `height=7` (Bing-traced)
- https://data.sfgov.org/resource/wv5m-vpq2.json — SF Assessor Historical Secured Property Tax Rolls, block 3776 lot 007: 1941, 2 storeys, Industrial / SLI, 3,390 sq ft on a 2,400 sq ft lot, 80 ft deep. The same query on lots 005 and 008 gives the two neighbours (1921 / 2 storeys / 19,997 sq ft, and 1907 / 3 storeys / 58,530 sq ft), which is what fixes this building as the *low* one on the block face.
- https://data.sfgov.org/resource/i98e-djp9.json — DBI building permits, block 3776 lot 007 (10 records, 1993–2016): the two reroofings, the 2015–16 interior renovation and its 2nd-floor walkway, the Type V construction entries, and the occupancy correction
- https://data.sfgov.org/resource/ynuv-fyni.json — SF 2010 LiDAR building footprints, record `SF3776007`: 993 half-metre cells (≈248 m2, corroborating the OSM polygon), ground mean 6.82 m, height median 6.66 m, height majority 6.57 m, height max 11.43 m. **The 11.43 m maximum is bleed from 574's party wall at 11.05 m, not a rooftop object** — see 2.15.
- https://poppin.imgix.net/press-assets/SF_Showroom_Lease_Signing_Press_Release.pdf — Poppin's own November 2016 lease announcement: 560 Third Street, ~4,200 sq ft, street-level access plus a second floor for ~35 employees, opening January 2017
- https://www.poppin.com/blogs/poppin-office-furniture-blog/what-makes-our-furniture-showrooms-so-special — the tenant describes the SF space as loft-style with abundant natural light and a "treehouse" feel from the big street tree seen out of the upstairs loft. This is the basis for reading the roof rectangles as skylights (*inferred*) and confirms the upper floor is one open volume behind the window band.
- KartaView sequence 13089 frame 5679 and sequence 12016 frames 3624/5118 (capture 2016-08), 3rd Street looking north-west from between Brannan and the site — establish the block sequence brown (574) → charcoal (560) → cream (550) and the two-storey proportion
- KartaView sequence 50032 frame 1811 (capture 2017-02-23, dusk), 3rd Street — **the night reference**: the upper glazed band lit warm amber across the full frontage with the ceiling and light fittings visible through it, the ground floor almost dark
- KartaView sequence 10065 frames 4431/5004 and sequence 10657 frames 6727/7800 (capture 2016-07) — the charcoal wall, the parapet line against 574's third floor, and the shopfront
- Esri World Imagery (z20, oblique) — the roof reading in §2.4 "Top": pale membrane, two bright rectangles, the SE half in 574's shadow. The frame leans, so roof-object positions from it are approximate.

### 2.3 Orientation and placement

A mid-block infill on the south-west side of 3rd Street between South Park and
Brannan, 80 ft deep on a 30 ft frontage. The SoMa grid here is rotated ~45 deg
from true north: 3rd Street runs 134.8 deg / 314.8 deg, and this building's long
axis is perpendicular to it at 43.9 deg.

Measured footprint, reprojected with the app's tangent projection and recentred
on the oriented-bbox centre (x east, y north, metres):

```
( 11.71,   5.31)
(  4.96,  11.86)
(-12.03,  -4.99)
( -4.97, -12.04)
```

| Edge | Length | Outward normal (true) | What it is |
|---|---|---|---|
| v0 → v1 | 9.40 m | 44.1 deg (NE) | **3rd Street front — the only public elevation** |
| v1 → v2 | 23.93 m | 315.1 deg (NW) | party wall with 550 3rd |
| v2 → v3 | 9.98 m | 224.9 deg (SW) | rear party wall — 550 3rd wraps behind this lot |
| v3 → v0 | 24.07 m | 134.9 deg (SE) | party wall with 574 (566–586) 3rd |

Author `+Y` = north and place the polygon exactly as measured. The contract's
"front faces −Y" cannot be met — the real front faces north-east — so real-world
orientation wins per the README orientation note and AGENTS rule 5.

The polygon is very slightly non-rectangular (9.40 m front, 9.98 m rear) because
it is Bing-traced; the assessor's 30 x 80 ft lot is a rectangle. Build the OSM
polygon as measured — the party-wall neighbours in the bake were traced from the
same source and will line up with it, which a "corrected" rectangle would not.

### 2.4 What each side shows

**North-east (3rd Street) — the only public face.** 9.4 m wide, two storeys,
painted a flat near-black charcoal from parapet to pavement. The upper storey is
one wide glazed band running nearly the full frontage: four tall panes divided by
slim dark mullions, set in a shallow dark reveal, with a solid charcoal spandrel
below it and a plain charcoal band above it up to the parapet. The ground floor is
a dark glazed shopfront — a full-height glass door at the south-east (574) end,
then a display window, all in the same dark frame, with a narrow dark base rail.
A shallow horizontal shadow line marks the storefront head. The parapet is flat and
plain with a thin cap; there is no cornice, no signage band and no ornament. A
mature street tree stands at the kerb directly in front — it belongs to the city,
not the asset, but it is what the building's own tenant called its "treehouse"
view, and it is why most street photography of this facade is partly obscured.

**South-east (long, 24.1 m).** A blind party wall shared with 574 3rd. 574 stands
11.05 m to its roof and 15.4 m to its crest, so **every square metre of this wall
is buried**. Nothing is visible; nothing should be modelled beyond a clean plane.

**North-west (long, 23.9 m).** A blind party wall shared with 550 3rd, whose roof
is 7.23 m — a few centimetres above this building's own parapet — and whose
post-2025 penthouse reaches 11.0 m. Also buried.

**South-west (rear, 10.0 m).** Not a street elevation. 550 3rd's 48 m bar wraps
behind this lot (the "kink at v2" that `docs/asset-plans/550-third.md` §2.3
records in *its* party wall is the notch this building sits in), so the rear wall
abuts a neighbour as well. Buried.

**Top — the asset's real facade.** A flat pale-grey membrane roof at 6.66 m,
ringed by a low parapet, sitting in a four-metre-deep slot between 574's tall
brown wall and 550's white one. Two large bright rectangles read clearly in the
satellite frame: one about a third of the way back from 3rd Street, one near the
middle of the depth. The tenant's description of a loft-style upper floor "with
abundant natural light" behind a single street window makes skylights the natural
reading (*inferred*: they could be roof hatches or unit housings). Small scattered
vents and a compact mechanical cluster occupy the rear third. The south-east half
of the roof sits in permanent shadow from 574's wall — a fact worth respecting in
the palette rather than fighting.

### 2.5 Recognition cues (ranked)

1. **The dark notch.** A near-black two-storey box four metres lower than the
   walls on either side, between a brown 3-storey block and a cream one. From the
   app's aerial camera this reads before any detail does — it is the only dark,
   low thing on the block face.
2. **The upper glazed band**: one wide four-pane window filling most of a 9.4 m
   frontage — the whole street elevation is that band, a spandrel and a door.
3. **The proportion**: 9.4 m wide by 24 m deep, taller than it is wide from the
   street and four times longer than wide in plan. A sliver.
4. **The two roof skylights** on a pale membrane, the only roof event in the slot.
5. **The night lantern**: at dusk the upper band is a single warm rectangle in a
   dark facade — the reference image (2.2) is exactly the composition to build.

### 2.6 Miniature translation

**Preserve**

- The true footprint polygon, including its slight taper (9.40 m front, 9.98 m rear)
- The two-storey proportion; roof plane at 6.66 m, parapet crest at 7.20 m
- The near-black facade value — this is the identity, and it must stay dark
  enough to read as a gap next to `Toy_white` and the brown of 574
- The single wide glazed band with four panes, spanning most of the frontage
- The flat, unornamented parapet
- The two roof skylights and the pale membrane field

**Simplify / exaggerate**

- The window band becomes one `Toy_glass` panel behind four `Toy_ink` mullions in
  a 0.15 m recess — rhythm, not mullion count (style bible §5). Make it ~10%
  taller than measured so it still reads at city distance (§9).
- The shopfront becomes a single recessed `Toy_glass` plane with an `Toy_ink`
  frame, a `Toy_ink` door leaf at the SE end and a low `Toy_ink` base rail
- The storefront head becomes one crisp `Toy_ink` band, not a modelled canopy
- Skylights become `Toy_steel` frames 0.3 m proud with a single raised
  `Toy_glassl` pane — sized ~15% larger than measured (§9)
- The mechanical cluster becomes two beveled `Toy_roofd` boxes on a low curb
- The three party walls are single flat `Toy_ink`-toned planes with a parapet cap
  and nothing else — no panels, no reveals, no punched openings
- No street number signage: the real facade carries none

**Do not add** a cornice, a roof deck, planting, a bulkhead, a crown, or any
silhouette event. The building's charm is that it is small, dark, low and quiet
between two larger neighbours, and it disappears the moment it is given drama it
does not have.

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. **Body:** extrude the measured footprint from z=0 to z=6.66 (roof structure),
   `Toy_roofd`-adjacent dark wall colour (`Toy_ink` at facade value — see 2.8).
2. **Roof field:** a `Toy_stone` slab inset 0.30 m from the parapet inner face,
   top at z=6.78 (membrane build-up).
3. **Parapets:** 0.30 m thick, matching the wall colour, capped with a 0.10 m
   `Toy_steel` band; crest at **z=7.20** on all four sides — the real parapet is
   uniform and unstepped.
4. **3rd Street front** (9.40 m wide):
   - storefront recess 0.20 m deep, 8.4 m wide, from z=0.15 to z=3.30, filled
     with a `Toy_glass` plane in an `Toy_ink` frame;
   - a 1.10 m wide `Toy_ink` door leaf at the south-east end of that recess, with
     a slim `Toy_glassl` vision panel;
   - a 0.25 m `Toy_ink` head band at z=3.30–3.55;
   - the upper glazed band: recess 0.15 m deep, 8.0 m wide, z=4.05–6.05, a
     `Toy_glass` plane behind four `Toy_ink` mullions 0.12 m wide, with an
     `Toy_ink` sill and head reveal;
   - solid wall above to the parapet cap.
5. **Party walls (NW, SE) and rear (SW):** flat planes in the wall colour, no
   openings, parapet cap continued.
6. **Skylights:** two, 3.2 x 2.2 m, on the roof centreline — one centred 7.5 m
   back from the 3rd Street parapet, one centred 14.5 m back. `Toy_steel` frames
   0.30 m proud, `Toy_glassl` pane on top.
7. **Mechanical cluster (rear third):** two `Toy_roofd` boxes 1.3 x 0.9 x 0.7 m
   on a 0.12 m `Toy_roofd` curb, plus one short duct run and two 0.4 m vent
   cylinders (8 segments).
8. **Roof hatch:** one 1.0 x 0.9 x 0.35 m `Toy_steel` box near the rear party
   wall.
9. Bevel 0.1 m, 2 segments, on everything.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_ink` | `#3a3530` | the painted charcoal walls and parapets (all four sides), window mullions, storefront frame, door, head band, base rail |
| `Toy_stone` | `#d9d2c2` | roof membrane field |
| `Toy_glass` | `#2a4d73` | upper window band, storefront glazing |
| `Toy_glassl` | `#6f95b8` | skylight panes, door vision panel |
| `Toy_steel` | `#9aa0a6` | parapet cap, skylight frames, roof hatch |
| `Toy_roofd` | `#45454a` | mechanical units, curb, ducts, vents |
| `Toy_glass_Glow` | `#2a4d73` | the upper window band at night — **the hero glow** |
| `Toy_glassl_Glow` | `#6f95b8` | the two skylights at night — the supporting cue, and the only thing that identifies this building from the air after dark |

`Toy_ink` is deliberately used as a *wall* colour here, which no other building in
the Third Street set does. That is the point: against 550's `Toy_white` and 574's
brown, this building has to read as the dark gap. If the executing agent finds
`Toy_ink` too heavy at city distance, `Toy_roofd` (`#45454a`) is the one
acceptable substitute — do not lighten it further.

**Night state.** One warm rectangle in a dark box, plus two glowing skylights seen
from above. The February 2017 dusk reference is the composition: the upper band
lit across its full width, the ground floor essentially dark. Nothing else lights
— no parapet wash, no signage, no ground-floor spill beyond a hint at the door.
Glow shells must be thin surfaces proud of the opaque glazing behind them — the
app renders `_Glow` in a separate layer at ~12% alpha by day, so a primary surface
must never be authored as glow.

### 2.9 Top surface

At 7.2 m with one 9.4 m elevation, well over 90% of what this asset ever shows the
player is its roof. A blank roof would make it a dark rectangle in a gap. Steps 6–8
of §2.7 exist because they are the only events on it. Keep them few and large:
this is a 233 m2 roof, and the style bible's graphical repetition (§10) has room
for exactly two skylights and one plant cluster before it turns to clutter. The
permanent shadow cast by 574 across the south-east half is real and should be left
to the renderer, not baked into the palette.

### 2.10 Scope

**In the GLB:** the building shell, parapets and cap, the 3rd Street front with
its storefront and window band, the roof membrane, two skylights, the mechanical
cluster and the roof hatch

**Not in the GLB:** 3rd Street, the kerbside street tree, 550 3rd, 574 3rd, street
furniture, parking meters, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 8,000 — the smallest in the Third Street set, below 592 Third's 9,000 and well
below 550 Third's 14,000, because there is one designed elevation instead of four
and no roof programme beyond two skylights. Suggested split: shell, parapets and
cap ~1.8k; 3rd Street front (storefront, door, band, mullions, reveals) ~3.2k; roof
field ~0.4k; two skylights ~0.8k; mechanical cluster, ducts, vents and hatch ~1.2k;
spare ~0.6k. If the build comes in far under the cap, spend the slack on bevels and
mullion crispness, not on new objects.

### 2.12 Draft manifest entry

```json
{
  "id": "560-third",
  "file": "560-third.glb",
  "anchor": [
    -122.3951188,
    37.7804142
  ],
  "targetHeightM": 7.2,
  "cat": 3,
  "name": "560 Third Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`loadRadius` is the skill's default `max(2500, targetHeightM * 30)`; at 7.2 m the
building is illegible long before 2,500 m, so the carved hole left beyond the
radius costs nothing. No `alwaysLoaded`.

`cat: 3` (Office) follows the neighbours and the building's actual use; the
assessor's Industrial classification and the DBI "warehouse" occupancy correction
are recorded in 2.1 but describe the paperwork, not what stands there.

### 2.13 Integration notes (for later, not this task)

- **New landmark (Case B).** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: '560Third'`, lon/lat as above, `height: 7.2`) and re-bake the affected
  tiles, or the baked footprint will sit inside the model.
- **The exclusion radius is the whole risk, and the window is narrow.**
  `excluded()` in `pipeline/buildings.mjs` drops a footprint when *any* of its
  vertices falls inside the radius. This lot has party walls on three sides, so
  the neighbours' vertices sit *on* its boundary. Two numbers are already known
  from the neighbours' own plans, measured against the real bake input:
  - from **550 Third's** anchor, this building's footprint `SF3776007` has its
    nearest vertex at **11.17 m** — which is why 550 ships `exclude: 8` and not 12
    (`docs/asset-plans/550-third.md` §2.13);
  - from **574 Third's** anchor, `SF3776007`'s nearest vertex is **16.35 m** —
    which is why 574 ships `exclude: 12` and why 18 m would have eaten this
    building (`pipeline/lib/landmarks.mjs`, the 574Third comment).

  Both of those are distances *into* this lot from outside. The radius this
  landmark needs is the mirror image and must be measured the same way, from
  **this** anchor against the actual bake input (DataSF footprints simplified at
  the pipeline's 0.6 m tolerance, `ringCentroid`), not from the OSM polygon:
  find this footprint's ring centroid offset, then the nearest *neighbour* vertex,
  and take the middle of the band between them. This building's own half-length is
  ~12 m, so a radius sized off its ring rather than its centroid will certainly
  take 550 and 574 with it. Expect a small number — the same 8–10 m family as its
  neighbours — and record the measured band in the registry comment the way 550,
  574 and 400 Brannan do.
- **Unavoidable collateral is possible here and is not a bug.** This is an infill
  site with shared party-wall vertices on three sides; if no radius separates this
  footprint from a neighbour's, say so in the report rather than widening until
  something breaks.
- Manifest id `560-third` maps to registry id `560Third`.
- No camera preset key. At 7.2 m this is texture in the block, not a destination.
- The building sits on near-flat made ground (LiDAR ground mean 6.82 m NAVD88 over
  the footprint, range 0.53 m — the flattest of the three lots). Terrain seating
  should be uneventful; check it anyway.
- **Verify visually against both neighbours after the re-bake.** This asset is
  4 m lower than everything around it, which is exactly the condition in which a
  surviving procedural block hides the GLB completely. An unbaked check proves
  nothing here.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] bbox top exactly 7.20 m so the loader's scale factor is 1.0
- [ ] Dimensions plausible in meters and consistent with 2.1 (≈10.0 x 24.1 x 7.2)
- [ ] Triangles at or under 8,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the upper window band and the two skylights
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume + deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + night render + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The parapet crest is derived, not measured.** 6.66 m to the roof plane is
  measured from 2010 city LiDAR; 7.2 m adds an assumed 0.55 m parapet. OSM's
  Bing-traced `height=7` agrees but is a photogrammetric trace of the same edge,
  not an independent measurement. If a better source moves the crest, only
  `targetHeightM` and the parapet top move with it — the shell is measured.
- **The LiDAR maximum is contaminated.** `SF3776007`'s `hgt_maxcm` is 11.43 m,
  which is within centimetres of 574 Third's measured 11.05 m roof and is bleed
  from the shared party wall, not a rooftop object. Do not model a bulkhead to
  explain it. (`hgt_stdcm` 0.88 m against a 6.57 m majority says the same thing.)
- **Construction type is contradictory.** DBI's 2015–16 applications say wood
  frame (Type V); a 2003 permit says Type 2; the assessor codes the parcel `C`.
  For a flat-color miniature this changes nothing, but it is a live disagreement
  and should not be laundered into a confident statement in `REFERENCE.md`.
- **The roof rectangles are inferred as skylights.** They could be roof hatches or
  mechanical housings. If better imagery shows they are not glazed, drop the
  `Toy_glassl_Glow` from them and the night state loses its aerial cue — in which
  case the upper window band carries the night alone, which is acceptable.
- **The imagery is old.** The closest facade views are July–August 2016 and
  February 2017, from the Poppin fit-out; the newest usable frame is March 2019
  and is across the street. The satellite frame leans. Nothing here proves the
  facade is still charcoal in 2026. Check before committing to the palette; if it
  has been repainted, the *value* (dark, low, quiet) matters more than the exact
  hue, and 2.5 cue 1 must survive whatever the new colour is.
- **This is the narrowest asset in the set.** 9.4 m of frontage is roughly one
  pane of 550 Third's window grid. Judge it in place, next to
  `artifacts/550-third/` and `artifacts/574-third/`, not alone on a turntable —
  alone it will look like an unremarkable dark box, because alone it is one.
