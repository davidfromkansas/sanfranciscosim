"""Deterministic Blender build of the SF-SIM miniature 150 South Park.

    blender -b --python build_150_south_park.py -- [--out DIR]

Writes 150-south-park.blend and 150-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading - the
loader applies no rotation. Origin = footprint area centroid (anchor
lon -122.3947673, lat 37.7813810), min Z = 0, front parapet crest exactly 8.0 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured DataSF LiDAR footprint (mblr SF3775065) - a WEDGE, 5.54 m wide at
  South Park Street and 9.72 m at the rear over an 18.7 m depth, because South
  Park Street curves around the west tip of the oval while the party walls stay
  on the old rectilinear lot lines. The taper is entirely on the south-west
  side: the north-east party wall is dead straight for its whole 18.57 m and the
  south-west wall kinks 26 deg, 6.6 m from the back. Building a symmetric taper
  would look right in plan and wrong in every elevation;
* the 2017-18 re-face, which is the building anyone recognises: a near-black
  painted-brick upper storey (Toy_ink) sitting directly on a bright white stucco
  ground floor (Toy_white), split hard at 4.55 m. That value split is the whole
  silhouette at diorama scale, and it is the exact INVERSE of 155 South Park
  across the oval - which is why both are worth having in the row;
* the identity features, carried hard: two oxblood-framed square windows on the
  5.54 m front (the only warm colour on the building), the flat black steel
  canopy on its two diagonal rod stays with a gooseneck lamp outboard of each
  end, and the vertically stacked "150" numerals on white stucco;
* no ornament anywhere else. This is a 1959 utility building with a designer
  re-face, standing between an Edwardian front with a bracketed cornice (140)
  and a 1925 industrial front (156). Its plainness IS the recognition cue and
  adding a cornice or a coping band would erase it;
* night state: the shopfront is the hero glow - warm gold under the canopy, the
  one lit ground floor at the head of the park - plus BOTH upper windows lit
  cool, because that floor is a live/work unit (2017 permits) and a home with
  one window lit and one dark reads as an office. The rear does not glow; a back
  yard that lights up would misread. Glow surfaces are thin shells proud of the
  opaque glazing (the app renders _Glow in a separate layer that is ~12% alpha
  by day - never author a primary surface as glow);
* a roof designed for the app's downward camera without inventing plant the
  permit record does not contain: a slim steel coping ring over a dark deck so
  the parapet reads from above, three skylights spaced down the long axis to
  draw the eye along the taper, and one vent cluster. Nothing above 7.9 m, so
  the parapet - not a vent - sets the bounding-box top.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# Local tangent projection, AGENTS.md "Coordinate & data conventions".
LAT0, LON0 = 37.77, -122.4375
ANCHOR_LON, ANCHOR_LAT = -122.3947673, 37.7813810

# DataSF building footprint SF3775065 (dataset ynuv-fyni), survey order. The
# three near-coincident nodes around the street's south-west corner (0.19 m
# apart) collapse to one in dedupe(); everything else is the survey ring.
FOOTPRINT_LONLAT = [
    (-122.39469491, 37.78130676),
    (-122.394696544, 37.781307282),
    (-122.394829315, 37.781356303),
    (-122.394876289, 37.781402937),
    (-122.394797855, 37.781464817),
    (-122.394652026, 37.781343474),
    (-122.39469381, 37.781308462),
]

Z_ROOF = 7.50        # roof deck: DataSF LiDAR modal cell 7.48 m (measured)
# Parapet crest -> the bbox top, must land exactly. It runs at one height the
# whole way round: the plan's 2.7 step 9 proposed a lower rear parapet, but
# neither the frontage nor the Taber Place photograph shows a step, and
# fabricating one would be invention. Recorded in REPORT.md.
Z_CREST = 8.00
# The black/white junction. NOT the second-floor line: it is a finish line with
# a projecting drip, and the Jan 2025 photograph puts it at ~58% of the wall's
# pixel height, which after the pano's tan expansion is ~4.5-4.9 m rather than
# the ~3.8 m a storey count would suggest. The plan's 2.7 assumed 3.80 m from
# the storey reading; the photograph overrules it. Recorded in REPORT.md.
Z_SPLIT = 4.55
Z_LIP = 0.10         # white drip lip above the split

Z_CAN0, Z_CAN1 = 3.60, 3.85   # canopy slab
Z_W0, Z_W1 = 5.15, 6.50       # upper windows (and the rear window band)

SKIN = 0.06          # the white ground-floor skin stands this far proud

PALETTE_HEX = {
    "Toy_ink": "3a3530",
    "Toy_white": "f7f4ec",
    # Deliberate palette extension. The window frames are a dark warm brown-red;
    # Toy_rust (a86444) is too orange and too light on a 0.25 m frame and
    # Toy_coral far too saturated. Documented as a WARN in REPORT.md, exactly as
    # 155 South Park's Toy_peach and 380 Brannan's Toy_slate were.
    "Toy_oxblood": "7a4034",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_gold_Glow": "caa64a",
    "Toy_glass_Glow": "6f95b8",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


# ------------------------------------------------------ footprint derivation


def project(lon, lat):
    return (
        (lon - LON0) * 111320.0 * math.cos(math.radians(LAT0)),
        (lat - LAT0) * 110540.0,
    )


def dedupe(poly, tol=0.5):
    out = []
    for p in poly:
        if not out or math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) > tol:
            out.append(p)
    if len(out) > 1 and math.hypot(out[0][0] - out[-1][0], out[0][1] - out[-1][1]) <= tol:
        out.pop()
    return out


def signed_area(poly):
    n = len(poly)
    return (
        sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
        / 2.0
    )


def area_centroid(poly):
    n = len(poly)
    a2 = cx = cy = 0.0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        cr = x1 * y2 - x2 * y1
        a2 += cr
        cx += (x1 + x2) * cr
        cy += (y1 + y2) * cr
    a2 /= 2.0
    return (cx / (6.0 * a2), cy / (6.0 * a2))


_ax, _ay = project(ANCHOR_LON, ANCHOR_LAT)
_ring = dedupe([project(lon, lat) for lon, lat in FOOTPRINT_LONLAT])
_c = area_centroid(_ring)
assert math.hypot(_c[0] - _ax, _c[1] - _ay) < 0.05, "anchor is not the footprint centroid"
FOOT = [(x - _ax, y - _ay) for x, y in _ring]
if signed_area(FOOT) < 0:
    FOOT.reverse()  # the build assumes CCW: poly_edge's outward normal depends on it
# Rotate so index 0 is the rear north-east corner, which fixes the edge indices
# below to the elevations they name.
_start = max(range(len(FOOT)), key=lambda i: FOOT[i][1])
FOOT = FOOT[_start:] + FOOT[:_start]

E_REAR = 0    #  9.72 m, faces NW 315.2 deg - the rear yard and Taber Place
E_SW_R = 1    #  6.60 m, party wall with 156 South Park, rear run
E_SW_F = 2    # 13.04 m, party wall with 156 South Park, front run
E_FRONT = 3   #  5.54 m, faces SE 133.1 deg - South Park Street, the hero face
E_NE = 4      # 18.57 m, party wall with 140 South Park, one straight run


# --------------------------------------------------------------- 2D helpers


def poly_edge(poly, i):
    """Edge i of poly: (origin, length, tangent unit, outward normal)."""
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def offset_polygon(poly, d):
    """Miter offset of a convex CCW footprint; positive d moves outward."""
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


# The lot's own frame, taken from the north-east party wall (the one straight
# run in the footprint): +v points toward South Park Street, +u toward 140 South
# Park. Used only to place roof furniture on the building's own grid.
_a, _len_ne, _t_ne, _n_ne = poly_edge(FOOT, E_NE)
VDIR = (-_t_ne[0], -_t_ne[1])      # NE wall runs rear-ward, so negate for street-ward
UDIR = (_n_ne[0], _n_ne[1])


def to_world(u, v):
    return (u * UDIR[0] + v * VDIR[0], u * UDIR[1] + v * VDIR[1])


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


def bevel(obj, width=0.10, segments=2):
    """Miniature-style edge softening (style bible s.4). The width is capped at
    a third of the object's thinnest dimension: the applied panels here are
    40-250 mm thick and a flat bevel on those collapses opposing profiles into
    zero-area slivers even with clamp_overlap."""
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


def face_panel(name, poly, edge, u_centre, profile, d0, d1, mat):
    """Closed prism of a (u, z) profile lying in the plane of wall `edge`,
    extruded outward from offset d0 to d1 along that wall's normal."""
    a, _length, t, n = poly_edge(poly, edge)
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


def strut(name, p0, p1, r, mat):
    """Square-section rod between two 3D points. face_panel cannot express a
    member that runs out AND up at once, and the canopy's two tension stays do
    exactly that - modelled as an L they read as coat hooks."""
    ax = Vector(p1) - Vector(p0)
    n = ax.normalized()
    up = Vector((0.0, 0.0, 1.0))
    if abs(n.dot(up)) > 0.95:
        up = Vector((1.0, 0.0, 0.0))
    e1 = n.cross(up).normalized() * r
    e2 = n.cross(e1).normalized() * r
    verts = []
    for p in (Vector(p0), Vector(p1)):
        for s1, s2 in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            verts.append(tuple(p + e1 * s1 + e2 * s2))
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


def wall_point(poly, edge, u, d, z):
    """3D point on wall `edge`: u along it from its origin, d out along its
    normal, z up."""
    a, _length, t, n = poly_edge(poly, edge)
    return (a[0] + t[0] * u + n[0] * d, a[1] + t[1] * u + n[1] * d, z)


def lot_box(name, u, v, z0, z1, su, sv, mat):
    """Box on the lot's own grid: centre at (u, v), sides su across the lot and
    sv along it, rotated with the building."""
    cx, cy = to_world(u, v)
    corners = []
    for lu, lv in ((-su / 2, -sv / 2), (su / 2, -sv / 2), (su / 2, sv / 2), (-su / 2, sv / 2)):
        dx, dy = to_world(lu, lv)
        corners.append((cx + dx, cy + dy))
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


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


# --------------------------------------------------------------------- parts


def rect_opening(tag, poly, edge, u, w, z0, z1, frame_mat, fill_mat, base=0.0, glow_mat=None):
    """Frame panel + a smaller fill that protrudes further, so the frame reads
    as a border ring around a recessed opening. No booleans, all closed solids."""
    face_panel(f"{tag}_frame", poly, edge, u, rect_profile(w, z0, z1), 0.0, base + 0.05, frame_mat)
    inset = 0.14
    face_panel(
        f"{tag}_fill",
        poly,
        edge,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        0.0,
        base + 0.11,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.26
        face_panel(
            f"{tag}_glow",
            poly,
            edge,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            base + 0.08,
            base + 0.15,
            glow_mat,
        )


def punched_window(tag, poly, edge, u, w, z0, z1, frame, glass, base=0.0, glow_mat=None):
    """The building's signature upper opening: a square-ish light in a thick
    oxblood frame with a matching sill. Two of these on a 5.54 m front are the
    only warm colour on the building, so the frame is deliberately over-thick
    (0.25 m, 0.09 m proud) to survive at thumbnail size."""
    face_panel(f"{tag}_frame", poly, edge, u, rect_profile(w, z0, z1), 0.0, base + 0.09, frame)
    face_panel(
        f"{tag}_sill", poly, edge, u, rect_profile(w + 0.22, z0 - 0.13, z0), 0.0, base + 0.17, frame
    )
    face_panel(
        f"{tag}_light",
        poly,
        edge,
        u,
        rect_profile(w - 0.34, z0 + 0.17, z1 - 0.17),
        0.0,
        base + 0.14,
        glass,
    )
    if glow_mat is not None:
        face_panel(
            f"{tag}_glow",
            poly,
            edge,
            u,
            rect_profile(w - 0.56, z0 + 0.28, z1 - 0.28),
            base + 0.11,
            base + 0.18,
            glow_mat,
        )


# The address numerals are STACKED VERTICALLY on the white wall between the
# display window and the entrance door - a 0.28 m wide, 0.86 m tall column in
# the Jan 2025 photograph. Built from bars in a 0.40 x 0.34 m glyph box (the
# stroke is exaggerated from ~25 mm to 60 mm, and the column from 0.86 m to
# 1.04 m, so a listed recognition cue survives at thumbnail size). A font object
# would not be deterministic across machines and a traced outline would cost ten
# times the triangles. Each bar is (du, dz, w, h) in metres.
BAR = 0.06
GLYPHS = {
    "1": [(0.05, 0.0, BAR, 0.34), (-0.04, 0.14, 0.11, BAR)],
    "5": [
        (0.0, 0.14, 0.34, BAR),
        (-0.14, 0.07, BAR, 0.20),
        (0.0, -0.01, 0.34, BAR),
        (0.14, -0.08, BAR, 0.19),
        (0.0, -0.14, 0.34, BAR),
    ],
    "0": [
        (0.0, 0.14, 0.34, BAR),
        (0.0, -0.14, 0.34, BAR),
        (-0.14, 0.0, BAR, 0.34),
        (0.14, 0.0, BAR, 0.34),
    ],
}


def numerals_stacked(text, poly, edge, u_centre, z_top, mat, base=0.0, pitch=0.36):
    z = z_top
    for ch in text:
        for k, (du, dz, w, h) in enumerate(GLYPHS[ch]):
            face_panel(
                f"num_{ch}_{k}_{z:.2f}",
                poly,
                edge,
                u_centre + du,
                rect_profile(w, z + dz - h / 2, z + dz + h / 2),
                base,
                base + 0.035,
                mat,
            )
        z -= pitch


# --------------------------------------------------------------------- build


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    ink = material("Toy_ink")
    white = material("Toy_white")
    oxblood = material("Toy_oxblood")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    gglow = material("Toy_gold_Glow")
    wglow = material("Toy_glass_Glow")

    len_front = poly_edge(FOOT, E_FRONT)[1]
    len_rear = poly_edge(FOOT, E_REAR)[1]
    mid = len_front / 2.0

    # --- the one mass: painted brick, the wedge, roof deck on top -----------
    prism("shell", FOOT, 0.0, Z_ROOF, ink, mat_caps=roofd)

    # --- parapet: plain brick with a slim steel coping. The real building has
    # --- no cornice and no coping band, and that plainness next to 140's
    # --- bracketed cornice is a recognition cue - but a parapet on a painted
    # --- brick building does carry metal flashing, and it is what makes the
    # --- ring read against the deck from the app's downward camera. ----------
    # The coping ring sets the bounding-box top and must land exactly on Z_CREST.
    ring_band("parapet", FOOT, Z_ROOF, Z_CREST - 0.09, -0.25, 0.0, ink)
    ring_band("coping", FOOT, Z_CREST - 0.09, Z_CREST, -0.30, 0.04, steel)

    # --- South Park Street front, ground floor: the white stucco base --------
    face_panel(
        "stucco", FOOT, E_FRONT, mid, rect_profile(len_front, 0.0, Z_SPLIT), 0.0, SKIN, white
    )
    face_panel(
        "drip",
        FOOT,
        E_FRONT,
        mid,
        rect_profile(len_front, Z_SPLIT - Z_LIP, Z_SPLIT),
        0.0,
        SKIN + 0.07,
        white,
    )
    # The white returns ~0.7 m down each party wall so the base does not read as
    # a decal when the aerial camera swings off square.
    for tag, edge in (("ne", E_NE), ("sw", E_SW_F)):
        L = poly_edge(FOOT, edge)[1]
        u0 = 0.35 if edge == E_NE else L - 0.35
        face_panel(
            f"stucco_return_{tag}",
            FOOT,
            edge,
            u0,
            rect_profile(0.70, 0.0, Z_SPLIT),
            0.0,
            SKIN,
            white,
        )

    # u runs from the south-west corner, which is the viewer's LEFT from the
    # street. Layout measured off the Jan 2025 frontage photograph.
    # Every u and z below is scaled off the Jan 2025 frontage photograph against
    # the measured 5.54 m frontage (94.8 px/m horizontally). The four ground-
    # floor elements tile the front with white between them, which is what the
    # building actually does; the plan's 2.7 spacing was a guess and is wrong.
    rect_opening("sidedoor", FOOT, E_FRONT, 0.66, 0.90, 0.0, 2.05, ink, ink, base=SKIN)
    rect_opening(
        "shopwin", FOOT, E_FRONT, 2.79, 1.89, 0.40, 2.75, ink, glass, base=SKIN, glow_mat=gglow
    )
    rect_opening(
        "entry", FOOT, E_FRONT, 4.88, 0.90, 0.0, 2.75, ink, glass, base=SKIN, glow_mat=gglow
    )
    # The entrance leaf is divided by a transom bar at ~2.10 m.
    face_panel(
        "entry_bar",
        FOOT,
        E_FRONT,
        4.88,
        rect_profile(0.90, 2.06, 2.14),
        0.0,
        SKIN + 0.14,
        ink,
    )
    numerals_stacked("150", FOOT, E_FRONT, 4.08, 2.47, ink, base=SKIN + 0.02, pitch=0.36)

    # --- the flat black canopy, its two rod stays and the gooseneck lamps ----
    face_panel(
        "canopy",
        FOOT,
        E_FRONT,
        2.61,
        rect_profile(3.00, Z_CAN0, Z_CAN1),
        0.0,
        SKIN + 0.95,
        roofd,
    )
    for i, u in enumerate((1.35, 3.85)):
        strut(
            f"stay{i}",
            wall_point(FOOT, E_FRONT, u, SKIN, 4.32),
            wall_point(FOOT, E_FRONT, u, SKIN + 0.88, Z_CAN1),
            0.035,
            steel,
        )
    # Gooseneck lamps sit OUTBOARD of the canopy, one over each door.
    for i, u in enumerate((0.60, 4.87)):
        face_panel(
            f"lamp{i}_arm",
            FOOT,
            E_FRONT,
            u,
            rect_profile(0.09, 3.62, 3.72),
            SKIN,
            SKIN + 0.40,
            roofd,
        )
        face_panel(
            f"lamp{i}_shade",
            FOOT,
            E_FRONT,
            u,
            rect_profile(0.34, 3.40, 3.64),
            SKIN + 0.28,
            SKIN + 0.44,
            roofd,
        )

    # --- the two upper windows: the only warm colour on the building ---------
    for i, u in enumerate((1.40, 4.31)):
        punched_window(
            f"w{i}", FOOT, E_FRONT, u, 1.15, Z_W0, Z_W1, oxblood, glass, glow_mat=wglow
        )

    # --- rear (Taber Place): the same wall, one band of two lights -----------
    # 5.40 m of a 9.72 m wall: the Jan 2025 pano shows the band running most of
    # the way across, and the aerial camera reads this face over the rear yard.
    # The wall BELOW the band is left deliberately blank - the 3 m fence hid it
    # in the only photograph there is, and inventing a door would be worse than
    # admitting the gap. It is this model's weakest surface (REPORT.md).
    punched_window(
        "rear", FOOT, E_REAR, len_rear / 2.0, 5.40, Z_W0, Z_W1 + 0.15, oxblood, glass
    )

    # --- flanks: party walls, hard up against 140 and 156 for their whole
    # --- length. No windows, no light wells - there is no gap on either side.

    # --- roof: the surface the app's camera sees most. Three skylights spaced
    # --- down the long axis so they draw the eye along the taper, one vent
    # --- cluster, nothing above 7.9 m. ---------------------------------------
    for i, (u, v) in enumerate(((1.40, 5.60), (0.40, 0.40), (-0.70, -4.60))):
        lot_box(f"skylight{i}_kerb", u, v, Z_ROOF, Z_ROOF + 0.16, 1.30, 1.00, steel)
        lot_box(f"skylight{i}", u, v, Z_ROOF + 0.13, Z_ROOF + 0.32, 1.06, 0.80, glassl)
    lot_box("vent_a", 2.40, -6.40, Z_ROOF, Z_ROOF + 0.50, 0.48, 0.48, steel)
    lot_box("vent_b", 1.55, -7.10, Z_ROOF, Z_ROOF + 0.38, 0.38, 0.38, steel)
    lot_box("hatch", -2.30, -6.60, Z_ROOF, Z_ROOF + 0.34, 1.20, 0.95, roofd)

    # Bevel budget: the shell and the parapet carry the miniature read and get
    # the full 0.10/2. Applied panels are small and numerous - frames get a
    # token 1-segment softening, and fills, glow shells and numerals none at
    # all, which is what keeps this under the 6,000-triangle cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.startswith("num_") or obj.name.endswith(("_fill", "_glow", "_light")):
            continue
        if obj.name.endswith(("_frame", "_sill", "_arm", "_shade")) or obj.name.startswith(
            ("stay", "drip", "stucco_return")
        ):
            bevel(obj, width=0.04, segments=1)
        else:
            bevel(obj, width=0.10, segments=2)

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
    print(f"[build] footprint edges={[round(poly_edge(FOOT, i)[1], 2) for i in range(len(FOOT))]}")
    print(f"[build] anchor lon/lat: {ANCHOR_LON} {ANCHOR_LAT} (footprint area centroid)")
    print("[build] South Park front heading: 133.1 deg true (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "150-south-park.blend")
    glb = os.path.join(out, "150-south-park.glb")
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
