# Hills Brothers Building — build report

Miniature GLB of 2 Harrison Street (Hills Bros. Coffee Plant, SF Landmark 157)
for SF-SIM, built 19 August 2026 from
`docs/asset-plans/hills-brothers-building.md`. Deliverables in this folder:
deterministic build script, .blend, .glb, six day renders + night render +
contact sheet, REFERENCE.md, validation.json.

## Numbers (validated, fresh-scene re-import of the shipping GLB)

| | |
|---|---|
| Triangles | 10,242 (budget 24,000) |
| Objects | 13 (516 authored; stage 4 joined per material — 15 draw submeshes) |
| Dimensions | 84.85 × 84.85 × 53.2 m (world-axis bbox of the 45°-rotated quad) |
| min Z / centre offset | 0.0 / (0.0, 0.0) |
| Crest | 53.2 m exactly = `targetHeightM` (loader scale lands at 1.0) |
| File | **267 KB raw** shipped (stage-4 meshopt; 753 KB pre-optimize archived at `optimize/input/`) |
| Materials | Toy_brick, Toy_rust, Toy_trim, Toy_cream, Toy_glass, Toy_ink, Toy_stone, Toy_roofd, Toy_steel, Toy_red, Toy_red_Glow, Toy_white_Glow |
| Validation | `validation.json` — **all checks PASS** |

## Orientation

Authored true-world: Blender +Y = north. The Embarcadero facade (75.4 m)
faces south-east (normal 135° true); Harrison Street is the south-west side;
the campanile projects north-west toward the mid-block plaza. The asset
contract's "front faces −Y" is deviated from deliberately — real-world
orientation wins (AGENTS rule 5, plans README orientation note); the loader
applies no rotation.

## Design decisions

- **Massing**: OSM ring idealized to a 75.5 × 44.2 m rectangle (max deviation
  0.5 m from the measured ring), lightwell at its measured offset position,
  built as four interpenetrating wing prisms so the well is a true void; well
  floor at ~5 m with window pads on the inner walls.
- **Facades**: continuous ground arcade of segmental-arched openings (photos
  show arches across the base, iterated from an alternating first pass), four
  recessed sash rows, arcaded sixth floor, stone base band, trim corbel band,
  tall parapet with light cap — 12 bays on the long facades at the 5.8 m
  module (real ~13; compressed one module by the corner margins).
- **Campanile**: 15.4 × 15.7 m, smooth shaft with paired slit recesses
  (slimmed in iteration 2), arcade stage with four arched recesses per free
  face (two on the face over the wing), trim corbel cornice, low parapet,
  terracotta pyramid, steel finial at exactly 53.2 m. The real flagpole above
  the finial is omitted (plan 2.15 risk 1).
- **Penthouse (1985)**: cream volumes with hipped `Toy_rust` roofs ringing the
  lightwell on the SE/SW/NW wings; the NE wing is the pale mechanical roof
  with four steel units, matching the satellite. A small cream gable with an
  arched pad marks the feature visible over the sign in the Pier 14 photo.
  Iteration 2 thinned the hip wedges (walls 28.1, crest 29.2) — the first
  pass read as one giant mansard.
- **Sign**: "HILLS BROS COFFEE" as chunky `Toy_red` letter blocks on a fine
  steel lattice (posts + two rails), SE wing roof edge near the Harrison
  corner, faces the bay. Letters carry `Toy_red_Glow` plates proud of the
  SE faces only — the hero night glow. Not literal typography (plan 2.15
  risk 5).
- **Night state**: sign red + tower arcade warm-white plates
  (`Toy_white_Glow`), both matching the Commons night photo. Glow plates are
  thin shells proud of opaque geometry, never primary surfaces.

## Dossier corrections / verifications made while building

1. The plan's §2.3 said the tower projects at the "south-west end" of the NW
   facade; the measured building-frame coordinates put it mid-facade, u
   −11.1..4.3 of −38..37.4 (directly north-west of the lightwell). Built from
   the vertex table, not the prose.
2. Penthouse crest lowered from the plan's 29.5 m to 29.2 m after the aerial
   review (the LiDAR shoulder supports 28–30; the flatter wedge reads truer
   to the satellite).
3. Night-render method: the glTF round-trip re-imports `_Glow` materials with
   default white emission; the render rig copies Base Color into Emission
   Color before lighting (plans README, "Night renders"), which is exactly
   what the app's unlit night layer does.

## Render iterations (logged per stage-3 rules)

1. **v1**: window/arch panels were recessed *into* the wall solids (negative
   panel depths) and invisible — every facade rendered blank. Rebuilt with
   panels proud of the wall plane (the reference implementation's idiom).
2. **v2 review (aerial/top/elevations)**: ground arcade made continuous
   (was alternating); tower slits slimmed 1.1→0.7 m and shortened; sign
   lattice thinned; penthouse hips thinned and the gable moved to engage the
   SE band; roof-deck strip extended along the sign; aerial camera pulled
   back to clear the pyramid.
3. **v3**: night pass re-rendered with base-color-driven emission (sign now
   red, arcade warm white). Final.

## Stage 3 — approval

The user pre-authorized the whole pipeline for this session:
**"APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"** (David, 19 Aug 2026, the
session's opening instruction, quoted verbatim). Gate 3 is recorded as
satisfied by that standing instruction; renders and contact sheet are
committed for after-the-fact review.

## Draft manifest entry (verified numbers)

```json
{
  "id": "hills-brothers-building",
  "file": "hills-brothers-building.glb",
  "anchor": [-122.3892854, 37.7894167],
  "targetHeightM": 53.2,
  "cat": 3,
  "name": "Hills Brothers Building",
  "estimated": false,
  "dims": [84.9, 84.9, 53.2],
  "tris": 10242
}
```
