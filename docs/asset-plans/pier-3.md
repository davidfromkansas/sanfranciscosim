# Pier 3 — SF-SIM asset plan

**Pier 3 (Hornblower Landing)**, 374 The Embarcadero — a 1918 Beaux-Arts finger pier in the
**Central Embarcadero Piers Historic District** (Piers 1, 1½, 3 and 5, National Register).
A 140-foot-wide concrete slab pier on spiral-reinforced piles running 700-odd feet into the
bay, fronted on the Embarcadero by a two-storey stucco bulkhead building whose centrepiece
is a **monumental arched portal with "PIER · 3" cut into the pediment and a flagpole above
it**. Condemned in 2004, rehabilitated 2004-2006 by San Francisco Waterfront Partners with
Tom Eliot Fisch, Hannum Associates and Page & Turnbull; the transit shed behind the
bulkhead is gone, replaced by a Class-B office block with two big glazed roof monitors and
an open public deck that today works as the City Cruises / Hornblower excursion landing and
a 125-space surface car park.

This is a **water asset**: nothing under it is land. The loader seats generic landmarks at
`max(0, sampleElevation(x, z))`, so over the bay the origin lands exactly on the water plane
y = 0 — the same contract the bridges and Alcatraz use. Every height in this plan is quoted
**above water level**, not above the promenade.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/pier-3/`. This document is the plan only: Part 1 is the runnable task prompt,
Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `pier-3` |
| Existing procedural builder | none — new landmark, **Case B** (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3947017, 37.7982322` (pier polygon area centroid, over water) |
| Target height | **18.5 m** to the arch-pavilion attic crest above water; bulkhead cornice ~14.0 m; deck top 3.0 m |
| Footprint | 212.79 m x 53.50 m oriented bounding box, 8,926 m2 measured; long axis bearing 53.92° |
| Triangle cap | 18,000 |
| Category | `25` (transit_station) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Pier 3 GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of **Pier 3 (Hornblower Landing), 374 The Embarcadero,
San Francisco** and deliver it as a downloadable, validated GLB.

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
7. `artifacts/ferry-building/` — the closest reference implementation in character: the other
   Embarcadero maritime terminal, same 1898-1918 waterfront family, same problem of a long
   arcaded wall that must stay legible from a high camera
8. `docs/asset-plans/pier-3.md` — this plan, whose dossier is your research starting point,
   not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md` governs
repository and integration rules. Do not invent a new style and do not copy visual
instructions from unrelated prompts.

## Must capture

- The **arched bulkhead portal**: a projecting pedimented pavilion on the Embarcadero
  frontage, a single deep semicircular arch with a voussoir surround, "PIER · 3" incised in
  the tympanum, a raised attic block over the pediment and a flagpole on top. This is the
  entire identity of the asset and where the semantic exaggeration goes
- The **two-storey Beaux-Arts bulkhead wall** flanking the portal: a pale stucco/cast-stone
  wall with a rusticated ground storey, a regular pilaster-and-bay rhythm, paired
  upper-storey windows, and a strong continuous cornice with a low parapet above it
- The **pier deck itself**, sitting on piles above the water — a long low concrete slab with
  a fendered edge, bollards, a railed public promenade down both flanks and a plain open
  apron. The deck is the majority of the asset's plan area and it is what makes the thing
  read as a pier rather than a building
- The **modern office block** on the shoreward third of the deck, behind the bulkhead: a
  flat-roofed two-storey volume carrying **two large glazed roof monitors / skylight arrays**
  and a rank of rooftop mechanical units. From the app's camera this roof is the second-most
  visible surface in the whole asset
- The **surface car park** reading on the outer two-thirds of the deck — painted bays, a
  couple of small service sheds, a light standard rhythm. It is what is actually there and
  it is what stops the deck reading as an empty slab
- The **taper**: the pier is ~53.5 m across at the bulkhead and ~40 m across at the head

## Research Pier 3 independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, the deck elevation above water, and
the real-world orientation, and gather references covering:

- The Embarcadero (southwest) elevation straight on — the portal, the bay rhythm, the cornice
- Both long flanks from the water and from the neighbouring piers (Pier 5 to the northwest,
  Pier 1½ / Pier 1 to the southeast)
- The pier head from the bay
- Aerial and roof views — the two roof monitors, the rooftop plant, the car-park layout
- Night views if any exist

Prefer the National Register nomination for the historic district, Port of San Francisco
documents, the rehabilitation architects' project pages, planning and permitting documents,
architectural press, geolocated photography, and aerial/satellite imagery. Never rely on a
single photograph, a single AI-generated image, or a single unsourced 3D model. Separate
verified facts from visual inference; if sources disagree, document the disagreement and
decide.

**Four source conflicts are already known and resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:**

- The postal code is quoted as both **94105** and **94111** by reputable sources. It does not
  affect the model; do not spend time on it.
- OSM has **no `building` way for Pier 3 at all** — way 281428977 is tagged `man_made=pier`
  and is the *pier structure* outline, which is what this plan uses as the footprint. Do not
  go looking for a building polygon; there isn't one.
- The DataSF LiDAR footprint that covers the bulkhead (`mblr = CN9900003`) is a **merged
  polygon spanning the Pier 3, Pier 1½ and Pier 1 bulkheads at once**. Its `hgt_maxcm = 1685`
  and `hgt_mediancm = 1146` are statistics over three buildings, not over Pier 3. Use them
  only as a sanity bound.
- Commercial listings give "Year Built 1900" and "2 Stories, 39,700 SF". The 1900 is a
  placeholder; the pier is **1918**. The 39,700 SF is the rentable office area, not the
  footprint.

## Create a reference dossier

Write `artifacts/pier-3/REFERENCE.md` containing: source links and what each establishes;
verified dimensions and location; orientation; observations from all four sides and above;
the 3-5 strongest recognition cues; features to preserve; features to simplify;
uncertainties and conflicting evidence. A contact sheet of attributed reference thumbnails is
welcome if legally permissible — do not commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the recognition
cues, strip nonessential information, rebuild the massing from a few confident volumes,
exaggerate only the signature features, simplify the facade into broad rhythms, deliberately
design every surface visible from above, evaluate from the app's high three-quarter aerial
camera, then simplify again.

This is a **hero-adjacent landmark**: a National Register structure on the city's most
photographed waterfront, but an ordinary working pier rather than a monument. Spend the
budget on the portal, the bulkhead's bay rhythm, the two roof monitors and the deck edge.
Resist adding monument-tier ornament anywhere else — in particular the deck must stay honest
and plain.

The finished asset must be immediately recognizable as Pier 3, consistent with the real
structure from all four sides and above, architecturally credible, and a premium handcrafted
miniature — not photorealistic, not voxel art, not generic low-poly, and never accurate in
one view while invented in the others.

## Scope of the exported asset

Export the pier structure only: the pile-supported deck and its edge, the bulkhead building
with its portal, the office block and its roofscape, the deck's fixed furniture (railings,
bollards, light standards, the two small service sheds, painted parking bays).

**Do not include** the Embarcadero roadway, Herb Caen Way, the F-line tracks, palm trees, the
seawall promenade, the neighbouring Pier 5 and Pier 1½ bulkheads, the water surface, the
moored excursion vessels (*San Francisco Belle*, *Santa Rosa*) or any other boat, parked
cars, people, plinths, cameras or lights. Temporary context may appear in review renders but
must not leak into the GLB.

The moored vessels are a real and characterful part of the site and it is tempting to include
one. **Do not.** They move, the app already has a live-vessel layer, and a boat baked into a
static landmark would be wrong within the hour.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms; no
negative scales; outward normals; no duplicate or foreign geometry; no image textures; no
transparency; flat-color materials named `Toy_*` from the project palette; `_Glow` suffix only
on surfaces that glow at night; no `Toy_body`; no cameras, lights, animations, armatures or
constraints; no external dependencies; at most 18,000 triangles.

**Water datum — read this twice.** This asset stands over the bay. Its origin sits on the
water plane, exactly like a bridge or an island, because `placeGeneric` in `app/src/assets.js`
seats it at `max(0, sampleElevation(x, z))` and the bay samples at or below zero. Therefore:

- Minimum geometry Z = 0 is the **waterline**, not the deck and not the promenade.
- The pile field and the deck soffit occupy 0 → 3.0 m and must be modelled, not implied. A
  deck slab floating with nothing under it will be seen: the app's camera goes to water level.
- Every height in 2.1 and 2.7 is already expressed above this datum. Do not add the
  promenade elevation to them a second time.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops into
the city at its real-world heading — the loader applies no rotation. The pier runs out into
the bay on a bearing of **53.92°**; the bulkhead frontage faces southwest at **233.92°**.
Build on the measured footprint polygon in 2.3 rather than modelling an axis-aligned box and
rotating it by eye. Record the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the attic crest over the arch
pediment) must land at exactly **18.5 m** so the loader's `targetHeightM / measuredHeight`
scale is 1.0. If you model the flagpole, it must be **shorter** than that crest or it becomes
the bounding-box top and rescales the entire pier — see 2.15.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/pier-3/build_pier_3.py` (deterministic build script),
`artifacts/pier-3/pier-3.blend`, and `artifacts/pier-3/pier-3.glb`. The script must rebuild
the model reliably enough for future revision. Do not modify or rename an unrelated existing
GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `pier-3-top.png`,
`pier-3-north.png`, `pier-3-east.png`, `pier-3-south.png`, `pier-3-west.png`, plus
`pier-3-contact-sheet.png`, at least one high three-quarter aerial beauty render
`pier-3-aerial.png`, and a night render `pier-3-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the top
view must clearly show the two roof monitors, the rooftop plant, the deck's parking layout
and the fendered edge; the aerial view uses the style bible's camera assumptions (30-50
degrees down, long lens) and should be flown from the **southwest**, which is the only angle
that shows the portal and the full run of the pier at once. Because the asset is 213 m long
and 53 m wide, also render one **low three-quarter from the water** — it is the only view
that proves the piles, the deck soffit and the deck edge were actually built.

Simple tabletop lighting, neutral warm background, minimal depth of field, and every image
must depict the same exported model.

## Validate the exported GLB

Re-import `pier-3.glb` into a fresh isolated Blender scene and validate the re-import, not
the source scene. Report object count, triangle count, dimensions, bounding-box min/max, min
Z, XY center offset, material names, image-texture count, camera count, light count,
animation count, applied-transform status, negative-scale status, normal-orientation status,
unexpected geometry, and per-material contract compliance. Render at least one review image
from the re-imported asset. Write `artifacts/pier-3/validation.json` and
`artifacts/pier-3/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **196 x 162 m** even though the
pier is 212.8 x 53.5 m — that is the expected consequence of the 53.92° heading, not a scale
error. It is also, by a wide margin, the largest XY footprint of any non-bridge landmark in
the manifest; check the shared-batch budget note in 2.13 before integration.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft entry
in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "pier-3",
  "file": "pier-3.glb",
  "anchor": [
    -122.3947017,
    37.7982322
  ],
  "targetHeightM": 18.5,
  "cat": 25,
  "name": "Pier 3 (Hornblower Landing)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or
any app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in
`docs/asset-plans/pier-3.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify anything it
relies on. Everything marked *measured* was computed in this session from the named dataset
and the arithmetic is reproducible from 2.3 and 2.16.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Name | **Pier 3**; marketed as "Pier 3, Hornblower Landing" | Port of SF; City Experiences; LoopNet |
| Street address | **374 The Embarcadero** (quoted as 94105 and as 94111) | MapQuest/Foursquare 94105-1204; Hornblower's own parking sheet says 94111 |
| Built | **1918** | NPS, Central Embarcadero Piers Historic District; Pacific Waterfront Partners |
| Style | Beaux-Arts; two-storey stucco-on-timber-frame bulkhead with a two-storey arch | NPS district description |
| Historic status | Contributor, **Central Embarcadero Piers Historic District**, National Register (Piers 1, 1½, 3, 5) | NPS |
| Pier structure | **140 ft wide concrete slab on spiral-reinforced piles, extending 720 ft into the bay** | National Register nomination (npgallery) — the single best structural source |
| Known alteration | "loss of much of the transit shed and parts of Pier 3 and Pier 5"; **a single-storey addition to Pier 3's north** | National Register nomination |
| Rehabilitation | 2004-2006, ~$46-54 M, San Francisco Waterfront Partners / Pacific Waterfront Partners with the Port | Pacific Waterfront Partners; SF Chronicle; BayCrossings |
| Architects (rehab) | **Tom Eliot Fisch (TEF)**, in association with **Hannum Associates** and **Page & Turnbull** | tefarch.com; BayCrossings |
| Rehab scope | 120,000 sq ft mixed-use across Piers 1½/3/5; Class A office, three cafes/restaurants, an acre of public waterfront, boat docks, water-taxi landing, a Hornblower ticket office fronting Herb Caen Way | tefarch.com; BayCrossings |
| Marine works | Pier 3 **complete deck replacement on existing piles**, new cast-in-place girders/beams and deck with utility trenches, access vaults and an elevator pit **to support a new commercial building** | Vortex Marine Construction |
| Office building | 2 storeys, **39,700 SF**, Class B, typical floor 30,470 SF, atrium, **125 surface parking spaces** | LoopNet listing 21091039 |
| 2021 MEP works | Piers 1½ & 3, 21,900 sq ft, **nine rooftop HVAC units replaced** (VAV AHUs, packaged rooftop units, exhaust fans); architect **Studios Architecture**; owner Port of SF | Pragmatic Professional Engineers |
| Tenants | Bloomberg, Starbucks (Piers 1½/3); a venture-capital firm on a full floor | Pragmatic Professional Engineers; SF Chronicle |
| Current maritime use | **City Cruises / Hornblower excursion landing**; *San Francisco Belle* and *Santa Rosa* moored alongside | OSM ship ways 281243626 / 281243360; City Experiences |
| Footprint (pier structure) | **8,926 m2**; OBB **212.79 m x 53.50 m**, 78.4% rectangular fill | OSM way 281428977 reprojected — **measured** |
| Heading | long axis bearing **53.92°**; bulkhead frontage faces **233.92°** | minimum-area OBB over the footprint — **measured** |
| Anchor (area centroid) | **-122.3947017, 37.7982322** | same polygon — **measured** |
| Promenade / deck grade | **3.07 m** above datum | DataSF LiDAR `gnd_mediancm = 307` for `CN9900003` — **measured** |
| Arch-pavilion attic crest | **18.5 m** above water (15.5 m above grade) | Street View photogrammetry, two independent distance solutions agreeing — **measured, see 2.16** |
| Arch extrados crown | **~12.5 m** above water (9.5 m above grade) | same measurement — **measured** |
| Bulkhead cornice / parapet | **~14.0 m** above water | *inferred* from the elevation photographs against the measured crest |
| Office block roof | **~13 m** above water | *inferred* from imagery; two storeys over a 3.0 m deck |
| LiDAR bound on the bulkhead | `hgt_maxcm = 1685`, `hgt_mediancm = 1146`, over a **merged three-pier polygon** | DataSF `ynuv-fyni`, `mblr = CN9900003` — a bound, not a measurement of Pier 3 |
| Neighbours | Pier 5 (way 91913148) to the northwest, Pier 1½ (way 281428976) and Pier 1 (way 25489482) to the southeast | OSM |

### 2.2 Sources

- `https://www.nps.gov/places/central-embarcadero-piers-historic-district.htm` — NPS summary
  of the district: 1918, Beaux-Arts, Piers 1/1½/3/5, bulkheads and transit sheds
- `https://npgallery.nps.gov/GetAsset/d2f2efab-74ad-432e-ad10-4d27ffc6e593` — the National
  Register nomination itself. **The best single source.** Establishes the bulkheads as
  two-storey stucco-on-timber-frame with two-storey arches, and Pier 3 specifically as a
  140-ft-wide concrete slab pier on spiral-reinforced piles extending 720 ft, with rail
  remnants in the north breezeway, a lost transit shed and a single-storey north addition
- `https://tefarch.com/projects/detail/22` — Tom Eliot Fisch, "Piers 1-1/2, 3, and 5":
  120,000 sq ft mixed use, seismic upgrade, Class A office, an acre of public access
- `https://www.pacificwaterfront.com/the-piers/` — the developer's own history: 1918,
  condemned 2004, National Register listing for the federal tax credits, built 2004-2006
- `https://www.baycrossings.com/construction-to-commence-on-historic-rehabilitation-of-piers-1%C2%BD-3-5-project/`
  — construction announcement: S.J. Amoroso, 22 months, $46 M, CalSTRS financing, the
  Hornblower ticket office on Herb Caen Way, the Pier 1-to-Pier 7 waterside walkway
- `http://vortex-sfb.com/portfolio-items/san-francisco-pier-rehab-and-construction/` — the
  marine contractor: Pier 3 deck fully replaced on existing piles, 400 piles carbon-fibre
  wrapped, 12 seismic bracing assemblies, a 66-pile 150-ft portwalk
- `https://www.pragmaticprofessionalengineers.com/featured-projects/piers-1-1/2-3-san-francisco-ca`
  — 2021 rooftop HVAC replacement, nine units, Studios Architecture, tenants Bloomberg and
  Starbucks
- `https://www.loopnet.com/Listing/Pier-3-Hornblower-landing-San-Francisco-CA/21091039/` —
  2 storeys, 39,700 SF, Class B, atrium, 125 surface parking spaces
- `https://www.sfchronicle.com/bayarea/place/article/san-francisco-restored-piers-pay-tribute-to-2484158.php`
  — the $54 M restoration read as architecture criticism; 77,000 sq ft commercial
- `https://www.openstreetmap.org/way/281428977` — `man_made=pier`, `name=Pier 3`. The
  footprint this plan measures. Also ways 91913148 (Pier 5 building), 281428976 (Pier 1½),
  25489482 (Pier 1), 281255140 (Pier 3 promenade), and node 8839646288 ("City Experiences",
  `office=guide`, `addr:housenumber=Pier 3`)
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived),
  record `mblr = CN9900003` — ground elevation 3.07 m; height statistics **merged across
  three bulkheads**, usable only as a bound
- Esri World Imagery z20, reprojected into local metres and overlaid on the OSM polygon —
  the roof monitors, the rooftop plant, the car-park layout, the taper
- Google Street View panorama `MuiqVIFnVEnHxOVKIKtJhQ` (The Embarcadero opposite Pier 3) and
  panoramas `H_cSsG60buJ9wEvC_z0ZnQ` and `tybmfcgGy1bcjFw6NdmDtw` for the two oblique
  elevations — the source of the height measurement in 2.16 and of the facade reading in 2.4

### 2.3 Orientation and placement

The pier runs out into the bay on a bearing of **53.92°** from a bulkhead frontage on The
Embarcadero. The frontage itself runs 327.6°/147.6° and faces **southwest, at 233.92°**.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
already centred on the anchor `-122.3947017, 37.7982322`. Sub-2 m chamfers at the pier head
have been merged into single corners; the two ~13 m jogs on the northwest flank are real and
worth keeping.

```
A  (  73.400,   78.000)   pier head, north corner
B  (  97.200,   46.400)   pier head, east corner
C  ( -67.083,  -75.299)
D  ( -69.996,  -83.291)
E  ( -98.691,  -38.003)
F  ( -86.328,  -34.422)
G  ( -74.818,  -27.988)
H  (  -0.726,   25.148)
I  (   8.769,   32.101)
```

Edges, with outward normals:

| Edge | Length | Faces | What it is |
|---|---|---|---|
| `A -> B` | 39.6 m | NE 143.0° | **pier head** — the seaward end face, open bay beyond |
| `B -> C` | 204.5 m | SE 143.5° | **southeast flank** — faces Pier 1½ and Pier 1 across a slip |
| `C -> D` | 8.5 m | SE | short return at the shoreward corner |
| `D -> E` | 53.6 m | **SW 233.9°** | **the Embarcadero frontage** — the bulkhead and the portal |
| `E -> F` | 12.9 m | NW | jog |
| `F -> G` | 13.2 m | NW | jog |
| `G -> H` | 91.2 m | NW 323.9° | **northwest flank** — faces Pier 5 across a slip |
| `H -> I` | 11.8 m | NW | jog |
| `I -> A` | 79.3 m | NW 323.9° | northwest flank, outer run |

Because of the 53.92° heading the axis-aligned bounding box is roughly **196 x 162 m**. That
is correct, and it is the largest of any non-bridge landmark in the manifest.

### 2.4 What each side shows

**Southwest (The Embarcadero)** — The hero, and the only elevation most people ever see. A
two-storey pale stucco/cast-stone wall, rusticated at ground level, divided by flat pilasters
into a regular rhythm of bays; paired rectangular windows with moulded surrounds on the upper
storey; shopfront and cafe openings with awnings at ground level; a strong continuous cornice
with a low parapet above. At the centre, projecting slightly and rising above the parapet, the
**arched portal pavilion**: a single deep semicircular arch about 8 m wide springing from
imposts at ~5 m above grade to a crown at ~9.5 m, a stepped voussoir surround, a triangular
pediment with "PIER · 3" incised in the tympanum, and above the pediment a plain raised attic
block carrying a flagpole. Behind the arch the opening is glazed with a dark steel-framed
screen and a service door. Blue banners hang on the pavilion's flanking piers.

**Northwest flank** — Faces the slip toward Pier 5. The shoreward third is the office block's
long wall; beyond it the deck is open, edged with a fendered concrete curb, bollards, a
tubular railing and a line of light standards. The *Santa Rosa* is usually moored along this
side — not in the GLB.

**Southeast flank** — Faces the slip and the Pier 1½ promenade. Same grammar: office wall for
the shoreward third, then open fendered deck. The public waterside walkway that links Pier 1
to Pier 7 runs along here. Small service sheds and a row of parking bays.

**Northeast (pier head)** — The seaward end. A plain 40 m concrete end wall with fendering, a
guard rail, bollards and a few light standards. Nothing architectural; the value here is that
it reads as the *end of a pier*, with the pile field visible below at low camera angles.

**Top** — The second most important surface after the portal, because the app's camera looks
down. Three distinct fields, running shoreward to seaward:
1. the **bulkhead roof**: a low-pitched or flat roof behind the parapet, with the pavilion's
   pediment and attic block breaking it at the centre;
2. the **office block roof**: flat, pale, carrying **two large rectangular glazed monitors /
   skylight arrays** running with the pier axis, plus a rank of grey rooftop mechanical units
   (nine were replaced in 2021) and a screened plant enclosure;
3. the **open deck**: a long pale concrete apron with painted parking bays (125 spaces), two
   small flat-roofed service sheds, a light-standard rhythm down both edges, and the fendered
   perimeter. Real, plain, and exactly what the site is.

**Underside** — Not a facade in the usual sense, but this asset sits on water and the app's
camera reaches water level. A pile field and a deck soffit are required geometry, not optional
detail. Piles are the original 1918 spiral-reinforced concrete, carbon-fibre wrapped in 2005.

### 2.5 Recognition cues (ranked)

1. **The arched "PIER · 3" portal with its flagpole** — the one thing everybody photographs,
   and the only element that distinguishes this pier from Pier 5 and Pier 1½ at a glance
2. **The silhouette of a long finger pier running out into the bay** at 54°, low and flat,
   with the two-storey bulkhead as its only tall element
3. The **two glazed roof monitors** on the office block — the identity from directly above
4. The **two-storey Beaux-Arts bulkhead wall** with its pilaster-and-cornice rhythm, reading
   as one continuous Embarcadero wall with its neighbours
5. The **open working deck**: parking bays, bollards, railings, service sheds

### 2.6 Miniature translation

**Preserve**

- The pier at its real 53.92° heading, its real 213 m length and its taper
- The portal pavilion's whole composition: arch, voussoirs, pediment, inscription, attic block
- The pile field and deck soffit — this is what makes it a pier
- Two roof monitors as real geometry, not decals
- The fendered deck edge, its railing line and its light standards

**Simplify / exaggerate**

- The bulkhead frontage becomes **7 bays** at ~7 m pitch either side of a central pavilion
  ~11 m wide, all identical. The real bay count is not surveyed; do not present it as such
- Upper-storey paired windows become one flat recessed `Toy_glass` panel per bay; the
  pilaster shadow carries the rhythm
- The **"PIER · 3" inscription is enlarged** to roughly 1.6x scale and cut as proud letters,
  not incised — incised text is invisible at city scale. This is where the semantic
  exaggeration is spent, and it is the only text on the asset
- The arch is exaggerated: keep it a true semicircle, widen it to ~9 m and deepen the voussoir
  surround so the shadow reads from above
- The flagpole becomes a short mast **kept below the attic crest** (see 2.15) with no flag
- The pile field becomes a regular grid of chunky square piles on a ~7.5 m pitch, only under
  the visible edge band and the head — a full 400-pile grid is invisible and unaffordable
- The 125 parking bays become painted stripes on the deck material, modelled as flat quads
  slightly proud, in two double-loaded rows
- Railings become a solid low `Toy_steel` ribbon with a top rail, not balusters
- Bollards, cleats, fenders reduce to a repeated chunky block on a wide pitch
- The bulkhead's ground-floor shopfronts reduce to four recessed openings with awnings

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render. **All Z values are above the
water plane, which is Z = 0.**

1. **Pile field**: square piles 0.9 x 0.9 m from Z = 0 to Z = 2.4, `Toy_stone`, on a 7.5 m
   grid, populated only within 10 m of the footprint edge plus a spine down the centreline.
   Cap the count — this must not eat the triangle budget.
2. **Deck slab**: extrude the 2.3 footprint from Z = 2.4 to Z = 3.0, `Toy_stone`. Chamfer the
   outer edge 0.15 m. This is the soffit-plus-slab; the pile heads meet it.
3. **Deck surface**: at Z = 3.0, `Toy_conc`, inset 0.4 m from the slab edge. Painted bays as
   `Toy_trim` quads at Z = 3.01, two double-loaded rows on the outer two-thirds.
4. **Fender / curb ring**: 0.5 m wide, 0.5 m proud, `Toy_ink`, following the whole perimeter
   except the frontage edge.
5. **Railing ribbon**: 1.1 m tall, 0.12 m thick, `Toy_steel`, set 0.3 m in from the curb along
   both flanks and the head.
6. **Bulkhead body**: from the frontage edge `D -> E`, a block 53.5 m along the frontage x
   14 m deep, Z = 3.0 to Z = 12.6, `Toy_cream`. Pilasters 1.1 m wide, proud 0.2 m, on a 7 m
   pitch. Ground storey Z = 3.0 to 7.4 rusticated: four horizontal grooves 0.06 m deep.
7. **Bulkhead cornice and parapet**: cornice band Z = 12.6 to 13.2, proud 0.45 m,
   `Toy_stone`; parapet Z = 13.2 to **14.0**, flush, `Toy_cream`, capped `Toy_stone`.
8. **Bulkhead roof** at Z = 12.6, `Toy_roofd`, behind the parapet, with three vent stacks.
9. **Portal pavilion**: centred on the frontage, 11 m wide, projecting 0.8 m proud of the
   bulkhead wall, rising to a pediment. Wall to Z = 14.0; **triangular pediment** apex at
   Z = 16.8 with a raking cornice 0.4 m proud, `Toy_stone`; **attic block** 5.0 x 2.2 m over
   the pediment from Z = 16.8 to **18.5** in `Toy_cream` with a `Toy_stone` coping — this
   sets the bounding-box top and must land exactly on 18.5.
10. **The arch**: semicircular, 9.0 m span, springing at Z = 8.0, crown at Z = 12.5, cut
    through the pavilion. 16-segment arc. Voussoir surround 0.8 m wide proud 0.25 m,
    `Toy_stone`. Reveal `Toy_ink`. Behind it a recessed `Toy_glass` screen at 1.2 m depth with
    a `Toy_steel` mullion cross.
11. **"PIER · 3"**: proud letters 0.9 m tall, `Toy_stone`, on the pediment tympanum at
    Z ≈ 15.4, centred. Extruded 0.12 m. Simple sans/roman forms; no attempt at the real
    lettering's serifs.
12. **Flagpole**: 0.16 m mast on the attic block, top at Z = 18.2 — **below** the attic crest.
13. **Office block**: on the deck immediately northeast of the bulkhead, 62 m (along the pier
    axis) x 40 m, Z = 3.0 to Z = 12.4, `Toy_sand`, with a shallow set-back from both flanks so
    the deck's edge walkway continues past it. Two window bands, sills at Z = 5.2 and 8.8,
    `Toy_glass`, recessed 0.2 m.
14. **Roof monitors**: two rectangular glazed arrays on the office roof, 24 x 9 m each, 0.9 m
    proud, running with the pier axis, `Toy_glassl` tops with `Toy_steel` frames.
15. **Rooftop plant**: nine `Toy_steel` boxes 2.4 x 1.8 x 1.4 m in two ranks, one 6 x 4 x 2.2 m
    screened enclosure, `Toy_roofd` deck between.
16. **Service sheds**: two flat-roofed boxes 8 x 4 x 3.2 m on the outer deck, `Toy_steel`.
17. **Light standards**: 5.5 m poles, `Toy_ink`, at 24 m pitch down both flanks.
18. **Bollards**: 0.45 m chunky cylinders, `Toy_ink`, at 12 m pitch on both flanks.
19. Bevel 0.10 m, 2 segments, on everything above deck level.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | bulkhead walls, pilasters, portal pavilion, attic block |
| `Toy_sand` | `#ece4d4` | the office block body |
| `Toy_stone` | `#d9d2c2` | cornice, parapet cap, voussoirs, the "PIER · 3" letters, deck slab, piles |
| `Toy_conc` | `#cfc9bd` | the deck walking/parking surface |
| `Toy_trim` | `#f3efe6` | painted parking bays and deck markings |
| `Toy_glass` | `#2a4d73` | bulkhead and office windows, the arch screen |
| `Toy_glassl` | `#6f95b8` | the two roof monitors (lighter, reads as up-facing) |
| `Toy_roofd` | `#45454a` | flat roof membranes |
| `Toy_steel` | `#9aa0a6` | railings, rooftop plant, mullions, service sheds |
| `Toy_ink` | `#3a3530` | fender curb, arch reveal, bollards, light standards |
| `Toy_glass_Glow` | `#2a4d73` | lit windows at night |
| `Toy_glassl_Glow` | `#6f95b8` | one lit roof monitor at night |
| `Toy_amber_Glow` | `#e8b563` | the arch soffit and the deck light standards at night |

Check `Toy_conc` against the shipped palette before using it; if it is not in the list, use
`Toy_stone` for the deck surface and push the slab to a slightly darker neighbour so the two
planes still separate from above.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque geometry —
the app renders `_Glow` in a separate layer, and a closed glow shell reads as two alpha
layers by day (~23%, not 12%), so it will tint the facade it sits on. Author open shells, not
closed boxes.

- **Hero glow:** the **arch soffit**, lit warm from within so the portal reads as a lit
  gateway from a distance. It is the identity, and at night it is the only thing that will be
  legible at all.
- **Supporting:** one of the two roof monitors lit from inside — an office still working, and
  it reads from directly overhead where the elevations do not.
- **Accent:** the deck light standards as small amber points down both flanks — this is what
  draws the pier's *line* into the bay at night, which is the whole point of a pier in a
  night skyline; plus six to eight lit upper-storey windows on the bulkhead and office.
- The "PIER · 3" letters do **not** glow. They are a daylight identity feature, and lighting
  them would turn a 1918 inscription into a sign.

### 2.9 Top surface

The camera looks down, and this asset is 213 m of mostly-horizontal surface, so the roofscape
carries more of the load here than on any ordinary building. Three fields must read as three
distinct planes: the pale bulkhead roof behind its parapet, the office roof with its two
bright glazed monitors and grey plant, and the long pale deck with its painted bays. Keep the
deck surface clearly lighter than the fender curb and clearly separated from the roof planes,
and keep the monitors the brightest thing on the asset so the eye lands on the office block
and then runs out along the pier.

Resist decorating the outer deck. It is a car park on a working pier and a truthful, plain,
well-proportioned apron with a crisp fendered edge will look better in the diorama than an
invented plaza.

### 2.10 Scope

**In the GLB:** the pile field, deck slab and deck surface; the fender curb, railings,
bollards and light standards; the bulkhead building with its portal pavilion, arch and
inscription; the office block with its roof monitors and rooftop plant; the two service sheds;
the painted parking bays.

**Not in the GLB:** The Embarcadero, Herb Caen Way, the F-line tracks and overhead, palm
trees, the seawall promenade, Pier 5 and Pier 1½ and their bulkheads, the water surface, the
moored *San Francisco Belle* and *Santa Rosa* or any other vessel, parked cars, people,
plinths, cameras or lights.

### 2.11 Triangle budget

Cap 18,000. Suggested split: pile field ~2.5k (hard cap — cut the grid before anything else);
deck slab, surface, curb and markings ~2k; railings, bollards and light standards ~2k;
bulkhead body, pilasters and rustication ~2.5k; cornice and parapet ~1k; portal pavilion,
arch and voussoirs ~2.5k; the "PIER · 3" letters ~1k; office block and windows ~2k; roof
monitors, plant and sheds ~1.5k; glow shells ~1k.

If the budget bites, the pile field is the first thing to thin and the portal is the last.

### 2.12 Draft manifest entry

```json
{
  "id": "pier-3",
  "file": "pier-3.glb",
  "anchor": [
    -122.3947017,
    37.7982322
  ],
  "targetHeightM": 18.5,
  "cat": 25,
  "name": "Pier 3 (Hornblower Landing)",
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

- **Case B — new landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: 'pier-3'`,
  `height: 18.5`, `exclude: 45`) and re-bake the affected tiles.

- **The exclusion window is unusually comfortable, and it was measured, not guessed.**
  Decoding the committed toy tiles around the anchor gives these minimum ring-vertex
  distances:

  | Distance from anchor | What it is | Verdict |
  |---|---|---|
  | 13.6 m | 3.5 m shed on the Pier 3 deck (centre 3764.9, -3137.2) | **must go** |
  | 31.2 m | 3.5 m shed on the Pier 3 deck (centre 3784.9, -3149.9) | **must go** |
  | 74.2 m | Pier 1½ bulkhead, 14.4 m tall | **must stay** |
  | 78.8 m | Pier 1½ rooftop element | must stay |
  | 83.9 m | Pier 1½ / Pier 1 bulkhead, 10.7 m | must stay |
  | 121.6 m | Pier 1 transit shed | must stay |
  | 123.9 m | Pier 5 building | must stay |

  Anything from 32 m to 74 m works. **45 m** takes both deck sheds with a 29 m margin to the
  nearest keeper. Verify at integration with `pipeline/verify-rebake.mjs` — and remember that
  it compares per-cell *counts*, so confirm the two sheds are gone by decoding tile
  `23_9.bin`, not by reading the count diff.

- **There is no baked building on the Pier 3 bulkhead site.** The DataSF footprint that
  covers it (`CN9900003`) does not survive into the bake, so the GLB is adding a bulkhead
  where the city currently shows nothing. Two consequences: there is no interpenetration risk
  at the shoreward end, and the Case B fallback leaves genuinely empty water rather than a
  procedural stand-in. That is correct and expected — do not "fix" it.

- **Do not raise the exclusion past 74 m under any circumstances.** `CN9900003` is a *merged*
  DataSF polygon spanning the Pier 3, Pier 1½ and Pier 1 bulkheads as one record, and the
  bake's `excluded()` test fires on any ring vertex. Should that footprint ever start baking,
  a 75 m radius would delete all three bulkheads at once and put a hole in the Embarcadero.

- **Shared-batch budget.** At 213 x 53 m this is the largest non-bridge landmark in the
  manifest by plan area, and the shared landmark `BatchedMesh` has been measured at 99% full
  in SoMa and has overflowed at 84 landmarks. Check the reserve *before* integrating, not
  after: an overflow silently drops a *different* landmark on each reload, so the symptom
  will not point at Pier 3.

- **Water seating.** `placeGeneric` uses `Math.max(0, sampleElevation(x, z))`, and the anchor
  is over open water, so `y` will be exactly 0. Confirm that in local QA by reading the merge
  line — a non-zero seat means the anchor drifted onto the seawall and must be moved back to
  the polygon centroid, not compensated for in the model.

- Suggested camera preset: `{ distance: 430, yaw: 215, pitch: 20 }` — the southwest
  three-quarter that shows the portal and the full run of the pier at once.

- `loadRadius`: the default rule gives `max(2500, 18.5 * 30) = 2500` m. Take the default. The
  site is empty water beyond that radius, which is honest: a pier with nothing on it is much
  less wrong at 2.5 km than a building-shaped hole would be.

- If Pier 1 and Pier 5 are built later, revisit the three bulkheads together — they are one
  architectural wall in reality and will look best if their cornice heights and palettes were
  decided as a set.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0 **and that Z = 0 is the waterline**, with pile geometry
      reaching it — not the deck
- [ ] XY center offset within ~2 m (the tolerance is looser here only because the asset is
      213 m long; do not use it as slack for a misplaced model)
- [ ] Bounding-box top exactly 18.5 m (loader scale lands at 1.0), and the flagpole is
      **below** it
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~196 x 162 m expected)
- [ ] Triangles at or under 18,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the arch soffit, one roof monitor, the deck lights and the scattered lit
      windows; glow shells open and proud, never closed boxes over a primary surface
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for
      the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes; **no boats**
- [ ] Six review renders + contact sheet + night render + the low-from-the-water view,
      all regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **18.5 m is a photogrammetric measurement, not a published figure, and it scales the whole
  asset.** The honest range is **17.5-19.5 m**. It comes from one Street View panorama by two
  independent routes that agree (2.16); no drawing, survey or Wikidata entry for this pier's
  height was found. If a better source turns up, correct it and rebuild rather than nudging
  the attic block.
- **The flagpole is a trap.** It is the visually tallest thing on the real pier and it is
  roughly 4 m above the attic crest. If it is modelled at true height it becomes the
  bounding-box top, `targetHeightM / measuredHeight` divides by ~22.5 instead of 18.5, and
  the entire 213 m pier shrinks by 18%. Model it short, or leave it out.
- **The bay count on the bulkhead frontage is a design simplification**, not a survey. Seven
  bays either side of the pavilion is a proportion read off oblique photographs. Do not
  present it as measured.
- **The office block's dimensions are read off aerial imagery**, not from a plan. 62 x 40 m
  and 12.4 m tall are *inferred*; the LoopNet 39,700 SF over two floors implies ~1,845 m2 per
  floor, which a 62 x 40 m block over-supplies, so the real building is probably smaller or
  L-shaped. Re-measure before building, and prefer the imagery to this plan's numbers.
- **The roof monitors are the least-verified identity feature.** They are unmistakable in z20
  aerial imagery as two large rectangular glazed arrays, but no ground or interior source was
  found to confirm whether they are skylights over an atrium (the LoopNet listing does say
  "Atrium") or photovoltaic arrays. If they turn out to be solar panels the roof reads much
  darker and the night glow on them must be dropped.
- **The single-storey north addition** named in the National Register nomination was not
  positively identified in imagery. It may be one of the deck sheds. Do not invent it.
- **The pile field is a guess in its particulars.** 400 piles were carbon-fibre wrapped in the
  2005 works, and the 1918 piles are spiral-reinforced concrete, but no pile-spacing drawing
  was found. A 7.5 m grid is a plausible reading of a 1918 slab pier; label it *inferred*.
- **The deck level is taken as equal to the promenade at 3.07 m.** The two are continuous at
  the bulkhead in Street View, but the outer deck may step down. If it does, the step is
  small and modelling it flat is the safe choice.
- **The postal code disagreement (94105 vs 94111) is real and unresolved** across otherwise
  reliable sources. It affects nothing in the model.
- **Pier 5 and Pier 1½ stay procedural after this lands.** Pier 3 will be a crisp hand-built
  bulkhead sitting between two baked blocks of different height and palette. That seam is
  acceptable but it is a seam; judge it in local QA from the Embarcadero, not only from the
  aerial.

### 2.16 How the height was measured

Recorded here because 18.5 m has no published source behind it and the next agent should be
able to attack the method rather than re-do it blind.

Google Street View panorama `MuiqVIFnVEnHxOVKIKtJhQ`, on The Embarcadero at
`37.79785953, -122.39632222`, stitched from zoom-3 tiles to 4096 x 2048 equirectangular. The
equirect is levelled, so the horizon is the centre row and elevation angle is
`(1024 - y) / 2048 * 180°`.

At the arch's centre column (x ≈ 3850):

- attic crest at y ≈ 853 → **+15.03°**
- arch extrados crown at y ≈ 930 → **+8.26°**
- pavement at the wall base at y ≈ 1057 → **-2.90°**

The base angle gives horizontal distance as `L = h_cam / tan(2.90°) = h_cam / 0.05067`, which
needs the camera height. Two independent routes pinned `L` without assuming one:

1. **Bearing intersection.** Calibrating the panorama's yaw against the Ferry Building clock
   tower (pano x ≈ 4034, true bearing 134.83° from this camera) puts the arch at 119.1°.
   Intersecting that ray with the bulkhead frontage line — taken from OSM way 91913148,
   Pier 5's building, whose street face runs 144.0°/324.0° and lies 20.32 m from the camera —
   gives **L = 48.2 m**.
2. **Plan identification.** The portal's gabled pavilion is directly visible in Esri z20
   imagery reprojected into local metres, at roughly `(3671, -3069)`, which is **48.7 m** from
   the camera.

The two agree to 0.5 m. Feeding `L = 48.5 m` back through the base angle returns
`h_cam = 2.46 m` — the standard Street View camera height, which is the check that the whole
construction is self-consistent rather than three errors cancelling.

Then `H = h_cam + L·tan(15.03°) = 2.46 + 13.02 = 15.5 m above the promenade`, and the
promenade is 3.07 m above datum (DataSF `gnd_mediancm` for `CN9900003`), giving
**18.5 m above water**. The arch crown works out at 9.5 m above grade, i.e. 12.5 m above
water, which matches the National Register's description of "two-story arches".

As an independent bound, DataSF's LiDAR maximum over the merged three-bulkhead polygon is
16.85 m above ground = 19.9 m above datum. That is above 18.5 m and below 18.5 m plus a
flagpole, which is exactly where it should sit.
