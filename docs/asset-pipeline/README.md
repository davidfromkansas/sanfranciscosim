# Asset pipeline — address in, landmark out

One command turns an SF address or building name into an integrated,
optimized landmark in the scene:

- [**ADDRESS-TO-ASSET.md**](./ADDRESS-TO-ASSET.md) — the orchestrator. Give an
  agent this file plus `BUILDING: <name or address>`; it resolves the
  building, writes the research plan, builds the GLB, stops for the owner's
  approval, shrinks it, and integrates it locally. Five stages, five gates.
- [**GLB-OPTIMIZE-PROMPT.md**](./GLB-OPTIMIZE-PROMPT.md) — stage 4 standalone:
  the intake shrink pass every shipped GLB goes through (meshopt + geometry
  cleanup, 4–6× smaller, appearance-gated). Generic scripts in
  [`tools/glb-optimize/`](../../tools/glb-optimize/).
- [**BATCH-INTEGRATE.md**](./BATCH-INTEGRATE.md) — stage 5 for several landmarks
  at once. Building more than one landmark at a time? Each session stops at a
  source-only branch (ADDRESS-TO-ASSET stage 5, "Batch mode") and this bakes the
  city once for all of them. A per-landmark bake rewrites ~600 generated files,
  so branches that each commit one cannot be merged.

The stages delegate to the existing authoritative docs rather than duplicating
them: plans per `docs/asset-plans/README.md`, the build contract per
`.agents/skills/sf-asset-check/SKILL.md` and `docs/styles/miniature-toy.md`,
integration per `docs/asset-plans/INTEGRATION-PROMPT.md`. Update those files,
not copies.
