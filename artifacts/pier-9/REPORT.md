# Pier 9 — build report

**Asset:** `artifacts/pier-9/pier-9.glb` — the 1936–38 Pier 9 finger pier (The
Embarcadero at Vallejo St), twin of Pier 19: classical stucco bulkhead building with
monumental arch and `PIER 9` lettering, 240 m grey precast transit shed under a
near-black roof with a continuous glazed monitor, asymmetric working aprons with a
container run, and the Bar Pilots station at the bay end.

Built per `docs/asset-plans/pier-9.md` (Part 1 executed as written; deviations below).
Deterministic build: `build_pier_9.py` (Blender 5.2 LTS, headless). Renders:
`render_pier_9.py`. Validation: `validate_pier_9.py` → `validation.json`, **all PASS**.

## Numbers

| | |
|---|---|
| Triangles | **11,788 shipped** (11,820 pre-optimize; cap 24,000) |
| Objects | 16 meshes / 19 draw submeshes shipped (675 pre-optimize) |
| Dimensions (axis-aligned) | 235.28 × 188.42 × **17.60** m |
| min Z | **−2.60 m — deliberate, a PASS** (deck-top origin; see below) |
| XY centre offset | 0.0, 0.0 |
| Materials | 13 `Toy_*` (10 opaque + 3 `_Glow`); no textures, no transparency |
| Glow strips | 36 open faces, 36 outward |
| Normals | signed volume: all closed objects positive; ray residual 0.013 % (≤ 0.15 %) |
| **Manifest anchor** | **−122.3967994, 37.8006708** (model bbox centre from the build's recentre pass) |
| Axis | long axis 054.59° true; facade faces 234.59° |

**`targetHeightM = 17.6` is a VERTICAL EXTENT, not a height above water** — the model
runs from the pile-stub bottoms at −2.6 m to the bulkhead attic crest at +15.0 m above
the deck-top origin. The loader's `targetHeightM / size.y` scale lands at exactly 1.0.

Two expected results that are **not** failures (stated in `validation.json` too):

- **min Z = −2.6 m, not 0.** Local z = 0 is the top of the pier deck (the pier-1
  precedent): the app's DEM carries this pier as a ~2.5 m ridge, `placeGeneric()` seats
  the origin on that sample, and the fascia + pile stubs below zero are what make the
  tip read as a pier standing out of the water where the DEM falls to 0.
- **The XY bbox is 235 × 188 m although the pier is 254 × 49 m** — the 54.59° heading,
  not a scale error.

## Dossier corrections made while building

- **The plan's "expected bbox ≈ 215 × 175 m" was wrong**; the correct rotation of a
  254.3 × 48.5 m footprint at 54.59° is **235.3 × 188.4 m**. The plan text was corrected
  to the built values.
- **Manifest anchor refined** from the design value (−122.3967912, 37.8006745) to the
  built bbox centre (−122.3967994, 37.8006708) — a 0.8 m shift from the deck's SE bump
  at the bulkhead wharf. Use the built value in the manifest; the registry exclusion
  zones in plan 2.13 were solved around the design anchor and keep working (the main
  zone has 15 m of spare margin against the nearest keeper).
- The raking cornice was first built from stepped boxes and rendered as a crenellated
  staircase; rebuilt as one smooth sloped slab per gable edge.
- The monitor was first started at along −76 (main shed only); extended to −95 so it
  reads full-length per the NRHP description, with the roof planes extended to match.

## Design decisions of record

- Arch enlarged 9.8 → 11.3 m and the archivolt deepened (style bible §8/§9); `PIER 9`
  extruded at 1.15 m in `Toy_ink` (raised dark metal letters in reality). The letters do
  **not** glow.
- The roof is `Toy_roofd` on both planes and the monitor cap — the real built-up roof is
  near-black and the pale monitor + grey plant give it structure. Risk 4 of the plan
  (roof reading as a hole at night) is judged acceptable from the night render: the lit
  monitor stretches and amber lamp line keep the pier's shape legible.
- Night state: warm arch (hero, `Toy_glassl_Glow` f4dcb0), three scattered lit monitor
  stretches + Bar Pilots lookout + 7 lit south windows + 2 wing windows (cool
  `Toy_glass_Glow` cbd8e0), amber lamp globes (`Toy_amber_Glow` e8b563 — off-palette,
  a deliberate WARN; the globes are closed spheres because they ARE the light source,
  unlike the open glow strips).
- Flagpoles/masts: the bulkhead flagpole is omitted (bbox trap); the end-gable pole
  (11.0 m) and Bar Pilots masts (13.8 / 12.6 m) stay below the +15.0 crest.

## Draft manifest entry

```json
{
  "id": "pier-9",
  "file": "pier-9.glb",
  "anchor": [-122.3967994, 37.8006708],
  "targetHeightM": 17.6,
  "cat": 3,
  "name": "Pier 9",
  "estimated": false,
  "dims": [235.28, 17.6, 188.42],
  "tris": 11788,
  "loadRadius": 2500
}
```

Integration: Case B — registry entry + solved three-zone exclusion in
`docs/asset-plans/pier-9.md` §2.13 (do not re-derive by the half-diagonal rule).

## Stage 4 (optimize)

`optimize/REPORT.md`: 915.7 KB -> **283.2 KB raw (-69.1 %)**, 680 -> 19 draw
submeshes, appearance identical within gates (worst 0.33 % night far). The shipped
`pier-9.glb` re-passed the full stage-2 contract validator after the swap; the original
is archived at `optimize/input/pier-9.glb`.

## Approval

- Stage 3 (2026-08-19): approval granted by standing instruction in the session brief —
  "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION" (the user, at pipeline invocation).
  Contact sheet, aerials day/night and numbers were produced and recorded before
  advancing.
