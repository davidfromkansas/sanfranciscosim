# The Towers at Rincon (88 Howard Street) — build report

`towers-at-rincon.glb`, built by `build_towers_at_rincon.py`, validated by
`validate_towers_at_rincon.py` against a fresh re-import of the exported file.
Research and sources are in `REFERENCE.md`; this file records what was decided,
what the plan got wrong, and what the numbers came out to.

## Shipping numbers

| | |
|---|---|
| Triangles | **17,034** (cap 18,000) |
| Objects | 252 |
| Dimensions | **108.66 × 108.67 × 89.00 m** |
| min Z | 0.0000 |
| XY centre offset | 0.0000, 0.0000 |
| Materials | 10, all `Toy_*`, flat, no textures, no alpha |
| Glow materials | `Toy_glassl_Glow`, `Toy_gold_Glow` |
| Open glow-strip faces | 188, all 188 facing outward |
| Signed-volume inverted objects | 0 |
| Normals ray test | 27,367 first hits, 11 flipped = **0.040 %** (tolerance 0.15 %) |
| Validation | **PASS** (`validation.json`) |
| Manifest anchor | `-122.3924907, 37.7919910` |
| `targetHeightM` | **89.00** — so the loader's scale is exactly 1.000 |

The XY box is 108.7 m because this is a **whole diamond city block at 45° to the
world axes**, whose own sides are 73–89 m. It is not a 109 m building.

## 1. Dossier correction — the courtyard is at grade, not on the roof

`docs/asset-plans/towers-at-rincon.md` §2.4 and §2.9 placed the circular plaza,
the curved planters and the pergolas on the **podium roof** in the north-west
quadrant, reading the owner's "7th-floor outdoor resident lounge" as the whole
story. It is wrong.

The DataSF footprint says so by itself: ring `201006.0000265` is a **C**, with a
~45 m wedge cut out of the north-west side. Whatever is in that wedge returned
*ground*, not a roof at 24.5 m. Google satellite at z21 confirms an open-air
paved court — circular plaza, radial paving, curved stepped planting terraces
with a stair, café seating, and a glazed canopy over the narrow south-east end —
which is the "ground floor promenade … and a central garden courtyard" the
*Los Angeles Times* described on 16 October 1988.

The model builds the courtyard at grade, and the podium is a C. **REPORT beats
plan.** The plan file has been corrected to match.

This mattered for more than the courtyard: the podium's plan is what makes the
building read from above, and a solid diamond would have been the wrong shape.

## 2. Heights are measured, and the crown is split between two sources

`targetHeightM = 89.00 m` (CTBUH architectural *and* to tip, both towers). The
DataSF LiDAR crest is 87.13 m above ground (87.27 m from the peak elevation), and
LiDAR does not return a thin mast — so the **arch apex is modelled at 87.20 m and
the mast tip at exactly 89.00 m**. Two independent sources, each describing the
part of the building it can actually see, and they agree.

The podium height was not assumed either. The LiDAR record is strongly bimodal
(mean 38.29, median 24.95, mode 24.21, σ 25.93, max 87.13); solving
`f·H+(1−f)·L = mean` and `f(1−f)(H−L)² = σ²` at `H = 87.0` gives **L = 24.49 m**
and `f = 0.221`. The podium roof is built at 24.50 m.

OSM's `height=93` was **rejected**: 5.9 m above the LiDAR crest, 4 m above CTBUH,
and OSM is not a height authority here.

Storey structure that reproduces those numbers: ground storey 5.00 m + five
office storeys at 3.90 m = 24.50 m; sixteen residential floors at 3.20 m to the
shoulder cornice at 75.70 m; 2.5 more in the central bay to 83.70 m; penthouse to
85.00 m; arch to 87.20 m; mast to 89.00 m. CTBUH says 22 storeys and Wikipedia
says 23 — the height is measured, so that is a labelling disagreement, not a
geometry one.

## 3. Three iterations that changed the model

**a. `Toy_roofd` on a roof deck reads black.** The first aerial and top renders
showed both tower roofs and the podium roof as holes punched in the model. The
decks are now `Toy_steel` and `Toy_roofd` is kept for mechanical masses only. The
palette comment in the build script records why, so the next pass does not undo it.

**b. Parapets built as solid prisms fill the roof.** `podium_parapet_i` and the
tower parapets were extruded inset polygons, which is a slab covering the whole
roof, not a rim — the podium roof became one blank cream field 25.4 m up with the
designed roofscape buried underneath it. Replaced with a `rim()` helper that
builds the actual band between a polygon and its inset. All five rims initially
failed the signed-volume test because the band was hand-wound; they are now let
through `recalc_face_normals`, which orients a closed manifold correctly.

**c. A two-point glow run has no handedness.** `glow_strip()` inferred which way
to face from the polyline's own centroid. That is fine for a long arc and
meaningless for a short run: a two-point run puts its centroid *on* the line, the
cross product is zero, and `copysign` returns an arbitrary sign. One run of the
east tower's bow came out facing inward at every lit floor — seven faces, and the
validator's open-strip ray test caught all seven. `glow_strip()` now takes a `ref`
point (the tower centre) and decides per segment. The crown's window band, which
is a single quad per side, is built by a new `glow_quad()` that is *told* its
outward direction by the frame that generated it.

That third one is the same class of bug as the offset-handedness note in the
project memory: never derive "outward" from a centroid that might be degenerate.

## 4. Design decisions

**Tower plans: OSM positions, photographic shapes.** OSM's `building:part` ways
944891683/944891684 are the only public source that separates the towers from the
podium, and satellite roof centroids sit ≈9.5 m north-north-west of them —
9.5/87 = 0.11, a ~6° off-nadir lean over an 87 m building, which is what an
oblique satellite does to a tall roof. So the OSM plans are correct *positions*.
The mapper's ten straight segments are not correct *shape*, so each tower's outer
long face is rebuilt as the bow it is (west R ≈ 32 m, east R ≈ 29 m, from the
mapper's own chain).

**Balconies stop at the piers.** The first pass ran a slab across the whole bow;
offset outward, the ends became spikes past the tower silhouette. The slabs now
cover the middle 50 % of the bow, which is also where the reference photograph
puts them, and the two vertical piers land at their ends.

**The piers were added, not found.** Sixteen bands plus sixteen slabs is a stack
of horizontal lines with nothing to stop the eye. The reference photograph shows
a strong pair of piers flanking the central bay; they are in the model at ±10 m
along each tower's axis and they carry the vertical rhythm.

**The rolled bullnose cornice is two steps, not one.** A single fascia band reads
as a ledge. This moulding is the building's single most identifying detail, so it
is built as a wide lower band plus a narrower cap and exaggerated slightly — style
bible §8, semantic exaggeration of the identifier.

**Roof furniture is validated, not placed by eye.** `ROOF_PROPS` are checked
corner-by-corner against the podium outline and both tower plans before they are
built, and anything that overhangs or collides prints a warning and is skipped.
Five props survive on the podium roof (two mechanical masses, two dark solar
arrays, one skylight row) plus a stair head; the two tower roofs carry a
mechanical penthouse at each shoulder.

**Night state.** Hero: the two arched crown window bands in `Toy_gold_Glow`, warm
and distinct. Supporting: an uneven, per-tower-different scatter of apartment
ribbons in `Toy_glassl_Glow` — 320 flats, not an office floor. The lit ribbons
are `Toy_glassl` (6f95b8), never `Toy_glass` (2a4d73): the app draws `_Glow` in a
separate unlit layer at `0.12 + 0.95·uNight`, so at night the surface shows its
raw base colour, and 2a4d73 is the navy of an *unlit* window. Every glow surface
is an open single-layer strip; there is no closed glow shell anywhere in the
model.

## 5. Orientation

Authored +Y = true north, +X = east; the loader applies no rotation. Street sides
were measured from `streets_datasf.geojson`, not assumed:

| Face | Street | Nearest centreline |
|---|---|---|
| South-east (135°) | **Howard Street** — address, entrance | 8.2 m |
| North-east (45°) | **Steuart Street** | 1.6 m |
| South-west (225°) | **Spear Street** | 0.5 m |
| North-west (315°) | party line with the Rincon Annex | (no street within 53 m) |

## 6. Triangle budget as built

| Group | Triangles |
|---|---|
| Podium bands and glazing (10 prisms of the 58-vertex ring) | ~2,280 |
| Podium shopfront, arcade piers, parapet, deck | ~1,900 |
| Podium roofscape (mech, solar, skylights, stair) | ~700 |
| Courtyard (floor, plaza, terraces, planting, pergola, atrium) | ~2,400 |
| Two tower shafts (32 banded prisms) | ~3,600 |
| Balcony slabs (32) | ~1,700 |
| Piers, cornices, central bays, arches, penthouses, masts | ~3,300 |
| Entrance canopy and arched window | ~800 |
| Glow strips | ~380 |

Under budget at 17,034 with the corner-cutting pass held to a selective one
(vertices are only inserted where the ring actually turns more than 18°; a blind
Chaikin pass doubled a ring that is extruded ten times).

## 7. Renders

All from the exported GLB, re-imported into an empty scene:
`-south` (Howard), `-east` (Steuart), `-west` (Spear), `-north` (Annex side and
the courtyard mouth) share one orthographic rig; `-top`; `-aerial` from the app's
high three-quarter camera; `-facade` square-on to Howard; `-aerial-night` with
the `_Glow` emission raised. Day renders fade `_Glow` to 0.12 alpha, which is what
the app actually shows by day. `towers-at-rincon-contact-sheet.png` composes them.

## 8. Approval

*Pending — presented at stage 3 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.*
