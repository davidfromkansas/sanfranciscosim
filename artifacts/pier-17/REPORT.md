# Pier 17 — build report

**Asset:** `artifacts/pier-17/pier-17.glb` — the 1912 pier shed on its own
deck, Embarcadero at Green Street, Exploratorium campus.

**Numbers (validated, fresh-scene re-import):** 1,998 triangles ·
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
