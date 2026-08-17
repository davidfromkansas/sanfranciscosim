# 41–43 South Park — build report

**What was built:** a validated miniature GLB of the 1911 Edwardian two-flat at
41–43 South Park, San Francisco, for the SF-SIM toy-diorama city. It lives at
`artifacts/41-south-park/41-south-park.glb`.

`REPORT.md` and `REFERENCE.md` beat `docs/asset-plans/41-south-park.md` wherever
they disagree. Every disagreement is listed in §3.

## 1. Shipped numbers

| | Pre-optimize |
|---|---|
| Objects | 72 |
| Triangles | **6,380** (cap 8,000) |
| Dimensions (AABB) | 22.456 × 22.473 × **10.600** m |
| Oriented footprint | **7.297 × 24.0 m** (25.15 m including the 0.95 m bay projection and the 1.20 m stoop) |
| `min Z` | 0.0000 |
| XY centre offset | 0.0000, 0.0000 |
| Materials | 11, all `Toy_*`, no `Toy_body` |
| Glow materials | `Toy_glass_Glow`, `Toy_glassl_Glow`, `Toy_gold_Glow` |
| Textures / cameras / lights / animations | 0 / 0 / 0 / 0 |
| Degenerate triangles | 0 |
| Signed-volume outward objects | 72 / 72 |
| Visibility-ray flipped fraction | **0.0032%** (1 of 31,500) — gate is ≤ 0.15% |
| File size | 380 KB uncompressed (gate is ≤ 500 KB compressed) |

The AABB is 22.5 × 22.5 m for a building that is 7.3 × 25.2 m. That is the
135.22° heading, not a scale error — the model is authored in world space so the
loader applies no rotation.

**Height normalization.** The bounding-box top is exactly **10.600 m** and it is
the cornice crest — not the parapet (10.10), not the terrace guard (10.48), not
the spa (10.47). The loader's `targetHeightM / measuredHeight` therefore lands on
1.0000.

**Anchor.** `DESIGN_ANCHOR` (the footprint's area centroid) is
`-122.3934770, 37.7815017`. The build recentres the model on its XY bbox centre,
a shift of (−0.199 m E, +0.206 m N), so the **manifest anchor is
`-122.3934793, 37.7815036`**. The shift exists because the stoop and the bays
hang off the front of the lot.

**Headings.** Street elevation faces **315.22°**; lot axis **135.22°**.

## 2. Contract validation

`validate_41_south_park.py` factory-resets Blender, re-imports the exported GLB
into a fresh isolated scene, and validates the re-import — never the authoring
scene. Full machine-readable output in `validation.json`.

**Overall: PASS.** All sixteen checks pass:

| Check | Result |
|---|---|
| metres and plausible dimensions | PASS |
| crest normalized to 10.60 m target | PASS |
| base at z = 0 | PASS |
| centred in XY | PASS |
| under triangle budget (6,380 / 8,000) | PASS |
| no image textures | PASS |
| no transparency | PASS |
| materials follow contract | PASS |
| no cameras or lights | PASS |
| no animation, skinning or constraints | PASS |
| transforms applied | PASS |
| no negative scales | PASS |
| normals outward — per-object signed volume | PASS (72/72) |
| normals outward — visibility-ray residual | PASS (0.0032%) |
| no degenerate geometry | PASS |
| no unexpected objects | PASS |

One deliberate WARN, not a FAIL: **`Toy_red` carries the off-palette hex
`6e3947`.** The real oxblood has no close palette entry (`Toy_rust` `a86444` is
far too orange, the palette's own `Toy_red` `c4453c` far too bright), the style
bible's San Francisco exception sanctions a tinted residential facade, and this
accent is the building's second-strongest recognition cue. The material keeps a
palette *name*, so the contract check and the loader's merge path are unaffected
— the same device `165-south-park` used for its siding.

## 3. Corrections made to the plan

**REPORT beats plan.** Ten changes were made to `docs/asset-plans/41-south-park.md`
during the build. Two of them were real bugs found by the validator.

### Bugs

1. **The arch spandrel polygon duplicated its two springing corners.** The
   semicircular arc was generated inclusive of `ang = 0` and `ang = π`, which
   repeats the rectangle's bottom two vertices. Blender exported degenerate
   slivers there, and the object accounted for **28 of the 52 flipped
   visibility rays**. Fixed by generating interior arc points only
   (`range(1, steps)`), and the arc was refined from 10 segments to 12.

2. **`inset_polygon()` resolved "inward" against the building's footprint
   centroid.** That is correct for the roof parapet, which is concentric with the
   building, and wrong for anything that is not: the spa's ring sits about 5 m
   off that centroid, so the near half of the ring inset *outward* and the
   annulus self-intersected. It accounted for **23 of the remaining 24 flipped
   rays**. Fixed by giving `inset_polygon()` and `rim()` an explicit `centre`
   argument, defaulting to the old behaviour so the parapet is unchanged.

   Normals residual across the three passes: 51 rays (0.162%, FAIL) → 24 rays
   (0.076%) after fix 1 → **1 ray (0.0032%)** after fix 2. Every per-object
   signed volume was positive throughout; the ray test is what found both.

### Design corrections

3. **The body split moved from the arch crown (5.15 m) to the storey line
   (5.60 m).** The building is two closed solids because the ground storey
   carries the entry notch. Split at the crown, the seam rendered as a second
   horizontal line 0.45 m below the bay's belt course, and on a blank 24 m party
   flank two parallel lines that close together read as a modelling error.

4. **The roof terrace moved from mid-roof to the front half** (u 12.5–15.5 →
   9.6–13.4) and grew from 4.0 × 3.0 to 4.2 × 3.8 m. The plan placed it on the
   nadir imagery alone; three independent sources say it *overlooks South Park*,
   and mid-roof left 12 m of blank membrane at the street end, which is where
   the app's camera looks first. The imagery's registration error on this block
   is 2–3 m, so both readings are satisfied.

5. **A slatted timber guard (0.45 m) was added on the terrace's street edge and
   two flanks.** It is what makes the deck read as an occupied place rather than
   a coloured rectangle, and it is the only thing on the roof with a vertical
   face. It was first drawn at 0.60 m, which put its top at 10.63 m and stole
   the bounding-box maximum from the cornice crest — the one number the loader's
   scale depends on. Reduced to 0.45 m (top 10.48 m).

6. **The spa shell became an annulus.** Built as a solid cylinder (the plan's
   recipe step 14), its top cap covered the water and the whole thing rendered as
   a grey pancake from the app's own camera angle. The water now sits 40 mm under
   the rim rather than 70, because deeper than that the shell shadows it back to
   the same grey.

7. **Skylights enlarged from 1.2 × 0.9 m to 2.0 × 1.4 m.** The sources say "huge
   rollaway skylights"; at the plan's size they read as two blue chips on an
   otherwise empty 24 m slab.

8. **A roof hatch was added** (0.55 m tall, 1.5 × 1.3 m), which the plan's recipe
   does not list. It is inferred from function rather than from a source: a roof
   terrace has to be reachable. It is also the only structure on the present roof
   that could plausibly relate to the unexplained 11.88 m LiDAR maximum, and it
   is nowhere near that height.

9. **A 0.03 m overlap (`LAP`) was introduced at every stacked interface** —
   window relief layers into their host wall, cornice band to cornice band, bay
   aprons into the bays, stoop riser into riser, roof furniture into the deck,
   recess linings into the notch. Butted solids leave coincident face pairs; this
   was a systematic cleanup done while chasing the normals residual. It was *not*
   the cause of the residual (bugs 1 and 2 were), but it is correct and it stayed.

10. **The dentil course is a continuous pale band, not modelled dentils.** The
    plan sanctioned this; recording it because it is the most visible
    simplification on the facade. At 300–500 m a pale line under a dark crown is
    exactly the dentil read, and 24 modelled blocks would have cost ~1,200
    triangles.

## 4. Judgment against the plan's "must capture" list

| Cue | Delivered |
|---|---|
| 1. The asymmetric bays — SW two-storey, NE one-storey | Yes. Verified in the aerial and north-west renders. |
| 2. The oxblood top-storey NE bay | Yes, `Toy_red` `6e3947`, on that bay and nothing else. |
| 3. The recessed arched entry on a stoop | Yes — a real 0.80 m notch in the ground-storey plan with a 12-segment arch spandrel across it and five risers climbing in. It reads as a hole, not a painted arch. |
| 4. The heavy bracketed cornice with a dentil band, returning over each bay | Yes — three bands following the front profile *including* both bay projections. It is also what draws the street end in the top view. |
| 5. The garage door | Yes, 3.10 m wide, layered relief with three grooves. |
| 6. The 7.3 : 24 proportion | Yes, exactly, from the surveyed parcel. |
| 7. The roof terrace with its spa | Yes, plus two skylights and a hatch. |

**Mirror check (the plan's non-negotiable):** in the top and north-west renders
the **oxblood bay and the entry stoop are on the north-east half** and the
**garage is on the south-west half**, matching the Compass photograph read with
the park behind the camera. PASS.

## 5. Approval (pipeline gate 3)

The pipeline's stage-3 human gate was pre-granted for this session. David's
invocation, verbatim, 16 August 2026:

> BUILDING: 41-43 S Park St, San Francisco, CA 94107
>
> BATCH: yes
>
> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

Recorded as the gate-3 approval on **16 August 2026**. The contact sheet, the
day and night aerials and the numbers in §1 are presented in the session summary
rather than held for a reply; the pipeline continues to stage 4. This is a
standing pre-approval of the asset review only — it does not extend to pushing,
opening a PR, or deploying, which `ADDRESS-TO-ASSET.md` stage 5 reserves for an
explicit instruction.

## 6. Files

| File | What it is |
|---|---|
| `build_41_south_park.py` | the deterministic build — `blender -b --python build_41_south_park.py -- [--out DIR]` |
| `render_41_south_park.py` | the review rig — add `--night` for the dusk pass, `--only aerial` for the iteration view |
| `validate_41_south_park.py` | fresh-scene contract validation → `validation.json` |
| `make_contact_sheet.py` | composes the seven renders into the contact sheet |
| `41-south-park.blend`, `41-south-park.glb` | the authoring scene and the shipping asset |
| `REFERENCE.md` | the verified dossier: sources, dimensions, orientation, every elevation, uncertainties |
| `validation.json` | machine-readable validation output |
| renders | `-aerial`, `-aerial-night`, `-top`, `-north-west`, `-north-east`, `-south-east`, `-south-west`, `-contact-sheet` |

## 7. Draft manifest entry

```json
{
  "id": "41-south-park",
  "file": "41-south-park.glb",
  "anchor": [
    -122.3934793,
    37.7815036
  ],
  "targetHeightM": 10.6,
  "cat": 1,
  "name": "41–43 South Park",
  "estimated": true,
  "dims": [
    22.4556,
    22.4731,
    10.6
  ],
  "tris": 6380,
  "loadRadius": 2500
}
```

`"estimated": true` because the 10.60 m crest is photogrammetric, not published
(`REFERENCE.md` §9.1). `cat: 1` is House. `loadRadius` is the default rule,
`max(2500, 10.6 × 30) = 2500`.
