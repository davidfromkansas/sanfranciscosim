"""Deterministic Blender build of the SF-SIM miniature 505 Van Ness Avenue
(Governor Edmund G. "Pat" Brown Building — California Public Utilities
Commission headquarters, San Francisco Civic Center).

    blender -b --python build_505_van_ness.py -- [--out DIR]

Writes 505-van-ness.blend and 505-van-ness.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = footprint ring bbox centre (anchor lon
-122.4212915, lat 37.7804835), min Z = 0, crest normalized to exactly 27.0 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured OSM relation/1735766 outer ring, closed-ring Douglas-Peucker
  simplified at 0.6 m to 18 vertices (area within 0.2% of the survey), with the
  south-east arc refitted to a circle and resampled to 14 segments — that arc
  is the building's whole silhouette and deserves a real curve;
* an L-shaped six-storey government block: a 106 m northern bar plus a southern
  wing along Van Ness, wrapped around a 36 m interior light court;
* the identity feature: the great bowed drum front addressing the Van Ness /
  McAllister corner, with a deep recessed central bay carrying an oversized
  Great Seal of California and the incised STATE OF CALIFORNIA lintel;
* the facade system: heavy rounded precast piers at ~8 m centres standing proud
  of six recessed ribbons of blue glazing — the pier projection, not a modelled
  reveal, is what makes the ribbons read as recessed;
* the plaza, which is half this building's identity: concentric curved steps
  sweeping down from the entrance, two cylindrical drum pedestals, two flagpoles;
* a dark red-brown fascia lid over the whole parapet — the one dark element in
  an otherwise pale composition, and what gives the silhouette its cap;
* night state: a restrained scatter of lit ribbon panels, the entrance soffit,
  and the seal ring as the hero. Glow surfaces are thin shells proud of the
  opaque glazing (the app renders _Glow in a separate layer that is ~12% alpha
  by day — never author a primary surface as glow);
* a designed roof for the app's downward camera: the open court with its
  faceted glazed stair tower, a mechanical row on the north bar, a skylight
  field, and the stair penthouse that sets the 27.0 m crest.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM relation/1735766 outer ring, projected with the app's tangent projection
# and recentred on the ring bbox centre. CCW (outward normal = (t.y, -t.x)).
# Indices ARC_I0..ARC_I1 inclusive are the bowed south-east front.
RING_RAW = [
    (-56.71, 26.04),
    (-52.84, -0.05),
    (-13.69, 5.70),
    (-5.33, -46.70),
    (-3.92, -46.48),
    (-4.18, -44.49),
    (15.79, -41.28),
    (15.44, -38.52),   # ARC start
    (30.75, -33.77),
    (39.99, -27.80),
    (43.60, -24.48),
    (50.20, -15.64),
    (55.65, -1.71),
    (56.71, 6.36),
    (55.83, 16.53),    # ARC end
    (50.82, 46.71),
    (-53.72, 29.68),
    (-56.10, 27.80),
]
ARC_I0, ARC_I1 = 7, 14
ARC_SEGMENTS = 14

# Interior light court, from the OSM inner ring bbox (39.3 x 39.1 m) pulled in
# to a designed 36 m octagon so the surrounding wings keep a believable depth.
COURT_C = (20.0, 1.5)
COURT_R = 18.0
COURT_CHAMFER = 0.42   # fraction that turns the square into a chamfered octagon

Z_PLINTH = 2.0       # top of the raised plaza podium / ground-floor datum
Z_DECK = 24.5        # roof deck, top of the precast body
Z_FASCIA1 = 26.2     # top of the dark fascia lid
Z_PARAPET = 26.5     # stone coping over the fascia
Z_CREST = 27.0       # stair-penthouse top -> the normalized bbox top

FLOORS = 6
FLOOR_H = (Z_DECK - Z_PLINTH) / FLOORS   # 3.75 m
WIN_Z0, WIN_Z1 = 1.15, 2.60              # ribbon within each floor band

D_GLASS = 0.06       # glazing sits just proud of the wall (no z-fighting)
D_PIER = 0.75        # piers stand well proud -> the ribbons read as recessed
PIER_W = 2.7
PIER_SPACING = 8.5

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",   # precast concrete: piers, spandrels, plinth, stair
    "Toy_trim": "f3efe6",    # coping, lintel band, pier caps
    "Toy_glass": "2a4d73",   # the blue ribbon glazing
    "Toy_glassl": "6f95b8",  # court glazing, skylights
    "Toy_sky": "6db3d9",     # the seal's field
    "Toy_gold": "caa64a",    # seal rim, court spandrel banding
    "Toy_rust": "a86444",    # the dark red-brown fascia lid
    "Toy_roofd": "45454a",   # roof deck, penthouses
    "Toy_steel": "9aa0a6",   # mechanical, flagpoles
    "Toy_ink": "3a3530",     # recessed-bay shadow
    "Toy_glass_Glow": "6f95b8",
    "Toy_trim_Glow": "f3efe6",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


# --------------------------------------------------------------- 2D helpers


def fit_circle(pts):
    """Least-squares circle through pts -> (cx, cy, r)."""
    n = len(pts)
    sx = sum(p[0] for p in pts)
    sy = sum(p[1] for p in pts)
    sxx = sum(p[0] * p[0] for p in pts)
    syy = sum(p[1] * p[1] for p in pts)
    sxy = sum(p[0] * p[1] for p in pts)
    sxz = sum(p[0] * (p[0] ** 2 + p[1] ** 2) for p in pts)
    syz = sum(p[1] * (p[0] ** 2 + p[1] ** 2) for p in pts)
    sz = sum(p[0] ** 2 + p[1] ** 2 for p in pts)
    a = [[sxx, sxy, sx], [sxy, syy, sy], [sx, sy, float(n)]]
    b = [sxz, syz, sz]
    # 3x3 Gaussian elimination
    for i in range(3):
        p = max(range(i, 3), key=lambda r: abs(a[r][i]))
        a[i], a[p] = a[p], a[i]
        b[i], b[p] = b[p], b[i]
        for r in range(i + 1, 3):
            f = a[r][i] / a[i][i]
            for c in range(i, 3):
                a[r][c] -= f * a[i][c]
            b[r] -= f * b[i]
    x = [0.0] * 3
    for i in (2, 1, 0):
        x[i] = (b[i] - sum(a[i][c] * x[c] for c in range(i + 1, 3))) / a[i][i]
    cx, cy = x[0] / 2.0, x[1] / 2.0
    r = math.sqrt(max(x[2] + cx * cx + cy * cy, 1e-9))
    return cx, cy, r


def build_ring():
    """RING_RAW with its south-east arc refitted and resampled."""
    arc = RING_RAW[ARC_I0 : ARC_I1 + 1]
    cx, cy, r = fit_circle(arc)
    a0 = math.atan2(arc[0][1] - cy, arc[0][0] - cx)
    a1 = math.atan2(arc[-1][1] - cy, arc[-1][0] - cx)
    while a1 < a0:
        a1 += 2 * math.pi
    resampled = [
        (cx + r * math.cos(a0 + (a1 - a0) * k / ARC_SEGMENTS),
         cy + r * math.sin(a0 + (a1 - a0) * k / ARC_SEGMENTS))
        for k in range(ARC_SEGMENTS + 1)
    ]
    ring = RING_RAW[:ARC_I0] + resampled + RING_RAW[ARC_I1 + 1 :]
    return ring, (cx, cy, r, a0, a1)


RING, ARC_FIT = build_ring()


def court_ring():
    """Chamfered-octagon light court, CCW."""
    cx, cy = COURT_C
    a = COURT_R
    c = a * COURT_CHAMFER
    pts = [
        (a, c - a), (a, a - c), (a - c, a), (c - a, a),
        (-a, a - c), (-a, c - a), (c - a, -a), (a - c, -a),
    ]
    return [(cx + x, cy + y) for x, y in pts]


COURT = court_ring()


def point_in(poly, x, y):
    """Even-odd point-in-polygon — the guard that keeps roof props on the roof."""
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            if x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
                inside = not inside
    return inside


def on_roof(x, y, margin=3.0):
    """Inside the footprint, outside the light court, clear of both edges."""
    if not point_in(offset_polygon(RING, -margin), x, y):
        return False
    return not point_in(offset_polygon(COURT, margin), x, y)


def poly_edge(poly, i):
    """Edge i of poly: (origin, length, tangent unit, outward normal)."""
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    return a, length, t, (t[1], -t[0])


def offset_polygon(poly, d):
    """Miter offset of a CCW footprint; positive d moves outward."""
    npts = len(poly)
    normals = []
    for i in range(npts):
        a, b = poly[i], poly[(i + 1) % npts]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1.0
        normals.append((dy / length, -dx / length))
    out = []
    for i in range(npts):
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


def perimeter_points(poly, spacing, skip=()):
    """Walk the ring at `spacing` and yield (x, y, heading, edge_index, u)."""
    out = []
    for i in range(len(poly)):
        origin, length, t, n = poly_edge(poly, i)
        if i in skip or length < spacing * 0.55:
            continue
        count = max(1, int(round(length / spacing)))
        for k in range(count):
            u = length * (k + 0.5) / count
            out.append((origin[0] + t[0] * u, origin[1] + t[1] * u,
                        math.atan2(t[1], t[0]), i, u, n))
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
    """Miniature-style edge softening on the chunky solids (style bible s.4).

    Width is capped at a third of the object's thinnest dimension: a flat bevel
    on a thin applied panel relies entirely on clamp_overlap, which collapses
    opposing profiles into zero-area slivers. The remove_doubles /
    dissolve_degenerate pass sweeps up whatever clamping still pinches shut.
    """
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
    """Closed extrusion of a CCW polygon (walls + both caps)."""
    npts = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces, face_mats = [], []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
        face_mats.append(0)
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    face_mats += [1 if mat_caps else 0] * 2
    mats = [mat, mat_caps] if mat_caps else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def ring_band(name, poly, z0, z1, off_in, off_out, mat):
    """Closed band following a footprint: 4 loops, quads between."""
    lo_in = offset_polygon(poly, off_in)
    lo_out = offset_polygon(poly, off_out)
    npts = len(lo_in)
    verts = []
    for loop, z in ((lo_in, z0), (lo_out, z0), (lo_out, z1), (lo_in, z1)):
        verts.extend([(x, y, z) for x, y in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * npts, ((k + 1) % 4) * npts
        for i in range(npts):
            j = (i + 1) % npts
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0):
    """Box with local +x along yaw and local +y 90 deg ccw of it."""
    c, s = math.cos(yaw), math.sin(yaw)
    corners = []
    for lx, ly in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)):
        corners.append((cx + lx * c - ly * s, cy + lx * s + ly * c))
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4),
             (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_mesh(name, verts, faces, [mat])


def cylinder(name, cx, cy, z0, z1, r, mat, seg=12, r_top=None):
    rt = r if r_top is None else r_top
    lo = [(cx + r * math.cos(2 * math.pi * k / seg), cy + r * math.sin(2 * math.pi * k / seg))
          for k in range(seg)]
    hi = [(cx + rt * math.cos(2 * math.pi * k / seg), cy + rt * math.sin(2 * math.pi * k / seg))
          for k in range(seg)]
    verts = [(x, y, z0) for x, y in lo] + [(x, y, z1) for x, y in hi]
    faces = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i) for i in range(seg)]
    faces.append(tuple(range(seg - 1, -1, -1)))
    faces.append(tuple(range(seg, 2 * seg)))
    return new_mesh(name, verts, faces, [mat])


def arc_band(name, cx, cy, r_in, r_out, z0, z1, a0, a1, mat, seg=20):
    """Closed annular sector solid — the plaza steps and the seal rings."""
    ai = [(cx + r_in * math.cos(a0 + (a1 - a0) * k / seg),
           cy + r_in * math.sin(a0 + (a1 - a0) * k / seg)) for k in range(seg + 1)]
    ao = [(cx + r_out * math.cos(a0 + (a1 - a0) * k / seg),
           cy + r_out * math.sin(a0 + (a1 - a0) * k / seg)) for k in range(seg + 1)]
    poly = ai + ao[::-1]
    return prism(name, poly, z0, z1, mat)


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
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# --------------------------------------------------------------------- build


def entrance_frame():
    """Centre of the bowed front: the arc midpoint, and the outward direction
    there. Everything about the entrance hangs off this frame."""
    cx, cy, r, a0, a1 = ARC_FIT
    am = (a0 + a1) / 2.0
    n = (math.cos(am), math.sin(am))          # outward from the drum centre
    t = (-math.sin(am), math.cos(am))         # along the arc
    p = (cx + r * math.cos(am), cy + r * math.sin(am))
    return p, t, n, (cx, cy, r, am)


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    stone = material("Toy_stone")
    trim = material("Toy_trim")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    sky = material("Toy_sky")
    gold = material("Toy_gold")
    rust = material("Toy_rust")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    ink = material("Toy_ink")
    gglow = material("Toy_glass_Glow")
    tglow = material("Toy_trim_Glow")

    # --- the precast body, and the court cut out of it ----------------------
    body = prism("body", RING, 0.0, Z_DECK, stone, mat_caps=roofd)
    cutter = prism("court_cutter", COURT, -2.0, Z_DECK + 2.0, stone)
    mod = body.modifiers.new("court", "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.solver = "EXACT"
    mod.object = cutter
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.modifier_apply(modifier="court")
    bpy.data.objects.remove(cutter, do_unlink=True)
    bm = bmesh.new()
    bm.from_mesh(body.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(body.data)
    bm.free()

    prism("court_floor", offset_polygon(COURT, -0.03), 0.0, 1.1, stone, mat_caps=stone)

    # --- six recessed ribbons of blue glazing, outside and in ---------------
    # Unbevelled on purpose: these are 60 mm shells, and a bevel on them buys
    # nothing at the app's camera while tripling their triangle cost.
    for f in range(FLOORS):
        z = Z_PLINTH + f * FLOOR_H
        ring_band(f"ribbon{f}", RING, z + WIN_Z0, z + WIN_Z1, 0.0, D_GLASS, glass)
        ring_band(f"court_ribbon{f}", COURT, z + WIN_Z0, z + WIN_Z1,
                  -D_GLASS, 0.0, glassl)
        # the court's warm spandrel banding, the one place this building is warm
        ring_band(f"court_band{f}", COURT, z + WIN_Z1, z + WIN_Z1 + 0.55,
                  -0.10, 0.0, gold)

    # --- the pier order: what makes the ribbons read as recessed ------------
    piers = perimeter_points(RING, PIER_SPACING)
    for i, (px, py, heading, _e, _u, _n) in enumerate(piers):
        p = box(f"pier{i}", px, py, Z_PLINTH - 0.4, Z_DECK, PIER_W, D_PIER * 2.0,
                stone, yaw=heading)
        p.location = Vector((0, 0, 0))
        bevel(p, width=0.14, segments=1)
    # One continuous trim band caps every pier at once: 49 individual cap boxes
    # cost 5,292 triangles and read identically from the app's camera.
    ring_band("pier_capband", RING, Z_DECK - 0.38, Z_DECK, 0.0, D_PIER + 0.10, trim)

    # --- ground-floor plinth band, all the way round ------------------------
    ring_band("plinth", RING, 0.0, Z_PLINTH + 0.55, 0.0, 0.42, stone)

    # --- the dark fascia lid + stone coping ---------------------------------
    ring_band("fascia", RING, Z_DECK, Z_FASCIA1, 0.0, 0.72, rust)
    ring_band("coping", RING, Z_FASCIA1, Z_PARAPET, -0.10, 0.82, trim)
    ring_band("court_coping", COURT, Z_DECK, Z_DECK + 0.55, -0.55, 0.0, trim)

    # --- the recessed entrance bay and the Great Seal ------------------------
    (ex, ey), et, en, (dcx, dcy, dr, am) = entrance_frame()
    bay_w = 11.5
    yaw = math.atan2(et[1], et[0])
    # the deep shadowed slot
    box("bay_shadow", ex - en[0] * 1.1, ey - en[1] * 1.1, Z_PLINTH, Z_DECK - 1.2,
        bay_w, 2.6, ink, yaw=yaw)
    # the lintel band carrying STATE OF CALIFORNIA
    box("bay_lintel", ex + en[0] * 0.15, ey + en[1] * 0.15,
        Z_PLINTH + 2.9, Z_PLINTH + 4.6, bay_w + 1.4, 1.5, trim, yaw=yaw)
    box("bay_lintel_glow", ex + en[0] * 0.62, ey + en[1] * 0.62,
        Z_PLINTH + 3.3, Z_PLINTH + 3.9, bay_w - 1.0, 0.30, tglow, yaw=yaw)
    # the entrance soffit, lit at night
    box("bay_soffit", ex + en[0] * 0.30, ey + en[1] * 0.30,
        Z_PLINTH - 0.05, Z_PLINTH + 2.9, bay_w - 3.0, 1.1, ink, yaw=yaw)
    box("bay_soffit_glow", ex + en[0] * 0.72, ey + en[1] * 0.72,
        Z_PLINTH + 0.3, Z_PLINTH + 2.6, bay_w - 5.2, 0.26, tglow, yaw=yaw)

    # The seal: semantic exaggeration (style bible s.8/s.9). ~8 m across, so it
    # still reads from the app's aerial camera; the real medallion is ~4 m.
    sx = ex + en[0] * 0.55
    sy = ey + en[1] * 0.55
    seal_z = Z_PLINTH + 12.2
    for tag, r0, r1, zt, m in (
        ("rim", 3.6, 4.1, 0.55, gold),
        ("field", 0.0, 3.6, 0.40, sky),
    ):
        c, s = math.cos(yaw), math.sin(yaw)
        seg = 14
        pts = []
        for k in range(seg):
            a = 2 * math.pi * k / seg
            lx, lz = r1 * math.cos(a), r1 * math.sin(a)
            pts.append((lx, lz))
        inner = [(r0 * math.cos(2 * math.pi * k / seg), r0 * math.sin(2 * math.pi * k / seg))
                 for k in range(seg)] if r0 > 0 else None
        loops = [pts] if inner is None else [inner, pts[::-1]]
        poly2d = loops[0] if inner is None else inner + pts[::-1]
        verts, faces = [], []
        n2 = len(poly2d)
        for d in (0.0, zt):
            for lx, lz in poly2d:
                verts.append((sx + lx * c + en[0] * d,
                              sy + lx * s + en[1] * d,
                              seal_z + lz))
        for i in range(n2):
            j = (i + 1) % n2
            faces.append((i, j, n2 + j, n2 + i))
        faces.append(tuple(range(n2 - 1, -1, -1)))
        faces.append(tuple(range(n2, 2 * n2)))
        new_mesh(f"seal_{tag}", verts, faces, [m])
    # The ring that carries the identity after dark. It must be an ANNULUS, not
    # a disc: the app drives the glow layer to opacity 0.12 + 0.95*uNight, so a
    # filled disc goes fully opaque white at night and erases the seal it is
    # supposed to announce. Ringing it keeps the blue field and gold rim legible.
    cseg = 14
    ring_in = [(3.30 * math.cos(2 * math.pi * k / cseg),
                3.30 * math.sin(2 * math.pi * k / cseg)) for k in range(cseg)]
    ring_out = [(4.05 * math.cos(2 * math.pi * k / cseg),
                 4.05 * math.sin(2 * math.pi * k / cseg)) for k in range(cseg)]
    poly2d = ring_in + ring_out[::-1]
    n2 = len(poly2d)
    verts, faces = [], []
    for d in (0.30, 0.62):
        for lx, lz in poly2d:
            verts.append((sx + lx * math.cos(yaw) + en[0] * d,
                          sy + lx * math.sin(yaw) + en[1] * d,
                          seal_z + lz))
    for i in range(n2):
        j = (i + 1) % n2
        faces.append((i, j, n2 + j, n2 + i))
    faces.append(tuple(range(n2 - 1, -1, -1)))
    faces.append(tuple(range(n2, 2 * n2)))
    new_mesh("seal_glow", verts, faces, [tglow])

    # --- the plaza: concentric curved steps, drums, flagpoles ---------------
    step_a0 = am - math.radians(19)
    step_a1 = am + math.radians(19)
    for k in range(7):
        r_in = dr + 2.0 + k * 1.5
        arc_band(f"step{k}", dcx, dcy, r_in, r_in + 1.7,
                 0.0, Z_PLINTH - k * (Z_PLINTH / 7.0), step_a0, step_a1, stone, seg=10)
    for side, sgn in (("n", 1), ("s", -1)):
        a = am + sgn * math.radians(23)
        px = dcx + (dr + 6.0) * math.cos(a)
        py = dcy + (dr + 6.0) * math.sin(a)
        cylinder(f"drum_{side}", px, py, 0.0, Z_PLINTH + 0.5, 2.7, stone, seg=12)
        cylinder(f"drumcap_{side}", px, py, Z_PLINTH + 0.5, Z_PLINTH + 1.0, 3.0,
                 trim, seg=12, r_top=2.4)
        fx = dcx + (dr + 1.2) * math.cos(a)
        fy = dcy + (dr + 1.2) * math.sin(a)
        cylinder(f"flagpole_{side}", fx, fy, Z_PLINTH, Z_PLINTH + 15.0, 0.34,
                 steel, seg=8)

    # --- the roof, which is the surface the app's camera sees most -----------
    # The court already gives the roof its big move; these clusters keep the
    # north bar from reading as an empty tray (style bible s.10).
    cylinder("court_tower", COURT_C[0], COURT_C[1], Z_PLINTH, Z_DECK + 1.4, 6.2,
             glassl, seg=8)
    cylinder("court_tower_cap", COURT_C[0], COURT_C[1], Z_DECK + 1.4, Z_DECK + 2.0,
             6.6, trim, seg=8)
    # Roof props are placed on positions DERIVED from the footprint, never
    # hand-typed: the north edge slopes 17 m across the building's 105 m, and
    # hand-picked coordinates put eight props out over the pavement in the
    # first pass. The grid is deterministic, so the build stays reproducible.
    candidates = []
    gx = -54.0
    while gx < 58.0:
        gy = -46.0
        while gy < 48.0:
            if on_roof(gx, gy, margin=5.5):
                candidates.append((round(gx, 2), round(gy, 2)))
            gy += 6.5
        gx += 6.5
    print(f"[build] roof candidates on deck: {len(candidates)}")

    def nearest(tx, ty):
        return min(candidates, key=lambda p: (p[0] - tx) ** 2 + (p[1] - ty) ** 2)

    px_, py_ = nearest(-34.0, 22.0)
    box("penthouse", px_, py_, Z_DECK, Z_CREST - 0.35, 11.0, 8.0, roofd)
    box("penthouse_cap", px_, py_, Z_CREST - 0.35, Z_CREST, 11.6, 8.6, trim)
    taken = {(px_, py_)}
    px_, py_ = nearest(26.0, 30.0)
    box("plantroom", px_, py_, Z_DECK, Z_DECK + 2.0, 13.0, 7.0, roofd)
    box("plantroom_cap", px_, py_, Z_DECK + 2.0, Z_DECK + 2.3, 13.6, 7.6, trim)
    taken.add((px_, py_))
    px_, py_ = nearest(4.0, -30.0)
    box("liftroom", px_, py_, Z_DECK, Z_DECK + 1.9, 7.0, 6.0, roofd)
    box("liftroom_cap", px_, py_, Z_DECK + 1.9, Z_DECK + 2.2, 7.6, 6.6, trim)
    taken.add((px_, py_))
    px_, py_ = nearest(-48.0, 12.0)
    box("roof_hatch", px_, py_, Z_DECK, Z_DECK + 0.6, 2.2, 1.8, roofd)
    taken.add((px_, py_))

    free = [p for p in candidates if p not in taken]
    for i, (bx, by) in enumerate(free):
        if i % 3 == 0:
            box(f"skylight_kerb{i}", bx, by, Z_DECK, Z_DECK + 0.28, 5.0, 3.4, trim)
            box(f"skylight{i}", bx, by, Z_DECK + 0.22, Z_DECK + 0.60, 4.5, 2.9, glassl)
        elif i % 7 == 1:
            h = 1.0 + 0.25 * (i % 4)
            box(f"hvac{i}", bx, by, Z_DECK, Z_DECK + h, 4.6, 3.8, steel)

    # --- night: a restrained scatter of lit ribbon panels --------------------
    # Thin shells proud of the opaque glazing, on the two photographed
    # elevations plus the court, never a primary surface.
    lit = perimeter_points(RING, PIER_SPACING)
    for i, (px, py, heading, _e, _u, _n) in enumerate(lit):
        if i % 3 != 1:
            continue
        for f in (1, 2, 4):
            z = Z_PLINTH + f * FLOOR_H
            box(f"lit{i}_{f}", px, py, z + WIN_Z0 + 0.35, z + WIN_Z1 - 0.35,
                PIER_SPACING - PIER_W - 1.6, D_GLASS * 2 + 0.14, gglow, yaw=heading)

    # Bevel budget: the chunky masses carry the miniature read and take the full
    # 0.12/2. The thin applied shells (ribbons, glow, bands) get none — that is
    # what keeps this comfortably under the 20,000-triangle cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if name.startswith(("ribbon", "court_ribbon", "court_band", "lit",
                            "seal_glow", "bay_lintel_glow", "bay_soffit_glow")):
            continue
        if name.startswith("pier") and not name.startswith("pier_capband"):
            continue  # already bevelled at creation
        if name.startswith("step"):
            continue  # thin slabs: a bevel here cost 6,800 triangles for nothing
        if name.startswith(("plinth", "fascia", "coping", "court_coping",
                            "pier_capband")):
            bevel(obj, width=0.12, segments=1)
            continue
        bevel(obj, width=0.12, segments=2)

    return scene


def normalize():
    """Sit the model on z=0, centre it in x/y, and put the crest at exactly
    Z_CREST so the loader's targetHeightM / measuredHeight scale lands on 1.000.
    Edits vertex data, so object transforms stay identity."""
    dg = bpy.context.evaluated_depsgraph_get()
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    for o in meshes:
        me = o.evaluated_get(dg).to_mesh()
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    # x/y centre on the RING (the real footprint), never on the full bbox: the
    # plaza steps project ~12 m past the drum and centring on them would slide
    # the building off its true coordinates (AGENTS rule 5).
    rx = [p[0] for p in RING]
    ry = [p[1] for p in RING]
    dx = (min(rx) + max(rx)) / 2.0
    dy = (min(ry) + max(ry)) / 2.0
    sz = Z_CREST / (mx.z - mn.z)
    for o in meshes:
        for v in o.data.vertices:
            v.co.x -= dx
            v.co.y -= dy
            v.co.z = (v.co.z - mn.z) * sz
    print(f"[build] normalize: dx={dx:.4f} dy={dy:.4f} z-scale={sz:.6f}")


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
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 4) for i in range(2)]}")
    print("[build] anchor lon/lat: -122.4212915 37.7804835 (ring bbox centre)")
    cx, cy, r, a0, a1 = ARC_FIT
    print(f"[build] drum arc: centre=({cx:.2f},{cy:.2f}) r={r:.2f} "
          f"sweep={math.degrees(a1 - a0):.1f} deg")
    _p, _t, en, _d = entrance_frame()
    print(f"[build] entrance heading: {math.degrees(math.atan2(en[0], en[1])) % 360:.1f} deg true")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    normalize()
    report()

    blend = os.path.join(out, "505-van-ness.blend")
    glb = os.path.join(out, "505-van-ness.glb")
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
