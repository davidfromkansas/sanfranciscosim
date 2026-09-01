"""Fresh isolated-scene validation of the final Oracle Park GLB."""
import json,math,os,sys
import bpy
from mathutils import Vector

def rounded(v): return [round(x,4) for x in v]
def main():
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []; here=os.path.dirname(os.path.abspath(__file__))
    def arg(flag,default): return argv[argv.index(flag)+1] if flag in argv else default
    glb=arg("--glb",os.path.join(here,"oracle-park.glb")); output=arg("--out",os.path.join(here,"validation.json"))
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=glb)
    objects=list(bpy.data.objects); meshes=[o for o in objects if o.type=="MESH"]; dg=bpy.context.evaluated_depsgraph_get()
    mn=Vector((1e12,1e12,1e12)); mx=Vector((-1e12,-1e12,-1e12)); tris=degenerate=invalid_normals=0; object_rows=[]
    for obj in meshes:
        ev=obj.evaluated_get(dg); me=ev.to_mesh(); me.calc_loop_triangles(); tris+=len(me.loop_triangles); degenerate+=sum(1 for t in me.loop_triangles if t.area<1e-8)
        for v in me.vertices:
            p=obj.matrix_world@v.co
            for i in range(3): mn[i]=min(mn[i],p[i]); mx[i]=max(mx[i],p[i])
        for loop in me.loops:
            n=loop.normal
            if not all(math.isfinite(v) for v in n) or abs(n.length-1)>1e-3: invalid_normals+=1
        object_rows.append({"name":obj.name,"triangles":len(me.loop_triangles),"location":rounded(obj.location),"rotation_euler":rounded(obj.rotation_euler),"scale":rounded(obj.scale)})
        ev.to_mesh_clear()
    allowed={"Toy_brick","Toy_verdigris","Toy_trim","Toy_mint","Toy_rust","Toy_steel","Toy_ink","Toy_roofd","Toy_glass","Toy_white_Glow","Toy_gold"}
    mat_rows=[]; textured=[]; transparent=[]; off=[]; glow_bad=[]
    for mat in bpy.data.materials:
        tex=[]; alpha=1.; rough=None; emission=0.
        if mat.use_nodes:
            tex=[n.name for n in mat.node_tree.nodes if n.type=="TEX_IMAGE"]; bsdf=mat.node_tree.nodes.get("Principled BSDF")
            if bsdf: alpha=float(bsdf.inputs["Alpha"].default_value); rough=float(bsdf.inputs["Roughness"].default_value); emission=float(bsdf.inputs["Emission Strength"].default_value)
        if tex: textured.append(mat.name)
        if alpha<.999: transparent.append(mat.name)
        if mat.name not in allowed or not mat.name.startswith("Toy_") or mat.name=="Toy_body": off.append(mat.name)
        if mat.name.endswith("_Glow") and mat.name!="Toy_white_Glow": glow_bad.append(mat.name)
        mat_rows.append({"name":mat.name,"image_texture_nodes":tex,"alpha":round(alpha,4),"roughness":round(rough,4) if rough is not None else None,"glow":mat.name.endswith("_Glow"),"exported_emission_strength":round(emission,4)})
    transforms=all(all(abs(v-1)<1e-5 for v in o.scale) and all(abs(v)<1e-5 for v in o.rotation_euler) and all(abs(v)<1e-5 for v in o.location) for o in meshes)
    negative=any(math.prod(o.matrix_world.to_scale())<0 for o in meshes); animations=sum(len(a.fcurves) for a in bpy.data.actions); unexpected=[o.name for o in objects if o.type!="MESH"]
    dims=mx-mn; center=(mn+mx)/2
    ray_hits=ray_flipped=0; flipped={}; golden=math.pi*(3-math.sqrt(5))
    targets=[Vector((center.x+dx*dims.x,center.y+dy*dims.y,mn.z+fz*dims.z)) for dx,dy in ((0,0),(-.2,-.15),(.2,.15)) for fz in (.12,.48,.84)]
    for target in targets:
        for i in range(900):
            q=1-2*(i+.5)/900; r=math.sqrt(max(0,1-q*q)); a=golden*i; outward=Vector((math.cos(a)*r,math.sin(a)*r,q)); direction=-outward
            hit,_,normal,_,hit_obj,_=bpy.context.scene.ray_cast(dg,target+outward*1000,direction,distance=1400)
            if hit:
                ray_hits+=1
                if normal.dot(direction)>1e-5: ray_flipped+=1; flipped[hit_obj.name]=flipped.get(hit_obj.name,0)+1
    tolerance=max(5,math.ceil(ray_hits*.008)); normals=invalid_normals==0 and ray_hits>0 and ray_flipped<=tolerance
    result={"asset":os.path.basename(glb),"validator":"Blender "+bpy.app.version_string,"fresh_isolated_scene":True,"reimported_final_glb":True,
      "object_count":len(objects),"mesh_object_count":len(meshes),"triangle_count":tris,"triangle_budget":27000,"dimensions_m":rounded(dims),"bbox_min_m":rounded(mn),"bbox_max_m":rounded(mx),
      "min_z_m":round(mn.z,4),"xy_center_offset_m":[round(center.x,4),round(center.y,4)],"materials":sorted(m.name for m in bpy.data.materials),"material_details":sorted(mat_rows,key=lambda x:x["name"]),
      "image_texture_count":len(bpy.data.images),"textured_materials":sorted(textured),"transparent_materials":sorted(transparent),"camera_count":len(bpy.data.cameras),"light_count":len(bpy.data.lights),
      "animation_fcurve_count":animations,"armature_count":sum(1 for o in objects if o.type=="ARMATURE"),"constraint_count":sum(len(o.constraints) for o in objects),"transforms_applied":transforms,
      "negative_scales":negative,"degenerate_triangle_count":degenerate,"invalid_or_nonunit_loop_normal_count":invalid_normals,"normal_ray_cast_first_hits":ray_hits,"normal_ray_cast_flipped_visible_faces":ray_flipped,
      "normal_ray_cast_flipped_by_object":dict(sorted(flipped.items())),"normal_ray_cast_tolerance":tolerance,"normal_orientation_status":"PASS" if normals else "FAIL",
      "normal_orientation_method":"Finite/unit re-imported loop normals plus 8,100 deterministic first-hit visibility rays; 0.8% tolerance permits coplanar decorative planes.",
      "unexpected_geometry_or_objects":unexpected,"material_contract_violations":sorted(off),"glow_contract_violations":sorted(glow_bad),"duplicate_object_names":sorted({o.name for o in objects if sum(x.name==o.name for x in objects)>1}),
      "object_details":sorted(object_rows,key=lambda x:x["name"])}
    result["checks"]={"meters_and_plausible_dimensions":210<=dims.x<=250 and 190<=dims.y<=250 and 44.8<=dims.z<=45.2,"base_at_z_zero":abs(mn.z)<=.05,"centered_xy":abs(center.x)<=.05 and abs(center.y)<=.05,
      "under_triangle_budget":tris<=27000,"no_image_textures":not bpy.data.images and not textured,"no_transparency":not transparent,"materials_follow_contract":not off and not glow_bad,"no_cameras_or_lights":not bpy.data.cameras and not bpy.data.lights,
      "no_animation_skin_or_constraints":animations==0 and result["armature_count"]==0 and result["constraint_count"]==0,"transforms_applied":transforms,"no_negative_scales":not negative,"normals_outward":normals,
      "no_degenerate_geometry":degenerate==0,"no_unexpected_objects":not unexpected,"unique_object_names":not result["duplicate_object_names"]}
    result["overall"]="PASS" if all(result["checks"].values()) else "FAIL"
    with open(output,"w",encoding="utf-8") as f: json.dump(result,f,indent=2); f.write("\n")
    print(json.dumps({k:result[k] for k in ("overall","triangle_count","dimensions_m","bbox_min_m","bbox_max_m","normal_ray_cast_flipped_visible_faces","normal_ray_cast_tolerance","checks")},indent=2))
if __name__=="__main__": main()
