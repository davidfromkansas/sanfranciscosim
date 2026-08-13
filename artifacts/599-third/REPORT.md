# 599 Third Street — build report

Built 12 August 2026 by the `docs/asset-pipeline/ADDRESS-TO-ASSET.md` pipeline
(`BUILDING: 599 3rd St, San Francisco, CA 94107`, `BATCH: yes`) on branch
`pipeline/599-third`. Plan: `docs/asset-plans/599-third.md`. Sources and
observations: `REFERENCE.md`.

**This report beats the plan wherever they disagree.** Three dossier corrections
were made before modelling and are recorded in §1.

## 0. Headline

| | |
|---|---|
| Asset | `artifacts/599-third/599-third.glb` (post-optimize; pre-optimize original archived at `optimize/input/`) |
| File size | **240,704 bytes** raw, meshopt-compressed (was 658,108 as authored) |
| Objects / triangles | **12** / **9,384** (cap 15,000; contract ceiling 27,000) — 376 objects as authored, joined per material by stage 4 |
| Dimensions (x, y, z) | 43.151 × 42.853 × **18.300** m |
| min Z / max Z | 0.000 / 18.300 |
| Loader scale factor | **1.000000** (`targetHeightM` 18.3 ÷ measured 18.3) |
| XY centre offset | (−0.002, −0.009) m |
| Materials | 12, all `Toy_*`; 3 `_Glow` |
| Anchor | −122.3942739, 37.7804504 |
| Long axis / entry normal | 44.8° / 224.8° true |
| Validator | **PASS** — all 15 checks |

## 1. Dossier corrections (REPORT beats plan)

**Correction 1 — the café is not on the corner.** The plan placed the
ground-floor café at the 3rd/Brannan corner. The OSM node for Golden Goat Coffee
(node/13765490836) projects onto the 3rd Street frontage at **s ≈ 2.2 m from the
north-west corner**, i.e. the far end of the address face from Brannan. The 2017
DBI permit describes converting the *existing garage*, and a garage door at that
end of the lot is consistent. The shopfront and its coral awning were moved to
the ground floor of 3rd Street bay A. Confidence: the OSM node is a POI centroid,
not a surveyed door, so the *end of the building* is well established but the
exact metre is not.

**Correction 2 — the north-west elevation is not a party wall.** The plan called
it blind. OSM shows a Shell filling station immediately north-west: way/124889473
(`height=4`, one level — the forecourt canopy) 23 m from the anchor on bearing
314°, with the station building at 551 3rd Street 44 m out. That elevation
therefore looks across an open forecourt and is visible from 3rd Street. It was
modelled with a reduced but real rhythm — small square punched windows at each of
the three loft levels — instead of blank stucco.

**Correction 3 — the building is residential, not office.** Initial scoping read
commercial listings ("6,400 sf, built 2001, office for lease") as describing the
building. DataSF parcels show map lot 3775140 subdivided into **24 condominium
lots** (3775140–3775163), and every DBI permit from 1999 to 2022 records
`artist live/work` use in a 4-storey Type V wood frame. The listings describe
single lofts. Manifest category corrected from `3` (Office) to **`2`
(Apartments)**, and the night state was redesigned from an even office grid to an
irregular lit-loft scatter.

## 2. Height decision

| Figure | Value | Source |
|---|---|---|
| LiDAR height median | 15.62 m | DataSF `ynuv-fyni`, `SF3775140` |
| LiDAR height mean | 15.81 m | same |
| OSM `height` tag | 16 m | way/124890326 (Bing) |
| **Modelled parapet** | **16.00 m** | the two above agree independently |
| LiDAR height max | 18.34 m | same record, `hgt_maxcm` |
| **Modelled crest / `targetHeightM`** | **18.30 m** | penthouse top |

Unusually for this set, the OSM `height` tag is *right*: it describes the parapet,
not a low shell, and the LiDAR median corroborates it. The open question is the
other end. `hgt_max` is the highest first return anywhere on the footprint, so a
mast, an aerial or a parapet corner would produce 18.34 m just as readily as the
stair/elevator penthouse. **This is the asset's single largest open risk.** It is
contained: if the crest moves, only `targetHeightM` and the top of the
`penthouse` volume move with it — the shell, the parapet and every facade datum
are measured independently.

`"estimated": false` in the manifest entry, because both numbers are measured
rather than inferred; the caveat above is about which feature the maximum
describes, not about whether it was measured.

## 3. Orientation

Authored with Blender `+Y` = true north, `+X` = east. `placeGeneric()` in
`app/src/assets.js` scales and positions but never rotates, so the model must
carry its real heading. The contract's "front faces −Y" **cannot be honoured**:
the entry faces south-west (outward normal 224.8° true). Real-world orientation
wins per `AGENTS.md` rule 5 and the orientation note in
`docs/asset-plans/README.md`. No `yawDeg` override is needed.

## 4. Build iterations

| # | Finding | Fix |
|---|---|---|
| 1 | First aerial: `penthouse_cap` was authored as a full-plan `ink` box, so from the app's downward camera the penthouse read as a **black rectangle punched into the roof** — the exact failure the style bible's §10 "roofs are facades" rule exists to catch | Replaced with four thin coping bars around the top edge; the penthouse top is now `Toy_trim` |
| 2 | The chevron brace was five stacked axis-aligned boxes per arm and read as a staircase of blocks, not structure | Added a `facade_prism()` helper that extrudes an arbitrary (s, z) profile along the wall normal; the brace is now two clean angled members, over-thickened per style bible §9 |
| 3 | The 599 numerals were too small to register | 0.75 m → 0.95 m, depth 0.10 → 0.12 |
| 4 | Validator FAIL: **105 degenerate triangles** in `parapet_cap` (36) and `deck_0..2` (69), plus one non-unit loop normal on `deck_0` — all from 0.10 m slabs carrying a 0.05 m bevel on each face, which `clamp_overlap` collapsed to zero area | Parapet coping 0.14 m at 0.04 bevel (crest still lands exactly on 16.00 by lowering `H_PAR` to 15.86); deck pads 0.16 m at 0.04 bevel |
| 5 | Second aerial: the chevron's two arms stopped 0.32 m short of each other and read as loose sticks | Arms cross 0.12 m past the centreline; overlapping solids are fine in a union of closed solids |
| 6 | First night render: **every glow surface rendered pure white**, skylights included. The rig (inherited from `550-third`) raised `Emission Strength` on the re-imported GLB, but glTF writes `emissiveFactor = 0` when authored strength is 0, so each `_Glow` material carries a **default white** emission colour — the exact trap documented at the foot of `docs/asset-plans/README.md`, which bit `chase-center` first | `light_glow()` now copies Base Color into Emission Color at strength 1.0, matching the README and `tools/glb-optimize/render_ab.py` |
| 7 | **Asset bug the white render was masking:** lit loft windows were authored `Toy_glass_Glow` `#2a4d73`. The app draws `_Glow` as an *unlit overlay at the material's own baked colour*, so in production those "lit" windows would have rendered **darker than the unlit ones beside them** | Lit lofts are now `Toy_mustard_Glow` `#d9a441`. Warm domestic light also reads as residential and separates this building from the city's cool commercial glows |

## 5. Validation

`validation.json`, produced by re-importing the **exported** GLB into a fresh
isolated Blender 5.2.0 scene (never the authoring scene).

| Check | Result |
|---|---|
| `meters_and_plausible_dimensions` | PASS |
| `base_at_z_zero` | PASS (min Z 0.000) |
| `crest_is_target_height` | PASS (max Z 18.300) |
| `centered_xy` | PASS (−0.002, −0.009) |
| `under_triangle_budget` | PASS (9,384 / 15,000) |
| `no_image_textures` | PASS |
| `no_transparency` | PASS |
| `materials_follow_contract` | PASS (12 `Toy_*`, no `Toy_body`) |
| `no_cameras_or_lights` | PASS |
| `no_animation_skin_or_constraints` | PASS |
| `transforms_applied` | PASS |
| `no_negative_scales` | PASS |
| `normals_outward` | PASS |
| `no_degenerate_geometry` | PASS (0) |
| `no_unexpected_objects` | PASS |
| **overall** | **PASS** |

Re-run against the **shipped** (post-optimize) GLB: still PASS on all 15, now at
12 objects instead of 376. Stage 4 details: `optimize/REPORT.md`.

Normals were checked two ways, as the pipeline requires: per-object signed volume
(authoritative for a union of closed solids) gave **zero inverted objects**, and
the deterministic visibility-ray test fired 31,500 rays from nine interior
targets for a residual of **0.000000** against a 0.15 % gate.

## 6. Night state

Residential, so a scatter rather than a display:

- `Toy_mustard_Glow` (`#d9a441`, warm) on **14 of 38** loft window units in an irregular pattern
  (`LIT_THIRD` / `LIT_BRANNAN` in the build script) — the hero;
- `Toy_glassl_Glow` on all nine roof skylights — the aerial identity;
- `Toy_trim_Glow` on the entry doors and the café shopfront — two ground cues.

Glow **colour** matters as much as placement: because the night layer is unlit and
drawn at the material's own baked colour, a glow colour darker than the surface
beneath it inverts the effect. Every glow here is lighter than its host surface.
Every glow surface is also a thin shell lifted clear of the opaque glazing behind
it; none is a primary surface. The app draws `_Glow` in a separate unlit layer at
`0.12 + 0.95 × uNight` alpha, so a primary surface authored as glow would wash
out by day and coincident faces would z-fight into a triangulated smear.

## 7. Approval (gate 3)

Approval was given in advance for the whole run, verbatim on **12 August 2026**:

> "Yes confirm -- proceed fully. no need to ask for approval"

Recorded per the pipeline's requirement that gate 3 be an explicit approval
quoted verbatim with its date. No renders were presented for sign-off before
stage 4 as a result; the review renders in this folder are the record.

## 8. Manifest entry (for integration, not applied here)

```json
{
  "id": "599-third",
  "file": "599-third.glb",
  "anchor": [
    -122.3942739,
    37.7804504
  ],
  "targetHeightM": 18.3,
  "cat": 2,
  "name": "599 Third Street",
  "estimated": false,
  "dims": [
    43.151,
    42.853,
    18.3
  ],
  "tris": 9384,
  "loadRadius": 2500
}
```

`loadRadius` is the skill default `max(2500, 18.3 × 30)` = 2500. At 18.3 m the
building is illegible long before 2,500 m, so the hole left beyond the radius by
the Case B exclusion costs nothing visually.

Registry id for `pipeline/lib/landmarks.mjs` is `599Third` (the `camelId()` round
trip from `599-third`). Exclusion radius must be measured against bake-side
geometry at integration time — see `docs/asset-plans/599-third.md` §2.13; all
four of this footprint's own vertices sit at 21.78–21.92 m from the anchor, so
the radius has to clear ~21.9 m without taking the neighbours.

## 9. Files

| File | What it is |
|---|---|
| `build_599_third.py` | deterministic headless Blender build |
| `599-third.blend` / `599-third.glb` | authoring scene / shipping asset |
| `render_599_third.py` | review rig; always renders the **exported** GLB |
| `validate_599_third.py` | fresh-scene re-import contract validator |
| `make_contact_sheet.py` | review montage |
| `599-third-{top,north,east,south,west,aerial,night}.png` | review renders |
| `599-third-contact-sheet.png` | the review sheet |
| `REFERENCE.md` / `validation.json` | dossier / validator output |
