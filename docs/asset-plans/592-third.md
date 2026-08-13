# 592 Third Street — SF-SIM asset plan

A 1905 two-storey industrial loft holding the **west corner of 3rd and Brannan**,
one lot deep and filling it completely: a 22 m × 23 m near-square on the 45° SoMa
grid with two full street elevations and two party walls. Today it is a pale
warm-grey stucco box over a continuous **near-black shopfront band** that turns
the corner unbroken — flat black awnings, big plate-glass bays, Kinoko Real
Estate on the 3rd Street side (588–592), Cafe Buenos Aires next to it, Divine
Yoga Studio and a roll-up garage door around on Brannan (400–414). Upstairs is a
quiet grid of white-framed punched windows with wall-mounted condensers under
them on the Brannan face. The roof is flat, parapeted, and carries roughly a
dozen skylights and hatches — an old industrial floor lit from above.

It is the **low** corner. Across 3rd Street stands 599 Third at 18.3 m; the
Brannan block face running south-west from it is 9.8–13.8 m; the neighbour it
shares its north-west party wall with is 11 m. At 8.2 m this building is the
one that opens the intersection up, and getting it *lower* than everything
around it is most of the job.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/592-third/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `592-third` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3946805, 37.7800910` (footprint AABB centre, measured) |
| Target height | **8.2 m** to the parapet crest (*estimated*); roof deck 7.8 m (LiDAR-measured) |
| Footprint | 21.67 m (3rd Street, NE) × 23.07 m (Brannan, SE), 488.7 m²; a near-square quadrilateral, measured — see the spike note in 2.3 |
| Triangle cap | 9,000 |
| Category | `3` (commercial / office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 592 Third Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 592 Third Street (the 588–592 3rd St /
400–414 Brannan St corner building) in San Francisco and deliver it as a
downloadable, validated GLB.

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
7. `artifacts/599-third/` — the building directly across 3rd Street, already
   built. This asset shares its intersection, its 45° heading and its render
   rig, and must look like it came out of the same toy box. It is a **taller,
   busier** building: 592 must not out-detail it.
8. `artifacts/370-brannan/` and `artifacts/362-brannan/` — the closest
   *typological* references: small two-storey SoMa flat-parapet boxes whose
   build scripts' footprint/edge/opening helpers this asset should reuse rather
   than reinvent
9. `docs/asset-plans/592-third.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The **corner condition**: two designed street elevations of almost equal
  length (21.7 m on 3rd, 23.1 m on Brannan) meeting at a sharp 90° east corner.
  Both get full treatment; neither is a blind wall.
- The **continuous near-black shopfront band** that wraps the corner without a
  break — flat black awnings, large plate-glass bays, a dark recessed entry
  between them. This band is the single strongest cue and reads at thumbnail
  size; the corner turn is what makes it a corner building.
- The **pale warm-grey stucco upper storey** above it: plain, no cornice, no
  ornament, a simple flat parapet.
- The **punched white-framed upper windows** — a quiet, slightly irregular
  rhythm, not a strict grid, and *not* the big industrial multi-pane grids of
  599 Third across the street.
- The **wall-mounted condenser boxes** in a row under the Brannan windows —
  small, but they are what says "old commercial loft, converted piecemeal".
- The **roll-up garage door** at the south-west end of the Brannan frontage.
- The **skylit roof**: a flat membrane deck inside a parapet ring with roughly
  eight to twelve small square skylights and hatch boxes scattered across it.
  A 1905 industrial floor is daylit from above, and from the app's camera this
  roof is the building's largest visible surface.
- The fact that it is **lower than everything around it**: 8.2 m against 599
  Third's 18.3 m across 3rd, 11.0 m for the north-west party-wall neighbour and
  9.8–13.8 m along Brannan. Do not round the height up to match the block.

## Research 592 Third Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The north-east (3rd Street) and south-east (Brannan Street) elevations in
  detail — the shopfront bay divisions, the awning positions, the upper-window
  rhythm on each face
- The east corner itself: whether the parapet steps up there, and whether the
  shopfront band turns as one plane or breaks
- The two party walls (south-west toward 414 Brannan, north-west toward the
  11 m neighbour on 3rd), which this dossier could only see from above
- Aerial and roof views — skylight count, sizes and positions
- Day and night appearance
- **The crest height.** This dossier's 8.2 m is the LiDAR roof-deck mode
  (7.82 m) plus an *estimated* 0.4 m parapet. A measured elevation, a planning
  drawing or a dated photograph against a known neighbour beats it. See the
  conflict note below.

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**Two source problems are already resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:**

1. The DataSF LiDAR `hgt_max` on this footprint is **11.65 m**, 3.8 m above the
   roof-deck mode on a roof with a 0.64 m standard deviation. It is *not* the
   crest. Two mature street trees overhang the 3rd Street parapet in both the
   2026 aerial imagery and the 2025 Street View capture, and the `hgt_min` of
   2.40 m on the same footprint is the matching edge artifact at the other end.
   Same failure mode as 250 Van Ness. Do not model an 11.65 m building.
2. OSM way/124903637 traces **478 m²** where the DataSF LiDAR footprint and the
   assessor's 5,318 sq ft lot both say **489–494 m²**, and OSM's polygon is
   shifted several metres north along the 3rd Street edge. The OSM way is
   `source=Bing`. **Build on the DataSF polygon in 2.3.**

## Create a reference dossier

Write `artifacts/592-third/REFERENCE.md` containing: source links and what each
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

This is a **secondary building** in the style bible's detail budget (§21) — a
tier below 599 Third across the street, and a tier above 370 Brannan. Two
designed elevations, one facade composition repeated around the corner, one
strong value contrast (black band / pale wall), and a genuinely designed roof.
Resist ornament: the real building has none, and inventing any would be a lie
about a plain 1905 loft.

The finished asset must be immediately recognizable as this corner, consistent
with the real building from all four sides and above, architecturally credible,
and a premium handcrafted miniature — not photorealistic, not voxel art, not
generic low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building: stucco body, parapet, both street elevations'
shopfront band and upper windows, both blank party walls, the garage door, the
roof deck and its roof furniture.

Do not include unrelated surrounding city geometry: 3rd Street, Brannan Street,
599 Third, 414 Brannan, the north-west neighbour, the two street trees, the
sidewalk, bike racks, traffic signals, parked cars, people, plinths, cameras or
lights. Temporary context may appear in review renders but must not leak into
the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0; applied
transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 9,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The 3rd Street
front faces **north-east, bearing 45.1°**; the Brannan front faces **south-east,
bearing 135.2°**. The building is rotated roughly 45° off the world axes, so
build directly on the measured footprint polygon in 2.3 rather than modelling an
axis-aligned box and rotating it.

**Height normalization:** the tallest geometry in the export (the parapet crest)
must land at exactly **8.2 m** so the loader's `targetHeightM / measuredHeight`
scale is 1.0. Nothing on the roof may poke above it.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/592-third/build_592_third.py` (deterministic build script),
`artifacts/592-third/592-third.blend`, and `artifacts/592-third/592-third.glb`.
The script must rebuild the model reliably enough for future revision. Do not
modify or rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `592-third-top.png`,
`592-third-north.png`, `592-third-east.png`, `592-third-south.png`,
`592-third-west.png`, plus `592-third-contact-sheet.png`, at least one high
three-quarter aerial beauty render `592-third-aerial.png`, and a night render
`592-third-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection;
use orthographic or long-lens cameras; label directions from the researched
orientation; the top view must clearly show the parapet ring and every skylight
and hatch; the aerial view uses the style bible's camera assumptions (30–50
degrees down, long lens). Simple tabletop lighting, neutral warm background,
minimal depth of field, and every image must depict the same exported model.

Because the building sits at 45° to the world axes, the "east" orthographic
camera looks straight at the east corner and shows both street elevations at
once — that view is the hero, and it is the one to iterate on first. Label the
images by world direction as required, but judge the facades from the aerial.

For the night render, drive `_Glow` from **Base Color**, not from the imported
emission — glTF writes `emissiveFactor = 0`, so a re-imported `_Glow` material
renders white otherwise. `tools/glb-optimize/render_ab.py` does this correctly.

## Validate the exported GLB

Re-import `592-third.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/592-third/validation.json` and
`artifacts/592-third/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **31.0 × 31.6 m** even
though the building is 21.7 × 23.1 m — that is the expected consequence of a ~45°
real-world heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "592-third",
  "file": "592-third.glb",
  "anchor": [
    -122.3946805,
    37.780091
  ],
  "targetHeightM": 8.2,
  "cat": 3,
  "name": "592 Third Street",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/592-third.md`.
````

---

## Part 2 — Research and design dossier

Compiled 13 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent
must re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | **1905** | SF Assessor secured roll 2025, block 3776 lot 114 |
| Storeys | **2** | SF Assessor roll AND the 2015 building permit (`number_of_existing_stories = 2`) |
| Construction | **Wood frame (Type V)** | SF building permits 2011–2015, `existing_construction_type_description = "wood frame (5)"` |
| Block / lot | 3776 / 114 | SF Assessor; DataSF footprint `mblr = SF3776114`; parcel `blklot 3776114` |
| Parcel address of record | **590 3rd St** | DataSF parcels `acdm-wktn` — 588 / 590 / 592 3rd and 400 / 406 / 410 / 414 Brannan are all tenant addresses on this one lot (see 2.15) |
| Footprint | 488.7 m²; 21.67 m (3rd St, NE) × 23.07 m (Brannan, SE) × 20.38 m (SW) × 23.44 m (NW), after de-spiking the published ring (2.3) | DataSF LiDAR building footprint, reprojected — **measured** |
| Lot area | 5,318 sq ft (494 m²) | SF Assessor — the building covers the lot to within 1 % |
| OSM footprint (cross-check) | 478 m², shifted several metres north on the 3rd St edge | OSM way/124903637, `source=Bing`; see 2.15 |
| Roof deck height | **7.82 m** above ground | DataSF LiDAR `hgt_majoritycm` 782, `hgt_median_m` 7.77, `hgt_meancm` 769, std 0.64 m — **measured** |
| Parapet crest | **8.2 m** above ground | *estimated*: roof-deck mode + 0.4 m of parapet. Not published anywhere. See 2.15 |
| LiDAR `hgt_max` | 11.65 m — **not the crest** | street-tree canopy over the 3rd Street parapet; `hgt_min` 2.40 m is the matching artifact. See 2.15 |
| OSM `height` tag | `8` | OSM way/124903637 — agrees with the LiDAR roof deck, i.e. it describes the deck, not the crest |
| Ground elevation | 6.94 m (NAVD88) `gnd_min_m`, mean 7.25 m, range 0.52 m — effectively flat | DataSF LiDAR — the app's terrain handles this, not the asset |
| Zoning | **CMUO** (Central SoMa Mixed Use Office); assessor class Industrial, historic zoning SLI | DataSF parcels + Assessor |
| Frontage headings | 3rd Street front faces **45.1° (NE)**; Brannan front faces **135.2° (SE)**; SW party wall 224.2°; NW party wall 312.0° | measured from the DataSF footprint polygon |
| Current occupants | Kinoko Real Estate (592, 3rd St), Cafe Buenos Aires (590, 3rd St), a disused dry cleaner (588), Buhler Commercial Construction (400 Brannan), Divine Yoga Studio (406 Brannan), J Body Works (410 Brannan) | OSM POI nodes, all `check_date=2026-04-26`; Google Maps listings; 2025 Street View signage |
| Neighbour heights (LiDAR mode) | NW party wall neighbour `SF3776008` **11.03 m**; Brannan block face SW `SF3776011` **9.77 / 13.76 / 11.13 m**; 599 Third across 3rd `SF3775140` **15.70 m** (18.34 m crest); across Brannan `SF3787001/2` 8.49 / 4.96 m | DataSF LiDAR — 592 is the **lowest** thing on its own block |

### 2.2 Sources

- https://www.openstreetmap.org/way/124903637 — footprint (`source=Bing`), `building=yes`, `height=8`
- OSM POI nodes 10270473366 (Kinoko, 592), 12983432802 (Cafe Buenos Aires, 590), 317124808 (disused dry cleaner, 588), 13765490847 (400 Brannan), 10869882845 (406 Brannan), 10869882844 (410 Brannan) — the tenant mix and, more usefully, which frontage each sits on
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, 2010 LiDAR-derived), record `SF3776114` — the authoritative footprint polygon, the 7.82 m roof deck, the 11.65 m max, and every neighbour height quoted in 2.1
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — `blklot 3776114`, address of record 590 3rd St, zoning CMUO, parcel centroid
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls, 2025) — 1905, block/lot, 2 storeys, 5,318 sq ft lot, use class Industrial
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits), block 3776 lot 114 — 6 records 2003–2018: 2 storeys throughout, wood frame, the 2014 ballet-studio fit-out at 410 Brannan, the 2011 corner stucco repair, the 2015 toilet-room remodel at 590 3rd
- Google Street View, capture **May 2025**, from 3rd Street opposite the frontage and from Brannan Street opposite the frontage — both street elevations in detail, and the corner
- Google satellite tiles (Vexcel/Airbus, 2026) at z20–21 and Esri World Imagery at z20 — the roof: flat membrane, the skylight/hatch scatter, the parapet ring, and the two street trees overhanging the 3rd Street edge
- `app/public/tiles/buildings/23_13.bin` (this repo's committed bake) — what the procedural city currently puts here: a 489 m² block, base 6.5 m, top 16.7 m, i.e. **10.2 m tall**. Used for the exclusion measurement in 2.13
- https://kinokorealestate.com/ — confirms 592 3rd St as the firm's home office, South Beach

Nothing here is behind a paywall or a login; no copyrighted imagery is committed
to the repo.

### 2.3 Orientation and placement

The building holds the **west corner** of 3rd and Brannan: 3rd Street runs
NW–SE past its north-east face, Brannan runs NE–SW past its south-east face, and
it has party walls on the other two sides. Directly across 3rd Street to the
north-east is 599 Third (already a manifest landmark); the Shell station at 551
Third and 550 Third are the next two along 3rd to the north-west.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y`
north), **counter-clockwise** from the north corner, already centred on the
anchor `-122.3946805, 37.7800910`:

```
n (  0.195,  15.815)   north corner — 3rd St / NW party wall
w (-15.485,  -1.605)   west corner  — the two party walls meet
s ( -0.875, -15.815)   south corner — Brannan / SW party wall
e ( 15.485,   0.455)   east corner  — 3rd St / Brannan, the hero corner
```

| Edge | Length | Outward normal | Elevation |
|---|---|---|---|
| n→w | 23.44 m | 312.0° (NW) | north-west party wall (the 11 m neighbour on 3rd) |
| w→s | 20.38 m | 224.2° (SW) | south-west party wall (414 Brannan block face) |
| s→e | 23.07 m | 135.2° (SE) | **Brannan Street front** — 400 / 406 / 410 / 414 |
| e→n | 21.67 m | 45.1° (NE) | **3rd Street front** — 588 / 590 / 592 |

Area 488.7 m², within 0.2 % of the published DataSF ring area of 489.4 m² and
within 1 % of the assessor's 494 m² lot.

**The published DataSF ring has a zero-width spike and it moves the north
corner.** `SF3776114` is published with 13 vertices. Its last vertex before
closing, `(-122.3946783, 37.7802340)`, lies **on** the 3rd Street frontage line
to within 9 mm, 2.23 m short of the ring's first vertex — so the first vertex is
a degenerate spike of zero width projecting north-west past the real corner, not
a corner. Taking the ring at face value gives a 3rd Street frontage of 23.90 m;
the real wall is **21.67 m**. Anything built on the naive reading is 2.2 m too
long on its most visible elevation and has its anchor 0.7 m out of place.
Everything in this plan uses the de-spiked quadrilateral above. The remaining
seven intermediate vertices along the NW party wall deviate from the straight
n→w chord by at most **0.55 m** — under the 0.6 m tolerance the tile bake
simplifies at — and are dropped as raster-edge noise on a wall nobody can see.

Note also that this is **not** a rectangle: the NW party wall runs 312.0° where
the Brannan front runs 135.2°, a 3.2° divergence, and the SW edge is 1.3 m
shorter than the NE edge. That skew is real — it is where the neighbouring lot
bites in — and it is worth keeping, because a perfect square would read as
invented on a block where nothing else is square either.

Because of the ~45° heading the axis-aligned bounding box is ~30.97 × 31.63 m.
That is correct.

### 2.4 What each side shows

**North-east (3rd Street front, 21.7 m)** — Two storeys, read as two horizontal
bands. The lower band is a continuous **near-black shopfront** running the full
frontage: flat black awnings, one per bay, with white sans-serif tenant lettering
on them; below each awning a large plate-glass window with a low dark bulkhead
and a white graphic band across the glass; between the Kinoko bays and the café a
**dark recessed entry** with a glass door. Kinoko (592) occupies the bays nearest
the Brannan corner, Cafe Buenos Aires (590) the middle, the disused dry cleaner
(588) the north-west end. The upper band is plain **pale warm-grey stucco** with
white-framed punched rectangular windows in a loose rhythm — a wide group toward
the corner, a pair mid-face, another group toward the north-west end. No cornice.
A plain flat parapet closes it. Two mature street trees stand in front and
partially occlude the wall in every available photograph.

**South-east (Brannan Street front, 23.1 m)** — The same two-band composition,
turning the corner without a break. The black shopfront band continues with
awnings for Divine Yoga Studio (406) and the neighbouring units, numerals `400`,
`406`, `410` painted small on the awning valances, and a **dark roll-up garage
door** at the south-west end. Above, the same pale stucco with punched windows —
here a longer, more regular run of them — and, distinctively, a row of small
**wall-mounted condenser/AC boxes** on brackets just below the sill line, with
short awnings over some of them. This is the more utilitarian of the two faces
and the one that most clearly says converted industrial loft.

**South-west and north-west (party walls)** — Both are built hard against
neighbours that are 1 to 5 m taller, so from the street neither is visible at
all. From the app's aerial camera they are still drawn, so build them as plain
blank stucco with no openings. Inventing windows on a party wall would be a
straightforward lie. The one exception worth considering is the top ~0.4 m of
each: the parapet ring is continuous around all four sides and should read as
such from above.

**Top** — The largest surface the app's camera sees, and the most interesting
thing about this building. A flat, weathered mid-grey membrane deck inside a
continuous parapet, and scattered across it roughly **eight to twelve small
square roof objects**: pale-curbed skylights with dark glazing, a couple of
plain pale hatch boxes, and a small number of vent stacks. They sit in no
particular grid — this is a 1905 industrial floor that was daylit from above and
then patched piecemeal for a century. There is **no penthouse, no stair
bulkhead, no large HVAC plant, and no rooftop billboard** (the billboard visible
in photographs of this corner stands on the brown-brick neighbour further
north-west along 3rd, not on this building). Two street-tree canopies overhang
the 3rd Street parapet.

### 2.5 Recognition cues (ranked)

1. **The wrapped black shopfront band** under a pale stucco upper storey, turning
   a sharp corner — at city scale this is the entire recognition
2. **The corner itself**: two nearly equal designed elevations meeting at 90°,
   with the same composition on both
3. **Being the low one** — 8.2 m against 18.3 m across the street and 11 m next
   door; the silhouette of the intersection depends on it
4. The skylight-scattered flat roof
5. The row of condenser boxes and the roll-up garage door on Brannan

### 2.6 Miniature translation

**Preserve**

- The 21.67 × 23.07 m footprint with its pulled-in west corner, and the real 45°
  heading, exactly
- The two-band composition, identical on both street faces, turning the corner
  unbroken
- The value contrast: near-black band, pale warm-grey wall. This is the asset's
  whole graphic identity and it must survive at 40 px
- The 8.2 m crest — lower than every neighbour

**Simplify / exaggerate**

- The awnings become one continuous black fascia per street face, stepped
  slightly proud, rather than individual per-bay awnings; individual awnings are
  sub-pixel and read as noise
- Tenant lettering, awning numerals and window decals are **not** modelled and
  not textured (the contract forbids textures). Recorded here so the omission is
  a decision, not an oversight
- The upper windows collapse to two groups per face of 2–3 punched openings
  each, keeping the *loose* rhythm but not the exact count
- The condenser row becomes 4 small boxes at even spacing on the Brannan face —
  slightly enlarged so they read from the aerial
- The roll-up door is modelled as one recessed dark panel with a horizontal
  ribbing suggestion at most
- The skylights are reduced to 8 objects, curbs thickened, arranged in the loose
  scatter of the aerial rather than a grid
- Street trees, bike racks, signals, sidewalk, the sandwich board and the wall
  meters all go

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render. `SKIN` = 0.10 m,
the depth the shopfront fascia stands proud of the wall.

1. Body: extrude the 2.3 footprint from z=0 to z=7.82 (roof deck), `Toy_stone`
   tinted pale warm grey, with a `Toy_roofd` top cap.
2. Parapet ring: z=7.82 to z=**8.2**, 0.30 m thick, following all four edges,
   `Toy_stone`. This sets the bounding-box top and must land exactly on 8.2.
3. Shopfront base band: on edges n→e and e→s, a `Toy_ink` field inset 0.05 m,
   from z=0 to z=3.55, turning the east corner as one continuous surface.
4. Awning fascia: a `Toy_ink` slab 0.55 m tall, 0.45 m proud, running the full
   length of both street edges at z=3.10–3.65, mitred at the east corner.
5. Shopfront glazing: on each street edge, `Toy_glass` panels z=0.55–3.05 inset
   0.18 m behind the band, divided by 0.18 m `Toy_ink` mullions into 3 bays on
   the 3rd Street face and 3 bays on Brannan; a `Toy_roofd` bulkhead z=0–0.55
   under each.
6. Entry recess: on edge n→e, one 1.6 m wide `Toy_ink` recess 0.35 m deep,
   z=0–3.55, at roughly 9 m from the east corner, with a `Toy_glass` door panel.
7. Garage door: on edge e→s, a 3.4 m wide `Toy_roofd` panel z=0–3.30 recessed
   0.12 m, at the south-west end.
8. Upper windows: on edge n→e, two groups (one of 3, one of 2) of 1.25 × 1.55 m
   openings with 0.10 m `Toy_trim` surrounds and `Toy_glass` fills, sills at
   z=4.85; on edge e→s, one run of 5 of the same, same sill height.
9. Condenser row: on edge e→s, four `Toy_roofd` boxes 0.75 × 0.45 × 0.55 m on
   small brackets, centred at z=4.30, evenly spaced.
10. Party walls (edges s→w and w→n): blank. No openings.
11. Roof at z=7.82, `Toy_roofd` deck. Eight objects in a loose scatter, none
    exceeding z=8.2: five skylights (`Toy_stone` curbs 1.5 × 1.5 × 0.20 m with
    `Toy_glassl` caps to z=8.15), two hatch boxes (`Toy_stone`,
    1.1 × 0.9 × 0.35 m), one vent cluster (`Toy_roofd`, 0.5 × 0.5 × 0.30 m).
12. Bevel 0.12 m / 2 segments on the solids, 0.05 m / 1 segment on the applied
    bands and fascia, none on fills and glow shells.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_stone` | `#d9d2c2` | body walls, parapet, skylight curbs, hatches |
| `Toy_trim` | `#f3efe6` | upper-window surrounds |
| `Toy_ink` | `#3a3530` | the shopfront band and awning fascia, mullions, entry recess — **the signature** |
| `Toy_glass` | `#2a4d73` | shopfront and upper-window glazing |
| `Toy_glassl` | `#6f95b8` | skylight caps |
| `Toy_roofd` | `#45454a` | roof deck, bulkheads, garage door, condensers, vents |
| `Toy_glass_Glow` | `#6f95b8` | lit shopfront bays at night |
| `Toy_glassl_Glow` | `#8fb4d4` | the two skylights nearest the corner, faintly lit from the floor below |

Note on the body colour: the real upper wall is a pale warm grey a shade cooler
than `Toy_stone`. `Toy_stone` is the right family and keeps the asset in the same
palette as its built neighbours 599 Third and 550 Third. If the aerial render
shows it disappearing into the neighbouring pale roofs, a dedicated `Toy_greige`
at roughly `#c9c4bb` is permissible — off-palette is a WARN not a FAIL. Decide
from the render and record the decision in `REPORT.md`.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
glazing — the app renders `_Glow` in a separate layer that is ~12 % alpha by day,
so a primary surface must never be authored as glow. Hero glow: the **shopfront
bays**, lit as a continuous warm band that turns the corner. A café and a real
estate office on a corner are exactly the thing that is lit at street level after
dark, and one wrapping band is far more legible at city scale than a scatter of
lit upper windows. Supporting accent: the two skylights nearest the east corner,
faintly lit. The upper-storey windows do **not** glow — a dark office floor over
a lit shopfront is what this corner actually looks like, and it keeps the
composition to one hero.

### 2.9 Top surface

An 8 m roof under a camera that spends most of its time above 100 m, on a
near-square 489 m² plan — proportionally this asset is more roof than facade.
Keep the deck value clearly darker than the parapet so the ring reads as a ring;
keep the skylight caps in `Toy_glassl` so the roof has a scatter of bright
points, which is the honest description of a daylit industrial floor and also the
only thing that stops a 24 m square from reading as a blank tile. Resist the
temptation to add a stair bulkhead or an HVAC unit for interest: the aerial
imagery shows neither, and 599 Third across the street already owns the
"working roof with a penthouse" role in this intersection.

### 2.10 Scope

**In the GLB:** the single 1905 building — stucco body, parapet, the wrapped
shopfront band and awning fascia, both streets' glazing and upper windows, the
garage door, the condenser row, both blank party walls, roof deck and roof
furniture

**Not in the GLB:** 3rd Street, Brannan Street, 599 Third, 414 Brannan, the
north-west neighbour, the two street trees, sidewalk, bike racks, signals,
vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 9,000 — above 370 Brannan's 7,000 because this building has two designed
elevations and a much larger roof, below 599 Third's 15,000 because it has half
the height, no penthouse and no industrial window grids. Suggested split: body,
parapet and shopfront band ~2.0k, awning fascia and mullions ~1.2k, shopfront
glazing and openings ~1.8k, upper windows ~1.5k, condensers and garage door
~0.6k, roof furniture ~1.4k, slack ~0.5k.

### 2.12 Draft manifest entry

```json
{
  "id": "592-third",
  "file": "592-third.glb",
  "anchor": [
    -122.3946805,
    37.780091
  ],
  "targetHeightM": 8.2,
  "cat": 3,
  "name": "592 Third Street",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`estimated: true` because the 8.2 m crest is a derived parapet allowance, not a
published or directly measured figure (2.1, 2.15).

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '592Third'`,
  `exclude: 6`) and re-bake the affected tiles, or the baked procedural building
  on this exact footprint will intersect the GLB. It will also *tower* over it:
  the committed bake gives this footprint a base of 6.5 m and a top of 16.7 m,
  i.e. **10.2 m** against the asset's 8.2 m, so without the exclusion the asset
  is simply invisible inside a taller block. This is the case the batch-mode
  note in `ADDRESS-TO-ASSET.md` warns about — do not judge the integration
  before the bake.
- **Exclusion radius, measured two ways.** Against this repo's committed bake
  (`app/public/tiles/buildings/23_13.bin`, the rings `excluded()` actually
  consumes, projected and simplified): this footprint's own ring centroid sits
  **1.64 m** from the anchor and the nearest **neighbour** vertex is **12.87 m**
  (`SF3776008`, the 11 m building on the north-west party wall). Against the raw
  DataSF LiDAR polygons the same two numbers are **0.90 m** and **12.20 m**.
  Since `excluded()` drops a ring on centroid **or** any vertex, the window that
  drops exactly this building is **1.7 m < r < 12.2 m**. **6 m** sits in the
  middle of it with better than 5 m of margin at both ends. Note that this
  building's own nearest vertex is 10.2 m out, so the exclusion fires on the
  centroid test, not the vertex test — do not shrink the radius below 2 m
  thinking the vertices will catch it. Re-run the measurement against the actual
  bake before committing.
- `loadRadius`: the skill's default formula gives `max(2500, 8.2 × 30) = 2500` m.
  Take the default.
- Camera preset: `{ distance: 200, yaw: 315, pitch: 26 }`. `camera` is
  **mandatory** even for a landmark with no number key — `main.js` maps every
  manifest landmark into `presets` and `camera.js` reads `preset.yaw`
  unconditionally (see the note on `599Third`). App yaw = 180 − true bearing, so
  yaw 315 stands the camera off the east corner at true bearing 225°, the one
  angle where both designed elevations and the corner between them read at once
  — the same reasoning that put 599 Third's camera on its own corner bisector.
  200 m suits an 8.2 m building (cf. 370Brannan 150 at 7.63 m, 550Third 190 at
  11 m).
- **This makes four manifest landmarks on one intersection** — 592 Third, 599
  Third, 551 Third and 550 Third — with the Brannan block face south-west of 592
  left procedural. Check in the local QA that 592's parapet meets its baked
  north-west neighbour without a gap or an overlap, and that the 3rd Street wall
  reads continuously from 592 through 551 to 550. A visible step where a
  landmark meets a baked neighbour is the failure mode this corner will show
  first.
- **Batch mode applies.** This landmark is being built alongside others, so
  stage 5 runs the bake, does the full QA on it, then throws it away
  (`git checkout -- app/public/tiles api/_data`) and commits source only.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 8.2 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~31.0 × 31.6 m is expected)
- [ ] Triangles at or under 9,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the shopfront bays and the two corner skylights; glow shells proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual ≤ 0.15 %)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The crest height is the weakest number in this dossier.** Everything else
  about the height is measured: the LiDAR roof-deck mode is 7.82 m over 1,946
  half-metre cells with a 0.64 m standard deviation, the OSM `height=8` tag
  independently agrees with it, and the assessor's two storeys are consistent
  with both. But no source anywhere gives a parapet height, so the 8.2 m crest
  is the deck plus an *estimated* 0.4 m — a typical low parapet on a building of
  this age and type. If the executing agent finds a measured elevation or a
  photograph scaled against a known neighbour, that beats it, and the manifest's
  `targetHeightM` should follow. The error bar is roughly ±0.3 m, which on this
  building is 4 %.
- **`hgt_max = 11.65 m` is a tree, not a building.** Two mature street trees
  stand directly against the 3rd Street kerb and their canopies overhang the
  parapet in both the 2026 satellite imagery and the 2025 Street View capture.
  On a footprint whose height standard deviation is 0.64 m, an 11.65 m maximum
  is a 6σ outlier, and the matching `hgt_min` of 2.40 m at the other end is the
  same kind of edge artifact. This is the 250 Van Ness failure mode exactly:
  a height read off a raster statistic is only as good as the raster's edges.
  Anyone who takes `hgt_max` as the crest here — the way 370 Brannan legitimately
  did, where the max was 0.6 m above the median — builds a three-storey building.
- **The OSM footprint is wrong enough to matter.** Way/124903637 is a
  `source=Bing` trace: 478 m² against the DataSF LiDAR footprint's 489 m² and
  the assessor's 494 m² lot, and its 3rd Street edge is displaced several metres
  north of the surveyed line. Separately, the DataSF ring itself carries a
  zero-width spike at the north corner that inflates the 3rd Street frontage by
  2.2 m if taken literally — see 2.3. On the block-face lesson the plans README already
  records (358 Brannan, 165 South Park), **the DataSF polygon is the survey and
  OSM is the cross-check.** Build on 2.3.
- **The address is ambiguous and the parcel disagrees with the request.** The
  lot's address of record is **590** 3rd Street; 592 is the Kinoko Real Estate
  tenant node inside the same building, and 588, 400, 406, 410 and 414 are five
  more tenant addresses on the same lot. There is exactly one building here.
  The manifest id `592-third` follows the requested address; if a sibling
  session is dispatched against "590 3rd St" it will resolve to this same
  footprint and the two must not both be built. (An empty `pipeline/590-third`
  branch already exists in the working tree — see 2.15's last bullet.)
- **The party walls are unsourced except from above.** Neither the SW nor the NW
  face has any street-level coverage — both are built hard against taller
  neighbours. Treating them as blank stucco is the honest reading and the one
  2.7 specifies, but it is an inference, not an observation.
- **Upper-window counts and positions are *inferred*** from two Street View
  captures partly occluded by street trees. 2.6 deliberately simplifies them to
  two loose groups per face, so being wrong about the exact count costs almost
  nothing; being wrong about the *rhythm* — regular grid vs loose grouping —
  would cost more.
- **No architect and no original-permit record** were found for the 1905
  building in any source consulted; the DBI permit record for this lot starts in
  2003.
- **A `pipeline/590-third` worktree and branch already exist** and are empty at
  the time of writing. If work has started there since, reconcile before
  integrating — the two would produce colliding registry entries for one
  building.
