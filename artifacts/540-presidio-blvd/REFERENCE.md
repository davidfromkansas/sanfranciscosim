# 540 Presidio Boulevard — reference dossier

Research behind `540-presidio-blvd.glb`. Compiled 12 August 2026. Everything below is
either **measured** (from open geodata, reproducibly) or **estimated** (derived or read
off a photograph). Nothing is asserted as published fact unless a source is named.

Read this with the plan (`docs/asset-plans/540-presidio-blvd.md`) and `REPORT.md`. Where
they disagree, **REPORT.md wins** — it records what was actually built.

## 1. What the building is

540 Presidio Boulevard is a two-storey Colonial Revival house built in **1912** as US
Army officers' family quarters at the Presidio of San Francisco, in the 4th Cavalry
era. It stands on a wooded rise on the west side of Presidio Boulevard, in a short row
of near-identical houses — OSM maps 540, 541, 542 and 543 with identical tags — and is
today a **duplex**: two rental units (540-A and 540-B), each about 1,620 sq ft, 4 bed /
2.5 bath, over a basement, with a detached single-car garage that is **not** part of
this asset.

It sits inside the Presidio of San Francisco National Historic Landmark District, on
Presidio Trust land inside the Golden Gate National Recreation Area.

## 2. Sources, and what each one establishes

| Source | Establishes |
|---|---|
| [OSM way/288360343](https://www.openstreetmap.org/way/288360343) — fetched from `api.openstreetmap.org/api/0.6/way/288360343/full.json` | the 13-node footprint polygon, `addr:housenumber=540`, `addr:street=Presidio Boulevard`, `building=yes`, `height=8`, `roof:shape=hipped`, `roof:colour=red` |
| Overpass query for buildings and highways within 120 m | the row (541 way/288361187, 542 way/288361188, 543 way/288361199 — all `height=8`, all `roof:shape=hipped`), the position of Presidio Boulevard east and below the row, and the footways that approach the house from the east |
| Nominatim geocode of the postal address | address → OSM feature resolution, postcode 94129, Presidio/Richmond District |
| [Presidio House, 544 Presidio Boulevard](https://pres.house/) — the neighbouring house of the same row and year | the row's architecture in the owner's own words: **"Cream stucco, a low terracotta roof, a pair of chimneys, and an arched entry"**; 1912 construction as officer's quarters, 4th Cavalry; **two floors**; **10' 6" ground-floor ceilings**; original casement windows; and a photograph of the front elevation showing the full-width columned porch, the raised base with steps, and the deep eave |
| [NPS — Presidio of San Francisco Architecture](https://www.nps.gov/articles/presidio-architecture.htm) | Colonial Revival as the Presidio's early-1900s design language |
| [FoundSF — Presidio Officers Row](https://www.foundsf.org/Presidio_Officers_Row) | the ~1912 officers' quarters row, and that it mixes single units, duplexes and quadruplexes — which is why 540 is a duplex and 544 is not |
| Public rental listings for units 540-A and 540-B | duplex, 4 bed / 2.5 bath, ~1,620 sq ft per unit, basement, detached garage |
| `artifacts/1008-general-kennedy/` in this repo | the closest built precedent — another Presidio two-storey stucco building under a red tile hipped roof with terracotta chimneys — and an independent check on the height stack (§4) |

### What could not be reached

- **The Presidio Trust / NPS historic building inventory record.** This is the most
  likely home of a measured height or an elevation drawing for this building number, and
  it was not found. Anyone who can reach it should — it would replace §4 outright.
- **Street-level imagery of 540 itself.** Google Maps, Bing Maps Bird's Eye and
  Mapillary all failed to render in the browser available to this session. The east
  front is evidenced by the photograph of 544; **north, south and west are inferred**
  from the footprint plus the type. This is stated again in §7 and in REPORT.md, and it
  is the largest soft spot in the asset.

No AI-generated image and no unsourced third-party 3D model was used at any point.

## 3. Measured geometry

All figures below were computed from the OSM polygon reprojected with the repo's local
tangent projection (`x=(lon−LON0)·111320·cos(LAT0)`, `y=(lat−LAT0)·110540`, LON0
−122.4375, LAT0 37.77), then reduced to a minimum-area oriented bounding box.

| Quantity | Value |
|---|---|
| Footprint area | **247.6 m²** |
| Oriented bounding box | **14.47 m × 19.72 m** |
| Plan yaw | **+6.49° CCW** of the cardinal grid |
| Footprint OBB centre | **−122.4519267, 37.7966669** |
| Main block (de-yawed, local) | u −5.94…+5.50 (11.44 m), v −9.86…+9.86 (19.72 m) |
| East bump-out (the porch) | u +5.50…+7.24 (1.74 m), v −4.80…+5.00 (**9.80 m**) |
| West bump-out (service bay) | u −7.24…−5.93 (1.31 m), v −1.77…+2.19 (3.96 m) |

The plan is a clean rectangle with exactly two projections, on opposite sides. The east
one is nine and a half metres long and less than two deep: that is a **porch**, not a
wing, and it is the single most useful thing the footprint tells us.

## 4. Height — the derivation, and its confidence

**No published architectural height was found.** The figure the asset ships with is a
derivation, and it is labelled `"estimated": true` in the manifest. The chain:

1. OSM tags **`height=8`** on 540 — *and identically on 541, 542 and 543*. A uniform tag
   across a repeated housing type is how eave/gutter heights usually get entered.
   `AGENTS.md` and the pipeline doc both warn that an OSM `height` on a pitched-roof
   building describes a low shell and must never be used as the target height.
2. That 8 m reconciles with the storey stack the row's own documentation gives:
   **1.10 m** raised basement to the first floor + **3.70 m** first floor (10' 6" ceiling
   plus structure) + **3.20 m** second floor = **8.00 m to the eave.** Two independent
   routes landing on the same number is why this asset treats 8 m as the eave.
3. Hip rise: the roof's eave rectangle is 12.94 m across (the 11.44 m block plus the
   0.75 m overhang each side), so the half-span to the ridge is 6.47 m. At **4.5:12** —
   inside the normal range for a low Mission/Colonial Revival tile roof, and chosen so
   the roof reads as a roof and not a plate from the app's downward camera — the rise is
   2.50 m. **Ridge = 10.50 m.**
4. The chimneys clear the ridge by **1.00 m**. **Architectural top = 11.50 m.**
5. **External check.** `1008-general-kennedy` — researched independently for this repo
   from a different evidence base (DataSF LiDAR + Overture) — landed on eave 7.8 m,
   ridge 10.9 m, chimney crest 11.9 m for the same Presidio type. Every level agrees
   with this stack to within 0.4 m.

Honest error bar: the eave is solid, the pitch is a judgement, the chimney clearance is a
convention. Worst case the top is off by roughly 0.7 m (6%).

## 5. Orientation

- **The front faces east.** Three independent signals agree: the 9.8 m porch bump-out is
  on the east face; the OSM footways serving the house approach from the east; and 544
  next door describes its living room as facing east for the morning light off the bay.
  The row sits on a rise *above* Presidio Boulevard, which runs below it to the east.
- The porch front bears **83.51° true**; the plan's long axis bears **353.51°**.
- Authored in true-world orientation (Blender +Y = north, +X = east) with the +6.49° yaw
  baked into the geometry, so the loader — which never rotates — drops it in at its real
  heading. Manifest `yawDeg` is absent.

## 6. What each side shows

| Side | Observation | Confidence |
|---|---|---|
| **East (front)** | Full-width covered porch: square columns on a solid rail, arched entry behind, steps down to the walk. Two storeys of tall casement windows above, symmetrical about the entry. Deep eave over all of it. | **evidenced** (photograph of 544; OSM bump-out) |
| **North** | Plain end wall, two storeys, a modest window pair per floor; the roof hips back from this end. | *inferred* |
| **South** | The mirror of the north end. | *inferred* |
| **West (rear)** | Service side: the small 3.96 × 1.31 m bump-out, fewer and smaller openings, the ground rising away. | *inferred* (bump-out itself is measured) |
| **Top** | The hero surface. Hipped tile roof: a short N–S ridge with four slopes falling from it, a deep overhang casting a hard shadow line, the lower porch roof stepping down on the east, two chimneys on the ridge. Terracotta red against cream. | *inferred*, but strongly constrained by `roof:shape=hipped` + `roof:colour=red` + the 544 photograph |

## 7. Recognition cues, ranked

1. **The low hipped terracotta roof with a deep overhang.** From the app's camera this is
   most of the building: red-orange against cream, with a hard eave shadow.
2. **The two chimneys** — they break the ridge and are the only vertical incident. The
   row's own material names them ("TWO CHIMNEYS").
3. **The full-width east porch** with square columns: what says *officers' quarters*
   rather than *house*.
4. **Cream stucco, calm and symmetrical**, with a regular grid of tall dark windows.
5. **The raised base and entry steps**, which read as a plinth line at any distance.

## 8. Preserved, simplified, invented

**Preserved:** the measured footprint including both bump-outs; the 2-storey height; the
hipped roof and its red tile; two chimneys; the covered porch on the east; the raised
base; the cream/red/dark-glass colour scheme; the true heading.

**Simplified:** tile courses become one flat `Toy_red` solid with terracotta ridge and hip
caps (tile texture at this size is exactly what the style bible §4 forbids); casement
mullions become plain recessed plates; the arched entry becomes a rectangular dark door
(an arch at 1.4 m wide is 3 px at city distance); the porch column count is a rhythm
decision, not a survey.

**Exaggerated, deliberately and only here:** the eave overhang, 0.75 m against a real
~0.6 m, so the shadow line survives at city distance (style bible §9). The massing and
the height are *not* exaggerated — they are the measured footprint and the derived
height, per AGENTS rule 5.

**Invented, and flagged as such:** the window positions and counts on all four
elevations (the rhythm is typical of the type, but no elevation drawing was available);
the two clipped hedges flanking the steps; the exact chimney positions along the ridge.

**Excluded on purpose:** the detached garage, the lawn and the cypress/eucalyptus stand,
Presidio Boulevard, the neighbouring houses, and any ground pad — the loader seats the
asset on baked terrain, so a pad would float or sink.

## 9. Uncertainties carried into the build

1. The height is derived, not measured (§4).
2. Three of four elevations are inferred (§2, §6).
3. The row is four near-identical houses; building one leaves a bespoke house beside
   three baked boxes. Accepted, and recorded in the plan's §2.15 as future work.
4. `cat: 1` (House) versus `cat: 2` (Apartments) is a genuine judgement call for a
   two-unit rental. House matches the built form the model shows.
