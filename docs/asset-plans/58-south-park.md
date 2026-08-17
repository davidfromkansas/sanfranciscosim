# 58 South Park — SF-SIM asset plan

A 2009 four-storey mixed-use infill on the north-west rim of the South Park oval: one
building, three stacked condominium lots — `58` the ground-floor creative office, `56` the
middle flat, `54` the penthouse that spans the two upper levels and the roof. It replaced a
two-storey office block that was demolished in 2005, and it was built as one half of a pair
with 44-46 South Park next door under the same 2005 permit set. Nine and a half metres of
frontage, thirty metres deep, party walls on **both** flanks, and a two-tone stack — pale
plaster below, a dark charcoal metal-panel box on top — that is the whole identity of the
building from any distance.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/58-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `58-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3938881, 37.7821223` (parcel centroid — measured) |
| Target height | **16.9 m** to the roof-level office/headhouse crest (main parapet 13.6 m) — *estimated*, see 2.1 and 2.15 |
| Footprint | 9.73 m (South Park frontage, SE) x 30.10 m deep; 292.8 m2, measured from the assessor parcel |
| Triangle cap | 10,000 |
| Category | `2` (apartments — two dwellings over one commercial condo) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 58 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 54-58 South Park in San Francisco (addressed here
as 58 South Park) and deliver it as a downloadable, validated GLB.

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
7. `artifacts/101-south-park/` — the closest reference implementation in scale, district and
   character (a modern, restrained, narrow-fronted South Park street building on a ~45°
   footprint with a designed flat roof and a small night state)
8. `artifacts/108-south-park/` — the closest reference for the *structural* situation here:
   a South Park row building with party walls on both flanks, where only the front and rear
   elevations exist
9. `docs/asset-plans/58-south-park.md` — this plan, whose dossier is your research starting
   point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules. Do not invent a new style and do not copy visual
instructions from unrelated prompts.

## Must capture

- A narrow, deep four-storey box: only 9.7 m of frontage on South Park, running 30.1 m back,
  **attached on both flanks** — the front (SE) and rear (NW) are the only real elevations
- The **two-tone stack**: three storeys of pale warm-gray plaster carrying a **dark charcoal
  metal-panel top storey**. This is the single strongest recognition cue and it must read
  from the app's aerial camera at thumbnail size
- The **tall dark-steel glazed bay at the west end of the frontage** — 58's own commercial
  entry, a two-storey mullioned window wall with glass doors and the `58` numerals above
- The **three-address rhythm along the ground floor**, west to east: 58's glazed shopfront,
  56's plaster bay with a dark slatted vehicle gate, 54's glass residential entry
- The **black horizontal-bar balcony railings** across the middle of the front elevation
- A **band of tall windows** set into the dark top storey, with the panel joints reading as a
  restrained grid
- A **designed roof**: this is a full-floor roof deck, not a bald membrane. Pavers, a
  perimeter guardrail, planters, a skylight, and the small roof-level office/headhouse that
  carries the building's crest

## Research 58 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation, and
gather references covering:

- The front (SE) elevation on South Park, day and night
- The rear (NW) elevation toward Taber Place and the block interior — no ground-level
  photography of it was found in this research pass
- Aerial and roof/top views — the roof layout in 2.9 is read off satellite imagery and
  listing copy only
- Where the mass steps down. The 2010 city LiDAR says ~17% of this footprint is only about
  4 m tall while the rest is at 13.6 m. **Where that low element sits — the rear of the lot,
  or a mid-depth lightwell — is the biggest open question in this plan (see 2.15).**
- The bay widths on the front: the dossier's 3.0 / 3.7 / 3.0 m reading is *inferred* from a
  single January 2025 pano scaled against a 2.13 m door

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**Three source conflicts are already known and are NOT resolved — do not silently inherit
a number from any of them (see 2.1 and 2.15):**

1. **Year built.** Every commercial listing for "58 South Park St" (CoStar-derived: Cityfeet,
   LoopNet and friends) says "Year Built 1907 … this charming three-story building".
   **That is stale CoStar data for the demolished predecessor.** The 2005 permit set records
   "to demolish 2 story office building" on this lot and "to erect 4 story, 2 family dwelling
   w/retail commercial"; the assessor roll records `year_property_built = 2009` for all three
   condo lots; SocketSite photographed the building under construction in May 2009. It is a
   **2009 building with four storeys**. Do not model a 1907 building.
2. **Height.** OSM tags `height=14`. The 2010 city LiDAR over this footprint reports a
   *majority* of 13.59 m, a *median* of 13.50 m and a *maximum* of 16.94 m. The two
   neighbours report maxima of 16.15 m and 16.35 m, which is close enough that mature street
   trees overhanging the front could be contaminating all three. This plan takes 13.6 m for
   the main parapet and 16.9 m for the roof-office crest. **Re-derive the crest yourself and
   say how** — it is the number the loader scales by.
3. **Floor area.** The listings say "8,000 SF total building size" and the assessor records
   2,050 sq ft (56) + 2,960 sq ft (54) of net living area. Four storeys on a 292.8 m2
   (3,152 sq ft) lot is ~12,600 sq ft gross, so the assessor's net areas leave a third to a
   half of each upper floor unaccounted for. That is normal for net-vs-gross with a garage,
   an elevator core and large decks — but it is also what you would see if the upper floors
   are genuinely set back. **Resolve it from imagery, not arithmetic.**

## Create a reference dossier

Write `artifacts/58-south-park/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the 3-5 strongest recognition cues; features to preserve; features to
simplify; uncertainties and conflicting evidence. A contact sheet of attributed reference
thumbnails is welcome if legally permissible — do not commit copyrighted full-resolution
imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few confident
volumes, exaggerate only the signature features, simplify the facade into broad rhythms,
deliberately design every surface visible from above, evaluate from the app's high
three-quarter aerial camera, then simplify again.

This is a **secondary building** in the style bible's detail budget (§21), not a hero
landmark: clear massing, one strong facade rhythm, a designed roof, and exactly one identity
cue carried hard — the dark charcoal top storey sitting on pale plaster. Resist adding
hero-tier ornament.

Note the specific style risk here: a four-storey rectangle 9.7 m wide is very close to a
plain box, and the two neighbours it is attached to are the same height. The three things
that stop it reading as procedural filler are the two-tone stack, the tall glazed bay at the
west end of the front, and the roof deck. Spend the detail budget there.

The finished asset must be immediately recognizable as 54-58 South Park, consistent with the
real building from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and never
accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building on block 3775, lots 219/220/221: body, the stepped rear element,
parapet, the front and rear elevations' openings, the entrances, the balcony railings, and
the roof deck with its furniture and headhouse.

Do not include unrelated surrounding city geometry: South Park (the oval, its lawn, paths or
play structure), South Park Street, Taber Place, the neighbouring buildings at 44-46 and 70
South Park, street trees, the sidewalk, parked cars, motorcycles, people, plinths, cameras
or lights. Temporary context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms; no
negative scales; outward normals; no duplicate or foreign geometry; no image textures; no
transparency; flat-color materials named `Toy_*` from the project palette; `_Glow` suffix
only on surfaces that glow at night; no `Toy_body`; no cameras, lights, animations,
armatures or constraints; no external dependencies; at most 10,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops into
the city at its real-world heading — the loader applies no rotation (`placeGeneric` in
`app/src/assets.js` only scales and positions). The South Park front faces **southeast,
outward normal 135.22°**; the building is rotated roughly 45° off the world axes, so build
directly on the measured footprint polygon in 2.3 rather than modelling an axis-aligned box
and rotating it. This is the case the plans README calls out: the contract's "front faces
−Y" rule cannot be honoured literally here, real-world orientation wins, and the deviation
must be recorded in `REPORT.md` along with the measured heading.

**Height normalization:** the tallest geometry in the export must land at exactly the height
you verify (this plan's estimate is **16.9 m** to the roof-office crest; the main parapet
sits at 13.6 m) so the loader's `targetHeightM / measuredHeight` scale is 1.0. If your
research moves the height, move both the model and the draft manifest entry together and say
so in `REPORT.md`.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/58-south-park/build_58_south_park.py` (deterministic build script),
`artifacts/58-south-park/58-south-park.blend`, and
`artifacts/58-south-park/58-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy the
task.

## Required review renders

Render the exact final geometry from controlled cameras: `58-south-park-top.png`,
`58-south-park-north.png`, `58-south-park-east.png`, `58-south-park-south.png`,
`58-south-park-west.png`, plus `58-south-park-contact-sheet.png`, at least one high
three-quarter aerial beauty render `58-south-park-aerial.png`, and a night render
`58-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the top
view must clearly show the deck, the guardrail ring, the skylight, the planters and the
roof-office headhouse; the aerial view uses the style bible's camera assumptions (30-50
degrees down, long lens). Simple tabletop lighting, neutral warm background, minimal depth
of field, and every image must depict the same exported model.

For the night render, drive the `_Glow` materials from Base Color (copy `Base Color` into
`Emission Color`, strength 1.0) — see the note at the end of `docs/asset-plans/README.md`.
A re-imported GLB's `_Glow` materials otherwise render as white slabs.

## Validate the exported GLB

Re-import `58-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count, camera
count, light count, animation count, applied-transform status, negative-scale status,
normal-orientation status, unexpected geometry, and per-material contract compliance. Render
at least one review image from the re-imported asset. Write
`artifacts/58-south-park/validation.json` and `artifacts/58-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **28 x 28 m** even though the
building is 9.7 x 30.1 m — that is the expected consequence of a ~45° real-world heading,
not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "58-south-park",
  "file": "58-south-park.glb",
  "anchor": [
    -122.3938881,
    37.7821223
  ],
  "targetHeightM": 16.9,
  "cat": 2,
  "name": "54-58 South Park",
  "estimated": true,
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
`docs/asset-plans/58-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* or *estimated* are
visual or derived, not published figures — the executing agent must re-verify anything it
relies on. Like the other South Park street buildings, this one has no architectural
literature: the primary evidence is city data, real-estate copy and photography.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 58 South Park (also 54 and 56 South Park — one building, three condo lots) | SF Assessor `property_location`; DataSF parcels |
| Block / lots | 3775 / **219** (58, commercial), **220** (56), **221** (54) — all three carry the *same* polygon | DataSF Parcels, all mapped 2009-09-09 |
| Predecessor lot | 3775/218 (2007-12-31 → 2009-09-09), before that 3775/050 | DataSF Parcels — **measured** |
| Built | **2009** | SF Assessor `year_property_built = 2009` on all three lots; SocketSite photographed it under construction May 2009 |
| Demolition of predecessor | permit filed 2005-01-05, "to demolish 2 story office building", addressed **64 South Park** | SF Building Permits |
| Construction permit | 2005-01-05, `200501052622`: "to erect **4 story**, 2 family dwelling w/retail commercial" at 54, 56 **and** 58 South Park | SF Building Permits — **the storey count is from here** |
| Paired development | the same day, "to erect 4 story 1 residential condo & retail" at 44 and 46 South Park next door | SF Building Permits |
| Storeys | **4**, plus a roof level | 2005 permit; 2007 and 2009 sprinkler permits all record `existing_stories = 4` |
| Elevator | yes, serving all levels including the roof | 2007-12-05 permit "monitoring of sprinkler system - elevator recall"; 54's listing copy |
| Roof structure | a roof-level room — "roof storage area", given a new window in 2013; marketed as a "private office" beside the full-floor roof deck | 2013-10-15 permit on lot 221; Compass listing for 54 S Park St |
| Use mix | 58 = Commercial Retail (creative office; tenants have included Custom Spaces, Creandum, Branch); 54 and 56 = Single Family Residential condos | SF Assessor `use_definition`; Cityfeet tenant list |
| Net living area | 56: 2,050 sq ft (1 storey, 6 rooms). 54: 2,960 sq ft (2 storeys, 6 rooms). 58: not recorded | SF Assessor secured roll 2016-2025 |
| Gross building area (marketed) | 8,000 sq ft | Cityfeet / CoStar listing — consistent with the assessor's net areas plus a ground-floor commercial condo |
| Footprint | **9.73 m (SE frontage) x 30.10 m deep; 292.8 m2 = 3,152 sq ft** | DataSF assessor parcel polygon, reprojected — **measured**; the listing's "lot 3,168 sq ft" agrees within 0.5% |
| OSM footprint (cross-check) | 9.68 x 29.43 m, 284.9 m2, way `124884349`, `addr:housenumber=54;56;58`, `height=14` | agrees on shape, shifted ~2.3 m NW of the parcel and 3% smaller |
| DataSF LiDAR footprint (cross-check) | 8.69 x 29.7 m, 258.9 m2, `mblr = SF3775219` | roof-outline derived and inset ~0.5 m per side; used for the *heights*, not the plan |
| Party walls | **both flanks.** The parcel polygon shares its NE edge vertex-for-vertex with 3775/217 (44-46 South Park) and its SW edge vertex-for-vertex with 3775/053 (70 South Park) | DataSF Parcels — **measured**, and see 2.13 |
| Ground elevation | 11.58 m min / 11.93 m median (NAVD88), range 0.85 m across the footprint | DataSF `gnd_min_m`, `gnd_mediancm` — the app's terrain handles this, not the asset |
| Roof height, 2010 LiDAR **majority** | **13.59 m** above local ground | DataSF `hgt_majoritycm` — measured; the single largest roof plane |
| Roof height, 2010 LiDAR median / mean / std | 13.50 m / 12.01 m / 3.89 m | DataSF — measured; the mean-below-median skew is what says part of the lot is low |
| Roof height, 2010 LiDAR **minimum** | **3.97 m** | DataSF `hgt_mincm` — measured; ~17% of the footprint, position unknown (see 2.15) |
| Roof height, 2010 LiDAR **maximum** | **16.94 m** | DataSF `hgt_maxcm` — measured, but see the tree caveat in 2.15 |
| Main parapet crest | **13.6 m** | LiDAR majority 13.59, OSM `height=14`, and 4 storeys at ~3.4 m — three independent readings that agree |
| Model crest (roof office) | **16.9 m** | *estimated* from the LiDAR maximum; the 2013 roof-room permit is what makes it credible as a structure rather than a tree |
| Frontage heading | front faces **135.22°** (SE, onto the park); rear faces 315.22°; NE flank 45.18°; SW flank 225.18° | measured from the parcel polygon |

### 2.2 Sources

- https://www.openstreetmap.org/way/124884349 — footprint, `addr:housenumber=54;56;58`, `addr:street=South Park`, `building=yes`, `height=14`
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels — Active and Retired) — the three condo lots, their shared polygon, the 2009-09-09 mapping date, the retired predecessor lots, and the vertex-shared boundaries with 44-46 and 70 South Park
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, 2010 LiDAR-derived) — `SF3775219`: the height distribution quoted in 2.1, plus the neighbours `SF3775217` and `SF3775053` used as controls
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — 29 permits on this lot: the 2005 demolition and 4-storey erection permits, the 2007-2009 sprinkler and elevator permits, the 2008 address-verification permit that spells out "54 residential / 56 residential / 58 commercial", and the 2013 roof-storage window
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls, 2016-2025) — `year_property_built = 2009`, the use classes, and the 2,050 / 2,960 sq ft net areas
- https://socketsite.com/archives/2009/05/the_socketsite_scoop_on_5458_south_park_the_condos_comi.html — the May 2009 construction-stage exterior photograph (`.../uploads/2009/05/54-58-South-Park.jpg`), the unit programme (56: ~2,000 sq ft, 14 ft ceilings, 1,000 sq ft deck; 54: 3,000+ sq ft, 15 ft living-room ceilings, retractable skylight, 1,500+ sq ft deck), and Vanguard Properties as developer. **This is the only unobstructed photograph of the upper facade that was found** — in January 2025 the street trees cover it.
- https://www.compass.com/homedetails/54-S-Park-St-San-Francisco-CA-94107/1PHE91_pid/ and https://nataliacolmenerohomes.com/properties/54-south-park-street-san-francisco-ca-94107-422687643 — 54 sold 23 Dec 2022 for $4,406,000; 3,104 sq ft over 4 levels; 12.5 ft ceilings; walkout deck overlooking the park; floor-to-ceiling windows; retractable skylight; elevator to all levels; **"the full floor roof deck … completing this level is a private office"**
- https://www.cityfeet.com/cont/listing/58-south-park-st-san-francisco-ca-94107/cs36666880 — 58 as creative office, 8,000 SF, tenant list, polished concrete floors, one secured parking space. **Its "Year Built 1907" is wrong — see 2.15.**
- Google Street View, South Park pano at 56 S Park St (capture January 2025) — the ground-floor elevation described in 2.4, and the upward view that shows the crown
- Google Maps satellite (Vexcel imagery, 2026) — the roof layout in 2.9
- https://en.wikipedia.org/wiki/South_Park,_San_Francisco — the oval's context only

No architect is credited anywhere in these sources. Vanguard Properties appears as the
developer/marketer, not the designer. Treat the building as unattributed.

### 2.3 Orientation and placement

The building sits on the **north-west rim** of the South Park oval, roughly a third of the
way along from the eastern end, with its narrow front on the park and its long flanks as
party walls against 44-46 South Park (north-east) and 70 South Park (south-west). Like the
whole SoMa grid it is rotated about 45° from the world axes; South Park's own long axis runs
at bearing 45.5°.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north), already
centred on the anchor `-122.3938881, 37.7821223`:

```
(-14.055,   7.244)      rear (NW) corner, west side
( -7.160,  14.107)      rear (NW) corner, east side
( 14.059,  -7.248)      front (SE) corner, east side
(  7.154, -14.101)      front (SE) corner, west side
```

It is a clean parallelogram — the four edges close to within 10 mm.

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(14.059,-7.248) -> (7.154,-14.101)` | **9.73 m** | SE 135.22° | **South Park front — the hero elevation** |
| `(7.154,-14.101) -> (-14.055,7.244)` | 30.09 m | SW 225.18° | party wall with 70 South Park |
| `(-14.055,7.244) -> (-7.160,14.107)` | 9.73 m | NW 315.13° | rear, onto the block interior toward Taber Place |
| `(-7.160,14.107) -> (14.059,-7.248)` | 30.10 m | NE 45.18° | party wall with 44-46 South Park |

Because of the ~45° heading the axis-aligned bounding box is ~28.1 x 28.2 m. That is
correct.

**The two flanks are literal party walls** — the assessor's parcel polygons for 44-46 and 70
South Park share these edges vertex-for-vertex, at 0.00 m separation. Nothing on them is
visible in the real world or in the app. Model them blank and spend nothing there.

### 2.4 What each side shows

**Southeast (South Park front)** — The hero elevation and effectively the only one that has
been photographed. Four registers, and it changes material halfway up:

- *Ground floor*, west to east, reading the January 2025 pano scaled against a 2.13 m
  entrance door (bay widths *inferred*, ±0.4 m):
  - **58** (~3.0 m, west end): a dark steel-framed glazed shopfront — a pair of glass doors
    with a transom, a fixed glazed sidelight, and the numerals `58` on the dark spandrel
    above. Above it the same dark steel framing continues up as a **tall two-storey mullioned
    window wall**, which is the one place the facade breaks its own horizontal banding.
  - **56** (~3.7 m, middle): pale plaster wall; a **dark vertical-slat metal vehicle gate**
    (the secured parking space) with a narrow pedestrian door beside it; the numerals `56`;
    a pair of tall dark planters flanking the opening.
  - **54** (~3.0 m, east end): pale plaster; glass entry doors in a dark frame; the
    numerals `54`.
- *Second and third storeys*: a flat pale warm-gray plaster plane with punched rectangular
  openings, and a run of **black horizontal-bar balcony railings** in front of the openings
  — a slim, wiry, very horizontal element that is the strongest texture on the middle of the
  building.
- *Fourth storey*: a **dark charcoal metal-panel box**, its panels expressed as a shallow
  grid with visible fastener dots, carrying a horizontal band of tall windows in dark frames.
  In the May 2009 photograph this volume reads as a single dark cap sitting on the pale wall,
  and that is exactly how the miniature should read.
- *Above*: the roof deck's guardrail, and behind it the roof office.

**Northeast flank** and **southwest flank** — party walls, 30 m each, zero separation from
the neighbours. Blank; *not modelled beyond a plain wall*.

**Northwest (rear)** — 9.73 m facing the interior of the block toward Taber Place. No usable
ground-level photography was found. *Inferred*: a plainer version of the front — pale
plaster, a regular stack of large openings (the units' "city views" face this way), a
service door, and the stepped-down low element discussed in 2.15.

**Top** — See 2.9. This is the surface the app's camera sees most, and the listing copy
describes it better than the imagery does.

### 2.5 Recognition cues (ranked)

1. **The two-tone stack** — three storeys of pale plaster carrying a dark charcoal
   metal-panel top storey. Reads at any distance and from directly above as a dark band at
   the park edge of a pale roof.
2. **The tall dark glazed bay at the west end of the front**, running the full height of the
   lower registers — the only vertical element on a horizontally banded facade.
3. The **three-address ground floor**: shopfront, vehicle gate, residential door, in that
   order west to east.
4. The **black horizontal-bar balcony railings** across the middle.
5. The narrow (9.7 m) front on a deep (30.1 m) plan, on the ~45° SoMa heading, with a full
   roof deck on top.

### 2.6 Miniature translation

**Preserve**

- The narrow-front / deep-plan proportion and the real 45° heading
- The pale-below / dark-above split, and the exact storey it happens at (the fourth)
- The tall glazed bay at the west end of the front, full height, unbroken
- A designed roof deck — pavers, guardrail, planters, headhouse
- The step down at the low part of the lot (position to be confirmed, see 2.15)

**Simplify / exaggerate**

- The dark top storey is **pushed 0.15 m proud** of the plaster plane below, so the split
  casts its own shadow line instead of relying on colour alone. This is the one place
  semantic exaggeration is spent.
- The panel grid on the dark box becomes three or four shallow score lines, not a real panel
  layout; the fastener dots disappear entirely (sub-pixel).
- The punched middle-storey windows become one regular grid of recessed rectangles, two per
  storey, not a survey of the real ones.
- The balcony railings become a single chunky horizontal bar element per storey — the real
  ones are five or six thin bars, which vanish and alias at diorama scale.
- The vehicle gate becomes one dark recessed panel with three broad score lines.
- The house numbers, planters at the door, wall lamps, intercom and mailbox all disappear.
- The roof deck's furniture becomes one seating cluster and two planters, grouped toward the
  park end, not scattered.

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render, and adjust *all* of them if the
verified height differs from 16.9 m. `u` runs along the 30.1 m depth from the front (u=0 at
the SE face) toward the rear; `v` runs across the 9.73 m width, west negative.

1. **Main body**: extrude the 2.3 footprint from z=0 to z=10.2 over `u = 0 … 25.1`,
   `Toy_sand`. Three storeys of pale plaster: floor-to-floor 3.4 m.
2. **Rear step-down** (**conditional on 2.15**): the rear `u = 25.1 … 30.1` drops to z=4.0
   with its own thin parapet at 4.3 m, `Toy_sand`. If the research resolves the low element
   as a mid-depth lightwell instead, cut it there and keep the rear full height — but do not
   omit it, because the LiDAR is unambiguous that ~17% of this lot is one storey tall.
3. **Dark top storey**: z=10.2 to z=13.2 over `u = 0 … 25.1`, `Toy_roofd`, offset **0.15 m
   proud** of the body on the SE face and flush elsewhere (the flanks are party walls).
4. **Main parapet**: z=13.2 to z=13.6 following the footprint, 0.3 m thick, `Toy_roofd` with
   a `Toy_steel` coping strip on the SE face only.
5. **Front glazed bay** (`v = -4.87 … -1.87`, i.e. the west 3.0 m of the front): a single
   recessed opening 2.6 m wide from z=0.2 to z=9.6, recessed 0.25 m, frame `Toy_ink` at
   0.18 m, glass `Toy_glass`, with three horizontal transom bars. **Do not subdivide it into
   a mullion grid** — the depth of the reveal is what carries it.
6. **Front ground floor, remaining bays**: 56's vehicle gate 2.6 x 2.6 m recessed 0.2 m,
   `Toy_ink` with three score lines; 54's entry door 1.4 x 2.4 m recessed 0.25 m,
   `Toy_glass` in a `Toy_ink` frame.
7. **Front middle-storey openings**: two openings per storey at z=4.4 and z=7.8, each
   2.0 x 1.9 m, recessed 0.15 m, `Toy_glass`; a `Toy_ink` railing bar 0.12 m deep and 0.5 m
   tall standing 0.1 m proud at each opening's sill.
8. **Dark storey window band**: one opening 5.6 x 1.9 m centred on the front, recessed
   0.15 m, `Toy_glass`, reveal `Toy_roofd`.
9. **Rear openings**: a regular 2 x 4 grid of 1.6 x 1.6 m recessed openings, `Toy_glass`,
   plus one service door.
10. **Roof deck** at z=13.2, `Toy_stone` paving. A `Toy_steel` guardrail ring 1.0 m tall,
    0.08 m thick, inset 0.2 m from the parapet on the SE half only (the parapet does the job
    elsewhere). One skylight box 2.2 x 1.4 x 0.25 m `Toy_glassl` over the park half. Two
    planters 1.6 x 0.7 x 0.6 m `Toy_verdigris`. One seating cluster (a 1.8 x 0.9 x 0.45 m
    bench block and two 0.5 m cubes) `Toy_trim`.
11. **Roof office / headhouse**: 4.0 x 3.6 m footprint on the rear third of the deck, from
    z=13.2 to **z=16.9** (the crest), `Toy_roofd`, with one 1.4 x 1.1 m `Toy_glass` window on
    its SE face (the 2013 permit) and a `Toy_steel` coping. **This element sets the bounding
    box and must land exactly on the verified height.**
12. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_sand` | `#ece4d4` | the pale plaster body, three lower storeys, rear step |
| `Toy_roofd` | `#45454a` | **the dark charcoal top storey**, its parapet, the roof headhouse |
| `Toy_ink` | `#3a3530` | the glazed bay's frame, the vehicle gate, the balcony rails, door frames |
| `Toy_glass` | `#2a4d73` | all windows and glazed doors |
| `Toy_glassl` | `#6f95b8` | the roof skylight |
| `Toy_steel` | `#9aa0a6` | parapet coping, the roof guardrail |
| `Toy_stone` | `#d9d2c2` | the roof deck paving |
| `Toy_verdigris` | `#9fb8a8` | roof planters |
| `Toy_trim` | `#f3efe6` | roof seating cluster |
| `Toy_glass_Glow` | `#2a4d73` | the lit ground-floor glazed bay, and two or three upper lights |

Note on the body colour: the real plaster is a light warm gray — between the palette's
`sand` (`#ece4d4`, warmer and lighter) and `stone` (`#d9d2c2`). `Toy_sand` is the safe
choice because it maximises the contrast with the dark cap, which is the whole point of the
building. If the aerial render shows it reading as cream rather than gray, `Toy_stone` is
the correct fallback; record the decision in `REPORT.md`.

Note on the dark cap: `Toy_roofd` (`#45454a`) is the palette's cool dark gray and is right.
Do **not** reach for `Toy_ink` (`#3a3530`) for the cap — it is warmer and darker and it
would make the cap read as a hole rather than as a solid volume, and `Toy_ink` is already
carrying the frames and rails, which need to stay distinguishable from the cap behind them.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
a closed `_Glow` shell is two alpha layers and reads at roughly a quarter opacity by day, so
never author a primary surface as glow. Hero glow: the tall glazed bay at the west end of
the front, lit fully — it is a nine-metre column of warm light on a narrow facade and it is
the whole night identity of this building. Supporting accents: two of the middle-storey
openings and one light in the dark storey's window band. The roof office's window may take a
small glow. Nothing else glows; there is no signage and no crown lighting.

### 2.9 Top surface

A full-floor roof deck 13.2 m up on a block the camera flies over constantly. The listing
copy is explicit — "the full floor roof deck is an oasis with city views that sparkle at
night. Completing this level is a private office" — and the 2013 permit for a window in the
"roof storage area" confirms the office is an enclosed structure, not a pergola.

From 2026 satellite imagery the roof reads as a pale deck with a dark structure toward the
rear, planting along one edge and furniture grouped toward the park end. Resolution at the
best available zoom (z21, Vexcel) is marginal for this 9.7 m wide roof, so the layout in 2.7
is *inferred* from the copy plus the imagery rather than surveyed.

Keep the deck paving clearly lighter than the parapet ring, keep the headhouse at the rear
so the park half of the deck stays open, and group the furniture — an evenly sprinkled roof
reads as noise from the aerial camera. The dark top storey means this building already
presents a dark band at the park edge of the roof; the deck's pale paving inside it is what
makes the ring read.

### 2.10 Scope

**In the GLB:** the single building on block 3775 lots 219/220/221 — pale body, dark top
storey, rear step, parapet, the front and rear elevations' openings, the three entrances,
the balcony rails, the roof deck and its furniture and headhouse

**Not in the GLB:** South Park itself, South Park Street, Taber Place, the neighbouring
buildings at 44-46 and 70 South Park, street trees, sidewalk, vehicles, people, plinths,
cameras or lights

### 2.11 Triangle budget

Cap 10,000 — a secondary building with one more register than 101 South Park and a real
roof programme. Suggested split: body, cap, rear step and parapet ~2k; the tall glazed bay
~1.2k; ground-floor bays ~1.2k; middle-storey openings and rails ~1.8k; dark-storey band
~0.5k; rear openings ~1k; roof deck, guardrail and furniture ~2k.

### 2.12 Draft manifest entry

```json
{
  "id": "58-south-park",
  "file": "58-south-park.glb",
  "anchor": [
    -122.3938881,
    37.7821223
  ],
  "targetHeightM": 16.9,
  "cat": 2,
  "name": "54-58 South Park",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated. `estimated` is
`true` because no crest height is published anywhere — 16.9 m is the 2010 LiDAR maximum over
this footprint and carries the tree caveat in 2.15. `cat` is `2` (apartments): two dwellings
over one commercial condo, so the building reads residential even though the addressed unit
is the office. `name` is `54-58 South Park` rather than `58 South Park` because that is what
the building is; the manifest id keeps the requested address.

### 2.13 Integration notes (for later, not this task)

- **New landmark, Case B.** Neither `pipeline/lib/landmarks.mjs` nor the manifest knows this
  id. Integration needs a `pipeline/lib/landmarks.mjs` entry (`id: '58SouthPark'`) **and a
  re-bake of the affected tiles**, or the baked procedural building on this exact footprint
  will intersect the GLB.
- **The exclusion radius is the delicate part, and this is a both-flanks party-wall case.**
  The assessor parcels for 44-46 and 70 South Park share this building's flank edges
  vertex-for-vertex, and `excluded()` drops a footprint when its centroid **or any ring
  vertex** falls inside the radius. So a radius large enough to catch this building's own
  ring may also catch a neighbour's — exactly the situation 106 and 108 South Park
  documented. Measure the window at integration time against the two files the bake actually
  reads (`pipeline/data/buildings_datasf.geojson` and `overture_buildings.geojsonseq`),
  record the table in the registry comment the way the neighbours do, and check *which*
  rings drop rather than how many.
- The nearest already-integrated landmarks are 106 (`exclude: 2.1`) and 132
  (`exclude: 2` plus `extraExclusions`) South Park — both ended up with radii of about 2 m
  for the same reason. Expect a similar order of magnitude here, not the 16 m that a
  free-standing building would take.
- **The procedural stand-in here is roughly the right height** (OSM `height=14` against a
  13.6 m parapet), so unlike 101 South Park the unbaked view will *not* obviously reveal an
  exclusion mistake — the procedural block and the asset will be within a metre of each
  other and will simply z-fight. Do the bake before judging, and check the tile diff.
- `loadRadius`: the default formula gives `max(2500, 16.9 * 30) = 2500` m. Take the default.
- If other landmarks are in flight, run stage 5 in **batch mode** (see
  `docs/asset-pipeline/ADDRESS-TO-ASSET.md`): still bake, still QA the bake, then throw the
  bake away and commit source only.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly the verified height (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~28 x 28 m is expected)
- [ ] Triangles at or under 10,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the glazed bay and a few upper lights; glow shells proud of the opaque
      glazing, never a closed shell around a primary surface
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for
      the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **Where is the low element?** The 2010 LiDAR over this footprint has a minimum of 3.97 m
  against a majority of 13.59 m, and the mean (12.01 m) sitting well below the median
  (13.50 m) says that roughly a sixth of the lot is one storey tall. On a 30 m deep,
  9.7 m wide lot with party walls on both sides, that is either **the rear ~5 m** (a
  ground-level yard or garage roof) or **a mid-depth lightwell** — which is the more likely
  answer on code grounds, because the middle rooms of a 30 m deep building need daylight from
  somewhere. The two produce visibly different silhouettes from the app's camera. **This is
  the single most important thing to confirm before modelling**, from oblique aerial imagery
  or the rear of the block.
- **The crest is the weakest number here.** The main parapet at 13.6 m is solid — the LiDAR
  majority, the OSM tag and four storeys of arithmetic all agree. The 16.9 m crest is the
  LiDAR *maximum*, and the two attached neighbours report maxima of 16.15 m and 16.35 m
  despite being lower buildings, which is the signature of mature street trees overhanging
  all three footprints. What rescues it is the 2013 permit for a window in a roof storage
  area and the listing's "private office" on the roof level: a real enclosed structure is
  known to stand up there. Still, ±1 m is honest. Re-derive it, ideally photogrammetrically
  from more than one view, and record the method.
- **"Year Built 1907" is in every commercial listing for this address and it is wrong.** It
  is CoStar data inherited from the demolished predecessor. The permit record, the assessor
  roll and a construction photograph all say 2009. This matters because a plausible-looking
  1907 South Park building is exactly the wrong answer, and it is one search away.
- **The building is unattributed.** No architect is credited in any source found. Do not
  invent one, and do not model to a named architect's language.
- **Only the front elevation has photography, and only from 2009 for the upper half.** The
  January 2025 Street View pano is almost entirely obscured by two mature street trees above
  the ground floor. The May 2009 SocketSite photograph shows the upper facade clearly but the
  building was still under construction — the ground floor in it is unfinished, with red
  primer and temporary rails. Neither photograph alone is sufficient; the model's front comes
  from combining them, and that combination is *inferred*.
- **The rear elevation is entirely inferred.** It faces the block interior and no imagery of
  it was found. It is visible from the app's camera. It deserves a real attempt at reference
  before it is invented.
- **Bay widths on the front are inferred from one pano** scaled against an assumed 2.13 m
  door, ±0.4 m. The 3.0 / 3.7 / 3.0 m split adds to 9.7 m, which is the measured frontage, so
  the reading is at least self-consistent — but the individual widths are not surveyed.
- **Style risk.** A four-storey rectangle 9.7 m wide, attached on both sides, with neighbours
  of the same height, is one bad decision away from reading as procedural filler. The
  two-tone stack, the full-height glazed bay and the designed roof deck are the three things
  that prevent it, and none of them is optional. Judge from the aerial camera first.
- **Naming.** The building is 54-58 South Park; the manifest id is `58-south-park` because
  that is the address requested. If the concierge or a search card ever surfaces "54-58
  South Park" for a query about "58 South Park", that is correct behaviour, not a bug.
