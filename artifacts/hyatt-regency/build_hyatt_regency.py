"""Deterministic Blender build of the SF-SIM miniature Hyatt Regency San Francisco.

    blender -b --python build_hyatt_regency.py -- [--out DIR]

Writes hyatt-regency.blend and hyatt-regency.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y true
north; the model is recentred on its XY bbox at the end (contract rule 2) and its
crest normalised to exactly 80.8 m (the loader's targetHeightM).

Design (see REFERENCE.md for the sources behind every number):

* the plan is the real OSM footprint (way/28319370) reduced to seven points,
  6,663 m2 against the surveyed 6,672 (0.13%). It is a wedge in PLAN: 23.6 m deep
  at the Embarcadero Plaza prow, 82.7 m at Drumm Street;
* a wedge in SECTION too: fifteen guest-room slabs, slab n being the site polygon
  clipped to v >= V_WING - 3.0*(14-n). One rule, and the site polygon does the
  rest - which is why the terrace count runs from fifteen at Drumm down to three
  at the prow, exactly as the aerial photography shows;
* every slab is a dark recessed body under a pale fascia, so the stepped mass
  reads as a staircase of floor plates from the app's aerial camera;
* deep precast piers with narrow window slots on the three full-height faces
  (Market, the plaza prow, the Market/Drumm end) - the brutalist rhythm;
* a two-storey podium with a recessed glazed arcade (the night-glow hero: the
  world's largest hotel atrium is behind it) and a projecting eave;
* the Equinox pavilion at the Drumm end: a drum under two cantilevered concrete
  frames, whose upper ring IS the 80.8 m architectural top;
* flat Toy_* materials only. Two glow surfaces: the podium arcade glass and one
  warm band under the Equinox upper frame.
"""

import math
import os
import sys

import bmesh
import bpy

# ---------------------------------------------------------------- parameters

H_TOP = 80.8          # CTBUH architectural top; DataSF LiDAR max 80.64
H_PODIUM = 12.0       # podium roof / underside of the stepped mass
H_DECK = 72.0         # wing roof deck = top of slab 14
H_PARAPET = 73.4

AXIS = 45.8           # true bearing of the Market Street frontage
V_MARKET = 39.12      # v of the Market frontage line
V_WING = 13.12        # v of the wing's inner face = the top slab's back edge

N_SLAB = 15
DZ_SLAB = 4.0
DV_SLAB = 3.9         # ~44 deg: the wedge reaches the far site line at Drumm

LIP_H = 1.5           # pale slab edge - the tread you see from above
LIP_PROUD = 0.35      # how far it oversails the dark band
LIP_TREAD = 2.6       # how far the pale tread runs back before the dark reveal

FIN_PITCH = 4.8       # precast pier rhythm on the full-height faces
FIN_W = 3.2           # wide pier, narrow slot - as built
FIN_PROUD = 0.60      # piers run past the floor lines
FIN_BITE = 0.20       # and bite into the wall behind, so nothing floats

PLINTH_H = 1.4
ARCADE_HI = 7.2
ARCADE_IN = 1.3
EAVE_LO = 10.9
EAVE_OUT = 1.1

RIDGE_U0, RIDGE_U1 = -18.0, 50.0
RIDGE_V0, RIDGE_V1 = 26.1, 29.6
RIDGE_H = 1.9

EQ_U, EQ_V = -38.0, 18.0
EQ_CORE = 14.0
EQ_DRUM_R = 10.0
EQ_DRUM_SEG = 16
EQ_DRUM_LO, EQ_DRUM_HI = 73.4, 78.2
EQ_F1 = (28.0, 24.0, 77.0, 78.4)
EQ_F2 = (32.0, 27.0, 79.4, H_TOP)
EQ_FRAME_T = 4.0
EQ_GLOW_H = 0.9       # the revolving-restaurant window band

BEVEL = 0.12
BEVEL_SEG = 2

# Simplified footprint in building axes (plan 2.3). Clockwise in uv.
PLAN_UV = [
    (-40.40, 39.11),   # P0  Market/Drumm end of the Market frontage
    (55.21, 39.13),    # P1  east corner
    (55.21, 29.18),    # P2  prow
    (55.21, 15.54),    # P3  prow / start of the north-west frontage
    (-28.16, -43.61),  # P4  north-west corner
    (-43.26, -29.71),  # P5  Drumm jog
    (-75.56, 22.61),   # P6  Market/Drumm corner
]

# Full-height fin walls: Market (0), the two prow segments (1, 2), the
# Market/Drumm end (6). Edges 3-5 are the terraced faces.
FIN_EDGES = (0, 1, 2, 6)

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    "Toy_steel": "9aa0a6",
    "Toy_glass": "2a4d73",
    "Toy_glassl_Glow": "6f95b8",
    "Toy_gold_Glow": "caa64a",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


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
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    return mat


# --------------------------------------------------------------- uv -> world

_A = math.radians(AXIS)
_SU, _CU = math.sin(_A), math.cos(_A)
_SV, _CV = math.sin(_A + math.pi / 2), math.cos(_A + math.pi / 2)


def world(u, v):
    return (u * _SU + v * _SV, u * _CU + v * _CV)


# world() has Jacobian determinant -1: it maps (u, v) to (east, north) through a
# reflection, so a polygon that is counter-clockwise in uv comes out CLOCKWISE in
# world space. Every face winding below is therefore taken from the uv area with
# the sign FLIPPED - getting this backwards inverted every solid in the asset and
# the ray test reported 100% of visible faces flipped.
def world_ccw(pts):
    return pts[::-1] if poly_area(pts) > 0 else list(pts)


# ------------------------------------------------------------ plan utilities


def poly_area(pts):
    a = 0.0
    n = len(pts)
    for i in range(n):
        u1, v1 = pts[i]
        u2, v2 = pts[(i + 1) % n]
        a += u1 * v2 - u2 * v1
    return a / 2.0


def dedup(pts, eps=1e-6):
    out = []
    for p in pts:
        if not out or math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) > eps:
            out.append(p)
    while len(out) > 1 and math.hypot(out[0][0] - out[-1][0], out[0][1] - out[-1][1]) <= eps:
        out.pop()
    return out


def inward_normal(du, dv, ccw):
    ln = math.hypot(du, dv)
    if ln < 1e-12:
        return (0.0, 0.0)
    return (-dv / ln, du / ln) if ccw else (dv / ln, -du / ln)


def inset(pts, d):
    """Offset every edge inward by d (negative expands). Convex plans only."""
    pts = dedup(pts)
    ccw = poly_area(pts) > 0
    lines = []
    n = len(pts)
    for i in range(n):
        u1, v1 = pts[i]
        u2, v2 = pts[(i + 1) % n]
        du, dv = u2 - u1, v2 - v1
        ln = math.hypot(du, dv)
        if ln < 1e-9:
            continue
        nu, nv = inward_normal(du, dv, ccw)
        lines.append((u1 + nu * d, v1 + nv * d, du / ln, dv / ln))
    out = []
    m = len(lines)
    for i in range(m):
        ax, ay, adx, ady = lines[i - 1]
        bx, by, bdx, bdy = lines[i]
        den = adx * bdy - ady * bdx
        if abs(den) < 1e-9:
            out.append((bx, by))
            continue
        t = ((bx - ax) * bdy - (by - ay) * bdx) / den
        out.append((ax + adx * t, ay + ady * t))
    return out


def clip_half(pts, vmin):
    """Sutherland-Hodgman clip of a uv polygon to the half-plane v >= vmin."""
    out = []
    n = len(pts)
    for i in range(n):
        cu, cv = pts[i]
        pu, pv = pts[i - 1]
        cin, pin = cv >= vmin, pv >= vmin
        if cin != pin:
            t = (vmin - pv) / (cv - pv)
            out.append((pu + t * (cu - pu), vmin))
        if cin:
            out.append((cu, cv))
    return out


# ------------------------------------------------------------------ geometry

MESHES = []


def emit(name, bm, mat):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(material(mat))
    bpy.context.collection.objects.link(ob)
    MESHES.append(ob)
    return ob


def prism(name, uv_pts, z0, z1, mat):
    pts = dedup(uv_pts)
    if len(pts) < 3 or abs(poly_area(pts)) < 1e-3 or z1 - z0 < 1e-4:
        return None
    pts = world_ccw(pts)
    bm = bmesh.new()
    lo = [bm.verts.new((*world(u, v), z0)) for u, v in pts]
    hi = [bm.verts.new((*world(u, v), z1)) for u, v in pts]
    bm.verts.ensure_lookup_table()
    n = len(pts)
    for i in range(n):
        bm.faces.new((lo[i], lo[(i + 1) % n], hi[(i + 1) % n], hi[i]))
    bm.faces.new(hi)                          # +Z
    bm.faces.new(lo[::-1])                    # -Z
    bm.normal_update()
    return emit(name, bm, mat)


def box_uv(name, u0, u1, v0, v1, z0, z1, mat):
    return prism(name, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], z0, z1, mat)


def ring_prism(name, outer, inner, z0, z1, mat):
    """A closed ring solid between two same-length polygons."""
    o = dedup(outer)
    i = dedup(inner)
    if len(o) != len(i) or len(o) < 3:
        return None
    if poly_area(o) > 0:
        o, i = o[::-1], i[::-1]
    bm = bmesh.new()
    n = len(o)
    ov0 = [bm.verts.new((*world(*p), z0)) for p in o]
    ov1 = [bm.verts.new((*world(*p), z1)) for p in o]
    iv0 = [bm.verts.new((*world(*p), z0)) for p in i]
    iv1 = [bm.verts.new((*world(*p), z1)) for p in i]
    for k in range(n):
        j = (k + 1) % n
        bm.faces.new((ov0[k], ov0[j], ov1[j], ov1[k]))     # outer wall
        bm.faces.new((iv0[j], iv0[k], iv1[k], iv1[j]))     # inner wall
        bm.faces.new((ov1[k], ov1[j], iv1[j], iv1[k]))     # top
        bm.faces.new((iv0[k], iv0[j], ov0[j], ov0[k]))     # bottom
    bm.normal_update()
    return emit(name, bm, mat)


def cylinder(name, cu, cv, r, z0, z1, seg, mat):
    pts = [
        (cu + r * math.cos(2 * math.pi * i / seg), cv + r * math.sin(2 * math.pi * i / seg))
        for i in range(seg)
    ]
    return prism(name, pts, z0, z1, mat)


def frame_ring(name, cu, cv, su, sv, z0, z1, t, mat):
    """A hollow rectangular ring built from four bars (outer su x sv)."""
    ou0, ou1 = cu - su / 2, cu + su / 2
    ov0, ov1 = cv - sv / 2, cv + sv / 2
    iu0, iu1 = ou0 + t, ou1 - t
    iv0, iv1 = ov0 + t, ov1 - t
    for k, (a, b, c, d) in enumerate(
        [
            (ou0, ou1, ov0, iv0),
            (ou0, ou1, iv1, ov1),
            (ou0, iu0, iv0, iv1),
            (iu1, ou1, iv0, iv1),
        ]
    ):
        box_uv(f"{name}_{k}", a, b, c, d, z0, z1, mat)


# ----------------------------------------------------------------- the build


def slab_v(n):
    return V_WING - DV_SLAB * (N_SLAB - 1 - n)


def simplify(pts, eps=0.30, flat=0.02):
    """Drop slivers a half-plane clip leaves where it grazes a plan corner.

    slab_lip_00's clip passed 0.73 m from P4 and produced two sub-millimetre
    edges; after the bevel those became four degenerate triangles and eight
    non-unit loop normals, which is a validator FAIL for the whole asset.
    """
    pts = dedup(pts, eps)
    out = []
    n = len(pts)
    for i in range(n):
        au, av = pts[i - 1]
        bu, bv = pts[i]
        cu, cv = pts[(i + 1) % n]
        du, dv = cu - au, cv - av
        ln = math.hypot(du, dv)
        if ln > 1e-9 and abs((bu - au) * dv - (bv - av) * du) / ln < flat:
            continue
        out.append((bu, bv))
    return out if len(out) >= 3 else pts


def slab_plan(n):
    return simplify(clip_half(PLAN_UV, slab_v(n)))


def fins():
    """Precast piers on the three full-height faces. Every slab reaches these
    edges (their v never drops below V_WING), so the wall runs 12.0 -> 72.0."""
    ccw = poly_area(PLAN_UV) > 0
    n = len(PLAN_UV)
    for e in FIN_EDGES:
        u1, v1 = PLAN_UV[e]
        u2, v2 = PLAN_UV[(e + 1) % n]
        du, dv = u2 - u1, v2 - v1
        ln = math.hypot(du, dv)
        if ln < FIN_PITCH:
            continue
        tu, tv = du / ln, dv / ln
        nu, nv = inward_normal(du, dv, ccw)
        count = max(1, int(round(ln / FIN_PITCH)))
        gap = ln / count
        for i in range(count):
            t = gap * (i + 0.5)
            cu, cv = u1 + tu * t, v1 + tv * t
            half = min(FIN_W, gap - 1.2) / 2.0
            a = (cu - tu * half - nu * FIN_PROUD, cv - tv * half - nv * FIN_PROUD)
            b = (cu + tu * half - nu * FIN_PROUD, cv + tv * half - nv * FIN_PROUD)
            c = (b[0] + nu * (FIN_PROUD + FIN_BITE), b[1] + nv * (FIN_PROUD + FIN_BITE))
            d = (a[0] + nu * (FIN_PROUD + FIN_BITE), a[1] + nv * (FIN_PROUD + FIN_BITE))
            prism(f"fin_{e}_{i:02d}", [a, b, c, d], H_PODIUM, H_DECK, "Toy_stone")


def build():
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    for me in list(bpy.data.meshes):
        bpy.data.meshes.remove(me)
    MESHES.clear()

    # ---- podium: plinth, recessed glazed arcade, upper band, eave ----------
    prism("podium_plinth", PLAN_UV, 0.0, PLINTH_H, "Toy_stone")
    prism("podium_arcade", inset(PLAN_UV, ARCADE_IN), PLINTH_H, ARCADE_HI,
          "Toy_glassl_Glow")
    prism("podium_upper", PLAN_UV, ARCADE_HI, EAVE_LO, "Toy_stone")
    prism("podium_eave", inset(PLAN_UV, -EAVE_OUT), EAVE_LO, H_PODIUM, "Toy_trim")

    # ---- the stepped mass: a dark band under a proud pale slab edge --------
    # Fifteen times. From the side this is the Portman balcony rhythm; from
    # directly above the lips are the treads and the whole wedge reads as a
    # concrete staircase, which is what the app's camera actually sees.
    for n in range(N_SLAB):
        pts = slab_plan(n)
        if len(pts) < 3:
            continue
        z0 = H_PODIUM + DZ_SLAB * n
        z1 = z0 + DZ_SLAB
        prism(f"slab_band_{n:02d}", pts, z0, z1 - LIP_H, "Toy_glass")
        # The lip is a RING, not a plate: from directly above the pale tread
        # runs LIP_TREAD back and then the dark band top shows as a reveal, so
        # the staircase has contrast in plan instead of being one flat field.
        outer = inset(pts, -LIP_PROUD)
        inner = inset(pts, LIP_TREAD)
        top_slab = n == N_SLAB - 1
        if not top_slab and abs(poly_area(inner)) > 0.15 * abs(poly_area(outer)):
            ring_prism(f"slab_lip_{n:02d}", outer, inner, z1 - LIP_H, z1, "Toy_stone")
        else:
            prism(f"slab_lip_{n:02d}", outer, z1 - LIP_H, z1, "Toy_stone")

    fins()

    # ---- wing roof ---------------------------------------------------------
    wing = slab_plan(N_SLAB - 1)
    prism("wing_deck", inset(wing, 1.10), H_DECK, H_DECK + 0.18, "Toy_steel")
    ring_prism("wing_parapet", inset(wing, -0.30), inset(wing, 1.10),
               H_DECK, H_PARAPET, "Toy_steel")
    box_uv("wing_ridge", RIDGE_U0, RIDGE_U1, RIDGE_V0, RIDGE_V1,
           H_DECK, H_DECK + RIDGE_H, "Toy_steel")
    box_uv("wing_ridge_cap", RIDGE_U0 - 0.4, RIDGE_U1 + 0.4, RIDGE_V0 - 0.4,
           RIDGE_V1 + 0.4, H_DECK + RIDGE_H - 0.45, H_DECK + RIDGE_H, "Toy_trim")
    for i, u in enumerate((-10.0, 8.0, 26.0, 42.0)):
        cylinder(f"wing_mech_{i}", u, 20.5, 2.6, H_DECK, H_DECK + 2.4, 12, "Toy_steel")

    # ---- Equinox pavilion --------------------------------------------------
    box_uv("eq_core", EQ_U - EQ_CORE / 2, EQ_U + EQ_CORE / 2,
           EQ_V - EQ_CORE / 2, EQ_V + EQ_CORE / 2, H_PODIUM, H_PARAPET, "Toy_stone")
    cylinder("eq_drum", EQ_U, EQ_V, EQ_DRUM_R, EQ_DRUM_LO, EQ_DRUM_HI - EQ_GLOW_H,
             EQ_DRUM_SEG, "Toy_steel")
    # the revolving restaurant's window band is the warm night accent, and it
    # sits ON the drum rather than under the frame: a Toy_glass drum inside a
    # 4 m-deep concrete frame renders as a black hole by day.
    cylinder("eq_glow", EQ_U, EQ_V, EQ_DRUM_R + 0.12, EQ_DRUM_HI - EQ_GLOW_H,
             EQ_DRUM_HI, EQ_DRUM_SEG, "Toy_gold_Glow")
    cylinder("eq_drum_cap", EQ_U, EQ_V, EQ_DRUM_R + 0.45, EQ_DRUM_HI,
             EQ_DRUM_HI + 0.7, EQ_DRUM_SEG, "Toy_trim")
    su, sv, z0, z1 = EQ_F1
    frame_ring("eq_frame1", EQ_U, EQ_V, su, sv, z0, z1, EQ_FRAME_T, "Toy_trim")
    su, sv, z0, z1 = EQ_F2
    frame_ring("eq_frame2", EQ_U, EQ_V, su, sv, z0, z1, EQ_FRAME_T, "Toy_trim")


# ----------------------------------------------------------------- finishing


def measure():
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    mn = [1e9] * 3
    mx = [-1e9] * 3
    tris = 0
    for ob in MESHES:
        ev = ob.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for v in me.vertices:
            w = ob.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
        ev.to_mesh_clear()
    return mn, mx, tris


def finish(out_dir):
    for ob in MESHES:
        m = ob.modifiers.new("Bevel", "BEVEL")
        m.width = BEVEL
        m.segments = BEVEL_SEG
        m.limit_method = "ANGLE"
        m.angle_limit = math.radians(35)

    mn, mx, _ = measure()
    scale = H_TOP / (mx[2] - mn[2])
    cx, cy = (mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2
    for ob in MESHES:
        ob.location = (
            (ob.location.x - cx) * scale,
            (ob.location.y - cy) * scale,
            (ob.location.z - mn[2]) * scale,
        )
        ob.scale = (scale, scale, scale)
    bpy.context.view_layer.update()
    bpy.ops.object.select_all(action="DESELECT")
    for ob in MESHES:
        ob.select_set(True)
    bpy.context.view_layer.objects.active = MESHES[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    mn, mx, tris = measure()
    print("OBJECTS %d  TRIS %d" % (len(MESHES), tris))
    print("DIMS %.3f x %.3f x %.3f" % tuple(mx[i] - mn[i] for i in range(3)))
    print("MINZ %.4f  MAXZ %.4f  CENTER %.4f %.4f"
          % (mn[2], mx[2], (mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2))

    os.makedirs(out_dir, exist_ok=True)
    blend = os.path.join(out_dir, "hyatt-regency.blend")
    glb = os.path.join(out_dir, "hyatt-regency.glb")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    bpy.ops.object.select_all(action="DESELECT")
    for ob in MESHES:
        ob.select_set(True)
    bpy.ops.export_scene.gltf(
        filepath=glb,
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_cameras=False,
        export_lights=False,
        export_animations=False,
    )
    print("WROTE", glb)


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    build()
    finish(out)


main()
