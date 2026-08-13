# 551 Third Street (Shell Service Station) — SF-SIM asset plan

A working 24-hour Shell filling station on the north-east side of 3rd Street,
mid-block between South Park and Brannan. It is the first asset in the set that
is not a building: the landmark is a **forecourt** — an 807 m² lot holding a
two-wing steel canopy over three fuelling lanes, a small 2000-built kiosk at the
north-west end, and a lot of asphalt. It is also the set's strongest night
subject, because a service station at night is one bright ceiling plane and a
red-and-yellow lightbar, and nothing else on this block does that.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/551-third/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `551-third` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13, which is **not a routine case**) |
| WGS84 anchor | `-122.3946431, 37.7806625` (parcel centroid, measured) |
| Target height | **6.6 m** (canopy pecten/lightbar crown; canopy deck 5.10 m measured, kiosk parapet 3.91 m measured) |
| Site footprint | 39.7 x 20.4 m lot, 807 m2, long side fronting 3rd Street on the 315 deg SoMa grid (parcel 3775/025, measured) |
| Triangle cap | 12,000 |
| Category | `21` (Gas station) — first use of that code in the manifest |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 551 Third Street (Shell station) GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the Shell service station at 551 3rd
Street in San Francisco and deliver it as a downloadable, validated GLB.

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
8. `artifacts/550-third/` — the closest neighbour, directly across 3rd Street,
   and the closest match in scale and detail budget
9. `docs/asset-plans/551-third.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

**This asset is a site, not a building.** Everything below about the canopy, the
islands, the kiosk and the apron is one composition sitting on one lot. Judge it
as a whole from directly above before you judge any part of it.

## Must capture

- The two-wing flat steel canopy floating over the forecourt on slim columns —
  the single strongest cue from any angle
- Its fascia band in Shell red over yellow, wrapping all four sides of both
  wings, with the illuminated lightbar and the pecten (scallop) disc that crowns
  it — this is the identity of the asset and its entire night state
- The pump islands with their dispensers, bollards and hose reels, standing on
  low raised curbs
- The 2000-built single-storey kiosk at the north-west end of the lot: a flat
  parapet box with a glazed shopfront facing the forecourt
- The asphalt apron with painted lane markings, the two curb cuts, and the
  perimeter kerb and bollard line along 3rd Street
- The small forecourt furniture that makes it read as a working station: air and
  water station, waste bins, a windscreen-squeegee stand, the price sign

## Research 551 Third Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the site footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The 3rd Street (south-west) frontage — the public face
- The north-west, north-east and south-east sides of the lot
- Aerial and roof views — **the canopy roof is the primary facade here**
- Ground-level views under the canopy
- Day and night appearance (night is unusually important for this asset)
- Publicly available drawings, plans or diagrams
- **The number, position and orientation of the pump islands and dispensers,
  which this dossier only infers** from three mapped covered lanes. Aerial
  imagery settles it; count the dispensers before you model them.
- **Whether a freestanding price pylon exists on the 3rd Street frontage.** Two
  separate permits to erect a double-faced freestanding electric sign (2000 and
  2001) both expired without completion, so the dossier cannot confirm one.
- The canopy's exact wing geometry — this dossier reads the OSM outline as two
  parallel wings with an open slot between them, which is unusual and should be
  confirmed against imagery before it is modelled

**A dated-source trap specific to this site.** Between 2018 and 2024 this was
San Francisco's first public hydrogen station: two H70 hydrogen dispensers under
this same gasoline canopy, plus a hydrogen equipment enclosure, storage tanks and
an underground offload vault. All of it was demolished under DBI permit
202407015640, **completed 25 August 2025**. Any photograph, article, streetview
capture or 3D model from 2018–2025 shows equipment that no longer exists. Model
the current, post-removal gasoline-and-diesel station. If you find imagery
showing a hydrogen enclosure, that imagery is out of date — do not "correct" the
model toward it.

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/551-third/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3-5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. A contact sheet of
attributed reference thumbnails is welcome if legally permissible — do not commit
copyrighted full-resolution imagery.

**Trademark note.** Shell's pecten and its red/yellow livery are registered
marks. Author them the way the style bible authors every other sign: a
simplified, obviously-toy graphical shape in the project palette, at miniature
scale, as a depiction of a real place at its real address. Do not reproduce
brand artwork, do not commit brand asset files, and do not chase logotype
fidelity — a scalloped disc in `Toy_red` and `Toy_mustard` is the target.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

This asset has no silhouette and no facade in the usual sense. Its composition is
a **plane held above a plane**: a bright canopy deck floating over a dark apron,
with small chunky objects between them. §10 (roofs as secondary facades) governs
the canopy top; the real design problem is the *gap* — the model has to read as
covered space, not as a solid slab, from a camera 30-50 degrees above the
horizon. Keep the columns slim, keep the clearance generous, and make the
underside a deliberately designed surface.

Resist two failure modes specific to this subject: a canopy so thick it becomes a
building, and an apron so empty it becomes a parking lot. The fascia band and the
island cluster are what stop both.

The finished asset must be immediately recognizable as a Shell service station at
this address, consistent with the real site from all four sides and above,
architecturally credible, and a premium handcrafted miniature — not
photorealistic, not voxel art, not generic low-poly, and never accurate in one
view while invented in the others.

## Scope of the exported asset

Export the station site: the canopy and its columns and fascia, the pump islands
and dispensers, the kiosk, the price sign if one is verified, the forecourt
apron with its markings and kerbs, and the fixed forecourt furniture (air/water
station, bins, bollards, squeegee stand).

The apron is part of the asset — it is the ground plane the whole composition
sits on, and without it the canopy floats over baked terrain. Keep it a thin slab
confined to the parcel boundary.

Do not include unrelated surrounding city geometry: 3rd Street itself, the
sidewalk beyond the property line, neighbouring buildings at 181 South Park or
550 3rd Street, street furniture outside the lot, street trees, people,
**vehicles** (the app has its own fleet and will drive its own cars past),
plinths, cameras or lights. Temporary context may appear in review renders but
must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 12,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The lot's long
axis runs 315.1 deg / 135.1 deg true and its 3rd Street frontage faces
225.1 deg (SW), so the contract's "front faces −Y" cannot be honoured literally.
Real-world orientation wins (AGENTS rule 5). Record the decision and the measured
heading in `REPORT.md`.

**Height normalization:** make the exported bounding-box top land exactly on the
verified architectural height, so the loader's `targetHeightM / measuredHeight`
scale is 1.0. Note that the crest is a *thin* element (the pecten/lightbar crown
at 6.6 m) sitting above the canopy deck at 5.10 m — an error in the crest
rescales the entire station, so verify it before you normalize. If you cannot
verify any element above the canopy deck, drop it, set the crest to the measured
5.10 m deck, and say so in `REPORT.md`.

**Normals warning specific to this asset.** A canopy is a thin plate seen from
both sides and the apron is a thin slab, so this model is not a union of closed
solids in the usual way. Build every plate as a real closed box, never as a
zero-thickness plane, or the per-object signed-volume normals test is
meaningless and the app's single-sided rendering will punch holes in it.

## Reproducible Blender workflow

Blender 4.5 LTS or newer, headless only: `blender -b --python script.py -- args`;
no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/551-third/build_551_third.py` (deterministic build script),
`artifacts/551-third/551-third.blend`, and `artifacts/551-third/551-third.glb`.
The script must rebuild the model reliably enough for future revision. Do not
modify or rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`551-third-top.png`, `551-third-north.png`, `551-third-east.png`,
`551-third-south.png`, `551-third-west.png`, plus `551-third-contact-sheet.png`,
at least one high three-quarter aerial beauty render `551-third-aerial.png`, and
a night render `551-third-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the two canopy wings, the
lane and island layout beneath them, the kiosk and the apron markings; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).

**The night render is a hero image for this asset, not a checkbox** — it is the
one view where a service station outperforms every building around it. Give it
the same iteration you give the aerial.

Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `551-third.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Normals are checked two ways: per-object signed
volume (authoritative for a union of closed solids) and a deterministic
visibility-ray test (≤ 0.15% residual, zero for single shells). Render at least
one review image from the re-imported asset. Write
`artifacts/551-third/validation.json` and `artifacts/551-third/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "551-third",
  "file": "551-third.glb",
  "anchor": [
    -122.3946431,
    37.7806625
  ],
  "targetHeightM": 6.6,
  "cat": 21,
  "name": "551 Third Street (Shell Station)",
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
for that, together with the integration notes in `docs/asset-plans/551-third.md`,
**which describe an exclusion-zone problem this site does not share with any
other landmark in the set.**
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent
must re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 551 3rd Street, San Francisco, CA 94107 | OSM `addr` tags (survey-sourced), DBI permits |
| Parcel | Block 3775, Lot 025; address range 551–561 3rd St | DataSF parcels (measured) |
| Lot | 39.7 x 20.4 m rectangle, 807 m2, long side on 3rd Street | DataSF parcel polygon, reprojected (measured) |
| Use | Filling / service station, continuously since at least 1998 | DBI permits, all 26 records 1998–2025 |
| Operator / brand | Shell, `brand:wikidata` Q110716465; open 24/7; self-service | OSM, surveyed `check_date` 2026-04-26 |
| Fuels | Diesel, octane 87 / 89 / 91 | OSM (surveyed 2026-04-26). No `fuel:H2` — see the hydrogen row |
| Canopy | `building=roof`, 151 m2 polygon, 16 vertices, two wings | OSM way/124889461 (measured) |
| Canopy deck top | **5.10 m** above grade | SF 2010 LiDAR footprint SF3775025 / 201006.0050940, `hgt_majoritycm` 510, `hgt_mediancm` 509, std 0.42 m over 601 cells (measured) |
| Canopy crest | **6.64 m** above grade | same record, `hgt_maxcm` 664 — a real feature at >3σ, attributed to the illuminated lightbar / pecten crown (*attribution inferred*, see 2.15) |
| Canopy clearance | ~4.3 m to the underside | *inferred* from the 0.8 m fascia the 2003–04 permits describe, and standard CA forecourt clearance |
| Kiosk | 12.96 x 7.11 m, 92 m2, single storey | OSM way/124889473 (measured); `building:levels=1` |
| Kiosk height | **3.91 m** | LiDAR footprint 201006.0147259, `hgt_mediancm` 391, corroborated by OSM `height=4` (measured) |
| Kiosk built | 2000 — a one-storey retail sales / food market, replacing a demolished one-storey building | DBI PA 9916996 and 20000110593, both complete 2000-06-07 |
| Fuelling lanes | 3 covered lanes, running parallel to 3rd Street | OSM ways 1000437722 / 1000437726 / 1000437730, `covered=yes` (measured) |
| Canopy livery | Red striped vinyl fascia, repainted with an internally illuminated LED lightbar added | DBI PA 200312081764 and 200410187093 (2003–04) |
| Fuel system | Tanks, piping and dispensers wholly replaced 2012 ($210k); enhanced vapour recovery 2008 | DBI PA 201201232709 complete 2012-09-20; 200812108195 complete 2009-05-01 |
| Hydrogen chapter | Two H70 dispensers under the existing gasoline canopy, opened 2018–19; **fully demolished, complete 2025-08-22** | DBI PA 201711083489 complete 2019-04-09; PA 202407015640 complete 2025-08-22; Fiedler Group project recap |
| Anchor | -122.3946431, 37.7806625 | parcel centroid (measured) |
| Long-axis heading | 315.1 deg / 135.1 deg true | parcel geometry (measured) |
| 3rd Street frontage | faces 225.1 deg (SW) | parcel geometry vs 3rd Street centreline, ~30 m SW (measured) |
| Ground | Flat: LiDAR ground mean 6.88 m NAVD88 over the canopy footprint, range 0.35 m | LiDAR record (measured) |
| Air / water | Public compressed-air point on the forecourt | OSM node/10874867184 |

### 2.2 Sources

- https://www.openstreetmap.org/way/124889461 — canopy outline, `building=roof`,
  `amenity=fuel`, Shell brand and fuel tags, surveyed 2026-04-26
- https://www.openstreetmap.org/way/124889473 — kiosk outline,
  `building=commercial`, `building:levels=1`, `height=4`, `shop=convenience`
- OSM ways 1000437720–1000437730 — the forecourt circulation network; the three
  `covered=yes` segments are the fuelling lanes and are the only direct evidence
  of the lane layout
- https://data.sfgov.org/resource/acdm-wktn.json — DataSF parcels, `blklot`
  3775025: the 807 m2 lot polygon and the 551–561 address range
- https://data.sfgov.org/resource/ynuv-fyni.json — SF 2010 LiDAR building
  footprints, records `201006.0050940` (canopy: 601 half-metre cells ≈ 150 m2,
  matching the 151 m2 OSM polygon almost exactly; height median 5.09 m, majority
  5.10 m, std 0.42 m, max 6.64 m) and `201006.0147259` (kiosk: 331 cells ≈ 83 m2,
  height median 3.91 m). **This is also the pipeline's own building source**, so
  these two records are exactly what the bake will draw here.
- https://data.sfgov.org/resource/i98e-djp9.json — DBI building permits, block
  3775 lot 025 (26 records, 1998–2025): the 2000 kiosk rebuild, the 2003–04
  canopy fascia and LED lightbar, the 2004 and 2012 dispenser and tank
  replacements, the 2008 vapour recovery, the 2017–19 hydrogen installation, and
  the 2024–25 hydrogen demolition
- https://www.fiedlergroup.com/architecture-engineering-project-recaps/shell-opens-san-franciscos-first-hydrogen-stations/
  — the architect/engineer's recap, which establishes that the hydrogen
  dispensers were placed *under the existing gasoline canopy* (so the canopy
  predates 2018 and survived the 2025 removal unchanged)
- https://h2fcp.org/content/san-francisco-third-st and
  https://h2fcp.org/sites/default/files/Shell_LD_Closure.pdf — the hydrogen
  station's opening and Shell's light-duty hydrogen closure notice
- https://find.shell.com/us/fuel/10008255-551-3rd-st/en_US — Shell's own current
  site listing
- Aerial/satellite imagery — **not yet consulted for this dossier**; the island
  layout in 2.4 and 2.7 is derived from the OSM lane geometry alone and is the
  weakest part of it

### 2.3 Orientation and placement

A mid-block lot on the north-east side of 3rd Street, between South Park to the
north-west and Brannan Street ~43 m to the south-east. It is *not* a corner lot,
despite being commonly described as "3rd and Brannan". Directly across 3rd Street
to the south-west is 550 Third Street, already in the manifest — the two assets
face each other and will be seen together, which is a useful calibration for
scale and palette.

The SoMa grid here is rotated ~45 deg from true north: 3rd Street runs
135.1 deg / 315.1 deg, and the lot's long side lies along it.

Site-aligned coordinates used throughout this dossier: origin at the parcel
centroid, **u** positive toward 315 deg (north-west, along 3rd Street), **v**
positive toward 45 deg (north-east, into the lot away from 3rd Street). Metres.

```
Parcel        u -21.1 .. +18.6   v -11.4 .. +9.0     (39.7 x 20.4 m, 807 m2)
Canopy        u  -2.9 .. + 8.0   v -13.2 .. +5.6     (two wings, 151 m2)
  wing S      u  -2.9 .. + 8.0   v -13.2 .. -4.5     (10.9 x 8.7 m)
  wing N      u  -2.8 .. + 7.9   v  +0.7 .. +5.6     (10.8 x 4.9 m)
Kiosk         u -21.5 .. -14.3   v  -5.0 .. +8.0     (7.2 x 13.0 m)
Fuel lanes    v = -9.85, -4.55, +4.00, each running in u, ~7-9 m long
```

| Lot edge | Length | Outward normal (true) | What it is |
|---|---|---|---|
| v = -11.4 | 39.7 m | 225.1 deg (SW) | **3rd Street frontage** — both curb cuts |
| u = +18.6 | 20.4 m | 315.1 deg (NW) | side line toward South Park |
| v = +9.0 | 39.7 m | 45.1 deg (NE) | rear line, abuts 181 South Park (14.2 m tall) |
| u = -21.1 | 20.4 m | 135.1 deg (SE) | side line toward Brannan |

Author `+Y` = north and place the lot exactly as measured. The contract's "front
faces −Y" cannot be met — the frontage faces south-west — so real-world
orientation wins per the README orientation note and AGENTS rule 5.

Note that the canopy overhangs the mapped 3rd Street lot line by ~1.8 m at
v = -13.2. That is normal for a forecourt canopy over a sidewalk setback, but it
may equally be OSM tracing slop; the executing agent should decide whether to
clip the canopy to the parcel or let it oversail, and record the decision.

### 2.4 What each side shows

**South-west (3rd Street) — the public face.** The lot is open to the street:
no building line, just a kerb, a bollard run, and two curb cuts with the canopy
and its lit fascia standing back behind them. This is the one direction from
which the station reads as a gap in the block — 550 Third opposite is a solid
48 m wall of warehouse, and this side of the street simply stops. That contrast
is the asset's placement value.

**North-west (toward South Park).** The kiosk end. A blank painted side wall,
service door, bins, and the edge of the apron.

**North-east (rear).** The back of the lot, hard against the 14.2 m flank of
181 South Park, which towers over the whole composition. Perimeter wall, a
line of parked-service clutter, the air/water point.

**South-east (toward Brannan).** Open asphalt and the lot line; the canopy's
south wing fascia is the dominant object.

**Top — the primary facade.** From above the composition is, north-west to
south-east:

1. the kiosk's flat parapet roof with its small mechanical plant;
2. a strip of open apron;
3. the small canopy wing (10.8 x 4.9 m) over one fuelling lane;
4. a ~5 m open slot between the wings — this is the unusual feature and the one
   most in need of verification;
5. the large canopy wing (10.9 x 8.7 m) over two fuelling lanes and the island
   between them;
6. the 3rd Street apron with lane markings and the two curb cuts.

The canopy decks are plain light plates; their whole graphic job from above is
the **fascia band** visible on all four edges of each wing, and the pecten disc.

*The number and position of the pump islands is inferred from the three mapped
lanes and is the least reliable statement in this dossier.* Two islands (one
under each wing) is the reading that fits the lane spacing (5.3 m and 8.55 m);
three is possible. Count them from imagery.

### 2.5 Recognition cues (ranked)

1. **The floating canopy** — a bright plate held ~4.3 m above a dark apron on
   slim columns. Read from any angle and at any distance, and unique on this
   block.
2. **The red-over-yellow fascia band and the pecten disc.** The only saturated
   brand colour in a district of cream and brick.
3. **The hole in the street wall.** An open asphalt lot where every neighbour is
   a continuous two-to-four-storey frontage.
4. **The island cluster** — small chunky dispensers, bollards and curbs under
   the canopy, which is what stops the model reading as a car park.
5. **At night, the lit ceiling.** The underside of the canopy is the brightest
   plane for a block in any direction.

### 2.6 Miniature translation

**Preserve**

- The true lot rectangle and the canopy's two-wing plan
- The 4.3 m clearance — the gap is the composition; do not shrink it
- Deck at 5.10 m, kiosk parapet at 3.91 m, crest at 6.6 m
- The three-lane rhythm and the island positions between them
- The kiosk's setback at the north-west end, and the open apron between it and
  the canopy

**Simplify / exaggerate**

- The fascia band goes **thicker and bolder** than reality (style bible §8) —
  it is the identity and it must survive at city distance
- The pecten becomes a chunky low-segment scalloped disc, oversized, one per
  visible canopy face at most; do not model brand typography
- Dispensers become chunky beveled boxes with a `Toy_ink` face panel and a short
  hose loop — no nozzles, no keypads, no screens
- Lane markings become two or three flat inset `Toy_trim` stripes, not a striping
  plan
- The kiosk shopfront becomes one wide `Toy_glass` band in an `Toy_ink` frame
  with a single door — no product displays
- Bollards become a repeated capsule, 8-segment
- Canopy columns: square, slim, `Toy_steel`, one per wing corner plus a mid pair
  under the large wing

**Do not add** a car wash, a service bay, vehicles, fuel-price digits, people, or
any hydrogen equipment. Do not thicken the canopy into a building, and do not
fill the apron — the emptiness is accurate and it is what makes the site read.

### 2.7 Massing recipe

Build order for the deterministic script, in the site-aligned u/v coordinates of
2.3, z up from the apron surface. Dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render, and after verifying
the island layout.

1. **Apron:** the parcel rectangle, u -21.1..18.6, v -11.4..9.0, extruded
   z=0.00 to 0.14, `Toy_roofd`. This is the asset's base plane; its top at 0.14
   is the ground everything else stands on.
2. **Perimeter kerb:** 0.30 m wide, 0.18 m proud, `Toy_stone`, around the lot
   except at the two curb cuts on the 3rd Street edge (each 8 m wide, centred at
   u ≈ +9 and u ≈ -6, *inferred*).
3. **Lane markings:** three flat `Toy_trim` stripes 0.25 m wide inset into the
   apron top along v = -9.85, -4.55, +4.00.
4. **Canopy wing S:** deck slab u -2.9..8.0, v -13.2..-4.5, underside at
   z=4.30, deck top at **z=5.10**; `Toy_white` soffit and top, with the fascia
   as a separate 0.80 m band wrapping all four edges (see step 6).
5. **Canopy wing N:** deck slab u -2.8..7.9, v 0.7..5.6, same z profile.
6. **Fascia bands:** on both wings, z=4.30..5.10, 0.12 m proud of the deck edge.
   Lower 0.45 m `Toy_mustard`, upper 0.35 m `Toy_red` — the classic Shell
   two-band livery. A thin `Toy_mustard_Glow` shell 0.02 m proud of the yellow
   band is the lightbar (see 2.8).
7. **Pecten crown:** a scalloped disc 1.8 m across, `Toy_mustard` face on a
   `Toy_red` backing ring, 0.25 m thick, standing above the fascia on the
   south-west face of wing S, top at **z=6.60** — the crest. 12-segment scallop
   at most.
8. **Columns:** 0.42 m square `Toy_steel`, z=0.14..4.30. Four at the corners of
   wing S plus a mid pair on its long edges; four at the corners of wing N.
9. **Pump islands:** raised curbs 0.20 m tall, `Toy_stone`, 1.2 m wide, running
   in u. One under wing S at v ≈ -7.2, one under wing N at v ≈ +1.5 (*both
   inferred — verify*). Length ~7 m each.
10. **Dispensers:** two per island, chunky boxes 1.1 x 0.7 x 1.9 m, `Toy_trim`
    body with an `Toy_ink` face panel and a `Toy_red` cap band; a short
    `Toy_ink` hose loop on each side.
11. **Bollards:** `Toy_mustard` capsules 0.22 m across, 1.0 m tall, at both ends
    of every island and in a line of six along the 3rd Street kerb.
12. **Kiosk:** box u -21.1..-14.3, v -5.0..8.0, z=0.14 to **3.91**, `Toy_cream`
    walls under a 0.35 m `Toy_ink` parapet cap. Shopfront on the south-east face
    (toward the forecourt): one `Toy_glass` band 1.0..2.6 m in an `Toy_ink`
    frame, with a 1.1 m door. A `Toy_red` sign panel over the door. Flat
    `Toy_stone` roof with two small `Toy_roofd` plant boxes.
13. **Price sign:** *only if verified* — a 0.35 m thick `Toy_ink` blade on a
    single post near the 3rd Street kerb at u ≈ +14, with `Toy_red` and
    `Toy_mustard` panels. If it is built and reaches above 6.6 m, the crest
    moves to it and `targetHeightM` moves with it.
14. **Forecourt furniture:** an air/water cabinet 0.7 x 0.5 x 1.3 m in
    `Toy_teal` near the rear line (OSM places one at roughly u +7, v +4); two
    `Toy_ink` waste bins; one squeegee stand beside each island.
15. Bevel 0.1 m, 2 segments, on everything. Every plate is a closed box — see
    the normals warning in Part 1.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_white` | `#f7f4ec` | canopy deck top and soffit |
| `Toy_red` | `#c4453c` | upper fascia band, pecten backing ring, dispenser cap bands, kiosk sign panel |
| `Toy_mustard` | `#d9a441` | lower fascia band, pecten face, bollards |
| `Toy_steel` | `#9aa0a6` | canopy columns |
| `Toy_roofd` | `#45454a` | asphalt apron, kiosk roof plant |
| `Toy_stone` | `#d9d2c2` | perimeter kerb, island curbs, kiosk roof |
| `Toy_trim` | `#f3efe6` | lane markings, dispenser bodies |
| `Toy_cream` | `#f2ede3` | kiosk walls |
| `Toy_ink` | `#3a3530` | parapet cap, shopfront frame and door, dispenser face panels, hoses, bins, price-sign blade |
| `Toy_glass` | `#2a4d73` | kiosk shopfront glazing |
| `Toy_teal` | `#3fa8a0` | air/water cabinet (the one cool accent) |
| `Toy_trim_Glow` | `#f3efe6` | canopy soffit light plane |
| `Toy_mustard_Glow` | `#d9a441` | fascia lightbar band, pecten face |
| `Toy_glassl_Glow` | `#6f95b8` | kiosk shopfront at night |

**Night state.** This is the asset's best view and its composition is unusually
simple: **one big hero plane** — the canopy soffit, lit like a ceiling — with the
fascia lightbar drawing the wing outlines in yellow around it, the pecten as a
single bright disc, and the kiosk shopfront as a small warm ground cue. Nothing
else lights: not the apron, not the dispensers, not the kerb.

Glow shells must be thin surfaces proud of the opaque surface behind them — the
app renders `_Glow` in a separate layer at ~12% alpha by day, so a primary
surface must never be authored as glow. That matters more here than on any
previous asset: the canopy soffit is a primary surface, so author it opaque in
`Toy_white` and hang a separate `Toy_trim_Glow` plate 0.02 m below it. Same for
the lightbar band over the yellow fascia.

Follow the README's night-render note — copy `Base Color` into `Emission Color`
at strength 1.0 when rendering the re-imported GLB, or every glow surface renders
white and the yellow lightbar will be lost.

### 2.9 Top surface

The canopy decks are the top surface and they are deliberately plain: two light
plates, each ringed by its fascia band. The design work from above is not on the
decks but *between and around* them — the open slot between the wings, the lane
markings and islands visible through it and around the wings, the kiosk roof, and
the apron. This asset is the set's clearest case of §10 mattering for what a roof
*reveals* rather than what it carries. Resist decorating the decks; if the top
view looks empty, the fault is a canopy that is too large or an apron that is too
bare, not a deck that needs pattern.

### 2.10 Scope

**In the GLB:** the apron and its kerbs and markings, the two canopy wings with
columns, fascia and pecten, the pump islands and dispensers, the bollards, the
kiosk, the forecourt furniture, and the price sign if verified

**Not in the GLB:** 3rd Street, the public sidewalk, 550 3rd Street, 181 South
Park, street trees, street furniture off the lot, people, vehicles, any hydrogen
equipment, plinths, cameras or lights

### 2.11 Triangle budget

Cap 12,000 — below 550 Third's 14,000, because the massing is simpler and the
detail is repetitive rather than varied. Suggested split: apron, kerbs and
markings ~1.2k; two canopy decks and soffits ~1.5k; fascia bands ~1.5k; pecten
~0.8k; columns ~0.8k; islands, dispensers and hoses ~2.5k; bollards ~1k; kiosk
shell, shopfront and roof ~1.8k; forecourt furniture and price sign ~0.6k; spare
~0.3k.

Beware the bollards and the pecten: a capsule at default resolution and a
smooth-scalloped disc will each eat a third of the budget alone. 8-segment
capsules, 12-segment scallop.

### 2.12 Draft manifest entry

```json
{
  "id": "551-third",
  "file": "551-third.glb",
  "anchor": [
    -122.3946431,
    37.7806625
  ],
  "targetHeightM": 6.6,
  "cat": 21,
  "name": "551 Third Street (Shell Station)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`cat: 21` is `Gas station` in `CATEGORY_LABELS` (`app/src/context.js`) and is
used here for the first time by a manifest landmark; `CAT_TONE` in
`app/src/cards.js` already carries index 21 (`mustard`), so the card chip needs
no code change — but look at it once, because nothing in the manifest has
exercised that row before. `loadRadius` is the skill's default
`max(2500, targetHeightM * 30)`.

### 2.13 Integration notes (for later, not this task)

**New landmark**, and the exclusion zone here is a genuine problem rather than a
formality. Read this before running `INTEGRATION-PROMPT.md`.

The bake draws this lot from DataSF `ynuv-fyni`, which holds **two** footprints
on parcel SF3775025 — the canopy (151 m2, 5.09 m) and the kiosk (84 m2, 3.91 m).
Both would sit inside the model. `excluded()` in `pipeline/buildings.mjs` drops a
footprint when its ring centroid **or any vertex** falls inside a single circle
per landmark, and the geometry here does not allow one circle to take both:

| Footprint | Ring centroid from anchor | Nearest vertex from anchor |
|---|---|---|
| Own canopy `201006.0050940` | **2.30 m** | 2.97 m |
| Own kiosk `201006.0147259` | **18.55 m** | 14.93 m |
| Neighbour 181 South Park `201006.0006296` (14.2 m tall, 535 m2) | 15.62 m | **9.00 m** |

A radius must exceed 18.55 m to catch the kiosk by its centroid, but anything
over 9.00 m deletes 181 South Park and opens a hole in the block behind the
station. There is no valid single radius. Moving the anchor does not rescue it
either: a numeric search over the anchor position finds a working window only
13.6 m away from the parcel centroid, which would place the whole station 13.6 m
off its real location — AGENTS rule 5 forbids that.

Three ways out, in order of preference:

1. **Two exclusion zones.** A second circle centred on the kiosk footprint's own
   centroid, `-122.3944607, 37.7805621`, with `r = 5`, drops the kiosk by the
   centroid test with 2 m of margin (the nearest neighbour vertex from that
   point is 6.98 m). Combined with `exclude: 8.5` at the landmark anchor, both
   own footprints go and every neighbour survives. This needs a small
   `pipeline/buildings.mjs` change — an optional array of extra zones on a
   registry entry, roughly five lines, since `exclusions` is already a flat list
   independent of the landmarks that produced it. **It is a pipeline change, so
   it is an owner decision, not the integrating agent's.**
2. **Re-measure first.** The 550 Third integration found the pipeline's own
   numbers — DataSF rings simplified at the 0.6 m tolerance, `ringCentroid` —
   differed enough from the raw measurements to change the answer (its estimated
   12 became a measured 8). Compute the table above against the pipeline's
   actual cleaned rings before concluding that option 1 is needed.
3. **Ship `exclude: 8.5` alone** and accept that the baked 3.91 m kiosk block
   remains, coincident with the modelled kiosk. This is a visible defect
   (z-fighting on two near-identical boxes) and should only be a temporary state.

Whichever path is taken, verify visually that the baked canopy and kiosk are gone
and that 181 South Park, 171 South Park and 550 3rd Street all survive.

Other notes:

- Manifest id `551-third` maps to registry id `551Third`.
- No camera preset key. At 6.6 m this is texture in the block, not a
  destination — the key row stays reserved for skyline landmarks.
- The lot is flat made ground (LiDAR ground mean 6.88 m NAVD88, range 0.35 m
  over the canopy footprint). Terrain seating should be uneventful, but the
  apron is a 20 x 40 m plate and a plate shows terrain error that a small
  building would hide — check the seating carefully at all four lot corners.
- Batch mode applies: this is a Case B landmark, so the re-bake must be run for
  QA and then thrown away before committing, per
  `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] bbox top exactly 6.6 m so the loader's scale factor is 1.0
- [ ] Footprint ≈ 39.7 x 20.4 m and confined to the parcel (or the canopy's
      oversail explicitly justified in `REPORT.md`)
- [ ] Triangles at or under 12,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the canopy soffit plate, the fascia lightbar, the pecten
      face, and the kiosk shopfront — and every one of them a thin shell proud
      of an opaque surface
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume + deterministic ray test); every plate a closed box, no
      zero-thickness planes
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] No vehicles and no hydrogen equipment anywhere in the export
- [ ] Six review renders + night render + contact sheet regenerated from the
      final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The crest is a thin element and its identity is inferred.** 5.10 m to the
  canopy deck is measured and tight (601 LiDAR cells, std 0.42 m). The 6.64 m
  maximum over the same footprint is a real feature at more than 3σ, and the
  2003–04 permits for an internally illuminated LED lightbar and a repainted
  fascia make a lit pecten crown the natural explanation — but the attribution
  is inference, not observation. Because `targetHeightM` is the crest, getting
  it wrong rescales the entire station. Verify from imagery; if nothing above
  the deck can be confirmed, set the crest to 5.10 m and say so.
- **The pump island layout is inferred from three mapped lanes and nothing
  else.** No source consulted here states how many islands or dispensers exist.
  This is the single most likely thing to be wrong, and it is in the middle of
  the composition.
- **The two-wing canopy with an open slot is an unusual form** read off one OSM
  outline traced from Bing. It could equally be a single canopy with a
  re-entrant corner, or two independent canopies. Confirm before modelling.
- **No freestanding price pylon is confirmed.** Both permits to erect one (2000,
  2001) expired. If one exists and is tall, it becomes the crest.
- **Dated sources are actively misleading for this site.** 2018–2025 imagery and
  articles show a hydrogen installation demolished in August 2025. 2010 LiDAR
  and Bing-traced OSM predate it entirely and are therefore *safer* here than
  recent photography — the opposite of the usual situation.
- **The exclusion zone cannot be solved with the current pipeline** without
  either a code change or an accepted defect (2.13). Do not start integration
  assuming it is routine.
- **This is the first asset in the set that is a site rather than a building**,
  and the first to ship a large flat ground plate. Two style risks follow: the
  apron can read as a hole in the city if its colour drifts from the baked
  street tone, and the canopy can read as a solid block if the clearance is
  compressed. Judge both from the high three-quarter aerial before anything
  else.
- The kiosk's LiDAR footprint carries a 14.2 m maximum return over an otherwise
  3.9 m building — almost certainly overhanging vegetation or a neighbouring
  parapet caught in the polygon, not a structure. It is ignored here. If
  imagery shows something tall on the kiosk, revisit.
