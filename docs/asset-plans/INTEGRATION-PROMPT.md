# Landmark integration prompt

The plans in this folder stop at a validated GLB in `artifacts/<slug>/`. This is the
second half: the runnable prompt that puts a finished asset into the scene and ships
it, plus the reference notes behind it.

Use it once per landmark, after that landmark's asset job has produced
`artifacts/<slug>/<slug>.glb`, `validation.json` and `REPORT.md`.

**Fill in three values before running:** `<slug>` (e.g. `coit-tower`), `<Name>`
(e.g. `Coit Tower`) and the case from §B.2 (**A** replaces a procedural landmark,
**B** is a brand-new landmark that also needs a pipeline re-bake). Everything else
the prompt derives from the plan file and the asset's own `REPORT.md`.

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh session.

````markdown
# Integrate the finished <Name> GLB into SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

The asset already exists at `artifacts/<slug>/<slug>.glb` with its `REFERENCE.md`,
`REPORT.md`, `validation.json` and review renders. Your job is to put it into the
running scene at its real location and height, prove it renders correctly locally
and in production, and ship it — without breaking the procedural fallback.

Do not re-model, re-scale, re-orient or re-export the asset. If it fails validation,
stop and report; a broken asset is fixed on the authoring side, not patched here.

## Read first

1. `AGENTS.md` — especially rule 2 (performance budgets), rule 3 (procedural
   fallback is a guarantee, never delete it), rule 5 (real coordinates and real
   heights) and rule 6 (commit hygiene, deploy, QA reporting)
2. `.agents/skills/sf-asset-check/SKILL.md` — the contract and the manifest format
3. `.agents/skills/testing-sf-3d/SKILL.md` — dev commands, key bindings, the
   `window.SF` debug API and the Devin-browser gotchas
4. `docs/asset-plans/<slug>.md` — §2.12 (draft manifest entry) and §2.13
   (integration notes for this specific landmark)
5. `docs/asset-plans/INTEGRATION-PROMPT.md` §B — how the loader, the id mapping and
   the exclusion zones actually work
6. `artifacts/<slug>/REPORT.md` and `validation.json` — the measured dims, triangle
   count, anchor and height you will put in the manifest
7. `app/src/assets.js`, `app/public/sf-assets/landmarks_manifest.json` and the
   Salesforce Tower entry in git history (`git log -p -- app/public/sf-assets/landmarks_manifest.json`)
   as the worked example

## Step 1 — Re-validate the asset before touching the app

Do not trust the previous session's report. In a fresh, isolated Blender scene
(`blender -b --python ... --` headless; Blender 4.5 is on PATH), re-import
`artifacts/<slug>/<slug>.glb` and re-run the `sf-asset-check` checklist:

- triangle count within the landmark cap (<= 27,000)
- `min Z` ~ 0 (0.5 m tolerance), XY centre ~ (0, 0)
- dimensions in plausible real metres and consistent with the plan's §2.1
- every material named `Toy_*`, flat, no image texture, no transparency, no `Toy_body`
- `_Glow` only on surfaces that should light at night
- no cameras, lights, animations, armatures or foreign geometry

Record the actual `dims` and `tris` you measure — those exact numbers go in the
manifest. **If any check fails, stop here**, report which rule failed with the
measured value, and do not copy the file into `app/`.

## Step 2 — Drop the asset in

Copy the GLB to `app/public/sf-assets/landmarks/<slug>.glb` (keep the artifacts copy;
both are committed). Do not rename it, do not re-export it through another tool, and
do not compress it.

## Step 3 — Register it in the runtime manifest

Append one entry to `app/public/sf-assets/landmarks_manifest.json`:

```json
{
  "id": "<slug>",
  "file": "<slug>.glb",
  "anchor": [<verified lon>, <verified lat>],
  "targetHeightM": <verified architectural height>,
  "cat": <category int>,
  "name": "<Name>",
  "estimated": false,
  "dims": [<measured x>, <measured y>, <measured z>],
  "tris": <measured triangles>,
  "loadRadius": <metres, see below — or omit>
}
```

Rules for the values:

- `loadRadius` (PERF-PLAN #3) makes the asset **streamed**: the GLB is fetched
  only when the camera comes within this many metres of the anchor and is
  released again past 1.25×. Choose it so the swap happens while the asset is
  still small on screen (a good default is `max(2500, targetHeightM * 30)`).
  Omit it — or set `"alwaysLoaded": true` — only for skyline-scale pieces
  (bridges, towers over ~150 m) that must never leave the frame. Every new
  integration MUST make this decision explicitly and record it in the REPORT;
  remember the far stand-in is the baked/code-built version, and for a bespoke
  landmark whose baked buildings were carved out, beyond the radius the site
  is empty — pick a radius at which that absence is illegible.

- `anchor` and `targetHeightM` are the **real** WGS84 position and architectural
  height (AGENTS rule 5). Never nudge them to make the model sit better; if the model
  looks wrong at its real anchor, the model is wrong.
- If the height is still inferred rather than published, set `"estimated": true`.
- `dims`/`tris` come from your Step 1 measurement, not from the plan.
- `id` is kebab-case. The loader maps it to the pipeline's camelCase landmark id with
  `camelId()` (`app/src/assets.js`) — verify the round trip: `<slug>` must map to the
  id used in `pipeline/lib/landmarks.mjs` and `app/src/landmarks.js`, or the
  procedural version will not be hidden and you will see two buildings.
- Keep the JSON valid and consistently formatted with the existing entries.

## Step 4 — Case A or Case B

**Case A — the landmark already exists procedurally.** Nothing else is needed:
the id match makes the loader hide the code-built version, and the existing
`exclude` radius in `pipeline/lib/landmarks.mjs` already keeps baked footprints out
of the way. Skip to Step 5. Do NOT delete or edit the procedural builder in
`app/src/landmarks.js` — it is the mandated fallback (AGENTS rule 3).

**Case B — this is a new landmark.** The baked city still contains the procedural
building on that footprint, so the GLB will intersect it. You must also:

1. Add an entry to `LANDMARKS` in `pipeline/lib/landmarks.mjs`:
   ```js
   { id: '<camelId>', name: '<Name>', lon: <lon>, lat: <lat>, height: <height>,
     exclude: <radius m>, camera: { distance: <m>, yaw: <deg>, pitch: <deg> } }
   ```
   The exclusion radius must cover the asset's real footprint plus a margin — see the
   plan's §2.13 for the suggested value. Only add a `key` if the user wants a
   number-key preset; keys `0`-`9` are already taken.
2. Re-bake the affected tiles so `excluded()` in `pipeline/buildings.mjs` drops the
   procedural footprints, then re-publish. `pipeline/data/` and `pipeline/out/` are
   gitignored, so a clean machine needs the download step first:
   ```
   cd pipeline && npm install
   npm run download && npm run loredata   # ~700 MB; only if pipeline/data/ is absent
   npm run terrain && npm run bridges && npm run buildings && npm run streets \
     && npm run landcover && npm run validate && npm run lore && npm run toy \
     && npm run notables && npm run context && npm run muni-shapes
   # or just: npm run all (same order, includes the downloads)
   ```
   **`muni-shapes` belongs on that line too**, though without `MUNI_511_KEY` it
   only prints "leaving the committed file as is" and exits. That used to be a
   trap: the publish step wiped `app/public/tiles/` wholesale, so the committed
   `muni-shapes.bin` was already gone by then and nothing restored it. `validate`
   now clears only the tiers it owns. If the file does go missing, the symptom is
   a `sf-muni: no route shapes (shapes bad magic)` console warning and buses that
   dead-reckon; put it back with
   `git checkout origin/main -- app/public/tiles/muni-shapes.bin`.
   **Run the whole chain — stopping at `toy` is a trap.** `context.mjs` imports
   `LANDMARKS`, so the context tier owns your landmark's pick box, its
   `search-index` entry and its `context/landmarks.json` row; and the publish step
   in `validate.mjs` drops `app/public/tiles/ctx/` and `context/`, so stopping
   early silently deletes ~550 committed files and breaks search and the
   concierge. `lore` must run before `context`, or `context` fails its own
   "every building has a pick box and an identity" check against a stale join.
   `context` also rewrites `api/_data/`.
   Commit the regenerated files under `app/public/tiles/` and `api/_data/` that
   actually changed — **unless this landmark is part of a batch**, in which case
   run the bake for the Step 5/6 QA and then discard it
   (`git checkout -- app/public/tiles api/_data`), committing source only. A
   bake rewrites ~600 generated files regardless of which landmark triggered it,
   so two landmark branches that each commit one cannot be merged. The batch is
   baked once by `docs/asset-pipeline/BATCH-INTEGRATE.md`. If you do not know
   whether other landmarks are in flight, assume they are.
3. Confirm with `node pipeline/audit.mjs` that check 1.6 (no procedural footprint
   inside a bespoke landmark exclusion zone) passes, and with
   `node pipeline/verify-rebake.mjs` that only your landmark's cell changed and
   that nothing is left standing inside its exclusion radius.

Never hand-edit anything under `app/public/tiles/` — it is generated.

## Step 5 — Verify locally

```
cd app && npm install && npm run dev
```

Then, in the browser (real key presses, not synthetic events — see the testing skill):

- Fly to the landmark (`SF.goTo(lon, lat)` or its preset key if it has one).
- Confirm the console logs a line like
  `sf-assets: <slug> merged N objects / M materials -> 2 draw calls (... tris body ...); uniform xS at X, Z`
  and that the scale `S` is close to 1.0. A scale far from 1.0 means the authored
  height and `targetHeightM` disagree — investigate before shipping.
- Confirm there is exactly **one** building at that spot: no procedural twin, no baked
  block poking through, no z-fighting.
- Check the footprint size against reality (compare with the neighbouring blocks and
  the plan's §2.1). The loader scales uniformly by height, so a height error shows up
  as a plan-size error — this matters most for wide, low assets.
- Check orientation: the real front must face the real street. Assets should still be
  authored in true-world orientation; an explicit manifest `yawDeg` is a
  data-visible placement override only when the authored heading is wrong.
- Check it sits on the terrain: no floating, no sinking (hill sites especially).
- Night: sweep the time slider past dusk and confirm only the intended `_Glow`
  surfaces light up.
- Budgets (AGENTS rule 2): open the stats overlay and confirm draw calls stay under
  300 and the frame rate is unchanged at street level downtown.

Capture day and night screenshots of the landmark plus one wide shot.

## Step 6 — Fallback drill (mandatory)

Temporarily rename `app/public/sf-assets/landmarks/<slug>.glb`, reload, and confirm:

- the app still boots and the area renders,
- exactly one `sf-assets: ... — keeping the code-built landmark` console warning,
- Case A: the procedural landmark reappears; Case B: the site is empty ground inside
  the exclusion zone (expected — note it in the report).

Restore the file afterwards.

## Step 7 — Ship it

- `cd app && npm run lint && npm run build` (run whatever lint/build scripts the repo
  actually defines; fix anything you broke).
- Commit with the GitHub noreply author email
  `16072284+davidfromkansas@users.noreply.github.com`. Stage only the files you
  intended: the GLB, the manifest, the artifacts, and for Case B the registry plus the
  regenerated tiles. No `git add .`, no force pushes, no amends.
- Open a PR with the before/after screenshots embedded.
- After it merges and Vercel deploys, do the production QA on
  https://sf-3d.vercel.app :
  - `curl -sSI https://sf-3d.vercel.app/sf-assets/landmarks/<slug>.glb` returns 200,
  - a cold, cache-cleared load boots straight into the diorama,
  - the console logs the same merge line,
  - screenshots of the landmark day and night on the deployed site,
  - the manifest entry is being served (`curl -s .../sf-assets/landmarks_manifest.json`).

## Report

Finish with the production URL as the first line, then a PASS/FAIL table covering:
re-validation, manifest entry, id mapping, (Case B) registry + re-bake + audit 1.6,
single-building check, scale factor, orientation, terrain seating, night glow, draw
calls, fallback drill, lint/build, deployed QA. A FAIL with an explanation is
acceptable; a hidden one is not.

## Do not

- delete, disable or "clean up" the procedural builder in `app/src/landmarks.js`
- move, rescale or invent the real anchor or height to make the model fit
- edit any other landmark, asset or manifest entry
- hand-edit generated tiles, or skip the re-bake in Case B
- add dependencies, paid services or build-time data fetches
- force-push, amend, or commit with a non-noreply author email
````

---

## Part 2 — Integration reference

### B.1 How the runtime actually consumes an asset

`app/src/assets.js`:

- `load()` fetches `sf-assets/landmarks_manifest.json` after the first paint and
  places each entry in turn. Any failure logs **one** warning and leaves the
  code-built landmark alone — that is the fallback guarantee.
- `collect()` walks the GLB and rejects it if any material is not `Toy_*`, or uses a
  texture or transparency. Everything valid is merged into at most two draw calls
  (opaque body + `_Glow` set).
- `placeGeneric()` is the whole placement rule:
  ```js
  const scale = entry.targetHeightM / size.y;       // measured, never read from the file
  const [x, z] = data.project(entry.anchor[0], entry.anchor[1]);
  group.scale.setScalar(scale);
  group.position.set(x, entry.seaLevel ? 0 : Math.max(0, data.sampleElevation(x, z)), z);
  ```
  Uniform scale from height, position from the real anchor and sampled terrain, and
  optional `yawDeg` rotation about the model's vertical axis through its placement
  origin. Assets must still be authored in true-world orientation; `yawDeg` is an
  explicit, data-visible override for an asset whose authored heading is wrong.
- **`seaLevel: true`** seats the asset on the water plane instead of the terrain, and
  is for structures that stand IN THE BAY — piers, wharves, anything whose authored
  `Z = 0` is the waterline rather than the ground. It exists because the Terrarium DEM
  is not ground truth out there: at 7.5 m per sample it carries spurious 2 m+ bumps
  over open water (moored vessels and the pier decks bleed into the source), so
  `sampleElevation` at Pier 3's anchor returns 2.23 m while reading 0.00 m thirty
  metres either side, which lifts a 213 m pier clear of the bay with daylight under
  its piles. Added with `pier-3`, the first over-water landmark that is not a bridge.
  Do **not** reach for it to fix a land asset that sits badly, and do not solve the
  same problem by sliding the anchor until the raster reads zero — that is forbidden
  by the "Do not" list above and breaks again on the next terrain bake.
- `camelId('<slug>')` (`id.replace(/-([a-z])/g, ...)`) produces the pipeline's
  landmark id; `onPlaced` then lets `app/src/landmarks.js` hide the procedural twin.
  Bridges take the separate `placeBridge()` path with `ends`/`southEnd`.

### B.2 Which case each of the 19 is

**Case A — id already exists procedurally and in the pipeline registry.** Manifest
entry only, no pipeline work:

`transamerica`, `ferry-building`, `coit-tower`, `palace-of-fine-arts`, `city-hall`,
`painted-ladies`, `sutro-tower`, `oracle-park`, `grace-cathedral`

**Case B — new landmark; also needs a `pipeline/lib/landmarks.mjs` entry and a
re-bake:**

`mission-dolores`, `columbus-tower`, `555-california`, `one-rincon-hill`,
`st-marys-cathedral`, `cal-academy`, `de-young`, `conservatory-of-flowers`,
`opera-house`, `fairmont`

Why the re-bake matters: `pipeline/buildings.mjs` builds its exclusion list from
`LANDMARKS` at bake time (`excluded(ring, cx, cz, topY)`), and the resulting tiles are
committed under `app/public/tiles/`. Adding a registry entry without re-baking changes
nothing on screen; adding a GLB without the registry entry leaves the baked building
inside the new asset.

### B.3 Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Asset never appears, one console warning | manifest 404, bad JSON, contract violation, or GLB 404 | read the warning text; re-run Step 1 |
| Two buildings on the same spot | `camelId(id)` does not match the procedural/pipeline id, or Case B without a re-bake | fix the id, or add the registry entry and re-bake |
| Baked blocks poking through the model | exclusion radius too small | raise `exclude`, re-bake, re-run `pipeline/audit.mjs` check 1.6 |
| Model far too large or small | `targetHeightM` disagrees with the authored height | log line shows the scale factor; fix the manifest height, not the model |
| Model faces the wrong way | authored to the `-Y` convention instead of true-world orientation | fix in authoring, or use an explicit manifest `yawDeg` override for a known authored-heading error |
| Model floats or sinks | terrain sampled at the anchor differs from the model's base | check `min Z` ~ 0 and the anchor; hill sites need a real base plinth |
| Whole facade glows at night | `_Glow` on the wrong materials | fix material names in authoring |
| More than 2 draw calls for the asset | more than one glow material set, or unmerged parts | check the merge line; usually an authoring issue |
