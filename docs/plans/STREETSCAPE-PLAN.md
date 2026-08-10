# PLAN — Streetscape upgrade: baked roads & sidewalks + GLB furniture kit

Two layers. **Layer 1** upgrades the ground itself — the baked toy streets gain
raised sidewalks with chunky curbs, oversized center dashes, and crosswalk
zebras. **Layer 2** is a new reusable GLB *streetscape furniture kit* — lamps,
traffic signals, hydrants, shelters, benches, stalls — authored in headless
Blender and instanced across the whole city by placement rules.

Read `AGENTS.md` first (iron rules apply, especially rule 2 perf budgets,
rule 3 procedural fallback, rule 5 data accuracy). Read
`docs/styles/miniature-toy.md` §13 (roads/ground plane) and §14 (street
objects) — it is the artistic gate for everything here. Read
`.agents/skills/sf-asset-check/SKILL.md` — its contract governs the kit GLBs.

## Design rationale (why not modular road-tile GLBs)

SF streets follow real OSM/DataSF centerlines over real terrain: rotated
grids, diagonals (Market), curves, and steep grades. Rigid road-tile pieces
cannot cover that without breaking iron rule 5 or bending geometry per
instance. So the ROAD SURFACE stays baked ribbon geometry (it inherits real
alignment and hills for free), and GLB reuse is reserved for point-placed
objects that never bend: the furniture.

Reference look: toy-diorama city renders with light sidewalk plinths, bold
white dashes, zebra crosswalks, lamp rhythm. Asphalt stays CHARCOAL per the
style bible (contrast comes from the pale sidewalks, not lighter asphalt).

---

# LAYER 1 — Baked road surface (`pipeline/toy.mjs` + tile runtime)

## 1.1 Current state (read this code first)

- `pipeline/streets.mjs` bakes DataSF centerlines into per-cell polyline
  blobs, draped on terrain, classed by `pipeline/lib/classes.mjs`
  (freeway 22 m … residential 9 m, other 6 m, each with `lanes`, `color`).
- `pipeline/toy.mjs` (streets section, ~line 452) restyles those charcoal and
  adds two white EDGE ribbons per road at `±(w/2 − 0.3)`, lifted 0.02 m, via
  `offsetLine()`. The runtime (`app/src/city.js` / `city.worker.js`) turns
  polylines into flat ribbons.
- Cars (`app/src/agents.js`) drive at lane offset `±(path.width / 4)`,
  `CAR_LIFT = 0.2` above the road surface. Pedestrians spawn at
  `±(path.width / 2 + 1.9)` at ROAD height (~line 1062).

## 1.2 Changes

All new geometry uses the same `offsetLine` polyline-offset technique and the
existing street-blob format (add new ribbon classes to `TOY_STREET_CLASSES`
rather than inventing a parallel path).

1. **Sidewalk plinths.** Per street of class collector and up (and
   residential), two sidewalk ribbons offset `±(w/2 + SIDEWALK_W/2)` with
   `SIDEWALK_W` ≈ 3 m (4 m on major/arterial), color warm off-white
   (style-bible stone/trim range, e.g. #d9d2c2), top surface lifted
   `CURB_H = 0.35 m` above the road. The runtime ribbon builder gets a "curb"
   profile: an L-section (top strip + outer AND inner vertical faces) instead
   of a flat strip, so the curb face reads from the 42° diorama camera. If the
   ribbon builder cannot do an L-profile cheaply, bake the sidewalk as a flat
   ribbon at +0.35 plus a separate thin vertical curb ribbon — whichever costs
   fewer vertices.
   - Freeways and ramps get NO sidewalks. `other` class (alleys) gets none.
   - Sidewalks are suppressed inside bridge deck corridors (streets.mjs
     already knows `deckSurfaceAt`) and across water.
2. **Retire the white edge ribbons** (`EDGE_CLASS` lines). The pale sidewalk
   next to charcoal asphalt replaces their contrast job. Keep the code path
   one commit until visual QA confirms, then remove.
3. **Center dashes.** Replace nothing — add: chop each centerline into
   dash segments (dash 3 m / gap 6 m; scale ×1.5 on major/freeway), white
   ribbons ~0.5 m wide lifted 0.03 m (must stay below CAR_LIFT 0.2 so cars
   pass over without z-fighting). Only on residential class and up; none on
   `other`. Trim dashes to stop ~8 m short of intersection nodes.
4. **Crosswalk zebras.** Detect intersection nodes: endpoints shared by ≥2
   walkable-class polylines within 1 m tolerance. For each incoming street,
   lay 5–6 white bars (bar ~0.8 m × road width, gap ≈ bar) perpendicular to
   the street, 4–6 m out from the node center, lifted 0.03 m. Cap: skip
   crosswalks where street grade exceeds ~12% if bars visually shear (judge
   one steep test cell, e.g. Russian Hill, before deciding).
5. **Intersection boxes stay clean** — no markings inside the node area.

## 1.3 Vehicle & pedestrian fit (hard requirements)

- **Cars must fit between curbs.** Lane offset is `width/4`; widest fleet car
  half-width ≈ 1.1 m; narrowest class is 6 m (`other`, no sidewalks) and 9 m
  residential → outer car edge ≈ 3.35 m vs road half-width 4.5 m. Verify per
  class in a table in your report: `width/4 + carHalfWidth < w/2` for every
  class. Do NOT change lane offsets or street widths to make room — if
  something doesn't fit, the sidewalk/curb geometry is what moves.
- **Markings under cars:** dash/zebra lift (0.03) < CAR_LIFT (0.2). Cars
  visually drive OVER markings, never through curbs. Screenshot a car
  crossing a zebra at street level to prove no z-fight.
- **Pedestrians ride the sidewalk top.** `agents.js` spawns peds at
  `width/2 + 1.9` at road height — that point is now ON the sidewalk, so add
  `CURB_H` to ped `y` when the street class has sidewalks (export the
  class→sidewalk mapping from the tile manifest so the runtime doesn't
  hardcode it). Peds must not float on no-sidewalk classes.
- Parked/prop vehicles baked by `pipeline/toy.mjs` (§2 lore props) that sit
  in the curb lane must remain on ASPHALT, inside the curb line — check the
  prop placement offsets against the new sidewalk extent.

## 1.4 Budgets & bake mechanics

- Re-bake with `node toy.mjs` (supports `--cells=downtown,sunset` for dev
  loop). Report before/after `toystreets` MB (currently logged by the bake).
  Gate: total street tile payload growth ≤ 2×; if over, reduce dash density
  before touching sidewalks.
- Runtime: street ribbons must stay merged per cell (no per-feature draw
  calls). Draw calls < 300 worst case, verified at street level Mission +
  downtown with the stats overlay.
- LOD: sidewalks/dashes/zebras appear in the near tier only; the far tier
  keeps plain charcoal ribbons (check how the near/far street tiers split in
  `city.worker.js` and put the new classes in the near path).

---

# LAYER 2 — GLB streetscape furniture kit

## 2.1 The pieces

Author in headless Blender with a deterministic Python script (keep the
script; commit it under `pipeline/` or `artifacts/` per repo convention set
by the Salesforce Tower build). Every piece follows the sf-asset-check
contract: meters, base-center origin at z=0, front −Y, flat `Toy_*` colors
from the project palette, subtle bevels, no textures. Budget ≤ 300 tris per
piece (vehicle class); stalls/shelters may reach 500.

| id | piece | glow | notes |
|---|---|---|---|
| `sl_standard` | streetlamp, curved single head | head `Toy_lamp_Glow` | the default citywide lamp |
| `sl_pathofgold` | Market St "Path of Gold" double-globe lamp | globes glow | Market St corridor only |
| `sl_residential` | short lantern lamp | glow | residential streets |
| `traffic_signal` | pole + 3-light head + ped signal | lit faces glow | arterial/major intersections |
| `hydrant` | SF fire hydrant | — | coral or mustard body |
| `mailbox` | USPS box | — | navy |
| `muni_shelter` | Muni bus shelter | small glow strip | major/arterial stops |
| `bench` | park/sidewalk bench | — | |
| `trashcan` | city trash can | — | |
| `newsboxes` | 3-box news rack cluster | — | one piece, not three |
| `planter` | concrete planter + shrub | — | |
| `bikerack` | inverted-U rack ×3 | — | one piece |
| `cafe_set` | table + 2 chairs + umbrella | — | commercial frontage; umbrella = saturated accent |
| `market_stall` | stall with striped awning | — | commercial frontage |
| `parklet` | curbside parklet deck + planter + bench | — | commercial, replaces a car-lane slot |

Deliver as `app/public/sf-assets/streetkit/*.glb` +
`streetkit_index.json` (same shape idea as the building kit's
`kit_index.json`: id, file, dims, tris). Every piece also validated per
sf-asset-check (re-import in fresh scene; PASS/FAIL table in the PR).

## 2.2 Placement rules (runtime, deterministic)

New module `app/src/streetkit.js`, modeled on `app/src/kit.js` (building-kit
instancing). Placement derives ONLY from data already streamed: street
polylines + class, intersection nodes, the context/zoning layer, terrain via
`sampleElevation`. Deterministic per cell (hash cell key + index — same
layout every load).

- **Lamps:** every ~40 m along sidewalk-bearing streets, alternating sides,
  standing ON the sidewalk (y = road + CURB_H), 0.8 m in from the curb.
  `sl_pathofgold` only along Market St (match by street name from the
  context layer if available, else the Market centerline corridor);
  `sl_residential` on residential class; `sl_standard` elsewhere.
- **Traffic signals:** at intersections where BOTH streets are arterial
  class or higher; one signal per corner, max 4, rotated to face incoming
  traffic. Residential×residential intersections get nothing (SF uses stop
  signs; a stop sign piece is optional stretch).
- **Hydrants:** ~1 per block face on a cell-hash, near corners.
- **Muni shelters:** on major/arterial, every ~250 m, commercial zones first.
- **Commercial frontage set** (`cafe_set`, `market_stall`, `newsboxes`,
  `bikerack`, `parklet`): only where the context layer marks commercial;
  density capped (≤ 2 special pieces per 40 m of frontage) so it garnishes
  rather than clutters (bible §16: clusters, not uniform scatter).
- **Exclusions:** landmark exclusion zones (landmarks_manifest), bridge
  decks, freeways/ramps, inside crosswalk spans, and the deck corridors.
- **Slope:** pieces stand plumb (world-up), positioned at sidewalk height at
  their anchor point; skip placement where local cross-slope would sink or
  float a piece by > 0.4 m.

## 2.3 Rendering & budgets

- One merged geometry per piece type (bake `Toy_*` colors → vertex colors at
  load, exactly like the landmark/kit loader in `app/src/assets.js`), drawn
  as `InstancedMesh` per 500 m cell stream — ≤ 2 draw calls per piece TYPE
  visible (body + glow), NOT per instance.
- Instance caps per cell (e.g. ≤ 400 lamps, ≤ 60 signals) so a dense cell
  can't blow memory; far tier renders NO furniture (it's invisible at that
  distance anyway).
- Glow surfaces register with the existing dusk system (`shared.uNight`) the
  same way landmark `_Glow` sets do. **Lamp-double check:** the night scene
  already has emissive street-lamp treatment (env.js references street lamps
  as emissive shader terms; check the toy tile flag bits and `signs.js`/
  `props.js`). Find the existing lamp glow representation and make sure kit
  lamps REPLACE rather than double it wherever both would appear — two lamp
  glows at one spot is a bug.
- Total added draw calls across all piece types ≤ 35 worst case; overall
  budget < 300 holds at street level Mission + downtown, day and night.

## 2.4 Fallback (iron rule 3)

`streetkit/` missing, `streetkit_index.json` malformed, or any piece failing
to load → that piece type (or the whole kit) simply doesn't place, ONE console
warning, Layer 1 streets render untouched. Layer 1 itself falls back the same
as today: broken toy street tiles degrade to the base procedural streets.

---

# Execution order & QA

Ship as two PRs in order (Layer 1 first — it changes the ground the furniture
stands on):

**PR 1 (Layer 1):** bake changes + runtime ribbon profile + ped height fix.
QA on the DEPLOYED site, PASS/FAIL each:
1. Street-level Mission: charcoal road, raised pale sidewalks with visible
   curb faces, bold dashes, zebras at intersections; day + night screenshots.
2. A car crossing a zebra: markings under car, no z-fight; car never clips a
   curb (drive-by screenshot on a residential street).
3. Pedestrians walk ON sidewalk tops, not in them.
4. Steep-street check (Russian Hill / Filbert): ribbons and curbs follow the
   grade without floating or shearing artifacts.
5. Bridge decks and freeways unchanged (no sidewalks on them).
6. Tile payload before/after MB; draw calls + fps unchanged (± noise).
7. Fallback drill: remove a toystreets cell locally → procedural fallback.

**PR 2 (Layer 2):** kit GLBs + `streetkit_index.json` + `streetkit.js`.
QA on the DEPLOYED site, PASS/FAIL each:
1. Contract table for all pieces (sf-asset-check).
2. Commercial strip (Valencia or Clement) at street level: lamps in rhythm,
   café/stall clusters at storefronts, day + night (lamp heads glow, no
   double-glow anywhere).
3. Market St shows Path-of-Gold lamps; a residential Sunset block shows the
   lantern lamps; arterial intersection shows signals facing traffic.
4. Nothing floats, sinks, blocks a crosswalk, or intrudes into a landmark
   exclusion zone (spot-check 3 landmarks).
5. Draw calls < 300 and 60 fps at street level Mission + downtown, day AND
   night; report the furniture's share of draw calls.
6. Fallback drill: rename `streetkit/` → city renders exactly as PR 1 left
   it, one warning.
7. `vercel deploy --prod`; production URL first line of the summary.

## Out of scope

No road-tile GLBs, no lane arrows/stop bars/street-name text, no new traffic
behavior changes (cars keep their current paths/lanes), no weather, no
pipeline re-downloads (the bake re-uses existing `out/` data).
