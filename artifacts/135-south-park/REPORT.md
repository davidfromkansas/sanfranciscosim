# 135 South Park — build report

Asset: `135-south-park.glb`. Plan: [`docs/asset-plans/135-south-park.md`](../../docs/asset-plans/135-south-park.md).
Dossier: [`REFERENCE.md`](./REFERENCE.md). Machine-readable checks: [`validation.json`](./validation.json).

**What was built.** A stylized miniature of the 1925 two-storey brick building at
135 South Park, San Francisco (block 3775, lot 033), on its measured L-shaped footprint at
its real 45° heading, with a glazed roof monitor as its identity feature and its night
state.

**REPORT beats plan.** Where this file and the plan disagree, this file is what shipped.

---

## 1. Headline numbers

| | |
|---|---|
| Objects | **10** shipped (65 as authored; stage 4 joined them per material) |
| Triangles | **3,836** shipped (4,016 as authored; cap 8,000 — 48% of budget) |
| Dimensions (X, Y, Z) | 34.45 × 25.95 × **8.500** m |
| bbox min / max Z | 0.000 / 8.500 |
| XY centre offset | 0.968, 0.667 m |
| Materials | 9, all `Toy_*`, flat, no textures, no alpha |
| Glow materials | `Toy_glassl_Glow`, `Toy_glass_Glow` |
| File | **108,524 B** shipped (247,772 B pre-optimize) — see `optimize/REPORT.md` |
| Draw submeshes | **11** shipped (66 pre-optimize) |
| Anchor | `-122.3940203, 37.7811030` |
| Target height | 8.5 m |
| Front heading | 315.4° true (NW) |

The 34.45 × 25.95 m axis-aligned XY box is the expected consequence of a 19.71 × 28.65 m
building at a ~45° heading, not a scale error. The crest lands on 8.500 m exactly, so the
loader's `targetHeightM / measuredHeight` scale is 1.0.

**On the XY centre offset.** 0.97 / 0.67 m is inside the ±1 m tolerance but not close to
zero, and that is deliberate: the origin is the footprint's **area centroid**, which is
also what the manifest `anchor` names. For an L-shaped plan the area centroid and the
bounding-box centre are ~1.2 m apart; centring on the bbox instead would have put the
building ~1.2 m off its real position in the city. AGENTS rule 5 decides it — real
coordinates win over a prettier validator number.

## 2. Contract validation

Fresh-scene re-import of the exported GLB (never the authoring scene). **16 of 16 PASS.**
Re-run after the stage-4 swap, so the table below describes the **shipped** optimized
file, not the pre-optimize one.

| Check | Result |
|---|---|
| Metres and plausible dimensions | PASS |
| Crest normalized to target (8.5 m ± 0.02) | PASS |
| Base at z = 0 | PASS |
| Centred in XY (≤ 1 m) | PASS |
| Under triangle budget | PASS — 3,836 / 8,000 |
| No image textures | PASS — 0 |
| No transparency | PASS |
| Materials follow contract | PASS — 0 violations |
| No cameras or lights | PASS |
| No animation, skinning or constraints | PASS |
| Transforms applied | PASS |
| No negative scales | PASS |
| Normals outward (per-object signed volume) | PASS — 10/10, 0 inverted |
| Normals outward (ray residual) | PASS — 0 flipped, 0.00% |
| No degenerate geometry | PASS — 0 degenerate triangles |
| No unexpected/foreign objects | PASS |

### Validator constants had to be corrected

`validate_135_south_park.py` was derived from `artifacts/380-brannan/`, and the copy
carried three of that asset's per-asset constants: its anchor (`-122.3940217, 37.7806308`),
its front heading (135.6°), and a dimension-plausibility window of 12.4–12.8 m in Z with a
symmetric 29–33 m in X and Y. This asset legitimately failed that window, and the first
validation run reported `overall: FAIL` on `meters_and_plausible_dimensions` while also
recording the wrong building's anchor and heading in its output.

Corrected to this asset's values, with the X/Y window made **asymmetric** (33.0–36.0 X,
24.5–27.5 Y) and commented, because a symmetric window would happily pass a model that had
been rotated 90° — exactly the failure a heading check is supposed to catch.

Anyone deriving the next asset's validator from a previous one should re-check these four
constants first.

## 3. Design decisions and deviations from the plan

**Masonry is `Toy_rust` (`a86444`), not the plan's `Toy_brick` (`c96f4a`).** The same swap
380 Brannan made 55 m away on the same block. `c96f4a` is saturated enough that a whole
building of it reads as an accent, and style bible §7 reserves saturation for identity;
here the identity is the roof monitor, and the walls need to be a neutral. Using the
browner value also makes the two assets read as one district (§24, structure families).

**No painted front skin.** The plan allowed for a `Toy_stone` panel on the north-west
elevation if photography showed a painted front. No photography was obtained (§5), so the
building is one masonry material on all four elevations — the lower-invention choice.

**Full `Toy_trim` coping ring, not a partial cap.** The plan proposed a coping on the front
and south-west flank only. Carried right round instead: it is what makes the roof read as a
designed ring rather than an open tray from the app's downward camera, and it is what
traces the re-entrant rear yard — the silhouette this building is recognised by.

**The north-east party wall carries no openings at all.** Not a stylistic choice: it is
shared with 123 South Park at a measured 0.0 m gap, and it is the only facade fact in the
dossier that rests on evidence rather than inference.

## 4. Revision log

### Revision 1 → 2: the roof monitor (after the first aerial review)

The style bible says to review from the high three-quarter aerial first. Doing so caught a
design failure that the elevations alone would not have:

| | rev 1 | rev 2 |
|---|---|---|
| Lid material | `Toy_roofd` `45454a` | **`Toy_trim` `f3efe6`** |
| Plan size | 11.0 × 4.2 m | **12.0 × 3.6 m** |
| Glow band | z 7.34 – 8.20 | **z 7.95 – 8.26** (revised again in rev 3, below) |

1. **The dark lid erased the identity cue.** Capping the monitor in `Toy_roofd` put a dark
   slab on a dark deck, and its 0.15 m overhang hid the `Toy_glassl` clerestory from
   directly overhead. In the rev-1 top view the monitor read as a shadowed recess rather
   than a raised lantern. The bright lid ties it to the coping ring instead, so the roof
   composition is three legible elements at thumbnail size: dark deck, bright ring, bright
   bar.
2. **It was too wide for its wing.** At 4.2 m plus overhang in a 7.75 m wing it read as a
   container filling the wing. 3.6 m leaves ~2 m of deck each side and reads as a discrete
   object. Both figures sit inside the 4–5 m the aerial imagery supports; the narrower one
   is also the better-composed one.
3. **More than half the night glow was hidden behind the parapet.** The glow shells started
   at 7.34 m while the parapet crests at 7.9 m, so from any viewpoint outside the building
   only ~0.3 m of the lit band cleared the ring. Since a lit monitor on a dark roof is the
   entire reason this asset is worth building, this was the most consequential of the
   three. The band now starts at 7.95 m, fully clear.

### Revision 2 → 3: the glow band was still clipped to the parapet

The rev-2 night render showed the fix working — four lit front bays and the monitor's
clerestory reading as a bright bar on a dark roof — but the bar was thin. The band ran
7.95–8.26 m, only **0.31 m of a 1.14 m clerestory**.

That number came from reasoning about a *side* view: start above the 7.9 m parapet so
nothing is hidden. It was the wrong frame of reference. The app's camera looks **down** at
30–50°, sees over the parapet onto the deck, and the monitor stands in the middle of a
7.75 m wing — well inside a ring that is only 0.35 m thick. Clipping the glow to the
parapet threw away two thirds of the feature for an occlusion that mostly does not happen
at the camera the asset is designed for.

The band now runs **7.35–8.26 m** (0.91 m). From the aerial the whole of it reads; from
street level the parapet still hides its lower half, which is exactly what a real
clerestory behind a parapet does. Geometry is unchanged — still 65 objects and 4,016
triangles, crest still 8.500 m.

**What was deliberately not changed: the parapet stayed at 7.9 m.** Lowering it would have
given the monitor more clearance and made the feature pop, and it was tempting. But
deck + 0.9 m is the dossier's stated inference and the 1990 parapet-strengthening permit
supports a substantial parapet; shaving a researched number to flatter a design cue is
exactly the kind of quiet fudge this pipeline's gates exist to prevent. The monitor was
fixed on its own terms instead.

**The front block's roof was left nearly empty, on purpose.** Style bible §10 says never
leave a prominent roof blank, and ~274 m² of dark membrane with one vent cowl and one hatch
brushes against that. It stays because the Esri aerial shows that half of the real roof as
an uncluttered field, with the mechanical cluster genuinely on the rear wing. Inventing a
skylight array would improve the render and falsify the building. The bright coping ring
and monitor lid carry the composition instead.

## 5. The honest caveat: the facade is unverified

**No photograph of 135 South Park's street elevation was located during this work.** Google
Maps would not render in the available browser environment; LoopNet and Yelp galleries
returned HTTP 403; the occupant's own site (`mh-a.com`) serves a certificate for a
different domain and the fetch aborted. `REFERENCE.md` §1 lists each attempt.

What this means for the asset:

| Aspect | Status |
|---|---|
| Footprint, anchor, orientation, 45° heading | **measured** — OSM way/113545684 |
| Deck 7.0 m, crest 8.5 m | **measured** — DataSF LiDAR `SF3775033` |
| 1925, 2 storeys, Industrial class, parapet | **documented** — assessor rolls + permits |
| Blank north-east party wall | **measured** — 0.0 m gap to 123 South Park |
| Roof: dark deck, raised element on the wing, cowl, rear plant | **observed** — Esri aerial ~0.12 m/px |
| Raised element is *glazed* rather than solid | **inferred** — not resolvable at 0.12 m/px |
| Front elevation: raw brick, bay count, ground-floor openings | **inferred** — typological, from the 1925 date, the Industrial class, the masonry parapet permit, and 380 Brannan's material language |

The massing is trustworthy. The facade is a reasoned reconstruction and is labelled as one
here, in `REFERENCE.md` §7, and in the plan's 2.15. One good photograph of the north-west
elevation would upgrade half of this in a single step, and is the first thing any revision
should get.

The 8.52 m LiDAR maximum is also worth restating: a 7.06 m deck plus a 0.9–1.1 m parapet
reaches 7.9–8.2 m, so the maximum alone cannot distinguish a roof monitor from the parapet
itself. The aerial decides it in favour of a raised element — a distinct lighter plane with
its own shadow, far wider than a parapet line — but whether that element is glazed is not
resolved. **It does not change the target height either way** (8.5 m is the crest
regardless), so the manifest is correct whichever reading is true. It changes the design
completely. If it turns out to be a solid mechanical penthouse, the fix is to re-plan the
night state around the front windows and re-run stage 2.

## 6. Files

| File | What it is |
|---|---|
| `build_135_south_park.py` | deterministic build; rebuilds the GLB from the measured footprint |
| `render_135_south_park.py` | review rig; re-imports and renders the **exported** GLB |
| `validate_135_south_park.py` | fresh-scene contract validation → `validation.json` |
| `make_contact_sheet.py` | composes the seven review images |
| `135-south-park.glb` / `.blend` | the asset and its authoring scene |
| `135-south-park-{north,east,south,west}.png` | four elevations, one rig, identical but for azimuth |
| `135-south-park-top.png` | plan view — the important one for this asset |
| `135-south-park-aerial.png` | the app's high three-quarter camera |
| `135-south-park-aerial-night.png` | the night state |
| `135-south-park-contact-sheet.png` | all seven |
| `optimize/` | stage-4 scripts and the byte-for-byte input copy |

The render rig is pinned to Cycles **CPU**. Metal was tried on this machine — eight asset
sessions of the batch were competing for the CPU — and the headless
`-b --factory-startup` process blocked at 0% CPU before the first tile, so the rig stays on
the path known to produce these images. The attempt is recorded in the script.

## 7. Draft manifest entry

Not applied here — integration is a separate job
(`docs/asset-plans/INTEGRATION-PROMPT.md`, Case B). `dims` and `tris` below are the
measured values from `validation.json`.

```json
{
  "id": "135-south-park",
  "file": "135-south-park.glb",
  "anchor": [
    -122.3940203,
    37.7811030
  ],
  "targetHeightM": 8.5,
  "cat": 3,
  "name": "135 South Park",
  "estimated": false,
  "dims": [
    34.45,
    25.95,
    8.5
  ],
  "tris": 3836,
  "loadRadius": 2500
}
```

`loadRadius` is the skill's default, `max(2500, 8.5 × 30) = 2500` m — the streaming
decision is explicit, per contract rule 9. Beyond that radius the carved-out site is a gap,
but an 8.5 m building at 2.5 km is far below a pixel, so the absence is illegible.

`cat: 3` (office) reflects the current use. The assessor still classes the parcel
Industrial; the building has been offices for years and the category drives the app's card
and prop vocabulary, so office is the truer runtime answer.

`camelId('135-south-park')` → `135SouthPark`, which must match the
`pipeline/lib/landmarks.mjs` id at integration or the procedural version will not be hidden
and the site will show two buildings. Verified against `app/src/assets.js`.

## 8. Stage 5 — local integration QA (batch mode)

Case B, batch mode: the bake was run in full for QA and then discarded, and only source
was committed.

| Check | Result |
|---|---|
| Re-validation of the shipped GLB | PASS — 16/16, §2 |
| Manifest entry | PASS — valid JSON, 36 entries |
| id mapping `135-south-park` → `135SouthPark` | PASS — verified against `camelId()` in `app/src/assets.js` |
| Registry entry | PASS — 42 landmarks, no duplicate ids |
| **Exclusion drops exactly one footprint** | **PASS — A/B bake: 174,755 without the entry, 174,754 with it** |
| `audit.mjs` check 1.6 | PASS — "42 landmarks clear" |
| Context tier | PASS — `landmark:135SouthPark` in `context/landmarks.json` at x 3826, z −1227.3, h 8.5 with its camera preset; present in `search-index.json` |
| Loader merge line | PASS — `merged 11 objects / 9 materials -> batched (2113 tris body); uniform x1.0000 at 3826, -1227` |
| Scale factor | PASS — **x1.0000** |
| Single building at the site | PASS — procedural stand-in excluded, GLB placed, no twin |
| Night glow | PASS — monitor clerestory + four front bays light; nothing else |
| Draw calls < 300 | PASS — 87/frame hero, 65/frame near streamed landmarks (`landmark-streaming-check.mjs`) |
| Streaming lifecycle | PASS — all 6 checks: boot/approach/depart/re-approach, zero failures |
| Fallback drill | PASS — see below |
| `npm run lint` | PASS |
| `npm run build` | PASS — 3,315 tiles 56.3 → 31.6 MB |
| Bake discarded, source only | PASS — see §9 |

**Fallback drill.** With `app/public/sf-assets/landmarks/135-south-park.glb` renamed away
and the page reloaded, the app booted, South Park rendered, and the console carried exactly
one warning:

```
sf-assets: 135-south-park failed to load (Unexpected token '<', "<!doctype "... is not valid JSON)
stats: { entries: 36, live: 18, fading: 10, failed: 1 }
```

Ten other landmarks streamed in alongside it. Case B, so the site is empty ground inside
the exclusion zone — expected, and noted here per the integration prompt. File restored and
re-verified byte-identical to the artifact.

**Audit failures that are not mine.** `audit.mjs` reports 29 pass / 3 fail / 1 info. The
three failures are **1.2b** (p95 height 13.9 m vs an expected 25–120 m band the DataSF
source cannot satisfy), **1.3c** (Telegraph Hill terrain 90.5 m from the Terrarium DEM vs a
surveyed 84 m) and **1.7b** (1 of 793 sampled trees offshore). All three live in tiers this
change does not touch, and `docs/asset-pipeline/BATCH-INTEGRATE.md` states outright that
"Checks 1.2b, 1.3c and 1.7b fail on main today; they are pre-existing and not yours."

**One honest limitation.** The in-editor preview pane hides its window, which pauses
`requestAnimationFrame`, so the LOD cross-fade never settles there and the renderer's
draw-call counter reports whatever the last partial frame did. Visual screenshots taken in
that pane are therefore not trustworthy evidence, and no claim here rests on them. The
draw-call and lifecycle results above come from `pipeline/landmark-streaming-check.mjs`,
which drives the built app in headless Chrome precisely because, in its own words,
"rendering runs continuously there, which the in-editor preview pane cannot guarantee."

## 9. Batch mode: what was committed

`docs/asset-pipeline/ADDRESS-TO-ASSET.md` "Batch mode" applies — seven other landmark
sessions were running on this machine concurrently (101 and 165 South Park, 350/358/370
Brannan, 551/599 Third). A Case B re-bake rewrites ~600 generated files whatever the
landmark was, so two such branches cannot merge.

The bake **was** run in full (terrain → bridges → buildings → streets → landcover →
validate → lore → toy → notables → context → muni-shapes) because a Case B landmark cannot
be judged without its exclusion applied, and then discarded:

```
git checkout -- app/public/tiles api/_data
```

It touched `app/public/tiles/buildings/23_13.bin`, `toy/23_13.bin`, ~590 `ctx/*.json`
sidecars, the tile indexes and `api/_data/` — all thrown away. Committed source only:

- `app/public/sf-assets/landmarks/135-south-park.glb`
- the `landmarks_manifest.json` entry
- the `pipeline/lib/landmarks.mjs` entry
- this asset plan and `artifacts/135-south-park/`

All three shared files are append-only lists that merge mechanically. The city gets rebuilt
once for the whole batch by `docs/asset-pipeline/BATCH-INTEGRATE.md`, which is also where
the single PR is opened. **Nothing was pushed.**

## 10. Integration warning: the exclusion radius is the tightest in the registry

Full derivation in the plan's 2.13. Measured from this anchor, against the metric
`excluded()` in `pipeline/buildings.mjs` actually uses — *centroid **or** any ring vertex
inside the circle*:

| | nearest vertex | centroid |
|---|---|---|
| own footprint (OSM) | 1.03 m | 3.04 m |
| own footprint (DataSF) | 4.68 m | 3.29 m |
| **nearest neighbour (OSM way/1311547493, rear)** | **6.18 m** | 12.96 m |
| nearest neighbour (DataSF `SF3775036`) | 10.32 m | 15.37 m |

`exclude: 5` satisfies both sources, with 0.3 m of headroom over our own DataSF vertex and
1.2 m below the nearest neighbour. **Verify it empirically against the re-bake** — dropped
procedural footprints must be exactly one, and `pipeline/audit.mjs` check 1.6 must pass. If
the count is 0 the radius is under our own ring; if it is 2 or more it is eating a
neighbour.
