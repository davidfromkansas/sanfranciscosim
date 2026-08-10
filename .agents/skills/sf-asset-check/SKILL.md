---
name: sf-asset-check
description: Validate and conform a 3D model (GLB) for the San Francisco toy-diorama city (sanfranciscosim repo / sf-3d.vercel.app). Use whenever the user wants to add, check, fix, or intake a 3D asset/GLB/model for the SF scene — "is this model compatible", "add this landmark", "check this glb", "intake this asset". Runs the contract checklist in Blender via MCP, conforms failures, renders a review thumbnail, and produces the manifest entry.
---

# SF Asset Check — contract validation & conform for scene GLBs

The SF city app loads assets via a manifest-driven pipeline with strict conventions ("the contract"). This skill verifies a GLB against the contract, fixes what it can in Blender, and outputs the manifest entry + repo instructions. Blender must be running with the MCP add-on connected (tools `mcp__blender__*`; load via ToolSearch if deferred).

## The contract (authoritative checklist)

1. **Units: real-world meters.** A house ≈ 10 m, a tower ≈ its real height. (Any uniform scale is tolerable for landmarks since the app rescales by `targetHeightM`, but dims should be plausible.)
2. **Origin at base-center:** the model SITS ON z=0 (Blender) — min-z of all geometry ≈ 0 (tolerance 0.5 m), centered in x/y. Bridges/piers: z=0 = water level.
3. **Orientation:** front faces −Y in Blender (exports to −Z glTF). Bridges: span axis along X; if one end is meaningful (e.g. a south end), record `southEnd` in the manifest.
4. **Materials: flat colors ONLY.** No image textures, no transparency/alpha, no PBR maps, roughness ~0.85. Material names `Toy_<key>` (palette below); `Toy_<key>_Glow` suffix = night-glow surface (emissive at night: signs, crowns, beacons, lit windows). `Toy_body` = per-instance TINTABLE (near-white #d8d3c8) — kit pieces only, never landmarks.
5. **Budgets:** landmark ≤ 27,000 triangles (hero one-offs like bridges may reach ~24k; typical 1–6k), kit piece ≤ 2,000 avg / towers higher, vehicle piece ≤ 300. No animations, no skinning, no cameras/lights in the export.
6. **Toy style:** chunky massing, beveled edges (Bevel modifier 0.1–0.15, 2 segments), low-seg curves (8–14), geometric windows or none — must sit next to the existing kit like pieces from one toy box. Full art direction: `docs/styles/miniature-toy.md` (the canonical style bible).
7. **Palette** (hex, flat): cream f2ede3 · sand ece4d4 · trim f3efe6 · teal 3fa8a0 · coral e8735a · mustard d9a441 · mint 8fd0a8 · sky 6db3d9 · navy 2c4a70 · glass 2a4d73 · glassl 6f95b8 · ink 3a3530 · roofd 45454a · brick c96f4a · stone d9d2c2 · red c4453c · steel 9aa0a6 · rust a86444 · gold caa64a · ioorange c0402a · verdigris 9fb8a8 · white f7f4ec. Off-palette colors are a WARN, not a fail.

## Workflow

1. **Locate the file** (ask if not given). Copy nothing yet.
2. **Inspect in an isolated Blender scene** — run this via `mcp__blender__execute_blender_code` (adjust `GLB` path; it never touches the user's other scenes):

```python
import bpy, json
GLB="/path/to/asset.glb"
sc=bpy.data.scenes.new("AssetCheck"); bpy.context.window.scene=sc
before=set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=GLB)
objs=[o for o in set(bpy.data.objects)-before]
dg=bpy.context.evaluated_depsgraph_get()
mn=[1e9]*3; mx=[-1e9]*3; tris=0; mats=set(); tex=[]; anims=[]
for o in objs:
    if o.animation_data: anims.append(o.name)
    if o.type!='MESH': continue
    ev=o.evaluated_get(dg); me=ev.to_mesh(); me.calc_loop_triangles(); tris+=len(me.loop_triangles)
    for m in me.materials:
        if not m: continue
        mats.add(m.name)
        if m.use_nodes and any(n.type=='TEX_IMAGE' for n in m.node_tree.nodes): tex.append(m.name)
    for v in me.vertices:
        w=o.matrix_world@v.co
        for i in range(3): mn[i]=min(mn[i],w[i]); mx[i]=max(mx[i],w[i])
    ev.to_mesh_clear()
result={"objects":len(objs),"tris":tris,"dims":[round(mx[i]-mn[i],2) for i in range(3)],
 "min_z":round(mn[2],2),"center_xy":[round((mn[0]+mx[0])/2,2),round((mn[1]+mx[1])/2,2)],
 "materials":sorted(mats),"textured_materials":tex,"animated":anims}
```

3. **Judge each contract rule** from the result: origin (min_z ≈ 0, center ≈ 0,0), plausible dims, tri budget, no textured/animated items, `Toy_*` names, `_Glow` presence if it should light at night. Render a thumbnail (frame camera by dims, sun + hemisphere light) and VIEW it — style judgment (rule 6) is visual.
4. **Conform what fails** (in the same scene, then re-check): recenter (`o.location -= offset`), rotate front to −Y, bake textured/PBR materials to their flat dominant base color and rename `Toy_x`, decimate if over budget (`Decimate` modifier, ratio to target), delete cameras/lights/animation data. Photogrammetry scans usually aren't worth conforming — reject and say why.
5. **Export leak-proof:** deselect ALL objects in every scene (glTF selected-export leaks selections from other scenes in the same blend file), select only the asset's objects, `bpy.ops.export_scene.gltf(filepath=..., use_selection=True, export_apply=True)`. Re-import the exported file once into a fresh scene to verify it contains only the asset. Then delete the check scene(s) and purge orphans — leave the user's Blender exactly as found.
6. **Produce the manifest entry** (landmarks):

```json
{ "id": "kebab-name", "file": "kebab-name.glb", "anchor": [lon, lat],
  "targetHeightM": <real height>, "cat": <category int>, "name": "Display Name",
  "estimated": false, "dims": [x, y, z], "tris": N }
```

Anchor = real WGS84 lon/lat (verify against a map; mark `"estimated": true` if unsure). `cat` uses the project's category enum (16 = attraction/misc is the safe default).

7. **Deliver:** PASS/FAIL/WARN table per rule, the thumbnail, the conformed GLB path, the manifest entry, and the drop instructions: copy into `~/sanfranciscosim/app/public/sf-assets/landmarks/`, append the manifest entry to `app/public/sf-assets/landmarks_manifest.json`, commit (author email must be the GitHub noreply address) and push — Vercel auto-deploys. Also copy the GLB to `~/sf-3d-assets/landmarks/` (the durable asset library).

## Context

- Kit pieces (instanced buildings) additionally need fit metadata (`kind`, `cat`, footprint dims) and only work once the full-pack instancing machinery is integrated; landmarks drop in any time after the pilot.
- The app-side loader merges every asset to ≤ 2 draw calls and falls back to procedural models on any failure — a bad asset can't crash the scene, it just won't appear (which is why this skill's job is making sure it DOES appear, correctly).
- Full project state: `~/.claude/projects/-Users-david-lietjauw/memory/project_sf_3d.md`. Asset library + factory scripts: `~/sf-3d-assets/`.
