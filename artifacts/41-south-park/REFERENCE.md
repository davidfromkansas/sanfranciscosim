# 41–43 South Park — reference dossier

The verified record behind `41-south-park.glb`. Everything here was re-checked
against primary sources during the build; where it disagrees with
`docs/asset-plans/41-south-park.md`, **this file and `REPORT.md` win**.

## 1. What the building is

A **1911 Edwardian two-flat** on the north-east rim of the South Park oval in
SoMa, 7.297 m of frontage against 24 m of depth. It was gutted and rebuilt
behind its retained facade in 2012–13 as a single residence — double-height
dining room, ground-floor media room, two-car garage, rollaway skylights and a
roof terrace with a custom spa — listed at $7.65 M in April 2013 and sold for
$5.70 M on 22 September 2014.

| | |
|---|---|
| Address | 41 and 43 South Park, San Francisco CA 94107 |
| Parcel | block 3775, lot 040 (`3775040`), zoning `SPD` |
| OSM | way `112759867`, `addr:housenumber=41;43` |
| Year built | 1911 |
| Units | 2 (a two-flat, since combined) |
| Construction | wood frame (assessor type `D`) |
| Neighbours | 35 South Park (lot 102, north-east) and 45–47–49 South Park (lot 039, south-west), both party-wall |

## 2. Sources, and what each establishes

| Source | Establishes |
|---|---|
| DataSF **Parcels** `acdm-wktn`, `blklot=3775040` | the surveyed lot: **7.297 × 32.287 m parallelogram, 235.6 m²**, the 41→43 address range, SPD zoning. The geometric backbone. |
| DataSF **Addresses** `ramy-di5m` | 41 and 43 both resolve to lot 040 — the confirmation they are one property; 35 → lot 102, 45/47/49 → lot 039 |
| DataSF **Building Footprints** `ynuv-fyni`, `201006.0038546` (2010 LiDAR, refreshed 2023-09-11) | ground **11.76 m** NAVD88 median (67 cm range); **roof deck 9.83 m** above grade (median over 672 cells at 50 cm, σ 1.08 m); maximum 11.88 m; built extent −1.92 → **+24.55 m** along the lot axis |
| DataSF **Assessor roll** `wv5m-vpq2`, row `20253775040` | **1911** build year, 2 units, 3,600 sq ft, wood frame, `SRES` use, sale 2014-09-22, Home Owners exemption, lot 2,578 sq ft |
| **Compass MLS #423723952** (© SFARMLS), street-elevation photograph from the park lawn | **the primary photographic source.** Every facade dimension in §4 is measured from it. *Observed (listing photo).* |
| socketsite.com (Apr 2013, Oct 2014) | the two-unit status, the rebuild, the rooftop terrace and spa, the price history |
| onekindesign.com (Apr 2013) | "the Edwardian appeal of the building's **original 1911 facade**", 3,600 sq ft, two-car garage/workspace, **rollaway skylights**, rooftop terrace with custom spa |
| skyboxrealty.com | "historically maintained Edwardian facade", **three floors** of living space, roof terrace with SF views and a custom spa |
| leveragere.com / Vanguard Properties | "from the historically maintained Edwardian façade to the modern amenities" |
| **Google satellite, z21 nadir (~0.059 m/px), 2026** | *observed*: flat pale membrane roof; a dark rectangular deck with a pale circular object inside it (read as the terrace and spa); round roof penetrations; the shaded rear yard |
| Esri World Imagery, z20 nadir | *observed*, cross-check on the roof and on the continuity of the rim |
| en.wikipedia.org/wiki/South_Park,_San_Francisco | the oval's 1852 origin, the curved line of buildings, the 3–4 storey rim |

**Two sources were rejected during research and must stay rejected:**

- `archpaper.com/2025/04/saw-old-new-san-francisco-1910-quarter-round-house/` —
  an Exa summariser attached this address to it. The page text places the
  project in **Ashbury Heights**. Not this building.
- `jerryklerarchitects.com/index.php/south-park-facade/` — a South Park facade
  restoration (18 windows, new envelope, "an upgraded color scheme") that fits
  this building's present appearance well but **never states an address**.
  Plausible, uncited, kept out of the facts table.

## 3. Location and orientation

| | |
|---|---|
| Design footprint | **7.297 × 24.0 m = 175.1 m²** — the surveyed parcel truncated at the LiDAR rear extent, leaving an 8.3 m rear yard |
| Design anchor (footprint centroid) | `-122.3934770, 37.7815017` |
| **Manifest anchor** (model bbox centre) | **`-122.3934793, 37.7815036`** — the build recentres the model on its XY bbox centre, 0.29 m from the footprint centroid (the stoop and bays hang off the front) |
| Street facade faces | **315.22°** — north-west, square onto the park |
| Lot axis | **135.22°** into the block, constant |
| AABB | 22.46 × 22.48 × 10.60 m — the consequence of a 135° heading, **not** a scale error |
| Ground | flat to 0.67 m under the footprint, so `placeGeneric`'s single terrain sample is correct here |

**Three geometries exist and they do not agree.** Resolved as:

| Source | What it is | Verdict |
|---|---|---|
| DataSF parcel `3775040` | surveyed lot, 235.6 m² | **authoritative for shape and position** |
| DataSF LiDAR `201006.0038546` | 2010 raster footprint, 164.8 m², 28 ragged vertices, offset ~1.9 m streetward | **authoritative for built depth only** |
| OSM `way/112759867` | 5-vertex trace, 177.5 m², offset ~2.9 m streetward | **rejected for placement**; kept only as the Overture stand-in for exclusion sizing |

The streetward overshoot is **partly real**: SF bay windows project over the
property line. The model puts the main wall plane on the property line and the
bays 0.95 m in front of it, which reproduces most of the overshoot; the residual
~1 m is raster registration error and is discarded. Applying the same correction
to the rear extent moves 24.55 m to ~23.6 m, which is why the built depth is
24.0 m — a figure that also reproduces the assessor's 3,600 sq ft over two
counted storeys to within 7%.

**Authoring frame.** `t` runs along the frontage from the **south-west** party
wall (t = 0, the 45–49 side, the garage) to the **north-east** one (t = 7.297,
the 35 side, the stoop and the oxblood bay); `d` runs outward toward the park;
`u = −d` runs into the lot.

## 4. What each side shows

### North-west — the street elevation, and the only public face

Measured from the Compass photograph by scaling its 288-pixel facade width to
the surveyed 7.297 m frontage (39.45 px/m). The cross-check is the garage door,
which comes out **3.30 × 2.00 m** — a standard San Francisco garage opening, so
the scale is right to within about 5%. The photograph's verticals are parallel
to within a pixel or two, which is the evidence that the camera was level.

| Element | Measured |
|---|---|
| Cornice crest | z **10.60 m** |
| Dentil band top | z 9.71 m |
| Bay cornices | z 9.08 m |
| Storey line, 2nd→3rd | z ≈ 5.60 m |
| South-west bay springs | z ≈ 2.48 m (modelled 2.30) |
| Garage lintel | z 2.05 m |
| North-east bay | t 4.15 → 7.10 (2.95 m), **top storey only**, oxblood |
| South-west bay | t 0.20 → 3.15 (2.95 m), **two storeys**, charcoal |
| Arched entry recess | t 4.20 → 6.80 (2.60 m), springing 3.85 m, crown 5.15 m |
| Garage door | t 0.25 → 3.35 (3.10 m), head 2.05 m |

Everything is painted one **charcoal slate grey** except the north-east
top-storey bay, which is **deep oxblood**. The window sashes and the horizontal
mouldings under each bay read a full value lighter — pale grey — and that
contrast is the only thing that makes the ornament legible in a near-black
facade. Two burgundy phormium clumps flank the stoop; a young street tree stands
in front of the north-east half. Neither is in the GLB.

### North-east and south-west — the party flanks

Blind. The north-east flank abuts 35 South Park, the south-west abuts 45–49.
Neither is visible from the app's camera at any useful angle. Built as flat
charcoal planes with no openings; the only articulation is the seam at the
storey line where the two body solids meet.

### South-east — the rear

Faces a private walled patio and yard. The 2012–13 rebuild put a "soaring glass
wall" here opening onto that yard; **no photograph of this elevation was
located**, so its size, position and storey are *inferred*. Modelled as one
4.2 × 3.3 m recessed glazed panel plus a door. Visible only from directly above,
so the cost of being wrong is low.

### Top — the real facade

A flat **pale membrane** roof at 9.83 m behind a 0.27 m parapet, with the
cornice lifting to 10.60 m at the street end only. Incidents, in order along the
lot: a rollaway skylight at u ≈ 5 m; the **timber terrace with its round spa** in
the front half; a low roof hatch; a second skylight at u ≈ 19 m. The value
contrast between the pale roof and the charcoal walls is the single most useful
thing about this asset from the app's camera.

## 5. Recognition cues (ranked)

1. **The asymmetric pair of bays** — one two-storey, one single-storey — over a
   recessed arched entry. No other house on this rim has that composition.
2. **The oxblood bay against a charcoal building**, on an oval of cream, sage and
   pale grey. The only saturated colour for fifty metres.
3. **The value of the thing.** It is the darkest building on the rim; at
   thumbnail size it reads as a dark notch in a pale row before any detail
   resolves.
4. **The heavy bracketed cornice with its pale dentil band**, returning over both
   bays — which is also what draws the street end in the top view.
5. **The pale flat roof with its timber terrace and round spa.**
6. **The proportion** — 7.3 m of frontage against 24 m of depth.

## 6. Preserved exactly

- The 7.297 m frontage, the 24.0 m depth, the 135.22° axis, the 315.22° facade
  heading and the parallelogram plan
- The bay asymmetry, and **which side each bay is on**
- The 0.95 m bay projection over the property line
- The arched entry as a genuine 0.80 m notch in the plan, with the stoop rising
  into it
- The flat roof as a genuinely flat plane, with the parapet lifting to the
  cornice at the street end only
- The single-colour discipline of the real building: charcoal everywhere, one
  accent

## 7. Simplified or exaggerated (each with its reason)

| Move | Reason |
|---|---|
| Canted bays get **five facets**, not a curve | style bible §4 — chunky beveled massing |
| Windows become a three-layer relief stack (pale surround → ink reveal → glass), no muntins or sash divisions | muntins are sub-pixel at 300–500 m and cost ~1,500 triangles |
| The cornice is a **1.50 m** three-step band projecting 0.45 m, heavier than the real one | style bible §9 — it is the Edwardian signature, and an accurately scaled cornice is one dark pixel at camera distance |
| The dentils are a continuous **pale band**, not modelled blocks | at 300–500 m a pale line under a dark crown *is* the dentil read; 24 blocks would cost ~1,200 triangles for nothing |
| The oxblood covers the whole north-east top-storey bay including its cornice return | slightly more than the photograph shows, so the accent survives at thumbnail size |
| The arch head is a 10-segment semicircle in a single extruded spandrel plate | one object, no boolean, and it reads as an arch from every angle |
| The stoop is five solid risers with no handrail | a handrail is sub-pixel and costs ~400 triangles |
| Skylights at 2.0 × 1.4 m | the sources say "huge rollaway skylights"; the first build's 1.2 × 0.9 curbs read as two blue chips on an empty 24 m slab |
| Dropped entirely | brackets, panel mouldings, downpipes, meters, house numbers, the phormium, the street tree, the rear yard |

## 8. Materials

| Material | Hex | Used for |
|---|---|---|
| `Toy_roofd` | `45454a` | the whole charcoal body — walls, SW bay, cornice, parapet, arch spandrel, roof hatch |
| `Toy_red` | `6e3947` | **the oxblood bay, and nothing else** — OFF-PALETTE, see below |
| `Toy_steel` | `9aa0a6` | sashes, trim, bay aprons, the dentil course, the spa shell |
| `Toy_glass` | `2a4d73` | all windows and the rear glazed wall |
| `Toy_ink` | `3a3530` | garage leaf, entry recess lining, stoop, skylight curbs, rear door |
| `Toy_stone` | `d9d2c2` | the flat pale roof membrane |
| `Toy_rust` | `a86444` | the roof terrace decking and its guard |
| `Toy_glassl` | `6f95b8` | the spa water, skylight glazing |
| `Toy_glass_Glow` | `6f95b8` | the four lit top-storey bay windows — **hero** |
| `Toy_glassl_Glow` | `6f95b8` | the lit spa |
| `Toy_gold_Glow` | `caa64a` | the warm spill in the entry recess |

**`Toy_red` carries an off-palette hex.** The real colour is a deep oxblood
around `#6e3947` and no palette entry is close — `Toy_rust` (`a86444`) is far too
orange, the palette's own `Toy_red` (`c4453c`) far too bright. The style bible's
San Francisco exception (painted residential rows keep their tinted facades)
sanctions the deviation, and this accent *is* recognition cue #2. Off-palette
colours are a **WARN, not a FAIL** (`sf-asset-check` §7). The material keeps a
palette *name* so the contract check and the loader's merge path are unaffected —
the same device `165-south-park` used for its siding.

**Night state.** Hero: the four top-storey bay windows lit — two on the oxblood
bay, two on the charcoal one. Supporting accents: the spa glowing pale blue on
the roof terrace, and a warm spill in the arched entry recess that tells the eye
at night the arch is a hole. The garage, the middle storey and the roof membrane
stay dark. Every glow surface is a **single thin panel proud of an opaque
parent** — a closed glow shell is two alpha layers and reads ~23% by day instead
of ~12%, tinting the facade it sits on.

## 9. Uncertainties

1. **The 10.60 m crest is photogrammetric, not published.** The 9.83 m roof deck
   is a real LiDAR measurement; the 0.77 m of cornice above it is measured off
   one photograph. The error is contained: the build normalizes the crest to
   exactly 10.60 and the loader scales by `targetHeightM / measuredHeight`, so
   the scale lands on 1.0 and the plan dimensions stay exact whatever the truth
   is. `"estimated": true` in the manifest.
2. **The LiDAR maximum of 11.88 m is unexplained**, and 1.28 m above the modelled
   crest. The survey is from 2010 and the building was gutted in 2012–13, so
   whatever produced that return may no longer exist; today's nadir imagery shows
   no tall roof structure. The modelled roof hatch is the only candidate on the
   present roof and is nowhere near that height. Unresolved.
3. **The facade reading rests on one photograph** — a 2013 marketing image partly
   obscured by a street tree. The bay asymmetry in it is unambiguous and that is
   the important part; the exact bay widths are not.
4. **The rear elevation was never seen.**
5. **The terrace's position is inferred to ±3 m.** The nadir imagery reads it
   12–16 m back; the listings say it overlooks South Park. The model puts it at
   9.6–13.4 m, which satisfies both within the imagery's registration error on
   this block.
6. **The roof hatch is inferred from function, not from a source** — a roof
   terrace has to be reachable.
7. **The present facade is 2012–13 work over 1911 fabric.** The massing, bays,
   arch and cornice are original; the charcoal-and-oxblood scheme, the garage
   door and the sashes are not. The model depicts the building as it stands.
