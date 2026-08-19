# 345 Spear Street (Hills Plaza) — build report

**Asset:** `artifacts/345-spear/345-spear.glb` — the 1989–91 Whisler-Patri half
of Hills Plaza: buff-brick office podium + 18-storey white residential tower
(One Hills Plaza, 75 Folsom) + terracotta hip pavilion on Spear + level-8 roof
garden + sunken courtyard. The Hills Brothers Building (2 Harrison) is a
separate in-flight landmark and is not part of this asset.

## Numbers (validated re-import, `validation.json`)

| | |
|---|---|
| Objects / triangles | 233 / **17,428** (cap 24,000) |
| Dimensions | 106.33 × 118.99 × **68.50 m** (bbox top = LiDAR hgt_max, scale lands at 1.0) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Materials | 15 `Toy_*`, flat, no textures, no alpha |
| Glow groups | `Toy_white_Glow` (arcade, hero), `Toy_gold_Glow` (crown band + entry sign), `Toy_glass_Glow` (6 lit tower windows) |
| Cameras / lights / animations | 0 / 0 / 0 |
| Normals | per-object signed volume all outward; ray test PASS |
| Validation | **all-PASS** |

## Manifest draft (integration values)

```json
{
  "id": "345-spear",
  "file": "345-spear.glb",
  "anchor": [-122.3901941, 37.7900769],
  "targetHeightM": 68.5,
  "cat": 3,
  "name": "Hills Plaza (345 Spear)",
  "estimated": false,
  "dims": [106.3305, 118.9857, 68.5],
  "tris": 17428
}
```

- The **manifest anchor is the model's bbox centre** (placeGeneric puts the GLB
  origin at the anchor): the authored OBB anchor −122.3900655, 37.7900324
  plus the measured AABB offset (11.32, −4.92) m. The **registry/exclusion
  anchor stays the OBB centre** −122.3900655, 37.7900324 (see the plan's 2.13;
  the two anchors differ by design — bbox vs footprint centre).
- Case B: new landmark; registry entry + re-bake required. Preliminary safe
  exclusion window r ≈ 12–30 m (own DataSF/Overture centroids ≤ 6 m from the
  OBB anchor; nearest Hills Brothers vertex ~35–40 m). BATCH mode: bake for QA,
  then discard tiles before commit.

## Dossier corrections made while building

1. **The tower is rotated 45° off the street grid** (true N–S, facing the bay
   square-on) — measured from the nadir Google ortho with the OSM rings
   overlaid, corroborated by Street View. The plan's massing recipe assumed a
   grid-aligned tower; REFERENCE.md §4 records the measurement. This diamond
   silhouette is the asset's strongest aerial cue and is preserved exactly.
2. **Manifest anchor moved to the bbox centre** (−122.3901941, 37.7900769).
   The plan's §2.12 draft used the OBB centre; for this asymmetric diagonal
   footprint the two differ by 12.3 m and placeGeneric needs the bbox centre.
3. Podium split refined against LiDAR: wings 24.2 m (mode), street frontages
   29.4 m (median + parapet), SE plaza wing 27.0 m.

## Review-driven iterations (aerial-first, then formal rig)

1. *First aerial:* terrace planters floated outside the staircase footprint
   (placed at the parapet line); the sunken courtyard was invisible (its
   recessed-well prisms were capped and buried inside the podium solid).
   → planters moved inboard of each step's parapet; the court re-done as the
   501-second light-court pattern — a dark `Toy_roofd` panel + `Toy_trim`
   border + mint planting ribbon + paving spine on the deck (no boolean; from
   the app camera a real recess reads identically).
2. *Same pass:* the pavilion attic began at 29.4 m and floated over the 24.2 m
   podium on its courtyard side → body extended down to the podium deck.
3. *Validator:* `transforms_applied` FAIL — the recentring pass had shifted
   object locations instead of geometry → recentring now bakes the full world
   transform into every mesh (`mesh.transform`), objects ship at identity.

## Night state

Hero: the arcade arches (Embarcadero, plaza and terrace-step faces) glow warm
white — thin shells proud of the opaque glass fills. Support: one gold band
under the tower's setback parapet, the gold entry sign strip on Spear, and a
scatter of six lit windows on the tower shaft. Day colors of all glow surfaces
match their non-glow neighbours.

## Approval

- Gate 3: the user pre-approved the full pipeline for this batch session in the
  invocation: **"APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"** (2026-08-19).
  Recorded here verbatim per the pipeline's stage-3 rule; renders and contact
  sheet are committed alongside for after-the-fact review.
