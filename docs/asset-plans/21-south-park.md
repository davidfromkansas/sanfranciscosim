# 21–29 South Park — SF-SIM asset plan

A 1919 two-storey unreinforced-brick warehouse on the **south-east rim of the South Park
oval**, at its Second Street end: 1,115 m² of floorplate, painted bright off-white,
with a long regular rank of **segmental-arched upper windows in near-black teal
industrial sash**, wide ground-floor loft bays under cast-iron spandrel panels, a teal
freight door, and a corbelled brick cornice over a braced parapet. Assessor class
"Industrial"; in practice it has been an office building since the 1990s and is now
venture-capital tenancy — Redpoint Ventures took the 4,200 sq ft ground floor at 27–29
in 2016.

The thing that makes it worth a bespoke asset is not the architecture, it is the
**plan**: the front wall does not run straight. It goes 19.69 m parallel to the park,
then **turns 29° and runs another 12.07 m**, because the lot fronts the *curve* of the
South Park oval where the oval closes at its north-east tip. Nothing else in the
manifest has a street front that bends mid-block. From the app's aerial camera that
bend, on a bright white plane in a block of grey, is the entire recognition.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/21-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `21-south-park` |
| Registry id | `21SouthPark` (`camelId()` in `app/src/assets.js` maps one to the other) |
| Existing procedural builder | none — new landmark (**Case B**: needs a `pipeline/lib/landmarks.mjs` entry and a tile re-bake, see 2.13) |
| WGS84 anchor | `-122.3931063, 37.7817676` — the **world-axis-aligned bbox centre** of the DataSF footprint, NOT the OBB centre (2.3 explains why this one differs) |
| Target height | **11.73 m** to the roof bulkhead — LiDAR maximum, *measured*. Roof deck **9.50 m**, cornice crest **10.20 m** *estimated* (2.1, 2.15) |
| Footprint | 32.75 m (frontage-parallel) × 40.68 m (deep) oriented, 1,115.1 m², 83.7 % filled; developed South Park frontage 33.7 m in two planes |
| Axis-aligned XY bbox | 46.57 × 51.10 m — expected, not a scale error: a 32.7 × 40.7 m building at a 46° heading |
| Triangle cap | 9,000 |
| Category | `3` (Office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 21–29 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of **21–29 South Park** (also signed and leased as
**27 South Park**) in San Francisco and deliver it as a downloadable, validated GLB.

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
7. `artifacts/102-south-park/` — the closest reference for **build machinery** on this
   oval: footprint-driven prism, `face_panel` openings, ring bands, cornice steps, the
   bevel budget, the light-well notches. Read `build_102_south_park.py` before writing a
   line.
8. `artifacts/2-south-park/` — the closest reference for a **brick warehouse with a
   roof bulkhead** (its stair/lift penthouse at 17.72 m over a 12.83 m deck is exactly
   the massing relationship this asset has at 11.73 m over 9.50 m).
9. `artifacts/181-south-park/` and `artifacts/135-south-park/` — palette and bevel
   continuity with the rest of the oval. This asset has to look like it came out of the
   same toy box as the nineteen buildings that already ring South Park.
10. `docs/asset-plans/21-south-park.md` — this plan, whose dossier is your research
    starting point, not a substitute for your own verification.

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules. Do not invent a new style and do not copy
visual instructions from unrelated prompts.

## Must capture

- **The bend in the street wall.** 19.69 m of frontage on outward normal 315.7°, then
  12.07 m on outward normal 286.7°, with a 1.9 m jog between them. This is the single
  identifying feature of the building and the only bent street front in the manifest.
  Build directly on the measured footprint polygon in 2.3. **Do not straighten it, do
  not round it off, and do not model an axis-aligned box and rotate it.**
- **The painted white brick.** The entire building is painted a warm off-white. On a
  block of greige stucco and grey concrete it is the bright plane, and that value
  contrast is what carries it from 400 m.
- **The rank of segmental-arched upper windows** in near-black teal industrial sash,
  running the whole frontage and *turning the corner* at the bend. The arch is shallow
  — a segmental brick arch, not a semicircle. Around eight of them.
- **The ground-floor loft bays**: wide openings, each with a big multi-pane window, a
  **decorative cast-iron spandrel panel** above it, and a **transom row of small panes**
  above that. Three registers per opening, and the spandrel panel is what makes it read
  as a 1919 warehouse rather than a modern shopfront.
- **The freight door** at the bend — a tall pair of flush teal doors with its own
  spandrel and transom, sitting where a warehouse loading doorway used to be — and the
  **warm timber office entrance** beside it, the one saturated thing on the building.
- **The corbelled brick cornice and the parapet** capping a two-storey box. The parapet
  was braced under the city's UMB ordinance in 1990; it is a real, thick, present
  element on all four sides, not a trim line.
- **The equipment-loaded roof with a clear park-facing apron.** The camera looks down.
  The front third of the roof is empty grey membrane; behind it a dense field of
  condensers, ducts and a stair/lift bulkhead. That contrast is the roof's composition.

## Research 21–29 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation,
and gather references covering:

- The north-west (South Park) front, which is the only exposed elevation and the only
  one with photography. Google Street View, **January 2025**, is the primary source;
  the panos at `37.7819404,-122.3934446` and `37.7818985,-122.3933928` are the two used
  here.
- Aerial and roof views. The equipment layout in 2.9 is read off Esri World Imagery at
  z20 only.
- **The bay counts.** The window and opening counts in 2.7 are read off two oblique
  Street View panos with a street tree in front of them. Count them again from a better
  angle before committing. Getting the *rhythm* right matters more than the exact count.
- Whether the roof bulkhead really is a bulkhead. See 2.15.
- Day and night appearance.

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**Three source conflicts are already known and are NOT resolved (2.15):**

1. **Build year.** The SF Assessor roll says **1919**. LoopNet's listing for this exact
   parcel says **1950**. A Perkins&Will project page for an unidentified South Park
   building says "the 1920s". Neither affects the model. Do not present any of them as
   established.
2. **Footprint.** DataSF has **one** footprint over the whole parcel (`SF3775042`,
   1,115.1 m²). OSM has the same building split into **three** ways (`112759863` = 21,
   `112759868` = 27, `112759865` = unnamed/29) that sum to 1,114 m² — the same building,
   differently drawn. Build on the DataSF polygon in 2.3: it is the bake input, so the
   model and the baked city agree with each other.
3. **Height.** The 2010 city LiDAR gives a roof-plane median of **9.60 m**, a majority
   of 9.82 m, a mean of 9.52 m with σ 0.45 m, and a maximum of **11.73 m**. This plan
   takes 9.50 m as the deck, estimates the cornice crest at 10.20 m, and takes 11.73 m
   as the bulkhead crest and therefore the bounding-box top. **Re-derive the height
   yourself and say how.**

## Create a reference dossier

Write `artifacts/21-south-park/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the 3–5 strongest recognition cues; features to preserve; features to
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
two identity cues carried hard — the bent front and the arched-window rank on white.
Resist adding hero-tier ornament.

Note the specific style risk here: this is a **big plain white box**. 32.7 × 40.7 m of
two-storey warehouse is the largest footprint on this oval and the least articulated
mass in the set. The failure mode is a blank slab that reads as a placeholder. The four
things that prevent it are the bend, the dark sash against the white wall, the three-
register ground-floor openings, and a roof that has been *designed* rather than left
flat. None of them is optional.

The finished asset must be immediately recognizable as 21–29 South Park, consistent
with the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building on lot 3775/042: body on the measured 8-vertex footprint,
cornice and parapet, all four elevations, the ground-floor bays, the freight door and
the office entrance, and the roof deck with its equipment field and bulkhead.

Do not include unrelated surrounding city geometry: South Park (the oval, its lawn,
paths or play structure), South Park Street or its sidewalk, 17–19 South Park, 35 South
Park, 318/326 Brannan or any other neighbour, **the crape myrtle street trees in front
of the building** (they are prominent in every photograph and must not be modelled),
parked cars, people, plinths, cameras or lights. Temporary context may appear in review
renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms; no
negative scales; outward normals; no duplicate or foreign geometry; no image textures;
no transparency; flat-color materials named `Toy_*` from the project palette; `_Glow`
suffix only on surfaces that glow at night; no `Toy_body`; no cameras, lights,
animations, armatures or constraints; no external dependencies; at most 9,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The main South Park
front faces **north-west, outward normal 315.7°**; the angled front faces **286.7°**.
The building is rotated ~46° off the world axes, so build directly on the measured
footprint polygon in 2.3. This is the case the plans README calls out: the contract's
"front faces −Y" rule cannot be honoured literally, real-world orientation wins, and
the deviation must be recorded in `REPORT.md` along with the measured heading.

**Centring:** the origin is the **world-axis-aligned bbox centre** of the footprint, not
the oriented-bbox centre. On a skewed quadrilateral these are 2.63 m apart, and only the
AABB centre makes the exported model's XY centre offset land on zero — which is what
`placeGeneric` actually seats. The polygon in 2.3 is already expressed about it. See 2.3.

**Height normalization:** the tallest geometry in the export must land at exactly the
height you verify (this plan's figure is **11.73 m** at the roof bulkhead; the parapet
crest sits at 10.20 m and the deck at 9.50 m) so the loader's
`targetHeightM / measuredHeight` scale is 1.0. If your research moves the height, move
both the model and the draft manifest entry together and say so in `REPORT.md`.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/21-south-park/build_21_south_park.py` (deterministic build script),
`artifacts/21-south-park/21-south-park.blend`, and
`artifacts/21-south-park/21-south-park.glb`. The script must rebuild the model reliably
enough for future revision. No interactive modelling, no random numbers (use a `hash01`
mixer seeded off the feature index for any variation). Do not modify or rename an
unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `21-south-park-top.png`,
`21-south-park-north.png`, `21-south-park-east.png`, `21-south-park-south.png`,
`21-south-park-west.png`, plus `21-south-park-contact-sheet.png`, at least one high
three-quarter aerial beauty render `21-south-park-aerial.png`, and a night render
`21-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the bend, the parapet ring, the clear park-facing apron, the
equipment field and the bulkhead; the aerial view uses the style bible's camera
assumptions (30–50 degrees down, long lens). **Review the aerial first and iterate on
it** before running the formal rig. Simple tabletop lighting, neutral warm background,
minimal depth of field, and every image must depict the same exported model.

For the night render, drive the `_Glow` materials from Base Color (copy `Base Color`
into `Emission Color`, strength 1.0) — see the note at the end of
`docs/asset-plans/README.md`. A re-imported GLB's `_Glow` materials otherwise render as
white slabs.

## Validate the exported GLB

Re-import `21-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Per-object signed-volume normals test is authoritative for a union of
solids; whole-model ray residual ≤ 0.15 %. Render at least one review image from the
re-imported asset. Write `artifacts/21-south-park/validation.json` and
`artifacts/21-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **46.6 × 51.1 m** even though
the building is 32.7 × 40.7 m — that is the expected consequence of a ~46° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "21-south-park",
  "file": "21-south-park.glb",
  "anchor": [
    -122.3931063,
    37.7817676
  ],
  "targetHeightM": 11.73,
  "cat": 3,
  "name": "21-29 South Park",
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
`docs/asset-plans/21-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* or *estimated*
are visual or derived, not published figures — the executing agent must re-verify
anything it relies on. Like the other South Park plans this dossier is thin on published
architectural literature: the building has never been written about as architecture. The
primary evidence is city data (assessor, parcels, LiDAR footprints, 53 building permits)
plus photography, and the strongest single source is the January 2025 Street View pano
of the front.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 21–29 South Park (address range on the parcel; the street is signed "SOUTH PARK", Google and the lease listings write "21-29 S Park St"; the building is marketed as **27 South Park**) | DataSF parcels `3775042` `from_address_num=21`, `to_address_num=29`, `odd_even=O`; OSM `addr:housenumber` 21 and 27 on two of the three ways |
| Block / lot | **3775 / 042** | SF Assessor secured roll; DataSF parcel `3775042`; DataSF footprint `mblr = SF3775042` |
| Built | **1919** | SF Assessor `year_property_built` (rolls 2019 and 2022). LoopNet says 1950 — **unresolved**, see 2.15 |
| Storeys | **2** | SF Assessor `number_of_stories = 2.0`; 53 DataSF building permits all record `number_of_existing_stories = 2`; confirmed by the Jan 2025 pano |
| Property class / use | "Industrial" / "Industrial" on the assessor roll; **office** in practice since the mid-1990s | SF Assessor secured roll; permit `existing_use` runs `warehouse` → `office` from 1991 onward |
| Construction | **Unreinforced brick masonry** with **wooden roof trusses**; construction type 3 | DataSF permits: 1990 "parapet bracing", 1990 "parapet corrective", 1993 "repair to (e) wooden roof trusses", 1993 "umb warehouse to have two party walls as per s.f. bldg. code", 2001 "umb upgrade — plywood diaphragm & collector beams … to (e) braceframe" — **verified** |
| Lot area / building area | 13,420 sq ft (1,246.7 m²) / **24,680 sq ft** (2,292.8 m²) — i.e. two floors of full-lot plate | SF Assessor secured roll; LoopNet gives the same 24,680 SF and a 10,904 SF typical floor |
| Zoning | SPD (SOMA – South Park) | DataSF parcels — **verified** |
| Footprint (DataSF, the bake input) | **1,115.1 m²**; oriented bounding box **32.749 × 40.676 m**, 83.7 % filled; long axis (the depth) bearing 315.97°/135.97° | `SF3775042` reprojected — **measured** |
| Footprint (OSM, cross-check) | the same building drawn as **three** ways — `112759863` (21, 453 m²), `112759868` (27, 408 m²), `112759865` (unnamed, 253 m²) — summing to **1,114 m²**, i.e. the same building to 0.1 % | OSM — **measured**; see 2.15 |
| Anchor (world-AABB centre) | **−122.3931063, 37.7817676** | **measured**. The polygon area centroid is 1.63 m away at −122.3931097, 37.7817531; the OBB centre is 2.63 m away at −122.3931361, 37.7817716; the DataSF parcel centroid is 4.3 m away. See 2.3 for why the AABB centre wins here |
| Developed frontage on South Park | **33.7 m** in two planes: 19.69 m at outward normal **315.7°** and 12.07 m at outward normal **286.7°**, plus a 1.93 m jog between them | **measured** from the footprint polygon |
| Party walls | NE 40.70 m (34.12 + 6.58, outward 43.8°/45.7°) against 17–19 South Park; SE rear 32.75 m (outward 136.0°) against 318/326 Brannan; SW 33.32 m (outward 226.3°) against 35 South Park. **Only the north-west front is exposed** | **measured**; corroborated by the Esri nadir, where all three sides abut roofs |
| Roof height, 2010 LiDAR **median** | **9.60 m** (majority 9.82 m, mean 9.52 m, σ **0.45 m**, min 5.31 m) | DataSF `hgt_median_m` / `hgt_majoritycm` — measured. σ 0.45 m over 4,479 cells is a very flat deck |
| Roof height, 2010 LiDAR **maximum** | **11.73 m** | DataSF `hgt_maxcm` — measured; taken here as the stair/lift bulkhead, see 2.15 |
| Ground elevation | 11.96 m min, 13.45 m max, 12.58 m mean (NAVD88); the site falls **1.49 m** across the footprint | DataSF `gnd_*` — measured. The app's terrain handles this; the fall is small enough that the asset is **not** draped (unlike `64-south-park`) |
| Ground-floor tenancy | **Redpoint Ventures**, 4,200 sq ft raw brick-and-timber ground floor at 27–29 South Park, fitted out by **IwamotoScott Architecture**, 2016 — includes a preserved brick archway from a former warehouse doorway | Architizer / IwamotoScott — **verified** |
| Other tenancy | Transpose Platform Management and seven related LLCs registered at 27 South Park Suite 100 (2017–2024); permit record shows continuous VC/office tenant improvements 2017–2021 | bizprofile.net, DataSF permits — **verified** |
| Lease description | 2 storeys, "brick and timber", "operable windows with views of South Park", 10 ft unfinished ceiling, Class C office, ground-floor identity, surface and covered parking | LoopNet listing 20707079 — **verified as a listing description**, i.e. *observed (listing copy)* |
| Historic status | **none found.** Not a contributor to the South End Historic District (that nomination covers 1 South Park / 3775-007, not 3775-042); no Article 10/11 designation surfaced | National Register nomination for the South End Historic District, searched in full — **verified negative**, see 2.15 |
| OSM tagging | `building=yes` on all three ways, **no `height`, no `building:levels`** on any of them | OSM — **verified**. The baked city's height for this parcel therefore comes from DataSF/Overture, not OSM |

### 2.2 Sources

- https://www.openstreetmap.org/way/112759863 — `addr:housenumber=21`, `addr:street=South Park`
- https://www.openstreetmap.org/way/112759868 — `addr:housenumber=27`, the middle third
- https://www.openstreetmap.org/way/112759865 — the untagged third (29)
- https://www.openstreetmap.org/way/147508663 — 17;19 South Park, the north-east party-wall neighbour
- https://www.openstreetmap.org/way/112759864 — 35 South Park, the south-west party-wall neighbour (`height=10`)
- https://www.openstreetmap.org/way/112759869 — 318 Brannan, behind (`height=8`)
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived),
  record `SF3775042` — the 9.60 m / 11.73 m heights, the full height distribution, and
  the single-polygon footprint the pipeline bakes
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels), record `3775042` — the
  21–29 address range, SPD zoning, parcel centroid
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property
  Tax Rolls), block 3775 lot 042, rolls 2019 and 2022 — 1919, 2 storeys, Industrial
  class, 13,420 / 24,680 sq ft
- `https://data.sfgov.org/resource/i98e-djp9` (DataSF Building Permits), block 3775 lot
  042, 53 permits 1990–2021 — the UMB/parapet/roof-truss evidence, the warehouse→office
  use change, and the 2016–2021 VC fit-out sequence
- https://www.loopnet.com/Listing/21-29-S-Park-St-San-Francisco-CA/20707079/ — the lease
  listing: 2 storeys, brick and timber, 24,680 SF, 10,904 SF floor plate, operable
  windows on the park, Class C
- https://architizer.com/projects/redpoint-ventures/ — IwamotoScott, Redpoint Ventures,
  27–29 South Park, 2016: "4,200 sq ft raw brick and timber ground floor fronting South
  Park", the preserved brick archway
- https://sfplanninggis.org/docs/NatRegDistricts/2008-06-26_Final-NR-SouthEndHistDist.pdf
  — searched in full (194 pp.): the district's only South Park entry is **1 South Park
  (570 Second Street), 3775/007**, the 1913 Tobacco Company of California warehouse by
  William H. Crim Jr. This parcel is **not** in it
- https://sfcityguides.org/tour/old-south-park/ — the block's Gold Rush → Japanese and
  Filipino → warehousing → dot-com → VC arc, which is the story this building sits in
- Google Street View, South Park panos at `37.7819404,-122.3934446` and
  `37.7818985,-122.3933928`, capture **January 2025** — the front elevation described in
  2.4, at two headings
- Esri World Imagery, nadir, z20 (~0.15 m/px) — the roof described in 2.9, and the
  confirmation that all three non-street sides abut neighbouring roofs

Exa searches run, for the record: `21 South Park San Francisco building`;
`21-29 South Park Street San Francisco 1919 warehouse office building history architect`;
`27 South Park San Francisco office building brick timber warehouse tenants history`.
Domains that yielded material: loopnet.com, architizer.com, openpermitdata.com,
checkpermits.com, bizprofile.net, sfplanninggis.org, sfcityguides.org. The
architecture-press and historic-survey queries returned **nothing about this address** —
there is no published architectural description of this building. Everything in 2.4
below the permit row is read off photographs.

Two searches returned near-misses that must not be mistaken for this building:
**One South Park** (1 South Park / 570 Second Street, the 1913 tobacco warehouse
converted to 35 lofts by Levy Design Partners / LDP Architecture) is the *other* end of
the oval, and **Perkins&Will's "South Park Venture Capital Firm"** (16,420 sq ft, 2023,
"a historic 1920s brick-clad building", with a penthouse lounge and roof deck) is a
building this dossier could not identify — the floor area does not match 24,680 sq ft
and a penthouse lounge does not match a two-storey box. Neither is cited as evidence here.

### 2.3 Orientation and placement

The building sits on the **south-east rim** of the South Park oval, at its **north-east
(Second Street) end**, with its whole 33.7 m front on the park and party walls on the
other three sides. Like the whole SoMa grid it is rotated ~46° from the world axes;
South Park's own long axis runs at bearing 45.47°.

In the park's own frame (origin at the park OBB centre, +u north-east along the oval,
+v south-east across it) the building occupies **u 48.8 → 81.5, v 16.1 → 56.8** — i.e.
the last 33 m of the oval's south-east side before it closes. That position is why the
front bends: at u ≈ 69 the street loop starts curving round the oval's tip, and the lot
line follows it.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
already centred on the anchor `-122.3931063, 37.7817676`:

```
( -23.281,  -1.470)   (  -9.193,  12.281)   (  -5.717,  23.844)   (  -6.192,  24.330)
(  -5.919,  25.546)   (  18.693,   1.913)   (  23.286,  -2.796)   (  -0.261, -25.556)
```

Edges, with outward normals:

| Edge | Length | Outward normal | Elevation |
|---|---|---|---|
| `(-23.281,-1.470) -> (-9.193,12.281)` | **19.69 m** | NW **315.7°** | **South Park front, main plane** — exposed |
| `(-9.193,12.281) -> (-5.717,23.844)` | **12.07 m** | WNW **286.7°** | **South Park front, angled plane** — exposed |
| `(-5.717,23.844) -> (-6.192,24.330)` | 0.68 m | SW 225.7° | the jog at the north corner |
| `(-6.192,24.330) -> (-5.919,25.546)` | 1.25 m | WNW 282.6° | the jog at the north corner |
| `(-5.919,25.546) -> (18.693,1.913)` | 34.12 m | NE 43.8° | party wall, 17–19 South Park |
| `(18.693,1.913) -> (23.286,-2.796)` | 6.58 m | NE 45.7° | party wall, continued |
| `(23.286,-2.796) -> (-0.261,-25.556)` | 32.75 m | SE 136.0° | rear party wall, 318/326 Brannan |
| `(-0.261,-25.556) -> (-23.281,-1.470)` | 33.32 m | SW 226.3° | party wall, 35 South Park |

**Why the anchor is the AABB centre and not the OBB centre.** Every other South Park
plan anchors on the oriented-bounding-box centre, and on those near-rectangular
footprints the OBB centre and the world-axis-aligned bbox centre are the same point to
within a few centimetres. This footprint is a **skewed quadrilateral** — the front is
cut on a 29° diagonal — and the two centres are **2.63 m apart**. `placeGeneric()` puts
the *model's origin* at the anchor, and the contract requires the model's origin to be
its XY bbox centre (`xy_center_offset` ≈ 0). So anchoring on the OBB centre would slide
the whole building 2.63 m west of its real footprint, which AGENTS rule 5 forbids.
Centred on the AABB centre the offset comes out **(0.003, −0.005) m**. Record this
choice in REPORT.md; it is a deviation from the habit of the neighbouring plans, not
from the contract.

Because of the ~46° heading the axis-aligned bounding box is **46.57 × 51.10 m** for a
32.75 × 40.68 m building. That is correct.

**Watch the sign of the heading.** An AABB check cannot tell a +46° building from a
−46° one, and `civic-center-plaza` shipped mirrored for exactly that reason. The check
here is: **the angled plane must be at the NORTH-EAST end of the frontage** (nearer
Second Street and 17–19 South Park), and the long straight plane at the south-west end
(nearer 35 South Park). If the bend is at the south-west end the model is mirrored.
Verify in the top render before anything else.

### 2.4 What each side shows

**North-west (South Park front)** — The hero elevation, the only exposed one, and the
only one with photography (Google Street View, January 2025). Painted warm off-white
brick, 33.7 m long, bending 29° a little past the middle, in three registers:

- *Ground floor*: a run of wide loft bays in near-black teal joinery. Each bay is one
  large multi-pane window under a **decorative cast-iron spandrel panel** carrying a
  repeated rosette-and-bar motif, under a **transom row of four small panes**. At the
  bend, a **tall pair of flush teal freight doors** with the same spandrel and transom
  above them — the surviving warehouse loading bay. A few metres north-east of it, the
  **office entrance**: a warm timber double door with a small transom, with the street
  number painted on the brick beside it.
- *Second floor*: a regular rank of **segmental-arched windows**, teal sash, multi-pane,
  set directly into arched brick openings with no architrave — the brick arch itself is
  the surround. The rank runs the whole frontage and turns the bend without interruption,
  which is what makes the bend read as deliberate rather than as damage.
- *Cornice and parapet*: a projecting **corbelled brick cornice** band, painted the same
  off-white, with a flat parapet above it. No signage, no ornament, no crown.

Vertical service runs — a downpipe and a surface conduit — are visible on the wall and
are part of the building's character; one of each is worth modelling.

**North-east flank (17–19 South Park side)** — 40.70 m of party wall. The neighbour
carries a LiDAR median of 6.60 m and a maximum of 16.90 m, so the wall is partly buried
and partly exposed, unpredictably. *Inferred*: blank painted brick, no openings.

**South-east (rear)** — 32.75 m of party wall against the Brannan Street row (318
Brannan `height=8`, 326 Brannan, 334 Brannan `height=12`). *Inferred*: blank painted
brick, no openings, a service door at most.

**South-west flank (35 South Park side)** — 33.32 m of party wall. 35 South Park carries
`height=10` in OSM, slightly taller than this building's 9.50 m deck, so essentially
nothing of this wall is visible. *Inferred*: blank.

**Top** — See 2.9. The best-evidenced surface after the front, and the one the app's
camera sees most.

### 2.5 Recognition cues (ranked)

1. **The bend in the street wall** — 19.69 m, then 29°, then 12.07 m, following the
   curve of the oval. Unique in the manifest and unmistakable from the aerial camera.
2. **The bright painted-white brick mass** against a block of greige and grey.
3. **The unbroken rank of segmental-arched teal windows** turning the corner with the
   wall.
4. **The three-register ground-floor loft bays** — window, cast-iron spandrel, transom —
   with the teal freight door among them.
5. **The corbelled cornice and thick parapet** capping a low two-storey box on a block
   where the neighbours are three and four storeys.
6. **The roof**: a clear grey apron on the park side, a dense equipment field behind it,
   one bulkhead.

### 2.6 Miniature translation

**Preserve**

- The bent footprint, exactly as measured, and the real ~46° heading
- The two-storey proportion and the low, wide mass — this building is *shorter* than
  most of its neighbours and that is part of its identity
- The arched-window rank and the fact that it turns the corner
- The three registers of the ground-floor bay
- The cornice and parapet as distinct elements
- The park-side roof apron

**Simplify / exaggerate**

- Each arched window becomes one opening: a recessed teal reveal, a flat glass fill, and
  a **7-segment segmental arch**. The individual sash muntins are sub-pixel at city scale
  and are dropped; the *arch* is what has to survive, so the reveal is widened to ~0.18 m
- The cast-iron spandrel panel becomes **one recessed panel with three horizontal
  ribs** — no rosettes. Three ribs at 0.10 m read as ornament from above; a modelled
  rosette reads as noise
- The transom row becomes **four flat panes** in one frame, not four modelled openings
- The freight door becomes a single flush slab with a 0.06 m centre reveal
- The office entrance is **widened and its timber deepened past reality**; it is the only
  saturated element on 33.7 m of white wall and it anchors the base
- The corbelled cornice becomes a **two-step profile**, not a row of modelled corbels —
  a corbel is one pixel
- The party-wall elevations get no openings at all
- Roof clutter resolves into one bulkhead, three condenser clusters, one duct run and
  two vents — not the two dozen objects the imagery shows

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render, and adjust *all* of them if
the verified height differs from 11.73 m.

1. **Body**: extrude the 8-vertex footprint of 2.3 from z = 0 to z = **9.50**,
   `Toy_white`. One volume; there is no setback anywhere.
2. **Beltcourse**: a ring band at z = 4.55–4.75 on the two front planes only, projecting
   0.08 m, `Toy_stone`. The line that separates the loft bays from the arched rank.
3. **Ground-floor bays, main plane** (19.69 m): **4 bays** on 4.45 m centres, each
   opening 3.55 m wide, recessed 0.16 m. Within each: glass `Toy_glass` 0.75 → 2.95;
   spandrel panel `Toy_sash` with three 0.10 m ribs, 2.95 → 3.35; transom, four panes
   `Toy_glass` in a `Toy_sash` frame, 3.35 → 4.20. Frames `Toy_sash` throughout.
4. **Ground-floor bays, angled plane** (12.07 m): the **freight door** 2.45 m wide,
   0 → 3.35 m, flush `Toy_sash` with a 0.06 m centre reveal, its spandrel and transom
   carried over it to 4.20 m; **one bay** as (3); and the **office entrance**, 1.70 m
   wide, 0 → 2.95 m, `Toy_rust`, with a single transom pane above to 3.55 m.
5. **Second-floor arched rank**: openings 1.95 m wide, sill 5.55 m, springing 8.05 m,
   crown 8.60 m (0.55 m segmental rise, 7 segments). **5 on the main plane** at 3.55 m
   centres, **3 on the angled plane** at 3.30 m centres. Reveal `Toy_sash` 0.18 m, fill
   `Toy_glass`, no architrave — the brick arch is the surround.
6. **Cornice**: on the two front planes only, plus 1.0 m returns onto the NE and SW
   party walls. Two steps — z = 9.50–9.85 projecting 0.18 m, z = 9.85–**10.20**
   projecting 0.34 m — `Toy_stone`.
7. **Parapet**: a ring band on the three party sides, z = 9.50–9.90, 0.32 m thick,
   `Toy_white` with a `Toy_stone` coping. This is a real braced UMB parapet, not trim.
8. **Roof deck** at z = 9.50, `Toy_stone`. The north-west third (the park-facing apron)
   stays **empty**. Behind it: one **bulkhead** 5.6 × 4.0 m from 9.50 to **11.73**,
   `Toy_steel` with a `Toy_stone` cap — **its top face is the bounding-box top and must
   land exactly on 11.73 m**; three condenser clusters of four 1.3 × 0.9 × 0.8 m units,
   `Toy_steel`; one duct run 14 m × 0.7 × 0.6 m, `Toy_steel`; two vents 0.5 × 0.5 × 0.7 m.
9. **Services**: one downpipe (ø 0.14 m, full height) and one surface conduit on the
   main front plane, `Toy_steel`.
10. **Bevel** 0.12 m / 2 segments on the masses, 0.05 m / 1 segment on the applied
    frames and cornice steps, none on fills, glow shells or spandrel ribs. Clamp every
    bevel to a third of the thinnest dimension.

Storey heights: ground floor 0 → 4.65 m, second floor 4.65 → 9.50 m. Two ~4.7 m loft
storeys is what a 1919 warehouse with a 10 ft finished ceiling and a truss roof gives,
and it is what the LiDAR deck at 9.5–9.6 m independently implies.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette unless noted.

| Material | Hex | Used for |
|---|---|---|
| `Toy_white` | `#f7f4ec` | the painted brick body, parapet |
| `Toy_stone` | `#d9d2c2` | cornice, parapet coping, beltcourse, roof deck, bulkhead cap — a half-tone darker than the body so every cap reads from above |
| `Toy_sash` | `#2f4f49` | **the signature near-black teal industrial joinery**: every window reveal and frame, the spandrel panels, the freight door — see the note below |
| `Toy_glass` | `#2a4d73` | all glazing |
| `Toy_rust` | `#a86444` | **the timber office entrance** — the one saturated accent |
| `Toy_steel` | `#9aa0a6` | roof bulkhead, condensers, duct run, vents, downpipe, conduit |
| `Toy_mustard_Glow` | `#d9a441` | the lit ground-floor loft bays at night — the hero glow |
| `Toy_glassl_Glow` | `#6f95b8` | a scatter of lit second-floor windows |

**`Toy_sash` is off-palette and deliberate.** The observed joinery is a very dark
blue-green, roughly `#2f4f49`. The palette's nearest neighbours are `Toy_roofd`
(`#45454a`, a neutral dark grey) and `Toy_navy` (`#2c4a70`, distinctly blue); neither is
the colour, and this joinery is the second-strongest identity cue after the bend, so it
gets its own key. Off-palette is a WARN, not a FAIL. Say so in `REPORT.md` so a later
reader does not read it as a mistake. If the aerial render shows it reading as flat
black rather than as dark teal, lighten it toward `#375a53` rather than switching to
`Toy_roofd` — the tint is the point. Note also that dark values that look right in the
Blender rig can render near-black in the app's lighting; check it there at stage 5, not
only in the rig.

**Night state (required).** Glow surfaces must be **thin single-sided plates proud of
the opaque glazing**, never closed boxes: the app draws `_Glow` in a separate layer, and
a *closed* shell presents two alpha layers to the daylight camera and tints the surface
it is supposed to be invisible over. Hero glow: the **ground-floor loft bays**, lit warm
and lit fully. This is a VC office building on the park and its big ground-floor windows
are the block's brightest thing after dark; four or five bays of warm light along a
bending white wall is the whole night composition. Supporting accent: five or six lit
second-floor windows scattered across both front planes, never a full rank. Nothing else
glows — there is no signage, no crown, and the roof is dark.

### 2.9 Top surface

A flat grey membrane roof 9.5 m up on a 1,115 m² plate, in a district the camera flies
over constantly, and the largest single roof on the South Park oval. From Esri z20
nadir:

- the **north-west third**, behind the cornice, is **clear** — an empty grey apron with
  nothing on it;
- behind that, a **dense band of mechanical equipment** running roughly parallel to the
  frontage: boxy condensers in loose rows, a long light-toned duct or monitor run down
  the middle, and a larger rectangular structure toward the north-east that reads as a
  **stair/lift bulkhead**;
- the rear third carries scattered units and what appear to be small skylights.

The composition to keep is the **contrast between the empty apron and the loaded field**
— it is what stops a 1,115 m² roof from reading as a blank slab, and it is real. Keep
the equipment in loose rows aligned to the building's own axes (style bible §10: strong
graphical repetition), keep the parapet coping clearly darker than the deck so the ring
and the bend read from directly above, and do **not** fill the apron. The bulkhead is
the only thing that breaks the silhouette; place it where the imagery puts it, toward
the north-east, not in the middle.

### 2.10 Scope

**In the GLB:** the single building on lot 3775/042 — body on the measured 8-vertex
footprint, beltcourse, ground-floor bays, freight door, office entrance, arched rank,
cornice, parapet, roof deck, equipment field, bulkhead, downpipe and conduit.

**Not in the GLB:** South Park itself, South Park Street, its sidewalk and kerb, the
crape myrtle street trees in front of the building, 17–19 South Park, 35 South Park, the
Brannan Street row behind, vehicles, people, plinths, cameras or lights.

### 2.11 Triangle budget

Cap **9,000** — a secondary building, and the cap should bind. Suggested split:

| Element | Estimate |
|---|---|
| body (8-vertex prism, bevelled) + parapet ring + coping | 900 |
| cornice, two steps with returns | 500 |
| beltcourse | 200 |
| 5 ground-floor bays × (glass + ribbed spandrel + 4-pane transom + frame) | 2,600 |
| freight door + office entrance | 400 |
| 8 arched windows, 7 segments each, reveal + fill | 2,600 |
| roof deck + bulkhead | 400 |
| 12 condensers, duct run, 2 vents | 900 |
| downpipe, conduit | 150 |
| glow plates (5 bays + 6 windows) | 200 |
| **Total** | **~8,850** |

The arches are the one place where segment count matters. Seven segments per arch is
enough to read as a shallow segmental curve at diorama scale and is what the budget
assumes; going to twelve costs ~600 triangles for nothing visible.

### 2.12 Draft manifest entry

```json
{
  "id": "21-south-park",
  "file": "21-south-park.glb",
  "anchor": [
    -122.3931063,
    37.7817676
  ],
  "targetHeightM": 11.73,
  "cat": 3,
  "name": "21-29 South Park",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated; `dims` will
be the axis-aligned box, ~46.57 × 51.10 × 11.73 m, while the oriented footprint is
32.75 × 40.68 m. `estimated` is `true` because the crest is a LiDAR maximum *interpreted*
as a bulkhead and the cornice line is read off photographs — flip it to `false` only if
a citable architectural height turns up. `cat: 3` is Office in `CATEGORY_LABELS`, which
is what the building has been since the 1990s and what every permit since 1991 calls it;
the assessor's "Industrial" describes 1919, not 2026. `loadRadius`: the default formula
gives `max(2500, 11.73 × 30) = 2500` m. Take the default — this is a low ground-level
building, not a skyline piece, and `alwaysLoaded` would be wrong.

### 2.13 Integration notes (for later, not this task)

- **New landmark, Case B.** Neither `pipeline/lib/landmarks.mjs` nor
  `app/src/landmarks.js` knows this id. Integration needs a `pipeline/lib/landmarks.mjs`
  entry (`id: '21SouthPark'`) **and a re-bake of the affected tiles**, or the baked
  procedural building on this exact footprint will intersect the GLB.

- **The exclusion must be measured against the real committed bake input**, not taken
  from here. What follows is the measurement done at plan time against the two candidate
  inputs, and the two answers are very different — which is the whole reason to re-measure:

  Against **DataSF footprints** (`ynuv-fyni`), which is the primary bake input,
  `excluded()`'s metric (centroid OR any ring vertex inside the radius), distances from
  the anchor:

  ```
     1.63 m  this building's own footprint SF3775042, via CENTROID   <- the FLOOR
    18.79 m  SF3775046 (17-19 South Park), nearest ring VERTEX       <- the CEILING
    20.78 m  SF3775100, nearest vertex
    22.37 m  SF3775012, nearest vertex
    23.33 m  SF3775102, nearest vertex
  ```

  Safe window **(1.63, 18.79) m** — unusually wide for this oval, because DataSF merges
  the whole parcel into one 1,115 m² polygon and the neighbours' *vertices* sit at the
  far ends of the shared party walls.

  Against **OSM/Overture** (`overture_buildings.geojsonseq`), which gap-fills:

  ```
     4.74 m  own sub-way 112759868 (27), via centroid
     7.92 m  own sub-way 112759863 (21), via centroid
    14.60 m  own sub-way 112759865 (29),  via centroid   <- the FLOOR if OSM is baked
    17.29 m  way 147508663 (17;19 South Park), nearest VERTEX  <- the CEILING
    19.58 m  ways 1168876044 / 112759869 (326 / 318 Brannan), nearest vertex
  ```

  Safe window **(14.60, 17.29) m** — only 2.7 m wide, because OSM splits this building
  into three and the third piece's centroid is 14.6 m out.

  The intersection of the two windows is **(14.60, 17.29) m**, and `exclude: 16` is the
  working answer: it clears every one of this building's own representations in either
  input and stops 1.29 m short of the first neighbour vertex. **Verify it against the
  committed input before believing it**, count the footprints dropped in the affected
  cells, and if the margin above turns out to be thinner than 1 m prefer
  `extraExclusions` circles on the three own-footprint centroids over one large radius.

- **Party-wall collateral is likely and may be unavoidable.** 17–19 South Park, 35 South
  Park and the Brannan row all share the party-wall lines, so some of their ring vertices
  lie *on* this building's boundary. If the measurement shows a neighbour vertex inside
  any workable radius, that is the known infill-site problem — no radius spares a
  shared party-wall vertex — and the honest response is to record which neighbour loses
  its procedural block and whether a GLB replaces it, not to shrink the radius until this
  building's own twin survives.

- **The procedural stand-in is ~9.6 m and the asset is 11.73 m at the bulkhead, 10.20 m
  at the cornice.** The baked city takes its height from DataSF/Overture, not from OSM
  (which has no `height` tag on any of the three ways), so the procedural block is only
  ~0.6 m shorter than this asset's cornice. An unbaked local check will therefore show a
  near-perfect overlap and prove nothing at all. **Do the bake before judging.**

- **No `clearTrees`.** This is a paved party-wall block with no landcover inside the
  footprint. The crape myrtles in front of the building are street trees in the road
  reserve, outside the exclusion's job and outside the asset's scope.

- **Camera.** App yaw = 180 − true bearing. The two front planes face 315.7° and 286.7°,
  so a camera standing at bearing **300°** (west-north-west, out over the park) sees both
  planes and the roof in one three-quarter — `yaw: 240`. `camera: { distance: 170,
  yaw: 240, pitch: 26 }`. **Render it before believing it** (the `592Third` lesson: a
  yaw derived on paper shipped facing two blank party walls).

- **This makes twenty landmarks on one 160 m oval.** After integration run
  `node pipeline/landmark-streaming-check.mjs` against a build: this is by far the
  densest `loadRadius` cluster in the manifest and the procedural fallback would hide a
  loader failure from the eye.

- **Batch mode applies.** If other landmarks are in flight, run stage 5 in batch mode
  (see `docs/asset-pipeline/ADDRESS-TO-ASSET.md`): still bake, still QA the bake, then
  `git checkout -- app/public/tiles api/_data` and commit source only.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0; XY center offset within 0.5 m (this footprint is centred
      to land on ~0.00 — see 2.3)
- [ ] Bounding-box top exactly **11.73 m** (loader scale lands at 1.0)
- [ ] Cornice crest at 10.20 m; roof deck at 9.50 m
- [ ] Oriented footprint 32.75 × 40.68 m ± 0.3 m; AABB ≈ 46.57 × 51.10 m (the ~46°
      heading, not a scale error)
- [ ] **The bend is at the north-east end of the frontage** — the mirror check (2.3)
- [ ] Frontage planes measure 19.69 m and 12.07 m with outward normals 315.7° and 286.7°
- [ ] Triangles at or under 9,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`; `Toy_sash` is
      the one off-palette key and is documented in REPORT.md
- [ ] `_Glow` only on the ground-floor bays and a scatter of second-floor windows; every
      glow surface a **single-sided plate** proud of the opaque glazing, day colours
      matching their non-glow neighbours
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume
      for the union of solids; ray-test residual ≤ 0.15 %)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Top render shows the bend, the empty park-side apron, the equipment field and one
      bulkhead — in that order of legibility
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The crest is an interpretation, the deck is not.** The 2010 LiDAR is exceptionally
  well-behaved on this footprint — median 9.60 m, majority 9.82 m, mean 9.52 m, σ 0.45 m
  over 4,479 cells — so a roof deck at ~9.5 m is about as solid as a derived number gets.
  What is *interpreted* is the 11.73 m maximum: this plan reads it as a stair/lift
  bulkhead, on the strength of the rectangular structure visible in the Esri nadir. It
  could equally be a tall packaged HVAC unit. **The error is contained**: because the
  build normalizes `max_z` to exactly 11.73 and the loader scales by
  `targetHeightM / measuredHeight`, the scale lands at 1.0 and the building's real mass —
  the 9.50 m deck and the 10.20 m cornice — stays correct whatever that object is. A
  wrong reading makes one rooftop box wrong, not the building. Drive the crest from a
  named constant and assert it in the validator so it is a two-minute change.
- **The cornice line at 10.20 m is estimated at ±0.4 m.** It is 0.70 m above the deck,
  read off the January 2025 pano at an oblique angle with a street tree across it. A
  second photograph, or any elevation drawing from the 1990 parapet-bracing permit set,
  would settle it.
- **Build year: 1919 vs 1950 vs "the 1920s".** The assessor roll says 1919 and is the
  best of the three; LoopNet's 1950 is listing metadata and is not corroborated by
  anything; Perkins&Will's "1920s" is about a building this dossier could not confirm is
  this one. Nothing in the model depends on it — but do not assert any of them.
- **Two surveys disagree about how many buildings this is.** DataSF draws one 1,115 m²
  footprint; OSM draws three ways summing to 1,114 m². The assessor settles it — one
  parcel, one 24,680 sq ft building on two floors — and the Street View front is visibly
  continuous across all three, with one cornice, one parapet and one uninterrupted
  window rank. Build one building. But the disagreement has a real consequence at
  integration: it is why the OSM exclusion window (2.13) is 2.7 m wide when the DataSF
  one is 17 m wide.
- **The bay and window counts are the softest numbers in this plan.** Five arched windows
  on the main plane and three on the angled plane, four ground-floor bays plus a freight
  door plus an entrance, are counted from two oblique panos with a crape myrtle in front
  of them. The *rhythm* — a continuous even rank above, wide three-register bays below,
  the freight door at the bend — is well evidenced. The counts are not. Re-count them,
  and if the true count differs, keep the spacing regular rather than forcing this plan's
  number.
- **Three of four elevations are party walls, which is a gift and a trap.** It means
  almost no invented geometry — but it also means the model's whole burden falls on one
  elevation and the roof, and there is nowhere to hide a weak facade. It also means the
  height relationship with the neighbours matters: 35 South Park carries `height=10` in
  OSM against this building's 9.50 m deck, so if that is right, the south-west party wall
  is entirely hidden and the parapet on that side is the only thing that shows. Confirm
  before spending triangles on it.
- **No historic-resource record was found**, and one may not exist. The South End
  Historic District nomination was searched in full and covers 1 South Park (3775/007),
  not this parcel; no Article 10/11 designation and no DPR 523 form surfaced. If one
  exists it would settle the facade description completely; it is the single
  highest-value source still missing.
- **The anchor convention differs from every neighbouring plan** (2.3). This is
  deliberate and measured, but it is exactly the kind of quiet difference that a later
  reader will "fix". It is called out in REFERENCE.md, REPORT.md and the registry
  comment for that reason.
- **Style risk: this is the biggest and plainest box on the oval.** 1,115 m² of two
  storeys, painted one colour, with no setback, no tower, no crown and no ornament above
  the cornice. Every other South Park landmark is a narrow 25-foot lot whose proportion
  does the work. Here nothing does the work except the bend, the value contrast, the
  window rhythm and the roof. Judge it from the app's aerial early and often; if it
  reads as a slab at that distance, the fix is a bolder cornice and a more strongly
  composed roof, **not** more windows.
