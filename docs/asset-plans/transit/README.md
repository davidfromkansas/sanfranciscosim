# Muni transit fleet — asset plans

<!--
Planning documents. Nothing here has been built: no GLB, manifest, pipeline code,
tile data or app code has been changed by these plans.
-->

Five plans covering the five vehicle families SFMTA operates
([sfmta.com/muni-transit](https://www.sfmta.com/muni-transit)). Each file is a
self-contained handoff: **Part 1** is a runnable task prompt for a fresh agent
session, **Part 2** is the research and design dossier behind it, and **Part 3**
is the shrink-and-bake stage every transit GLB must pass.

**Five families, five GLBs — one per family.** The count comes from the data, not
from taste: see "Why five" below.

| Plan | Slug | The model | Tris |
|---|---|---|---|
| [Muni hybrid bus](./muni-hybrid-bus.md) | `muni-bus` | New Flyer XDE40, 40 ft rigid | 3,000 |
| [Muni trolley coach](./trolley-coach.md) | `muni-trolley` | New Flyer XT40, 40 ft rigid | 3,400 |
| [Muni Metro LRV](./muni-metro-lrv.md) | `muni-lrv` | Siemens S200 SF | 5,000 |
| [Cable car](./cable-car.md) | `cable-car` | Powell single-ended | 6,000 |
| [Historic streetcar](./historic-streetcar.md) | `f-line` | PCC, 3–5 liveries by tint | 4,000 |

Total: **5 GLBs, 5 draw calls, ~21,400 triangles.**

**Build order.** The hybrid bus is the pilot: it proves the vehicle contract, the
destination-sign pattern, the night-glow pass and the shrink stage before
anything else is attempted. The trolley coach reuses the bus body wholesale and
is second. The other three follow in any order — the cable car first if you want
the highest-value asset early, since it is the one that most says "San
Francisco."

---

## Why five

The number comes from what the live feed can actually distinguish.

511.org's SIRI VehicleMonitoring returns, per vehicle: `VehicleRef`,
`LineRef` / `PublishedLineName`, `DestinationName`, `VehicleLocation` and
`Bearing` — verified against `api/ferries.mjs`, which already parses exactly
these fields for the ferry fleet.

Muni routes are fixed to a mode, so **`LineRef` alone resolves the model**:

| `LineRef` | Model |
|---|---|
| `J` `K` `L` `M` `N` `T` | Muni Metro LRV |
| `F`, `E` | Historic streetcar |
| `PM`, `PH`, `CA` | Cable car |
| Trolleybus route numbers (1, 2, 3, 5, 6, 7, 14, 21, 22, 24, 30, 31, 33, 41, 45, 49) | Trolley coach |
| All other numbered routes | Hybrid bus |

Five buckets, matching SFMTA's own "Meet Our Fleet" page exactly. One GLB per
bucket renders the feed faithfully with no guessing.

(**Verified 2026-08-12** against the live feed: all five modes report positions —
329 buses, 108 trolley coaches, 65 LRVs, 9 `F` streetcars on PCC fleet numbers,
and 6 cable cars on `PM` / `PH` / `CA`. Details, including the bus-substitution
trap, in [INTEGRATION-LATER.md](./INTEGRATION-LATER.md).)

**What was cut, and why it can come back.** Earlier drafts split four of the
families by sub-variant — 40 vs 60 foot, Powell vs California, PCC vs Milan — for
nine GLBs. None of those are *mode* distinctions, so none are required. Each is
retained as a "deferred variant" section at the end of its plan, with dimensions,
fleet numbers and build notes intact.

They are cheap to add later because the feed can drive them too: `VehicleRef` is
a real Muni fleet number and the ranges are blocked by model (8601–8969 XDE40,
6500–6730 XDE60, 5701–5885 XT40, 7201–7293 XT60, 1006–1080 PCC, 1807–1895
Milan), so a lookup table would pick the right GLB per vehicle. Every build
script is therefore specified as reusable component functions rather than a
straight-line script.

---

## Scope: models only

**Owner decision, 12 August 2026.** These plans produce **validated GLBs and
nothing else**. No manifest edits, no app code, no spawning, no placement.

Making the fleet reflect real Muni positions in the city is a separate,
explicitly deferred job. Everything already discovered about it — including that
live Muni data is one parameter away from the existing ferry endpoint — is parked
in **[INTEGRATION-LATER.md](./INTEGRATION-LATER.md)** so the modelling sessions
do not have to carry it and the follow-up session does not have to rediscover it.

A related decision, because it does affect the models: **no rails, no overhead
wires, no cable slot** — the scene is not detailed enough to support them, so no
GLB in this set contains track or catenary hardware of any kind. Two
consequences the plans handle explicitly:

- Every vehicle's `min y = 0` is the **street surface**, like a bus. There is no
  top-of-rail question anywhere in this set.
- The trolley coach's poles and the Metro's pantograph reach toward nothing. The
  trolley coach plan's §2.15 treats that as a real open question with a decision
  render attached; the Metro's is minor and its §2.15 says why.

---

## What still constrains the models

Everything in this section changes how the asset is authored, which is why it is
here and not in the deferred file. All measured from `origin/main`.

### The vehicle contract differs from the landmark contract

`app/public/sf-assets/vehicles_manifest.json` states it, and
`.agents/skills/sf-asset-check/SKILL.md` rule 3 assumes buildings:

| | Landmark / kit | **Vehicle** |
|---|---|---|
| Front faces | `−Y` in Blender | **`−Z` in Blender** |
| Origin | base centre, min z = 0 | **centred in X/Z footprint, min y = 0 on the ground** |
| Rotation at load | none (`placeGeneric` authors world-true) | `merged.rotateY(Math.PI)` in `agents.js` |

Authoring a transit vehicle to the landmark convention ships it driving sideways.

### One manifest entry = one permanent draw call

`loadVehicles()` in `app/src/agents.js` builds **one `InstancedMesh` per manifest
entry**, `frustumCulled = false`, alive for the session. 15 entries today = 15
draw calls against the 300-call budget of AGENTS rule 2.

This is an authoring constraint, not just an integration one:

- **Liveries must not each be a GLB.** Five PCC colour schemes as five entries is
  five draw calls for one silhouette. The F-line plan specifies one geometry with
  the livery panels on `Toy_body` for per-instance tinting instead — see that
  plan's §2.6.
- The five plans together add **5 entries, 5 draw calls**. Any deferred variant
  picked up later adds one more each; re-do the arithmetic before adding.

### The app renders vehicles at 1.6× real scale

```js
// app/src/agents.js, setToy()
carScale = on ? 1.6 : 1;
```

Diorama mode is the only mode, so `carScale` is always 1.6, and it applies to the
fleet instances (`dummy.scale.setScalar(carScale)` at ~line 1035), not just the
procedural fallback boxes. Author in **real metres regardless** — AGENTS rule 5 —
but know the on-screen consequence:

| Vehicle | Real length | Rendered at 1.6× |
|---|---|---|
| 40 ft bus / trolley coach | 12.2 m | 19.5 m |
| Siemens S200 LRV | 22.9 m | 36.6 m |
| PCC streetcar | 14.0 m | 22.4 m |
| Powell cable car | 8.4 m | 13.4 m |

A 36.6 m LRV is most of a Sunset block. **Every plan requires a 1.6×-scaled
render against real baked city geometry before the model is called done** — this is the single most likely way these assets
fail, and it will not show up on an isolated turntable.

### No vehicle has a `_Glow` material today

Verified across all 15 shipped GLBs: zero `_Glow` materials. The whole fleet goes
dark while the buildings around it light up.

Transit is the right place to fix that — a lit destination sign is the cheapest
possible "this city is alive" cue — so every plan specifies a glow set. The
loader puts `_Glow` surfaces in a separate unlit layer at
`opacity = 0.12 + 0.95 * uNight`, so, as the Conservatory and Grace Cathedral
work established, a glow surface must be a **thin shell 3–5 cm proud of an opaque
surface**, never the primary surface itself, or it renders 88% transparent by day.

Ship emission at 0.0 per contract. Render gotcha: a glTF `emissiveFactor` of
(0,0,0) makes Blender's importer default Emission Color to **white**, so copy
Base Color into Emission Color before raising strength or every glow surface
previews white.

---

## Part 3 — the shrink and bake stage (shared recipe)

Every plan's Part 3 cites this section rather than restating it. Two things
happen here, and they are not the same thing.

### Stage 1 — meshopt intake compression (mandatory, already in the repo)

`pipeline/compress-assets.mjs` is the shipped intake compressor. Every GLB under
`app/public/sf-assets/` is meshopt-compressed and the decoder is wired in
`app/src/gltf.js`. A new asset that skips this step is the only uncompressed file
in the tree.

```bash
node pipeline/compress-assets.mjs --check   # report only
node pipeline/compress-assets.mjs           # compress in place
```

Two flag constraints are load-bearing and were paid for in bugs:

- **`-km` is required.** Without it gltfpack merges materials with identical
  parameters across the `_Glow` boundary — glow-ness is name-only — silently
  destroying the night layer.
- **`-noq` is required.** Quantisation looks like free savings and is not: the
  kit and landmark merge paths bake world matrices directly into the position
  arrays, and int16 `KHR_mesh_quantization` attributes corrupt them. Verified —
  quantised pieces fail their dims gate and fall back to procedural.

The effective flag set is therefore `-cc -kn -km -noq`.

### Stage 2 — the geometry shrink pass (per asset, before intake)

Compression re-encodes bytes; it does not remove waste. The shrink pass does,
and the reference implementation with generic scripts is
`~/sf-3d-assets/optimized/st-marys-cathedral/` (`inspect.py`, `optimize.py`,
`validate.py`, `render_ab.py`, `diff_ab.py`) driven by
`~/sf-3d-assets/GLB-OPTIMIZE-PROMPT.md`, run with `ASSET_CLASS=vehicle`.

Order of operations, measuring tri/vert deltas after each step:

1. **Weld** coincident verts within each object at ≤ 1 mm — but **never across a
   `_Glow` boundary**, which would flatten the intentional 3–5 cm proud shells.
2. **Delete degenerate faces** (< 1 mm²) and interior faces buried inside unioned
   solids. Interior-face occluders must be **closed meshes**: the signed volume
   of an open shell is meaningless and lets it masquerade as a solid box, eating
   real faces.
3. **Limited dissolve at 0.05°, not 0.5°.** The prompt doc's 0.5° is unsafe on
   curved shells — transitive merging builds twisted ngons that re-triangulate
   with flipped windings. Savings at 0.05° are near-identical.
4. **Retessellate over-segmented curves.** Wheels, poles and roof pods are the
   usual offenders. Segment counts are set against the vehicle camera distances
   (near 15 m, far 120 m), *then* multiplied by the 1.6× render scale.
5. **Join objects sharing a material** into one mesh per material. On a bus with
   a hundred small parts this is the largest single file-size win.
6. **Normals audit**: per-object signed volume positive. A vehicle is a union of
   solids, so expect the ~0.1% ray-test residual; signed volume is the
   authoritative gate.

Then run Stage 1 on the result.

### What is explicitly out of scope

**Do not run the high→low texture bake** (`ALLOW_BAKE=yes`, normal + AO maps to
KTX2). It is the sanctioned exception for hero landmarks, and it is wrong here:
these are 8–23 m objects seen at 1.6× from a 42° aerial camera, drawn as
instanced meshes where a per-type texture atlas is pure GPU cost against
geometry that is already cheap. The flat-colour contract stands. If an asset
cannot make its triangle budget without a bake, the model is too detailed —
simplify it.

### Budget gates for transit assets

| Gate | Threshold |
|---|---|
| G1 Contract | material name set identical pre/post; `_Glow` layer intact and separate; front `−Z` and min y = 0 preserved |
| G2 Fidelity | bbox within max(1 cm, 0.1%); origin offset within 1 cm; per-object signed volume positive |
| G3 Round-trip | re-imports in Blender **and** loads through `createGLTFLoader()` from `app/src/gltf.js` with the meshopt decoder |
| G4 Appearance | day **and** night A/B at 15 m and 120 m, rendered at 1.6× scale; mean pixel delta ≤ 4% near, ≤ 2% far |
| G5 Draw calls | primitive count ≤ input |
| G6 Size | file smaller after the pass; if under target, the waste census must prove the remaining bytes are silhouette |
| G8 Hygiene | no leaked objects from other Blender scenes (re-import count check); `.blend1` backups deleted |

For reference, the shipped fleet after meshopt intake:

| Vehicle | Tris | GLB bytes |
|---|---:|---:|
| `commuter-bus` | 4,888 | 64,628 |
| `sedan-coral` | 5,788 | 75,524 |
| `taxi` | 9,688 | 121,500 |
| `sf-bay-ferry` | 27,224 | 539,420 |

### A contract discrepancy to work around

`.agents/skills/sf-asset-check/SKILL.md` rule 5 states **"vehicle piece ≤ 300"**
triangles. The shipped fleet runs 4,888–9,688 — 16× to 32× over. Since the fleet
is live and passing, the skill line is the stale one.

These plans budget against the **shipped fleet** as the de facto standard, at the
lean end of it (3,000–6,000 depending on family, stated per plan). Correcting the
skill is noted in [INTEGRATION-LATER.md](./INTEGRATION-LATER.md).

---

## Shared contract for all five

- Style: `docs/styles/miniature-toy.md` — authoritative for artistic decisions.
  Vehicles are explicitly covered: they are storytelling props, chunky and
  beveled, flat saturated colour, never scanned or photoreal.
- Technical contract: `.agents/skills/sf-asset-check/SKILL.md`, **with the
  vehicle overrides above** (front `−Z`, min y = 0, origin centred).
- Repo rules: `AGENTS.md` — rule 3 (procedural fallback survives —
  `carArchetype()` in `agents.js` stays), rule 5 (real dimensions).
- Reference implementations: `app/public/sf-assets/vehicles/` for the vehicle
  contract, `artifacts/streetkit/` for a multi-piece kit's build + validate
  scripts, `artifacts/salesforce-tower/` for the full artifact-directory shape.
- Binary GLB, real metres, applied transforms, flat `Toy_*` colours, `_Glow`
  only for night surfaces, no textures, no transparency, no cameras, lights,
  animation or armatures in the export.
- **No rails, wires, catenary poles, cable slots, sleepers or track hardware in
  any GLB in this set.**
- **No manifest edits and no app code changes** in any modelling session. The
  draft manifest entry belongs in the asset's `REPORT.md`.

## Deliverable shape (all five)

```
artifacts/<slug>/
  REFERENCE.md          research dossier with sources
  build_<slug>.py       deterministic Blender build script
  validate_<slug>.py    fresh-scene re-import validator
  render_<slug>.py      day + night review renders at 1.6x
  <slug>.blend
  <slug>.glb            the single model
  validation.json
  REPORT.md             results, PASS/FAIL per gate, draft manifest entries
  renders/              elevations, aerial, contact sheet, night, in-city 1.6x test
```

## Sources

- [SFMTA — Muni transit](https://www.sfmta.com/muni-transit) — the five families
- [San Francisco Municipal Railway fleet](https://en.wikipedia.org/wiki/San_Francisco_Municipal_Railway_fleet) — models, fleet numbers, quantities
- [Muni Metro](https://en.wikipedia.org/wiki/Muni_Metro) — LRV fleet, surface lines
- [San Francisco cable car system](https://en.wikipedia.org/wiki/San_Francisco_cable_car_system) — car dimensions, fleet counts
- [F Market & Wharves](https://en.wikipedia.org/wiki/F_Market_%26_Wharves) — historic fleet composition and liveries
- This repository: `app/src/agents.js`, `app/src/gltf.js`,
  `pipeline/compress-assets.mjs`, `app/public/sf-assets/vehicles_manifest.json`
