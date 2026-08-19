# Micro-pass (GLB-OPTIMIZE-PROMPT s.6, "prune unused data ... UV layers").
# This asset has NO textures and the runtime merge path builds a vertex-colour
# Lambert, so the exported UV layer is dead weight on every vertex. Removing it
# uniformly keeps the merge path's attribute sets consistent.
#   "$BLENDER" -b --python prune_uv.py -- <in.glb> <out.glb>
import bpy, sys, contextlib, io

argv = sys.argv[sys.argv.index("--") + 1:]
IN, OUT = argv[0], argv[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=IN)
removed = 0
for o in [o for o in bpy.context.scene.objects if o.type == "MESH"]:
    while o.data.uv_layers:
        o.data.uv_layers.remove(o.data.uv_layers[0])
        removed += 1
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    bpy.ops.export_scene.gltf(
        filepath=OUT, export_format="GLB", export_apply=True, export_yup=True,
        use_selection=False, use_active_scene=True, export_cameras=False,
        export_lights=False, export_animations=False, export_skins=False,
        export_morph=False, export_materials="EXPORT", export_image_format="NONE",
    )
print("PRUNE-UV-OK removed_layers", removed)
