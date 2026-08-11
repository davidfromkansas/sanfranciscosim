# Flora kit — asset plan

<!--
Planning document. Nothing here has been built: no GLB, pipeline code, tile data
or app code has been changed by this plan.
-->

| Field | Value |
|---|---|
| Kit | Flora kit (trees, shrubs, landscape props) |
| Slug | `flora` |
| Asset path | `app/public/sf-assets/flora/` |
| Index | `flora_index.json` |
| Build artifacts | `artifacts/flora-kit/` |
| Replaces | `toyTreeArchetype()` in `app/src/city.js` (kept as the fallback) |
| Instanced | yes — one shared `InstancedMesh` pair per species, city-wide |
| Pieces | 4 tree species + 4 landscape props (proposed) |
| Precedent | `app/public/sf-assets/streetkit/` (207-piece building kit, 15-piece street kit) |

**In one sentence:** replace the single procedurally-generated lollipop tree that
every one of San Francisco's 289,741 baked trees currently uses with a small
Blender-authored kit of species archetypes, loaded and instanced exactly the way
the street furniture kit already is.

---

## Why this is a kit and not 289,741 assets

The constraint is not modelling effort, it is instancing. Every tree in the city
is drawn from **one** geometry via `InstancedMesh`, which is the only reason
289,741 of them cost almost nothing. Authoring unique trees is impossible;
authoring 4–8 archetypes that the runtime instances costs the same draw calls as
today and is a purely additive change.

Measured from the committed tiles (`app/public/tiles/toy.json`):

| Fact | Value |
|---|---|
| Trees city-wide (toy tier) | 289,741 |
| Cells containing trees | 547 |
| Median trees per cell | 136 |
| 95th percentile | 2,480 |
| Worst cell (`12_18`) | 4,350 |

Current archetype cost, counted from `toyTreeArchetype()`:
`IcosahedronGeometry(4.2, 1)` = 80 triangles, `CylinderGeometry(0.55, 0.7, 3.4, 6, 1)`
= 24 triangles → **~104 triangles per tree**. The worst cell therefore draws
about 452k tree triangles today. That number is the budget this kit has to
respect, and it is the single most important line in this plan.

---

## Part 1 — Task prompt (copy this into a fresh session)

````markdown
# Build the flora kit for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Replace the procedural lollipop tree with a Blender-authored kit of species
archetypes, so Golden Gate Park's cypresses, the Presidio's eucalyptus, Dolores
Park's palms and a Washington Square street tree are visibly different plants —
without changing the draw-call budget.

## Read first (in this order)

1. `AGENTS.md` — iron rules. Rule 2 (draw calls < 300, 60 fps, no per-frame
   allocation), rule 3 (procedural fallback is a guarantee — `toyTreeArchetype()`
   stays and is used when the kit fails to load).
2. `docs/styles/miniature-toy.md` — the art gate. Planting is explicitly covered:
   manicured landscaping, chunky beveled forms, flat saturated model-railway
   greens. These are toy trees, not scanned foliage.
3. `.agents/skills/sf-asset-check/SKILL.md` — the GLB contract every piece must
   pass. Note rule 4: `Toy_body` is the per-instance tintable material and is
   allowed for kit pieces (it is forbidden on landmarks). Flora is a kit.
4. `docs/plans/parks/README.md` §E3 and §E8 — the species encoding and the
   loader architecture this kit plugs into.
5. This file's Part 2 — the measured budget and the species list.
6. The code you will change: `app/src/city.js` (`toyTreeArchetype()`, the tree
   `InstancedMesh` loop around line 511), `app/src/streetkit.js` (**copy this
   file's architecture**), `pipeline/landcover.mjs` (`scatterTrees()`),
   `pipeline/lib/binio.mjs` (`writeLandcoverBlob()`, the `treeVar` byte).

Blender 4.5 LTS is on this machine at `/opt/blender`, on `PATH` as `blender`.
Run it headless only: `blender -b --python script.py -- args`. There is no GPU,
so use Workbench or CPU Cycles for review renders.

## Layer 1 — author the kit in Blender

Follow the `artifacts/streetkit/` pattern exactly: one deterministic
`build_flora_kit.py` that generates every piece, a `.blend`, a
`validate_flora_kit.py` that re-imports each exported GLB into a fresh scene and
writes `flora-contract.json`, plus review renders and a contact sheet.

Pieces (see Part 2 for the shape notes and the per-piece triangle ceiling):

| id | Species | Ceiling | Where it is used |
|---|---|---|---|
| `tree_broadleaf` | generic street/park broadleaf | 180 tris | default everywhere; must match today's silhouette closely |
| `tree_cypress` | Monterey cypress | 200 tris | Golden Gate Park, Presidio, Crissy Field windbreak |
| `tree_eucalyptus` | blue gum eucalyptus | 200 tris | Buena Vista, Glen Canyon, Presidio, GGP |
| `tree_palm` | Canary/Mexican fan palm | 160 tris | Dolores Park, Music Concourse, Embarcadero |
| `shrub_low` | low massing shrub | 60 tris | understory, park edges |
| `rock_outcrop` | chert outcrop block | 80 tris | Glen Canyon, Presidio bluffs |
| `bench_park` | park bench | 90 tris | optional; only if the street kit's bench does not suit |
| `sign_park` | park entrance marker | 90 tris | optional |

Hard rules for this kit specifically, on top of the asset-check contract:

- **Triangle ceilings are per-piece and non-negotiable** — this geometry is drawn
  up to 4,350 times in a single cell. If a species needs more, simplify the
  species, do not raise the ceiling.
- **Origin at the base of the trunk**, min z = 0, so `scatterTrees()`'s sampled
  ground elevation places it correctly with no offset.
- **Canopy colour goes in `Toy_body`**, the tintable material, so the runtime can
  shift a species' green per park (dry western GGP vs damp Presidio) without new
  geometry. Trunks use a fixed `Toy_*` colour.
- **No `_Glow`.** Trees do not light up at night.
- **Model at real scale, roughly 8–12 m tall.** The runtime still applies the
  existing per-instance size variation, so do not build in variety.
- **Symmetric enough to rotate.** Every instance gets a hashed Y rotation; a
  piece that only looks right from one angle will look wrong 300,000 times.

Gate: every piece passes `sf-asset-check` on re-import into a fresh scene, and
`flora-contract.json` records tris/dims/materials per piece.

## Layer 2 — load and instance it

Copy the architecture in `app/src/streetkit.js`, which already solves this
problem for street furniture:

- `mergePiece()` bakes each GLB's flat `Toy_*` material colours down to vertex
  colours and merges the whole piece into one body buffer (plus one glow buffer,
  unused here) — so a multi-object tree still costs one geometry.
- The fleet owns **one `InstancedMesh` per piece type, shared by every streamed
  cell**, with `frustumCulled = false` and a capacity pool that groups add to and
  remove from.

That last point is the whole design. The obvious implementation — one
`InstancedMesh` per species *per cell* — turns today's ~1 draw call per treed
cell into 4, which across the near tier is a real fraction of the 300-call
budget. A city-wide pool per species is **4 draw calls total, at any distance**,
which is *fewer* than today. Do it the streetkit way.

Fallback (rule 3): if `flora_index.json` 404s, a GLB fails to load, or any piece
breaks the contract, log **one** warning and fall back to `toyTreeArchetype()`
for every tree. Never a hole, never a crash. Keep `toyTreeArchetype()` in the
source; do not delete it.

## Layer 3 — species selection

Species come from the tree record's existing 4th byte. Per `docs/plans/parks/README.md`
§E3, re-encode it as `species * 4 + sizeVariant`:

```js
// app/src/city.js, in the tree loop
const packed  = result.trees[i * 4 + 3];
const species = packed >> 2;          // 0 = broadleaf, 1 = cypress, 2 = eucalyptus, 3 = palm
const variant = packed & 3;           // exactly today's 0..2 size bucket
```

`scatterTrees()` in `pipeline/landcover.mjs` writes it:

```js
// today
cell.trees.push(x, sampleElevation(x, z), z, Math.floor(hash01(seedBase + i * 7) * 3));
// proposed
const species = pickSpecies(kind, tags, parkId, hash01(seedBase + i * 11));
cell.trees.push(x, sampleElevation(x, z), z, species * 4 + Math.floor(hash01(seedBase + i * 7) * 3));
```

Old blobs decode as species 0 (broadleaf) with the identical size variant, so
**no blob version bump is needed** and un-rebaked cells keep working. Verify that
claim against `writeLandcoverBlob()` before relying on it — `treeVar` is a
`Uint8Array`, so values up to 15 fit, but confirm nothing else reads the byte.

Species weighting must be data-driven from the first commit (a table keyed by
park id and OSM tags), not hard-coded in the scatter loop. Getting this wrong
globally means palms in the Presidio.

## Budgets and gates

Measure and report all of these, before and after:

- **Triangles in the worst cell.** Today `12_18` holds 4,350 trees at ~104 tris
  = ~452k. Gate: no more than **2×** that after the kit lands. If a species
  ceiling pushes past it, cut the ceiling.
- **Draw calls**, at the hero view and at street level in the Mission and
  downtown stress cells. Gate: the tree layer costs **no more** calls than today
  (the shared-pool architecture should make it fewer).
- **60 fps** on the stress cells, `devicePixelRatio` ≤ 2, no per-frame
  allocation, no memory growth while flying.
- Kit payload over the wire: 8 small GLBs, expected well under 1 MB total.

## Verify

With `cd app && npm run dev`:

- Golden Gate Park and the Presidio read as coniferous; Dolores Park's palms are
  unmistakably palms; Buena Vista's eucalyptus canopy is visibly taller and
  greyer than a street broadleaf.
- From the 9 km hero camera the city's greens still read as coherent masses, not
  as speckle. If the new geometry reads noisier at distance, that is a fail —
  simplify, or add the far-LOD swap discussed in Part 2 §3.
- Fallback drill: rename `app/public/sf-assets/flora/` → the app boots, logs one
  warning, and every tree is the old lollipop.
- Day and night, deployed.

## Ship

- `cd app && npm run lint && npm run build`.
- Commit with author email `16072284+davidfromkansas@users.noreply.github.com`;
  stage only intended files; no `git add .`, no force-push, no amend.
- The GLBs and `flora_index.json` are committed assets (they are small); the
  Blender sources live in `artifacts/flora-kit/`.
- Open a PR with before/after screenshots from the diorama camera, day and night,
  plus the measured triangle and draw-call table above.

## Do not

- raise a triangle ceiling to fit a nicer model
- build one `InstancedMesh` per species per cell
- delete `toyTreeArchetype()` or bypass the fallback
- add per-tree meshes, billboards with alpha textures, or any image texture at all
- ship photoreal or scanned foliage — the style bible governs
- bake species choices into the scatter loop instead of a data table
````

---

## Part 2 — Research and design dossier

### 2.1 What is there today

`app/src/city.js` builds exactly one tree geometry:

```js
function toyTreeArchetype() {
  const trunk  = new CylinderGeometry(0.55, 0.7, 3.4, 6, 1).toNonIndexed(); // 24 tris
  trunk.translate(0, 1.7, 0);                                               // brown 0.42,0.28,0.18
  const canopy = new IcosahedronGeometry(4.2, 1);                           // 80 tris
  canopy.scale(1, 0.92, 1);
  canopy.translate(0, 7.2, 0);                                              // green 0.24,0.62,0.27
  return mergeGeometries([trunk, canopy], false);
}
```

Colour is baked to vertex colours with a vertical shade gradient on the canopy;
one `MeshLambertMaterial({ vertexColors: true })` serves every tree. Placement
comes from the baked blob (see §2.2), and the only per-instance variation is:

```js
const s = 0.62 + variant * 0.26 + ((x * 7.3 + z * 3.1) % 1) * 0.35;
dummy.scale.set(s, s * (0.85 + variant * 0.2), s);
dummy.rotation.y = ((x * 13.7 + z * 5.3) % 1) * Math.PI * 2;
```

So: three size buckets, a hashed rotation, one shape. Every tree in San Francisco
is the same object.

### 2.2 How trees get into the tiles

`scatterTrees()` in `pipeline/landcover.mjs` does rejection sampling inside each
classified polygon — one tree per `TREE_AREA_TREES = 90` m² for forest, one per
`TREE_AREA_PARK = 200` m² for parks — with positions from a pure integer hash
seeded per OSM element, so the same data always bakes the identical forest.
`pipeline/toy.mjs` then multiplies the count by `TREE_MULTIPLIER = 1.5` with a
seeded 6 m nudge, which is why the toy tier has 289,741 trees against the base
tier's 186,475.

`writeLandcoverBlob()` in `pipeline/lib/binio.mjs` stores each tree as quantised
`Int16` x/z, an `Int16` y (decimetres) and **one `Uint8` variant byte** — the byte
this plan re-purposes. Values 0–15 fit comfortably; today only 0–2 are used.

### 2.3 The budget, and the honest constraint

| Cell | Trees | Tris today (~104 ea) | At 200 tris/piece |
|---|---:|---:|---:|
| Median cell | 136 | 14k | 27k |
| 95th percentile | 2,480 | 258k | 496k |
| Worst (`12_18`) | 4,350 | 452k | 870k |

Roughly doubling the worst cell is acceptable on a modern laptop and is the
recommended starting point. What is **not** affordable is a 500–1,000 triangle
"nice" tree: that is 2–4M triangles in one cell, and it will not hold 60 fps.

This is why the ceilings in Part 1 are tight, and why the honest recommendation
is **one archetype per species, no LOD, measured first**. If the near-camera
result looks too coarse afterwards, the follow-up is a distance-based swap —
a detailed archetype for trees within roughly 150 m and the cheap one beyond —
which is a real feature with real complexity and should be its own change, not
smuggled into this one.

### 2.4 Species and shape notes

Design decisions, not measurements. All four should read as members of one toy
set — the difference is silhouette and value, not detail.

- **Broadleaf** — essentially today's lollipop, cleaned up: a slightly tapered
  trunk and a chunky faceted crown. It is the default, so it must not look worse
  than what it replaces.
- **Monterey cypress** — the SF signature. Wide, flat-topped, wind-sheared crown
  on a short trunk; darker and cooler than the broadleaf green. Reads as
  horizontal.
- **Blue gum eucalyptus** — tall, thin, bare-trunked, with a small greyish-green
  crown high up. This is what makes Buena Vista Park read as a mountain: its
  height, not its width.
- **Palm** — a bare ringed trunk with a small sparse crown of angular fronds.
  The hardest to keep cheap; consider 6–8 frond planes as solid wedges rather
  than modelled leaves.

Landscape props (`shrub_low`, `rock_outcrop`) exist so the parks plans' `rock`
and understory ideas have something to place; they are instanced through the
same pool and are optional in a first pass.

### 2.5 Precedent in this repo

This is not a new pattern. `app/public/sf-assets/streetkit/` ships 15 authored
pieces at 148–264 triangles each with a `streetkit_index.json` recording
`id`/`file`/`dims`/`tris`/`materials`/`glow` per piece, built by
`artifacts/streetkit/build_streetkit.py`, validated into
`streetkit-contract.json`, and loaded by `app/src/streetkit.js` into shared
city-wide instanced pools with a clean single-warning fallback. The flora kit
should be a near copy of all of it, and `flora_index.json` should mirror the
street kit index field for field.

The 207-piece building kit (`sf-assets/kit/`) is the precedent for `Toy_body`
per-instance tinting, which is what lets one cypress geometry be a dry
grey-green in the western Sunset and a damp dark green in the Presidio.

### 2.6 Relationship to the park plans

`docs/plans/parks/README.md` §E3 already specifies the species encoding and the
`ring`/`row`/`grid` placement modes, and every park plan references it. What
changes with this plan is only the *source* of the archetypes: authored GLBs
instead of procedural `CylinderGeometry` + `IcosahedronGeometry`. The encoding,
the weighting table and the placement modes are unchanged.

Build order that avoids wasted work:

1. This kit (authoring + loader + fallback), verified with everything still
   baking species 0. Nothing visibly changes yet — that is the point, it is a
   safe swap.
2. `scatterTrees()` species selection + a re-bake, so parks start choosing.
3. The individual park plans, starting with the Presidio.

### 2.7 Risks and open questions

- **The worst-cell triangle count is the real gate.** If four species at 200 tris
  cannot hold 60 fps in cell `12_18`, the answer is cheaper geometry, not a
  bigger budget.
- **Distance noise.** More silhouette detail can read as speckle from the 9 km
  hero camera, which would be a visual regression even at good frame rates.
  Judge it from the hero view before judging it up close.
- **`Toy_body` tinting** is proven for kit buildings but has not been used on
  instanced flora; confirm the loader path supports per-instance tint before
  designing the palette around it, and fall back to per-species fixed colours if
  not.
- **The variant byte** is assumed to be read only by the tree loop. Grep before
  re-encoding it.
- Blender here is headless with no GPU, so review renders are Workbench or CPU
  Cycles — fine for contact sheets, slow for anything ambitious.

### 2.8 Sources

- This repository: `app/src/city.js`, `app/src/streetkit.js`,
  `pipeline/landcover.mjs`, `pipeline/toy.mjs`, `pipeline/lib/binio.mjs`.
- Measured counts from the committed `app/public/tiles/toy.json` and
  `manifest.json`.
- `app/public/sf-assets/streetkit/streetkit_index.json` and
  `artifacts/streetkit/streetkit-contract.json` for the kit precedent.
- `.agents/skills/sf-asset-check/SKILL.md` for the contract and palette.
