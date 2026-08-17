# 49 South Park (Gran Oriente Filipino Residence) — SF-SIM asset plan

A 1909 Edwardian flats building on the corner of South Park and Jack London Alley,
bought by the **Gran Oriente Filipino** — the first Filipino-founded Masonic lodge in
the United States — in September 1947, and still owned by them. It is the second half
of a designated-eligible landmark complex whose other half, the Gran Oriente Filipino
Hotel at 104–106 South Park, is already in this manifest as `106-south-park`.

Where 104–106 is a narrow, flat-fronted, ornament-stripped tooth in a row, 49 South
Park is the opposite: a **corner building whose entire street face is bay windows** —
three rounded bays on three corners, four canted bays between them, all riding on
brackets under a wide bracketed cornice, over a ground floor of paired columned
entrances and four quatrefoil stained-glass rosettes. Two elevations are fully
exposed and fully detailed. It is the richest small building on the South Park oval
and, from the app's aerial camera, the only one that reads as a rectangle with
**rounded bulges**.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/49-south-park/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `49-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3935869, 37.7814643` |
| Target height | **13.0 m** to the corner-bay crown (roof deck 12.05 m, cornice crest 12.30 m) — LiDAR-derived, see 2.1 |
| Footprint | 12.90 m South Park frontage (NW) × 17.70 m deep; 228 m² of wall box, 278.6 m² of LiDAR outline including bays and rear stairs; measured |
| Triangle cap | 11,000 |
| Category | `2` (apartments) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 49 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 45–49 South Park in San Francisco (the Gran
Oriente Filipino Residence) and deliver it as a downloadable, validated GLB.

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
7. `artifacts/106-south-park/` — **the reference implementation.** The other half of
   the same landmark complex, the same owner, the same block, the same
   three-storey-over-basement Edwardian type, and the same 45°-rotated authoring
   frame. Its `build_106_south_park.py` shows the world-space authoring convention
   this asset must follow; its REPORT.md records two palette reversals worth reading
   before you pick colours.
8. `artifacts/102-south-park/` — the nearest example of a bay-windowed South Park
   front, for how much bay detail survives at this scale
9. `docs/asset-plans/49-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules. Do not invent a new style and do not copy
visual instructions from unrelated prompts.

## Must capture

- A **corner building**: 12.90 m of frontage on South Park (facing north-west, out
  over the oval) and 17.70 m of fully exposed flank on Jack London Alley (facing
  south-west). Both are hero elevations. Only the north-east side is a party wall.
- **The bay-window facade.** Three *rounded* bays on three corners and four *canted*
  bays between them, every one of them spanning the second and third storeys only,
  every one of them carried on brackets, every one with its own little cornice cap.
  This is the building; if the bays are timid the model is wrong.
- The **rounded corner bay** at the South Park × Jack London Alley corner, which
  wraps the corner on the diagonal and whose crown rises above the main cornice.
  This is the single strongest recognition cue and the tallest point of the model.
- The **wide overhanging cornice on chunky brackets** running unbroken around both
  street elevations.
- The **ground floor**: two entrances, each recessed behind a decorative iron gate
  and flanked by columns with Corinthian capitals, with **four quatrefoil stained-glass
  rosettes** in heavy cream moulding distributed around them, and a plain
  double-hung window at each end of the front.
- The **dark raised basement** — a painted-brick band about 1.5 m tall under the pale
  body, with small grilled windows and a thin red water-table stripe at its head. The
  base/body/cap layering is what makes this read as an SF Edwardian and not a box.
- The **flat roof** behind the cornice, and the fact that from above the cornice ring
  is not a rectangle: the bays push it out into three rounded bulges and four canted
  ones.

## Research 49 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation,
and gather references covering:

- The North-West (South Park) elevation and the South-West (Jack London Alley)
  elevation — both are visible in the app and both must be right
- Aerial and roof views: the roof layout in 2.9 is read off satellite imagery only
- Day and night appearance
- **The current paint scheme.** The dossier's colours come from two January 2017
  photographs in the landmark designation report. Nine years is long enough for a
  repaint. Find something more recent before you commit the hues; the *relations*
  (pale body, lighter trim, distinctly darker basement) are much safer than the
  values.
- **The bay count and rhythm.** The dossier reads four bays across the front and four
  along the flank from two photographs, one of them half-hidden by a street tree.
  Confirm it.

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**One trap is already known and is signposted here so you do not fall into it:** the
sibling building at 104–106 South Park was gutted and re-skinned in a $3.1 M
2019–2021 rehabilitation that *removed* its painted ornament, and `106-south-park`
had to be modelled as the post-rehab building rather than the nominated one. **49
South Park was not part of that project.** The rehabilitation permits are all on block
3775 lot **058**; lot **039** has no permit of any kind after a November 2018 street-space
permit, and no building permit after a 2016 rear-stair repair. The ornament described
in this plan is therefore expected to be intact — but that is an argument from an
absence of permits, so confirm it with a photograph.

## Create a reference dossier

Write `artifacts/49-south-park/REFERENCE.md` containing: source links and what each
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

This is a **secondary building** in the style bible's detail budget (§21) — but it is
the most articulated secondary building in the set, and the budget is spent almost
entirely on one thing: the bays. Everything else (siding boards, window mullions,
the ironwork of the gates, the fluting of the columns) goes.

Note the specific style risk here: the failure mode is a *lumpy* building. Seven
projecting bays on a 12.9 × 17.7 m box is a lot of silhouette, and if every bay is
modelled at full literal projection with full literal trim the result is a blob with
no readable form. The discipline is: bays project a real but modest amount, they all
sit on one shared bracket line and one shared cap line, and the cornice above them
stays a single clean unbroken ring. Read the aerial render early — this building is
judged from above first.

The finished asset must be immediately recognizable as 49 South Park, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1909 residence on the north-west half of lot 3775/039: body,
basement, all seven bays, both street elevations' openings, the two entrances, the
cornice, and the roof deck with its furniture.

**Do not include the Gran Oriente Filipino Masonic Temple at 95 Jack London Alley.**
It stands on the same lot, at the far (south-east) end, with a ~6 m gap between the
two buildings, and it is a separate address, a separate 1951 building and a separate
footprint in the bake. The integration exclusion is sized to leave the procedural
temple standing — see 2.13. If you model it, the scene gets two of it.

Do not include any other surrounding city geometry: South Park (the oval, its lawn or
paths), South Park Street, Jack London Alley, the neighbour at 41–43 South Park,
street trees, the sidewalk, parked cars, people, plinths, cameras or lights. Temporary
context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project
palette; `_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no
cameras, lights, animations, armatures or constraints; no external dependencies; at
most 11,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The South Park
front faces **north-west, outward normal 315.8°**; the Jack London Alley flank faces
**south-west, outward normal 225.8°**. The building is rotated ~45° off the world
axes, so build directly on the measured footprint in 2.3 rather than modelling an
axis-aligned box and rotating it (`artifacts/106-south-park/build_106_south_park.py`
does exactly this and is the pattern to copy). This is the case the plans README calls
out: the contract's "front faces −Y" rule cannot be honoured literally here, real-world
orientation wins, and the deviation must be recorded in `REPORT.md` with the measured
heading.

**Height normalization:** the tallest geometry in the export — the crown of the
rounded corner bay — must land at exactly the height you verify (this plan's figure is
**13.0 m**, with the roof deck at 12.05 m and the main cornice crest at 12.30 m) so the
loader's `targetHeightM / measuredHeight` scale is 1.0. If your research moves the
height, move the model and the draft manifest entry together and say so in `REPORT.md`.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/49-south-park/build_49_south_park.py` (deterministic build script),
`artifacts/49-south-park/49-south-park.blend`, and
`artifacts/49-south-park/49-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to
satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `49-south-park-top.png`,
`49-south-park-north.png`, `49-south-park-east.png`, `49-south-park-south.png`,
`49-south-park-west.png`, plus `49-south-park-contact-sheet.png`, at least one high
three-quarter aerial beauty render `49-south-park-aerial.png` taken over the
**west corner** so both street elevations and the corner bay are in frame, and a night
render `49-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation;
the top view must clearly show the cornice ring with its seven bulges, the roof
furniture and the corner-bay crown; the aerial view uses the style bible's camera
assumptions (30–50 degrees down, long lens). Simple tabletop lighting, neutral warm
background, minimal depth of field, and every image must depict the same exported
model.

For the night render, drive the `_Glow` materials from Base Color (copy `Base Color`
into `Emission Color`, strength 1.0) — see the note at the end of
`docs/asset-plans/README.md`. A re-imported GLB's `_Glow` materials otherwise render as
white slabs.

## Validate the exported GLB

Re-import `49-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Render at least one review image from the re-imported asset. Write
`artifacts/49-south-park/validation.json` and `artifacts/49-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **22 × 22 m** even though
the building is 12.9 × 17.7 m — that is the expected consequence of a ~45° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "49-south-park",
  "file": "49-south-park.glb",
  "anchor": [
    -122.3935869,
    37.7814643
  ],
  "targetHeightM": 13.0,
  "cat": 2,
  "name": "Gran Oriente Filipino Residence (45–49 South Park)",
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
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes
in `docs/asset-plans/49-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* or
*estimated* are visual or derived, not published figures — the executing agent must
re-verify anything it relies on.

This dossier is unusually well sourced for an ordinary flats building, because the
building is half of a proposed Article 10 landmark and the city's designation report
enumerates its character-defining features feature by feature. The weakest evidence
here is not the form; it is the **paint**.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 45–49 South Park (the street is signed "SOUTH PARK"; Google and the postal file render it "S Park St") | SF Assessor `property_location` = `0049 0045 SOUTH PARK`; DataSF EAS address points 45 / 47 / 49 all at `-122.393530, 37.781406` |
| Historic name | **Gran Oriente Filipino Residence** | SF Planning landmark designation report (draft 2017) |
| Block / lot | 3775 / 039 | SF Assessor secured roll; DataSF parcel `3775039`; DataSF footprints `mblr = SF3775039` |
| Built | **1909** | SF Assessor secured roll; designation report ("Built: 1907, 1909, 1951" for the three complex buildings) |
| Architect | **unknown** | designation report title page |
| Style | **Edwardian** | designation report: "45-49 South Park Street exhibits the typical characteristics of the Edwardian style" |
| Storeys | **3 over a raised basement** | designation report character-defining features; SF permits 2010–2016 (`number_of_existing_stories = 3`); both 2017 photographs |
| Construction | wood frame (assessor construction type `D`) | SF Assessor secured roll |
| Use | 7-unit apartment building, 40 rooms, 8 baths; assessor class `A5` "Apartment 5 to 14 Units" | SF Assessor secured roll (2024, 2025 closed rolls) |
| Owner | **Gran Oriente Filipino** since **September 1947** | designation report; still the owner of record |
| Zoning | SPD (SoMa South Park) | DataSF parcel; designation report |
| Historic status | Contributor to the South Park Historic District (period 1854–1935); Central SoMa Historic Resources Survey 2016; eligible but not listed on the California / National Registers; a 2017 draft Article 10 landmark designation report covers it | designation report; Central SoMa survey |
| Footprint (LiDAR outline) | 278.6 m², oriented bounding box 14.63 × 20.91 m at heading 45.8° | DataSF `ynuv-fyni` building `201006.0014671` — **measured** |
| Footprint (wall box) | **12.90 m** front × **17.70 m** deep = 228 m² | derived from the same polygon: the 12.88 m front edge and the 17.71 m south-west flank edge are the two clean measured sides; the extra outline area is bay and cornice overhang plus rear stairs |
| OSM footprint (cross-check) | 271 m², `way/71211339`, `addr:housenumber = 45;47;49`, `height = 12` | agrees with DataSF within 3%, and the OSM height agrees with the LiDAR median to 0.08 m |
| Parcel | 13.84 m frontage × 32.29 m deep = 447 m² (assessor `lot_area` 4,887 ft² = 454 m²) | DataSF parcel polygon — **measured** |
| Roof deck height | **12.08 m** above ground | **measured** — DataSF LiDAR median over 1,099 cells; mean 11.93, majority 12.05, σ 0.73 — a flat roof, so median ≈ deck |
| Tallest point | **13.00 m** above ground | **measured** — DataSF LiDAR `hgt_max`; assigned to the corner-bay crown, which every photograph shows rising above the cornice (*that assignment is inferred*) |
| Ground elevation | 10.99 m (NAVD88) | DataSF `gnd_min_m` — the app's terrain handles this, not the asset |
| Frontage heading | front faces **315.8°** (NW, over the park); alley flank faces **225.8°** (SW); party wall faces 45.8° (NE); rear faces 135.8° (SE) | measured from the footprint polygon |
| Neighbours | 41–43 South Park (NE, party wall, roof 9.83 m — **2.3 m shorter**); 101 South Park (across the alley to the SW, roof 5.56 m); Gran Oriente Masonic Temple, same lot, ~6 m to the SE (roof 7.84 m) | **measured** (DataSF LiDAR) |

### 2.2 Sources

- **SF Planning, *Gran Oriente Filipino Hotel, Residence, and Masonic Temple Complex*
  landmark designation report**, draft 2017 —
  `https://static1.squarespace.com/static/5b2c30b58f51305e3d641e81/t/607d36dc86015c6f61d7e31e/1618818784827/Gran+Oriente_Landmark+Designation+Report.pdf`
  — **the primary source.** Statement of significance, the Edwardian style attribution,
  the integrity assessment, the itemised character-defining features quoted in 2.4, and
  **two January 2017 colour photographs of this building** (page 19) covering the South
  Park front and the South Park × Jack London Alley corner with most of the alley flank.
  Landmark site boundary: "Encompassing all of and limited to Lots 058 and 039 in
  Assessor's Block 3775."
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived)
  — the authoritative footprint polygon and every height figure in 2.1. Two footprints
  carry `mblr = SF3775039`: `201006.0014671` (the residence, 278.6 m², median 12.08 m,
  max 13.00 m) and `201006.0108499` (the Masonic Temple, 112.9 m², median 7.84 m).
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF parcels) — lot `3775039`, address
  range 45–49, polygon and dimensions.
- `https://data.sfgov.org/resource/ramy-di5m` (DataSF Enterprise Addressing System) —
  the address points for 45, 47 and 49 South Park, which are all one point.
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property
  Tax Rolls) — 1909, 3 storeys, 7 units, 40 rooms, 11,010 ft² of building on a
  4,887 ft² lot, class A5, construction type D.
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — the whole permit
  history of lot 039 (12 permits, 1982–2018) and, critically, the *contrasting* permit
  history of lot 058. See 2.15 risk 1.
- `https://www.openstreetmap.org/way/71211339` — footprint cross-check,
  `addr:housenumber = 45;47;49`, `addr:street = South Park`, `building = yes`,
  `height = 12`.
- `https://knowthis.place/san-francisco/east-cut/south-park/45/` — a convenient
  aggregation of the assessor, permit and survey records for this parcel; used only to
  find the primary sources it cites (Central SoMa Historic Context Statement 2016,
  Heritage Rating C).
- `https://www.sfheritage.org/cultural-districts/soma-pilipinas/landmark-tuesdays-gran-oriente-filipino-hotel/`
  and `https://www.somapilipinas.org/cultural-assets-1/2018/7/25/gran-oriente-filipino-masoni-lodge`
  — SOMA Pilipinas / SF Heritage context on the lodge and the complex.
- Google Maps satellite (Vexcel / Airbus / Maxar imagery, 2026) — the roof layout in
  2.9. Google Street View exists for this corner (January 2025 capture) but would not
  render during this research pass; it is the first thing the executing agent should
  open, because it settles both open questions in 2.15.
- `artifacts/106-south-park/` — the sibling building's dossier, report and build script.

### 2.3 Orientation and placement

The building stands on the **south-east rim of the South Park oval, at the corner where
Jack London Alley meets it.** Its narrow front is on the park; its long flank runs back
along the alley; its north-east side is a party wall shared with 41–43 South Park (which
the Gran Oriente also owned until 2011); its rear faces a ~6 m gap and then the lodge's
1951 Masonic Temple. Like the whole SoMa grid it is rotated about 45° from the world
axes: the front edge runs at bearing **45.8°**.

Anchor: `-122.3935869, 37.7814643`, the centre of the wall box. Measured wall-box
corners, in Blender coordinates (metres, `+X` east, `+Y` north), relative to that
anchor:

```
W corner (front x alley)   ( -10.794,   1.848 )
N corner (front x party)   (  -1.546,  10.841 )
E corner (party x rear)    (  10.794,  -1.848 )
S corner (alley x rear)    (   1.546, -10.841 )
```

| Edge | Length | Outward normal | Elevation |
|---|---|---|---|
| `W -> N` | **12.90 m** | 315.8° (NW) | **South Park front** — hero |
| `S -> W` | **17.70 m** | 225.8° (SW) | **Jack London Alley flank** — hero, fully exposed |
| `N -> E` | 17.70 m | 45.8° (NE) | party wall with 41–43 South Park — blind |
| `E -> S` | 12.90 m | 135.8° (SE) | rear, faces the gap and the Masonic Temple |

Two notes on the outline:

- The LiDAR polygon's south-west line sits **1.36 m outboard** of the wall box, and its
  front line about 0.9 m outboard. That is not a survey error and it is not a bigger
  building: it is the **bay windows and the cornice**, which is exactly what a
  roof-derived outline traces. Use the wall box for the walls and let the bays project
  into the difference. The consistency check that this reading passes: the front edge
  (12.88 m) and the south-west flank edge (17.71 m) reproduce the wall box to within
  0.02 m.
- The rear edge carries three small projections reaching a further ~2.3 m — the exterior
  wood rear stairs that permits record being repaired in 2010 and 2016, plus a light
  well. They are invisible from both street elevations and from the app's camera, and
  they are the reason the LiDAR OBB is 20.91 m deep against a 17.70 m building. Model at
  most one simplified stair box, or none.

Because of the ~45° heading the axis-aligned bounding box will be about 22 × 22 m. That
is correct.

### 2.4 What each side shows

The designation report's character-defining features for this building, quoted, are the
spine of this section:

> - Three-story, plus raised basement rectangular massing and plan with flat roof
> - Brick cladding at basement, drop channel horizontal wood siding at first floor, and
>   horizontal tongue and groove horizontal wood siding
> - Regularly spaced fenestration pattern with brick sills at basement and wood window
>   frames and sills at first, second, and third stories
> - Rounded bay windows supported by brackets spanning second and third stories at
>   northeast, northwest and southwest corners of the building
> - Angled bay windows supported by brackets spanning the second and third stories
>   between rounded bays
> - Simple raised spandrel panels at bay windows
> - Wide, overhanging cornice supported by brackets
> - Two primary entrances on South Park Street flanked by wood squared engaged columns
>   and round columns both with Corinthian capitals
> - Four quatrefoil shaped stained glass windows surrounded by heavy molding flanking
>   primary entrances

(The report's compass words treat the park front as facing north; in true bearings its
"north-east / north-west / south-west corners" are this plan's N, W and S corners.)

**North-west (South Park front), 12.90 m.** The hero elevation. Three registers:

- *Raised basement*, ~1.5 m: painted brick, dark olive-grey, with small horizontal
  grilled openings, and a thin **red-oxide water-table stripe** at its head separating
  it from the pale body above.
- *First storey*: a flat wall carrying, from the party (NE) end to the alley (SW) end —
  a plain double-hung window, a quatrefoil rosette, **entrance 1**, two quatrefoil
  rosettes side by side, **entrance 2**, a quatrefoil rosette, a plain double-hung
  window. Each entrance is a shallow recess behind a decorative wrought-iron security
  gate, framed by a pair of round columns with Corinthian capitals against squared
  engaged columns. The rosettes are four-lobed cloverleaves in heavy cream moulding,
  glazed dark green-teal.
- *Second and third storeys*: **all bay**. A rounded bay at the N (party) corner, two
  canted bays, and the rounded corner bay at the W corner. Each bay is carried on
  brackets at the first-floor ceiling line, each has raised spandrel panels between and
  under its lights, and each carries its own small cornice cap at the top.
- *Cornice*: wide, overhanging, on closely spaced chunky brackets, unbroken across the
  whole front. Flat roof behind it.

**South-west (Jack London Alley flank), 17.70 m.** A real elevation, not a service
side, and the app's camera sees it as much as the front. The same three registers and
the same rhythm: the wrapping corner bay at the W corner, then flat wall with paired
double-hung windows, a canted bay, more flat wall, a second canted bay, and a rounded
bay near the S (rear) corner. The first storey and basement are flat, with regularly
spaced double-hung windows.

**North-east (party wall), 17.70 m.** Blind. Shares the boundary with 41–43 South Park,
whose roof is 2.3 m lower, so about 2.3 m of this wall is exposed above the neighbour in
the real city and in the baked city. Plain siding; one small light well notch about
2.3 m long and 2.3 m deep two-thirds of the way back (visible in the LiDAR outline).

**South-east (rear), 12.90 m.** Faces the gap to the Masonic Temple. *Inferred*: plain,
a rear door, a few openings and the wood stair structure the permits describe. No
usable photography was found and none is needed — it is invisible from every camera
angle the app allows.

**Top.** See 2.9.

### 2.5 Recognition cues (ranked)

1. **The bays — seven of them, three rounded, on two adjacent elevations.** No other
   building on the oval looks like this. From the aerial camera the cornice ring is a
   rectangle with rounded bulges, and that silhouette alone identifies it.
2. **The rounded corner bay wrapping the South Park × Jack London Alley corner**, its
   crown standing proud of the cornice. It is the tallest and most photographed thing
   about the building.
3. **The wide bracketed cornice** — a strong horizontal cap on a strongly modelled body.
4. **The pale body over a dark raised basement**, with cream trim: the SF Edwardian
   base / body / cap sandwich.
5. **The quatrefoil rosettes and twin columned entrances** — small, odd, heraldic, and
   the thing a person who knows this building remembers about its ground floor.

### 2.6 Miniature translation

**Preserve**

- The corner condition: two fully detailed elevations meeting at a rounded bay, on the
  real 45.8° heading.
- The seven-bay rhythm and the *distinction* between rounded and canted bays. If they
  all become canted, the building loses its identity; if they all become rounded, it
  becomes a wedding cake.
- The single shared bracket line under the bays and the single shared cap line above
  them — the discipline that keeps seven projections from reading as lumps.
- The three-register elevation: dark basement, first storey, two bay storeys, cornice.
- The four quatrefoils. They survive only if exaggerated (below).

**Simplify / exaggerate**

- Rounded bays become **low-segment cylinder segments (9 segments across ~150°)**, not
  smooth revolutions. Canted bays become three flat faces. Both project **0.85–0.95 m**,
  slightly less than the real ~1.1 m, so the silhouette stays legible from above.
- Bay brackets become one continuous chamfered shelf under each bay, not individual
  scrolls. Cornice brackets become a **dentil-like run of small blocks** — the reading is
  "a bracketed cornice", not "thirty-four brackets".
- Window mullions and the double-hung meeting rails go entirely. Each bay light becomes
  one flat glass panel in a chunky cream frame; the spandrel panels below become one
  recessed rectangle per bay per floor.
- The quatrefoils are **enlarged to ~1.3 m across** (from ~0.9 m) and become a cream
  torus-free four-lobe plate with a dark teal centre — a flat two-piece decal in relief,
  no moulding profile. This is the one place semantic exaggeration is spent on the
  ground floor.
- The entrances become a 1.6 m recess 0.35 m deep with a dark opening, flanked by two
  simple cream cylinders with a chunky square abacus for a capital. No fluting, no
  acanthus, no ironwork; the gate becomes a dark flat panel.
- Basement grilles become small dark recessed rectangles. The red water-table stripe
  stays — it is one thin band and it is worth a lot.
- Wood siding boards are **not** modelled. If the aerial render looks flat, add at most
  two shallow horizontal grooves per storey, as `106-south-park` does on its flank.
- Rear stairs and light wells: one simplified box or nothing.

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render, and adjust *all* of them if
the verified height differs from 13.0 m. Positions along an elevation are given as `s`,
measured from the W corner.

1. **Body**: extrude the 2.3 wall box (12.90 × 17.70 m) from z = 0 to z = 11.20,
   `Toy_stone`.
2. **Raised basement**: z = 0 → 1.50, the same plan **outset 0.06 m**, `Toy_roofd`. A
   `Toy_red` water-table stripe 0.10 m tall at z = 1.40 → 1.50, running both street
   elevations only. Six small recessed openings 0.7 × 0.45 m on the front, eight on the
   alley flank, `Toy_ink`.
3. **First storey**, z = 1.50 → 4.80, flat wall on both street elevations:
   - Front: windows 1.1 × 2.1 m recessed 0.12 m at s = 0.9 and s = 12.0; entrances
     1.6 m wide × 2.9 m tall recessed 0.35 m at s = 4.2 and s = 8.4, opening `Toy_ink`,
     head trim and column pair `Toy_trim` (columns Ø 0.30 m, 8 segments, square abacus
     0.40 × 0.40 × 0.18 m); quatrefoil rosettes at s = 2.6, 6.0, 6.9, 10.2, centred at
     z = 3.9, 1.3 m across, `Toy_trim` plate with a `Toy_navy` centre disc.
   - Alley flank: five windows 1.1 × 2.1 m recessed 0.12 m at even centres from s = 2.2
     to s = 15.6.
4. **Bay bracket shelf**: a continuous chamfered ledge at z = 4.55 → 4.80 under every
   bay, projecting 0.10 m further than the bay above it, `Toy_trim`.
5. **Bays**, all spanning z = 4.80 → 11.20, all projecting **0.90 m**:
   - *Rounded*, chord 3.40 m, a 9-segment cylinder segment: at the **W corner**
     (centred on the corner and rotated onto the corner bisector, bearing 270.8° — the
     hero), at the **N corner** on the front, and at the **S corner** on the flank.
   - *Canted*, front face 1.9 m with 0.75 m returns at 45° (chord 3.0 m): two on the
     front at s = 5.0 and s = 8.2, two on the flank at s = 6.6 and s = 11.4.
   - Each bay: two glass bands (z 5.35–7.55 and 8.55–10.75) `Toy_glass` in `Toy_trim`
     frames 0.16 m wide, with a recessed spandrel panel 0.5 m tall below each band.
   - Each bay cap: z = 11.20 → 11.95, `Toy_trim`, projecting 0.12 m beyond the bay.
6. **Cornice**: bed mould at z = 11.20, a run of bracket blocks 0.22 × 0.22 × 0.55 m at
   0.55 m centres from z = 11.30 to 11.85, crown fascia z = 11.85 → 12.30 overhanging
   **0.55 m**, `Toy_trim`. It runs unbroken around the front, the alley flank and 1 m
   round each end; the party and rear elevations get a plain parapet band instead.
7. **Roof deck** at z = 12.05, `Toy_steel`, inside the cornice. Furniture (2.9): one
   roof hatch 1.2 × 1.2 × 0.35 m `Toy_ink`; one skylight bank 2.6 × 1.4 × 0.30 m
   `Toy_glassl` toward the rear third; two vent stacks Ø 0.25 × 0.9 m `Toy_trim`; one
   small mechanical block 1.4 × 1.0 × 0.6 m `Toy_roofd`.
8. **Corner-bay crown**: over the W-corner rounded bay only, a stepped cap rising from
   the cornice crest to **z = 13.00** — the model's height normalization target.
9. Bevel 0.10 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_stone` | `#d9d2c2` | the body — all three storeys of wall and every bay's solid faces |
| `Toy_trim` | `#f3efe6` | cornice, brackets, bay caps, bay frames, window trim and sills, columns, quatrefoil plates, vent stacks |
| `Toy_roofd` | `#45454a` | the raised basement, the roof mechanical block |
| `Toy_red` | `#c4453c` | the water-table stripe at the head of the basement |
| `Toy_glass` | `#2a4d73` | all windows |
| `Toy_navy` | `#2c4a70` | the quatrefoil rosettes' glazed centres |
| `Toy_ink` | `#3a3530` | entrance openings and gates, basement openings, roof hatch |
| `Toy_steel` | `#9aa0a6` | the flat roof deck |
| `Toy_glassl` | `#6f95b8` | the roof skylight bank |
| `Toy_glass_Glow` | `#2a4d73` | the lit bay windows at night |
| `Toy_trim_Glow` | `#f3efe6` | a warm spill in the two entrance recesses at night |

Three notes on colour:

- **The body colour is the weakest observation in this dossier.** Both photographs are
  January 2017, overcast, and the elevation was in shadow behind a full-grown street
  tree. What they establish reliably is the *relation*: a pale, slightly green-grey body;
  trim clearly lighter than the body but not white; a distinctly darker basement; a thin
  red line between them. `Toy_stone` over `Toy_trim` over `Toy_roofd` reproduces that
  relation with palette entries. If the executing agent finds a 2025 Street View pano
  showing a warmer or cooler scheme, adjust and say so in `REPORT.md`.
- **Do not push the body toward `Toy_cream`.** The sibling at 104–106 is `Toy_cream`, and
  these two buildings sit 90 m apart on the same oval under the same owner; if both are
  the same near-white they merge in the aerial view. This one is genuinely the greyer,
  greener of the pair, and `Toy_stone` keeps them distinguishable.
- The palette has no true olive. The real basement is a dark grey-green; `Toy_roofd`
  (`#45454a`) is the closest and is the safe choice. Off-palette is a WARN not a FAIL,
  so a dedicated `Toy_olive` at roughly `#4c4d42` is permissible if the render justifies
  it — decide from the aerial render and record the decision in `REPORT.md`.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
glazing — the app renders `_Glow` in a separate layer, and a *closed* glow shell is two
alpha layers deep, so it reads far brighter by day than a single face does. Author glow
as single faces standing 0.02 m proud of the glass, never as boxes, and never as the
primary surface. Hero glow: the bay windows of the **corner bay** and about half of the
other bays' lights, lit unevenly — this is seven apartments, not an office floor, and an
evenly lit grid reads institutional. Supporting accent: a warm spill in the two entrance
recesses. Nothing else glows; there is no signage, no crown lighting and no storefront.

### 2.9 Top surface

A flat roof about 12.05 m up, on a corner the camera flies over constantly. From 2026
satellite imagery: a uniform **taupe / warm mid-grey membrane**, noticeably darker and
warmer than the near-white roofs of the newer buildings across the alley — that contrast
is a real and useful cue, so do not make this a pale "cool roof". Visible on it: a small
dark square roof hatch near the centre, a pale grid-like skylight or light-well grating
toward the rear (south-east) third, and a scatter of small vents and pipes. Nothing
large; no PV array, no plant deck.

The thing that actually matters from above is **the cornice ring**. It is the brightest
element on the building and it is not a rectangle: the seven bays push it outward into
three rounded and four canted bulges along two of its four sides, while the party and
rear sides stay straight. Keep the cornice value clearly lighter than both the deck and
the body so the ring reads, and get the bulges right — that plan silhouette is this
building's signature in the app's default view.

### 2.10 Scope

**In the GLB:** the 1909 residence on the north-west half of lot 3775/039 — basement,
body, all seven bays, both street elevations' openings, the two entrances, the cornice,
the roof deck and its furniture, and at most one simplified rear stair box.

**Not in the GLB:** the Gran Oriente Filipino Masonic Temple at 95 Jack London Alley
(same lot, ~6 m to the south-east, kept procedural — see 2.13), 41–43 South Park, 101
South Park, South Park itself, South Park Street, Jack London Alley, street trees,
sidewalk, vehicles, people, plinths, cameras or lights.

### 2.11 Triangle budget

Cap **11,000** — higher than the 3.9k of `106-south-park` and the 7.5k of
`101-south-park`, because this building has two hero elevations and seven bays, and it
is the articulation that carries the recognition. The cap should still bind. Suggested
split: body, basement and rear ~1,200; three rounded bays (9 segments × 2 storeys, caps
and spandrels) ~2,400; four canted bays ~1,500; bracket shelf and cornice with its
bracket run ~2,200; first storey (2 entrances, 4 columns, 4 quatrefoils, 7 windows)
~2,200; bay glazing ~800; roof deck and furniture ~700.

If the count runs over, take it out of the cornice bracket run (fewer, chunkier blocks)
before taking it out of the bays.

### 2.12 Draft manifest entry

```json
{
  "id": "49-south-park",
  "file": "49-south-park.glb",
  "anchor": [
    -122.3935869,
    37.7814643
  ],
  "targetHeightM": 13.0,
  "cat": 2,
  "name": "Gran Oriente Filipino Residence (45–49 South Park)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated. `estimated`
is `false` because both height figures are measured LiDAR values cross-checked against
OSM's `height = 12`; the executing agent should flip it to `true` only if it moves the
height onto a photogrammetric estimate. The anchor is the wall-box centre — once the
model exists, move it so it coincides with the model's **XY bounding-box centre**
(the bays project on two sides only, so the two are not identical), and record the shift
in `REPORT.md` exactly as `106-south-park` did.

`cat: 2` (apartments), matching the assessor's `A5 — Apartment 5 to 14 Units` and the
sibling `106-south-park`.

### 2.13 Integration notes (for later, not this task)

- **New landmark, Case B.** Neither `pipeline/lib/landmarks.mjs` nor `app/src/landmarks.js`
  knows this id. Integration needs a `pipeline/lib/landmarks.mjs` entry
  (`id: '49SouthPark'`) **and a re-bake of the affected tiles**, or the baked procedural
  building on this footprint will intersect the GLB.
- **The exclusion radius must be small — target `exclude: 3`, and it must not exceed
  5.0 m.** `excluded()` in `pipeline/buildings.mjs` drops a footprint when its *centroid
  or any of its vertices* falls inside the circle, so a radius only has to reach this
  building's own ring centroid to delete it. Meanwhile 41–43 South Park is a party-wall
  neighbour whose nearest vertex is **5.24 m** from this footprint's area centroid, and a
  radius that reaches it deletes the whole of 41–43. The South Park block is already
  calibrated for exactly this: `165SouthPark` uses `exclude: 1.3`, `160SouthPark` 1.2,
  `132SouthPark` 2, `106SouthPark` 2.1, `101SouthPark` 4.
- **Do not exclude the Masonic Temple.** The second footprint on this lot
  (`201006.0108499`, 112.9 m², roof 7.84 m) is the 1951 Gran Oriente Filipino Masonic
  Temple at 95 Jack London Alley. It is a separate building the GLB does not contain, it
  is ~6 m clear of this one, and its nearest vertex is 11.4 m from this footprint's
  centroid. A correctly sized `exclude` leaves it alone and it stays procedural, which is
  what we want. **Do not add an `extraExclusions` entry for it** — that is the mechanism
  `132SouthPark` uses to clear a multi-building lot it *does* model in full, and using it
  here would punch a hole in the block.
- Expect the re-bake to drop **one or two rings** for this site, not one: DataSF and
  Overture both trace parts of this block, so `verify-rebake.mjs` reporting two removals
  at this anchor is normal. What it must *not* report is a removal at 41–43, 101, or the
  temple.
- **The procedural stand-in here is about the same height as the asset** (LiDAR median
  12.08 m against a 13.0 m crown), which is the dangerous case: an un-baked local check
  will look almost right whether or not the exclusion is correct. Do the bake before
  judging, and check the neighbours are still standing rather than checking that this
  building looks fine.
- `loadRadius`: the default formula gives `max(2500, 13.0 × 30) = 2500` m. Take the
  default.
- Camera preset: `app/src/camera.js` puts the eye at `target + distance × (sin yaw, ., cos yaw)`
  with `+z` south, so camera bearing = 180 − yaw. This building's whole point is its
  corner, whose outward bisector is 270.8°, so **`yaw: 270`** stands the camera due west
  and frames both street elevations and the corner bay at once. `distance: 165`,
  `pitch: 26` — in line with `106SouthPark` (150 at 11.58 m) and `181SouthPark`
  (190 at 16.5 m). No `key`: at 13 m this is texture in the block, not a destination.
- Name it **"Gran Oriente Filipino Residence (45–49 South Park)"**, parallel to the
  existing `106-south-park` entry "Gran Oriente Filipino Hotel (104–106 South Park)".
  The two entries are the two halves of one landmark and should read that way in the
  search list.
- If other landmarks are in flight, run stage 5 in **batch mode** (see
  `docs/asset-pipeline/ADDRESS-TO-ASSET.md`): still bake, still QA the bake, then throw
  the bake away and commit source only.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 13.0 m — the corner-bay crown, not a stray vent (loader
      scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~22 × 22 m is
      expected)
- [ ] Triangles at or under 11,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on bay windows and the two entrance recesses; glow authored as single
      faces proud of the opaque glazing, never closed shells
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume
      for the union of solids; ray-test residual ≤ 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] The top view shows the cornice ring's seven bulges clearly
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

1. **Has the building been repainted or altered since January 2017?** This is the one
   question the executing agent must answer before modelling, and it has a specific
   reason for existing: the sibling at 104–106 South Park was gutted and re-skinned
   between 2019 and 2022 under a $3.1 M "rehab/renovation improvement for single room
   occupancy" permit, and that project **removed** the painted ornament every earlier
   photograph shows — `106-south-park` had to be modelled as the post-rehab building.
   The evidence that 45–49 escaped it is entirely negative: the rehabilitation permits
   are all on lot **058**, while lot **039** shows nothing after a November 2018
   street-space permit and no building permit after a 2016 rear-stair repair. That is
   good evidence, and the same permit dataset does capture the lot-058 work, so the
   absence is meaningful — but it is still an absence. **Open the January 2025 Street
   View pano and confirm with your eyes.**
2. **The bay rhythm is read from two photographs.** The front reads as rounded / canted
   / canted / rounded and the flank as (corner rounded) / canted / canted / rounded, but
   the front photograph is half-hidden by a street tree and the flank photograph is
   oblique. The *count* of rounded bays (three, one per exposed corner) is stated in the
   designation report and is solid; the number and spacing of the canted bays between
   them is inferred. Confirm before committing the facade rhythm — this is the one thing
   that would make the model wrong rather than merely approximate.
3. **Does the corner bay really wrap the corner?** This plan models it as a rounded bay
   centred on the W corner and rotated onto the corner bisector, because that is what the
   2017 corner photograph appears to show and because it is by far the strongest reading
   for the miniature. The alternative — two separate rounded bays, one on each elevation,
   meeting at the corner — is not fully excluded by the available imagery. Settle it from
   Street View and record the decision.
4. **The 13.00 m figure is measured; its *attribution* is not.** DataSF's `hgt_max` over
   this footprint is 13.00 m and the median is 12.08 m, which is a textbook flat-roof
   signature with one taller element. This plan assigns the taller element to the
   corner-bay crown because that is what the photographs show standing above the cornice
   line. It could instead be a vent stack or a stair bulkhead. If the executing agent
   concludes it is a vent, the correct move is to keep the crown at 13.0 m anyway (a
   vent must never be the model's height normalization target) and note it.
5. **The floor-area arithmetic does not close cleanly.** The assessor records 11,010 ft²
   (1,023 m²) of building on this lot. Three storeys plus basement on a 228 m² wall box
   is about 912 m², and the temple adds roughly 226 m² over two floors — together
   1,138 m², about 11% over. The discrepancy is not large enough to change anything, and
   AGENTS rule 5 settles the method regardless: model the addressed building on its own
   measured footprint.
6. **The rear elevation is entirely inferred**, as is the party wall above 41–43's
   roofline. Neither is visible from any camera position the app allows, and neither is
   worth research time — but they must still be plausible, not blank.
7. **Style risk: lumpiness.** Seven bays on a small box is the most articulated
   silhouette in the South Park set. The failure mode is a model that reads as a lump of
   bumps rather than a building. The three things that prevent it — one shared bracket
   line, one shared cap line, and one clean unbroken cornice above them — are called out
   in 2.6 and 2.7 and none of them is optional.
