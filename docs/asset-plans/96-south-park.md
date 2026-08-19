# 86–96 South Park — SF-SIM asset plan

A 1996 live/work loft building by **Levy Design Partners** (Toby S. Levy, FAIA) on the
**corner of South Park and Jack London Alley** — the architect's own building, four
residential units over two commercial spaces, framed entirely in lightweight steel and
assembled from a deliberately mixed vocabulary of materials chosen to "age gracefully".

It is the only piece of *authored* modern architecture in the South Park set. Everything
else on the oval is a warehouse conversion, an Edwardian hotel, a 25-foot row building or a
tech re-skin; this one is a designed collage of overlapping cubic volumes — dark glazed
blue-grey brick, ribbed galvanized metal, bronze-brown panel — cut by a **rust-orange
perforated steel gate**, banded by a **stripe of coloured mosaic tile**, and crowned by a
**ribbed metal cylinder** that rises above the roofline. San Francisco Heritage calls it a
loft building with "an ambiguated facade of cubic forms".

It is also, unusually for this row, a **three-sided building**: South Park on the southeast
front, Jack London Alley down the whole 30 m southwest flank, Taber Place at the rear. Only
the northeast wall is a party wall (with 84 South Park). The app's camera will see three
elevations and the roof, and all three elevations are photographed.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/96-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `96-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3941704, 37.7818909` (axis-aligned bbox centre of the modelled footprint) |
| Target height | **13.7 m** to the top of the rooftop cylinder — LiDAR-derived maximum; main parapet 11.3 m, rear block 12.4 m (see 2.1 and 2.15) |
| Footprint | 14.44 m (South Park frontage, SE) x 30.06 m deep lot; 378 m2 modelled (full lot less a rear-northeast yard), measured |
| Triangle cap | 11,000 |
| Category | `2` (apartments) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 86–96 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 86–96 South Park (Levy Design Partners, 1996) in
San Francisco and deliver it as a downloadable, validated GLB.

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
7. `artifacts/181-south-park/` — the closest reference implementation for the *build
   machinery* (footprint-driven prisms, `face_panel` openings, ring bands, the bevel
   budget)
8. `artifacts/102-south-park/` — the closest reference for a South Park building whose
   front is its hero elevation, and for the night-glow treatment of a lit ground floor
9. `docs/asset-plans/96-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules. Do not invent a new style and do not copy visual
instructions from unrelated prompts.

## Must capture

- The **corner condition**. This is not a row building. South Park is the front, Jack
  London Alley runs the full 30 m southwest flank, Taber Place closes the rear, and only
  the northeast wall is shared (with 84 South Park). Three elevations are real and must be
  designed; the model will be looked at from all of them.
- The **collage of overlapping cubic volumes** — the building's whole idea. Volumes step
  forward and back and change material at every seam: a dark glazed-brick base block, a
  ribbed-metal upper block, a bronze-brown box cantilevered over the alley corner, a
  gabled metal volume behind the front parapet. Nothing lines up, and that is deliberate.
- The **rooftop cylinder** — a vertical-ribbed metal drum on the southwest half of the
  roof, rising above every parapet to 13.7 m. It is the single most identifiable thing
  about this building from the air, and the app's camera looks down. Draw it big.
- The **rust-orange perforated steel gates** — one on the South Park front between the "88"
  and "86" numbers, one on the Jack London Alley flank at "94/96" with a short flight of
  steps. In a building of greys, browns and blue-blacks these are the only saturated
  elements. They are the identity accent (§9 semantic scale): widen and brighten them.
- The **mosaic tile band** — a continuous horizontal stripe of small coloured squares
  (blue, teal, green, violet) set into the dark glazed brick at roughly sill height,
  running the whole length of the alley elevation and returning onto the front. It is a
  1-pixel detail at city scale, so draw it as one clean band of one colour with a hint of
  variation, not as tiles.
- The **dark glazed blue-grey brick base** against **ribbed silver-grey metal above**. Two
  materials, one dark and one light, split roughly at the second floor. This is the
  building's value structure and it must survive simplification.
- The **projecting window boxes and their thin metal railings** on the front and alley
  elevations — small cantilevered bays with steel-framed multi-pane windows, several with
  fold-out metal window hoods.
- The **recessed barrel-soffit archway** at the southwest end of the South Park front —
  the deep vehicular/pedestrian opening with a curved ceiling, one of two ground-floor
  voids on the frontage.
- The **rooftop steel pergola** over the terrace at the northeast end of the front block,
  with planting in it.
- The **rear-northeast yard**: the lot is not fully built. Roughly 6.4 x 8.7 m at the
  Taber Place / 84 South Park corner is open. The roof reads as an L, not a rectangle.

## Research 86–96 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation, and
gather references covering:

- The southeast (South Park) front — well photographed, Google Street View Jan 2025
- The southwest (Jack London Alley) flank — well photographed, Street View Jan 2025 and
  Feb 2021; this is where the cylinder and the mosaic band read best
- The northwest (Taber Place) rear, for which nothing was found
- Aerial and roof views — the roof description in 2.9 is read off satellite imagery only
- Day and night appearance
- **Whether the rooftop cylinder is a drum, a half-drum or a curved wall**, where exactly
  it sits, and how far it rises — see 2.15, this is the plan's biggest single risk
- Whether the rear-northeast corner of the lot is really unbuilt (2.15)
- Any published photograph of the finished building by the architect. LDP Architecture's
  own site (ldparchitecture.com) and Architizer both carry the project but neither served
  usable images to the tooling used for this dossier; a human with a browser will do
  better, and the architect's own photographs would settle every open question here.

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**One source conflict is already known and is NOT resolved (see 2.15):** Architizer
credits the building to **LDP Architecture, Inc.**; San Francisco Heritage credits **Levy
Art + Architecture**. These are the same practice under two names — Toby Levy's firm has
traded as Levy Design Partners, Levy Art + Architecture and LDP Architecture — but no
source was found that states the firm name as it stood in 1996. Do not put a firm name in
the manifest.

## Create a reference dossier

Write `artifacts/96-south-park/REFERENCE.md` containing: source links and what each
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

This is a **secondary building** in the style bible's detail budget (§21) — but a rich one,
and it gets a larger triangle cap than its neighbours (11,000 against their 3-8k) because
it genuinely has three designed elevations and a curved roof element. Spend the extra
budget on the cylinder, the volume seams and the two orange gates. Do not spend it on
window count.

Note the specific style risk here: the real building is a *collage*, and a collage
simplified badly becomes visual noise — a grey lump with random dents. The discipline is to
resolve it into **four or five volumes with hard seams**, each one flat-coloured, and let
the seams do the work. If a step is smaller than about 0.6 m, delete it rather than model
it. Contrast between adjoining volumes matters more than the number of volumes.

The finished asset must be immediately recognizable as 86–96 South Park, consistent with
the real building from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and never
accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building on parcel 3775/116–121 (the condominium lots addressed 86–96
South Park): body volumes, parapets, all three exposed elevations' openings plus the party
wall, both orange gates, the storefronts, the rooftop cylinder, the pergola and the roof
deck.

Do not include unrelated surrounding city geometry: South Park (the oval, its lawn, paths
or play structure), South Park Street, Jack London Alley, Taber Place, Bryant Street,
84 South Park or any other neighbouring building, street trees (the pleached trees in front
of this building are prominent in every photograph and must **not** be modelled), the
sidewalk, parked cars, construction fencing, people, plinths, cameras or lights. Temporary
context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms; no
negative scales; outward normals; no duplicate or foreign geometry; no image textures; no
transparency; flat-color materials named `Toy_*` from the project palette; `_Glow` suffix
only on surfaces that glow at night; no `Toy_body`; no cameras, lights, animations,
armatures or constraints; no external dependencies; at most 11,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric` in
`app/src/assets.js` only scales and positions). The South Park entrance front faces
**southeast, outward normal 135.1°**; the building is rotated roughly 45° off the world
axes, so build directly on the measured footprint polygon in 2.3 rather than modelling an
axis-aligned box and rotating it. This is the case the plans README calls out: the
contract's "front faces −Y" rule cannot be honoured literally here, real-world orientation
wins, and the deviation must be recorded in `REPORT.md` along with the measured heading.

**Height normalization:** the tallest geometry in the export — the top of the rooftop
cylinder — must land at exactly the height you verify (this plan's figure is **13.7 m**) so
the loader's `targetHeightM / measuredHeight` scale is 1.0. If your research moves the
height, move both the model and the draft manifest entry together and say so in
`REPORT.md`.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/96-south-park/build_96_south_park.py` (deterministic build script),
`artifacts/96-south-park/96-south-park.blend`, and
`artifacts/96-south-park/96-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras: `96-south-park-top.png`,
`96-south-park-north.png`, `96-south-park-east.png`, `96-south-park-south.png`,
`96-south-park-west.png`, plus `96-south-park-contact-sheet.png`, at least one high
three-quarter aerial beauty render `96-south-park-aerial.png`, and a night render
`96-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the cylinder, the rear-northeast yard notch, the pergola and the
parapet steps; the aerial view uses the style bible's camera assumptions (30-50 degrees
down, long lens) and should be taken from the **south** so it shows the front and the alley
flank together. Simple tabletop lighting, neutral warm background, minimal depth of field,
and every image must depict the same exported model.

For the night render, drive the `_Glow` materials from Base Color (copy `Base Color` into
`Emission Color`, strength 1.0) — see the note at the end of `docs/asset-plans/README.md`.
A re-imported GLB's `_Glow` materials otherwise render as white slabs.

## Validate the exported GLB

Re-import `96-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count, camera
count, light count, animation count, applied-transform status, negative-scale status,
normal-orientation status, unexpected geometry, and per-material contract compliance.
Render at least one review image from the re-imported asset. Write
`artifacts/96-south-park/validation.json` and `artifacts/96-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **31.5 x 27.0 m** even though the
building is 14.44 x 30.06 m — that is the expected consequence of a ~45° real-world
heading, not a scale error. The anchor in 2.12 is the **bbox centre**, not the lot centroid,
precisely so that the contract's "centered in x/y" rule holds exactly despite the L-shaped
plan; keep the model's origin there.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "96-south-park",
  "file": "96-south-park.glb",
  "anchor": [
    -122.3941704,
    37.7818909
  ],
  "targetHeightM": 13.7,
  "cat": 2,
  "name": "86–96 South Park",
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
`docs/asset-plans/96-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* or *estimated*
are visual or derived, not published figures — the executing agent must re-verify anything
it relies on. Unlike the rest of the South Park set this building **does** have published
architectural provenance (an architect, a firm statement, a heritage-survey mention), but
no published photographs reached the tooling used here: the visual evidence is Street View
and satellite imagery.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 96 South Park is one address in a range signed **86–96 South Park**; the alley elevation carries "94" and "96". Google writes "96 S Park St" | SF EAS address point; DataSF parcel `from_address_num` 86 / `to_address_num` 96; Street View wall numbers |
| Block / lot | 3775 / **116, 117, 118, 119, 120, 121** — six condominium lots sharing one 435 m2 parcel footprint; the EAS record for "96 SOUTH PARK" points at lot **119** | DataSF parcels `acdm-wktn`; DataSF EAS `ramy-di5m`; DataSF building footprint `mblr = SF3775116` |
| Built | **1996** | SF Assessor `year_property_built` (rolls 2024–2025); SF Heritage "In 1996, Levy Art + Architecture created a loft unit building…" |
| Architect | **Toby S. Levy, FAIA** — the practice appears as Levy Design Partners / Levy Art + Architecture / LDP Architecture | Architizer project page (LDP Architecture); SF Heritage (Levy Art + Architecture) — **naming unresolved, see 2.15** |
| Programme | **four residential units and two commercial spaces**, on a corner site | Architizer project description (the firm's own text) |
| Structure & materials | "framed entirely in lightweight steel"; "all construction materials incorporated non-toxic, renewable, and recycled materials" | Architizer project description |
| Design intent | "flexibility of space, hierarchical organization, and overlay of geometries reflecting the position of the buildings on the site"; "an ambiguated facade of cubic forms" | Architizer; SF Heritage, *The Rise of Modern SOMA* |
| Property class / use | "Live/Work Condominium" (`LZ`) per unit | SF Assessor secured roll, block 3775 lot 119, rolls 2024–2025 |
| Unit area (lot 119 = "96") | 2,262 sq ft (210 m2) | SF Assessor `property_area`; BlockShopper mirrors the same figure |
| Owners of record | Toby S. Levy and Rick A. Holman (family trust) — the architect lives in her own building | BlockShopper public property records for 94 and 96 South Park Avenue |
| Current commercial tenants | **645 Ventures** (registered at 96 South Park), OpenMind | California LP filings via bizprofile.net; Google Maps POI labels on this footprint |
| Site condition | **corner lot** — South Park (SE front), Jack London Alley (SW flank, full 30 m), Taber Place (NW rear), party wall with 84 South Park (NE) | DataSF street centrelines: Jack London Aly at 13.4 m southwest of the lot centreline, Taber Pl at 18.1 m northwest — **measured** |
| Parcel / lot | 14.44 m (South Park frontage) x 30.06 m deep, 434.1 m2 | DataSF surveyed parcel `3775119` reprojected — **measured** |
| Built footprint (LiDAR) | 289.7 m2 in two rings: 208.7 m2 over the front and northeast, 81.0 m2 over the rear southwest | DataSF LiDAR building footprints `SF3775116` (`201006.0022147`, `201006.0149656`) — **measured** |
| Roof height, front block, 2010 LiDAR **median** | **11.15 m** (majority 9.49 m, mean 10.99 m, σ 1.51 m) | DataSF `hgt_median_m` on `201006.0022147` — measured |
| Roof height, front block, LiDAR **maximum** | 13.28 m | DataSF `hgt_maxcm` — measured |
| Roof height, rear block, 2010 LiDAR **median** | **12.32 m** (majority 9.86 m, mean 11.72 m, σ 1.56 m) | DataSF `hgt_median_m` on `201006.0149656` — measured |
| Roof height, rear block, LiDAR **maximum** | **13.73 m** | DataSF `hgt_maxcm` — measured; taken as the crest, see 2.15 |
| Ground elevation | 10.5–11.0 m (NAVD88) | DataSF `gnd_median_m` on the two rings — the app's terrain handles this, not the asset |
| Storeys | **4** on the alley elevation (assessor reports `number_of_stories = 0` for condominium lots and is useless here) | OSM `building:levels=4` on way/113545691; confirmed by the Jan 2025 and Feb 2021 panos |
| Frontage heading | front faces 135.1° (SE, toward the park); alley flank 225.2°; rear 315.1°; party wall 45.2° | measured from the surveyed parcel polygon |
| OSM tagging | modelled as **two** ways, neither addressed 96: way/113545685 (untagged, 116 m2, the front-northeast piece) and way/113545691 (`92 Jack London Alley`, `building=apartments`, `building:levels=4`, 184 m2, the southwest strip). Neither carries a `height`. Do not inherit either. | OSM — **both are copies of this building and both must be excluded at bake time, see 2.13** |

### 2.2 Sources

- `https://data.sfgov.org/resource/ramy-di5m.json` (DataSF Enterprise Addressing System),
  record `423704-643402-467048` — "96 SOUTH PARK", parcel 3775119, `-122.394155, 37.781911`
- `https://data.sfgov.org/resource/acdm-wktn.json` (DataSF Parcels), `blklot=3775119` and
  the block-3775 set — the 86–96 address range, the six condominium lots, the surveyed
  14.44 x 30.06 m polygon
- `https://data.sfgov.org/resource/ynuv-fyni.json` (DataSF Building Footprints,
  LiDAR-derived), records `201006.0022147` and `201006.0149656`, both `mblr = SF3775116` —
  the two footprint rings and all four height figures
- `https://data.sfgov.org/resource/wv5m-vpq2.json` (SF Assessor Historical Secured Property
  Tax Rolls), block 3775 lot 119, rolls 2024–2025 — 1996, Live/Work Condominium, 2,262 sq ft
- https://architizer.com/projects/86-96-south-park/ — LDP Architecture's own project page:
  four residential units, two commercial spaces, corner site, lightweight steel frame,
  non-toxic/renewable/recycled materials, "overlay of geometries"
- https://www.sfheritage.org/heritage-in-the-neighborhoods/the-rise-of-modern-soma/ — San
  Francisco Heritage: "In 1996, Levy Art + Architecture created a loft unit building with
  an ambiguated facade of cubic forms on South Park street where Georgian townhouses had
  stood before the 1906 earthquake and fire."
- https://architizer.com/firms/levy-design-partners/ and
  https://www.ldparchitecture.com/about-leadership.html — the practice: founded 1979 by
  Toby S. Levy, FAIA, ten people, woman-owned
- https://wagnercreative.medium.com/women-in-architecture-417087bc461a — interview with
  Toby Levy; "how she became the mayor of South Park"
- https://www.alamy.com/toby-levy-an-architect-that-has-lived-in-south-park-since-1985-in-her-neighborhood-park-in-san-francisco-calif-on-friday-april-9-2010-...-image527446798.html
  — SF Chronicle photograph, 9 April 2010, caption: "The multi use building at left was her
  design built 15 years ago" (i.e. 1995/96), located in South Park
- https://blockshopper.com/ca/san-francisco-county/san-francisco/property/3775119/96-south-park-avenue
  and `/3775118/94-south-park-avenue` — ownership (Levy / Holman family trust), unit areas
- https://www.bizprofile.net/principal-address/96-south-park-san-francisco-ca-94107 — five
  645 Ventures limited partnerships registered at 96 South Park
- https://www.loopnet.com/Listing/90-96-S-Park-St-San-Francisco-CA/34831293/ and
  https://property.compstak.com/96-South-Park-Street-San-Francisco/p/351471 — the building
  marketed as live/work loft space; CompStak calls it a class-B office of 5,000 SF
- https://www.openstreetmap.org/way/113545685 and
  https://www.openstreetmap.org/way/113545691 — the two OSM footprints over this parcel
- https://www.openstreetmap.org/way/113545687 — 84 South Park, the attached northeast
  neighbour (`height=11`)
- Google Street View, **South Park pano, capture January 2025** — the southeast front at
  three headings and two zooms; the wall numbers "88" and "86"; the orange front gate
- Google Street View, **Jack London Alley panos, captures January 2025 and February 2021** —
  the southwest flank; the wall numbers "96" and "94"; the orange alley gate and its steps;
  the mosaic tile band; the ribbed metal cylinder
- Google Street View, **South Park user photosphere, April 2017 (Eric Arneson)** — the front
  at distance from inside the oval, showing the rooftop pergola against the sky
- Google Maps satellite, 2026 Vexcel imagery — the roof described in 2.9; the "645
  Ventures" and "OpenMind" POI pins in that view are what confirm which roof belongs to
  this address
- DataSF street centrelines (`streets_datasf.geojson`, the bake's own input) — the
  corner-lot geometry in 2.3

Exa searches run: `96 South Park San Francisco live/work loft building`;
`Toby Levy Architecture 86-96 South Park San Francisco live work loft facade photos`. The
first returned the Architizer and SF Heritage pages that establish the provenance; the
second returned the practice's history but **no photographs of the finished building**.
Both Architizer and ldparchitecture.com carry image galleries that did not render to text
extraction — a human with a browser is the missing step, see 2.15.

### 2.3 Orientation and placement

The building occupies the whole corner of **South Park and Jack London Alley**, on the north
rim of the oval near its east end. Measured against the bake's own street centrelines, in
lot coordinates (`s` across the frontage, positive northeast; `t` into the depth, positive
away from the park; both metres from the lot centre):

| Feature | Position | Note |
|---|---|---|
| South Park centreline | `t = -21.1` | 6.1 m beyond the front property line at `t = -15.03` |
| Jack London Alley centreline | `s = -13.4` | 6.2 m beyond the southwest property line at `s = -7.22` |
| Taber Place centreline | `t = +18.1` | 3.1 m beyond the rear property line at `t = +15.03` |
| 84 South Park | `s > +7.22` | attached, party wall, no gap |

That is what Architizer means by "corner site", and it is why the building is articulated
on three sides instead of one.

Like the whole SoMa grid it is rotated 45° from the world axes; South Park's own long axis
runs at bearing 45°.

**Modelled footprint** in Blender coordinates (metres, `+X` east, `+Y` north), origin at the
anchor `-122.3941704, 37.7818909` — the axis-aligned bounding-box centre, chosen so the
contract's "centered in x/y" rule holds exactly on an L-shaped plan:

```
(  5.479, -13.475)   ( 15.729,  -3.305)   (  0.680,  11.811)
( -3.877,   7.289)   (-10.036,  13.475)   (-15.729,   7.827)
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(5.479,-13.475) -> (15.729,-3.305)` | 14.44 m | SE 135.1° | **South Park front** |
| `(15.729,-3.305) -> (0.680,11.811)` | 21.33 m | NE 45.2° | party wall with 84 South Park, **blind** |
| `(0.680,11.811) -> (-3.877,7.289)` | 6.42 m | NW 315.1° | faces the rear yard |
| `(-3.877,7.289) -> (-10.036,13.475)` | 8.73 m | NE 45.2° | faces the rear yard |
| `(-10.036,13.475) -> (-15.729,7.827)` | 8.02 m | NW 315.1° | **Taber Place rear** |
| `(-15.729,7.827) -> (5.479,-13.475)` | 30.06 m | SW 225.2° | **Jack London Alley flank**, fully exposed |

The rear-northeast **6.42 x 8.73 m** rectangle of the lot is left open — a yard or deck at
the Taber Place / 84 South Park inside corner. This is read from the LiDAR footprints, not
from a photograph; see 2.15.

Because of the ~45° heading the axis-aligned bounding box is ~31.5 x 27.0 m. That is
correct.

Sanity check on the anchor: the lot's own area centroid projects to
`-122.3941704, 37.7819114`, and DataSF's independent EAS address point for "96 SOUTH PARK"
sits at `-122.3941549, 37.7819114` — 1.4 m apart. The published anchor is 2.26 m southeast
of both, by construction (see above).

### 2.4 What each side shows

**Southeast (South Park front), 14.44 m** — Three overlapping volumes across a narrow
frontage, reading left (southwest, at the alley corner) to right (northeast, at the party
wall):

- *Southwest third*: a **bronze-brown / rust-coloured clad volume** at the alley corner,
  with a full-height narrow vertical strip of the same colour at the very corner. A
  projecting box bay at second floor with a thin steel railing in front of it. At ground, a
  very large pale storefront window in a dark frame, and beside it the **recessed archway**
  — a deep opening about 3.5 m wide with a **curved barrel soffit**, giving onto the
  building's inner circulation.
- *Middle*: **dark glazed blue-grey brick**, running from the pavement to the second-floor
  sill, with the **mosaic tile band** at about 2.7 m turning the corner from the alley. The
  wall numbers **88** and **86** are painted on it. Between them, the **rust-orange
  perforated steel gate**, a tall narrow slot roughly 1.1 m wide and 2.6 m high, set in a
  reveal. Above the brick, a steel-framed window wall of four-pane sashes with external
  guard rails and planters on the sills.
- *Northeast third*: **light ribbed metal panel** with large steel-framed windows, and
  behind the parapet a **gabled metal volume** whose ridge is visible from the street. At
  roof level, an open **steel pergola** frame over a terrace, with agave and other planting
  in it.
- The parapet line steps: lower over the middle, higher over the northeast, with the gable
  and pergola above it.

**Southwest (Jack London Alley flank), 30.06 m** — The best-photographed elevation and the
one that carries the building's character. Two clear horizontal registers:

- *Base, ground to ~4.5 m*: **dark glazed blue-grey brick** in running bond over a plain
  grey concrete plinth, with the **mosaic tile band** — a continuous stripe of small
  coloured squares, blue / teal / green / violet, three or four courses of them — running
  the full 30 m at about 2.7 m. Openings are sparse and tall: a garage door at the Taber
  Place end, two or three narrow steel-framed windows, a dark recessed doorway, and the
  second **rust-orange perforated steel gate** at "94/96" reached by a short flight of
  steps. The numbers **96** and **94** are painted on the brick either side of it.
- *Upper, ~4.5 m to the parapet*: **light ribbed / corrugated galvanized metal panel**,
  broken by bronze-brown flat panels around some windows, angular projecting bays, and a
  shed-roofed volume. Windows are large, steel-framed, irregularly placed — the "overlay of
  geometries" is at its most visible here.
- Rising above the parapet on the southwest half, the **vertical-ribbed metal cylinder**.

**Northeast (party wall with 84 South Park), 21.33 m** — Attached for its whole length to
84 South Park (LiDAR median 11.36 m), so the two buildings are within ~0.2 m of the same
height and almost none of this wall is visible. *Inferred*: blank, in the same ribbed metal
above and brick below, no openings on the shared plane.

**Northwest (Taber Place rear), 8.02 m plus the two yard faces** — No photography found.
*Inferred*: a service elevation — a garage or roll-up door, a personnel door, and a plain
rhythm of small openings above, in the same two materials. The two faces onto the rear yard
get the same treatment plus a few larger windows, because a yard is worth looking into.

**Top** — See 2.9. Well evidenced from satellite; the cylinder is the event.

### 2.5 Recognition cues (ranked)

1. The **ribbed metal cylinder** on the roof — nothing else in the manifest has one, and it
   is the first thing the app's downward camera meets
2. The **two rust-orange perforated gates**, one per street elevation, on an otherwise
   grey-brown building
3. The **dark glazed blue-grey brick base with a coloured mosaic stripe**, wrapping the
   corner and running 30 m down the alley
4. The **collage of stepped cubic volumes in three materials** — brick, ribbed silver
   metal, bronze-brown panel — with no two seams aligned
5. The **corner condition itself**: a 14 x 30 m building with three exposed faces on a rim
   of party-wall row buildings
6. The **rooftop pergola** over the front terrace, and the **gable** behind the front parapet

### 2.6 Miniature translation

**Preserve**

- The three-sided corner condition and the real 45° heading
- Four or five volumes with hard seams and a genuine material change at each
- The dark base / light top value split
- The cylinder, the two orange gates, the mosaic band
- The rear-northeast yard notch, which is what makes the roof an L

**Simplify / exaggerate**

- The cylinder is **enlarged**: 4.6 m diameter rather than the ~3.5–4 m it looks in the
  panos, and its vertical ribs become 16 flat facets — a faceted drum reads as a cylinder at
  diorama scale and costs a fraction of a smooth one
- Both orange gates are **widened to ~1.4 m and brightened** past the real rust colour.
  The perforation pattern is dropped; the gate is one flat saturated plane in a dark reveal
- The mosaic band becomes **one continuous 0.30 m band** of a single teal-blue, projecting
  0.03 m, with no individual tiles. At city scale the stripe is the detail
- The window boxes become four or five projecting slabs with a single railing bar each;
  the fold-out hoods disappear
- The barrel soffit of the front archway becomes a **five-segment arch**, not a smooth one
- Flank openings become a deliberate irregular rhythm of six to eight tall openings, not a
  survey of the real ones
- Every step smaller than 0.6 m is deleted. The real building has dozens; the model gets
  the four or five that change the silhouette
- Roof clutter becomes the cylinder, the pergola, one stair bulkhead and two vents

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render, and adjust *all* of them if the
verified height differs from 13.7 m. Positions are given in lot coordinates `(s, t)` as
defined in 2.3, because that is the frame the building was actually designed in; convert
with `X = 0.70988 s - 0.70552 t`, `Y = 0.70432 s + 0.70868 t`.

1. **Front block**: the footprint region `s -7.22..+7.22`, `t -15.03..+0.90`, extruded
   z=0 to **z=11.30**, `Toy_steel_l` (the light ribbed-metal body colour). This is the
   building's main mass.
2. **Northeast wing**: `s +0.80..+7.22`, `t +0.90..+6.30`, z=0 to **z=11.30**, same
   material. Merges with (1) into an L.
3. **Rear southwest block**: `s -7.22..+0.80`, `t +0.90..+15.03`, z=0 to **z=12.40**, same
   material. The 1.1 m step between (1) and (3) is one of the four seams that matter.
4. **Brick base**: a ring band following the whole footprint from z=0 to **z=4.50**,
   projecting 0.10 m, `Toy_slate` — the dark glazed brick. This is the value split and it
   must go all the way round, including the party wall and the yard faces.
5. **Mosaic band**: a ring band z=**2.60–2.90**, projecting 0.13 m, `Toy_teal`, on the
   South Park front and the Jack London Alley flank only (it stops at the party wall and at
   the rear). One flat colour.
6. **Bronze corner volume**: `s -7.22..-2.60`, `t -15.03..-9.50`, from z=4.50 to
   **z=11.30**, `Toy_bronze`, projecting 0.25 m proud of the front block. This is the
   southwest third of the front elevation and the alley corner.
7. **Front archway**: a recess 3.5 m wide x 3.6 m high, 1.6 m deep, centred at `s -4.6` on
   the front face, with a **five-segment barrel soffit**; reveal `Toy_ink`, soffit
   `Toy_trim`.
8. **Front storefront**: one window 3.4 x 2.7 m at z=0.55–3.25, centred at `s +1.0`; frame
   `Toy_ink`, glass `Toy_glass`.
9. **Front orange gate**: 1.40 m wide, z=0–2.70, at `s +3.6`, recessed 0.25 m,
   `Toy_orange`, reveal `Toy_ink`.
10. **Front upper glazing**: two bands of steel-framed windows, z=5.10–7.40 and
    z=7.90–10.20, each divided into three lights across the northeast two-thirds of the
    frontage; frames `Toy_ink`, glass `Toy_glass`. Two of them get a projecting box bay
    0.45 m deep with a single railing bar in `Toy_steel`.
11. **Front gable**: a gabled prism over `s +1.5..+7.22`, `t -15.03..-10.00`, eave at
    z=11.30, **ridge at z=13.00**, `Toy_steel_l`, ridge running parallel to the frontage.
12. **Rooftop pergola**: an open frame 4.4 x 3.4 m over the terrace at `s +2.0..+6.4`,
    `t -9.0..-5.6`; four posts 0.16 m square, a top grid of five members, top face at
    **z=12.90**, `Toy_ink`. Two planter boxes 0.9 x 0.9 x 0.5 m in `Toy_verdigris`.
13. **Alley elevation**: six tall openings 1.05 x 2.55 m in the brick base at irregular
    spacing along `t -13..+14`; one garage door 3.2 x 2.9 m near `t +12`; the second orange
    gate 1.40 m wide, z=0.60–3.30 at `t -1.5` with a three-step stoop in `Toy_stone`. Above
    the base, seven openings 1.5 x 2.1 m across the two upper floors, three of them in a
    projecting bronze panel 0.20 m proud, `Toy_bronze`.
14. **Rooftop cylinder**: a 16-sided prism, **diameter 4.6 m**, centred at `(s -4.4,
    t +2.6)`, from z=8.00 up to **z=13.70**, `Toy_steel_l`, with a flat cap in `Toy_steel`.
    The bottom is buried inside the rear block; only the top 1.3 m stands clear of that
    block's 12.40 m parapet. **Its cap is the bounding-box top and must land exactly on
    13.70 m.**
15. **Parapets**: ring bands 0.28 m thick with a `Toy_steel` coping — z=11.30–11.75 on the
    front block and northeast wing, z=12.40–12.85 on the rear block.
16. **Roof decks** at z=11.30 and z=12.40, `Toy_ash`. One stair bulkhead 2.4 x 2.0 m from
    12.40 to 13.30 `Toy_steel_l`; two vents 0.5 x 0.5 x 0.7 m `Toy_steel`.
17. **Rear (Taber Place) and yard faces**: a roll-up door 3.0 x 3.0 m, a personnel door
    1.0 x 2.3 m, and five 1.0 x 1.5 m openings spread over the upper floors.
18. **Party wall (northeast)**: blank. No openings.
19. Bevel 0.12 m / 2 segments on the masses, 0.05 m / 1 segment on the applied frames and
    bands, none on fills, glow shells, the cylinder facets or the pergola members.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_steel_l` | `#b9bec4` | the ribbed-metal body of every volume, the cylinder, the gable, the stair bulkhead |
| `Toy_slate` | `#39434f` | **the dark glazed blue-grey brick base**, all round |
| `Toy_teal` | `#3f7f86` | **the mosaic tile band** — one flat stripe |
| `Toy_bronze` | `#7a5f4a` | the bronze-brown corner volume and the alley panel |
| `Toy_orange` | `#d4622a` | **both perforated steel gates** — the identity accent |
| `Toy_glass` | `#2a4d73` | all glazing |
| `Toy_ink` | `#3a3530` | window frames, reveals, doors, the pergola frame |
| `Toy_steel` | `#9aa0a6` | parapet copings, railings, vents, the cylinder cap |
| `Toy_trim` | `#f3efe6` | the archway soffit |
| `Toy_stone` | `#d9d2c2` | the concrete plinth and the alley stoop |
| `Toy_ash` | `#c8c4bc` | roof decks |
| `Toy_verdigris` | `#9fb8a8` | rooftop planters |
| `Toy_mustard_Glow` | `#d9a441` | the two ground-floor commercial fronts at night — the hero glow |
| `Toy_glassl_Glow` | `#6f95b8` | a scatter of lit loft windows |

Any hex above that is not already in the palette file is a **WARN, not a FAIL** — take the
nearest palette entry first and only introduce a new `Toy_*` name if the render shows the
substitute collapsing a needed contrast. Record every substitution in `REPORT.md`.

Two colour decisions carry the building and neither is negotiable: the **`Toy_slate` /
`Toy_steel_l` value split** at 4.5 m, and the **`Toy_orange` gates**. If the aerial render
shows the orange reading as brown, brighten it.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that reads roughly a quarter opaque by day even
for a closed shell, so a primary surface must never be authored as glow. Hero glow: the two
ground-floor commercial fronts (the big South Park storefront and the alley doorway), lit
warm — this is a working office building and its base is the lit thing. Supporting accent:
six or seven lit loft windows scattered over the upper floors of the front and alley
elevations, never a full floor. Nothing else glows; there is no signage, and the cylinder
stays dark — a glowing drum would be a lighthouse and this is not one.

### 2.9 Top surface

An L-shaped roof on a 14.44 x 30.06 m lot with a 6.4 x 8.7 m bite out of the rear-northeast
corner, in a district the camera flies over constantly. From 2026 Vexcel satellite imagery
the roof is a **stepped grey membrane** in two planes (the front block low, the rear block
about a metre higher), carrying:

- the **cylinder**, unmistakable from above as a light circle — the only curve on this side
  of the oval
- a **triangular gable ridge** behind the front parapet, reading as a bright wedge
- the **pergola frame** over a terrace at the front-northeast, with planting
- the open **rear-northeast yard**, which from above reads as a darker rectangle at the
  inside corner and is what breaks the roof out of a plain rectangle

Unlike the Mission Housing row two doors along, there are **no solar panels** on this roof.
The graphical repetition the style bible asks for (§10) has to come from the parapet steps
and the circle-plus-wedge pair, so keep the parapet copings clearly darker than the deck and
keep the cylinder large and light against a mid-grey deck.

### 2.10 Scope

**In the GLB:** the single building on parcel 3775/116–121 — all body volumes with their
material seams, the brick base and mosaic band, parapets and copings, three exposed
elevations' openings plus the blind party wall, both orange gates, the front archway and
storefront, the alley garage and stoop, the rooftop cylinder, gable, pergola, stair bulkhead
and vents, and both roof decks

**Not in the GLB:** South Park itself, South Park Street, Jack London Alley, Taber Place,
Bryant Street, 84 South Park or any other neighbour, the pleached street trees in front of
the building and along the alley, sidewalk, kerbs, construction fencing, vehicles, people,
plinths, cameras or lights

### 2.11 Triangle budget

Cap 11,000 — above the 3–8k the rest of the South Park row runs at, because this building
genuinely has three designed elevations, four material zones and a curved element. The cap
should still bind. Suggested split: the three body volumes with their seams, parapets and
bands ~3k; the 16-sided cylinder with cap ~0.7k; the gable ~0.3k; front elevation
(archway, storefront, gate, two bands of glazing, box bays) ~2.5k; alley elevation
(fourteen openings, garage, gate, stoop, bronze panel) ~2.8k; rear and yard faces ~0.9k;
roof furniture and pergola ~0.8k.

The cylinder is the one place where segment count matters. Sixteen sides is enough to read
as a drum at diorama scale; thirty-two costs ~350 triangles for nothing visible.

### 2.12 Draft manifest entry

```json
{
  "id": "96-south-park",
  "file": "96-south-park.glb",
  "anchor": [
    -122.3941704,
    37.7818909
  ],
  "targetHeightM": 13.7,
  "cat": 2,
  "name": "86–96 South Park",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated. `estimated` is
`true` because 13.7 m is a LiDAR maximum interpreted as the cylinder cap, not a published
figure. `cat: 2` (Apartments) is the best fit for four residential units over two
commercial spaces; `3` (Office) would also be defensible given the current tenancy, and
`4`/`5` would not.

`name` deliberately uses the **86–96** range rather than "96 South Park": that is how the
parcel, the architect and the building's own painted wall numbers describe it, and the
`96-south-park` id already carries the address the user asked for.

### 2.13 Integration notes (for later, not this task)

- **New landmark, Case B.** Neither `pipeline/lib/landmarks.mjs` nor `app/src/landmarks.js`
  knows this id. Integration needs a `pipeline/lib/landmarks.mjs` entry
  (`id: '96SouthPark'`) **and a re-bake of the affected tiles**, or the baked procedural
  buildings on this exact footprint will intersect the GLB.
- **This site carries FOUR source footprints, not one or two.** Both bake inputs split the
  building in half, and differently. `excluded()` drops a footprint when its ring centroid
  **or any ring vertex** falls inside the radius; measured on the *simplified* rings the
  bake actually builds (`simplifyRing(ring, 0.6)`), from the anchor
  `-122.3941704, 37.7818909`:

  ```
    2.54 m  DataSF SF3775116 / 201006.0022147  (h 11.15, front + NE)   vertex
    3.31 m  Overture 9de15a80bf  == OSM way/113545685  (h 10.8)        vertex
    3.71 m  DataSF SF3775116 / 201006.0149656  (h 12.32, rear SW)      vertex
    4.99 m  Overture aaf221991f  == OSM way/113545691  (h 4)           centroid
            -> the FLOOR: below 5.00 m at least one copy of this
               building survives and the asset sits inside it
   12.30 m  DataSF SF3775055 (84 South Park, h 11.36)                  centroid
            -> the CEILING, and the binding constraint
   12.41 m  Overture 3df1e9b461 (84 South Park, h 11)                  centroid
   16.03 m  DataSF SF3775054 (76–82 South Park)                        vertex
   19.10 m  Overture 5128010cd5 (76–82 South Park)                     vertex
  ```

  Safe window **(5.00, 12.30) m**. **`exclude: 8`** sits near the middle with 3.00 m of
  margin below and 4.30 m above, and drops exactly four footprints — all four copies of
  this building, nothing else. Verify against the re-bake: the tile's footprint count must
  fall by four, and nothing removed within 20 m of the anchor may be a neighbour.
- Note that 84 South Park's DataSF ring **shares two party-wall vertices** with our front
  footprint at 7.5 m and 15.3 m from the anchor. Those vertices survive
  `simplifyRing(0.6)` only in the raw data — Douglas-Peucker removes the 7.5 m one because
  it is nearly collinear with its neighbours, which is why the ceiling comes out at 12.30 m
  instead of 7.5 m. **Measure on the simplified rings, not the raw ones**, or this entry
  will look impossible.
- **Height check before judging.** The procedural stand-ins here are 11.15 m and 12.32 m;
  the asset is 13.7 m. The GLB is taller than both, so an *unbaked* local check will show
  the asset apparently fine while a procedural block is still standing inside it. Do the
  bake before judging.
- `loadRadius`: the default formula gives `max(2500, 13.7 * 30) = 2500` m. Take the default.
- `camera`: the front faces 135.1° and the exposed alley flank 225.2°, so bearing 180 (due
  south of the building) is the three-quarter that shows both. `camera.yaw` is
  `180 - bearing`, so **`{ distance: 160, yaw: 0, pitch: 26 }`**.
- This is the twentieth one-off South Park building. The question 380 Brannan, 101 South
  Park and 102 South Park all raised stands: a manifest of individually authored row
  buildings does not stream well, and the kit/instancing route
  (`KIT-INTEGRATION-PROMPT.md`) is probably the right long-term home for that class —
  though *this* building, with a cylinder and four material zones, is exactly the kind that
  would never come out of a kit.
- If other landmarks are in flight, run stage 5 in **batch mode** (see
  `docs/asset-pipeline/ADDRESS-TO-ASSET.md`): still bake, still QA the bake, then throw the
  bake away and commit source only.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~0.5 m of the origin (the anchor
      in 2.12 is the bbox centre precisely so this holds on an L-shaped plan)
- [ ] Bounding-box top exactly 13.70 m at the cylinder cap (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~31.5 x 27.0 m is
      expected for a 14.44 x 30.06 m building at a 45° heading)
- [ ] Triangles at or under 11,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the two commercial fronts and a scatter of upper windows; glow shells
      proud of the opaque glazing; the cylinder is NOT glow
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for
      the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The cylinder is the plan's biggest bet.** It is unmistakable in the February 2021 Jack
  London Alley pano — a pale, vertically ribbed curved form standing above the roofline —
  and the 2026 satellite imagery shows a matching light curved shape on the roof. What is
  *not* established is whether it is a full drum, a half-drum against a wall, or a curved
  wall enclosing a stair; nor its exact diameter or position along the flank. The plan
  commits to a full 4.6 m drum at `(s -4.4, t +2.6)` because that is the reading that
  survives both views, and because a full drum is the version that still reads from the
  air if the guess is slightly wrong. **Find one good photograph before building it.**
- **13.7 m is a LiDAR maximum, not a measured crest.** The two footprint rings give medians
  of 11.15 m and 12.32 m with maxima of 13.28 m and 13.73 m and σ around 1.5 m. The plan
  reads the medians as the two parapet planes and the rear ring's 13.73 m maximum as the
  cylinder — which is self-consistent, since the cylinder sits on the rear block. But 2010
  LiDAR maxima over a 30 m lot lined with pleached trees are exactly the reading that can
  be a branch. If the executing agent can scale the cylinder against a storey height in a
  photograph, that measurement wins over this inference and **both the model and the
  manifest height move together**.
- **The rear-northeast yard is inferred from LiDAR coverage only.** The two footprint rings
  total 289.7 m2 on a 434.1 m2 lot, and the uncovered area is concentrated at the Taber
  Place / 84 South Park inside corner. The plan models 378 m2 — the full lot less that
  corner — which splits the difference, on the assumption that LiDAR footprints
  under-report single-storey and set-back parts. If satellite imagery shows the corner
  built, fill it in and the roof becomes a plain rectangle; nothing else changes.
- **The Taber Place rear elevation is entirely invented.** No photograph of it was found.
  It is a short face (8.02 m) at the back of an alley, so the risk is contained, but it is
  the one elevation with no evidence at all, and it faces a street the camera can fly down.
- **No photographs by the architect were obtained.** Both Architizer and
  ldparchitecture.com host galleries for this project; neither served images to the search
  tooling used here. This is the single highest-value missing source and a human with a
  browser can probably fix it in two minutes. Levy Design Partners' own photography would
  settle the cylinder, the material list, the roof and the rear in one pass.
- **Firm name.** Architizer says LDP Architecture, Inc.; SF Heritage says Levy Art +
  Architecture. Same practice, different eras. Nothing in the model depends on it, and
  nothing about it goes in the manifest.
- **The "corner site" claim is corroborated, not assumed.** Architizer calls it a corner
  site and the bake's own street centrelines put Jack London Alley 6.2 m off the southwest
  property line and Taber Place 3.1 m off the rear. That is the fact that makes this a
  three-elevation model rather than a one-elevation model, so it is worth restating: the
  southwest flank is not a party wall, and building it blank would be a serious error.
- **Style risk.** This is a collage building, and the failure mode is mush — a grey lump
  with arbitrary bumps that reads as a modelling accident rather than a design. Four or
  five volumes with real material contrast at every seam, the dark base, the orange gates
  and the cylinder are what prevent it. If the aerial render looks busy, delete volumes;
  do not add detail.
