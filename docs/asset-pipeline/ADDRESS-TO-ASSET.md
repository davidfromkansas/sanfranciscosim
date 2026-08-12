# Address → Asset — the one-command landmark pipeline

Turn "the Fairmont Hotel" or "950 Mason St" into a planned, built, approved,
optimized, integrated landmark in the live scene — one session, five stages,
each reusing a proven repo procedure. This document is the orchestrator: it
adds no new rules of its own; it sequences the authoritative ones and defines
the gates between them.

**Invocation:** give the agent this file plus one line:
`BUILDING: <address or colloquial name>`. Optional: `STOP_AFTER: <stage>`.

**Session ground rules (read before stage 0):**

- Read `AGENTS.md` first — its iron rules override everything here.
- Work on a dedicated branch off up-to-date `origin/main` (e.g.
  `pipeline/<slug>`). Commit locally at each stage boundary so every stage is
  reviewable and resumable. **Never push, open PRs, or deploy without the
  user's explicit instruction** — the pipeline ends with a local, verified
  integration and asks.
- Parallel sessions may share the tree: never touch other `artifacts/*`
  folders, never switch an existing checkout's branch — prefer a fresh
  `git worktree`.
- A stage's gate must pass before the next stage starts. A FAIL with an
  explanation beats a hidden one, at every stage.

---

## Stage 0 — RESOLVE (name/address → slug + route)

1. Geocode the input within SF (Nominatim bounded to the city bbox, then
   Overpass for the building way/relation). If the name is ambiguous
   ("St Mary's" — cathedral or church?), present the candidates with
   addresses and ask the user; never guess.
2. Derive the kebab-case `<slug>` and `<Name>`.
3. Route by existing state — check ALL of:
   - `app/public/sf-assets/landmarks_manifest.json` → already integrated?
     Report and stop (or run stage 4 retroactively if it predates the
     optimize pass and the user wants it).
   - `artifacts/<slug>/` with a validated GLB → skip to stage 3.
   - `docs/asset-plans/<slug>.md` → skip to stage 2.
   - Neither → start at stage 1.
   - Also record now, for stage 5: does the id exist in
     `pipeline/lib/landmarks.mjs` / `app/src/landmarks.js`? That decides
     integration Case A (replaces procedural) vs Case B (new landmark,
     needs registry entry + tile re-bake).

**Gate 0:** user confirms the resolved building (one line: name, address,
OSM id, case A/B, route). Cheap to confirm, expensive to model the wrong
building.

## Stage 1 — PLAN (research dossier)

Author `docs/asset-plans/<slug>.md` in the established two-part format —
follow `docs/asset-plans/README.md` ("Research method and confidence") and
mirror the structure of an existing plan (e.g. `fairmont-san-francisco.md`)
section for section, including Part 1's ready-to-run task prompt.

Non-negotiables from past corrections:

- Footprint measured from OSM geometry via the API, reduced to an oriented
  bounding box; anchor derived from the geometry the model will actually
  center on (rear service wings skew centroids).
- Height = the ARCHITECTURAL top from Wikidata/Wikipedia/architect sources.
  OSM `height` tags often describe a low shell (City Hall 30 m, St Mary's
  18.9 m) and must never be the target height. Record eave vs crest
  explicitly.
- Photo research: elevations for all four sides plus roof/aerial — the
  camera looks down; roofs are facades (style bible).
- Everything unverified is labelled *inferred* / *estimated*.
- Add the landmark's row to the README table with its runtime status.

**Gate 1:** plan file complete with sources; commit
(`docs: add <slug> asset plan`).

## Stage 2 — BUILD (plan → validated GLB)

Execute **Part 1 of `docs/asset-plans/<slug>.md`** exactly as written — it
already encodes the style bible, the `sf-asset-check` contract, the reference
implementation, and produces `artifacts/<slug>/` (REFERENCE.md, deterministic
build/render/validate scripts, GLB, day+night renders, contact sheet,
validation.json, REPORT.md).

Session-hardened overrides that apply on top of any plan:

- **Re-verify the dossier before modelling** (heights, anchor, orientation,
  entrance side) — plans have been wrong before; document corrections
  prominently in REFERENCE.md and REPORT.md. REPORT beats plan, always.
- **Normalize the bbox top to the verified height exactly**, so the loader's
  `targetHeightM / measuredHeight` scale lands at 1.0.
- **Night state is required**: `_Glow` design whose day colors match non-glow
  palette neighbours; restrained composition (hero glow + supporting
  accents); night render + night tile on the contact sheet.
- **Validator gates**: fresh-scene re-import, full contract checks, normals
  test (per-object signed volume authoritative for union-of-solids; ray test
  ≤ 0.15% residual, zero for single shells).
- Review renders from the high three-quarter aerial FIRST, iterate, only
  then run the formal rig.

**Gate 2:** validation.json all-PASS; commit
(`assets: build <slug> (pre-approval)`).

## Stage 3 — APPROVE (the human gate)

Present to the user: the contact sheet, the aerial day and night renders,
and one line of numbers (tris, dims, materials, glow groups). Then **stop
and wait**.

- Feedback → revise (stage 2 loop), re-render, re-present. Every iteration
  logged in REPORT.md.
- Only an explicit approval ("approved", "looks good, ship it") advances the
  pipeline. Silence, or "interesting", does not.

**Gate 3:** the user's approval, quoted verbatim in REPORT.md with date.

## Stage 4 — OPTIMIZE (approved GLB → light GLB)

Run `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` on `artifacts/<slug>/`
(defaults: `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`).
Start from the generic scripts in `tools/glb-optimize/` — adapt constants,
don't rewrite. Expected outcome at current results: 4–6× smaller file,
submeshes collapsed toward the ≤ 2-draw merge, appearance identical within
the pixel-delta gates.

The optimized GLB replaces `artifacts/<slug>/<slug>.glb` as the shipping
file; the original is archived under `optimize/input/`. REPORT.md and
validation.json are updated to shipped numbers.

**Gate 4:** all optimize gates (G1–G8) PASS; commit
(`assets: optimize <slug> (NNN→MM KB)`).

## Stage 5 — INTEGRATE (GLB → live scene, locally verified)

Execute **Part 1 of `docs/asset-plans/INTEGRATION-PROMPT.md`** with
`<slug>`, `<Name>`, and the Case recorded at stage 0. That prompt owns:
re-validation, the manifest entry (including the explicit `loadRadius`
streaming decision), Case B registry + tile re-bake + audit 1.6, local
verification (single building, scale ≈ 1.0, orientation, terrain seating,
night glow, draw calls < 300), and the mandatory fallback drill.

Two pipeline-specific amendments:

- Its Step 2 note "do not compress" refers to integration-side re-exporting.
  The stage-4 output IS the asset — integrate it as-is; never re-export or
  "fix" it here. Asset problems go back to stage 2/4.
- Its Step 7 (push, PR, deploy, production QA) is **replaced by a stop**:
  finish the local QA + fallback drill, commit locally
  (`feat: integrate <slug>`), then present the verification evidence
  (screenshots day/night, console merge line, stats) and ask the user
  whether to push/PR/deploy. Production QA runs only after they say yes.

**Gate 5:** local QA PASS table + the user's ship decision.

## Final report

One table, one row per stage: PASS/FAIL, artifact paths, commits. Then the
numbers that matter (tris, file KB raw/gzip, scale factor, draw calls) and
every dossier correction made along the way. First line: what was built and
where it now lives.

## Resumability

Each stage's gate commit is a checkpoint. To resume a half-done building,
re-run stage 0 — its route table lands you at the right stage
automatically. `STOP_AFTER: <stage>` runs the pipeline partially (e.g.
`STOP_AFTER: 3` to end the session at approval and optimize later).
