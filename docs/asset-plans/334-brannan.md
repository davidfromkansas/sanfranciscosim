# 334 Brannan Street (Sherman and Clay Building) — SF-SIM asset plan

A 1929 reinforced-concrete industrial loft on the northwest side of Brannan, four
lots northeast of 350 Brannan and a contributor to the **South End Historic
District**. It is the only building on this stretch that spends money on its
facade: six bays of steel industrial sash between broad concrete piers, each pier
capped with a small **gilded block**, and a **gold geometric frieze band** running
the whole parapet. At the northeast end a narrow **entry tower** carries a
round-headed portal, the vertical "334" plate, and two **pale-pink Deco panels**
under their own gilt caps.

It is the opposite design problem from 358 Brannan two doors southwest, which is
memorable by proportion (a red slot). This one is a plain square box — 21 m by
21 m, three storeys — that is memorable entirely by **ornament and colour**: warm
greige piers against sage-green recessed panels, gold at the crest, pink at the
tower. Lose the frieze and the caps and this becomes any concrete box in SoMa.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/334-brannan/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `334-brannan` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3930344, 37.7814147` |
| Target height | **13.4 m** to the pier caps; parapet/frieze crest 13.1 m; roof deck 12.15 m (LiDAR measured) |
| Footprint | 21.08 m (Brannan frontage, SE) x 21.13 m deep; 452 m2, measured |
| Triangle cap | 9,000 |
| Category | `19` (industrial) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 334 Brannan Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 334 Brannan Street (the Sherman and Clay
Building) in San Francisco and deliver it as a downloadable, validated GLB.

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
7. `artifacts/350-brannan/` — the closest reference implementation: the same
   block, the same year (1929), the same construction class, a near-identical
   45-degree square footprint, and a build script whose footprint / panel /
   opening / roof-box helpers this asset should reuse rather than reinvent
8. `docs/asset-plans/334-brannan.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A **square three-storey concrete box**, 21.1 m x 21.1 m, sitting at 45 degrees
  to the world axes like the whole SoMa grid, with a flat roof and a substantial
  parapet
- **Six bays of tall steel industrial sash** on the Brannan elevation, separated
  by broad flat piers — the bay rhythm is the building's backbone
- The **gilded frieze**: a band of gold/ochre geometric ornament across the top of
  every bay, and a small **gilt capital block** at the head of every pier. This is
  the single most important feature; it is what makes the building a district
  contributor and it is the only gold on the block
- The **two-tone paint**: warm greige piers, spandrels and surrounds against
  **sage-green** recessed panels, parapet field, roll-up door and base plinth
- The **entry tower** at the northeast end: a narrow sage-green bay with a
  round-headed portal, the vertical `334` plate, and **two pale-pink vertical
  panels** with gilt caps near its crest
- A **very wide sage-green roll-up freight door** filling most of the ground
  floor (the loading dock the leasing copy sells), with two multi-light ground
  windows between it and the entry tower
- The **exposed northeast flank**: 326 Brannan next door is a one-storey building
  set back from the street, so this flank is a plainly visible painted wall above
  a **green living wall** at its base (the JAX Vineyards garden is against it)
- A **used roof deck** — the listing's "roof deck with city views" — with
  furniture, planters, a low stair bulkhead and mechanical clutter, all kept
  below the parapet

## Research 334 Brannan Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The Brannan (southeast) elevation in detail — the bay count, the frieze
  ornament, the pier caps, the pink tower panels, the portal head
- The exposed northeast flank over the neighbouring garden
- Aerial and roof views (the roof deck, its furniture, the bulkhead)
- Ground-level views, day and night
- The exact parapet and pier-cap heights — the weakest numbers in this dossier
  (see 2.15)

**Three source conflicts are already known and resolved in 2.1 — re-check them,
do not silently re-inherit the wrong value:** every commercial listing dates this
building to **1911**, which is the construction date of **340 Brannan next door**
(South End Historic District data form, APN 3775/015) — the Assessor's roll and
the district's own data form for 3775/101 both say **1929**; the DataSF LiDAR
`hgt_maxcm` of **15.63 m is not this building** but bleed from 340 Brannan's
rooftop penthouse across the shared property line (see 2.15); and the Assessor
calls the lot 5,597 sq ft where the surveyed parcel polygon measures 452 m2
(4,865 sq ft) — the polygon is the one the model must sit on.

## Create a reference dossier

Write `artifacts/334-brannan/REFERENCE.md` containing: source links and what each
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

This is a **secondary building** in the style bible's detail budget (§21), but an
ornamented one. The massing is a single box and must stay one: every triangle you
save on the box is a triangle available for the frieze, the caps and the tower,
which are the only things that distinguish this building from its neighbours.
Resist adding hero-tier ornament and resist modelling individual muntins.

The finished asset must be immediately recognizable as 334 Brannan Street,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel
art, not generic low-poly, and never accurate in one view while invented in the
others.

## Scope of the exported asset

Export the single 1929 building: all four elevations, the entry tower, the roof
and its furniture.

Do not include unrelated surrounding city geometry: Brannan Street, the
neighbouring buildings at 326 and 340 Brannan, the JAX Vineyards garden and its
fence, South Park, street trees, the sidewalk, parked cars, people, plinths,
cameras or lights. Temporary context may appear in review renders but must not
leak into the GLB.

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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The Brannan
Street front faces **southeast, bearing 135.1°**; the exposed flank faces
**northeast, 45.1°**; the party wall faces **southwest, 225.1°**; the rear faces
**northwest, 315.1°**. The building is rotated about 45° off the world axes, so
build directly on the measured footprint quad in 2.3 rather than modelling an
axis-aligned box and rotating it.

**Height normalization:** the tallest geometry in the export (the pier caps and
the entry tower's caps) must land at exactly **13.4 m** so the loader's
`targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/334-brannan/build_334_brannan.py` (deterministic build script),
`artifacts/334-brannan/334-brannan.blend`, and
`artifacts/334-brannan/334-brannan.glb`. The script must rebuild the model
reliably enough for future revision. Do not modify or rename an unrelated
existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `334-brannan-top.png`,
`334-brannan-north.png`, `334-brannan-east.png`, `334-brannan-south.png`,
`334-brannan-west.png`, plus `334-brannan-contact-sheet.png`, at least one high
three-quarter aerial beauty render `334-brannan-aerial.png`, and a night render
`334-brannan-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection;
use orthographic or long-lens cameras; label directions from the researched
orientation; the top view must clearly show the parapet ring, the roof deck and
its furniture, the bulkhead and the skylights; the aerial view uses the style
bible's camera assumptions (30-50 degrees down, long lens). Simple tabletop
lighting, neutral warm background, minimal depth of field, and every image must
depict the same exported model.

Note that the axis-aligned elevation renders will each show the building corner-on
at 45°, and each "north"/"south"/"east"/"west" view sees two elevations at once.
That is the expected consequence of the real heading, not a camera error.

## Validate the exported GLB

Re-import `334-brannan.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/334-brannan/validation.json` and
`artifacts/334-brannan/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **30 x 30 m** even
though the building is 21.1 x 21.1 m — that is the expected consequence of a 45°
real-world heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "334-brannan",
  "file": "334-brannan.glb",
  "anchor": [
    -122.3930344,
    37.7814147
  ],
  "targetHeightM": 13.4,
  "cat": 19,
  "name": "334 Brannan Street (Sherman and Clay Building)",
  "estimated": true,
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
for that, together with the integration notes in
`docs/asset-plans/334-brannan.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent
must re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Block / lot | 3775 / 101 | DataSF parcels `acdm-wktn` — `blklot=3775101`, `from_address_num = to_address_num = 334 BRANNAN ST`, active, mapped 1998-07-01 |
| Building name | **Sherman and Clay** | South End Historic District updated building data form, APN 3775/101 (Page & Turnbull, 2008) |
| Built | **1929** | SF Assessor secured roll (identical every year 2007-2025) **and** the district data form. Commercial listings say 1911 — that is 340 Brannan's date, see 2.15 |
| Storeys | **3** | Assessor roll (`number_of_stories = 3.0`), district data form ("3"), and all three building permits (`number_of_existing_stories = 3`) |
| Style | 20th-Century Industrial | district data form |
| Construction / exterior | Reinforced concrete / concrete | district data form; Assessor `construction_type = B` |
| Historic status | **Contributory** to the South End Historic District; NR status code **3D** | district data form; NR certification package, June 2008 |
| Use (assessor) | Industrial (`use_code = IND`) | SF Assessor roll |
| Use (permits) | "printing plant" 2006-2009, "office" 2010 | SF permits 200612069258, 200906150392, 201008048117 |
| Use (today) | boutique creative office, multi-tenant | Avison Young / Showcase / CompStak listings; tenants HBA (Hirsch Bedner Associates), Stuut Inc., AIX Capital, Pika Earth |
| Lot area (assessor) | 5,597 sq ft = 520 m2 | SF Assessor roll — disagrees with the surveyed polygon, see 2.15 |
| Footprint | **452 m2; 21.08 m (SE frontage) x 21.13 m deep**, a near-square rotated ~45° | DataSF parcel polygon `3775101` and OSM way 71211341 agree vertex for vertex — **measured** |
| LiDAR footprint area | 465.5 m2 (1,862 cells at 50 cm) | DataSF LiDAR building footprints `ynuv-fyni`, `mblr = SF3775101` — agrees with the polygon to 3% |
| Roof deck height | **12.14 m above ground** (median), majority 12.18 m, mean 12.14 m, std 1.41 m | DataSF LiDAR `hgt_median_m` — **measured** |
| Ground elevation | 11.44 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Building area | 15,868 sq ft rentable (listings); 25,000 sq ft gross (CompStak) | Avison Young, CompStak — 15,868 / 3 floors = 5,289 sq ft ≈ 491 m2 per floor, consistent with a 452 m2 footprint |
| Frontage heading | Brannan front faces **135.1°** (SE); exposed flank 45.1° (NE); party wall 225.1° (SW); rear 315.1° (NW) | measured from the parcel polygon |
| Zoning | CMUO (Central SoMa mixed use — office); Assessor still records the old SSO | DataSF parcels |
| Marketed features | roof deck with city views, exterior signage, parking / loading dock, showers on each floor, polished concrete and hardwood floors | Avison Young / Showcase / TenantBase listing copy |
| Northeast neighbour | 326 Brannan (lot 012), a 1959 one-storey utilitarian building **set back from the street**, LiDAR medians 2.93 m and 5.66 m | district data form; DataSF LiDAR |
| Southwest neighbour | 340 Brannan (lot 015), 1911, 5 storeys, LiDAR median 14.82 m, max 17.79 m | district data form; DataSF LiDAR |

### 2.2 Sources

- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — **the address-to-lot link**: `3775101 = 334 Brannan St`, and the surveyed parcel polygon this model is built on
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — record `SF3775101`: 1,862 cells, `hgt_median 12.14`, `hgt_majority 12.18`, `hgt_max 15.63`, `gnd_min 11.44`
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — 1929, 3 storeys, Industrial, 5,597 sq ft lot
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — 2006-12-06 ground-floor assembly room (use "printing plant"); 2009-06-15 final inspection; **2010-08-04 re-roofing, $88,855** (the membrane roof the aerial shows); several street-space permits
- `https://sfplanninggis.org/docs/NatRegDistricts/2008-06-26_Final-NR-SouthEndHistDist.pdf` (Page & Turnbull, *South End Historic District* National Register certification, 26 June 2008) — Appendix A2 building data form for APN 3775/101: **"Sherman and Clay", 1929, 20th-Century Industrial, 3 storeys, reinforced concrete, Contributory, 3D**. Section V lists the district's character-defining features: rectangular massing, rhythmically spaced deeply recessed fenestration, large arched loading docks, restrained detailing of "abstract pilaster-like elements", earth-tone colour
- https://www.openstreetmap.org/way/71211341 — footprint and `addr:housenumber=334`; its `height=12` tag agrees with the LiDAR median (unusually, for once)
- Google Street View, Brannan Street panorama (capture **May 2025**) — the two-tone paint, the six bays, the gilt pier caps, the gold frieze, the entry tower with its pink panels and vertical "334", the wide roll-up door, the two ground windows, the black fire escape at the southwest end
- Google Street View / user photosphere inside JAX Vineyards' garden at 326 Brannan (capture Jan 2019) — the **exposed northeast flank**: a plain painted wall with a planted living wall at its base
- Google Maps satellite (Vexcel imagery, 2026) — the roof: a light membrane deck, a used roof-deck zone with furniture and planters toward Brannan, a low bulkhead near the north corner
- Avison Young / Showcase / TenantBase / CompStak listings for "334 Brannan St" — 15,868 RSF, roof deck, loading dock, three storeys; **their 1911 date is wrong**, see 2.15

### 2.3 Orientation and placement

The building occupies its entire lot mid-block on the northwest side of Brannan
Street. It is rotated about 45° from the world axes, like the whole SoMa grid, and
its footprint is a near-perfect square standing on a corner: the four corners lie
almost exactly south, west, north and east of the anchor.

Footprint quad, in Blender coordinates (metres, `+X` east, `+Y` north), already
centred on the anchor `-122.3930344, 37.7814147`, in the winding order the build
script uses:

```
E  ( 14.89,  -0.28)
S  ( -0.04, -15.17)
W  (-14.88,   0.22)
N  (  0.04,  15.17)
```

A fifth surveyed vertex at `(7.30, 7.66)` lies 0.03 m off the straight N→E edge
(bearings 136.0° and 136.3°) and is dropped as survey noise. Keeping it costs
geometry and buys nothing.

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `E -> S` | 21.08 m | SE 135.1° | **Brannan Street front** — the hero elevation |
| `S -> W` | 21.38 m | SW 225.1° | party wall against 340 Brannan (5 storeys, taller) — blind |
| `W -> N` | 21.13 m | NW 315.1° | rear, faces the block interior |
| `N -> E` | 21.43 m | NE 45.1° | **exposed flank** over the 326 Brannan garden |

Because of the 45° heading the axis-aligned bounding box is ~30 x 30 m for a
building that is 21.1 x 21.1 m. That is correct.

### 2.4 What each side shows

**Southeast (Brannan Street front)** — Three storeys of painted reinforced
concrete in two tones: **warm greige** for the structural frame (piers, spandrels,
window surrounds, the ground-floor band) and **sage green** for everything
recessed (the parapet field, the panels behind the pier heads, the roll-up door,
the base plinth, the entry tower). Six bays of tall **steel industrial sash** —
near-black multi-light grids with awning openers — fill floors 2 and 3, each bay
framed by a broad flat pier. Every pier terminates in a small **gilded capital
block** just below the parapet line, and between the piers a band of **gold
geometric ornament** runs across the top of every bay. Ground floor: a very wide
**sage-green roll-up freight door** occupying roughly the southwest two-thirds of
the frontage under a heavy greige lintel band, then a pair of tall multi-light
windows, then the **entry tower** at the northeast end — a narrower sage-green bay
with a round-headed portal, a vertical `334` plate beside it, and **two pale-pink
vertical panels with gilt caps** near its crest. A black steel fire escape hangs
at the extreme southwest end against the party-wall return.

**Northeast (exposed flank)** — Not a hidden party wall. 326 Brannan next door is
a one-storey 1959 building set back from the street, and the gap is JAX Vineyards'
walled garden, so this whole 21 m elevation reads from the sidewalk. It is a plain
painted wall — the same sage green as the recessed panels — with a **planted living
wall** at its base inside the garden, and the parapet band continuing round. No
window rhythm is visible in any reference.

**Southwest (party wall)** — Hard against 340 Brannan, which is two to three
metres taller. Blind, pale concrete, invisible in practice.

**Northwest (rear)** — Faces the interior of the block, overlooked by taller
neighbours and not visible from any street. Plain wall with a service opening.
Treated as blind in the model, and labelled *inferred*.

**Top** — A single flat level at 12.15 m inside a parapet whose Brannan side
carries the frieze. A light membrane roof (re-roofed 2010, $88,855). The
Brannan half is a **used roof deck**: the aerial shows a scatter of tables,
chairs and planters, which is what the leasing copy's "roof deck with city views"
means. Toward the north corner sits a low bulkhead, plus mechanical clutter and
a hatch. The camera sees this more than it sees any elevation — design it.

### 2.5 Recognition cues (ranked)

1. **The gold frieze and the gilt pier caps** — the only gold on this block face,
   and the reason the building is a district contributor. At thumbnail size this
   is the entire identity
2. **Two-tone greige-and-sage paint** with the six-bay pier rhythm
3. **The entry tower** at the northeast end with its two pink panels
4. **The very wide roll-up freight door** filling the ground floor
5. The square 45°-on footprint and the used roof deck

### 2.6 Miniature translation

**Preserve**

- The 21.08 x 21.13 m square footprint and the real 45° heading, exactly
- Six bays. Not five, not seven — the rhythm is the backbone and it is countable
  from the app's aerial camera
- The gold frieze as a continuous band with per-bay articulation, and a gilt cap
  on every pier including the tower's
- The two-tone paint split: greige frame, sage recess. Getting this backwards
  turns the building into a green box
- The pink tower panels, at legible size

**Simplify / exaggerate**

- The frieze ornament is a repeating cast pattern in reality; it becomes one flat
  gold panel per bay with a shallow step. Individual rosettes are sub-pixel
- Roughly forty small panes per sash become one glazed panel per opening with a
  frame; muntins disappear
- The pier caps are pushed up to **13.4 m**, a little proud of the parapet, so the
  silhouette has a deliberate saw-tooth crest rather than one extruded stripe.
  This is the one place semantic exaggeration is spent
- The pink panels are widened to ~0.45 m so they survive at city scale
- The fire escape at the southwest end is dropped: it sits in the shadow of a
  taller neighbour, reads as noise at city scale, and 350 Brannan two doors away
  already carries the block's one modelled fire escape
- Roof clutter becomes four deck tables, two planters, one bulkhead, one
  mechanical block, two skylight boxes and a hatch. Nothing more

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render. `u` runs along each
edge from its first-listed corner.

1. Body: extrude the 2.3 quad from z=0 to z=12.15 (`Toy_stone` walls), cap
   `Toy_cream` — the light membrane roof deck.
2. Parapet ring z=12.15 to 13.10, 0.35 m thick, `Toy_stone`, with a `Toy_trim`
   coping in the top 0.15 m.
3. Brannan skin: 0.10 m proud panel over the front edge, `Toy_stone` — the greige
   frame plane. All front detail is applied to this.
4. Six pier-framed bays, centres at u = 1.75, 4.45, 7.15, 9.85, 12.55, 15.25
   (pitch 2.70 m over a 16.6 m main block). Each bay: a recessed sage panel
   (`Toy_sage`) 2.05 m wide from z=4.60 to z=12.15, then two window openings in
   `Toy_glass` with `Toy_ink` frames — middle floor z=5.10-8.10, top floor
   z=8.60-11.60 (the top floor slightly taller, which is what makes the sash read
   as industrial).
5. Ground floor: `Toy_sage` roll-up freight door 10.6 m wide, z=0 to 4.20, centred
   at u=5.90; two `Toy_glass` ground windows 1.70 m wide, z=1.50-3.90, at u=12.55
   and 15.25; a `Toy_trim` lintel band across the whole frontage at z=4.30-4.60.
6. **The frieze**: one `Toy_gold` panel per bay, 2.30 m wide, z=12.30-12.95,
   0.06 m proud of the parapet field; and a `Toy_gold` capital block 0.55 x 0.55 m
   at the head of each of the seven piers, z=12.95-13.40 — **these set the
   bounding-box top and must land exactly on 13.40**.
7. **Entry tower**: a `Toy_sage` bay 4.40 m wide at the northeast end of the front
   edge (centre u=18.85), 0.18 m proud of the frame plane, z=0 to 13.40, with a
   round-headed `Toy_ink` portal 2.20 m wide, z=0-3.40, rise 0.35; two `Toy_pink`
   panels 0.45 x 1.60 m at z=11.20-12.80, centred at u=17.95 and 19.75, each under
   its own `Toy_gold` cap; a `Toy_trim` `334` plate block beside the portal.
8. Northeast flank: plain `Toy_sage` skin panel z=0 to 12.15 over the whole edge,
   with a `Toy_leaf` living-wall band z=0.30-3.20 across its middle 12 m.
9. Rear and party wall: plain `Toy_stone`; one `Toy_roofd` service door on the
   rear at u=4.0, z=0-3.0.
10. Roof: four deck tables 1.1 x 1.1 x 0.75 m (`Toy_trim`) and two planters
    1.4 x 0.8 x 0.8 m (`Toy_leaf`) clustered in the Brannan half; a bulkhead
    4.2 x 3.2 m, z=12.15-13.15 (`Toy_cream`) near the north corner; one mechanical
    block 2.2 x 1.6 x 1.0 m and one duct (`Toy_steel`); two skylight boxes
    2.0 x 1.4 x 0.35 m (`Toy_glassl` on `Toy_trim` kerbs); one hatch (`Toy_roofd`).
    **Nothing on the roof may exceed 13.10 m** — the parapet hides it all, which
    is why the street photographs show no bulkhead.
11. Bevel 0.12 m, 2 segments on the masses; 0.05/1 on applied panels; none on
    fills and glow shells.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_stone` | `d9d2c2` | the greige concrete frame — piers, spandrels, surrounds, flanks, parapet |
| `Toy_sage` | `8f9b86` | recessed bay panels, parapet field, roll-up door, entry tower, base plinth (palette extension; precedent `Toy_slate` on 358/380 Brannan) |
| `Toy_cream` | `f2ede3` | roof membrane, bulkhead |
| `Toy_trim` | `f3efe6` | lintel band, parapet coping, skylight kerbs, deck tables, `334` plate |
| `Toy_gold` | `c9a227` | **the frieze band and the pier caps** — the identity, and the only saturated warm surface |
| `Toy_pink` | `e8b3ae` | the two entry-tower accent panels (palette extension) |
| `Toy_glass` | `2a4d73` | steel-sash windows |
| `Toy_glassl` | `6f95b8` | skylights |
| `Toy_ink` | `3a3530` | window frames, the portal, door reveals |
| `Toy_roofd` | `45454a` | service door, roof hatch |
| `Toy_steel` | `9aa0a6` | mechanical block and duct |
| `Toy_leaf` | `6d8558` | the living wall on the northeast flank, roof planters |
| `Toy_gold_Glow` | `c9a227` | **the frieze band lit at night** — the hero |
| `Toy_glass_Glow` | `6f95b8` | a restrained scatter of lit windows |

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
surface behind them — the app renders `_Glow` in a separate layer that is ~12%
alpha by day (a *closed* shell is two layers and reads ~23%), so a primary surface
must never be authored as glow, and every glow colour here equals its non-glow
neighbour's day colour. Hero glow: **the gold frieze**, a thin plate over the
frieze panels — the crown lit at night is exactly what this facade is for.
Supporting accent: five lit windows across the two upper floors of the Brannan
elevation, and the portal head. The northeast flank and the rear do not glow.

### 2.9 Top surface

452 m2 of roof seen constantly from above, and unlike its neighbours this one is
*used*. The composition: keep the membrane light and the clutter dark so the
parapet ring reads as a bright edge; put the furniture cluster in the Brannan half
where a real deck would be (city views), against the northeast flank so the middle
of the deck stays open; keep the bulkhead low and toward the north corner. The
parapet's Brannan side is the only one carrying the frieze, which from directly
overhead is a thin gold line along one edge of the square — that is deliberate and
it is how the aerial camera tells this building from 350 Brannan.

### 2.10 Scope

**In the GLB:** the single 1929 building — body, parapet and frieze, all four
elevations, the entry tower, the living-wall band, the roof and its furniture

**Not in the GLB:** Brannan Street, 326 and 340 Brannan, the JAX Vineyards garden
and its fence, South Park, street trees, sidewalk, vehicles, people, plinths,
cameras or lights

### 2.11 Triangle budget

Cap 9,000 — above 358 Brannan's 7,000 because the frontage is three times as wide
and carries a frieze, and below 500 Third's 17,000 because the massing is one box.
Suggested split: body, parapet and coping ~1.2k, the six bays and their windows
~3.0k, ground floor ~0.8k, frieze and pier caps ~1.2k, entry tower ~0.9k, flanks
and living wall ~0.5k, roof furniture ~1.2k.

### 2.12 Draft manifest entry

```json
{
  "id": "334-brannan",
  "file": "334-brannan.glb",
  "anchor": [
    -122.3930344,
    37.7814147
  ],
  "targetHeightM": 13.4,
  "cat": 19,
  "name": "334 Brannan Street (Sherman and Clay Building)",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`"estimated": true` because the target height is photogrammetric, not published —
see 2.15.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '334Brannan'`,
  camelCase like its siblings) and re-bake the affected tiles, or the baked
  procedural building on this footprint will fight the GLB. Size `exclude` by
  measuring against the real bake input, not by analogy: `excluded()` tests every
  ring VERTEX as well as the centroid, and this lot's neighbours are **touching**
  on the southwest and within a few metres on the northeast. The safe band is
  expected to be narrow; the registry's own comments for `370Brannan` (3 m),
  `358Brannan` (7 m) and `362Brannan` (8 m) show the method. Record the measured
  drop counts in `REPORT.md`.
- `loadRadius`: the skill's default formula gives `max(2500, 13.4 * 30) = 2500` m.
  Take the default.
- This is the **eighth** landmark on the 300-400 block of Brannan (334, 350, 358,
  362, 370, 380, 400 and, eventually, 340). Judge it in the aerial beside 350 and
  358: three 1929-era concrete boxes in a row must not read as one building
  repeated. 334's separation is the gold; 350's is the arched portals; 358's is
  its narrowness.
- The block's remaining gap after this is **340 Brannan** (1911, 5 storeys,
  non-contributory, "appears extensively altered"), whose bulk is what makes 334's
  southwest party wall invisible. Build it before judging this one's flank.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 13.4 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~30 x 30 m is expected)
- [ ] Footprint proportion preserved: the building must measure 21.1 x 21.1 m along its own axes
- [ ] Six bays on the Brannan elevation, countable in the top and aerial renders
- [ ] Nothing on the roof rises above the 13.10 m parapet
- [ ] Triangles at or under 9,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the frieze, five windows and the portal head; glow shells proud of the opaque surface
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **Every commercial listing dates this building to 1911, and they are all wrong.**
  Avison Young, Showcase, TenantBase, CompStak and Compass-derived pages repeat
  "built 1911" (CompStak adds "renovated 1984"). 1911 is the construction date of
  **340 Brannan next door** (South End Historic District data form, APN 3775/015,
  5 storeys, non-contributory). The Assessor's roll for 3775/101 says 1929 in
  every year from 2007 to 2025, and the district's own data form for 3775/101 says
  1929. Build the 1929 building: the gold frieze and the pink Deco panels are
  1929 detailing, not 1911 detailing, and they are visibly there.
- **The target height is estimated, and it is the weakest number here.** No
  published height exists; the district data form's Height field is blank. The
  roof deck at 12.14 m is LiDAR-measured and solid. The parapet (13.10) and the
  pier caps (13.40) are scaled off the May 2025 Brannan panorama against the
  measured 21.08 m frontage, with roughly ±0.5 m of uncertainty. The manifest
  entry is therefore `"estimated": true`.
- **DataSF `hgt_maxcm` = 15.63 m is almost certainly not this building.** The same
  record gives `hgt_median 12.14`, `hgt_majority 12.18`, `std 1.41` over 1,862
  cells. 340 Brannan shares the southwest property line, has a LiDAR median of
  14.82 m and a max of 17.79 m on a ground 1.26 m lower, and its rooftop penthouse
  stands right on that boundary — expressed against this building's ground it
  would read 15-16.5 m. Treat the 15.63 as polygon-edge bleed, not a penthouse,
  and **do not build a fourth storey because of it.** This is the same trap 358
  Brannan's dossier documents at 13.32 m, with the neighbour identified this time.
- **The Assessor's 5,597 sq ft lot area disagrees with the 4,865 sq ft surveyed
  polygon by 15%.** The parcel polygon and the OSM way agree vertex for vertex,
  and the LiDAR footprint agrees with them to 3%. Build on the polygon.
- **No architect is recorded** for the 1929 building in any source consulted; the
  district data form leaves Architect and Builder blank. "Sherman and Clay" is the
  building name from that form — Sherman, Clay & Co. was the West Coast piano and
  Victor-phonograph house, and a 1929 warehouse-and-service building for them fits
  the use history, but no source consulted states the original owner explicitly.
- **The rear elevation is unphotographed.** It faces the block interior with no
  public vantage. Modelling it blind is a deliberate choice: a truthful blank beats
  an invented window grid, and the aerial camera sees mostly its parapet.
- **The exact bay count is read from one panorama.** Six bays is counted twice —
  once from the window columns, once from the frieze panel groups — but at a 45°
  heading the northeast end foreshortens; confirm from a second oblique before
  committing.
- Whether the entry portal's head is a true round arch or a flat head with a
  rounded soffit is *inferred* from a single frontal photograph. It reads arched.
