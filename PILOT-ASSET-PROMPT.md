# PILOT: Integrate ONE hand-made landmark GLB (Golden Gate Bridge) — end-to-end test

The repo now contains `app/public/sf-assets/landmarks/golden-gate-bridge.glb` (~1.3 MB, 18,384 triangles, authored from ~790 source objects) and `app/public/sf-assets/landmarks_manifest.json` (one entry). This is a deliberate single-asset pilot of the full asset pipeline: ~300 more GLBs (a 200-piece building kit + ~300 unique landmarks) follow ONLY after this works end to end. Build the integration exactly as specified so the full pack later drops in with zero code changes.

**Asset contract (guaranteed by the authoring side; the loader may assume it):** GLB in real meters, origin at base-center (z=0 is water level for this asset; towers rise 227 m, deck at 67 m), long span axis along the model's X (the manifest's `southEnd: "+X"` marks the San Francisco end — it carries the Fort Point arch and must land on the SF shore), flat-color materials only (no textures, no transparency), materials named `Toy_*`; any material name ending `_Glow` marks night-glow surfaces — this asset has amber deck light strips and red tower beacons as `_Glow`. Assets may contain MANY objects/materials — merging is the loader's job.

## Build this

1. **Manifest-driven loader** (`app/src/assets.js`): fetch `sf-assets/landmarks_manifest.json`; for each entry, lazily (after first paint) load the GLB with `GLTFLoader`, then MERGE: traverse the scene, apply world matrices to geometries, bake each material's base color into vertex colors, and merge into at most TWO geometries — `body` (one `MeshLambertMaterial({ vertexColors: true })`) and `glow` (all `_Glow` meshes, registered with the night/dusk system as emissive). ≤ 2 draw calls for the whole bridge, verified in the log.
2. **Placement — bridge-specific:** scale uniformly so tower height = `targetHeightM` (measure the merged bounds height; never trust the file). Align the model's span axis (X) along the REAL bridge centerline (the OSM-snapped Golden Gate Bridge polyline already in the pipeline data): center at the polyline midpoint, yaw from the polyline bearing. Ground at water level (y = 0), NOT terrain-sampled. If the scaled span doesn't reach both real anchorage points, stretch along the span axis ONLY (non-uniform X scale is allowed for bridges alone) until deck ends meet the shorelines.
3. **Replace:** remove/hide the existing code-built Golden Gate Bridge entirely (towers, cables, deck — no double-render, no leftovers). The existing approach roads must connect to the new deck height (~67 m scaled) within 2 m vertical / 5 m horizontal — reuse the approach-ramp logic. The bridge keeps its existing camera preset, pick zone, and context card.
4. **Fallback:** if the GLB is missing/fails/violates the contract, log ONE warning and keep the code-built bridge. The app must behave exactly as today with the `sf-assets` folder deleted.
5. **Works in every mode:** diorama (default) and golden, day and night. At night the `_Glow` deck strips and tower beacons ignite with the existing dusk system. The far tier must not double-draw the old bridge.

## QA (on the deployed site — include PASS/FAIL for each in your summary)

- [ ] Hero view: the new bridge spans the real Golden Gate strait — two art-deco stepped towers, continuous swooping main cables with suspenders, deck truss, anchorage blocks at both shores, approach viaducts on columns beyond each anchorage, and the Fort Point brick fort with its steel arch under the south approach; International Orange; correctly oriented along the real alignment.
- [ ] Approach roads flow onto the deck with no gap or kink (screenshot both ends); numeric gap check logged.
- [ ] Bridge preset frames the new model; clicking it opens the existing card; no procedural buildings intersect the anchorages.
- [ ] Night: deck light strips + red tower beacons glow; day look otherwise unchanged.
- [ ] Merge log printed: ~790 source objects / N materials → 2 draw calls; total draw calls and fps unchanged vs before (± noise).
- [ ] Delete the GLB locally → code-built bridge returns with one warning; restore → GLB returns.
- [ ] `vercel deploy --prod`; production URL first line of the summary.

Nothing else in this pilot: no kit, no other landmarks, no refactors. When this passes, report DONE — the full pack arrives as more files in the same folders plus manifest entries, and your loader should need zero changes.
