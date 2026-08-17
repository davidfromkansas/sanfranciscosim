# 35 South Park (Accel) — build report

Asset: `artifacts/35-south-park/35-south-park.glb`
Plan: `docs/asset-plans/35-south-park.md`
Dossier: `REFERENCE.md` (this asset's own research; it beats the plan where they differ)
Built: 17 August 2026, Blender 5.2.0 LTS, `build_35_south_park.py`

## 1. Shipped numbers

These are the numbers of the **shipped** file, i.e. after stage 4
(`optimize/REPORT.md`). The pre-optimize build is archived at
`optimize/input/35-south-park.glb`; where the two differ the pre-optimize figure is
given in brackets.

| | |
|---|---|
| File size | **211,704 bytes raw** [394,856 pre-optimize, −46.4%] |
| Triangles | **6,980** (budget 9,000) — unchanged by the optimize pass |
| Objects | **10** [95 pre-optimize] |
| Draw submeshes | **10** [95] |
| Materials | 10 — `Toy_glass`, `Toy_glass_Glow`, `Toy_glassl`, `Toy_gold_Glow`, `Toy_ink`, `Toy_roofd`, `Toy_steel`, `Toy_stone`, `Toy_trim`, `Toy_verdigris` |
| Glow groups | 2 — `Toy_glass_Glow` (the five lit arches), `Toy_gold_Glow` (four pier sconces) |
| AABB dimensions | 42.059 × 40.299 × 13.400 m |
| Footprint in plan | 22.72 × 35.80 m with a 7.96 × 2.44 m notch — the measured OSM ring |
| min Z | 0.000 m |
| XY centre offset | (−0.000, 0.829) m — see §3 |
| Crest | **13.400 m** — the penthouse cap, exactly on target, so the loader's `targetHeightM / measuredHeight` lands at 1.0 |
| Anchor | `-122.3933378, 37.7815714` (OSM way 112759864 OBB centre) |
| Arcade heading | 315.9° true (NW), authored, no rotation at load |
| Validation | `validation.json` — **all 16 checks PASS**; ray-flipped fraction 0.000000 |

## 2. Deliverables

`build_35_south_park.py`, `render_35_south_park.py`, `validate_35_south_park.py`,
`make_contact_sheet.py`, `35-south-park.blend`, `35-south-park.glb`, `REFERENCE.md`,
`REPORT.md`, `validation.json`, and the renders `-north`, `-east`, `-south`, `-west`,
`-front`, `-top`, `-aerial`, `-aerial-night`, `-contact-sheet`.

`-front.png` is an extra view beyond the standard rig: on a 45.5° heading the four
compass elevations each show two faces, which is correct but useless for judging the
one elevation that carries the design.

## 3. Deliberate deviations from the contract

- **"Front faces −Y" is not honoured.** The real heading is 315.9° and the loader
  applies no rotation, so the model is authored on its true bearing (AGENTS rule 5).
  Every South Park asset takes this deviation.
- **The axis-aligned bounding box is 42.06 × 40.30 m** for a 22.72 × 35.80 m building.
  That is the 45.5° heading, not a scale error.
- **The XY centre offset is 0.829 m in Y**, inside the ~1 m tolerance but not zero. It
  is not an off-centre model: the origin *is* the oriented bounding-box centre. The
  rear notch removes the southern corner of the rectangle, so the *axis-aligned* box is
  asymmetric in Y by exactly half the notch's Y extent. Recentring on the AABB would
  push the building 0.83 m off its own party wall, which is the error that matters.

## 4. Dossier corrections made while modelling

Four, all carried back into this report rather than into the plan's numbers, which
stand:

1. **The roof membrane is light, not dark.** The plan's §2.7 step 8 called for a
   `Toy_roofd` deck "clearly darker than the parapet cap so the ring reads from above".
   Built that way (first aerial review) the deck and the penthouse merged into one dark
   mass and the roof lost its composition — and it also contradicted the plan's own
   §2.4, which records a *bright white membrane, conspicuously brighter than every
   neighbouring roof*. The deck is now `Toy_steel` (`9aa0a6`), the precedent 2 South
   Park set one block away for exactly this. The parapet ring still reads, because the
   coping is `Toy_trim` and lighter still; the penthouse, the mechanical plant and the
   hatch went to `Toy_roofd` and now read as dark objects on a light field.
2. **The roof slab was coplanar with the body's top face** and z-fought across the
   whole deck in the first render (visible as diagonal blotches). The slab now sits
   0.06 m proud of the body top and 0.20 m thick.
3. **Bay geometry: the opening is 2.80 m, not the plan's 3.50 m.** At 3.50 m the piers
   came out 1.04 m clear *before* the archivolts, which left no pier for the roundels
   and no wall between arches. Re-measuring the arch:pitch ratio off the
   across-the-park capture (≈0.72) gives a 3.44 m outer arch on a 4.544 m pitch, so the
   clear opening is 2.80 m and the pier 1.10 m. The roundels shrank to match: 1.24 m
   outer diameter rather than the plan's 1.6 m exaggeration, which would not have fitted.
4. **Four roundels, not five.** The plan says "five roundels, one per pier". A five-bay
   arcade has four *interior* piers; the two end piers are narrow returns and no capture
   resolves whether they carry roundels. Four is what shipped, and §5 of REFERENCE.md
   records the open question.

Two smaller build fixes worth recording because they are easy to reintroduce:

- The arch mullions originally stopped at a flat height and the outer two poked through
  the archivolt as dark ticks. Each vertical now stops on the arch curve.
- The glow shells were originally proud of the mullions, so the lit arches read as blank
  white slabs at night. The mullions now sit in front of the glow (0.16–0.20 against
  0.12–0.18), and the night render shows five lit sash windows instead.

## 5. What stayed inferred

- The **penthouse crest at 13.40 m** (REFERENCE.md §2 and §5) — photogrammetric, ±0.7 m,
  driven by a single constant `Z_CREST`.
- The **hedge crest at 11.30 m** and its 1.10 m depth.
- The **penthouse plan (11.0 × 7.5 m, set back 8 m)** — read off the nadir aerial.
- The **north-east flank and the rear**, which nothing consulted photographs. Both are
  modelled plain, with the entablature carried right round — the device 2 South Park
  uses, and the reason the blind party wall still reads as part of the building from
  the app's downward camera.
- The **notch in section** — modelled as a full-height void.

## 6. Night state

Hero: the five arches, lit from the double-height interior, with the mullion grid
reading dark against them. Supporting accent: the four pier sconces in
`Toy_gold_Glow`. The penthouse, the roof lights, the roof and the three blind
elevations stay dark. Every glow surface is a thin shell proud of an opaque parent and
none is a primary surface, so the day render (which previews the app's 12%-alpha glow
layer) is unaffected.

## 7. Manifest entry

```json
{
  "id": "35-south-park",
  "file": "35-south-park.glb",
  "anchor": [
    -122.3933378,
    37.7815714
  ],
  "targetHeightM": 13.4,
  "cat": 3,
  "name": "Accel (35 South Park)",
  "estimated": true,
  "dims": [42.06, 40.3, 13.4],
  "tris": 6980,
  "loadRadius": 2500
}
```

`dims` and `tris` are the shipped figures: the optimize pass changed neither
(6,980 triangles in and out, bbox identical to five decimal places).

## 8. Approval

Stage 3 gate. Presented: contact sheet, aerial day, aerial night, front elevation, and
the numbers in §1.

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION" — David, 16 August 2026

Blanket approval given with the pipeline invocation, ahead of the presentation.

## 9. Stage-5 local QA (17 August 2026)

Run in real headless Chrome over CDP against a static server on `app/dist`
(`preview_start` was out of dev-server slots — the documented escape hatch). Screenshots
are held outside the repo at the session scratchpad; the numbers below are from
`qa.json` / `qa2.json`.

| check | result | evidence |
|---|---|---|
| Re-validation of the shipped GLB | **PASS** | `validation.json`, all 16 checks, 6,980 tris, 10 objects |
| Manifest entry | **PASS** | 19 insertions, 0 deletions — appended as text, no other entry touched |
| id mapping | **PASS** | `camelId('35-south-park')` → `35SouthPark`, which is the registry id |
| Case B registry + re-bake | **PASS** | `pipeline/lib/landmarks.mjs` entry added; full chain re-baked (`terrain → bridges → buildings → streets → landcover → validate → lore → toy → notables → context → muni-shapes`) |
| audit 1.6 | **PASS** | "83 zones over 80 landmarks clear". 1.2b / 1.3c / 1.7b fail on `main` already and are unrelated |
| `verify-rebake` | **PASS** | "584 of 585 cells unchanged; 23_13 201 → 200 ← 35SouthPark"; nearest surviving footprint 10.7 m against the 6 m radius |
| Single building on the site | **PASS** | exactly one procedural footprint dropped; no twin, no baked block through the model, no z-fighting |
| Scale factor | **PASS** | `sf-assets: 35-south-park merged 10 objects / 10 materials -> batched (4759 tris body); uniform x1.0000 at 3886, -1279` — 1.0000, and the position matches the surveyed anchor to the metre |
| Orientation | **PASS** | the arcade faces north-west across the street into the park; camera preset `yaw 225` looks square onto it |
| Terrain seating | **PASS** | sits flat on the sidewalk, no float, no sink |
| Night glow | **PASS** | five lit arches with the mullion grid reading dark against them, four gold sconces; nothing else lights |
| Draw calls (AGENTS rule 2) | **PASS** | **103–105** at the landmark, **88–96** downtown, against the 300 budget. Measured by hooking `renderer.render` and taking the per-frame max — the stats overlay reads 1 because `toypost` resets `renderer.info` |
| Fallback drill | **PASS** | GLB served as a real 404: exactly one warning (`sf-assets: 35-south-park failed to load (… 404 …)`), `failed: 1`, app boots, the other 67 landmarks render, and the site is empty ground inside the exclusion zone — expected for Case B |
| lint | **PASS** | `npm run lint` clean |
| build | **PASS** | `npm run build` clean |
| Deployed QA | **not run** | batch mode — see below |

**Batch mode.** `BATCH: yes`, so the bake was run for this QA and then discarded
(`git checkout -- app/public/tiles api/_data`) and only source was committed: the GLB,
the manifest entry, the registry entry, the plan and this artifacts folder.
`git diff --name-only origin/main` lists nothing under `app/public/tiles/` or
`api/_data/`. The city is re-baked once for the whole batch by
`docs/asset-pipeline/BATCH-INTEGRATE.md`, which is also where the PR is opened.
