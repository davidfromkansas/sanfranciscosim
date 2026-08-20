# 252–254 Ritch Street — SF-SIM asset plan

A 1915 two-flat on Ritch Street, one of the SoMa alleys south of Bryant. It is 7.6 m
wide, two storeys over a raised base, and the whole thing — walls, bay, cornice, doors,
stoop, base — is painted **one dark warm gray**. On a block of cream and beige neighbours
that single decision is the entire identity of the building: from the app's aerial camera
252–254 Ritch is *the dark house in the row*.

It is the first plan in this set for a **Ritch Street** building and the first for the
*exposed-flank alley flat* type: a party wall on one side, an open surface parking lot on
the other, so three of its four elevations are actually visible. The design brief is "the
darkest small building on the block, with a designed roof", not "landmark".

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/254-ritch/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `254-ritch` |
| Existing procedural builder | none — new landmark (Case B: needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor (manifest, placement) | `-122.3956361, 37.7801244` |
| WGS84 anchor (registry, exclusion only) | `-122.3956361, 37.7801244` — **the same point**, see 2.13 |
| Target height | **8.8 m** to the roof flue cap (LiDAR maximum, measured); cornice crest 8.05 m, roof deck 7.95 m |
| Footprint | 7.60 m frontage × 14.2 m deep, 108 m²; parcel width, LiDAR depth |
| Axis | lot axis 45.05°/135.05°; front facade faces **45.05°** (north-east, onto Ritch Street) |
| Triangle cap | 7,000 |
| Category | `1` (house) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 252–254 Ritch Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the two-flat at 252–254 Ritch Street,
San Francisco, and deliver it as a downloadable, validated GLB.

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
7. `artifacts/165-south-park/` — the closest reference implementation in scale, budget
   and type (narrow two-storey wooden flats, low triangle count, restrained night state)
8. `docs/asset-plans/254-ritch.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- **The colour.** The building is uniformly dark warm gray — siding, trim, cornice,
  bay, doors, base and stoop all the same value (measured `#6b696a` in overcast light).
  Its neighbour at 248–250 is cream. That contrast is the recognition cue and it must
  survive at thumbnail size. A modeller who paints this building light gray has failed.
- The **two-storey canted bay window** filling the south-east 3.7 m of the 7.6 m
  frontage: three sashes per storey (narrow angled cheek, wide centre, narrow cheek),
  projecting ~0.6 m, carried on a flared skirt over the base.
- The **recessed twin-door entry** in the remaining north-west 2.3 m, under a small
  bracketed hood, reached by a straight stoop of six steps projecting toward the street.
  Two doors, not one — this is a duplex and both numbers are on the same recess.
- The **bracketed cornice**: a dentil course under small modillion blocks, running the
  full frontage and returning over the bay. It is the only ornament on the building and
  the brightest edge it has from above.
- The **designed flat roof**, which is what the app's camera actually sees: a pale
  membrane much lighter than the walls, **two light-well shafts** (one against the
  north-west party wall, one notched into the south-east flank), a small mechanical
  cluster mid-roof, and a vent flue that is the tallest thing on the building.
- The **exposed south-east flank.** 252–254 is not a party-wall building on both sides:
  a surface parking lot occupies the lot to the south-east and that whole elevation is
  visible from the street and from the air. Build it as a real elevation, blind but real.

## Research 252–254 Ritch Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The north-east (street) elevation — the bay, the entry recess, the stoop, the cornice
- The **roof from directly above**: the two light wells, the mechanical cluster, and
  which rooftop object is actually the tallest. This decides the target height.
- The south-east flank, fully exposed to the parking lot
- The south-west (rear) elevation and the rear yard
- The north-west party wall against 248–250 Ritch (blind, but its line matters)
- Day and night appearance

Prefer DataSF datasets, SF Planning records, assessor data, geolocated photography and
aerial imagery. Never rely on a single photograph, a single AI-generated image, or a
single unsourced 3D model. Separate verified facts from visual inference; if sources
disagree, document the disagreement and decide.

**Three source problems are already known and resolved in 2.1–2.3 and 2.15 — re-check
them, do not silently re-inherit the wrong value:**

1. **The address 254 does not have its own building.** DataSF resolves 252 and 254 to
   the same point and the same parcel, `3776106`, whose address range is literally
   `252`–`254`. OSM tags the single way `147508935` as `addr:housenumber=252;254`.
   One asset owns both numbers and both doors. Do not model half a building.
2. **The building footprints are offset ~1.2 m along the street from the surveyed
   parcels**, consistently in both DataSF and Overture, and OSM/Overture is offset a
   further ~1.1 m along and ~1.7 m back from the street on top of that. The plan places
   the asset in the **DataSF frame**, not the parcel frame, so that it sits flush against
   its baked neighbour rather than 1.2 m proud of it. See 2.3 — this is a deliberate
   decision and the reasoning must survive into `REPORT.md`.
3. **`hgt_maxcm` is 8.81 m and `hgt_median_m` is 8.04 m, and both are used.** The median
   is the roof deck of a genuinely flat roof and is trustworthy; the 0.77 m above it is a
   rooftop object, and the model's tallest geometry must reach 8.80 m so the loader's
   scale lands at 1.0. If your aerial research shows the tallest object belongs to the
   *neighbour's* roof, say so and re-derive the target rather than clipping it.

## Create a reference dossier

Write `artifacts/254-ritch/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3–5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. A contact sheet of
attributed reference thumbnails is welcome if legally permissible — do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

This is a **background building** in the style bible's detail budget (§21). Clear
massing, one facade rhythm, a designed roof, and exactly two identity cues carried hard:
the dark monochrome and the bay. Resist adding ornament beyond the cornice.

The finished asset must be immediately recognizable as this building, consistent with the
real one from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and never
accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building: the two-storey volume on the measured footprint, the base
band, the canted bay, the entry recess with its two doors and hood, the stoop, the
cornice, the flat roof with its two light wells and its mechanical cluster, and the rear
elevation.

Do not include unrelated surrounding city geometry: 248–250 Ritch Street, the surface
parking lot to the south-east, the rear yard and its trees, the street, the sidewalk, the
overhead wires, the landscape boulders at the base, the utility cabinet and gas meters,
parked cars, people, plinths, cameras or lights. Temporary context may appear in review
renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; at most
7,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The street facade faces
**45.05°** and the lot runs back at 225.05°. Build directly on the measured polygon in 2.3
rather than modelling an axis-aligned box and rotating it. Record the measured heading in
`REPORT.md`.

**Height normalization:** the tallest geometry in the export (the roof flue cap) must land
at exactly **8.80 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/254-ritch/build_254_ritch.py` (deterministic build script),
`artifacts/254-ritch/254-ritch.blend`, and `artifacts/254-ritch/254-ritch.glb`. The
script must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`254-ritch-top.png`, `-north.png`, `-east.png`, `-south.png`, `-west.png`, plus
`254-ritch-contact-sheet.png`, at least one high three-quarter aerial beauty
render `254-ritch-aerial.png`, and a night render `254-ritch-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the roof plane, the cornice, both light wells and the
mechanical cluster; the aerial view uses the style bible's camera assumptions (30–50
degrees down, long lens). Simple tabletop lighting, neutral warm background, minimal depth
of field, and every image must depict the same exported model.

Because the building sits at 45° to the compass, none of the four cardinal elevations is a
flat-on view of a facade. Render them anyway for comparability, and add a fifth
`254-ritch-frontal.png` looking down the true facade normal (from 45.05°) so the bay and
the entry can be judged without foreshortening.

**Night renders:** drive `_Glow` from Base Color, not from the imported emission — see the
note at the end of `docs/asset-plans/README.md`. A re-imported `_Glow` material carries a
default white emission and will render every glow surface as a white slab otherwise.

## Validate the exported GLB

Re-import `254-ritch.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/254-ritch/validation.json` and
`artifacts/254-ritch/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **15.8 × 15.8 m** even though
the building is 7.6 × 14.2 m — that is the expected consequence of the 45° real-world
heading, not a scale error. The XY centre will sit a few decimetres north-east of the
origin because the stoop and the bay project toward the street; keep it inside ±1 m.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "254-ritch",
  "file": "254-ritch.glb",
  "anchor": [
    -122.3956361,
    37.7801244
  ],
  "targetHeightM": 8.8,
  "cat": 1,
  "name": "252–254 Ritch Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`"estimated": false` is deliberate — 8.80 m is the DataSF LiDAR maximum over this
building's own footprint cells, a measurement rather than a derived crest. See 2.15.

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/254-ritch.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 252 and 254 Ritch Street, San Francisco CA 94107 | DataSF address dataset `ramy-di5m`: both numbers resolve to the same coordinate, `-122.3956577, 37.7800922` |
| Parcel | `3776106` (block 3776, lot 106), `from_address_num` 252, `to_address_num` 254, zoning `SLI` | DataSF parcels `acdm-wktn` — **this is the authoritative confirmation that 252 and 254 are one property** |
| Build year | **1915** | SF assessor roll `wv5m-vpq2`, block 3776 lot 106, closed roll years 2023–2025 (identical) |
| Storeys | **2** | assessor record; corroborated by every photograph |
| Units | **2** (9 rooms) | assessor record, "Flats & Duplex", Multi-Family Residential |
| Gross floor area | 2,100 sq ft (195 m²) | assessor record — see 2.15, it does not reconcile with the footprint |
| Lot | 181.7 m² measured (assessor says 1,875 sq ft = 174 m²); 7.60 m frontage, 23.91 m deep | DataSF parcel polygon — **measured** |
| Built footprint | ~108 m², 7.60 × 14.2 m | parcel width + LiDAR depth; see 2.3 — **derived** |
| LiDAR building | `201006.0125003`, 102.9 m² raw / 104 m² after the bake's 0.6 m simplify | DataSF Building Footprints `ynuv-fyni` — **measured, but offset, see 2.3** |
| Ground | 18.50 m NAVD88 (`p2010_zminn88ft` 18.4981) | same |
| Roof deck | **8.04 m** above grade (`hgt_median_m`), σ 1.18 m | same — **measured**; a flat roof, so median ≈ deck |
| LiDAR maximum | **8.81 m** above grade (`hgt_maxcm` 881) | same — **measured**; the rooftop flue/vent cluster |
| LiDAR minimum | 2.13 m (`hgt_mincm` 213) | same — the light-well shafts cutting into the roof plane |
| OSM height tag | 8 m (`source=Bing`) | OSM way `147508935` — independent corroboration of the deck |
| Photogrammetric check | 7.8 m sidewalk → roof edge | measured off the straight-on listing elevation using the 7.60 m frontage as the scale bar — corroborates 8.04 m to within 3% |
| Facade colour | `#6b696a` overcast / `#5e5652` in shade | median-sampled from the listing photography |
| Roof membrane colour | `#cac8c9` overcast / `#c3bdb8` sunlit | same |
| Sale | listed $995,000 Oct 2025, sold $1,250,000 Oct 2025, 2 × 1BD/1BA, upper unit vacant | Compass / Allison Chapleau listing and offering memorandum |
| Owner (pre-sale) | Ritch Street LLC; prior sale 1996-05-20 | Augrented (assessor-derived) |
| Neighbours | 248–250 Ritch (parcel `3776105`, party wall, north-west, cream) and a surface parking lot (parcel `3776149`, south-east) | DataSF parcels + photography |
| Neighbourhood | South of Market / South Beach; Ritch Street is a 200-block alley running Bryant → Brannan | DataSF street centrelines `3psu-pn9h`, `street=RITCH` |

### 2.2 Sources

- DataSF `acdm-wktn` (Parcels), `blklot=3776106` — the surveyed lot polygon, the
  252→254 address range, and the SLI zoning. This is the geometric backbone of the plan.
- DataSF `acdm-wktn`, `blklot=3776105` — 248–250 Ritch, used to establish that the
  ~1.2 m footprint offset in 2.3 is systematic rather than a fault in our own polygon.
- DataSF `ramy-di5m` (Addresses with Units), `street_name=RITCH`, numbers 240–280 — the
  mapping of 252 and 254 to one point, and of 246 to an 40-unit condo two doors along.
- DataSF `wv5m-vpq2` (Assessor Historical Secured Property Tax Rolls), block 3776 lot 106
  — build year, storeys, units, rooms, use class, lot and property area.
- DataSF `ynuv-fyni` (Building Footprints, LiDAR-derived), building `201006.0125003` —
  footprint, ground elevation, and the height statistics used for the roof deck and the
  target height.
- DataSF `3psu-pn9h` (Street Centerlines), `street=RITCH`, the Bryant→Brannan block
  (`lf_fadd` 201, `rt_fadd` 200) — the 135.05° street bearing that fixes the facade normal.
- https://www.openstreetmap.org/way/147508935 — `addr:housenumber=252;254`,
  `height=8`, `source=Bing`. Used for the height corroboration and, via Overture, as one
  of the two rings the exclusion has to consume. **Not** used for placement; see 2.3.
- Overture Maps buildings (the copy in `pipeline/data/overture_buildings.geojsonseq`,
  as downloaded 2026-08-13) — the ring at the site is byte-for-byte the OSM way: 100.0 m²,
  `height` 8.0.
- Exa search, `254 Ritch Street San Francisco building` (10 results, highlights on
  "facade elevation photo") — returned the Compass listing, the Augrented property record,
  the Allison Chapleau sale page and the offering-memorandum PDF. It also returned
  several stale directory listings for a recording studio ("Studio 254", "The Studio",
  254 Ritch St) — see 2.15.
- https://cdn.prod.website-files.com/5b2d7567fd7a4dceac9fedab/68e132514af690b8995e2517_252-254%20Ritch%20St%20-%20OM.pdf
  — the offering memorandum, *observed (listing photo)*. Five exterior frames, and the
  best reference material this dossier has: a near-orthographic straight-on street
  elevation, a high three-quarter aerial over the front, an oblique that reads the whole
  roof plane, a wide aerial showing the exposed south-east flank against the parking lot,
  and **a true top-down drone frame of the roof**. Photography credited to Elite Studios LLC.
- https://augrented.com/sf/3776106-252-254-ritch-st — assessor-derived build year,
  storeys, units, area, ownership and sale history.
- https://www.compass.com/homedetails/252-254-Ritch-St-San-Francisco-CA-94107/1ZXOX5_pid/
  and https://www.allisonchapleau.com/listing/252-254-ritch-street — price, unit mix,
  "Large Basement With Additional Storage & Bonus Bath", "Well-Maintained Building".

### 2.3 Orientation and placement

Ritch Street's Bryant→Brannan block runs **135.05°**. The lot is a standard 25 × 78 ft
SoMa alley lot laid orthogonally on it, so the street facade faces **45.05°** —
north-east — and the lot runs back at 225.05°. Nothing about the site is curved or
skewed; the only geometric question is *where along the street* the building sits, and
the three available sources disagree.

Measured in the lot's own frame (origin at the parcel's north-west front corner, *along*
positive toward Brannan/south-east, *setback* positive away from the street):

| Source | along | setback | Verdict |
|---|---|---|---|
| Parcel `3776106` (ours) | −0.12 … 7.60 | 0.00 … 23.92 | **authoritative for width and heading** |
| Parcel `3776105` (248–250) | −7.72 … 0.00 | 0.00 … 23.91 | the party line is exactly at along 0 |
| DataSF footprint `201006.0125003` (ours) | −1.28 … 6.70 | 0.64 … 15.23 | **authoritative for depth and for position** |
| DataSF footprint `201006.0040021` (248–250) | −8.93 … −1.21 | 0.54 … 24.35 | the same −1.2 m offset — so it is systematic |
| OSM/Overture `147508935` | −2.33 … 5.57 | 2.74 … 16.55 | **rejected for placement** — a Bing trace, offset a further ~1.1 m along and ~1.7 m back |

The two DataSF footprints share a party line at along ≈ −1.24 while the two parcels share
one at along 0. Both footprints are therefore shifted ~1.2 m north-west of the survey, in
step with each other. This is a registration offset in the footprint layer, not a defect
in either polygon.

**The asset is placed in the DataSF frame, not the parcel frame, and that is deliberate.**
Everything this building will stand next to in the app is baked out of exactly those
footprints — 248–250 Ritch included, and it is *not* excluded. Anchoring on the surveyed
parcel would be 1.2 m more correct in absolute terms and would open a 1.2 m slot between
this asset's party wall and its neighbour's, which is the one error the aerial camera
would actually see. AGENTS rule 5 forbids moving real features for convenience; sitting
flush with the row is not convenience, it is the same registration every neighbour uses.
Record the trade-off in `REPORT.md`.

The design footprint is therefore a rectangle of the **parcel's** width on the **footprint
layer's** position and depth:

- width **7.60 m**, along −1.24 … 6.36
- depth **14.2 m**, setback 1.00 … 15.20 (the LiDAR's 0.64 m front extent is read as the
  cornice overhang, so the wall plane sits at 1.00)
- area **108 m²**, with a ~8.7 m rear yard behind it

Anchor (both manifest and registry): **`-122.3956361, 37.7801244`**, the centre of that
rectangle. It falls 0.09 m from the DataSF footprint's own area centroid, which is why one
point can serve both jobs here (contrast 165 South Park, where they had to differ).

Design polygon, in Blender coordinates (metres, `+X` east, `+Y` north), already centred on
the anchor:

```
NW front   (  2.340,   7.705)
SE front   (  7.709,   2.327)
SE rear    ( -2.340,  -7.705)
NW rear    ( -7.709,  -2.327)
```

Because of the 45° heading the axis-aligned bounding box is ~15.8 × 15.8 m for a 7.6 ×
14.2 m building. That is correct and is not a scale error.

**Heights**, all above the sidewalk at the front (grade 0). The three facade-plane
readings marked ✓ were taken off the straight-on listing elevation with the 7.60 m
frontage as the scale bar and agree with the design section to within 5 cm, which is why
this section is unusually confident for an *inferred* storey breakdown:

| Level | z | Confidence |
|---|---|---|
| Top of base band / porch floor | 1.35 | *inferred* |
| Ground-floor window sill (bay) | 2.05 | *inferred* |
| Ground-floor window head (bay) | 3.75 | *inferred* |
| Entry hood crest / floor line | 4.30 | ✓ measured 4.27 |
| Upper window sill | 5.15 | ✓ measured 5.14 |
| Upper window head | 6.85 | ✓ measured 6.89 |
| Top of wall (cornice springing) | 7.45 | *inferred* |
| Roof deck | 7.95 | LiDAR median 8.04 |
| Cornice crest | 8.05 | *inferred*; photogrammetric roof edge 7.82 |
| Light-well curb | 8.20 | *inferred* |
| Condenser stand | 8.50 | *inferred* |
| **Roof flue cap — tallest geometry** | **8.80** | LiDAR maximum 8.81 |

### 2.4 What each side shows

**North-east (street elevation, 7.60 m).** Two storeys of horizontal lap siding over a
dark base band, everything one dark warm gray. The south-east 3.7 m is a two-storey canted
bay projecting ~0.6 m: three double-hung sashes per storey — a narrow one on each 45°
cheek and a wide one on the centre face — with a small cornice over the upper bay and a
flared skirt where the lower bay meets the base. The north-west 2.3 m carries a single
double-hung window upstairs and, at ground level, a deep entry recess holding **two**
adjacent part-glazed doors (254 to the south-east, 252 to the north-west), the house
numbers painted on the reveals either side. A small bracketed hood with its own dentil
course caps the recess at the floor line. A straight flight of six steps with a solid
cheek wall on its south-east side climbs from the sidewalk into the recess, projecting
~1.8 m past the wall plane. Above everything, the main cornice: a dentil course under
widely spaced modillion blocks, projecting ~0.35 m, returning over the bay.

**South-east (flank, 14.2 m — exposed).** The lot next door is a surface parking lot, so
this whole elevation is public. It is blind: flat siding, one downpipe, and a rectangular
notch about 3.0 m long and 1.3 m deep cut into it 4.2–7.8 m back from the front wall,
where the south-east light well opens. Nothing else. Its value in the model is that it is
*there*: the building reads as a free-standing object on this side, which almost nothing
else on the block does.

**North-west (party wall, 14.2 m).** Blind against 248–250 Ritch, which is a two-storey
cream building of about the same height with its own bay. Never visible. Build it as a
flat plane, and keep it exactly on the design polygon so the two roofs abut cleanly.

**South-west (rear).** Faces the rear yard, visible only from the air. Expect the plain
treatment of the type — siding, a rear door, a window or two, an exterior stair down to
the yard. Unverified; keep it simple and consistent.

**Top.** This is the surface the app's camera actually sees and it is a genuinely good
roof. A flat pale membrane, clearly lighter in value than the walls, bounded on the street
side by the bright cornice band with the bay's chamfer notched into it. Two rectangular
light wells cut through it: one **1.1 m (deep) × 2.1 m (wide)** hard against the north-west
party wall, 7.0–8.1 m back from the front; one **3.6 m (deep) × 1.4 m (wide)** notched
into the south-east flank, 4.2–7.8 m back. Between them, mid-roof and about 3.8 m from the
north-west edge, a small mechanical cluster: a mini-split condenser on a low stand, one
mushroom vent and a small equipment box. Near the north-west party wall about 9 m back
stands the flue with a rain cap that is the tallest object on the building.

### 2.5 Recognition cues (ranked)

1. **The monochrome dark gray**, against a block of cream neighbours. From the aerial
   camera this is the building. Everything else is secondary.
2. **The two-storey canted bay** on the south-east half of a 7.6 m frontage — the bay is
   half the building's width, which is what makes the entry side read as narrow.
3. **The exposed south-east flank** with the parking lot beside it: a small building
   standing free where the rest of the row is welded together.
4. **The pale roof against the dark walls**, and the two dark light-well rectangles
   punched through it. The value inversion — light roof, dark building — is unusual on the
   block and reads instantly from directly overhead.
5. **The bracketed cornice**, the one piece of ornament, catching light along the street
   edge.

### 2.6 Miniature translation

**Preserve**

- The 7.60 × 14.2 m footprint, the 45.05° facade heading, and the party line on the
  north-west edge exactly
- The dark monochrome across every surface except the roof, the glazing and the recesses
- The bay's share of the frontage (3.7 of 7.6 m) and its 0.6 m projection
- Two doors in the entry recess, not one
- Both light wells, at their measured sizes and positions — they are the roof's design
- The value inversion between the pale roof and the dark walls

**Simplify / exaggerate**

- Individual clapboards become flat colour; horizontality is carried by one shallow
  shadow groove at the floor line, not by modelled boards
- The dentil course and modillions become a single stepped cornice profile with a
  suggestion of blocks — three chunky steps, no individual dentils. At 8 m tall on a
  120 m camera the dentil course is sub-pixel; the *projection* is what reads.
- Windows become recessed rectangles (0.12 m) with a 0.08 m proud sill and surround.
  Three sashes per bay storey, one on the north-west upper wall: eight openings total.
- The stoop becomes six clean treads plus a solid cheek wall; no railing, no handrail
- The flue is exaggerated to a chunky 0.35 m cylinder with a proud cap so it survives at
  thumbnail size and so the height normalization does not rest on a hairline object
- The base band is thickened to a clean 1.35 m with a 0.06 m proud edge
- Overhead wires, the utility cabinet, the gas meters, the landscape boulders, the
  downpipe and the satellite dish all disappear
- The rear yard is not modelled — the asset stops at the rear wall

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Main volume: extrude the 2.3 polygon from z=0 to z=7.45, `Toy_slate`.
2. Base band: the same polygon's north-east, south-east and south-west edges inset and
   re-extruded z=0 to z=1.35, 0.06 m proud, `Toy_slate` (same colour, read by the shadow
   of its own edge — the real building does not change colour here).
3. Bay: a canted prism on the street facade, 3.70 m of frontage starting 0.59 m in from
   the south-east corner, projecting 0.60 m with 45° cheeks 0.85 m wide, from z=1.35 to
   z=7.45, `Toy_slate`. Flare its bottom 0.25 m into the base band.
4. Bay cornice: a 0.25 m band around the bay head at z=7.20…7.45, 0.10 m proud, `Toy_slate`.
5. Main cornice: from z=7.45 to **z=8.05**, projecting 0.35 m, as three stepped faces
   (a plain fascia, a set-back block course, a crowning fillet), running the full street
   elevation and returning 0.4 m down each flank and around the bay, `Toy_slate`.
6. Roof plane: flat cap at z=7.95, `Toy_stone`.
7. Bay windows: six openings, 3 per storey — cheeks 0.55 × 1.70 m, centre 1.40 × 1.70 m —
   sills at z=2.05 and z=5.15, recessed 0.12 m, `Toy_glass`, each with a 0.08 m proud
   `Toy_slate` sill and surround.
8. North-west upper window: one 1.05 × 1.70 m opening, sill z=5.15, same treatment.
9. Entry recess: a 2.28 m wide × 1.20 m deep void from z=1.35 to z=3.95 in the north-west
   part of the frontage, lined `Toy_ink`, holding two 1.00 × 2.15 m door slabs in
   `Toy_slate` with a single recessed `Toy_glass` light in the upper half of each.
10. Entry hood: a 0.35 m band over the recess from z=3.95 to z=4.30, 0.20 m proud,
    `Toy_slate`.
11. Stoop: six 0.30 m risers × 0.30 m treads climbing from grade to z=1.35, 1.60 m wide,
    projecting 1.80 m from the wall plane, with a 0.20 m solid cheek wall on the
    south-east side only. `Toy_slate`.
12. Floor-line groove: a 0.04 m shadow groove around the street elevation and the exposed
    south-east flank at z=4.30.
13. Light well A (party side): a 1.10 × 2.10 m hole through the roof plane at the
    north-west edge, 7.0–8.1 m back from the front wall, sunk 3.0 m, lined `Toy_ink`,
    with a 0.25 m curb rising to z=8.20 in `Toy_stone`.
14. Light well B (flank side): a 3.60 × 1.40 m notch cut into the south-east flank,
    4.2–7.8 m back from the front wall, from the roof down 3.0 m, lined `Toy_ink`, curbed
    to z=8.20 on its three roof edges.
15. Mechanical cluster, mid-roof, ~7.0 m back and ~3.8 m from the north-west edge: a
    0.85 × 0.35 × 0.55 m condenser on a 0.20 m stand topping out at z=8.50 (`Toy_steel`),
    one 0.18 m mushroom vent, and a 0.40 × 0.30 × 0.25 m equipment box (`Toy_steel`).
16. Roof flue: a 0.35 m diameter cylinder at the north-west edge ~9.0 m back, rising from
    the roof to a proud cap whose top is exactly **z=8.80**, `Toy_steel`. **This is the
    tallest geometry in the export and it sets the height normalization.**
17. Rear elevation: one 1.00 × 2.15 m recessed door and two 0.90 × 1.50 m recessed
    windows, `Toy_ink` / `Toy_glass`.
18. Bevel 0.10 m, 2 segments.

### 2.8 Materials and palette

Flat colors only. One entry is deliberately off-palette; see the note below.

| Material | Hex | Used for |
|---|---|---|
| `Toy_slate` | `#756f69` | **everything painted** — siding, base band, bay, cornices, doors, stoop, window surrounds, all four elevations. Off-palette; see below. |
| `Toy_stone` | `#d9d2c2` | the roof membrane and the light-well curbs |
| `Toy_ink` | `#3a3530` | entry recess lining, light-well shafts, rear door reveal |
| `Toy_glass` | `#2a4d73` | all glazing |
| `Toy_steel` | `#9aa0a6` | the roof flue, the condenser, the vent and the equipment box |
| `Toy_gold_Glow` | `#caa64a` | the three upper bay sashes, lit at night |
| `Toy_trim_Glow` | `#f6e6c4` | a thin warm spill panel in the entry recess |

**On `Toy_slate`.** The measured facade is `#6b696a` in overcast light and `#5e5652` in
shade — a neutral-to-warm mid-dark gray. No palette entry is close: `Toy_steel` (`#9aa0a6`)
is far too light and would destroy the one cue this building has, and `Toy_roofd`
(`#45454a`) and `Toy_ink` (`#3a3530`) are traps — `Toy_roofd` has already been observed
rendering as `rgb(9,9,12)`, effectively black, on a roof deck in this app. The style
bible's SF exception (painted residential rows keep their tinted facades) sanctions the
deviation, so `#756f69` — the measured colour lifted about 8% so it survives the app's
Lambert shading — ships as a WARN, not a FAIL. **If the aerial render still reads black or
muddy, lift toward `#857e76`; never go darker.** Justify whichever you pick in `REPORT.md`.

**On the roof.** `Toy_stone` is lighter than the walls, which is exactly the real
relationship and is also what makes the outline read from directly overhead. Do not
"correct" it to a dark roof colour because roofs are usually dark.

**Night state (required).** Glow surfaces must be thin single-sided shells proud of the
opaque glazing — never a closed box. The app draws `_Glow` as a separate layer at ~12%
alpha per surface, so a closed shell stacks two layers and reads at ~23% in daylight,
tinting the whole facade. Hero glow: the **three upper bay sashes**, warm. Supporting
accent: a thin warm spill panel inside the entry recess, which is what tells the eye at
night that the recess is a doorway and not a painted panel. The **single north-west upper
window stays dark** — the upper unit was vacant at sale, the lower one occupied, and a
fully lit two-flat reads as an office. The roof, the flue and the light wells do not glow.

### 2.9 Top surface

A 7.6 × 14.2 m pale rectangle with a bright cornice band along its street edge, a chamfer
notched into that band where the bay meets it, and two dark rectangles punched through it.
Its quality comes from four things and nothing else: the value inversion against the dark
walls, the crispness of the cornice band, the two light wells reading as real holes rather
than painted patches, and the small mechanical cluster giving the middle of the roof one
place for the eye to land. Do not add invented rooftop clutter — the two wells and the
cluster are all real, and the emptiness around them is accurate.

### 2.10 Scope

**In the GLB:** the single building — the two-storey volume on the measured footprint, the
base band, the canted bay, the entry recess with both doors and its hood, the stoop, the
cornices, the flat roof with both light wells, the mechanical cluster and the flue, the
window openings on all elevations, and the rear door

**Not in the GLB:** 248–250 Ritch Street, the surface parking lot, the rear yard and its
trees, the street, the sidewalk, overhead wires and poles, the landscape boulders, the
utility cabinet, the gas meters, the downpipe, the satellite dish, vehicles, people,
plinths, cameras or lights

### 2.11 Triangle budget

Cap 7,000 — a background building, and the cap should bind. Suggested split: main volume
and base ~600, bay ~600, cornices ~900, roof plane ~200, eight window bays with trim
~1,900, entry recess and two doors ~600, hood ~200, stoop ~400, two light wells with
curbs ~700, mechanical cluster and flue ~500, rear openings ~300, bevel overhead ~1,000.
If the first build lands above 7,000 the answer is fewer window subdivisions and a coarser
flue cylinder, not a raised cap.

### 2.12 Draft manifest entry

```json
{
  "id": "254-ritch",
  "file": "254-ritch.glb",
  "anchor": [
    -122.3956361,
    37.7801244
  ],
  "targetHeightM": 8.8,
  "cat": 1,
  "name": "252–254 Ritch Street",
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

- **Case B — new landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '254Ritch'`)
  and re-bake the affected tiles, or the baked procedural building will intersect the GLB.
  The procedural block here is baked from `hgt_median_m` and `hgt_maxcm` averaged
  (`datasfHeight` in `pipeline/buildings.mjs`), so it stands at (8.04 + 8.81)/2 ≈ 8.4 m —
  taller than the asset's cornice. An unbaked local check will therefore show nothing
  wrong while the asset is in fact buried. Run the bake before judging it.

- **The manifest anchor and the registry `lon`/`lat` are the same point**, unusually.
  `placeGeneric` positions the GLB from the **manifest** `anchor`; `pipeline/lib/landmarks.mjs`
  `lon`/`lat` is only the centre of the bake-time exclusion circle. Here the design
  footprint's centre and the DataSF footprint's area centroid fall 0.09 m apart, so one
  value serves both. Use `-122.3956361, 37.7801244` for each.

- **Exclusion radius: `exclude: 2.9`.** `excluded()` in `pipeline/buildings.mjs` drops a
  footprint when its centroid **or any ring vertex** falls inside the circle. Measured
  from the anchor above against the **real bake input** (`pipeline/data/buildings_datasf.geojson`
  and `pipeline/data/overture_buildings.geojsonseq`, each ring first simplified at the
  bake's own 0.6 m tolerance):

  | Polygon | Triggers at | Source |
  |---|---|---|
  | this building | **0.09 m** (its own centroid) | DataSF `201006.0125003`, 104 m² |
  | this building | **1.95 m** (centroid) | Overture — the OSM way, 100 m² |
  | 248–250 Ritch | **3.82 m** (nearest vertex) | DataSF `201006.0040021`, 167 m² |
  | 248–250 Ritch | 5.08 m (nearest vertex) | Overture, 101 m² |

  So the radius must be **greater than 1.95 m** and **less than 3.82 m**. `2.9` sits
  0.95 m above the floor and 0.92 m below the ceiling — a 1.87 m window, comfortable by
  the standards of this registry.

- **Two rings, not one.** DataSF and Overture both trace this building and the two
  polygons are 1.9 m apart, so a radius chosen to clear only the DataSF ring would leave
  the Overture gap-fill standing on top of the asset. `2.9` consumes both. After the bake,
  confirm with `pipeline/verify-rebake.mjs` — and note that `verify-rebake` compares
  per-cell building *counts*, which can read "dropped nothing" when one exclusion removes
  a DataSF ring and the Overture pass declines to re-add. Settle it from the tile bytes if
  the count looks wrong.

- **Do not set `clearTrees: true`.** At 2.9 m the radius is inside the building's own
  footprint; there is no street tree in front of 252–254 and the parking lot next door has
  no furniture to clear.

- `loadRadius`: the default formula gives `max(2500, 8.8 × 30) = 2500` m. Take the default.

- Camera preset: the only designed elevations are the street front and the exposed
  south-east flank, and both are visible from over Ritch Street. App yaw = 180 − true
  bearing, so a facade normal of 45.05° gives **yaw 135** — camera to the north-east,
  out over the alley, looking back at the front and catching the flank in three-quarter.
  `camera: { distance: 120, yaw: 135, pitch: 26 }` as a starting point, tuned against the
  live scene. `camera` is mandatory even without a number `key`.

- **Manifest edit: append as text.** Do not round-trip
  `app/public/sf-assets/landmarks_manifest.json` through `JSON.stringify` — it rewrites
  values like `11.0` to `11` across unrelated landmarks and produces a diff that is not
  yours.

- **This is the fourth non-monument small residential building in the manifest and the
  case for the kit route keeps getting stronger.** 380 Brannan raised it, 1008 General
  Kennedy sharpened it, 165–167 South Park argued it explicitly. A 7.6 m alley flat with a
  canted bay is the single most repeated object in San Francisco; if Ritch Street or the
  Bryant/Brannan alleys are going to be built out, build the *alley flat* as a kit piece
  with a tintable body and place forty of it. This one earns a bespoke asset only because
  its exposed flank and its monochrome make it legible as an individual, and because it is
  a useful pilot for the type.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m (the stoop and bay push it
      north-east; that is expected)
- [ ] Bounding-box top exactly 8.80 m, set by the roof flue cap (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~15.8 × 15.8 m is expected)
- [ ] Frontage 7.60 m and depth 14.2 m, not rounded toward a square plan
- [ ] The bay occupies the south-east half of the frontage and the entry the north-west —
      not mirrored
- [ ] Two doors in the entry recess
- [ ] Both light wells present, at their measured sizes, reading as holes not panels
- [ ] The roof is lighter in value than the walls
- [ ] Triangles at or under 7,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`; the one
      off-palette value (`Toy_slate`) justified in `REPORT.md`
- [ ] `_Glow` only on the three upper bay sashes and the entry spill; glow shells thin,
      single-sided and proud of the opaque glazing
- [ ] The north-west upper window does **not** glow
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume
      for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + the frontal view + contact sheet + night render, all
      regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The tallest rooftop object is identified by measurement but not by name.** DataSF's
  `hgt_maxcm` of 8.81 m is computed over this footprint's own 50 cm cells, so something on
  *this* roof reaches 8.81 m — the number is safe even though the object is not certain.
  The oblique listing frame shows a capped flue and a satellite dish near the party wall,
  and a mini-split condenser mid-roof; the flue is the most plausible candidate and 2.7
  step 16 makes it the height-setting element deliberately, as a chunky designed object
  rather than a hairline pipe. If aerial research shows that flue standing on 248–250's
  roof rather than this one, re-derive the target from whatever does reach 8.81 and flag
  it — do not clip the model to 8.05 and leave the manifest at 8.8.
- **The assessor's 2,100 sq ft does not reconcile with the footprint.** 195 m² over two
  storeys implies 97.6 m² per floor and a 12.8 m depth at 7.60 m width; the LiDAR
  footprint measures 14.6 m and the OSM trace 13.8 m. The listing separately advertises
  unit 254 alone as "approximately 1,700 square feet" across two levels, which cannot fit
  inside 2,100 sq ft for the whole building. The assessor figure is the outlier and the
  plan follows the LiDAR at 14.2 m, but the rear wall's position is the part of 2.3 most
  likely to be wrong.
- **The 1.2 m footprint-vs-parcel offset is a judgement call, not a fact.** 2.3 places the
  asset in the DataSF frame to keep it flush with its baked neighbour. If a future pass
  re-registers the footprint layer against the parcels — or if 248–250 Ritch ever becomes
  an asset itself and is excluded — the right anchor becomes the parcel-frame point
  `-122.3956253, 37.7801171`, 2.7 m to the south-east. Both are recorded here on purpose.
- **The exposed south-east flank may not stay exposed.** The neighbouring lot `3776149` is
  a surface parking lot in SoMa on SLI zoning, which is exactly what gets developed. The
  asset is correct for the city as baked; if that lot is built the flank becomes a party
  wall and the model needs nothing changed, but the composition loses its third cue.
- **The rear elevation is entirely unverified.** No source shows it. 2.7 step 17 invents a
  plausible door and two windows. Confirm from aerial imagery if anything is visible over
  the roof edge, and otherwise keep it as plain as the plan says rather than inventing a
  stair or a deck.
- **The light wells' depths are inferred.** Their plan positions and sizes are measured off
  the top-down drone frame against the 14.2 m roof as a scale bar and are good to ~0.3 m;
  their 3.0 m depth is a guess constrained only by `hgt_mincm` = 2.13 m, which says the
  roof surface descends to 2.13 m above grade *somewhere* — plausibly at the bottom of a
  well. Read as holes from above, the depth barely matters; do not spend triangles on it.
- **"Studio 254" is a red herring.** Several business directories list a recording studio
  at 254 Ritch Street, and Ritch Street's alley blocks did host studios and clubs. The
  assessor has classified this parcel as Flats & Duplex, Multi-Family Residential in every
  roll year on record, and the 2025 sale was as a 2-unit residential building. Do not model
  a commercial ground floor, a roll-up door or signage on the strength of those listings.
  The ICIJ Offshore Leaks entry for the address is likewise a residential-address record
  and says nothing about the building.
- **The 1915 date and the unit count come from assessor data**, not from a primary record.
  They are consistent with the building's type and with SoMa's post-earthquake rebuilding.
  No architect is recorded, and none would be expected for a speculative alley flat.
- **All five exterior photographs come from one 2025 marketing shoot.** They are excellent
  — a straight-on elevation, a top-down and three aerials — but they are one photographer,
  one day and one set of colour decisions. The measured `#6b696a` inherits that shoot's
  grade. Corroborate the value against Street View or aerial imagery before committing to
  it, and remember the style bible expects a lift regardless.
