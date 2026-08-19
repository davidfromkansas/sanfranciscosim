# 140 South Park — SF-SIM asset plan

A 1907 light-industrial loft at the **west tip of the South Park oval**, and the one
building the district's own historic survey stops to single out: *"The light industrial
building at 140 South Park Street (1907) features **wood frame construction**, like the
residential buildings going up at the time, **instead of brick**."* Every other industrial
building on the oval is brick or reinforced concrete. This one is a carpenter's building
wearing a carpenter's ornament — horizontal lap siding and a **bracketed Italianate
cornice** — on the narrowest frontage in the district.

Its shape is the other half of the identity: a **6.84 m × 29.8 m stick**, 10.7 m tall,
wedged between a party wall and a side passage. From the app's downward camera it is a
long dark bar where its neighbours are broad pale blocks, and it is the only building on
the north-west rim whose frontage is narrower than one bay of the buildings either side.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/140-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `140-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3947379, 37.7814643` (DataSF footprint OBB centre, measured) |
| Target height | **10.68 m** to the cornice crest; roof deck 9.85 m — LiDAR-derived, see 2.1 and 2.15 |
| Footprint | near-rectangular, 200.8 m²; **6.84 m frontage** on South Park × 29.81 m deep, long axis on the 135°/315° line; measured |
| Triangle cap | 7,000 |
| Category | `3` (office) — assessor reclassified Industrial → Commercial Office in 2018 |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 140 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 140 South Park in San Francisco and deliver it
as a downloadable, validated GLB.

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
7. `artifacts/155-south-park/` — the closest reference implementation: same oval, same
   era, same narrow-lot geometry (8.16 × 31.22 m against this building's 6.84 × 29.81 m),
   same problem of a hero elevation only one bay wide. Its `build_155_south_park.py`
   helper set (`prism`, `ring_band`, `face_panel`, `lot_box`, `rect_opening`) is the
   intended starting point — adapt the constants, do not rewrite the helpers.
8. `docs/asset-plans/140-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Read 2.15 before you start

The massing, the footprint, the anchor and the height are measured to survey
accuracy. The **material of the front wall** and the **date of the cornice** are not,
and the roof is measured only as it stood in 2010. 2.15 says exactly which is which.
Do not promote the inferred paragraphs to fact in `REFERENCE.md`.

## Must capture

- The **stick**: a 6.84 m × 29.81 m bar, 10.68 m tall, on the real footprint at the
  real 135°/315° heading. This aspect ratio is the silhouette and the whole read from
  above — do not fatten it, do not square it to the world axes
- The **bracketed cornice** across the 6.84 m South Park front, carried as the single
  piece of ornament and enlarged so the bracket row survives at thumbnail size. It is
  the crest: the bounding-box top lands on it, not on the roof deck
- **No parapet.** A 2018 permit correction records "no existing parapet" explicitly.
  The flanks and rear get a thin fascia at the deck and nothing more
- A **dark desaturated gray-green body** (`Toy_olive`, see the palette map in 2.9)
  against white, black and brick neighbours — the value slot no other building on the
  north-west rim occupies
- **Horizontal lap siding** on the upper front, read as three or four shallow shadow
  lines, not as modelled boards
- Three tall **multi-pane upper windows** in near-black frames, the centre one wider
- A ground floor of **near-black shopfront**: display glazing, a full-width transom
  band, a **natural-wood glazed double door** (the one warm accent on the building),
  and a narrow dark service door at the north-east end
- The **blank south-west party wall** shared with 150 South Park: no openings at all
- The **north-east side passage flank**: plain, one or two high service windows, a
  downpipe. It is 29.7 m of wall that the aerial camera sees in full
- A roof designed for the downward camera without inventing what the 2010 LiDAR says
  was not there: bare deck, a low condenser pair (permitted 2019), a hatch, a vent

## Research 140 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- **Whether the front wall is horizontal wood siding, stucco, or stucco over siding.**
  This is the single largest gap. A 2005 permit repairs "loose **stucco** in front of
  building"; the Jan 2025 Street View pano reads as horizontal lap siding. Both can be
  true of different parts of the wall, or the stucco may have been stripped in the 2016
  renovation. Decide, and say which evidence you decided on
- **Whether the cornice is original 1907 or a 2016 restoration.** The 2016 permit covers
  new storefront windows and window replacement on the south elevation but says nothing
  about the cornice
- The bay count and pane grid of the three upper windows
- The rear (north-west) elevation onto the Bryant Street block, ~6 m away — no source
  consulted here shows it at all
- The roof: confirm the condenser cluster's position and count. The 2010 LiDAR predates
  it, so the survey cannot help
- Day and night appearance

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**One source conflict is already known and resolved in 2.1 — re-check it, do not
silently re-inherit the wrong value:** OSM tags `height = 10` and the DataSF LiDAR
*modal* cell is 9.89 m, so the two look like corroboration for a 10 m building. They
are not the crest. Both describe the **roof deck**. The LiDAR *maximum*, 10.68 m, is
the cornice, and it is the target height. 2.15 explains why the maximum here is safe
to use when it usually is not.

## Create a reference dossier

Write `artifacts/140-south-park/REFERENCE.md` before modelling: what the building is,
every source and what it establishes, the verified dimensions with per-row confidence,
observations from all four sides and above, the recognition cues, the massing recipe,
the palette map, and the corrections you made to this plan. `REFERENCE.md` outranks
this plan wherever they disagree.

## Build, validate, render

Deterministic scripts, no interactive Blender work:

- `build_140_south_park.py` — writes `140-south-park.blend` and `140-south-park.glb`
- `validate_140_south_park.py` — factory-resets, imports **only the exported GLB**,
  writes `validation.json`
- `render_140_south_park.py` — six review renders (four elevations, top, high
  three-quarter aerial) plus the night aerial
- `make_contact_sheet.py` — the contact sheet, night tile included

Contract gates, all of which must PASS in `validation.json`:

- GLB, real metres, +Z up in Blender / +Y up on export, applied transforms
- Origin at the footprint centre, `min Z` within 0.5 m of 0, XY centre offset ≤ 1 m
- **Bounding-box top exactly 10.68 m**, so the loader's `targetHeightM / measuredHeight`
  scale lands at 1.0
- ≤ 7,000 triangles
- All materials `Toy_*`, flat colours, no textures, no alpha, no `Toy_body`
- `_Glow` only on night-glow surfaces, authored as thin shells proud of the opaque
  glazing — never as a primary surface
- No cameras, lights, animations, armatures, constraints, no leaked foreign geometry
- Outward normals: per-object signed volume authoritative for the union of solids,
  ray test residual ≤ 0.15%

Review the high three-quarter aerial FIRST and iterate on it. Only then run the formal
render rig. Log every iteration in `REPORT.md`.

## Deliverables

`artifacts/140-south-park/` containing the two scene files, the three scripts plus the
contact-sheet script, seven renders, the contact sheet, `validation.json`,
`REFERENCE.md` and `REPORT.md`. Commit; do not integrate.
````

---

## Part 2 — Research and design dossier

### 2.1 Identity, dates and dimensions

| Item | Value | Confidence |
|---|---|---|
| Address | 140 South Park Street, San Francisco, CA 94107 | **verified** |
| APN (block / lot) | **3775-064** | **verified** — DPR 523D contributor table; CompStak; DataSF `mblr = SF3775064` |
| OSM way | **124884359** (`addr:housenumber = 140`, `addr:street = South Park`, `height = 10`) | **verified** |
| Built | **1907** | **verified** — DPR 523D contributor table and all 19 assessor rolls 2007–2025 agree |
| Construction | **wood frame** | **verified** — DPR 523D narrative, explicitly contrasted with the district's brick industrial buildings |
| Historic status | **contributor**, CHRSC `5D3`, potential South Park Historic District; type `HP8. Industrial` | **verified** — DPR 523D |
| Storeys | **2** | **verified** — assessor roll (`number_of_stories = 2.0`, every year 2007–2025); every permit 2005–2019 (`number_of_existing_stories = 2`) |
| Units | 2 | **verified** — assessor roll |
| Assessor use class | Industrial 2007–2017 → **Commercial Office** 2018–2025 | **verified** — assessor roll; the reclassification is the 2016 change-of-use permit landing |
| Building area | 4,310 sq ft over a 0.049-acre lot | **verified** — CompStak (2 × the 200 m² footprint, consistent) |
| Renovated | 2018 | **verified** — CompStak; corroborated by the 2016–2019 permit run |
| Current tenants | Flourish Ventures (lease 2025–2028); Thomvest Ventures at 138 S Park next door | **verified** |
| Footprint area | **200.8 m²** (DataSF) / 208.2 m² (OSM) | **measured** — 3.6% apart, same building |
| Footprint OBB | **29.81 × 6.84 m at 135.0°** (DataSF) / 29.66 × 7.03 m at 135.05° (OSM) | **measured** |
| Anchor (WGS84) | **`-122.3947379, 37.7814643`** | **measured** — DataSF footprint OBB centre |
| Roof deck | **9.85 m** above grade | **measured** — DataSF LiDAR modal cell `hgt_majoritycm = 989`, median 988; OSM `height = 10` agrees |
| **Cornice crest (target height)** | **10.68 m** | **measured** — DataSF LiDAR `hgt_maxcm = 1068`; see 2.15 for why the maximum is the right number here |
| Ground elevation | 7.37 m NAVD88 (`gnd_min_m`) | measured; the app's terrain handles this, not the asset |
| Street frontage | faces **135° (SE)**, onto the South Park oval | **measured** from the footprint |
| Long flanks | run 45° / 225° | **measured** |

### 2.2 Sources and what each establishes

| Source | Establishes |
|---|---|
| SF Planning / Page & Turnbull, *South Park Historic District*, DPR 523D continuation sheets, 30 June 2009 (`https://default.sfplanning.org/GIS/SouthSoMa/Docs/2009-06-30_South%20Park%20Dform.pdf`) | 1907 date; APN 3775-064; `HP8. Industrial`; contributor status `5D3`; and the identity sentence on p.5 — **wood frame construction instead of brick**, the only building in the district given that treatment. Also establishes the neighbours: 150 South Park (3775-065) is a 1959 non-contributor; 136 South Park (3775-063) was **vacant** in 2009 |
| DataSF Building Footprints, LiDAR-derived (`https://data.sfgov.org/resource/ynuv-fyni`) | the authoritative footprint polygon (200.8 m², 808 × 0.25 m² cells) and the height statistics: modal cell **9.89 m**, median 9.88 m, mean 9.57 m, **max 10.68 m**, ground 7.37 m NAVD88. Source raster `Sanfran_Orig_1381.flt`, **flown 2010** |
| SF Assessor Historical Secured Property Tax Rolls (`https://data.sfgov.org/resource/wv5m-vpq2`) | 1907; block 3775 lot 064; 2 storeys; 2 units; Industrial → Commercial Office in the 2018 roll |
| SF Building Permits (`https://data.sfgov.org/resource/i98e-djp9`) | 2005 "repair loose **stucco** in front of building & rotted wood around window"; 2016 change of use to 1st-floor retail + 2nd-floor office with **new storefront windows on the south elevation**; 2016 seismic upgrade; 2017 ground floor re-framed to slab on grade; **2018 correction "no existing parapet"**; 2019 VRF mechanical with a **relocated condensing unit** |
| OSM way/124884359 | cross-check footprint (208.2 m², within 3.6% of DataSF); `height = 10` |
| Google Street View, South Park Street pano, captured **Jan 2025** | the entire front elevation in detail (see 2.4) |
| Google Maps place imagery, 140 S Park St | the north-east side passage and the exposed flank |
| Google Maps satellite, Vexcel imagery 2026 | flat roof; a rooftop mechanical cluster toward the middle of the bar |
| CompStak property record (`https://property.compstak.com/140-South-Park-Street-San-Francisco/p/858127`) | 1907 built / 2018 renovated; 2 storeys; 4,310 SF; class B office; APN 3775-064; tenant Flourish Ventures |
| SF Registered Business Locations via opengovus | Thomvest Ventures LLC dba "140 South Park Street", registered at **138** S Park St — the reason not to read press about "138 South Park" as being about this building (see 2.15) |

### 2.3 Where it sits

140 South Park is the sixth building along the **north-west rim** of the oval counting
from Third Street, in the run 102 · 106 · 108–110 · 112 · 126 · **140** · 150 · 156 · 158
· 164 · 166–168. Every building in that run is a narrow bar running back from the oval
toward the Bryant Street block; 140's is the narrowest.

Measured from the anchor, in the plane:

| Neighbour | Nearest ring vertex | Area centroid |
|---|---|---|
| **150 South Park** (SW party wall, APN 3775-065, 1959) | **5.27 m** (DataSF) / 6.64 m (OSM) | 9.56 m |
| 136 South Park (NE, APN 3775-063, recorded vacant 2009) | 9.57 m (DataSF) | 13.58 m |
| way 124884351 (NE side passage) | 9.76 m (OSM) | 15.48 m |
| way 124884341 (NE side passage) | 10.49 m (OSM) | 16.71 m |
| 126 South Park (APN 3775-061) | 17.42 m (DataSF) | 20.56 m |
| 473 / 477 Bryant Street (rear) | 20.80 m (OSM) | 32.91 m |

The south-west long flank is a **party wall with 150 South Park** — the two OSM rings
share a node exactly (0.00 m gap). The north-east long flank is **open**: a ~6 m paved
side passage runs the full 29.7 m depth of the lot, which is why that flank is a real
elevation and not a party wall. The rear stands ~6 m off the backs of 473 and 477 Bryant.
The South Park street kerb is ~12 m off the front; the park lawn begins there.

### 2.4 Observations from all four sides and above

**South-east — South Park Street (the hero elevation, 6.84 m wide).** Two very tall
storeys under a bracketed cornice, the whole thing painted one dark desaturated
gray-green. Top down: a plain flat cap band; below it a projecting crown moulding; below
that a row of small **modillion brackets**, roughly nine across the 6.84 m — the only
ornament on the building, and read from the street as a dark dotted line under a lighter
edge. Below the cornice, a plain field of **horizontal lap siding** carrying three tall
windows in near-black frames: a wider centre light flanked by two narrower ones, each
divided into a grid of small panes three rows deep, sitting on a plain apron with no
sills of consequence. A strong horizontal **recessed panel band** separates the floors.
The ground floor is a near-black timber shopfront the full width: a **transom band** of
glazing runs across the top; below it, a wide multi-pane display window at the south-west
(150 South Park) end, then a **natural-wood glazed double door** right of centre with a
stone threshold, then a narrow dark service door at the north-east end. A red fire
department connection and an alarm bell sit on the south-west pier; two gooseneck lamps
sit under the cornice of the neighbour, not this building.

**South-west — the party wall with 150 South Park (29.81 m).** Blank. 150's own facade
runs hard against it with no gap; nothing on this flank is visible from anywhere.

**North-east — the side passage (29.72 m).** The full depth of the wall stands open onto
a paved passage about 6 m wide, with a corrugated white wall opposite. Plain body colour,
no storefront, no articulation beyond a downpipe and (from the Jan 2025 imagery, at an
oblique) a small high window or two. This is 29.7 m of otherwise featureless wall that
the app's downward camera sees end to end, so it needs the shadow line of the siding and
nothing else.

**North-west — the rear (6.65 m).** **Not observed by any source consulted.** It stands
~6 m off the rear of 473/477 Bryant. Reconstructed in 2.6 as a blunt service face.

**Above.** A flat roof, no parapet ring (permit, 2018). The 2010 LiDAR is nearly uniform
across the whole 200 m² — modal 9.89 m, median 9.88 m, standard deviation 1.11 m almost
all of which is edge effect — so in 2010 the roof carried **nothing at all**, and the
10.68 m maximum is the cornice at the street edge. The 2026 satellite shows a mechanical
cluster toward the middle of the bar, which the **2019 permit accounts for**: a variable
refrigerant flow system serving the first-floor build-out, with a condensing unit
relocated on revision. Anything else on that roof would be invention.

### 2.5 Recognition cues

Five, in the order the style bible ranks them:

1. **The stick.** 6.84 × 29.81 m, 4.4 : 1. From above it is a long thin bar in a row of
   broad ones. Nothing else on the oval is this slender.
2. **The dark gray-green body.** 150 next door is white over black, 155 is white, 135 is
   dark brick, 126 and 112 are pale. A mid-dark desaturated green-gray is a value and hue
   slot no neighbour holds, and it is what the building actually is.
3. **The bracketed cornice.** The one piece of ornament, on the one elevation that has
   any. It is also the crest, so it defines the silhouette.
4. **Three tall black-framed windows over a black shopfront.** A 2:1 value stack —
   dark base, dark openings, dark cap — on a mid-dark wall.
5. **The wood double door.** The single warm, saturated thing on the building, dead
   centre of the frontage. It is the only accent the palette gets.

### 2.6 Massing recipe

One mass. No secondary volume, no step, no wing — the survey shows a single
near-rectangular prism and inventing an articulation would be a lie about the type.

Lot frame: `+u` runs across the lot to the **north-east** (toward the side passage),
`+v` runs along it to the **north-west** (toward the rear, away from South Park Street).
`ROT_DEG = 45`, so world `(E, N) = (u cos45° − v sin45°, u sin45° + v cos45°)`.

Footprint, CCW, in metres from the anchor:

```
(-3.325,  14.900)   rear, south-west corner
(-3.419, -14.905)   front, south-west corner
( 3.422, -14.904)   front, north-east corner
( 3.327,  14.812)   rear, north-east corner
```

Edge 0 = the south-west **party wall** (29.81 m) · edge 1 = the south-east **South Park
front** (6.84 m) · edge 2 = the north-east **side passage flank** (29.72 m) · edge 3 =
the north-west **rear** (6.65 m).

Vertical scheme:

| Element | Z (m) | Basis |
|---|---|---|
| Grade | 0.00 | |
| Shopfront head / transom top | 4.35 | inferred from the frontage photograph |
| Panelled belt band | 4.35 → 5.20 | observed |
| Upper window group | 5.60 → 8.55 | observed proportions |
| Cornice frieze | 8.90 → 9.25 | observed |
| Bracket row | 9.25 → 9.72 | observed; **enlarged**, see 2.15 |
| Crown moulding | 9.72 → 10.14 | observed |
| **Cornice cap crest** | **10.68** | **measured** — LiDAR `hgt_maxcm`; sets the bbox top exactly |
| Roof deck | 9.85 | **measured** — LiDAR modal cell |
| Deck fascia (flanks + rear only) | 9.85 → 10.00 | permit: no parapet |
| Condenser pair, hatch, vent | ≤ 10.57 | permitted 2019; kept below the crest |

### 2.7 The roof

Bare dark deck, a thin fascia on three sides, the cornice on the fourth. On the deck,
three clusters and nothing more: a **pair of low condensers** on steel frames toward the
middle of the bar (the 2019 VRF units), a **roof hatch** near the rear third, and a
single **vent stack**. All under 0.72 m so the cornice keeps the crest. The lap-siding
shadow lines run over the two long flanks, which is what stops 29.7 m of blank wall from
reading as a slab from above.

### 2.8 Night state

The west tip of the oval is the dark end of South Park — the park's own lighting stops
short of it and 150 next door has been marketed for lease since at least Jan 2025. So the
night composition is deliberately sparse:

- **Hero:** the ground-floor shopfront and its transom band, warm gold (`Toy_gold_Glow`).
  One lit thing at the dark end of the street.
- **Supporting:** the three upper windows, cool (`Toy_glass_Glow`), at lower area.
- Nothing on the flanks, the rear, or the roof.

Every glow surface is a thin shell proud of the opaque glazing it sits over. Day colours
of the glow materials match their non-glow neighbours so the ~12% day alpha reads as
part of the wall.

### 2.9 Palette map

| Element | Material | Hex |
|---|---|---|
| Body walls, cornice frieze and crown | **`Toy_olive`** (new — see 2.15) | `5f655c` |
| Shopfront frame, window frames, bracket row, service door | `Toy_ink` | `3a3530` |
| Wood entrance doors | `Toy_oak` | `c08e50` |
| Glazing | `Toy_glass` | `2a4d73` |
| Transom band | `Toy_glassl` | `6f95b8` |
| Roof deck, hatch | `Toy_roofd` | `45454a` |
| Condensers, vent, downpipe | `Toy_steel` | `9aa0a6` |
| Fire department connection | `Toy_red` | `c4453c` |
| Shopfront night glow | `Toy_gold_Glow` | `caa64a` |
| Upper window night glow | `Toy_glass_Glow` | `6f95b8` |

`Toy_olive` is a deliberate palette extension, documented as a WARN in `REPORT.md`
exactly as 155 South Park's `Toy_peach` and 380 Brannan's `Toy_slate` were. `Toy_slate`
(`6f7883`) is a blue-gray and too light; `Toy_pine` (`3f6b4f`) is a saturated green and
far too strong for a whole wall. Neither is this building.

### 2.10 Triangle budget

**7,000**, matching 155 South Park (which shipped at 4,048). One mass, one ornamented
elevation, one detailed roof. The bracket row is the only element that could run away —
build it as a single panel of nine small boxes, not nine framed openings.

### 2.11 Draft manifest entry

```json
{
  "id": "140-south-park",
  "file": "140-south-park.glb",
  "anchor": [-122.3947379, 37.7814643],
  "targetHeightM": 10.68,
  "cat": 3,
  "name": "140 South Park",
  "estimated": false,
  "dims": [<measured x>, <measured y>, 10.68],
  "tris": <measured>,
  "loadRadius": 2500
}
```

`loadRadius`: the default rule is `max(2500, targetHeightM × 30)` = `max(2500, 320)` =
**2500**. Not `alwaysLoaded` — a 10.7 m building contributes nothing to the skyline and
that list must stay short (AGENTS.md, streaming and batching).

### 2.12 Integration case

**Case B** — new landmark. `140SouthPark` does not exist in `pipeline/lib/landmarks.mjs`
or `app/src/landmarks.js`, so integration needs a registry entry, an exclusion radius,
and a tile re-bake.

### 2.13 Exclusion radius — derived, not guessed

`excluded()` in `pipeline/buildings.mjs` drops a footprint when its **area centroid**
(`ringCentroid`, area-weighted) **or any ring vertex** falls inside the circle. The bake
reads DataSF first and gap-fills from Overture, which carries OSM geometry, so **both
sources bind**. Measured from this anchor:

|  | nearest vertex | area centroid |
|---|---|---|
| own footprint (DataSF `SF3775064`) | 9.54 m | **0.09 m** |
| own footprint (OSM way/124884359) | 6.64 m | **1.38 m** ← binding lower bound |
| **150 South Park (DataSF `SF3775065`)** | **5.27 m** ← binding upper bound | 9.56 m |
| 150 South Park (OSM way/124884352) | 6.64 m | 9.27 m |
| 136 South Park (DataSF `SF3775063`) | 9.57 m | 13.58 m |

Safe window **1.38 m < r < 5.27 m**. Use **`exclude: 3`** — 1.62 m of headroom over the
binding self-centroid and 2.27 m below the binding neighbour vertex, both comfortably
larger than the bake's 0.6 m `SIMPLIFY_TOLERANCE`.

Do not raise it. 150 South Park is an existing 8 m building on the oval with no GLB
behind it; at r > 5.3 its party-wall vertex falls inside the circle and the bake punches
a hole in the row that nothing fills.

**Note on the anchor choice.** The DataSF OBB centre was chosen over the OSM centroid
specifically because it widens this window: from the OSM centroid the safe band is only
1.46–3.99 m. The two anchors are 1.38 m apart.

Registry entry:

```js
{
  id: '140SouthPark',
  name: '140 South Park',
  lon: -122.3947379,
  lat: 37.7814643,
  height: 10.68,
  exclude: 3,
  // camera.js puts the eye at target + distance*(sin yaw, ., cos yaw) with +x
  // east and +z south, so yaw 45 stands south-east of the building — square onto
  // the South Park front, the only elevation with any ornament on it.
  camera: { distance: 150, yaw: 45, pitch: 26 },
}
```

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY centre offset within ~1 m
- [ ] Bounding-box top exactly **10.68 m** (loader scale lands at 1.0)
- [ ] Dimensions plausible in metres and consistent with 2.1 (XY bbox ~26 × 26 m is
      expected: a 29.8 × 6.8 m bar at 45° projects to a near-square AABB)
- [ ] Triangles at or under 7,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the shopfront, transom and three upper windows; glow shells proud
      of the opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume
      for the union of solids; ray test residual ≤ 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The LiDAR maximum is the target height here, and that is unusual.** The plans README
  warns against the LiDAR maximum because on most buildings it is a stair penthouse, a
  lift overrun or a tree overhanging the polygon. On this building it cannot be: the
  spread between the modal cell (9.89 m) and the maximum (10.68 m) is **0.79 m**, far too
  small for any of those, and exactly the height a false-front cornice projects above a
  roof deck on a two-storey 1907 commercial front. The 2018 permit's "no existing
  parapet" rules out the other candidate. **10.68 m is the cornice.** If a later source
  shows a stair bulkhead, the target height moves and the manifest entry with it.
- **The 2010 LiDAR predates the rooftop mechanical, which is why the roof is trustworthy
  and the mechanical is not.** The DataSF raster is `Sanfran_Orig_1381.flt`, flown 2010;
  the condensing unit is permitted in 2019. So the survey proves the roof was **bare** in
  2010 — a genuinely useful negative — but says nothing about where the condensers went.
  Their position is read off 2026 satellite imagery and is *inferred*.
- **Stucco or siding? Unresolved.** The 2005 permit repairs "loose stucco in front of
  building"; the Jan 2025 photograph reads as horizontal lap siding under paint. The plan
  builds **siding**, because the 2016 renovation was extensive enough to have stripped a
  stucco skin and because the DPR's emphasis on wood-frame construction makes siding the
  typologically expected finish — but this is a decision, not a fact, and it is the most
  likely thing in this dossier to be wrong.
- **The cornice may not be original.** Nothing dates it. The 2016 permit covers storefront
  and window work on the south elevation and is silent on the cornice. It is on the
  building now, which is what the asset models; the plan does not claim 1907 for it.
- **Do not confuse this building with 138 South Park.** Thomvest Ventures is registered
  at 138 and its "140 South Park Street" DBA is a trading name, not an address. The
  Perkins&Will "South Park Venture Capital Firm" project — 16,420 sq ft, brick-clad,
  "originally built in the 1920s" — is **not** this building: 140 is 4,310 sq ft, wood
  frame, and 1907. Every one of those three facts contradicts it. Press about a South
  Park VC office is about the neighbour.
- **The rear elevation is unobserved.** No source consulted shows the north-west face. It
  is reconstructed as a blunt service wall on the strength of the type. Anyone who can
  reach the Bryant Street block should verify it before the roof design is frozen, since
  the rear third of the roof is where the hatch goes.
- **The bracket row is deliberately enlarged.** The cornice assembly reads about 1.2 m on
  the photograph; the model builds it at 1.78 m (8.90 → 10.68). That is semantic
  exaggeration under style bible §9 — at the app's camera a 1.2 m cornice on a 6.84 m
  frontage is three pixels and the building loses its only ornament. Recorded here so it
  is not later mistaken for a measurement error.
- **The frontage is only 6.84 m and three windows have to fit in it.** At 0.60 m piers
  and 0.30 m gaps the lights come out 1.55 / 1.95 / 1.55 m. There is no room to widen
  anything; if the model needs more window it has to come out of the piers.
- **No architect or builder is recorded** for the 1907 building in the DPR form or in any
  other source consulted.
