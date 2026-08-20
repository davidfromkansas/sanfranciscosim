# Pier 1 — build report

`pier-1.glb`, built by `build_pier_1.py` (Blender 5.2.0 LTS, headless), rendered by
`render_pier_1.py`, validated by `validate_pier_1.py` against a fresh re-import of the
exported file.

**REPORT beats plan.** Where this file and `docs/asset-plans/pier-1.md` disagree, this one is
what was built and why.

## 1. Numbers

| | |
|---|---|
| Objects | 792 authored, 13 shipped (joined per material at stage 4) |
| Triangles | 13,330 (cap 24,000) |
| Dimensions (axis-aligned) | 215.43 × 185.43 × 15.40 m |
| Vertical extent = `targetHeightM` | **15.400 m** — loader scale 1.0000 |
| bbox min Z | **−2.60 m** (deliberate, see §2) |
| bbox max Z | +12.80 m (pavilion apex) |
| XY centre offset | 0.000, 0.000 |
| Manifest anchor | **−122.3941164, 37.7974191** |
| Long-axis heading | 053.77° true; facade normal 233.77° |
| Shipped GLB | **329.2 KB** raw (158.6 KB gzip), meshopt-compressed at stage 4 |
| Pre-optimize GLB | 1,052.1 KB raw — archived at `optimize/input/pier-1.glb` |
| Draw submeshes | **16** (798 before stage 4) |
| Contract validation | **PASS**, all 18 checks, re-run on the SHIPPED (optimized) file; 0 / 17,425 flipped ray hits; 74 / 74 glow faces outward; no inverted solids |
| Materials | 11 `Toy_*`, of which 2 `_Glow` |

The axis-aligned XY box is 215 × 185 m for a pier that is 234 × 55 m. That is the expected
consequence of a 53.77° real-world heading, not a scale error.

## 2. The origin rule, and why `min Z` is negative

This asset deliberately breaks the contract's "geometry sits on z = 0".

`placeGeneric()` in `app/src/assets.js` takes **one** terrain sample at the anchor and puts
the GLB's origin there. Over the Bay that sample is not the ground the building stands on —
except that the app's Terrarium DEM already carries this pier as a ~2.1–2.5 m ridge along its
centreline, with water (0.0) either side and past the tip. Sampled directly from
`app/public/tiles/terrain.bin`:

```
along     -40   -20     0    20    60   100   140   180   200   220
perp   0  3.0   2.8   2.2   2.1   2.2   2.1   2.2   2.1   0.7   0.0
perp  20  2.9   2.5   2.3   2.5   2.5   2.4   2.0   1.5   0.7   0.0
perp  40  2.9   2.9   2.0   1.8   1.0   0.5   0.1   0.0   0.0   0.0
```

That ridge is the app's stand-in for the pier deck, and it is within half a metre of the real
deck elevation (~2.9 m). So **local Z = 0 is the top of the pier deck**, and the deck fascia
and pile stubs run down to −2.6 m. Placed at the anchor the deck lands at ~2.4 m world and
the pile stubs reach ~−0.2 m — just under the water plane, where they belong. At the tip,
where the DEM has fallen to 0, the deck correctly reads as standing 2.4 m out of the water on
piles.

Consequences, all recorded in `validation.json`:

- `targetHeightM = 15.4` is the **vertical extent** (−2.6 to +12.8), not a height above water
  and not an architectural height. Same convention as `64-south-park`.
- `min_z_m = −2.6` is a **PASS**. `validation.json` replaces the usual `base_at_z_zero` check
  with `deck_plane_at_z_zero` and `sub_deck_depth_expected`, and carries an
  `origin_convention` string saying why.
- Dropping this model onto z = 0 would raise the whole pier 2.6 m. Don't.

The bulkhead end sits over terrain of ~2.8–3.0 m while the model's deck lands at ~2.4 m, so
the bulkhead's plinth is buried by ~0.5 m at the Embarcadero. That is the right way round
(buried, not floating) and the 0.8 m plinth absorbs it.

## 3. Corrections to the dossier

Four, all re-measured during this build and carried into `REFERENCE.md` §8:

1. **The roof was inverted in the plan.** The plan described a 9 m monitor spine with two
   8.4 m solar fields flanking it on the *low* roof. The georeferenced ortho cross-section
   (three stations, 0.08 m/px) shows the opposite: 12.7 m of flat white roof, a 0.6 m hard
   shadow line, then a **raised spine ~9.5 m wide whose top carries a single ~7 m array**,
   then 12 m of flat white roof. Built as measured. The first build followed the plan and
   the aerial read as a hangar with a ridge instead of a striped flat roof.
2. **Spine height 2.3 m, not 2.7 m.**
3. **Wing parapet 8.4 m** (plan: 8.6) and **pavilion entablature 10.3 m**, from a cleaner
   photogrammetric pass. The 12.8 m pavilion apex is unchanged.
4. **The arch is 9.6 m wide with its springing at 4.35 m**, not ~10 m springing at 5.5 m. The
   plan's springing was the archivolt's outer edge, which would have made the opening
   segmental; it is a semicircle. Modelled at 10.4 m wide (enlarged per style bible §8/§9)
   with the springing at 4.4 m, crowning at 9.6 m, clear of the 10.3 m entablature.

## 4. Build iterations

| # | Problem | Fix |
|---|---|---|
| 1 | The parapet coping was a solid slab over the whole roof, burying the roof deck | `rim()` — a closed ring band, offset inward by `offset_polygon()` |
| 2 | Every shed window was buried inside the wall solid; the flanks rendered blank except on the bays whose glow quads happened to have the sign right | `out` is the OUTWARD direction, so proud is `p_wall + out*d`. The build had it as `p_wall − out*d` |
| 3 | The "window frame" was a solid navy slab standing proud of the glass, hiding it, and the flank read as a picket fence | One dark glazing panel poking 0.02 m proud with a single light steel transom across it |
| 4 | 6 m of glass in a 7.5 m bay ran the openings into one another; the flank read as a continuous glazed ribbon | 4.5 m of glass, 3 m of solid pier |
| 5 | The pediment was extruded the full 13.6 m depth of the bulkhead and read as a gabled hall | Everything above the wing parapet is a 2.7 m screen |
| 6 | The arch was recessed *into* a solid and was therefore invisible | A dark panel 0.06 m proud with the archivolt 0.25 m proud of that; the ring's own shadow reads as the reveal |
| 7 | `PIER · 1` was white-on-white and unreadable | Slate blue, extruded 0.22 m, 1.45 m cap height |
| 8 | The day renders showed every lit surface as a flat tan panel | `fade_glow()` looked the Principled node up by *name*; the glTF importer does not always use that name. Now found by type — and the 12% day blend is baked into the base colour rather than set as alpha, because EEVEE's blended render method needs more than one property |
| 9 | The top view rendered the pier diagonally across a 2600×900 frame and cropped both ends | For a top-down camera image-right maps to world `(cos rz, sin rz)`, so `rz = 90 − AXIS` |
| 10 | The deck stepped out to meet the bulkhead's own 50.6 m face and left a wart beside the frontispiece | The SE deck edge runs as one converging line |
| 11 | Night render at emission strength 3.0 blew the cool clerestory to flat white | 1.8 — the app's night layer draws `_Glow` at its own base colour with no multiplier, so a strong push here would flatter a wrong colour |
| 12 | `shed_cope` was inside-out — the parapet band was hand-wound and flipped on the taper's concave corner | `rim()` now lets bmesh settle the winding; the band is a closed manifold shell |
| 13 | `voussoirs` had no usable signed volume: the archivolt was built as a radial quad at *every* profile index — a stack of internal partitions — with its two springing ends left open | Rebuilt as two longitudinal surfaces (soffit + extrados) plus two end caps |
| 14 | One glow quad faced inward, and every facade glow quad was wound backwards without it showing in any render (nothing here culls back faces) | `glow_quad()` now takes the real outward direction as a `(da, dp)` vector and **checks** its own winding against it, instead of deriving it from a ±1 flag |

Iterations 12–14 were all found by `validate_pier_1.py`, not by looking at renders,
and the ray residual fell 1.43% → 0.19% → **0.00%** across them.

## 5. Night state

Authored from Base Color, not from an emission boost, because glTF writes `emissiveFactor = 0`
for an authored strength of 0 and a re-imported `_Glow` material otherwise carries a default
**white** emission.

- **Hero:** the arched lunette and the door screen behind it — one warm pale glow (`f4dcb0`)
  filling the arch. From the Embarcadero this is the whole identity at night.
- **Supporting:** the ground-floor shopfront band along the Embarcadero facade, same hue.
- **Accent:** roughly half the shed's clerestory bays, in a scattered pattern
  (`LIT_PATTERN` in the build script), cool (`cbd8e0`) so they sit under the arch rather than
  competing with it. An office building at night is not uniformly on, and a fully-lit 213 m
  clerestory would out-shout the frontispiece.
- **Not lit:** roof, solar arrays, apron, deck, piles, vents, lamps.

Every glow surface is an **open, single-layer, outward-facing quad**, never a closed shell:
the app draws `_Glow` in a separate translucent layer and a closed box shows its front *and*
back face, reading at roughly twice the intended day alpha.

By day each glow colour sits in the same family as its non-glow neighbour, which is why the
lit glazing is a warm pale rather than a saturated yellow.

## 6. Known limitations

1. **The roof spine is the least-verified element in the asset.** No photograph shows it —
   every street-level view is from an apron whose parapet hides the roof. Its existence and
   its 2.3 m height are a shadow measurement corroborated by the 3.1 m gap between DataSF's
   LiDAR median (9.66 m) and its max (12.73 m). If it turns out to be solar racking rather
   than a monitor the roof loses 2.3 m of relief; `targetHeightM` is unaffected, because the
   pavilion sets it.
2. **The shared-rig `-west.png` and `-east.png` elevations are small by construction.** One
   orthographic scale has to cover a 234 m asset, so the 64.7 m facade and the 26.5 m end
   wall occupy a fraction of the frame. That is the price of the contract's "four elevations
   share one rig"; `-facade.png` is the frame to judge the frontispiece from.
3. **Bay counts are inferred**, from oblique Street View where the far end of every run is
   foreshortened to nothing.
4. **The pier deck elevation is inferred**, not sourced.
5. **The build date is contested** (1918 vs 1931); both are recorded rather than resolved.
6. **No flagpole.** Deliberate — see `REFERENCE.md` §7.

## 7. Optimize (stage 4)

Full report: `optimize/REPORT.md`. Headline: 1,052.1 → **329.2 KB** raw (−68.7%, target
60%) and 798 → **16** draw submeshes, with triangles unchanged at 13,330 — the whole win
is object-count overhead, which is what a 792-object procedural build costs. All gates
G1–G6 and G8 PASS (G7 n/a, no bake); worst appearance delta 0.40% against a 2% gate.

One judgment call: the **limited dissolve was skipped**, per `GLB-OPTIMIZE-PROMPT` §3
step 3. This asset is built from long coplanar ring bands — the 234 m deck slab, the shed
plinth, the parapet coping annulus, the 200 m monitor spine — and dissolving those emits
slivers that no area-based test catches and that only surface after the shipping swap.

The stage-2 contract validation above was re-run on the optimized file, not inherited from
the pre-optimize build.

## 8. Local QA (stage 5)

Run against `npm run dev` on the re-baked tiles, at the Embarcadero.

| Check | Result |
|---|---|
| Merge line / scale | `uniform x1.0000 at 3818, -3031` — the authored vertical extent and `targetHeightM` agree exactly |
| Seated height | placed at **y = 2.44 m**, the DEM ridge at the anchor. The deck lands at 2.44, the pile stubs reach −0.16 m, just under the water plane — the origin decision in §2 works as designed |
| One building, no twin | PASS — the frontispiece stands clear on the Embarcadero with no procedural slab through it. This is what the second exclusion zone exists for and it is invisible from the aerial camera |
| Orientation | PASS — the arched facade faces the Embarcadero at 233.8° |
| Footprint against neighbours | PASS — the pier reads at the right length against Piers 1½/3 and the Ferry Building |
| Night glow | PASS — the arch reads warm amber, the shopfront band supports it, the clerestory bays are cool-white dashes up the flank. Confirmed **in the app**, whose night layer draws `_Glow` at its raw base colour with no multiplier |
| Draw calls | **73** with 74 landmarks live, against a 300 budget |
| Asset states | 91 entries, 0 failed |
| Lint / tests | `eslint` clean; `npm test` 26/26 pass |
| Fallback drill | PASS — exactly one warning (`sf-assets: pier-1 failed to load …`), app still boots, 73 other landmarks live, and the Case B site is empty deck |
| Audit 1.6 | PASS — 101 zones over 97 landmarks clear |
| Audit 1.2b / 1.3c / 1.7b | FAIL, **pre-existing on main** — `BATCH-INTEGRATE.md` line 124 says so, and `135-south-park`'s report records the identical three with identical values |
| `landmark-streaming-check` boot / hero draws / stream-in | PASS — far 73 / live 18; avg **184** draw calls per frame |
| `landmark-streaming-check` stream-out | FAIL (times out), and **pre-existing** — see below |

**The streaming check's stream-out step fails, and it is not this asset's.** Verified by
running the identical check against a build of `main` with no Pier 1 in it:

| Step | main (90 entries) | this branch (91 entries) |
|---|---|---|
| boot keeps streamed unloaded | PASS — far 72 / live 18 | PASS — far 73 / live 18 |
| hero draw calls | PASS — avg 182/frame | PASS — avg 184/frame |
| streamed landmark loads on approach | PASS | PASS |
| streamed landmarks release on depart | **timed out** — far 20 / live 70 | **timed out** — far 20 / live 71 |

Same failure mode, same numbers to within the one entry Pier 1 adds. The step asserts that
`live` FELL after flying away, but the departure target (the Ferry Building) is itself
inside the radius of enough other streamed entries that the count never drops. Nothing to
do with this landmark.

**Two QA notes for whoever runs this next.**

1. **The Browser pane is backgrounded between tool calls, which throttles rAF**, so the
   streaming scan barely ticks and every streamed landmark sits in `far` forever. That is
   an artefact of the harness, not of the asset — one manual `SF.assets.update(camera, dt)`
   promoted 18 entries immediately. Pump it with a `setInterval` for the duration of QA.
   Same cause makes `renderer.info.render` report a partial frame; force one
   `SF.renderer.render(scene, camera)` and read it straight after.
2. **`verify-rebake` reports 23_9 as "exclusion dropped nothing (no footprint in the source
   data?)"** and that is wrong. It compares per-cell COUNTS, and the count is 17 either way
   because two footprints were dropped while two others shifted in from the data snapshot.
   Decode the tile. It also flags cell 23_13 as a stray; a control bake with `pier1` removed
   from the registry produces the identical 169 → 182 change, so that is the
   `pipeline/data` vintage, not the radius.

## 9. Integration

Case **B**. The registry entry, the two-zone exclusion and its verified drop set live in
`docs/asset-plans/pier-1.md` §2.13, which also names the collateral. Do not re-derive the
exclusion radius from the half-diagonal rule: one Overture polygon traces both Pier 1's
Beaux-Arts facade and Pier 3's bulkhead, and the solved zone list is what keeps the
frontispiece from being buried under a 14.4 m procedural slab.

Draft manifest entry:

```json
{
  "id": "pier-1",
  "file": "pier-1.glb",
  "anchor": [-122.3941164, 37.7974191],
  "targetHeightM": 15.4,
  "cat": 3,
  "name": "Pier 1",
  "estimated": false,
  "dims": [215.4314, 185.4287, 15.4],
  "tris": 13330,
  "loadRadius": 3000
}
```
