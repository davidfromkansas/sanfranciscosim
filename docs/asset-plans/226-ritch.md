# 226 Ritch Street — SF-SIM asset plan

A 1994-96 live/work loft building on the south-west side of Ritch Street, the
one-block alley between Bryant and Brannan in SoMa. Eight lofts with 15-foot
ceilings and mezzanines stacked three levels over a ground-floor garage, on a
12 m x 20 m infill lot. What makes it findable is not its size — it is smaller
than everything around it — but its **colour and its ironmongery**: a sage-green
stucco block with a sand-tiled base, a red roll-up garage door, big white
multi-lite loft windows on its north-west half, and a galvanised fire-escape
stair zig-zagging across its south-east half up to a roof deck. It is the only
green building on an alley of grey concrete warehouses and beige loft blocks.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/226-ritch/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `226-ritch` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3960899, 37.7804376` (DataSF footprint SF3776120 oriented-bounding-box centre, measured) |
| Target height | **18.1 m** to the roof crest (stair bulkhead over the roof deck); main street parapet **16.0 m** — see 2.1 and the height gate in Part 1 |
| Footprint | 12.13 m frontage (NW–SE, on Ritch) x 22.80 m deep (NE–SW); 251 m2 gross, measured — a rectangle at bearing 45.6°/135.6° with a notched rear |
| Triangle cap | 9,000 |
| Category | `2` (apartments — live/work lofts) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 226 Ritch Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 226 Ritch Street in San Francisco and deliver
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
7. `artifacts/188-south-park/` — the closest reference implementation in scale,
   programme and neighbourhood: a live/work loft block of almost exactly the same
   height (15.93 m against this one's 16.0 m parapet) with a flat roof and a roof
   terrace. Take its detail budget, its facade discipline and its roof treatment.
   Note the differences: 188 is a wide 2002 stucco-and-stone building presenting a
   23.7 m face to an open park; this is a narrow 1990s building presenting a 12.1 m
   face to a 12 m alley, with an external fire escape and a garage door
8. `artifacts/181-south-park/` — for how a small SoMa live/work block's window
   rhythm was resolved at this triangle budget
9. `docs/asset-plans/226-ritch.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## The height gate — settle this before you model anything

The one number that scales the whole asset is unresolved to ±1.1 m and you must
close it first. Three independent sources agree on the **main street parapet at
16.0 m**: OSM way 148217483 carries `height=16`; DataSF LiDAR footprint SF3776120
gives `hgt_median` 15.90 m and `hgt_mean` 15.99 m over 1,018 cells; and a rectified
Street View elevation (method and numbers in 2.1) puts it at 15.2-16.0 m. Treat
16.0 m as settled.

What is *not* settled is the **crest**. The same LiDAR footprint has `hgt_max`
18.14 m and `hgt_majority` 17.63 m, i.e. something solid stands about 2 m above
the roof plane. The dossier argues (2.1, 2.9) that this is a stair bulkhead
serving the roof deck — the deck is documented by permit 200605040680 ("remove
stucco around perimeter of deck (10x12)") and by the penthouse unit's four
private balconies, the fire escape visibly runs to roof level, and the HOA fee
includes an elevator. That reasoning is sound but it is *inference from an
aerial and a permit record*, not an observation.

So:

1. Confirm from aerial imagery whether a solid rooftop enclosure exists, where it
   sits on the roof, and roughly how big it is.
2. **If it exists:** author the main parapet at exactly 16.0 m, the bulkhead crest
   at 18.1 m, and set `targetHeightM` to 18.1.
3. **If it does not exist:** the crest is the roof-deck railing. Author the parapet
   at 16.0 m, the railing at ~17.0 m, and set `targetHeightM` to the model's actual
   crest. Do not keep 18.1 out of deference to this plan.

Either way the parapet lands at 16.0 m in world space. Record which branch you took,
with the imagery you took it from, in `REFERENCE.md` and `REPORT.md`.

## Photo research is a hard gate on the flanks and the roof

The street (north-east) elevation in 2.4 is **observed and metric** — it was
rectified off a Google Street View panorama to a 60 px/m elevation and the bay
positions in 2.7 are measured, not eyeballed. Trust it and reproduce it.

The other three faces are weak and must be improved before you model them:

1. **The rear (south-west) and north-west faces** are known only from two 1998
   permits — vinyl siding to the "rear & north sides" and to the "left side of
   house not visible". No photography of either could be consulted. The rear
   faces the interior of the block; it may not be reachable at all, in which case
   say so and treat it as a service face per 2.4.
2. **The south-east flank**, where a 1997 permit filled in two mezzanine windows.
   Establish whether there is a light gap to 230 Ritch or a party wall.
3. **The roof.** 2.9's inventory — skylight domes, tiled deck, mechanical units,
   bulkhead — came off Google satellite imagery whose registration against the
   survey footprints is off by roughly 3 m, so *which* of the observed roof
   objects belong to this building rather than to 218 Ritch next door is not
   certain. The camera looks down; this is the face that most needs improving.
4. **Night appearance.** No night imagery was consulted at all.

Record what you found and how in `REFERENCE.md` and `REPORT.md`.

## Must capture

- The **proportion**: a narrow 12.1 m frontage on a 22.8 m deep lot — a slot
  building, deeper than it is wide, standing shoulder to shoulder with its
  neighbours on both party walls
- **The green.** This is the single strongest recognition cue on the alley: a
  muted sage/olive stucco body against a street of grey concrete and beige brick
- The **sand-tiled ground band** to about 2.35 m, with the **red roll-up garage
  door** in it — the second cue, and the only saturated accent
- Three loft levels of roughly 4.5 m floor-to-floor — the "15-foot ceilings" the
  listings sell, which is why a three-storey building is 16 m tall
- The **split facade**: big white-framed multi-lite loft window grids on the
  north-west half, recessed loggias with dark steel railings on the south-east
  half
- The **fire escape** — a galvanised zig-zag stair on the south-east half running
  from level 1 to the roof. It is the busiest thing on the building and it is
  what makes the elevation read as a 1990s SoMa live/work block
- A deliberately designed roof: parapet, deck with railing, skylight domes, and
  the bulkhead if confirmed

## Research 226 Ritch Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- All four elevations. Only ONE of them is a designed face: the 12.1 m north-east
  front onto Ritch. The 22.8 m flanks are party/side walls and the south-west rear
  faces the block interior
- Aerial and roof views at higher resolution and better registration than 2.9
  could reach
- Ground-level views along Ritch from both directions, which settle the parapet
  line against the neighbours
- Day and night appearance
- The exact colour of the green — 2.8's values are sampled from a single
  part-shaded panorama and are the weakest numbers in the palette

Prefer architect/engineer publications, owner or institutional material, planning
and permitting documents, architectural press, geolocated photography, and
aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**Two source conflicts are already known — re-check them, do not silently
re-inherit either value:**

1. **Unit and storey count.** The 1994 new-construction permit says "three story
   nine unit live/work structure"; a 1996 permit eliminated one dwelling unit; the
   DataSF address file lists eight units (101-103, 201-203, 301-302); MLS listings
   say variously "STORIES 3" and "STORIES 4". Three structural storeys with
   mezzanines inside each unit reconciles all of it, and is what the measured
   elevation shows. Confirm rather than assume.
2. **Depth.** OSM's ring is a clean 20.18 m x 12.10 m rectangle; DataSF's 21-vertex
   ring is 22.80 m x 12.13 m with a notched rear. DataSF is the survey and is what
   the bake consumes, so 2.3 uses it — but the rear notches are exactly the part no
   photograph confirms.

**One trap to avoid.** Searching "Ritch Street lofts architect" surfaces Santos
Prescott's *Ritch/Zoe Studio* (1998, 15,000 sq ft, frontage on both Ritch and Zoe,
courtyard carved from a concrete warehouse). **That is a different building.** This
one is a 1994 wood-frame new build on a 3,146 sq ft lot with no Zoe Street
frontage. No architect could be attributed to 226 Ritch; if you find one, that is
new information and belongs in `REFERENCE.md`.

## Create a reference dossier

Write `artifacts/226-ritch/REFERENCE.md` containing: source links and what each
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

This is a **background/secondary building** in the style bible's detail budget
(§21), not a hero landmark: one clear volume, one strong facade rhythm, a simple
designed roof, and exactly two identity cues carried hard — the green body with
its red garage door, and the fire escape. Resist adding hero-tier ornament, and in
particular resist modelling the multi-lite window grids pane by pane; they are a
*texture* at this scale and must be spent as a few chunky mullions, not as
geometry.

The finished asset must be immediately recognizable as 226 Ritch Street, consistent
with the real building from all four sides and above, architecturally credible, and
a premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1994-96 loft block: body, all four elevations' openings, the
ground-floor garage and entry, the flat roof with its deck, railing, skylights and
bulkhead, and the fire escape.

Do not include unrelated surrounding city geometry: Ritch Street, 218 or 230 Ritch
next door, the sidewalk, the utility poles and overhead wiring in front of the
building (they are the most visually prominent things in every photograph of it and
they are NOT part of the asset), parked cars, people, plinths, cameras or lights.
Temporary context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 9,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The Ritch Street
entrance faces **north-east, bearing 45.6°**; the building's long axis runs
45.6°/225.6° (NE-SW), so build directly on the measured footprint rectangle in 2.3
rather than modelling an axis-aligned box and rotating it. The contract's "front
faces −Y" cannot be honoured literally here; real-world orientation wins
(AGENTS rule 5) and the deviation goes in `REPORT.md`.

**Height normalization:** the main street parapet must land at exactly **16.0 m**,
and the tallest geometry in the export must land at exactly the `targetHeightM` you
put in the manifest draft, so the loader's `targetHeightM / measuredHeight` scale is
1.0. See the height gate above.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/226-ritch/build_226_ritch.py` (deterministic build script),
`artifacts/226-ritch/226-ritch.blend`, and `artifacts/226-ritch/226-ritch.glb`. The
script must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`226-ritch-top.png`, `226-ritch-north.png`, `226-ritch-east.png`,
`226-ritch-south.png`, `226-ritch-west.png`, plus `226-ritch-contact-sheet.png`,
at least one high three-quarter aerial beauty render `226-ritch-aerial.png`, and a
night render `226-ritch-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection;
use orthographic or long-lens cameras; label directions from the researched
orientation; the top view must clearly show the full 12.1 x 22.8 m roof — its deck,
railing, skylights and bulkhead; the aerial view uses the style bible's camera
assumptions (30-50 degrees down, long lens). Simple tabletop lighting, neutral warm
background, minimal depth of field, and every image must depict the same exported
model.

Because the building is rotated ~45° from the world axes, the four compass renders
will each show two faces at 45°. That is correct and expected — do not rotate the
model to make the elevations square on.

## Validate the exported GLB

Re-import `226-ritch.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Render at least one review image from the re-imported asset. Write
`artifacts/226-ritch/validation.json` and `artifacts/226-ritch/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **25 x 25 m** even though
the building is 12.1 x 22.8 m — that is the expected consequence of a ~45°
real-world heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "226-ritch",
  "file": "226-ritch.glb",
  "anchor": [
    -122.3960899,
    37.7804376
  ],
  "targetHeightM": 18.1,
  "cat": 2,
  "name": "226 Ritch Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/226-ritch.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
documentary inference, not measurement; values marked *measured* were computed here from
the named dataset and the arithmetic is shown.

### 2.1 Verified facts

| Fact | Value | Confidence / source |
|---|---|---|
| Address | 226 Ritch Street, San Francisco, CA 94107 | verified (DataSF EAS, OSM) |
| Name | 226 Ritch Street Condominiums | verified (Trulia building record) |
| Neighbourhood | South of Market / South Beach; DataSF `nhood` = South of Market | verified |
| OSM | way `148217483`, `building=yes`, `addr:housenumber=226`, `height=16` | verified |
| DataSF footprint | `SF3776120` / `sf16_bldgid` 201006.0016315 | verified |
| Assessor block | 3776; condo lots 3776120-3776127 (eight) | verified (DataSF EAS) |
| Lot area | 3,146 sq ft = 292 m2 | verified (MLS 422635708, 422696775) |
| Built | permit filed 1994, completed 1996; assessor/MLS year built **1996** | verified (SF DBI permits; MLS) |
| Original permit | `9420930s`, "Erect a three story nine unit live/work structure", new construction wood frame, $400,000, completed 21 Dec 1994 | verified (SF DBI) |
| Structural revision | `9516754` (1995): "Rev pa #9420930. Chng from type II to V/1hr. Bldg ht reduced." | verified (SF DBI) |
| Unit count | 9 permitted, one eliminated in 1996 (`9600830`); **8 today** (101-103, 201-203, 301-302) | verified (SF DBI; DataSF EAS; MLS "only 8 units in the building") |
| Storeys | **3** structural, each loft with an internal mezzanine | verified (permit; MLS "STORIES 3"; measured elevation) |
| Ceiling height | 15 ft (4.57 m) in the lofts | verified (multiple MLS/rental listings) |
| Floor-to-floor | ~4.5 m *measured* from the rectified elevation (2.4) | measured |
| Use | artist live/work, now condominium apartments; ground-floor garage, laundry in garage | verified (permit "current use" progression; MLS) |
| Architect | **not established** | — (see the trap note in Part 1) |
| Main parapet | **16.0 m** | verified three ways: OSM `height=16`; DataSF LiDAR `hgt_median` 15.90 m / `hgt_mean` 15.99 m; rectified Street View elevation 15.2-16.0 m |
| Roof crest | **18.1 m** *inferred* — stair bulkhead over the roof deck | DataSF LiDAR `hgt_max` 18.14 m, `hgt_majority` 17.63 m; corroborated by the roof deck permit and the fire escape reaching roof level. **Unconfirmed by imagery** — see the height gate |
| Ground band | sand-coloured large-format tile, 0 to **2.35 m** | measured (rectified elevation) |
| Footprint (DataSF) | 22.80 m x 12.13 m OBB, 251.5 m2, long axis bearing 45.6°/225.6° | measured |
| Footprint (OSM) | 20.18 m x 12.10 m OBB, 244.1 m2, same bearing | measured |
| Anchor | `-122.3960899, 37.7804376` (DataSF OBB centre) | measured |
| Front face normal | bearing **45.6°** (north-east, onto Ritch Street) | measured from DataSF centreline and the footprint winding |
| Ground elevation | 5.59 m NAVD88 (`gnd_median`), range 5.27-5.72 m — flat | verified (DataSF) |

**How the parapet was measured photogrammetrically.** Google Street View pano
`ghoSOzaNSJJK1wpjaYBtwA` (titled "226 Ritch St") was pulled as a levelled 4096x2048
equirectangular. The yaw offset was calibrated against the two front-corner bearings
computed from the footprint (179.8° and 265.1° from the reported camera position);
both corners fitted the *same* offset of 49.8° ± 0.2°, which corroborates the
panorama's reported position rather than condemning it — a spread of several degrees
would have meant the position was wrong (see the standing warning in the project
memory on Street View photogrammetry). The perpendicular distance from the lens to the
facade plane is then 6.5-6.7 m and the parapet subtends 64.3° of elevation at the
perpendicular foot, giving 15.5-16.0 m above the sidewalk depending on the assumed
camera height (2.0-2.05 m above the pavement at the wall). The facade was then
resampled into a metric 60 px/m rectified elevation, from which all the dimensions in
2.4 and 2.7 are read.

**Why `hgt_max` is quoted here and refused elsewhere.** The project's standing rule is
that a LiDAR maximum is not a landmark height (a street tree over a parapet has faked
one before). It is quoted here because the distribution supports it: `hgt_mean` 15.99
and `hgt_median` 15.90 are within 0.1 m of each other, so the roof plane is
unambiguously ~15.9 m and symmetric; `hgt_std` is 1.71 m over 1,018 cells, far too
large for a flat roof alone; and `hgt_majority` 17.63 m puts a *repeated* value 1.7 m
above the plane, which a single spurious return cannot do. There is no street tree
within the footprint — the nearest are on the opposite kerb. That is a rooftop
structure, not an outlier. It is still labelled *inferred* because nothing has been
seen.

### 2.2 Sources

| Source | Establishes |
|---|---|
| OSM way 148217483 (Overpass API, geometry + tags) | footprint ring, address, `height=16` |
| DataSF *Building Footprints* `ynuv-fyni`, footprint `SF3776120` | 21-vertex survey ring, LiDAR height distribution, ground elevation |
| DataSF *Addresses with Units* `ramy-di5m` | the eight condo units and their parcel numbers; the neighbours at 212/218 and 230-236 Ritch |
| SF DBI permit history (via checkpermits.com and openpermitdata.com) | 1994 new construction, 1995 type/height revision, 1996 unit elimination, 1997 window fill-in, 1998 vinyl siding to rear and north, 2005 stucco/sliding-door work at unit 302, 2005 and 2024 reroofing, 2006 roof-deck rebuild |
| MLS 422635708 (unit 202), 422696775 (unit 101), 424073376 (unit 302), via jeffmarples.com and king-realtygroup.com | year built 1996, 3 storeys, 8 units, 15-ft ceilings, mezzanines, lot area, garage, penthouse with four balconies, elevator in HOA dues |
| Trulia building record; apartments.com; sanfranciscocondomarket.com | building name, loft character, unit mix |
| Google Street View panoramas `ghoSOzaNSJJK1wpjaYBtwA` (in front of the building), `3MCsiT2LemwvFtwJsgkTxA` and `cKwbxtiKXSiLVgZ5RJ_uFQ` (up and down Ritch) | the entire north-east elevation, its palette, and the street context |
| Google satellite imagery z21 over the block | roof furniture inventory (registration off by ~3 m against the survey rings — see 2.9) |
| Esri World Imagery z20 | attempted registration control; too soft at this scale to resolve roof objects |
| Santos Prescott, *Ritch / Zoe Studio* (1998) | **negative** result — a different building on the same alley; recorded so nobody re-attributes it |

Exa searches run: `226 Ritch Street San Francisco building lofts` (10 results, summaries)
and `226 Ritch Street San Francisco live/work lofts architect 1994 South Park Ritch alley`
(8 results, highlights). Productive domains: checkpermits.com, openpermitdata.com,
jeffmarples.com, trulia.com, apartments.com, santosprescott.com. Facts confirmed by them:
year built, storey count, unit count, ceiling height, permit history, facade materials.
Everything from a listing is labelled *observed (listing copy)* below — listings describe
the building as marketed, which is usually but not always its current state. No
Wikipedia, Wikidata or architectural-press entry for this building exists.

### 2.3 Orientation and placement

SoMa's grid is rotated ~45° from the compass. Bryant, Brannan and Townsend run
north-east/south-west; Ritch Street is one of the alleys cutting across them, running
**north-west to south-east**, from Bryant down to Brannan.

- **Ritch Street centreline** (OSM way 8917138, projected): passes (3625.1, −1197.8)
  → (3675.5, −1147.3) in app metres, i.e. bearing 135.1°.
- **226 Ritch sits on the SOUTH-WEST side of the alley.** Measured: the perpendicular
  from the anchor to the centreline is 17.3 m and its foot vector is (−12.3, +12.2),
  i.e. west and south of the centreline. The front wall stands ~7.3 m out from the
  centreline. *This is the number to re-derive rather than assume: an asset plan
  in this series has named the wrong face for a street before, and the fix was to
  measure the side from the centreline exactly like this.*
- **Long axis** (the 22.8 m depth) runs 45.6°/225.6°; the building extends
  south-west, away from the alley, into the block.
- **Frontage** (12.13 m) runs 135.6°/315.6° along the alley.
- **Front face outward normal: bearing 45.6°** — north-east. Derived from the ring
  winding, not from the centroid: the interior lies toward the rear corners, so
  outward is (+0.713, −0.700) in (x, z) = east and north.

Neighbours, from the same OSM/DataSF pull:

| Direction | Building | Height |
|---|---|---|
| North-west (party wall) | 218 Ritch St (OSM 148217499, DataSF SF3776144) | LiDAR median 10.75 m |
| Beyond that | 212 Ritch St (OSM 148217502) | OSM `height=7` |
| South-east | 230 / 234 / 236 Ritch St (block 3776, lots 144-147) | LiDAR median 12.49 m (SF3776093) |
| Across the alley (north-east) | 201 Ritch / 523-539 Bryant loft warehouses | OSM `height=8` to `19` |

So the building stands **3 to 5 m proud of both its immediate neighbours** and is
overtopped by the concrete loft warehouses across the alley. From the app's aerial
camera it reads as a small green step up in a low row.

Anchor choice: the DataSF oriented-bounding-box centre `-122.3960899, 37.7804376`.
The DataSF *area* centroid is 0.9 m from it and the OSM OBB centre 0.7 m — the lot is
close enough to rectangular that the choice barely matters, but the DataSF ring is
what the bake consumes, so the exclusion arithmetic in 2.13 is measured from this
point and must stay consistent with it.

### 2.4 What each side shows

**North-east — the front, onto Ritch Street (12.13 m wide). The only designed face.**
*Measured* from the rectified 60 px/m elevation; positions below are metres along the
frontage from the centre, negative = north-west.

- **0 to 2.35 m: the base.** Sand/tan large-format tile (roughly 0.6 m square,
  laid in a plain grid), running the full frontage and returning a little onto both
  flanks.
  - t −5.4 to −4.9: a solid timber door (service/bin store), dark stained.
  - t −4.6 to −3.2: the residential entry — a glazed aluminium door and sidelight
    in a shallow reveal, with a small `226` plaque above and a lantern-style wall
    sconce on each side.
  - t −0.4 to +1.6: the **red roll-up garage door**, ~2.0 m wide in the model's
    terms and 2.2 m tall, with two small vision panels near its head. Oxide/brick
    red, the only saturated colour on the building.
  - t +2 to +7: plain tiled wall with two brass hose bibs / fire-department
    connections at ~1.0 m.
- **2.35 m to 16.0 m: three loft levels in sage-green stucco**, floor-to-floor ~4.5 m.
  The facade is split lengthwise:
  - **North-west half (t −6 to −1):** recessed loggia openings with dark steel
    balcony railings, one per level, each about 2.4 m wide, plus a small awning
    window beside each. The **fire escape** — galvanised steel, a straight run of
    stair per level with a landing at each — zig-zags across this half from the
    first-floor landing (which cantilevers over the entry at ~4.0 m) up to the roof.
  - **South-east half (t +1 to +7):** the **loft windows** — large white-framed
    multi-lite assemblies, each roughly 2.6 m wide and 2.8 m tall, two per level
    side by side, divided into a grid of small panes with the mullions in the same
    white as the frames. These are what the listings sell as "expansive windows"
    with the mezzanine behind them.
  - Small round white light fittings between the openings at about 5.5, 9.5 and
    13.5 m.
  - The top level's windows are noticeably smaller — 2-over-2 white sash rather
    than the full loft grid.
- **16.0 m: the parapet**, a plain capped stucco band, no cornice.
- Above it, set back: the dark steel **roof-deck railing** across the north-west
  half, ~1.0 m tall, and (if confirmed) the bulkhead behind it.

**North-west flank (22.8 m) — party wall to 218 Ritch.** Blind for most of its
length. *Observed (permit)*: vinyl siding was installed to the "rear & north sides"
in 1998 (`9813871`, $22,000) and to the "left side of house not visible" (`9811148`,
$10,000) — so this face and the rear are **siding, not stucco**, in an off-white or
pale grey. No photography of it exists in the sources consulted. Treat as a service
face: no designed openings, a few small utility windows at most, and the base tile
returning ~1 m from the front corner. *Inferred.*

**South-east flank (22.8 m) — toward 230 Ritch.** Stucco (the 1997 permit
`9711104` fills in "2 windows on 2nd flr, mezzanine level 2 south side", which means
there were windows on this side and there are now two fewer). Otherwise blind.
*Inferred* whether a light gap survives or the buildings touch.

**South-west rear (12.13 m) — the block interior.** Vinyl siding per the 1998
permit. The DataSF ring puts three or four shallow notches in this end of the
footprint — light wells or a stepped rear wall — where OSM simply draws a straight
line. Listings mention a "covered patio" for the ground-floor units and a "terrace",
which is consistent with the rear stepping in. Not visible from any public street.
*Inferred.*

**Top.** See 2.9.

### 2.5 Recognition cues (ranked)

1. **The green.** A muted sage/olive stucco block on an alley of grey concrete
   warehouses and beige loft blocks. From the air it is the only green roof-edge on
   the street. If only one thing survives the simplification, it is this.
2. **The red garage door in the sand-tiled base.** The single saturated accent, dead
   centre of a 12 m frontage.
3. **The fire escape.** Galvanised zig-zag across half the elevation, running to roof
   level — the cue that says "1990s SoMa live/work", not "apartment block".
4. **The split facade rhythm:** big white multi-lite loft windows on one half,
   recessed railed loggias on the other. Asymmetry is the point; do not regularise it.
5. **The proportion:** narrow and deep, standing 3-5 m above its neighbours on both
   sides.

### 2.6 Miniature translation

Style bible §21 puts this in the **background/secondary** tier: it is 16 m tall on a
251 m2 footprint in a district the camera mostly flies over. The translation therefore
spends almost everything on silhouette and colour and almost nothing on detail.

- **Keep and chunk up:** the body proportion; the base band (thicken to ~2.5 m so it
  survives at distance); the garage door (widen slightly, it is a cue); the parapet
  (give it a real 0.25-0.35 m cap so the roof edge catches light); the fire escape
  (simplify to three chunky flights and three landings, one solid rail panel each —
  no balusters); the loggia recesses (real recesses, 0.4-0.5 m deep, so they read as
  shadow rather than as paint).
- **Simplify hard:** the multi-lite window grids become one recessed glazed panel per
  opening with 2 or 3 chunky white mullions, not a pane grid. The window *frames* are
  the read at this scale; the panes are noise.
- **Exaggerate deliberately** (semantic exaggeration per the style bible, applied in
  authoring not in placement): the green a step more saturated than the sampled value,
  because a 16 m building at diorama distance loses chroma; and the base band a step
  warmer, so the red door has something to sit against.
- **Drop entirely:** the utility poles and the overhead wiring (they dominate every
  photograph and belong to the street, not the building); the wall sconces; the hose
  bibs; the vision panels in the garage door; the pane grids; the mezzanine line.
- **Night** (`_Glow`): the loft windows on the south-east half are the hero — three
  levels of warm glow behind the recessed panels, which is exactly what a live/work
  building looks like at night. Supporting: the entry sconce band at the base, and a
  cooler dim glow from the loggia openings on the north-west half. **Not** the garage
  door, **not** the skylight domes, **not** the whole roof deck. Day colours of the
  `_Glow` materials must match their non-glow neighbours (see the standing rule: a
  glow material's base colour *is* its night look, and a closed glow shell reads as
  two alpha layers by day).

### 2.7 Massing recipe

All dimensions in metres, origin at the footprint centre, `+Y` north, `+X` east,
building rotated so its long axis runs 45.6°/225.6°.

1. **Body.** Box 12.13 (frontage) x 22.80 (depth) x 16.0 (parapet), on the measured
   footprint rectangle. Bevel the vertical arrises ~0.08 m — chunky-beveled massing
   per the style bible, and it is what stops a 12 m-wide box reading as a slab.
2. **Rear notches.** Cut two shallow recesses, ~1.2 m deep x 2.5 m wide, into the
   south-west end, per the DataSF ring. *Inferred in detail; the ring says something
   is there.* If research cannot confirm them, leave the rear flat and say so.
3. **Base band.** 0 to 2.35 m, inset 0.0 (flush) but a distinct material; return
   1.0 m onto each flank from the front corner.
4. **Openings, front only.** Garage door 2.2 x 2.2 recessed 0.15. Entry 2.4 wide x
   2.6 tall recessed 0.35. Service door 0.9 x 2.1, flush.
5. **Loft windows, front south-east half.** Six openings (2 wide x 3 levels), each
   2.6 x 2.8, recessed 0.20, sills at 3.2 / 7.7 / 12.2. The top level's pair is
   1.6 x 1.4 instead — the elevation shows them smaller.
6. **Loggias, front north-west half.** Three openings, 2.4 wide x 2.4 tall, recessed
   **0.5**, at the same three levels; a solid rail panel 1.05 tall across each mouth.
7. **Fire escape.** Three straight flights and three landings on the north-west half,
   from a landing at 4.0 m to the parapet. Stringers 0.12 thick, treads as one ramped
   slab per flight, rails as solid 0.9 m panels. Keep it to a few hundred triangles;
   this is where a budget gets eaten.
8. **Parapet.** 0.25 x 0.35 cap all round at 16.0.
9. **Roof.** See 2.9.
10. **Ground.** The site is flat (LiDAR ground range 0.45 m across the footprint), so
    the base sits on a plane at Z 0 with no plinth and no drape allowance.

### 2.8 Materials and palette

Sampled from the rectified elevation; these are **part-shaded panorama pixels, the
weakest numbers in this dossier**, and are given as a starting point for the project
palette match, not as authority. Every material must resolve to a `Toy_*` name from
the project palette per the asset contract.

| Surface | Sampled | Toy palette intent |
|---|---|---|
| Body stucco | `#79836E` shaded, `#8A9A7E` estimated in neutral light | a muted sage/olive green, one step more saturated than sampled |
| Base tile | `#A88664` | warm sand/tan, matt |
| Garage door | `#933730` | oxide/brick red — the accent |
| Window frames & mullions | near-white | the project's warm off-white, not pure white |
| Glazing | — | the project's dark blue-grey graphical window colour (style bible); `_Glow` variant for the six loft windows |
| Loggia rails, roof rail | dark, near-black steel | the project's dark steel/iron |
| Fire escape | galvanised, pale grey | a lighter neutral steel, distinct from the rails so it reads as a separate object |
| Rear & NW flank siding | not sampled | pale grey-white, flatter than the stucco |
| Roof membrane | dark grey (aerial) | the project's dark roof grey |
| Roof deck | terracotta (aerial) | a warm tile note — the roof's one accent |
| Entry door | `#502B1B` | dark stained timber |

Do **not** use image textures or transparency; the tile grid, the pane grid and the
siding are all colour-and-geometry problems, not texture problems.

### 2.9 Top surface

The camera looks down, so this is a facade. What the z21 satellite imagery over the
block shows, **with the caveat that its registration against the survey footprints is
off by roughly 3 m so some of these objects may belong to 218 Ritch**:

- A flat dark membrane roof, drained to the rear.
- A **row of five or six round white skylight domes**, ~0.9 m across, running down the
  spine of the roof. These are the most characterful thing up there and they are
  consistent with a deep loft plan that needs top light.
- A **tiled deck** at the south-east end, roughly 3.5 x 6 m, terracotta/pink, with a
  railing around it. Corroborated by permit 200605040680: "Remove stucco around
  perimeter of deck (10x12) approx 12 up. Remove tile deck & mortar." — a 10 x 12 ft
  tiled deck, which is 3.0 x 3.7 m.
- Two small **raised boxes**, one near the north-west party wall casting a clear
  shadow, one carrying a white mechanical unit. One of these is the candidate stair
  bulkhead of the height gate.
- The **roof-deck railing** returning along the front parapet on the north-west half,
  visible in the Street View elevation.

Design it as a composed surface: membrane, a lighter deck rectangle, the skylight
row as a deliberate rhythm, one bulkhead, one mechanical box, and the railing. Do not
scatter vents.

### 2.10 Scope

In: the single loft block, all four faces, the roof and its furniture, the fire
escape.

Out: Ritch Street, both neighbours, the sidewalk, the utility poles and overhead
wiring, street trees, vehicles, people, plinths, cameras, lights.

### 2.11 Triangle budget

Cap **9,000**, and expect to come in well under it — comparable buildings in this
series shipped at 3,352 (592 Third) to 4,200 (181 South Park) triangles.

| Element | Budget |
|---|---|
| Body + bevels + rear notches | 400 |
| Base band + returns | 200 |
| Front openings (garage, entry, service) | 350 |
| Loft windows (6, recessed + mullions) | 1,200 |
| Loggias (3, recessed + rail panels) | 900 |
| Fire escape (3 flights, 3 landings, rails) | 1,500 |
| Parapet cap | 250 |
| Roof: deck, railing, skylights, bulkhead, mechanical | 1,500 |
| Slack | 2,700 |

The fire escape is the one element that can run away. If it does, cut its rails to
solid panels before you cut anything on the roof — the roof is a facade here and the
fire escape is not visible from the aerial camera at all.

### 2.12 Draft manifest entry

```json
{
  "id": "226-ritch",
  "file": "226-ritch.glb",
  "anchor": [
    -122.3960899,
    37.7804376
  ],
  "targetHeightM": 18.1,
  "cat": 2,
  "name": "226 Ritch Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`loadRadius` 2500 is the default rule `max(2500, targetHeightM x 30)` = `max(2500, 543)`.
This is emphatically not an `alwaysLoaded` piece.

`estimated: false` — the height is measured three ways, not published-and-trusted.
Change it to `true` only if the height gate resolves against the LiDAR.

### 2.13 Integration notes (for later, not this task)

**Case B — this is a new landmark.** No `226Ritch` id exists in
`pipeline/lib/landmarks.mjs` or `app/src/landmarks.js`, so integration needs a registry
entry, an exclusion, and a tile re-bake, plus audit check 1.6.

Draft registry entry:

```js
{
  id: '226Ritch',
  name: '226 Ritch Street',
  lon: -122.3960899,
  lat: 37.7804376,
  height: 18.1,
  exclude: 5,
  camera: { distance: 180, yaw: 134, pitch: 28 },
},
```

**`exclude: 5` is measured, not guessed.** `excluded()` in `pipeline/buildings.mjs`
drops a footprint when its ring centroid **or any ring vertex** falls inside the
radius, so both metrics were computed from the anchor above against both bake inputs:

| Source | Own footprint | Nearest neighbour |
|---|---|---|
| DataSF `SF3776120` | centroid **0.85 m** (nearest own vertex 6.11 m) | 10.23 m — a vertex of `SF3776144` (218 Ritch) |
| OSM 148217483, as an Overture proxy | centroid **0.68 m** (nearest own vertex 11.08 m) | 9.75 m — the *centroid* of OSM 148217499 (218 Ritch) |

So the window that drops exactly this footprint and nothing else is
**0.9 < r < 9.75**, and it is wide — unusually so for a party-wall row, because 218
Ritch is a small 144 m2 building whose centroid is the binding constraint rather than
a shared party-wall vertex. `5` sits in the middle with ~4.1 m of margin below and
~4.75 m above. The exclusion fires on this footprint's **centroid**, not its vertices
(the nearest own vertex is 6.1 m out), so do not shrink r below 1 expecting the
vertices to catch it.

Two things to redo at integration time rather than inherit:

1. The Overture figures above are an **OSM proxy**. Re-measure against the real
   Overture rings the bake consumes before committing the radius, and re-run the drop
   simulation over both sources — it must remove exactly one footprint per source.
   Note that the pipeline's Overture download step has failed before on a 404 from the
   CLI's STAC catalog; stub it rather than skip it.
2. `verify-rebake` compares per-cell footprint **counts** and can report "dropped
   nothing" for a working exclusion. Settle it from the decoded tile, not the count.

`camera.yaw` 134: the app's yaw is `180 − true bearing`, and the front faces 45.6°, so
`180 − 45.6 = 134.4`. That stands the camera north-east of the building, out over the
alley, looking back at the one designed elevation. 180 m and pitch 28 are in line with
comparable 16-18 m buildings in the registry (188 South Park: 190 / 26; 599 Third:
18.3 m). **Render it before believing it** — a yaw has been wrong in this registry
before and pointed the camera at a blank party wall.

Fallback drill: with the GLB removed the app must fall back to the procedural block
with one console warning. Note that with the exclusion committed the procedural
footprint is *gone*, so the Case B fallback is an empty lot by design, not a hole
to debug.

Streaming: `loadRadius` 2500, no `alwaysLoaded`. Watch the shared landmark
`BatchedMesh` — SoMa is the district where it has run to 99% full and silently dropped
a different landmark on each reload. Check the buffer before blaming this asset.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import validated, not the source scene
- [ ] Real-world metres; origin at base centre; min Z ~ 0
- [ ] Main parapet at exactly 16.0 m; crest at exactly the manifest `targetHeightM`
- [ ] Transforms applied; no negative scales
- [ ] Normals outward — per-object signed volume authoritative for a union of solids,
      ray test ≤ 0.15 % residual (zero for single shells)
- [ ] No textures, no transparency, no `Toy_body`
- [ ] All materials `Toy_*`; `_Glow` only on night-glow surfaces; `_Glow` day colours
      match their non-glow neighbours
- [ ] No cameras, lights, animations, armatures, constraints, foreign geometry
- [ ] ≤ 9,000 triangles
- [ ] Axis-aligned XY bbox ~25 x 25 m (expected consequence of the 45.6° heading)
- [ ] Four elevations + top + aerial + night render + contact sheet, all from the
      same exported model
- [ ] `validation.json` all-PASS and `REPORT.md` written, with every dossier
      correction called out

### 2.15 Open questions and risks

1. **The crest (highest risk).** 18.1 m is inferred from a LiDAR maximum and a permit
   for a roof deck. If there is no bulkhead the model is 6-12 % too tall after the
   loader's scale. This is the height gate in Part 1 and it must be closed first.
2. **The rear and the north-west flank.** Known only from two 1998 vinyl-siding
   permits. Nothing has been seen. The rear notches in 2.7 step 2 come from the DataSF
   ring alone.
3. **The green.** Sampled from one part-shaded panorama, in shadow from a street tree
   for much of the elevation. `#79836E` is a floor, not the colour.
4. **The roof inventory.** Registration between the satellite imagery and the survey
   rings is off ~3 m; some of the objects in 2.9 may belong to 218 Ritch.
5. **The architect is unknown.** Absence of evidence here is fairly strong — a
   $400,000 nine-unit wood-frame infill in 1994 may simply not have had a named
   designer. Do not fill the gap with Santos Prescott's Ritch/Zoe Studio.
6. **OSM vs DataSF depth** — 20.18 m against 22.80 m. DataSF is used because it is the
   survey and it is what the bake consumes, but the extra 2.6 m is exactly the notched
   rear that nothing confirms.
7. **Night appearance is entirely unresearched.** 2.6's glow design is a reasoned
   proposal from the building's programme, not an observation.
8. **Ritch Street is 12 m wide.** No public vantage exists from which this building can
   be seen straight on, so every photograph of it is a steep oblique and every
   horizontal dimension in 2.4 comes from the rectification rather than from a
   photograph you can check by eye.
