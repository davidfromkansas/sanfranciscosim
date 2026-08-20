import bpy, sys, json
argv = sys.argv[sys.argv.index("--")+1:]
out = {}
for path in argv:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    tiny = 0; longest = 0.0; worst = None; ngons = 0; tot = 0
    for o in [o for o in bpy.context.scene.objects if o.type=="MESH"]:
        me = o.data
        ngons += sum(1 for p in me.polygons if len(p.vertices) > 4)
        me.calc_loop_triangles()
        for t in me.loop_triangles:
            tot += 1
            a,b,c = (me.vertices[i].co for i in t.vertices)
            area = (b-a).cross(c-a).length/2
            e = max((b-a).length,(c-b).length,(a-c).length)
            if area < 1e-4:
                tiny += 1
                if e > longest: longest, worst = e, (o.name, round(area,8))
    out[path] = {"tris": tot, "ngons": ngons, "sliver_tris_area_lt_1e-4": tiny,
                 "longest_sliver_edge_m": round(longest,3), "worst": worst}
print("SLIVER " + json.dumps(out))
