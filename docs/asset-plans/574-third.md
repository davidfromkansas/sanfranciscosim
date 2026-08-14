# 574 Third Street (566–586 Third Street) — SF-SIM asset plan

The largest ordinary building on its block face: a 1907 three-storey apartment block
that runs the full depth from Third Street through to Ritch Street, 1,906 m2 of
footprint carrying 104 units. Today it is the "Central Apartments". Its identity is
not ornament — it is *bulk plus rhythm*: a long chocolate-painted brick wall on Third
with a strict grid of tall narrow white-framed windows and fire escapes, shopfronts at
the base, a bare buff-brick end wall carrying a rooftop billboard at the northwest end,
an unpainted buff-brick rear on the Ritch Street alley, and a flat roof cut by two deep
light wells.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/574-third/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `574-third` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3950551, 37.7801937` |
| Target height | **15.4 m** to the rooftop billboard crest; parapet 11.9 m; roof deck 11.05 m (LiDAR median) |
| Footprint | 33.95 m (Third Street frontage, NE) x ~45 m deep to Ritch Street; 1,906 m2, measured |
| Triangle cap | 12,000 |
| Category | `2` (apartments) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 574 Third Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 574 Third Street — the 1907 apartment block
addressed 566–586 Third Street, "Central Apartments" — in San Francisco and deliver it
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
7. `artifacts/380-brannan/` — the closest reference implementation for a SoMa masonry
   block at a 45° heading with a designed flat roof and a restrained night state; its
   `build_380_brannan.py` is the script skeleton to adapt. `artifacts/550-third/` is
   the closest reference for a large through-block volume on this same street.
8. `docs/asset-plans/574-third.md` — this plan, whose dossier is your research starting
   point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules.

## Must capture

- A long **three-storey** block, flat-roofed, running the whole depth from Third Street
  to the Ritch Street alley — the biggest single mass on the block face
- The **strict grid of tall narrow windows** with pale frames on the Third Street
  elevation: this rhythm, repeated across ~11 bays and 2 upper floors, *is* the building
- **Painted front, bare brick elsewhere**: chocolate-brown painted masonry on Third,
  unpainted buff/tan brick on the Ritch Street rear and on the exposed northwest end wall
- **Fire escapes** on the Third Street elevation
- A ground floor of **shopfronts** on Third and service/garage openings on Ritch
- The **rooftop billboard** at the northwest end, standing above the bare end wall —
  the tallest thing on the building and the reason `targetHeightM` is 15.4 m
- A designed flat roof: parapet ring, **two deep light wells**, and a scatter of vents
  and skylights

## Research 574 Third Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation,
and gather references covering:

- The Third Street elevation (bay count, window proportion, fire-escape positions,
  shopfront line)
- The Ritch Street rear elevation — buff brick with segmental-arched openings and fire
  escapes in the 2019 photography cited in 2.2
- The northwest end wall and **the billboard**: confirm it is still there, whose
  structure it stands on, and its approximate size before making it the crest
- Aerial and roof views (the two light wells, vent scatter)
- Day and night appearance
- The **paint colour** of the Third Street elevation, recorded here as a dark
  chocolate brown from 2019 photography

**Two source traps are already known and resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:** Nominatim resolves "574 3rd St" onto the Third
Street **roadway** by TIGER interpolation, and no OSM building way carries the address
at all — OSM splits this single surveyed building into two comb-shaped Bing traces. The
resolution runs address → DataSF EAS → parcel 3776008 → the DataSF LiDAR footprint
`mblr = SF3776008`. And the assessor's "574 3rd St" is one of **eleven** street numbers
(566–586) on one parcel: this is one building, not a row.

## Create a reference dossier

Write `artifacts/574-third/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the 3–5 strongest recognition cues; features to preserve; features to
simplify; uncertainties and conflicting evidence. Do not commit copyrighted
full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade into
broad rhythms, deliberately design every surface visible from above, evaluate from the
app's high three-quarter aerial camera, then simplify again.

This is a **secondary building** in the style bible's detail budget (§21), but a large
one: its scale is the reason it is worth authoring at all. Spend the detail on the
window grid and the roof, not on ornament — the real building has almost none.

The finished asset must be immediately recognizable as this block, consistent with the
real building from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and
never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single apartment block: body, parapet, all four elevations' openings, fire
escapes, the roof deck with its light wells and furniture, and the rooftop billboard.

Do not include unrelated surrounding city geometry: Third Street, Ritch Street, the
neighbouring 400 Brannan corner block or 560 Third, street trees, the sidewalk, parked
cars, people, plinths, cameras or lights. **Do not put advertising artwork on the
billboard** — model it as a blank panel in a frame.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ≈ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project palette;
`_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no cameras, lights,
animations, armatures or constraints; at most 12,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The **Third Street
elevation faces northeast, bearing 44.8°**; the **Ritch Street rear faces southwest,
bearing 224.9°**; the southeast flank (toward Brannan and the 400 Brannan corner block)
faces 134.6°. Build directly on the measured footprint polygon in 2.3.

**Height normalization:** the tallest geometry in the export (the top of the billboard)
must land at exactly **15.4 m** so the loader's `targetHeightM / measuredHeight` scale
is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/574-third/build_574_third.py` (deterministic build script),
`artifacts/574-third/574-third.blend`, and `artifacts/574-third/574-third.glb`.

## Required review renders

Render the exact final geometry from controlled cameras: `574-third-top.png`,
`574-third-north.png`, `574-third-east.png`, `574-third-south.png`,
`574-third-west.png`, plus `574-third-contact-sheet.png`, at least one high
three-quarter aerial beauty render `574-third-aerial.png`, and a night render
`574-third-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; the
top view must clearly show the parapet ring, both light wells, the vent scatter and the
billboard.

## Validate the exported GLB

Re-import `574-third.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Write `artifacts/574-third/validation.json` and
`artifacts/574-third/REPORT.md`.

The axis-aligned XY bounding box will be roughly **66 x 60 m** even though the building
is 34 x 45 m — that is the expected consequence of a 45° real-world heading, not a
scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "574-third",
  "file": "574-third.glb",
  "anchor": [
    -122.3950551,
    37.7801937
  ],
  "targetHeightM": 15.4,
  "cat": 2,
  "name": "574 Third Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/574-third.md`.
````

---

## Part 2 — Research and design dossier

Compiled 13 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify anything
it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address resolution | `574 03RD ST` → parcel **3776008** (block 3776, lot 008) | DataSF EAS address layer (`ramy-di5m`) — **measured** |
| Address range on the parcel | 566, 568, 570, 572, **574**, 576, 578, 580, 582, 584, 586 Third St | EAS — eleven entrances, one building |
| Built | 1907 | SF Assessor secured roll 2025; the building's own management site says "established 1907" |
| Storeys | **3** | SF Assessor roll; unit numbers run #1xx/#2xx/#3xx; confirmed by street-level photography |
| Units | 104 | SF Assessor roll (`number_of_units`), 232 rooms |
| Use | Multi-family residential (`MRES`), rent-controlled | SF Assessor roll; listing copy |
| Building area | 58,530 sq ft (5,438 m2) | SF Assessor roll — 2.85 x the footprint, i.e. three near-full floors |
| Lot area | 21,597 sq ft (2,006 m2) | SF Assessor roll — 5% larger than the built footprint |
| Footprint | 1,906 m2; 33.95 m frontage on Third, 45.22 m rear wall on Ritch, ~45 m deep | DataSF building footprints (`ynuv-fyni`, `mblr = SF3776008`), reprojected — **measured** |
| Roof deck height | **11.05 m** above ground | DataSF LiDAR `hgt_median_m` (mode 11.03, mean 10.93, σ 1.18 over 7,629 cells) — **measured** |
| LiDAR maximum | **15.41 m** | DataSF LiDAR `hgt_maxcm` — read here as the rooftop billboard, see 2.15 |
| Parapet crest | ~11.9 m | *inferred*, deck + ~0.85 m parapet |
| Ground elevation | 5.32–7.05 m (NAVD88) | DataSF LiDAR — the app's terrain handles this, not the asset |
| Frontage headings | Third St front faces **44.8°** (NE); Ritch St rear faces **224.9°** (SW); SE flank 134.6°; NW flank 315.9° | measured from the footprint polygon |
| Current name | Central Apartments | management website; DataSF registered-business file |

### 2.2 Sources

- `https://data.sfgov.org/resource/ramy-di5m` (DataSF EAS Addresses) — address → parcel; the eleven-address range
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — the authoritative footprint polygon and the 11.05 m / 15.41 m heights
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — 1907, 3 storeys, 104 units, 58,530 sq ft
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — the 566–586 address range on lot 008
- `https://5743rdstcentralapartments.com/` — the building's own management site: "established 1907", 100+ units, historic building
- `https://augrented.com/sf/3776008-566-586-3rd-st` — independent restatement of 3 floors / 1907 / 104 units / 58,530 sq ft
- KartaView sequence 1352479 frame 35 (capture 2019-03-14), Third Street at Brannan looking northwest — the Third Street elevation: three storeys, chocolate-brown paint, tall narrow white-framed windows, ground-floor shopfronts, fire escapes, bare brick end wall, rooftop billboard
- KartaView sequences 2042946 / 2057142 (capture 2019-10/11), Ritch Street — the rear elevation: unpainted buff/tan brick, segmental-arched openings, fire escapes
- Esri World Imagery (z20 nadir, 2023 vintage) — the flat light-membrane roof, two long dark light wells, scattered small vents and skylights

### 2.3 Orientation and placement

The building occupies the middle of the block face between Brannan and Bryant on the
**southwest side of Third Street**, and runs through the block to the Ritch Street
alley. Its southeast flank abuts the 400 Brannan corner block
(`docs/asset-plans/400-brannan.md`); its northwest flank abuts 560 Third.

Measured DataSF footprint, in Blender coordinates (metres, `+X` east, `+Y` north),
already centred on the anchor `-122.3950551, 37.7801937` (the axis-aligned bounding-box
centre, which is what the loader's origin convention needs):

```
(  7.510,  29.965)   N corner  (Third St / 560 Third party line)
( 31.580,   6.025)   E corner  (Third St / 400 Brannan party line)
(  2.810, -24.915)   SE flank step
( -1.150, -29.965)   S corner  (Ritch St / 400 Brannan side)
(-33.160,   1.975)   W corner  (Ritch St / 560 Third side)
```

> **Superseded during the build — see `artifacts/574-third/REPORT.md`.** This
> five-vertex reduction hits the right area only by cancelling errors: it swings the
> northwest wall ~10° off the SoMa grid and deletes the building's real ~8.6 m step back
> from the party line near Third Street. The shipped asset uses a **seven-vertex**
> simplification (1,909.7 m2, +0.19%) in which every edge keeps its true grid bearing and
> the court survives. Build on that one.

That five-vertex simplification of the 21-vertex survey ring encloses 1,911.0 m2
against the survey's 1,906.1 m2 (+0.26%). The discarded vertices are sub-1.5 m survey
jogs plus the two light-well notches in the northwest wall, which are modelled as
recessed slots in the roof rather than as notches in the plan — from the app's camera
the two read identically, and a re-entrant plan would cost triangles on walls nobody
can see between two party-wall neighbours. Build on this polygon.

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| N→E | 33.95 m | NE 44.8° | **Third Street front** |
| E→SE | 42.28 m | SE 134.6° | southeast party flank (400 Brannan) |
| SE→S | 6.42 m | SE 135.8° | short return at the Ritch end |
| S→W | 45.22 m | SW 224.9° | **Ritch Street rear** |
| W→N | 49.28 m | NW 315.9° | northwest party flank (560 Third), sawtoothed in the survey |

Because of the 45° heading the axis-aligned bounding box is ~66 x 60 m. That is correct.

### 2.4 What each side shows

**Northeast (Third Street front)** — The hero elevation and the only painted one. A
long, flat, **dark chocolate-brown** wall, three storeys, with no cornice and only a
plain parapet. Two upper floors carry a strict grid of **tall narrow windows** with pale
frames, roughly 11 bays across, some grouped in pairs; a few bays carry **fire escapes**
in dark steel. The ground floor is a run of shopfronts and residential entrances in a
darker base. At the northwest end the paint stops and the wall becomes bare brick
(see below).

**Northwest end (visible above 560 Third)** — Because the neighbour is only two storeys,
the upper part of this party wall is exposed: raw dark-red/brown brick, no openings,
with faded painted ghost signage, and the **rooftop billboard** standing above it on a
steel frame, facing southeast down Third Street.

**Southwest (Ritch Street rear)** — Unpainted **buff/tan brick**, three storeys, with
segmental-arched window heads, sills, and dark **fire escapes** hung down the wall. The
ground floor has service doors and a garage-type opening. The alley is narrow so this
face is only ever seen obliquely in the real world — but the app's aerial camera sees
it plainly, so it must be built properly.

**Southeast (party flank toward 400 Brannan)** — Mostly buried against the neighbour at
the Third Street end and exposed toward the middle of the block. Treat as bare brick
with a sparse scatter of openings; do not invent a full window grid.

**Top** — A flat, light-gray membrane roof inside a continuous parapet, cut by **two
long dark light wells** running roughly perpendicular to Third Street, plus a scatter of
small skylights and vent boxes. This is the surface the app's camera sees most — design
it, do not leave it flat.

### 2.5 Recognition cues (ranked)

1. **Bulk and rhythm**: a three-storey mass 34 m wide and 45 m deep whose Third Street
   wall is one uninterrupted grid of tall narrow windows
2. The **chocolate-brown painted front** against bare buff brick everywhere else
3. The **rooftop billboard** over the bare northwest end wall
4. Fire escapes on both long elevations
5. The two roof light wells, from above

### 2.6 Miniature translation

**Preserve**

- The single long volume, its real 45° heading, and the full through-block depth
- The window grid's *rhythm and proportion* (tall, narrow, pale-framed) even at reduced count
- The painted-front / bare-brick split, including the exposed northwest end wall
- The billboard as the crest

**Simplify / exaggerate**

- ~11 real bays become 9 clean bays per upper floor on the Third elevation, 8 on Ritch
- Segmental arch heads survive on the Ritch rear only; the front's flat heads stay flat
- Fire escapes become two chunky balcony slabs with a rail each per elevation — no
  ladders, no treads
- Shopfronts become one recessed dark glazed band divided by piers
- The light wells become 0.9 m deep recessed slots in the roof deck, not full-height voids
- The billboard is modelled as a blank panel in a frame on two legs; no artwork
- Ghost signage, downpipes, meters and window bars all disappear

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 footprint from z=0 to z=11.05 in `Toy_stone` (the buff brick
   that the rear, both flanks and the exposed end wall show). Its top cap is the roof
   deck (`Toy_roofd`).
2. Painted front skin: a 0.12 m proud panel on the Third Street edge only, z=0 to
   z=11.9, `Toy_cocoa` — a deliberate palette extension (see 2.8), stopping 4.5 m short
   of the northwest end so the bare brick reads.
3. Base band: z=0 to z=0.55 in `Toy_ink`, front edge only.
4. Ground floor, z=0.55 to z=4.0: on the Third edge a recessed glazed band inset 0.25 m,
   broken by 0.6 m piers, with two 1.4 m entrance recesses in `Toy_ink`; on the Ritch
   edge, one 3.6 m segmental-arched service opening and three arched windows.
5. Floor-line course: 0.2 m `Toy_stone` band at z=4.2, front only.
6. Upper floors: two bands of windows, z=5.0–7.4 and z=7.9–10.3. Third elevation:
   9 bays, openings 1.35 x 2.4 m, recessed 0.2 m, `Toy_glass` with `Toy_trim` frames,
   flat heads. Ritch elevation: 8 bays, same size, segmental heads, `Toy_glass` in bare
   brick. Southeast flank: 4 sparse bays on the block-interior half only.
7. Parapet: z=11.05 to z=11.9, 0.35 m thick, following the footprint, `Toy_stone` with a
   0.16 m `Toy_stone` coping proud on both faces; the front returns in `Toy_cocoa`.
8. Roof deck at z=11.05, `Toy_roofd`: two light wells 3.4 x 12 m recessed to z=10.15 in
   `Toy_ink`, each with a 0.15 m kerb; five skylight boxes 2.2 x 1.6 x 0.35 m in
   `Toy_glassl`; three vent/mechanical boxes in `Toy_steel`; one stair bulkhead
   3.2 x 2.6 x 1.1 m in `Toy_roofd`.
9. Billboard at the northwest end of the roof: two `Toy_steel` legs from z=11.05 to
   z=12.2, a panel 7.6 m wide x 3.2 m tall from z=12.2 to **z=15.4** — `Toy_ink` face
   with a `Toy_trim` frame. This sets the bounding-box top and must land exactly on 15.4.
10. Fire escapes: on Third at bays 3 and 7, on Ritch at bays 2 and 6 — slab
    3.0 x 0.9 x 0.16 m at each upper floor level plus a 0.65 m rail, `Toy_ink`.
11. Bevel 0.12 m, 2 segments on the chunky solids; 0.05 m / 1 segment on window frames;
    none on fills and glow shells.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette, plus one documented extension.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cocoa` | `#6b4a3d` | **palette extension** — the painted Third Street front |
| `Toy_stone` | `#d9d2c2` | buff brick: rear, flanks, exposed end wall, parapet, courses |
| `Toy_ink` | `#3a3530` | base band, shopfront reveals, fire escapes, light wells, billboard face |
| `Toy_glass` | `#2a4d73` | all windows and the shopfront band |
| `Toy_glassl` | `#6f95b8` | roof skylights |
| `Toy_trim` | `#f3efe6` | window frames, billboard frame |
| `Toy_roofd` | `#45454a` | roof deck, bulkhead |
| `Toy_steel` | `#9aa0a6` | roof mechanical units, billboard legs |
| `Toy_glass_Glow` | `#6f95b8` | lit apartment windows at night |
| `Toy_trim_Glow` | `#f3efe6` | the billboard face's uplit edge at night |

Note on `Toy_cocoa`: the real paint is a dark chocolate brown with no palette match —
`Toy_rust` (`#a86444`) is far too orange and turns the building into a brick box, which
is precisely the distinction the front elevation exists to make. Off-palette is a WARN,
not a FAIL. Decide from the aerial render and record the decision in `REPORT.md`.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
glazing — the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a
primary surface must never be authored as glow. Hero glow: a **scatter of lit apartment
windows** across both long elevations — this is 104 flats, so roughly a third lit,
irregularly distributed, is the honest and much prettier reading. Supporting accent: a
thin lit strip along the bottom edge of the billboard face (billboards are uplit; the
panel itself must **not** be a glow surface). The shopfront band gets a modest glow at
the two entrance recesses only.

### 2.9 Top surface

1,900 m2 of flat roof 11 m up, directly under the camera's usual path over SoMa. The two
light wells are the gift here: long dark slots that break the deck into three legible
strips and are honest to the survey. Keep the deck value clearly darker than the parapet
coping, group the vents and skylights along the strips rather than scattering them
evenly, and let the billboard sit hard against the northwest parapet where it really is.

### 2.10 Scope

**In the GLB:** the single 1907 apartment block — body, parapet, all four elevations'
openings, fire escapes, roof deck, light wells, roof furniture, rooftop billboard

**Not in the GLB:** Third Street, Ritch Street, 400 Brannan, 560 Third, street trees,
sidewalk, vehicles, people, plinths, cameras, lights, or any advertising artwork

### 2.11 Triangle budget

Cap 12,000 — larger than 380 Brannan because there are four built elevations and 2.6x
the footprint, but the building has almost no ornament so the cap should still bind.
Suggested split: body, parapet and courses ~2k, upper window bays (~30) ~5k, ground
floor ~1.5k, roof deck, wells and furniture ~2k, fire escapes ~0.7k, billboard ~0.3k.

### 2.12 Draft manifest entry

```json
{
  "id": "574-third",
  "file": "574-third.glb",
  "anchor": [
    -122.3950551,
    37.7801937
  ],
  "targetHeightM": 15.4,
  "cat": 2,
  "name": "574 Third Street",
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

- **New landmark (Case B).** Add a `pipeline/lib/landmarks.mjs` entry (`id: '574Third'`,
  lon/lat as above, `height: 15.4`) and re-bake the affected tiles, or the baked
  procedural building on this footprint will intersect the GLB.
- **Exclusion radius:** this is a huge footprint whose ring vertices reach ~30 m from the
  anchor, so the radius has to cover the building's own ring without reaching the
  neighbours' — and `excluded()` tests every ring vertex as well as the centroid. The
  usual 8–12 m band used on the small Brannan lots is **not** transferable here; measure
  against the real bake input (`data/buildings_datasf.geojson`) and expect a radius in
  the 20–30 m range with a genuinely narrow safe window, because 400 Brannan and 560
  Third both share party walls with it. If no single radius works, use two zones as
  `551Third` does.
- `loadRadius`: the default formula gives `max(2500, 15.4 × 30) = 2500` m. Take the default.
- Batch: built alongside `400-brannan`, which shares its southeast party wall.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 15.4 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~66 x 60 m is expected)
- [ ] Triangles at or under 12,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on lit windows, the billboard's uplit edge and the two entrance recesses
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual ≤ 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The crest is a billboard, and billboards come down.** 15.4 m is the LiDAR maximum and
  it sits 3.5 m above the parapet at the northwest end — exactly where 2019 photography
  shows a rooftop billboard over the bare end wall. If the executing agent's imagery
  shows the billboard gone, drop it, set `targetHeightM` to the 11.9 m parapet, and say
  so in `REPORT.md`. Do not ship a crest that no longer exists.
- **OSM does not know this building.** No OSM way carries any of its eleven addresses;
  the two Bing-traced comb polygons that cover the site (ways 124903634 and 124903638)
  sum to 1,843 m2 against the survey's 1,906 m2 but neither is the building. On dense
  SoMa lots the DataSF footprint is the survey and OSM is a cross-check at best — the
  same lesson 358 Brannan and 165–167 South Park recorded.
- **Nominatim resolves the address to the roadway** by TIGER interpolation, as it does
  for 350 Brannan. Always check whether a geocoder's `way` is a building.
- The 11-bay window rhythm is *inferred* from one oblique photograph at ~60 m; the 9-bay
  simplification is a design decision on top of an uncertain count.
- The southeast flank's openings are entirely *inferred* — no view of that wall was
  found. Modelling it as quiet brick with a sparse scatter is the safe choice.
- The exposed northwest end wall's extent depends on 560 Third's height (LiDAR 6.66 m),
  so roughly 5 m of bare brick shows above it. That is *derived*, not observed.
- No architect is recorded for the 1907 building in any source consulted.
