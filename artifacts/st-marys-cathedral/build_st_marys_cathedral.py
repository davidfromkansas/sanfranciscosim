"""Deterministic Blender build of the SF-SIM miniature St. Mary's Cathedral.

    blender -b --python build_st_marys_cathedral.py -- [--out DIR]

Writes st-marys-cathedral.blend and st-marys-cathedral.glb next to this file
(or into --out). Geometry is authored in world space in metres, Z up, +X east,
+Y north, origin at the plan centre (the cupola centre = the manifest anchor),
min Z = 0, and the whole model carries the real +9.1 deg CCW grid yaw measured
from OSM, so the loader drops it in at its true heading with no rotation.

Design (see REFERENCE.md for the sources behind every number):

* the cupola is a genuine ruled surface, which is the whole point of this
  building: every vertical line of the mesh is a straight ruling from a point
  on the square spring plan to the matching point on the Greek-cross crown
  plan, mapped by arc length. That single construction produces all eight
  hyperbolic-paraboloid segments - vertical at the face centres, scooping
  inward and downward at the corners - and it is why the silhouette reads as
  St Mary's rather than as a tapered box;
* a recessed stained-glass slot runs up the centre of each face and continues
  over each crown ridge to the apex skylight, so the four shells are visibly
  eight. Toy_glass by day; Toy_white_Glow ribbons floating inside the slots
  give the app's dusk pass the cross of light that is the building's night
  signature;
* the crown cap is a tent over the cross plan (ridges along the axes, valleys
  on the diagonals), so the top view - the view the app's camera actually gets
  - shows the cross and the four surfaces sweeping down from it;
* the low travertine base: 77.7 m ground-floor square with a recessed glazing
  band, a thin projecting fascia the shells spring from, bronze relief doors
  on Geary and a warm entrance lamp;
* the raised plaza podium with the monumental south stair cut into its Geary
  edge, and the slender 16.8 m golden cross at the apex.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

YAW = math.radians(9.1)  # OSM grid: building edges bear 81.0 / 170.9 deg

Z_PLAZA = 4.0        # podium deck = nave floor level
Z_GLASS0 = 10.2      # recessed glazing band in the travertine base
Z_GLASS1 = 11.9
GLASS_INSET = 1.4    # deep enough that the band reads as shadow, not paint
Z_BASE_WALL = 13.2   # top of the base walls
Z_FASCIA = 14.6      # projecting eave slab; the shells spring off it
Z_APEX = 61.9        # crown apex: 190 ft (57.9 m) above the nave floor
Z_GABLE = 60.1       # ridge height where an arm meets its end wall
CROSS_H = 16.8       # the 55 ft golden cross -> tip at 78.7 m

A_SPRING = 30.0      # half-width of the shell spring square. OSM traces the
                     # cupola part at 62.7 m; pulled in slightly (60 m) because
                     # every photograph reads the shell taller relative to its
                     # width than the published numbers alone produce, and the
                     # shell is the signature feature (style bible s.3, s.22)
A_BASE = 38.85       # half-width of the 77.7 m ground-floor square
BASE_CHAMFER = 5.0
FASCIA_HW = 40.3     # fascia overhangs the base walls
ARM_HW = 9.4         # crown arm half-width (18.8 m, OSM crown trace)
ARM_END = 31.0       # crown arm half-span; the crown is slightly wider than
                     # the spring, which is what the photographs show
SLOT_HW = 1.3        # stained-glass slot half-width
SLOT_DEPTH = 0.5     # slot recess into the shell

PODIUM_HW = 41.4     # styled plaza, just proud of the fascia (real site is
                     # 124 x 106 m, most of which is parish buildings and lot)
STAIR_W = 26.0       # monumental south stair
STAIR_D = 9.0        # stair run cut into the podium edge
STEPS = 8

N_RINGS = 20         # rings along the rulings
N_SIDE = 8           # columns between a corner and the slot, per half face

# Crown tent: h = Z_APEX - A_CROSS * min(|x|,|y|) - A_ARM * max(|x|,|y|).
A_ARM = (Z_APEX - Z_GABLE) / ARM_END
A_CROSS = 0.170      # cross-slope of each ridge

# Project palette from .agents/skills/sf-asset-check (hex, sRGB). Materials
# are authored with the linear equivalents, matching the shipped kit GLBs.
PALETTE_HEX = {
    "Toy_white": "f7f4ec",
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    "Toy_glass": "2a4d73",
    "Toy_ink": "3a3530",
    "Toy_gold": "caa64a",
    "Toy_white_Glow": "f7f4ec",
    "Toy_gold_Glow": "caa64a",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# -------------------------------------------------------------- mesh helpers


def rot2(p, ang=YAW):
    c, s = math.cos(ang), math.sin(ang)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def new_mesh(name, verts, faces, materials, face_mats=None, recalc=True, smooth=False):
    """Create an object; every vertex is yawed onto the real city heading.

    recalc=False keeps the authored winding, used for the open sheets (crown
    cap, glow ribbons) whose outward side recalc_face_normals cannot infer.
    smooth=True is reserved for the doubly-curved shell, where the style
    bible's "smooth curves where they create a landmark silhouette" (s.4)
    beats faceting; every chunky solid stays flat-shaded.
    """
    yawed = [Vector((*rot2((v[0], v[1])), v[2])) for v in verts]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(yawed, [], faces)
    for m in materials:
        mesh.materials.append(m)
    if face_mats:
        for poly, mi in zip(mesh.polygons, face_mats):
            poly.material_index = mi
    mesh.validate()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    if recalc:
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.free()
    if smooth:
        mesh.shade_smooth()
    else:
        mesh.shade_flat()
    return obj


def bevel(obj, width=0.12, segments=2):
    """Miniature-style edge softening on the chunky solids (style bible s.4)."""
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
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def box(name, cx, cy, z0, z1, sx, sy, mat):
    hx, hy = sx / 2, sy / 2
    verts = [(cx + x, cy + y, z0) for x, y in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy))]
    verts += [(cx + x, cy + y, z1) for x, y in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy))]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_mesh(name, verts, faces, [mat])


def slab(name, x0, x1, y0, y1, z0, z1, mat):
    """Axis-aligned box from explicit plan extents (before the yaw)."""
    return box(name, (x0 + x1) / 2, (y0 + y1) / 2, z0, z1, x1 - x0, y1 - y0, mat)


def prism(name, plan, z0, z1, mat):
    """Extrude a closed CCW plan polygon between two heights, capped."""
    n = len(plan)
    verts = [(x, y, z0) for x, y in plan] + [(x, y, z1) for x, y in plan]
    faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    return new_mesh(name, verts, faces, [mat])


def ring_prism(name, outer, inner, z0, z1, mat):
    """A closed band between two matching plan polygons: outer wall, inner
    wall and both lips. Used for the base roof parapet."""
    n = len(outer)
    verts = [(x, y, z0) for x, y in outer] + [(x, y, z0) for x, y in inner]
    verts += [(x, y, z1) for x, y in outer] + [(x, y, z1) for x, y in inner]
    o0, i0, o1, i1 = 0, n, 2 * n, 3 * n
    faces = []
    for k in range(n):
        j = (k + 1) % n
        faces.append((o0 + k, o0 + j, o1 + j, o1 + k))  # outer wall
        faces.append((i0 + j, i0 + k, i1 + k, i1 + j))  # inner wall
        faces.append((o1 + k, o1 + j, i1 + j, i1 + k))  # top lip
        faces.append((i0 + k, i0 + j, o0 + j, o0 + k))  # bottom lip
    return new_mesh(name, verts, faces, [mat])


def chamfered_square(half, leg):
    """CCW octagon: a square of the given half-width with 45-degree corners."""
    h, l = half, leg
    return [
        (h, -h + l), (h, h - l), (h - l, h), (-h + l, h),
        (-h, h - l), (-h, -h + l), (-h + l, -h), (h - l, -h),
    ]


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
        # Flagged for the app's night pass; emission is off in the day asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    mat.blend_method = "OPAQUE"
    return mat


# --------------------------------------------------- the ruled hypar surface


def crown_height(x, y):
    """Tent over the Greek-cross crown: ridges on the axes, valleys on the
    diagonals. Gives the crown its four sloping arms and the apex."""
    p, q = min(abs(x), abs(y)), max(abs(x), abs(y))
    return Z_APEX - A_CROSS * p - A_ARM * q


def top_point(u):
    """Crown-plan point matched to bottom-edge parameter u in [-1, 1] on the
    +Y face, mapped by arc length: the correspondence that rules the hypar."""
    f = (u + 1.0) / 2.0
    side = ARM_END - ARM_HW
    ell = (1.0 - f) * 2.0 * ARM_END  # measured CCW from the +X-side corner
    if ell < side:
        return (ARM_HW, ARM_HW + ell)
    if ell < side + 2.0 * ARM_HW:
        return (ARM_HW - (ell - side), ARM_END)
    return (-ARM_HW, ARM_END - (ell - side - 2.0 * ARM_HW))


U_SLOT = SLOT_HW / A_SPRING


def columns():
    """One face's columns, CCW from its +X-side corner, excluding the next
    corner. Each column is (bottom_xy, top_xy, recess)."""
    cols = []
    for i in range(N_SIDE + 1):  # corner -> slot edge
        u = 1.0 - (1.0 - U_SLOT) * i / N_SIDE
        cols.append(((u * A_SPRING, A_SPRING), top_point(u), 0.0))
    for u in (U_SLOT, -U_SLOT):  # the recessed slot floor
        cols.append(((u * A_SPRING, A_SPRING), top_point(u), SLOT_DEPTH))
    for i in range(N_SIDE):  # slot edge -> just before the next corner
        u = -U_SLOT - (1.0 - U_SLOT) * i / N_SIDE
        cols.append(((u * A_SPRING, A_SPRING), top_point(u), 0.0))
    return cols


COLS = columns()
PER_FACE = len(COLS)
GLASS_STRIPS = {N_SIDE, N_SIDE + 1, N_SIDE + 2}  # step in, slot floor, step out


def column_point(col, t):
    """Straight ruling from the spring square to the crown outline."""
    (bx, by), (tx, ty), recess = col
    x = bx + (tx - bx) * t
    y = by + (ty - by) * t
    z = Z_FASCIA + (crown_height(tx, ty) - Z_FASCIA) * t
    if recess:
        d = math.hypot(x, y) or 1.0
        x -= x / d * recess
        y -= y / d * recess
    return x, y, z


def build_cupola(white, glass):
    verts = []
    for r in range(N_RINGS + 1):
        t = r / N_RINGS
        for quad in range(4):
            a = quad * math.pi / 2
            cq, sq = math.cos(a), math.sin(a)
            for col in COLS:
                x, y, z = column_point(col, t)
                verts.append((x * cq - y * sq, x * sq + y * cq, z))
    n = 4 * PER_FACE
    faces, mats = [], []
    for r in range(N_RINGS):
        for i in range(n):
            j = (i + 1) % n
            faces.append((r * n + i, r * n + j, (r + 1) * n + j, (r + 1) * n + i))
            mats.append(1 if (i % PER_FACE) in GLASS_STRIPS else 0)
    faces.append(tuple(range(n - 1, -1, -1)))  # bottom cap, hidden by the fascia
    mats.append(0)
    return new_mesh("cupola", verts, faces, [white, glass], mats, smooth=True)


def build_crown(white, glass):
    """Cap the crown: eight patches, one per half-arm, split on the diagonals
    so the ridges and the apex fall out of the tent function exactly."""
    objs = []
    n_p, n_q = 6, 6
    for quadn in range(4):
        a = quadn * math.pi / 2
        cq, sq = math.cos(a), math.sin(a)
        for sign in (1, -1):
            verts, faces, mats = [], [], []
            for i in range(n_p + 1):
                p = ARM_HW * i / n_p
                for j in range(n_q + 1):
                    q = p + (ARM_END - p) * j / n_q
                    z = crown_height(p, q)
                    x, y = sign * p, q
                    verts.append((x * cq - y * sq, x * sq + y * cq, z))
            for i in range(n_p):
                for j in range(n_q):
                    k = i * (n_q + 1) + j
                    # Wound so the patch faces up: the (p, q) grid traverses
                    # clockwise from above on the +p half and mirrors on -p.
                    quad = (k, k + 1, k + n_q + 2, k + n_q + 1)
                    faces.append(quad[::-1] if sign > 0 else quad)
                    mats.append(1 if ARM_HW * i / n_p < SLOT_HW else 0)
            objs.append(new_mesh(f"crown_{quadn}{'r' if sign > 0 else 'l'}",
                                 verts, faces, [white, glass], mats, recalc=False))
    return objs


def build_slot_glow(glow):
    """Night ribbons inside the slots: the cross of light.

    Each ribbon is a closed thin tube rather than a sheet, so it has no back
    face a grazing ray can see through the slot opening, and the normals can
    be recalculated rather than hand-wound.
    """
    objs = []
    ghw = 0.55    # narrower than the slot, so the dark glass frames the light
    lift = 0.22   # proud of the recessed floor, still behind the shell face
    thick = 0.14
    left = COLS[N_SIDE + 1]  # the two recessed columns bound the slot floor
    right = COLS[N_SIDE + 2]

    for quadn in range(4):
        a = quadn * math.pi / 2
        cq, sq = math.cos(a), math.sin(a)

        def R(x, y, z):
            return (x * cq - y * sq, x * sq + y * cq, z)

        # Centreline stations, each with the direction the lit face points.
        stations = []
        for r in range(N_RINGS + 1):
            t = max(r / N_RINGS, 0.03)
            xl, yl, zl = column_point(left, t)
            xr, yr, zr = column_point(right, t)
            cx, cy = (xl + xr) / 2, (yl + yr) / 2
            d = math.hypot(cx, cy) or 1.0
            nx, ny = cx / d, cy / d
            stations.append(((cx + nx * lift, cy + ny * lift, (zl + zr) / 2), (nx, ny, 0.0)))
        y_crest = ARM_END - 0.4
        stations.append(((0.0, y_crest, crown_height(0.0, y_crest) + 0.1), (0.0, 0.0, 1.0)))
        stations.append(((0.0, 0.0, Z_APEX + 0.1), (0.0, 0.0, 1.0)))

        verts, faces = [], []
        for (px, py, pz), (dx, dy, dz) in stations:
            for lx, back in ((ghw, 0.0), (ghw, 1.0), (-ghw, 1.0), (-ghw, 0.0)):
                verts.append(
                    R(px + lx - dx * thick * back, py - dy * thick * back,
                      pz - dz * thick * back)
                )
        for s in range(len(stations) - 1):
            k = 4 * s
            for e in range(4):
                f = (e + 1) % 4
                faces.append((k + e, k + f, k + 4 + f, k + 4 + e))
        faces.append((3, 2, 1, 0))
        k = 4 * (len(stations) - 1)
        faces.append((k, k + 1, k + 2, k + 3))
        objs.append(new_mesh(f"slot_glow_{quadn}", verts, faces, [glow]))
    return objs


# --------------------------------------------------------------------- build


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    white = material("Toy_white")
    stone = material("Toy_stone")
    trim = material("Toy_trim")
    glass = material("Toy_glass")
    ink = material("Toy_ink")
    gold = material("Toy_gold")
    glow = material("Toy_white_Glow")
    gold_glow = material("Toy_gold_Glow")

    # --- podium: the raised plaza, monumental stair cut into its Geary edge -
    hw, sw = PODIUM_HW, STAIR_W / 2
    y_notch = -hw + STAIR_D
    bevel(slab("podium_w", -hw, -sw, -hw, hw, 0.0, Z_PLAZA, stone))
    bevel(slab("podium_e", sw, hw, -hw, hw, 0.0, Z_PLAZA, stone))
    bevel(slab("podium_n", -sw, sw, y_notch, hw, 0.0, Z_PLAZA, stone))
    rise, run = Z_PLAZA / STEPS, STAIR_D / STEPS
    for k in range(STEPS):
        bevel(slab(f"stair_{k}", -sw, sw, -hw + k * run, y_notch, 0.0, (k + 1) * rise, stone),
              width=0.06)

    # A flush paving inlay keeps the plaza from reading as a blank plate from
    # the app's downward camera (style bible s.10) without adding any props.
    for k, (x0, x1, y0, y1) in enumerate(
        (
            (-hw + 1.6, hw - 1.6, -hw + 1.6, -hw + 2.3),
            (-hw + 1.6, hw - 1.6, hw - 2.3, hw - 1.6),
            (-hw + 1.6, -hw + 2.3, -hw + 2.3, hw - 2.3),
            (hw - 2.3, hw - 1.6, -hw + 2.3, hw - 2.3),
        )
    ):
        slab(f"plaza_inlay_{k}", x0, x1, y0, y1, Z_PLAZA - 0.06, Z_PLAZA + 0.02, trim)

    # --- travertine base: solid walls with a genuinely recessed glazing band -
    plan = chamfered_square(A_BASE, BASE_CHAMFER)
    inset = chamfered_square(A_BASE - GLASS_INSET, BASE_CHAMFER)
    bevel(prism("base_lower", plan, Z_PLAZA, Z_GLASS0, stone), width=0.12)
    prism("base_glazing", inset, Z_GLASS0, Z_GLASS1, glass)
    bevel(prism("base_upper", plan, Z_GLASS1, Z_BASE_WALL, stone), width=0.12)
    bevel(prism("fascia", chamfered_square(FASCIA_HW, BASE_CHAMFER + 1.5),
                Z_BASE_WALL, Z_FASCIA, trim), width=0.15)

    # The base roof is a broad surface under the app's downward camera, so it
    # is designed rather than left blank: a recessed deck inside a low parapet.
    deck_plan = chamfered_square(FASCIA_HW - 2.2, BASE_CHAMFER + 1.0)
    prism("roof_deck", deck_plan, Z_FASCIA - 0.5, Z_FASCIA + 0.02, stone)
    ring_prism("roof_parapet", chamfered_square(FASCIA_HW, BASE_CHAMFER + 1.5),
               deck_plan, Z_FASCIA, Z_FASCIA + 0.85, trim)

    # --- Geary entrance: bronze relief doors and the lamp band above them ---
    ds = -(A_BASE + 0.2)
    for k, dx in enumerate((-7.6, 0.0, 7.6)):
        bevel(box(f"door_{k}", dx, ds, Z_PLAZA, Z_PLAZA + 4.8, 5.8, 0.5, ink), width=0.08)
    bevel(box("entrance_lamp", 0.0, ds - 0.05, Z_PLAZA + 5.1, Z_PLAZA + 5.6, 19.0, 0.4,
              gold_glow), width=0.06)

    # --- the cupola, its crown, and the night ribbons in the glass slots ----
    build_cupola(white, glass)
    build_crown(white, glass)
    build_slot_glow(glow)

    # --- the 55 ft golden cross at the apex --------------------------------
    bevel(box("cross_post", 0.0, 0.0, Z_APEX, Z_APEX + CROSS_H, 1.0, 1.0, gold), width=0.12)
    bar_z = Z_APEX + CROSS_H * 0.64
    bevel(box("cross_bar", 0.0, 0.0, bar_z, bar_z + 1.0, 7.6, 0.9, gold), width=0.12)

    return scene


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
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "st-marys-cathedral.blend")
    glb = os.path.join(out, "st-marys-cathedral.glb")
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
