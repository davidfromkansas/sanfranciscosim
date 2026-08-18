# 49 Zoe Street — build report

**What this is:** a validated miniature GLB of 49 Zoe Street, a 16-unit artist
live/work loft building of 1996–97 in SoMa, San Francisco, re-clad in 2011–13.
Built for the SF-SIM toy-diorama city under `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

**Authority order:** `REPORT.md` beats `REFERENCE.md` beats
`docs/asset-plans/49-zoe.md`.

## Deliverables

| File | What it is |
|---|---|
| `build_49_zoe.py` | deterministic Blender build (5.2 LTS, headless) |
| `49-zoe.blend` | the source scene |
| `49-zoe.glb` | **the shipping asset** |
| `render_49_zoe.py` | the controlled review rig (re-imports the exported GLB) |
| `validate_49_zoe.py` | fresh-scene contract validation |
| `make_contact_sheet.py` | composes the contact sheet |
| `validation.json` | the machine-readable validation result |
| `49-zoe-{north,east,south,west,top,aerial,aerial-night}.png`, `49-zoe-contact-sheet.png` | review renders |

Rebuild: `blender -b --python build_49_zoe.py`
Re-render: `blender -b --python render_49_zoe.py -- --samples 48` (add `--night`)
Re-validate: `blender -b --python validate_49_zoe.py`

## Numbers as shipped

| | |
|---|---|
| Triangles | **7,688** (cap 11,000) |
| Mesh objects | 216 |
| Dimensions (x, y, z) | **34.108 × 34.613 × 17.000 m** |
| min Z | 0.000 |
| XY centre offset | (−0.029, −0.237) m |
| Materials | 12, all `Toy_*`, of which **3** are `_Glow` |
| Image textures / transparency | none / none |
| File | 492.2 KB raw, **74.2 KB gzip** (pre-stage-4) |
| Anchor | −122.3960338, 37.7800764 |
| Zoe elevation heading | 225.4° true |
| Target height | **17.00 m** |

The 34.1 × 34.6 m axis-aligned bounding box is the expected consequence of a
45.4° real-world heading on a 28.24 × 19.78 m plan — not a scale error. The y
extent runs 0.4 m longer than the x extent because the entry awning projects
0.90 m from the south-west (Zoe) wall.

## Validation — gate 2

`validation.json`, produced by re-importing `49-zoe.glb` into a **fresh isolated
Blender scene** (the source `.blend` is not inspected). **Overall: PASS.**

| Check | Result |
|---|---|
| meters and plausible dimensions | PASS |
| crest normalized to target (17.00 ± 0.02) | PASS |
| base at z = 0 | PASS |
| centered in xy | PASS |
| under triangle budget | PASS (7,688 / 11,000) |
| no image textures | PASS |
| no transparency | PASS |
| materials follow contract | PASS |
| no cameras or lights | PASS |
| no animation, skin or constraints | PASS |
| transforms applied | PASS |
| no negative scales | PASS |
| normals outward — per-object signed volume | PASS (216/216 positive, 0 inverted) |
| normals outward — ray residual | PASS (**31,500 rays, 0 flipped, 0.000%**) |
| no degenerate geometry | PASS (0) |
| no unexpected objects | PASS |

Normals were tested two ways, as the pipeline requires: per-object signed volume
is authoritative for this union of interpenetrating solids, and 31,500
deterministic visibility rays fired inward at nine interior targets provide the
secondary check. Both are clean, so the 0.15% residual allowance was not needed.

## Corrections and decisions made during the build

**Nothing in the plan's dossier was found to be wrong.** Every load-bearing
number — the anchor, the 28.24 × 19.78 m plan, the 45.4° heading, the 14.4 m roof
plane, the 17.0 m crest, the two-tier arrangement — survived re-verification.
Eight authoring decisions were taken on top of it:

1. **The round vent on the penthouse is the crest, not the penthouse cap.** The
   plan put the cap at 17.00 m with a vent on top; that would have pushed the
   bounding box to 17.37 m and broken the `targetHeightM / measuredHeight = 1.0`
   normalisation. The penthouse now runs to 16.62 m, its cap to 16.78 m, and the
   0.22 m round vent lands the crest on exactly 17.00 m. This is also the truer
   reading of the aerial, where the round element sits on the penthouse roof.

2. **The white spandrel band between each unit's window and its mezzanine was
   dropped.** In the first pass the four bays read as four white columns and the
   stripe identity disappeared. The rectified elevation shows the cladding running
   continuously between the two windows of a unit; it now does so in the model.

3. **The stripe count went from 17 to 23, and the window width from 3.50 m to
   3.20 m.** With 17 bands and 3.5 m windows, roughly half the pattern was hidden
   behind glazing and the facade read as a plain pale box with a few accents. 23
   narrower bands is closer to the real ~30 and survives the windows.

4. **The stripe relief was increased to 0.18 m proud / 0.02 m flush** (from
   0.13 / 0.06). Every stripe tone on this building is pale; the shadow line is
   what makes the rhythm read once the app's flatter lighting washes the tonal
   differences out.

5. **The juliet rails are an open guard — top rail, one mid rail and two posts —
   not a stack of slats.** Three or four solid horizontal slats across a
   floor-to-ceiling window read as a venetian blind at the app's camera distance
   and shortened the tall window to a punched one. The rails project 0.30 m rather
   than the real ~0.15 m, which is the plan's sanctioned exaggeration.

6. **The monitor glazing is the top surface of each roof monitor.** Built the
   other way round — kerb, cheeks, then glass inside them — the three monitors
   rendered as plain white boxes from directly above, which is the one view the
   element exists for. The kerb is now low, the glass is the ridge, and the white
   mullions cross it.

7. **The penthouse cap is `Toy_white`, not `Toy_steel`.** A grey cap on a grey
   membrane made the penthouse vanish in the top view; the aerial shows it pale
   against the roof.

8. **The garage-door reveal is a border, not a panel behind the door.** The first
   attempt drew a full-size `Toy_ink` panel behind each roll-up door and the base
   read as five black holes — the darkest thing on an otherwise pale building. The
   door leaf now stands proud of its reveal, so the reveal reads as a shadow line.

### Simplifications recorded

- The DataSF ring's two 0.33 m in/out jogs on the south-east face are not
  modelled; the plan is a clean rectangle. Every survey vertex is within 0.09 m.
- ~30 real cladding stripes become 23; the real mullion grids become single panes;
  the CMU coursing becomes one horizontal reveal at 1.50 m.
- The north-east and south-east elevations carry six and three punched openings
  respectively — a simplification of oblique satellite pixels, and *inferred*
  rather than observed. See `REFERENCE.md` §7 trap 7.

## Palette as shipped

| Material | Hex | Used for |
|---|---|---|
| `Toy_white` | `#f7f4ec` | lightest stripe, parapet coping, window frames, monitor mullions, skylight kerbs, penthouse, roof-deck walls |
| `Toy_trim` | `#f3efe6` | one stripe |
| `Toy_sand` | `#ece4d4` | warm pale stripe; the three non-street walls and the body |
| `Toy_stone` | `#d9d2c2` | the split-face CMU base, roof-deck paving, the party-wall reveal, side-window surrounds |
| `Toy_verdigris` | `#9fb8a8` | the sage stripe — the only stripe tone with hue in it (4 of 23 bands) |
| `Toy_steel` | `#9aa0a6` | blue-grey stripe, roof membrane, roll-up doors, juliet rails, entry awning, vent cans, roof hatch |
| `Toy_glass` | `#2a4d73` | loft glazing and the punched side windows |
| `Toy_glassl` | `#6f95b8` | monitor glazing and skylight domes |
| `Toy_ink` | `#3a3530` | fire escape, pedestrian and service doors, door reveals, base louvres |
| `Toy_glass_Glow` | `#6f95b8` | four lit loft windows |
| `Toy_glassl_Glow` | `#8fb4d8` | **the lit monitor spine — the night hero** |
| `Toy_gold_Glow` | `#caa64a` | two warm-lit loft windows and the strip under the entry awning |

All twelve are on the `sf-asset-check` palette except the two `_Glow` colours,
which are lit-appearance values rather than day tones — the app draws `_Glow`
unlit at the material's own base colour, so a night window that glows in its own
dark navy reads as a hole.

**Roof membrane note:** `Toy_steel` (mid grey) rather than `Toy_roofd`.
`Toy_roofd` renders near-black under the app's lighting; the aerial shows a
genuinely pale grey membrane, and a dark deck would also kill the white monitor
mullions and coping ring that make the roof read.

## Night state

Hero: **the monitor spine, lit end to end.** The internal circulation of a
16-unit building is on all night, and three glowing ridges down a dark roof is an
image no other asset in this district gives the app's downward camera.

Supporting: an uneven scatter of **six of the sixteen** loft windows on the Zoe
elevation — four `Toy_glass_Glow`, two `Toy_gold_Glow` — chosen so that no bay
and no row is fully lit; plus a small warm strip under the entry awning. The
stripes, the base, the roll-up doors, the roof deck and the three non-street
elevations do not glow.

Every glow surface is a thin shell standing proud of the opaque geometry behind
it. The app renders `_Glow` in a separate layer at roughly 12% alpha per layer by
day, so no primary surface is authored as glow and no glow shell wraps one.

**What `49-zoe-aerial-night.png` can and cannot tell you:** it judges *which*
surfaces glow and how restrained the scatter is. It does not judge the night
palette — any emission strength above ~1.0 clips these colours to white under the
Standard view transform, and the app draws the glow layer unlit at the material's
own baked colour. Read the palette off the table above, not off the render.

## Render rig

Blender 5.2 LTS, **EEVEE** at 48 samples, `view_transform = "Standard"`. The rig
re-imports the exported GLB into an empty scene, so every image depicts exactly
the geometry that ships. The four elevations share one camera rig — same
orthographic scale, framing, lighting, exposure and projection — and differ only
in azimuth; directions are true compass directions (north = Blender +Y).

The engine is EEVEE rather than CPU Cycles on purpose: this machine routinely runs
a dozen concurrent landmark sessions and was at load 250 during this build, where
a single 1200×1000 CPU-Cycles frame takes minutes and often never finishes. The
same rig in EEVEE renders all six frames in seconds with shadows, flat materials
and the glow layer intact, and nothing gate 2/3 judges — silhouette, massing, the
stripe rhythm, which surfaces glow — needs path tracing.

The **`south`** view is the one to read: it looks down the Zoe elevation's outward
normal, which is this building's subject. The **`top`** view is where a lazy roof
would be caught on a building this plain.

## Draft manifest entry

Do not apply this here — integration is a separate job
(`docs/asset-plans/INTEGRATION-PROMPT.md` plus `docs/asset-plans/49-zoe.md` §2.13).

```json
{
  "id": "49-zoe",
  "file": "49-zoe.glb",
  "anchor": [
    -122.3960338,
    37.7800764
  ],
  "targetHeightM": 17.0,
  "cat": 2,
  "name": "49 Zoe Street",
  "estimated": false,
  "dims": [
    34.108,
    34.613,
    17.0
  ],
  "tris": 7688,
  "loadRadius": 2500
}
```

`loadRadius` follows the default rule `max(2500, 17.0 × 30)` = 2500. Not
`alwaysLoaded`: at 17 m this is neighbourhood fabric, not a skyline piece.
`estimated: false` — the anchor and plan are surveyed and the height is
LiDAR-derived.

**Case B** at integration: no `49-zoe` id exists in `pipeline/lib/landmarks.mjs`
or `app/src/landmarks.js`, so it needs a registry entry and a tile re-bake. The
exclusion radius must be **measured against the real bake inputs** (DataSF *and*
Overture), not reasoned about — and the party wall with 33–35 Zoe touching at
0.00 m is the hard constraint. See `docs/asset-plans/49-zoe.md` §2.13.

## Gate 3 — approval

Pending.
