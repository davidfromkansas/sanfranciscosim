# 104–106 South Park (Gran Oriente Filipino Hotel) — SF-SIM asset plan

A 1907 three-storey-over-basement wood-frame rooming house on the north-west rim of
the South Park oval, designed by W. L. Schmolle and built by McLaughlin and Walsh.
It is the **narrowest and deepest** building yet planned for this set: the building
occupies the whole of a 24 ft × 97.5 ft lot, so it is 7.3 m of frontage against
29.7 m of depth — a 4:1 sliver, one storey taller than the low modern neighbour on
its south-west party wall and one storey shorter than the Italianate at 102 next
door on the north-east.

It matters far more than its size. Leased from 1935 and bought in 1948 by Gran
Oriente Filipino — the first Filipino-founded Masonic lodge in the United States —
it is one of the earliest Filipino-owned buildings in the South of Market, was
nominated to the National Register in 2019 under Criterion A for Filipino ethnic
heritage, and is now 24 studios of 100% affordable housing owned by Mission Housing.
The nomination is also, for our purposes, an unusually good gift: a surveyed,
published, elevation-by-elevation description of a building this small almost never
exists.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/106-south-park/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `106-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor (manifest, placement) | `-122.3944106, 37.7817227` |
| WGS84 anchor (registry, exclusion only) | same point — see 2.13, the band is wide here for once |
| Target height | **11.58 m** to the cornice crest (38 ft, published); roof deck 11.02 m (measured, LiDAR) |
| Footprint | 7.32 m frontage × 29.72 m deep, 217 m² — the building occupies the entire lot |
| Axis | long axis 135.0° / 315.0°; street facade faces **135.0°** (south-east, onto the oval) |
| Triangle cap | 7,000 |
| Category | `2` (apartments — 24-unit SRO) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 104–106 South Park (Gran Oriente Filipino Hotel) GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the Gran Oriente Filipino Hotel at
104–106 South Park Street, San Francisco, and deliver it as a downloadable,
validated GLB.

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
7. `artifacts/165-south-park/` — the closest reference implementation: the other
   narrow-lot party-wall sliver on the same oval, same background-building detail
   budget, same "legible only by its own width" problem. Take its massing
   discipline and its restraint. Note the differences: this building is three
   storeys not two, stucco not clapboard, and it has a documented three-bay
   facade rhythm and a real cornice where 165 has neither
8. `docs/asset-plans/106-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## This dossier is unusually strong — and exactly one thing in it is stale

The National Register nomination (2019) describes all four elevations, the roof,
the lot and the height in survey-grade prose. Trust its **form**. Do **not** trust
its **surfaces**: after the COVID-era Mission Housing rehabilitation (2020–21) the
building was repainted and the painted trompe-l'œil pediment lintels and Corinthian
columns that the nomination and every pre-2021 photograph show were **removed**.
The metal "GRAN ORIENTE FILIPINO" lettering over the entrance was kept.

**Model the building as it stands in 2026: a plain painted stucco facade.** A
modeller who works from the 1996 or 2019 photographs will build a Corinthian order
that no longer exists. See 2.4 and 2.15.

## Must capture

- **The sliver proportion.** 7.32 m of frontage against 29.72 m of depth, 3 storeys.
  From the app's aerial camera this proportion *is* the building.
- **Three storeys, flat roof, a real cornice.** The crest is 11.58 m; the roof deck
  is 11.02 m; the ~0.5 m difference is the cornice and parapet at the street end.
- **The three-bay window grid** on the two upper storeys of the street elevation —
  six openings total, one per bay per storey, evenly spaced across a 7.3 m frontage.
  This regular grid is the facade now that the painted ornament is gone.
- **The ground floor's two-part rhythm**: a recessed entry vestibule at the
  **south-west** (left, as seen from the park) end, and three storefront windows over
  a solid bulkhead to the north-east of it.
- **The "GRAN ORIENTE FILIPINO" sign band** above the vestibule — the one identity
  cue this building has, and the reason it is in the manifest at all. Carry it as a
  distinct horizontal band of a different value, not as legible lettering.
- **The south-west flank showing above its neighbour.** 108 South Park next door is
  ~7.8 m tall against this building's 11.0 m roof, so roughly 3.2 m of this
  building's south-west wall is exposed and clad in horizontal wood boards. It is
  visible from the app's camera and must be built.
- **A designed roof.** The camera looks down. The nomination records three large
  rectangular skylights along the south-west edge and five small square skylights
  along the north-east edge. Recent aerial imagery also shows dark rooftop arrays on
  this roof and its neighbours consistent with the rehabilitation's PV work —
  confirm before building, see 2.9.

## Research 104–106 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The **south-east street elevation** as it stands today, post-2021 repaint — the
  current paint scheme (see 2.8) is read from shaded photography and is the weakest
  colour call in this plan
- The **roof from above** — skylights, PV, stair bulkhead, mechanical. Settle the PV
  question; it changes the roof design completely
- The **north-west rear elevation on Taber Place**, which the nomination describes
  (asbestos shingle, inset service entrance, six upper windows, a metal fire escape
  on the two eastern bays) but which no photograph in this dossier shows
- The **south-west flank above 108 South Park** — how much of it shows and whether
  the horizontal wood boarding survived the rehabilitation
- Whether the dentilled cornice survived the repaint, and whether it was simplified
- Day and night appearance

Prefer DataSF datasets, SF Planning records, the National Register nomination,
assessor data, geolocated photography and aerial imagery. Never rely on a single
photograph, a single AI-generated image, or a single unsourced 3D model. Separate
verified facts from visual inference; if sources disagree, document the disagreement
and decide.

**Three source problems are already resolved in 2.1–2.3 and 2.15 — re-check them,
do not silently re-inherit the wrong value:**

1. **The building is 104 *and* 106 South Park, one property, one building.** The
   DataSF parcel `3775058` carries the address range 104–106 and the OSM way
   `124884343` carries only `106`. They are the same building. Do not model two.
2. **The LiDAR `hgt_max` of 13.50 m is not this building.** It is 2.5 m above the
   11.02 m roof-deck median on a footprint with a 0.67 m standard deviation, and it
   sits on the party wall shared with 102 South Park, whose own LiDAR median is
   12.88 m and max 15.20 m. It is the neighbour bleeding across a 0.5 m raster cell —
   the same failure the Earl Warren plan documents. There is no penthouse. The
   crest is the published 38 ft (11.58 m).
3. **OSM `height=11` is right for once, and it is still not the target.** It agrees
   with the LiDAR roof-deck median (11.02 m) to within 0.02 m, which makes it look
   corroborated; both are measuring the roof membrane behind the parapet, not the
   cornice crest. The target is 11.58 m.

## Create a reference dossier

Write `artifacts/106-south-park/REFERENCE.md` containing: source links and what each
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

This is a **background building** in the style bible's detail budget (§21), one step
below the secondary tier — but a background building with more documented content
than 165 South Park had: a three-bay grid, a cornice, a sign band, a two-part ground
floor, an exposed flank and a skylit roof. Spend the extra budget on those six
things and on nothing else. Resist inventing ornament; the ornament this building
had was painted on and has been painted off.

The finished asset must be immediately recognizable as this building, consistent
with the real one from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building: the three-storey stucco volume on the measured
footprint, the street facade's bay grid, the ground-floor vestibule recess and
storefront, the sign band, the cornice, the exposed south-west flank above the
neighbour, the rear elevation with its fire escape, and the flat roof with its
skylights and whatever rooftop equipment the research confirms.

Do not include unrelated surrounding city geometry: 102 South Park, 108 South Park,
the South Park oval or its lawn and trees, the large street tree in front of the
building, Taber Place, the street, the sidewalk, parked cars, motorcycles, people,
plinths, cameras or lights. Temporary context may appear in review renders but must
not leak into the GLB.

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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The street facade
faces **135.0°** and the long axis runs back at **315.0°**. Build on the measured
rectangle in 2.3 rather than modelling an axis-aligned bar and rotating it. Record
the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the street-end cornice
crest) must land at exactly **11.58 m** so the loader's
`targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/106-south-park/build_106_south_park.py` (deterministic build
script), `artifacts/106-south-park/106-south-park.blend`, and
`artifacts/106-south-park/106-south-park.glb`. The script must rebuild the model
reliably enough for future revision. Do not modify or rename an unrelated existing
GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`106-south-park-top.png`, `-north.png`, `-east.png`, `-south.png`, `-west.png`, plus
`106-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty
render `106-south-park-aerial.png`, and a night render
`106-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection;
use orthographic or long-lens cameras; label directions from the researched
orientation; the top view must clearly show the roof plane, the cornice at the
street end, and the skylight layout; the aerial view uses the style bible's camera
assumptions (30–50 degrees down, long lens). Simple tabletop lighting, neutral warm
background, minimal depth of field, and every image must depict the same exported
model.

Because the building is four times deeper than it is wide **and** stands at 135°,
frame all four elevations to the long dimension and accept empty frame on the
north and east views rather than zooming each view to fit — the reviewer needs to
be able to compare them. Add one extra view looking square-on at the 135° street
facade; the four cardinal elevations all show this building obliquely and none of
them shows its public face properly.

## Validate the exported GLB

Re-import `106-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/106-south-park/validation.json` and
`artifacts/106-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **26.2 × 26.2 m** even
though the building is 7.3 × 29.7 m — that is the exact consequence of a 45° heading
on a long thin box, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "106-south-park",
  "file": "106-south-park.glb",
  "anchor": [
    -122.3944106,
    37.7817227
  ],
  "targetHeightM": 11.58,
  "cat": 2,
  "name": "Gran Oriente Filipino Hotel (104–106 South Park)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`"estimated": false` is deliberate — the 38 ft crest is published in the National
Register nomination and independently corroborated by the LiDAR roof deck plus a
plausible cornice. See 2.1.

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/106-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* are visual
or derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 104–106 South Park Street, San Francisco CA 94107 | DataSF parcels `acdm-wktn`, `blklot=3775058`, `from_address_num` 104, `to_address_num` 106 — **one property, one building** |
| Also known as | Gran Oriente Filipino Hotel; earlier Hotel Maruichi, then Omiya Hotel (1920s) | NR nomination; SF Heritage |
| Block / lot | 3775 / 058; zoning `SPD` (SOMA–South Park), 40-X height and bulk | DataSF parcels; SF Planning case 2016-008192SRV |
| Built | **1907** | NR nomination — post-earthquake reconstruction |
| Architect | **W. L. Schmolle** (William L. Schmolle, 1865–1955); builder McLaughlin and Walsh | NR nomination, §8 Architect/Builder |
| Structure | three storeys over a basement, wood frame, brick foundation | NR nomination §7 — **measured/surveyed** |
| Height | **thirty-eight feet = 11.58 m** | NR nomination §7 — **published**; this is the crest |
| Lot | 24 ft × 97.5 ft = **7.32 × 29.72 m**, 217 m²; the building occupies the entire lot with frontages on both South Park Street and Taber Place | NR nomination §7 — **surveyed**, and it agrees with both geometry sources below to ~0.2 m |
| OSM footprint | `way/124884343`, min-area OBB **29.80 × 7.29 m** at 135.0°, 216.6 m² | OSM API, reprojected — **measured** |
| DataSF LiDAR footprint | `mblr` SF3775058 / `sf16_bldgid` 201006.0023494, OBB **30.02 × 7.02 m** at 45.0°, 202.6 m² polygon, 824 cells at 50 cm | DataSF `ynuv-fyni` — **measured** |
| Roof deck | **11.02 m** above grade (LiDAR height median); majority 10.92 m; mean 11.36 m; σ 0.67 m | DataSF `ynuv-fyni` — **measured**; flat roof, so median ≈ deck |
| LiDAR maximum | 13.50 m | same — **rejected as this building's crest**, see 2.15 risk 2 |
| Ground | 9.25 m NAVD88 minimum, 9.74 m median, 10.25 m maximum (1.0 m of fall across the lot) | same — the app's terrain handles this, not the asset |
| OSM tags | `building=residential`, `height=11`, `name=Gran Oriente Filipino`, `addr:housenumber=106` | OSM — the height matches the roof deck, not the crest |
| Facade heading | street elevation faces **135.0°** (SE, onto the oval); long axis 315.0° | measured from both footprint sources, which agree to 0.05° |
| Neighbours | **102 South Park** (lot 3775057, bearing 53°, NE party wall, LiDAR median 12.88 m — *taller*) and **108–110 South Park** (lot 3775059, bearing 217°, SW party wall, LiDAR median 7.76 m — *shorter*) | DataSF parcels + `ynuv-fyni` — **measured**; this asymmetry is a design fact, see 2.4 |
| Units today | **24 studios**, 100% affordable, formerly-homeless preference | Mission Housing; the SF Chronicle's 2018 piece says 27, the current listing says 24 |
| Ownership | Gran Oriente Filipino leased from 1935, purchased 1948, sold 2018 to Mission Housing Development Corporation | NR nomination §8; Mission Housing |
| Rehabilitation | 2020–21, part of Mission Housing's ~$60M "South Park Scattered Sites" (with Hotel Madrid and the Park View), LDP Architecture | Mission Housing; SCCS Group |
| Designation | NR-nominated 2019 (Criterion A, ETHNIC HERITAGE: Filipino / SOCIAL HISTORY, period of significance 1935–1968); owner declined to proceed in 2020; **remains eligible, not listed** | SF Planning HPC case 2016-008192SRV; SF Heritage |
| Neighbourhood | South Park, laid out 1852–54 by George Gordon; a 550 ft × 75 ft oblong park, bisected NE–SW by South Park Street and NW–SE by Jack London Alley; this building is in the north-west quadrant | NR nomination §7; SF Heritage |

### 2.2 Sources

- **SF Planning HPC packet, case 2016-008192SRV** (2 October 2019),
  `https://commissions.sfplanning.org/hpcpackets/2016-008192SRV%20-%20Gran%20Oriente.pdf`
  — contains the full National Register Registration Form prepared by Erica Schultz
  (Architectural Resources Group). This single document supplies the height, the lot
  dimensions, the storey count, the architect and builder, the roof and skylight
  layout, and an elevation-by-elevation description of all four sides. **It is the
  backbone of this plan.** Found via `exa` `web_search_advanced_exa`.
- SF Heritage, "South Park's Gran Oriente Filipino Hotel" (published January 2021,
  **updated October 2025**),
  `https://www.sfheritage.org/cultural-districts/soma-pilipinas/landmark-tuesdays-gran-oriente-filipino-hotel/`
  — the only source that documents the **post-COVID facade alterations**: repaint,
  removal of the trompe-l'œil lintels, Corinthian columns and metal entrance gates,
  retention of the metal lettering. Also carries the 1996 elevation photograph (by
  Aileen Lainez), two December 2020 construction photographs, a September 2025 street
  photograph, and a 2025 Google Maps crop of the renovated ground floor.
- Gran Oriente Landmark Designation Report (OASIS/LBB), `static1.squarespace.com`
  — covers the three-property Gran Oriente complex (104–106 South Park, 45–49 South
  Park, 95 Jack London Alley) and confirms the 1907/1909/1951 construction dates and
  the flat-roofed rectangular massing.
- Mission Housing, `https://www.missionhousing.org/granoriente` — 24 studios, the
  2018 acquisition, the $5M MOHCD Small Sites loan, and the 2019–2021 rehabilitation
  schedule. `https://www.missionhousing.org/post/preservation-and-transcendent-projects-finalized`
  — the South Park Scattered Sites scope and its PV/roof upgrades.
- DataSF `acdm-wktn` (Parcels), `blklot=3775058` — the surveyed lot, the 104→106
  address range, SPD zoning, and the neighbour lots 3775057 and 3775059.
- DataSF `ynuv-fyni` (Building Footprints, LiDAR-derived, 2010 survey, refreshed
  2023-09-11), `mblr` SF3775058 — footprint, ground elevation, roof-deck height and
  the neighbours' heights that explain the 13.50 m maximum.
- OSM `way/124884343` — the footprint cross-check and the `height=11` tag.
- Google Street View, South Park, January 2025 capture, viewed at
  `37.781575, -122.394230`, headings 300–318°, pitch 105–122° — the current ground
  floor and what can be seen of the upper storeys past the street tree.
- Google Maps satellite (2026, Vexcel imagery) at `37.7817229, -122.3944286`, and
  Esri World Imagery z20 with the OSM footprint overlaid — the roof and the row's
  rooftop arrays.
- SF Chronicle, "Gran Oriente hotel prepares for next chapter" (Beth Spotswood);
  SF Examiner, "The amazing saga of the Gran Oriente Filipino Hotel" (10 March 2023);
  Positively Filipino, "From Here to Fraternity"; California Freemason, "Portal to
  the Past" (2 June 2021) — history, tenancy and the rehabilitation, no useful
  exterior description.

### 2.3 Orientation and placement

South Park is an oblong park whose rim buildings face inward. This one sits in the
**north-west quadrant**, on the west side of South Park Street between Jack London
Alley and Third Street, and faces **south-east across the oval**. It is a through
lot: the rear elevation fronts Taber Place.

Three geometries exist and, unusually for this set, all three agree:

| Source | What it is | Verdict |
|---|---|---|
| NR nomination | 24 ft × 97.5 ft lot, fully occupied | **authoritative for dimensions** — 7.32 × 29.72 m |
| DataSF LiDAR footprint SF3775058 | 2010 raster-derived built area | **confirms** — OBB 30.02 × 7.02 m at 45.04°, area centroid `-122.3944106, 37.7817227` |
| OSM `way/124884343` | building trace tagged `106` | **confirms** — OBB 29.80 × 7.29 m at 135.03°, OBB centre `-122.3944286, 37.7817228` |

The two footprint centroids are **1.58 m apart**, along the long axis. That gap
matters only for the exclusion radius (2.13); for placement, take the DataSF area
centroid.

Design footprint: a plain rectangle **7.32 m × 29.72 m** centred on the manifest
anchor, long axis running back at 315.0° (north-west). In Blender coordinates
(metres, `+X` east, `+Y` north, origin on the anchor) the four corners are:

```
corner              X (east)   Y (north)   which end / which flank
street north-east    +13.10      -7.92     South Park St frontage, 102 party wall
street south-west     +7.92     -13.10     South Park St frontage, 108 party wall
rear    north-east     -7.92     +13.10     Taber Place end, 102 party wall
rear    south-west    -13.10      +7.92     Taber Place end, 108 party wall
```

The street frontage is the +13.10/+7.92 edge (7.32 m long, facing 135.0°); the two
long 29.72 m edges are the party walls, the north-east one facing 45° toward 102
South Park and the south-west one facing 225° toward 108–110.

Because the heading is 45° off the axes, the axis-aligned XY bounding box of the
bare volume is **26.20 × 26.20 m**, rising to about **26.4 × 26.4 m** once the
cornice oversails the street end. That is correct and is not a scale error.

**Party walls on both sides.** The building abuts its neighbours with no gap. The
north-east wall (toward 102 South Park) is completely hidden — 102 is 1.9 m taller.
The south-west wall (toward 108–110) is exposed for its top ~3.2 m, because 108 is
3.3 m shorter. Only two of the four elevations are ever seen: the south-east street
front and the north-west rear on Taber Place, plus that band of south-west flank.

### 2.4 What each side shows

**South-east (street elevation, the public face)** — Three storeys of painted
stucco. Today, after the 2020–21 repaint: the upper two storeys are a pale, warm
off-white; the ground floor is a distinctly darker slate/warm gray; a near-black
horizontal sign band runs between them, carrying the metal "GRAN ORIENTE FILIPINO"
letters over the entrance. The upper two storeys are divided into **three bays**
with one wood-sash double-hung window per bay per storey — **six openings, in a
regular grid**. A simple cornice, originally adorned with painted dentils, projects
above the third-storey windows and is the crest. The ground floor has, from
south-west to north-east: a recessed entry vestibule with two wood panelled doors
under transoms (the western door goes down to the basement, the eastern up to the
mailbox hallway), then **three wood-sash storefront windows** over a solid
bulkhead.

What is **gone**, and must not be modelled: the painted trompe-l'œil pediment
lintels above each upper window, the painted Corinthian columns flanking each bay,
and the ornamental metal entrance gates. All three appear in the 1996 photograph and
in the 2019 nomination; all three were removed after 2020. The metal lettering
stayed.

**North-east (party flank toward 102 South Park)** — Abuts the neighbour and is not
visible at all. 102 is taller. Build it blind.

**South-west (party flank toward 108–110 South Park)** — Blind for its lower two
thirds; the top ~3.2 m stands above 108's roof and is clad in **horizontal wood
boards** (the nomination's "the section of the southwest façade extending above the
adjacent building"). This strip is genuinely visible from the app's aerial camera
and is one of only two things that distinguish this building's silhouette from a
plain bar.

**North-west (rear, on Taber Place)** — The utilitarian face. Clad in asbestos
shingles over the original wood channel rustic siding. The basement level has a
large metal louvered vent to the east and a small screened window to the west; the
first storey has a **central inset service entrance** with a sliding metal screen
door, flanked by one-over-one double-hung windows; the two upper storeys carry
three one-over-one windows each (six total, matching the front), and a **metal fire
escape** serves the two eastern bays.

**Top** — Flat, at 11.02 m, with the cornice lifting the street end to 11.58 m. The
nomination records **three large rectangular skylights lining the south-west end of
the roof and five small square skylights lining the north-east end** — installed
1927, replaced in kind 1986. They cover interior light wells; the two southern large
wells drop to the first storey and the northern one to the second. Recent aerial
imagery of this block shows large dark rooftop arrays on several of these
rehabilitated SRO roofs, consistent with the project's PV work; whether this
particular roof carries them is *observed but unconfirmed* — see 2.9 and 2.15.

### 2.5 Recognition cues (ranked)

1. **The 4:1 sliver at three storeys.** 7.3 m wide, 29.7 m deep, 11.6 m tall. From
   above this is the entire silhouette and it is the sharpest such proportion on the
   oval.
2. **The stepped party-wall silhouette** — a shorter neighbour on the south-west and
   a taller one on the north-east, so the building reads as a single tooth standing
   proud of one side of the row. The exposed wood-boarded strip on the south-west
   flank is the visible evidence of it.
3. **The three-bay grid over a two-part ground floor** — six evenly spaced upper
   windows above a dark base split into a recessed vestibule and a run of shopfront
   glass.
4. **The sign band** between them. It is the only thing on the building that says
   what it is.
5. **The skylit flat roof** — a pale rectangle with a line of large skylights down
   one edge and a line of small ones down the other, which is a distinctive top at
   thumbnail size and is exactly the kind of designed roof the style bible asks for.

### 2.6 Miniature translation

**Preserve**

- The 7.32 × 29.72 m footprint, the 315° axis and the 135.0° facade heading, exactly
- Three storeys and the 11.02 m deck / 11.58 m crest relationship
- The three-bay grid, evenly spaced, one window per bay per storey
- The vestibule at the **south-west** end of the ground floor and the storefront run
  to the north-east of it — getting this handedness backwards mirrors the building
- The exposed south-west flank strip at its real height band (roughly z 7.8→11.0 m)
- The skylight layout: three large on the south-west edge, five small on the
  north-east edge

**Simplify / exaggerate**

- Individual windows become clean recessed rectangles with a proud sill; no muntins,
  no double-hung division, no transoms
- The three storefront windows become one recessed glazed band with two mullions
- The vestibule becomes a single deep rectangular recess with a dark back plane —
  it should read as a hole, not a painted panel
- The sign band is exaggerated: a full-width band ~0.55 m tall (real: a stucco panel
  with applied letters), in a distinctly darker value, with a 0.05 m proud edge. The
  lettering itself is sub-pixel and must **not** be modelled as glyphs; a shallow
  inset strip of a lighter value inside the band carries it
- The cornice is thickened to a clean 0.4 m band, 0.20 m proud; the dentils become a
  single shadow groove
- The fire escape becomes one flat slab per storey with two vertical posts — three
  boxes, not a truss. Do not model treads
- Asbestos shingle, wood channel rustic siding and stucco all become flat colour;
  the rear's difference from the front is carried by value alone
- The basement vent, meters, downpipes and conduit disappear
- The rear yard, the street tree, and both neighbours are not modelled at all

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render.

1. Main volume: extrude the 2.3 rectangle from z=0 to z=11.02, `Toy_bone`.
2. Ground-floor band: the same rectangle's street-end 0.4 m re-clad from z=0 to
   z=3.30 in `Toy_steel`, 0.04 m proud, wrapping only the south-east elevation and
   0.4 m around each front corner.
3. Sign band: a full-frontage band from z=3.30 to z=3.85 in `Toy_ink`, 0.05 m proud.
   Inside it, a 5.4 × 0.24 m inset strip in `Toy_trim` standing for the lettering.
4. Cornice: a 0.40 m band along the south-east elevation only, from z=11.18 to
   **z=11.58**, 0.20 m proud, `Toy_trim`. This sets the bounding-box top and must
   land exactly on 11.58. A 0.04 m shadow groove under it at z=11.14 stands for the
   dentils.
5. Roof plane: flat cap at z=11.02, `Toy_roofd`.
6. Street windows: six openings, 0.95 × 1.85 m, three per storey across the 7.32 m
   frontage at bay centres −2.30 / 0.00 / +2.30 m, sills at z=4.65 and z=8.05,
   recessed 0.12 m, `Toy_glass`; 0.09 m proud `Toy_trim` sill and surround on each.
7. Vestibule: a 1.55 m wide, 2.75 m tall, 1.10 m deep recess at the south-west end of
   the frontage, back plane `Toy_ink`, with one 0.95 × 2.15 m `Toy_ink` door slab set
   into it.
8. Storefront: a 4.30 × 2.05 m recessed glazed band to the north-east of the
   vestibule, sill at z=1.05, recessed 0.10 m, `Toy_glass`, split by two 0.10 m
   `Toy_trim` mullions, over a `Toy_steel` bulkhead.
9. South-west flank strip: re-clad the south-west face between z=7.80 and z=11.02 in
   `Toy_wood`, 0.03 m proud, with three shallow horizontal grooves. Everything below
   z=7.80 on that face is a party wall and stays `Toy_bone` (it is never seen).
10. Rear (north-west) elevation: `Toy_roofd` value change over the whole face; one
    1.40 × 2.30 m inset service entrance centred at grade in `Toy_ink`; six windows
    on the same 0.95 × 1.85 m module and the same two sill heights as the front, at
    bay centres −2.30 / 0.00 / +2.30 m.
11. Fire escape: three 2.60 × 0.85 m slabs in `Toy_ink` at z=4.35, 7.75 and 11.02 on
    the rear elevation, offset toward the north-east bays, joined by two 0.10 m
    square posts.
12. Skylights: three 2.10 × 1.05 m boxes 0.35 m proud along the south-west roof edge
    and five 0.65 × 0.65 m boxes 0.25 m proud along the north-east roof edge, all
    `Toy_glass` on top with `Toy_trim` kerbs.
13. Roof PV (**only if research confirms it**): two flush arrays in `Toy_ink` at
    0.30 m above the deck, on the roof between the two skylight lines. They stay
    below the cornice crest and do not change the target height.
14. Bevel 0.10 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_bone` | `#efe7d8` | the upper two storeys' stucco — the building's body colour |
| `Toy_steel` | `#9aa0a6` | the ground-floor stucco band and the storefront bulkhead |
| `Toy_ink` | `#3a3530` | sign band, vestibule recess and door, service entrance, fire escape, PV |
| `Toy_trim` | `#f3efe6` | cornice, window trim and sills, storefront mullions, skylight kerbs, sign inset |
| `Toy_glass` | `#2a4d73` | all windows, the storefront band, the skylight tops |
| `Toy_wood` | `#8a6a4a` | the exposed south-west flank strip above 108 South Park |
| `Toy_roofd` | `#45454a` | the flat roof plane and the rear elevation |
| `Toy_glass_Glow` | `#2a4d73` | four lit upper windows at night |
| `Toy_trim_Glow` | `#f3efe6` | a thin warm spill in the vestibule recess at night |

Two notes on colour:

- **The current paint scheme is the weakest observation in this dossier.** It is read
  from a shaded Google Maps crop and a January 2025 Street View pano, both taken
  under a full-grown street tree on a north-facing-in-shadow elevation. The *relation*
  is solid — pale upper storeys, distinctly darker ground floor, near-black band
  between them — but the hues are not. `Toy_bone` over `Toy_steel` over `Toy_ink`
  reproduces the relation with palette entries; if better photography turns up and it
  is, say, a warm gray rather than an off-white, say so in `REPORT.md` and adjust.
- `Toy_wood` on the flank strip is doing real work: it is the one warm accent on an
  otherwise neutral building and it is what makes the stepped-silhouette cue legible
  from the aerial camera. Do not neutralise it into the body colour.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
glazing — the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a
primary surface must never be authored as glow. Hero glow: **four** of the six upper
street windows lit, unevenly (this is 24 studios of housing on a quiet oval, not an
office — a fully lit grid would read wrong, and an evenly lit one would read
institutional). Supporting accent: a thin warm spill in the vestibule recess, which
at night is also what tells the eye the recess is an entrance. The storefront, the
rear elevation, the skylights and the roof do not glow.

### 2.9 Top surface

A 7.3 × 29.7 m flat rectangle at 11.02 m, seen constantly from above and, apart from
the street facade, from almost nowhere else. Three things carry it:

1. **The skylight signature** — three large boxes down one long edge and five small
   ones down the other. This is documented, asymmetric, and unusual enough to be a
   genuine identifying mark from directly overhead. It is the single best reason this
   building's roof will not read as a blank slab.
2. **The cornice lift at the street end**, reading as a bright edge in `Toy_trim`
   against the darker `Toy_roofd` deck.
3. **The stepped neighbours** — the roof sits 3.3 m above 108's and 1.9 m below 102's,
   so in the baked city this asset's roof plane is a distinct step in the row rather
   than part of a continuous surface.

**The open question is PV.** Google's 2026 satellite imagery of this block shows
large dark rectangular arrays across several of the rehabilitated SRO roofs here, and
Mission Housing's own project write-up records PV and roof upgrades in this
portfolio. Whether *this* roof carries an array could not be settled at plan time:
the imagery available was either too coarse (Esri z20, monochrome and
mis-registered against the footprint by a metre or two) or too oblique. Settle it
before building. If PV is present it becomes the dominant roof feature and step 13
applies; if it is not, the skylights carry the roof alone and the roof stays
deliberately sparse. Do **not** split the difference by inventing a token array.

### 2.10 Scope

**In the GLB:** the single building — the three-storey stucco volume on the measured
footprint, the ground-floor band, sign band and cornice, the six street windows, the
vestibule recess and door, the storefront band and bulkhead, the exposed south-west
flank strip, the rear elevation with its service entrance, six windows and fire
escape, and the flat roof with its skylights (and PV only if confirmed)

**Not in the GLB:** 102 South Park, 108–110 South Park, the South Park oval, its lawn,
paths or trees, the large street tree in front of the building, Taber Place, the
street, the sidewalk, the rear light wells, fences, vehicles, motorcycles, people,
plinths, cameras or lights

### 2.11 Triangle budget

Cap 7,000 — a background building, but one with more documented content than 165
South Park's 6,000 had to carry. Suggested split: main volume ~300, ground-floor and
sign bands ~500, cornice and dentil groove ~500, roof plane ~150, six street windows
with trim ~2,000, vestibule ~350, storefront band with mullions ~450, flank strip
~250, rear service entrance and six rear windows ~1,100, fire escape ~300, skylights
(eight boxes) ~700, bevel overhead ~400. If the first build lands above 7,000 the
answer is fewer window subdivisions and simpler skylight kerbs, not a raised cap.

### 2.12 Draft manifest entry

```json
{
  "id": "106-south-park",
  "file": "106-south-park.glb",
  "anchor": [
    -122.3944106,
    37.7817227
  ],
  "targetHeightM": 11.58,
  "cat": 2,
  "name": "Gran Oriente Filipino Hotel (104–106 South Park)",
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

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '106SouthPark'`)
  and re-bake the affected tiles, or the baked procedural building will intersect the
  GLB. This is the Case B path in `docs/asset-plans/INTEGRATION-PROMPT.md`.

- **The exclusion radius is comfortable here, which is rare on this oval.**
  `excluded()` in `pipeline/buildings.mjs` drops a footprint when its centroid **or
  any ring vertex** falls inside the circle. Measured from the manifest anchor
  (the DataSF LiDAR area centroid) against the DataSF footprints the bake reads:

  | Polygon | Triggers at | Via |
  |---|---|---|
  | this building (SF3775058) | **0.00 m** | its own centroid |
  | this building, OSM `way/124884343` as an Overture proxy | **1.58 m** | its centroid |
  | 108–110 South Park (SF3775059) | **3.82 m** | nearest ring vertex |
  | 102 South Park (SF3775057) | 3.90 m | nearest ring vertex |
  | 112 South Park (SF3775060) | 14.38 m | centroid |

  The safe window is therefore **(1.58, 3.82) m** — it has to exceed 1.58 so the
  Overture gap-fill version is dropped too (`addBuilding()` returns null on
  exclusion, so `markOccupied()` never runs and `occupiedFraction()` cannot be relied
  on to block a re-add), and stay under 3.82 so 108 South Park survives.
  **Use `exclude: 2.5`** — 0.92 m of margin below and 1.32 m above. That is more than
  four times the band 165 South Park had to work in.

  Measuring from the OSM OBB centre instead collapses the window to (0.00, 2.75) and
  measuring from the parcel centroid to (1.08, 3.73); both work but neither is as
  comfortable, which is why the manifest anchor and the registry point can be the
  **same** here. Confirm against the real
  `pipeline/data/overture_buildings.geojsonseq` at integration time and prove the
  outcome with `pipeline/verify-rebake.mjs`: exactly one footprint dropped in this
  cell, no neighbour lost.

- **`exclude` is also the tree-clear and street-furniture radius.** At 2.5 m it
  clears neither, which is correct: the large street tree in front of this building
  is real, is the single most photographed thing about it, and should stay. Do **not**
  set `clearTrees: true`.

- `loadRadius`: the default formula gives `max(2500, 11.58 × 30) = 2500` m. Take the
  default.

- **Camera preset — check the sense of `yaw` before copying a neighbour's.** In
  `app/src/camera.js` the rig places the camera at
  `(sin(yaw), sin(pitch), cos(yaw)) × distance` from the pivot, and the project's
  `+z` is **south**, so `yaw: 45` puts the camera south-east of the building, looking
  north-west at its street elevation — which is the only view of this building worth
  flying to. Start from `camera: { distance: 150, yaw: 45, pitch: 26 }` and tune
  against the live scene. Note that `165SouthPark`'s preset (`yaw: 350` for a
  building whose facade faces 349.7°) reads as the opposite convention; one of the
  two is wrong and this is a good opportunity to settle which.

- **This is the sixth South Park rim building to enter the manifest by hand, and 165
  South Park's argument now applies with force.** A row of narrow party-wall
  buildings on a residential oval is what `KIT-INTEGRATION-PROMPT.md` exists for.
  This one earns the bespoke route on grounds 165 did not have — a named,
  NR-nominated, architect-attributed building with a survey-grade published
  description and real cultural significance in SoMa Pilipinas — but the next
  anonymous sliver on this oval should be a kit piece.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 11.58 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~26.2 × 26.2 m
      is expected for a 7.32 × 29.72 m building at 45°)
- [ ] Frontage 7.32 m and depth 29.72 m, not rounded toward a squarer plan
- [ ] The street facade carries **no** Corinthian columns and **no** painted pediment
      lintels — they were removed after 2020
- [ ] Vestibule at the **south-west** end of the frontage, storefront to the
      north-east of it (not mirrored)
- [ ] The south-west flank strip exists, in `Toy_wood`, only above ~7.8 m
- [ ] Skylights present: three large on the south-west roof edge, five small on the
      north-east edge
- [ ] Triangles at or under 7,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on four upper street windows and the vestibule recess; glow shells
      proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + the extra square-on 135° facade view + contact sheet +
      night render, all regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

1. **The facade this dossier can show you is not the facade that exists.** Every
   photograph reproduced or described in 2.2 except the 2025 Street View pano and the
   2025 Google Maps crop predates the rehabilitation, and the two that do not are
   both partly hidden by a full-grown street tree. The 1996 elevation photograph is
   the only clear, complete, square-on record of the whole street front — and it
   shows a building with painted Corinthian columns and trompe-l'œil pediments that
   were removed after 2020. **This is the single likeliest way to get this asset
   wrong**, and it is a seductive error because the removed ornament is far more
   interesting than what replaced it. Model 2026.
2. **The LiDAR maximum is the neighbour, not a penthouse.** `hgt_max` is 13.50 m
   against a median of 11.02 m and a standard deviation of 0.67 m — a 3.7σ outlier —
   on a footprint that shares a party wall with 102 South Park, whose own LiDAR
   median is 12.88 m and maximum 15.20 m. This is the Earl Warren failure mode
   (a 0.5 m cell on a party wall sampling the taller building) and the Gran Oriente is
   a textbook case of it. Nothing in the nomination, which describes the roof in
   detail, mentions a bulkhead or penthouse. If aerial imagery does show a stair
   bulkhead, it becomes the tallest geometry and the target height changes — flag it
   rather than clipping it.
3. **The roof PV question is unresolved and it is the largest single visual unknown.**
   See 2.9. It is the difference between a sparse skylit roof and a roof that is
   mostly dark array.
4. **The current paint colours are read from shaded photography.** The value
   *relation* is confident; the hues are not. See 2.8.
5. **No photograph of the Taber Place rear elevation was located.** 2.4's description
   of it is the nomination's prose, which is detailed and survey-grade — but it is
   2019 prose, and the rehabilitation may have replaced the asbestos shingle cladding
   or the fire escape. The rear faces an alley and is visible in the app only from
   above and obliquely, so the risk is bounded, but it is unverified.
6. **The unit count disagrees across sources** — 24 studios (Mission Housing's current
   page and the 2025 SF Heritage post), 27 (the 2018 SF Chronicle piece), "24-room"
   historically. It changes nothing geometric; it only affects how many windows glow
   at night, and 2.8 fixes that at four regardless.
7. **The building is NR-*eligible*, not NR-*listed*.** The 2019 nomination went to the
   State Historical Resources Commission with a favourable SF Planning
   recommendation, but the new owners chose not to proceed in 2020. Describe it as
   eligible and as an SF Heritage / SoMa Pilipinas cultural landmark; do not call it
   listed in any card copy or lore text.
8. **The 1907 date is from the nomination and is solid; the architect attribution is
   from the same document's §8** and is therefore as good as the nomination's own
   research. No independent corroboration of W. L. Schmolle's authorship was found,
   which is unsurprising for a speculative rooming house.
