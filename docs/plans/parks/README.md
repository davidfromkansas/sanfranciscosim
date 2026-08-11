# Park plans — index and shared engine spec

<!--
Planning documents. Nothing in this folder has been built: no pipeline code,
tile data, GLB or app code has been changed by these plans.
-->

Ten San Francisco parks, each with a ready-to-run task prompt and a measured
research dossier, plus the engine work they share.

Parks are **not** single GLBs. A landmark is one asset dropped at an anchor; a
park is ground cover, terrain drape, tree placement and paths produced by
`pipeline/landcover.mjs` and `pipeline/toy.mjs`, with a handful of hero GLBs
inside it. Every plan below is written in three layers on that basis:

- **Layer A — ground and planting.** Landcover classes, tree species and
  density, paths, water. This is pipeline work and it is where most of the
  visual gain is.
- **Layer B — hero assets.** The few objects that need to be modelled GLBs.
  They follow the normal landmark route (`.agents/skills/sf-asset-check/SKILL.md`
  to author, `docs/asset-plans/INTEGRATION-PROMPT.md` to integrate).
- **Layer C — placement, camera and scatter.** `NAMED_PARKS`, `VIEW_PRESETS`,
  props, and the checks that prove the park reads.

## The parks

| Park | Plan | Area | Relief | Current bake | In `NAMED_PARKS` | Hero assets |
|---|---|---|---|---|---|---|
| Golden Gate Park | [`golden-gate-park.md`](golden-gate-park.md) | 404.5 ha | 122.3 m | 91.7% grass, 3.1% trees | yes `goldenGatePark` | 3 planned + 5–7 new |
| The Presidio | [`presidio.md`](presidio.md) | 381.0 ha | 119.5 m | 95.3% grass, 2.3% trees | yes `presidio` | 3 new |
| Crissy Field | [`crissy-field.md`](crissy-field.md) | 10.9 ha | 1.8 m | 100% grass | yes `crissyField` | 1 optional cluster |
| Mission Dolores Park | [`mission-dolores-park.md`](mission-dolores-park.md) | 6.4 ha | 30.4 m | 93.0% grass | yes `doloresPark` | none |
| Alamo Square | [`alamo-square.md`](alamo-square.md) | 5.1 ha | 30.3 m | 96.5% grass | yes `alamoSquare` | Painted Ladies (planned) |
| Washington Square | [`washington-square.md`](washington-square.md) | 0.9 ha | 5.6 m | 90.1% grass | **no** | Sts Peter & Paul (new) |
| Lafayette Park | [`lafayette-park.md`](lafayette-park.md) | 4.6 ha | 25.2 m | 93.8% grass | **no** | none |
| Buena Vista Park | [`buena-vista-park.md`](buena-vista-park.md) | 15.3 ha | 88.0 m | 96.8% trees | yes `buenaVista` | none |
| Yerba Buena Gardens | [`yerba-buena-gardens.md`](yerba-buena-gardens.md) | 1.6 ha | 3.8 m | 95.5% grass, 2.9% water | **no** | MLK waterfall (new) |
| Glen Canyon Park | [`glen-canyon-park.md`](glen-canyon-park.md) | 29.1 ha | 92.1 m | 37% trees, 36% grass, 20% scrub | yes `glenCanyon` | none |

All areas, reliefs and bake percentages above are measured — boundaries from the
OSM API, elevation from this repository's own `app/public/tiles/terrain.bin`,
cover from `app/public/tiles/landuse.bin`. Method is documented in §2.1 of each
plan.

## The headline finding

**The city's two biggest forests currently bake as lawns.** Golden Gate Park
samples 91.7% `grass` / 3.1% `trees`; the Presidio samples 95.3% `grass` / 2.3%
`trees`. The cause is in `classify()` in `pipeline/landcover.mjs`: `leisure=park`
maps to `KIND.grass`, and each park's single park-wide polygon paints over the
`natural=wood` polygons inside it. Buena Vista Park is the accidental control —
its OSM way carries `natural=wood` *as well as* `leisure=park`, so it bakes
96.8% `trees` and is the only park in the set that already looks right.

Fixing that one classification is worth more than every hero GLB in these ten
plans combined.

## Shared engine spec

These items are referenced by section number from the individual plans.
**Implement each one once, here, not per park.** Every one of them is a
proposal, written against the code as it stands today — verify the current
behaviour before building, and record any deviation.

### §E1 — New landcover kinds

`pipeline/lib/classes.mjs` currently defines seven kinds:

```js
export const LAND_KINDS = [
  { id: 'grass',  color: [0.36, 0.47, 0.25] },
  { id: 'trees',  color: [0.20, 0.34, 0.18] },
  { id: 'sand',   color: [0.78, 0.72, 0.55] },
  { id: 'water',  color: [0.12, 0.28, 0.34] },
  { id: 'pitch',  color: [0.31, 0.45, 0.28] },
  { id: 'scrub',  color: [0.42, 0.45, 0.28] },
  { id: 'paved',  color: [0.42, 0.42, 0.42] },
];
```

Proposed additions, each with the parks that need it:

| New kind | Source | Needed by |
|---|---|---|
| `marsh` | `natural=wetland` (currently **dropped** by `classify()`) | Crissy Field, Presidio |
| `rock` | `natural=bare_rock`, `natural=cliff`, or terrain grade > ~55% inside a park | Glen Canyon, Presidio bluffs |
| `pathdg` | the path tier, §E5 | every park |
| `court` | `leisure=pitch` with `sport=tennis|basketball` | Dolores, Lafayette |
| `meadowdry` | unirrigated grass; a per-park cover override rather than a tag | Glen Canyon, western Golden Gate Park |

The kind index is a `uint8` in the landcover blob (`writeLandcoverBlob()` in
`pipeline/lib/binio.mjs` writes one byte per vertex), so there is plenty of
headroom, but the app reads `landKinds[kind]` by index in `city.worker.js` —
**append, never reorder**, and bump the blob version if anything shifts.

### §E2 — `classify()` gaps

Verified missing branches in `pipeline/landcover.mjs`:

- `natural=wetland` → nothing. Crissy Marsh (6.4 ha) and MacArthur Meadow do not
  bake at all today.
- `natural=bare_rock` / `natural=cliff` → nothing.
- `leisure=stadium` → nothing (Kezar, the Polo Field stadium ring).
- `leisure=track` → nothing.
- Tennis and basketball courts fall into the generic `pitch` green.

### §E3 — Tree species

Today `app/src/city.js` builds **one** tree archetype (`toyTreeArchetype()`: a
cylinder trunk and an icosahedron canopy) and the fourth float of each tree
record is a `variant` used only to scale it:

```js
const s = 0.62 + variant * 0.26 + ((x * 7.3 + z * 3.1) % 1) * 0.35;
dummy.scale.set(s, s * (0.85 + variant * 0.2), s);
```

Every tree in San Francisco is therefore the same lollipop. Proposal:

1. Add archetypes for `broadleaf` (the current one), `cypress` (dark, columnar),
   `eucalyptus` (tall, thin, grey-green) and `palm` (bare trunk, small sparse
   crown). Four `InstancedMesh` sets per ground group instead of one — still a
   fixed, small number of draw calls.
2. Re-encode the tree record's fourth byte as `species * 4 + sizeVariant`, so
   `variant & 3` reproduces today's behaviour exactly and `variant >> 2` selects
   the archetype. Old blobs decode as species 0 without a version bump.
3. Choose species per polygon in `scatterTrees()` from a weighting table keyed
   by park id and OSM tags, not randomly. Default stays broadleaf, so nothing
   changes outside the parks that opt in.
4. Add placement **modes** alongside the default scatter:
   - `ring` — perimeter planting (Alamo Square, Washington Square)
   - `row` — along a path centreline (Yerba Buena Gardens, the Music Concourse)
   - `grid` — regular spacing (the Music Concourse)

Getting this wrong globally means palms in the Presidio. Make the weighting
data-driven from the first commit.

### §E4 — Park-interior cover overrides

Rather than changing what `leisure=park` means city-wide — which would affect
Dolores, Alamo Square and Washington Square, where the current grass is correct —
add a per-park override table alongside `NAMED_PARKS`:

```js
// sketch, not final
export const PARK_COVER = {
  goldenGatePark: { base: 'trees', density: 'forest', species: ['cypress', 'eucalyptus'] },
  presidio:       { base: 'trees', density: 'forest', species: ['cypress', 'eucalyptus'] },
  lafayettePark:  { base: 'trees', density: 'mid',    species: ['broadleaf'] },
  doloresPark:    { base: 'grass', density: 'sparse', species: ['palm', 'broadleaf'] },
  // ...
};
```

with carve-outs (meadows, lawns, fields, golf course) still driven by their own
OSM polygons, which already classify correctly and are painted after the base.

Density constants live in `pipeline/landcover.mjs`:
`TREE_AREA_TREES = 90`, `TREE_AREA_PARK = 200` m² per tree, multiplied again by
`TREE_MULTIPLIER` in `pipeline/toy.mjs`.

### §E5 — Park path tier

Parks currently have no paths at all: the drives bake as ordinary charcoal
streets and the 4,000-plus `highway=footway|path` ways in these ten parks are
ignored. Proposal: bake selected named paths as thin `pathdg` ribbons into the
existing landcover geometry (same merged mesh, no new draw calls), driven by an
allow-list per park rather than by taking every footway.

Priority paths: JFK Promenade, the Crissy Field promenade, the Presidio Tunnel
Tops walk, and the crossing walks in Washington Square, Alamo Square, Dolores
and Lafayette. Everything else is noise at diorama scale.

### §E6 — Drape resolution on steep ground

`triangulateDraped()` subdivides until the longest edge is under
`MAX_EDGE = 55` m. On Buena Vista Park (56% grade), Glen Canyon (69%) and the
Presidio bluffs (70%), a 55 m edge spans up to ~35 m of vertical fall, so
landcover facets across the terrain instead of following it.

Proposal: a smaller max edge (15–20 m) inside park polygons whose local grade
exceeds a threshold. This raises triangle counts, so it must be scoped to steep
park polygons only and measured per cell before and after.

### §E7 — Camera presets

Every plan proposes a `VIEW_PRESETS` entry, which in
`pipeline/lib/landmarks.mjs` takes the shape:

```js
{ id: 'doloresPark', name: 'Mission Dolores Park',
  lon: -122.42834, lat: 37.75855,
  camera: { distance: 1200, yaw: 40, pitch: 12 } }
```

The plans give lon/lat, distance and pitch; yaw is left to be tuned in-engine
because it is the value you cannot get right on paper. Presets are consumed by
`pipeline/validate.mjs` and `pipeline/context.mjs`, so adding one means a
re-bake.

### Order of work

The engine items are ordered by value:

1. **§E4 + §E2** — forest cover and the missing classes. Biggest visible change
   in the whole set, and it is a data/classification fix rather than new
   rendering.
2. **§E3** — tree species. Second biggest, and it is what makes the Presidio,
   Golden Gate Park, Buena Vista and Dolores look like different places.
3. **§E5** — paths. Makes the small parks (Washington Square, Alamo Square,
   Yerba Buena) legible at all.
4. **§E6** — drape resolution. Fixes silhouettes on the steep parks; the most
   expensive item, so do it last and measure.
5. **§E1's `rock`/`marsh`** can ship with whichever of the above touches their
   parks first.

## Parks not in `NAMED_PARKS`

`pipeline/lib/landmarks.mjs` lists 11 named parks. Three parks in this set are
missing and would need entries (plus a re-bake, since the match check runs at
bake time):

```js
{ id: 'washingtonSquare',   name: 'Washington Square',   lon: -122.41021,  lat: 37.800858 },
{ id: 'lafayettePark',      name: 'Lafayette Park',      lon: -122.426857, lat: 37.791483 },
{ id: 'yerbaBuenaGardens',  name: 'Yerba Buena Gardens', lon: -122.402406, lat: 37.784645 },
```

## Hero assets these plans call for

Already planned under `docs/asset-plans/` — run those plans, do not re-research:
de Young Museum, California Academy of Sciences, Conservatory of Flowers,
Painted Ladies, Mission Dolores Basilica, Palace of Fine Arts.

New, with no asset plan yet (each would need one written in the style of the 19
landmark plans before authoring):

| Asset | Park | Anchor (lon, lat) | Note |
|---|---|---|---|
| Dutch Windmill | Golden Gate Park | `-122.509414, 37.77044` | OSM `height=13` |
| Murphy Windmill | Golden Gate Park | `-122.508686, 37.765009` | OSM `height=10` |
| Spreckels Temple of Music | Golden Gate Park | `-122.46857, 37.769846` | OSM `height=12` |
| Japanese Tea Garden cluster | Golden Gate Park | `-122.46999, 37.77003` (verify) | pagoda + gate, not one building |
| Presidio Tunnel Tops | Presidio | `-122.456479, 37.802857` | mostly landform |
| Presidio Officers' Club | Presidio | `-122.459126, 37.797422` | Main Post anchor |
| Fort Point | Presidio | `-122.477075, 37.810588` | under the bridge, OSM `height=15` |
| Saints Peter and Paul Church | Washington Square | `-122.410252, 37.80156` | OSM `height=23` is the body, not the spires |
| MLK Jr. Memorial waterfall | Yerba Buena Gardens | `-122.402253, 37.784531` | small |

## How to use a plan

1. Open the park's file and read Part 2 first so you know what is measured and
   what is a design decision.
2. Copy the fenced block in Part 1 into a fresh session.
3. Do the shared engine work from this file before or alongside the first park
   that needs it — do not re-implement it per park.
4. Ship hero GLBs through `docs/asset-plans/INTEGRATION-PROMPT.md` as usual.

## Related

- [`../asset-plans/README.md`](../asset-plans/README.md) — the 19 landmark plans
- [`../asset-plans/INTEGRATION-PROMPT.md`](../asset-plans/INTEGRATION-PROMPT.md) — the reusable GLB integration prompt
- [`../styles/miniature-toy.md`](../styles/miniature-toy.md) — the art gate
- `.agents/skills/sf-asset-check/SKILL.md` — the GLB contract
