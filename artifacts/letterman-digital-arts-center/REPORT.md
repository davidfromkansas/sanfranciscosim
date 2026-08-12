# Letterman Digital Arts Center — build report

`letterman-digital-arts-center.glb` — the Lucasfilm campus at One Letterman
Drive as one grouped SF-SIM landmark: four buildings, the Halprin landscape,
and the Yoda Fountain.

**Status:** built, validated, approved, and optimized (stages 2-4 of
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`). The shipping GLB is the stage-4
output; `optimize/REPORT.md` carries that pass's gates and metrics.

**Gate 3 — approval, 12 August 2026.** David, on the contact sheet, aerial and
night renders: *"yay create a PR so i can review and merge"*. Advancing to
stage 4 (optimize) and stage 5 (integrate).

## Numbers

| | |
|---|---|
| Triangles | 18,238 / 27,000 budget |
| Objects | 197 (merged to ≤ 2 draw calls by the loader) |
| Dimensions | 312.22 × 298.16 × 22.00 m |
| bbox min / max | `[-156.111, -149.082, 0.0]` / `[156.111, 149.082, 22.0]` |
| min Z | 0.0 |
| XY centre offset | `[0.0, 0.0]` |
| File (shipped, post-optimize) | 166,464 B raw · 104,465 B gzip |
| File (as approved, pre-optimize) | 1,032,424 B raw · 249,384 B gzip |
| Draw primitives (shipped) | 20 (from 215) |
| Materials | 12, all `Toy_*`, flat, no textures, no alpha, no `Toy_body` |
| Glow objects | 6 — `b_glow_door`, `b_glow_fascia`, `win_{A,B,C,D}_lit` |
| Scale factor at load | **1.0** — bbox top is exactly `targetHeightM` |

## Contract validation

Fresh factory-reset scene, GLB re-imported, source `.blend` never inspected
(`validate_letterman_digital_arts_center.py` → `validation.json`).

| Check | Result |
|---|---|
| meters_and_plausible_dimensions | PASS |
| base_at_z_zero | PASS |
| centered_xy | PASS |
| under_triangle_budget | PASS (18,238 / 27,000) |
| no_image_textures | PASS |
| no_transparency | PASS |
| materials_follow_contract | PASS |
| no_cameras_or_lights | PASS |
| no_animation_skin_or_constraints | PASS |
| transforms_applied | PASS |
| no_negative_scales | PASS |
| normals_outward | PASS |
| no_degenerate_geometry | PASS |
| no_unexpected_objects | PASS |
| glow_limited_to_declared_night_surfaces | PASS |
| **overall** | **PASS** |

Normals method: closed solids run `recalc_face_normals`; facade and glow panes
are wound explicitly against the outward wall normal. The re-import is then
probed with 22,500 deterministic visibility rays toward nine interior targets —
0 flipped first hits on solids. The two open ground ribbons (`walk`, `stream`)
are single-sided by design and are verified separately: every face points up
(0 downward faces). That ribbon carve-out is the one validator gate that
differs from the fairmont reference, and it is checked, not waived.

## Orientation (contract deviation, recorded per AGENTS rule 5)

Authored `+Y` = true north, `+X` = east; the ~24.9° campus grid is baked into
the footprint coordinates. The contract's "front faces −Y" is **not** honoured
literally — this is a four-building campus facing a shared interior landscape,
and Building B's ILM entrance faces ~205° true (southwest, onto Letterman
Drive). Real-world orientation wins; `placeGeneric()` applies no rotation.

## Dossier corrections made during the build

The plan is a head start, not a citation. Six corrections, all detailed in
`REFERENCE.md` §3:

1. **Building layout was wrong in the plan** — A is the north bar (lagoon east
   of it), not the southern one. Corrected in the plan file too.
2. **Facade material split** — brick base + cream stucco upper body with one
   string course, not an all-brick body with two. Matches the documented "red
   brick, white stucco, terracotta roofs".
3. **Roof construction** — a two-step hip inset self-intersects wherever a wing
   is narrower than twice the offset and exports as inverted black roof faces.
   Replaced with one inset plus separate ridge-beam solids.
4. **Tree count 10 → 22** — the meadow read as an empty slab (style bible §17).
5. **Yoda Fountain 3 m → ~7.5 m** — semantic scale (style bible §9); at 3 m it
   disappeared at the app's camera distance.
6. **Glow design** — lit-room veneers across all facades (~3/8 of panes,
   deterministic) plus B's entrance canopy and door, rather than a single lit
   arcade row. A campus at night is occupied offices.

Two geometry bugs were found by the validator and fixed at source, not waived:
30 degenerate triangles from beveling a 0.08 m plaza slab by 0.04 m (thickened
to 0.22 m, bevel 0.05), and one downward-facing ribbon quad caused by
post-flipping polygons one at a time (`p.flip()` invalidates the cached normals
of polygons read after it) — ribbons are now wound explicitly at construction.

## Height — estimated, and why

**22.0 m**, `"estimated": true`. No published architectural height exists for
any LDAC building: Wikipedia's infobox height fields are blank, Wikidata has
none, and the owner and leasing material state none. OSM tags 15 m (A) and 18 m
(B/C/D), which read as eave heights, not architectural tops — these buildings
carry pitched terracotta roofs above the eave. Derivation (four storeys at
~4.2 m + pitched roof + mechanical) and the full argument are in `REFERENCE.md`
§2. Eave is modelled at 17.2 m, hip deck 20.0 m, ridge 21.0 m, tallest vent
22.0 m.

## Night state

Two glow groups, `Toy_gold_Glow` and `Toy_white_Glow`:

- **Hero** — Building B's entrance canopy fascia and door, the ILM front door.
- **Supporting** — lit-room window veneers, 3 cm in front of their always-present
  glass panes so the app's 0.12 day opacity barely tints them and the 1.0 night
  opacity reads as occupied rooms.

Day colours sit next to their non-glow neighbours (`Toy_gold` against
`Toy_glass`, `Toy_white` against `Toy_trim`). Night render:
`letterman-digital-arts-center-night.png`; night tile on the contact sheet.

## Deliverables

| File | What it is |
|---|---|
| `build_letterman_digital_arts_center.py` | deterministic build (no randomness; re-runs byte-stable) |
| `letterman-digital-arts-center.blend` | authoring scene |
| `letterman-digital-arts-center.glb` | **the asset** |
| `render_letterman_digital_arts_center.py` | review rig (re-imports the GLB; day + `--night`) |
| `validate_letterman_digital_arts_center.py` | fresh-scene contract validator |
| `make_contact_sheet.py` | contact sheet composer |
| `validation.json` | machine-readable validation record |
| `REFERENCE.md` | research dossier and corrections |
| `-north/-east/-south/-west/-top/-aerial/-night/-night-west.png` | review renders |
| `-contact-sheet.png` | the six-view sheet |

Elevations share one rig — same ortho scale, framing, lighting, exposure and
projection, differing only in azimuth. They use a 1800 × 460 letterbox frame:
the campus is 312 m wide and 22 m tall, and a 4:3 frame rendered the buildings
as a hairline.

## Draft manifest entry (not applied here — stage 5 owns the manifest)

```json
{
  "id": "letterman",
  "file": "letterman-digital-arts-center.glb",
  "anchor": [
    -122.4494466,
    37.7997327
  ],
  "targetHeightM": 22,
  "cat": 3,
  "name": "Letterman Digital Arts Center",
  "estimated": true,
  "dims": [
    312.22,
    298.16,
    22.0
  ],
  "tris": 18238,
  "loadRadius": 2500
}
```

`loadRadius` = default rule `max(2500, 22 × 30)` = 2500. The far stand-in is the
baked procedural version, which the exclusion zone will have carved out — 2.5 km
is far enough that the absence is illegible.

## Open risks for integration (stage 5)

- **Terrain seating.** The real site falls several metres from Letterman Drive
  to the lagoon; the base slab is flat and the loader seats it from one terrain
  sample at the anchor. A 312 m asset may float or sink at its edges — verify,
  and flatten the slab perimeter if needed.
- **Exclusion radius.** Must clear all four baked footprints *and* the lagoon:
  ~170 m from the anchor. Consider `clearTrees: true` (Palace of Fine Arts
  precedent) — the grounds are hand-modelled and baked scatter will conflict.
- **Lagoon colour** beside the app's own water material.

---

## Stage 5 — integration (local QA)

| Check | Result | Evidence |
|---|---|---|
| Re-validation of the shipping GLB (fresh Blender scene) | **PASS** | 18,238 tris; 312.222 × 298.157 × 21.993 m; min Z 0.0; centre (0.0, 0.004); 12 `Toy_*` materials; 0 textures, 0 transparent, 0 cameras/lights/actions/armatures |
| GLB dropped into `app/public/sf-assets/landmarks/` | **PASS** | byte-identical to the artifacts copy |
| Manifest entry | **PASS** | served 200, parsed by the app, `loadRadius: 2500` |
| id mapping `letterman` → `letterman` | **PASS** | no hyphens, so `camelId()` is identity; matches the registry id |
| Registry entry (Case B) | **PASS** | `pipeline/lib/landmarks.mjs`, `exclude: 185`, `clearTrees: true` |
| **Tile re-bake (Case B)** | **FAIL — not done, blocked** | see below |
| Asset loads and merges | **PASS** | `sf-assets: letterman merged 20 objects / 12 materials -> batched (9388 tris body); uniform x1.0003 at -1051, -3287` |
| Scale factor ≈ 1.0 | **PASS** | **1.0003** |
| Streaming lifecycle | **PASS** | starts `far`, transitions to `loading` → `live` inside the 2,500 m radius |
| Position / orientation | **PASS** | lands at world (−1051, −3287) = the manifest anchor; the ~25° campus grid lines up with Letterman Drive and O'Reilly Avenue on screen |
| Terrain seating | **PASS** (no visible float or sink at this site) | the 312 m base slab sits flush; the feared edge float did not materialise |
| Single building at the spot | **FAIL** | the baked procedural buildings are still present and intersect the model — the direct consequence of the missing re-bake |
| Night glow | **PASS** | at 22:30 local only the lit-room veneers and B's entrance light; the rest of the campus stays dark |
| Draw calls | **PASS** | the merge line ends in `-> batched`: the asset joins the shared `BatchedMesh` pair, so it adds 0 draw calls (landmarks cost 2 total regardless of count). Not read off the stats overlay — stated from the merge line plus `assets.js`'s batching architecture |
| Fallback drill | **PASS** | GLB renamed away → app boots, area renders, other 18 landmarks unaffected (`live: 18`), exactly one warning: `sf-assets: letterman failed to load (...)`. Case B, so the site is the baked ground — expected. File restored byte-identical |
| `npm run lint` | **PASS** | clean |
| `npm run build` | **PASS** | built in 1.77 s; 3,183 tiles compressed |

### The re-bake is blocked — the one FAIL, and why

Case B requires re-baking the tiles so `excluded()` drops the four procedural
footprints inside the new 185 m exclusion zone and `clearTrees` lifts the
Presidio scatter off the hand-modelled grounds. **That re-bake could not be
produced on this machine, and no tiles are committed in this change.**

`pipeline/buildings.mjs` gap-fills building heights from
`pipeline/data/overture_buildings.geojsonseq` — the source its own header
comment says carries "current OSM heights", because "the 2010 DataSF height
refresh predates the whole post-2015 SoMa skyline". **`pipeline/download.mjs`
never fetches that file**, and it exists nowhere on this machine.
`pipeline/data/` is gitignored, so a fresh `npm run download` produces a data
set the bake cannot reproduce the committed tiles from.

Measured consequences of running the bake anyway:

- `pipeline/validate.mjs` fails its own gate: *tallest procedural building
  200-340 m — 175.4 m*. `overtureAdded: 0`.
- Every building cell diverges from what is committed — 40/40 sampled cells
  differ, including cells nowhere near the Presidio. So the change cannot be
  narrowed to "the cells this landmark touched"; publishing it would flatten
  the downtown skyline across the whole city to fix one Presidio site.

Committing that was the wrong trade, so the tiles are untouched
(`git status app/public/tiles` = 0 changed) and the FAIL is reported here
rather than hidden.

**What this looks like until the re-bake happens:** the GLB loads and places
correctly, but the baked grey blocks stand on the same four footprints and the
Presidio tree scatter covers the meadow. Verified on screen at
`http://localhost:5344`.

**To finish it:** obtain `overture_buildings.geojsonseq` into `pipeline/data/`,
then `cd pipeline && node terrain.mjs && node bridges.mjs && node buildings.mjs
&& node streets.mjs && node landcover.mjs && node validate.mjs && node toy.mjs`,
confirm `node audit.mjs` check 1.6 passes, and commit the changed tiles. Worth
fixing at the source too: `download.mjs` should fetch the Overture extract so
the bake is reproducible from a clean checkout.
