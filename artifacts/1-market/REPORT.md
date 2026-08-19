# 1 Market Street (Southern Pacific Building) — build report

Stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, executed 19 August 2026
against `docs/asset-plans/1-market.md`. **This report beats the plan** wherever
they disagree; every correction is listed in §4.

## 1. Shipped numbers

| | |
|---|---|
| File | `1-market.glb` |
| Triangles | **21,292** (cap 28,000) |
| Objects | 733 closed solids |
| Dimensions | 112.208 x 112.098 x **48.700** m |
| bbox min / max | `[-56.105, -56.050, 0.000]` / `[56.104, 56.049, 48.700]` |
| min Z | **0.000** |
| XY centre offset | `[-0.0005, -0.0005]` m |
| Loader scale (`targetHeightM / measuredHeight`) | **1.000** |
| Materials | 12, all `Toy_*`, flat, opaque, no textures |
| Glow materials | `Toy_glassl_Glow`, `Toy_gold_Glow` |
| Raw / gzip size (pre-optimize) | 1,375.1 KB / 202.4 KB |
| Anchor | `-122.3948075, 37.7938412` |
| Target height | **48.70 m** (rooftop plant fan-bank cap) |

Heights as built: grade 0.00 → terra-cotta base 13.00 → base entablature and
balustrade 14.00 → eight brick storeys of 3.35 m → attic colonnade 40.80–44.10 →
roof deck 44.10 → cornice architrave 44.60 → corona 45.55 → **crowning cornice
crest 46.10** → plant enclosures 48.10 → plant cap 48.40 → **fan-bank crest
48.70**. Atrium glazing: eaves 35.20, apex 43.50.

Measured frontage headings, recorded from the built footprint: Market **315.2°**,
Steuart **45.2°**, Spear **225.2°**, the two Mission returns **135.2°**.

## 2. Validation — all PASS

`validate_1_market.py` factory-resets Blender, imports **only the exported GLB**
and reports on the re-import, never on the authoring scene. Full machine-readable
output in `validation.json`.

| Check | Result |
|---|---|
| Fresh isolated scene, re-imported final GLB | PASS |
| Triangle count 21,292 ≤ 28,000 | PASS |
| bbox top exactly 48.700 m → loader scale 1.000 | PASS |
| min Z 0.000, XY centre offset ≤ 0.0005 m | PASS |
| Image textures | 0 — PASS |
| Transparent materials | 0 — PASS |
| Material names all `Toy_*`, no `Toy_body` | PASS |
| `_Glow` suffix only on the two intended night materials | PASS |
| Cameras / lights / animations / armatures / constraints | 0 / 0 / 0 / 0 / 0 — PASS |
| Transforms applied, no negative scales | PASS |
| Normals: inverted-signed-volume objects | **0 of 733** — PASS |
| Normals: visibility-ray residual (gate ≤ 0.15%) | **0.00%** — PASS |
| Foreign / leaked geometry | none — PASS |

## 3. Renders

Regenerated from the exported GLB with Cycles on Metal GPU, `Standard` view
transform (AgX would eat the flat palette), 40 samples, denoised.

`1-market-aerial.png` (three-quarter on the Market x Steuart corner, 40° down),
`1-market-top.png`, `1-market-night.png`, and the four true elevations
`1-market-west.png` (Market), `1-market-north.png` (Steuart),
`1-market-east.png` (Mission / the open side of the court),
`1-market-south.png` (Spear), composed into `1-market-contact-sheet.png`.

**One fix to the review rig is worth carrying to other assets.** The night pass
inherited from `render_300_brannan.py` turned `Emission Strength` up on every
`_Glow` material. After a glTF round-trip those materials come back with
**`Emission Color` = white** — the emissive colour is not carried, because the
build exports at strength 0 — so the rig was rendering *every* glow surface
blown-out white and telling us nothing about what the app will draw. The app
draws `_Glow` in a separate **unlit** layer, i.e. at the material's own base
colour. `light_glow()` now copies base colour → emission and uses strength 1.0,
so the night render is what the app will show. It changed the review verdict
here: the atrium reads as a cool pale-blue lantern (112, 152, 189), not white.

## 4. Corrections to the plan

1. **Bounding box.** The plan predicted ~107.1 x 107.0 m from the wall ring. The
   export is **112.21 x 112.10 m**, because the crowning cornice projects 1.85 m
   and the base band 0.34 m beyond the wall plane on a 45°-rotated footprint.
   Expected, not a scale error — but the plan's number was the wall ring's, not
   the asset's.
2. **Storey split.** The plan's massing table gave the shaft 8 storeys of 3.55 m
   to 42.40 m and the attic only 2.20 m. Built as **8 x 3.35 m to 40.80 m** with a
   **3.30 m attic colonnade**, because at the plan's proportions the colonnade
   rendered as a dentil strip rather than the storey it is. Eleven storeys and the
   46.10 m crest are unchanged.
3. **Atrium glazing.** Plan: eaves 33.0, apex 43.0. Built: **eaves 35.20, apex
   43.50** — at the plan's eaves the glazed hip read as a swimming pool from the
   aerial camera rather than a roof.
4. **The atrium night glow is a shell, not a plate under the glazing.** The plan
   specified "a `_Glow` plane *under* the glazing, not a shell". That is
   unbuildable here: the glazing is opaque, so a plate beneath it is invisible —
   the first night render had a completely dark atrium. It is now a thin closed
   shell 0.12 m proud of the glass. A closed shell stacks two alpha layers and
   reads ~23% by day, so its colour is set to the glazing's own `Toy_glassl`
   value: by day the overlay is invisible, at night the hip becomes the lantern.
5. **The portal had to stand proud of its own surround.** Built first as a dark
   arch recessed behind a solid cream surround plate, which swallowed it
   completely — the applied-panel recess trap. The dark arch now sits 0.06 m in
   front of the surround and reads as a deep opening.
6. **Mullions carry no bevel.** They are 0.95 m hairline strips; beveling all 165
   of them cost 5,280 triangles and changed nothing visible. The plan's budget
   assumed they would be beveled.
7. **`Toy_slate` for the roof deck, not `Toy_roofd`.** `Toy_roofd` renders
   near-black on a large horizontal surface in the app; it is used here only on
   small vents.

## 5. Style-bible compliance

- Base / shaft / crown reads at a glance from the high three-quarter aerial.
- Semantic exaggeration spent in one place: the cornice projects 1.85 m against a
  surveyed ~1.15 m, ~+60%, because the silhouette is the building.
- Every roof surface designed: parapet ring, plant enclosures with fan discs,
  bulkheads, ducts, vents, walkways, and the glazed atrium hip in the court.
- Night state is one hero (the atrium) and two supports (the arcade band and the
  portal, warm; a sparse scatter of lit bays, cool). Roughly one bay in six is lit
  and no floor reads as a band. The cornice is not lit.
- No booleans anywhere: every opening is an applied plate standing proud of a
  solid wall.

## 6. Stage 3 — approval

Presented to the user on 19 August 2026 with the contact sheet, the aerial day and
night renders and the numbers above.

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION" — David, 19 August 2026,
> standing approval given with the pipeline invocation.

Taken as approval to advance to stage 4 (optimize) and stage 5 (integrate, batch
mode).

## 7. Draft manifest entry

```json
{
  "id": "1-market",
  "file": "1-market.glb",
  "anchor": [
    -122.3948075,
    37.7938412
  ],
  "targetHeightM": 48.7,
  "cat": 3,
  "name": "1 Market Street (Southern Pacific Building)",
  "estimated": false,
  "dims": [
    112.2081,
    112.0981,
    48.7
  ],
  "tris": 21292,
  "loadRadius": 2500
}
```

`dims` and `tris` are the pre-optimize figures and are re-stated after stage 4.
