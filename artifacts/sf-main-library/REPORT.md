# San Francisco Main Public Library — build report

`sf-main-library.glb` — a miniature of James Ingo Freed's 1996 New Main at
100 Larkin Street, for the SF toy-diorama city.

**REPORT beats plan.** Where this file and `docs/asset-plans/sf-main-library.md`
disagree, this file is the record of what shipped and why. The corrections are
in §4.

## 1. Shipped numbers

| | |
|---|---|
| File | `sf-main-library.glb` (post stage-4 optimize) |
| File bytes | **256,072 B** raw (633,248 B pre-optimize; budget 500 KB) |
| Triangles | **10,168** (cap 26,000) |
| Mesh objects | **10** (257 pre-optimize; joined per material) |
| Dimensions (m) | 116.243 x 74.506 x **28.980** |
| bbox min / max | (−58.121, −37.253, 0.000) / (58.121, 37.253, 28.980) |
| min Z | 0.000 |
| XY centre offset | (0.000, 0.000) |
| `targetHeightM` | 28.98 |
| Loader scale factor | **1.000000** |
| Materials | `Toy_cream`, `Toy_glass`, `Toy_glassl_Glow`, `Toy_gold_Glow`, `Toy_mint`, `Toy_roofd`, `Toy_sand`, `Toy_steel`, `Toy_stone`, `Toy_trim` |
| Glow groups | 2 — `Toy_glassl_Glow` (oculus cone + both skylight sheds), `Toy_gold_Glow` (the three Larkin doorways) |
| Image textures / cameras / lights / animations | 0 / 0 / 0 / 0 |
| Non-manifold objects | 0 |
| Inverted solids | 0 |
| Normal ray-cast residual | **0.000000** (tolerance 0.15%) |
| Validation | `validation.json` — **overall PASS** (shipped file; `--closed-solids` passed on the pre-optimize export) |
| Optimize | `optimize/REPORT.md` — gates G1–G6, G8 **PASS** |

The XY bbox is 116.24 x 74.51 m rather than 106.42 x 56.88 m because the
surveyed envelope is rotated 9.06 deg onto the Civic Center grid; the rotated
footprint plus the cornice and pavilion projections is what the bbox measures.

## 2. Orientation decision

Authored with Blender `+Y` = true north, `+X` = east, so the GLB drops into the
city at its real heading — `placeGeneric()` in `app/src/assets.js` scales and
positions but never rotates. The long axis runs at bearing **80.94 deg** and the
ceremonial entrance faces **west** onto Larkin Street.

The contract's "front faces −Y" therefore cannot be honoured literally. Real-world
orientation wins (AGENTS rule 5). Recorded here as the deviation, per
`docs/asset-plans/README.md`.

## 3. Height

`targetHeightM` = **28.98 m**, the DataSF 2010 LiDAR `hgt_maxcm` for this
footprint (`area_id=186`). The main roof plane is 24.02 m (`hgt_mediancm`), which
is the parapet datum in the model.

The OSM and Overture `height=46` tags were **not** used: that value is the NAVD88
roof elevation (153.78 ft = 46.87 m), the same trap the Asian Art Museum carries
on the identical number one block north. See `REFERENCE.md` §2.

The bbox top is normalised to 28.98 m exactly, so the loader's
`targetHeightM / measuredHeight` lands at 1.000000.

## 4. Corrections made to the plan's dossier

Re-verified before modelling, per the pipeline's stage-2 override.

1. **The crest is the skylight-shed ridge, not the pyramid apex.** The plan put
   the 28.98 m crest on the pyramid. The Civic Center Plaza photograph shows the
   glazed sheds standing clear above the parapet as the tallest roof structures,
   and they are the larger objects. Shed 0's ridge is now the crest; the pyramid
   apex sits at 28.20 m. Still *inferred* from photography, not drawings.
2. **Roof glazing is `Toy_glassl_Glow` (#6f95b8), not `Toy_white_Glow`.** The
   plan chose a near-white for frosted skylight glazing. In the first review
   aerial a white cone on a white drum read as a blank disc with no information
   in it. Pale blue glass reads as a skylight by day and as the lit atrium at
   night — which is what it physically is — and separates the glazed events from
   the trim. Both remain palette colours.
3. **The sheds were re-solved.** The plan's 30 x 20 m and 26 x 17 m at 52 deg
   overhang the south parapet and bury a ridge inside the 27 m corner pier.
   Solved numerically against the deck rectangle, the oculus circle and the pier
   footprint: shipped as 22 x 12 m at 38 deg (ridge 28.98) and 17 x 9 m at
   34 deg (ridge 28.10).
4. **The mechanical enclosure moved** off the Grove/Hyde corner — where the plan
   placed it, inside the corner pier — to the deck north of the pier.
5. **The oculus cone was deepened** from apex 27.40 to 28.10 m; 1.8 m of rise
   over a 10.45 m radius rendered as a flat plate.
6. **The footprint is a rectangle.** The reprojected OSM ring is square to within
   0.25 m, so none of the sibling assets' outline-offset machinery is used.
7. **The west flanking bays are not blank granite.** The plan's §2.8 gave the
   Larkin face only the centre pavilion; the first review render showed two large
   empty cream panels. Four tall windows and four base windows were added, at the
   quieter rhythm the photographs show.

## 5. Iteration log

| Pass | What the review render showed | What changed |
|---|---|---|
| 1 | Roof glazing read as white slabs; the oculus was a blank white disc | Roof glazing → `Toy_glassl_Glow` |
| 2 | Sheds overhung the south parapet and collided with the corner pier; the mechanical box was buried inside the pier | Sheds and mech re-solved numerically (§4.3, §4.4) |
| 3 | The corner-pier top rendered **black**, and a black notch appeared at the west parapet corner | Two coplanar-face bugs. The pier body and its cap shared a top face at z = 27.0, and `par_north` / `par_west` overlapped with identical tops. Fixed by dropping the pier body 1.05 m below its cap and re-cutting the four parapet walls so they **tile** instead of overlapping — the classical pair (north, west) owns both west corners, the modern pair stops short |
| 4 | Larkin flanks blank; oculus cone flat; a dead patch of deck where the mech box had been | West flank windows added, cone apex raised, two plant clusters added east of the pyramid |

## 6. Design decisions worth recording

**The split is the asset.** This building is the same size, the same stone and
90 m from the Asian Art Museum, on the same grid. If both reduce to "long pale
slab with a cornice" the city loses what Freed built. The classical/modern split
is therefore carried by three independent signals so it survives simplification:

- the parapet **projects 0.7 m** on Larkin and Fulton and is **flush and 0.4 m
  lower** on Grove and Hyde;
- the pilaster order exists **only** on Larkin and Fulton;
- the cresting of studs exists **only** on Larkin and Fulton.

**The roof gets the budget.** 6,000 m2 of roof under a camera that looks down.
The oculus, the 45-deg glazed pyramid, the two splayed skylight sheds, the
mechanical box, the linear slot and the roof garden are all read off a nadir
aerial rectified into the street-grid frame, so their positions are measured off
the image rather than invented.

**The atrium spiral was dropped.** It is a recognition cue in reality but the
toy's glass is an opaque flat colour, so nothing behind it could ever be seen.
Budget went to the roof composition instead.

## 7. Night state

Two glow groups, restrained:

- **Hero:** the roof glazing — the oculus cone and both skylight sheds —
  `Toy_glassl_Glow`. This is the truthful reading (the atrium is the lit volume)
  and the one that pays off under a downward camera.
- **Supporting:** the three Larkin doorways, `Toy_gold_Glow`.

The glazed pyramid stays dark so the oculus and the sheds carry the composition.
Both glow materials' day colours are palette neighbours of the non-glow surfaces,
so the daylight asset stays calm.

Night renders drive `_Glow` from **Base Color**, not from the imported emission —
glTF writes `emissiveFactor = 0` when the authored strength is 0, so a re-imported
`_Glow` material carries a default white emission. See the note at the end of
`docs/asset-plans/README.md`.

## 7a. Approval (gate 3)

Approved in advance by David on **13 August 2026**, at the top of the pipeline
session, verbatim:

> "I approve everything -- go ahead and do your thing. you dont need to ask for
> stage 3 approval. proceed w everything"

The contact sheet, the aerial day and night renders and the numbers in §1 were
still produced and reviewed before the pipeline advanced, and four revision
passes (§5) were made off those reviews.

## 8. Renders

All images are rendered from the **re-imported exported GLB**, never from the
authoring scene. The four elevations share one rig — same orthographic scale,
framing, lighting, exposure and projection — and differ only in azimuth.
Directions are true compass directions.

`sf-main-library-{north,east,south,west,top,aerial,night,night-larkin}.png` plus
`sf-main-library-contact-sheet.png`.

**One artifact worth naming rather than hiding.** In the true-world orthographic
elevations, the Fulton order appears as a striped band at the north edge of the
*west* view, and the Grove windows likewise at the south edge of the *east* view.
That is the building's 9.06 deg grid rotation projecting into an axis-aligned
camera — the north wall's pilasters spread 16.8 m in screen-x once the block is
rotated — not a modelling error. Every asset in this family authored on the Civic
Center grid has the same property. The rig was left honest rather than
axis-aligned to the building.

Rendered with Cycles CPU at 16 samples with denoising rather than the usual 64:
several other agent sessions were rendering on this machine concurrently and a
64-sample pass was taking upwards of half an hour per frame. The rig, lighting
and geometry are identical; only the sample count differs, and on flat-colour
geometry the denoised 16-sample result is visually indistinguishable.

## 9. Manifest entry (draft — not applied in this task)

```json
{
  "id": "sf-main-library",
  "file": "sf-main-library.glb",
  "anchor": [
    -122.4157709,
    37.7791281
  ],
  "targetHeightM": 28.98,
  "cat": 15,
  "name": "San Francisco Main Public Library",
  "estimated": false,
  "dims": [
    116.243,
    74.506,
    28.98
  ],
  "tris": 10168,
  "loadRadius": 2500
}
```

`cat` 15 is `Library` in `CATEGORY_LABELS` (`app/src/context.js`). `loadRadius`
is the default rule `max(2500, 28.98 x 30)` = 2500.

## 10. Integration note (Case B)

New landmark: no procedural builder, no registry entry. Integration needs a
`pipeline/lib/landmarks.mjs` entry and a tile re-bake. The exclusion radius is
**40 m**, measured rather than guessed — see `docs/asset-plans/sf-main-library.md`
§2.14 for the vertex-distance table. Do not use the OBB half-diagonal (60.33 m):
it would eat the Hyde/Market frontage.


## 11. Local QA (gate 5)

Run against `npm run dev` in this worktree after the Case B re-bake, with the
tile bake applied. The Browser pane runs with rAF suspended, so `SF.assets.update`
was driven by hand with a non-zero `dt` (a zero `dt` never decrements the scan
cooldown and the streaming scan never fires — worth knowing for the next session).

| Check | Result |
|---|---|
| Loader merge line | `sf-assets: sf-main-library merged 10 objects / 10 materials -> batched (5659 tris body); uniform x1.0000 at 1912, -1009` |
| Scale | **x1.0000** — authored crest and `targetHeightM` agree exactly |
| Placement | seated at (1912.07, −1009.02), matching the projected anchor to 1 cm; terrain height 16.0 m |
| Streaming | `loadRadius: 2500` — asset goes live on approach; 36 manifest entries, 29 live near Civic Center, **0 failed** |
| One building, no twin | PASS — `verify-rebake` shows cell 19_13 dropped exactly one footprint (105 → 104) and nothing survives inside the radius |
| Orientation | west front faces Larkin / Civic Center Plaza, long axis on the Civic Center grid |
| Terrain seating | PASS — no floating, no sinking |
| Night | PASS — only the roof glazing (oculus cone + both sheds) and the Larkin doorways light; the glazed pyramid stays dark |
| Draw calls | **96–109** worst case at street level in Civic Center (budget < 300) |
| Fallback drill | PASS — see below |

**Fallback drill.** With `app/public/sf-assets/landmarks/sf-main-library.glb`
renamed away: the app boots, the area renders, the block is empty ground (the
expected Case B result, because the baked footprint was excluded), and exactly
**one** warning appears:

```
sf-assets: sf-main-library failed to load (Unexpected token '<', "<!doctype "... is not valid JSON)
```

Note the failure is a **parse error, not a 404** — Vite serves `index.html` with
status 200 for a missing asset path, so the loader gets HTML where it expected a
GLB. All 28 other landmarks merged normally through the drill. File restored and
re-verified afterwards.

## 12. Bake verification (Case B)

```
node pipeline/verify-rebake.mjs
  new since origin/main: sfMainLibrary @ 19_13
  584 of 585 cells unchanged
  19_13    105 -> 104  <- sfMainLibrary
  ok   sfMainLibrary          50.6 m vs 40 m radius  (nearest is 17.0 m tall)
  PASS  only the new landmarks' cells moved, and every asset has clear ground under it

node pipeline/audit.mjs
  1.6    PASS    no procedural footprint inside a bespoke landmark exclusion zone   42 landmarks clear
```

The 50.6 m figure is exactly the nearest-neighbour distance measured in the plan's
§2.14 before anything was built — the exclusion radius behaved as designed, with
10.6 m of margin.

Checks 1.2b, 1.3c and 1.7b FAIL; they are pre-existing on `origin/main` and
documented as such in `docs/asset-pipeline/BATCH-INTEGRATE.md`.

**Batch mode:** the bake was run for this QA and then discarded
(`git checkout -- app/public/tiles api/_data`). This branch commits source only.
