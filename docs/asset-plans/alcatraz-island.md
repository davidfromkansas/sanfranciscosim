# Alcatraz Island — SF-SIM asset plan

The whole Rock, not just the prison: a fortified island where ~170 years of uses stay
visibly layered — Civil-War masonry, the federal penitentiary, staff housing, industry,
ruins, the 1969–71 American Indian occupation markings, gardens and seabirds. The National
Park Service treats the surviving landscape (buildings, circulation, topography,
vegetation, remnants) as one historic whole, and this asset must read the same way:
terrain first, then the buildings cascading down it.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/alcatraz-island/`. Part 1 is the runnable task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `alcatraz` (MUST be exactly this — it replaces the code-built `alcatraz` landmark and inherits its 300 m exclusion) |
| Existing procedural builder | `alcatraz` in `app/src/landmarks.js` (exclusion 300 m, camera preset baked) |
| WGS84 anchor | `-122.423, 37.8267` (the code-built anchor; re-derive the GLB's own bbox-centre anchor and reconcile in the REPORT) |
| Target height | **~65 m** — lighthouse focal plane is 214 ft above the Bay (USCG); the light tops the island. Verify before shipping; `targetHeightM` is to the model's highest point above water level |
| Island extent | ~511 × 180 m oval, long axis roughly NW–SE; summit plateau ~41 m |
| Triangle cap | **60,000** (`alwaysLoaded` skyline budget; the v2 starting point uses 25.3k, leaving ~35k for the gap list) |
| File cap | ≤ 500 KB compressed is the standard — an island complex may exceed it; justify the final size in the REPORT like a bridge would |
| Streaming | `alwaysLoaded: true` — the island is the Bay's silhouette from the entire waterfront; never streamed |
| Category | `16` (attraction) |

## ⚠ Start from the existing v2 asset — do not rebuild from scratch

`~/sf-3d-assets/landmarks/alcatraz-island-v2.glb` (2.4 MB raw, 2,033 objects, 25.3 k tris)
is a validated prior pass, built against photo/scan references and already restyled to the
style bible. It contains: terraced island terrain (17.8 k tris, previously approved),
cellhouse with two-tone paint and roof monitors, lighthouse with gold-glow lantern,
warden's house ruin, Building 64 with dock-level arcade, both Industries buildings, the
powerhouse ruin with its 46 m stack, QM warehouse with extruded ALCATRAZ roof text, water
tower on its lattice trestle, sally-port guardhouse, dock with sign + moored ferry, rec
yard with stepped seating, and 18 visitors in tour groups. **This plan is a v3 gap pass:**
audit v2 against Part 2's feature list, close the gaps, and re-validate — the terrain and
any building that already matches its reference should be carried, not remade.

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh asset session.

````markdown
# Upgrade the Alcatraz Island GLB to the full landmark complex (v3)

Work in: https://github.com/davidfromkansas/sanfranciscosim

Starting from `~/sf-3d-assets/landmarks/alcatraz-island-v2.glb`, produce the definitive
Alcatraz Island asset: the island and everything on it, as one GLB. Do not integrate or
deploy; create, validate, render and commit deliverables to your working branch under
`artifacts/alcatraz-island/`.

## Read the project sources first

1. `AGENTS.md` — note the asset budgets, compress-on-ship and streaming rules
2. `docs/styles/README.md`, then `docs/styles/miniature-toy.md`
3. `.agents/skills/sf-asset-check/SKILL.md` — the contract and workflow, including
   budget gates, `pipeline/compress-assets.mjs`, and the manifest streaming fields
4. `app/public/sf-assets/landmarks_manifest.json`
5. `artifacts/palace-of-fine-arts/` — the reference for a grounds-included complex
6. `docs/asset-plans/alcatraz-island.md` — this plan; its dossier is your starting
   point, not a substitute for verification

Authority order: style bible governs art, asset-check skill governs the contract,
AGENTS.md governs repo rules.

## Ground rules specific to this asset

- **Origin at water level** (z=0 = the Bay), like a bridge: the island rises from the
  water, terrain included in the GLB. `targetHeightM` is the highest point above water —
  verify the lighthouse focal plane (214 ft) yourself before trusting this plan.
- **Terrain accuracy beats window accuracy.** The island must read as a fortified rock
  with structures on tiers connected by the switchback road, stairs and retaining
  walls — never a flat pad with buildings on it. Carry v2's approved terrain unless a
  gap item requires a local edit.
- **Do not make it clean.** Ruins stay roofless, concrete stays stained, upper wall
  edges stay broken. Age-differentiate: dark rough masonry for the 19th-century
  fortification layer, pale weathered concrete for the penitentiary layer.
- **The occupation markings are required, not optional:** the water-tower graffiti
  ("PEACE AND FREEDOM / WELCOME / HOME OF THE FREE INDIAN LAND") in its documented red
  lettering, plus the dock-area occupation-era signage if references support it. Flat
  painted geometry (thin raised quads), no textures.
- Budgets: **≤ 60,000 tris** (this is an `alwaysLoaded` skyline piece; v2 is 25.3 k).
  Justify the compressed file size in the REPORT if it exceeds 500 KB.
- Birds are NOT baked: the app's agent system already flies gulls, and flocks anchor
  near the island. Static guano staining on cliff tops and roof edges IS in scope.

## The audit (do this before modeling)

Import v2, render the six standard elevations plus the aerial, and mark every Part 2
feature HAVE / PARTIAL / MISSING with a one-line justification. Commit this audit as
`artifacts/alcatraz-island/AUDIT.md` before touching geometry. Expected gaps (verify,
don't assume): parade ground as a distinct terrace, officers' club/social hall ruin,
historic fortification layer (sally port exists; casemate/battery remnants likely
missing), switchback road legibility from the aerial camera, garden pockets and
succulents, guano staining, water-tower graffiti, foundation-only ruins on the parade
ground, lighthouse beacon night state.

## Must capture (the recognition hierarchy, in priority order)

1. Steep rocky island — cliffs, seawalls, coves; no beaches
2. The cellhouse dominating the summit (largest mass by far, roof furniture, rec-yard
   void attached)
3. Lighthouse (tapered, white, dark lantern) + water tower (lattice legs, graffiti) as
   the two verticals
4. Warden's house and officers' club as roofless ruins beside them
5. Building 64 rising straight from the dock; ALCATRAZ signage readable from the water
6. The two Industries buildings stepping along the west cliff edge, distinct masses
7. Powerhouse + stack reading as infrastructure
8. Switchback road + stairs explaining the vertical circulation from dock to summit
9. Parade ground: a large flat terrace with foundation ruins, contrasting the summit
10. Fortification remnants, garden pockets, guano — the texture that makes it Alcatraz

## Night state

Design a `_Glow` set per the contract (glow ships at emission 0; the app drives it):
lighthouse lantern (the beacon itself — a rotating beam is an app-side feature, note it
in the REPORT as a follow-up, do not fake it in geometry), sparse warm windows in
Building 64 and the cellhouse administration wing (use the lit-window pattern from
`artifacts/grace-cathedral/`), dock lights. Ruins stay dark — that is the point of them.

## Validate, render, deliver

Per `.agents/skills/sf-asset-check/SKILL.md`: deterministic build/validate/render
scripts, six elevations + aerial + a night render, contact sheet, `validation.json`,
`REPORT.md` with the manifest entry. The manifest entry must use id `alcatraz` (exactly —
it replaces the code-built landmark), `alwaysLoaded: true`, and the anchor reconciled
against the model's own bbox centre. Run `node pipeline/compress-assets.mjs` before
measuring the final size. Set `clearTrees: true` in `pipeline/lib/landmarks.mjs` if the
baked landcover puts trees on the island (check `tiles/toyland` for the island's cell) —
the GLB carries its own vegetation.
````

---

## Part 2 — Research & design dossier

### The one-sentence read from San Francisco

Steep rock → enormous prison on top → lighthouse + water tower verticals → scattered
industrial and ruined buildings cascading toward a tiny dock → Bay. If a render does not
deliver that sequence, the asset is wrong regardless of per-building accuracy.

### Feature dossier (v2 status audited 2026-08 — re-verify in the AUDIT step)

| # | Feature | Requirements | v2 status |
|---|---------|--------------|-----------|
| 1 | Island / rock | Irregular oval, sheer gray/tan cliffs, terraced elevations, no beaches; recognizable from the waterfront | HAVE (approved terrain, 17.8 k tris) |
| 2 | Main cellhouse | Long pale concrete mass on the summit, tall repetitive windows, flat roof with vents/monitors/chimneys, attached admin wing | HAVE (two-tone paint, monitors) |
| 3 | Lighthouse | Tapered angular white concrete shaft, dark lantern + gallery, projects above the complex; working beacon = app follow-up | HAVE (gold-glow lantern); beacon note MISSING |
| 4 | Warden's house ruin | Roofless masonry shell, empty windows, vegetation inside; never restored | HAVE |
| 5 | Water tower | Cylindrical tank on four lattice legs, cross-bracing, ladder; **occupation graffiti required** | PARTIAL (tower yes, graffiti MISSING) |
| 6 | Building 64 | Long multi-story apartment block at the dock, balconies, arcade at dock level | HAVE |
| 7 | New Industries | Very long factory slab on the west edge, window ribbons (1939: laundry/factories) | HAVE |
| 8 | Model Industries | The older, separate industrial mass beside it — never merge the two | HAVE |
| 9 | Powerhouse | Heavy industrial volume + 46 m stack + utility clutter; reads as infrastructure | HAVE |
| 10 | Officers' club ruin | Large hollow shell between dock and summit, collapsed roof/floors | MISSING (verify) |
| 11 | Sally port / guardhouse | Fortified masonry entrance on the uphill road, arched openings | HAVE |
| 12 | Dock / pier | Concrete landing, ferry berth, shelter, ALCATRAZ signage readable from the water, road climbing immediately behind | HAVE (sign + moored ferry) |
| 13 | Road & switchbacks | Steep climb, retaining walls, stair shortcuts; tiers legible from the oblique aerial — exaggerate per the style bible if needed | PARTIAL (verify aerial read) |
| 14 | Parade ground | Broad flat southern terrace, weedy surface, retaining walls, foundation remnants | MISSING (verify) |
| 15 | Housing ruins | Foundations and broken walls around the parade ground — represent absence, don't reconstruct | MISSING |
| 16 | Recreation yard | Tall-walled rectangular void attached to the cellhouse; highly readable from the air | HAVE (stepped seating) |
| 17 | Administration / entrance | Attached cluster, formal entrance toward lighthouse/warden's house — not a standalone box | HAVE |
| 18 | Historic fortifications | Dark rough 19th-century masonry: battery remnants, magazines, fortified retaining walls embedded in rock | PARTIAL (sally port only) |
| 19 | Gardens & vegetation | Pockets of agaves/succulents/cypress at residences, terraces, roads — not uniform cover | PARTIAL (some trees; verify) |
| 20 | Seabirds & shore | Guano staining on cliffs/roofs, tide-pool rocks; live birds come from the app's gull system | MISSING (staining) |

### Verified data points (re-verify anything you ship)

- Code-built landmark: id `alcatraz`, anchor `-122.423, 37.8267`, **exclusion 300 m**,
  camera preset distance 1100 / yaw 170 / pitch 20 (`app/public/tiles/manifest.json`).
- Lighthouse focal plane 214 ft (~65.2 m) above the Bay — the island's highest built
  point; the 1909 tower replaced the West Coast's first lighthouse (1854).
- Island roughly 511 × 180 m; summit plateau ~41 m elevation.
- The 1969–71 American Indian occupation is one of the island's NPS-recognized historic
  periods; the water-tower lettering was restored by NPS in 2012 and is part of the
  present-day landmark. Model it as painted geometry in its documented red.
- NPS history & architecture: https://www.nps.gov/alca/learn/historyculture/index.htm

### Design principles carried from the owner's brief

- **Layered, not restored.** The visual identity is the overlap of eras — military
  masonry, penitentiary concrete, ruined shells, occupation markings, gardens, guano.
  A clean Alcatraz is a failed Alcatraz.
- **Terrain is the base truth**; a recognizable rock with approximate buildings beats
  perfect buildings on a flat pancake.
- **Ruins as ruins**: warden's house, officers' club and parade-ground foundations are
  kept hollow, roofless and stained. Foundations-only where the building is gone.
- **Priority under the budget:** terrain → cellhouse → lighthouse → water tower →
  warden's ruin → Building 64 → Industries pair → dock → rec yard → officers' club ruin →
  roads/retaining walls → vegetation → minor structures. Spend the remaining ~35 k tris
  top-down and stop when the budget says stop.
