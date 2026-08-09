# PILOT: Integrate ONE hand-made landmark GLB (Coit Tower) — end-to-end test

The repo now contains `app/public/sf-assets/landmarks/coit-tower.glb` and `app/public/sf-assets/landmarks_manifest.json` (one entry). This is a deliberate single-asset pilot of the full asset pipeline: ~300 more GLBs (a 200-piece building kit + ~300 unique landmarks) follow ONLY after this works end to end. Build the integration exactly as specified so the full pack later drops in with zero code changes.

**Asset contract (guaranteed by the authoring side; the loader may assume it):** GLB in real meters, origin at base-center (model sits ON z=0), front faces −Y in authoring terms (glTF −Z), flat-color materials only (no textures, no transparency), materials named `Toy_*`; any material name ending `_Glow` marks night-glow surfaces. Assets may contain MANY objects/materials — merging is the loader's job. `Toy_body` (if present) is a tintable near-white material; on landmarks it is NOT tinted.

## Build this

1. **Manifest-driven loader** (`app/src/assets.js`): fetch `sf-assets/landmarks_manifest.json`; for each entry, lazily (after first paint) load the GLB with `GLTFLoader`, then MERGE: traverse the scene, apply world matrices to geometries, bake each material's base color into vertex colors, and merge into at most TWO geometries — `body` (one `MeshLambertMaterial({ vertexColors: true })`) and `glow` (all `_Glow` meshes, registered with the night/dusk system as emissive). ≤ 2 draw calls per landmark, verified in the log.
2. **Placement:** position at `project(anchor)`, ground at `sampleElevation(x, z)`; uniform scale = `targetHeightM / measuredMergedHeight` (measure the merged bounding box — never trust the file); yaw 0 = front faces south.
3. **Replace-or-add:** `coit-tower` matches the existing bespoke Coit Tower — the GLB replaces the code-built model and inherits its camera preset, pick zone, context card, and procedural-exclusion radius. The swap must be invisible except the model improving (no flash, no hole, no double-render).
4. **Fallback:** if the GLB is missing or fails to parse or violates the contract (no meshes / zero height), log ONE warning and keep the code-built Coit Tower. The app must behave exactly as today with the `sf-assets` folder deleted.
5. **Works in every mode:** diorama (default) and golden, day and night (if night mode exists), at every LOD distance — the far tier's representation of Telegraph Hill must not double-draw the tower.

## QA (on the deployed site — include PASS/FAIL for each in your summary)

- [ ] Preset/fly-to for Coit Tower frames the NEW model: fluted cream cylinder with arched gallery top, portico at the base, standing on Telegraph Hill at ~64 m tall (sanity: taller than nearby North Beach buildings, far shorter than downtown towers).
- [ ] Clicking it opens the existing Coit Tower card; search still finds it; no procedural building intersects it.
- [ ] Merge log line printed: source objects/materials → 2 draw calls; draw-call total and fps unchanged vs before (± noise).
- [ ] Delete the GLB locally → code-built tower returns with one warning; restore → GLB returns.
- [ ] `vercel deploy --prod`; production URL first line of the summary.

Nothing else in this pilot: no kit, no other landmarks, no refactors. When this passes, report DONE — the full pack arrives as more files in the same folders plus manifest entries, and your loader should need zero changes.
