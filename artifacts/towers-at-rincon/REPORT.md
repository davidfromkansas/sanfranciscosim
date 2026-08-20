# The Towers at Rincon (88 Howard Street) — build report

`towers-at-rincon.glb`, built by `build_towers_at_rincon.py`, validated by
`validate_towers_at_rincon.py` against a fresh re-import of the exported file.
Research and sources are in `REFERENCE.md`; this file records what was decided,
what the plan got wrong, and what the numbers came out to.

## Shipping numbers

| | |
|---|---|
| Triangles | **17,035** (cap 18,000) |
| Objects (draw submeshes) | **10** — one per material, after the stage-4 join |
| Dimensions | **108.66 × 108.67 × 89.00 m** |
| min Z | 0.0000 |
| XY centre offset | 0.0000, 0.0000 |
| Materials | 10, all `Toy_*`, flat, no textures, no alpha |
| Glow materials | `Toy_cream_Glow` (flats), `Toy_gold_Glow` (crown, entrance) |
| Open glow-strip faces | 130, all 130 facing outward |
| Signed-volume inverted objects | 0 |
| Normals ray test | **0 flipped** first hits (tolerance 0.15 %) |
| Validation | **PASS** (`validation.json`) |
| File | **352,820 B** raw, meshopt-compressed (913,488 B before stage 4) |
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
85.40 m; arch to 87.20 m; mast to 89.00 m. CTBUH says 22 storeys and Wikipedia
says 23 — the height is measured, so that is a labelling disagreement, not a
geometry one.

## 3. Five iterations that changed the model

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

**c. The top glazing ribbon caps above the roof deck.** Every podium band's
glazing prism runs to `z0 + band + EMBED` — the embed exists so each ribbon sinks
into the band above it — but the top band has no band above it, so the topmost
ribbon's navy cap sat 4 cm proud of a roof deck that ended exactly at
`Z_PODIUM`. From the app's own overhead camera the entire podium roof rendered
dark navy: not a hole this time, a lake. The decks now finish 14 cm above
`Z_PODIUM` (and the equivalent for the tower shoulder and bay decks, where the
same arithmetic left only 1 cm of margin). Caught in the stage-2 aerial, after
the `Toy_roofd` fix had already been credited with fixing the roofs.

**d. A two-point glow run has no handedness.** `glow_strip()` inferred which way
to face from the polyline's own centroid. That is fine for a long arc and
meaningless for a short run: a two-point run puts its centroid *on* the line, the
cross product is zero, and `copysign` returns an arbitrary sign. One run of the
east tower's bow came out facing inward at every lit floor — seven faces, and the
validator's open-strip ray test caught all seven. `glow_strip()` now takes a `ref`
point (the tower centre) and decides per segment. The crown's window band, which
is a single quad per side, is built by a new `glow_quad()` that is *told* its
outward direction by the frame that generated it.

That last one is the same class of bug as the offset-handedness note in the
project memory: never derive "outward" from a centroid that might be degenerate.

**e. The lit windows were the wrong colour, and only the city could show it.**
The flats were `Toy_glassl_Glow` (6f95b8), chosen the way 49 South Park chose it —
anything but `Toy_glass_Glow` (2a4d73), which is the navy of an *unlit* window.
In the Blender night render it looked fine. In the app at 22:00, next to
procedural blocks whose windows emit `vec3(1.0, 0.78, 0.5)`
(`app/src/materials.js:296`), it read as the one cold building on the block —
a 320-flat residential tower glowing blue while its neighbours glowed amber.
Changed to `Toy_cream_Glow` (f2ede3): warm off-white, same family as the
neighbours, still a clear step cooler than the gold crown. Stage 4 was re-run
from scratch on the changed asset rather than patched.

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
and distinct — and 0.90 m deep, not the 0.20 m the first pass gave them, which
rendered the hero glow as a hairline. A warm band under the entrance canopy is
the only thing lit at street level. The lit apartment ribbons are
`Toy_cream_Glow` (f2ede3): see §3e, this was `Toy_glassl_Glow` until the local
QA put it next to the real city. Supporting: an uneven, per-tower-different scatter of apartment
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

**Engine: EEVEE, not Cycles.** This machine was running many parallel asset
sessions while these were made — load average above 500 — and a single 1200x1000
CPU Cycles frame of a 17k-triangle block was taking longer than the rest of the
stage. EEVEE with soft shadows and ambient occlusion gives the same reading of
massing, silhouette, banding and glow for a flat-material asset, and falling back
under render contention is the project's own documented practice. Noted so nobody
reads the slightly flatter shading as a modelling choice.

All from the exported GLB, re-imported into an empty scene:
`-south` (Howard), `-east` (Steuart), `-west` (Spear), `-north` (Annex side and
the courtyard mouth) share one orthographic rig; `-top`, rolled to the site-plan
convention with Howard Street at the bottom of the frame and the courtyard mouth
at the top; `-aerial` from the app's
high three-quarter camera; `-facade` square-on to Howard; `-aerial-night` with
the `_Glow` emission raised. Day renders fade `_Glow` to 0.12 alpha, which is what
the app actually shows by day. `towers-at-rincon-contact-sheet.png` composes them.

## 8. Stage 4 — optimize

The shipping file is the optimized one: 253 objects joined to 10 (one draw
submesh per material), 29,942 vertices welded to 9,123, meshopt-packed with
`-c -km -kn -noq`. Raw bytes 913,492 → 352,836 (−61.4 %); triangles, bounding
box, origin, material set and glow behaviour all unchanged; A/B pixel deltas
peak at 0.186 % and contain nothing but Cycles sampling noise. All gates G1–G6
and G8 pass (G7 n/a, no bake). Full metrics, census and per-phase savings in
`optimize/REPORT.md`; the pre-optimize asset is archived at
`optimize/input/towers-at-rincon.glb`.

## 9. Stage 5 — integration (batch mode)

Case B. `app/public/sf-assets/landmarks/towers-at-rincon.glb` (byte-identical to
the artifact), one appended manifest entry, one appended
`pipeline/lib/landmarks.mjs` entry (`towersAtRincon`, `exclude: 32`,
`camera: { distance: 620, yaw: 90, pitch: 22 }`), and a full tile re-bake that was
run for the QA and then **discarded** — this landmark is one of a batch, and a
Case B bake rewrites ~600 generated files whoever triggers it.

| Check | Result |
|---|---|
| Re-validation of the shipping GLB | PASS — 17,035 tris, 108.66 × 108.67 × 89.00 m, min z 0, centre (0,0) |
| Manifest entry | appended as TEXT, not via `json.dumps` — diff is **19 insertions, 0 deletions**, so no other landmark's `11.0` was rewritten to `11` |
| id mapping | `towers-at-rincon` → `camelId()` → `towersAtRincon`, matches the registry |
| Registry splice | landed in `LANDMARKS` (97), **not** in `VIEW_PRESETS` (still 6) |
| Bake | full chain terrain → … → context → muni-shapes, exit 0 |
| Audit 1.6 | **PASS** — "100 zones over 97 landmarks clear" |
| Exclusion, from the TILE | **0** procedural buildings have any vertex inside the 32 m radius; nearest surviving vertex **34.47 m** (the Rincon Annex, 28.6 m tall) |
| Both rings dropped | cell 23_11 goes 72 → 71: the DataSF ring and the Overture duplicate together were one baked building, and it is gone |
| Party-line slivers | neither Overture wedge baked — no `extraExclusions` needed after all |
| Collateral | none; the Annex keeps its procedural block |
| Merge line | `sf-assets: towers-at-rincon merged 10 objects / 10 materials -> batched (9050 tris body); uniform x1.0000 at 3961, -2431` |
| Scale factor | **1.0000** — authored height and `targetHeightM` agree exactly |
| One building on the site | yes — no procedural twin, no baked block through the model, no z-fighting |
| Terrain seating | pivot y 4.20 m at the anchor; real ground there is 3.36–4.67 m NAVD88 |
| Orientation | Howard Street frontage and the entrance face south-east, as authored |
| Night | warm flats + gold crown; only the intended `_Glow` surfaces light |
| Lint / build | `npm run lint` clean; `npm run build` clean (tests run inside it) |
| Fallback drill | PASS — see below |
| Batch sanity | `git diff --name-only <merge-base> HEAD` lists **nothing** under `app/public/tiles/` or `api/_data/` |

**The stray cell, settled.** `verify-rebake.mjs` reported my cell 23_11 (72 → 71,
correct) *and* a second cell 23_13 (169 → 182) that is ~2 km away and cannot be
reached by a 32 m radius. Its own diagnostic says to tell a radius overreach from
a data-snapshot difference by removing the landmark and re-baking: with
`towersAtRincon` deleted from the registry, **23_13 still differs from
origin/main by the same 169 → 182**. So it is the `pipeline/data/` vintage, not
this exclusion. (`origin/main` also advanced from `335cb9ac1` to `2c14d5f9f`
mid-session — worktrees share one repository — so the tile baseline moved
underneath the check.) The bake is discarded either way.

**Fallback drill (mandatory).** With the GLB renamed away: the app boots, the
area renders, and there is exactly **one** console warning naming the slug —
`sf-assets: towers-at-rincon failed to load (…)`. The site is bare ground inside
the exclusion zone, which is the documented Case B outcome, not a bug. Note the
wording is "failed to load", not INTEGRATION-PROMPT Step 6's "— keeping the
code-built landmark": a streamed landmark (one with a `loadRadius`) takes a
different path and warns differently. File restored and re-verified byte-identical.

**Draw calls: the counter in this build cannot answer the question.**
`app/src/toypost.js` renders the scene into a target and then draws a fullscreen
quad, and three resets `renderer.info` at the start of every `render()` call — so
the overlay, which reads it after the quad pass, reports `draw calls 1 /
triangles 0.00 M` at *every* location, including untouched stress cells
(downtown and the Mission both read 1). That is pre-existing and unrelated to
this change. What can be stated: the landmark **joins the shared `BatchedMesh`**
(the merge line says `-> batched`), which is 2 draw calls for all landmarks
together, so it adds none. Headless fps at street level was 98 (downtown), 130
(Mission), 126 (this site) under SwiftShader.

**One thing for the batch integrator.** With 71 landmarks live at this camera,
the shared body batch holds 328,267 triangles ≈ 985k of its 1,200,000-vertex
reserve — **82 % full**, and this asset is 9,050 of those triangles. Nothing
failed to batch here, but the reserve is the thing that silently drops a
different landmark each reload when it overflows. Re-check it once the whole
batch is in.

## 10. Approval

Stage 3 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md` is a human gate. The session
was opened with a standing instruction, quoted verbatim:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"
> — David, 18 August 2026, in the invocation of this pipeline run

That is a pre-authorisation for the whole run rather than a judgment on this
asset, so it is recorded as what it is: the contact sheet, the aerial day and
night renders and the numbers above were presented, and the pipeline advanced to
stage 4 on that standing instruction. Nothing here was pushed, PR'd or deployed —
those still wait for an explicit decision at gate 5.
