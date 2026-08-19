# Pier 15 (Exploratorium) — SF-SIM asset plan

**Pier 15, The Embarcadero at Green Street** — a 1931 concrete finger pier in the **Port of
San Francisco Embarcadero Historic District** (National Register), rebuilt 2010–2013 by EHDD
with Page & Turnbull as the home of the **Exploratorium**, the museum of science, art and
human perception. A steel-framed transit shed 823 feet long runs down the pier behind a
classical stucco bulkhead building whose centrepiece is a **monumental arched entry under a
gabled parapet, with "PIER 15" in raised letters, tapering piers, a giant white Exploratorium
"O" ring on the arch glazing, and a flagpole on the gable**. The entire shed roof carries a
**1.3 MW photovoltaic array (5,874 panels)** — the country's largest net-zero-energy museum —
and a continuous glazed monitor rides the ridge. At the bay end, a two-storey glazed **Bay
Observatory Gallery** (2013) and an open Observatory Terrace look across the water. Between
Pier 15 and Pier 17 the old paved "valley" was removed to daylight an **open water courtyard**.

This is a **water asset**: nothing under it is land. The loader seats generic landmarks at
`max(0, sampleElevation(x, z))`, so over the bay the origin lands exactly on the water plane
y = 0 — the same contract the bridges, Alcatraz and Pier 3 use. Every height in this plan is
quoted **above water level**, not above the promenade.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/pier-15/`. This document is the plan only: Part 1 is the runnable task prompt,
Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `pier-15` |
| Existing procedural builder | none — new landmark, **Case B** (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3974662, 37.8016046` (pier polygon area centroid, over water) |
| Target height | **16.4 m** to the bulkhead gable crest above water; monitor ridge ~13.9 m; wing parapet ~11.0 m; deck top 3.05 m |
| Footprint | pier structure 245.0 m x 94.8 m oriented bounding box (incl. aprons); shed 251 m x 54.7 m; long axis bearing 54.9° |
| Triangle cap | 22,000 |
| Category | `25` (transit_station) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Pier 15 (Exploratorium) GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of **Pier 15 (the Exploratorium), The Embarcadero at
Green Street, San Francisco** and deliver it as a downloadable, validated GLB.

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
7. `docs/asset-plans/pier-3.md` and `artifacts/ferry-building/` — the two closest reference
   implementations in character: the same 1918-1931 Embarcadero maritime family, the same
   problem of a long low structure on water that must stay legible from a high camera
8. `docs/asset-plans/pier-15.md` — this plan, whose dossier is your research starting point,
   not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md` governs
repository and integration rules. Do not invent a new style and do not copy visual
instructions from unrelated prompts.

## Must capture

- The **bulkhead pavilion**: a broad central pavilion with a monumental arched entry, a
  gabled parapet with raking cornice, "PIER 15" in an arc of raised letters on the gable,
  monumental tapering piers flanking the arch, and the **giant white Exploratorium "O" ring
  mounted on the arch's glazed fanlight**. This is the identity of the asset and where the
  semantic exaggeration goes
- The **two-storey classical stucco wings** flanking the pavilion: flat-roofed, tall
  25-light steel-sash windows below, 9-light windows above, a crisp parapet
- The **PV-wrapped shed roof**: 823 feet of low-slope roof carrying four longitudinal bands
  of dark blue-grey solar panels separated by pale walkway seams, with cross-platforms at
  intervals — from the app's camera this roof IS the building, and it is unmistakable
- The **continuous glazed roof monitor** riding above the panels (offset south of the shed's
  centreline — the pier was widened north in 1955, see dossier 2.3)
- The **shed side walls**: patinated grey precast concrete, scored, with a clerestory band
  of steel-sash windows near the top and roll-up door bays under canopies along the aprons
- The **Bay Observatory Gallery** at the bay end: a two-storey glazed pavilion with a PV
  roof and square skylight, plus the open Observatory Terrace between it and the shed
- The **pier deck on piles** with the public south apron promenade, the east apron, the
  fendered edge and railings — the deck is what makes it read as a pier
- The **water courtyard** along the northwest flank: the deck's notch stays OPEN — water
  shows between Pier 15 and Pier 17 by design

## Research Pier 15 independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural heights, the footprint, the WGS84 anchor, the deck elevation above water, and
the real-world orientation, and gather references covering:

- The Embarcadero (southwest) elevation straight on — the pavilion, arch, gable, lettering
- Both long flanks: the south apron side (public promenade) and the water-courtyard side
- The bay end with the Observatory building and terrace
- Aerial and roof views — the PV bands, the monitor, the walkway seams, the cross-platforms
- Night views — the glowing monitor and arch fanlight are the night identity

Prefer the National Register nomination for the Embarcadero Historic District (Section 7 has
a dedicated Pier 15 description), Port of San Francisco documents, EHDD's project pages,
the Exploratorium's own publications, architectural press (Architectural Record, AIA Top
Ten), geolocated photography, and aerial/satellite imagery. Never rely on a single
photograph, a single AI-generated image, or a single unsourced 3D model. Separate verified
facts from visual inference; if sources disagree, document the disagreement and decide.

**Known source conflicts, already resolved in 2.1 — re-check them, do not silently
re-inherit the wrong value:**

- Sources quote the pier as **1914, 1915 and 1931**. All are right about something: a wood
  pier of 1915 was demolished and the present concrete pier, shed and bulkhead were all
  built **1930–1931**. Model the 1931 building as renovated in 2013.
- The shed is quoted as **123 feet wide** (1931) but measures **~180 feet / 54.7 m** today:
  the pier was widened to the north in 1955-1956 and the shed extended. The monitor stays
  over the ORIGINAL central aisle, ~7.5 m southeast of today's centreline. Use the measured
  54.7 m and the offset monitor.
- OSM's building way 25478444 tags the shed `building=warehouse` with **no height**, and
  DataSF's LiDAR record for the pier (`SF9900015`, hgt_max 15.64 m) is a **merged polygon
  spanning Piers 15 AND 17 as one record** — its statistics are not Pier 15's. The heights
  in 2.1 were measured photogrammetrically for this plan (2.16); treat them as the best
  available but verify the method.
- The Exploratorium project cost is quoted as $133M, $152M, $205M, $220M and $300M —
  different scopes (construction vs project vs campaign). Irrelevant to the model.

## Create a reference dossier

Write `artifacts/pier-15/REFERENCE.md` containing: source links and what each establishes;
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

This is a **hero landmark**: a National Register structure, one of the city's most visited
museums, and a quarter-kilometre of the Embarcadero. Spend the budget on the pavilion, the
PV roofscape with its monitor, and the deck edge. The shed walls and aprons must stay honest
and plain — it is a working pier that happens to hold a museum, not a monument.

The finished asset must be immediately recognizable as Pier 15/the Exploratorium, consistent
with the real structure from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and
never accurate in one view while invented in the others.

## Scope of the exported asset

Export the pier structure only: the pile-supported deck and its edge, the bulkhead building
with its pavilion, the transit shed with its PV roof and monitor, the Bay Observatory
Gallery and Terrace, and the deck's fixed furniture (railings, bollards, light standards,
the forecourt flagpoles/banners reduced to masts, painted deck markings).

**Do not include** The Embarcadero roadway, Herb Caen Way, the F-line tracks or overhead,
palm trees, the seawall promenade, Pier 17 and its bulkhead, Pier 9, the water surface, any
moored or berthed vessel, the water-taxi float, the Buckyball sculpture on the forecourt
(it is on the seawall, not the pier), parked cars, people, plinths, cameras or lights.
Temporary context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms; no
negative scales; outward normals; no duplicate or foreign geometry; no image textures; no
transparency; flat-color materials named `Toy_*` from the project palette; `_Glow` suffix
only on surfaces that glow at night; no `Toy_body`; no cameras, lights, animations,
armatures or constraints; no external dependencies; at most 22,000 triangles.

**Water datum — read this twice.** This asset stands over the bay. Its origin sits on the
water plane, exactly like a bridge or Pier 3, because `placeGeneric` in `app/src/assets.js`
seats it at `max(0, sampleElevation(x, z))` and the bay samples at or below zero. Therefore:

- Minimum geometry Z = 0 is the **waterline**, not the deck and not the promenade.
- The pile field and the deck soffit occupy 0 → 3.05 m and must be modelled, not implied. A
  deck slab floating with nothing under it will be seen: the app's camera goes to water
  level, and the water courtyard makes the underside of THIS pier more visible than most.
- Every height in 2.1 and 2.7 is already expressed above this datum. Do not add the
  promenade elevation to them a second time.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops into
the city at its real-world heading — the loader applies no rotation. The pier runs out into
the bay on a bearing of **54.9°**; the bulkhead frontage faces southwest at **~235°**.
Build on the measured footprint polygons in 2.3 rather than modelling an axis-aligned box
and rotating it by eye. Record the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the bulkhead gable crest) must
land at exactly **16.4 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.
The real flagpole tops out ~6 m above the gable; if you model it at true height the whole
250 m pier shrinks by ~27%. Model it short (top below 16.4 m) or leave it out — see 2.15.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/pier-15/build_pier_15.py` (deterministic build script),
`artifacts/pier-15/pier-15.blend`, and `artifacts/pier-15/pier-15.glb`. The script must
rebuild the model reliably enough for future revision. Do not modify or rename an unrelated
existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `pier-15-top.png`,
`pier-15-north.png`, `pier-15-east.png`, `pier-15-south.png`, `pier-15-west.png`, plus
`pier-15-contact-sheet.png`, at least one high three-quarter aerial beauty render
`pier-15-aerial.png`, and a night render `pier-15-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the top
view must clearly show the PV bands, the walkway seams, the offset monitor, the terrace and
the observatory skylight; the aerial view uses the style bible's camera assumptions (30-50
degrees down, long lens) and should be flown from the **southwest**, the only angle that
shows the pavilion and the full run of the pier at once. Because the asset is 245 m long,
also render one **low three-quarter from the water** on the courtyard side — the only view
that proves the piles, the deck soffit and the deck edge were actually built.

Simple tabletop lighting, neutral warm background, minimal depth of field, and every image
must depict the same exported model.

## Validate the exported GLB

Re-import `pier-15.glb` into a fresh isolated Blender scene and validate the re-import, not
the source scene. Report object count, triangle count, dimensions, bounding-box min/max, min
Z, XY center offset, material names, image-texture count, camera count, light count,
animation count, applied-transform status, negative-scale status, normal-orientation status,
unexpected geometry, and per-material contract compliance. Render at least one review image
from the re-imported asset. Write `artifacts/pier-15/validation.json` and
`artifacts/pier-15/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **250 x 178 m** even though the
pier is 245 x 94.8 m — that is the expected consequence of the 54.9° heading, not a scale
error. It is the largest XY footprint of any non-bridge landmark in the manifest; check the
shared-batch budget note in 2.13 before integration.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft entry
in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "pier-15",
  "file": "pier-15.glb",
  "anchor": [
    -122.3974662,
    37.8016046
  ],
  "targetHeightM": 16.4,
  "cat": 25,
  "name": "Pier 15 (Exploratorium)",
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
`docs/asset-plans/pier-15.md`.
````

---

## Part 2 — Research and design dossier

Compiled 19 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify anything it
relies on. Everything marked *measured* was computed in this session from the named dataset
and the arithmetic is reproducible from 2.3 and 2.16.

> **Corrections from the build session (REPORT beats plan):** (1) the expected
> AABB is ~249 x 221 m, not "250 x 178" — a rotation-math slip. (2) The Bay
> Observatory Gallery is **OSM w738027034 on the north apron** (s 83.5-108.6,
> t -45.4..-25.5 in the pier frame), abutting the shed's NW wall line and
> overlooking the courtyard mouth — NOT the k-l-m-n region of the shed way,
> which is shed roof; and the shed runs near-full-width to s ≈ 106.6, so there
> is no deck-level terrace notch. §2.3/2.4/2.7's bay-end description is
> superseded by `artifacts/pier-15/REFERENCE.md` and the rectified-aerial
> verification recorded there. (3) The monitor centreline is t = +9.0.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Name | **Pier 15**; since April 2013 the **Exploratorium** | Port of SF; NPS |
| Address | Pier 15, The Embarcadero at Green Street, San Francisco 94111 | Port of SF; Exploratorium |
| Built | Substructure **1930-1931** (Healy-Tibbitts, $328,600); shed and bulkhead **1931** (E. T. Lesure, $101,569) | National Register nomination, Section 7 |
| Designers (1931) | Plans of 19 Feb 1931, **H. B. Fisher** in charge, under **Frank G. White**, Chief Engineer, BSHC | National Register nomination |
| Historic status | Contributor, **Port of San Francisco Embarcadero Historic District**, National Register | NPS |
| Predecessor | 1915 wood pier with coal bunkers, 90 ft wide, replaced in place | National Register nomination |
| Substructure | Reinforced-concrete piles (1915 creosoted piles reused in concrete jackets), caps and deck; originally **160 ft wide, 794 ft long** | National Register nomination / BSHC 1931 |
| Transit shed (1931) | Steel frame, precast concrete side walls (scored), cast-in-place bulkhead and outer end; **823 ft long, 123 ft wide**; steel rolling doors; steel sash with wire glass | BSHC [1932]:23 via nomination |
| Shed roof | Wood on longitudinal + transverse steel trusses; **central gabled monitor running the full length**; outer aisles low-slope | National Register nomination |
| 1955-1956 widening | Pier widened north; north wall rebuilt to match; Piers 15-17 joined as a quay terminal with a connecting shed and paved "valley" | National Register nomination |
| Rear (east) elevation | "Faintly Art Deco… six profiled piers rising to peaks just slightly above the roofline and a gabled central pavilion" | National Register nomination |
| Bulkhead building (1931) | Timber framed, stucco, classical; broad central pavilion, monumental arched entry, tapering piers, gabled parapet; two flat-roofed bays each side; "Pier 15" raised metal letters above the arch; flagpole on the gable | National Register nomination |
| Bulkhead windows | Steel sash: 25 lights per first-storey window, 9 lights per second-storey window | National Register nomination |
| Exploratorium rehab | 2010-2013, EHDD (project architect), Page & Turnbull (preservation), Rutherford & Chekene (structural), Nibbi Bros (GC); opened **17 April 2013** | Port of SF project sheet; EHDD |
| Rehab scope | 1,126 pilings repaired (3D laser scanned), new mega-piles, new 8" structural slab, seismic upgrade; ~93% of original structure and envelope retained; exterior concrete stripped and left patinated with ghost signage | ENR; AIA Top Ten; Architectural Record |
| Net zero | **1.3-1.4 MW PV array, 5,874 panels, on ~2 acres of roof**; bay-water heat exchange, radiant slabs; LEED Platinum; largest net-zero museum in the US | NPS; retrofit magazine; ENR; HPB |
| Observatory Building | New 2013 glazed 2-storey pavilion at the bay end (replaced the non-historic connector); café below, **Bay Observatory Gallery** above; public Observatory Terrace | Port of SF project sheet; Architectural Record |
| Water courtyard | Valley parking between Piers 15/17 removed; open water + outdoor exhibits; pedestrian bridges | Port of SF project sheet |
| Program | 330,000 sq ft campus; exhibits, two cafés, Kanbar Forum theatre, Tactile Dome, shops, offices; south-apron boat dock (water taxi); ships berth on the east apron | Port of SF; ENR |
| Footprint (pier structure) | OBB **245.0 m x 94.8 m** incl. aprons, area 18,441 m2; shed way 13,301 m2, **251 m x 54.7 m**; long axis bearing **54.9°** | OSM ways 1390720125 / 25478444 reprojected — **measured** |
| Anchor (area centroid) | **-122.3974662, 37.8016046** (pier way centroid, over water) | same polygon — **measured** |
| Deck grade | **3.05 m** above datum (taken from Pier 3's DataSF `gnd_mediancm = 307` on the same seawall; ±0.15 m) | DataSF via pier-3 plan — *transferred* |
| Bulkhead gable crest | **16.4 m** above water (13.3 m above deck) | Street View photogrammetry, camera solve verified two ways — **measured, see 2.16** |
| Arch crown (moulding) | **~11.0 m** above water (8.0 m above grade) | same measurement — **measured** |
| Wing parapet | **~11.0 m** above water (7.9 m above grade) | same measurement — **measured** |
| Monitor ridge | **~13.9 m** above water (10.8 ± 0.8 m above grade) | second pano, ray-intersection vs measured monitor line — **measured, see 2.16** |
| Shed north wall top | **~8.5 m** above water (5.4 m above grade) | same — **measured** |
| Flagpole ball | ~22.6 m above water — **do not model at true height** | same — **measured** |
| Monitor plan offset | Monitor centreline **~7.5 m southeast of today's shed centreline** (over the 1931 central aisle) | rectified z20 aerial vs OSM — **measured** |
| LiDAR record | DataSF `SF9900015`, hgt_max 15.64 m — a **merged polygon covering Piers 15 AND 17**; bound only | pipeline data — **measured** (point-in-polygon confirmed both piers inside) |
| Neighbours | Pier 17 (Overture h 16.4) NW across the courtyard; Pier 9 SE; both procedural today, Pier 9 has a sibling asset branch in flight | OSM/Overture |

### 2.2 Sources

- `https://www.sfport.com/files/2022-12/EmbarcaderoRegisterNominationSec7.pdf` — the National
  Register nomination, Section 7. **The best single source.** Dedicated Pier 15 description
  (pp. 131-135): substructure, shed, monitor, bulkhead composition, windows, signs, the 1955
  widening, the BSHC 1931/1932 construction quotes with dimensions (823 x 123 ft shed,
  794 x 160 ft pier)
- `https://www.nps.gov/articles/pier-15-ca.htm` — NPS summary: 1931, historic tax credits,
  5,874 solar panels, zero-net-energy museum, opened spring 2013
- `https://ehdd.com/project/the-exploratorium-at-pier-15/` — project architect's page:
  206,000 sf program, glass observatory, LEED Platinum Net Zero, awards
- `https://www.sfport.com/sites/default/files/FileCenter/Documents/450-ExplorPROJECT-December2010.pdf`
  — Port project sheet: development team, $205M, scope (Observatory Building replacing the
  connector, water courtyard, boat dock on south apron, ships berth on east apron)
- `https://www.architecturalrecord.com/articles/2831-san-francisco-s-exploratorium-museum-set-to-open-in-its-new-home`
  — Architectural Record: stripped/patinated exterior with ghost signage, redone stucco
  entrance, titanium bay-water heat exchangers, Bay Observatory Gallery and Terrace
- `https://www.aiatopten.org/node/472` — AIA Top Ten: 93% of structure/envelope retained,
  program, no on-site parking, public plaza
- `https://www.enr.com/articles/10645-san-franciscos-exploratorium-puts-sustainability-on-display`
  — ENR: 1,126 pilings, 3D laser scanning, low-decibel vibratory pile drivers, 1.4 MW PV,
  Kanbar Forum, two pedestrian bridges
- `https://retrofitmagazine.com/exploratorium-pier-15-living-laboratory-science-including-innovative-building-technologies/`
  — 1.3 MW PV on ~2 acres of roof, radiant bay-water system
- `https://www.hpbmagazine.org/content/uploads/2020/04/15S-The-Exploratorium-Pier-15-San-Francisco-CA.pdf`
  — HPB case study: east-west 700-ft pier, rooftop monitor, south-tilted low-slope roof
  sized for 1.4 MW PV, new 8" slab, mezzanine, continuous roof insulation
- `https://www.openstreetmap.org/way/25478444` (`building=warehouse`, `name=Pier 15` — the
  shed+bulkhead+observatory outline) and `https://www.openstreetmap.org/way/1390720125`
  (`man_made=pier` — the deck incl. aprons and forecourt). The footprints this plan measures
- Google satellite z20/z21 (Aug 2026 imagery), reprojected into the shed's axis frame — the
  PV bands, walkway seams, cross-platforms, monitor offset, terrace, observatory skylight
- Google Street View official panoramas `kxhcO1Z21OvTtJA4wdYHZg` (The Embarcadero opposite
  the bulkhead, 2025) and `2OZhgFbvl-4wmtDZpfAZcw` (valley gate, 2022) — the sources of the
  height solve in 2.16 and the facade/flank readings in 2.4

### 2.3 Orientation and placement

The pier runs out into the bay on a bearing of **54.9°** from a bulkhead frontage on The
Embarcadero. The frontage runs 144.9°/324.9° and faces **southwest at ~235°**.

Measured footprint polygons, in Blender coordinates (metres, `+X` east, `+Y` north),
already centred on the anchor `-122.3974662, 37.8016046`. Vertices under 2 m apart merged.

**Pier deck (OSM way 1390720125)** — the outline of the whole asset:

```
A  (   65.0,  110.0)   bay-end north corner
B  (   57.8,  105.0)
C  (   59.2,  103.3)
D  (   46.6,   94.2)   observatory NW face
E  (   39.5,   89.0)
F  (   22.1,   72.4)   courtyard notch, NE shoulder
G  (   -2.2,   49.1)   notch diagonal (33.6 m at 226°)
H  (    3.0,   41.9)   small-dock notch
I  (   13.0,   49.0)
J  (   15.0,   46.2)
K  (  -61.8,   -8.5)   NW apron edge along the water courtyard
L  (  -74.1,  -17.0)
M  ( -129.5,  -35.2)   west corner at the seawall
N  (  -77.0, -110.5)   south corner at the seawall (M->N = the 91.8 m frontage line)
O  (  -52.4,  -93.3)
P  (  -56.7,  -87.2)
Q  (  -58.7,  -84.6)
R  (   68.5,    4.9)   south apron edge (Q->R = 155.5 m at 54.9°)
S  (   72.4,   -0.8)
T  (  119.7,   32.8)   east corner (S->T apron continues)
                       T->A = 94.6 m bay-end face at 324.7°
```

**Shed + bulkhead + observatory (OSM way 25478444)**, same frame:

```
a  ( -123.2,  -66.6)   bulkhead front, NW corner
b  ( -107.7,  -87.1)   front mid (a->c = 54.3 m facing 235°)
c  (  -91.8, -110.8)   bulkhead front, SE corner
d..i steps NE: the bulkhead is ~9 m wider than the shed on the SE side
i  (  -54.7,  -75.2)   shed SE wall begins
j  (  108.7,   39.6)   shed SE wall ends (i->j = 199.6 m)
k  (   86.9,   69.9)   bay end face (j->k = 37.3 m at 324.3°)
l  (   83.3,   67.3)
m  (   72.7,   82.3)   Bay Observatory north corner
n  (   54.8,   69.9)   observatory SW face / terrace notch
o..r terrace notch verts; r ( 34.7, 54.5) shed NE-NW corner
s  ( -104.7,  -43.6)   shed NW wall (r->s = 170.5 m)
t..v bulkhead NW steps back to a
```

The shed's two long walls are 54.7 m apart. The monitor centreline lies **7.5 m southeast
of the shed centreline** (the 1931 aisle); in this frame it runs through points offset
+7.5 m along bearing 144.9° from the shed's midline. Because of the 54.9° heading the
axis-aligned bounding box is roughly **250 x 178 m**. That is correct.

### 2.4 What each side shows

**Southwest (The Embarcadero)** — The hero. A symmetrical classical stucco composition:
the broad central pavilion projecting slightly, monumental tapering piers flanking a
semicircular arched entry ~9 m wide, the arch filled with a dark steel-sash fanlight
carrying the **white Exploratorium "O"** (a ring ~4.5 m across mounted on the glazing);
glazed doors below a transom. Above the arch, "**·PIER·15·**" in dark raised letters set in
an arc, then the gabled parapet: raking cornice, small stepped crest block at the apex, and
the flagpole (US flag + Exploratorium house flag). Either side: two-storey flat-roofed wings
(two bays visible north, the wall stepping wider than the shed), tall 25-light steel-sash
windows at grade with circular exhibit graphics visible inside, 9-light windows above, thin
cornice and parapet. Dark vertical banner signs on the piers. The forecourt (part of the
DECK polygon, on the bulkhead wharf) carries an F-line shelter and the Buckyball sculpture —
both out of scope.

**Southeast flank (south apron)** — The public promenade: a wide apron between the shed
wall and the fendered edge, with railings, light standards, benches and the water-taxi
boat dock mid-length. The shed wall above: patinated grey scored precast concrete, roll-up
door bays under a continuous canopy on the shoreward half, a clerestory band of steel-sash
windows near the top. Ships berth alongside — not in the GLB.

**Northwest flank (water courtyard)** — The deck notches inward: open water between Piers
15 and 17, crossed by pedestrian bridges (out of scope — they belong to the courtyard, not
the pier ring). The shed's north wall (1955-6) matches the south in materials: scored
concrete, clerestory band, canopy over the old loading dock with banners. A small
one-storey kiosk sits on the notch deck (in the bake today as an Overture ring; see 2.13).

**Northeast (bay end)** — The Observatory end. The shed's Art Deco outer end (six profiled
piers peaking just above the roofline, gabled central pavilion — keep it low-key but real)
gives onto the east apron; north of the shed end, the open **Observatory Terrace**, then
the two-storey glazed **Bay Observatory Gallery** with its PV roof and square skylight,
reaching the bay-end north corner. Fendered edge, railings, bollards all around.

**Top** — The most important surface: 823 ft of roof read from above. Four longitudinal
dark blue-grey **PV bands** separated by pale walkway seams; **cross-platforms** linking
the seams at four or five stations; the **glazed monitor** riding above the panels, offset
southeast of centre; the bulkhead's separate roof plane at the SW end (partly PV, gable
breaking it at the centre); the observatory's PV roof with its pale square skylight at the
NE end; the pale terrace between. The aprons frame everything in warm concrete.

**Underside** — The asset sits on water and the courtyard makes this pier's soffit MORE
visible than most. Pile field (1931 concrete jackets) and deck soffit from 0 to 3.05 m are
required geometry.

### 2.5 Recognition cues (ranked)

1. **The PV-wrapped roof with its offset glazed monitor** — no other pier in the city reads
   as a quarter-kilometre solar array; from the app's camera this is the identity
2. **The bulkhead pavilion**: gable, "PIER 15" arc, tapering piers, arch with the white
   Exploratorium "O" ring — the street identity and the only elevation most people know
3. **The water courtyard**: open water separating Piers 15 and 17
4. **The Bay Observatory Gallery** — the glazed modern pavilion at the bay end
5. The **long low silhouette** at 54.9° with the gable as the only tall element

### 2.6 Miniature translation

**Preserve**

- The pier at its real 54.9° heading, real 245 m deck, real aprons and courtyard notch
- The pavilion's whole composition: tapering piers, arch, fanlight + "O", lettering, gable,
  crest block
- The four PV bands, the pale seams, three or four cross-platforms, the offset monitor
- The observatory block + terrace + skylight
- The pile field and deck soffit
- The Art Deco east end's gabled centre — one plane of relief, not six modelled piers

**Simplify / exaggerate**

- The **"O" ring is enlarged** to ~5.5 m and modelled as a proud white torus/ring on the
  fanlight — it is the museum's whole graphic identity and the one place the exaggeration
  budget goes. "PIER 15" becomes proud dark letters ~1.1 m tall in an arc; no other text
- Wings: two window bays each side of the pavilion at ~7 m pitch, one flat recessed
  `Toy_glass` panel per bay per storey
- Shed walls: the clerestory band becomes one continuous recessed `Toy_glass` strip; the
  roll-up doors become four recessed bays with canopy slabs on each flank; no scoring
- PV bands: flat panels 0.15 m proud of the roof plane, `Toy_glass` (dark) with the pale
  roof (`Toy_conc`/`Toy_stone`) showing as seams; do NOT model individual modules
- Monitor: one long gabled bar with recessed glazing strips both sides, stopped ~12 m short
  of each end wall
- Piles: chunky 0.9 m square piles on a ~8 m pitch under the visible edge band plus a
  centre spine; cap the count
- Railings: solid low `Toy_steel` ribbon; bollards: chunky blocks on a wide pitch; light
  standards: 5.5 m poles on the south apron and east apron
- The boat dock reduces to a small float + gangway hint on the south apron or is omitted;
  the pedestrian bridges over the courtyard are omitted (they read as courtyard furniture)

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render. **All Z values are above the
water plane, Z = 0.** Use the polygons of 2.3.

1. **Pile field**: 0.9 m square piles, Z 0 → 2.45, `Toy_stone`, ~8 m pitch within 10 m of
   the deck edge plus a centreline spine. Hard cap ~2.5k tris.
2. **Deck slab**: extrude the deck polygon Z 2.45 → 3.05, `Toy_stone`, 0.15 m edge chamfer.
3. **Deck surface**: `Toy_conc` inset 0.4 m at Z 3.05; apron markings as sparing
   `Toy_trim` quads at Z 3.06.
4. **Fender/curb ring**: 0.5 m wide, 0.45 m proud, `Toy_ink`, full perimeter except the
   seawall frontage edge M->N.
5. **Railing ribbon**: 1.1 m tall, 0.12 m thick, `Toy_steel`, along south apron, east
   apron, courtyard notch and terrace edges.
6. **Shed body**: walls from the shed polygon (i->j->k SE/end, r->s NW), Z 3.05 → 8.5,
   `Toy_stone` (patinated pale grey); clerestory strip Z 7.2 → 8.1 recessed 0.15 m,
   `Toy_glass`; four door bays per flank, recessed 0.2 m, `Toy_ink`, with `Toy_steel`
   canopy slabs at Z 6.0 on the shoreward half.
7. **Shed roof**: low-slope planes from the eaves (Z 8.5) rising to the monitor sides
   (Z ~9.6 at the monitor line, 7.5 m SE of the shed midline); `Toy_conc` base plane.
8. **PV bands**: four longitudinal `Toy_glass` slabs 0.15 m proud covering ~80% of each
   roof plane, pale seams between; three cross-platforms `Toy_conc` at even stations.
9. **Monitor**: gabled bar ~8 m wide, sides Z 9.6 → 12.8, ridge **13.9**, on the monitor
   line, stopped 12 m short of each end; sides `Toy_steel` frame with recessed
   `Toy_glassl` strips; small `Toy_glassl` cap-strip on the ridge.
10. **Bulkhead body**: front a->c plus the side steps, 14 m deep, Z 3.05 → 10.4,
    `Toy_cream`; ground-storey window bays recessed `Toy_glass` (tall), upper bays
    (short); thin cornice at 10.4, parapet to **11.0**, `Toy_stone` cap. Roof `Toy_roofd`
    at 10.4 behind the parapet with a few PV quads.
11. **Pavilion**: centred on the front, ~15 m wide, projecting 0.6 m; tapering piers
    (batter the flanking pier faces), wall to Z 11.0; **gabled parapet** raking from 11.0
    to apex **15.9**, raking cornice 0.35 m proud `Toy_stone`; **crest block** 2.0 x 1.0 m,
    Z 15.9 → **16.4** — this sets the bounding-box top exactly.
12. **The arch**: semicircular, 9.0 m span, springing Z 5.5, crown 10.0 (inner), cut into
    the pavilion; voussoir surround 0.7 m wide, 0.25 m proud, `Toy_stone`; reveal
    `Toy_ink`; recessed dark `Toy_glass` fanlight + door band; **the "O"**: a white ring
    (torus or extruded annulus) ~5.5 m outer diameter, 0.45 m tube, `Toy_trim`, proud of
    the fanlight, centred on the arch.
13. **"PIER 15"**: proud dark letters (`Toy_ink`), ~1.1 m tall, arced above the arch at
    Z ≈ 12.3. Simple forms.
14. **Flagpole**: 0.14 m mast on the gable, top at **Z 16.2 — below the crest block**.
15. **Bay Observatory**: block from the m..k region, ~30 x 21 m, Z 3.05 → 12.4;
    `Toy_steel` frame + broad recessed `Toy_glass` bands both storeys (it must read
    glazed); PV quads + pale square skylight (`Toy_glassl`, 0.3 m proud) on the roof.
16. **Observatory Terrace**: deck plane at Z 6.4 between shed end and observatory
    (`Toy_conc`), thin support walls, railing ribbon; one umbrella-sized `Toy_trim` disc
    optional.
17. **East end relief**: the shed's outer end wall gets a central gabled plane 0.2 m proud
    and shallow pier strips — the Art Deco end at miniature scale.
18. **Light standards**: 5.5 m `Toy_ink` poles at ~24 m pitch, south + east aprons.
19. **Bollards**: 0.45 m `Toy_ink` chunks at 12 m pitch on the aprons.
20. Bevel 0.10 m, 2 segments, on primary massing above deck level; skip hairline strips.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette. Verify each name against the shipped
palette at build time; substitute the nearest listed neighbour rather than inventing hexes.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | bulkhead walls, pavilion, gable |
| `Toy_stone` | `#d9d2c2` | cornices, voussoirs, crest block, deck slab, piles, shed walls |
| `Toy_conc` | `#cfc9bd` | deck surface, roof seams, terrace, cross-platforms |
| `Toy_trim` | `#f3efe6` | the "O" ring, apron markings, skylight frame |
| `Toy_glass` | `#2a4d73` | PV bands, fanlight, windows, clerestory strips |
| `Toy_glassl` | `#6f95b8` | monitor glazing, observatory skylight |
| `Toy_roofd` | `#45454a` | bulkhead roof membrane |
| `Toy_steel` | `#9aa0a6` | monitor frame, canopies, railings, observatory frame |
| `Toy_ink` | `#3a3530` | fender curb, reveals, "PIER 15" letters, bollards, poles |
| `Toy_glassl_Glow` | `#6f95b8` | the monitor's glazing strips at night — the hero glow |
| `Toy_amber_Glow` | `#e8b563` | arch fanlight + a warm wash behind the "O"; apron lights |
| `Toy_glass_Glow` | `#2a4d73` | scattered lit windows (observatory + a few bulkhead bays) |

**Night state (required).** Glow surfaces must be thin open shells proud of the opaque
geometry — a closed glow shell reads as two alpha layers by day (~23%) and tints its
facade; and a glow face lying ON a solid reads pale by day, so give each glow its own plate
in front of an opaque pane.

- **Hero glow: the monitor.** At night the real Exploratorium reads as a warm lit strip
  riding the dark roof — the whole pier's line drawn in light. Glow plates on both monitor
  glazing strips.
- **Supporting: the arch fanlight** behind the "O" (amber), so the gateway reads lit from
  the Embarcadero; the "O" itself does NOT glow (it is a daylight graphic).
- **Accent:** the observatory's upper band lit; apron light standards as small amber
  points; six to eight scattered lit windows. The PV panels never glow.

### 2.9 Top surface

The camera looks down at a quarter-kilometre of roof: this asset's top IS its identity.
Keep four cleanly separated fields: (1) the dark PV bands with their pale seams and
cross-platforms, (2) the brighter monitor bar riding above them, slightly off-axis, (3)
the bulkhead's smaller, calmer roof with the gable breaking it, (4) the observatory's
panel-and-skylight roof with the pale terrace beside it. The aprons frame everything in
warm concrete with crisp `Toy_ink` fender edges. Resist decorating the aprons — a working
pier's honesty is the look.

### 2.10 Scope

**In the GLB:** pile field, deck slab and surface with aprons and courtyard notch, fender
curb, railings, bollards, light standards; the bulkhead building with pavilion, arch, "O",
lettering, flagpole (short); the transit shed with clerestories, door bays, canopies, PV
roof, monitor; the Bay Observatory and Terrace; the east-end Art Deco relief.

**Not in the GLB:** The Embarcadero, Herb Caen Way, F-line tracks/overhead/shelter, palm
trees, the Buckyball sculpture, the seawall promenade, Pier 17 and Pier 9, the water
surface, the pedestrian courtyard bridges, the water-taxi float's pontoon (a gangway hint
on the apron is acceptable), any vessel, parked cars, people, plinths, cameras, lights.

### 2.11 Triangle budget

Cap 22,000. Suggested split: pile field ~2.5k (hard cap — thin the grid first); deck,
aprons, curb, markings ~2.5k; railings/bollards/poles ~2k; shed walls, clerestories, door
bays, canopies ~3k; roof planes + PV bands + seams + platforms ~2.5k; monitor ~1.5k;
bulkhead + pavilion + arch + voussoirs ~3k; "O" ring + letters ~1.5k; observatory +
terrace ~2k; east-end relief ~0.5k; glow shells ~1k.

If the budget bites, thin the piles, then the bollard/pole count; the pavilion and the
monitor are last.

### 2.12 Draft manifest entry

```json
{
  "id": "pier-15",
  "file": "pier-15.glb",
  "anchor": [
    -122.3974662,
    37.8016046
  ],
  "targetHeightM": 16.4,
  "cat": 25,
  "name": "Pier 15 (Exploratorium)",
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

- **Case B — new landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: 'pier-15'`,
  `height: 16.4`, `exclude: 70`) and re-bake the affected tiles (cells 22_8, 22_9, 23_8,
  23_9).

- **The exclusion window was measured against `pipeline/data` (19 Aug 2026), min(centroid,
  vertex) per ring after `simplifyRing(0.6)`, from the anchor:**

  | Gate (m) | Ring | Verdict |
  |---|---|---|
  | 13.1 | Overture "Pier 15" h 14.6 (centroid; nearest vertex 74.5) | **must go** |
  | 36.6 | DataSF `SF9900015` h 15.64 — the pier's baked block today (centroid) | **must go** |
  | 61.4 | Overture 6x5 m kiosk (OSM w1323673815) on the courtyard-notch deck | **should go** — orphaned once the pier is ours |
  | 84.9 | Overture "Pier 17" h 16.4 (centroid) | **must stay** |
  | 87.4 | OSM w738027034 — the **Bay Observatory Gallery, on THIS pier's north apron** (corrected: not on Pier 17). Inside the GLB; baked 23 m deep into the deck once SF9900015 dropped | **must go — via `extraExclusions`** |
  | 120.5 | Pier 9 (Overture h 8 / DataSF `SF9900009` h 15.5) | must stay — a sibling asset branch owns it |

  Anything in (61.4, 84.9) that also clears 61.4 works. **70 m** takes the three main "go"
  rings with a 14.9 m margin to Pier 17's gate. Do not exceed 84 m ever. The observatory
  ring gates at 87.4 — past that ceiling — so it is taken by
  `extraExclusions: [{ lon: -122.3968015, lat: 37.8023693, r: 12 }]` centred on its own
  centroid; from THAT centre Pier 17's nearest ring **vertex** is 29.1 m, so r must stay
  under 29.

- **Known, accepted collateral: `SF9900015` is a merged polygon covering Piers 15 AND 17**
  (point-in-polygon verified on both sheds). Excluding it un-bakes Pier 17's block as
  well — and (measured at integration, superseding this plan's earlier prediction)
  **Pier 17's Overture ring does NOT gap-fill**: its diagonal bbox reads 46% occupied in
  the bbox-based occupancy grid (`occupiedFraction 0.464 > 0.25` in
  `pipeline/buildings.mjs`), a pre-existing coarseness triggered by the neighbouring
  piers' own diagonal bboxes. **Pier 17's site bakes empty until a pier-17 asset lands**
  (follow-up task flagged). There is no safe radius that avoids this: ≥ 36.6 m kills the
  merged block, anything less leaves a 15.6 m block through the GLB.

- **Prove the exclusion from the tile, not the radius**: decode the four cells before and
  after the bake and point-in-polygon surviving rings against the deck polygon, reporting
  penetration depth. verify-rebake compares per-cell counts and can mislead in both
  directions (moved-main, sibling batches).

- **Water seating.** The anchor is over open water; the merge line must report y = 0. A
  non-zero seat means the anchor drifted onto the seawall — move it back to the polygon
  centroid, never compensate in the model.

- **Shared-batch budget.** At 245 x 95 m this becomes the largest non-bridge landmark in
  the manifest. The shared landmark `BatchedMesh` reserve was raised to 1.6M after
  overflowing at 1.2M with 89 live landmarks; check the reserve against GLB accessor
  counts before integrating (no browser needed), especially with the pier siblings
  (pier-1, pier-3, pier-9) converging on the same waterfront district.

- Suggested camera preset: `{ distance: 460, yaw: 215, pitch: 20 }` — the southwest
  three-quarter showing the pavilion and the full solar roof at once.

- `loadRadius`: default rule gives `max(2500, 16.4 * 30) = 2500` m. Take the default.

- If/when Pier 17 gets its own asset, revisit the courtyard as a pair — the two piers and
  their bridges are one composition in reality.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0 **and Z = 0 is the waterline**, with pile geometry reaching
      it — not the deck
- [ ] XY center offset within ~2 m (tolerance loosened only because the asset is 245 m
      long; not slack for a misplaced model)
- [ ] Bounding-box top exactly 16.4 m (loader scale 1.0), and the flagpole **below** it
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~250 x 178 m)
- [ ] Triangles at or under 22,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the monitor strips, arch fanlight, observatory band, apron lights and
      scattered windows; all glow shells open plates proud of opaque surfaces
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for
      the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry; **no boats, no bridges, no Buckyball**
- [ ] Six review renders + contact sheet + night render + the low-from-the-water courtyard
      view, all regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **16.4 m is a photogrammetric measurement, not a published figure, and it scales the
  whole asset.** Honest range **15.8-17.0 m** (camera height ±0.3 m, distance ±1 m). It
  comes from one 2025 pano whose position was verified two independent ways (2.16). No
  drawing or survey height for the bulkhead was found. If a better source appears, rebuild
  rather than nudging the crest.
- **The flagpole is a trap.** Its ball tops out ~22.6 m — ~6 m above the crest. Modelled at
  true height it becomes the bbox top and shrinks the 250 m pier by ~27%. Model it short.
- **The monitor ridge (13.9 m) has the widest error bars** (±0.8 m): it was measured at
  150-230 m range where a pixel is ~0.2 m. If the aerial review makes the roof feel too
  tall or too flat against the bulkhead, trust the proportions in the panos over the
  number, within the range 13.1-14.7.
- **The monitor's plan offset (7.5 m SE of centre) is solid** (aerial + 1931 aisle logic
  agree) — do not "fix" it to centred; the asymmetry is real and visible from above.
- **The Bay Observatory's height (12.4 m) and footprint (~30 x 21 m) are inferred** from
  aerial imagery and two-storey logic. It must stay below the gable crest. Re-measure from
  photos if it looks off.
- **The Observatory Terrace level (Z 6.4) is inferred** — public access documents put it at
  the Observatory's 2nd floor, aerial shadows are ambiguous. Range 5.5-7.5 m.
- **The shed wall top measured 8.5 m above water — lower than a classic transit shed.**
  The measurement is consistent across two stations, and the 2013 rebuild kept the
  envelope, so trust it; but if the low three-quarter render reads squat, the honest range
  is 8.2-9.3 m.
- **PV coverage is time-varying** (panels have been added/rearranged since 2013). Model
  the Aug 2026 aerial's four-band layout; do not chase older photos.
- **The Buckyball sculpture ("Buckyball", Leo Villareal) is on the seawall forecourt** —
  deliberately out of scope; it may deserve its own micro-asset someday.
- **Pier 17 stays procedural and changes source** after this lands (see 2.13). Judge the
  courtyard seam in local QA from water level, not only from the aerial.

### 2.16 How the heights were measured

Recorded because none of these numbers has a published source, and the next agent should
attack the method rather than redo it blind.

**Bulkhead (pano `kxhcO1Z21OvTtJA4wdYHZg`, 2025, The Embarcadero at reported
37.8005732, -122.3990326, stitched 8192 x 4096 from zoom-4 tiles, full content extent.)**
The equirect is levelled: horizon = row 2048, elevation = `(2048 - y) x 180 / 4096`°. The
yaw mapping is `heading(x) = (pano_yaw - 180) + 360x/W` with `pano_yaw = 144.285` from the
pano metadata. The reported camera position was verified two independent ways before use:
the pavilion centre's predicted bearing (50.2°) landed on the pavilion's actual column, and
the bulkhead's SE front corner's predicted column (2769) landed on the visible corner
(~2780). Perpendicular distance to the front plane **D = 39.5 m**; a pedestrian at the
doors scales to 1.82 m at that distance (sanity pass).

Rows: gable crest cap y=1712 → 14.77°; arch surround crown y=1880 → 7.38°; wing parapet at
the SE corner y=1907 → 6.19°; facade-base sidewalk y=2142.5 → -4.15°.

With camera 2.5 m above its road and the facade base reading 0.37 m below camera level:
crest = 2.5 + 39.5·tan(14.77°) + 0.37 = **13.3 m above grade**; arch crown **8.0 m**; wing
parapet (at 46.2 m corner distance) **7.9 m**. Deck grade 3.05 m above datum (Pier 3's
DataSF ground value on the same seawall) gives **16.4 / 11.0 / 11.0 m above water**.
Flagpole ball at 22.88° → 19.2 m above road → ~22.6 m above water.

**Shed monitor (pano `2OZhgFbvl-4wmtDZpfAZcw`, 2022, valley gate at 37.8012824,
-122.3996591, yaw 144.154.)** The monitor's plan line was first measured from Aug-2026
Google z20 imagery rectified into the shed's axis frame: monitor centreline 7.5 m SE of
the shed centreline (and the shed 54.7 m wide, matching OSM). Sight rays at three pano
columns were intersected with that line in plan (ranges 153-226 m), giving ridge heights
10.9-11.2 m above street at two stations and 10.1 at the farthest (pixel-limited);
adopted **10.8 ± 0.8 m above grade → 13.9 m above water**. The same construction against
the NW wall plane (ranges 105-140 m) gives the wall top at **5.4 m above grade → 8.5 m
above water**. Cross-check: the National Register nomination's monitor-over-central-aisle
description and the 1955 widening explain the offset; the HPB case study's "south-tilted
low-sloped roof" matches the PV planes rising toward the monitor.
