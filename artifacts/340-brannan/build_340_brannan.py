"""Deterministic Blender build of the SF-SIM miniature 340 Brannan Street.

    blender -b --python build_340_brannan.py -- [--out DIR]

Writes 340-brannan.blend and 340-brannan.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint centroid (anchor lon -122.3932324,
lat 37.7812786), min Z = 0, roof-penthouse crest exactly 17.79 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured DataSF LiDAR footprint (mblr SF3775015), reduced to its four real
  corners — every one of the survey's eleven vertices lies within 0.12 m of this
  quadrilateral, so the extra points are noise, not corners. 29.25 x 28.22 m,
  ~45 deg off the world axes like the whole SoMa grid;
* a SAGE / GRAY-GREEN STUCCO slab (Page & Turnbull's National Register form says
  stucco over reinforced concrete) — deliberately not the brick of 380 Brannan
  and not the white concrete of 350 Brannan across the alley, which are the two
  easiest mistakes to make on this block;
* FOUR window lines, not the five storeys of the paperwork: a 4.60 m recessed
  ground floor plus three 3.40 m floors lands the roof deck on 14.80 m, within
  2 cm of the measured 14.82 m LiDAR median. Photography agrees;
* the identity features: (a) the RAISED CENTRAL PARAPET with chamfered shoulders
  on the Brannan front, on a street of dead-flat parapets, and (b) the DEEPLY
  RECESSED BRONZE GROUND FLOOR under a continuous light fascia — a hard shadow
  line at one height across both finished faces;
* exactly two finished elevations (Brannan SE, Jack London Alley SW) and two
  blind party walls (NE against 334 Brannan at 12.14 m, NW against the Gran
  Oriente Filipino block at 7.84/10.49 m). Both party walls stand ~3-7 m proud
  of their neighbours, so they are modelled flat and left to show;
* night state: the lit lobby band under the fascia as hero glow, the "340" sign
  panel behind the opaque numerals, and a restrained scatter of lit windows.
  Glow surfaces are thin shells proud of the opaque geometry (the app renders
  _Glow in a separate layer that is ~12% alpha per layer by day — never author a
  primary surface as glow, and never wrap one in a closed shell);
* a designed roof for the app's downward camera, and unusually for this block it
  has real content: the stair/elevator penthouse that sets the 17.79 m crest, the
  open trellis frame over the atrium, two round cooling towers (permit
  2010-10-20, replaced in place), and the timber roof deck (permit 1987-10-22,
  460 sq ft).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF building footprint SF3775015 projected with the app's tangent
# projection, recentred on the footprint centroid and reduced to four corners.
# CCW, so outward normal = (t.y, -t.x).
FOOTPRINT = [
    (-20.281, -0.177),   # west corner
    (-0.396, -20.202),   # south corner — Brannan x Jack London Alley
    (20.429, 0.339),     # east corner
    (0.267, 20.139),     # north corner
]

EDGE_SW = 0      # 28.22 m, faces SW 225.2 deg — Jack London Alley
EDGE_FRONT = 1   # 29.25 m, faces SE 135.4 deg — Brannan Street
EDGE_NE = 2      # 28.26 m, faces NE  44.5 deg — party wall, blind
EDGE_NW = 3      # 28.90 m, faces NW 315.3 deg — party wall, blind

FINISHED = (EDGE_FRONT, EDGE_SW)

Z_DECK = 14.82       # roof deck / top of the body (LiDAR median 14.82)
Z_PARAPET = 15.45    # main parapet crest (inferred: deck + 0.63)
Z_PARAPET_HI = 16.35 # raised central section on the Brannan front
Z_CREST = 17.79      # roof penthouse top = LiDAR max 17.79 -> the bbox top

Z_G_TOP = 4.60       # ground-floor ceiling / underside of the fascia
Z_FASCIA = 5.05      # top of the light fascia band
RECESS = 1.20        # ground-floor setback on the two finished elevations

# Upper-floor window bands. Ground 4.60 + 3 x 3.20 floors = 14.20, plus a
# 0.62 m blank frieze under the parapet = the measured 14.82 m deck. The frieze
# matters: every photograph shows clear wall between the top window head and the
# roofline, and without it the top row runs straight into the coping.
Z_W = ((5.80, 7.65), (9.00, 10.85), (12.20, 14.05))
Z_REVEAL = (8.30, 11.50)   # scored horizontal reveals in the stucco

SKIN = 0.10          # applied-panel standoff from the wall plane
PARAPET_T = 0.35     # parapet wall thickness

PALETTE_HEX = {
    # Two deliberate palette extensions, both a WARN and not a FAIL under the
    # contract, both with precedent (380-brannan's Toy_slate, 140-south-park's
    # Toy_olive, 155-south-park's Toy_peach).
    "Toy_sage": "8d9082",    # the stucco body: mid gray-green, olive in sun
    "Toy_bronze": "5a4a3a",  # dark anodized storefront framing
    "Toy_trim": "f3efe6",    # fascia band, parapet cap, window surrounds
    "Toy_stone": "d9d2c2",   # roof membrane — light, as the real one is
    "Toy_glass": "2a4d73",   # punched office windows, storefront glazing
    "Toy_glassl": "6f95b8",  # skylights, atrium glazing
    "Toy_rust": "a86444",    # penthouse roof slab, roof deck, entrance pier
    "Toy_steel": "9aa0a6",   # cooling towers, eyebrow canopy, trellis
    "Toy_roofd": "45454a",   # service door, mechanical plinth
    "Toy_ink": "3a3530",     # recess back wall, entrance reveal, scored reveals
    "Toy_white": "f7f4ec",   # the "340" numerals
    # Glow colours are the LIT appearance, not the day colour: a night window
    # that glows in its own dark navy reads as a hole.
    "Toy_glass_Glow": "6f95b8",
    "Toy_white_Glow": "f7f4ec",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def poly_edge(i, poly=None):
    """Edge i of `poly`: (origin, length, tangent unit, outward normal)."""
    poly = FOOTPRINT if poly is None else poly
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def offset_polygon(poly, d):
    """Miter offset of the convex CCW footprint; positive d moves outward."""
    return offset_polygon_per_edge(poly, [d] * len(poly))


def offset_polygon_per_edge(poly, ds):
    """Miter offset with a separate distance per edge (positive = outward).

    Each edge line is pushed along its own outward normal and the offset
    vertices are the intersections of consecutive pushed lines — which is what
    lets the ground floor step back on the two finished elevations only while
    the party walls stay flush on the survey line.
    """
    npts = len(poly)
    normals = []
    for i in range(npts):
        normals.append(poly_edge(i, poly)[3])
    out = []
    for i in range(npts):
        n1, n2 = normals[i - 1], normals[i]
        d1, d2 = ds[i - 1], ds[i]
        v = poly[i]
        det = n1[0] * n2[1] - n1[1] * n2[0]
        if abs(det) < 1e-6:
            out.append((v[0] + n2[0] * d2, v[1] + n2[1] * d2))
            continue
        c1 = v[0] * n1[0] + v[1] * n1[1] + d1
        c2 = v[0] * n2[0] + v[1] * n2[1] + d2
        out.append(((c1 * n2[1] - c2 * n1[1]) / det, (c2 * n1[0] - c1 * n2[0]) / det))
    return out


def rect_profile(w, z0, z1):
    a = w / 2.0
    return [(-a, z0), (a, z0), (a, z1), (-a, z1)]


def ramp_profile(w, z0, z1, ramp):
    """Trapezoid: a raised band with chamfered shoulders at both ends.

    This is the building's silhouette signature — the Brannan parapet steps up
    across the middle of the facade and ramps back down at each end.
    """
    a = w / 2.0
    return [(-a, z0), (a, z0), (a - ramp, z1), (-a + ramp, z1)]


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

    Width is capped at a third of the object's thinnest dimension: the applied
    panels here are 70-230 mm thick and a flat 0.12 m bevel on those relies
    entirely on clamp_overlap, which collapses opposing profiles into zero-area
    slivers. The 1 mm remove_doubles/dissolve_degenerate pass afterwards sweeps
    up whatever clamping still pinches shut — a sliver with opposing face
    normals averages its shared vertex normal to zero, which fails the contract
    validator once gltfpack re-emits the stored normals.
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
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-3)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-3, edges=list(bm.edges))
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


def face_panel(name, edge, u_centre, profile, d0, d1, mat, poly=None):
    """Closed prism of a (u, z) profile lying in the plane of wall `edge`,
    extruded outward from offset d0 to d1 along that wall's normal."""
    a, _length, t, n = poly_edge(edge, poly)
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


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0):
    """Box with local +x along yaw and local +y 90 deg ccw of it."""
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
    return new_mesh(name, verts, faces, [mat])


def roof_uv(u, v):
    """Roof-grid coordinates: u runs along the Brannan edge from its south
    corner, v runs INTO the block (against the outward normal). The footprint
    is 29.25 x 28.24 in this frame, so u,v in [3, 26] is always inside."""
    origin, _l, t, n = poly_edge(EDGE_FRONT)
    return (origin[0] + t[0] * u - n[0] * v, origin[1] + t[1] * u - n[1] * v)


def roof_yaw():
    _o, _l, t, _n = poly_edge(EDGE_FRONT)
    return math.atan2(t[1], t[0])


def roof_box(name, u, v, z0, z1, su, sv, mat):
    cx, cy = roof_uv(u, v)
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=roof_yaw())


def roof_cylinder(name, u, v, z0, z1, radius, mat, segments=12):
    cx, cy = roof_uv(u, v)
    ring = [
        (cx + radius * math.cos(2 * math.pi * k / segments),
         cy + radius * math.sin(2 * math.pi * k / segments))
        for k in range(segments)
    ]
    return prism(name, ring, z0, z1, mat)


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


def rect_opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None, poly=None):
    """Frame panel + a smaller fill that protrudes further, so the frame reads
    as a border ring around a recessed opening. No booleans, all closed solids."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, SKIN + 0.06,
               frame_mat, poly)
    inset = 0.18
    face_panel(f"{tag}_fill", edge, u,
               rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
               0.0, SKIN + 0.13, fill_mat, poly)
    if glow_mat is not None:
        g = 0.32
        face_panel(f"{tag}_glow", edge, u,
                   rect_profile(w - 2 * g, z0 + g, z1 - g),
                   SKIN + 0.10, SKIN + 0.17, glow_mat, poly)


# Upper-floor bay centres per finished elevation. Five bays each is the
# dossier's regularisation of the real window rhythm (plan 2.6); the two party
# walls get none.
UPPER_BAYS = {
    EDGE_FRONT: [4.05 + i * 5.29 for i in range(5)],
    EDGE_SW: [3.91 + i * 5.10 for i in range(5)],
}
WIN_W = {EDGE_FRONT: 3.60, EDGE_SW: 3.40}
# Restrained: six lit windows across three floors and two elevations.
LIT = {
    (EDGE_FRONT, 0): {1},
    (EDGE_FRONT, 1): {3},
    (EDGE_FRONT, 2): {0, 4},
    (EDGE_SW, 0): set(),
    (EDGE_SW, 1): {2},
    (EDGE_SW, 2): {1},
}

TAG = {EDGE_FRONT: "f", EDGE_SW: "sw"}


def numerals(u, z0, height, depth_back, mat, poly):
    """The white "340" address numerals, on the recessed wall above the lobby.

    Built from a Blender text object so the digits are real letterforms rather
    than a seven-segment approximation; converted to a mesh immediately so the
    export carries no font dependency.
    """
    a, _l, t, n = poly_edge(EDGE_FRONT, poly)
    bpy.ops.object.text_add(location=(0.0, 0.0, 0.0))
    txt = bpy.context.object
    txt.name = "numerals"
    txt.data.body = "340"
    txt.data.size = height
    txt.data.extrude = 0.09
    txt.data.align_x = "CENTER"
    txt.data.align_y = "CENTER"
    bpy.ops.object.convert(target="MESH")
    obj = bpy.context.object
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    # Stand the text up (its face normal goes from +Z to -Y), then swing -Y onto
    # the wall's outward normal.
    yaw = math.atan2(n[0], -n[1])
    obj.rotation_euler = (math.pi / 2.0, 0.0, yaw)
    obj.location = (
        a[0] + t[0] * u + n[0] * depth_back,
        a[1] + t[1] * u + n[1] * depth_back,
        z0 + height / 2.0,
    )
    bpy.context.view_layer.update()
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.select_set(False)
    obj.data.shade_flat()
    return obj


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials, bpy.data.curves):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    sage = material("Toy_sage")
    bronze = material("Toy_bronze")
    trim = material("Toy_trim")
    stone = material("Toy_stone")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    rust = material("Toy_rust")
    steel = material("Toy_steel")
    roofd = material("Toy_roofd")
    ink = material("Toy_ink")
    white = material("Toy_white")
    gglow = material("Toy_glass_Glow")
    wglow = material("Toy_white_Glow")

    # The ground floor steps back 1.20 m on the two finished elevations only;
    # the party walls stay on the survey line all the way down.
    ground_ds = [0.0] * 4
    ground_ds[EDGE_FRONT] = -RECESS
    ground_ds[EDGE_SW] = -RECESS
    GROUND = offset_polygon_per_edge(FOOTPRINT, ground_ds)

    # --- masses -------------------------------------------------------------
    # Lower block sits inside the upper one, so the upper block's bottom cap IS
    # the soffit over the recess — the hard shadow line that separates the light
    # body from the dark base.
    prism("base", GROUND, 0.0, Z_G_TOP, ink)
    prism("body", FOOTPRINT, Z_G_TOP, Z_DECK, sage, mat_caps=stone)

    # --- parapet ring + light coping ---------------------------------------
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET - 0.14, -PARAPET_T, 0.0, sage)
    ring_band("coping", FOOTPRINT, Z_PARAPET - 0.14, Z_PARAPET, -PARAPET_T - 0.07, 0.07, trim)

    len_front = poly_edge(EDGE_FRONT)[1]
    len_sw = poly_edge(EDGE_SW)[1]

    # --- THE SILHOUETTE: raised central parapet with chamfered shoulders -----
    # Between 18% and 80% of the Brannan frontage, +0.65 m over the main crest,
    # with 2.2 m ramps. Widened slightly from the photographs on purpose: this
    # is the one place this asset spends semantic exaggeration (plan 2.6), and
    # at the app's camera a true-proportion step is two pixels of nothing.
    hi_u0, hi_u1 = 0.18 * len_front, 0.80 * len_front
    # Built as an extra COURSE sitting on the coping rather than as a band
    # applied to the wall: a raised section that overlaps the coping either
    # z-fights with it or leaves a 50 mm slot between their inner faces, and
    # that slot ambient-occludes to pure black and reads from the aerial camera
    # as a painted stripe across the roof. Stacking it clear of the coping and
    # 0.02 m proud on each side gives the same street silhouette with no seam.
    face_panel(
        "parapet_raised", EDGE_FRONT, (hi_u0 + hi_u1) / 2.0,
        ramp_profile(hi_u1 - hi_u0, Z_PARAPET - 0.06, Z_PARAPET_HI - 0.12, 2.20),
        -PARAPET_T - 0.09, 0.09, sage,
    )
    face_panel(
        "parapet_raised_cap", EDGE_FRONT, (hi_u0 + hi_u1) / 2.0,
        ramp_profile(hi_u1 - hi_u0 + 0.16, Z_PARAPET_HI - 0.12, Z_PARAPET_HI, 2.28),
        -PARAPET_T - 0.16, 0.16, trim,
    )

    # --- the light fascia band under which the base hangs -------------------
    for edge, length in ((EDGE_FRONT, len_front), (EDGE_SW, len_sw)):
        face_panel(
            f"fascia_{TAG[edge]}", edge, length / 2.0,
            rect_profile(length - 0.30, Z_G_TOP, Z_FASCIA), -0.02, SKIN + 0.04, trim,
        )

    # --- Brannan ground floor: bronze storefront inside the recess -----------
    # Two horizontal glass strips separated by a metal rail, on mullions — the
    # 1985 remodel's system, read at miniature scale.
    gl_front = poly_edge(EDGE_FRONT, GROUND)[1]

    # Entrance: right of centre seen from the street (u grows from the alley
    # corner toward the northeast), recessed a further 0.55 m, with the dark
    # brick-clad pier on its northeast side. The storefront runs to either side
    # of it — a full-width glazing band would bury the entrance behind glass.
    U_DOOR = gl_front / 2.0 + 4.00
    DOOR_W = 4.20
    runs = [
        (0.60, U_DOOR - DOOR_W / 2.0),
        (U_DOOR + DOOR_W / 2.0, gl_front - 0.60),
    ]
    for k, (ua, ub) in enumerate(runs):
        uc, w = (ua + ub) / 2.0, ub - ua
        face_panel(f"sf_f_lower{k}", EDGE_FRONT, uc,
                   rect_profile(w - 0.30, 0.40, 2.20), 0.0, SKIN + 0.10, glass, GROUND)
        face_panel(f"sf_f_upper{k}", EDGE_FRONT, uc,
                   rect_profile(w - 0.30, 2.60, 4.10), 0.0, SKIN + 0.10, glass, GROUND)
        face_panel(f"sf_f_rail{k}", EDGE_FRONT, uc,
                   rect_profile(w, 2.20, 2.60), 0.0, SKIN + 0.18, bronze, GROUND)
        face_panel(f"sf_f_sill{k}", EDGE_FRONT, uc,
                   rect_profile(w, 0.0, 0.40), 0.0, SKIN + 0.18, bronze, GROUND)
        face_panel(f"sf_f_head{k}", EDGE_FRONT, uc,
                   rect_profile(w, 4.10, Z_G_TOP), 0.0, SKIN + 0.18, bronze, GROUND)
        n_mull = max(int(round(w / 3.90)), 1)
        for i in range(n_mull + 1):
            face_panel(f"sf_f_mull{k}{i}", EDGE_FRONT, ua + i * w / n_mull,
                       rect_profile(0.35, 0.0, Z_G_TOP), 0.0, SKIN + 0.20, bronze, GROUND)

    face_panel("entry_reveal", EDGE_FRONT, U_DOOR,
               rect_profile(DOOR_W, 0.0, Z_G_TOP), -0.55, SKIN + 0.02, ink, GROUND)
    face_panel("entry_doors", EDGE_FRONT, U_DOOR,
               rect_profile(3.00, 0.0, 3.10), SKIN + 0.02, SKIN + 0.10, glass, GROUND)
    face_panel("entry_canopy", EDGE_FRONT, U_DOOR,
               rect_profile(DOOR_W + 0.60, 3.55, 3.75), -0.10, SKIN + 0.85, steel, GROUND)
    face_panel("entry_pier", EDGE_FRONT, U_DOOR + 2.65,
               rect_profile(1.10, 0.0, Z_G_TOP), 0.0, SKIN + 0.22, rust, GROUND)

    # The "340" sign: an opaque numeral solid standing proud of a thin glow
    # plate, so the halo lights at night and the digits stay solid by day.
    U_SIGN = U_DOOR + 4.80
    face_panel("sign_glow", EDGE_FRONT, U_SIGN,
               rect_profile(3.90, 3.00, 4.40), SKIN + 0.20, SKIN + 0.27, wglow, GROUND)
    numerals(U_SIGN, 3.10, 1.20, SKIN + 0.30, white, GROUND)

    # Hero night glow: the lit lobby band under the fascia, restrained to the
    # central two-thirds of the Brannan front and two segments on the alley.
    # Three short segments, not one long band: a _Glow shell is ~12% alpha per
    # layer by DAY, so a 16 m panel across the whole base reads as milk in
    # daylight. Short bays give the same night read at a third of the day cost.
    for i, u in enumerate((gl_front * 0.16, gl_front * 0.36, U_DOOR)):
        face_panel(f"lobby_glow_f{i}", EDGE_FRONT, u,
                   rect_profile(3.40, 0.95, 3.30), SKIN + 0.12, SKIN + 0.19,
                   wglow, GROUND)

    # --- Jack London Alley ground floor -------------------------------------
    gl_sw = poly_edge(EDGE_SW, GROUND)[1]
    face_panel("sf_sw_glass", EDGE_SW, gl_sw / 2.0,
               rect_profile(gl_sw - 1.2, 0.90, 3.90), 0.0, SKIN + 0.10, glass, GROUND)
    face_panel("sf_sw_sill", EDGE_SW, gl_sw / 2.0,
               rect_profile(gl_sw - 1.0, 0.0, 0.90), 0.0, SKIN + 0.18, bronze, GROUND)
    face_panel("sf_sw_head", EDGE_SW, gl_sw / 2.0,
               rect_profile(gl_sw - 1.0, 3.90, Z_G_TOP), 0.0, SKIN + 0.18, bronze, GROUND)
    for i in range(6):
        u = 3.20 + i * 4.10
        face_panel(f"sf_sw_mull{i}", EDGE_SW, u,
                   rect_profile(0.35, 0.0, Z_G_TOP), 0.0, SKIN + 0.20, bronze, GROUND)
    # the one flush service door, near the northwest end
    face_panel("sw_door", EDGE_SW, gl_sw - 3.60,
               rect_profile(1.60, 0.0, 2.70), 0.0, SKIN + 0.14, roofd, GROUND)
    for i, u in enumerate((gl_sw * 0.30, gl_sw * 0.58)):
        face_panel(f"lobby_glow_sw{i}", EDGE_SW, u,
                   rect_profile(3.00, 1.30, 3.40), SKIN + 0.12, SKIN + 0.19, wglow, GROUND)

    # The flat metal eyebrow canopy over the alley glazing, hung off the wall
    # line rather than off the recessed glass.
    face_panel("eyebrow_sw", EDGE_SW, len_sw / 2.0,
               rect_profile(len_sw - 0.6, 4.30, 4.50), -0.25, 0.70, steel)

    # --- three upper floors of wide horizontal punched windows --------------
    for edge, bays in UPPER_BAYS.items():
        for f, (z0, z1) in enumerate(Z_W):
            for i, u in enumerate(bays):
                rect_opening(
                    f"{TAG[edge]}w{f}{i}", edge, u, WIN_W[edge], z0, z1, trim, glass,
                    gglow if i in LIT[(edge, f)] else None,
                )
                # one horizontal mullion per opening — the real windows are a
                # two-light horizontal division and nothing more
                face_panel(f"{TAG[edge]}m{f}{i}", edge, u,
                           rect_profile(WIN_W[edge] - 0.36, (z0 + z1) / 2 - 0.05,
                                        (z0 + z1) / 2 + 0.05),
                           SKIN + 0.08, SKIN + 0.15, trim)

    # --- scored horizontal reveals in the stucco ----------------------------
    # A shallow recess at each floor line, not separate coloured bands: the
    # tonal striping in the alley pano may simply be lighting (plan 2.15).
    for edge, length in ((EDGE_FRONT, len_front), (EDGE_SW, len_sw)):
        for z in Z_REVEAL:
            face_panel(f"reveal_{TAG[edge]}_{z:.0f}", edge, length / 2.0,
                       rect_profile(length - 0.30, z, z + 0.12), -0.06, 0.02, ink)

    # --- roof: the surface the app's camera sees most -----------------------
    # Everything clusters in the southwest half; the northeast half of the
    # membrane stays clean.
    roof_box("penthouse", 11.00, 15.00, Z_DECK, Z_CREST - 0.22, 9.00, 7.00, sage)
    roof_box("penthouse_cap", 11.00, 15.00, Z_CREST - 0.22, Z_CREST, 9.30, 7.30, rust)

    # the open trellis / atrium skylight frame
    roof_box("atrium_glass", 19.50, 15.00, Z_DECK + 0.10, Z_DECK + 0.45, 6.20, 4.20, glassl)
    for du, dv in ((-3.30, -2.30), (3.30, -2.30), (3.30, 2.30), (-3.30, 2.30)):
        roof_box(f"trellis_post{du:+.0f}{dv:+.0f}", 19.50 + du, 15.00 + dv,
                 Z_DECK, Z_DECK + 2.20, 0.25, 0.25, steel)
    roof_box("trellis_beam_a", 19.50, 12.70, Z_DECK + 2.00, Z_DECK + 2.20, 6.85, 0.25, steel)
    roof_box("trellis_beam_b", 19.50, 17.30, Z_DECK + 2.00, Z_DECK + 2.20, 6.85, 0.25, steel)
    for k in range(5):
        roof_box(f"trellis_rib{k}", 16.85 + k * 1.325, 15.00,
                 Z_DECK + 2.02, Z_DECK + 2.18, 0.18, 4.60, steel)

    # two cooling towers on a shared plinth (permit 2010-10-20)
    roof_box("ct_plinth", 4.20, 22.20, Z_DECK, Z_DECK + 0.30, 3.20, 6.60, roofd)
    roof_cylinder("cooling_tower_a", 4.20, 20.20, Z_DECK + 0.30, Z_DECK + 2.70, 1.10, steel)
    roof_cylinder("cooling_tower_b", 4.20, 24.20, Z_DECK + 0.30, Z_DECK + 2.70, 1.10, steel)
    roof_box("duct", 7.20, 22.20, Z_DECK + 0.35, Z_DECK + 0.75, 3.00, 0.80, steel)

    # the permitted 460 sq ft timber roof deck, southwest of the penthouse
    roof_box("roof_deck", 9.00, 6.20, Z_DECK, Z_DECK + 0.20, 8.00, 5.00, rust)
    roof_box("deck_rail_a", 9.00, 3.70, Z_DECK + 0.20, Z_DECK + 1.05, 8.00, 0.12, steel)
    roof_box("deck_rail_b", 5.00, 6.20, Z_DECK + 0.20, Z_DECK + 1.05, 0.12, 5.00, steel)

    # skylights near the west corner, and a hatch
    for i, v in enumerate((11.60, 14.60)):
        roof_box(f"skylight_kerb{i}", 4.00, v, Z_DECK, Z_DECK + 0.20, 2.20, 1.40, trim)
        roof_box(f"skylight{i}", 4.00, v, Z_DECK + 0.16, Z_DECK + 0.42, 1.95, 1.15, glassl)
    roof_box("roof_hatch", 15.60, 21.80, Z_DECK, Z_DECK + 0.55, 1.50, 1.20, roofd)
    roof_box("vent_a", 24.00, 20.00, Z_DECK, Z_DECK + 1.00, 0.60, 0.60, steel)
    roof_box("vent_b", 25.20, 8.80, Z_DECK, Z_DECK + 0.85, 0.50, 0.50, steel)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.12/2. Applied window panels are small and numerous — their frames
    # get a token 1-segment softening and the fills/glow shells none at all,
    # which is what keeps this under the 11,000-triangle cap. The numerals are
    # already dense letterforms and get nothing.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.startswith("numerals") or obj.name.endswith(("_fill", "_glow")):
            continue
        # Hairline strips — mullions, window mullions, scored reveals, trellis
        # members, deck rails — read as lines, not as chunky solids, and a bevel
        # on them costs 96 triangles apiece and buys nothing at city scale.
        if "_mull" in obj.name or obj.name.startswith(
            ("fm", "swm", "reveal_", "trellis_rib", "deck_rail")
        ):
            continue
        if obj.name.endswith("_frame") or obj.name.startswith(("trellis_", "cooling_tower")):
            bevel(obj, width=0.05, segments=1)
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
    print("[build] anchor lon/lat: -122.3932324 37.7812786 (footprint centroid)")
    print("[build] Brannan front heading: 135.4 deg true (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "340-brannan.blend")
    glb = os.path.join(out, "340-brannan.glb")
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
