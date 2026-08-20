# Pier 17 — build report

**Asset:** `artifacts/pier-17/pier-17.glb` — the 1912 pier shed on its own
deck, Embarcadero at Green Street, Exploratorium campus.

**Numbers (validated, fresh-scene re-import of the SHIPPED, optimized GLB):** 1,998 triangles · 57,784 B raw (153,280 B pre-optimize, archived at optimize/input/) · 13 draw submeshes (was 92) ·
AABB 234.0 × 182.7 × 21.30 m · min z 0.0 (water level) · centered ·
10 materials (2 glow) · validation.json all-PASS.

**Anchor:** lon −122.3981018, lat 37.8022149 (model AABB centre, printed by
the deterministic build). `targetHeightM` **21.3** (flagpole tip; the export's
bbox top is normalized to it exactly).

## Dossier corrections made during the build

1. **The bay-end notch is on the SE (Valley) side, not the NW side.** The
   plan's prose said the NW half stops short; the OSM ring says the opposite —
   the NW two-thirds (w −21.4…+8.2) extends to s ≈ 119.6 and the **SE third
   stops at s ≈ 114.05**. Modelled from the ring, not the prose.
2. **Anchor moved ~3 m.** The plan derived the anchor from the deck ring's
   (s,w)-bbox midpoint (−122.3981053, 37.8022416). The loader centres on the
   **world-axis AABB**, whose centre is (−122.3981018, 37.8022149). The build
   recentres on the world AABB and prints the authoritative value.
3. **Roof material split corrected for readability.** The plan's Toy_stone
   roof read as the same value as the Toy_trim walls and Toy_stone deck from
   the app camera (first render pass, top view). The membrane is now
   `Toy_white` (on-palette), the deck stays `Toy_stone`, and the skylight
   strip gained an opaque `Toy_glass` layer under its glow plate so it reads
   dark by day instead of vanishing at 12% glow alpha.
4. **Sign backing changed ink → trim.** The real sign is a white plate; an
   ink backing read as a dark hole in the day pass. The diamond plate is now
   cream with the glow face proud of it.

## Design decisions of record

- The asset carries the **pier deck** (real OSM `man_made=pier` ring
  simplified to its 5 true corners, 2.0 m slab, `Toy_stone` top, `Toy_ink`
  pile/fender sides) because the app bakes no pier decks and `placeGeneric()`
  clamps its terrain sample to water level (0) over open water. Origin
  convention: bridge/island (min z = water).
- True-world orientation (bearing 54.9°); the contract's "front faces −Y" is
  overridden by AGENTS rule 5. The (s,w)→world map is a reflection; every
  ring passes `ring_ccw()` and normals derive from winding.
- Night state: ridge skylight strip is the hero (`Toy_glass_Glow`); sign
  face + transom (`Toy_trim_Glow`) and 3 Valley bays support. All glow faces
  are thin plates proud of opaque surfaces.
- Fog horn (the waterfront's last original) modelled on the bay-end gable,
  pointing to sea — the storytelling accent; the only saturated colour is
  the `Toy_ioorange` pennant.

## Stage gates

- **Gate 2 (validated GLB):** PASS — `validation.json` all-PASS at 1,998
  tris, dims plausible, normals clean (signed volume all-objects, ray residual 0).
- **Gate 3 (approval):** the user pre-approved the full pipeline for this
  batch run: **"APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"** —
  2026-08-19, quoted from the invocation. Logged here per stage-3 rules.

## Iteration log

- Pass 1: full build (1,962 tris), day renders reviewed from top + west.
  Found the roof/wall/deck value mush, the vanishing skylight, the dark sign
  (corrections 3–4). Aerial camera was mis-framed down the long axis;
  re-aimed from the SSE at 65 mm.
- Pass 2: rebuilt (1,974 tris), then a final pass aligned the strip windows to the pilaster bays and reframed the aerial (1,998 tris), re-rendered all views, re-validated: PASS.

## Stage 4 — optimize

GLB-OPTIMIZE-PROMPT v2 run in `optimize/`: full Phase B (weld 3,958→1,179
verts; dissolve no-op; join 90 objects→13 meshes) + gltfpack 0.24
`-c -km -kn -noq`. 153,280 → 57,784 B raw (−62%), submeshes 92 → 13, all
gates G1–G8 PASS (G4 max mean pixel delta 0.084%). The packed file re-passed
the full stage-2 contract validator (0 invalid normals). Shipping swap done;
pre-optimize original archived at `optimize/input/pier-17.glb`.

## Stage 5 — integrate (batch mode, Case B)

Production URL: **not deployed** — batch mode ends at a source-only branch;
`docs/asset-pipeline/BATCH-INTEGRATE.md` bakes the city once for the whole
piers batch and opens the single PR.

| check | result |
|---|---|
| re-validation of shipped GLB (fresh scene) | PASS (all checks, 1,998 tris) |
| GLB intake compression | PASS (already meshopt from stage 4; compress-assets skips it) |
| manifest entry (text-append, JSON valid) | PASS — 104 entries |
| id mapping camelId('pier-17') = 'pier-17' | PASS (digit hyphen untouched; registry id matches) |
| registry entry + exclusion | PASS — `exclude: 100`, window (74.5, 142.2) measured |
| re-bake (QA only, then discarded) | PASS — chain exit 0, zero-churn vs vintage dataset |
| audit 1.6 (no footprint in zone) | PASS — 114 zones over 110 landmarks clear |
| verify-rebake | PASS — only cell 22_8 changed (21→20); nearest survivor 142.2 m vs r=100 |
| tile decode proof | PASS — merged Pier 17 trace gone; Pier 19 top 13.8 m and Pier 15 top 14.3 m unchanged (no Overture height retarget) |
| single building / no twin / no z-fight | PASS (day + wide screenshots, artifacts/pier-17/qa/) |
| merge line + scale | PASS — `pier-17 merged 13 objects / 10 materials -> batched (1092 tris body); uniform x1.0000 at 3467, -3561` |
| orientation | PASS — front SW onto the Embarcadero, shed NE into the bay (wide.png) |
| terrain seating | PASS — seats at water level, own 2.0 m deck carries it (by design over water) |
| night glow | PASS — ridge skylight hero + sign/transom/3 bays only (night.png) |
| draw calls | PASS — avg 83/frame at the landmark (< 300) |
| fallback drill | PASS — app boots with the GLB served 404; exactly one streamed-path warning (`pier-17 failed to load (... 404)`); site is empty pier ground inside the zone (Case B, expected). Drill screenshots skipped under load ~500; see qa/drill_run.log note |
| lint / build / tests | PASS — eslint clean; `npm run build` (incl. muni-motion + asset-loading tests) exit 0 |
| streaming lifecycle check | DEFERRED to BATCH-INTEGRATE — `landmark-streaming-check.mjs` needs a served build and is specified per batch, not per landmark |
| batch sanity: no generated files vs origin/main | PASS — rebased onto f4f5f99f5; `git diff --name-only origin/main` lists nothing under app/public/tiles/ or api/_data/ |
| deployed QA | n/a until the batch PR ships |

Pre-existing audit FAILs observed (dataset-wide, unrelated to this landmark,
present in a clean bake of the vintage dataset): 1.2b p95 height, 1.3c
Telegraph Hill DEM, 1.7b one offshore sampled tree.

Leak checklist (batch-source-only): intake compression's in-place rewrite of
`vehicles/passenger-airplane.glb` was caught and reverted; `pipeline/data`
symlink and logs left untracked; author email is the GitHub noreply.
