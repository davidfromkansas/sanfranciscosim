# 166–168 South Park — SF-SIM asset plan

A 1912 two-storey red-brick commercial loft on the north-west rim of the South
Park oval — one lot wide, five lots deep. It is the narrowest building on the
rim: a 6.1 m frontage on a 29.8 m deep through-lot, wedged as a party-wall
sliver between the 2002 glass-and-metal block at 188 South Park (15.93 m) and
the low site at 164. Its whole identity is in that one small front: a stepped
brick parapet with a raised, gable-capped central bay, diamond accents set in
the brickwork, and a black shopfront under it. Above, it is a bright white
flat roof — the whitest surface on the block from the air.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/168-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `168-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3949862, 37.7811327` (OSM way 124884342 area centroid, measured) |
| Target height | **10.44 m** to the crest of the raised central parapet; main roof deck 7.98 m (LiDAR-derived, see 2.1) |
| Footprint | 6.10 m (wide, NE–SW) x 29.82 m (deep, NW–SE); 182 m2, measured — a parallelogram at bearing 135°/315° |
| Triangle cap | 6,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 166–168 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 166–168 South Park in San Francisco and deliver
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
7. `artifacts/358-brannan/` — the closest reference implementation. It is the
   other small SoMa brick front in this set whose whole job is one decorated
   street elevation on a plain shell, and its `PALETTE_HEX` comment block is the
   precedent for choosing `Toy_brick` over `Toy_rust` against pale neighbours.
   Take its skin-proud-of-shell technique, its parapet handling and its restraint;
   do **not** take its canted bay — this building has none.
8. `artifacts/188-south-park/` — the immediate south-west neighbour, sharing this
   building's party wall. Read it to keep the two consistent where they touch and
   deliberately different where they should be (2002 stucco/metal loft vs 1912
   brick), and to see what a South Park rim building looks like at this scale.
9. `docs/asset-plans/168-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## What is already observed, and what you still have to settle

Unlike most plans in this set, the street elevation here **was** observed —
Google Street View (Jan 2025 capture) reaches this frontage and 2.4 describes
what it shows. The roof was observed from Esri World Imagery (z20 nadir) and
Vexcel imagery via Google satellite. Treat 2.4 as fact, not hypothesis.

What is still open, in priority order:

1. **The second-floor window count and rhythm.** A street tree stands directly
   in front of the middle of the facade in the Jan 2025 capture and hides the
   ground and first-floor centre. One tall recessed second-floor opening is
   clearly visible in the south-west bay; the number of bays across the 6.1 m
   front is *inferred* as three from the parapet's three panels. Confirm from an
   older Street View capture (use the pano's date picker — earlier captures
   predate this tree's growth) or from listing photography.
2. **The exact parapet step profile.** 2.4 describes a raised central panel with
   a shallow gable cap and one step down on each side. Confirm the number of
   steps and whether the cap is a true triangular pediment or a segmental curve.
3. **Whether the 10.44 m LiDAR maximum is the front parapet.** See 2.15 risk 1.
   It is the single number that sets the model's height and it has one
   alternative explanation (party-wall bleed from the 15.93 m neighbour).
4. **The rear (north-west) elevation.** No imagery reached it — it faces a rear
   yard behind the lot, screened from 3rd Street by 188's block and the
   483 Bryant/Taber Place buildings. A 1995 permit records a **rear fire escape**.
   Anything else about that face is inference.

Record what you found and how in `REFERENCE.md` and `REPORT.md`.

## Must capture

- The **proportion**, which is the whole point of this building: 6.1 m wide and
  29.8 m deep, standing 10.4 m tall. It is a knife-blade in plan. Do not fatten
  it toward a comfortable box — the sliver is the recognition cue.
- The **stepped brick parapet** with its raised, gable-capped central bay — the
  only ornament this building has, and the thing that makes it findable
- The **diamond (lozenge) accents** set in the brick panels, one per parapet step
- Red brick, load-bearing, running bond, with brick pilasters dividing the front
- Tall recessed second-floor windows with dark frames
- A black shopfront at ground level under a brick surround: one wide display
  window and two dark entrance doors
- A **flat white roof** — this building's roof is a bright white membrane and is
  markedly lighter than every roof around it. From the app's downward camera that
  contrast is the second recognition cue, and it must survive into the miniature.

## Research 166–168 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The south-east (South Park) front in full, without the street tree in the way
- Aerial and roof views — the roof is the largest surface the app camera sees
- The two flanks. Note that **both are party walls**: the OSM footprint shares
  ring vertices with 188 South Park to the south-west (way 124884339) and with
  164 South Park to the north-east (way 124884357). Neither flank is a designed
  elevation and neither is normally visible; model them as plain brick.
- Day and night appearance
- The north-west (rear) elevation and its fire escape

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**One source conflict is already known — re-check it, do not silently
re-inherit the wrong value:** the construction type. Permits 8305456 (1983),
9001368/9001533 (1990), 9415428/9416646 (1994) and 9510796 (1995) all record
`constr type 3` (ordinary / masonry-walled), and the 1994 pair are a parapet
permit plus a "complete seismic upgrade" — the signature of an unreinforced
masonry retrofit. Permit 8404899 (1984) records `wood frame (5)`. The visible
facade is load-bearing brick, so type 3 is almost certainly right, but note that
the building does **not** appear on DataSF's unreinforced-masonry list (only
45 South Park does on block 3775). This affects nothing about the model's shape;
it matters only if you are tempted to describe the building's structure in
`REFERENCE.md`.

## Create a reference dossier

Write `artifacts/168-south-park/REFERENCE.md` containing: source links and what each
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

This is a **background building** in the style bible's detail budget (§21) that
earns one piece of hero treatment: the parapet. Everything else — flanks, rear,
roof — stays flat and quiet. Resist adding ornament anywhere except the front.

The finished asset must be immediately recognizable as 166–168 South Park, consistent
with the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1912 brick block: body, the decorated south-east front, the two
plain party-wall flanks, the plain rear with its fire escape, the flat white roof
and its parapet.

Do not include unrelated surrounding city geometry: South Park itself, the park's
trees or lawn, the street tree in front of the building, the sidewalk, 188 South
Park or 164 South Park, the rear yard, the hoarding on the neighbouring site,
parked cars, people, plinths, cameras or lights. Temporary context may appear in
review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 6,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The South Park
front faces **southeast, bearing 135°**; the long axis runs 135°/315° (NW–SE) and
the 6.10 m frontage runs 45°/225°. Build directly on the measured footprint
parallelogram in 2.3 rather than modelling an axis-aligned box and rotating it.
The contract's "front faces −Y" cannot be honoured literally here; real-world
orientation wins (AGENTS rule 5) and the deviation goes in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the raised central
parapet cap) must land at exactly **10.44 m** so the loader's
`targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/168-south-park/build_168_south_park.py` (deterministic build script),
`artifacts/168-south-park/168-south-park.blend`, and
`artifacts/168-south-park/168-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`168-south-park-top.png`, `168-south-park-north.png`, `168-south-park-east.png`,
`168-south-park-south.png`, `168-south-park-west.png`, plus
`168-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty render
`168-south-park-aerial.png`, and a night render `168-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the full 29.8 m roof and its
parapet return; the aerial view uses the style bible's camera assumptions (30-50
degrees down, long lens). Simple tabletop lighting, neutral warm background, minimal
depth of field, and every image must depict the same exported model.

Because the building is rotated 45° from the world axes, the four compass renders will
each show two faces at 45°. That is correct and expected — do not rotate the model to make
the elevations square on. Add one extra render square-on to the south-east front
(`168-south-park-front.png`): it is the only elevation that carries design, and a 45°
compass view will not let a reviewer judge the parapet.

## Validate the exported GLB

Re-import `168-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/168-south-park/validation.json` and
`artifacts/168-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **25 x 25 m** even though the
building is 6.1 x 29.8 m — that is the expected consequence of a 45° real-world heading,
not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "168-south-park",
  "file": "168-south-park.glb",
  "anchor": [
    -122.3949862,
    37.7811327
  ],
  "targetHeightM": 10.44,
  "cat": 3,
  "name": "166-168 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/168-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

**Evidence quality for this dossier.** Better than most in this set. Everything
geometric is measured from survey data (OSM, DataSF LiDAR footprints, DataSF
parcels) and is solid. The **roof** was observed from Esri World Imagery at z20
(0.118 m/px, geometrically registered against the OSM and DataSF footprints and
the parcel polygon — see the overlay method in 2.2) and from Vexcel imagery via
Google satellite. The **south-east front** was observed directly from Google
Street View (Jan 2025 capture), which does reach this frontage; 2.4's description
of it is observation, not inference. The **rear** and the exact bay count are the
two things nothing reached, and both are labelled.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 166–168 South Park St, San Francisco, CA 94107. 166 and 168 are the two floors of one building | OSM `addr:housenumber=166,168` (`addr:source:housenumber=survey`); LoopNet/Showcase list the property as "166-168 S Park St"; Zetta Venture Partners is recorded at 168, Floor 1 |
| Built | **1912** | LoopNet listing 24927521; Showcase 24341219 |
| Storeys | **2** | SF building permits 8305456 (1983), 8404899 (1984), 9001368/9001533 (1990), 9016636 (1990), 9415428/9416646 (1994), 9510796 (1995) — every one records `number_of_existing_stories = 2` and `number_of_proposed_stories = 2` |
| Building size | 4,600 sq ft total, ~2,300 sq ft typical floor; Class C office | LoopNet 24927521, Showcase 24341219 |
| Construction | `constr type 3` (ordinary / masonry-walled) on six permits; `wood frame (5)` on one (8404899). Facade is load-bearing brick | SF permits — see 2.15 risk 3 |
| Seismic history | 1994: permit 9416646 "parapet" and 9415428 "complete seismic upgrade begun and partially complete" — a URM-style parapet-bracing retrofit. **Not** on DataSF's unreinforced-masonry list (block 3775 lists only 45 South Park) | SF permits; DataSF `beah-shgi` |
| Rear fire escape | permit 9510796 (1995) "rear fire escape to convert 2nd flr res to office" | SF permits — **the only fact known about the rear elevation** |
| Storefront history | 1983 permit 8305456 "install new entrance doors and storefront"; 1984 permit 8404899 "install new front & sidewalk" | SF permits |
| Use | retail sales / 1–2 family dwelling until c. 1990, **office** since | SF permits (`existing_use` → `proposed_use` trail) |
| Current tenants | Zetta Venture Partners (Floor 1); Maple VC / Maple 3 VC / Maple SPV-A (registered 2022); previously Pliancy Inc. (2022–24), Thane Studio / SMW Design, Tish Key Interior Design | Google Maps place record; bizprofile.net; opengovus SF business registrations |
| Block / lot | 3775 / 070 (mapblklot 3775070) | DataSF parcels `acdm-wktn` |
| Zoning | SPD (SOMA – South Park) | DataSF parcels |
| Neighbourhood | Financial District/South Beach; planning district South of Market | DataSF parcels |
| Footprint | **6.10 m (wide, NE–SW) x 29.82 m (deep, NW–SE), 182 m2**, a parallelogram at bearing 135°/315° | OSM way 124884342, reprojected — **measured** |
| DataSF footprint (cross-check) | 7.44 x 33.94 m, 204 m2 — LiDAR outline, generous on both axes, and notched on the NE side | DataSF footprint SF3775070 — **measured, but inflated**; see 2.15 risk 2 |
| Parcel | 6.99 x 42.06 m, 294 m2 (0.073 acre) — the building fills the lot width and 29.8 m of the 42.1 m depth, leaving a ~9.5 m rear yard and a ~2.7 m gap to the front property line | DataSF parcels `acdm-wktn` lot 3775070 — **measured**. Showcase's 3,049 sq ft (0.07 AC) agrees |
| Party walls | **both flanks**. The OSM ring shares vertices with 188 South Park to the SW (way 124884339) and 164 South Park to the NE (way 124884357) | OSM geometry — **measured** |
| Roof form | flat, no penthouse, no roof structures beyond a few small vents/hatches | Esri World Imagery z20 nadir + Vexcel via Google satellite — **observed from above** |
| Roof crest height | **10.44 m** above ground | DataSF LiDAR `hgt_maxcm = 1044` — **measured** |
| Median roof height | 7.98 m (median), 7.83 m (mean) | DataSF LiDAR `hgt_mediancm = 798`, `hgt_meancm = 783` — **measured** |
| Minimum height | 4.73 m | DataSF LiDAR `hgt_mincm = 473` — edge cells over the rear yard or the front setback strip |
| Height std dev | 0.75 m | DataSF LiDAR `hgt_stdcm = 75` — very tight, i.e. a genuinely flat roof with one raised element |
| LiDAR sample size | 806 cells at 50 cm (= 201.5 m2, consistent with the DataSF outline) | DataSF LiDAR `hgt_cells50cm` |
| Ground elevation | 6.32 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Neighbour heights | 188 South Park (SW) 15.93 m max / 13.34 m median — **already a landmark asset**; 164 South Park (NE) 9.25 m max / 5.44 m median; 160 South Park 9.41 m / 7.79 m | DataSF LiDAR SF3775125, SF3775069, SF3775067 |

### 2.2 Sources

- https://www.openstreetmap.org/way/124884342 — footprint, `addr:housenumber=166,168`, `addr:street=South Park`, `building=yes`, `source=Bing`, **no height tag**
- `https://data.sfgov.org/resource/ynuv-fyni.json?mblr=SF3775070` (DataSF Building Footprints, LiDAR-derived) — heights 10.44 / 7.98 / 4.73 m, 806 cells, ground 6.32 m
- `https://data.sfgov.org/resource/acdm-wktn.json?mapblklot=3775070` (DataSF Parcels) — lot 3775/070, 6.99 x 42.06 m, zoning SPD
- `https://data.sfgov.org/resource/i98e-djp9.json?street_number=166&street_name=South%20Park` (SF Building Permits) — eight permits 1983–1995: two storeys throughout, storefront/entrance work, 1994 parapet + seismic upgrade, 1995 rear fire escape
- `https://data.sfgov.org/resource/beah-shgi.json?block=3775` (DataSF Unreinforced Masonry Buildings) — 166 South Park is **absent**; only 45 South Park is listed on this block
- https://www.loopnet.com/Listing/166-168-S-Park-St-San-Francisco-CA/24927521/ — 1912, 2 storeys, 4,600 SF, Class C office (page itself is login-walled; facts read via Exa's extracted text)
- https://www.showcase.com/166-168-s-park-st-san-francisco-ca-94107/24341219/ — 1912, 2 storeys, 4,600 SF, land 0.07 AC / 3,049 sq ft
- https://www.bizprofile.net/principal-address/168-south-park-street-san-francisco-ca-94107 — Maple 3 VC LLC, Maple VC Management LLC, Maple 3 VC LP, Maple SPV-A LLC (2022)
- https://opengovus.com/san-francisco-business/1313581-09-221 and `/0372757-01-001` — Pliancy Inc. at 166 S Park St (2022–2024); Thane Studio / SMW Design at 166 S Park St #1 (2003–2022)
- Google Street View, Jan 2025 capture, panorama at approx. `37.780973, -122.394785` looking 315°–320° — **the south-east front, observed**. The place record confirms the pano is anchored to "168 S Park St".
- Esri World Imagery (`services.arcgisonline.com/.../World_Imagery/MapServer/tile/20/…`), z20 nadir, 0.118 m/px — **the roof, observed**. Method: nine tiles stitched, then the OSM ring, the DataSF footprint and four parcel polygons drawn on top in Web-Mercator pixel space, which registers the imagery to the survey data to within a pixel. z21 and z22 return the "no data" placeholder here, and the Clarity service has no coverage, so z20 is the imagery ceiling from this source.
- Google Maps satellite (Vexcel Imaging US, 2026) at z20–z21 — sharper corroboration of the flat white roof; not used for measurement.
- `docs/asset-plans/188-south-park.md` §2.13 — the neighbour's exclusion analysis, whose open question ("is OSM way 124884355 a separate Overture footprint?") is answered in 2.13 below: **it is**.

### 2.3 Orientation and placement

The building sits on the north-west rim of the South Park oval, facing south-east
onto the park at bearing 135°, in the same row as (and immediately north-east of)
188 South Park. The lot is a through-lot running 42.06 m from the South Park
property line back toward 3rd Street. The building occupies the front 29.8 m of
it; the rear ~9.5 m is a yard. Both flanks are party walls.

The OSM ring has five nodes; two are collinear along the south-west flank, so the
real shape is a four-cornered parallelogram. Corners in Blender coordinates
(metres, `+X` east, `+Y` north), centred on the anchor `-122.3949862, 37.7811327`
(the ring's area centroid):

```
(  8.42, -12.64)   SE corner, south-west side  (South Park front)
( 12.74,  -8.34)   SE corner, north-east side
( -8.42,  12.63)   NW corner, north-east side  (rear yard)
(-12.74,   8.33)   NW corner, south-west side
```

in ring order:
`(8.42, -12.64) → (12.74, -8.34) → (-8.42, 12.63) → (-12.74, 8.33)`.

Derivation, so it can be checked: the OSM ring reprojected into the app's local
tangent frame is `(3728.30, -1238.94) (3738.03, -1229.29) (3749.45, -1217.97)
(3753.77, -1222.27) (3732.62, -1243.24)` in `(x, z)` metres, area centroid
`(3741.035, -1230.609)`; the second node is collinear with its neighbours and
drops out. Blender `X = x − 3741.035`, `Y = −1230.609 − z` (the app's `+z` is
south, Blender's `+Y` is north).

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(8.42,-12.64) -> (12.74,-8.34)` | 6.10 m | SE 135° | **South Park front** — the only designed elevation |
| `(12.74,-8.34) -> (-8.42,12.63)` | 29.82 m | NE 45° | NE party wall with 164 South Park |
| `(-8.42,12.63) -> (-12.74,8.33)` | 6.10 m | NW 315° | rear, onto the yard; carries the fire escape |
| `(-12.74,8.33) -> (8.42,-12.64)` | 29.82 m | SW 225° | SW party wall with 188 South Park |

Because of the 45° heading the axis-aligned bounding box is ~25 x 25 m. That is correct.

The building's front stands ~2.7 m behind the parcel's South Park property line.
That is almost certainly because the parcel extends under the sidewalk here (the
oval street was carved out of the original block), not because there is a
forecourt: Street View shows the shopfront directly behind the public sidewalk.
**Do not model a setback or a forecourt.** The anchor above is the building
centroid, so the setback is already accounted for.

### 2.4 What each side shows

**Southeast (South Park front) — observed.** 6.10 m wide, 10.44 m to the parapet
crest, so a tall narrow panel roughly 1 : 1.7. Red brick in running bond, warm
red-brown with darker mottled headers. Brick pilasters divide the front into
bays, and each bay's parapet is stepped: a **raised central panel capped by a
shallow gable with a projecting brick coping**, stepping down one level to each
side, with a grey metal coping run over the whole top. A **diamond (lozenge)
accent in a contrasting grey cast-stone or recessed brick** sits in each parapet
panel — at least three are visible across the front, following the steps, so they
sit at different heights. The second floor carries tall recessed window openings
with dark frames and brick soldier-course heads; one is clearly visible in the
south-west bay and the rest are behind a street tree in the Jan 2025 capture
(*the bay count is inferred as three from the three parapet panels*). The ground
floor is a black-framed shopfront set into a brick surround: one wide display
window carrying the tenant's vinyl lettering, and two dark entrance doors, with
brick piers between and at both ends. The 1983/84 permits date this shopfront.

**Northeast flank — party wall.** 29.82 m long, shares ring vertices with
164 South Park. Plain brick, no openings of consequence. In the Jan 2025 capture
164's frontage is a low red-painted structure behind plywood hoarding and a
graffiti-covered fence — a site in flux — so a strip of this flank is
momentarily exposed near the street. Do not design to that: model it as a plain
party wall.

**Northwest (rear) — not observed.** Faces the ~9.5 m rear yard, screened from
3rd Street. The only recorded fact is the 1995 **rear fire escape**. Expect a
plain brick face with a small number of utilitarian openings and the fire escape;
everything beyond that is *inferred*.

**Southwest flank — party wall** with 188 South Park (whose own asset already
exists). Plain brick, invisible in practice; 188 stands 5.5 m taller, so from the
air this flank reads as the shadowed side of the sliver.

**Top — observed.** 6.10 x 29.82 m of **flat, bright white roof** — a white
membrane or cool-roof coating, and by a wide margin the lightest roof on the
block in both Esri and Vexcel imagery. A loose line of small dark items (vents,
a hatch) runs along the middle third. There is **no penthouse and no roof
structure**; the LiDAR standard deviation of 0.75 m over 806 cells confirms a
genuinely flat deck. The brick parapet returns along both flanks and the rear at
a lower level than the front's raised centre.

### 2.5 Recognition cues (ranked)

1. **The sliver proportion** — 6.1 m wide, 29.8 m deep, 10.4 m tall, wedged
   between a 15.9 m glass block and a low site. Nothing else on the rim is this
   narrow. Get this wrong and no amount of facade detail saves the model.
2. **The stepped, gable-capped brick parapet** — the building's only ornament and
   the thing that reads from the street and from a low aerial.
3. **The bright white flat roof** — the second cue, and the one the app's camera
   actually spends its time looking at. It is a genuine, measurable contrast
   against every neighbouring roof.
4. **Red brick against a metal-and-glass neighbour** — the 1912/2002 collision on
   the party wall is the block's story in one joint.
5. The diamond accents and the black shopfront.

### 2.6 Miniature translation

**Preserve**

- The 6.10 x 29.82 m footprint and the real 135°/315° heading, exactly
- The two-storey height with the parapet lifting the crest to 10.44 m
- The stepped parapet silhouette, read as a silhouette rather than as brickwork
- The white roof's value — clearly lighter than the roofs around it
- The brick red, saturated enough to hold against 188's cool grey

**Simplify / exaggerate**

- Brick becomes one flat `Toy_brick` colour. No courses, no mortar lines, no
  per-brick geometry. The style bible's flat-material rule is absolute here.
- The parapet steps may be exaggerated in depth (not height — the crest must land
  on 10.44 m) so the silhouette reads from the aerial camera
- The diamond accents become three simple inset lozenges, one per panel — flat
  quads, not modelled reliefs
- Each second-floor window becomes a single tall recessed opening with one frame
  band; no mullions, no sashes
- The shopfront becomes one wide glazed opening plus two door recesses
- The fire escape becomes one simple stair-and-landing silhouette on the rear, or
  is omitted entirely if it costs more than ~300 triangles — it is never seen
- Roof furniture becomes two or three small blocks, grouped, nothing more

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 parallelogram from z=0 to the roof deck z=7.98,
   `Toy_brick`.
2. Front skin: a 0.10 m skin proud of the shell on the south-east face only
   (the `artifacts/358-brannan` technique), so the decorated front reads as a
   distinct plane from the plain flanks.
3. Ground floor, z=0 to z=3.9, on the front only: a brick surround with one
   2.6 m wide glazed shopfront (`Toy_glass`) and two 1.0 m dark door recesses
   (`Toy_ink`), separated and flanked by 0.35 m brick piers.
4. Storefront head: a 0.25 m `Toy_stone` lintel band at z=3.9 across the front.
5. Second floor, z=4.5 to z=7.3: three recessed openings (`Toy_glass`), each
   ~1.3 x 2.4 m, set back 0.18 m, with a 0.10 m `Toy_stone` frame band. Confirm
   the count from photography before committing (see Part 1, open question 1).
6. Flank and rear parapet: z=7.98 to z=8.6, 0.30 m thick, `Toy_brick`, capped
   with a 0.06 m `Toy_steel` coping. This is the level the roof deck sits below.
7. **Front parapet, z=7.98 to z=10.44** — the hero. Three panels: the central one
   rising to the full 10.44 m and capped with a shallow gable (rise ~0.25 m over
   the panel width) with a projecting 0.12 m brick coping; the two flanking
   panels stepping down to ~9.4 m and then to the 8.6 m flank return. One inset
   `Toy_stone` diamond per panel, ~0.55 m across, on the panel face.
8. **Roof, z=7.98 to z=8.06** — a thin flat slab in `Toy_white`, deliberately the
   lightest value in the model. Two or three `Toy_steel` vents (0.5 x 0.5 x 0.4 m)
   grouped in the middle third.
9. Rear: one door recess and two small openings (`Toy_ink`), plus an optional
   simplified fire escape in `Toy_steel`.
10. Bevel 0.08 m, 2 segments. The building is small; a 0.12 m bevel that suits a
    30 m block will eat this facade.

### 2.8 Materials and palette

Flat colors only, from the project palette (hexes as used in
`artifacts/358-brannan/build_358_brannan.py`).

| Material | Hex | Used for |
|---|---|---|
| `Toy_brick` | `c96f4a` | all brickwork — body, front skin, piers, parapet |
| `Toy_stone` | `d9d2c2` | storefront lintel band, window frame bands, the diamond accents |
| `Toy_glass` | `2a4d73` | shopfront glazing, second-floor windows |
| `Toy_white` | `f8f4ec` | the flat roof slab — the model's lightest value |
| `Toy_steel` | `9aa0a6` | parapet coping, roof vents, fire escape |
| `Toy_ink` | `3a3530` | door recesses, rear openings |
| `Toy_glass_Glow` | `6f95b8` | lit second-floor windows at night |
| `Toy_trim_Glow` | `f3efe6` | shopfront spill at street level |

`Toy_brick` (`c96f4a`) over the browner `Toy_rust`: this front's whole job is to
advance against 188 South Park's cool grey-and-glass wall on one side and a pale
low site on the other. That is the same argument 358 Brannan's palette comment
records, and the same one that made 380 Brannan go the other way — check the
first aerial render and say in `REPORT.md` which way it went and why.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
glazing — the app renders `_Glow` in a separate layer that is ~12% alpha by day,
so a primary surface must never be authored as glow. This is a small building
with one visible face, so the night composition is correspondingly small. Hero
glow: two of the three second-floor windows lit (an office building after hours,
not a lit-up hotel). Supporting accent: a low spill at the shopfront glazing.
The flanks, the rear and the roof stay dark — a party wall that glows would
misread badly, and this building's flanks are pressed against neighbours.

### 2.9 Top surface

6.10 x 29.82 m of flat white roof at 7.98 m, with the parapet returning around
it. There is nothing else up there, and the plan is not to invent anything: the
composition is the white plane, the brick parapet frame around it, and a small
group of vents off-centre. The one deliberate decision is **value**: keep
`Toy_white` clearly lighter than every other surface in the model and lighter
than the neighbouring assets' roofs, because that contrast is a measured
observation about the real building and it is the cue the app's downward camera
gets. Do not let the glb-optimize weld or a bevel wash the roof slab's flat
shading out — see the ground-plane lesson in `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.

### 2.10 Scope

**In the GLB:** the single 1912 brick block — body, the south-east front with its
shopfront, second-floor windows, pilasters, stepped parapet and diamond accents;
the two plain party-wall flanks; the plain rear with its fire escape; the flat
white roof, its parapet return and its vents

**Not in the GLB:** South Park, its trees or lawn, the street tree in front of the
building, the sidewalk, 188 South Park, 164 South Park, the rear yard, the
hoarding on the neighbouring site, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 6,000 — a background building with one decorated face, and the cap should
bind comfortably. Suggested split: body and flanks ~600; front skin, piers and
shopfront ~1,200; three second-floor openings ~900; the stepped parapet, its
gable cap, its coping and the three diamonds ~1,800; flank/rear parapet return
~500; roof slab and vents ~500; rear openings and fire escape ~500.

The one place this budget can run away is the parapet. Model the steps as a
single extruded profile swept along the front, not as separate boxes that each
need a bevel; and keep the diamonds as inset quads on the panel face rather than
as pyramidal reliefs. If the fire escape starts costing more than ~300 triangles,
delete it — nothing in the app will ever see it.

### 2.12 Draft manifest entry

```json
{
  "id": "168-south-park",
  "file": "168-south-park.glb",
  "anchor": [
    -122.3949862,
    37.7811327
  ],
  "targetHeightM": 10.44,
  "cat": 3,
  "name": "166-168 South Park",
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

- **New landmark (Case B).** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: '168SouthPark'`, `lon: -122.3949862`, `lat: 37.7811327`, `height: 10.44`,
  `exclude: 5`) and re-bake the affected tiles, or the baked procedural building
  on this exact footprint will intersect the GLB.
- **The anchor is the OSM ring's area centroid, not the DataSF LiDAR centroid.**
  This is the opposite of the choice made for 165–167 and 188 South Park, and
  deliberately so. Those are wide, roughly square footprints where the two
  centroids differ by centimetres. This one is a 6 m sliver, the two centroids
  are 1.08 m apart, and the DataSF outline is inflated by 1.3 m across a 6.1 m
  width — anchoring on it would place the model over a metre off its own party
  walls and push the GLB's XY centre offset past the contract's ~1 m tolerance.
  The OSM ring is also the topologically correct one: it shares nodes with both
  neighbours' rings, so it is the outline the party walls actually follow.
- **Exclusion window, measured against the real bake input.** `excluded()` in
  `pipeline/buildings.mjs` drops a footprint when its centroid **or any ring
  vertex** falls inside the radius, and the bake input is the DataSF footprint
  file plus the Overture gap-fill, both projected and simplified at the 0.6 m
  tolerance. Measured from this anchor against that exact input:

  | | trigger distance | |
  |---|---|---|
  | this building's own Overture footprint (`8b933808…`, = OSM way 124884342, via centroid) | **0.00 m** | must be dropped |
  | this building's own DataSF footprint (SF3775070, via centroid) | **1.07 m** | must be dropped → floor |
  | 188 South Park front (SF3775125 / Overture `9f571039…`, nearest vertex) | 2.95 / 3.28 m | already dropped by `188SouthPark` — no net change |
  | **OSM way 124884355 (Overture `c73e5800…`, height 15, area 208 m2), nearest vertex** | **8.05 m** | must survive → **ceiling** |
  | 164 South Park (Overture `31645c36…` / SF3775069, nearest vertex) | 9.93 / 10.04 m | must survive |
  | 160 South Park (SF3775067, nearest vertex) | 12.60 m | must survive |

  The safe window is **(1.07, 8.05) m**. `exclude: 5` sits in it with 3.93 m of
  margin below and 3.05 m above, and matches the radius every other South Park
  rim landmark uses. The larger margin is deliberately on the floor side: that
  bound is the DataSF LiDAR centroid, which is the value most likely to move in a
  data refresh, while the ceiling is an OSM trace.
- **This answers 188 South Park's open question.** `docs/asset-plans/188-south-park.md`
  §2.13 left it undecided whether OSM way 124884355 exists as a separate Overture
  footprint, and took the conservative window on that basis. It does exist —
  Overture `c73e5800-2507-4c24-816e-0b022d5c7d75`, record `w124884355@1`, height
  15 m from USGS LiDAR, 208 m2 — so 188's conservative reading was the correct
  one and its `exclude: 5` is safe. Note in passing that this footprint bakes as
  a 15 m procedural block immediately behind the 188 South Park landmark asset;
  that is a pre-existing condition of 188's integration, out of scope here, and
  worth a separate look.
- **Verify with `pipeline/audit.mjs` check 1.6 after the re-bake** and confirm
  visually that 164 South Park and the block behind 188 are both still standing
  before committing.
- `loadRadius`: the default formula gives `max(2500, 10.44 * 30) = 2500` m. Take
  the default.
- This is the eighth building on the South Park oval in the landmark manifest and
  the ninth in the immediate area. The same question applies as for 181 and 188:
  a manifest of one-off SoMa blocks will not stream well forever, and the
  kit/instancing route (`KIT-INTEGRATION-PROMPT.md`) is the better long-term home
  for buildings of this class. This one has an unusually strong case for staying
  bespoke, though — no kit piece is 6 m wide with a shaped parapet.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 10.44 m — the raised central parapet cap, not a roof vent (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~25 x 25 m is expected)
- [ ] The footprint is still 6.10 x 29.82 m in plan — measure it, do not eyeball it, and check that it did not get fattened for comfort
- [ ] Triangles at or under 6,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the lit second-floor windows and the shopfront; glow shells proud of opaque glazing; flanks, rear and roof dark
- [ ] The roof slab is the lightest value in the model and still reads flat after bevelling
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + the extra square-on front + contact sheet + night render, all regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed
- [ ] The 2.15 risk 1 height question answered in `REPORT.md`, with the evidence that answered it
- [ ] The second-floor bay count either observed or, if it stayed inferred, said so plainly in `REPORT.md`

### 2.15 Open questions and risks

1. **Is the 10.44 m LiDAR maximum the front parapet, or bleed from next door?**
   This is the most consequential number in the plan. In favour of it being real:
   Street View shows a raised central parapet section that clearly stands well
   above the flanking roofline, and 10.44 − 7.98 = 2.46 m is a normal height for
   a 1912 shaped false front; the 1994 parapet permit confirms there is a parapet
   substantial enough to need bracing; and the 0.75 m standard deviation says the
   rest of the roof is genuinely flat, so the maximum is one distinct element and
   not noise. Against: 188 South Park stands 15.93 m tall on the shared party wall
   and the DataSF outline is inflated 1.3 m across a 6.1 m width, so some cells at
   the south-west edge could be sampling the neighbour. The executing agent should
   settle it from a square-on Street View capture with a ground reference in
   frame. If it turns out to be bleed, the crest is the flank parapet, roughly
   8.6 m, and 2.7's step heights all move down.
2. **The footprint width: 6.10 m (OSM) or 6.99 m (parcel) or 7.44 m (DataSF)?**
   The plan takes OSM's 6.10 m because it is the only outline that shares nodes
   with both neighbours' rings — i.e. the only one that describes party walls —
   and because it matches the visible roof edge in the registered Esri overlay.
   An angular estimate off the Street View capture (facade spanning ~33.6° at
   ~11 m) gives ~6.6 m, between OSM and the parcel. If better imagery shows the
   building filling its 6.99 m lot, widening to 6.9 m is acceptable; re-derive the
   anchor if you do, and re-run the 2.13 measurement, because the floor of the
   exclusion window is only 1.07 m.
3. **Construction type is inconsistent in the permit record.** Six permits say
   `constr type 3`, one says `wood frame (5)`, and the building is absent from
   DataSF's unreinforced-masonry list even though it took a 1994 parapet-plus-
   seismic-upgrade permit. Nothing here changes the model. It is recorded because
   `REFERENCE.md` will be tempted to state a structure, and it should not state
   one confidently.
4. **The second-floor bay count is inferred.** Three, from the three parapet
   panels. A street tree hides the middle of the facade in the Jan 2025 Street
   View capture. Earlier captures should settle it — the pano's date picker was
   not reachable in the authoring session, but it exists.
5. **The rear elevation is entirely unobserved.** One permit-confirmed fire
   escape and nothing else. It faces a 9.5 m rear yard that no public vantage
   reaches. Model it plain and say so.
6. **164 South Park is in flux.** The Jan 2025 Street View capture shows plywood
   hoarding and a graffiti fence in front of a low red-painted structure on the
   neighbouring lot, while DataSF still records a 9.25 m building there. If that
   lot is rebuilt, the north-east party wall could become an exposed elevation.
   That would be a revision to this asset, not a reason to design the flank now.
7. **The 4.73 m LiDAR minimum is unexplained** but harmless: on a 6.1 m wide
   footprint with a 1.3 m inflated outline, the low cells are almost certainly
   edge cells falling on the rear yard or the front setback strip rather than on
   any part of the building. It does not imply a stepped massing.
8. **Neither OSM nor Overture carries a height for this building.** OSM way
   124884342 has no `height` tag and the Overture record inherits none, so unlike
   181 South Park there is no wrong number to inherit — but it also means the
   DataSF LiDAR is the *only* height source, which is why risk 1 matters as much
   as it does.
