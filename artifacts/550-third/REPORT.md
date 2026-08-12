# 550 Third Street — build report

Deliverable of stages 1–3 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run
12 August 2026 from the input `BUILDING: 550 3rd St, San Francisco, CA 94107`.

**What this is:** a miniature GLB of the 1921 SoMa warehouse at 550 Third
Street as it stands after its 2022–25 conversion — a long low bar whose whole
identity is its roof. `REFERENCE.md` holds the research; this file holds what
was built, what was corrected, and what was measured.

## Shipped numbers

| | |
|---|---|
| File | `550-third.glb` |
| Raw / gzipped | **69,364 B / 39,716 B** shipped (380,076 / 63,101 as authored — stage 4 cut it 5.5×, see `optimize/REPORT.md`) |
| Triangles | **6,244** shipped, 6,280 as authored (cap 14,000) |
| Objects | 13 shipped (135 as authored; joined per material), 14 draw primitives |
| Dimensions (m) | 49.209 × 50.410 × **11.000** |
| min Z | 0.000 |
| XY centre offset | (0.022, 0.021) m |
| Loader scale factor | **1.000** (`targetHeightM 11.0 / measuredHeight 11.0`) |
| Materials | 13, all `Toy_*`, flat, no textures, no alpha, no `Toy_body` |
| Glow materials | `Toy_glassl_Glow`, `Toy_white_Glow` |
| Anchor | −122.3953409, 37.7804407 |
| Long-axis heading | 45.3° true |
| Validator | Blender 5.2.0 LTS, fresh-scene re-import of the exported GLB |

`validation.json` is the machine-readable version: overall **PASS**, all 15
authoring checks, plus a `shipped` block carrying the packed file's numbers.
The packed file's own gates are in `optimize/validation.json` (G1/G2/G5) and
`optimize/g3check`.

## Orientation — a documented contract deviation

The contract in `.agents/skills/sf-asset-check/SKILL.md` says "front faces −Y".
This building's front faces **north-east** (outward normal 44.6° true), because
the SoMa grid is rotated ~45°. `placeGeneric()` in `app/src/assets.js` scales and
positions but never rotates, so honouring "front faces −Y" literally would drop
the building into the city facing the wrong street.

The asset is therefore authored in **true-world orientation** (`+Y` = north,
`+X` = east), per AGENTS rule 5 and the orientation note in
`docs/asset-plans/README.md`. No `yawDeg` override is needed.

## Corrections made to the plan's dossier

**REPORT beats plan.** Four corrections, all found by verification rather than
inherited:

1. **Facade openings had to be built proud of the wall, not recessed into it.**
   The plan's §2.7 specified negative depths for every window, door and reveal.
   The walls are solid prisms with no cut openings, so all of that geometry was
   buried inside the shell: the first aerial review render showed a completely
   blank 3rd Street elevation. Every facade assembly now sits 0–0.16 m proud, and
   the apparent recess comes from the pilasters standing 0.20 m in front.
2. **Exclusion radius is 8 m, not the plan's estimated 12 m.** Measured against
   the actual bake-side geometry (DataSF footprints simplified at the pipeline's
   0.6 m tolerance, `ringCentroid`): this footprint's ring centroid is 0.96 m
   from the anchor; the nearest *neighbour* vertex is 11.17 m (SF3776007) and the
   next is 12.19 m (SF3776008). The radius window that drops this building alone
   is 0.96 < r ≤ 11.17 — **12 would have deleted the neighbour and opened a hole
   in the block.** Recorded in `pipeline/lib/landmarks.mjs` with the numbers.
3. **Roof duct runs collided with the fifth skylight** at the station the plan
   gave. Moved inboard to u −17.9, tight against the plant curb — scattered roof
   props read as noise from the app's camera (style bible §10).
4. **Glow shells need clearance.** The plan did not specify one. Coincident faces
   z-fight, and at the app's 12% day alpha that reads as a triangulated smear
   across the glass. Every glow shell is now inset in plan and lifted clear of
   the opaque surface behind it.

Two further build-side fixes, not plan errors: the paver-walk segments were
overlapping coplanar (now they butt), and three thin plates (`entry_reveal` at
0.03 m, the garage doors and rear door at 0.07 m) carried bevels wider than they
could take, clamping into 40 degenerate faces and 45 non-unit loop normals. The
"550" numerals are unbevelled for the same reason — the thinnest stroke is
0.10 m.

## Night state

The composition is a dark low bar with a lit lantern on it:

- **hero** — the penthouse pavilion glazing (`Toy_glassl_Glow`);
- **supporting** — the five skylights glowing from the office below, which is the
  only thing that identifies this building from the air after dark;
- **one ground cue** — the 3rd Street entry transom (`Toy_white_Glow`).

Nothing else lights. Every glow surface is a thin shell proud of the opaque
glazing behind it, never a primary surface.

## Deliberate omissions

The architect's roof axonometric shows two sculptural built-in bench forms
mid-roof. They were dropped: at city scale they compete with the skylight
rhythm, which is the identity, and §10 asks for clear clusters rather than
scattered props. Nothing tower-like, crowned or curved was added — the building's
charm is that it is long, low and quiet with one jewel on top.

## Review renders

All regenerated from the final export. `550-third-top.png` is the hero image for
this asset, because the roof is the facade.

| File | View |
|---|---|
| `550-third-top.png` | orthographic roof plan |
| `550-third-aerial.png` | high three-quarter, 80° azimuth, 40° down, 105 mm |
| `550-third-night.png` | same rig, dusk world, glow emission up |
| `550-third-{north,east,south,west}.png` | four elevations, one shared ortho rig |
| `550-third-contact-sheet.png` | all seven |

The aerial azimuth is deliberately 80° rather than the 44.6° front normal, so
the 3rd Street elevation and the SE party wall's property-line windows appear in
the same frame.

## Gate 3 — approval

Approved by David on 12 August 2026, quoted verbatim:

> "hey just checking in please proceed to finish the entire pipeline. i approve
> it all. dont wait for me"

This is a blanket approval covering stages 3–5; the ship decision (push, PR,
deploy) is still presented separately at the end of stage 5, as the pipeline
requires.

## Draft manifest entry

```json
{
  "id": "550-third",
  "file": "550-third.glb",
  "anchor": [
    -122.3953409,
    37.7804407
  ],
  "targetHeightM": 11.0,
  "cat": 3,
  "name": "550 Third Street",
  "estimated": true,
  "dims": [
    49.209,
    50.41,
    11.0
  ],
  "tris": 6244,
  "loadRadius": 2500
}
```

`"estimated": true` — deliberately. The footprint and the main roof are measured,
but the 11.0 m crest depends on a penthouse built after every height source that
exists for this parcel (see `REFERENCE.md` §8). The integration prompt says to
set this flag when the height is inferred rather than published, and it is.

`loadRadius` 2500 is the skill's default `max(2500, targetHeightM × 30)`. Beyond
that radius the site is empty ground, because the bake carves the footprint out —
at 2,500 m an 11 m building is illegible, so the absence costs nothing.

## Reproducing

```bash
BLENDER=/Applications/Blender.app/Contents/MacOS/Blender
"$BLENDER" -b --python build_550_third.py                       # .blend + .glb
"$BLENDER" -b --python validate_550_third.py                    # validation.json
"$BLENDER" -b --python render_550_third.py -- --only top        # and aerial / elev
"$BLENDER" -b --python render_550_third.py -- --night
python3 make_contact_sheet.py
```

`make_contact_sheet.py` uses Pillow rather than Blender's compositor: Blender 5.x
replaced `Scene.node_tree` with a compositing node group, and a photo montage is
not worth a version-sensitive dependency.
