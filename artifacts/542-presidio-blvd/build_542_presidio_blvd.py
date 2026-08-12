"""Deterministic Blender build of the SF-SIM miniature 542 Presidio Boulevard.

    blender -b --python build_542_presidio_blvd.py -- [--out DIR]

Writes 542-presidio-blvd.blend and 542-presidio-blvd.glb next to this file (or
into --out). Geometry is authored directly in world space in metres, Z up,
+X east, +Y north, origin at the base centre, min Z = 0, so the export needs
no transforms applied after the fact.

Design (see REFERENCE.md for the sources behind every number):

* a 1912-17 Mission Revival officers' family duplex on Presidio Boulevard: a
  quiet cream stucco box under a low terracotta hipped tile roof, which at
  10.6 m is what the app's downward camera actually reads;
* the roof is the hero surface - low ~4:12 hips, a short 5.4 m ridge on the
  long NNE-SSW axis, a 0.65 m eave overhang whose shadow line is what stops
  the asset reading as a red box, and capped ridge and hip courses that make
  the hip form legible from directly above;
* the facade is split into two bands by a terracotta pent roof at 4.7 m, which
  also caps the full-width recessed porch below it;
* the porch: four chunky square columns over a solid stucco balustrade wall,
  two front doors side by side because this is a duplex, not a villa;
* the only glow is a porch light and three lit upper windows - a house is not
  a skyline piece. Both glow materials share a hex with a non-glow palette
  neighbour, so daylight is unaffected.

Authoring frame: geometry is laid out in a local (u, v) frame - u along the
long axis / roof ridge (bearing 31 deg, NNE), v along the short axis pointing
at the entrance front (bearing 121 deg, ESE, onto Presidio Boulevard) - and
rotated into true-world orientation on the way out. The front therefore does
NOT face -Y; real-world orientation wins (docs/asset-plans/README.md).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

H_CREST = 10.6  # architectural crest, ridge of the hipped roof
H_EAVE = 8.0    # top plate / eave line (OSM height=8 is this, not the crest)
H_PENT = 4.7    # pent roof / belt course, top of the ground storey
H_PLINTH = 1.1  # raised base the house sits on

L = 19.2   # body length along u (long axis, ridge direction)
W = 13.8   # body width along v (short axis, front to back)
PLINTH_OUT = 0.1   # plinth steps out beyond the wall line
EAVE_OUT = 0.65    # roof overhang past the wall line - exaggerated on purpose
PENT_OUT = 0.5     # pent roof projection
PENT_T = 0.35      # pent roof thickness

PORCH_DEPTH = 2.2   # how far the ground floor is recessed on the front
PORCH_HALF = 8.2    # porch opening runs u in [-8.2, 8.2]; 1.4 m returns
BALUSTRADE_H = 1.15
BALUSTRADE_T = 0.36
COLUMN_HALF = 0.26
WIN_W = 1.35       # window width; the reveal adds WIN_PAD on every side
WIN_PAD = 0.07
RIDGE_CAP = 0.18   # ridge and hip caps: the roof's only modelled ornament
COURSE_T = 0.12    # tile course banding on the two main slopes
STEP_N = 6
STEP_W = 3.0
STEP_TREAD = 0.26

RIDGE_HALF = 2.7   # ridge half-length: equal-pitch full hips over L x W + eaves
CHIMNEY = (0.9, 0.6)

YAW = math.radians(31.0)  # long axis / ridge bearing, measured from OSM geometry

BEVEL_CHUNKY = 0.12
BEVEL_THIN = 0.05

# Project palette from .agents/skills/sf-asset-check (hex, sRGB). Materials are
# authored with the linear equivalents, which is what the shipped kit GLBs hold.
PALETTE_HEX = {
    "Toy_cream": "f2ede3",   # stucco walls, chimney shafts
    "Toy_brick": "c96f4a",   # terracotta mission tile: main roof and pent roof
    "Toy_trim": "f3efe6",    # porch columns, balustrade, cornice, eave fascia
    "Toy_stone": "d9d2c2",   # raised base and entry steps
    "Toy_glass": "2a4d73",   # windows
    "Toy_ink": "3a3530",     # window reveals, doors, chimney caps
    "Toy_glass_Glow": "2a4d73",  # lit upper windows - same hex as Toy_glass
    "Toy_white_Glow": "f7f4ec",  # porch soffit light - same hex as Toy_white
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

U_DIR = (math.sin(YAW), math.cos(YAW))            # bearing 31 deg
V_DIR = (math.sin(YAW + math.pi / 2), math.cos(YAW + math.pi / 2))  # bearing 121 deg


def to_world(u, v, z):
    """Local (u, v, z) -> true-world (x east, y north, z up)."""
    return (u * U_DIR[0] + v * V_DIR[0], u * U_DIR[1] + v * V_DIR[1], z)


# ------------------------------------------------------------------ materials


def material(name):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    rgb = PALETTE[name]
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.85
    bsdf.inputs["Metallic"].default_value = 0.0
    if name.endswith("_Glow"):
        # Flagged for the app's night pass; emission is off in the daylight asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    return mat


# ------------------------------------------------------------------- geometry


def new_mesh(name, verts, faces, mats):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.validate()
    for m in mats:
        mesh.materials.append(m)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.shade_flat()
    return obj


def box(name, u0, u1, v0, v1, z0, z1, mat):
    """Axis-aligned box in the local (u, v) frame, emitted in world space."""
    corners = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
    verts = [to_world(u, v, z0) for u, v in corners]
    verts += [to_world(u, v, z1) for u, v in corners]
    faces = [
        (0, 3, 2, 1),          # bottom
        (4, 5, 6, 7),          # top
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


def ring(name, u_out, v_out, u_in, v_in, z0, z1, mat):
    """Hollow rectangular band (a picture frame) - used for the pent roof."""
    outer = [(-u_out, -v_out), (u_out, -v_out), (u_out, v_out), (-u_out, v_out)]
    inner = [(-u_in, -v_in), (u_in, -v_in), (u_in, v_in), (-u_in, v_in)]
    verts = [to_world(u, v, z0) for u, v in outer]
    verts += [to_world(u, v, z0) for u, v in inner]
    verts += [to_world(u, v, z1) for u, v in outer]
    verts += [to_world(u, v, z1) for u, v in inner]
    faces = []
    for i in range(4):
        j = (i + 1) % 4
        faces.append((i, j, 4 + j, 4 + i))              # bottom annulus
        faces.append((8 + i, 12 + i, 12 + j, 8 + j))    # top annulus
        faces.append((i, 8 + i, 8 + j, j))              # outer wall
        faces.append((4 + i, 4 + j, 12 + j, 12 + i))    # inner wall
    return new_mesh(name, verts, faces, [mat])


def hip_roof(name, u_half, v_half, ridge_half, z0, z1, mat):
    """Equal-pitch hipped roof solid: two trapezoid slopes, two triangular hips."""
    verts = [
        to_world(-u_half, -v_half, z0),
        to_world(u_half, -v_half, z0),
        to_world(u_half, v_half, z0),
        to_world(-u_half, v_half, z0),
        to_world(-ridge_half, 0.0, z1),
        to_world(ridge_half, 0.0, z1),
    ]
    faces = [
        (0, 3, 2, 1),      # underside
        (0, 1, 5, 4),      # rear slope
        (2, 3, 4, 5),      # front slope
        (1, 2, 5),         # NNE hip
        (3, 0, 4),         # SSW hip
    ]
    return new_mesh(name, verts, faces, [mat])


def segment_cap(name, p0, p1, half_w, h, mat):
    """A prism running along a local-space segment, standing `h` proud in +Z.

    Used for the ridge and hip caps - on a real mission-tile roof those capping
    courses are the only ornament, and they are what makes the hip form legible
    from the app's downward camera.
    """
    d = (p1[0] - p0[0], p1[1] - p0[1])
    ln = math.hypot(d[0], d[1]) or 1.0
    px, py = -d[1] / ln * half_w, d[0] / ln * half_w
    base = [
        (p0[0] - px, p0[1] - py, p0[2]),
        (p0[0] + px, p0[1] + py, p0[2]),
        (p1[0] + px, p1[1] + py, p1[2]),
        (p1[0] - px, p1[1] - py, p1[2]),
    ]
    verts = [to_world(*b) for b in base]
    verts += [to_world(b[0], b[1], b[2] + h) for b in base]
    faces = [
        (0, 3, 2, 1),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


def roof_courses(u_half, v_half, ridge_half, z0, z1, mat):
    """Shallow tile courses on the two main slopes, parallel to the eaves.

    Each band straddles the slope plane, so half sinks in and half stands
    proud - which is exactly how a course of mission tile reads in silhouette.
    """
    made = []
    for side in (1.0, -1.0):
        for frac in (0.32, 0.56, 0.80):
            v = side * frac * v_half
            z = z1 - (z1 - z0) * frac
            u = ridge_half + (u_half - ridge_half) * frac
            made.append(
                box(
                    f"course_{'f' if side > 0 else 'r'}_{int(frac * 100)}",
                    -u, u, v - 0.18, v + 0.18, z - COURSE_T / 2, z + COURSE_T / 2, mat,
                )
            )
    return made


def bevel(obj, width=BEVEL_CHUNKY, segments=2):
    """Miniature-style edge softening on the chunky solids (style bible s.4).

    The width is clamped to a fraction of the object's own smallest dimension.
    A fixed 0.12 m bevel on a 0.15 m thick cornice self-intersects: it inverts
    the solid and leaves a scatter of zero-area faces, which fails both the
    signed-volume normals gate and the degenerate-geometry gate.
    """
    co = [v.co for v in obj.data.vertices]
    extent = [max(c[i] for c in co) - min(c[i] for c in co) for i in range(3)]
    width = min(width, 0.3 * min(e for e in extent if e > 1e-6))

    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.bevel(
        bm,
        geom=list(bm.verts) + list(bm.edges),
        offset=width,
        segments=segments,
        profile=0.5,
        affect="EDGES",
        clamp_overlap=True,
    )
    bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=list(bm.edges))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def window(name, axis, pos, offset, z0, z1, width, lit=False):
    """A dark reveal plate flush with the wall, with the glass set just behind.

    Cheap by design: two thin boxes read as a recessed window from the city
    camera for ~24 triangles, where a modelled reveal would cost hundreds.
    `axis` is 'v' for the long (front/rear) faces, 'u' for the short ends.
    `offset` is the signed wall coordinate on the other axis.
    """
    glass = material("Toy_glass_Glow" if lit else "Toy_glass")
    ink = material("Toy_ink")
    pad = WIN_PAD
    # The glass sits PROUD of the reveal plate. The other way round buries the
    # pane in its own shadow and every window renders as a black hole.
    if axis == "v":
        s = 1.0 if offset > 0 else -1.0
        box(f"{name}_reveal", pos - width / 2 - pad, pos + width / 2 + pad,
            offset - 0.12 * s, offset - 0.02 * s, z0 - pad, z1 + pad, ink)
        box(f"{name}_glass", pos - width / 2, pos + width / 2,
            offset - 0.07 * s, offset + 0.01 * s, z0, z1, glass)
    else:
        s = 1.0 if offset > 0 else -1.0
        box(f"{name}_reveal", offset - 0.12 * s, offset - 0.02 * s,
            pos - width / 2 - pad, pos + width / 2 + pad, z0 - pad, z1 + pad, ink)
        box(f"{name}_glass", offset - 0.07 * s, offset + 0.01 * s,
            pos - width / 2, pos + width / 2, z0, z1, glass)


# ---------------------------------------------------------------------- build


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)

    cream = material("Toy_cream")
    brick = material("Toy_brick")
    trim = material("Toy_trim")
    stone = material("Toy_stone")
    ink = material("Toy_ink")

    lu, lv = L / 2, W / 2                 # wall half-extents
    pu, pv = lu + PLINTH_OUT, lv + PLINTH_OUT
    porch_back = lv - PORCH_DEPTH         # the recessed ground-floor front wall

    chunky = []

    # 1. raised base -------------------------------------------------------
    chunky.append(box("plinth", -pu, pu, -pv, pv, 0.0, H_PLINTH, stone))

    # 2. body, built around the porch void so no boolean is needed ----------
    chunky.append(box("body_main", -lu, lu, -lv, porch_back, H_PLINTH, H_EAVE, cream))
    chunky.append(box("return_nne", PORCH_HALF, lu, porch_back, lv, H_PLINTH, H_EAVE, cream))
    chunky.append(box("return_ssw", -lu, -PORCH_HALF, porch_back, lv, H_PLINTH, H_EAVE, cream))
    # the second storey oversails the porch
    chunky.append(box("body_over_porch", -PORCH_HALF, PORCH_HALF, porch_back, lv,
                      H_PENT, H_EAVE, cream))

    # 3. pent roof / belt course, and the trim cornice under it ------------
    chunky.append(ring("cornice", lu + 0.25, lv + 0.25, lu - 0.1, lv - 0.1,
                       H_PENT - 0.15, H_PENT, trim))
    chunky.append(ring("pent_roof", lu + PENT_OUT, lv + PENT_OUT, lu - 0.15, lv - 0.15,
                       H_PENT, H_PENT + PENT_T, brick))

    # 4. porch: four chunky columns over a solid stucco balustrade ---------
    for i, u in enumerate((-7.4, -2.5, 2.5, 7.4)):
        chunky.append(box(f"column_{i}", u - COLUMN_HALF, u + COLUMN_HALF,
                          lv - 2 * COLUMN_HALF, lv, H_PLINTH, H_PENT, trim))
    for i, (u0, u1) in enumerate(((-PORCH_HALF, -1.6), (1.6, PORCH_HALF))):
        chunky.append(box(f"balustrade_{i}", u0, u1, lv - BALUSTRADE_T, lv,
                          H_PLINTH, H_PLINTH + BALUSTRADE_H, trim))

    # 5. entry steps -------------------------------------------------------
    for i in range(STEP_N):
        z0 = i * H_PLINTH / STEP_N
        z1 = (i + 1) * H_PLINTH / STEP_N
        out = lv + (STEP_N - 1 - i) * STEP_TREAD
        box(f"step_{i}", -STEP_W / 2, STEP_W / 2, lv - 0.1, out, z0, z1, stone)

    # 6. two front doors - the duplex cue ----------------------------------
    for i, u in enumerate((-1.2, 1.2)):
        box(f"door_{i}", u - 0.5, u + 0.5, porch_back, porch_back + 0.09,
            H_PLINTH, H_PLINTH + 2.1, ink)

    # 7. windows -----------------------------------------------------------
    up_z = (5.6, 7.5)      # upper storey
    lo_z = (1.75, 3.65)    # ground storey (rear and ends only; the front is porch)
    lit = {("v", 1, -7.2), ("v", 1, 2.4), ("v", -1, -2.4)}
    for u in (-7.2, -2.4, 2.4, 7.2):
        window(f"win_up_front_{u}", "v", u, lv, *up_z, WIN_W,
               lit=("v", 1, u) in lit)
        window(f"win_up_rear_{u}", "v", u, -lv, *up_z, WIN_W,
               lit=("v", -1, u) in lit)
        window(f"win_lo_rear_{u}", "v", u, -lv, *lo_z, WIN_W)
    for v in (-3.4, 3.4):
        window(f"win_up_nne_{v}", "u", v, lu, *up_z, WIN_W)
        window(f"win_up_ssw_{v}", "u", v, -lu, *up_z, WIN_W)
        window(f"win_lo_nne_{v}", "u", v, lu, *lo_z, WIN_W)
        window(f"win_lo_ssw_{v}", "u", v, -lu, *lo_z, WIN_W)

    # 8. porch soffit light - the hero glow --------------------------------
    box("porch_light", -1.8, 1.8, lv - 1.7, lv - 0.5, H_PENT - 0.14, H_PENT - 0.02,
        material("Toy_white_Glow"))

    # 9. main hipped roof, capped ridge and hips, eave fascia --------------
    ru, rv = lu + EAVE_OUT, lv + EAVE_OUT
    z_ridge = H_CREST - RIDGE_CAP  # the capping course is what reaches the crest
    chunky.append(hip_roof("roof", ru, rv, RIDGE_HALF, H_EAVE, z_ridge, brick))
    chunky.append(ring("fascia", ru, rv, ru - 0.22, rv - 0.22,
                       H_EAVE - 0.18, H_EAVE, trim))
    roof_courses(ru, rv, RIDGE_HALF, H_EAVE, z_ridge, brick)
    segment_cap("ridge_cap", (-RIDGE_HALF, 0.0, z_ridge), (RIDGE_HALF, 0.0, z_ridge),
                0.26, RIDGE_CAP, brick)
    for i, (su, sv) in enumerate(((1, 1), (1, -1), (-1, 1), (-1, -1))):
        segment_cap(f"hip_cap_{i}", (su * RIDGE_HALF, 0.0, z_ridge),
                    (su * ru, sv * rv, H_EAVE), 0.22, RIDGE_CAP * 0.85, brick)

    # 10. chimneys ---------------------------------------------------------
    cu, cv = CHIMNEY
    for i, u in enumerate((-5.5, 5.5)):
        chunky.append(box(f"chimney_{i}", u - cu / 2, u + cu / 2, -3.0 - cv / 2,
                          -3.0 + cv / 2, H_EAVE - 1.2, H_CREST - 0.22, cream))
        box(f"chimney_cap_{i}", u - cu / 2 - 0.12, u + cu / 2 + 0.12,
            -3.0 - cv / 2 - 0.12, -3.0 + cv / 2 + 0.12,
            H_CREST - 0.22, H_CREST, ink)

    for obj in chunky:
        bevel(obj, BEVEL_CHUNKY if obj.name != "pent_roof" else BEVEL_THIN)


def normalise():
    """Sit the asset on z=0, centre the building on the origin, and land the
    crest on H_CREST exactly so the loader's targetHeightM/measured scale = 1.0.

    Bevelling shaves a few centimetres off the ridge; a uniform correction of
    well under 1% restores the contract without distorting proportions.
    """
    dg = bpy.context.evaluated_depsgraph_get()
    objs = [o for o in bpy.data.objects if o.type == "MESH"]

    def bbox():
        mn = Vector((1e9, 1e9, 1e9))
        mx = Vector((-1e9, -1e9, -1e9))
        for o in objs:
            ev = o.evaluated_get(dg)
            me = ev.to_mesh()
            for v in me.vertices:
                w = o.matrix_world @ v.co
                for i in range(3):
                    mn[i] = min(mn[i], w[i])
                    mx[i] = max(mx[i], w[i])
            ev.to_mesh_clear()
        return mn, mx

    mn, mx = bbox()
    scale = H_CREST / (mx[2] - mn[2])
    for o in objs:
        for v in o.data.vertices:
            w = o.matrix_world @ v.co
            v.co = Vector(((w[0]) * scale, (w[1]) * scale, (w[2] - mn[2]) * scale))
        o.matrix_world.identity()

    # Centre the BUILDING (plinth + roof) on the origin, not the bbox: the
    # entry steps project on one side only and must not shift the anchor.
    mn, mx = bbox()
    roof = bpy.data.objects["roof"]
    rmn = Vector((1e9, 1e9))
    rmx = Vector((-1e9, -1e9))
    for v in roof.data.vertices:
        for i in range(2):
            rmn[i] = min(rmn[i], v.co[i])
            rmx[i] = max(rmx[i], v.co[i])
    off = Vector(((rmn[0] + rmx[0]) / 2, (rmn[1] + rmx[1]) / 2, 0.0))
    for o in objs:
        for v in o.data.vertices:
            v.co -= off
    print(f"[build] normalise: scale={scale:.5f} recentre={[round(c, 3) for c in off]}")


def report():
    dg = bpy.context.evaluated_depsgraph_get()
    tris = 0
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    for o in objs:
        me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] materials={sorted(m.name for m in bpy.data.materials)}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    normalise()
    report()

    blend = os.path.join(out, "542-presidio-blvd.blend")
    glb = os.path.join(out, "542-presidio-blvd.glb")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    bpy.ops.export_scene.gltf(
        filepath=glb,
        export_format="GLB",
        export_apply=True,
        export_yup=True,
        use_selection=False,
        export_cameras=False,
        export_lights=False,
        export_animations=False,
        export_skins=False,
        export_morph=False,
        export_materials="EXPORT",
        export_image_format="NONE",
    )
    print(f"[build] wrote {blend}")
    print(f"[build] wrote {glb}")


if __name__ == "__main__":
    main()
