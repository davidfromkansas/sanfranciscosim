# 131 Steuart Street (Steuart Place) — SF-SIM asset plan

A 1907 red-brick commercial block on the Steuart Street waterfront row, four doors
southeast of the Audiffred Building. Seven storeys, a measured **21.8 m brick cornice**,
and a set-back glazed penthouse under a curved cream barrel roof reaching **27.7 m** —
on a 14.16 x 42.07 m through-lot that runs the full block depth from Steuart Street to
The Embarcadero.

Its design problem is unusual for this repo. It is a **narrow party-walled slot** —
14 m of frontage carrying 42 m of depth, blind on both long flanks — and it has **two
completely different public ends**. The Steuart Street end is the 1907 building: red
brick, five bays, dark-green painted metal storefront and a projecting green cornice.
The Embarcadero end is the 1983 renovation: pale cast-stone with curved corners, big
steel-sash office glazing, and a set-back barrel-roofed penthouse that is the crest and
the only thing about this building visible from the bay.

From the app's aerial camera it is a thin brick sliver in a row of thin brick slivers,
and the only thing that individuates it is that **crest**: the pale barrel-roofed lantern
at the northeast end, sitting 6 m above the brick cornice its neighbours share. That is
the brief.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/131-steuart/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `131-steuart` |
| Existing procedural builder | none — new landmark (Case B: needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3924393, 37.7930564` |
| Target height | **27.7 m** to the penthouse barrel crown; brick cornice 21.8 m (measured); string course 17.6 m; ground-floor cornice 5.2 m |
| Footprint | 14.16 m (Steuart Street frontage) x 42.07 m (depth to The Embarcadero); 601.8 m2, measured from OSM way 193054132 |
| Triangle cap | 12,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 131 Steuart Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 131 Steuart Street ("Steuart Place") in San
Francisco and deliver it as a downloadable, validated GLB.

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
7. `artifacts/358-brannan/` — the closest palette precedent: the red-brick SoMa
   warehouse whose `Toy_brick` / `Toy_rust` / `Toy_slate` values this asset should reuse
   rather than invent
8. `artifacts/500-third/` and `artifacts/501-second/` — the closest precedents for a
   MULTI-STOREY block with a real cornice and a bay rhythm; check their triangle split
   before designing the window grid, and reuse `500-third`'s `poly_edge` / `wall_box` /
   `bay_spans` / `glazed_elevation` helpers, which are built for exactly this
   45-degree-rotated footprint case
9. `artifacts/300-brannan/` — the nearest precedent for a **penthouse crest above a
   lower parapet** (25.2 m crest over a 21.34 m parapet), which is this building's whole
   silhouette problem
10. `docs/asset-plans/131-steuart.md` — this plan, whose dossier is your research
    starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules. Do not invent a new style and do not copy
visual instructions from unrelated prompts.

## Must capture

- A **narrow deep slot**: 14.16 m of Steuart frontage carrying 42.07 m of depth. It is
  three times as deep as it is wide and it must read that way from above. Do not fatten
  it toward a square.
- **Two different public ends on one building.** This is the identity:
  1. **Southwest (Steuart Street), 14.16 m** — the 1907 face. Red brick, **five bays**,
     six storeys of punched rectangular windows over a tall green-painted metal
     storefront, a **green string course at 17.6 m**, and a **projecting dark-green
     cornice whose top is at 21.8 m**. Gold "131 / STEUART PLACE" lettering on the green
     board over a recessed entry.
  2. **Northeast (The Embarcadero), 14.46 m** — the 1983 face. Pale cast stone with
     **rounded corners**, wide steel-sash office windows in horizontal bands, a
     white-painted ground floor of shopfront glass, and above the 21.8 m line a
     **set-back glazed penthouse under a curved cream barrel roof crowning at 27.7 m**.
- The **crest**, which is the only individuating feature at city scale: the barrel-roofed
  penthouse occupies roughly the northeast **quarter** of the roof (about 10 m of the
  42 m depth, full width) and stands ~6 m proud of the brick cornice. Everything else on
  this block is a flat brick parapet at 20–30 m.
- **Two blind party walls.** The northwest flank (42.03 m) abuts 121 Steuart, the
  southeast flank (42.07 m) abuts 141 Steuart. They are plain brick. But note: 141
  Steuart only reaches ~21.8 m and 121 Steuart ~29.6 m, so the **southeast flank is
  genuinely exposed above about 18 m** and the penthouse is exposed on all four sides.
  Model those exposed strips as real brick and cast-stone surfaces, not as a hole.
- **Colour contrast within one object**: red brick at the Steuart end, pale cast stone at
  the Embarcadero end. Do not homogenise them.

## Research 131 Steuart Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation,
and gather references covering:

- **Both** public ends. A model built from the Steuart Street photograph alone will have
  an invented waterfront elevation, and that is the elevation the app's camera sees from
  the bay.
- Aerial and roof views — the penthouse extent, the roof plant, the light monitor along
  the middle of the roof, and whether the roof steps.
- Ground-level views, day and night.
- The storey count and the cornice height — see 2.15, where the sources conflict.
- The architect (unresolved in this dossier) and the 1983 renovation's scope.

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**Three source conflicts are already known and resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:**

1. **Storey count.** Transwestern, SKYDB and the Assessor's current roll say **7**;
   CompStak says **6**. Counting window rows on the rectified Street View elevation gives
   six rows over a tall ground floor, i.e. **7 storeys**, and the DataSF address file
   carries suites up to `#700`. Seven is right.
2. **`roof:shape=gabled` on OSM way 193054132 is wrong.** Both the aerial and both
   Street View elevations show a flat roof behind a parapet with a curved-roof penthouse
   at the Embarcadero end. Do not build a gable.
3. **DataSF LiDAR `hgt_maxcm` 27.77 m is real here**, and it is the *penthouse*, not the
   cornice. `hgt_mediancm` 23.07 m and `hgt_majoritycm` 24.99 m are a mix of the 21.8 m
   main roof and the curved penthouse roof above it — this footprint is genuinely
   bimodal (sd 3.70 m over 2,461 cells). Independent photogrammetry from two Street View
   panoramas put the crown at 27.5 m, 0.3 m from the LiDAR maximum. See 2.1 and 2.15.

## Create a reference dossier

Write `artifacts/131-steuart/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the 3–5 strongest recognition cues; features to preserve; features to
simplify; uncertainties and conflicting evidence. A contact sheet of attributed reference
thumbnails is welcome if legally permissible — do not commit copyrighted full-resolution
imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade into broad
rhythms, deliberately design every surface visible from above, evaluate from the app's
high three-quarter aerial camera, then simplify again.

This is a **secondary-tier** building in the style bible's sense (§21) — a good street
citizen, not a hero. Spend the detail on the **four moves that survive at thumbnail
size**: the green cornice band, the green ground-floor band, the brick/stone colour split
between the two ends, and the barrel-roofed penthouse. Spend nothing on individual window
muntins, the storefront grilles, the "Saigon" neon, or the cornice modillions; at city
scale they are sub-pixel and they will eat the budget the cornice and the penthouse need.

The finished asset must be immediately recognizable as 131 Steuart Street, consistent
with the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic low-poly,
and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building on parcel lot 3715-025's **131 half only**: both public ends,
both party-wall flanks, the cornice, the parapet, the roof, its penthouse and its plant.

Do not include 141 Steuart (the two-storey classical block with the curved glass box on
top, which shares the parcel but is a separate mass and stays procedural), 121 Steuart,
the Audiffred Building, Steuart Street, The Embarcadero, street trees, the sidewalk,
parked cars, people, plinths, cameras or lights. Temporary context may appear in review
renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms; no
negative scales; outward normals; no duplicate or foreign geometry; no image textures; no
transparency; flat-color materials named `Toy_*` from the project palette; `_Glow` suffix
only on surfaces that glow at night; no `Toy_body`; no cameras, lights, animations,
armatures or constraints; no external dependencies; at most 12,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric`
in `app/src/assets.js` only scales and positions). The Steuart Street front faces
**southwest, bearing 224.9°**; The Embarcadero front faces **northeast, 44.8°**; the
party wall to 141 Steuart faces **southeast, 135.0°**; the party wall to 121 Steuart
faces **northwest, 314.6°**. The building is rotated about 45° off the world axes, so
build directly on the measured footprint rectangle in 2.3 rather than modelling an
axis-aligned box and rotating it.

**Height normalization:** the tallest geometry in the export (the penthouse barrel crown)
must land at exactly **27.7 m** so the loader's `targetHeightM / measuredHeight` scale is
1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/131-steuart/build_131_steuart.py` (deterministic build script),
`artifacts/131-steuart/131-steuart.blend`, and `artifacts/131-steuart/131-steuart.glb`.
The script must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `131-steuart-top.png`,
`131-steuart-north.png`, `131-steuart-east.png`, `131-steuart-south.png`,
`131-steuart-west.png`, plus `131-steuart-contact-sheet.png`, at least one high
three-quarter aerial beauty render `131-steuart-aerial.png`, and a night render
`131-steuart-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the parapet ring, the cornice overhang, the penthouse and the
roof plant; the aerial view uses the style bible's camera assumptions (30–50 degrees down,
long lens), from the **northeast** so that the penthouse crest and The Embarcadero
elevation are seen together — that is the view the app's bay-side camera gets.

Note that the axis-aligned elevation renders will each show the building at 45°. That is
the expected consequence of the real heading, not a camera error.

## Validate the exported GLB

Re-import `131-steuart.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Render at least one review image from the re-imported asset. Write
`artifacts/131-steuart/validation.json` and `artifacts/131-steuart/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **39.8 x 39.8 m** even though
the building is 14.16 x 42.07 m — that is the expected consequence of a ~45° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "131-steuart",
  "file": "131-steuart.glb",
  "anchor": [
    -122.3924393,
    37.7930564
  ],
  "targetHeightM": 27.7,
  "cat": 3,
  "name": "Steuart Place (131 Steuart Street)",
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
`docs/asset-plans/131-steuart.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026. Values marked *inferred* or *estimated* are visual or derived,
not published figures — the executing agent must re-verify anything it relies on.

### 2.1 Verified facts

| Fact | Value | Confidence |
|---|---|---|
| Name | Steuart Place | verified (building signage reads "131 / STEUART PLACE"; Transwestern, CompStak, SKYDB) |
| Address | 131 Steuart Street, San Francisco, CA 94105 | verified |
| Parcel | block 3715, lot 025 (APN 3715-025), address range **131–141 Steuart St** | verified (DataSF `acdm-wktn`) |
| Lot area | 12,603.26 sq ft (1,171 m2) — **the whole 131+141 parcel**, not this building | verified (Assessor `wv5m-vpq2`) |
| Year built | 1907 | verified (Assessor `year_property_built`; Transwestern; CompStak) |
| Renovated | 1983 | verified (Transwestern, CompStak) |
| Storeys | **7** (ground + 6) | verified — Assessor `number_of_stories` 7.0; six window rows counted on the rectified elevation; DataSF address file lists suites to `#700`. CompStak's "6" is wrong (see 2.15 risk 1) |
| Use | Commercial office, class B; welfare exemption (nonprofit hub) | verified (Assessor `use_code` COMO, `exemption_code_definition` "Welfare") |
| Owner | 131 Steuart Street Foundation / Jewish Community Federation (bought Nov 2000) | verified (Assessor `current_sales_date` 2000-11-02; j. weekly, Oct 2000) |
| Zoning | C-3-O (Downtown Office) | verified (DataSF `acdm-wktn`) |
| Neighbourhood | Financial District / South Beach; Supervisorial District 6 | verified |
| OSM | way `193054132`, `building=commercial`, `name=Steuart Place`, `building:levels=7` | verified |
| Footprint | **14.16 m x 42.07 m**, 601.8 m2 (OSM ring); OBB 14.46 x 42.07 m; DataSF LiDAR ring 611 m2, 92% overlap | verified (measured, 2.3) |
| Heading | long axis 44.8° true; Steuart frontage normal 224.9° | verified (measured; method validated against `500-third`, 2.3) |
| Ground | 3.52 m NAVD88 (DataSF `gnd_mediancm`, range 3.44–3.68 m — flat) | verified |
| Main brick cornice, top | **21.8 m** above grade | measured — Street View photogrammetry, two independent panoramas (21.8 m Steuart side, 21.6 m Embarcadero side) |
| Green string course | **17.6 m** | measured (same) |
| Ground-floor cornice / green band | **5.2 m** | measured (same; 5.0 m on the Embarcadero side) |
| Penthouse barrel crown | **27.7 m** — the architectural top | verified — DataSF LiDAR `hgt_maxcm` 2777 (27.77 m); photogrammetry 27.5 m |
| Typical floor-to-floor | 2.77 m (16.6 m over six floors) | derived |
| Building area | 68,400 sq ft (CompStak) / 79,800 sq ft (Transwestern) — **both figures cover 131+141 together** | verified, but not usable for this building alone |
| Architect | **unknown** | unresolved — see 2.15 risk 4 |

**On the LiDAR statistics.** DataSF `ynuv-fyni` for this footprint (`mblr` SF3715025,
611 m2, 2,461 cells at 50 cm) reads `hgt_max` 27.77 m, `hgt_majority` 24.99 m,
`hgt_median` 23.07 m, `hgt_mean` 22.69 m, `hgt_std` **3.70 m**. Applying the sd test from
`164-south-park`: 3.70 m of spread is far too wide for one flat plane with an outlier, so
this footprint is genuinely two-level and the maximum must **not** be discarded. Solving
the two-level model (`f·H + (1−f)·L = mean`, `f(1−f)(H−L)² = σ²`) against the measured
21.8 m main roof gives roughly **a quarter of the plan area** on the higher level — which
is exactly the penthouse footprint read off the Embarcadero elevation. The three sources
(LiDAR maximum, two-panorama photogrammetry, and the Embarcadero elevation) agree to
0.3 m.

### 2.2 Sources

| Source | URL | Establishes |
|---|---|---|
| Transwestern — Steuart Place | https://transwestern.com/property/steuart-place | 1907, renovated 1983, 7 stories, class B office, 131–141 Steuart |
| LoopNet listing | https://www.loopnet.com/Listing/131-141-Steuart-St-San-Francisco-CA/18425801/ | 131 Steuart Street Foundation / Jewish Community Federation nonprofit hub |
| CompStak property page | https://property.compstak.com/131-Steuart-Street-San-Francisco/p/2765 | APN 3715-025, 68,400 sq ft, tenant roster; **says 6 stories — conflicts, see 2.15** |
| SKYDB | https://www.skydb.net/building/137152324/steuart-place/ | 7 floors, low-rise, commercial office |
| j. the Jewish news of Northern California, 6 Oct 2000 | https://jweekly.com/2000/10/06/jcf-proceeds-with-plan-to-buy-2-next-door-buildings/ | JCF purchase of 131 **and** 141 as two adjacent buildings; ground-floor restaurants |
| commercialsearch.com | https://www.commercialsearch.com/commercial-property/us/ca/san-francisco/131-141-steuart-street/ | South Beach, multi-tenant |
| DataSF Parcels `acdm-wktn` | `blklot=3715025` | address range 131–141, C-3-O zoning, parcel centroid |
| DataSF Assessor roll `wv5m-vpq2` | `block=3715 AND lot=025` | 1907, 7 stories, COMO office, welfare exemption, lot area |
| DataSF Building Footprints `ynuv-fyni` | `mblr=SF3715025` | LiDAR height statistics (2010 survey, published 2023) |
| DataSF Addresses `ramy-di5m` | `address like '%STEUART%'` | suite list to `#700`; the 115 / 121 / 131 / 133 / 139 / 141 / 155 sequence along the row |
| DataSF Street Centrelines `3psu-pn9h` | cached in `pipeline/data/streets_datasf.geojson` | which face is Steuart and which is The Embarcadero (2.3) |
| OSM way 193054132 (+ 193054135, 193054137, 193054133, 256969674, 193054136) | https://api.openstreetmap.org/api/0.6/way/193054132/full.json | footprint geometry for this building and its whole block row |
| Google Street View, Steuart Street | panoids `bGhpWtWQe6cDHkmec2tCsA` (2022), `0F4-09tgUjGg6sPgyJ31Gg` (2013), `CmtflDlV1RNYt6bOrZhq-Q`, `44TDz4Q3xLN7ddQOI0pCsw` | the 1907 brick elevation; bay count; storefront; cornice and string course; the photogrammetric height solve |
| Google Street View, The Embarcadero | panoid `bItenxt1tDuMrvL05opHTQ` (2025) | the 1983 cast-stone elevation, the set-back barrel-roofed penthouse, the ground-floor restaurant |
| Google satellite tiles z21/z22 | `https://mt1.google.com/vt/lyrs=s&x=&y=&z=` | flat roof, roof plant, the light monitor along the roof spine; disproves `roof:shape=gabled` |

Everything Street-View-derived is *observed*, not published. Listing photographs are
*observed (listing photo)* — they show the building as marketed.

### 2.3 Orientation and placement

Local tangent projection (`AGENTS.md`): `x=(lon−(−122.4375))·111320·cos(37.77)`,
`z=−(lat−37.77)·110540`.

**Footprint** (OSM way 193054132, four corners, closes to a near-perfect rectangle):

| Corner | lon, lat | x, z (m) | Meaning |
|---|---|---|---|
| P0 | −122.3926647, 37.7929668 | 3945.32, −2538.75 | Steuart frontage, 121 Steuart side |
| P1 | −122.3925508, 37.7928763 | 3955.34, −2528.75 | Steuart frontage, 141 Steuart side |
| P2 | −122.3922125, 37.7931452 | 3985.11, −2558.47 | Embarcadero frontage, 141 side |
| P3 | −122.3923291, 37.7932374 | 3974.85, −2568.66 | Embarcadero frontage, 121 side |

Signed area (x,z) = −601.8 m2 (clockwise). Minimum-area OBB **14.462 x 42.068 m**,
608.4 m2, long axis at 44.8° true.

**Anchor.** OBB centre and polygon centroid agree to 14 mm: `x = 3965.155, z = −2548.65`
→ **`-122.3924393, 37.7930564`**. Use this, not the DataSF parcel centroid
(−122.3923736, 37.7930116) or CompStak's lat/lon — both of those are the centroid of the
**131+141** parcel and sit ~7 m southeast of this building.

**Edge normals** (outward, true bearings):

| Edge | Length | Outward normal | What it is |
|---|---|---|---|
| P0→P1 | 14.16 m | **224.9°** (southwest) | **Steuart Street front** — the address |
| P1→P2 | 42.07 m | 135.0° (southeast) | party wall with 141 Steuart |
| P2→P3 | 14.46 m | **44.8°** (northeast) | **The Embarcadero front** |
| P3→P0 | 42.03 m | 314.6° (northwest) | party wall with 121 Steuart |

**How the street sides were established, and the control that validates the method.**
Perpendicular offsets from the anchor to each named centreline in
`pipeline/data/streets_datasf.geojson`:

| Street | Perpendicular distance | Lies at |
|---|---|---|
| STEUART ST | 32.6 m | 225.1° true (southwest) |
| THE EMBARCADERO | 37.3 m | 48.5° true (northeast) |
| MISSION ST | 59.6 m | 315.2° true (northwest) |
| HOWARD ST | 131.8 m | 135.5° true (southeast) |

Running the identical script against the already-shipped `500Third` anchor returned
3rd Street 45.0°, Ritch 224.9°, Bryant 134.9° — matching `E_THIRD` 44.9°, `E_RITCH`
225.0° and `E_BRYANT` 314.0° in `artifacts/500-third/build_500_third.py` to 0.2° once
both are read in true bearings. The control passes, so the result above is trustworthy.
Two independent confirmations: the DataSF address point for `131 STEUART ST`
(−122.392576, 37.792970) sits **southwest** of the footprint centroid, on the Steuart
side; and the four street bearings form a consistent 45°-rotated grid.

**Neighbours** (all party-wall contacts, from OSM and DataSF LiDAR):

| Neighbour | Side | OSM levels | DataSF `hgt_max` | Consequence for this model |
|---|---|---|---|---|
| 121 Steuart (way 193054135) | northwest | 7 | 29.57 m | covers the northwest flank completely; only the penthouse pokes above |
| 141 Steuart (way 193054137) | southeast | 3 | 21.82 m | **the southeast flank is exposed above ~18 m** |
| 155 Steuart, Hotel Griffon | beyond 141 | 5 | — | context only |
| Audiffred Building (way 193054136) | four doors northwest | 3 | — | context only; a City Landmark, planned separately |

### 2.4 What each side shows

**Southwest — Steuart Street (14.16 m, the address).** The 1907 building.

- Tall ground floor, 0 → 5.2 m, faced in dark-green painted metal and brick: a recessed
  central entry with a shallow arch, gold serif lettering reading "131" over
  "STEUART PLACE" on the green board, flanking storefronts (a print shop and a Vietnamese
  restaurant at the time of the panoramas), roll-down grilles, louvred transoms.
- Six storeys of red brick above, 5.2 → 21.8 m, **five bays wide**, punched rectangular
  windows with dark green-painted frames and pale sills, roughly 2.77 m floor to floor.
  The brick is common bond, weathered orange-red, with pale efflorescence streaks.
- A green string course at 17.6 m under the top floor, and a **projecting dark-green
  sheet-metal cornice** whose top is at 21.8 m. The cornice is the strongest horizontal
  in the row.
- The penthouse is **not visible from Steuart Street** — it is set back at the far end.

**Northeast — The Embarcadero (14.46 m).** The 1983 renovation, and the elevation the
app's bay-side camera actually gets.

- White-painted ground floor, 0 → 5.0 m: a restaurant behind full-height shopfront glass
  between dark pilasters, with a street-level parklet.
- Pale cast stone above with **rounded corners**, five storeys of wide steel-sash office
  windows in continuous horizontal bands separated by pale spandrels, up to the 21.6 m
  parapet band.
- Above that, **set back**, a fully glazed penthouse storey under a **shallow curved cream
  barrel roof** crowning at **27.7 m**. This is the crest and the recognition cue.

**Southeast — party wall with 141 Steuart (42.07 m).** Plain brick below ~18 m (hidden),
exposed brick above, and fully exposed at the penthouse. Blind — no openings.

**Northwest — party wall with 121 Steuart (42.03 m).** Plain brick, hidden to ~29 m by
121 Steuart. Blind. Only the penthouse's northwest face is seen, and only just.

**Top.** Flat membrane roof at ~21.4 m behind the cornice/parapet ring. Along the middle
of the roof runs a raised **light monitor / stair-and-mechanical spine**, with clustered
condensers, ducting and a large dark skylight/light well at mid-depth. The northeast
quarter is the penthouse with its curved roof. The camera looks down; this whole surface
is a facade.

### 2.5 Recognition cues (ranked)

1. **The pale barrel-roofed penthouse at the northeast end**, 6 m proud of a brick cornice
   line its whole block shares. The only silhouette break for 100 m in either direction.
2. **The narrow-and-deep proportion** — 14 m wide, 42 m deep, one of five near-identical
   slots in a row.
3. **The dark-green cornice and the dark-green ground-floor band** bracketing a red brick
   middle. Green-on-brick is the block's signature and this building has the crispest
   example of it.
4. **The two-material split**: red brick at the street end, pale cast stone at the water
   end, on one continuous mass.
5. **Five-bay window grid** at a tight 2.77 m floor rhythm — a dense, small-windowed
   1907 texture, unlike the big-glazed neighbours.

### 2.6 Miniature translation

Secondary tier (style bible §21). The building is a **slab with a hat**. Build it as
three volumes and resist adding a fourth:

- the brick slab (14.16 x 42.07 x 21.4 m) with a chunky beveled cornice ring on top,
- the pale cast-stone re-clad zone at the northeast end — not a separate volume, a
  *material band* wrapping the last ~8 m of both flanks and the whole northeast end,
- the penthouse (14.16 x ~10 m x 6.3 m) with a curved cap.

Exaggerate: the cornice depth (make it read at 3–4 px), the green bands' saturation, and
the penthouse's barrel curvature. Suppress: window frame profiles, the storefront
grilles, the entry arch's mouldings, all signage lettering except a single incised "131"
if it survives the triangle budget.

The five-bay rhythm should be cut as recessed openings in the brick, not as applied
frames — a 1907 punched-window wall reads as *holes*, and holes are cheaper than frames.

### 2.7 Massing recipe

1. Lay out the footprint rectangle from the four measured corners in 2.3 (do **not**
   model axis-aligned and rotate).
2. Extrude the brick slab to **21.4 m** (roof deck). Bevel the vertical arrises ~0.10 m.
3. Ground-floor band: a 0.10 m proud green plinth-and-fascia from 0 to **5.2 m** on the
   two public ends only, with the entry recess cut ~1.2 m deep and ~4.2 m wide, centred,
   on the Steuart end.
4. String course: a 0.08 m proud green band at **17.4–17.6 m**, both public ends.
5. Cornice: a projecting ring 0.45 m proud, **20.3 → 21.8 m**, bevelled, on the two public
   ends and returning ~1.0 m onto each flank. A plain parapet to 21.8 m closes the ring on
   the flanks.
6. Windows: five bays x six floors on the Steuart end, recessed 0.12 m, sills at
   5.9/8.7/11.5/14.2/17.0/19.0 m *(derive these from the measured 2.77 m rhythm rather
   than copying them)*. On the Embarcadero end, five continuous horizontal glazing bands
   instead of a grid — that is what the 1983 face actually does.
7. Cast-stone band: replace the brick material on the last **8 m of depth** at the
   northeast end, all round, with `Toy_stone`, and round those four vertical arrises to a
   0.6 m radius (the real building's rounded corners).
8. Roof: membrane at 21.4 m; a 0.9 m-high monitor spine 2.2 m wide running the middle
   ~18 m of the depth; two or three condenser blocks; one dark skylight panel.
9. Penthouse: from 21.4 m, a **14.16 x 10.0 m** box in `Toy_stone` to 25.0 m, glazed on
   all four sides, capped with a shallow barrel (rise 2.7 m, crown at **27.7 m**) — the
   crown must be the tallest geometry in the file.

**Applied-band discipline** (memory of `sf3d-applied-band-ao-slot` and
`sf3d-applied-panel-recess-trap`): every proud band above must be *embedded* into the wall
it sits on, not floated in front of it, and the entry recess must be cut as an opening
rather than built as a solid prism in front of the door.

### 2.8 Materials and palette

Reuse existing palette values; do not invent new hexes. Precedents in brackets.

| Material | Hex | Where |
|---|---|---|
| `Toy_brick` | `c96f4a` [358-brannan] | the 1907 slab, both flanks, the parapet |
| `Toy_rust` | `a86444` [358-brannan] | recessed window reveals, entry recess sides |
| `Toy_stone` | `d9d2c2` [500-third] | the 1983 cast-stone band and the penthouse walls |
| `Toy_cream` | `f2ede3` [501-second] | the penthouse barrel roof |
| `Toy_slate` | `6f7883` [358-brannan] | the green-black cornice, string course and ground-floor band — the real colour is a very dark desaturated green; **do not use `Toy_roofd`** (memory: it renders rgb(9,9,12) in the app) |
| `Toy_glass` | `2a4d73` [500-third] | Steuart-end window glass |
| `Toy_glassl` | `6f95b8` [500-third] | Embarcadero-end glazing bands and the penthouse |
| `Toy_steel` | `9aa0a6` [500-third] | roof membrane, monitor spine, condensers |
| `Toy_ink` | `3a3530` [500-third] | shopfront mullions, the incised "131" |
| `Toy_glassl_Glow` | `6f95b8` | lit office windows and the penthouse lantern |
| `Toy_gold_Glow` | `caa64a` [501-second] | the two ground-floor entrances |

The `_Glow` day colours must match their non-glow neighbours exactly, and a `_Glow`
material's **base colour is its night look** (memory: `sf3d-glow-colour-is-unlit`) — pick
it for how it reads unlit in the app, not for how it renders under a Blender emission
strength. Do not build a closed glow shell (memory: `sf3d-glow-shell-day-alpha`).

### 2.9 Top surface

The camera looks down and this roof is 42 m long, so it must be designed:

- flat `Toy_steel` membrane at 21.4 m inside the parapet ring,
- the monitor spine as one clean chamfered ridge, not a row of boxes,
- condensers grouped, not scattered — two clusters, one at mid-depth and one against the
  penthouse,
- one dark skylight rectangle,
- the penthouse barrel as the visual terminus, its curve running **across** the width
  (ridge parallel to the long axis) so that from the aerial camera it reads as a rounded
  cap, not a gable.

### 2.10 Scope

In: the 131 building only, both ends, both flanks, cornice, parapet, roof, plant,
penthouse. Out: 141 Steuart, 121 Steuart, the Audiffred Building, streets, sidewalks,
trees, vehicles, people, the parklet, signage beyond one incised "131".

### 2.11 Triangle budget

| Element | Budget |
|---|---|
| Brick slab + bevels | 900 |
| Cornice ring + string course + ground band | 1,600 |
| Steuart windows (5 x 6, recessed) | 3,000 |
| Embarcadero glazing bands (5) | 1,100 |
| Entry recess + shopfronts | 900 |
| Cast-stone band + rounded arrises | 900 |
| Roof membrane, monitor, plant, skylight | 1,400 |
| Penthouse box + barrel cap | 1,400 |
| Glow duplicates | 600 |
| **Total** | **11,800** (cap 12,000) |

If it overruns, cut the Steuart window recess depth to a flat inset panel (saves ~1,200)
before touching the cornice or the penthouse.

### 2.12 Draft manifest entry

```json
{
  "id": "131-steuart",
  "file": "131-steuart.glb",
  "anchor": [-122.3924393, 37.7930564],
  "targetHeightM": 27.7,
  "cat": 3,
  "name": "Steuart Place (131 Steuart Street)",
  "estimated": false,
  "dims": [39.8, 39.8, 27.7],
  "tris": 11800,
  "loadRadius": 2500
}
```

`loadRadius` follows the default rule `max(2500, 27.7 x 30 = 831)` → **2500**. Not
`alwaysLoaded`: at 27.7 m this is not a skyline piece.

Append the entry as **text**, never by `JSON.parse` → `JSON.stringify` — the round trip
rewrites `11.0` to `11` across six other landmarks (memory:
`sf3d-manifest-text-append`).

### 2.13 Integration notes (for later, not this task)

**Case B — new landmark.** There is no `131Steuart` id in `pipeline/lib/landmarks.mjs` or
`app/src/landmarks.js`, so integration needs a registry entry and a tile re-bake in
addition to the manifest entry.

**Exclusion radius: `exclude: 8`.** Measured against the real bake inputs
(`pipeline/data/buildings_datasf.geojson` + `overture_buildings.geojsonseq`, replaying
`buildings.mjs`'s `simplifyRing` → `ringCentroid` → `excluded()` exactly) from this
anchor:

| `exclude` | Footprints dropped | Which |
|---|---|---|
| 1 m | 1 | the Overture ring only (centroid 0.08 m) — misses the DataSF ring |
| **2–13 m** | **2** | **correct: the Overture ring (0.08 m) and the DataSF ring (1.80 m), both tracing 131** |
| 14 m | 4 | starts eating **121 Steuart** (DataSF SF3715003 centroid 13.59 m + its Overture twin) |
| 16–25 m | 6 | also eats **141 Steuart** (DataSF SF3715025 area 513 m2, centroid 14.57 m) |
| 30 m | 10 | eats 111 and 155 as well — a crater through the row |

This is the two-rings case: **both** DataSF and Overture trace this building, so anything
below 2 m leaves a procedural block standing inside the asset. The window 2–13 m is wide
and 8 m sits in the middle of it. Note that the party-wall vertices are 19.5–22.2 m away
from the anchor even though the walls physically touch — the gate measures from the
**anchor**, not from the footprint edge (memory:
`sf3d-exclusion-gate-is-anchor-distance`), which is what makes a clean single-building
exclusion possible on a party-walled slot.

**141 Steuart stays procedural.** It shares the parcel but is a separate mass (two
classical storeys plus a curved glass box, DataSF `hgt_max` 21.82 m). Only one asset per
parcel can own the exclusion; this one owns it, and 141 keeps its baked block.

Registry entry sketch for `pipeline/lib/landmarks.mjs`:

```js
{
  id: '131Steuart',
  name: 'Steuart Place (131 Steuart Street)',
  lon: -122.3924393,
  lat: 37.7930564,
  exclude: 8,
}
```

**BATCH mode applies** if other landmarks are in flight: run the bake and the full
Step 5/6 QA on it, then `git checkout -- app/public/tiles api/_data` before committing,
and ship a source-only branch (`docs/asset-pipeline/ADDRESS-TO-ASSET.md`, "Batch mode").
Verify with `git diff --name-only origin/main` listing nothing under `app/public/tiles/`
or `api/_data/`.

**Watch the shared landmark BatchedMesh.** SoMa/Embarcadero is where it is fullest
(memory: `sf3d-landmark-batch-full`, `sf3d-batch-reserve-overflow`) — check the buffer
occupancy in the console merge line after adding this one, and do not blame a new asset
for a landmark that silently disappears somewhere else.

### 2.14 Validation checklist

- [ ] Re-import validation all-PASS; ≤ 12,000 triangles; no textures, transparency,
      cameras, lights, animations
- [ ] Tallest geometry lands at exactly 27.7 m; min Z ≈ 0; XY centre offset ≈ 0
- [ ] Materials all `Toy_*` from 2.8; `_Glow` day colours match their neighbours
- [ ] Axis-aligned bbox ≈ 39.8 x 39.8 m (expected at 45° heading, not a scale error)
- [ ] Steuart front faces 224.9°, Embarcadero front 44.8° — check on the top render
- [ ] Penthouse is at the **northeast** end, set back, and is the tallest thing
- [ ] Roof designed, not blank; barrel ridge runs parallel to the long axis
- [ ] Night render: penthouse lantern reads as the hero; entrances gold; office windows
      scattered, not uniform
- [ ] Both party-wall flanks are real surfaces, and the southeast flank above 18 m is
      finished brick

### 2.15 Open questions and risks

1. **Storey count conflict — resolved, but re-check.** CompStak says 6 stories;
   Transwestern, SKYDB and the Assessor say 7. Six window rows are countable above the
   ground floor on the rectified Steuart elevation, and the DataSF address file lists
   suites through `#700`. **7 is right**; CompStak is probably counting the leasable
   office floors above a retail ground floor.
2. **The photogrammetry was hard-won; treat the 21.8 m cornice as measured, not
   published.** The first pass disagreed with the LiDAR by 15% and the cause was two real
   traps worth knowing:
   - The 2013-era panorama `0F4-09tgUjGg6sPgyJ31Gg` has a **3584 x 1664** equirect, not
     4096 x 2048 — 0.1004°/px and a horizon at row 832. Assuming the modern geometry made
     every height ~10% low. Always measure the non-black extent of the stitched equirect
     before using it.
   - The panorama's **reported lat/lon is not reliable**. The camera was solved instead
     by least-squares fitting four known party-line corners (111/121, 121/131, 131/141,
     141/155) to their observed columns: RMS **0.9 px** (0.08°) and a perpendicular
     distance of **15.00 m** to the street wall. A sensitivity sweep confirms the solve is
     not degenerate despite the targets being collinear — forcing D to 15.5 m raises the
     RMS to 9.3 px, and to 16.0 m raises it to 18.1 px. D is good to ±0.4 m.

   The two independent solves (Steuart pano 1, D 15.00 m → cornice 21.8 m; Embarcadero
   pano, D 14.99 m → parapet 21.6 m) agree to 0.2 m, and the Embarcadero pano puts the
   penthouse crown at 27.5 m against a LiDAR maximum of 27.77 m.
3. **The penthouse's plan extent is inferred, not measured.** It is full-width on the
   Embarcadero elevation, and the LiDAR two-level solve puts roughly a quarter of the
   footprint on the upper level — hence ~10 m of the 42 m depth. The aerial imagery over
   this block leans badly enough that the roof outline cannot be registered to the
   footprint, so this number could be off by several metres. **Verify it from a
   non-leaning aerial or an oblique before committing to the massing.**
4. **The architect is unknown.** Eight searches across listing sites, permit aggregators
   and the local press turned up nothing. The 1983 renovation architect is likewise
   unattributed. Worth one pass at the SF Planning historic-resource files and the
   Article 11 downtown conservation-district inventory — this row (Audiffred, Hotel
   Griffon, Harbor Court, YMCA) is dense with rated buildings and 131 is very likely a
   contributor.
5. **`roof:shape=gabled` on OSM is wrong** and should not be re-inherited. Consider
   fixing it upstream in OSM after the asset ships.
6. **131 and 141 share a parcel and share nothing else.** Every square-foot figure you
   will find online (68,400 / 75,000 / 79,800) covers both. Do not divide any of them by
   7 to sanity-check a floor plate.
7. **The Embarcadero face may date the model.** The 1983 re-clad is what is there now, in
   panoramas through 2025. If a future renovation restores a brick waterfront elevation,
   this asset's northeast end is the part that goes stale first.
