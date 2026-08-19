# Orpheum Theatre — build report

`artifacts/orpheum-theatre/` — a validated miniature GLB of the Orpheum Theatre,
1192 Market Street, for the SF toy-diorama city. Built 19 August 2026 from
`docs/asset-plans/orpheum-theatre.md`; the dossier that governs it is
[`REFERENCE.md`](./REFERENCE.md), and where dossier and plan disagree the dossier wins.

## Shipped numbers

| | |
|---|---|
| File | `orpheum-theatre.glb` |
| Triangles | **7,496** (cap 24,000) |
| Objects | 242 |
| Dimensions | **67.651 x 77.623 x 27.200 m** |
| Min Z / XY centre | 0.000 / (0.000, 0.000) |
| Size on disk | 501,316 B raw, 85,292 B gzip |
| Materials | 11, all `Toy_*`; 2 glow (`Toy_white_Glow`, `Toy_mustard_Glow`), both shipping at emission strength 0 |
| Textures / transparency / cameras / lights / animation | 0 / 0 / 0 / 0 / 0 |
| Normals | PASS — 0 inverted solids by per-object signed volume; ray test 0.0 % flipped over 22,500 first hits |
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
| `orpheum-theatre.blend` / `.glb` | source scene / shipped asset |
| `orpheum-theatre-{north,east,south,west,top,aerial,night,night-market}.png` | reviews |

The four elevations share one rig — same orthographic scale, framing, lighting, exposure
and projection — and differ only in azimuth. **The Market front bears 45.9° and faces
south-east**, so it is split between the "south" and "east" elevations and is seen square
only in the aerial and night views. That is the site, not a rig error.

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

## Gate 3 — approval

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"
> — David, 19 August 2026, in the session prompt

Recorded verbatim as the standing approval for stages 3, 4 and 5. Stage 5 still stops
before push/PR/deploy, per `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

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
  "tris": 7496,
  "loadRadius": 2500
}
```

Integration is a separate job — `docs/asset-plans/INTEGRATION-PROMPT.md` plus §2.13 of
the plan and §8 of `REFERENCE.md` (which carries the measured `exclude: 20`).
