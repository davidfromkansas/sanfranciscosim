# 590 Third Street — build report

Built 13 August 2026 by the `docs/asset-pipeline/ADDRESS-TO-ASSET.md` pipeline
(`BUILDING: 590 3rd St, San Francisco, CA 94107`, `BATCH: yes`) on branch
`pipeline/590-third`. Plan: `docs/asset-plans/590-third.md`. Sources and
observations: `REFERENCE.md`.

**This report beats the plan wherever they disagree.** Six build corrections were
made and are recorded in §1 and §4.

## 0. Headline (shipped, post-optimize)

| | |
|---|---|
| Asset | `artifacts/590-third/590-third.glb` (post-optimize; pre-optimize original archived at `optimize/input/`) |
| File size | **143,672 bytes** raw, meshopt-compressed (was 310,156 as authored) |
| Objects / triangles | **12** / **5,312** (cap 11,000; contract ceiling 27,000) — 92 objects as authored, joined per material by stage 4 |
| Dimensions (x, y, z) | 31.913 × 31.531 × **9.500** m |
| min Z / max Z | 0.000 / 9.500 |
| Loader scale factor | **1.000000** (`targetHeightM` 9.5 ÷ measured 9.5) |
| XY centre offset | (+0.151, −0.000) m |
| Materials | 11, all `Toy_*`; 3 `_Glow` |
| Anchor | −122.3946749, 37.7800837 |
| 3rd Street front normal / Brannan front normal | 45.2° / 135.1° true |
| Draw submeshes | **14** (94 as authored) |
| Validator | **PASS** — all 15 checks on the SHIPPED file, ray residual 0.000000 |

## 1. Dossier verification and corrections (REPORT beats plan)

The plan's dossier was re-verified against its own sources before modelling.
Footprint, anchor, orientation, LiDAR heights and the light well all held. Two
substantive corrections and four modelling corrections were made.

**Correction 1 — the footprint is the parcel, not OSM.** The plan already said
this; it is restated because it is the single decision that most affects
placement. OSM way/124903637 is a Bing trace: 478 m² with a 0.6 m jog on the NW
edge that no other source shows. The DataSF parcel polygon (491.5 m²) agrees with
the assessor's 5,318 sf lot to +0.5% and with the LiDAR footprint (489 m²) to
−0.5%. The asset is built from the parcel: a clean parallelogram, 21.28 m along
3rd × 23.10 m along Brannan.

**Correction 2 — the 11.65 m LiDAR maximum is the neighbour, and no penthouse
was modelled for it.** See §2.

**Correction 3 — the shopfront fascia had to stand proud, and the awnings had to
shrink.** The plan's §2.7 put the fascia flush at 0.12 m and gave the awnings
0.8 m of depth. Built that way, the first aerial review render showed the awnings
covering the fascia completely from the app's downward camera — the building's
strongest recognition cue, invisible in the only view that matters. The fascia is
now a dedicated solid standing **0.20 m** proud from z 3.24 to 4.10, and the
awnings are **0.60 m** deep and 0.20 m tall, tucked under it.

**Correction 4 — the café panel had to move out with it.** Once the fascia stood
0.20 m proud, the plan's café panel at d 0.05–0.13 was buried inside the band it
is screwed to. It now sits at d 0.18–0.28.

**Correction 5 — the night glow is per-bay, not one continuous strip.** The plan
called for a single glowing ribbon per street face. The app draws `_Glow` in a
separate layer at ~12% alpha **by day**, so a strip spanning both faces veiled the
entire ground floor pale in the day render — destroying the dark base this
building exists to be. The ribbon is now one glow panel per shopfront bay, inset
0.45 m from each mullion. At night it still reads as a continuous band wrapping
the corner (the mullions between are what a real shopfront has anyway); by day the
veil is a row of patches with navy glazing around them.

**Correction 6 — roof density and the stair-head cap.** The plan's five skylights
and three plant boxes left a 490 m² roof reading empty at aerial distance; built
with **seven** skylights and **four** boxes. The stair head was specified in
`Toy_trim` and rendered as the hottest object in the whole top view; it is now
`Toy_stone` like the walls. Its coping is four thin bars around the top edge, not
a lid — a full-plan cap box reads from directly above as a black hole punched in
the roof, which 599 Third learned the same way.

## 2. Height decision

| Figure | Value | Source |
|---|---|---|
| LiDAR height median | 7.77 m | DataSF `ynuv-fyni`, `SF3776114` |
| LiDAR height mean / majority | 7.69 / 7.82 m | same record |
| LiDAR height σ | **0.64 m** | same record — the roof is genuinely flat |
| OSM `height` tag | 8 m | way/124903637, independent import |
| LiDAR height max | 11.65 m | same record — **attributed to the neighbour** |
| Modelled roof membrane | 7.90 m | LiDAR median + a 0.13 m build-up |
| Modelled main parapet crest | 8.40 m | *estimated* |
| Modelled raised corner crest | **9.50 m** | *estimated* — **`targetHeightM`** |

The 11.65 m maximum is 6σ above a roof whose σ is 0.64 m. The building shares its
NW party wall with a 1,906 m² brick warehouse whose own LiDAR median is 11.05 m,
so edge cells along that wall produce this number without any structure on this
roof. Nothing in the 2026 aerial imagery or in any Street View pano rises near
11.6 m. **No penthouse was modelled to explain it.**

The parapet and the corner step are photogrammetric estimates, scaled off Street
View against the known 23.10 m Brannan face with an eye-level camera ~20 m out;
±0.5 m is possible. The manifest entry therefore carries `estimated: true`. If
the crest moves, only `targetHeightM` and the top of the corner block move with
it — the roof membrane at 7.77 m is measured and stays.

## 3. Orientation

Authored in true-world orientation, Blender `+Y` = north, `+X` = east; the loader
applies no rotation (`placeGeneric` in `app/src/assets.js` only scales and
positions). The 3rd Street front's outward normal is 45.2° true and the Brannan
front's is 135.1° true, so the contract's "front faces −Y" **cannot be honoured**
— neither street face points south. Real-world orientation wins per AGENTS rule 5
and the orientation note in `docs/asset-plans/README.md`. Recorded here as the
deviation that rule requires.

The east corner (footprint vertex E, +15.714, +0.602 from the anchor) is the
3rd/Brannan street corner and the hero point; the raised parapet sits over it.

## 4. Build iterations

| # | Change | Why |
|---|---|---|
| 1 | first build, 77 objects / 4,364 tris | baseline |
| 2 | raised corner parapet rebuilt proud of the main coping (d_out 0.10 vs the coping's 0.08) | flush, the ink coping ran across in front of it and read as a shadow gap slung under a floating slab |
| 3 | fascia became its own proud solid; awnings shrunk to 0.60 × 0.20 m | correction 3 above |
| 4 | roof density 5→7 skylights, 3→4 boxes; stair head `Toy_trim`→`Toy_stone`; lid cap → four coping bars | correction 6 above |
| 5 | café panel pushed to d 0.18–0.28 | correction 4 above |
| 6 | shopfront glow split into per-bay panels, z 0.75–2.65 | correction 5 above |
| — | final: 92 objects / 5,312 tris | |

Every iteration was reviewed from the high three-quarter aerial first, per the
style bible, before the formal render rig was run.

## 5. Validation

`validate_590_third.py` factory-resets Blender, imports **only** the exported
GLB, and reports on the re-import. Full machine-readable output in
`validation.json`.

| Check | Result |
|---|---|
| meters and plausible dimensions | PASS — 31.913 × 31.531 × 9.500 m |
| base at z = 0 | PASS — min Z 0.000 |
| crest is target height | PASS — max Z 9.500, loader scale 1.000000 |
| centred in XY | PASS — (+0.151, −0.000) m |
| under triangle budget | PASS — 5,312 of 11,000 |
| no image textures | PASS — 0 images, 0 textured materials |
| no transparency | PASS |
| materials follow contract | PASS — 11 materials, all `Toy_*`, no `Toy_body` |
| no cameras or lights | PASS |
| no animation, skins or constraints | PASS |
| transforms applied | PASS |
| no negative scales | PASS |
| normals outward | PASS — 0 inverted signed volumes; **ray residual 0.000000** |
| no degenerate geometry | PASS |
| no unexpected objects | PASS |

**Overall: PASS (15/15).**

Note on the light well: the body is a genus-1 solid — the well is a real hole cut
through the shell, with the shaft skin wound so its normals point into the shaft
(outward from the solid) and the caps bridged corner to corner. The build script
asserts that the annulus spokes never cross before it builds the mesh. The ray
test came back at exactly 0.000000 residual anyway, so the hole cost nothing.

## 6. Night state

A **band**, not a scatter — deliberately the opposite of `599-third` across the
street, so that the intersection reads "shops below, homes above":

- the shopfront glazing glows per bay in `Toy_trim_Glow`, continuously around the
  east corner — the hero;
- the `CAFE BUENOS AIRES` panel glows in `Toy_sky_Glow` — the one saturated cue;
- exactly two upper windows are lit in warm `Toy_mustard_Glow` (Brannan bay 3,
  3rd Street bay 1);
- walls, parapets, roof, AC boxes, garage door and blade sign stay dark.

Every glow surface is a thin shell standing proud of the opaque glazing behind
it, never a primary surface, because the app renders that layer at ~12% alpha by
day. Glow colours are all light: the app's night layer is unlit and drawn at the
material's own baked colour, so a dark glow would make a lit window read darker
than an unlit one.

## 7. Approval (gate 3)

> "I approve everything -- go ahead and do your thing. you dont need to ask for
> stage 3 approval. proceed w everything"
> — David, 13 August 2026, in the pipeline invocation

Blanket approval given in advance of the build, covering gate 3. Recorded
verbatim as the gate requires. The contact sheet, aerial, night render and the
numbers above are presented in the session summary rather than held for a reply.

## 8. Manifest entry (for integration, not applied here)

```json
{
  "id": "590-third",
  "file": "590-third.glb",
  "anchor": [
    -122.3946749,
    37.7800837
  ],
  "targetHeightM": 9.5,
  "cat": 4,
  "name": "590 Third Street",
  "estimated": true,
  "dims": [
    31.913,
    31.531,
    9.5
  ],
  "tris": 5312,
  "loadRadius": 2500
}
```

`cat 4` (Shop): the building's public identity is its storefront band. The
assessor still classes the parcel `Industrial`, which describes 1905, not 2026.
`estimated: true` because `targetHeightM` rests on the photogrammetric parapet
estimate in §2, not on the measured LiDAR roof. `loadRadius` is the default
`max(2500, 9.5 × 30)` = 2500.

Registry entry for `pipeline/lib/landmarks.mjs`:

```js
{
  id: '590Third',
  name: '590 Third Street',
  lon: -122.3946749,
  lat: 37.7800837,
  height: 9.5,
  exclude: 7,
  camera: { distance: 180, yaw: 90, pitch: 30 },
}
```

`exclude: 7` is measured against the bake's own source — see
`docs/asset-plans/590-third.md` §2.13, and re-measure against the actual bake
input at integration.

## 9. Files

| File | Bytes |
|---|---|
| `590-third.glb` | 143,672 (shipped, meshopt) |
| `optimize/input/590-third.glb` | 310,156 (pre-optimize archive) |
| `590-third.blend` | authoring scene |
| `build_590_third.py` / `render_590_third.py` / `validate_590_third.py` / `make_contact_sheet.py` | deterministic rig |
| `590-third-{aerial,top,north,east,south,west,night}.png` | review renders |
| `590-third-contact-sheet.png` | review sheet |
| `validation.json` | validation report |
| `REFERENCE.md` | sources and observations |
| `optimize/` | stage 4 — scripts, A/B renders, diffs, gate results (`optimize/REPORT.md`) |
