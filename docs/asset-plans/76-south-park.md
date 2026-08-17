# 76–82 South Park — SF-SIM asset plan

A 22-foot-wide 1906 post-earthquake flats building on the north-west rim of the South
Park oval, wedged party-wall-to-party-wall between 70 and 84 South Park. Four levels
over a 6.9 m frontage and a 29.7 m depth — the narrowest, deepest thing in this whole
set. Its identity is a **two-storey canted bay in dark bronze-brown board, cantilevered
off a rusticated cast-stone pier with a tall arched opening**, and a **roof deck** with
a stair penthouse that is the only part of it the app's camera will see most of the
time.

This is the eighth South Park rim building to enter the manifest by hand, and the first
with no name, no architect, no landmark status and no published description of any kind.
Everything below the assessor roll is read off photographs. The design brief is "the
narrowest bay-fronted sliver on the oval, and proud of it" — not "landmark".

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/76-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `76-south-park` |
| Registry id | `76SouthPark` (`camelId()` in `app/src/assets.js` maps one to the other) |
| Existing procedural builder | none — new landmark (**Case B**: needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3940150, 37.7820265` (DataSF LiDAR area centroid, `SF3775054`) |
| Target height | **16.28 m** to the roof-stair penthouse crest (LiDAR max); roof deck **13.08 m** (LiDAR median, measured). The penthouse attribution is this dossier's weakest claim — see 2.1 and 2.15 risk 1 |
| Footprint | 6.90 m (South Park frontage, SE) × 29.70 m deep; 204.9 m², reconciled from three disagreeing sources (2.3) |
| Triangle cap | 9,000 |
| Category | `2` (Apartments) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 76–82 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 76–82 South Park in San Francisco and deliver it
as a downloadable, validated GLB.

Do not integrate or deploy the model yet. Create the asset, validate it, render review
images, and commit the deliverables to your working branch.

## Read the project sources first

Before any research or modeling, read in this order:

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-miniature-style/SKILL.md`
5. `.agents/skills/sf-asset-check/SKILL.md`
6. `app/public/sf-assets/landmarks_manifest.json`
7. `artifacts/106-south-park/` — the closest reference implementation: the same oval, the
   same era, the same 45°-rotated narrow-and-deep party-walled plan, the same
   two-visible-elevations problem
8. `artifacts/108-south-park/` — second reference, for how a shorter neighbour's exposed
   flank strip was handled
9. `docs/asset-plans/76-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules. Do not invent a new style and do not copy
visual instructions from unrelated prompts.

## This dossier is thin, and you must treat it that way

Unlike 104–106 South Park, this building has **no National Register nomination, no
architect attribution, no published architectural description and no name**. The only
survey-grade numbers in Part 2 are the SF Assessor roll, the DataSF LiDAR footprint
statistics, and the OSM trace. Every statement about what the building *looks like* is
read off two photographs and one January 2025 Street View pano. Re-verify before you
model, and say in `REPORT.md` what you confirmed, what you corrected, and what you could
not settle.

## Must capture

- The **extreme proportion**: 6.9 m of frontage running 29.7 m back, four levels tall.
  This is the thing. Do not let it drift toward a squarer, friendlier box.
- The **two-storey canted bay** on the north-east half of the street front — a classic
  San Francisco slanted bay with a wide front light and two narrow angled returns,
  clad in dark bronze-brown board, carried on a corbel out of the stone pier below
- The **rusticated cast-stone base** — a mottled warm tan-grey ashlar covering the
  ground and first levels, with a **tall arched opening** in it. This is the one
  genuinely unusual thing on the building and the strongest recognition cue after
  the proportion.
- The **large industrial multi-pane grid window** on the south-west half of the upper
  street front, in dark frames — the counterweight to the bay
- The ground floor's three-part rhythm: a **plain dark service bay** at the south-west
  end, the **recessed entry** under the stone pier, and the **storefront glazing** to
  the north-east — plus the slim first-floor **balcony railing** over the entry. (The
  documented two-car garage is *not* confidently locatable on this elevation; see 2.4.)
- The **roof deck**: real, documented, furnished, with a barbecue, and the stair
  penthouse that serves it — from the app's camera this roof is the building
- The **step down to 84 South Park**: the south-west party wall is exposed for a band
  of about 1.7 m above 84's roofline. The north-east wall against 70 is not — 70 is
  only 0.21 m shorter and that edge should read as continuous.

## Research 76–82 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint width, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The south-east street elevation on the park, in better light than the January 2025
  pano — it is a north-west-facing wall under a full-grown street tree and every
  available image of it is shaded
- Aerial and roof views. **The roof is the priority**: the deck layout, the railing,
  the penthouse, and whatever mechanical plant is up there
- The north-west rear elevation and the rear yard, which the 311 record says is used
  for parking and which no available photograph shows
- Day and night appearance
- Whether the bay is on the north-east half and the grid window on the south-west, or
  mirrored — the dossier's reading is from a single oblique pano and is *inferred*
- The current state of the painted mural on the stone pier (see 2.4)

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**Four source conflicts are already known and are NOT resolved — do not silently
inherit a number from any of them (see 2.1 and 2.15):**

1. **The crest.** The 2010 LiDAR maximum over this footprint is 16.28 m, 3.20 m above
   the 13.08 m roof deck. The neighbouring 70 South Park reports an almost identical
   maximum (16.35 m) over its own footprint while its deck is 12.87 m. **One tall
   element sits at or near the shared party wall and the LiDAR cannot tell you which
   building owns it.** This plan attributes it to 76–82 on photographic grounds
   (2.1). Re-derive it and say how. If it belongs to 70, drop the penthouse and
   retarget to the parapet crest.
2. **Storey count.** The assessor roll says **3 stories**; the leasing agent lists
   **four** separate tenancies by floor (82 = 1st, 80 = 2nd, 78 = 3rd, plus 76); the
   January 2025 pano shows a ground floor plus three upper levels. Build **four
   levels** — but do not treat the assessor's 3 as an error without saying so.
3. **Floor area.** The assessor says 3,928 sq ft; the commercial listing says 6,100 sq
   ft; the four advertised floor plates sum to 6,000 sq ft. The assessor figure cannot
   cover four levels on this footprint. Model the volume from the measured footprint
   and the measured height, not from any floor area.
4. **Width.** OSM traces 7.22 m, the DataSF LiDAR raster gives 6.93 m, and the
   assessor's lot area over its lot depth gives 6.71 m. This plan uses **6.90 m**.
   Say which you used.

## Create a reference dossier

Write `artifacts/76-south-park/REFERENCE.md` containing: source links and what each
one establishes, the measured footprint and how it was derived, the height derivation
with its uncertainty stated, the orientation, an elevation-by-elevation description,
the palette map, and an explicit list of every correction you made to this plan.
**REPORT beats plan, always** — if you find this dossier wrong, the artifact is right
and the plan is stale.

## Make your own design decisions

The massing recipe in 2.7 and the palette in 2.8 are a starting point, not a
specification. You are the modeller: if the aerial shows the roof deck is at the rear
rather than the front, or the bay is three-sided rather than canted, or the stone base
covers only the ground floor, follow what you find. Log every deviation in `REPORT.md`.

Review renders from the high three-quarter aerial FIRST and iterate there, before you
run the formal rig. That is the camera the app actually uses.

## Scope of the exported asset

Export the single building: the four-level volume on the measured footprint, the
rusticated stone base with its arched opening, the canted bay, the grid window, the
garage door, the storefront and entry, the exposed south-west flank band, the plain
north-west rear elevation with its rear stair, and the flat roof with its deck,
railing, stair penthouse and mechanical plant.

Do not include unrelated surrounding city geometry: 70 South Park, 84 South Park, the
South Park oval or its lawn and trees, the street trees in front of the building,
the street, the sidewalk, parked cars, people, plinths, cameras or lights. Temporary
context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project palette;
`_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no cameras, lights,
animations, armatures or constraints; at most 9,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric`
in `app/src/assets.js` only scales and positions). The street facade faces **135.0°**
and the long axis runs back at **315.0°**. Build on the measured rectangle in 2.3 rather
than modelling an axis-aligned bar and rotating it. Record the measured heading in
`REPORT.md`.

**Height normalization:** the tallest geometry in the export (the roof-stair penthouse
crest) must land at exactly **16.28 m** so the loader's `targetHeightM / measuredHeight`
scale is 1.0. If your research kills the penthouse, renormalize to whatever the new
crest is and update the manifest draft — do not leave a 16.28 m target on a 13.5 m
building.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/76-south-park/build_76_south_park.py` (deterministic build script),
`artifacts/76-south-park/76-south-park.blend`, and
`artifacts/76-south-park/76-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras: `76-south-park-top.png`,
`-north.png`, `-east.png`, `-south.png`, `-west.png`, plus
`76-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty render
`76-south-park-aerial.png`, and a night render `76-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the roof plane, the deck, the penthouse and the parapet at
the street end; the aerial view uses the style bible's camera assumptions (30–50 degrees
down, long lens). Simple tabletop lighting, neutral warm background, minimal depth of
field, and every image must depict the same exported model.

Because the building is **more than four times deeper than it is wide** and stands at
135°, frame all four elevations to the long dimension and accept empty frame on the
north and east views rather than zooming each view to fit — the reviewer needs to be
able to compare them. Add one extra view looking square-on at the 135° street facade;
the four cardinal elevations all show this building obliquely and none of them shows
its public face properly. Add a second extra view looking straight down the roof.

## Validate the exported GLB

Re-import `76-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Render at least one review image from the re-imported asset. Write
`artifacts/76-south-park/validation.json` and `artifacts/76-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **25.9 × 25.9 m** even though
the building is 6.9 × 29.7 m — that is the exact consequence of a 45° heading on a long
thin box, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "76-south-park",
  "file": "76-south-park.glb",
  "anchor": [
    -122.3940150,
    37.7820265
  ],
  "targetHeightM": 16.28,
  "cat": 2,
  "name": "76–82 South Park",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`"estimated": true` is deliberate and is the honest reading: the roof deck at 13.08 m
is measured, but the 16.28 m crest that the asset is normalized to is an attribution,
not a published figure. See 2.1.

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/76-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify anything
it relies on.

### 2.1 Verified facts

| Fact | Value | Source / status |
|---|---|---|
| Address | 76–82 South Park (the street is signed "SOUTH PARK"; Google writes "76 S Park St"; one listing writes "76 S Park Ave") | SF Assessor `property_location = "0082 0076 SOUTH PARK ST"`; OSM `addr:housenumber = 76;78;80;82` |
| Block / lot | 3775 / 054 | SF Assessor secured roll; DataSF footprint `mblr = SF3775054`; `sf16_bldgid 201006.0026693` |
| Built | **1906** | SF Assessor `year_property_built`; independently repeated by Showcase and Augrented — **verified**, and the year makes it a direct post-earthquake rebuild |
| Storeys | assessor **3**; four tenancies let by floor; **four levels observed** | conflict, see 2.15 risk 2 |
| Units | 3 | SF Assessor `number_of_units = 3.0`, `number_of_rooms = 15.0`, `number_of_bathrooms = 3.0` |
| Property class / use | "Flats & Duplex" (`F`) / "Multi-Family Residential" (`MRES`); marketed as office / live-work | SF Assessor secured roll; The Hawthorne Group and Showcase listings |
| Zoning | `SPD` (South Park District) | SF Assessor; Showcase |
| Construction type | `D` (wood frame) | SF Assessor `construction_type` |
| Lot area / depth | 2,147.2 sq ft (199.5 m²) / 97.6 ft (29.75 m); `lot_frontage` not recorded | SF Assessor — implies a **22.0 ft (6.71 m)** lot width |
| Building area | 3,928 sq ft (assessor) vs 6,100 sq ft (listing) vs 6,000 sq ft (four floor plates summed) | **unresolved**, see 2.15 risk 3 |
| Advertised floor plates | 82 = 1st floor 1,600 SF · 80 = 2nd floor 1,400 SF · 78 = 3rd floor 1,500 SF · 76 = 1,500 SF | The Hawthorne Group — *observed (listing)* |
| Amenities that shape the model | **common roof deck**, furnished, with a barbecue, "open nights and weekends"; **two-car garage** | Zumper and The Hawthorne Group listings — *observed (listing)*, and the single most useful fact in this dossier for the roof |
| Ground elevation | 10.91 m min / 11.43 m median / 11.75 m max NAVD88 over the footprint — the site falls **0.84 m** toward the park | DataSF `ynuv-fyni` — **measured** |
| Roof deck | **13.08 m** above grade (LiDAR height median); majority 12.84 m; mean 11.86 m; σ 3.47 m; min 3.76 m | DataSF `ynuv-fyni`, 763 cells at 50 cm — **measured** |
| LiDAR maximum | **16.28 m** | same — **attributed** to this building's roof stair penthouse, not rejected; see below and 2.15 risk 1 |
| OSM `height` tag | 13 | OSM `way/124884340` — agrees with the LiDAR *deck*, not the crest, which is the usual OSM failure mode and here it is harmless |
| Facade heading | street elevation faces **135.0°** (SE, onto the oval); long axis 315.0° | measured from both footprint sources, which agree to 0.5° |
| Neighbours | **70 South Park** (lot 3775053, bearing 45°, NE party wall, LiDAR median 12.87 m — *0.21 m shorter*) and **84 South Park** (lot 3775055, bearing 225°, SW party wall, LiDAR median 11.36 m — *1.72 m shorter*) | DataSF parcels + `ynuv-fyni` — **measured**; this asymmetry is a design fact, see 2.4 |
| Owner / last sale | Siamak Akhavan Trust; 1997-11-12 | SF Assessor secured roll |
| Major works | 2007 renovation: HVAC, electrical panels, plumbing, fire sprinklers, dry standpipes, rear stairs. Earlier violation cluster 2002–04 covering stair repairs and window replacement. | DBI complaint record as summarised by Augrented — *secondary* |

**Why the 16.28 m maximum is kept rather than rejected.** 104–106 South Park's plan
rejected its LiDAR maximum because the tall cells sat on a party wall shared with a
*taller* neighbour, so bleed explained them. That argument does not apply here: 70
South Park's roof deck (12.87 m) is **lower** than this building's (13.08 m), so 70
cannot be the source of a 16.3 m return. Both footprints report a maximum near 16.3 m
because one tall element straddles or abuts their shared boundary — and it must belong
to one of them. Two things point at this building:

- Both listings document a **common roof deck** here. A deck needs a stair bulkhead,
  and 2.4–3.0 m is exactly what one measures.
- The Hawthorne Group's own exterior photograph shows a **dark box standing above the
  roofline** toward the north-east (70-facing) side of this building, plus a smaller
  vent at the south-west edge.

A photogrammetric check on that photograph supports it. Working in the 1067 × 800
original: the horizon sits at about y = 660, the building's roofline at y = 318, and the
roofline is 13.08 m above grade — so the 342 px from horizon to roofline subtend
`atan(11.58 / D)` and calibrate the image at about 23.8 px per degree for a camera
roughly 45 m out in the park. The dark rooftop box tops out at y = 290, i.e. 370 px
above the horizon, i.e. 15.55°. Solving for height at various setbacks:

| Setback behind the facade | Camera distance | Implied crest |
|---|---|---|
| 0 m (on the facade plane) | 45 m | 14.0 m |
| 6 m | 51 m | 15.7 m |
| 10 m | 55 m | **16.8 m** |

A rooftop bulkhead standing on the facade plane would be very unusual; one set back
8–11 m on a 29.7 m deep roof is exactly normal, and that band brackets 16.28 m. The
naive same-plane reading (14.0 m) is the only one that contradicts the LiDAR, and it is
the one geometrically implausible case.

Two caveats remain, and they are why this is still risk 1. The box in the photograph is
centred **on or just past the party wall** with 70 — it spans roughly x = 570–668 where
this building's right edge is near x = 610 — so it may be a shared or mirrored structure
serving both buildings, or 70's alone. And the photograph is undated. **Model the
penthouse as a separate, cleanly deletable object** so that if better imagery kills it,
the fix is one deletion plus a renormalization rather than a rebuild.

### 2.2 Sources

- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property
  Tax Roll), `block='3775' AND lot='054'` — build year, storeys, units, class, use,
  zoning, lot area and depth, construction type, ownership. The single most reliable
  source in this dossier.
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints,
  LiDAR-derived, 2010 survey), `mblr = SF3775054` — footprint polygon, ground
  elevation, roof-deck height and maximum. Also queried for `SF3775053` (70 South Park)
  and `SF3775055` (84 South Park) to size the exposed flank and the exclusion radius.
- OpenStreetMap `way/124884340`, tagged `addr:housenumber = 76;78;80;82`,
  `addr:street = South Park`, `height = 13` — the building trace. Neighbour traces
  `way/124884345` (70) and `way/113545687` (84) confirm the shared party-wall edges.
- The Hawthorne Group, `https://www.thgcommercial.com/project/76-82-south-park-street/`
  — floor-by-floor tenancies, common deck, two-car garage, and the exterior photograph
  at `https://www.thgcommercial.com/wp-content/uploads/2024/03/76-82_South-Park.jpg`.
  *Observed (listing photo)*: this is the only clear whole-facade image found, it is
  taken from inside the park, and it is undated — the vehicles in it suggest the
  mid-2010s, so it may predate the current paint.
- Showcase, `https://www.showcase.com/76-82-s-park-st-san-francisco-ca-94107/37902715/`
  — total building size 6,100 SF, building class C, year built 1906, land 2,178 SF,
  zoning SPD. *Observed (listing)*.
- Zumper, `https://www.zumper.com/address/76-s-park-ave-san-francisco-ca-94107-usa` —
  "Common roof deck with furnishings and barbecue, open nights and weekends",
  "3 bedrooms/offices with views of South Park", "downtown views", double-paned
  windows, 1,500 sqft. *Observed (listing)*.
- Augrented, `https://augrented.com/sf/3775054-76-82-south-park` — a secondary
  aggregation of the DBI complaint and violation record and the assessor roll. Useful
  for the 2007 renovation scope; **not** used for any dimension.
- Zoneomics, `https://www.zoneomics.com/zoning-maps/california/san-francisco/76-South-Park-Street,San-Francisco,CA-94107/37.7819612/-122.3939021`
  — carries an address point at `37.7819612, -122.3939021`, which falls within 5 m of
  the measured street-end midpoint of the footprint and is the independent confirmation
  that the **south-east end is the addressed frontage**.
- Google Street View, January 2025, pano `xwBAWoi-oQKrwMaSWwutNA` at
  `37.7818698, -122.3939012` — the working views used for 2.4 were
  `https://www.google.com/maps/@37.7818698,-122.3939012,3a,100y,350h,118t/data=!3m7!1e1!3m5!1sxwBAWoi-oQKrwMaSWwutNA!2e0!7i16384!8i8192`
  (whole facade, with 84's door number and 70's number both in frame — this is what
  fixes the identification) and the same pano at `55y,354h,122t` and `18y,350h,110t`
  for the bay and the stone base. Adjacent pano `VNjTSqMURh5c_TFZCV6J3Q` at
  `37.7819313, -122.3938256` is labelled 70 S Park St.
- Google Maps satellite, `@37.782035,-122.394045,20z` (Airbus / Vexcel 2026) — the roof.
  At 20z this is about 0.12 m per CSS pixel, which is enough to see that the roof is
  occupied and not enough to lay out the deck. **This is the biggest research gap.**

**Not found, and searched for:** any architect attribution, any historic-resource
listing, any name for the building, any published architectural description, any
interior-free elevation photograph, and any oblique aerial. Exa searches on the address,
the address plus "architect", and the address plus "rooftop" returned only listing and
data-aggregator pages. Two searches surfaced *other* South Park buildings that are
well documented (One South Park, the Perkins&Will venture-capital fit-out at 101) and
neither is this building.

### 2.3 Orientation and placement

South Park is an oblong park whose rim buildings face inward. This one sits on the
**north-west rim**, between Jack London Alley and Bryant Street, and faces **south-east
across the oval**. It is not a through lot: the rear elevation opens onto a mid-block
yard, which the 311 record says is used for parking.

Three geometries exist and, unlike 104–106, they do **not** agree:

| Source | What it is | Width × depth | Verdict |
|---|---|---|---|
| OSM `way/124884340` | building trace tagged `76;78;80;82` | OBB **7.22 × 29.43 m** at 314.7°, area 212.5 m² | traces run generous; the polygon is a clean rectangle to within 0.4 m² |
| DataSF LiDAR footprint `SF3775054` | 2010 raster-derived built area, 20 vertices | OBB **6.93 × 30.60 m** at 314.2°, polygon area 190.6 m² | **authoritative for width** — it is a measurement of the structure, not a trace |
| SF Assessor | legal parcel | 2,147.2 sq ft over 97.6 ft depth ⇒ **6.71 × 29.75 m** | **authoritative for depth** — 97.6 ft is a recorded figure |

Design footprint: a plain rectangle **6.90 m × 29.70 m** (204.9 m²) centred on the
manifest anchor, long axis running back at 315.0°. That is the DataSF width and the
assessor depth, and it sits inside all three sources. In Blender coordinates (metres,
`+X` east, `+Y` north, origin on the anchor) the four corners are:

```
corner              X (east)   Y (north)   which end / which flank
street north-east    +12.940     -8.060    South Park frontage, 70 party wall
street south-west     +8.060    -12.940    South Park frontage, 84 party wall
rear   north-east      -8.060    +12.940   rear yard end, 70 party wall
rear   south-west     -12.940     +8.060   rear yard end, 84 party wall
```

The street frontage is the +12.940/+8.060 edge (6.90 m long, facing 135.0°); the two
long 29.70 m edges are the party walls, the north-east one facing 45° toward 70 South
Park and the south-west one facing 225° toward 84.

Because the heading is 45° off the axes, the axis-aligned XY bounding box of the bare
volume is **25.88 × 25.88 m**. That is correct and is not a scale error.

**Party walls on both sides, and only one of them shows.** The building abuts its
neighbours with no gap. The north-east wall (toward 70) is effectively invisible — 70's
deck is 12.87 m against this building's 13.08 m, so 0.21 m of wall is exposed and at
diorama scale that edge should read as a continuous roofline, not a step. The south-west
wall (toward 84) is exposed for its top **1.72 m**, because 84's deck is 11.36 m. Only
two-and-a-bit of the four elevations are ever seen: the south-east street front, the
north-west rear, and that thin band of south-west flank.

**Anchor choice.** Take the DataSF LiDAR area centroid, `-122.3940150, 37.7820265`.
The OSM polygon's centroid is 1.92 m away along the long axis, and the OBB centre
1.30 m away; the difference does not matter for placement but it decides the exclusion
radius (2.13).

### 2.4 What each side shows

**South-east (street elevation, the public face).** Four levels on 6.9 m of frontage.
Read from the January 2025 pano, north-east to south-west:

- A **rusticated cast-stone base** — mottled warm tan / grey-olive ashlar in courses —
  covering the ground level and rising as a vertical pier through the first. A **tall
  arched opening** springs from it; the arch is the strongest single detail on the
  building and reads at diorama scale.
- Out of that pier, a **corbel** carries a **two-storey canted bay** on the north-east
  half of the front: a wide front light with two narrow angled returns, one window per
  level per face, clad in **dark bronze-brown board**, sashes in a pale off-white.
- On the south-west half, set slightly back, a **large industrial multi-pane grid
  window** in dark frames — roughly four lights wide by three high — with a
  cantilevered soffit or shallow balcony over it.
- At ground level: dark storefront glazing to the north-east of the pier, and a
  recessed entry immediately under it. A **balcony with a slim metal railing** crosses
  the front at the first-floor line, just above the entry.
- A small blank plaque sits at the foot of the stone pier; the address numerals were
  not legible in any available image.

**Where the two-car garage is, is unresolved.** Both listings document one. The 2007
DBI complaint ("blocked access to the garage and the street") reads like a street
frontage, but the 311 record separately describes parking in the **rear yard**, and no
roll-up door is legible within this building's 6.9 m of frontage in either available
image — the roll-up shutter visible in the Hawthorne photograph is on a neighbour, well
to the south-west. Model the south-west end of the ground floor as a **wide plain dark
service bay** that can become a roll-up door or a plain wall once the research settles
it, and do not commit `Toy_steel` door grooves to the street front on present evidence.

**The mural.** The Hawthorne Group photograph shows a tall painted figure in warm ochre
and gold running down the stone pier, from the first level to the ground — a strong,
saturated, unmistakable identity mark. In the January 2025 pano the pier is largely
bare stone with only a small patch of colour surviving near its head. Either it was
painted out, or it has weathered, or the two images are the same wall in different
light. **Treat the mural as gone unless you can prove otherwise**, and if you keep an
accent, keep it small and at the top of the pier where the surviving colour is. Do not
paint a full-height mural from a photograph of unknown date. (AGENTS rule 5.)

**North-east flank (toward 70).** Not visible. 0.21 m of wall.

**South-west flank (toward 84).** A 1.72 m band of plain wall above 84's roofline,
running the full 29.7 m. This is the only place the building's depth is legible from
the ground, and in the baked city it reads for free because the shorter neighbour is
really there.

**North-west (rear).** No photograph found. The DBI record says there are **rear
stairs** (repaired 2002–04, worked on again in 2007) and the 311 record says the rear
yard is parked in. Model it plainly: a flat wall, a modest window grid, a rear stair,
and a service door. State in `REPORT.md` that it is unobserved.

**Roof.** See 2.9.

### 2.5 Recognition cues (ranked)

1. **The proportion.** 6.9 m wide, 29.7 m deep, four levels. From the aerial camera
   this is a splinter, and that is the point.
2. **The canted bay**, two storeys of it, on a 6.9 m front — the bay occupies more than
   half the frontage, which is what makes the building read as a San Francisco house
   rather than a warehouse.
3. **The rusticated stone base and its arch**, pale against a dark body.
4. **The roof deck and its penthouse**, which is what the app's camera sees.
5. **The step down to 84**, a 1.72 m shoulder on the south-west side.
6. The large industrial grid window, which pairs oddly and memorably with the bay.

### 2.6 Miniature translation

The style bible's "chunky beveled massing, flat clean materials, restrained neutral
architecture with saturated accents" maps onto this building almost without argument,
with one warning: **at 6.9 m wide, every detail competes for the same few pixels.**
Six things, and no more, should survive the translation — the bay, the stone base, the
arch, the grid window, the garage door, and the roof deck. Everything else is bevel and
colour.

Exaggerate two things semantically, per the bible's licence:

- **The bay's projection.** Real canted bays project 0.6–0.9 m. Take it to ~1.0 m so
  the shadow line reads from above.
- **The arch.** Give it a definite, generous radius rather than the shallow segmental
  head the photograph suggests, so it survives at 4 px.

Do **not** exaggerate the height or the width. This building's whole character is that
it is thinner than it ought to be, and the row on either side is real geometry that will
call out any cheating.

### 2.7 Massing recipe

1. Base volume: 6.90 × 29.70 m rectangle, extruded to **13.08 m** (the roof deck),
   long axis at 315.0°, origin at base centre, min Z = 0. Bevel 0.12 m, 2 segments.
2. Parapet: a 0.35 m lift on the street end and both flanks, from 13.08 to **13.43 m**,
   inset 0.15 m from the wall plane.
3. Stone base: a 0.10 m proud skin on the street elevation only, from z = 0 to
   **z = 6.6 m** (ground plus first level), in `Toy_stone`, with two horizontal
   rustication grooves.
4. The arch: a round-headed recess 2.2 m wide, springing at z = 3.6 m, crown at
   z = 4.7 m, cut 0.35 m into the stone skin, faced in `Toy_ink`.
5. Corbel: a 1.0 m deep wedge under the bay, z = 6.4 to 7.0 m, in `Toy_stone`.
6. Canted bay: from z = 7.0 to 12.9 m, on the north-east half of the front, front face
   2.4 m wide projecting 1.0 m, two 0.9 m angled returns. Two levels of glazing, one
   window per face per level, six lights in all.
7. Grid window: on the south-west half, z = 7.4 to 10.2 m, 2.6 m wide, a 4 × 3 mullion
   grid in `Toy_trim`, glazing `Toy_glass`, recessed 0.15 m.
8. Soffit / shallow balcony over the grid window at z = 10.6 m, 0.5 m deep.
9. Ground floor: storefront band z = 0.4 to 3.2 m on the north-east third, `Toy_glass`
   behind `Toy_trim` mullions; recessed entry 1.1 m wide, 0.5 m deep, under the pier;
   a plain dark service bay 2.6 m wide, z = 0 to 3.0 m, at the south-west end, in
   `Toy_ink` — **not** a detailed roll-up door until the garage question in 2.4 is
   settled.
9a. Balcony: a 0.25 m deep ledge with a slim `Toy_steel` railing across the front at
   z = 6.9 m, over the entry.
10. South-west flank band: a value change over the whole 29.7 m face, above
    **z = 11.36 m** only, in `Toy_sand`.
11. Rear elevation: plain `Toy_roofd` face, a 2 × 3 window grid, one service door, and
    a simple external stair in `Toy_ink` running to level 2.
12. Roof: flat deck at 13.08 m in `Toy_roofd`, with the deck platform, railing,
    penthouse and plant of 2.9 laid on top.
13. Stair penthouse: 2.6 × 3.2 m box, from 13.08 to **16.28 m**, set back 8–11 m from
    the street end, toward the north-east party wall. **This is the tallest geometry
    and it sets the normalization.**

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette (hexes quoted from
`.agents/skills/sf-asset-check/SKILL.md` §7).

| Material | Hex | Used for |
|---|---|---|
| `Toy_ink` | `#3a3530` | the dark bronze-brown board body and the canted bay — the building's body colour — plus the arch reveal, the entry recess and the rear stair |
| `Toy_stone` | `#d9d2c2` | the rusticated cast-stone base, the pier and the bay corbel |
| `Toy_trim` | `#f3efe6` | window sashes, bay trim, grid-window mullions, storefront mullions, parapet cap |
| `Toy_glass` | `#2a4d73` | all windows, the storefront band |
| `Toy_steel` | `#9aa0a6` | roof-deck railing, the first-floor balcony railing, rooftop mechanical plant |
| `Toy_roofd` | `#45454a` | the roof deck membrane and the north-west rear elevation |
| `Toy_sand` | `#ece4d4` | the exposed south-west flank band above 84 South Park |
| `Toy_brick` | `#c96f4a` | the roof-deck timber decking — the one warm note, and it is genuinely there |
| `Toy_gold` | `#caa64a` | **optional**, at most 0.6 m², the surviving patch of mural colour at the head of the stone pier. Omit it if the research says the mural is gone. |
| `Toy_glassl_Glow` | `#6f95b8` | three lit windows at night |
| `Toy_trim_Glow` | `#f3efe6` | a thin warm spill in the entry recess, and a low warm line along the roof-deck railing |

Two notes on colour:

- **The body hue is the weakest colour observation.** The January 2025 pano is a
  north-west-facing wall in shade under a street tree, and the Hawthorne photograph is
  in full sun but possibly a decade old. Both agree the body is **dark and warm** and
  that the base band is **distinctly paler**; neither pins the hue. `Toy_ink` over
  `Toy_stone` reproduces that relation with palette entries. If better photography
  turns up and the body is, say, a true chocolate rather than a warm near-black, say so
  in `REPORT.md` and adjust.
- **The roof decking is the accent, not the facade.** The bible wants saturated accents
  used sparingly, and on a building this narrow the facade cannot carry one without
  turning into a toy. The deck can: it is warm, it is real, it is documented, and it is
  on the surface the camera actually looks at.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
glazing — the app renders `_Glow` in a separate layer that is not fully transparent by
day, so a primary surface must never be authored as glow, and a closed glow shell reads
as two stacked layers and will tint the facade in daylight. Author open shells only.

Hero glow: **three** windows lit — two in the bay (different levels, not stacked) and
one in the grid window. This is three flats on a quiet residential oval; a fully lit
grid would read as an office. Supporting accent: a thin warm spill in the entry recess,
which at night is also what tells the eye the recess is a door, and a low warm line
along the roof-deck railing, which is the one place this building is documented to be
used after dark ("open nights and weekends"). The storefront, the garage door, the rear
elevation and the stone base do not glow.

### 2.9 Top surface

A 6.90 × 29.70 m flat rectangle at 13.08 m — 205 m², seen constantly from above and,
apart from the street facade, from almost nowhere else. Three things carry it:

1. **The roof deck.** Documented twice, furnished, with a barbecue. This is the roof's
   subject. Put it on the **street (south-east) third** — that is where the "downtown
   views" and "views of South Park" the listing sells actually are — as a raised timber
   platform in `Toy_brick` with a `Toy_steel` railing, and leave the rear two-thirds as
   plain membrane.
2. **The stair penthouse**, 2.6 × 3.2 m, rising 3.20 m to the 16.28 m crest, set back
   from the street end toward the north-east party wall. It is both the tallest thing
   on the asset and the reason there is a deck at all.
3. **The stepped neighbours.** The roof sits 1.72 m above 84's and 0.21 m below 70's,
   so in the baked city this asset's roof plane is a distinct step **on one side only** —
   a shoulder to the south-west and a flush join to the north-east. Get that asymmetry
   right; it is the cheapest realism available here.

**The open question is the deck's position and the plant.** The 20z satellite is enough
to show the roof is occupied and not enough to lay it out, and no oblique aerial was
found. Settle it before building. If the deck turns out to be at the **rear**, over the
low structure that the LiDAR minimum (3.76 m) hints at, then item 1 moves and the roof
reads completely differently — so do not build the deck until you have looked. Do not
split the difference by scattering token furniture over the whole roof.

**What the 3.76 m LiDAR minimum probably is.** About 16% of the footprint's cells sit
near 4 m — reconciling the 11.86 m mean against the 13.08 m median needs roughly that
fraction low. Over a 6.9 m width that is about 4.5 m of the rear depth at one storey.
Most likely a single-storey rear structure or a covered part of the rear yard. It is
*inferred* from the statistics alone, it is at the invisible end of the building, and
it should be modelled only if the aerial confirms it.

### 2.10 Scope

**In the GLB:** the single building — the four-level volume on the measured footprint,
the rusticated stone base with its arch and pier, the canted bay, the grid window and
its soffit, the storefront, the recessed entry, the garage door, the exposed south-west
flank band, the plain rear elevation with its rear stair and service door, and the flat
roof with its deck, railing, stair penthouse and mechanical plant

**Not in the GLB:** 70 South Park, 84 South Park, the South Park oval, its lawn, paths
or trees, the street trees in front of the building, the rear yard, fences, the street,
the sidewalk, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 9,000 — higher than 104–106's 7,000 because a canted bay, an arched head and a
furnished roof deck are all curved or faceted, and lower than a hero because nothing
here is a monument. Suggested split: main volume ~300; parapet ~250; stone base with
rustication grooves ~600; arch head ~700; corbel ~150; canted bay shell ~900; six bay
windows with trim ~1,800; grid window with a 4 × 3 mullion grid ~900; soffit ~150;
storefront and entry recess ~600; garage door with grooves ~350; flank band ~120; rear
elevation, windows, door and stair ~900; roof deck platform and railing ~800; penthouse
~250; mechanical plant ~250; bevel overhead ~500. If the first build lands above 9,000
the answer is fewer window subdivisions and a coarser arch, not a raised cap.

### 2.12 Draft manifest entry

```json
{
  "id": "76-south-park",
  "file": "76-south-park.glb",
  "anchor": [-122.3940150, 37.7820265],
  "targetHeightM": 16.28,
  "cat": 2,
  "name": "76–82 South Park",
  "estimated": true,
  "dims": [25.88, 25.88, 16.28],
  "tris": 0,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders for the built numbers. `cat: 2` is `Apartments` in
`CATEGORY_LABELS` (`app/src/context.js`), which is what the assessor calls it
("Flats & Duplex", "Multi-Family Residential") whatever the leasing agent markets it as.
`estimated: true` because the normalization height is an attribution — see 2.1.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '76SouthPark'`) and
  re-bake the affected tiles, or the baked procedural building will intersect the GLB.
  This is the Case B path in `docs/asset-plans/INTEGRATION-PROMPT.md`.

- **The exclusion window is tight — 2.1 m wide.** `excluded()` in
  `pipeline/buildings.mjs` drops a footprint when its centroid **or any ring vertex**
  falls inside the circle.

  **Measure on the SIMPLIFIED ring, not the raw one.** `addBuilding()` runs
  `simplifyRing(ring, 0.6)` *before* it calls `excluded()`, so the ring the gate sees is
  not the ring in the geojson. On this site that moves the window in both directions —
  84 South Park's nearest vertex goes out from 3.64 m to 3.97 m and this footprint's own
  OSM centroid comes in from 1.92 m to 1.83 m. Distances from the manifest anchor
  against the simplified rings:

  | Polygon | Triggers at | Via |
  |---|---|---|
  | this building (`SF3775054`) | **0.18 m** | its own centroid |
  | this building, OSM `way/124884340` as an Overture proxy | **1.83 m** | its centroid |
  | 84 South Park (`SF3775055`) | **3.97 m** | nearest ring vertex |
  | 84 South Park, OSM `way/113545687` | 5.52 m | nearest ring vertex |
  | 70 South Park (`SF3775053`) | 7.20 m | centroid |
  | 70 South Park, OSM `way/124884345` | 7.34 m | centroid |

  The safe window is therefore **(1.83, 3.97) m** — it has to exceed 1.83 so the
  Overture gap-fill version is dropped too (`addBuilding()` returns null on exclusion,
  so `markOccupied()` never runs and `occupiedFraction()` cannot be relied on to block
  a re-add), and stay under 3.97 so 84 South Park survives. **Use `exclude: 2.9`** —
  1.07 m either side, dead centre, but still only half the room 104–106 had. Confirm
  against the real `pipeline/data/overture_buildings.geojsonseq` at integration time and
  prove the outcome with `pipeline/verify-rebake.mjs`: check **which** rings were
  dropped, not how many — DataSF and Overture both trace some buildings on this oval, so
  two rings disappearing can be correct and one disappearing can be wrong.

- **84 South Park is the one to watch.** Its nearest ring vertex is 3.64 m out because
  the two buildings share a party wall and the raster traces run right up to it. If the
  Overture geometry differs from the DataSF geometry by even half a metre on that edge,
  the window can close. Re-measure against Overture before committing, and if the
  window collapses, move the registry point (not the manifest anchor) a metre
  north-west along the long axis and re-measure.

- **`exclude` is also the tree-clear and street-furniture radius.** At 2.75 m it clears
  neither, which is correct: the street trees in front of this building are real, they
  are in every photograph of it, and they should stay. Do **not** set `clearTrees: true`.

- `loadRadius`: the default formula gives `max(2500, 16.28 × 30) = 2500` m. Take the
  default. Nothing about a 205 m² flats building justifies `alwaysLoaded`. Note what the
  fallback past that radius is: this is Case B with **no procedural builder**, so beyond
  2500 m the site is empty ground rather than a stand-in block. At 2.5 km, on a 6.9 m
  frontage, that absence is illegible.

- **Camera preset.** In `app/src/camera.js` the rig places the camera at
  `(sin(yaw), sin(pitch), cos(yaw)) × distance` from the pivot, and the project's `+z`
  is **south**, so `yaw: 45` puts the camera south-east of the building, looking
  north-west at its street elevation — the only view of this building worth flying to.
  **Settled against `app/src/camera.js:119-127` rather than against a neighbour's
  comment:** `apply()` sets `position = pivot + distance × (sin yaw, sin pitch, cos yaw)`,
  and the project's `+z` is south, so `yaw: 45` puts the camera south-east — square onto
  the 135° front. Shipped `camera: { distance: 130, yaw: 45, pitch: 26 }`; 130 m rather
  than the ~90 m the height suggests, because the building is 29.70 m long. This also
  resolves the disagreement 104–106's plan flagged: `126SouthPark`'s comment is right and
  `64SouthPark`'s "app yaw = 180 − true bearing" is wrong. Neither was edited here — the
  integration prompt forbids touching another landmark — but it is worth a follow-up.

- **This one has no case for the bespoke route, and that should be said plainly.**
  104–106 earned it — a named, NR-nominated, architect-attributed building with a
  survey-grade description and real cultural significance. 76–82 has none of that: it is
  an anonymous 22-foot sliver whose entire documentary record is a tax roll and three
  rental listings. It is being built because it was asked for, and it will be a good
  asset, but `KIT-INTEGRATION-PROMPT.md` is what this building is for, and the argument
  that the next anonymous sliver on this oval should be a kit piece is now two plans old.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly **16.28 m** (loader scale lands at 1.0) — or the
      re-derived crest, with the manifest draft updated to match
- [ ] Roof deck plane lands at **13.08 m**
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~25.9 × 25.9 m is
      expected for a 6.90 × 29.70 m building at 45°)
- [ ] Frontage 6.90 m and depth 29.70 m, not rounded toward a squarer plan — this is the
      single most likely way to get this asset wrong
- [ ] The canted bay is on the **north-east** half of the frontage and the grid window
      on the south-west (not mirrored), or the research says otherwise and `REPORT.md`
      records it
- [ ] The south-west end of the ground floor is a plain dark service bay, **not** a
      detailed roll-up door (see 2.4 — the garage position is unresolved)
- [ ] The stair penthouse is a **separate, deletable object** (see 2.15 risk 1)
- [ ] The south-west flank band exists, in `Toy_sand`, only above 11.36 m
- [ ] The north-east flank has **no** step — 70 is only 0.21 m lower
- [ ] Roof deck present, on the street third unless research moves it; railing and
      penthouse present
- [ ] No full-height mural (see 2.4)
- [ ] Exactly three lit windows at night; glow shells open, never closed
- [ ] Triangles at or under 9,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`

### 2.15 Open questions and risks

1. **The crest, and therefore the normalization.** 16.28 m is a LiDAR maximum attributed
   to this building's roof-stair penthouse on the strength of a documented roof deck, a
   dark box visible above the roofline in one undated photograph, and a rough
   photogrammetric check that is consistent but not conclusive. 70 South Park reports an
   almost identical maximum. If the element belongs to 70, this asset is 3.2 m too tall
   in silhouette and the correct target is the parapet at ~13.43 m. **Settle this from
   an oblique aerial before building.** This is the highest-consequence open item in the
   dossier.
2. **Storey count.** Assessor 3, leasing 4, photograph 4. The plan builds four. If the
   assessor is right and one of the four "floors" is a mezzanine or the garage level,
   the facade divisions in 2.7 are wrong even though the height is not.
3. **Floor area.** 3,928 vs 6,100 vs 6,000 sq ft. Four levels of 205 m² is about
   8,800 sq ft gross, so *all three* published figures are below a full-plate reading —
   which is expected, since the upper levels do not cover the full lot depth. No floor
   area was used to derive any dimension in this plan, and none should be.
4. **Width.** 7.22 / 6.93 / 6.71 m from three sources. 6.90 m was chosen. The party
   walls mean the neighbours define the true width, so an error here propagates into the
   whole row when 70 and 84 are eventually built — record the choice prominently.
5. **The roof layout is unobserved.** No oblique aerial was found and the best nadir
   imagery is 0.12 m/px. The deck's position, the railing, the plant and the rear
   low structure are all *inferred*. Since the roof is what the app's camera sees, this
   is the second-highest-consequence gap.
6. **The rear elevation is entirely unobserved.** Nothing beyond "there are rear stairs"
   from a DBI complaint summary.
7. **The mural.** Present and dominant in one undated photograph, effectively absent in
   the January 2025 pano. Treated as gone. If it is in fact current, the building's
   single most memorable feature is missing from the asset.
7a. **The two-car garage.** Documented by two listings, but not locatable on the street
   front in either available image, and the 311 record points at the rear yard instead.
   Modelled as a neutral service bay so that either answer is a small edit.
8. **The body colour hue.** Dark and warm is solid; the exact hue is not.
9. **Every visual statement in 2.4 comes from two images.** There is no second
   photographer, no elevation drawing, and no survey. The confidence gap between this
   dossier and 104–106's is large and the executing agent should expect to correct
   things.
