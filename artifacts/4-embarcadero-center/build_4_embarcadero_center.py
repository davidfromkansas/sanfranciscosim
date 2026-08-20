"""Deterministic Blender build of the SF-SIM miniature Four Embarcadero Center.

    blender -b --python build_4_embarcadero_center.py -- [--out DIR]

Writes 4-embarcadero-center.blend and 4-embarcadero-center.glb next to this file
(or into --out). Geometry is authored directly in world space in metres, Z up,
+X east, +Y north, so the model drops into the city at its real-world heading —
the loader applies no rotation. Origin = the OSM way/616812910 oriented-bounding-
box centre (anchor lon -122.3961998, lat 37.7953001), min Z = 0, crest exactly
179.00 m.

Design (see REFERENCE.md for the sources behind every number, and REPORT.md for
the corrections this build made to the plan):

* 63.46 x 37.34 m plan, long axis bearing 81.09 deg true (the Financial District
  grid).  Long faces look NORTH onto Clay Street / Sue Bierman Park and SOUTH
  into the Embarcadero Center podium plaza; the short ends look EAST toward the
  Ferry Building and WEST toward Drumm Street;
* 45 storeys, main parapet 173.70 m (CTBUH architectural top, 570 ft), rooftop
  cooling-tower crest 179.00 m (DataSF LiDAR hgt_max 179.05 m).  3.86 m
  floor-to-floor;
* the recognition feature: John King's "blunt cliff when viewed from north or
  south, spiked outcrops from east or west".  The slab is flat-topped at 173.70
  over the middle 43.4 m of its length; in the outer 10 m at EACH end it splits
  into six north-south fins whose tops step DOWN away from a central spine
  (173.70 / 154.40 / 135.10) and whose plan projections step BACK from that same
  spine.  Both moves are measured off the OSM polygon (see STRIPS);
* the north-west corner is chopped back 5.5 m where the tower meets Clay and
  Drumm;
* warm off-white precast, not glass: a pale body with a fine grain of dark
  punched-window slots and pale piers.  Colour is the second recognition cue —
  this is an opaque cream tower in a district of dark glass;
* roof: a pale deck with a raised north curb carrying four large circular
  cooling towers in a row (Google satellite z20), one penthouse box and a
  window-washing davit track.  The two lower end tiers get their own decks and
  parapets, so the crown reads from above as well as from the side;
* night state: the top three modules glow as three descending crown rings — the
  daytime silhouette is the night silhouette — plus a seeded scatter of lit
  windows, the Clay Street lobby band, and one aviation bead on the spine.
  Glow surfaces are thin shells proud of the opaque glazing (the app renders
  _Glow in a separate layer — never author a primary surface as glow).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

BEARING = 81.09                       # long-axis bearing, deg true
_TH = math.radians(90.0 - BEARING)    # +8.91 deg CCW from +X
_C, _S = math.cos(_TH), math.sin(_TH)

# Heights ------------------------------------------------------------------
Z_PLINTH = 2.00        # Embarcadero Center podium deck under the tower
Z_BASE_TOP = 12.00     # top of the base band / bottom of the facade grid
Z_T1 = 135.10          # outer fins (strips 1 and 6)      = 173.70 - 10 floors
Z_T2 = 154.40          # middle fins (strips 2 and 5)     = 173.70 -  5 floors
Z_TOP = 173.70         # main parapet, CTBUH architectural top
Z_DECK = 172.50        # roof slab under the parapet
Z_CREST = 179.00       # cooling-tower crest = bbox top
FLOOR = 173.70 / 45.0  # 3.86 m

PARAPET = Z_TOP - Z_DECK   # 1.20 m

# Plan ---------------------------------------------------------------------
# (u, v) frame: u along the long axis (+u EAST-ish), v across it (+v SOUTH).
V_N = -18.65           # north face
V_S = +18.65           # south face
U_END_E = +21.70       # where the east end zone starts
U_END_W = -21.70       # where the west end zone starts

# Six north-south strips, measured off OSM way/616812910.
#   (v0, v1, u_east, u_west, top_z)
# The east values are the measured ones.  The west end is genuinely shallower
# (its spine is strip 3, and the measured plan runs flush at -30.20 across
# strips 4/5/6); strips 5 and 6 are recessed to -29.40 / -28.60 so the west end
# tapers like the east one instead of reading as a flat wall.  The overall
# -31.72 .. +31.73 length is untouched.
STRIPS = (
    (V_N,   -13.29, 26.84, -24.46, Z_T1),   # 1  north corner, chopped NW
    (-13.29, -6.30, 28.65, -30.01, Z_T2),   # 2
    (-6.30,  -1.00, 29.28, -31.72, Z_TOP),  # 3  spine (west's furthest)
    (-1.00,  +4.89, 31.73, -30.20, Z_TOP),  # 4  spine (east's furthest)
    (+4.89, +11.20, 28.98, -29.40, Z_T2),   # 5
    (+11.20, V_S,   26.52, -28.60, Z_T1),   # 6  south corner
)

N_PIER_LONG = 20       # window modules per long face
N_SLOT_ROWS = 7        # stacked segments per module: a ~5-storey horizontal beat
SLOT_GAP = 0.90        # pale spandrel between segments
SLOT_DEPTH = 0.10      # dark slot boxes sit just proud of the body
GLOW_PROUD = 0.06      # glow shells sit proud of the slot

PLINTH_HALF_U = 34.0
PLINTH_HALF_V = 21.0

PALETTE_HEX = {
    "Toy_sand": "ece4d4",         # the precast body — the primary colour
    "Toy_cream": "f2ede3",        # piers, parapets, base band (a half-step lighter)
    "Toy_trim": "f3efe6",         # horizontal trim bands
    "Toy_glass": "2a4d73",        # dark punched-window slots
    "Toy_stone": "d9d2c2",        # podium plinth
    "Toy_steel": "9aa0a6",        # roof decks, cooling towers, curbs
    "Toy_ink": "3a3530",          # cooling-tower grille discs, davit
    "Toy_glassl_Glow": "6f95b8",  # lit windows and the crown rings at night
    "Toy_red_Glow": "c4453c",     # aviation obstruction bead
}
# Toy_roofd is deliberately absent: it renders near-black on a horizontal deck
# under the app's lighting and would kill the pale-tower read.  Toy_steel is the
# roof material here.


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


# --------------------------------------------------------------- 2D helpers


def uv(u, v):
    """Building (u, v) -> world (X east, Y north), long axis at BEARING."""
    return (u * _C + v * _S, u * _S - v * _C)


def ccw(poly):
    a = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        a += x1 * y2 - x2 * y1
    return poly if a > 0 else poly[::-1]


def footprint_poly(u_west_of, u_east_of, v0=V_N, v1=V_S):
    """The staircase footprint between two per-strip u limits (callables)."""
    pts = []
    for (a, b, ue, uw, _t) in STRIPS:                       # east side, N -> S
        if b <= v0 or a >= v1:
            continue
        lo, hi = max(a, v0), min(b, v1)
        u = u_east_of(ue)
        pts.append((u, lo))
        pts.append((u, hi))
    for (a, b, ue, uw, _t) in reversed(STRIPS):             # west side, S -> N
        if b <= v0 or a >= v1:
            continue
        lo, hi = max(a, v0), min(b, v1)
        u = u_west_of(uw)
        pts.append((u, hi))
        pts.append((u, lo))
    out = []
    for p in pts:                                            # drop collinear dupes
        if not out or abs(out[-1][0] - p[0]) > 1e-6 or abs(out[-1][1] - p[1]) > 1e-6:
            out.append(p)
    if len(out) > 1 and out[0] == out[-1]:
        out.pop()
    return ccw([uv(u, v) for u, v in out])


def rect_uv(u0, u1, v0, v1):
    return ccw([uv(u0, v0), uv(u1, v0), uv(u1, v1), uv(u0, v1)])


def offset_polygon(poly, d):
    """Miter offset of a CCW polygon; positive d moves outward."""
    n = len(poly)
    normals = []
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1.0
        normals.append((dy / length, -dx / length))
    out = []
    for i in range(n):
        n1, n2 = normals[i - 1], normals[i]
        v = poly[i]
        det = n1[0] * n2[1] - n1[1] * n2[0]
        if abs(det) < 1e-6:
            out.append((v[0] + n2[0] * d, v[1] + n2[1] * d))
            continue
        c1 = v[0] * n1[0] + v[1] * n1[1] + d
        c2 = v[0] * n2[0] + v[1] * n2[1] + d
        out.append(((c1 * n2[1] - c2 * n1[1]) / det, (c2 * n1[0] - c1 * n2[0]) / det))
    return out


# -------------------------------------------------------------- mesh helpers


def new_mesh(name, verts, faces, materials, face_mats=None):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(v) for v in verts], [], faces)
    for m in materials:
        mesh.materials.append(m)
    if face_mats:
        for poly, mi in zip(mesh.polygons, face_mats):
            poly.material_index = mi
    mesh.validate()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.shade_flat()
    return obj


def bevel(obj, width=0.12, segments=2):
    thin = min((d for d in obj.dimensions if d > 1e-6), default=width)
    offset = min(width, thin * 0.30)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.bevel(
        bm,
        geom=list(bm.verts) + list(bm.edges),
        offset=offset,
        segments=segments,
        profile=0.5,
        affect="EDGES",
        clamp_overlap=True,
    )
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-4)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-4, edges=list(bm.edges))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def prism(name, poly, z0, z1, mat, mat_caps=None):
    n = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    mats = [mat]
    cap = mat_caps or mat
    if cap not in mats:
        mats.append(cap)
    faces, face_mats = [], []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
        face_mats.append(0)
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    face_mats += [mats.index(cap)] * 2
    return new_mesh(name, verts, faces, mats, face_mats)


def ring_band(name, poly, z0, z1, off_in, off_out, mat):
    lo_in = offset_polygon(poly, off_in)
    lo_out = offset_polygon(poly, off_out)
    n = len(lo_in)
    verts = []
    for loop, z in ((lo_in, z0), (lo_out, z0), (lo_out, z1), (lo_in, z1)):
        verts.extend([(x, y, z) for x, y in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * n, ((k + 1) % 4) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])


def uv_box(name, u0, u1, v0, v1, z0, z1, mat, mat_caps=None):
    return prism(name, rect_uv(u0, u1, v0, v1), z0, z1, mat, mat_caps)


def uv_cyl(name, u, v, z0, z1, r, sides, mat, mat_caps=None):
    poly = ccw([uv(u + r * math.cos(2 * math.pi * i / sides),
                   v + r * math.sin(2 * math.pi * i / sides)) for i in range(sides)])
    return prism(name, poly, z0, z1, mat, mat_caps)


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
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


def slot_rows(z0, z1):
    """Split a full-height window module into N_SLOT_ROWS stacked panes."""
    span = (z1 - z0 - (N_SLOT_ROWS - 1) * SLOT_GAP) / N_SLOT_ROWS
    if span <= 0.4:
        return [(z0, z1)]
    return [(z0 + i * (span + SLOT_GAP), z0 + i * (span + SLOT_GAP) + span)
            for i in range(N_SLOT_ROWS)]


# --------------------------------------------------------------- lit pattern

def lit(i):
    """Deterministic ~1-in-3 lit-window pattern (a fixed LCG, never random)."""
    x = (i * 1103515245 + 12345) & 0x7FFFFFFF
    return (x >> 7) % 3 == 0


# --------------------------------------------------------------------- build


def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.objects):
        for item in list(coll):
            coll.remove(item)


def build():
    clear()
    scene = bpy.context.scene
    m = {k: material(k) for k in PALETTE_HEX}

    core_lo = footprint_poly(lambda uw: U_END_W, lambda ue: U_END_E)

    # 1 -- podium plinth (the Embarcadero Center deck the tower stands on)
    pl = [(-PLINTH_HALF_U, -PLINTH_HALF_V + 4.0), (-PLINTH_HALF_U + 4.0, -PLINTH_HALF_V),
          (PLINTH_HALF_U, -PLINTH_HALF_V), (PLINTH_HALF_U, PLINTH_HALF_V),
          (-PLINTH_HALF_U, PLINTH_HALF_V)]
    prism("plinth", ccw([uv(u, v) for u, v in pl]), 0.0, Z_PLINTH,
          m["Toy_stone"], m["Toy_stone"])

    # 2 -- base band, full staircase footprint, one storey band + Clay St lobby
    full = footprint_poly(lambda uw: uw, lambda ue: ue)
    prism("base", full, Z_PLINTH, Z_BASE_TOP, m["Toy_cream"], m["Toy_cream"])
    uv_box("lobby", -14.0, 14.0, V_N - 0.34, V_N, 3.0, 9.0, m["Toy_glass"])
    uv_box("lobby_glow", -13.4, 13.4, V_N - 0.42, V_N - 0.30, 3.3, 8.6,
           m["Toy_glassl_Glow"])

    # 3 -- the slab core: flat-topped over the middle 43.4 m
    prism("core", core_lo, Z_BASE_TOP, Z_DECK, m["Toy_sand"], m["Toy_steel"])

    # 4 -- the two end zones: six fins each, stepping down and back
    for si, (v0, v1, ue, uw, top) in enumerate(STRIPS):
        for side, (ua, ub) in (("e", (U_END_E, ue)), ("w", (uw, U_END_W))):
            deck = top - PARAPET
            prism(f"fin_{side}{si}", rect_uv(ua, ub, v0, v1), Z_BASE_TOP, deck,
                  m["Toy_sand"], m["Toy_steel"])
            ring_band(f"fincap_{side}{si}", rect_uv(ua, ub, v0, v1), deck, top,
                      -0.65, 0.0, m["Toy_cream"])

    # 5 -- parapet on the core roof, and the trim band at the base of the grid
    ring_band("parapet", core_lo, Z_DECK, Z_TOP, -0.65, 0.0, m["Toy_cream"])
    ring_band("trim_base", full, Z_BASE_TOP - 0.60, Z_BASE_TOP, -0.20, 0.28,
              m["Toy_trim"])

    # 6 -- facade grain: dark window modules, stacked panes, over every face.
    #      The top two panes of every module are also glow shells, so the crown
    #      lights up as three descending rings at night without putting a
    #      day-visible band across the tower.
    idx = 0
    pitch = (2.0 * U_END_E) / N_PIER_LONG

    def module(tag, box, z_top):
        """One window module: N_SLOT_ROWS stacked panes + its glow shells."""
        nonlocal idx
        rows = slot_rows(Z_BASE_TOP + 0.8, z_top - 1.2)
        on = lit(idx)
        for r, (za, zb) in enumerate(rows):
            box(f"win_{tag}_{r}", za, zb, False)
            if r == len(rows) - 1:                      # the crown ring
                box(f"winglow_{tag}_{r}", zb - (zb - za) * 0.40, zb - 0.18, True)
            elif on and lit(idx * 17 + r):
                box(f"winglow_{tag}_{r}", za + 0.18, zb - 0.18, True)
        idx += 1

    # long faces: they run the FULL length, and drop to the outer fin's top
    # beyond the end-zone line (the north face is strip 1, the south strip 6)
    for face, vf, sgn, si in (("n", V_N, -1.0, 0), ("s", V_S, +1.0, 5)):
        _v0, _v1, ue, uw, tp = STRIPS[si]
        count = int((ue - uw) / pitch)
        start = uw + ((ue - uw) - count * pitch) / 2.0
        for i in range(count):
            uc = start + (i + 0.5) * pitch
            w = pitch * 0.52
            z_top = Z_DECK if abs(uc) + w / 2 <= U_END_E else tp - PARAPET

            def box(name, za, zb, glow, uc=uc, w=w, vf=vf, sgn=sgn):
                if glow:
                    uv_box(name, uc - w / 2 + 0.22, uc + w / 2 - 0.22,
                           vf + sgn * SLOT_DEPTH, vf + sgn * (SLOT_DEPTH + GLOW_PROUD),
                           za, zb, m["Toy_glassl_Glow"])
                else:
                    uv_box(name, uc - w / 2, uc + w / 2,
                           vf + sgn * 0.0, vf + sgn * SLOT_DEPTH, za, zb, m["Toy_glass"])

            module(f"{face}{i}", box, z_top)

    # fin end faces — this is where the chevron is read from
    for si, (v0, v1, ue, uw, top) in enumerate(STRIPS):
        for side, uf, sgn in (("e", ue, +1.0), ("w", uw, -1.0)):
            nslot = 2 if (v1 - v0) < 6.5 else 3
            fw = (v1 - v0) / nslot
            for i in range(nslot):
                vc = v0 + (i + 0.5) * fw
                w = fw * 0.52

                def box(name, za, zb, glow, uf=uf, sgn=sgn, vc=vc, w=w):
                    if glow:
                        uv_box(name, uf + sgn * SLOT_DEPTH,
                               uf + sgn * (SLOT_DEPTH + GLOW_PROUD),
                               vc - w / 2 + 0.22, vc + w / 2 - 0.22, za, zb,
                               m["Toy_glassl_Glow"])
                    else:
                        uv_box(name, uf + sgn * 0.0, uf + sgn * SLOT_DEPTH,
                               vc - w / 2, vc + w / 2, za, zb, m["Toy_glass"])

                module(f"{side}{si}_{i}", box, top - PARAPET)

    # the core's own end faces, where the lower fins leave them exposed
    for si, (v0, v1, ue, uw, top) in enumerate(STRIPS):
        if top >= Z_TOP:
            continue
        for side, uf, sgn in (("e", U_END_E, +1.0), ("w", U_END_W, -1.0)):
            nslot = 2 if (v1 - v0) < 6.5 else 3
            fw = (v1 - v0) / nslot
            for i in range(nslot):
                vc = v0 + (i + 0.5) * fw
                w = fw * 0.52
                rows = slot_rows(top + 1.0, Z_DECK - 1.2)
                on = lit(idx)
                for r, (za, zb) in enumerate(rows):
                    uv_box(f"win_c{side}{si}_{i}_{r}",
                           uf + sgn * 0.0, uf + sgn * SLOT_DEPTH,
                           vc - w / 2, vc + w / 2, za, zb, m["Toy_glass"])
                    crown = r == len(rows) - 1
                    if crown or (on and lit(idx * 17 + r)):
                        g0 = zb - (zb - za) * 0.40 if crown else za + 0.18
                        uv_box(f"winglow_c{side}{si}_{i}_{r}",
                               uf + sgn * SLOT_DEPTH,
                               uf + sgn * (SLOT_DEPTH + GLOW_PROUD),
                               vc - w / 2 + 0.22, vc + w / 2 - 0.22,
                               g0, zb - 0.18, m["Toy_glassl_Glow"])
                idx += 1

    # 8 -- roof plant on the main deck: the four cooling towers, north half
    uv_box("plant_curb", -13.5, 13.5, -13.0, -5.0, Z_DECK, Z_DECK + 1.20,
           m["Toy_steel"], m["Toy_steel"])
    for i in range(4):
        u = -9.6 + i * 6.4
        uv_cyl(f"cooler{i}", u, -9.0, Z_DECK + 1.20, Z_CREST - 0.35, 2.60, 14,
               m["Toy_steel"], m["Toy_steel"])
        uv_cyl(f"coolergrille{i}", u, -9.0, Z_CREST - 0.35, Z_CREST, 2.15, 14,
               m["Toy_ink"], m["Toy_ink"])
    uv_box("penthouse", 4.0, 13.0, 1.0, 7.0, Z_DECK, Z_DECK + 3.50,
           m["Toy_steel"], m["Toy_steel"])
    uv_box("davit", -14.0, 14.0, 11.6, 12.2, Z_DECK, Z_DECK + 0.45,
           m["Toy_ink"], m["Toy_ink"])
    uv_cyl("beacon", 20.0, 1.9, Z_TOP, Z_TOP + 0.9, 0.55, 8,
           material("Toy_red_Glow"), material("Toy_red_Glow"))

    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.startswith(("win", "crown_")):
            continue      # flat recessed panes: crisp edges, 12 tris each
        if obj.name.startswith(("davit", "beacon", "coolergrille")):
            bevel(obj, width=0.05, segments=1)
        elif obj.name.startswith(("trim_", "fincap", "parapet")):
            bevel(obj, width=0.10, segments=1)
        elif obj.name.startswith(("cooler", "penthouse", "plant_")):
            bevel(obj, width=0.10, segments=2)
        else:
            bevel(obj, width=0.14, segments=2)

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
        o.evaluated_get(dg).to_mesh_clear()
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    print("[build] anchor lon/lat: -122.3961998 37.7953001 (OSM way/616812910 OBB centre)")
    print(f"[build] long-axis bearing: {BEARING} deg true; entrance faces NORTH (55 Clay St)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "4-embarcadero-center.blend")
    glb = os.path.join(out, "4-embarcadero-center.glb")
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
