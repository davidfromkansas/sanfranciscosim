"""Deterministic Blender build of the SF-SIM miniature Oracle Park.

    blender -b --python build_oracle_park.py -- [--out DIR]

Real-world metres. Blender +X east, +Y true north, +Z up. The field axis
(home plate toward center field) is authored at bearing 76 degrees clockwise
from true north, measured from mapped pitch geometry and satellite imagery.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

FIELD_BEARING = math.radians(76.0)
TOTAL_H = 45.0
RIGHT_FIELD_WALL_H = 7.32

PALETTE_HEX = {
    "Toy_brick": "c96f4a",
    "Toy_verdigris": "9fb8a8",
    "Toy_trim": "f3efe6",
    "Toy_mint": "8fd0a8",
    "Toy_rust": "a86444",
    "Toy_steel": "9aa0a6",
    "Toy_ink": "3a3530",
    "Toy_roofd": "45454a",
    "Toy_glass": "2a4d73",
    "Toy_white_Glow": "f7f4ec",
    "Toy_gold": "caa64a",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {name: srgb_to_linear(value) for name, value in PALETTE_HEX.items()}


def world(u, v, z):
    """Local +u follows home-to-center field; +v points toward left field."""
    east = math.sin(FIELD_BEARING) * u - math.cos(FIELD_BEARING) * v
    north = math.cos(FIELD_BEARING) * u + math.sin(FIELD_BEARING) * v
    return (east, north, z)


def material(name):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    rgb = PALETTE[name]
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.85
    bsdf.inputs["Metallic"].default_value = 0.0
    if name.endswith("_Glow"):
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    return mat


def new_mesh(name, verts, faces, mats, face_mats=None, bevel=0.0, recalc=True):
    me = bpy.data.meshes.new(name)
    me.from_pydata([Vector(v) for v in verts], [], faces)
    for mat in mats:
        me.materials.append(mat)
    if face_mats:
        for poly, idx in zip(me.polygons, face_mats):
            poly.material_index = idx
    me.validate()
    obj = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new(); bm.from_mesh(me)
    if recalc:
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if bevel:
        bmesh.ops.bevel(bm, geom=list(bm.verts) + list(bm.edges), offset=bevel,
                        segments=2, profile=0.5, affect="EDGES", clamp_overlap=True)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free(); me.shade_flat()
    return obj


def local_box(name, cu, cv, z0, z1, su, sv, mat, angle=0.0, bevel=0.12):
    hu, hv = su / 2, sv / 2
    c, s = math.cos(angle), math.sin(angle)
    def p(x, y, z):
        return world(cu + x * c - y * s, cv + x * s + y * c, z)
    q = [(-hu, -hv), (hu, -hv), (hu, hv), (-hu, hv)]
    verts = [p(x, y, z0) for x, y in q] + [p(x, y, z1) for x, y in q]
    faces = [(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    return new_mesh(name, verts, faces, [mat], bevel=bevel)


def prism_polygon(name, points, z0, z1, mat, bevel=0.0):
    verts = [world(u, v, z0) for u, v in points] + [world(u, v, z1) for u, v in points]
    n = len(points)
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    faces += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return new_mesh(name, verts, faces, [mat], bevel=bevel)


def ring_segment(name, center_u, center_v, r_in_u, r_in_v, r_out_u, r_out_v,
                 z_inner, z_outer, z_base, start_deg, end_deg, mat, segments=48):
    angles = [math.radians(start_deg + (end_deg - start_deg) * i / segments) for i in range(segments + 1)]
    verts = []
    for z, ru, rv in ((z_base, r_in_u, r_in_v), (z_base, r_out_u, r_out_v),
                      (z_inner, r_in_u, r_in_v), (z_outer, r_out_u, r_out_v)):
        verts += [world(center_u + ru * math.cos(a), center_v + rv * math.sin(a), z) for a in angles]
    m = len(angles); faces = []
    for i in range(segments):
        faces += [
            (i, i + 1, m + i + 1, m + i),
            (2*m+i, 3*m+i, 3*m+i+1, 2*m+i+1),
            (i, 2*m+i, 2*m+i+1, i+1),
            (m+i+1, 3*m+i+1, 3*m+i, m+i),
        ]
    faces += [(0,m,3*m,2*m),(m-1,2*m-1,4*m-1,3*m-1)]
    return new_mesh(name, verts, faces, [mat])


def arch_plane(name, cu, cv, z0, width, height, mat, tangent_angle, segments=10):
    r = width / 2; spring = height - r
    pts = [(-r, 0), (r, 0), (r, spring)]
    for i in range(1, segments + 1):
        a = i * math.pi / segments
        pts.append((r * math.cos(a), spring + r * math.sin(a)))
    c, s = math.cos(tangent_angle), math.sin(tangent_angle)
    verts = [world(cu + x*c, cv + x*s, z0 + z) for x, z in pts]
    return new_mesh(name, verts, [tuple(range(len(verts)))], [mat], recalc=False)


def radial_box(name, center_u, center_v, radius, theta, z0, z1, tangential, radial, mat, bevel=0.1):
    u = center_u + radius * math.cos(theta); v = center_v + radius * math.sin(theta)
    return local_box(name, u, v, z0, z1, radial, tangential, mat, angle=theta, bevel=bevel)


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"; scene.unit_settings.length_unit = "METERS"

    brick = material("Toy_brick"); green = material("Toy_verdigris")
    trim = material("Toy_trim"); grass = material("Toy_mint")
    dirt = material("Toy_rust"); steel = material("Toy_steel")
    ink = material("Toy_ink"); roof = material("Toy_roofd")
    glass = material("Toy_glass"); glow = material("Toy_white_Glow")
    gold = material("Toy_gold")

    # Asymmetric field graphic, with the short right-field corner toward -v.
    field = [(-48,-11),(-42,-31),(10,-72),(40,-73),(78,-30),(83,3),(66,54),(25,75),(-25,34),(-48,11)]
    prism_polygon("field_grass", field, 0.0, 0.35, grass, 0.06)
    prism_polygon("warning_track", [(-52,-14),(-46,-35),(8,-78),(44,-79),(84,-33),(89,4),(71,59),(27,81),(-29,38),(-52,14)], 0.0, 0.16, dirt)
    prism_polygon("field_grass_top", field, 0.16, 0.40, grass)

    home = (-43.0, 0.0)
    diamond = [home,(-21,-22),(1,0),(-21,22)]
    prism_polygon("infield_dirt", [(-50,-7),(-46,-17),(-22,-31),(8,-12),(10,12),(-22,31),(-46,17)], 0.38, 0.55, dirt)
    prism_polygon("infield_grass", [(-38,-1),(-21,-18),(-4,0),(-21,18)], 0.54, 0.61, grass)
    # Bright base-path strokes and bases are deliberately oversized for the aerial camera.
    for i, (a, b) in enumerate(zip(diamond, diamond[1:] + diamond[:1])):
        au,av=a; bu,bv=b; du,dv=bu-au,bv-av; length=math.hypot(du,dv)
        local_box(f"baseline_{i}",(au+bu)/2,(av+bv)/2,0.60,0.76,length,0.55,trim,math.atan2(dv,du),0.03)
    for i,(u,v) in enumerate(diamond):
        local_box(f"base_{i}",u,v,0.75,0.92,1.8,1.8,trim,math.pi/4,0.04)
    local_box("pitcher_mound",-21,0,0.55,0.82,7.0,7.0,dirt,math.pi/4,0.08)
    local_box("pitcher_rubber",-21,0,0.82,0.92,2.4,0.55,trim,0,0.02)

    # Three readable seating tiers: steep/tall behind home, deliberately open toward the Bay.
    center_u = -17.0
    ring_segment("lower_bowl", center_u,0,55,50,75,68,4.0,11.0,0.5,53,307,ink,52)
    ring_segment("club_bowl", center_u,0,76,69,93,84,12.0,23.0,8.5,62,298,ink,50)
    ring_segment("upper_bowl", center_u,0,94,85,109,98,24.0,34.0,20.0,78,282,ink,46)

    # Broad pale aisle separators keep the seat mass graphical rather than noisy.
    for i, deg in enumerate(range(76, 287, 18)):
        th = math.radians(deg)
        radial_box(f"aisle_lower_{i}",center_u,0,66,th,10.0,11.25,2.0,30.0,trim,0.0)
        if 84 <= deg <= 276:
            radial_box(f"aisle_upper_{i}",center_u,0,101,th,33.0,34.25,2.2,31.0,trim,0.0)

    # Brick street shell and a dark canopy read as the west/north horseshoe exterior.
    ring_segment("outer_brick_shell", center_u,0,108,97,113,102,15.0,24.0,0.0,70,290,brick,52)
    ring_segment("upper_green_structure", center_u,0,109,98,113,102,25.0,34.0,22.5,80,280,green,46)
    ring_segment("canopy_ring", center_u,0,99,89,114,103,34.0,36.2,33.0,78,282,roof,48)

    # Warehouse-like street rhythm: tall inset panels, brick piers and pale cornice blocks.
    for i, deg in enumerate(range(86, 279, 12)):
        th=math.radians(deg)
        radial_box(f"street_recess_{i}",center_u,0,113.2,th,3.0,17.0,5.4,0.18,glass,0.0)
        radial_box(f"street_pier_{i}",center_u,0,113.6,th,0.0,21.0,1.4,1.2,brick,0.0)
        radial_box(f"street_cornice_{i}",center_u,0,114.0,th,20.7,22.0,7.5,1.0,trim,0.0)

    # North-west Willie Mays Plaza identity block: paired brick towers, sign and clock.
    entry_theta=math.radians(126)
    eu=center_u+112*math.cos(entry_theta); ev=112*math.sin(entry_theta)
    local_box("entry_left_tower",eu-9*math.sin(entry_theta),ev+9*math.cos(entry_theta),0,29,12,12,brick,entry_theta,0.18)
    local_box("entry_right_tower",eu+9*math.sin(entry_theta),ev-9*math.cos(entry_theta),0,29,12,12,brick,entry_theta,0.18)
    local_box("entry_sign_bridge",eu,ev,17,25,30,4.5,brick,entry_theta,0.14)
    local_box("entry_sign_face",eu-1.7*math.cos(entry_theta),ev-1.7*math.sin(entry_theta),19,23.5,21,0.35,ink,entry_theta,0.02)
    local_box("entry_clock",eu+9*math.sin(entry_theta)-1.8*math.cos(entry_theta),ev-9*math.cos(entry_theta)-1.8*math.sin(entry_theta),18,24,6,0.3,glow,entry_theta,0.02)
    for sgn in (-1,1):
        radial_box(f"entry_roof_{sgn}",center_u,0,117,entry_theta+sgn*0.075,29,32,13,12,roof,0.12)

    # Waterfront Portwalk arcade: pale low shell, five major view arches and brick wall.
    a=(18,-77); b=(78,-27); du=b[0]-a[0]; dv=b[1]-a[1]
    length=math.hypot(du,dv); angle=math.atan2(dv,du); cu=(a[0]+b[0])/2; cv=(a[1]+b[1])/2
    local_box("waterfront_arcade",cu,cv,0,9.4,length+9,8.0,trim,angle,0.16)
    local_box("right_field_wall",cu-1.0*math.sin(angle),cv+1.0*math.cos(angle),0,RIGHT_FIELD_WALL_H,length-4,3.0,brick,angle,0.12)
    local_box("arcade_top_walk",cu,cv,9.2,10.4,length+10,10.0,steel,angle,0.10)
    for i in range(5):
        t=(i+0.5)/5; u=a[0]+du*t; v=a[1]+dv*t
        arch_plane(f"right_field_arch_{i}",u-4.05*math.sin(angle),v+4.05*math.cos(angle),1.0,9.2,6.8,ink,angle,10)
        local_box(f"arcade_pier_{i}",u,v,0,9.8,1.8,9.0,brick,angle,0.08)
    # Short right-field foul pole and wall termination.
    local_box("right_foul_pole",18,-77,7.0,37.0,0.65,0.65,gold,0,0.02)
    local_box("left_foul_pole",25,75,2.0,32.0,0.65,0.65,gold,0,0.02)

    # Giant center-field scoreboard facing home plate.
    local_box("scoreboard_frame",79,24,23.0,40.0,4.0,40.0,ink,0,0.18)
    local_box("scoreboard_face",76.92,24,25.0,38.5,0.28,36.0,glow,0,0.02)
    local_box("scoreboard_header",76.6,24,38.3,41.0,0.5,30.0,brick,0,0.05)
    for i in range(4):
        local_box(f"scoreboard_leg_{i}",80,9+i*10,9.0,24.0,1.1,1.1,green,0,0.05)

    # Five owner-verified standards. Paired masts + a chunky lamp array read at city scale.
    light_specs=[(108,42),(155,43),(200,45),(245,44),(282,42)]
    for i,(deg,top) in enumerate(light_specs):
        th=math.radians(deg); r=111
        u=center_u+r*math.cos(th); v=r*math.sin(th)
        tang=(-math.sin(th),math.cos(th))
        for j,off in enumerate((-4.0,4.0)):
            mu=u+tang[0]*off; mv=v+tang[1]*off
            local_box(f"light_{i}_mast_{j}",mu,mv,25.0,top-5.0,1.2,1.2,green,0,0.0)
        local_box(f"light_{i}_array",u,v,top-5.5,top,2.5,18.0,roof,th,0.10)
        local_box(f"light_{i}_glow",u-1.3*math.cos(th),v-1.3*math.sin(th),top-4.8,top-0.7,0.20,15.5,glow,th,0.01)
        for k in (-5,0,5):
            local_box(f"light_{i}_brace_{k}",u+tang[0]*k,v+tang[1]*k,top-7.0,top-5.3,0.65,0.65,steel,0,0.0)

    # A few coherent upper-deck roof masses — designed from above, not scattered noise.
    for i,(deg,w) in enumerate(((104,13),(142,16),(188,18),(232,16),(270,13))):
        th=math.radians(deg)
        radial_box(f"roof_pavilion_{i}",center_u,0,111,th,34.0,37.5,w,10.0,roof,0.12)

    # Recentre exact evaluated bounds to base-centre while retaining true-world heading.
    dg=bpy.context.evaluated_depsgraph_get(); mn=Vector((1e9,1e9,1e9)); mx=Vector((-1e9,-1e9,-1e9))
    for obj in [o for o in bpy.data.objects if o.type=="MESH"]:
        me=obj.evaluated_get(dg).to_mesh()
        for vert in me.vertices:
            p=obj.matrix_world@vert.co
            for k in range(3): mn[k]=min(mn[k],p[k]); mx[k]=max(mx[k],p[k])
        obj.evaluated_get(dg).to_mesh_clear()
    offset=Vector(((mn.x+mx.x)/2,(mn.y+mx.y)/2,mn.z))
    for obj in bpy.data.objects:
        if obj.type=="MESH":
            for vert in obj.data.vertices: vert.co-=offset
    return scene


def report():
    dg=bpy.context.evaluated_depsgraph_get(); mn=Vector((1e9,1e9,1e9)); mx=Vector((-1e9,-1e9,-1e9)); tris=0
    objs=[o for o in bpy.data.objects if o.type=="MESH"]
    for obj in objs:
        me=obj.evaluated_get(dg).to_mesh(); me.calc_loop_triangles(); tris+=len(me.loop_triangles)
        for vert in me.vertices:
            p=obj.matrix_world@vert.co
            for k in range(3): mn[k]=min(mn[k],p[k]); mx[k]=max(mx[k],p[k])
        obj.evaluated_get(dg).to_mesh_clear()
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v,3) for v in mn]} max={[round(v,3) for v in mx]}")
    print(f"[build] dims={[round(mx[i]-mn[i],3) for i in range(3)]}")


def main():
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    out=os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv: out=argv[argv.index("--out")+1]
    os.makedirs(out,exist_ok=True)
    build(); report()
    blend=os.path.join(out,"oracle-park.blend"); glb=os.path.join(out,"oracle-park.glb")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    bpy.ops.export_scene.gltf(filepath=glb,export_format="GLB",export_apply=True,export_yup=True,
        use_selection=False,export_cameras=False,export_lights=False,export_animations=False,
        export_skins=False,export_morph=False,export_materials="EXPORT",export_image_format="NONE")
    print(f"[build] wrote {blend}"); print(f"[build] wrote {glb}")


if __name__ == "__main__": main()
