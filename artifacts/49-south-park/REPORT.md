# 45–49 South Park (Gran Oriente Filipino Residence) — build report

**Asset:** `artifacts/49-south-park/49-south-park.glb` — a miniature of the 1909
Edwardian flats building on the corner of South Park and Jack London Alley, half of the
Gran Oriente Filipino landmark complex whose other half is already in the manifest as
`106-south-park`.

Research: `REFERENCE.md`. Plan: `docs/asset-plans/49-south-park.md`. Where this report
and the plan disagree, **this report is the record** — the plan was written before the
model existed.

## Numbers

| | |
|---|---|
| Triangles | **9,262** (cap 11,000) |
| Objects | **12** mesh after the stage-4 join (165 as authored), 0 anything else |
| Dimensions | 23.6255 × 22.5585 × **13.0000** m |
| Wall box | 12.90 m (South Park front) × 17.70 m deep |
| min Z / XY centre offset | 0.000 m / (0.000, 0.000) |
| File (shipped, post-stage-4) | **219,356 B** raw, 141,289 B gzip — from 537,592 B raw |
| Materials | 11, all `Toy_*`, flat, opaque, no textures |
| Glow | `Toy_glass_Glow`, `Toy_trim_Glow` — 90 faces, all open single-layer strips |
| Front heading | 315.8° (NW) · flank 225.8° (SW) · party 45.8° · rear 135.8° |
| Manifest anchor | `-122.3935929, 37.7814646` |
| Target height | 13.00 m → loader scale exactly **1.0** |
| Validation | **PASS**, all 17 checks — `validation.json` (re-run against the shipped, optimized file) |
| Stage 4 | −59.2% raw, 167 → 14 draw submeshes, all 8 gates PASS — `optimize/REPORT.md` |

The 23.63 × 22.56 m XY box is the 45.8° rotation of a 12.90 × 17.70 m building plus its
bays. It is not a 23 m building.

Every review render, the contact sheet and `validation.json` were regenerated from the
**shipped** file after the stage-4 swap, so nothing in this directory depicts a build
that is not the one being integrated. The pre-optimize asset is archived byte-for-byte
at `optimize/input/49-south-park.glb`.

## Corrections to the dossier, made during the build

Five, all documented in the build script at the point of change.

**1. The body colour is off-palette, and that was a deliberate reversal.** The plan
specified `Toy_stone` (`#d9d2c2`) for the body against `Toy_trim` (`#f3efe6`) for the
cornice, frames and rosettes. Built that way and rendered, the two read as *the same
cream*: the body disappeared into its own trim and the seven bays — the entire point of
this building — stopped reading as projections at all. The value step the elevation
depends on simply is not there between those two palette entries.

The body is now **`Toy_sage` `#b5b4a2`**, which is off-palette (a WARN, not a fail) and
is defended on three grounds: the style bible's explicit SF exception for painted
residential facades; the palette having no pale sage at all; and the 2017 photographs
showing a body that is clearly a step darker than its trim and faintly green. The three
value relations the dossier is confident about — pale body, lighter trim, much darker
basement, thin red line at the joint — all survive.

Two related choices held: the body is deliberately **not** `Toy_cream`, because
`106-south-park` is `Toy_cream` and stands 90 m away on the same oval under the same
owner, and two near-whites merge from the air; and the roof deck stayed `Toy_steel`
(`#9aa0a6`), which is what makes the cream cornice ring read from directly above.

**2. The bays were shrunk and the cornice projection cut, because they are coupled.**
The cornice follows the *bay outline* — one polygon with every bay spliced into it —
so its outward offset has to fit inside the flat gap between two neighbouring bays. At
the plan's 3.40 m rounded and 3.00 m canted bays, the front's three gaps came out
between 0.15 m and 1.00 m, and the plan's 0.55 m cornice folded through itself in them.
The first renders showed black wedges wherever that happened.

Bays are now 3.10 m rounded and 2.60 m canted, and the cornice steps are 0.12 / 0.24 /
0.38 m. Every gap on the front is now 0.83 m, wider than two 0.38 m offsets meeting.
Bay centres moved with them (front 4.23 / 7.66 / 11.34; flank 5.83 / 10.86 / 16.15).

That alone was not enough. Two more guards went in:

- `inset_polygon()` now **caps the vertex displacement at 1.3× the offset**. Without it,
  a reflex vertex sends the two offset lines to an intersection far away and the result
  is a long sail.
- The cornice runs on a `relax_polygon()`-chamfered copy of the outline, which replaces
  every reflex vertex with a short chamfer. Every junction where a bay meets the wall is
  reflex; the turret's two are the worst, because it wraps a 90° corner and comes back
  into both walls steeply. With the chamfer, the offset has somewhere to go.

The turret crown was rebuilt the same way in spirit: it is now two calls to
`turret_arc()` at smaller `attach`/`reach`, never an offset of the turret polygon.
Offsetting *that* polygon — which closes back on the corner point through two wall-line
edges — sails in either direction.

**3. The bays now run to the roof deck, not to the third-storey ceiling.** Stopping the
bay solids at 11.20 m left an open well between each bay and the cornice above it, which
from directly above read as a dark hole punched through every bulge in the ring. They
now run to 12.05 m.

**4. The flank carries two canted bays, not three.** The plan left this open. Re-reading
the 2017 corner photograph, the alley elevation reads as turret / canted / canted /
rounded over 17.70 m, with real flat wall between — so two it is. The *rounded* count,
three, one per exposed corner, is from the designation report and was never in doubt.

**5. The offset helpers were deciding "outward" the wrong way, and stage 4 caught it.**
Not a visual defect — a contract one. `inset_polygon()` and the polyline offset used by
the bay glazing bands worked out which side of each edge was outward by comparing it to
the *building centroid*. That is fine for a rectangle. It is wrong for a corner turret
that sweeps 242°, and wrong for a rounded bay sitting near a far corner, because some of
their segments genuinely face back past the centroid — so those segments offset inward,
their bands folded through themselves, and the folded faces read as flipped to a ray
test. The stage-4 gate measured 0.202% flipped first hits against a 0.15% tolerance and
refused the pass.

Both helpers now decide handedness once and geometrically: `inset_polygon()` from the
polygon's own **winding**, and the open-polyline offset from its **middle segment**,
which on a convex arc always faces squarely out. The glow strips use the same rule. The
input then measured 2 flipped hits in 17,325 (0.012%), and the shipped file 1.

Two things were fixed alongside it. Every applied band — bay glazing, bay frames,
cornice steps, water table, window sills, roof furniture — is now sunk 30 mm into the
surface it sits on (`EMBED`), because a face exactly coincident with another solid's
face makes a ray's first hit ambiguous; overlapping solids are the supported model here.
And this file's own `glow_strips_face_outward` check was rewritten: it used to dot each
glow face against the model centre, which is the *same* mistake, and it now casts a ray
inward along each face's own normal and requires that face to be the first thing hit.

## Design decisions worth recording

- **The corner turret is modelled as wrapping the corner**, centred on the West corner
  and swung onto the corner bisector (270.8°), sweeping ~242° on an 8-segment arc. This
  is a reading of the photographs, not a certainty — see REFERENCE.md §6.4 — but it is
  much the strongest reading for a miniature and it gives the model its silhouette.
- **The quatrefoil rosettes are exaggerated to 1.30 m** from a real ~0.90 m. This is the
  only semantic exaggeration in the asset. At 12.90 m of frontage the real thing is a
  couple of pixels from the app's camera, and it is the ground floor's whole identity.
- **The roof is furnished, deliberately.** Two brick chimney stacks (12.88 and 12.80 m),
  a stair bulkhead, two skylights, a hatch, a curb and five vent stacks. A 1909
  wood-frame flats building has chimneys, the 2017 corner photograph shows white vent
  pipes clustered at the park end, and a bare 12 × 18 m deck under this app's camera is
  the one thing the style bible will not forgive. Everything is capped at 12.90 m so the
  turret crown at 13.00 m stays the tallest geometry and the loader's height
  normalization cannot pick a chimney.
- **Night glow is open single-layer strips, never closed shells.** The app draws `_Glow`
  in a separate translucent layer; a closed box presents its front *and* its back face
  and reads at roughly twice the intended day alpha, which is enough to tint a whole
  facade. `glow_band()` emits one row of one-sided quads with the winding set explicitly
  and never recalculated. The validator checks these with an outward-normal test rather
  than the signed-volume test, which does not apply to an open surface: 90 faces, 90
  facing outward.
- Lit at night: the turret on both storeys (hero), then an uneven scatter — this is
  seven apartments, not an office floor, and an even grid reads institutional. Plus a
  warm spill in the two entrance recesses.
- **The Masonic Temple is not in this asset.** 95 Jack London Alley stands on the same
  lot, ~6 m to the south-east, and is a separate address, a separate 1951 building and a
  separate footprint in the bake. It stays procedural, and the integration exclusion is
  sized to leave it standing — see the plan's 2.13.
- Bevel is 0.10 m / 2 segments on the chunky masses only. The cornice, the bracket run,
  the rosette lobes, the columns and the basement openings are left sharp: beveling the
  cornice alone cost 2,800 triangles and looked identical from the app's camera, because
  three corbelled steps read as chunky whether or not their arrises are rounded.

## Contract deviations

- **The contract's "front faces −Y" rule is not honoured**, and cannot be. The building
  stands at 45.8° to the world axes and AGENTS rule 5 requires real-world placement, so
  the model is authored in world space at its true heading: the South Park front faces
  **315.8°**. This is the case `docs/asset-plans/README.md` calls out.
- **`Toy_sage` `#b5b4a2` is off-palette.** WARN, not a fail; reasoning in correction 1.

## Validation

Fresh factory-reset scene, GLB re-imported, source `.blend` never inspected.
`validate_49_south_park.py` → `validation.json`, **overall PASS**, every check true:

meters and plausible dimensions · crest normalized to target (13.000) · base at z=0 ·
centred in XY · under triangle budget (9,262 / 11,000) · no image textures · no
transparency · materials follow contract · no cameras or lights · no animation, skin or
constraints · transforms applied · no negative scales · normals outward by signed volume
(0 inverted) · glow strips face outward (90 / 90, each one the first thing a ray fired
back along its own normal hits) · normals outward by ray test (31,500 rays, 4 flipped
first hits = 0.0127%, tolerance 0.15%) · no degenerate geometry · no unexpected objects.

## Files

```
build_49_south_park.py        deterministic build      -> .blend + .glb
render_49_south_park.py       controlled review renders (re-imports the GLB)
make_contact_sheet.py         composes the contact sheet
validate_49_south_park.py     fresh-scene contract validation -> validation.json
49-south-park.blend           authoring scene
49-south-park.glb             THE ASSET
49-south-park-{north,south,east,west}.png   four elevations, one rig
49-south-park-facade.png      square-on long lens at the 315.8 deg park front
49-south-park-top.png         the cornice ring and its seven bulges
49-south-park-aerial.png      high three-quarter over the West corner
49-south-park-aerial-night.png
49-south-park-contact-sheet.png
REFERENCE.md                  research dossier
validation.json               machine-readable validation (of the SHIPPED file)
optimize/                     stage-4 shrink pass: byte-identical input archive,
                              adapted scripts, gate results, A/B renders, REPORT.md
```

## Draft manifest entry

```json
{
  "id": "49-south-park",
  "file": "49-south-park.glb",
  "anchor": [
    -122.3935929,
    37.7814646
  ],
  "targetHeightM": 13.0,
  "cat": 2,
  "name": "Gran Oriente Filipino Residence (45–49 South Park)",
  "estimated": false,
  "dims": [
    23.6255,
    22.5585,
    13.0
  ],
  "tris": 9262,
  "loadRadius": 2500
}
```

## Approval (stage 3)

Presented: contact sheet, aerial day and night renders, and the numbers above.

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"
> — David, 16 August 2026, standing approval given with the pipeline invocation

Recorded verbatim per `docs/asset-pipeline/ADDRESS-TO-ASSET.md` gate 3. No revision
rounds were requested after presentation; the four corrections above were made by the
build session itself before presenting, in response to its own review renders.
