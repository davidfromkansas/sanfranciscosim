# F-line PCC streetcar — build report

**Deliverable:** `artifacts/f-line/f-line-pcc.glb` — one validated miniature
streetcar, 1,923 triangles, 52,920 bytes, **PASS** on every gate.

Built to [`docs/asset-plans/transit/historic-streetcar.md`](../../docs/asset-plans/transit/historic-streetcar.md)
Part 1. Research dossier: [`REFERENCE.md`](./REFERENCE.md). Nothing in
`app/` was modified; the manifest entry below is a **draft**, not applied.

---

## THE ONE THING THE INTEGRATION MUST KNOW

**This asset does not work until `agents.js` learns `kitfleet.js`'s per-instance
tinting.**

The car ships with its livery panels on a material named **`Toy_body`**,
authored near-neutral `#d8d3c8`, exactly as the 207-piece building kit authors
its tintable pieces. Five cities-series liveries are then five per-instance
colours over **one geometry and one draw call**.

`loadVehicles()` in `app/src/agents.js` does not implement that today.
`mergeVehicle()` bakes each material's colour into vertex colours and hands one
shared `MeshLambertMaterial` to an `InstancedMesh`, so **as of today this car
loads and renders correctly but comes out warm off-white on every instance** —
it degrades to one bland colour, not to an error. The fallback is silent, which
is the whole reason this section is at the top.

What the port needs, from `app/src/kitfleet.js`:

```js
// Toy_body is authored mid-warm-grey, and the batch colour multiplies it, so
// a tint has to be divided by the body colour to land on the palette entry.
const BODY_BASE = new Color().setRGB(0.694, 0.659, 0.586);   // = #d8d3c8
```

The asset is authored against that exact constant. `loader-roundtrip.json`
records that `Toy_body` arrives through the app's own `createGLTFLoader()` at
**`#d8d3c8`**, so the division lands where `KIT_TINTS` expects it.

Three practical notes for whoever does the port:

- The tint must apply **only** to the `Toy_body` share of the merged geometry.
  Everything else — roof, glazing, reveals, doors, trucks, wheels, pole,
  anti-climbers, headlight, route board — is deliberately on fixed materials so
  a tint cannot wash the trim out. In the current `mergeVehicle()` those colours
  are already baked per-vertex, so a per-instance multiply over the whole
  geometry would tint the silver roof too. The port needs either a per-vertex
  tint **mask** (a second vertex attribute, 1 on `Toy_body` faces and 0
  elsewhere) or `kitfleet.js`'s `BatchedMesh` route.
- `Toy_body` is on **exactly one object** in the file (`body_shell`, 428 of the
  1,923 triangles), so the mask is trivial to derive at merge time from the
  source material name — no authoring change needed.
- The livery sheet (`renders/f-line-pcc-livery-sheet.png`) was rendered by
  reproducing that arithmetic, clamp included, in `render_scenarios.py`. It is
  the evidence that the design works before any code is written.

**The fallback, surfaced as a decision, not taken silently.** If the tinting
port is rejected, ship **three** baked-livery GLBs — Muni "Wings", St. Louis and
Baltimore, the three most distinct — not five. That is **3 permanent draw
calls instead of 1** against AGENTS rule 2's 300-call budget, and it changes the
manifest from one entry to three. Five would be five draw calls for one
silhouette and is not defensible. This report does **not** pick that path.

---

## What was built, and the decisions behind it

**The car is Muni's 1050 class** — ex-Philadelphia Transportation Company,
built 1947–48, 13 operational, **single-ended**, `48′5″ × 8′4″ × 10′3″` =
**14.76 × 2.54 × 3.124 m**. It is the largest operational class on the line.
Full reasoning and the fleet table in [`REFERENCE.md`](./REFERENCE.md) §2–3.

**This supersedes the plan's `targetLengthM: 14.0`**, which is the bottom of the
generic worldwide PCC range rather than a San Francisco car. AGENTS rule 5 says
real dimensions; 14.76 m is the real dimension. The draft manifest below uses it.

**`min y = 0` is the wheel contact patch — the top of rail.** The plan asks for
that statement explicitly, and it needs one qualification: the scene contains no
rails (the transit README's no-rails-no-wires decision), so top of rail
coincides with the street surface and the car grounds exactly like a bus. The
practical consequence is that a real PCC's body sits one rail-head (~0.15 m)
higher above the pavement than this model does. At 1.6× that is 0.24 m of a
23.6 m vehicle and nothing in the scene can reveal it.

**Three judgement calls worth challenging:**

1. **The roof is silver, not charcoal.** The plan's §2.8 specifies `Toy_roofd`.
   The first aerial review render showed why that is wrong here: a charcoal lid
   on a 14.76 m object is the largest single surface at the app's 42° camera and
   it swallowed the whole silhouette — the livery, which is the entire point of
   the asset, could not be read. It is also less accurate: 1063 wears a "Pearl
   gray roof" and 1009 a "silver roof". The roof is `Toy_steel` with `Toy_roofd`
   ventilators and drip rails, which gives the crown rhythm and an edge.

2. **The tinted band is taller than the real livery split.** On a real two-tone
   PCC the body colour stops at the window sill and cream carries everything
   above. Authored that way, the tint owned only the bottom 1.3 m of a 3.12 m
   car and every livery read as cream from the app's camera. `Toy_body`
   therefore runs from the skirt up to the **window head** and the cream is
   compressed to the letterboard band between the window head and the roof
   crown. This is style-bible §9/§26 semantic exaggeration and it is deliberate:
   silhouette carries the era, colour carries the identity, and the colour has
   to be visible for that to be true. Every livery in the sheet still reads as
   the real scheme.

3. **The trolley pole is 4.5 m at 20°, not 5.5 m at 30°.** The plan's geometry
   puts the shoe 6.0 m above the rail and 0.8 m beyond the tail — at the app's
   1.6× render scale, a 9.6 m mast reaching for an overhead wire the scene does
   not contain, dominating the silhouette of every heritage car in the city. The
   pole is authored trailing along the roof instead: it still reads as period
   hardware, it stays inside the car's own length, and it is not something a
   viewer tries to trace upward. The plan's §2.16 raises this question and
   leaves the geometry open; this is the answer, and it is reversible in one
   constant (`trolley_pole()` in `build_f_line.py`).

**Recognition cues delivered:** rounded raking nose over the anti-climber ·
crowned roof curving down into it · wrapped two-pane windscreen · **single
central headlight** · ten-window rhythm behind a recessed chamfered band · metal
anti-climbers · trolley pole with base, tapered shank and shoe · standard-gauge
1.435 m wheels, visibly wider than the cable car's 1.067 m.

**Liveries chosen and rejected** — five chosen from real F-line cars, five
documented rejections including Pacific Electric (three colours) and the Market
Street Railway zip stripe (identity lives in the roof, which is fixed). Table
with sources in [`REFERENCE.md`](./REFERENCE.md) §5.

---

## Validation — shipped file

`validation-final.json` (fresh Blender scene, re-imported `f-line-pcc.glb`),
reported in glTF/three space.

| | |
|---|---|
| Objects | 8 |
| Triangles | **1,923** / 4,000 budget |
| Dimensions (x, y, z) | **2.566 × 4.904 × 14.760 m** |
| bbox min / max | `[-1.283, 0.0, -7.380]` / `[1.283, 4.904, 7.380]` |
| Body height (rail → roof crown) | **3.124 m** = published 10′3″ |
| **min y** | **0.0000 m** = the wheel contact patch = top of rail (= street surface, no rails in scene) |
| XZ centre offset | `[0.0000, 0.0000]` |
| **Front face** | **−Z**, proved by asymmetry: headlight glow at z −7.368…−7.318, tail-light glow at z +7.320…+7.375 |
| Wheel gauge | 1.435 m (measured on the authored export; the wheels are joined away by the shrink pass) |
| Materials | `Toy_body` `Toy_cream` `Toy_glass` `Toy_ink` `Toy_mustard_Glow` `Toy_red_Glow` `Toy_roofd` `Toy_steel` `Toy_white_Glow` |
| **`Toy_body` present and separately addressable** | **yes** — one material, one object (`body_shell`), 428 tris |
| Textures / cameras / lights / animations / armatures / constraints | 0 / 0 / 0 / 0 / 0 / 0 |
| Transforms applied | yes |
| Negative scales | none |
| Degenerate triangles | 0 |
| Non-unit or non-finite loop normals | 0 |

Height note: the bbox is 4.904 m because the trolley pole and the roof
ventilators stand above the crown. **3.124 m** is the figure that matches the
published dimension and it is gated separately.

Per-object signed volumes are all positive on the authored export and every
joined group is positive on the shipped one — `mergeVehicle()` reverses any
source mesh with negative volume, so a negative group would ship that whole
material inside out:

```
body_shell 96.871   grp_Toy_ink 6.379   grp_Toy_roofd 0.393   grp_Toy_steel 0.224
grp_Toy_glass 0.155  grp_Toy_mustard_Glow 0.126  grp_Toy_red_Glow 0.0036
headlight_lens 0.0023
```

### Contract checks

18 gates on the shipped file, 22 on the authored one (the four extra are
per-object checks the join makes structurally inapplicable). **All PASS.**

Both stages gate `toy_body_present_and_addressable` — the one check this asset
**inverts** relative to every other vehicle and landmark in the repo, which are
checked for `Toy_body`'s *absence*.

### Materials

| Material | Hex | Used for | Notes |
|---|---|---|---|
| **`Toy_body`** | `#d8d3c8` | **the livery panels — skirt to window head, and the nose fascia** | **TINTABLE.** This asset's sanctioned exception |
| `Toy_cream` | `#f2ede3` | letterboard band above the windows | fixed |
| `Toy_ink` | `#3a3530` | underframe, trucks, window reveals, doors, pole plinth and shoe, route-board backing, windscreen post | fixed |
| `Toy_glass` | `#2a4d73` | side windows, wrapped windscreen, rear window | fixed |
| `Toy_steel` | `#9aa0a6` | roof crown, anti-climbers, headlight bezel, pole shank | fixed |
| `Toy_roofd` | `#45454a` | ventilators, drip rails, wheels | fixed |
| `Toy_white_Glow` | `#f7f4ec` | headlight lens | night |
| `Toy_mustard_Glow` | `#d9a441` | route board, lit interior strips | night |
| `Toy_red_Glow` | `#c4453c` | tail lights | night |

All nine on the contract palette; **zero off-palette warnings**. Emission ships
at 0.0 on every glow material per contract.

### The night-glow set

Every glow surface is a thin shell **3.5 cm proud** of an opaque surface with its
back edge **buried 1.5–2 cm** inside it, because the loader draws `_Glow` in a
separate unlit layer at `opacity = 0.12 + 0.95 * uNight` — 88% transparent by
day, so an exposed shell edge would be visible at noon.

| Surface | Material | Reads as |
|---|---|---|
| Headlight lens | `Toy_white_Glow` | the PCC's single central lamp |
| Route board face | `Toy_mustard_Glow` | lit destination sign, with an extruded `F` standing on it |
| Interior ceiling strips | `Toy_mustard_Glow` | a warm lit vintage saloon |
| Tail lights | `Toy_red_Glow` | rear identification |

The interior strips are **broken at the doors** on the kerb side. Authored as two
continuous lines they read at night as a neon tube down each flank rather than
as light spilling out of a saloon; the breaks are what turn them back into
windows. Warmth is deliberately above the modern fleet's — these are
incandescent-era cars.

**This is the first `_Glow` set in the vehicle fleet.** All 15 shipped vehicle
GLBs have zero. Note that `mergeVehicle()` in `agents.js` has no `_Glow` branch
either — unlike `streetkit.js` and `ferries.js`, which both split on the name —
so today these four surfaces will render as ordinary opaque flat colours by day
and stay dark at night. That is a second, smaller integration dependency; it
does not break anything.

---

## Shrink stage

Run per the transit README Part 3, `ASSET_CLASS=vehicle`. `shrink-stats.json`.

| Step | Tris | Verts | Objects |
|---|---:|---:|---:|
| input (authored) | 1,924 | 1,092 | 65 |
| weld ≤ 1 mm + degenerate | 1,924 | 1,092 | 65 |
| interior faces | 1,923 | 1,092 | 65 |
| limited dissolve @ **0.05°** | 1,923 | 1,092 | 65 |
| join per material | 1,923 | 1,092 | **8** |

| File | Bytes |
|---|---:|
| authored | 134,404 |
| shrunk | 108,996 |
| **shipped** (gltfpack `-cc -kn -km -noq`) | **52,920** |

**Honest reading of that table: the geometry shrink pass removed one triangle.**
That is not a failure of the pass, it is what a model authored to its budget
looks like — there is no waste to remove. The size win is entirely the join
(65 objects → 8 primitives) and meshopt. The pass is still worth running and
worth keeping, because it is where the windings and the material set are
audited, and that is where it earned its keep on this asset (see below).

**Retessellation was skipped deliberately.** The wheels are 10-segment discs and
the pole a 6-segment shank, already authored against the vehicle camera band
(near 15 m, far 120 m) times the 1.6× render scale. Halving the wheels
flat-spots them against a street the car never leaves.

**Limited dissolve at 0.05°, not 0.5°.** The nose is nine lofted rings of 24-gon
cross-section; consecutive quads differ by a degree or two, which 0.5° merges
transitively into twisted ngons that re-triangulate with flipped windings.
`inverted_after_dissolve` is empty.

### `Toy_body` survival — checked three ways, not inferred

1. The join groups by material **set**, and the shell's set
   `{Toy_body, Toy_cream, Toy_glass, Toy_ink, Toy_steel}` is unique to it, so
   it cannot be folded into another group. `tintable_not_merged_into_another_material_group: true`.
2. `toy_body_survived: true` on the Blender re-import after the shrink.
3. **The shipped file's material list is read back out of the GLB JSON in
   `make.sh` and the build fails if `Toy_body` is missing.** Shipped list:
   `Toy_body Toy_cream Toy_steel Toy_ink Toy_glass Toy_mustard_Glow Toy_red_Glow Toy_roofd Toy_white_Glow`.

One finding worth recording: **on this asset `-km` turned out not to be
load-bearing** — a control run with `-cc -kn -noq` and no `-km` also preserved
all nine materials, because all nine differ in base colour. `-km` is kept
because the risk is one edit away: `Toy_body` `#d8d3c8` and `Toy_cream` `#f2ede3`
are both near-neutral warm whites, and anyone "harmonising" them would hand
gltfpack two identical materials to merge and kill the livery design silently.

### Gates

| Gate | Result |
|---|---|
| G1 Contract — material set identical pre/post, `_Glow` layer intact and separate, front `−Z` and min y = 0 preserved | **PASS** (`material_set_ok`, `glow_layer_intact`) |
| G2 Fidelity — bbox within max(1 cm, 0.1%), origin within 1 cm, per-group signed volume positive | **PASS** (`bbox_ok`, `merge_vehicle_safe`) |
| G3 Round-trip — re-imports in Blender **and** loads through `createGLTFLoader()` with the meshopt decoder | **PASS** — `loader-roundtrip.json`: `EXT_meshopt_compression` decoded, 1,923 tris, min y 0, `Toy_body` baked at `#d8d3c8`, **0 meshes `mergeVehicle()` would reverse** |
| G4 Appearance — day and night at 1.6× | **PASS** by review renders; **no A/B pixel delta was computed**, because with one triangle removed there is no meaningful before/after to diff. Stated rather than fudged. |
| G5 Draw calls — primitive count ≤ input | **PASS** — 65 objects in, 12 primitives out |
| G6 Size — smaller after the pass | **PASS** — 134,404 → 52,920 bytes (61%) |
| G8 Hygiene — no leaked objects, no `.blend1` | **PASS** — leak-proof export via a temp scene with `use_active_scene`, re-import object count verified; `.blend1` gitignored |

The high→low texture bake was **not** run, per the plan.

---

## Renders

`renders/`, all from the **shipped** GLB.

| File | What it shows |
|---|---|
| `f-line-pcc-front.png` | cab end: wrapped windscreen, single central headlight, route board, anti-climber |
| `f-line-pcc-rear.png` | single-ended rear: rounded lid, rear window, tail lights |
| `f-line-pcc-left.png` | blind flank, 10 windows |
| `f-line-pcc-right.png` | kerb flank, front and centre doors |
| `f-line-pcc-top.png` | silver crown, drip rails, ventilator line, pole |
| `f-line-pcc-aerial.png` | the app's camera, 42°, long lens |
| `f-line-pcc-night.png` | the glow set from a front three-quarter |
| `f-line-pcc-backlit.png` | silhouette at 120 m |
| **`f-line-pcc-in-city.png`** | **the 1.6× scale test** |
| **`f-line-pcc-livery-sheet.png`** | **all five tints, one geometry** |
| `f-line-pcc-livery-<city>.png` | the five individually |
| `f-line-pcc-contact-sheet.png` | everything above on one sheet |

### The 1.6× in-city scale test

The car stands on **the real baked Embarcadero** (tile cell 22_9, around Green
Street — F-line track on the Fisherman's Wharf leg), beside the shipped
`commuter-bus.glb` and `sedan-red.glb`, all three at `carScale = 1.6`. The PCC
renders at **23.6 m**.

**Verdict: it fits.** It reads as clearly longer than the 40-foot bus (17.2 m at
1.6×) and roughly three sedans, which is the correct relationship, and it sits
inside a block without straddling two intersections.

Worth recording for whoever does the next transit asset: **lower Market was the
first choice and had to be abandoned.** It is the more iconic F-line location,
but 79 of its 142 baked buildings clear 60 m, and at the app's 42° camera any
azimuth more than about 8° off the street axis puts the camera *inside* a tower
— the render came back as a flat grey wall twice. The Embarcadero has the same
F-line track and not one building over 60 m in the crop.

### The livery sheet

All five proposed tints, applied through `kitfleet.js`'s own arithmetic
(`min(2.5, target / BODY_BASE)`, clamp included) to the same shipped geometry,
from the app camera.

**Verdict: the design works.** Five distinct, clean liveries; none reads muddy;
the fixed cream letterboard and silver roof read as *livery* in all five rather
than fighting the body colour — the Baltimore car in particular is nearly the
real scheme, because "Alexandria Blue, Picador cream, Pearl gray roof" is
exactly this model's fixed trim plus one tint.

---

## Draft manifest entry — NOT APPLIED

`app/public/sf-assets/vehicles_manifest.json` was **not** edited, and neither was
`app/src/agents.js` or any other app code.

```json
{ "id": "f-line-pcc", "file": "vehicles/f-line-pcc.glb", "kind": "streetcar",
  "dims": [2.566, 4.904, 14.76], "targetLengthM": 14.76, "front": "-Z",
  "tris": 1923, "weight": 1,
  "tints": ["#2f7a55", "#c4453c", "#e0762f", "#e0af35", "#3f9aa8"],
  "notes": "Heritage vehicle, Muni 1050 class (ex-Philadelphia PTC), single-ended. One geometry, per-instance Toy_body tint supplies the cities-series liveries: Muni Wings / St. Louis / Boston Elevated / Los Angeles Railway / Baltimore Transit. Requires kitfleet.js-style tinting in agents.js — without it every instance renders warm off-white. min y = 0 is the wheel contact patch (top of rail; no rails in scene, so it grounds like a bus). dims y 4.904 includes the trolley pole; body height is 3.124 m." }
```

Three things the integration has to decide, flagged rather than assumed:

- **`tints` is a proposed manifest extension.** No existing entry has one. The
  alternative is a code-side palette table like `kitplan.js`'s `KIT_TINTS`,
  which is where the building kit keeps its equivalent. Either works; the asset
  does not care.
- **`targetLengthM: 14.76`, not the plan's 14.0** — see [`REFERENCE.md`](./REFERENCE.md) §2.
  No road vehicle entry currently uses `targetLengthM` (only the ferry does), so
  this may be informational.
- **`weight: 1`** puts the streetcar in the road spawner alongside cars and
  buses. That is what the plan's draft says and it is probably wrong once
  placement is designed — a streetcar on an arbitrary residential street is a
  data-accuracy problem (AGENTS rule 5). It belongs with the deferred placement
  work in [`INTEGRATION-LATER.md`](../../docs/asset-plans/transit/INTEGRATION-LATER.md),
  not in this asset.

---

## Reproducing

```bash
cd artifacts/f-line && ./make.sh
```

Runs in about a minute and is deterministic: build → validate authored →
shrink → gltfpack → validate shipped → app-loader round-trip → renders →
contact sheets. Every stage fails the script rather than warning.

| File | |
|---|---|
| `build_f_line.py` | the deterministic build, written as reusable component functions (`running_gear`, `glazing`, `trolley_pole`, `glow_plate`) because the deferred Milan Peter Witt car shares all of them but not the body |
| `validate_f_line.py` | fresh-scene contract validation, `--stage authored\|shipped` |
| `optimize_f_line.py` | the shrink pass |
| `loader_roundtrip.mjs` | gate G3 through the app's own loader |
| `export_city_cell.mjs` | exports the real baked Embarcadero for the scale test |
| `render_f_line.py` | elevations, roof, aerial, night; `--tint` applies one livery |
| `render_scenarios.py` | in-city 1.6×, the five liveries, backlit |
| `make_contact_sheet.py` | the two sheets |

Committed outputs: `f-line.blend`, `f-line-pcc.glb`, `validation.json`,
`validation-final.json`, `shrink-stats.json`, `loader-roundtrip.json`,
`renders/`. `build/`, `city-cell.json` and the authored GLB are derived and
gitignored.

---

## Known limitations

- **The car is monochrome until `agents.js` is changed.** Restated because it is
  the only thing that makes this asset less than finished.
- **The `_Glow` set is inert until `mergeVehicle()` learns the name suffix.**
  Smaller, and harmless.
- **No fleet numbers or system lettering.** Textures are forbidden and extruded
  numerals would cost more than the running gear for something illegible past
  20 m. Only the route `F` on the front board is modelled.
- **No standee windows.** Real and characteristic, but they merge into the
  window band they sit over at the app's camera distance.
- **Body width measures 2.566 m against the published 2.54 m** — the two kerb-side
  doors stand 12 mm proud of the flank, which is how a plug door reads. The XZ
  centre offset is still 0.0000 m because the glazing recess absorbs it.
- **G4 has no numeric A/B delta**, because the shrink pass changed one triangle.
  Judged by review render instead, and said so rather than reporting a
  meaningless 0.0%.
- **The 1928 Milan Peter Witt car is out of scope** per the plan's §2.17. The
  component functions in `build_f_line.py` are structured for it.
