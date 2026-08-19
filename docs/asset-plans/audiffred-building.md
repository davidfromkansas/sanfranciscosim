# The Audiffred Building (1 Mission Street) — SF-SIM asset plan

An 1889 Second Empire brick-and-slate commercial block at the southwest corner of
Mission Street and The Embarcadero — **San Francisco City Landmark No. 7**, NRHP
79000528, and the only building on the landward side of The Embarcadero to survive the
1906 earthquake and fire intact. Three storeys, the third inside a blue-grey slate
mansard, a measured 15.4 m roof deck, and a segmental glazed barrel vault added in the
1983–84 reconstruction that carries the crest to 17.5 m. Footprint 14.00 x 41.84 m —
**585.6 m2, the narrowest bespoke footprint in the set**, a 3:1 slab where every SoMa
precedent is a squat block.

It is a different design problem from the SoMa warehouses. Those are big plain volumes
whose identity is proportion plus one ornament. This one is small, thin, and *entirely*
ornament: a three-part horizontal sandwich — a cream cast-iron shopfront under a red
brick middle under a dark slate mansard — repeated as a fine bay rhythm along 42 m of
Mission Street and wrapped around two 14 m ends. The brief is "the little dark-roofed
French building on the waterfront corner", and the whole job is holding that
cream/red/slate stack and the dormer-and-chimney skyline at thumbnail size without
spending 30,000 triangles on nineteen dormers.

Its neighbours are all modern and pale. Nothing else on this block is red brick, and
nothing else in the district has a mansard. That contrast is the asset.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/audiffred-building/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `audiffred-building` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3927748, 37.7933216` |
| Target height | **17.5 m** to the barrel-vault crest; mansard crest / roof deck 15.4 m (measured); top of brick 10.95 m; shopfront entablature 6.15 m |
| Footprint | 41.84 m (Mission Street long axis) x 14.00 m (Embarcadero / Steuart ends); 585.6 m2, measured |
| Triangle cap | 12,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Audiffred Building GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the Audiffred Building (1 Mission Street /
100 The Embarcadero) in San Francisco and deliver it as a downloadable, validated GLB.

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
7. `artifacts/49-south-park/` — the closest precedent in *kind*: a small, ornamented,
   corner-sited historic building whose identity is a facade rhythm rather than a mass.
   Reuse its bay/opening/cornice-ring helpers rather than reinventing them
8. `artifacts/334-brannan/` and `artifacts/340-brannan/` — the two nearest precedents for
   a brick landmark with a strong cornice line; check their triangle split before
   designing the dormer rhythm
9. `docs/asset-plans/audiffred-building.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A **thin slab**: 41.84 x 14.00 m, three storeys, roof deck at a measured 15.4 m,
  barrel-vault crest at 17.5 m. It is small and narrow next to everything around it and
  must read that way — do not fatten it toward its neighbours
- The **three-band horizontal sandwich**, which is the entire identity:
  1. a **cream cast-iron shopfront** with a heavy ornate white entablature, ground to
     6.15 m, its glazing and awnings near-black,
  2. a **red brick middle storey** with segmental-arched windows under corbelled brick
     "eyebrow" hoods, white quoins at every corner, ending in a **corbel table** of white
     dentils on brick brackets at 10.95 m,
  3. a **blue-grey slate mansard** to 15.4 m, its dormers hooded with white pediments and
     punctuated by red brick chimneys with white corbelled caps
- **Red brick and dark slate in a district of pale modern boxes.** The colour contrast
  against the 24.4 m neighbour sharing its southeast wall, and against Rincon Annex and
  the 1 Hotel, is half of why it is recognisable from the air
- The **glazed barrel vault** riding just inside the mansard crest on all three exposed
  sides, rising to 17.5 m — the crest, the 1983–84 addition, and the single most visible
  feature from the app's downward camera
- **Three public elevations, one party wall.** Mission Street (northwest, 41.80 m — the
  address and the hero), The Embarcadero (northeast, 14.00 m), Steuart Street (southwest,
  14.00 m). The **southeast long side is a blind brick party wall** — the NRHP nomination
  is explicit that the mansard exists on three sides only and the common wall runs
  straight up to the roof. Do not put a mansard, dormers or windows on it

## Research the Audiffred Building independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation,
and gather references covering:

- All three public elevations. A model built from the Mission Street photograph alone
  will have an invented 14 m end and a wrongly-detailed party wall
- Aerial and roof views — the barrel vault's extent, the flat deck inside it, the
  mechanical plant, and where the chimneys sit
- Ground-level views, day and night
- The **bay count**, the weakest number in this dossier (see 2.15)
- The 1983–84 reconstruction's scope, and which of the ground-floor bays are Bank of
  Italy's 1924 nautical frieze and which are the original plain fascia

Prefer the NRHP nomination form and its 15 photographs, planning and permitting
documents, architectural press, geolocated photography, and aerial/satellite imagery.
Never rely on a single photograph, a single AI-generated image, or a single unsourced
3D model. Separate verified facts from visual inference; if sources disagree, document
the disagreement and decide.

**Three source conflicts are already known and resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:** DataSF LiDAR `hgt_maxcm` is **19.18 m and is
rejected here** as rooftop plant, against a 15.36 m median and a 17.4 m Overture height
(see 2.15 — this is the opposite call from 501 Second Street); the Assessor records
**4 stories** on a building every historical source calls three, because the vaulted
penthouse level added in 1983–84 is the fourth; and the building carries **two street
addresses** (1–21 Mission Street and 100 The Embarcadero) for one parcel, Block 3715
Lot 001.

## Create a reference dossier

Write `artifacts/audiffred-building/REFERENCE.md` containing: source links and what each
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

This is a **secondary-tier** asset by the style bible's §21 scale — small, but a named
city landmark whose whole value is ornament. Spend the detail on the **three horizontal
bands** and on the **mansard skyline** — dormer hoods and chimney caps are what make the
roof read from above. Spend nothing on the floral "A" column capitals, the nautical
frieze's individual seahorses and lighthouses, the slate's diamond-cut centre band, the
window muntins or the corbelled brick coursing; at city scale they are sub-pixel and
they will eat the triangle budget the dormers need.

The finished asset must be immediately recognizable as the Audiffred Building, consistent
with the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1889 building: three public elevations, the southeast party wall, the
shopfront entablature, the corbel table, the mansard with its dormers and chimneys, the
barrel vault, the flat roof deck and its plant.

Do not include unrelated surrounding city geometry: Mission Street, The Embarcadero,
Steuart Street, the neighbour at 100 The Embarcadero, the 1 Hotel across Mission, the
Bloody Thursday memorial in the sidewalk, street trees, the sidewalk, parked cars,
people, plinths, cameras or lights. Temporary context may appear in review renders but
must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project palette;
`_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no cameras, lights,
animations, armatures or constraints; at most 12,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric`
in `app/src/assets.js` only scales and positions). The Mission Street elevation faces
**northwest, bearing 315.2°**; The Embarcadero end faces **northeast, 44.8°**; the
Steuart Street end faces **southwest, 225.0°**; the party wall faces **southeast,
135.2°**. The building is rotated about 45° off the world axes, so build directly on the
measured footprint rectangle in 2.3 rather than modelling an axis-aligned box and
rotating it.

**Height normalization:** the tallest geometry in the export (the barrel-vault ridge)
must land at exactly **17.5 m** so the loader's `targetHeightM / measuredHeight` scale is
1.0. Nothing — no chimney, no rooftop plant — may out-top it.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/audiffred-building/build_audiffred_building.py` (deterministic build
script), `artifacts/audiffred-building/audiffred-building.blend`, and
`artifacts/audiffred-building/audiffred-building.glb`. The script must rebuild the model
reliably enough for future revision. Do not modify or rename an unrelated existing GLB to
satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`audiffred-building-top.png`, `audiffred-building-north.png`,
`audiffred-building-east.png`, `audiffred-building-south.png`,
`audiffred-building-west.png`, plus `audiffred-building-contact-sheet.png`, at least one
high three-quarter aerial beauty render `audiffred-building-aerial.png`, and a night
render `audiffred-building-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the mansard ring, the dormer and chimney rhythm, the barrel
vault, the flat deck and the plant. The aerial view uses the style bible's camera
assumptions (30–50 degrees down, long lens), from the **north**, so that the Mission
Street elevation and The Embarcadero end are seen together across the corner.

Note that the axis-aligned elevation renders will each show the building at 45°. That is
the expected consequence of the real heading, not a camera error.

## Validate the exported GLB

Re-import `audiffred-building.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Render at least one review image from the re-imported asset. Write
`artifacts/audiffred-building/validation.json` and
`artifacts/audiffred-building/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **39.6 x 39.3 m** even though
the building is 41.84 x 14.00 m — that is the expected consequence of a ~45° real-world
heading, not a scale error. A 3:1 building whose axis-aligned bbox comes out square is
correct here; check the footprint along the building's OWN axes before concluding
anything is wrong.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "audiffred-building",
  "file": "audiffred-building.glb",
  "anchor": [
    -122.3927748,
    37.7933216
  ],
  "targetHeightM": 17.5,
  "cat": 3,
  "name": "Audiffred Building (1 Mission Street)",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/audiffred-building.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* or *estimated*
are visual or derived, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Block / lot | 3715 / 001 (`mblr` `SF3715001`) | DataSF parcels `acdm-wktn` — `blklot=3715001`, `from_address_num = to_address_num = 1`, `MISSION ST`, zoning C-3-O; matches the NRHP nomination's "Lot #1 in Assessor's Block 3715" exactly |
| Addresses | **1–21 Mission Street** and **100 The Embarcadero** | one parcel, two street frontages; NRHP files it under 100 The Embarcadero, the Assessor and OSM under both |
| Built | **1889** | NRHP nomination (SF Water Department records); SF Assessor `year_property_built = 1889` — two independent sources agreeing on an 1889 date is unusually good |
| Architect | **none of record**; Hippolite d'Audiffret (owner-builder), William E. Cullen credited by PCAD and for the 1983–84 rebuild | NRHP says "the designer is unknown"; NPS NRIS says "Architects: Unknown"; Wikipedia and PCAD name d'Audiffret and Cullen — see 2.15 |
| Style | **Second Empire** (French mansard) | NPS NRIS `Architectural Styles: SECOND EMPIRE`; NRHP describes "the intent to duplicate French Mansard architecture" |
| Storeys | **3** occupied storeys, the third inside the mansard, **plus a vaulted penthouse level** added 1983–84 | NRHP: "The apparent mansard 'attic' is, in fact, the third floor"; Wikipedia "three floors"; SF Assessor `number_of_stories = 4.0` counts the penthouse |
| Use | Commercial Office; Boulevard restaurant on the ground floor since 1993 | SF Assessor `use_definition = Commercial Office`, `use_code COMO`; OSM `building=retail` + the `Boulevard` restaurant node |
| Building area | 24,908 sq ft = 2,314 m2 | SF Assessor `property_area` — 3.95x the 585.6 m2 footprint, i.e. four levels, which is what corroborates the Assessor's storey count |
| Lot area | 6,301.63 sq ft = **585.4 m2** | SF Assessor `lot_area` — agrees with the OSM footprint area (585.6 m2) to **0.03%** |
| Footprint | 585.6 m2; **41.84 m x 14.00 m**, 99.9% rectangular fill | OSM way 193054136 OBB — **measured**; the NRHP's "45 feet 10 inches wide and 135½ feet long" is 13.97 x 41.30 m, a 0.2% / 1.3% agreement |
| Roof deck / mansard crest | **15.4 m** | DataSF LiDAR `hgt_majoritycm 1544` (the modal roof plane) and `hgt_mediancm 1536`, over 2,238 cells — **measured** |
| Barrel-vault crest | **17.5 m** | Overture `height 17.4`; photogrammetry off the corner elevation gives 17.4–18.1 m — *estimated*, and the number the model is normalized to (see 2.15) |
| Rejected height | DataSF LiDAR `hgt_maxcm` **19.18 m** | rooftop plant, not architecture — see 2.15 |
| Ground elevation | 3.27 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Corner condition | Mission Street (NW, long) x The Embarcadero (NE, short); Steuart Street (SW, short); **party wall** to 100 The Embarcadero (SE, long) | NRHP ("a common brick party wall and three exposed walls"); OSM; confirmed on the Vexcel aerial |
| Frontage headings | Mission 315.2° (NW); Embarcadero 44.8° (NE); Steuart 225.0° (SW); party wall 135.2° (SE) | measured from the footprint OBB |
| Landmark status | **SF City Landmark No. 7** (designated 13 October 1968); **NRHP 79000528** (listed 10 May 1979) | SF Planning Code Article 10 Appendix A; NPS NRIS |
| Wikidata | `Q38585977` | OSM tag on way 193054136 |
| Reconstruction | gutted by a gas fire in **1978**; rebuilt 1983–84, penthouse and barrel vault added | NRHP continuation sheets (written mid-restoration, December 1978 photos); Wikipedia; CAENLUCIER |

### 2.2 Sources

- **NRHP nomination form 79000528** (`https://npgallery.nps.gov/GetAsset/3aa06aad-5c07-4dd2-8e26-752c546519a8/`)
  — the single most valuable source here, and the one the modeller should read first. It
  gives the construction system floor by floor (cast-iron ground storey, common-bond brick
  second storey with header courses every eighth course, wood-framed slate mansard third
  storey), the **party wall on one long side and three exposed walls**, the corner quoins,
  the corbelled brick "eyebrow" window mouldings, the corbel table of soldier course over
  dentils, the 1924 Bank of Italy nautical frieze on the *eastern half* of the ground
  floor, the diamond-cut slate centre band, and the lot dimensions
- `https://npgallery.nps.gov/GetAsset/48cabe18-9d82-4d86-a5d9-930d166003fa/` — the
  nomination's **15 photographs**, December 1978, captioned by elevation ("Third floor
  (mansard) Steuart Street", "Detail of third floor (mansard) corner of Steuart and
  Mission"). Pre-fire-restoration, so read them for *form*, not for the current roof
- `https://en.wikipedia.org/wiki/Audiffred_Building` — three floors, Second Empire, brick
  with projecting quoins, wood-framed tiled mansard with a diamond pattern, fluted
  cast-iron columns with floral "A" capitals, the nautical frieze (dolphins, lighthouses,
  sailing ships, seahorses), **the domed penthouse added in the reconstruction**
- `https://pcad.lib.washington.edu/building/2370/` — Second Empire, 1889, "A remodeling of
  this building occurred in 1983. A penthouse was also added at this time"; SF Landmark
  No. 7 (1968-10-13), NRHP 79000528
- `https://www.foundsf.org/Audiffred_Building` — Libby Ingalls' labour-history essay, plus
  three dated photographs (c. 1905, 1964 under the Embarcadero Freeway, 2012)
- `https://noehill.com/sf/landmarks/sf007.asp` — SF Landmark No. 7 record and photographs
- `https://caenlucier.com/blog-press/2019/1/18/the-survival-of-landmark-7` — the 1983–84
  refurbishment by William E. Cullen for Dusan Mills
- `https://commons.wikimedia.org/wiki/Category:Audiffred_Building` — **26 freely-licensed
  photographs**, the best reference set available for this building. The ones that matter:
  `Audiffred Building (San Francisco).JPG` (the Mission x Embarcadero corner from the
  northeast, camera at 37.793851/−122.392617 — shows the corner, the mansard, the chimneys
  and the barrel vault together), `Audifred Building, The Embarcadero, San Francisco,
  California.jpg` (the Steuart end and the full Mission run from the southwest),
  `Audiffred Building-5.jpg` (the Steuart corner close up — the brick coursing, the eyebrow
  hoods, the corbel table, the diamond-cut slate band, a chimney cap)
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived)
  — polygon `SF3715001`: 2,238 cells, `hgt_median 15.36`, `hgt_majority 15.44`,
  `hgt_mean 14.66`, `hgt_std 2.33`, `hgt_max 19.18`, ground 3.27 m
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — `3715001 = 1 MISSION ST`,
  C-3-O zoning, Financial District/South Beach
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor, 2025 roll) — Commercial Office,
  built 1889, 4.0 stories, 24,908 sq ft, lot 6,301.63 sq ft
- https://www.openstreetmap.org/way/193054136 — `name=The Audiffred Building`,
  `addr:housenumber=100`, `addr:street=The Embarcadero`, `building=retail`,
  `building:levels=3`, `roof:shape=mansard`, `wikidata=Q38585977`. **No `height` tag** —
  unusually, OSM contributes nothing to the height question here
- `pipeline/data/overture_buildings.geojsonseq` — the ring named "The Audiffred Building",
  `height 17.4`, 4 vertices, centroid 0.04 m from the anchor
- Google Maps satellite (Vexcel imagery) — the roof: the mansard ring on three sides, the
  glazed barrel vault just inside it, the pale flat deck, the mechanical cluster on the
  centre line, and the neighbour's roof garden beyond the party wall

Exa queries run (all via `web_search_advanced_exa`): "Audiffred Building 1 Mission Street
San Francisco architect history" (8 results, summaries — yielded the NRHP form, PCAD,
Wikipedia, NPGallery, FoundSF); "Audiffred Building San Francisco domed penthouse rooftop
Boulevard restaurant aerial photo" (10 results, highlights — yielded Wikimedia Commons,
the NRHP photo set, CAENLUCIER, noehill). Facts confirmed by Exa: 1889, Second Empire,
three storeys, SF Landmark No. 7, NRHP 79000528, the 1978 fire, the 1983–84 penthouse.
Everything dimensional came from DataSF, OSM and the NRHP nomination, not from Exa.

### 2.3 Orientation and placement

The building fills the whole 585 m2 corner lot and runs 41.8 m back from The Embarcadero
to Steuart Street. It is rotated about 45° from the world axes, like the whole downtown
grid. The address elevation is the **long** one.

OSM, DataSF LiDAR, the Overture ring and the NRHP's surveyed lot dimensions all agree
within 1.3% here — a four-way agreement this asset does not need to relitigate. The OSM
OBB is used.

Footprint rectangle, in Blender coordinates (metres, `+X` east, `+Y` north), clockwise,
already centred on the anchor `-122.3927748, 37.7933216`:

```
(  9.88,  19.66)   north corner  — Mission x The Embarcadero
( 19.81,   9.79)   east corner   — The Embarcadero x party wall
( -9.89, -19.67)   south corner  — party wall x Steuart
(-19.80,  -9.78)   west corner   — Steuart x Mission
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `( 9.88,19.66) -> (19.81,9.79)` | 14.00 m | NE 44.8° | **The Embarcadero** (the waterfront end) |
| `(19.81,9.79) -> (-9.89,-19.67)` | 41.84 m | SE 135.2° | **party wall** to 100 The Embarcadero — blind |
| `(-9.89,-19.67) -> (-19.80,-9.78)` | 14.00 m | SW 225.0° | **Steuart Street** |
| `(-19.80,-9.78) -> (9.88,19.66)` | 41.80 m | NW 315.2° | **Mission Street** (the address, the hero) |

Because of the 45.2° heading the axis-aligned bounding box is ~39.6 x 39.3 m for a
building that is 41.84 x 14.00 m. A 3:1 slab whose world-aligned bbox is square is the
correct outcome here, and it is the single most likely thing for a reviewer to
misdiagnose as a modelling error.

### 2.4 What each side shows

**Northwest — Mission Street (the address, 41.80 m).** The hero elevation and the long
one. Bottom: a cream-painted cast-iron shopfront, its columns fluted with a lattice
wainscot and floral "A" capitals, glazed near-black with dark awnings, capped by a heavy
white entablature carrying "The Audiffred Building" in incised lettering, with the
**Bank of Italy nautical frieze** on the eastern (Embarcadero-side) half only and the
plainer original sawtooth fascia on the western half. Middle: red common-bond brick with
white quoins at the corners, tall segmental-arched window pairs under corbelled brick
eyebrow hoods that run together into a continuous string, ending in a **corbel table** of
white dentils over brick brackets at 10.95 m. Top: the blue-grey slate mansard, one
white pedimented dormer per bay, red brick chimneys with white corbelled caps punctuating
the run, and the glazed barrel vault riding behind the crown moulding.

**Northeast — The Embarcadero (14.00 m).** The waterfront end and the second-most-seen
face, because it is what the camera meets coming along the Embarcadero. Same three bands
at a wider rhythm: three bays, and the NRHP notes that **the corner windows of the end
elevations are double width**. A chimney at each corner. The vault turns the corner here
with a mitred hip — visible in the reference corner photograph and the one place the
crest reads unambiguously.

**Southwest — Steuart Street (14.00 m).** The mirror of the Embarcadero end: three bays,
double-width corner windows, mansard, dormers, corner chimneys. Boulevard's street sign
and the "100 STEUART" address plate are here. No frieze — the nautical band never reached
this end.

**Southeast (41.84 m).** **Party wall.** Blind brick, no quoins, no eyebrows, no corbel
table, no mansard, no dormers — the NRHP is explicit that "the masonry common wall
continues to the roof while the three exposed walls are of wood frame covered with slate
shingles". Its neighbour at 100 The Embarcadero is 24.4 m tall, so this face is buried
for most of its height and only its top few metres are ever seen. Do not invent windows.

**Top.** 586 m2 at 15.4 m, and the surface the app's camera spends the most pixels on
for a building this short. The Vexcel aerial reads: the **mansard ring on three sides**,
the **glazed barrel vault** immediately inside it — a continuous shallow segmental vault
running the length of Mission and turning both ends, its crown at 17.5 m — a **pale flat
membrane deck** filling the middle and the party-wall side, a **mechanical cluster** along
the centre line (this is what DataSF's 19.18 m maximum is measuring), and a roof hatch.
The neighbour's roof garden beyond the party wall is not part of this asset.

### 2.5 Recognition cues (ranked)

1. **The dark slate mansard with its dormer-and-chimney skyline.** Nothing else in the
   Financial District has one. From above it is the whole building
2. **The cream / red / slate horizontal sandwich** — three bands, bottom to top, read as
   three colours at distance
3. **The glazed barrel vault** riding the crest on three sides — the one non-19th-century
   move, and the highest point
4. **Thinness.** 41.8 x 14.0 m at 17.5 m, hard against a 24.4 m neighbour on one whole
   long side. If it reads as a square block, it is wrong
5. The waterfront corner position — the last small old building on the landward side of
   The Embarcadero, with the Ferry Building across the street

### 2.6 Miniature translation

**Preserve**

- The 41.84 x 14.00 m proportion, the 15.4 m deck, the 17.5 m crest and the real 45.2°
  heading, exactly
- The three colour bands and their two dividing lines (the shopfront entablature at
  6.15 m, the corbel table at 10.95 m) — exaggerate both mouldings' projection rather
  than lose them
- The mansard's slope and its dormer rhythm on the three exposed sides only
- The chimneys. They are small but they are the silhouette
- The barrel vault as the crest
- Red brick and blue-grey slate. Never grey brick, never black slate

**Simplify / exaggerate**

- The cast-iron shopfront becomes a cream colonnade of plain chunky piers with one dark
  glazed panel per bay; the fluting, the lattice wainscot and the floral "A" capitals go
- The nautical frieze becomes one continuous recessed band on the eastern half of the
  Mission elevation and around the Embarcadero end, distinguished from the western half's
  plain fascia only by depth — no seahorses
- Each segmental-arched window pair becomes one arched dark opening in a white surround;
  the corbelled eyebrow becomes a single white arch band
- The corbel table becomes one continuous white dentil ring; the individual brick
  brackets go
- Each dormer becomes a box with a white triangular hood and one pale glazed face
- The slate's diamond-cut centre band is dropped — at this scale it is noise on the one
  surface that must read as a single dark plane
- Downpipes, conduit, the awnings' scalloped edges, the sidewalk memorial and the street
  furniture are dropped
- Roof clutter becomes three `Toy_steel` plant blocks and one hatch, all below the vault

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 rectangle from z=0 to z=10.95 (`Toy_brick` walls), cap it for
   now; the mansard replaces the cap in step 8.
2. Shopfront band: 0 to z=5.75, `Toy_cream`, inset 0.15 m from the brick above on the
   three public faces so the brick reads as overhanging slightly.
3. Shopfront piers: one 0.55 m `Toy_cream` pier per bay boundary on the three public
   faces, z=0 to z=5.75, projecting 0.18 m.
4. Shopfront glazing: one `Toy_ink` panel per bay, z=0.9 to z=5.35, recessed 0.2 m; a
   `Toy_ink` awning slab over each, projecting 0.7 m at z=5.0.
5. **Entablature**: ring on the three public faces, z=5.75 to z=6.15, projecting 0.45 m,
   `Toy_trim` — the first of the two horizontal moves. Add a 0.12 m recessed `Toy_trim`
   frieze band on the Embarcadero half of Mission and around the Embarcadero end only.
6. Brick storey: corner **quoins** as 0.6 x 0.6 m `Toy_trim` columns at the three exposed
   corners, z=6.15 to z=10.55, projecting 0.10 m; one arched `Toy_glass` opening per bay,
   z=7.0 to z=10.0, in a 0.15 m `Toy_trim` surround with a 0.25 m arch band above.
7. **Corbel table**: ring on the three public faces, z=10.55 to z=10.95, projecting
   0.35 m, `Toy_trim` — the second horizontal move.
8. **Mansard**: on the three exposed faces only, a slope from the wall plane at z=10.95
   inward 1.6 m to z=15.10, `Toy_navy`. The party-wall face carries no slope: the
   `Toy_brick` wall continues straight to z=15.4.
9. Crown moulding: `Toy_trim` ring at the top of the slope, z=15.10 to z=15.40,
   projecting 0.30 m.
10. Roof deck: `Toy_sand` cap at z=15.40 inside the mansard ring.
11. **Dormers**: one per bay on the three exposed faces — a 1.1 m wide box set into the
    slope, a `Toy_glassl` face, a `Toy_trim` triangular pedimented hood. This is the
    single biggest triangle line item; see 2.11.
12. **Chimneys**: `Toy_brick` stacks 0.9 x 0.6 m rising from z=10.95 to z=16.2 with a
    `Toy_trim` corbelled cap — two at each end elevation's corners and roughly one per
    three bays along Mission. Nothing here may exceed z=17.5.
13. **Barrel vault**: a segmental `Toy_verdigris` vault, 3.4 m wide, springing from
    z=15.4, ridge at **z=17.5**, running the length of the Mission side and mitring
    around both ends, set 0.4 m inside the crown moulding. 10-segment arc. This sets the
    bounding-box top and must land exactly on 17.5.
14. Roof plant: three `Toy_steel` blocks (max 1.6 m tall) and one hatch on the deck,
    grouped toward the party wall so the vault ring stays clear.
15. Bevel 0.10 m, 2 segments on the masses; 0.04/1 on applied bands, mouldings, dormers
    and quoins.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_brick` | `#c96f4a` | the brick storey, the chimneys, the party wall — **the identity colour** |
| `Toy_navy` | `#2c4a70` | the slate mansard on the three exposed faces — **the other identity colour** |
| `Toy_trim` | `#f3efe6` | the entablature, the corbel table, the crown moulding, quoins, window surrounds, dormer hoods, chimney caps |
| `Toy_cream` | `#f2ede3` | the cast-iron shopfront band and its piers |
| `Toy_ink` | `#3a3530` | shopfront glazing and awnings |
| `Toy_glass` | `#2a4d73` | the arched second-storey windows |
| `Toy_glassl` | `#6f95b8` | dormer sashes (they read pale, not dark, in every reference photo) |
| `Toy_verdigris` | `#9fb8a8` | the barrel vault |
| `Toy_sand` | `#ece4d4` | the flat roof deck |
| `Toy_steel` | `#9aa0a6` | rooftop plant and hatch |
| `Toy_gold_Glow` | `#caa64a` | the entablature sign band — the night hero |
| `Toy_glass_Glow` | `#6f95b8` | scattered lit second-storey and dormer windows |

**Mansard colour note.** `Toy_navy`, not `Toy_roofd`. This is settled repo knowledge:
`Toy_roofd` (#45454a) measured **rgb(9, 9, 12)** in the live scene on a roof deck — it is
effectively black under the app's lighting, and the mansard is the single largest and most
identifying surface on this asset. `Toy_navy` is also what the slate actually reads as in
daylight (the NRHP calls it "hand-cut blue-grey slate"). Keep `Toy_roofd` out of this
build entirely.

**Vault colour note.** The vault is glass in a metal frame and photographs as pale
blue-white in direct sun and pale green-grey in shade. `Toy_verdigris` is chosen over
`Toy_glassl` because the crest needs to separate from the dormer sashes from directly
above, and because a green-grey crown over a navy mansard is the more legible toy read.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque surface
behind them — the app renders `_Glow` in a separate layer, and a closed glow shell is two
alpha layers, so it reads at roughly a fifth opacity by DAY and will tint whatever it
encloses. Never author a primary surface as glow, and never wrap the vault in a closed
glow shell. Remember that a `_Glow` material's **base colour is its night appearance**:
pick it as if unlit.

Hero glow: the **entablature sign band** in `Toy_gold_Glow`, a thin strip proud of the
`Toy_trim` entablature on the three public faces — this is Boulevard's warm restaurant
light, which is what this building actually looks like after dark, and it runs the whole
41.8 m of Mission Street. Supporting: `Toy_glass_Glow` shells over a scatter of
second-storey and dormer windows. Keep it under about a fifth of the openings, and
scatter rather than grid — the upper floors are offices, so a few lit windows is the
truthful pattern. The **party wall stays dark**; there is nothing behind it to light.

### 2.9 Top surface

586 m2 — small, but this is a 17.5 m building under a camera that looks down, so the roof
is a larger share of its pixels than for anything in the SoMa set. The composition is:
the **mansard ring** framing three sides with its dormer bumps and chimney stacks; the
**barrel vault** as a single continuous positive ribbon just inside it, turning both end
corners; the **pale membrane deck** as the quiet middle; and the plant grouped against the
party wall so the vault ribbon stays unbroken. Keep the deck pale (2.8) and the plant
mid-grey, so the roof reads as a designed plane with objects on it rather than a grey
field. The one thing that must survive at thumbnail size is the **contrast between the
navy ring and the pale interior** — that shape, seen from above, is the building.

### 2.10 Scope

**In the GLB:** the single 1889 building — body, shopfront band and piers, entablature and
frieze, brick storey with quoins and arched openings, corbel table, the mansard on three
faces, dormers, chimneys, the crown moulding, the barrel vault, the flat deck and its
plant, and the blind southeast party wall

**Not in the GLB:** Mission Street, The Embarcadero, Steuart Street, 100 The Embarcadero,
the 1 Hotel at 8 Mission, the Bloody Thursday memorial, street trees, sidewalk, vehicles,
people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 12,000 — small for the set, and appropriate for a 586 m2 building, but not as small
as the footprint suggests, because 70 m of public elevation carries a fine bay rhythm on
three sides. Suggested split: body, bands, mouldings and mansard slope ~2.2k; shopfront
piers and glazing ~1.5k; brick openings, surrounds and quoins ~2.0k; **dormers ~2.6k**;
chimneys ~0.8k; barrel vault ~0.9k; deck and plant ~0.6k; glow shells ~0.5k.

**The dormers are the risk.** Nineteen of them at ~140 triangles each is 2.6k before
bevels, and a naive dormer with a mitred hood is easily three times that. If the first
build lands over budget, simplify the dormer hood to a flat plate before touching the
entablature or the corbel table — those two lines are the identity and the dormers are
rhythm.

### 2.12 Draft manifest entry

```json
{
  "id": "audiffred-building",
  "file": "audiffred-building.glb",
  "anchor": [
    -122.3927748,
    37.7933216
  ],
  "targetHeightM": 17.5,
  "cat": 3,
  "name": "Audiffred Building (1 Mission Street)",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`"estimated": true` because the 17.5 m crest the model is normalized to is
photogrammetric plus an Overture figure, not a LiDAR measurement — the 15.4 m deck below
it is measured, but that is not the number in this field. See 2.15.

`cat: 3` (Office) follows the Assessor's `Commercial Office` and the fact that three of
the four levels are offices. Boulevard occupies the ground floor only; if the reviewer
prefers the public-facing identity, `cat: 5` (Restaurant or café) is the alternative and
the name field already carries the address.

### 2.13 Integration notes (for later, not this task)

- **New landmark — Case B.** `audiffred-building` is in neither
  `pipeline/lib/landmarks.mjs` nor `app/src/landmarks.js`, so integration adds a registry
  entry (`id: 'audiffredBuilding'`) and re-bakes the affected tiles. Without the
  exclusion the baked procedural block on this footprint stands at **17.27 m** —
  `datasfHeight()` averages the 15.36 m median with the 19.18 m maximum — which is within
  0.25 m of the asset's own crest and would z-fight it across the entire roof rather than
  poke through it. This is the failure mode an unbaked check cannot see.
- **Exclusion radius — measured against the real bake input.** `excluded()` in
  `pipeline/buildings.mjs` fires on the centroid **or any ring vertex**, on rings already
  passed through `simplifyRing(ring, 0.6)`. Measured from the anchor
  `-122.3927748, 37.7933216` against `pipeline/data/buildings_datasf.geojson` and
  `pipeline/data/overture_buildings.geojsonseq`:

  | Ring | centroid | nearest vertex |
  |---|---|---|
  | Overture "The Audiffred Building" (h 17.4) | **0.04 m** | 21.99 m |
  | DataSF `SF3715001` (h 19.18) | **1.95 m** | 19.99 m |
  | DataSF `SF3715002` — 100 The Embarcadero, h 24.4 | 13.70 m | **19.99 m** |
  | Overture equivalent of the same neighbour (h 20.3) | 13.92 m | 22.03 m |
  | DataSF `SF3715003` (h 29.6) | 28.16 m | 28.47 m |

  Both of this building's own rings are caught by **centroid**, at under 2 m. The
  neighbour is caught by **centroid at 13.70 m**. So the safe window is
  **r ∈ (1.95, 13.70) m**, and **`exclude: 7`** sits near its middle with 3.6x margin
  below and 2.0x above. Note that the nearest vertex of the neighbour and the nearest
  vertex of this building are **the same two points at 19.99 m** — they share the party
  wall, so no radius can ever reach this building's ring vertices without also eating the
  neighbour. It does not need to: the centroid test is what clears this footprint.
- **Verify by penetration, not by count.** `pipeline/verify-rebake.mjs` compares
  per-cell footprint COUNTS and can report "dropped nothing" on a working exclusion.
  Settle it by decoding the tile that contains `-122.3927748, 37.7933216` and confirming
  no procedural geometry remains inside the 41.84 x 14.00 m rectangle.
- `loadRadius`: the default formula gives `max(2500, 17.5 * 30) = 2500` m. Take the
  default. This is not an `alwaysLoaded` piece — at 17.5 m it is not skyline.
- **Camera preset.** Camera offset is `(sin yaw, ·, cos yaw)` with `+z` south, so camera
  bearing = `180 − yaw`. The two hero elevations are Mission (normal 315.2°) and The
  Embarcadero end (44.8°); their bisector is 0°, due north, so **`yaw: 180`** stands the
  eye off the Mission x Embarcadero corner and sees both. `distance: 230` suits a 17.5 m
  building that is 42 m long (cf. `340Brannan` at 240 for 17.79 m, `181SouthPark` at 190
  for 16.5 m). `pitch: 26`. No `key`: this is a small landmark, not a numbered hotkey.
- **Check the shared landmark batch before shipping.** `BODY_VERTS` in
  `app/src/assets.js` reserves 1,200,000 vertices for all *simultaneously loaded*
  landmarks, and the manifest already sums to ~2.3 M across 90 entries. The Embarcadero /
  Steuart cluster currently has **nine landmarks in flight at once** (`8-mission`,
  `110-embarcadero`, `132-embarcadero`, `188-embarcadero`, `121-steuart`, `131-steuart`,
  `165-steuart`, `169-steuart`, `1-steuart-lane`) plus the Ferry Building and Rincon
  Annex within a `loadRadius` of each other. A full batch will silently drop a different
  landmark on each reload if the reserve overflows. Read the console merge line and check
  the buffer occupancy at this corner, not just that this one asset appears.
- **Judge it against its neighbour.** The 24.4 m block at 100 The Embarcadero shares this
  building's whole southeast wall. If the pair does not read as "small old brick thing
  tucked against big plain modern thing" from the aerial, the massing has failed
  regardless of what the elevations look like.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 17.5 m (loader scale lands at 1.0), and the vault ridge —
      not a chimney or a plant block — is what reaches it
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~39.6 x 39.3 m is
      expected for a 41.84 x 14.00 m building at a 45° heading)
- [ ] Footprint proportion preserved: the building must measure 41.84 x 14.00 m along its
      own axes — check this explicitly, the square world bbox hides a fattened slab
- [ ] Roof deck lands at 15.4 m; entablature at 6.15 m and corbel table at 10.95 m both
      project and read from directly above
- [ ] The southeast face carries **no mansard, no dormers, no quoins, no windows**
- [ ] Triangles at or under 12,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`, **no `Toy_roofd`**
- [ ] `_Glow` only on the entablature sign band and the scattered lit windows; glow shells
      proud of the opaque surface, no closed glow shell anywhere
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume
      for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The 17.5 m crest is the weakest number here, and DataSF's 19.18 m maximum is
  rejected — the opposite call from 501 Second Street.** At 501 Second the LiDAR maximum
  was real: a 6.41 m standard deviation over 12,467 cells with a distinct raised block
  visible on the aerial. Here the standard deviation is **2.33 m** over 2,238 cells with a
  modal plane at 15.44 m, and the 19.18 m maximum is 1.64 sd above the median — inside
  spike range, not outside it. Three things argue it is rooftop plant rather than
  architecture: the reference corner photograph shows a **large dark mechanical unit and a
  tank standing on the deck**; the Overture ring for this building carries **`height 17.4`**
  independently; and a photogrammetric read of the vault crown above the crown moulding on
  that same photograph gives **+2.0 to +2.7 m over the 15.4 m deck**, i.e. 17.4–18.1 m, not
  19.2 m. 17.5 m is the convergence of the last two. **Re-derive it before building** — the
  15.4 m deck is measured and safe, but the crest is not, and it is the number the loader
  normalizes against. If a better source puts the vault ridge elsewhere, move the vault and
  keep the deck.
- **The bay count is inferred, and it drives nineteen dormers.** Three bays on each 14 m
  end (with double-width corner windows, per the NRHP) is confident. **Thirteen bays on
  the 41.8 m Mission elevation is a count off a foreshortened photograph** partly occluded
  by street trees, and implies a 3.2 m bay against the ends' 4.67 m — a real
  inconsistency that the NRHP's double-width corner windows only partly explain. Verify
  from a square-on Mission Street photograph before committing. This is the most likely
  place for the model to be visibly wrong, and it is also the biggest line in the triangle
  budget.
- **Every intermediate height is photogrammetric.** The 6.15 m entablature and the 10.95 m
  corbel table come from measuring the corner elevation's vertical proportions
  (0.40 : 0.31 : 0.29 of the 15.4 m to the crest) on a single photograph. Only the 15.4 m
  deck is measured. A 6.15 m ground floor is tall for a three-storey building; it is
  plausible for an 1889 cast-iron waterfront storefront with a deep entablature, but it is
  not verified.
- **The architect is genuinely unresolved, and this is not a data problem to fix.** The
  NRHP nomination says "the designer is unknown"; NPS NRIS says "Architects: Unknown";
  the artandarchitecture-sf essay says "There is no record of an architect on this
  project"; PCAD and Wikipedia name Hippolite d'Audiffret (the owner) and William E.
  Cullen (who did the 1983–84 rebuild, ninety-four years later). Treat the building as
  owner-built to a pattern-book Parisian model, which is what every primary source says.
- **How much of the current fabric is 1889 and how much is 1984 is unclear.** The 1978
  gas fire gutted the interior completely and the exterior was restored around it, the
  Dori's 21 masonry infill was reversed, and the vaulted penthouse is entirely new. The
  model is of the **current** building, which is the right call for a city simulation, but
  a reviewer comparing it to the c. 1905 or 1964 photographs will find differences that
  are not errors.
- **The nautical frieze covers only half of one elevation.** The NRHP is specific: Bank of
  Italy modified "the eastern entablature" in 1924, and the western half retains the
  original sawtooth fascia. Modelling it across the whole building would be a visible
  factual error on the elevation the camera sees most. It is also small enough that
  dropping it entirely is a defensible simplification — what is not defensible is
  applying it uniformly.
- **The party wall's exposure depends on a neighbour this asset does not control.** At
  24.4 m the neighbour buries the party wall almost completely, but `110-embarcadero` is
  in flight in a parallel session and may change what stands there. The party wall is
  modelled blind either way; if the neighbour ends up shorter, the top of a blank brick
  wall is the correct thing to see.
- **Nine sibling landmarks are being built on these two blocks at the same time.** Beyond
  the shared-batch capacity risk in 2.13, the practical hazard is that two of them claim
  overlapping exclusion circles. `exclude: 7` here is deliberately far inside the 13.70 m
  ceiling, which leaves room for the neighbour's own radius; check the sibling plans for
  each other before the batch merge.
