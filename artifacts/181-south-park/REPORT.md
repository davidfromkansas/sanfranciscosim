# 181 South Park — build report

Deliverable: `181-south-park.glb`, a miniature-toy GLB of 181 South Park, San
Francisco, authored in Blender 5.2 LTS from `build_181_south_park.py` and
validated from a fresh re-import of the exported file.

**REPORT beats plan.** Where this file and `docs/asset-plans/181-south-park.md`
disagree, this file is what shipped. Section 2 records the plan's biggest open
question and how it was closed; section 6 records what is still unverified.

---

## 1. Numbers

| | |
|---|---|
| Triangles | 4,200 (budget 9,000) |
| Objects | 9 (121 before the stage-4 optimize pass) |
| File | 139,356 B raw / 86,139 B gzip −9 (290,832 B raw pre-optimize, −52.1%) |
| Dimensions | 40.836 x 40.528 x 16.5 m |
| Bounding-box top | 16.5 m exactly — the roof ridge; loader scale lands on 1.0 |
| min Z | 0.0 |
| XY centre offset | (−0.0025, 0.0119) m |
| Materials | 9, all `Toy_*`, flat, untextured, opaque |
| Glow materials | `Toy_glass_Glow`, `Toy_trim_Glow` |
| Anchor | `-122.3945113, 37.7807582` |
| Front heading | 315.2° true (NW, onto South Park) |
| Validation | all 16 contract checks PASS (`validation.json`), re-run against the shipped optimized file |
| Renderer | EEVEE, 128 samples — see below |

**The committed renders are EEVEE, not Cycles.** These materials are flat,
untextured and opaque, so the two engines are visually equivalent for this asset,
and the authoring machine was running several batch sessions at once (load
average ~490) where Cycles CPU could not finish the rig at all. Pass
`--engine CYCLES` to `render_181_south_park.py` to reproduce in Cycles.

The axis-aligned bounding box is ~40.8 x 40.5 m even though the building is
43.21 x 13.84 m. That is the expected consequence of a 135.2° real-world
heading, not a scale error.

**Orientation deviates from the contract, deliberately.** The asset contract asks
for "front faces −Y". This building's front faces NW (315.2°). Real-world
orientation wins (AGENTS rule 5, and the plans README's standing note), because
`placeGeneric()` in `app/src/assets.js` scales and positions but never rotates.

## 2. The correction that mattered: the roof is a gable

The plan shipped with one large unknown — the roof was flat at ~14.2 m with
something reaching 16.5 m, form unknown — and it was narrowed once during
planning and closed during the build.

**First:** aerial imagery (Bing/Vexcel 2026 nadir) showed the roof is not flat at
all. It is a light-grey standing-seam ridged metal roof with its ridge running
along the long axis for most of the building's length, hipped down at the NW end,
roof monitors on the ridge, mechanical grouped at the Varney end. No penthouse.
The plan was revised for this before any modelling.

**Then:** the imagery could not resolve whether the section was a barrel or a
gable, and the two produce very different silhouettes. The LiDAR height
distribution settles it. A roof's height distribution over its own footprint has
a shape set by its section, so the gap between the median height and the maximum
identifies the section:

| Section | Median, as a fraction of the rise | Implied eave, given median 14.18 m and ridge 16.54 m |
|---|---|---|
| straight gable (uniform) | 0.50 | **11.82 m** |
| parabolic arc | 0.75 | 7.10 m |
| circular barrel | 0.866 | −1.07 m |

A curved roof concentrates plan area near its crown and pulls the median up
toward the ridge. For the median to sit as low as 14.18 m under a 16.54 m ridge,
a parabolic roof would need eaves at 7.1 m and a circular one below ground —
neither possible on a four-storey building. Only the straight slope closes, on an
eave of 11.82 m, which is two generous loft floors over a 4.0 m commercial ground
floor with the fourth storey inside the roof.

That also reconciles the unit listings' "arched hardwood high ceilings": the arch
is an interior ceiling hung inside a straight-pitched roof, not the roof's own
section. Both facts hold; neither has to be thrown away.

Built accordingly: eave 11.82 m, ridge 16.5 m, ~33.8° pitch, hipped at the NW
end over a 6.92 m run, with the last 6.5 m at the Varney end a flat mechanical
roof behind a parapet.

## 3. Other corrections to the plan

- **The plan's massing recipe assumed a flat roof and a parapet.** Replaced
  wholesale by section 2. The eave fascia replaces the parapet ring, and the
  building's wall storeys drop from three to two with the fourth inside the roof.
- **`OSM height=14` is neither eave nor ridge.** It matches the LiDAR median to
  0.02 m, which makes it look corroborated rather than merely repeated. On a
  ridged roof the median is a mid-slope value corresponding to no physical line
  on the building at all. This is the sharpest version of the height-tag trap in
  the plans README and it is worth carrying forward.
- **The plan's `Toy_roofd` roof became `Toy_steel`.** The aerial shows light-grey
  standing-seam metal, not a dark membrane. `Toy_roofd` is now used only for the
  Varney-end mechanical deck and the garage door.

## 4. Build iterations

Each iteration is a review of the high three-quarter aerial, per stage 2 of
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

1. **First build.** Bounding-box top landed at 16.464 m, not 16.5: bevelling a
   knife-edge ridge apex cuts ~36 mm off it, which would have handed the loader a
   scale of 1.002. Fixed by giving the ridge a 0.30 m flat cap — which is what a
   real standing-seam gable is finished with anyway, and whose face holds its
   height however hard the edges are rounded.
2. **First aerial.** Two problems. The camera cropped the building: a 105 mm lens
   at 3.1 x span framed 43 m across a 45 m diagonal. Backed the camera off to
   4.4 x span rather than shortening the lens (style bible §18 wants the long
   lens). And the roof glazing, at 3.2 x 2.7 m panels, read as four blue pool
   covers; replaced with six narrow slots per slope lined up with the bays below.
   The loft windows at 2.5 m wide against a 2.95 m band read as a square
   institutional grid, so they were narrowed to 1.95 m to read vertical.
3. **Second aerial.** The gable did not read at all — azimuth 225° looks square
   onto the SW slope, so the roof rendered as a flat plane. Moved the review and
   beauty cameras to 255°, a true three-quarter to the building's own 135° axis,
   where the ridge silhouette, the hipped end and the exposed flank read
   together. Also: the ridge vents had been authored 0.16 m above the ridge and
   set the bbox top to 16.66 m — dropped flush with the ridge cap, where their
   0.95 m width still stands them ~0.22 m proud of the slopes.
4. **Third aerial.** 43 m of blank plinth under the loft rhythm; the commercial
   base went from three openings to five, widened, and moved onto the bay grid —
   the first attempt used round numbers and the ground openings sat visibly
   between the bays above them.
5. **First night render.** Every glow surface rendered as a pure white slab. This
   is the failure `docs/asset-plans/README.md` documents at the bottom: glTF
   writes `emissiveFactor = 0` when the authored emission strength is 0, so a
   re-imported `_Glow` material carries a **default white** emission colour, and
   a review rig that simply raises `Emission Strength` lights that white. The rig
   inherited from `artifacts/380-brannan/render_380_brannan.py` does exactly
   that. Fixed here by copying Base Color into Emission Color at strength 1.0,
   which is also what the app does — its night layer is an unlit overlay drawn at
   the material's own baked colour. **`artifacts/380-brannan/` still carries the
   uncorrected rig and its committed night render should be re-checked.**

## 4b. Optimize pass (stage 4)

`optimize/REPORT.md` has the full record. Headline: 121 draw submeshes → 9,
8,680 verts → 2,336, raw file −52.1%, triangles unchanged because every triangle
in this asset is on a visible surface. All eight gates pass; the A/B pixel delta
is 0.0002% at the near day camera.

One finding worth carrying to other assets: the generic Phase-B weld averages
loop normals at welded seams and put a visible-under-amplification smooth
gradient across this building's roof slopes. A flat-shading re-assert after the
weld restores the authored state and takes the delta to zero. It is generic, not
asset-specific, and belongs in `tools/glb-optimize/optimize.py` once a second
asset confirms it.

## 5. Design decisions worth recording

- **The proportion is the identity.** 43.21 x 13.84 m, 3.1:1, running the whole
  depth of the block. Nothing else on this side of the oval is shaped like it,
  and nothing in the build was allowed to square it up.
- **The NE flank is authored blind.** 171 South Park abuts it and reaches 11 m
  against this building's 11.82 m eave, so in reality only the roof clears the
  neighbour. It gets recessed blind bays on the same rhythm as the exposed flank
  — articulation the aerial camera can read, without inventing a window grid on
  a fire wall.
- **The roof furniture is grouped where it was observed**, at the Varney end, on
  a flat deck rather than scattered along 43 m of slope. The LiDAR mean sits
  1.03 m below its median, so roughly a sixth of the footprint is well under the
  main roof; the flat section is the reading that satisfies both the statistic
  and the image.
- **No roof deck.** Permit 200108166212 changed the designed roof deck to an
  unoccupied roof in 2001, so there are no railings, planters or paving.
- **Night state.** Six of the twenty loft windows on the exposed SW flank, two of
  its roof glazing slots, and the storefront and entry canopy at the park end.
  The alley end and the party wall stay dark — a service alley that glowed would
  misread. All glow surfaces are thin shells proud of the opaque glazing, since
  the app draws `_Glow` in a separate layer at ~12% alpha by day.

## 6. What is NOT verified in this asset

This model was built without street-level photography. Google Maps and Street
View were unreachable from the authoring session, Bing Streetside has no coverage
on this block, and Bing's 3D mesh would not render. One nadir aerial image is the
only picture of this building that informed the build.

Verified and reliable: the footprint, the anchor, the orientation, the storey
count, the programme, the roof's form and material, and the height.

**Not verified, and shipped anyway:**

- **The facade material and colour.** The body is `Toy_stone` (`#d9d2c2`), a
  neutral chosen because no evidence pointed anywhere else — not because the
  building is known to be that colour. If a photograph shows a warmer stucco, a
  metal-panel element or a signature accent, this is the first thing to change.
- **The window rhythm and bay count.** Ten bays at 4.32 m centres is a
  proportion guess.
- **The eave line at 11.82 m** is arithmetic from the LiDAR distribution
  (section 2), not a measurement.
- **The two-wall-storeys-plus-loft-in-the-roof layout** follows from that eave
  line. If the eave is really at 13 m, the building has three wall storeys and a
  shallower roof, and section 5's massing is wrong.
- **The extent of the Varney-end flat roof** (6.5 m modelled) is an estimate.
- **The South Park and Varney elevations' detail** — storefront width, entry
  position, garage door size — is inference from the permit record.

One street-level photograph would settle all of it. Until then this asset is
honest about being a well-measured massing with an inferred skin, and the plan's
Part 1 photo gate stays open for whoever gets there first.

## 6b. Integration QA (stage 5, batch mode)

Run locally against `npm run dev` on the re-baked tree. Batch mode: the bake was
run for this QA and then discarded, and the branch commits source only.

| Check | Result |
|---|---|
| Manifest entry / `camelId` round trip | PASS — `181-south-park` -> `181SouthPark`, matches `pipeline/lib/landmarks.mjs` |
| Loader merge line | `sf-assets: 181-south-park merged 9 objects / 9 materials -> batched (3109 tris body); uniform x1.0000 at 3783, -1189` |
| **Scale** | **x1.0000** — authored height and `targetHeightM` agree exactly |
| Exactly one building on the site | PASS — no procedural twin, no baked block poking through, no z-fighting |
| Terrain seating | PASS — placed at y 7.3835, the sampled ground there; no float, no sink |
| Orientation | PASS — long axis parallel to the block, hipped end toward South Park, garage end toward Varney Place |
| Night glow | PASS — only the intended `_Glow` surfaces light: a scatter of SW-flank windows, two roof glazing slots, storefront and canopy. Alley end and party wall stay dark |
| Draw calls | PASS — peak 86 at this station, budget < 300 (AGENTS rule 2) |
| `pipeline/audit.mjs` check 1.6 | PASS — no procedural footprint inside a bespoke landmark exclusion zone, 42 landmarks clear |
| `pipeline/verify-rebake.mjs` | PASS — 584/585 cells unchanged; only 23_13 moved, 233 -> 232 buildings; nearest surviving footprint 7.6 m against a 5 m radius |
| **Fallback drill** | PASS — see below |

**Re-bake attribution.** Exactly one building tile changed (`23_13.bin`, this
landmark's cell) and its count dropped by exactly one. Terrain, landcover and
street tiers came out byte-identical to `origin/main`, so the seeded
`pipeline/data/` snapshot matches the vintage that baked main and there is no
drift to attribute — unusual for this pipeline, and worth knowing the check came
out clean. The other 580 changed files are the context/ctx tier and `api/_data`,
which `validate.mjs` and `context.mjs` republish wholesale every run.

`audit.mjs` reports 3 unrelated failures — 1.2b (citywide p95 building height),
1.3c (Telegraph Hill terrain elevation vs the Terrarium DEM) and 1.7b (one of
793 sampled trees offshore). None of them is this landmark's: 1.3c and 1.7b read
terrain and landcover tiles that this bake left byte-identical to `origin/main`,
and 1.2b is a percentile over 174,754 buildings that removing one 14 m footprint
cannot move.

**Fallback drill (AGENTS rule 3).** With
`app/public/sf-assets/landmarks/181-south-park.glb` renamed away and the page
reloaded: the app boots normally, the whole area renders (streets, trees,
neighbours, traffic), and the console carries exactly one warning —

```
sf-assets: 181-south-park failed to load (Unexpected token '<', "<!doctype "... is not valid JSON)
```

— which is the streamed-asset path's per-asset warning (the dev server answers a
missing `.glb` with `index.html`; in production it is a 404). The site is empty
ground inside the exclusion zone. That is the expected Case B outcome, not a
regression: there is no procedural stand-in to fall back to, because the
exclusion removed it. No crash, no hole in the terrain, no missing tiles. File
restored afterwards and verified byte-identical to the artifact.

## 7. Approval

Stage 3 of the pipeline is the human gate. The user's instruction for this
session, verbatim, on 13 August 2026:

> build to the inferred reading and flag it in REPORT.md. continue going -- dont
> ask me for permission its all good!

That is a pre-authorisation given **before** seeing any render, not a review of
the images below. It is recorded here as what it is. The renders in this folder
are the first ones the user has had the chance to look at, and if the inferred
skin is wrong, section 6 is the list to work through.
