# 500 Third Street — build report

Deliverable of stages 1–3 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run
13 August 2026 from the input `BUILDING: 500 3rd street San Francisco` with
`BATCH: yes`.

**What this is:** a miniature GLB of the 1927 concrete industrial loft at 3rd and
Bryant — a five-storey block whose identity is a steel-sash window grid on three
sides, a charcoal storefront base, and one signed corner crown. `REFERENCE.md`
holds the research; this file holds what was built, what was corrected, and what
was measured.

## Shipped numbers

| | |
|---|---|
| File | `500-third.glb` |
| Raw / gzipped | **183,916 B / 90,750 B** shipped (1,151,788 / 167,849 as authored — stage 4 cut it 6.3x, see `optimize/REPORT.md`) |
| Triangles | **17,320** (cap 22,000), unchanged by the optimize pass |
| Objects | 13 shipped (546 as authored; joined per material), 14 draw primitives |
| Dimensions (m) | 75.239 × 76.238 × **26.500** |
| min Z | 0.000 |
| XY centre offset | (0.000, 0.000) m |
| Loader scale factor | **1.000** (`targetHeightM 26.5 / measuredHeight 26.5`) |
| Materials | 13, all `Toy_*`, flat, no textures, no alpha, no `Toy_body` |
| Glow materials | `Toy_glassl_Glow`, `Toy_white_Glow` |
| Anchor | −122.3958224, 37.7808279 |
| 3rd Street front normal | 44.9° true |
| Validator | Blender 5.2.0 LTS, fresh-scene re-import of the exported GLB — **overall PASS**, all 15 checks |
| Degenerate triangles | 0 |
| Inverted signed volumes | 0 |
| Normal ray-cast residual | 0.0% (gate 0.15%) |

The X/Y dimensions are the axis-aligned bounding box, not the building: the
block is 58.59 × 47.68 m sitting at 45° to the compass, so its AABB is the
diagonal envelope. `validation.json` is the machine-readable version: overall **PASS**, all 15
authoring checks, plus a `shipped` block carrying the packed file's numbers. The
packed file's own gates are in `optimize/validation.json` (G1/G2/G5) and
`optimize/g3check`.

## Orientation — a documented contract deviation

The contract in `.agents/skills/sf-asset-check/SKILL.md` says "front faces −Y".
This building's front faces **north-east** (outward normal 44.9° true), because
the SoMa grid is rotated ~45°. `placeGeneric()` in `app/src/assets.js` scales and
positions but never rotates, so honouring "front faces −Y" literally would drop
the building into the city facing the wrong street.

The asset is therefore authored in **true-world orientation** (`+Y` = north,
`+X` = east), per AGENTS rule 5 and the orientation note in
`docs/asset-plans/README.md`. No `yawDeg` override is needed.

## Corrections and decisions on top of the plan

**REPORT beats plan.** Everything here was settled during the build:

1. **Storey count resolved to five.** The plan flagged the conflict (assessor
   "6", DBI permits 5 and 6). Street View of all four elevations shows one tall
   ground floor plus exactly four upper window bands, on every side. Five floors
   — a ~5.6 m ground floor and four of 4.0 m, plus a 1.0 m parapet — reproduces
   the measured 23.0 m parapet exactly. The "6" is read as a count that includes
   the ground floor's mezzanine, which DBI permits do reference.
2. **Target height is the bulkhead, not the parapet.** OSM `height=23` and the
   2010 LiDAR median (22.74 m) both describe the parapet. The LiDAR *maximum*
   over the footprint is 26.62 m — the rooftop bulkhead. The bbox top is
   normalised to **26.5 m** so the loader's scale factor is exactly 1.0; nothing
   in the model, flag masts included, rises above it.
3. **The SE elevation is a real facade, not a party wall.** The neighbouring lot
   is open surface parking, so that side is fully exposed to the app's camera. It
   is modelled with the same seven-bay window grid as Bryant.
4. **The exclusion radius was measured, not estimated.** The plan suggested a
   provisional 12 m; against the pipeline's own bake input (DataSF footprints
   projected and simplified at the 0.6 m tolerance) this building's ring centroid
   is 0.93 m from the anchor and the nearest *neighbour* vertex is 35.59 m
   (SF3776100). The window that drops only this building is
   `0.93 < r <= 35.59`, so the registry entry uses **`exclude: 20`** — clear of
   both ends. See "Integration notes" below.
5. **Review renders are true elevations, not compass elevations.** A cardinal
   camera on a 45°-rotated block shows two faces at once. The four elevation
   cameras are aimed along the four measured face normals; the filenames keep the
   pipeline's `north/east/south/west` names and map as: `north` = 3rd Street
   (NE), `east` = SE over the parking lot, `south` = Ritch Street (SW),
   `west` = Bryant Street (NW).
6. **The corner sign is a plain illuminated band, not lettering.** The real crown
   carries a tenant's logo; reproducing a company mark in city geometry is not
   the building's identity and would date the asset. The band reads as an
   illuminated sign at every distance the app shows. The building's own address
   numerals — "500", which the real entry carries as "500 THIRD" — are modelled
   over the 3rd Street entry instead.
7. **The fire escape was dropped.** Thin diagonal steelwork on the southern part
   of the 3rd Street elevation is exactly the detail the style bible tells us to
   strip; at city distance it would be noise and at close range it would be the
   most expensive geometry on the model.

## Iterations

Four review rounds, each rebuilt from the deterministic script — three from the
high three-quarter aerial, one from the validator:

1. **First massing.** Correct in proportion, but the roof carried a 26 × 12 m
   mechanical curb that read from the air as a dark slab, and the bulkhead cap
   was near-black. Removed the curb, lightened the cap to `Toy_steel`.
2. **Second pass.** The 2,800 m² membrane was blank — the style bible's "design
   every surface visible from above" was not met. Added a gravel-stop band inside
   the parapet, an L-shaped walkway off the bulkhead, three roof hatches, four
   vent stacks, and spread the plant into two clean rows across the south half.
   Raised the corner crown 0.4 m and stood it 0.10 m proud so it reads from the
   aerial camera.
3. **Third pass.** The "500" numerals were authored in `Toy_ink` on an `Toy_ink`
   entry beam that stands 0.30 m proud — invisible in both senses. They are now
   `Toy_trim` and start at the beam's outer face. The Ritch Street punched
   windows grew from 0.95 m to 1.25 m, which is where they stop reading as dots.

4. **Contract pass.** The first fresh-scene validation failed two checks:
   630 degenerate triangles and six window reveals with inverted signed volume,
   all of them the 0.05 m thin `*_reveal` plates. Three changes fixed it and are
   now permanent in the build script: `bevel()` clamps its width to 40% of the
   object's thinnest dimension (a 0.05 m plate beveled at 0.05 m collapses),
   dissolves degenerate edges after beveling, and a final `ensure_outward()` pass
   flips any object whose signed volume comes out non-positive. The reveal's back
   face also moved 0.06 m into the wall, so the plate is 0.11 m thick while its
   visible outer face stays where it was. Re-validation: **PASS**, 0 degenerate,
   0 inverted, ray residual 0.0%.

Triangle count across the passes: 23,184 → 16,036 → 17,320 → 17,320. The drop came from
one bevel segment on the 92 window reveals and unbeveled sill bands; the rise is
the roof furniture added in pass 2.

## Night state

A dark grey block with a lit corner:

- **Hero:** the crown sign band, `Toy_white_Glow`, on both the 3rd Street and
  Bryant faces of the raised north corner.
- **Supporting:** fifteen scattered lit upper bays, `Toy_glassl_Glow`, one bay in
  four and never a whole floor, so the building reads as occupied rather than as
  a light box.
- **Ground:** the entry transom and the two lobby bays flanking it.
- **Dark:** the entire Ritch Street service rear, as in life.

Every glow surface is a thin shell standing proud of the opaque glazing behind
it. `assets.js` renders `_Glow` in a separate unlit layer at
`opacity = 0.12 + 0.95·uNight`, so a primary surface is never authored as glow;
by day these shells sit at ~12% alpha over the `Toy_glass` behind them.

## Deliberate omissions

Not in the GLB: 3rd Street, Bryant Street, Ritch Street, the SE parking lot,
neighbouring buildings, street trees, street furniture, people, vehicles,
plinths, cameras, lights. The fire escape, the through-wall air-conditioners and
the real 8 × 6 mullion counts are simplifications, listed in `REFERENCE.md` §7.

## Review renders

Rendered from the **exported GLB**, re-imported into an empty scene, so every
image depicts exactly the geometry that ships.

| Image | What it shows |
|---|---|
| `500-third-aerial.png` | the app's camera: high three-quarter on the north corner, both street elevations and the roof |
| `500-third-top.png` | the roof composition — gravel stop, bulkhead, walkway, plant rows, hatches |
| `500-third-north.png` | 3rd Street (NE): nine bays, the entry and its 500 numerals, the crown at the north end |
| `500-third-west.png` | Bryant Street (NW): seven bays, the crown at the north end |
| `500-third-east.png` | SE elevation over the parking lot: seven bays, no entry |
| `500-third-south.png` | Ritch Street (SW): the blind service rear |
| `500-third-night.png` | the dusk pass: crown band, scattered lit bays, entry |
| `500-third-contact-sheet.png` | all of the above in one frame |

**Engine note.** The rig's reference engine is Cycles (40 samples, CPU). This
machine was running a dozen parallel Blender sessions during the build and a
single Cycles frame was getting ~5% of one core, so the shipped day images were
rendered with `--fast`: Workbench, studio light, cavity, shadows off — Workbench's
shadow map leaks light through the proud window reveals and speckles the roof.
The night image uses EEVEE, which the glow layer needs. The flat-colour toy
palette survives the swap intact; `render_500_third.py` without `--fast` still
reproduces the Cycles rig unchanged.

## Gate 3 — approval

Approval was given in advance, in the session's opening instruction:

> "I approve everything -- go ahead and do your thing. you dont need to ask for
> stage 3 approval. proceed w everything" — 13 August 2026

Recorded here as the pipeline requires. No design feedback was received, so the
three iterations above are self-directed against the style bible rather than
responses to review.

## Draft manifest entry

```json
{
  "id": "500-third",
  "file": "500-third.glb",
  "anchor": [
    -122.3958224,
    37.7808279
  ],
  "targetHeightM": 26.5,
  "cat": 3,
  "name": "500 Third Street",
  "estimated": false,
  "dims": [
    75.239,
    76.238,
    26.5
  ],
  "tris": 17320,
  "loadRadius": 2500
}
```

`loadRadius` is the skill's default `max(2500, targetHeightM × 30)`; at 26.5 m
the 2,500 m floor applies. A 26 m block is illegible long before that, and the
exclusion hole it leaves behind is invisible at that range.

## Integration notes

- **Case B** — new landmark. `pipeline/lib/landmarks.mjs` needs
  `{ id: '500Third', name: '500 Third Street', lon: -122.3958224,
  lat: 37.7808279, height: 26.5, exclude: 20 }`, and the affected tiles must be
  re-baked.
- The exclusion window is measured, not guessed: `0.93 < r <= 35.59` (see
  correction 4). 20 m sits in the middle of it.
- Manifest id `500-third` maps to registry id `500Third`.
- No camera preset key. At 26.5 m this is SoMa fabric, not a destination.
- Flat made ground (LiDAR ground mean 5.64 m NAVD88, range 0.97 m over the whole
  footprint) — terrain seating should be uneventful.

## Reproducing

```
blender -b --python build_500_third.py         # writes .blend and .glb
blender -b --python render_500_third.py        # Cycles rig (add --fast for Workbench/EEVEE)
blender -b --python render_500_third.py -- --night
blender -b --python validate_500_third.py      # fresh-scene contract check
python3 make_contact_sheet.py
```
