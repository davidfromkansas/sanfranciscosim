"""Controlled renders of the exact exported Oracle Park GLB."""
import math, os, sys
import bpy
from mathutils import Vector

ELEV_RES=(1600,900); AER_RES=(1600,1200); TOP_RES=(1400,1400)
BG=(0.86,0.80,0.69,1.0)
VIEWS=[("north",0),("east",90),("south",180),("west",270)]

def clear(): bpy.ops.wm.read_factory_settings(use_empty=True)
def aim(obj,target): obj.rotation_euler=(target-obj.location).to_track_quat("-Z","Y").to_euler()
def camera(name):
    cam=bpy.data.cameras.new(name); cam.clip_start=1; cam.clip_end=5000
    obj=bpy.data.objects.new(name,cam); bpy.context.collection.objects.link(obj); return obj

def import_glb(path):
    bpy.ops.import_scene.gltf(filepath=path); objs=[o for o in bpy.data.objects if o.type=="MESH"]
    mn=Vector((1e9,1e9,1e9)); mx=Vector((-1e9,-1e9,-1e9))
    for obj in objs:
        for corner in obj.bound_box:
            p=obj.matrix_world@Vector(corner)
            for i in range(3): mn[i]=min(mn[i],p[i]); mx[i]=max(mx[i],p[i])
    return mn,mx

def setup():
    sc=bpy.context.scene; sc.render.engine="BLENDER_EEVEE_NEXT"; sc.render.film_transparent=False
    sc.render.image_settings.file_format="PNG"; sc.render.image_settings.color_mode="RGBA"
    sc.view_settings.look="None"; sc.view_settings.view_transform="Standard"
    sc.world=bpy.data.worlds.new("Studio"); sc.world.use_nodes=True
    bg=sc.world.node_tree.nodes["Background"]; bg.inputs[0].default_value=BG; bg.inputs[1].default_value=0.65

def lights(span):
    key=bpy.data.lights.new("key","AREA"); key.energy=1900; key.shape="DISK"; key.size=span*0.7
    ko=bpy.data.objects.new("key",key); bpy.context.collection.objects.link(ko); ko.location=(-span*.55,-span*.65,span*.65); aim(ko,Vector((0,0,15)))
    fill=bpy.data.lights.new("fill","AREA"); fill.energy=900; fill.size=span*.5
    fo=bpy.data.objects.new("fill",fill); bpy.context.collection.objects.link(fo); fo.location=(span*.65,span*.25,span*.45); aim(fo,Vector((0,0,15)))
    sun=bpy.data.lights.new("rim","SUN"); sun.energy=1.2; sun.angle=math.radians(10)
    so=bpy.data.objects.new("rim",sun); bpy.context.collection.objects.link(so); so.rotation_euler=(math.radians(45),0,math.radians(135))
    bpy.ops.mesh.primitive_plane_add(size=span*4,location=(0,0,-0.03)); floor=bpy.context.object
    mat=bpy.data.materials.new("Studio_Table"); mat.use_nodes=True; bsdf=mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value=(0.62,0.55,0.45,1); bsdf.inputs["Roughness"].default_value=.95; floor.data.materials.append(mat)

def render(path,cam,res):
    sc=bpy.context.scene; sc.camera=cam; sc.render.resolution_x,sc.render.resolution_y=res; sc.render.resolution_percentage=100; sc.render.filepath=path
    bpy.ops.render.render(write_still=True); print("[render]",path)

def main():
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []; here=os.path.dirname(os.path.abspath(__file__))
    def arg(flag,default): return argv[argv.index(flag)+1] if flag in argv else default
    glb=arg("--glb",os.path.join(here,"oracle-park.glb")); out=arg("--out",here); os.makedirs(out,exist_ok=True)
    clear(); mn,mx=import_glb(glb); setup(); dims=mx-mn; span=max(dims.x,dims.y); center=(mn+mx)/2; lights(span)
    aspect=ELEV_RES[0]/ELEV_RES[1]; ortho=max(span*1.12,dims.z*aspect*1.35); dist=span*2.5
    for name,az in VIEWS:
        c=camera("cam_"+name); c.data.type="ORTHO"; c.data.ortho_scale=ortho; a=math.radians(az)
        c.location=Vector((center.x+dist*math.sin(a),center.y+dist*math.cos(a),center.z+2)); aim(c,center)
        render(os.path.join(out,f"oracle-park-{name}.png"),c,ELEV_RES)
    top=camera("cam_top"); top.data.type="ORTHO"; top.data.ortho_scale=span*1.10; top.location=(center.x,center.y,mx.z+span); top.rotation_euler=(0,0,0)
    render(os.path.join(out,"oracle-park-top.png"),top,TOP_RES)
    aer=camera("cam_aerial"); aer.data.type="PERSP"; aer.data.lens=78; pitch=math.radians(40); az=math.radians(235); radius=span*2.5
    aer.location=Vector((center.x+radius*math.cos(pitch)*math.sin(az),center.y+radius*math.cos(pitch)*math.cos(az),center.z+radius*math.sin(pitch)))
    aim(aer,Vector((center.x,center.y,12))); render(os.path.join(out,"oracle-park-aerial.png"),aer,AER_RES)

if __name__=="__main__": main()
