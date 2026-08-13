# 505 Van Ness Avenue — build report

**Governor Edmund G. "Pat" Brown Building** (California Public Utilities
Commission HQ), San Francisco Civic Center. Stage 2 of
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run from
`docs/asset-plans/505-van-ness.md`.

**This report beats the plan.** Where a number here differs from the dossier,
this one was measured on the asset that actually exists.

## What was built

> **Shipped numbers.** The figures below are the **pre-optimize** build. The
> file that ships is the stage-4 output: **18,774 triangles, 13 objects,
> 449,024 bytes**, same bbox. See `optimize/REPORT.md`.

| | |
|---|---|
| Shipping file | `505-van-ness.glb` |
| Triangles | **19,122** (plan budget 20,000; contract cap 27,000) |
| Objects | 190 |
| Bbox | **124.226 × 95.319 × 27.000 m** |
| Anchor (origin) | **lon −122.4212915, lat 37.7804835** |
| Entrance heading | 126.3° true (ESE) |
| Materials | 12, all `Toy_*`, all project palette, no extension |
| Glow materials | `Toy_glass_Glow`, `Toy_trim_Glow` |
| Blender | 5.2.0 LTS, headless |

## Corrections to the dossier

1. **The light court is ~39 × 39 m, not 39 × 21 m.** The plan's §2.5 misread the
   OSM inner-ring bbox: Δlat 0.000354 → 39.1 m and Δlon 0.000447 → 39.3 m. The
   court is square-ish. Modelled as a chamfered octagon at r = 18 m, pulled in
   from the survey so the surrounding wings keep a believable depth.
2. **The asset bbox is 124.2 m wide, not the 113.4 m footprint width.** The
   entrance stair projects ~12 m past the drum. The plan's draft manifest
   `dims` were the footprint, not the asset; the real measured dims are above
   and are what the manifest entry uses.
3. Everything else in §2.2–2.4 (anchor, ring, arc radius, heading, 27.0 m crest)
   survived re-verification unchanged.

## Deviations from the contract, and why

- **Front does not face −Y.** The asset is authored in true-world orientation
  (+Y north, +X east) because `placeGeneric()` never rotates; the entrance faces
  126.3°. This is the standing exception recorded in
  `docs/asset-plans/README.md` ("Orientation note that applies to every plan"),
  and AGENTS rule 5 makes real-world orientation win.
- **Origin is the footprint centre, not the full-asset bbox centre.** Centring
  on the full bbox would slide the building ~4.6 m west of its true coordinates
  to compensate for a stair that exists on one side only. `validate_505_van_ness.py`
  allows |centre.x| ≤ 6 m and carries a `centering_note` explaining it;
  |centre.y| is within 1 mm.

## Iteration log

**Pass 1 — massing.** 34,280 triangles, over the contract cap. Aerial review:
the massing, drum, court, fascia lid and stair all read, but three failures.

- *The facade was a horizontal barcode.* Six strong blue ribbons with nothing
  vertical; the real building is emphatically vertical, ordered by heavy rounded
  precast piers. The piers existed but were too small and too shy to win.
- *The Great Seal was invisible.* **Bug:** the medallion was built with its width
  along the wall **normal** instead of the arc **tangent**, so it rendered
  edge-on as a hairline inside the entrance bay.
- *The roof was a bare tray* — a large dark field with one mechanical row, which
  style bible §10 explicitly forbids for a building the camera looks down on.

**Triangle census** (the cuts that got 34,280 → 13,202):

| Group | Before | Action | Saved |
|---|---|---|---|
| `step*` | 7,420 | arc seg 18 → 10, and no bevel — a bevel on a thin slab was 86 % of its cost | 6,830 |
| `piercap*` (49 boxes) | 5,292 | replaced by ONE continuous `pier_capband` ring; identical at the app's camera | 5,292 |
| `plinth`/`fascia`/`coping` | 5,400 | 2-segment → 1-segment bevel | 2,700 |
| `pier*` | 5,292 | spacing 8 → 10 m, 1-segment bevel | ~1,100 |
| `seal_*` | 1,610 | 20 → 14 segments | ~500 |
| skylights | 1,728 | 8 clusters → 5 | 648 |

**Pass 2 — identity.** Seal frame bug fixed. Piers 2.1 → 2.7 m wide, 0.55 → 0.75 m
proud, spacing back to 8.5 m; glazing band shortened (1.00–2.95 → 1.15–2.60
within each floor) so precast, not glass, is the dominant surface. Roof
populated. Seal lifted to its real storey and the bay tightened 15.0 → 11.5 m.
Result: 17,334 triangles, and the facade now reads vertical.

Two new defects visible in that render:

- *Three roof volumes rendered pure black.* The penthouse, plantroom and
  liftroom each had a trim cap whose **top face was coplanar with the body's
  top face**. Fixed by dropping each body below its cap.
- *Two roof props were lying on the pavement beside the building.* Hand-typed
  coordinates.

**Pass 3 — placement made structural.** Rather than nudging the eight bad
coordinates, roof props are now **derived from the footprint**: a deterministic
6.5 m grid filtered by `on_roof()` (inside the ring less 5.5 m, outside the
court plus 5.5 m), with the four named volumes snapped to the nearest valid
candidate. 61 candidates survive on the deck. This is why the hand placement
failed — **the north edge falls 17 m across the building's 105 m length**, so
"y = 37" is comfortably inside at the east end and out over the pavement at the
west end. The court also got a floor (the boolean had cut clean through).

Final: all roof props on the deck, no black faces.

**Pass 4 — the night state.** The first night render came back with the seal as
a solid white blob. The glow shell was built as a **disc**, and the app drives
the glow layer to `opacity = 0.12 + 0.95·uNight`, so at full night it went
opaque white and erased the very feature it exists to announce. Rebuilt as an
annulus (r 3.30 → 4.05), which reads as a lit ring with the blue field and gold
rim still legible. Final: **19,122 triangles**.

## Height: corroborated after a scare

The plan carried 27.0 m as *estimated* from OSM. While sizing the exclusion zone
the baked tile appeared to contradict it with `topY = 50.0 m`, which would have
made the model 46 % too short. It does not: `topY` is **absolute roof elevation**,
and the height is `topY − baseY` = 50.0 − 21.3 = **28.70 m**. Independently,
DataSF's 2010 LiDAR carries `gnd1st_delta = 26.53 m` for this footprint. So:

| Source | Height |
|---|---|
| OSM `height` tag (+ `building:levels=6`) | 27.0 m |
| DataSF 2010 LiDAR `gnd1st_delta` | 26.53 m |
| Baked pipeline (`topY − baseY`) | 28.70 m |

Three independent figures inside a 2.2 m band. **27.0 m stands.** The manifest
still carries `"estimated": true` because no *published* architectural height
(architect statement, Wikidata claim) was found — corroborated is not published.

## Design decisions worth keeping

- The measured 8-chord arc was **refitted to a least-squares circle** (centre
  (9.81, 8.05), r = 46.86 m) and resampled to 14 segments. An 8-chord polyline
  reads as a facet, and this curve is the entire silhouette.
- **Recess by projection, not by reveal.** No booleans on the facade: ribbons
  sit 60 mm proud, piers 750 mm proud, so the ribbons read as recessed between
  them at a fraction of the cost.
- **One boolean, and it earns its keep** — the light court, which turns the body
  into a genuine ring so the downward camera sees a real well with its glazed
  stair tower.
- **The seal is exaggerated to ~8 m** (real ≈ 4 m) so it survives the aerial
  camera. It and the dark fascia lid are the only non-neutral elements on a
  124 m building.
- **The plaza ships with the building** — the concentric stair, two drum
  pedestals and two flagpoles are as recognisable as the facade.

## Night state

`_Glow` shells stand proud of the opaque glazing, never a primary surface (the
app renders the glow layer at ~12 % alpha by day, so the day renders fade them
to 0.12 to judge what the app actually shows):

- `Toy_glass_Glow` — lit ribbon panels, every third bay, floors 2/3/5.
- `Toy_trim_Glow` — entrance soffit, lintel band, and the **seal ring**, which
  is what keeps the identity legible after dark.

## Validation

See `validation.json` — fresh factory-reset scene, re-imports the exported GLB
only, and gates on: metres and plausible dims, crest normalized to 27.000,
base at z = 0, centring, triangle budget, no textures, no transparency, all
materials on contract, no cameras/lights/animation/skins, transforms applied,
no negative scales, per-object signed volume positive (authoritative for a union
of interpenetrating solids), 31,500-ray visibility residual ≤ 0.15 %, no
degenerate geometry, no foreign objects.

## Stage 3 — approval

Granted in advance by David, 12 Aug 2026, verbatim:

> "Do it on a new branch and PR -- i approve all stages just proceed"

## Stage 5 — integration evidence (Case B)

| Item | Result |
|---|---|
| Registry entry | `505VanNess` in `pipeline/lib/landmarks.mjs`, `exclude: 13.5` |
| Manifest entry | `505-van-ness`, `cat` 18, `loadRadius` 2500, `estimated: true` |
| id round trip | `camelId('505-van-ness')` = `505VanNess` — matches the registry |
| Re-bake | buildings **174,770 → 174,769**; only cell `18_13` changed count (96 → 95) |
| Files changed | 584 = 3 target-cell binaries + 9 index/manifest JSONs + 572 `ctx` sidecars |
| **Audit 1.6** | **PASS** — "no procedural footprint inside a bespoke landmark exclusion zone — 29 landmarks clear" |
| Other audit failures | 1.2b, 1.3c, 1.7b — **pre-existing on main**, unrelated to this change |
| App build | clean; `dist` 880.59 kB js / 244.86 kB gzip |
| Streaming check | **all PASS** — 23 entries, 0 failed, boot/approach/depart/re-approach |
| Draw calls | 153/frame hero, 64/frame near streamed landmarks (iron-rule budget 300) |

### The exclusion radius is 13.5 m, and that is not a typo

`excluded()` drops a whole footprint when its centroid **or any single ring
vertex** falls inside the radius. Measured against the committed
`buildings/18_13.bin`:

| Footprint | Nearest vertex to anchor |
|---|---|
| this building (6,339 m², matches the 6,263 m² survey) | **12.7 m** |
| a separate neighbour to the south-west (1,296 m²) | **14.4 m** |
| City Hall | 58.2 m |

12.7 < r < 14.4 is the only window that clears this building and spares the
neighbour. A centroid-only reading (12.0 m vs 36.3 m) would suggest a
comfortable 30 m and silently delete a real building — the plan's proposed 70 m
would have done exactly that. One vertex inside removes all 6,339 m², so 13.5
does the full job, and the re-bake's −1 building count confirms it.

### Fallback drill

Renamed `dist/sf-assets/landmarks/505-van-ness.glb` away and re-ran the
streaming check. **The app did not crash**: boot passed, the other 22 landmarks
loaded, draw calls stayed at 153/frame, and the entry reported `failed: 1`. The
check *harness* then timed out waiting for stream-out, because a failed entry
never transitions to `fading` — a limitation of the harness, not an app failure.

Honest caveat, and it is inherent to every Case B landmark here: because the
procedural footprint is now excluded from the bake, the fallback for a missing
GLB is an **empty site**, not a procedural stand-in. AGENTS rule 3 is satisfied
in the sense that matters — no hole in the render loop, no crash, one warning —
but there is no code-built version of this building to fall back to, exactly as
`INTEGRATION-PROMPT.md` describes for carved-out landmarks.

### Not done

Browser QA on a running dev server was **not** performed: five dev servers from
other concurrent agent sessions were already occupying the per-folder limit and
they were not mine to stop. Verification was done headlessly instead — a
production build plus `pipeline/landmark-streaming-check.mjs`, which drives the
built app in headless Chrome and walks the full load/fade/release lifecycle.
That tool exists precisely because the procedural fallback hides loader failures
from visual inspection, so it is the stronger check of the two, but it does not
replace looking at the building in situ. Deployed QA has not been run.

## Reproduce

```bash
blender -b --python build_505_van_ness.py
blender -b --python render_505_van_ness.py
blender -b --python render_505_van_ness.py -- --night
blender -b --python validate_505_van_ness.py
python3 make_contact_sheet.py
```

`render_505_van_ness.py -- --fast` renders the aerial alone at 20 samples; the
full rig is ~20 minutes on CPU Cycles and design iteration does not need it.
