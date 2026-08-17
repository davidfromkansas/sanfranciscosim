# 92 South Park (86–96 South Park) — SF-SIM asset plan

The **one Modernist building on the South Park oval**, and the only one in this whole
plan set that is not a survivor of the district's 1900s–1920s brick-and-frame stock.
**86–96 South Park Street, built 1996 to Toby S. Levy's design** (Levy Design Partners /
LDP Architecture, whose office is still unit 90 and whose home is still unit 94), is a
six-unit live/work condominium on the corner of South Park Street and Jack London Alley,
framed entirely in **lightweight steel** and clad in **a deliberately mismatched
vocabulary of metals** — lead-coated zinc panel, weathering copper sheet, copper shingle
and dark blue-black glazed tile — chosen, in the architect's words, to "express their
nature and age gracefully". San Francisco Heritage calls it *"a loft unit building with
an ambiguated facade of cubic forms … where Georgian townhouses had stood before the
1906 earthquake and fire."*

Two things make it read from the app's downward camera in a way no neighbour does:

1. **It is a courtyard building.** A 14.5 m × 30 m corner lot carries a full-width front
   mass on South Park, a narrow bar down the Jack London Alley side at the rear, a thin
   arm down the party wall with 84 South Park, and an **open paved court** between them
   with an external steel stair and a curved corrugated wall in it. From above it is a
   C, not a bar — the only C on the oval.
2. **It is a colour outlier.** Every other building modelled on this oval is white,
   cream, pale stucco or dark brick. This one is **cool silver-gray metal with a deep
   rust-brown corner tower and a near-black tiled base**, plus one saturated red column
   at the street corner. It is the value-and-hue slot nothing else on the rim occupies.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/92-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `92-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3941630, 37.7819166` (union OBB centre of the two DataSF footprints, measured) |
| Target height | **13.28 m** to the corner-tower crest; front-block roof deck 11.15 m, rear bar deck 12.32 m — LiDAR-derived, see 2.1 and 2.15 |
| Footprint | corner lot **14.47 m frontage × 30.06 m deep** at 44.78°/134.82°; **289.7 m² built** on a 435 m² lot (front block 208.7 m², rear bar 81.0 m², court ~72 m²); measured |
| Triangle cap | 12,000 |
| Category | `2` (`apartments`) — six Live/Work Condominium lots, four residential + two commercial |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 92 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 92 South Park (the building addressed
86–96 South Park Street) in San Francisco and deliver it as a downloadable,
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
7. `artifacts/132-south-park/` — the closest reference implementation for the
   *problem*, not the style: it is the other South Park lot whose asset has to
   represent **two separate structures with a gap between them** on one anchor, and
   its `build_132_south_park.py` helper set (`prism`, `ring_band`, `face_panel`,
   `lot_box`, `rect_opening`) is the intended starting point. Adapt the constants,
   do not rewrite the helpers.
8. `artifacts/106-south-park/` — read its `PALETTE_HEX` block for how a per-asset
   palette is documented in place, and its REPORT.md for how a reversed colour
   decision is recorded.
9. `docs/asset-plans/92-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Read 2.15 before you start

The footprint, the lot frame, the anchor and the exclusion window are measured to
survey accuracy. **The crest is a choice between two LiDAR maxima that differ by
0.45 m**, and the 1996 photographs that carry almost all of the material evidence are
**thirty years old** — the copper in them has since weathered from orange to dark
brown. 2.15 says exactly which is which. Do not promote the inferred paragraphs to
fact in `REFERENCE.md`.

## Must capture

- The **C-plan around an open court**. Three masses on one lot: a full-width front
  block on South Park, a narrow bar down the Jack London Alley side at the rear, and a
  thin arm down the 84 South Park party wall — with a real, open, paved court between
  them. From the app's downward camera this void is the entire identity. Do not fill
  it, do not roof it, do not simplify the plan to a rectangle
- The **corner tower** at South Park × Jack London Alley: a projecting weathering-metal
  cube carried the full height and up past every neighbouring parapet. It is the crest —
  the bounding-box top lands on it
- The **red column** on that corner, floor to parapet: a single saturated vertical in
  an otherwise entirely desaturated building. It is the one accent the palette gets and
  it is what makes the building findable at thumbnail size
- **Cubic forms that do not line up.** Levy's own word is "ambiguated": volumes step in
  and out by 0.3–0.8 m, parapets sit at three different heights, and one parapet is
  **raked** (a straight diagonal, not a gable). Model the steps; a flush facade is the
  wrong building
- A **cool silver-gray metal body** (`Toy_steel`) as the field, with **rust-brown
  weathering metal** (`Toy_rust`) on the corner tower and the rear bar's upper volume,
  and a **copper-shingle panel** (`Toy_cocoa`) on the Jack London Alley end
- A **near-black blue tiled base** the full perimeter, about one storey tall, carrying a
  thin **mosaic accent stripe** — one horizontal line of `Toy_teal` at about 1.6 m. That
  stripe is 1996 and it is on every published photograph of the base
- **Two beige roll-up garage doors** on the Jack London Alley elevation, and two
  **commercial shopfronts** on the South Park frontage (units 86 and 92 are the two
  commercial condominiums)
- Large, irregular, deliberately unaligned windows in near-black frames, several with
  **projecting hinged sunshade panels** and small **balconies with teal-green rails**
- Two **polished stainless flue pipes** running the full height of the court elevation.
  They are thin, they are bright, and they are the most-photographed detail on the
  building after the red column
- A roof designed for the downward camera: three parapets at three heights, one raked;
  a **triangular skylight** over the front block (visible in current aerial imagery); a
  **curved element** at the court's south end; a roof deck with rail

## Research 92 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- **Which of the two LiDAR maxima is the crest** (13.28 m on the front block vs 13.73 m
  on the rear bar) — see 2.1 and 2.15. This plan builds 13.28 and says why
- **What the copper looks like in 2026.** Every published photograph of this building
  except one is from 1996–1997, when the copper was orange. The 2025 San Francisco
  Heritage photograph shows it dark chocolate-brown. Build the weathered state
- **The rear (north-west) elevation**, onto the backs of the Bryant Street block — no
  source consulted here shows it at all
- **The court's current state.** The 1996 photographs show a curved corrugated wall, an
  external steel stair and curved balcony rails; current aerial imagery shows a
  triangular skylight and what may be a tarpaulin over part of the court. Decide what
  is there now, and say which evidence you decided on
- The bay count and the current shopfront occupancy on the South Park frontage
- Day and night appearance

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**One resolution is already known and must not be silently re-opened:** "92 South Park"
is **not a separate building**. It is one of six condominium lots (block 3775, lots
116–121) on a single 435 m² parcel whose building is addressed 86–96 South Park, and
the numbers 88/90/92/94/96 were all assigned to it in one 2003 address-assignment
permit on the original 86 South Park. Model the whole building. See 2.15 risk 1 —
there is a sibling `pipeline/96-south-park` branch that resolves to the same parcel.

## Create a reference dossier

Write `artifacts/92-south-park/REFERENCE.md` before modelling: what the building is,
every source and what it establishes, the verified dimensions with per-row confidence,
observations from all four sides and above, the recognition cues, the massing recipe,
the palette map, and the corrections you made to this plan. `REFERENCE.md` outranks
this plan wherever they disagree.

## Build, validate, render

Deterministic scripts, no interactive Blender work:

- `build_92_south_park.py` — writes `92-south-park.blend` and `92-south-park.glb`
- `validate_92_south_park.py` — factory-resets, imports **only the exported GLB**,
  writes `validation.json`
- `render_92_south_park.py` — six review renders (four elevations, top, high
  three-quarter aerial) plus the night aerial
- `make_contact_sheet.py` — the contact sheet, night tile included

Contract gates, all of which must PASS in `validation.json`:

- GLB, real metres, +Z up in Blender / +Y up on export, applied transforms
- Origin at the footprint centre, `min Z` within 0.5 m of 0, XY centre offset ≤ 1 m
- **Bounding-box top exactly 13.28 m**, so the loader's `targetHeightM / measuredHeight`
  scale lands at 1.0
- ≤ 12,000 triangles
- All materials `Toy_*`, flat colours, no textures, no alpha, no `Toy_body`
- `_Glow` only on night-glow surfaces, authored as thin shells proud of the opaque
  glazing — never as a primary surface, and never as a closed shell (a closed `_Glow`
  box is two alpha layers and reads ~23% by day, not 12%)
- No cameras, lights, animations, armatures, constraints, no leaked foreign geometry
- Outward normals: per-object signed volume authoritative for the union of solids,
  ray test residual ≤ 0.15%

Review the high three-quarter aerial FIRST and iterate on it. Only then run the formal
render rig. Log every iteration in `REPORT.md`.

## Deliverables

`artifacts/92-south-park/` containing the two scene files, the three scripts plus the
contact-sheet script, seven renders, the contact sheet, `validation.json`,
`REFERENCE.md` and `REPORT.md`. Commit; do not integrate.
````

---

## Part 2 — Research and design dossier

### 2.1 Identity, dates and dimensions

| Item | Value | Confidence |
|---|---|---|
| Address | 92 South Park Street, San Francisco, CA 94107 — one of six unit addresses (86, 88, 90, 92, 94, 96) on the building **86–96 South Park** | **verified** |
| APN (block / lots) | **3775-116 … 3775-121**, six condominium lots on ONE 435 m² parcel | **verified** — DataSF parcels `acdm-wktn`; all six carry identical geometry and the address ranges 86-86, 86-88, 86-90, 86-94, 86-96 |
| OSM ways | **113545691** (`addr:housenumber = 92`, `addr:street = Jack London Alley`, `building = apartments`, `building:levels = 4`) and **113545685** (untagged) | **verified** |
| Built | **1996** | **verified** — SF Assessor roll `year_property_built = 1996` on five of the six lots; SF Heritage; construction permit 9318430 filed 20 Oct 1993 |
| Architect | **Toby S. Levy, FAIA — Levy Design Partners / LDP Architecture**, whose own office (unit 90) and residence (unit 94) are in it | **verified** — Architizer project page (firm's own listing); SF Heritage; Assessor owner record for lot 118 (Holman-Levy family trust) |
| Programme | **six units: four residential + two commercial**, all "Live/Work Condominium" | **verified** — Architizer project description; Assessor roll (`Live/Work Condominium` ×5, `Office - Condominium` ×1) |
| Structure | **framed entirely in lightweight steel**; non-toxic, renewable and recycled materials throughout | **verified** — Architizer, the firm's own text |
| Storeys | **4** | **verified** — OSM `building:levels = 4`; permits 2015/2025 record `number_of_existing_stories = 4`. The 1993 original application says 3, and 1994–1995 revisions say 3 or 4; the built condition is 4 |
| Unit areas | 741 / 1,195 / 1,257 / 1,947 / 2,262 / 2,345 sq ft = **9,747 sq ft** total | **verified** — Assessor roll, lots 121/116/117/120/119/118 |
| Address history | 88, 90, 92, 94 and 96 South Park were all created by **one "address assignment - additional" permit dated 8 Oct 2003** against 86 South Park | **verified** — SF building permits `i98e-djp9` |
| Parcel | **14.47 m × 30.06 m, 435 m²**, corner of South Park Street and Jack London Alley | **measured** — DataSF parcels |
| Built footprint | **289.7 m²** — front block 208.7 m² (`sf16_bldgid 201006.0022147`) + rear bar 81.0 m² (`201006.0149656`); both carry `mblr = SF3775116` | **measured** — DataSF LiDAR footprints |
| Anchor (WGS84) | **`-122.3941630, 37.7819166`** | **measured** — union OBB centre of the two DataSF footprints (31.31 × 15.03 m at 133.11°) |
| Lot frame | frontage runs **44.78°** (NE); depth runs **134.82°** (NW). Parcel in that frame, from the anchor: `u ∈ [−7.13, +7.34]`, `v ∈ [−15.95, +14.11]` | **measured** |
| Front-block roof deck | **11.15 m** | **measured** — DataSF LiDAR `hgt_mediancm = 1115` over 837 cells |
| Rear-bar roof deck | **12.32 m** | **measured** — DataSF LiDAR `hgt_mediancm = 1232` over 324 cells |
| **Corner-tower crest (target height)** | **13.28 m** | **measured** — DataSF `hgt_maxcm = 1328` on the front block; see 2.15 risk 2 for why this and not the rear bar's 13.73 m |
| Absolute crest | **≈ 24.13 m NAVD88** | **measured** — `peak_1st_m` 24.11 (front) / 24.15 (rear): the two polygons sample the *same* physical high point |
| Ground | 10.65–11.06 m NAVD88 | measured; the app's terrain handles this, not the asset |
| Street frontage | faces **224.8° (SW→SE arc of the oval)**, i.e. the frontage edge runs NE and the building looks out over the park to the **south-east** | **measured** from the parcel |

### 2.2 Sources and what each establishes

| Source | Establishes |
|---|---|
| **Architizer, "86 - 96 South Park" by LDP Architecture, Inc.** (`https://architizer.com/projects/86-96-south-park/`) | The firm's own project record: four residential units and two commercial spaces on a corner site; "overlay of geometries reflecting the position of the buildings on the site"; framed **entirely in lightweight steel**; non-toxic/renewable/recycled materials; "adjust the scale of forms and elements to assemble a **complex vocabulary of materials that will express their nature and age gracefully**". Also the **seven original 1996–97 photographs** (`JLSP_*`, `8912*`) that carry nearly all the material evidence in 2.4 |
| **San Francisco Heritage, "The Rise of Modern SOMA"**, Woody LaBounty, 27 Oct 2025 (`https://www.sfheritage.org/heritage-in-the-neighborhoods/the-rise-of-modern-soma/`) | The 1996 date and the attribution to Levy Art + Architecture; the phrase "**ambiguated facade of cubic forms**"; the pre-1906 Georgian townhouses on the site; and **the only recent photograph** of the building (Oct 2025), which is what establishes the weathered state of the metals |
| DataSF Building Footprints, LiDAR-derived (`ynuv-fyni`) | The two authoritative footprint polygons and their height statistics (front: median 11.15 m, max 13.28 m, mean 10.99 m, std 1.51 m, 837 cells, raster `Sanfran_Orig_1241.flt`; rear: median 12.32 m, max 13.73 m, std 1.56 m, 324 cells, raster `Sanfran_Orig_1245.flt`). **Flown 2010** — fourteen years after construction, so unlike most plans in this set the survey is *younger* than the building and describes it correctly |
| DataSF Parcels (`acdm-wktn`) | That lots 3775-116 … 3775-121 are six condominium lots on **one** 435 m² polygon with a 14.47 m frontage — the fact that resolves "92 South Park" |
| SF Assessor Historical Secured Property Tax Rolls (`wv5m-vpq2`) | 1996; six Live/Work Condominium units; per-unit areas; the Holman-Levy ownership of lot 118 (94 South Park) |
| SF Building Permits (`i98e-djp9`) | Application **9318430**, 20 Oct 1993, "erect a three story two unit residential bldg" at 86 South Park, and its 1994–95 revision run ("add one wndw on side & rear elevation", storefront change, kitchen alterations); the **8 Oct 2003 address assignments** for 88/90/92/94/96; a 2015 ground-floor office renovation in "suite F" of ~900 sq ft; 2024 reroofing at 86 and 88; a 2025 third-floor bathroom remodel at 94 |
| Kidder Mathews lease flyer, **"92 South Park St"** | That unit 92 is a **±1,075 RSF ground-floor office** — one of the building's two commercial condominiums — "located on a premier corner of South Park" |
| Overture Maps buildings (the bake's own gap-fill input) | Two polygons over this lot — `ea748f47…` (OSM-sourced, `num_floors = 4`, residential, **no height**) and `552799e9…` (OSM + USGS LiDAR, `height = 10.8`) — both of which the exclusion zone has to reach; see 2.13 |
| Google Maps satellite, Vexcel imagery 2026 | The current roofscape: a **triangular skylight** over the front block, a curved element at the court's south end, rooftop mechanical, and the open court itself |

### 2.3 Where it sits

92 South Park is the **corner** of the north-west rim of the oval and Jack London Alley,
in the run 70 · 76–82 · 84 · **86–96** · 102 · 104–106 · 108–110 · 112 · 126 · 140 · 150.
Everything to the north-east of it is 1900s stock; everything across the alley to the
south-west is the 1920s Park View block. It is the only building in that run with a
courtyard and the only one built after 1930.

Measured from the anchor, in the plane, against the two files the bake actually reads
(`pipeline/data/buildings_datasf.geojson` and `overture_buildings.geojsonseq`, after
`simplifyRing(0.6)`):

| Neighbour | Area centroid | Nearest ring vertex |
|---|---|---|
| **own front block** (DataSF `SF3775116`) | 7.18 m | **0.83 m** |
| **own rear bar** (DataSF `SF3775116`) | 9.17 m | 3.13 m |
| **own Overture twin** (`552799e9…`, h 10.8) | 7.04 m | 1.53 m |
| **own Overture twin** (`ea748f47…`, 4 floors) | **4.67 m** ← binding lower bound | 13.53 m |
| **84 South Park** (Overture `0b2c3805…`, h 11) | **10.45 m** ← binding upper bound | 13.04 m |
| **84 South Park** (DataSF `SF3775055`) | 10.90 m | 13.29 m |
| 84 South Park rear shed (DataSF `SF3775055`) | 17.82 m | 14.94 m |
| 76–82 South Park (DataSF `SF3775054`) | 17.81 m | 14.70 m |
| 76–82 South Park (Overture `9c0a0b02…`, h 13) | 17.79 m | 19.53 m |
| 102 South Park (DataSF `SF3775057`) | 22.56 m | 23.25 m |

The **north-east flank is a party wall with 84 South Park** — the two footprints touch,
which is why 84's DataSF ring centroid falls only 10.90 m from our anchor and its OSM
twin's only 10.45 m. The **south-west flank is Jack London Alley**, ~5 m of paved alley
with the Park View block opposite. The **south-east frontage is South Park Street**, with
the park lawn beginning about 11 m off the kerb, and mature street trees in front of the
building in every photograph from 1996 onward.

### 2.4 Observations from all four sides and above

**South-east — South Park Street (the hero elevation, 14.47 m wide).** Four storeys,
composed as three or four distinct cubic volumes that do not align with one another
either vertically or at the parapet. At the **south corner** (with Jack London Alley) a
projecting tower clad in weathering metal — orange copper in 1996, dark chocolate-brown
by 2025 — runs the full height and stands above every other parapet on the building; a
single **saturated red vertical column** runs up its outer corner from the shopfront head
to the parapet, with a spiral or helical element on it. To its north-east, a broad
**silver-gray metal panel** volume, then a further volume whose parapet is **raked** —
a straight diagonal rising toward the north-east, the sharpest silhouette line on the
whole rim. Windows are large, rectangular, in near-black frames, at deliberately
inconsistent heights; several carry projecting **hinged sunshade panels** hung off the
head, and two carry shallow balconies with **teal-green rails**. The ground floor is a
**near-black blue-glazed tile base** with a thin **mosaic accent stripe** at about 1.6 m,
carrying two commercial shopfronts (units 86 and 92) in dark frames with teal-green
glass, a recessed residential entry with a copper-mesh gate, and an orange-red door.

**South-west — Jack London Alley (30.06 m).** The photograph titled `JLSP_Back` shows
this elevation in full. Silver-gray **lead-coated metal panel** over the whole upper
three storeys, laid in large flat sheets whose faint diagonal creases are the material's
signature; small punched rectangular windows in black frames, sparse and irregular; at
the far (north-west) end a **copper-shingle panel**, diamond-lapped, cut to a raked
triangular profile that steps down toward the rear. The ground floor repeats the dark
blue tile base with its mosaic stripe and carries **two beige roll-up garage doors**. At
the top, a volume with corner glazing and a triangular white soffit oversails the corner.

**North-east — the party wall with 84 South Park (~16 m along the front block, then the
court arm).** Blank where the two buildings touch. The narrow arm that runs back along
this line encloses the court's north-east side and is clad, on its court face, in the
same silver panel with an **external steel stair** on it.

**North-west — the rear (14.5 m).** **Not observed by any source consulted.** It stands
on the parcel line against the backs of the Bryant Street block. Reconstructed in 2.6 as
a blunt service face in the body material.

**The court (~5 × 14 m, open to the sky).** The `JLSP_Deck2` photograph is taken in it.
Paved in a chequer of warm and gray slate; a **curved corrugated galvanized wall** at its
south end; an **external steel stair** with teal rails climbing the north-east arm; two
**curved balcony rails** off the rear bar; a Cor-Ten volume above with a raked parapet;
a dark projecting box with recessed downlights oversailing on the south-east; planting.

**Above.** Three parapets at three heights: front block ~11.15 m, rear bar ~12.32 m,
corner tower 13.28 m, plus one raked line between them. The 2010 LiDAR's height standard
deviation of 1.5 m across both polygons is not noise — it is the stepped massing, and it
is the reason a single flat box is the wrong model. Current aerial imagery adds a
**triangular skylight** over the front block, a **curved element** at the court's south
end, a small roof deck with rail, and two **polished stainless flue pipes** rising past
the court elevation.

### 2.5 Recognition cues

Five, in the order the style bible ranks them:

1. **The court.** A C-plan with a real hole in it, on a rim where every other building is
   a solid bar. From the app's downward camera this is the whole read.
2. **The rust-brown corner tower.** Highest thing on the building, on the corner, in the
   one hue nothing else on the oval uses.
3. **The red column.** One saturated vertical on an otherwise silver-and-brown building.
   It is what makes the model findable at thumbnail size.
4. **Three parapets at three heights, one of them raked.** The "ambiguated cubic forms",
   reduced to the one thing that survives at 40 px.
5. **The near-black tiled base with its teal mosaic stripe.** A hard dark plinth under a
   light body — the inverse of every stucco neighbour, and the reason the building reads
   as heavier at the ground than anything beside it.

### 2.6 Massing recipe

Three masses and a void. Lot frame: `+u` runs across the lot toward the **north-east**
(the 84 South Park party wall), `+v` runs along it toward the **north-west** (the rear,
away from South Park Street). `ROT_DEG = 44.78`, so world
`(E, N) = (u cos44.78° − v sin44.78°, u sin44.78° + v cos44.78°)`.

Parcel, CCW, in metres from the anchor in the lot frame:

```
(-7.09, -15.94)   south corner  — South Park × Jack London Alley
( 7.36, -15.95)   east corner   — South Park × 84 South Park party wall
( 7.33,  14.11)   north corner  — rear × party wall
(-7.17,  14.10)   west corner   — rear × Jack London Alley
```

The three built masses, measured from the DataSF footprints in the same frame:

| Mass | `u` range | `v` range | Deck | Crest |
|---|---|---|---|---|
| **A — front block** (full width, on South Park) | −7.1 … +7.3 | −15.9 … **0.0** | 11.15 | — |
| **A′ — corner tower** (projecting, within A) | −7.1 … −3.4 | −15.9 … −12.2 | — | **13.28** |
| **B — rear bar** (Jack London Alley side) | −7.4 … −0.5 | 0.0 … +15.7 → clip to +14.1 | 12.32 | — |
| **C — party arm** (84 South Park side) | +4.6 … +7.3 | 0.0 … +9.7 | 11.15 | — |
| **court** (void) | −0.5 … +4.6 | 0.0 … +14.1 | — | — |

Edge 0 = the south-east **South Park front** (14.45 m) · edge 1 = the north-east **party
wall** with 84 South Park (30.06 m) · edge 2 = the north-west **rear** (14.50 m) ·
edge 3 = the south-west **Jack London Alley flank** (30.04 m).

Vertical scheme:

| Element | Z (m) | Basis |
|---|---|---|
| Grade | 0.00 | |
| Tile base top / shopfront head | 3.55 | inferred from the frontage photographs, 4 storeys in 13.28 m |
| Mosaic accent stripe | 1.58 → 1.72 | observed |
| Storey 2 | 3.55 → 6.75 | inferred |
| Storey 3 | 6.75 → 9.95 | inferred |
| Storey 4 | 9.95 → 11.15 (front) / 12.32 (rear bar) | **measured** — LiDAR medians |
| Front-block parapet | 11.15 → 11.45 | measured deck + inferred coping |
| Raked parapet (front block, NE end) | 11.45 → 12.60 | observed (a straight diagonal) |
| Rear-bar parapet | 12.32 → 12.62 | measured deck + inferred coping |
| **Corner-tower crest** | **13.28** | **measured** — LiDAR `hgt_maxcm`; sets the bbox top exactly |
| Stainless flue pipes | ≤ 13.10 | observed; kept below the crest |
| Triangular skylight, roof rail, mechanical | ≤ 12.10 | observed on 2026 aerial |

### 2.7 The roof

Not one roof — four surfaces at four heights plus a hole. The front block's deck at
11.15 m carries the **triangular skylight** and the roof rail; its north-east end rises
into the **raked parapet**. The rear bar's deck at 12.32 m is plain with a hatch and a
vent. The party arm matches the front block. The corner tower is a solid capped cube at
13.28 m. Between B and C is the **open court**, whose paved floor is visible from the
app's camera and must be modelled as a real floor, not a black hole — chequered slate
paving, the curved corrugated wall at its south end, and the external stair.

### 2.8 Night state

The building holds two commercial units at street level on a corner that stays busy
after dark (Caffe Centro and The Park View are within 40 m), and four live/work units
above whose windows are large and irregular. So the night composition is layered rather
than sparse, but still restrained:

- **Hero:** the two South Park shopfronts and the recessed entry, warm gold
  (`Toy_gold_Glow`). Two lit boxes in the dark tile plinth.
- **Supporting:** four or five of the upper windows, cool (`Toy_glass_Glow`), deliberately
  *not* all of them and deliberately not aligned — the unlit ones are as much of the
  composition as the lit ones.
- **Accent:** the court, lit from below by two small warm patches at the foot of the
  external stair. This is the only landmark on the oval that can show light coming out
  of a hole in its own plan, and it is worth the two extra glow surfaces.
- Nothing on the Jack London Alley flank above the garage doors, nothing on the rear,
  nothing on the roof.

Every glow surface is a thin shell proud of the opaque glazing it sits over — never a
closed box. Day colours of the glow materials match their non-glow neighbours.

### 2.9 Palette map

| Element | Material | Hex |
|---|---|---|
| Body walls (lead-coated zinc panel), party arm, court walls, corrugated curved wall | `Toy_steel` | `9aa0a6` |
| Corner tower, rear-bar upper volume (weathered copper / Cor-Ten) | `Toy_rust` | `a86444` |
| Copper-shingle panel, Jack London Alley end | `Toy_cocoa` | `6b4a3d` |
| Ground-floor tile base, parapet copings | **`Toy_bluestone`** (new — see 2.15) | `2f3a44` |
| Window frames, sunshade panels, shopfront frames, service doors, roof rail | `Toy_ink` | `3a3530` |
| **Red corner column** | `Toy_ioorange` | `c0402a` |
| Mosaic accent stripe, balcony and stair rails | `Toy_teal` | `3fa8a0` |
| Glazing | `Toy_glass` | `2a4d73` |
| Shopfront and skylight glazing | `Toy_glassl` | `6f95b8` |
| Roll-up garage doors | `Toy_sand` | `ece4d4` |
| Roof decks, court paving | `Toy_roofd` | `45454a` |
| Flue pipes, stair stringers, mechanical | `Toy_trim` | `f3efe6` |
| Shopfront / entry night glow | `Toy_gold_Glow` | `caa64a` |
| Upper window and court night glow | `Toy_glass_Glow` | `6f95b8` |

`Toy_bluestone` is a deliberate palette extension, documented as a WARN in `REPORT.md`
exactly as 140 South Park's `Toy_olive` and 155 South Park's `Toy_peach` were. `Toy_ink`
(`3a3530`) is warm near-black and would put the plinth in the same family as the window
frames, losing the blue that is the base's whole character; `Toy_navy` (`2c4a70`) is too
close to `Toy_glass` (`2a4d73`) and the shopfronts would disappear into the wall around
them. `2f3a44` sits between the two: darker than the glazing, bluer than the ink.

### 2.10 Triangle budget

**12,000** — roughly three times the South Park average (the oval's shipped assets run
2,000–8,100), and justified by three things that none of them have: a four-sided court
that has to be modelled inside and out, three stepped masses instead of one prism, and a
facade whose openings are deliberately non-repeating so they cannot be instanced from one
bay. The elements that could run away are the mosaic stripe (build it as one thin band,
not as tiles), the copper shingle panel (one panel with three or four shadow lines, not
lapped shingles) and the external stair (a stringer pair plus a stepped ramp solid, not
individual treads).

### 2.11 Draft manifest entry

```json
{
  "id": "92-south-park",
  "file": "92-south-park.glb",
  "anchor": [-122.3941630, 37.7819166],
  "targetHeightM": 13.28,
  "cat": 2,
  "name": "92 South Park (86-96 South Park)",
  "estimated": false,
  "dims": [<measured x>, <measured y>, 13.28],
  "tris": <measured>,
  "loadRadius": 2500
}
```

`loadRadius`: the default rule is `max(2500, targetHeightM × 30)` = `max(2500, 398)` =
**2500**. Not `alwaysLoaded` — a 13.3 m building contributes nothing to the skyline and
that list must stay short (AGENTS.md, streaming and batching).

The XY `dims` will come out near **31 × 28 m**: a 30.06 × 14.47 m lot standing at 44.78°
projects to a near-square world-axis AABB, exactly as 140 South Park's 29.8 × 6.8 m bar
did.

### 2.12 Integration case

**Case B** — new landmark. `92SouthPark` does not exist in `pipeline/lib/landmarks.mjs`
or `app/src/landmarks.js`, so integration needs a registry entry, an exclusion radius,
and a tile re-bake.

### 2.13 Exclusion radius — derived, not guessed

`excluded()` in `pipeline/buildings.mjs` drops a footprint when its **area centroid**
(`ringCentroid`, area-weighted) **or any ring vertex** falls inside the circle. The bake
reads DataSF first and gap-fills from Overture, so **both sources bind**. Measured from
this anchor against the two files the bake actually reads, after `simplifyRing(0.6)`:

|  | area centroid | nearest vertex |
|---|---|---|
| own front block (DataSF `SF3775116`) | 7.18 m | **0.83 m** |
| own rear bar (DataSF `SF3775116`) | 9.17 m | 3.13 m |
| own Overture twin `552799e9…` (h 10.8) | 7.04 m | 1.53 m |
| **own Overture twin `ea748f47…`** (OSM, 4 floors, no `height`) | **4.67 m** ← binding lower bound | 13.53 m |
| **84 South Park (Overture `0b2c3805…`, h 11)** | **10.45 m** ← binding upper bound | 13.04 m |
| 84 South Park (DataSF `SF3775055`) | 10.90 m | 13.29 m |
| 84 South Park rear shed (DataSF `SF3775055`) | 17.82 m | 14.94 m |
| 76–82 South Park (DataSF `SF3775054`) | 17.81 m | 14.70 m |

Safe window **4.67 m < r < 10.45 m**. Use **`exclude: 7.5`** — 2.83 m of headroom over
the binding self-centroid and 2.95 m below the binding neighbour centroid, both far
larger than the bake's 0.6 m `SIMPLIFY_TOLERANCE`. Nothing else falls in the window.

Two things make this window unusually comfortable and both are worth understanding
before anyone tightens it:

- **The lower bound is set by an Overture polygon, not by our own DataSF footprints.**
  `ea748f47…` is OSM way 113545691 — the whole-building trace tagged *92 Jack London
  Alley, apartments, 4 levels*. It has no `height`, but `overtureHeight()` falls through
  to `num_floors × 3.2 + 1 = 13.8 m`, so the gap-fill would happily re-add a 13.8 m block
  on top of the asset. Its ring is large enough that its nearest **vertex** is 13.53 m
  away — further out than 84 South Park's — so it can only be dropped by the **centroid**
  test at 4.67 m. Sizing this radius off vertices alone gives the wrong answer here.
- **The upper bound is 84 South Park's centroid, not its vertices.** The two buildings
  share a party wall, so 84's DataSF ring reaches to within 13.29 m and its Overture twin
  to within 13.04 m — but their *centroids* sit at 10.90 m and 10.45 m, closer than their
  own nearest vertices, because the anchor lies almost on the line of the shared wall.
  84 South Park has no GLB behind it and its own `pipeline/84-south-park` branch is in
  flight; deleting it here would leave a hole in the rim that nothing fills (AGENTS rule
  3 and rule 5).

No `clearTrees`: the mature street trees in front of this building are real, they are in
every photograph of it from 1996 to 2025, and at 7.5 m the radius does not reach the kerb
line anyway.

Registry entry:

```js
{
  // 86-96 South Park: Toby Levy's 1996 six-unit live/work condominium, and the
  // only Modernist building on the oval. One 435 m2 corner parcel (block 3775,
  // lots 116-121) carrying TWO baked footprints -- the 208.7 m2 front block on
  // South Park and the 81.0 m2 rear bar down Jack London Alley -- with an open
  // court between them. The anchor is the union OBB centre of the two.
  //
  // The exclusion window is 4.67 < r < 10.45 and BOTH ends are set by centroid
  // tests rather than vertices, which is unusual; excluded() drops a footprint
  // when its centroid OR any ring vertex is inside. Measured from this anchor
  // against the two files the bake reads, after simplifyRing(0.6):
  //
  //       polygon                              centroid   vertex
  //       own front block   (DataSF)             7.18 m    0.83 m
  //       own rear bar      (DataSF)             9.17 m    3.13 m
  //       own twin 552799e9 (Overture, h 10.8)   7.04 m    1.53 m
  //       own twin ea748f47 (Overture, 4 flr)    4.67 m   13.53 m
  //       84 South Park     (Overture, h 11)    10.45 m   13.04 m
  //       84 South Park     (DataSF)            10.90 m   13.29 m
  //
  // So r must EXCEED 4.67 -- below that the Overture gap-fill re-adds OSM way
  // 113545691 (no `height`, but num_floors 4 -> 13.8 m) straight through the
  // asset, because addBuilding() returns null on exclusion so markOccupied()
  // never runs and occupiedFraction() cannot block it -- and stay UNDER 10.45,
  // or 84 South Park disappears and leaves a hole where a real building stands.
  // 7.5 sits in the middle with 2.83 m below and 2.95 m of margin above.
  //
  // No clearTrees: the street trees on the South Park frontage are real and the
  // radius does not reach the kerb.
  id: '92SouthPark',
  name: '92 South Park (86-96 South Park)',
  lon: -122.3941630,
  lat: 37.7819166,
  height: 13.28,
  exclude: 7.5,
  // Camera bearing = 180 - yaw (camera.js apply(): the offset is
  // (sin yaw, ., cos yaw) and +z is south), so yaw 45 stands the camera at
  // bearing 135 = SE, square onto the South Park front and looking straight at
  // the corner tower. Same value as 132SouthPark and 380Brannan, whose fronts
  // face the same way.
  camera: { distance: 200, yaw: 45, pitch: 26 },
}
```

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY centre offset within ~1 m
- [ ] Bounding-box top exactly **13.28 m** (loader scale lands at 1.0)
- [ ] Dimensions plausible in metres and consistent with 2.1 (XY bbox ~31 × 28 m is
      expected: a 30.1 × 14.5 m lot at 44.78° projects to a near-square AABB)
- [ ] Triangles at or under 12,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the two shopfronts, the entry, the chosen upper windows and the two
      court patches; every glow surface a thin shell proud of the opaque glazing, none of
      them a closed box
- [ ] The court is an actual void with a modelled floor — check it on the top render
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume
      for the union of solids; ray test residual ≤ 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

1. **"92 South Park" is a unit address, and a sibling branch is building the same
   building.** There is no separate structure at 92. Block 3775 lots 116–121 are six
   condominium lots on one 435 m² parcel; the building is 86–96 South Park; DataSF's EAS
   address file lists 86, 88, 90, 94 and 96 but not 92 at all, and 92 exists only because
   of the 8 Oct 2003 "address assignment - additional" permit and the Kidder Mathews
   lease listing for the ground-floor commercial condominium. **`pipeline/96-south-park`
   was opened in the same batch and resolves to this identical parcel.** Both branches
   will produce a GLB, a manifest entry and an exclusion zone for one building. Only one
   of them can be merged. This plan proceeds because the address the pipeline was given
   is a real address on a real building and modelling it is the correct answer to the
   request — but the batch integrator must drop one of the two before opening the PR, and
   the pipeline doc's Gate 0 confirmation is the step that would normally have caught it.
2. **The crest is a choice between two LiDAR maxima 0.45 m apart, and the plan takes the
   lower one.** The front block reads `hgt_max = 13.28 m` over 837 cells; the rear bar
   reads `13.73 m` over 324. They are not independent measurements of different things —
   their absolute first-return peaks are 24.11 and 24.15 m NAVD88, i.e. **the same
   physical high point**, and the 0.45 m is the difference between the two polygons'
   ground references. The plan takes **13.28** because the front block's polygon lies
   entirely inside the parcel while the rear bar's overhangs the north-west parcel line by
   ~1.6 m into the backs of the Bryant Street block, so its ground statistic is partly
   somebody else's grade. If a measured source puts the corner tower above 13.3 m, the
   target height moves and the manifest entry with it.
3. **Almost all the material evidence is thirty years old.** Seven of the eight
   photographs consulted are the architect's own 1996–97 project shots. In them the
   weathering metal is bright orange copper and the panel work is fresh silver. The one
   2025 photograph shows the copper gone dark chocolate-brown and the panels dulled. The
   plan builds the **weathered** state, because that is the building the app depicts and
   because "express their nature and age gracefully" was the design intent — but the
   *locations* of the materials come from the 1996 photographs and could have been
   changed by any re-clad since. Nothing in the permit record suggests one.
4. **The court's current contents are inferred.** The 1996 photographs establish a curved
   corrugated wall, an external steel stair, curved balcony rails and chequered slate
   paving. 2026 aerial imagery shows a triangular skylight and something pale and
   possibly temporary (a tarpaulin?) over part of the court that no other source explains.
   The plan builds the 1996 court plus the skylight and ignores the pale object.
5. **The rear elevation is unobserved.** No source consulted shows the north-west face.
   It is reconstructed as a blunt service wall in the body material on the strength of the
   type and of the fact that it stands on the parcel line against the Bryant block.
6. **The storey count in the permit record is inconsistent.** The original 1993
   application says "three story two unit"; the 1994 sprinkler permit says four; the 1994
   and 1995 revisions say three; the 2015 and 2025 permits say four. OSM says four and the
   photographs show four. The building as built is four storeys and six units, and the
   1993 application describes a scheme that changed during design — which the 1994–95
   revision run ("change to storefront", "alt kitchens in units a & b", "add one wndw on
   side & rear elevation") documents.
7. **`Toy_bluestone` is a new palette entry.** Justified in 2.9. If the reviewer would
   rather not extend the palette, `Toy_ink` is the fallback and the base loses its blue —
   record the substitution in `REPORT.md` rather than changing the plan quietly.
8. **The red column is the one thing in this model that is exaggerated.** On the real
   building it is a slender painted steel column perhaps 200 mm across with a helical
   element on it — three pixels at the app's camera. The style bible's §9 semantic
   exaggeration is what licenses building it fat enough to survive at thumbnail size.
   Recorded here so it is not later mistaken for a measurement error.
9. **No award or publication record beyond Architizer and SF Heritage was found.** The
   firm's own website (`ldparchitecture.com`) does not carry this project at all; its
   South Park entry is the unrelated One South Park warehouse conversion at 1 South Park.
   Do not confuse the two — One South Park is a 52,164 sq ft 1926 concrete warehouse
   thirty times this building's size, at the opposite end of the oval.
