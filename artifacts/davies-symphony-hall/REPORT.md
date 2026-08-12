# Davies Symphony Hall — build report

`davies-symphony-hall.glb`, built 12 August 2026 from
`docs/asset-plans/davies-symphony-hall.md` via
`build_davies_symphony_hall.py` (Blender 5.2.0 LTS, headless).

**This report beats the plan.** Where the two disagree, what is written here is
what was verified at build time and what the asset actually contains.

## Numbers

| | |
|---|---|
| Triangles | **9,829** (cap 16,000) |
| Objects | 177 |
| Dimensions | 124.75 × 95.04 × **35.00** m |
| Min Z | 0.000 |
| XY centre offset | 0.110, 0.708 m |
| Loader scale (`targetHeightM / measuredHeight`) | **1.000000** |
| Materials | 11, all `Toy_*`, 3 of them `_Glow` |
| Front arc, measured back out of the export | 42 fins on R 44.75 m about local `(10.03, −1.02)`, max residual 0.71 m |
| File | see `validation.json` for the full machine-readable report |

Materials: `Toy_cream`, `Toy_glass`, `Toy_gold`, `Toy_gold_Glow`, `Toy_ink`,
`Toy_mustard_Glow`, `Toy_roofd`, `Toy_steel`, `Toy_stone`, `Toy_trim`,
`Toy_white`.

## Validation — `validation.json`, `overall: PASS`

| Check | Result |
|---|---|
| Fresh isolated scene, re-imported final GLB | PASS |
| Metres, plausible dimensions | PASS |
| Crest lands on the 35.0 m target height | PASS (35.000) |
| Base at z = 0 | PASS (0.000) |
| Centred in XY | PASS (0.11, 0.71 m) |
| Front arc preserved (R 44.75 m) | PASS (42 fins, max residual 0.71 m) |
| Under the triangle budget | PASS (9,829 / 16,000) |
| No image textures | PASS |
| No transparency | PASS |
| Materials follow the contract | PASS |
| No cameras or lights | PASS |
| No animation, skinning or constraints | PASS |
| Transforms applied | PASS |
| No negative scales | PASS |
| Normals outward | PASS |
| No degenerate geometry | PASS |
| No unexpected objects | PASS |
| Night-glow materials present | PASS |

**Normals method.** Every source mesh runs `bmesh.ops.recalc_face_normals`
before export. On re-import, per-object signed volume is authoritative for the
closed solids and all of them come back positive — note that glTF stores split
vertices for flat shading, so the validator welds coincident vertices before
asking whether a mesh is closed, otherwise every solid falsely reads as an open
shell. Eight objects are single-sided *by design* — `shell_roof`, `shell_ribs`,
`shell_crown`, `lettering_band`, `lettering_glow`, `promenade_glow_l1`,
`promenade_glow_l2`, `clerestory_glow` — so 22,500 deterministic visibility rays
gate the back-facing residual at 0.15%. Measured residual: **0.12%**.

## Dossier corrections made at build time

1. **The OSM `height=49 m` tag is wrong and was rejected.** The asset is built
   to **35.0 m**. DataSF's LiDAR footprint record `201006.0000141` — whose
   bounding box matches OSM way 32865746 to five decimals across 28,160
   half-metre cells — gives a roof median of 26.12 m and a maximum of 34.95 m
   above a mean ground of 18.91 m NAVD88. Those two figures land exactly on the
   two datums visible in any photograph: the parapet ring and the crest of the
   shell roof. SOM's own statement that the design matches its neighbours'
   cornices corroborates the 26.1 m ring, which is within a metre of the Opera
   House's. And 49 m would put Davies above the Opera House's 44 m fly tower,
   which every aerial photograph of Civic Center contradicts. Full argument in
   `REFERENCE.md` §3.
2. **The front arc was measured, not eyeballed.** A least-squares circle fit to
   the eleven OSM arc nodes gives centre `(10.03, −1.02)` local, R = 44.75 m,
   sweep −4.5° → 99.1° (103.6°), residuals −0.82 … +0.53 m. That circle — not a
   chamfer, not a spline — is what the model is built on, and the validator
   measures it back out of the export.
3. **Wikidata carries no height claim (P2048)** and SOM publishes only gross
   area, so no published architectural height exists to prefer over the LiDAR.

## Deviations from the contract and the plan, and why

- **Front does not face −Y.** Davies' front arc faces north-east. Real-world
  orientation wins (AGENTS rule 5 and the standing note in
  `docs/asset-plans/README.md`); the model is authored on the measured polygon
  so it carries the Civic Center grid's ~9° rotation itself and the loader
  applies no rotation.
- **XY bounding box is 124.7 × 95.0 m, not the 122.6 × 91.2 m footprint.** The
  plinth aprons 1.2 m past the footprint and the two terrace slabs cantilever
  4.5 m off the ends of the arc. That is a cantilever, not a scale error. The
  plan said 5.5 m; reduced to 4.5 m so the model stays closer to its block.
- **The flagpole at the crest is not modelled**, deliberately: it would take the
  bounding-box top and cost the height normalization for two pixels of mast.
- **The gold lettering runs across the arc only**, not around the whole
  perimeter. A first pass put a gold ring on the full cornice and it turned a
  restrained civic building into a casino.
- **Triangle budget came in at 61% of cap.** The first build was 18,712 — over
  budget — and the cause was bevelling the cornice and fascia rings, which alone
  cost 8,208 triangles. Those two are thin bands where a bevel is invisible at
  city scale; dropping it freed the budget for a denser arc, 75 fins and 78
  clerestory slots.

## Iteration log

| Pass | Change | Why |
|---|---|---|
| 1 | First aerial | Massing and arc read correctly; three faults visible |
| 2 | Day renders composite `_Glow` at 12% alpha | The app draws the glow set in a separate ~12% layer by day; rendering it opaque made the whole promenade a wall of amber and hid the glazing. Preview-only — the GLB stays fully opaque. |
| 3 | Shell given its own footprint | Interpolating a cap over the re-entrant block outline folded the roof into a drooping flap over Van Ness. The shell is now a polar curve about the arc centre — star-shaped by construction, so it cannot fold. |
| 4 | Main block top became a real `Toy_roofd` deck | Once the shell stopped covering everything, the roof around it had to be a designed surface |
| 5 | Gold ring → arc-only lettering band; terrace rails became solids | Restraint; and a single-sided ribbon rail fails the normals test |
| 6 | Shell grown to fill the block, inset 1.4 m from the parapet | Matches the day photograph, where the roof meets the parapet on the visible sides |
| 7 | Shell back radius smoothed (6 passes, then clamped back inside the outline) | The top view showed the shell kinking into a V where the raw block outline jumps at the Grove notch and the Van Ness stair bay. Roofs do not kink. The clamp guarantees smoothing can never push the shell out over a street. |
| 8 | Cornice/fascia bevels dropped, arc and fin density raised | Budget, see above |
| 9 | Shell sampled against a *simplified* outline with the two small street bays removed | Smoothing alone still let the roof dive into the recessed Grove entrance bay and nick its own edge. A first attempt (a local-minimum filter on the radius) removed the nick but pulled the shell right off the Hayes parapet, so the fix moved to the input: a roof spans a recessed entrance, it does not follow it. |

## Stage 3 — approval

Approved by David on 12 August 2026, verbatim: **"i approve all stages just
proceed"** — given in advance for every gate of the address-to-asset pipeline
in this session, together with the instruction to work on a new branch and open
a PR (which overrides the pipeline's default "stop before pushing").

## Night state

The night photograph is the design and the model follows it: both promenade
levels burn warm behind the fin rhythm (`Toy_mustard_Glow` shells 0.06 m proud
of the opaque `Toy_glass`, never the glass itself), the clerestory slot band
glows above them, and the lettering band on the arc's fascia is picked out. The
precast, the shell roof and the whole back-of-house stay dark. Both glow
materials' day colours are palette members, so the daylight read stays
consistent with the Opera House next door.

## Renders

All generated from the exported GLB, re-imported into an empty scene — every
image depicts exactly the geometry that ships.

`davies-symphony-hall-north.png`, `-east.png`, `-south.png`, `-west.png` (one
orthographic rig, identical scale/framing/lighting/exposure, differing only in
azimuth), `-top.png`, `-aerial.png` (105 mm, 38° down, from the north-east —
the only angle from which the arc reads as an arc), `-aerial-night.png`, and
`-contact-sheet.png`.

## Draft manifest entry

Not applied here — integration is a separate job
(`docs/asset-plans/INTEGRATION-PROMPT.md`).

```json
{
  "id": "davies-symphony-hall",
  "file": "davies-symphony-hall.glb",
  "anchor": [
    -122.4206030,
    37.7776227
  ],
  "targetHeightM": 35.0,
  "cat": 17,
  "name": "Davies Symphony Hall",
  "estimated": false,
  "dims": [
    124.747,
    95.0375,
    35.0
  ],
  "tris": 9829,
  "loadRadius": 2500
}
```

`"estimated": false` — both the cornice and the crest are LiDAR measurements.
`cat: 17` matches `opera-house`, so the two Performing Arts Center halls are
treated consistently by search and the concierge.

## Notes for integration

- **Case B**: no procedural builder and no registry entry exist, so integration
  needs a `pipeline/lib/landmarks.mjs` entry and a re-bake of the affected tiles.
- The building fills its own block with no attached neighbours, so a plain
  exclusion radius works here. Half the 122.6 m envelope is 61 m, but 62 m would
  reach buildings across Hayes Street — the block's south edge is only ~40 m
  from the anchor and Hayes is ~20 m wide. **Use 55 m**, which clears the Davies
  footprint (its centroid sits ~5 m from the anchor) and leaves the Hayes and
  Grove frontages alone.
- Check the `opera-house` exclusion zone at the same time: the two blocks are
  25 m apart across Grove Street, and something real now stands on the Davies
  block.
- `loadRadius`: the default rule gives `max(2500, 35 × 30) = 2500` m. Take it.
- The Henry Moore *Large Four Piece Reclining Figure* stands in the forecourt at
  the Van Ness/Grove corner. Out of scope here; worth a props pass later.
