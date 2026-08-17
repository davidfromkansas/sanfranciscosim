# 340 Brannan Street — build report

Miniature GLB for the SF toy-diorama city, built from
`docs/asset-plans/340-brannan.md` under
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`. **REPORT beats plan**: where this
document and the plan disagree, this document is what shipped.

## Shipped numbers

| | |
|---|---|
| File | `340-brannan.glb` |
| Objects | 176 |
| Triangles | **8,880** (cap 11,000) |
| Dimensions (AABB) | 41.05 x 40.68 x **17.79** m |
| Min Z | 0.000 m |
| XY centre offset | (-0.015, -0.119) m |
| File size | 557 KB raw / 99 KB gzip (pre-optimize) |
| Materials | 13, all `Toy_*`, flat, no textures, no alpha, no `Toy_body` |
| Glow materials | `Toy_glass_Glow`, `Toy_white_Glow` |
| Anchor (WGS84) | -122.3932324, 37.7812786 |
| Brannan front heading | 135.4° true (SE) |
| Contract validation | **PASS** — all 16 checks, fresh re-import (`validation.json`) |

The 41 x 41 m axis-aligned bounding box on a 29.25 x 28.22 m building is the
expected consequence of the ~45° SoMa heading, not a scale error.

## What was built

A four-window-line sage stucco slab on the northeast corner of Brannan Street
and Jack London Alley:

- the measured DataSF LiDAR footprint reduced to its four real corners;
- a 4.60 m recessed ground floor under a continuous light fascia, with a dark
  bronze storefront in two horizontal glass strips, the recessed lobby entrance
  with its flat canopy and dark pier, and the white **"340"** numerals;
- three floors of wide horizontal punched windows, five bays per finished
  elevation, one horizontal division each, over a blank frieze;
- the **raised central parapet with chamfered shoulders** on the Brannan front —
  the building's silhouette signature;
- two blind party walls (northeast, northwest), left flat and left to show,
  because this building stands 3–7 m proud of both its neighbours;
- a designed roof: penthouse (which sets the 17.79 m crest), open trellis over
  the atrium, two cooling towers on a plinth, the permitted timber roof deck,
  two skylights, a hatch and two vents;
- night state: the lit lobby band as hero glow, the "340" sign panel, and six lit
  windows scattered across the two finished elevations.

## Dossier corrections made during the build

The plan's dimensions were explicitly a starting point. Five things changed:

1. **Footprint reduced from 11 vertices to 4.** The plan's §2.3 originally
   described a "clipped north corner" and a 3.91 m step. Measuring every survey
   vertex against the simple quadrilateral showed a maximum deviation of
   **0.115 m** — the extra points are survey noise, not corners. The plan was
   corrected before this build (area 821.7 → 821.0 m2, alley edge 27.07 →
   28.22 m, alley bearing 225.3 → 225.2°, NE bearing 44.3 → 44.5°).
2. **Floor heights changed from 3 x 3.40 m to 3 x 3.20 m plus a 0.62 m frieze.**
   The plan's arithmetic (4.60 + 3 x 3.40 = 14.80) landed the top window head at
   14.65 m against a 14.82 m deck — 17 cm of wall. Every photograph shows a clear
   band of wall between the top window head and the roofline, and without it the
   top row ran straight into the coping. Window bands are now 5.80–7.65,
   9.00–10.85 and 12.20–14.05.
3. **Raised parapet built as a course ON the coping, not as a band applied to the
   wall, and raised 0.90 m rather than 0.65 m.** Two failures got it there. Flush
   with the wall it disappeared behind the coping (which projects 0.07 m and runs
   the whole perimeter) in every head-on view. Standing it proud but taking its
   inner face deeper than the coping's left a 50 mm slot between them that
   ambient-occludes to pure black and read from the aerial camera as **a painted
   stripe across the roof**. Stacking it clear of the coping, 0.02 m proud on each
   side, gives the street silhouette with no seam and nothing on the roof.
4. **Entrance pier is `Toy_rust` (`a86444`), not `Toy_brick` (`c96f4a`).** The
   palette brick is a bright terracotta and at 4.6 m tall it shouted over the
   whole facade; the real pier is a dark reddish-brown. `Toy_brick` is not used
   in this asset at all.
5. **The lobby glow was cut from one 16 m band to three 3.4 m bays** (and the
   alley's two from 5.2 m to 3.0 m). A `_Glow` shell renders at ~12% alpha per
   layer by **day**, so a band across the whole base read as milk in daylight.
   Short bays give the same night read at a third of the day cost.

Two plan values were also carried forward unchanged and are worth restating
because they are the ones most likely to be "corrected" by a later reader:

- **Four window lines, not five storeys.** The assessor roll, the National
  Register form and every commercial listing say five storeys; the permit record
  splits 4/5 across the 1982–89 applications; photography from three Street View
  positions shows a tall recessed ground floor plus three upper window lines. The
  measured 14.82 m deck only supports four. Built as photographed.
- **Stucco, not brick.** Page & Turnbull's National Register building data form
  for block/lot 3775/015 records exterior material **Stucco** over reinforced
  concrete, and classes the building **non-contributory** to the South End
  Historic District ("appears extensively altered from original appearance"). The
  brick-warehouse literature that surrounds this lot is not evidence about it.

## Palette extensions (WARN, not FAIL)

Two colours are outside the `sf-asset-check` palette. Precedent:
`380-brannan`'s `Toy_slate`, `140-south-park`'s `Toy_olive`,
`155-south-park`'s `Toy_peach`.

| Material | Hex | Why not a palette entry |
|---|---|---|
| `Toy_sage` | `8d9082` | The body colour, and the whole point of this asset on this block. `Toy_steel` (`9aa0a6`) is a blue-gray and kills the green; `Toy_verdigris` (`9fb8a8`) is far too mint; `Toy_olive` (`5f655c`) is the right hue but far too dark for a 15 m street wall. |
| `Toy_bronze` | `5a4a3a` | The dark anodized storefront. `Toy_ink` (`3a3530`) reads black and flattens the entrance against the recess behind it; `Toy_roofd` (`45454a`) is a cool gray. |

Both are offered for a palette review to fold in or reject.

## Validation

`validation.json` is written from a **fresh factory-reset scene containing only
the exported GLB** — never the authoring `.blend`. All checks PASS:

meters and plausible dimensions · crest normalized to 17.79 · base at z=0 ·
centered in XY · under triangle budget · no image textures · no transparency ·
materials follow contract · no cameras or lights · no animation/skin/constraints ·
transforms applied · no negative scales · normals outward (per-object signed
volume) · normals outward (31,500-ray residual within tolerance) ·
no degenerate geometry · no unexpected objects

## Files

```
build_340_brannan.py        deterministic build (Blender 5.2 LTS, headless)
render_340_brannan.py       controlled review rig, renders the EXPORTED GLB
validate_340_brannan.py     fresh-scene contract validation
make_contact_sheet.py       composes the contact sheet
340-brannan.blend           authoring scene
340-brannan.glb             the asset
340-brannan-{north,east,south,west,top,aerial}.png
340-brannan-aerial-night.png
340-brannan-contact-sheet.png
validation.json
REFERENCE.md                research dossier and sources
```

Reproduce with:

```
blender -b --python build_340_brannan.py
blender -b --python render_340_brannan.py
blender -b --python render_340_brannan.py -- --night
blender -b --python validate_340_brannan.py
python3 make_contact_sheet.py
```

## Draft manifest entry

```json
{
  "id": "340-brannan",
  "file": "340-brannan.glb",
  "anchor": [
    -122.3932324,
    37.7812786
  ],
  "targetHeightM": 17.79,
  "cat": 3,
  "name": "340 Brannan Street",
  "estimated": false,
  "dims": [
    41.05,
    40.68,
    17.79
  ],
  "tris": 8880,
  "loadRadius": 2500
}
```

`dims` and `tris` are the pre-optimize figures and are updated by stage 4.

## Approval

_Stage 3 (APPROVE) — awaiting the user's verbatim decision._
