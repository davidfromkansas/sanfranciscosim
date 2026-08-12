# Letterman Digital Arts Center — reference dossier

Research behind `letterman-digital-arts-center.glb`. Compiled 12 August 2026.
This dossier is the executing side's own verification of
`docs/asset-plans/letterman-digital-arts-center.md` — where the two disagree,
this file and `REPORT.md` win.

## 1. What was verified, and against what

| Item | Value used | Source | Confidence |
|---|---|---|---|
| Identity | Letterman Digital Arts Center, One Letterman Drive, Presidio — ILM + Lucasfilm divisions | Wikipedia, Wikidata Q6533683 | verified |
| Opened | July 2005 (ground broken November 2002) | Wikipedia | verified |
| Design architect / AOR | Gensler / HKS, Inc. | Wikipedia | verified |
| Landscape architect | Lawrence Halprin | Wikipedia, TCLF | verified |
| Program | 850,000 sq ft, ~$350M, ~1,500 staff | Wikipedia | verified |
| Site | 23 acres; four buildings on ~6 acres; ~17 acres public parkland | Wikipedia, TCLF | verified |
| Storeys | Four, all four buildings | Wikipedia; One Letterman leasing material | verified |
| Materials | Red brick, white stucco, terracotta roofs echoing the Presidio's historic stock | Wikipedia | verified |
| Interior ceilings | "up to 24 feet"; raised floors; LEED Gold | One Letterman leasing material | verified |
| Building A footprint | OBB 137.7 × 75.5 m, 10,400 m² | OSM way/288374441, reprojected + min-area OBB | measured |
| Building B footprint | OBB 93.7 × 121.5 m, 11,386 m² | OSM way/288374442 | measured |
| Building C footprint | OBB 86.1 × 86.4 m, 7,441 m² | OSM way/288374438 | measured |
| Building D footprint | OBB 88.4 × 88.3 m, 7,801 m² | OSM way/288374439 | measured |
| Campus grid rotation | ~24.9° off cardinal | OSM (B's OBB long axis) | measured |
| Yoda Fountain | `-122.45049, 37.79882` — Building B's SW forecourt | OSM node/665688981 | measured |
| Lagoon | `-122.44856, 37.80035`, ~839 m², boulder-lined | OSM way/32651841; TCLF | measured |
| Landscape structure | Sloping central meadow; cascading rocky stream to a boulder-lined lagoon and plaza; two stone overlook plazas; groves and hillocks buffering building mass; a meandering walk to the Presidio Promenade | TCLF | verified (descriptive) |
| **Architectural height** | **22.0 m** to the tallest rooftop element | *estimated* — see §2 | **estimated** |

## 2. The height question — the plan's biggest risk, re-checked

No published architectural height exists for any LDAC building. Neither the
Wikipedia infobox (every height field is blank), Wikidata, nor the owner and
leasing material states one.

OSM tags 15 m (A) and 18 m (B, C, D). The repo's own research note warns that
OSM `height` on this kind of building describes a low shell (City Hall 30 m,
St Mary's 18.9 m). Here the tags are more defensible than usual — they are
plausible eave heights for a four-storey building — but they cannot be the
architectural top, because these buildings carry pitched terracotta roofs with
dormers above the eave.

Derivation used, and stated as an estimate in the manifest:

- four storeys at ~4.2 m floor-to-floor (raised floors, "ceiling heights up to
  24 feet" in the double-height volumes) ≈ 16.8 m to the eave — consistent
  with the OSM 18 m tag for B/C/D
- pitched roof above the eave ≈ 3–4 m to the ridge
- rooftop mechanical ≈ 1 m above that

The model is authored so `Z_DECK` (eave band top) = 17.2 m, the hip deck =
20.0 m, ridge beams = 21.0 m and the tallest mechanical vent = **exactly
22.0 m**, which is the bbox top and therefore the `targetHeightM`. The scale
factor at load is 1.0 by construction.

`"estimated": true` ships in the manifest entry. If a published height ever
surfaces, only `Z_RIDGE`/vent heights and the manifest value need to change.

## 3. Corrections to the plan's dossier

| Plan said | Actual | Effect |
|---|---|---|
| "A is the long bar on the south, C and D pair up on the east" | A is the **north** bar (along O'Reilly Ave, lagoon due east of it); B is southwest with the entrance; C is south-centre; D is southeast | Plan file corrected; massing built from the measured layout |
| Massing recipe §2.7: brick body top to bottom with two stucco string courses | Brick **base** (plinth to the first string course) + **cream stucco** upper body, one string course — matches "red brick, white stucco" and the photographic record better than an all-brick body | One extra palette entry (`Toy_cream`); facade reads as Presidio rather than as a warehouse |
| Roof: "hipped mass z=17 to z=22" as one inset | A single inset to a hip deck **plus separate ridge beams**. A two-step inset was tried and self-intersects wherever a wing is narrower than twice the offset (the straight skeleton collapses), exporting as inverted black roof faces | Documented in the build script; ridge beams are degeneracy-proof |
| Trees "6-10" | 22 — at 5-6 m crown radius on a 312 m campus, ten crowns left the meadow reading as an empty slab | Style bible §17 (no dead zones); still grouped into groves, not scattered |
| Yoda Fountain "~3-4 m with plinth and pool" | ~7.5 m to the ear tips, 10.4 m pool diameter | Style bible §9 semantic scale — at 3 m it vanished at the app's camera distance |
| Glow: "one arcade window row per park-facing facade" | Lit-room veneers scattered across all facades and rows (~3/8 of panes, deterministic), plus B's entrance canopy fascia and door | A campus at night is occupied offices, not a lit colonnade; two glow materials, six glow objects |

## 4. Orientation

Authored in true-world orientation: Blender `+Y` = true north, `+X` = east,
matching `placeGeneric()` in `app/src/assets.js`, which scales and positions but
never rotates. The campus grid runs ~24.9° off cardinal and is baked into the
footprint coordinates rather than applied as a transform.

The contract's "front faces −Y" cannot be honoured literally: this is a campus
of four buildings facing a shared interior landscape, and Building B's ILM
entrance faces roughly **southwest** (normal ≈ 205° true) onto Letterman Drive.
Real-world orientation wins (AGENTS rule 5, and the orientation note in
`docs/asset-plans/README.md`); the deviation is recorded in `REPORT.md`.

## 5. What each side shows, and what the model does about it

**Southwest (Letterman Drive)** — B's entrance elevation. Modelled: the circular
stone forecourt, the exaggerated Yoda Fountain, a trim canopy with a glow
fascia and a glow door beneath it.

**Northwest (O'Reilly Avenue)** — A and B's rear elevations; same facade family,
no entrance event. Modelled as the plain family elevation.

**Northeast / East (park side)** — the postcard: all four buildings over the
meadow, stream and lagoon. Modelled: the full landscape base — meadow, stream
ribbon, boulder-clustered lagoon, two stone plazas, the meandering walk.

**Top** — four terracotta hipped roofs with dormer rows along the long eaves,
ridge beams, and two mechanical clusters each; the green meadow with the blue
lagoon and stream, the pale walk cutting across it. This is the surface the
app's camera spends the most time on and carries the most designed detail
(style bible §10).

## 6. Recognition cues, ranked

1. Four matching brick-and-terracotta buildings ringing a green — a campus, not
   a tower
2. The lagoon and the stream winding down the meadow
3. The Yoda Fountain at the front door
4. Terracotta hipped roofs with dormers over cream-and-brick facades — Presidio DNA
5. The pale meandering walk crossing the green

## 7. Preserved / simplified

**Preserved:** four distinct buildings on true relative footprints and true
headings; the meadow-stream-lagoon diagonal; the hipped terracotta roof family;
the brick-base / stucco-body / terracotta-roof tripartite facade.

**Simplified:** OSM footprints reduced (RDP 3.5 m, then a Visvalingam pass that
drops any vertex spanning under 40 m² — the micro-notches self-intersect under
the roof inset); hundreds of windows to three regular rows of identical panes;
roof clutter to dormer rows plus two vent clusters; the 17-acre park to the
campus's own grounds; the arboretum to 22 grouped crowns.

## 8. Uncertainties

- **The height** (§2) — estimated, not published.
- **The site slope.** The real ground falls several metres from Letterman Drive
  to the lagoon. The model's base is a flat 1 m slab; the loader seats it on one
  terrain sample at the anchor, so a 312 m-wide asset can float or sink at its
  edges. Flagged for stage-5 verification.
- **Interior courtyards.** The OSM footprints are outlines; whether B and D
  enclose true courtyards is not established from the sources used, so none are
  cut.
- **Lagoon colour.** `Toy_sky` flat colour, per the no-transparency contract.
  Whether it reads as water beside the app's own water material is a stage-5
  check.

## 9. Sources

- https://en.wikipedia.org/wiki/Letterman_Digital_Arts_Center
- https://www.wikidata.org/wiki/Q6533683
- https://www.tclf.org/landscapes/letterman-digital-arts-center
- https://www.openstreetmap.org/way/288374441 · /288374442 · /288374438 · /288374439
- https://www.openstreetmap.org/node/665688981 (Yoda Fountain)
- https://www.openstreetmap.org/way/32651841 (lagoon)
- https://www.onelettermandrive.com/
- https://www.webcor.com/projects/letterman-digital-arts-center
- https://www.lucasfilm.com/campuses/san-francisco/

No copyrighted imagery is committed. Footprint geometry is © OpenStreetMap
contributors, ODbL.
