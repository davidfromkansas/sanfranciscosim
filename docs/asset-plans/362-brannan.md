# 362 Brannan Street — SF-SIM asset plan

A 1925 SoMa industrial shop, still working: **Standard Sheet Metal & Marine Plumbing**
occupies it, and has done for decades. Not a monument and not even a converted one —
this is the block's last un-gentrified building, sitting between a venture-office
conversion and a design showroom. Its identity is a cream stucco street wall with
**dark bottle-green joinery**: a band of green-framed steel-sash factory windows over
the two-storey front bay, two green diamond lozenges in the frieze above it, a green
water-table stripe running the whole frontage, and three green roll-up freight doors on
the Varney Place back. A low-pitched ribbed metal roof shows over the front parapet.

It is the second Brannan Street building in this set (after `380-brannan`, four doors
southwest) and the design brief is the same: *the block's most memorable ordinary
building*, not a monument.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/362-brannan/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `362-brannan` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3937450, 37.7808430` |
| Target height | **8.6 m** to the ridge of the front bay's sloped roof; front eave/parapet ~7.1 m; main low-block roof deck 5.6 m |
| Footprint | 20.12 m (Brannan frontage, SE) x 24.79 m deep; 487.0 m2, measured |
| Triangle cap | 8,000 |
| Category | `19` (industrial) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 362 Brannan Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 362 Brannan Street in San Francisco and deliver
it as a downloadable, validated GLB.

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
7. `artifacts/380-brannan/` — the closest reference implementation: the same street,
   the same block face, the same "ordinary building done well" brief, the same ~45°
   heading and ~480 m2 footprint. Match its level of detail, not a civic landmark's.
8. `docs/asset-plans/362-brannan.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style and do
not copy visual instructions from unrelated prompts.

## Must capture

- The **two-part massing**: a taller two-storey bay at the southwest end of the Brannan
  frontage, and a long one-storey block filling the rest of the lot to Varney Place.
  Getting this step right is most of the job — a single flat box is the failure mode.
- The **steel-sash factory window band** on the two-storey bay: white/pale multi-light
  glazing inside a **dark bottle-green** frame and mullion system.
- The **two green diamond lozenges** in the plain frieze above the window band.
- The **green water-table stripe** running the full ground-floor frontage at about
  1.2–1.7 m, and the small dark slot windows set high in that low wall.
- The **low-pitched ribbed metal roof** over the front bay, sloping up away from the
  street — it is why the crest is higher than the street parapet.
- The Varney Place back: a plain cream wall with **three roll-up freight doors** (two
  green, one gray) and a continuous simple parapet.
- Cream/ivory stucco everywhere; green is the only other colour.

## Research 362 Brannan Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation,
and gather references covering:

- All four elevations, with particular attention to the height step between the
  two-storey bay and the one-storey block, and to where along the frontage it happens
- Aerial and roof/top views — the roof carries rows of skylights/monitors and mechanical
  units and the app's camera looks straight down at it
- Ground-level views on both Brannan Street and Varney Place
- Day and night appearance
- The number of window units in the steel-sash band and the number of lights in each —
  the dossier's "3 units, ~6 x 5 lights" reading is *inferred* from photography
- The number and spacing of the ground-floor slot windows
- Whether the two frieze diamonds are the only ones, or whether more continue across
  the blank part of the upper wall

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**Three source conflicts are already known and resolved in 2.1 and 2.15 — re-check them,
do not silently re-inherit the wrong value:** OSM `height=6` (source: Bing) is close to
the LiDAR *majority* of this roof, i.e. the low block, and is **not** the crest; the
assessor's "2 stories" is true only of the front bay, which is roughly a fifth of the
floor plate; and Google's address point and Street View pano for "362 Brannan St" sit on
**Varney Place**, at the back — the first pano you open is the rear elevation, not the
front, and the dusty-rose corrugated gate it faces belongs to the property across the
alley, not to this building.

## Create a reference dossier

Write `artifacts/362-brannan/REFERENCE.md` containing: source links and what each
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

This is a **secondary building** in the style bible's detail budget (§21), not a hero
landmark: clear massing, one strong facade rhythm, a simple designed roof, and exactly
two identity cues carried hard — the green window band and the green frieze diamonds.
Resist adding hero-tier ornament.

The finished asset must be immediately recognizable as 362 Brannan Street, consistent
with the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic low-poly,
and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single industrial block: the two-storey front bay, the one-storey body, all
four elevations' openings, the sloped front roof, the flat roof deck and its furniture.

Do not include unrelated surrounding city geometry: Brannan Street, Varney Place, the
neighbouring buildings on either flank (370 and 358 Brannan are party-wall neighbours),
street trees, the sidewalk, parked cars, people, plinths, cameras or lights. Temporary
context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms; no
negative scales; outward normals; no duplicate or foreign geometry; no image textures;
no transparency; flat-color materials named `Toy_*` from the project palette; `_Glow`
suffix only on surfaces that glow at night; no `Toy_body`; no cameras, lights,
animations, armatures or constraints; no external dependencies; at most 8,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric`
in `app/src/assets.js` only scales and positions). The Brannan Street entrance front
faces **southeast, bearing 134.8°**; the Varney Place back faces **northwest, 314.1°**.
The building is rotated roughly 45° off the world axes, so build directly on the
measured footprint polygon in 2.3 rather than modelling an axis-aligned box and rotating
it. Record the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the ridge of the front
bay's sloped roof) must land at exactly **8.6 m** so the loader's
`targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/362-brannan/build_362_brannan.py` (deterministic build script),
`artifacts/362-brannan/362-brannan.blend`, and `artifacts/362-brannan/362-brannan.glb`.
The script must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `362-brannan-top.png`,
`362-brannan-north.png`, `362-brannan-east.png`, `362-brannan-south.png`,
`362-brannan-west.png`, plus `362-brannan-contact-sheet.png`, at least one high
three-quarter aerial beauty render `362-brannan-aerial.png`, and a night render
`362-brannan-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the height step, the sloped front roof, the parapet ring, the
skylight rows and the mechanical cluster; the aerial view uses the style bible's camera
assumptions (30-50 degrees down, long lens). Simple tabletop lighting, neutral warm
background, minimal depth of field, and every image must depict the same exported model.

## Validate the exported GLB

Re-import `362-brannan.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Render at least one review image from the re-imported asset. Write
`artifacts/362-brannan/validation.json` and `artifacts/362-brannan/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **32 x 32 m** even though the
building is 20.1 x 24.8 m — that is the expected consequence of a ~45° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "362-brannan",
  "file": "362-brannan.glb",
  "anchor": [
    -122.3937450,
    37.7808430
  ],
  "targetHeightM": 8.6,
  "cat": 19,
  "name": "362 Brannan Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`,
or any app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in
`docs/asset-plans/362-brannan.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify anything it
relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | 1925 | SF Assessor secured roll, block 3775 lot 018 (consistent 2022-2025) |
| Use | Industrial | SF Assessor `use_code = IND`, unchanged through 2025 |
| Storeys | 2 | SF Assessor `number_of_stories = 2.0`; the 2014 permit also records 2 existing storeys. True of the **front bay only** — see 2.15 |
| Construction | Assessor construction type `C`; unreinforced masonry parapets | SF Assessor; SF building permits 1991-01-02 and 1992-03-25, both "parapet strengthening" (the UMB parapet-bracing programme) |
| Last roof work | 2014-05-20, "reroofing" | SF Building Permits, filed under street number 366 |
| Block / lot | 3775 / 018 | SF Assessor; DataSF building footprints (`mblr = SF3775018`) |
| Lot area | 5,279 sq ft = 490.4 m2 | SF Assessor — the building covers essentially the whole lot |
| Footprint | 487.0 m2; 20.12 m (SE frontage) x 24.79 m deep; 97.7% rectangular fill | DataSF LiDAR building footprint, reprojected — **measured** |
| OSM footprint (cross-check) | 479.9 m2, 24.39 x 19.67 m | OSM way/124890322 — agrees with DataSF within ~1.5 m |
| Main roof deck height | 5.63 m above ground | DataSF LiDAR `hgt_median_m` — **measured** |
| Most common roof height | 4.90 m | DataSF LiDAR `hgt_majoritycm` — **measured**; this is the one-storey block |
| Maximum feature height | 8.58 m above ground | DataSF LiDAR `hgt_maxcm` — **measured**; the ridge of the front bay's sloped roof |
| Front bay street parapet/eave | ~7.1 m | *inferred*, photogrammetric from the Brannan pano (2.15) |
| Ground elevation | 9.57 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Addresses | 362 and 366 Brannan Street; 25 Varney Place (rear) | OSM `addr:housenumber = 362;366`; "366" on the entrance door; "25 VARNEY PLACE" plaque on the rear wall |
| Current occupant | Standard Sheet Metal & Marine Plumbing | OSM node 10869882853 (`craft=metal_construction`); occupant website; door signage |
| Frontage heading | Brannan front faces 134.8° (SE); Varney back faces 314.1° (NW) | measured from the DataSF footprint polygon |
| Neighbours | 370 Brannan (SW, party wall), 358 Brannan (NE, party wall) | OSM ways 124890321 / 124890324; DataSF SF3775017 / SF3775020 |

### 2.2 Sources

- https://www.openstreetmap.org/way/124890322 — footprint, `addr:housenumber=362;366`,
  `building=yes`, `height=6` (`source=Bing`)
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived)
  — authoritative footprint polygon and the 4.90 / 5.63 / 8.58 m heights, and the
  neighbour footprints used for the exclusion radius in 2.13
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax
  Rolls) — 1925, block/lot, industrial use, storey count, 5,279 sq ft lot
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — the two parapet
  strengthening permits (1991, 1992) and the 2014 reroof
- Google Street View, Brannan Street pano `QGmjHr1j26kBQJg4CIIlyQ` (capture 2025) — the
  whole SE front elevation: cream stucco, green steel-sash band, frieze diamonds, green
  water table, slot windows, the "366" entrance, the height step, the ribbed roof
- Google Street View, Varney Place pano `zsvZkZZuwu-5Yt5suLIXbQ` (capture 2025) — the NW
  rear elevation: cream wall, three roll-up freight doors, "25 VARNEY PLACE" plaque, NFPA
  704 placard
- Google Maps satellite (Vexcel imagery, 2026) — roof: rows of skylights/monitors,
  scattered mechanical units, the sloped front roof reading darker than the flat deck
- https://standardsheetmetalsf.com/ and the Yelp listing for
  "Standard Sheet Metal & Marine Plumbing, 366 Brannan St" — occupant, address confirmation

Nothing was found in the architectural press, and no architect is recorded for the 1925
building in any source consulted. This building has no published history; the dossier is
built from municipal records plus photography, and that is the honest state of it.

### 2.3 Orientation and placement

The building sits mid-block on the northwest side of Brannan Street, running the full
depth of the block to the Varney Place alley — the same through-lot condition as
`380-brannan`, four doors southwest. It is rotated about 45° from the world axes, like
the whole SoMa grid.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
already centred on the anchor `-122.3937450, 37.7808430`. Vertices run clockwise viewed
from above, starting at the north corner; the sub-metre segments are survey jogs at the
corners:

```
( -1.653,  15.662)   north corner
(  5.955,   8.023)
(  6.729,   7.498)
(  6.622,   7.395)
( 14.815,  -1.242)
( 14.547,  -1.488)
( 15.392,  -2.180)   east corner
(  2.037, -15.118)
(  1.531, -14.656)
(  1.102, -15.100)
(  1.065, -15.052)   south corner
(-15.870,   1.705)   west corner
( -1.735,  15.745)
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(15.392,-2.180) -> (2.037,-15.118)` | 18.59 m | SE 134.1° | **Brannan Street front** (plus corner jogs, 20.1 m overall) |
| `(1.065,-15.052) -> (-15.870,1.705)` | 23.82 m | SW 225.3° | southwest flank — party wall to 370 Brannan |
| `(-15.870,1.705) -> (-1.735,15.745)` | 19.92 m | NW 314.8° | **Varney Place back** |
| `(-1.653,15.662) -> ... -> (14.815,-1.242)` | 10.78 + 11.90 m | NE 44.9° / 43.5° | northeast flank — party wall to 358 Brannan, with a slight jog |

Because of the 45° heading the axis-aligned bounding box is ~32 x 32 m. That is correct.

**The height step.** The two-storey bay occupies the **southwest end of the Brannan
frontage**, i.e. the corner shared with 370 Brannan. Its extent is *inferred*: the LiDAR
statistics (mean 5.74 m, median 5.63 m, std 0.96 m against a 4.90 m majority and an
8.58 m max) put only about 8–20% of the roof area above the low block, which for a
~11–12 m frontage share means the bay is roughly **12 m wide x 8 m deep**. Photography is
consistent with the bay covering something under half the frontage. Confirm before
committing to the massing; this is the single most consequential *inferred* number in
this dossier.

### 2.4 What each side shows

**Southeast (Brannan Street front)** — The hero elevation, and a study in two heights.
The southwest portion rises two storeys in cream stucco and carries a continuous band of
**steel-sash factory windows**: pale/white multi-light glazing (roughly three units,
about six lights across and five high each, *inferred*) set inside a **dark bottle-green**
perimeter frame with green mullions at the unit divisions. Above the band, a plain
stucco frieze carries **two dark green diamond lozenges**, evenly spaced, and above that a
simple cornice band with the ribbed metal roof visible sloping up and back behind it.
The rest of the frontage, to the northeast, is a single-storey cream wall: plain stucco,
a **dark green water-table stripe** at roughly 1.2–1.7 m running the whole width, and
three or four small dark horizontal slot windows set high in the wall. The entrance sits
at the step: a narrow glazed aluminium storefront with "366" above it and the
Standard Sheet Metal signboard beside it. A faint ghost sign survives on the upper wall.

**Northwest (Varney Place back)** — Plain painted cream wall, a continuous simple
parapet that steps very slightly along its length, and **three roll-up freight doors** —
two dark green corrugated, one gray — plus a green corrugated infill panel at the
southwest end. No windows. A dark plaque reads "25 VARNEY PLACE"; an NFPA 704 placard sits
beside it. The alley is narrow, so this face is only ever seen obliquely in the real
world — but the app's aerial camera sees it plainly, so it must be built properly.

**Northeast / southwest flanks** — Party walls, hard against 358 and 370 Brannan, not
visible from any public vantage and not photographable. Build them as plain cream stucco
with no openings; do not invent windows.

**Top** — Predominantly flat, light-gray membrane over the one-storey block, with the
**low-pitched ribbed metal roof** over the front bay sloping up away from Brannan (this is
what puts the crest 1.5 m above the street parapet). The satellite shows rows of small
dark roof monitors/skylights running parallel to the Brannan edge, two or three larger
gridded skylight panels, and scattered mechanical units. This is the surface the app's
camera sees most — design it, do not leave it flat.

### 2.5 Recognition cues (ranked)

1. **Cream stucco with dark bottle-green joinery** — the band frame, the diamonds, the
   water table, the freight doors. One colour pair carries the whole building.
2. The **steel-sash factory window band** on the raised front bay.
3. The **two green frieze diamonds** above it — the only ornament on the building, and
   the thing that makes it not-generic.
4. The **two-height massing** with the step partway along the frontage, and the ribbed
   roof sloping up behind the front parapet.
5. The green water-table stripe with slot windows above it on the long low wall.

### 2.6 Miniature translation

**Preserve**

- The two-height massing and its real 45° heading — this is the silhouette
- The green-on-cream colour discipline; no third colour anywhere
- The window band as a single continuous horizontal event, not a row of separate windows
- The two frieze diamonds, at readable size
- The water-table stripe running unbroken across the low wall
- Three roll-up doors on the Varney back

**Simplify / exaggerate**

- The ~6 x 5 lights per window unit become a 4 x 3 grid per unit — anything finer is
  sub-pixel from the app's camera
- The frieze diamonds are enlarged to ~0.9 m across so they survive at thumbnail size;
  this is the one place semantic exaggeration is spent
- The water-table stripe is thickened to ~0.6 m
- The slot windows become four identical recessed dark rectangles
- Stucco texture, ghost sign, downpipes, conduit and signage all disappear
- The ribbed metal roof becomes one clean sloped plane, no ribs — the slope is the cue
- Roof clutter becomes two rows of three low skylight boxes, one gridded skylight panel,
  and one HVAC cluster of two blocks

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render.

1. Low block: extrude the 2.3 footprint from z=0 to z=5.6, `Toy_cream`. This is the whole
   lot; the front bay is added on top of its southwest-front corner.
2. Low-block parapet: z=5.6 to z=5.95, following the footprint, 0.3 m thick, `Toy_cream`
   with a `Toy_sand` cap so the ring reads from above.
3. Front bay: a box on the southwest end of the Brannan edge, ~12 m along the frontage x
   ~8 m deep, from z=0 to z=7.1, `Toy_cream`. Its Brannan face is flush with the low
   block's; its two inboard faces are exposed cream wall.
4. Bay roof: a single plane sloping from the front parapet at z=7.1 up to the ridge at
   **z=8.6** at the back of the bay, `Toy_steel` — this sets the bounding-box top and must
   land exactly on 8.6.
5. Window band on the bay's SE face: sill z=4.2, head z=6.0, inset 0.15 m. Three units
   separated by 0.25 m green mullions, each glazed `Toy_glass` behind a `Toy_verdigris`
   frame; a 4 x 3 light grid per unit as thin `Toy_trim` glazing bars.
6. Frieze: plain cream from z=6.2 to z=7.0 on the bay's SE face, carrying two
   `Toy_verdigris` diamonds ~0.9 m across, centred at z=6.6, at the third points of the
   bay width, proud 0.06 m.
7. Water table: `Toy_verdigris` band z=1.2 to z=1.8 across the whole SE frontage
   (including under the bay) and returning 0.5 m onto neither flank — it is a street-front
   feature only.
8. Slot windows: four openings 1.4 x 0.5 m at z=3.4 on the low block's SE face, recessed
   0.15 m, `Toy_ink`.
9. Entrance: a 1.9 m wide x 2.9 m tall recessed storefront at the step, `Toy_glass` with a
   `Toy_trim` frame and a small `Toy_trim` sign panel above at z=3.0.
10. Varney back: three roll-up doors 3.2 x 3.8 m, evenly spaced, recessed 0.12 m — two
    `Toy_verdigris`, one `Toy_steel` — plus a `Toy_verdigris` panel 2.0 x 3.8 m at the
    southwest end.
11. Roof deck at z=5.6, `Toy_roofd`. Two rows of three skylight boxes 2.2 x 1.2 x 0.3 m
    parallel to the Brannan edge, `Toy_glassl`; one gridded skylight panel 3.4 x 2.4 m;
    two HVAC blocks (2.0 x 1.4 x 0.9 m and 1.4 x 1.0 x 0.7 m) `Toy_steel`.
12. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | all stucco walls, front and back and flanks |
| `Toy_sand` | `#ece4d4` | parapet caps, entrance reveal |
| `Toy_verdigris` | `#9fb8a8` | **the signature green**: window frame and mullions, frieze diamonds, water table, two roll-up doors |
| `Toy_glass` | `#2a4d73` | the window band glazing, entrance glazing |
| `Toy_glassl` | `#6f95b8` | skylights (lighter, reads as up-facing glazing) |
| `Toy_trim` | `#f3efe6` | glazing bars, entrance frame, sign panel |
| `Toy_steel` | `#9aa0a6` | the sloped bay roof, HVAC blocks, the gray roll-up door |
| `Toy_roofd` | `#45454a` | flat roof deck |
| `Toy_ink` | `#3a3530` | slot windows, door recesses |
| `Toy_glass_Glow` | `#2a4d73` | a few lit lights in the window band at night |
| `Toy_trim_Glow` | `#f3efe6` | the entrance sign panel at night |

Note on the green: the real colour is a dark bottle green, considerably darker and more
saturated than the palette's `Toy_verdigris` (`#9fb8a8`), which is a pale sage. Off-palette
is a WARN not a FAIL, so a dedicated `Toy_bottle` at roughly `#2f4f3f` is permissible and is
probably the right call — the green-on-cream contrast IS the building. Decide from the
aerial render and record the decision in `REPORT.md`.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a primary surface
must never be authored as glow. Hero glow: four or five lit lights scattered in the window
band, not the whole band — this is a working shop, not an office floor. Supporting accent:
the entrance sign panel. The frieze diamonds and the water table do **not** glow; they are
daylight identity features and lighting them would misread as signage.

### 2.9 Top surface

A mostly flat roof 5.6 m up with a sloped metal plane rising to 8.6 m at the Brannan end,
in a district the camera flies over constantly. Two rows of three skylight boxes parallel
to the Brannan edge, one larger gridded skylight, an HVAC pair grouped off-centre toward
Varney, and a continuous parapet ring so the deck never reads as an open tray. Keep the
deck value clearly darker than the parapet cap so the ring reads from above, and keep the
sloped bay roof lighter than the deck so the two-height story is legible from straight
down — from directly overhead the slope is the only thing that says "the front is taller".

### 2.10 Scope

**In the GLB:** the single 1925 industrial block — two-storey front bay, one-storey body,
all four elevations' openings, sloped bay roof, flat roof deck and roof furniture

**Not in the GLB:** Brannan Street, Varney Place, the party-wall neighbours at 358 and 370
Brannan, street trees, sidewalk, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 8,000 — this is a secondary building and a simpler one than `380-brannan` (which
shipped at 7,760 against a 9,000 cap), so the cap should bind. Suggested split: massing,
parapets and bay roof ~2k; window band and its glazing bars ~2.5k; ground-floor openings,
entrance and water table ~1.5k; Varney doors ~0.7k; roof furniture ~1.3k.

### 2.12 Draft manifest entry

```json
{
  "id": "362-brannan",
  "file": "362-brannan.glb",
  "anchor": [
    -122.3937450,
    37.7808430
  ],
  "targetHeightM": 8.6,
  "cat": 19,
  "name": "362 Brannan Street",
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

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '362Brannan'` — the
  registry uses camelCase ids while the manifest uses kebab-case) and re-bake the affected
  tiles, or the baked procedural building on this exact footprint will intersect the GLB.
- **Exclusion radius: 8 m.** Measured from the DataSF footprints: this building's own
  centroid sits 3.53 m from the anchor, and the nearest **neighbour** centroid is
  SF3775017 at 12.95 m (then SF3775020 at 14.76 m). The safe band is therefore
  `3.6 < r < 12.9`; 8 m is the middle of it. Do not raise it past 12 — this is a mid-block
  site with party walls on both flanks and a generous radius eats the neighbours, exactly
  as documented for `380Brannan` four doors away. Re-run the audit 1.6 check to confirm
  exactly one building is dropped.
- `camera`: required, not optional — `context.mjs` bakes it straight into
  `context/landmarks.json` and `camera.js` reads `preset.yaw` unconditionally, so omitting
  it makes the whole city fail to boot. Mirror the neighbour:
  `{ distance: 200, yaw: 45, pitch: 24 }` (same street, same heading, a slightly smaller
  building than 380 Brannan's 220).
- `loadRadius`: the skill's default formula gives `max(2500, 8.6 * 30) = 2500` m. Take the
  default. Beyond that radius the carved-out site is a gap, but at 2.5 km an 8.6 m building
  is far below a pixel and the absence is illegible.
- **Batch mode applies.** This landmark is being built alongside others; stage 5 runs the
  bake and the full QA on it, then throws the bake away
  (`git checkout -- app/public/tiles api/_data`) and commits source only. See
  "Batch mode" in `docs/asset-pipeline/ADDRESS-TO-ASSET.md` and
  `docs/asset-pipeline/BATCH-INTEGRATE.md`.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 8.6 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~32 x 32 m is expected)
- [ ] The two-height step is present and reads from the aerial camera
- [ ] Triangles at or under 8,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on a few window lights and the sign panel; glow shells proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **OSM `height=6` is the low block, not the building.** The tag is `source=Bing` and lands
  between the LiDAR majority (4.90 m) and median (5.63 m) — i.e. it describes the
  one-storey part that covers most of the plan and misses the front bay entirely. Building
  to 6 m would produce a flat box and lose the whole silhouette. This is the trap the plans
  README warns about, in its most seductive form: the tag is not absurd, it is just the
  wrong feature.
- **The crest and the street parapet are different numbers, and both matter.** DataSF's
  `hgt_maxcm` of 8.58 m is the ridge of the bay's sloped roof, set back from the street. A
  photogrammetric estimate from the Brannan pano, scaled off a sidewalk waste bin and a
  parking sign, puts the *front* parapet at ~7.0–7.1 m. Scaling the same photo off the
  entrance storefront instead gives anywhere from 5.4 m (if it is a bare 2.15 m door) to
  7.4 m (if it is a 2.9 m storefront with transom) — which is why the storefront was not
  used as the datum. Target height is the crest, 8.6 m; the ~7.1 m eave is *inferred* and
  should be re-derived.
- **"2 storeys" is true of about a fifth of the floor plate.** The assessor and the 2014
  permit both say 2, and the front bay is genuinely two storeys — but the LiDAR
  distribution (majority 4.90 m, std 0.96 m) says most of the building is one tall
  industrial storey. A modeller who reads only the storey count builds a uniform two-storey
  box and gets the silhouette wrong.
- **Google's address point for "362 Brannan St" is on Varney Place**, at the back of the
  lot. The first Street View pano it opens looks at a dusty-rose corrugated gate that
  belongs to the property *across* the alley, not to this building. Two panos are named in
  2.2 for exactly this reason; use `QGmjHr1j26kBQJg4CIIlyQ` for the front.
- **The extent of the two-storey bay is the weakest number in this dossier** (2.3). Both
  its frontage share (~12 m of 20.1) and its depth (~8 m of 24.8) are derived from LiDAR
  area statistics plus oblique photography, not measured. Confirm from aerial imagery
  before committing to the massing.
- The window band's unit count and light grid (~3 units, ~6 x 5 lights) are *inferred* from
  photography at an angle, as is the count of ground-floor slot windows (3–4 visible).
- Whether the two frieze diamonds are the only ones, or whether the series continues across
  the blank upper wall northeast of the band, is unresolved — the trees obscure it.
- No architect and no historical record were found for the 1925 building. If the executing
  agent finds one (SF Planning's historic resource surveys are the likeliest source), add
  it to `REFERENCE.md`.
