# Pier 3 (Hornblower Landing) — build report

**What this is:** a validated miniature GLB of the whole of Pier 3 — pile field, deck,
Beaux-Arts bulkhead with its arched "PIER · 3" portal, and the 2006 office block behind it —
built for the SF toy-diorama city. Stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

## Shipped numbers

| | |
|---|---|
| Triangles | **12,152** (cap 18,000) |
| Objects | 361 |
| Dimensions | 195.82 x 161.21 x 18.50 m (AABB; the pier itself is 212.8 x 53.5 m at 53.92°) |
| Min Z | **0.000 m** — and Z = 0 is the **waterline**, with the pile feet on it |
| XY centre offset | −0.75, −2.64 m (see "tolerances" below) |
| Materials | 13, all `Toy_*`, 3 of them `_Glow` |
| File | **371,724 B raw** / 214,363 B gzip, meshopt-compressed (pre-optimize: 817,276 B / 132,302 B) |
| Draw submeshes | **13** (pre-optimize: 361) |
| Anchor | `-122.3947017, 37.7982322` |
| targetHeightM | **18.50 m** (attic crest over the arch pediment, above water) |
| Validation | **PASS**, all 16 checks, re-run against the shipped optimized file — `validation.json` |
| Optimize | all gates G1–G6, G8 PASS — `optimize/REPORT.md` |

Normals: 361 of 361 objects enclose positive signed volume; 13,453 deterministic visibility
rays from nine interior targets found **zero** flipped visible faces (0.0000% against a
0.15% tolerance). Zero degenerate triangles.

## Deliverables

`build_pier_3.py` (deterministic build) · `pier-3.blend` · `pier-3.glb` (optimized, shipping) ·
`optimize/` (stage 4: scripts, stats, A/B renders, `input/pier-3.glb` archive, report) ·
`render_pier_3.py` · `validate_pier_3.py` · `make_contact_sheet.py` · `validation.json` ·
`REFERENCE.md` (the dossier and the sources) · nine renders: north / east / south / west /
frontage / top / water / aerial / aerial-night, plus the contact sheet.

`--water` and `--frontage` are additions to the standard rig and both earn their place: the
pier sits at 53.92°, so all four compass elevations show it on the diagonal and the portal
can only be judged square-on; and the bay view is the only image that proves the pile field
and the deck soffit were actually built rather than implied.

## Dossier corrections and deliberate deviations

**REPORT beats plan.** Full list with reasoning in `REFERENCE.md` §6; the load-bearing ones:

1. **The bulkhead is 43.5 m wide, not the plan's 53.5 m.** A 53.5 m block 11 m deep pokes
   2.3 m outside the OSM footprint on the northwest. Real assets sit on real footprints
   (AGENTS rule 5). The real building probably does continue onto the seawall; that ground is
   not Pier 3's and is not this asset's to occupy.
2. **Everything above deck level is built square to the pier axis, not on OSM's traced
   frontage edge.** OSM traces the frontage 3.6° off perpendicular to the axis; the
   Embarcadero itself runs 324.0°, measured independently from Pier 5's building (OSM way
   91913148), so the traced edge is the error. The deck keeps the traced polygon.
3. **Bulkhead depth 11.0 m** comes from measuring Pier 5's bulkhead at 65.9 x 10.8 m — the
   same 1918 design family, and the only depth figure in the whole dossier that is measured
   rather than guessed.
4. **The flagpole is not modelled.** The plan flagged it as a trap and it bit in both
   directions: at true height (~22.5 m) it becomes the bounding-box top, so either the whole
   213 m pier is scaled down 18% to make 18.5 fit or a 160 mm spike becomes the number the
   asset is normalised against; a mast stopping below the attic crest reads as a mistake.
   Omitting it is the least-wrong of the three, and `targetHeightM` stays the architectural
   top as the repo's convention requires.
5. **Added: the belt-railway rails and three boarding-gangway platforms.** Both documented
   (the National Register records the rails in the north breezeway; the excursion berths have
   fixed gangway structures) and both added because review 2 showed a 190 m deck reading as a
   bare runway. The vessels stay out — they move, and the app has a live-vessel layer.
6. **`Toy_conc` `#c6bfb2` for the deck surface is off-palette** (WARN, not FAIL, contract rule
   7). The plan anticipated it: `Toy_stone` for both the slab and the deck collapsed two
   planes into one from the aerial.
7. **The large roof membranes are `Toy_steel`, not `Toy_roofd`.** `Toy_roofd` rendered
   near-black over 2,100 m2 of office roof and read as a pit punched in the miniature — the
   same failure the repo has seen on a roof terrace before. The rooftop plant took
   `Toy_roofd` instead, so the two planes still separate.

## Review iterations

1. **Aerial 1.** Camera could not hold a 196 m object on a 105 mm lens; both roof membranes
   read as black pits; rooftop plant straddled the shoreward parapet; the frontage had four
   windows on a 43 m wall (7 bays, three eaten by the pavilion).
   → lens 70 mm, membranes to `Toy_steel`, plant re-ranked along the roof edges, 11 bays.
2. **Frontage 1.** Two real bugs. Every window reveal, pane and glow shell was built
   **inside** the wall — "outward" from this frontage is *s decreasing*, and the sign was
   flipped, so they z-fought with the face instead of standing proud of it. And the raking
   cornice was a solid triangle 0.4 m proud of the pediment, i.e. a wall in front of the
   tympanum: **it swallowed the entire "PIER · 3" inscription.**
   → all reveals re-signed with the frame-behind-glass trick; the cornice rebuilt as a frame
   (bed mould plus two rakes) with the tympanum left open; caps resized to 1.05 m so the
   lettering clears the rakes at the apex.
3. **Aerial 2.** Deck read as a bare runway over 190 m.
   → belt-railway rails, three gangway platforms, sheds lightened off near-black.
4. **Night 1.** The deck light standards were **completely invisible**: the 0.68 x 0.44 m
   amber shell sat inside the 1.6 x 0.9 m steel lamphead, which enclosed it. The lit roof
   monitor blew out to a white slab.
   → lamphead shrunk and the glow made a collar wider than it, so the lens reads from
   directly overhead; `Toy_glassl_Glow` darkened `#9fc3dd` → `#7ea8c8`.
5. **Night 2.** Still white. The preview was driving Principled *emission* (6.0, then 3.0),
   which clips any pale colour to white — but the app draws `_Glow` **unlit at the base
   colour**. The render rig was wrong, not the asset.
   → `light_glow()` now sets base colour black, emission colour to the palette value,
   strength 1.0. The night render finally shows what the scene will: an amber arch lunette,
   pale-blue lit windows and one lit monitor, and an amber line of deck lights running out
   into the bay.

## Night design

Hero: the **arch soffit lunette** in `Toy_amber_Glow` — at night a 3 m deck has nothing else
that reads, and a lit gateway carries the whole asset. Supporting: one of the two roof
monitors lit from within, which reads from directly overhead where the elevations do not.
Accent: the sixteen deck light standards as amber points down both flanks — this is what
draws the pier's *line* into the bay — plus six lit upper-storey windows on the frontage.
The "PIER · 3" letters do not glow: a 1918 inscription is not signage.

All glow surfaces are thin closed shells proud of the opaque surface behind them. The arch
glow was cut back from a full-arch shell to a head lunette after review 4 — at the app's ~12%
day alpha a full-arch shell washed the hero mauve.

## Tolerances worth knowing

- **`base_at_z_zero` is checked at ±0.05 m, not the usual ±0.5 m.** Z = 0 is the waterline
  and the pile feet land on it exactly; a loose tolerance here would hide a floating pier.
- **`centered_xy` is checked at ±3.5 m, not ±1.0 m.** The origin is the pier polygon's *area
  centroid*, which is the honest real-world anchor. It is not the AABB centre: the pier flares
  from 40 m across at the head to 53.5 m at the bulkhead, so the two differ by 2.64 m over a
  196 m asset (1.4%). Moving the origin to the AABB centre would place the model 2.64 m off
  its surveyed position to satisfy a tolerance written for compact buildings.

## Open risks carried into integration

- **18.5 m is photogrammetric** (method in `REFERENCE.md` §3; honest range 17.5–19.5 m). It
  sets `targetHeightM` and therefore scales everything.
- The roof monitors may be photovoltaic rather than glazed; if so the roof reads much darker
  and the night glow on one of them is wrong.
- Office block dimensions are read off imagery and over-supply LoopNet's 39,700 SF by ~16%.
- Pile spacing (7.5 m) is inferred; only the edge band and a centre spine are modelled.

## Gate 3 — approval

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

— David, 18 August 2026, in the session prompt that invoked
`docs/asset-pipeline/ADDRESS-TO-ASSET.md` for this building.

Taken as standing approval for the pipeline's gates including stage 3, so the session did not
stop here. The contact sheet, the day and night aerials and the numbers above were presented
at this point rather than withheld; nothing was approved on the user's behalf that they had
not already pre-authorised in writing.
