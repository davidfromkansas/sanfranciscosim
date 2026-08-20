# Orpheum Theatre — build report

`artifacts/orpheum-theatre/` — a validated miniature GLB of the Orpheum Theatre,
1192 Market Street, for the SF toy-diorama city. Built 19 August 2026 from
`docs/asset-plans/orpheum-theatre.md`; the dossier that governs it is
[`REFERENCE.md`](./REFERENCE.md), and where dossier and plan disagree the dossier wins.

## Shipped numbers

| | |
|---|---|
| File | `orpheum-theatre.glb` |
| Triangles | **7,193** (cap 24,000) — 7,200 as authored, meshopt-packed |
| Objects / draw submeshes | 11 (242 as authored, joined per material by the optimize pass) |
| Dimensions | **67.651 x 77.623 x 27.200 m** |
| Min Z / XY centre | 0.000 / (0.000, 0.000) |
| Size on disk | **193,912 B** raw, 119,175 B gzip (pre-optimize 488,736 B raw) |
| Materials | 11, all `Toy_*`; 2 glow (`Toy_white_Glow`, `Toy_mustard_Glow`), both shipping at emission strength 0 |
| Textures / transparency / cameras / lights / animation | 0 / 0 / 0 / 0 / 0 |
| Normals | PASS — 0 inverted solids by per-object signed volume; ray test 0.0 % flipped over 22,500 first hits |
| Degenerate triangles | 0 |
| Heading | Market frontage 45.9° cw from true north, authored world-true (`+Y` = north) |
| **Anchor** | **−122.4146087, 37.7793182** |
| **targetHeightM** | **27.2** — stage-house roof, LiDAR `hgt_max`, normalised so the loader's scale lands at 1.0 |
| Validator | `validation.json`, overall **PASS**, all 15 checks true |

## What it is

The Market Street show front in cream terra-cotta over a round-arched ground arcade,
under a projecting red mission-tile pent roof: three glazed storeys and a 24.3 m parapet
on the Hyde/chamfer/SW-Market block, stepping down to two storeys and 17.5 m on the
north-east wing. Between them the crested entrance bay carrying the **vertical ORPHEUM
blade sign** (crown 26.0 m) with the marquee at its foot and the poster panel to its
west. Behind: a light-silver hipped auditorium roof, a mechanical valley, and the 1998
stage house standing clear at the north-east corner at 27.2 m — the model's bbox top.

Night set is deliberately two surfaces: **hero = the blade sign's bulb letters and crown
lamps** (`Toy_white_Glow`), **supporting = the marquee chase line and its warm soffit**
(`Toy_mustard_Glow`). The offices stay dark — a theatre's offices are dark at curtain,
and 60 m of lit windows would out-shout the Main Library across Hyde. The letters are
separate raised pucks on a non-glow ground, never a closed glow shell.

## Files

| File | What |
|---|---|
| `build_orpheum_theatre.py` | deterministic build; `blender -b --python build_orpheum_theatre.py` |
| `render_orpheum_theatre.py` | the eight review renders, always from the re-imported GLB |
| `validate_orpheum_theatre.py` | fresh-scene contract validation → `validation.json` |
| `make_contact_sheet.py` | composes `orpheum-theatre-contact-sheet.png` |
| `orpheum-theatre.blend` / `.glb` | source scene / shipped asset (meshopt-packed by stage 4) |
| `optimize/` | stage 4: the four-variant table, gates, A/B renders, and the pre-optimize archive at `optimize/input/` |
| `orpheum-theatre-{north,east,south,west,top,aerial,night,night-market}.png` | reviews |
| `qa-app-{day,night,wide}.png`, `qa-fallback-drill.png` | stage-5 local QA in the running app |

The four elevations share one rig — same orthographic scale, framing, lighting, exposure
and projection — and differ only in azimuth. **The Market front bears 45.9° and faces
south-east**, so it is split between the "south" and "east" elevations and is seen square
only in the aerial and night views. That is the site, not a rig error.

## Stage 4 — optimize

488,736 → **193,912 B** raw (−60.3 %), 242 → **11** draw submeshes, appearance
identical within 0.03–0.21 % mean RGB across day/night × near/far and the four
elevations. Weld on, limited dissolve **off** — the dissolve buys 0.4 % of raw bytes
and is the one Phase B step that can manufacture slivers on an asset built from
coplanar ring bands. Full table, gates and toolchain in
[`optimize/REPORT.md`](./optimize/REPORT.md).

The pass also surfaced a build bug it did not cause: a zero-area triangle in
`low_cap` from the collinear mid-edge inserts (`M1`, `M2`, `HM`) that the glTF
exporter triangulates out of the cap n-gon. Fixed in the build script
(`collinear_drops`), which took the asset from 7,496 to 7,200 authored triangles,
and every gate was re-run from scratch on the rebuilt pair.

## Corrections made during the build

Ten, all recorded in `REFERENCE.md` §7. The ones that would bite a future editor:

1. **OSM's `height=46 m` is the roof's absolute NAVD88 elevation in feet, converted to
   metres and mistagged.** The real height above ground is 27.19 m. Do not "restore" it.
2. **The anchor is the exported model's AABB centre, not the footprint's** — 3.0 m east
   of the plan's value, because the 1.2 m tile eave and the 4.2 m marquee and blade
   overhang the Market sidewalk and the loader places the GLB origin, which the contract
   puts at the model bbox base-centre. The build script prints the shipped anchor.
3. **There are no booleans in this pipeline.** The first pass built the arcade and
   windows as recessed prisms; they were buried inside the wall solid and rendered as
   nothing. Every opening is now applied proud, with depths increasing outward
   (pier 0.12 < reveal 0.08 … glass 0.18) so no surround shadows what it surrounds.
4. **Mixed per-edge wing insets are only safe across near-right-angle corners.** 13 m
   behind Market against 6 m behind the 13 m chamfer — the two offset lines meet at 34° —
   put the miter 12 m outside the building and inverted the band. Uniform 10 m then
   collapsed the chamfer's inner edge to 0.4 m. 7 m ships.
5. **The concave north-east step-out is its own solid.** Any polygon containing it
   self-intersects under an inward offset, and it carries the site's northernmost point.
   `CORE` + `NE_ANNEX` reproduces the real outline exactly; clipping it would have lost
   5 m of building and straightening the flank would have trespassed on 1170 Market.
6. **The blade sign's beads run down its long edges, not beside the letters.**
   Full-height trim strips on the faces made the sign read near-white by day.
7. **The camera preset is `yaw: 0` (due south), not `yaw: 44` (south-east).** The sign's
   faces point NE and SW; from the south-east the hero cue is edge-on.
8. **`Toy_roofd` renders near-black in the app.** The first local QA showed the roof
   deck as a hole in the block. Decks are now `Toy_steel`, the auditorium hip
   `Toy_stone`, and `Toy_roofd` survives only on the small machinery units. Caught in
   the running app, not in a render — the Blender rig is more forgiving than the
   diorama light.

## Gate 3 — approval

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"
> — David, 19 August 2026, in the session prompt

Recorded verbatim as the standing approval for stages 3, 4 and 5. Stage 5 still stops
before push/PR/deploy, per `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

## Stage 5 — integration (Case B, batch mode)

Ran `docs/asset-plans/INTEGRATION-PROMPT.md` Steps 1–6. Step 7 is replaced by a stop:
nothing is pushed, no PR, no deploy.

| Step | Result | Evidence |
|---|---|---|
| 1 Re-validation | **PASS** | `validation.json`, overall PASS, all 15 checks; 7,193 tris, 11 objects, 0 degenerate, 0 invalid loop normals, dims 67.6506 × 77.6234 × 27.2, min Z 0.0, centre (0, 0) |
| 2 Asset in place | **PASS** | `app/public/sf-assets/landmarks/orpheum-theatre.glb`, 193,952 B, integrated as the stage-4 output, not re-exported |
| 3 Manifest entry | **PASS** | appended as text (a `json.dump` rewrite would renumber `11.0` → `11` across other entries); 19 inserted lines, nothing else in the file touched; manifest now 104 entries |
| id → camelId round trip | **PASS** | `orpheum-theatre` → `orpheumTheatre`, which is the `pipeline/lib/landmarks.mjs` id |
| 4 Registry entry | **PASS** | `orpheumTheatre`, `exclude: 20`, `camera: { distance: 380, yaw: 0, pitch: 22 }`; 44 inserted lines, all inside `LANDMARKS` |
| 4 Re-bake | **PASS** | full chain: terrain → bridges → buildings → streets → landcover → validate → lore → toy → notables → context → muni-shapes. 174,682 buildings into 585 cells |
| 4 `verify-rebake` | **PASS** | "only the new landmarks' cells moved"; cell 20_13 184 → 183, cell 19_13 unchanged; nearest surviving footprint 27.5 m vs the 20 m radius |
| 4 Penetration check | **PASS** | exactly one baked ring has a vertex within 70 m of the anchor (City College, 1170 Market, nearest vertex 27.54 m) and **zero of its vertices fall inside the modelled footprint** — the party wall is a party wall, not an intrusion |
| 4 `audit.mjs` 1.6 | **PASS** | "no procedural footprint inside a bespoke landmark exclusion zone — 114 zones over 110 landmarks clear" |
| 5 Single building | **PASS** | one building on the site; no procedural twin, no baked block through the walls, no z-fighting — `qa-app-day.png` |
| 5 Scale | **PASS** | console: `sf-assets: orpheum-theatre merged 11 objects / 11 materials -> batched (4344 tris body); uniform x1.0000 at 2014, -1030`. Scale exactly 1.0000, and the placement matches the computed AABB centre (2014.15, −1030.09) to 0.15 m |
| 5 Orientation | **PASS** | the Market frontage, entrance bay and blade sign face Market Street; Hyde is the west flank, Grove the north — `qa-app-day.png` |
| 5 Terrain seating | **PASS** | sits on the ground on all four sides, no float, no sink |
| 5 Night glow | **PASS** | only the blade sign's bulbs, the crown lamps, the marquee chase and its soffit light — `qa-app-night.png` |
| 5 Draw calls | **PASS** | peak sampled inside the render loop over 45 frames: 95 at the landmark preset, 92 at its street level, **109 at Mission street level**, 104 downtown, 114 wide — all far under the 300 budget |
| 6 Fallback drill | **PASS** | GLB renamed → the app still boots, the area renders, exactly one Orpheum warning (`sf-assets: orpheum-theatre failed to load (… 404)`), `failed: 1` of 104 entries, and the site is empty ground inside the exclusion zone, which is the expected Case B behaviour — `qa-fallback-drill.png`. File restored and re-verified afterwards |
| Lint + build | **PASS** | `npm run lint` clean; `npm run build` succeeds (tests run inside it) |

### Batch mode

`BATCH: yes`. The bake was run and used for the Step 5/6 QA — a Case B landmark cannot
be judged without its exclusion applied — and then **discarded**
(`git checkout -- app/public/tiles api/_data`, 589 generated files). The branch commits
source only: the GLB, the manifest entry, the registry entry, the asset plan and
`artifacts/orpheum-theatre/`. The city is baked once for the whole batch by
`docs/asset-pipeline/BATCH-INTEGRATE.md`.

### Notes for the batch bake

- **Shared landmark `BatchedMesh` headroom.** Measured from the GLB accessor counts:
  104 landmarks now total **1,447,795 body vertices** against the 1,600,000 reserve in
  `app/src/assets.js` (90.5 % full, 152 k left), 76,841 glow of 250,000, and 2,555,544
  indices of 3,600,000. The Orpheum adds 13,031 body vertices. The method reproduces
  the committed 103-landmark figure (1,434,764) exactly. Nothing to do here, but the
  next few SoMa landmarks will need the reserve raised.
- **`audit.mjs` reports three pre-existing FAILs** unrelated to this change: 1.2b
  (95th-percentile height 13.9 m vs the 25–120 m band, a property of the DataSF source
  data), 1.3c (Telegraph Hill terrain 90.5 m from the Terrarium DEM vs a surveyed 84 m),
  and 1.7b (1 of 792 sampled trees more than 30 m offshore). Check **1.6**, the one this
  landmark owns, passes.
- **The fallback warning text differs from the prompt.** Step 6 of
  `INTEGRATION-PROMPT.md` quotes "keeping the code-built landmark". A landmark with a
  `loadRadius` is streamed, and the streamed path warns
  `sf-assets: <id> failed to load (…)` instead. Same guarantee, different string.

## Draft manifest entry

```json
{
  "id": "orpheum-theatre",
  "file": "orpheum-theatre.glb",
  "anchor": [-122.4146087, 37.7793182],
  "targetHeightM": 27.2,
  "cat": 17,
  "name": "Orpheum Theatre",
  "estimated": false,
  "dims": [67.651, 77.623, 27.2],
  "tris": 7193,
  "loadRadius": 2500
}
```

Shipped as written above. The registry entry and the exclusion measurement behind it
are in `pipeline/lib/landmarks.mjs` and §8 of `REFERENCE.md`.
