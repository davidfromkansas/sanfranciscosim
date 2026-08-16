# 102 South Park (The Park View) — build report

`102-south-park.glb` — a stylized miniature of the 1913 Park View Hotel on the north rim
of the South Park oval, four storeys of SRO over Caffe Centro on a 25-foot lot.

Built by `build_102_south_park.py` (Blender 5.2.0 LTS, headless, deterministic), rendered
by `render_102_south_park.py` from the **exported GLB**, validated by
`validate_102_south_park.py` in a fresh factory-reset scene.

## 1. Shipped numbers

| | |
|---|---|
| Triangles | **8,100** (budget 9,000; hard gate 30,000) |
| Objects (shipped, after the stage-4 join) | 11 — 140 before optimize |
| File size (shipped) | **219,692 bytes** raw, meshopt-compressed — 489,472 before optimize, −55.1 % (gate ≤ 500 KB) |
| Dimensions | 27.253 × 27.146 × **14.000** m |
| min Z | 0.000 m |
| XY centre offset | (0.214, −0.214) m |
| Materials | 11, all `Toy_*`, flat, opaque, no textures |
| Glow groups | 2 — `Toy_mustard_Glow` (café), `Toy_glassl_Glow` (lit SRO rooms) |
| Anchor | −122.3943678, 37.7817707 (footprint OBB centre) |
| Front heading | 135.4° true (SE, onto South Park) |
| `targetHeightM` | 14.0 — the loader's scale lands at exactly 1.0 |
| Validation | **PASS**, all 16 checks |

The 27.25 × 27.15 m axis-aligned XY box is the expected consequence of a 7.78 × 29.76 m
building sitting at a 135.4° heading. It is not a scale error.

## 2. Contract deviation: "front faces −Y"

The asset is authored in **true-world orientation** (`+Y` = north, `+X` = east) so it drops
into the city at its real heading — `placeGeneric()` in `app/src/assets.js` scales and
positions but never rotates. This building's front faces **135.4°**, so the contract's
"front faces −Y" rule cannot be honoured literally. Real-world orientation wins
(AGENTS rule 5), exactly as `docs/asset-plans/README.md` prescribes. Recorded here as the
deviation.

## 3. Corrections and decisions made against the plan

**3.1 The plan's edge indices were wrong and were re-derived.** The plan lists the
footprint clockwise; the build reverses it to get a CCW ring (so `n = (t.y, −t.x)` is
outward). After the reversal the elevations are edges **13 / 14 / 15 / 0**, not the
0 / 1 / 14 / 15 the first draft assumed. The first build put a 30 m cornice down the
northeast flank and produced a 38.3 m bounding box with a 5.3 m centre offset. The build
script now prints every edge's measured outward normal (135.4 / 45.0 / 315.4 / 225.0) so
this cannot silently regress.

**3.2 The 15.20 m LiDAR maximum is deliberately not the crest.** DataSF `SF3775057` reports
median 12.88 m, majority 12.71 m, mean 12.58 m, σ 1.60 m, max 15.20 m. The max sits 1.6σ
above the mean, so unlike 592 Third Street's 6σ outlier it is *not* obviously a tree
artifact — but the flowering trees standing directly in front of this cornice are exactly
the geometry that produces such a reading, and a 2.3 m element over a 12.9 m deck would be
an implausibly large bulkhead on a plate 7.78 m wide. **Decision: the roof deck takes the
LiDAR median (12.90 m), the front cornice crest is estimated at 14.00 m and is the bbox
top, and the stair bulkhead is modelled at 13.90 m — below the crest.** If photographic
evidence of a tall roof bulkhead turns up, the model and the manifest height move together.

**3.3 The light-well notches are built, not simplified away.** The plan allowed either. They
cost ~300 triangles on the prism and the parapet, they are the only irregularity the roof
has, and the aerial and top renders show them reading clearly as slots on the southwest
side. Roof furniture is kept clear of them (`V_NOTCH_LIMIT`), which is why the solar array
is **two rows of six** rather than the plan's three rows of four — a third row would have
run over the wells.

**3.4 `Toy_verdigris` was rejected for the awning; `Toy_awning` #4f7d63 ships instead.**
The plan flagged this and the first render settled it: the palette's soft sage (#9fb8a8) on
a pale greige wall read as a pale mint slab with almost no contrast, on the one element that
is supposed to be the building's only saturated accent. `Toy_awning` is off-palette, which
is a WARN and not a FAIL, and it is both more accurate and much more legible. This is the
single off-palette colour in the asset.

**3.5 `Toy_glassl` is used as an opaque trim colour, not as glass.** #6f95b8 is the
palette's exact match for the observed dusty blue-gray window joinery, and the loader only
bakes the colour — the key name carries no behaviour. Every architrave, keystone, sill and
flank-window surround in this asset is `Toy_glassl`. Flagged so a later reader does not
read it as a mistake.

**3.6 First-aerial revisions.** Three things changed after the first review render, before
the formal rig: the keystone was shrunk (0.34 → 0.26 m wide, and less proud) because the
arch plus a large keystone read as a tombstone; the flank windows were enlarged
(1.10 × 1.35 → 1.30 × 1.50 m) because they disappeared at diorama scale; and the storefront
was enlarged (3.50 × 2.60 → 3.60 × 2.85 m) because it was a dark postage stamp under the
awning. The stair bulkhead was also moved from the park end to the rear so the park end of
the roof stays clear, which is what the satellite imagery shows.

**3.7 The `building=retail` OSM tag was not inherited.** It describes Caffe Centro. The
building is a residential hotel; the manifest uses `cat: 7` (Hotel), which is what the
assessor calls it.

## 4. Night state

Hero glow: the **Caffe Centro storefront**, lit warm (`Toy_mustard_Glow` #d9a441) and lit
fully — the only lit ground floor on this stretch of the oval and the whole reason the
building has a story at night. Supporting accent: **six lit SRO rooms** scattered across the
three upper floors of the front and northeast elevations (`Toy_glassl_Glow` #6f95b8) —
never a full floor, because an SRO at night is mostly dark with a few rooms on. Nothing
else glows; there is no signage and no crown.

Every glow surface is a thin shell standing proud of the opaque glazing behind it, so the
app's ~12 % day alpha on the glow layer reads through to the real window colour. The day
renders preview that correctly (`fade_glow()`); the night render drives emission from Base
Color, not from the imported `emissiveFactor`, per the note at the end of
`docs/asset-plans/README.md`.

## 5. Files

| File | What |
|---|---|
| `build_102_south_park.py` | deterministic build; writes the .blend and the .glb |
| `render_102_south_park.py` | review rig; always re-imports the exported GLB |
| `validate_102_south_park.py` | fresh-scene contract validation → `validation.json` |
| `make_contact_sheet.py` | composes the seven renders into the contact sheet |
| `102-south-park.glb` | **the shipping asset** — the stage-4 optimized, meshopt-packed file |
| `optimize/` | stage-4 shrink pass: scripts, stats, A/B renders, `REPORT.md`, and the pre-optimize original archived at `optimize/input/` |
| `102-south-park.blend` | authoring scene |
| `102-south-park-{north,east,south,west,top}.png` | one rig, identical but for azimuth |
| `102-south-park-aerial.png` | high three-quarter, 38° down, 105 mm lens, azimuth 105° |
| `102-south-park-aerial-night.png` | the dusk pass |
| `102-south-park-contact-sheet.png` | all seven |
| `validation.json` | the machine-readable report |
| `REFERENCE.md` | sources, verification, per-elevation observations |

## 6. Draft manifest entry

```json
{
  "id": "102-south-park",
  "file": "102-south-park.glb",
  "anchor": [-122.3943678, 37.7817707],
  "targetHeightM": 14.0,
  "cat": 7,
  "name": "The Park View (102 South Park)",
  "estimated": true,
  "dims": [27.2532, 27.1464, 14.0],
  "tris": 8100,
  "loadRadius": 2500
}
```

`estimated: true` because the cornice crest is a photogrammetric estimate, not a published
figure. `loadRadius` takes the default `max(2500, 14.0 × 30) = 2500` m.

## 7. Stage 4 — optimize

Run per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`; full write-up in
`optimize/REPORT.md`. **489,472 → 219,692 bytes (−55.1 %), 140 → 11 draw
submeshes, 8,100 triangles unchanged, all eight gates PASS**, worst A/B pixel
delta 0.0596 % against a 2 % gate. The limited-dissolve step was skipped because
this asset carries three large coplanar ring bands (the 350-brannan sliver
lesson). The optimized file is what ships; the pre-optimize original is archived
at `optimize/input/102-south-park.glb`.

## 8. Stage 5 — integration (batch mode)

Case B. Registry entry `102SouthPark` added to `pipeline/lib/landmarks.mjs`
(`exclude: 4`, `camera: { distance: 170, yaw: 75, pitch: 26 }`), manifest entry
appended, GLB copied to `app/public/sf-assets/landmarks/`, full twelve-stage bake
run, QA'd, and then **discarded** — this branch commits source only, per the batch
rule in `docs/asset-pipeline/ADDRESS-TO-ASSET.md`. `git diff --name-only
origin/main` lists nothing under `app/public/tiles/` or `api/_data/`.

### Exclusion radius

Measured, not guessed — and re-measured once. `addBuilding()` runs
`simplifyRing(ring, 0.6)` **before** `excluded()`, so the raw geojson ring is the
wrong thing to measure: on the unsimplified rings 106 South Park's shared
light-well vertex sits 3.03 m from the anchor and forces `exclude: 2.6`, while on
the rings the gate actually sees its nearest approach is 6.50 m. Final band
(2.02, 6.5]; shipped **4**, the middle. Full working in the registry comment.

### QA table

| Item | Result | Evidence |
|---|---|---|
| Re-validation of the shipped GLB | **PASS** | fresh-scene `validate_102_south_park.py`, 16/16 checks, on the packed file |
| Manifest entry | **PASS** | 59 entries served; formatting of the other 58 untouched |
| id mapping | **PASS** | `camelId('102-south-park')` = `102SouthPark`, matches the registry |
| Registry + re-bake | **PASS** | full chain `terrain -> muni-shapes`, exit 0 |
| Audit check 1.6 | **PASS** | "66 zones over 65 landmarks clear" |
| `verify-rebake.mjs` | **PASS** | 584/585 cells unchanged; 23_13 only; nearest surviving footprint 7.9 m vs a 4 m radius |
| Single building on the site | **PASS** | tile 23_13 decoded: the 15.0 m block at 1.95 m from the anchor is gone, all seven neighbours within 22 m survive (nearest 5.88 m) |
| Scale factor | **PASS** | `uniform x1.0000 at 3795, -1301` |
| Orientation | **PASS** | arched front faces the oval, flank runs toward Jack London Alley — screenshot |
| Terrain seating | **PASS** | sits flush, no float or sink |
| Night glow | **PASS** | café storefront warm, six SRO rooms cool, nothing else lit |
| Draw calls | **PASS** | 80 parked at the landmark, 117 with the whole neighbourhood pumped in — budget is 300 |
| Streaming | **PASS** | `entries 59, failed 0, live 51, loading 0` |
| Fallback drill | **PASS** | GLB moved aside -> one warning, `failed: 1`, app boots, everything else renders, site is empty ground (Case B expected) |
| lint / build | **PASS** | `eslint src` clean; `vite build` ok, 3315 tiles compressed |
| Deployed QA | **not run** | the pipeline ends at a local verification and an ask |

Two things worth recording that are **not** attributable to this landmark:

1. **Tile 23_13 loses two footprints, not one.** The second (107.5 m from the
   anchor, 15.4 m tall) disappears just as reliably with the registry entry
   temporarily removed and `buildings.mjs` re-run — it is `pipeline/data/`
   vintage drift between the committed tiles and the snapshot on disk, not this
   exclusion zone. That is the decisive test from the data-vintage note, run here
   before the claim was made.
2. **`THREE.BatchedMesh: Reserved space request exceeds the maximum buffer size`
   is reachable, but not by this asset.** Hand-pumping `assets.update()` and
   `city.update()` at 250 ms while resetting the camera each tick exhausted the
   shared 1.2 M-vertex batch and failed 30 landmarks at once, most of them
   pre-existing ones. On a clean load with normal streaming the same camera
   position gives `failed: 0, live: 51`. The failure is batch churn from the QA
   harness, not manifest growth.

Three audit checks (1.2b, 1.3c, 1.7b) fail; all three are pre-existing on `main`
and unrelated to this landmark.

## 9. Approval

Stage 3 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION" — David, 16 August 2026

Pre-approved in the session's opening instruction, quoted verbatim. The contact sheet, the
day aerial and the night aerial were still presented before the pipeline advanced.
