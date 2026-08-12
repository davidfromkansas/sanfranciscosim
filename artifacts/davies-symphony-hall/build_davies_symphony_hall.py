"""Deterministic Blender build of the SF-SIM miniature Davies Symphony Hall.

    blender -b --python build_davies_symphony_hall.py -- [--out DIR]

Writes davies-symphony-hall.blend and davies-symphony-hall.glb next to this file
(or into --out). Geometry is authored directly in world space in metres, Z up,
+X east, +Y north, origin at the footprint bounding-box centre, min Z = 0, so
the export needs no transforms applied after the fact.

Design (see REFERENCE.md for the sources behind every number):

* the measured OSM footprint of the whole Civic Center block (122.6 x 91.2 m
  envelope, 7,396 m2), used verbatim rather than idealised -- the block sits on
  the Civic Center grid ~9 deg off the world axes and the model inherits that
  from the polygon itself, so the loader never rotates it;
* the hero is the 103.6 deg convex glass arc across the Van Ness / Grove corner:
  a true circular arc, centre (10.03, -1.02), R = 44.75 m, least-squares fitted
  to the eleven OSM arc nodes with sub-metre residuals;
* two glazed promenade levels recessed 1.0 m behind a rhythm of slender precast
  fins, running the arc and continuing onto the Grove and Van Ness flanks;
* a solid attic band above them carrying a row of dark clerestory slots, a
  cornice ring at the LiDAR-measured 26.1 m, and a gold lettering fascia;
* a shallow ribbed metal shell roof cresting at exactly 35.0 m (LiDAR max
  34.95 m) -- 8.1 m of rise over a ~100 m span, radially ribbed;
* the south-west back-of-house block capped low and flat with tidy plant, and
  the two cantilevered curved terrace slabs at the ends of the arc.

Night state: the two promenade bands are the hero glow, the clerestory band and
the gold fascia are the supporting accents, everything else stays dark.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

Z_PLINTH = 1.6           # top of the stone sidewalk wall
Z_GLASS0 = 2.5           # promenade level 1 sill
Z_SPAND0 = 9.5           # spandrel between the two promenade levels
Z_SPAND1 = 10.5
Z_GLASS1 = 17.5          # head of promenade level 2
Z_CORNICE0 = 25.2        # underside of the cornice ring
Z_CORNICE1 = 26.1        # LiDAR median roof height -- the Beaux-Arts cornice line
Z_FASCIA1 = 26.9         # top of the gold lettering fascia; the shell springs here
Z_CREST = 35.0           # LiDAR max 34.95 -- the crest of the shell roof
Z_WING = 24.0            # back-of-house flat roof
Z_WING_PARAPET = 25.2

GLASS_INSET = 1.0        # promenade glazing recessed behind the wall plane
GLOW_INSET = 0.94        # glow shells proud of the opaque glazing, behind the fins
FIN_W = 0.55
FIN_D = 0.6
FIN_PITCH = 2.6          # target arc-length spacing along the glazed run
CORNICE_OUT = 0.6
FASCIA_OUT = 0.35
PLINTH_OUT = 1.2
SLOT_W = 0.7             # clerestory slots
SLOT_H = 2.2
SLOT_PITCH = 2.4
SLOT_Z = 22.2
TERRACE_OUT = 4.5
TERRACE_T = 0.45
RIBS = 40                # radial ribs on the shell roof
RIB_W = 0.55
RIB_RISE = 0.3
CREST_R = 6.0            # flat crest crown the ribs die into
RIB_STOP = 0.14          # ribs stop this far (in radial fraction) from the crest
SHELL_RINGS = 5
ARC_STEP = 2.2           # target chord along the front arc, metres

ARC_CX, ARC_CY, ARC_R = 10.03, -1.02, 44.75

# Measured OSM footprint (way/32865746), reprojected and centred on the anchor
# -122.4206030, 37.7776227. Counter-clockwise. Index 16..26 is the front arc and
# is replaced by a densified true arc at build time.
FOOT = [
    (-48.51, 38.89), (-47.70, 32.98), (-33.99, 34.98), (-26.79, -6.84),
    (-61.31, -12.43), (-56.07, -45.58), (-22.44, -40.25), (58.50, -27.44),
    (56.77, -16.19), (58.56, -15.41), (60.07, -14.17), (61.08, -12.19),
    (61.31, -9.45), (60.35, -7.29), (59.04, -5.69), (56.93, -4.78),
    (55.17, -4.57), (52.56, 9.97), (49.62, 19.71), (44.68, 27.31),
    (37.13, 34.80), (32.07, 38.19), (26.57, 40.81), (20.07, 42.53),
    (13.98, 43.48), (8.42, 43.57), (2.99, 43.14), (-7.43, 41.55),
    (-8.91, 42.65), (-11.20, 43.05), (-14.07, 42.21), (-15.43, 40.97),
    (-16.53, 39.15), (-17.16, 36.88), (-18.73, 45.58), (-39.91, 42.30),
    (-39.69, 40.22), (-44.03, 39.57),
]
ARC_FIRST, ARC_LAST = 16, 26   # inclusive indices of the fitted arc in FOOT
WING_IDX = [3, 4, 5, 6]        # the south-west back-of-house quadrant

PALETTE_HEX = {
    "Toy_cream": "f2ede3",
    "Toy_white": "f7f4ec",
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    "Toy_steel": "9aa0a6",
    "Toy_glass": "2a4d73",
    "Toy_ink": "3a3530",
    "Toy_roofd": "45454a",
    "Toy_gold": "caa64a",
    "Toy_mustard_Glow": "d9a441",
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
    mat.blend_method = "OPAQUE"
    return mat


def new_mesh(name, verts, faces, materials, face_mats=None, smooth=False):
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
    bmesh.ops.dissolve_degenerate(bm, dist=1e-4, edges=bm.edges)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    if smooth:
        mesh.polygons.foreach_set("use_smooth", [True] * len(mesh.polygons))
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


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0):
    hx, hy = sx / 2, sy / 2
    c, s = math.cos(yaw), math.sin(yaw)
    corners = [(-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)]
    corners = [(x * c - y * s, x * s + y * c) for x, y in corners]
    verts = [(cx + x, cy + y, z0) for x, y in corners]
    verts += [(cx + x, cy + y, z1) for x, y in corners]
    faces = [
        (3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4),
        (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


# ------------------------------------------------------------ polygon helpers


def densify_arc(poly, i0, i1, cx, cy, r, step):
    """Replace poly[i0:i1+1] with a true circular arc sampled at `step` chord."""
    a0 = math.atan2(poly[i0][1] - cy, poly[i0][0] - cx)
    a1 = math.atan2(poly[i1][1] - cy, poly[i1][0] - cx)
    while a1 < a0:
        a1 += 2 * math.pi
    n = max(2, int(round(r * (a1 - a0) / step)))
    arc = [
        (cx + r * math.cos(a0 + (a1 - a0) * k / n), cy + r * math.sin(a0 + (a1 - a0) * k / n))
        for k in range(n + 1)
    ]
    return poly[:i0] + arc + poly[i1 + 1 :], i0, i0 + n


def signed_area(poly):
    return 0.5 * sum(
        poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
        for i in range(len(poly))
    )


def vertex_normals(poly):
    """Inward unit bisector per vertex (polygon must be counter-clockwise)."""
    n = len(poly)
    out = []
    for i in range(n):
        px, py = poly[i - 1]
        cx, cy = poly[i]
        nx, ny = poly[(i + 1) % n]
        acc = [0.0, 0.0]
        for (ax, ay), (bx, by) in (((px, py), (cx, cy)), ((cx, cy), (nx, ny))):
            dx, dy = bx - ax, by - ay
            L = math.hypot(dx, dy) or 1.0
            acc[0] += -dy / L
            acc[1] += dx / L
        L = math.hypot(*acc) or 1.0
        out.append((acc[0] / L, acc[1] / L))
    return out


def offset_poly(poly, dist):
    """Offset inward by `dist` (negative expands outward)."""
    nrm = vertex_normals(poly)
    return [(p[0] + n[0] * dist, p[1] + n[1] * dist) for p, n in zip(poly, nrm)]


def prism(name, poly, z0, z1, side_mat, cap_mat=None, cap_top=True, cap_bottom=True):
    n = len(poly)
    mats = [side_mat] + ([cap_mat] if cap_mat and cap_mat is not side_mat else [])
    cap_i = len(mats) - 1
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces, fm = [], []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
        fm.append(0)
    if cap_bottom:
        faces.append(tuple(range(n - 1, -1, -1)))
        fm.append(cap_i)
    if cap_top:
        faces.append(tuple(range(n, 2 * n)))
        fm.append(cap_i)
    return new_mesh(name, verts, faces, mats, fm)


def ring_band(name, poly_out, poly_in, z0, z1, mat, closed=True, cap=True):
    """A closed band between two rings, extruded z0..z1 (a cornice / parapet)."""
    n = len(poly_out)
    verts = [(x, y, z0) for x, y in poly_out] + [(x, y, z0) for x, y in poly_in]
    verts += [(x, y, z1) for x, y in poly_out] + [(x, y, z1) for x, y in poly_in]
    O0, I0, O1, I1 = 0, n, 2 * n, 3 * n
    faces = []
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        j = (i + 1) % n
        faces.append((O0 + i, O0 + j, O1 + j, O1 + i))       # outer face
        faces.append((I1 + i, I1 + j, I0 + j, I0 + i))       # inner face
        if cap:
            faces.append((O1 + i, O1 + j, I1 + j, I1 + i))   # top
            faces.append((I0 + i, I0 + j, O0 + j, O0 + i))   # bottom
    return new_mesh(name, verts, faces, [mat])


# ---------------------------------------------------------------------- build


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    M = {k: material(k) for k in PALETTE_HEX}

    foot, arc_a, arc_b = densify_arc(FOOT, ARC_FIRST, ARC_LAST, ARC_CX, ARC_CY, ARC_R, ARC_STEP)
    shift = len(foot) - len(FOOT)
    wing = [FOOT[i] for i in WING_IDX]
    # main block = the whole footprint minus the south-west wing (indices 4 and 5)
    keep = [i for i in range(len(foot)) if i not in (4 + 0, 5 + 0)]
    # indices 4 and 5 of FOOT sit before the arc, so they are unshifted
    main = [foot[i] for i in keep]

    if signed_area(main) < 0:
        raise RuntimeError("main block polygon is not counter-clockwise")

    # Which edges of `main` carry the promenade glazing: the Van Ness flank, the
    # arc, and the Grove flank -- i.e. everything from the Hayes/Van Ness corner
    # round to the north-west corner. In `main` those are the vertices that came
    # from FOOT indices 7..37 and 0.
    src = [i for i in keep]
    glazed_v = set()
    for k, i in enumerate(src):
        # arc vertices (arc_a..arc_b) plus the Van Ness / Grove straight runs
        if arc_a <= i <= arc_b or (7 <= i <= arc_a) or (arc_b <= i <= len(foot) - 1) or i == 0:
            glazed_v.add(k)
    glazed_e = {k for k in range(len(main)) if k in glazed_v and (k + 1) % len(main) in glazed_v}

    build_body(main, glazed_v, glazed_e, M)
    build_fins(main, glazed_e, M)
    build_clerestory(main, glazed_e, M)
    build_cornice(main, M)
    # The shell is sampled against a SIMPLIFIED outline with the two small
    # street bays removed — the protruding Van Ness stair bay (FOOT 8..15) and
    # the recessed Grove one (FOOT 28..33). Sampling the raw outline makes the
    # roof dive into the recess and nick its own edge; a roof spans a recessed
    # entrance, it does not follow it.
    bays = set(range(8, 16)) | set(range(arc_b + 2, arc_b + 8))
    main_simple = [foot[i] for i in keep if i not in bays]
    build_shell(main_simple, M)
    build_wing(wing, M)
    build_terraces(M)
    build_plinth(foot, M)
    return scene


def build_body(main, glazed_v, glazed_e, M):
    """The hall volume: a lofted shell with the promenade recess cut into it."""
    n = len(main)
    nrm = vertex_normals(main)
    # (z, inset) per ring; duplicated z values give horizontal reveal faces
    rings = [
        (0.0, 0.0), (Z_GLASS0, 0.0), (Z_GLASS0, GLASS_INSET),
        (Z_SPAND0, GLASS_INSET), (Z_SPAND1, GLASS_INSET), (Z_GLASS1, GLASS_INSET),
        (Z_GLASS1, 0.0), (Z_CORNICE1, 0.0),
    ]
    # band materials, bottom to top
    band_mat = ["Toy_cream", "Toy_trim", "Toy_glass", "Toy_cream", "Toy_glass",
                "Toy_trim", "Toy_cream"]

    verts = []
    for z, inset in rings:
        for i, (x, y) in enumerate(main):
            d = inset if i in glazed_v else 0.0
            verts.append((x + nrm[i][0] * d, y + nrm[i][1] * d, z))

    mats = [M["Toy_cream"], M["Toy_trim"], M["Toy_glass"], M["Toy_roofd"]]
    midx = {"Toy_cream": 0, "Toy_trim": 1, "Toy_glass": 2, "Toy_roofd": 3}
    faces, fm = [], []
    for b in range(len(rings) - 1):
        base, top = b * n, (b + 1) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((base + i, base + j, top + j, top + i))
            key = band_mat[b]
            if key == "Toy_glass" and i not in glazed_e:
                key = "Toy_cream"
            fm.append(midx[key])
    # The main block's top is a real flat roof deck: the shell only covers the
    # auditorium, and the deck around it is what the app camera sees behind it.
    top = (len(rings) - 1) * n
    faces.append(tuple(range(top, top + n)))
    fm.append(midx["Toy_roofd"])
    faces.append(tuple(range(n - 1, -1, -1)))
    fm.append(midx["Toy_cream"])
    new_mesh("hall_body", verts, faces, mats, fm)

    # Night glow shells: thin panels proud of the opaque glazing, one per level.
    glow = M["Toy_mustard_Glow"]
    for tag, (z0, z1) in (("l1", (Z_GLASS0 + 0.25, Z_SPAND0 - 0.25)),
                          ("l2", (Z_SPAND1 + 0.25, Z_GLASS1 - 0.25))):
        gv, gf = [], []
        idx = {}
        for i in sorted(glazed_v):
            p = main[i]
            q = (p[0] + nrm[i][0] * GLOW_INSET, p[1] + nrm[i][1] * GLOW_INSET)
            idx[i] = len(gv)
            gv.append((q[0], q[1], z0))
            gv.append((q[0], q[1], z1))
        for i in sorted(glazed_e):
            j = (i + 1) % len(main)
            if j not in idx:
                continue
            a, b = idx[i], idx[j]
            gf.append((a, b, b + 1, a + 1))
        new_mesh(f"promenade_glow_{tag}", gv, gf, [glow])


def build_fins(main, glazed_e, M):
    """Slender precast fins at a constant pitch along the glazed run."""
    n = len(main)
    nrm = vertex_normals(main)
    placed = 0
    for i in sorted(glazed_e):
        j = (i + 1) % n
        ax, ay = main[i]
        bx, by = main[j]
        L = math.hypot(bx - ax, by - ay)
        if L < 0.2:
            continue
        k = max(1, int(round(L / FIN_PITCH)))
        for s in range(k):
            t = (s + 0.5) / k
            px = ax + (bx - ax) * t
            py = ay + (by - ay) * t
            nx = nrm[i][0] * (1 - t) + nrm[j][0] * t
            ny = nrm[i][1] * (1 - t) + nrm[j][1] * t
            ln = math.hypot(nx, ny) or 1.0
            nx, ny = nx / ln, ny / ln
            cx = px + nx * (FIN_D / 2)
            cy = py + ny * (FIN_D / 2)
            yaw = math.atan2(by - ay, bx - ax)
            box(f"fin_{placed:03d}", cx, cy, Z_GLASS0, Z_GLASS1,
                FIN_W, FIN_D, M["Toy_white"], yaw=yaw)
            placed += 1
    print(f"[build] fins={placed}")


def build_clerestory(main, glazed_e, M):
    """Dark slot band under the cornice, with its night-glow twin."""
    n = len(main)
    nrm = vertex_normals(main)
    slots = 0
    gv, gf = [], []
    for i in sorted(glazed_e):
        j = (i + 1) % n
        ax, ay = main[i]
        bx, by = main[j]
        L = math.hypot(bx - ax, by - ay)
        if L < 0.5:
            continue
        k = max(1, int(round(L / SLOT_PITCH)))
        for s in range(k):
            t = (s + 0.5) / k
            px = ax + (bx - ax) * t
            py = ay + (by - ay) * t
            nx = nrm[i][0] * (1 - t) + nrm[j][0] * t
            ny = nrm[i][1] * (1 - t) + nrm[j][1] * t
            ln = math.hypot(nx, ny) or 1.0
            nx, ny = nx / ln, ny / ln
            yaw = math.atan2(by - ay, bx - ax)
            box(f"slot_{slots:03d}", px - nx * 0.03, py - ny * 0.03,
                SLOT_Z, SLOT_Z + SLOT_H, SLOT_W, 0.12, M["Toy_ink"], yaw=yaw)
            # glow twin, a hair proud of the slot
            hw = SLOT_W / 2
            dx, dy = (bx - ax) / L, (by - ay) / L
            ox, oy = px - nx * 0.10, py - ny * 0.10
            base = len(gv)
            gv += [
                (ox - dx * hw, oy - dy * hw, SLOT_Z + 0.1),
                (ox + dx * hw, oy + dy * hw, SLOT_Z + 0.1),
                (ox + dx * hw, oy + dy * hw, SLOT_Z + SLOT_H - 0.1),
                (ox - dx * hw, oy - dy * hw, SLOT_Z + SLOT_H - 0.1),
            ]
            gf.append((base, base + 1, base + 2, base + 3))
            slots += 1
    new_mesh("clerestory_glow", gv, gf, [M["Toy_gold_Glow"]])
    print(f"[build] clerestory slots={slots}")


def build_cornice(main, M):
    """Cornice ring at the 26.1 m civic datum, plus the gold lettering fascia."""
    out = offset_poly(main, -CORNICE_OUT)
    ring_band("cornice", out, main, Z_CORNICE0, Z_CORNICE1, M["Toy_trim"])
    fout = offset_poly(main, -FASCIA_OUT)
    ring_band("fascia", fout, main, Z_CORNICE1, Z_FASCIA1, M["Toy_trim"])

    # The gold lettering runs across the ARC ONLY, the way it does in life --
    # a ring of gold all the way round would turn a restrained civic building
    # into a casino.
    a0, a1 = math.radians(2.0), math.radians(92.0)
    seg = 22
    lv, lf = [], []
    for k in range(seg + 1):
        a = a0 + (a1 - a0) * k / seg
        for r in (ARC_R + FASCIA_OUT - 0.06, ARC_R + FASCIA_OUT + 0.06):
            x, y = ARC_CX + r * math.cos(a), ARC_CY + r * math.sin(a)
            lv.append((x, y, Z_CORNICE1 + 0.14))
            lv.append((x, y, Z_FASCIA1 - 0.14))
        if k:
            b = (k - 1) * 4
            lf += [
                (b + 2, b + 3, b + 7, b + 6),   # outer face
                (b + 1, b + 0, b + 4, b + 5),   # inner face
                (b + 3, b + 1, b + 5, b + 7),   # top
                (b + 0, b + 2, b + 6, b + 4),   # bottom
            ]
    new_mesh("lettering_band", lv, lf, [M["Toy_gold"]])
    gv = [(x, y, z + (0.0 if i % 2 else 0.0)) for i, (x, y, z) in enumerate(lv)]
    gv = [(x + (x - ARC_CX) * 0.0016, y + (y - ARC_CY) * 0.0016, z) for x, y, z in gv]
    new_mesh("lettering_glow", gv, lf, [M["Toy_gold_Glow"]])


SHELL_DECK_INSET = 1.4   # strip of flat deck left between the shell and the parapet


def first_hit(poly, cx, cy, ang):
    """Distance to the FIRST boundary crossing of a ray -- using the nearest
    hit is what makes the sampled curve star-shaped even where the block
    outline is re-entrant."""
    dx, dy = math.cos(ang), math.sin(ang)
    best = None
    n = len(poly)
    for i in range(n):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % n]
        ex, ey = bx - ax, by - ay
        den = dx * ey - dy * ex
        if abs(den) < 1e-9:
            continue
        t = ((ax - cx) * ey - (ay - cy) * ex) / den
        u = ((ax - cx) * dy - (ay - cy) * dx) / den
        if t > 0 and -1e-6 <= u <= 1 + 1e-6 and (best is None or t < best):
            best = t
    return best if best else 1.0


def shell_boundary(main):
    """The shell's own footprint, as a polar curve about the arc centre.

    The front 103.6 deg IS the building's real arc, so the shell springs off
    the fascia there, exactly as the photographs show. Behind that it pulls in
    to a smooth oval and dies flush onto the flat roof deck, keeping the dome
    over the auditorium and clear of the back-of-house. Being polar about a
    single centre, it is star-shaped by construction and the cap can never
    fold the way it does over a re-entrant block outline.

    Returns (x, y, spring_z) per vertex.
    """
    a0, a1 = math.radians(-4.5), math.radians(99.1)
    front = max(2, int(round(ARC_R * (a1 - a0) / ARC_STEP)))
    back = 40
    poly = []
    for k in range(front + 1):
        a = a0 + (a1 - a0) * k / front
        poly.append((ARC_CX + ARC_R * math.cos(a), ARC_CY + ARC_R * math.sin(a),
                     Z_FASCIA1))
    span = 2 * math.pi - (a1 - a0)
    angles, raw, ease = [], [], []
    for k in range(1, back):
        s = k / back
        a = a1 + span * s
        # ease the deck strip in and out so the shell leaves the fascia smoothly
        e = min(1.0, min(s, 1 - s) * back / 3.0)
        angles.append(a)
        ease.append(e)
        raw.append(max(6.0, first_hit(main, ARC_CX, ARC_CY, a) - SHELL_DECK_INSET * e))

    # The block outline is re-entrant behind the arc (the Grove notch, the Van
    # Ness stair bay, the wing cut), so the raw radius jumps. A roof does not.
    # Take a local minimum first so the shell pulls IN around a notch instead
    # of diving into it, then smooth, then clamp back inside the outline so
    # smoothing can never push the shell out over a street.
    smooth = raw[:]
    for _ in range(6):
        smooth = [
            smooth[i] if i in (0, len(smooth) - 1)
            else 0.25 * smooth[i - 1] + 0.5 * smooth[i] + 0.25 * smooth[i + 1]
            for i in range(len(smooth))
        ]
    for a, r_s, r_raw, e in zip(angles, smooth, raw, ease):
        r = min(r_s, r_raw)
        z = Z_FASCIA1 - (Z_FASCIA1 - (Z_CORNICE1 - 0.05)) * e
        poly.append((ARC_CX + r * math.cos(a), ARC_CY + r * math.sin(a), z))
    return poly


def build_shell(_main, M):
    """The shallow ribbed metal shell: a paraboloid cap over the auditorium."""
    main = shell_boundary(_main)
    n = len(main)
    cx, cy = ARC_CX, ARC_CY
    # The ribs stand RIB_RISE proud, so the shell surface itself crests that
    # much lower and the rib crown lands on exactly Z_CREST.
    apex_z = Z_CREST - RIB_RISE

    def z_at(t, spring):  # t = 1 at the boundary, 0 at the crest
        return spring + (apex_z - spring) * (1.0 - t * t)

    verts, faces = [], []
    for r in range(SHELL_RINGS + 1):
        t = 1.0 - r / SHELL_RINGS
        for x, y, spring in main:
            verts.append((cx + (x - cx) * t, cy + (y - cy) * t, z_at(t, spring)))
    apex = len(verts)
    verts.append((cx, cy, apex_z))
    for r in range(SHELL_RINGS - 1):
        a, b = r * n, (r + 1) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((a + i, a + j, b + j, b + i))
    last = (SHELL_RINGS - 1) * n
    for i in range(n):
        faces.append((last + i, last + (i + 1) % n, apex))
    shell = new_mesh("shell_roof", verts, faces, [M["Toy_steel"]], smooth=True)
    shell.data.shade_smooth()

    # radial ribs, running with the curve; they die into the crest crown
    rv, rf = [], []
    seg = 5
    for k in range(RIBS):
        a = 2 * math.pi * k / RIBS
        # boundary point of the star-shaped shell footprint along this ray
        bx, by, spring = ray_to_polygon(main, cx, cy, a)
        for s in range(seg + 1):
            t = 1.0 - (1.0 - RIB_STOP) * s / seg
            px = cx + (bx - cx) * t
            py = cy + (by - cy) * t
            z = z_at(t, spring) + RIB_RISE
            hw = RIB_W / 2
            base = len(rv)
            rv.append((px - math.sin(a) * hw, py + math.cos(a) * hw, z))
            rv.append((px + math.sin(a) * hw, py - math.cos(a) * hw, z))
            if s:
                rf.append((base - 2, base - 1, base + 1, base))
    new_mesh("shell_ribs", rv, rf, [M["Toy_steel"]], smooth=True)

    # crest crown: the flat cap the ribs run into, and the model's true top
    crown = [
        (cx + CREST_R * math.cos(2 * math.pi * i / 14),
         cy + CREST_R * math.sin(2 * math.pi * i / 14))
        for i in range(14)
    ]
    prism("shell_crown", crown, z_at(RIB_STOP, Z_CORNICE1) - 0.1, Z_CREST,
          M["Toy_steel"], M["Toy_steel"], cap_bottom=False)


def ray_to_polygon(poly, cx, cy, ang):
    """First intersection of a ray from (cx, cy) with the boundary, plus the
    spring height interpolated onto it."""
    dx, dy = math.cos(ang), math.sin(ang)
    best = None
    best_z = poly[0][2]
    n = len(poly)
    for i in range(n):
        ax, ay, az = poly[i]
        bx, by, bz = poly[(i + 1) % n]
        ex, ey = bx - ax, by - ay
        den = dx * ey - dy * ex
        if abs(den) < 1e-9:
            continue
        t = ((ax - cx) * ey - (ay - cy) * ex) / den
        u = ((ax - cx) * dy - (ay - cy) * dx) / den
        if t > 0 and -1e-6 <= u <= 1 + 1e-6:
            if best is None or t < best:
                best = t
                best_z = az + (bz - az) * min(max(u, 0.0), 1.0)
    if best is None:
        best = 1.0
    return cx + dx * best, cy + dy * best, best_z


def build_wing(wing, M):
    """South-west back-of-house: a calm low block with a parapet and tidy plant."""
    if signed_area(wing) < 0:
        wing = wing[::-1]
    prism("boh_block", wing, 0.0, Z_WING, M["Toy_cream"], M["Toy_roofd"])
    inner = offset_poly(wing, 0.9)
    bevel(ring_band("boh_parapet", wing, inner, Z_WING, Z_WING_PARAPET, M["Toy_cream"]), 0.1)
    cx = sum(p[0] for p in wing) / 4
    cy = sum(p[1] for p in wing) / 4
    for k, (dx, dy, sx, sy, h) in enumerate((
        (-8.0, 6.0, 11.0, 7.0, 3.2),
        (6.0, -2.0, 9.0, 6.0, 2.4),
        (-2.0, -11.0, 7.0, 5.0, 2.0),
    )):
        bevel(box(f"boh_plant_{k}", cx + dx, cy + dy, Z_WING, Z_WING + h,
                  sx, sy, M["Toy_steel"]), 0.1)
    # Anything hung on a wall is placed ON that wall segment, because the
    # back-of-house walls are not axis-aligned (Civic Center grid).
    def on_wall(a, b, t, out):
        ax, ay = wing[a]
        bx, by = wing[b]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy)
        nx, ny = dy / L, -dx / L          # outward for a CCW ring
        return (ax + dx * t + nx * out, ay + dy * t + ny * out,
                math.atan2(dy, dx))

    # service canopy over the Hayes Street loading entrance
    x, y, yaw = on_wall(2, 3, 0.55, 1.4)
    bevel(box("service_canopy", x, y, 5.4, 5.9, 13.0, 3.6, M["Toy_trim"], yaw=yaw), 0.1)
    x, y, yaw = on_wall(2, 3, 0.55, 0.05)
    bevel(box("loading_recess", x, y, 0.0, 5.4, 11.0, 0.5, M["Toy_ink"], yaw=yaw), 0.05)
    # a single arched-window stand-in high on the Franklin wall
    x, y, yaw = on_wall(1, 2, 0.45, 0.05)
    bevel(box("franklin_window", x, y, 14.0, 20.0, 7.0, 0.5, M["Toy_glass"], yaw=yaw), 0.05)


def build_deck_plant(M):
    """Tidy mechanical clusters on the flat deck that rings the shell -- the
    camera looks down, so the deck is a designed surface, not a leftover."""
    for k, (x, y, sx, sy, h, yaw) in enumerate((
        (-34.0, 20.0, 12.0, 7.0, 2.6, math.radians(-9)),
        (2.0, -33.0, 10.0, 5.0, 2.0, math.radians(-9)),
        (45.0, -22.0, 8.0, 5.0, 2.3, math.radians(-9)),
    )):
        bevel(box(f"deck_plant_{k}", x, y, Z_CORNICE1, Z_CORNICE1 + h,
                  sx, sy, M["Toy_steel"], yaw=yaw), 0.1)


def build_terraces(M):
    """Cantilevered curved terrace slabs at both ends of the front arc."""
    a0 = math.radians(-4.5)
    a1 = math.radians(99.1)
    span = math.radians(13.0)
    for tag, (s0, s1) in (("e", (a0, a0 + span)), ("n", (a1 - span, a1))):
        verts, faces = [], []
        seg = 8
        for k in range(seg + 1):
            a = s0 + (s1 - s0) * k / seg
            for r in (ARC_R - 0.5, ARC_R + TERRACE_OUT):
                verts.append((ARC_CX + r * math.cos(a), ARC_CY + r * math.sin(a), Z_GLASS1))
                verts.append((ARC_CX + r * math.cos(a), ARC_CY + r * math.sin(a),
                              Z_GLASS1 + TERRACE_T))
        for k in range(seg):
            b = k * 4
            faces += [
                (b + 1, b + 3, b + 7, b + 5),   # top
                (b + 2, b + 0, b + 4, b + 6),   # bottom
                (b + 3, b + 2, b + 6, b + 7),   # outer nose
                (b + 0, b + 1, b + 5, b + 4),   # inner
            ]
        faces.append((0, 2, 3, 1))
        b = seg * 4
        faces.append((b + 1, b + 3, b + 2, b + 0))
        bevel(new_mesh(f"terrace_{tag}", verts, faces, [M["Toy_trim"]]), 0.08)

        # pipe rail along the nose, as a solid so it survives the normals test
        z0, z1 = Z_GLASS1 + TERRACE_T, Z_GLASS1 + TERRACE_T + 1.0
        rv, rf = [], []
        for k in range(seg + 1):
            a = s0 + (s1 - s0) * k / seg
            for r in (ARC_R + TERRACE_OUT - 0.35, ARC_R + TERRACE_OUT - 0.15):
                x, y = ARC_CX + r * math.cos(a), ARC_CY + r * math.sin(a)
                rv += [(x, y, z0), (x, y, z1)]
            if k:
                b = (k - 1) * 4
                rf += [
                    (b + 2, b + 3, b + 7, b + 6),
                    (b + 1, b + 0, b + 4, b + 5),
                    (b + 3, b + 1, b + 5, b + 7),
                    (b + 0, b + 2, b + 6, b + 4),
                ]
        rf.append((0, 1, 3, 2))
        b = seg * 4
        rf.append((b + 2, b + 3, b + 1, b + 0))
        new_mesh(f"terrace_rail_{tag}", rv, rf, [M["Toy_steel"]])


def build_plinth(foot, M):
    """The stone sidewalk wall; also hides the terrain seam."""
    outer = offset_poly(foot, -PLINTH_OUT)
    bevel(prism("plinth", outer, 0.0, Z_PLINTH, M["Toy_stone"], M["Toy_stone"]), 0.12)


# --------------------------------------------------------------------- report


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

    blend = os.path.join(out, "davies-symphony-hall.blend")
    glb = os.path.join(out, "davies-symphony-hall.glb")
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
