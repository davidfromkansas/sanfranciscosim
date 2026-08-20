"""Deterministic Blender build of the SF-SIM miniature 414 Brannan Street.

    blender -b --python build_414_brannan.py -- [--out DIR]

Writes 414-brannan.blend and 414-brannan.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = parcel AABB centre (anchor lon -122.3948685,
lat 37.7799308), min Z = 0, roof-monitor crest exactly 14.0 m.

Design (see REFERENCE.md for the sources behind every number):

* the surveyed DataSF parcel 3776011 — a true four-vertex parallelogram, 24.90 m
  of Brannan frontage by 21.28 m deep, 530.0 m2, sitting 45.2 deg off the world
  axes like the whole SoMa grid. The building covers 95% of it;
* a CORNER site: Brannan (SE) and Ritch (SW) are both finished street
  elevations. The northeast side is a party wall against 400 Brannan and the
  northwest side is the block interior — quiet, finished, no invented grid;
* the identity feature: a red clay-tile pent roof over a vermilion frieze band,
  running the full Brannan parapet and returning 6 m onto Ritch. It is a red
  line on a slate box seen from directly overhead, which is what the app's
  camera sees, so it gets the exaggeration budget — a 0.50 m projection and a
  ribbed top face;
* the teal arched entry with a cream fan tympanum and a gold medallion, hard
  against the northeast party wall where the real one is;
* three curved wrought-iron Juliet balconies at the southwest end of Brannan,
  which every frontal Street View frame hides behind a row of mature ficus and
  only the oblique from the Ritch corner shows;
* a slate blue-gray monolithic body: no base course, no cornice. The hex is
  LIFTED from the photographic value (#8a97a8 against a measured #6a798b in
  shade) because the diorama has far less ambient light than this render rig —
  see REPORT.md;
* three roof levels — NE bay deck 10.0 m, SW bay 11.19 m, and the raised
  daylight monitor over the middle bay at 13.55 m deck / 14.0 m crest;
* night state: the frosted ground-floor bays are the hero (they are translucent
  panels by day and lit boxes by night, and this ground floor is a lobby and
  cafe), with three lit upper windows, the monitor clerestory and the tympanum
  medallion as accents. Glow surfaces are thin shells proud of the opaque fills
  and cover only part of each opening — the app renders _Glow in a separate
  layer and a closed shell reads ~23% opaque in the day pass.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF parcel 3776011 projected with the app's tangent projection and
# recentred on its own AABB centre. Four vertices, no simplification: the lot is
# a true parallelogram. CCW.
FOOTPRINT = [
    (-1.325, -16.306),   # 0  S corner — the Brannan / Ritch street corner
    (16.353, 1.237),     # 1  E corner — Brannan frontage, party line with 400 Brannan
    (1.325, 16.306),     # 2  N corner — rear, northeast end
    (-16.353, -1.237),   # 3  W corner — rear, southwest end
]

# Edge i runs FOOTPRINT[i] -> FOOTPRINT[i+1]. Outward normals from the winding,
# never from the centroid.
EDGE_BRANNAN = 0    # 24.90 m, faces SE 135.2 deg — Brannan Street
EDGE_PARTY = 1      # 21.28 m, faces NE  45.2 deg — party wall, 400 Brannan
EDGE_REAR = 2       # 24.90 m, faces NW 315.2 deg — block interior
EDGE_RITCH = 3      # 21.28 m, faces SW 225.2 deg — Ritch Street

Z_DECK = 9.85         # NE-bay roof deck (LiDAR NE median 10.32 incl. the pent)
Z_WALL = 10.20        # wall top the tile pent sits on
Z_TILE = 10.39        # clay-tile ridge (Street View photogrammetry, 10.39 m)
Z_EAVE = 10.05        # outer lip of the tile pent, 0.68 m out and sloping down
Z_FRIEZE0 = 9.05      # underside of the vermilion frieze (measured 9.22 m,
                      # dropped 0.17 m: the band is the thumbnail-scale cue)
Z_SW_DECK = 11.19     # southwest bay deck (LiDAR median)
Z_SW_CAP = 11.44      # its coping
Z_MON0 = 9.85         # monitor springs off the NE deck level
Z_MON_DECK = 13.55    # monitor deck (LiDAR middle-bay median 13.47)
Z_CREST = 14.00       # monitor coping -> the bbox top, = targetHeightM

Z_GF0, Z_GF1 = 0.30, 4.58        # ground-floor bays (head measured at 4.58 m)
Z_WIN0, Z_WIN1 = 5.75, 8.10      # upper windows (measured sill and head)
Z_ARCH_SPRING = 3.35             # arch springing
Z_ARCH_CROWN = 4.70              # arch crown
Z_BALC0, Z_BALC1 = 5.58, 6.62    # Juliet balcony rail

PARAPET_T = 0.35
TILE_PROJ = 0.68
TILE_RIB = 1.25                  # rib pitch along the pent
RITCH_TILE_RUN = 6.0             # how far the pent returns onto Ritch

PALETTE_HEX = {
    # The one deliberate off-palette colour. #6a798b is the measured shadow
    # value and #b0b7bd the measured sunlit value; this sits between them and,
    # critically, has ~2.2x the luminance of Toy_roofd, which measures
    # rgb(9,9,12) in the running diorama.
    "Toy_slate": "8a97a8",
    "Toy_ioorange": "c0402a",
    "Toy_brick": "c96f4a",
    "Toy_rust": "a86444",
    "Toy_teal": "3fa8a0",
    "Toy_trim": "f3efe6",
    "Toy_gold": "caa64a",
    "Toy_ink": "3a3530",
    "Toy_glass": "2a4d73",
    "Toy_stone": "d9d2c2",
    "Toy_steel": "9aa0a6",
    "Toy_roofd": "45454a",
    "Toy_trim_Glow": "f3efe6",
    "Toy_glass_Glow": "6f95b8",
    "Toy_gold_Glow": "caa64a",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def poly_edge(i):
    """Edge i of FOOTPRINT: (origin, length, tangent unit, outward normal)."""
    a = FOOTPRINT[i]
    b = FOOTPRINT[(i + 1) % len(FOOTPRINT)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def offset_polygon(poly, d):
    """Miter offset of the CCW footprint; positive d moves outward."""
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


def rect_profile(w, z0, z1):
    a = w / 2.0
    return [(-a, z0), (a, z0), (a, z1), (-a, z1)]


def arch_band_profile(r_out, r_in, z_spring, segments=9):
    """A C-shaped closed polygon: the archivolt of a round arch. Outer arc left
    to right over the top, inner arc back. Jambs are separate rectangles."""
    pts = []
    for i in range(segments + 1):
        a = math.pi - i * math.pi / segments
        pts.append((r_out * math.cos(a), z_spring + r_out * math.sin(a)))
    for i in range(segments + 1):
        a = i * math.pi / segments
        pts.append((r_in * math.cos(a), z_spring + r_in * math.sin(a)))
    return pts


def half_disc_profile(r, z_spring, segments=9):
    pts = [(-r, z_spring)]
    for i in range(1, segments):
        a = math.pi - i * math.pi / segments
        pts.append((r * math.cos(a), z_spring + r * math.sin(a)))
    pts.append((r, z_spring))
    return pts


def disc_profile(r, zc, segments=10):
    return [
        (r * math.cos(2 * math.pi * i / segments), zc + r * math.sin(2 * math.pi * i / segments))
        for i in range(segments)
    ]


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
    """Miniature-style edge softening (style bible s.4), capped at a third of
    the thinnest dimension so applied panels do not collapse into slivers."""
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


def face_panel(name, edge, u_centre, profile, d0, d1, mat):
    """Closed prism of a (u, z) profile lying in the plane of wall `edge`,
    extruded outward from offset d0 to d1 along that wall's normal."""
    a, _length, t, n = poly_edge(edge)
    verts = []
    for d in (d0, d1):
        for du, z in profile:
            px = a[0] + t[0] * (u_centre + du) + n[0] * d
            py = a[1] + t[1] * (u_centre + du) + n[1] * d
            verts.append((px, py, z))
    npts = len(profile)
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0, mat_caps=None):
    c, s = math.cos(yaw), math.sin(yaw)
    corners = []
    for lx, ly in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)):
        corners.append((cx + lx * c - ly * s, cy + lx * s + ly * c))
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    if mat_caps is None:
        return new_mesh(name, verts, faces, [mat])
    return new_mesh(name, verts, faces, [mat, mat_caps], [1, 1, 0, 0, 0, 0])


def roof_box(name, u, v, z0, z1, su, sv, mat, mat_caps=None):
    """Box on the roof, aligned to the building's own grid: u runs along the
    Brannan edge from its Ritch end, v runs INTO the block."""
    origin, _l, t, n = poly_edge(EDGE_BRANNAN)
    cx = origin[0] + t[0] * u - n[0] * v
    cy = origin[1] + t[1] * u - n[1] * v
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=math.atan2(t[1], t[0]),
               mat_caps=mat_caps)


def roof_rect(u, v, su, sv):
    """CCW world polygon of a rectangle on the roof grid (u along Brannan from
    its Ritch end, v into the block)."""
    origin, _l, t, n = poly_edge(EDGE_BRANNAN)
    e1, e2 = t, (-n[0], -n[1])
    pts = []
    for du, dv in ((-su / 2, -sv / 2), (su / 2, -sv / 2), (su / 2, sv / 2), (-su / 2, sv / 2)):
        uu, vv = u + du, v + dv
        pts.append((origin[0] + e1[0] * uu + e2[0] * vv, origin[1] + e1[1] * uu + e2[1] * vv))
    return pts


def roof_coping(name, u, v, su, sv, z0, z1, t, mat):
    """A coping band round a raised roof volume — a ring, never a solid lid, or
    the cream cap swallows the deck design underneath it."""
    return ring_band(name, roof_rect(u, v, su, sv), z0, z1, -t, 0.06, mat)


def pent_roof(name, edge, u0, u1, mat):
    """The clay-tile pent: a sloping hood swept along `edge` from u0 to u1,
    ridge at the wall (Z_TILE) and eave TILE_PROJ metres out (Z_EAVE), with a
    ribbed top face implying barrel tile. Closed solid."""
    a, _length, t, n = poly_edge(edge)
    span = u1 - u0
    nseg = max(2, int(round(span / TILE_RIB)))

    def p(u, d, z):
        return (a[0] + t[0] * u + n[0] * d, a[1] + t[1] * u + n[1] * d, z)

    verts, faces = [], []
    # four rails: inner-bottom, outer-bottom, outer-top, inner-top. The top two
    # rails ripple by +/-0.035 m per segment; the bottom two stay flat.
    for i in range(nseg + 1):
        u = u0 + span * i / nseg
        bump = 0.05 if i % 2 == 0 else -0.05
        verts.append(p(u, -0.02, Z_TILE - 0.30))          # 4i+0 inner bottom
        verts.append(p(u, TILE_PROJ, Z_EAVE - 0.26))      # 4i+1 outer bottom
        verts.append(p(u, TILE_PROJ, Z_EAVE + bump))      # 4i+2 outer top
        verts.append(p(u, -0.02, Z_TILE + bump))          # 4i+3 inner top
    for i in range(nseg):
        b0, b1 = 4 * i, 4 * (i + 1)
        for k in range(4):
            k2 = (k + 1) % 4
            faces.append((b0 + k, b0 + k2, b1 + k2, b1 + k))
    faces.append((3, 2, 1, 0))
    last = 4 * nseg
    faces.append((last + 0, last + 1, last + 2, last + 3))
    return new_mesh(name, verts, faces, [mat])


def balcony(name, edge, u, mat, radius=0.72, thick=0.10, segments=6):
    """A curved wrought-iron Juliet balcony: a half-annulus in plan, extruded
    between Z_BALC0 and Z_BALC1, plus its floor slab."""
    a, _length, t, n = poly_edge(edge)

    def p(du, d, z):
        return (a[0] + t[0] * (u + du) + n[0] * d, a[1] + t[1] * (u + du) + n[1] * d, z)

    outer, inner = [], []
    for i in range(segments + 1):
        ang = math.pi * i / segments
        outer.append((-radius * math.cos(ang), radius * math.sin(ang)))
        inner.append((-(radius - thick) * math.cos(ang), (radius - thick) * math.sin(ang)))
    loop = outer + inner[::-1]
    npts = len(loop)
    verts = [p(du, d, Z_BALC0) for du, d in loop] + [p(du, d, Z_BALC1) for du, d in loop]
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    new_mesh(name, verts, faces, [mat])
    # floor slab: the full half-disc, 0.10 m thick
    slab = [(-radius * math.cos(math.pi * i / segments), radius * math.sin(math.pi * i / segments))
            for i in range(segments + 1)]
    slab.append((radius, 0.0))
    slab.append((-radius, 0.0))
    sv = [p(du, d, Z_BALC0 - 0.12) for du, d in slab] + [p(du, d, Z_BALC0) for du, d in slab]
    m = len(slab)
    sf = []
    for i in range(m):
        j = (i + 1) % m
        sf.append((i, j, m + j, m + i))
    sf.append(tuple(range(m - 1, -1, -1)))
    sf.append(tuple(range(m, 2 * m)))
    return new_mesh(name + "_slab", sv, sf, [mat])


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


# --------------------------------------------------------------------- parts


def rect_opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None,
                 inset=0.18, glow_frac=1.0):
    """A punched opening: a proud frame with the fill set back inside it, so the
    opening reads as a recess. `glow_frac` covers only the lower part of the
    fill — a full-height shell tints the whole facade in the day pass."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, 0.06, frame_mat)
    face_panel(
        f"{tag}_fill", edge, u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset), 0.0, 0.12, fill_mat,
    )
    if glow_mat is not None:
        g = inset + 0.12
        zg1 = z0 + g + (z1 - z0 - 2 * g) * glow_frac
        face_panel(
            f"{tag}_glow", edge, u,
            rect_profile(w - 2 * g, z0 + g, zg1), 0.09, 0.16, glow_mat,
        )


def recessed_panel(tag, edge, u, w, z0, z1, mat, bar=0.22, depth=0.14):
    """A large blank wall panel read as a recess: four thin bars standing proud
    of the wall around an untouched field, so the shadow line does the work."""
    face_panel(f"{tag}_top", edge, u, rect_profile(w, z1 - bar, z1), 0.0, depth, mat)
    face_panel(f"{tag}_bot", edge, u, rect_profile(w, z0, z0 + bar), 0.0, depth, mat)
    for side, tagname in ((-1, "lft"), (1, "rgt")):
        face_panel(
            f"{tag}_{tagname}", edge, u + side * (w - bar) / 2.0,
            rect_profile(bar, z0, z1), 0.0, depth, mat,
        )


def glazed_bay(tag, edge, u, w, mats, lit=False):
    """A tall ground-floor bay: bronze frame, 3-part frosted panel, louvre base."""
    ink, trim, roofd, tglow = mats
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, Z_GF0, Z_GF1), 0.0, 0.06, ink)
    # frosted glazing, split by two transoms into the 3-part grid
    zs = [(0.95, 2.05), (2.20, 3.05), (3.20, 4.42)]
    for k, (za, zb) in enumerate(zs):
        face_panel(f"{tag}_fill{k}", edge, u, rect_profile(w - 0.34, za, zb), 0.0, 0.13, trim)
    # louvred base
    face_panel(f"{tag}_louvre", edge, u, rect_profile(w - 0.34, 0.42, 0.80), 0.0, 0.11, roofd)
    if lit:
        face_panel(f"{tag}_glow", edge, u, rect_profile(w - 0.62, 1.05, 3.00), 0.10, 0.17, tglow)


def arched_entry(tag, edge, u, mats):
    """The teal portal: jambs, archivolt, cream fan tympanum, gold medallion."""
    teal, trim, gold, ink, gglow = mats
    r_in = 1.05
    r_out = 1.42
    # jambs
    for side in (-1, 1):
        face_panel(
            f"{tag}_jamb{'L' if side < 0 else 'R'}", edge,
            u + side * (r_in + r_out) / 2.0,
            rect_profile(r_out - r_in, 0.0, Z_ARCH_SPRING), 0.0, 0.17, teal,
        )
    face_panel(f"{tag}_arch", edge, u, arch_band_profile(r_out, r_in, Z_ARCH_SPRING),
               0.0, 0.17, teal)
    # tympanum fan and the door beneath it
    face_panel(f"{tag}_fan_fill", edge, u, half_disc_profile(r_in - 0.04, Z_ARCH_SPRING),
               0.08, 0.19, trim)
    face_panel(f"{tag}_door_fill", edge, u,
               rect_profile(2 * r_in - 0.08, 0.0, Z_ARCH_SPRING), 0.0, 0.09, ink)
    face_panel(f"{tag}_medal_fill", edge, u, disc_profile(0.30, Z_ARCH_SPRING + 0.44),
               0.19, 0.26, gold)
    face_panel(f"{tag}_medal_glow", edge, u, disc_profile(0.22, Z_ARCH_SPRING + 0.44),
               0.24, 0.30, gglow)


def street_elevation_brannan(mats):
    slate, ink, trim, glass, stone, roofd, teal, gold, tglow, gglow = mats
    e = EDGE_BRANNAN
    # southwest half: two large blank recessed panels (former loading bays)
    for i, (u, w) in enumerate(((3.9, 4.6), (8.9, 4.6))):
        recessed_panel(f"bran_blank{i}", e, u, w, 0.55, 4.30, slate)
    # northeast half: four frosted glazed bays under the tile line
    for i, u in enumerate((12.2, 14.8, 17.4, 20.0)):
        glazed_bay(f"bran_bay{i}", e, u, 2.15, (ink, trim, roofd, tglow), lit=True)
    # the arch, hard against the party wall
    arched_entry("bran_arch", e, 22.7, (teal, trim, gold, ink, gglow))
    # upper floor: seven punched windows, three of them balconied at the SW end
    for i, u in enumerate((1.9, 5.2, 8.5, 11.8, 15.1, 18.9, 22.7)):
        rect_opening(
            f"bran_win{i}", e, u, 1.55, Z_WIN0, Z_WIN1, trim, glass,
            gglow if i in (2, 5) else None, inset=0.16, glow_frac=0.62,
        )
        face_panel(f"bran_sill{i}", e, u, rect_profile(1.85, Z_WIN0 - 0.14, Z_WIN0),
                   0.0, 0.16, stone)
        if i < 3:
            balcony(f"bran_balc{i}", e, u, ink)


def street_elevation_ritch(mats):
    slate, ink, trim, glass, stone, roofd, _teal, _gold, tglow, gglow = mats
    e = EDGE_RITCH
    # ground: rear roll-up, louvred panel, frosted bay, corner roll-up
    face_panel("ritch_roll0_frame", e, 5.0, rect_profile(3.6, 0.0, 3.55), 0.0, 0.06, ink)
    face_panel("ritch_roll0_fill", e, 5.0, rect_profile(3.26, 0.16, 3.39), 0.0, 0.12, stone)
    face_panel("ritch_vent_frame", e, 9.5, rect_profile(3.0, 1.10, 3.30), 0.0, 0.06, ink)
    face_panel("ritch_vent_fill", e, 9.5, rect_profile(2.70, 1.26, 3.14), 0.0, 0.12, roofd)
    glazed_bay("ritch_bay0", e, 14.3, 2.30, (ink, trim, roofd, tglow), lit=True)
    face_panel("ritch_roll1_frame", e, 18.4, rect_profile(2.60, 0.0, 3.30), 0.0, 0.06, ink)
    face_panel("ritch_roll1_fill", e, 18.4, rect_profile(2.28, 0.16, 3.14), 0.0, 0.12, trim)
    recessed_panel("ritch_blank0", e, 1.9, 2.6, 0.55, 4.30, slate)
    # upper floor: five smaller punched windows, one balcony at the Brannan end
    for i, u in enumerate((3.2, 6.6, 10.0, 13.4, 17.5)):
        rect_opening(
            f"ritch_win{i}", e, u, 1.25, Z_WIN0, Z_WIN1, trim, glass,
            gglow if i == 3 else None, inset=0.15, glow_frac=0.62,
        )
        face_panel(f"ritch_sill{i}", e, u, rect_profile(1.52, Z_WIN0 - 0.14, Z_WIN0),
                   0.0, 0.15, stone)
    balcony("ritch_balc0", e, 19.6, ink)
    # the round wall plaque, high on the rear half
    face_panel("ritch_plaque_fill", e, 8.2, disc_profile(0.34, 9.05), 0.0, 0.10, stone)


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    slate = material("Toy_slate")
    ioorange = material("Toy_ioorange")
    brick = material("Toy_brick")
    rust = material("Toy_rust")
    teal = material("Toy_teal")
    trim = material("Toy_trim")
    gold = material("Toy_gold")
    ink = material("Toy_ink")
    glass = material("Toy_glass")
    stone = material("Toy_stone")
    steel = material("Toy_steel")
    roofd = material("Toy_roofd")
    tglow = material("Toy_trim_Glow")
    gglow = material("Toy_glass_Glow")
    ldglow = material("Toy_gold_Glow")

    # --- body: one board-formed concrete box, its top cap IS the NE roof deck
    prism("body", FOOTPRINT, 0.0, Z_DECK, slate, mat_caps=stone)

    # --- parapet ring: 0.30 m of wall standing proud of the deck -------------
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_WALL, -PARAPET_T, 0.0, slate)

    # --- the identity band: vermilion frieze under a red clay-tile pent ------
    # Both are street-face only; the party wall and the rear carry neither, as
    # the photographs show. The Ritch return stops 6 m from the corner.
    len_b = poly_edge(EDGE_BRANNAN)[1]
    len_r = poly_edge(EDGE_RITCH)[1]
    face_panel("frieze_bran", EDGE_BRANNAN, len_b / 2.0,
               rect_profile(len_b - 0.10, Z_FRIEZE0, Z_WALL), 0.0, 0.06, ioorange)
    face_panel("frieze_ritch", EDGE_RITCH, len_r - RITCH_TILE_RUN / 2.0,
               rect_profile(RITCH_TILE_RUN, Z_FRIEZE0, Z_WALL), 0.0, 0.06, ioorange)
    pent_roof("pent_bran", EDGE_BRANNAN, 0.0, len_b, brick)
    pent_roof("pent_ritch", EDGE_RITCH, len_r - RITCH_TILE_RUN, len_r, brick)
    # a darker fascia lip so the eave keeps a line at thumbnail size
    face_panel("pent_fascia_bran", EDGE_BRANNAN, len_b / 2.0,
               rect_profile(len_b, Z_EAVE - 0.27, Z_EAVE - 0.06), 0.63, 0.71, rust)
    face_panel("pent_fascia_ritch", EDGE_RITCH, len_r - RITCH_TILE_RUN / 2.0,
               rect_profile(RITCH_TILE_RUN, Z_EAVE - 0.27, Z_EAVE - 0.06), 0.63, 0.71, rust)

    mats = (slate, ink, trim, glass, stone, roofd, teal, gold, tglow, gglow)
    street_elevation_brannan(mats)
    street_elevation_ritch(mats)

    # --- party wall and rear: quiet, finished, no invented grid --------------
    for tag, edge, us in (
        ("party", EDGE_PARTY, (4.8, 10.6, 16.4)),
        ("rear", EDGE_REAR, (5.2, 10.6, 15.4, 20.2)),
    ):
        for i, u in enumerate(us):
            rect_opening(f"{tag}win{i}", edge, u, 1.15, Z_WIN0 + 0.25, Z_WIN1 - 0.25,
                         trim, glass, inset=0.14)

    # --- the second roof level: the southwest bay, set back from Brannan -----
    # LiDAR median 11.19 m over that bay; the Ritch elevation photographs show
    # the parapet stepping UP toward the rear, which is where this sits.
    roof_box("swbay", 4.2, 13.6, Z_DECK - 0.4, Z_SW_DECK, 7.4, 13.2, slate, mat_caps=stone)
    roof_coping("swbay_cap", 4.2, 13.6, 7.4, 13.2, Z_SW_DECK - 0.20, Z_SW_CAP, 0.34, steel)

    # --- the roof monitor over the middle bay -------------------------------
    # 8.3 m of frontage wide, inset 6.0 m from Brannan, running to 1 m short of
    # the rear wall. A daylight monitor over the sanctuary's timber trusses.
    MON_U, MON_V = 12.45, 13.14
    MON_SU, MON_SV = 7.90, 14.28
    roof_box("monitor", MON_U, MON_V, Z_MON0, Z_MON_DECK, MON_SU, MON_SV, slate,
             mat_caps=stone)
    roof_coping("monitor_cap", MON_U, MON_V, MON_SU, MON_SV,
                Z_MON_DECK - 0.22, Z_CREST, 0.34, steel)
    # clerestory lights down both long sides, lit at night
    for k in range(4):
        v = MON_V - MON_SV / 2.0 + 2.4 + k * 3.1
        for side, du in (("a", MON_SU / 2.0 + 0.04), ("b", -MON_SU / 2.0 - 0.04)):
            roof_box(f"mon_cler{k}{side}_fill", MON_U + du, v,
                     Z_MON_DECK - 1.55, Z_MON_DECK - 0.35, 0.12, 2.1, glass)
            roof_box(f"mon_cler{k}{side}_glow", MON_U + du * 1.02, v,
                     Z_MON_DECK - 1.45, Z_MON_DECK - 0.45, 0.10, 1.9, gglow)

    # --- roof furniture: on the NE bay's deck, grouped toward the block ------
    roof_box("mech_pad", 20.3, 12.4, Z_DECK, Z_DECK + 0.14, 6.4, 5.2, steel)
    roof_box("mech_a", 19.0, 11.4, Z_DECK + 0.14, Z_DECK + 0.99, 1.8, 1.3, trim)
    roof_box("mech_b", 21.4, 12.8, Z_DECK + 0.14, Z_DECK + 0.76, 1.2, 1.0, trim)
    roof_box("mech_c", 20.0, 14.6, Z_DECK + 0.14, Z_DECK + 1.19, 0.9, 0.9, trim)
    roof_box("duct", 22.1, 15.4, Z_DECK + 0.2, Z_DECK + 0.45, 0.6, 2.2, steel)
    roof_box("hatch", 18.0, 18.6, Z_DECK, Z_DECK + 0.45, 1.4, 1.1, roofd)
    roof_box("skylight_kerb", 21.6, 8.0, Z_DECK, Z_DECK + 0.22, 2.2, 2.2, steel)
    roof_box("skylight_fill", 21.6, 8.0, Z_DECK + 0.22, Z_DECK + 0.30, 1.8, 1.8, glass)
    roof_box("vent_stack", 6.0, 19.4, Z_SW_DECK, Z_SW_DECK + 1.15, 0.55, 0.55, steel)
    roof_box("sw_mech", 3.0, 17.0, Z_SW_DECK, Z_SW_DECK + 0.7, 1.5, 1.1, trim)

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.12/2; frames get a token 1-segment softening; fills, glow shells and the
    # hairline fascia strips get none, which is what keeps this under the cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        base = obj.name.split(".")[0]
        if "_fill" in base or "_glow" in base or base.startswith("pent_fascia"):
            continue
        if base.endswith("_frame") or base.startswith(("bran_sill", "ritch_sill")):
            bevel(obj, width=0.05, segments=1)
        elif base.startswith("pent_") or "_balc" in base or base.endswith("_louvre"):
            bevel(obj, width=0.04, segments=1)
        else:
            bevel(obj, width=0.12, segments=2)

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
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    print("[build] anchor lon/lat: -122.3948685 37.7799308 (parcel AABB centre)")
    print("[build] Brannan front heading 135.2 deg; Ritch front heading 225.2 deg")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "414-brannan.blend")
    glb = os.path.join(out, "414-brannan.glb")
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
