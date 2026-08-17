# 86–96 South Park — build report

Asset: `artifacts/96-south-park/96-south-park.glb`
Plan: `docs/asset-plans/96-south-park.md`
Dossier: `REFERENCE.md`
Built with `build_96_south_park.py` on Blender 5.2.0 LTS, 17 August 2026.

**REPORT beats plan.** Where this file and the plan disagree, this file is what
shipped.

## 1. Shipped numbers

| | |
|---|---|
| Triangles | **6,312** (cap 11,000) |
| Objects | **14** after the stage-4 join (155 as authored) |
| File size | **181,952 bytes** shipped (419,860 pre-optimize, −56.7%) |
| Dimensions (m) | 31.809 × 27.621 × **13.700** |
| bbox min / max | `[-15.905, -13.970, 0.0]` / `[15.905, 13.651, 13.700]` |
| min Z | 0.000 |
| XY centre offset | `[0.000, -0.159]` m |
| Materials | 14, all `Toy_*`, flat, opaque, no textures |
| Glow materials | `Toy_mustard_Glow`, `Toy_glassl_Glow` |
| Anchor | `-122.3941704, 37.7818909` |
| Front heading | 135.2° (measured in-build from the footprint polygon) |
| Validation | `validation.json` — **overall PASS**, all 16 checks true (re-run against the shipped, optimized GLB) |
| Optimize | stage 4 complete — see `optimize/REPORT.md`; all gates G1–G6, G8 PASS |

The axis-aligned XY box is 31.8 × 27.6 m for a 14.44 × 30.06 m building. That is
the expected consequence of the real-world 45° heading, not a scale error.

## 2. Corrections this build made to the plan

### 2.1 Three roof planes, not two — the biggest change

The plan read the two DataSF LiDAR **medians** (11.15 m and 12.32 m) as the two
parapet planes and put a cylinder above them. Built that way, the first aerial
render was a **flat box**: two decks a metre apart on a 14 × 30 m plan do not
make a silhouette, and the cylinder had only 1.3 m of clearance so it read as a
water tank lying on the roof.

The LiDAR distribution actually has three modes, and the plan only used one of
them:

| ring | majority | median | mean | max | σ |
|---|---|---|---|---|---|
| `201006.0022147` (front + NE) | 9.49 | 11.15 | 10.99 | 13.28 | 1.51 |
| `201006.0149656` (rear SW) | 9.86 | 12.32 | 11.72 | 13.73 | 1.56 |

The **majority** plane — what most of the roof area actually is — is 9.5–9.9 m
on both rings. Reading it as a third plane gives:

- **main plate 10.00 m** over the whole footprint (the majority)
- **two upper volumes at 12.30 m** on diagonally opposite corners, front-northeast
  and rear-southwest (the medians)
- **gable ridge 13.35 m**, **cylinder cap 13.70 m** (the maxima)

That is both a better fit to the data and a far better miniature: the two upper
volumes on opposite corners are what make this read as Levy's "overlay of
geometries" instead of a shoebox. The crest is unchanged at 13.70 m, so the
manifest height in the plan still stands.

Floor plates moved with it: ground 0–4.20 m (was 4.60), F2 4.90, F3 7.50, F4
10.40 inside the upper volumes only. The brick base top moved 4.50 → 4.20 m.

### 2.2 The cylinder moved out of the rear block onto the alley wall

The plan put the drum at `(s -4.40, t +2.60)`, inside the rear volume's
footprint. Built there it was invisible from the street and nearly invisible
from the air. It now sits at **`(s -6.30, t +1.20)`, radius 2.75 m**, mid-flank
on Jack London Alley and **overhanging the alley wall by 1.83 m**, rising from
5.00 m to the 13.70 m cap. It stands 3.70 m clear of the main plate.

This is closer to the Feb 2021 pano than the plan was: in that photograph the
drum reads as part of the alley wall, not as a rooftop object. Diameter went
4.60 → **5.50 m** (plan 2.6 licenses enlarging it; at 4.6 m it still read small
against a 30 m wall).

It is also **darker than the body** — `Toy_steel` (`#9aa0a6`) rather than
`Toy_steel_l` — with a `Toy_slate` coping *ring* rather than a solid cap. A pale
drum on a pale wall under a pale deck disappeared from the aerial camera, which
is the one view it exists for; a solid dark lid, tried next, read as a hole.

### 2.3 Both orange gates enlarged again

The plan's 1.40 × 2.70 m gates were still invisible in the first aerial. Built
at **1.80 m wide** and taken to the full ground-floor height (3.55 m on the
front, 3.85 m on the alley), with a deeper `Toy_ink` reveal. They now read from
the app's camera distance, which is the whole point of them.

### 2.4 The alley window rhythm was regularised

The plan asked for "a deliberate irregular rhythm of six to eight tall
openings". Built irregular, the 30 m wall read as noise. It is now **seven bays
at 4.30 m centres** on two registers, with the irregularity carried where it
belongs — by the bronze panel, the volume steps and the drum. This is a
deliberate departure from the plan's instruction and the reason is in the
plan's own §2.6: contrast between adjoining volumes matters more than the
number of volumes.

### 2.5 The alley bronze panel moved

Plan: `u 12.60`, mid-flank. Built: **`u 6.60`** (measured from the Taber Place
end), widened to 8.60 m and taken up to 11.75 m, so the seam sits between the
drum and the rear corner instead of colliding with the drum.

### 2.6 The front gable is a triangle on top of the volume

The plan's gable had eaves below the volume's own wall top, so the wall hid it.
It is now a clean three-point triangular prism sitting **on** the front upper
volume, eaves 12.12 m, ridge 13.35 m, extruded 7.0 m back. An eaves band tried
between the two just added a stray horizontal line and was deleted.

### 2.7 The pergola moved and shrank

The plan put a 4.4 × 3.4 m pergola over a front-northeast terrace, from the
April 2017 photosphere. The 2026 satellite imagery shows the roof terrace with
furniture on the **neighbour's** roof (84 South Park, the "Vertex Ventures HC"
pin), so that reading is not safe. The pergola is kept but **moved to the
terrace between the two upper volumes** at `(s -3.2..-0.2, t -6.6..-3.2)`, top
11.20 m, where it is a plausible roof structure rather than a claim about a
specific photograph. **Flagged as the model's weakest invention.**

### 2.8 Two small material notes

- `Toy_steel_l` (`#b9bec4`) is used as the ribbed-metal body colour. It is not a
  pre-existing palette entry; it is a lighter sibling of `Toy_steel`. Off-palette
  is a WARN, not a FAIL, and the building needs a light metal that is clearly
  lighter than the coping.
- `Toy_teal` (`#3f7f86`) carries the mosaic band as one flat colour. The real
  band is multi-coloured; at diorama scale the stripe is the detail and the
  variation is sub-pixel.

## 3. Open risks carried into approval

1. **The cylinder is the model's biggest bet.** Its existence is solid (two
   independent views); its diameter, exact position and whether it is a full drum
   are not. Built as a full drum because that is the version that still reads
   from the air if the guess is slightly wrong.
2. **13.70 m is a LiDAR maximum interpreted as the drum cap**, not a measured
   crest. If a photograph lets someone scale the drum against a storey height,
   that measurement wins and the model and the manifest move together.
3. **The rear-northeast yard** is inferred from LiDAR coverage (289.7 m² of
   built footprint on a 434.1 m² lot, the gap concentrated at that corner). If
   satellite imagery shows it built, fill it in; the roof becomes a rectangle and
   nothing else changes.
4. **The Taber Place rear elevation is invented.** No photograph of it exists in
   any source consulted.
5. **The rooftop pergola is invented** in its current position — see §2.7.
6. **No architect's photographs were obtained.** Architizer and
   ldparchitecture.com both host galleries that did not render to text
   extraction. A human with a browser would likely settle risks 1, 3, 4 and 5 in
   one pass.

## 4. Contract deviations recorded

- **"Front faces −Y" is not honoured, deliberately.** The asset is authored at
  its real-world heading (front normal 135.2°) so the loader can place it with no
  rotation, exactly as `docs/asset-plans/README.md` prescribes for the 45° SoMa
  grid. `placeGeneric` in `app/src/assets.js` applies scale and translation only.
- **The origin is the modelled footprint's axis-aligned bbox centre, not the lot
  centroid.** The L-shaped plan pushes the bbox 2.261 m northwest of the lot
  centre; anchoring on the bbox centre is what lets "centered in x/y" hold
  exactly (measured offset `[0.000, -0.159]` m). The published anchor is that
  point, so the building still lands where the survey says it is.

## 5. Draft manifest entry

```json
{
  "id": "96-south-park",
  "file": "96-south-park.glb",
  "anchor": [
    -122.3941704,
    37.7818909
  ],
  "targetHeightM": 13.7,
  "cat": 2,
  "name": "86–96 South Park",
  "estimated": true,
  "dims": [
    31.8092,
    27.6214,
    13.7
  ],
  "tris": 6312,
  "loadRadius": 2500
}
```

## 6. Approval

Stage 3 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`. Standing approval given by
the user in the session's opening instruction, 16 August 2026, verbatim:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

Recorded as a blanket pre-approval covering this gate. The contact sheet, the
day and night aerials and the numbers in §1 were presented at the same time so
the approval is reviewable after the fact rather than before it, and the open
risks in §3 stand and are not waived by it.
