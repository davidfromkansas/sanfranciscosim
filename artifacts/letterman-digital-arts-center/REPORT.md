# Letterman Digital Arts Center — build report

`letterman-digital-arts-center.glb` — the Lucasfilm campus at One Letterman
Drive as one grouped SF-SIM landmark: four buildings, the Halprin landscape,
and the Yoda Fountain.

**Status:** built and validated (stage 2 of
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`). Pre-approval, pre-optimize.

## Numbers

| | |
|---|---|
| Triangles | 18,238 / 27,000 budget |
| Objects | 197 (merged to ≤ 2 draw calls by the loader) |
| Dimensions | 312.22 × 298.16 × 22.00 m |
| bbox min / max | `[-156.111, -149.082, 0.0]` / `[156.111, 149.082, 22.0]` |
| min Z | 0.0 |
| XY centre offset | `[0.0, 0.0]` |
| File | 1,032,424 B raw · 249,384 B gzip (pre-optimize) |
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
