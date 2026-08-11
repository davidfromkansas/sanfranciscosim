# Mission Dolores — build and validation report

Miniature GLB of the 1918 Mission Dolores Basilica and the 1791 Old Mission
adobe chapel beside it, authored for the SF-SIM toy-diorama city. Research and
sources: [`REFERENCE.md`](./REFERENCE.md). Machine-readable validation:
[`validation.json`](./validation.json).

**Status: PASS — 14/14 contract checks on a fresh-scene re-import of the
exported GLB.** Not integrated, not deployed, not committed (local only).

## 1. Deliverables

| File | What it is |
|---|---|
| `mission-dolores.glb` | the asset, 517,808 bytes (506 KiB); a durable copy is at `~/sf-3d-assets/landmarks/mission-dolores.glb` |
| `mission-dolores.blend` | authoring scene the build script saved |
| `build_mission_dolores.py` | deterministic rebuild (`blender -b --python build_mission_dolores.py --`) |
| `render_mission_dolores.py` | review renders, always from the exported GLB |
| `validate_mission_dolores.py` | fresh-scene contract validation → `validation.json` |
| `make_contact_sheet.py` | assembles the contact sheet from the renders |
| `REFERENCE.md` | research dossier, sources, verified vs inferred |
| 8 PNG renders + contact sheet | see §5 |

Blender used: **5.2.0 LTS** at `/Applications/Blender.app/Contents/MacOS/Blender`
(the plan's `/opt/blender` 4.5 does not exist on this machine; the scripts are
version-agnostic apart from tolerating `blend_method` having been removed).

## 2. Orientation decision — the front faces EAST, and the −Y rule is inverted

The asset is authored with Blender **+Y = true north, +X = east**, so it drops
into the city at its real-world heading and the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions — verified in
the source).

The task prompt stated both facades face north onto Dolores Street. **That is
wrong and was not followed.** Both facades face **EAST** onto Dolores Street:

- the 2008 DPR 523A survey text quoted in SF Planning packet 2019-005041COA
  says plainly "The façade faces east";
- Esri World Imagery at z19 shows Dolores Street running north–south along the
  east edge of the block, with both entrance fronts and the basilica stair
  facing it, and the nave running east–west into the block;
- the mapped long axes are ~86° (basilica) and ~82° (adobe) clockwise from
  true north — east–west naves, not north–south.

The plan document also mis-stated its own bearing ("naves run north–south into
the block" alongside a measured 85° axis). Measured headings as built:
**basilica facade normal 086°, adobe facade normal 082°** (the real 4° splay).

Consequence for the contract: the `sf-asset-check` rule "front faces −Y" is
**deliberately inverted here** — this asset's fronts face **+X (east)**,
because true-world orientation is what a no-rotation loader requires for a
two-building composition that must sit on two real footprints. Anyone
integrating it must not rotate it.

## 3. Verified inputs

| Quantity | Value used | Basis |
|---|---|---|
| Basilica footprint | 58.7 × 33.6 m, axis 086° | OSM way/256442760, measured in the project projection |
| Adobe footprint | modelled 37.0 × 12.2 m, axis 082° | OSM way/256442765 minus the ca.-1975 gift-shop annex |
| Basilica eaves | 14.0 m | OSM `height` tag |
| Main cornice | 19.0 m | photo measurement scaled by the 24.6 m facade width |
| South tower | 27.8 m to the cross | photo measurement (±1–2 m) |
| **North tower** | **41.0 m to the cross tip** | photo measurement (±1–2 m); no published figure exists |
| Adobe eaves / ridge | 6.8 / 10.3 m | photo proportion; OSM tags 8 m, see §7 |
| Gap between buildings | 1.4–2.0 m at the street | OSM polygons, min separation 1.90 m |
| Anchor (origin) | −122.4269098, 37.7643109 | WGS84 of the combined bbox base centre, computed by the build script |

## 4. Validation (fresh isolated scene, re-imported GLB)

| Check | Result |
|---|---|
| Objects / mesh objects | 255 / 255 |
| Triangles | **8,414** (budget 24,000) |
| Dimensions (x, y, z) m | 67.214 × 45.482 × **41.000** |
| BBox min / max m | (−33.607, −22.741, 0.000) / (33.607, 22.741, 41.000) |
| min Z | **0.0000** |
| XY centre offset | **(0.0000, 0.0000)** |
| Materials | Toy_brick, Toy_cream, Toy_glass, Toy_gold, Toy_gold_Glow, Toy_ink, Toy_ioorange, Toy_roofd, Toy_rust, Toy_stone, Toy_trim, Toy_verdigris, Toy_white_Glow |
| Glow materials | Toy_gold_Glow, Toy_white_Glow |
| Image textures | 0 |
| Transparent materials | 0 (every alpha = 1.0, roughness 0.85) |
| Cameras / lights | 0 / 0 |
| Animations / armatures / constraints | 0 / 0 / 0 |
| Transforms applied | true (every object identity loc/rot/scale) |
| Negative scales | false |
| Degenerate triangles | 0 |
| Normal orientation | **PASS** — 0 non-unit loop normals; 23,730 first hits from 30,000 deterministic visibility rays, **0 flipped visible faces** |
| Unexpected objects | none |
| Material contract violations | none (all `Toy_*`, no `Toy_body`) |
| **Overall** | **PASS** |

Every material is flat colour from the `sf-asset-check` palette. `Toy_roofd`
appears only on the two narthex-roof vent caps.

## 5. Renders

All eight are made by re-importing the exported GLB, so every image depicts the
shipped geometry. The four elevations share one rig — same orthographic
projection, ortho scale, distance, lighting, exposure — differing only in
azimuth; directions are true compass directions.

| File | View |
|---|---|
| `mission-dolores-east.png` | Dolores Street front (the identity view) |
| `mission-dolores-north.png` | 16th Street flank |
| `mission-dolores-south.png` | adobe flank |
| `mission-dolores-west.png` | apse, crossing dome, parish wing |
| `mission-dolores-top.png` | both tile roofs, crossing dome, two tower caps |
| `mission-dolores-aerial.png` | high three-quarter, 36° down, 105 mm |
| `mission-dolores-night.png` | app dusk state, aerial |
| `mission-dolores-night-front.png` | app dusk state, street level |
| `mission-dolores-contact-sheet.png` | all of the above, labelled |

**Day renders show the glow layer at 12 % opacity**, matching the app: `kit.js`
`updateLandmarkGlow` sets the glow mesh opacity to `0.12 + 0.95 * uNight`, so
`_Glow` surfaces are near-invisible ghosts by day and ignite at night. Every
`_Glow` surface here is a thin shell standing 4–6 cm proud of an opaque day
surface (glass, ink reveal), never a primary surface — so nothing goes
translucent in daylight.

**Night state: every window in both buildings lights up.** 38 warm
`Toy_gold_Glow` shells cover the nave clerestory (10), the aisle windows (10),
the transept windows (2), the crossing-dome drum windows (4), the parish-wing
windows (2), the tower slit windows (4), the aisle roof skylights (4 — they
read as lit interiors from the app's downward camera), the adobe's three bell
openings and its four flank openings, plus the great central window and the
belfry arches of both towers. The only non-window glow is the white
`Toy_white_Glow` uplight strips washing the three portal bays.

Two glow materials total, so the app still merges the whole night layer into a
single draw call.

## 6. Design decisions (style bible §22)

Recognition cues kept, in rank order: the pairing of a tiny 1791 adobe against
a big 1918 basilica; the **asymmetric** towers (short domed cupola south, tall
three-stage tower north, both with verdigris ribbed domes); the ornate central
bay between plain shafts over a full-width stair; red-orange tile roofs with a
big octagonal tiled crossing dome; the adobe's four-column / balcony / three-bell
facade under huge dark eaves.

Simplified: Churrigueresque filigree → one raised panel field, layered arch
surrounds, two niches and a crest niche (the density the bible caps at);
spiral columns → plain round columns with square caps; tile courses → flat
`Toy_ioorange` with chunky ridge caps and eave bands; statuary → omitted;
rear parish additions → one clean wing volume. Roofs are designed rather than
blank: ridge caps, white aisle decks with skylight strips, narthex vents,
lantern and cross on the dome.

Scope: basilica + towers + entrance stair + adobe chapel only. No cemetery,
school, street, trees, people, vehicles, plinths, cameras or lights — the
validator confirms 0 cameras/lights and no unexpected objects.

## 6b. A glTF round-trip trap in the night renders (fixed here, present in sibling scripts)

Worth recording because it silently falsifies night review renders. The
exporter correctly writes `emissiveFactor = [0, 0, 0]` for every material — the
shipped asset must not self-emit, since the app supplies the night pass. On
re-import, Blender's glTF importer therefore hands back **Emission Colour =
white (1,1,1)** with strength 0. A night preview that lights `_Glow` materials
by raising *only* Emission Strength consequently renders **every glow surface
white**, whatever colour it actually is — warm gold and cream become the same
blown-out white, and no choice of strength fixes it.

`render_mission_dolores.py` now drives emission from each material's own **base
colour** at strength 1.0, which is exactly what the app's unlit glow layer
uses, so the render shows the real colour. The same
strength-only pattern exists in `artifacts/coit-tower/render_coit_tower.py` and
`artifacts/conservatory-of-flowers/render_conservatory_of_flowers.py`; their
night images should be read as white-washed rather than as those assets' true
glow colours. I did not modify those files — out of scope for this task.

## 7. Uncertainties, conflicts, and what I decided

- **Tower height is measured, not published.** No source gives one. 41.0 m is a
  photogrammetric read of the 2025 Commons frontal photograph scaled by the
  24.6 m facade width, cross-checked against a second frontal photo; ±1–2 m.
  The manifest entry is therefore `"estimated": true`.
- **Symmetrical vs asymmetrical towers.** The HPC packet's staff-written
  feature list says "symmetrical"; the DPR 523A text it quotes says
  "asymmetrical", the 1926 record says one tower was extended, and every
  photograph shows two different tops. Built asymmetrical.
- **Adobe height.** OSM tags 8 m; photographs against the basilica put the
  ridge nearer 10 m. Built 6.8 m eaves / 10.3 m ridge, inferred.
- **Adobe extent.** The OSM way is 45.7 × 17.0 m including a rear annex and the
  ca.-1975 gift shop. Only the historic chapel volume (37.0 × 12.2 m) is
  modelled; the gift shop is deliberately absent.
- **Including the adobe at all** is a judgement call — it is a separate OSM
  building. Included because the pairing is the top recognition cue and the
  task asked for it. Both sit at their true relative offset and splay, so the
  asset covers two footprints; whoever integrates must exclude both.

## 8. Draft manifest entry (do NOT apply in this task)

Anchor re-derived from the model itself: the origin is the combined
bounding-box base centre, and `placeGeneric` puts the group **origin** on the
anchor with no recentring, so the anchor is the WGS84 of that point.
`targetHeightM` 41 equals the model's own height, giving loader scale ×1.0000
and keeping both real footprints at true metres.

```json
{
  "id": "mission-dolores",
  "file": "mission-dolores.glb",
  "anchor": [
    -122.4269098,
    37.7643109
  ],
  "targetHeightM": 41,
  "cat": 8,
  "name": "Mission Dolores Basilica",
  "estimated": true,
  "dims": [
    67.21,
    45.48,
    41.0
  ],
  "tris": 8386
}
```

Changes from the plan's draft: anchor moved (the plan's point is ~5 m off the
combined-model origin), `targetHeightM` 30 → **41** (the plan's 30 m was a
guess at the tower height and does not match the measured cross tip), and
`estimated` false → **true**, since the height remains unpublished.

## 9. Integration notes (a separate job — `docs/asset-plans/INTEGRATION-PROMPT.md`)

- New landmark: needs a `pipeline/lib/landmarks.mjs` entry (`id:
  'missionDolores'`) and a re-bake, or the baked procedural block will
  intersect the GLB. The exclusion radius must cover **both** buildings —
  ~45 m from the anchor, not the plan's 70 m centred elsewhere.
- No procedural builder exists to hide, so the fallback is the baked city block.
- **Do not rotate the asset on load** (§2).
- The app also bakes street furniture and trees around this block; check the
  Dolores Street frontage for furniture standing inside the stair.

See `OPTIMIZATION.md`: this GLB is the size-optimized build (geometry-identical; objects joined per material). Figures above reflect the shipped file.
