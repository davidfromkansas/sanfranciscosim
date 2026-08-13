"""Deterministic Blender build of the SF-SIM miniature 101 South Park.

    blender -b --python build_101_south_park.py -- [--out DIR]

Writes 101-south-park.blend and 101-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = footprint OBB centre (anchor
lon -122.3937582, lat 37.7812624), min Z = 0, penthouse crest exactly 10.9 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured DataSF LiDAR footprint (mblr SF3775038), a 13.07 x 29.7 m
  parallelogram at 44.5 deg off the world axes like the whole SoMa grid, with
  only 13 m of frontage on the South Park oval and 29.6 m of depth behind it;
* a single charcoal volume — this building has almost no colour, and that
  restraint is its identity on a park ringed by pastel and brick neighbours;
* the identity feature: the row of tall WARM-OAK shopfront window bays at street
  level on the South Park front, deliberately over-framed so the one warm
  element survives at diorama scale. They are also the hero night glow;
* the recessed upper storey: a continuous ribbon window set 0.35 m back behind
  the plane of the front wall, so the coping and the two end piers read as a
  thin frame around a band of shadow. The recess depth is the effect — it is
  not a drawn panel, and because this asset is a union of closed solids with no
  booleans, the recess is made by building the REST of the front proud of it;
* night state: the full ground-floor oak window row lit warm, plus three lights
  in the upper ribbon. Nothing else glows — there is no signage and no crown.
  Glow surfaces are thin shells proud of the opaque glazing (the app renders
  _Glow in a separate layer that is ~12% alpha by day — never author a primary
  surface as glow);
* a designed roof for the app's downward camera: the real building carries a
  2014 four-ply "cool" roof, so the deck is near-white and reads in deliberate
  contrast with the dark walls. Skylight field, mechanical cluster and stair
  penthouse are grouped in the front third, matching 2026 satellite imagery;
  the penthouse sets the 10.9 m crest, one metre above the 10.0 m parapet.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

# ---------------------------------------------------------------- parameters

# DataSF building footprint SF3775038 projected with the app's tangent
# projection and recentred on the OBB centre, wound CCW.
#
# The survey draws the southwest boundary as four segments; they are collinear
# to within 0.18 m, so they are merged into one wall here, and the 0.077 m
# chamfer at the west corner is merged into a single vertex. The result is a
# clean quadrilateral of 378.2 m2 against the survey's 380.1 m2 (0.5%), which is
# far inside the contract's tolerances and much healthier for the bevel pass
# than four near-parallel walls. Recorded in REPORT.md.
FOOTPRINT = [
    (6.037, -15.039),    # south corner
    (15.195, -5.708),    # east corner
    (-5.419, 14.435),    # north corner
    (-14.967, 5.868),    # west corner
]

# Edge index -> elevation. Outward normals verified against the survey.
EDGE_REAR = 0    # 13.07 m, faces SE 134.4 deg — rear, toward Varney Place
EDGE_NE = 1      # 28.82 m, faces NE  44.3 deg — Jack London Alley side
EDGE_FRONT = 2   # 12.83 m, faces NW 318.3 deg — SOUTH PARK
EDGE_SW = 3      # 29.63 m, faces SW 224.9 deg — party wall with 117 South Park

# Stage-2 correction to the plan's single figure of 10.0 m (see REPORT.md).
# 10.0 m is the PARAPET crest — that is what the photogrammetric read off the
# January 2025 pano measures, and it is the height the building presents to the
# street. The asset's bounding box has to reach the tallest FEATURE, and the
# 2010 LiDAR maximum over this footprint is 10.92 m: a roof element that already
# stood a metre above the parapet. Splitting the two numbers this way makes both
# measurements consistent instead of forcing a choice between them, and it is
# the same parapet/crest split 380-brannan uses.
Z_DECK = 9.50        # roof deck / top of the body
Z_PARAPET = 10.00    # main parapet crest — the architectural height
Z_CREST = 10.90      # stair penthouse top = the bbox top, = targetHeightM
Z_GROUND_TOP = 4.60  # ground-floor ceiling line

Z_GWIN0, Z_GWIN1 = 0.85, 3.90   # oak shopfront bays
Z_DOOR1 = 2.95                  # oak entrance door head
Z_UWIN0, Z_UWIN1 = 6.00, 8.60   # upper ribbon window

RECESS = 0.35        # depth the upper ribbon sits behind the front plane
RIBBON_W = 11.00     # width of the recessed upper ribbon window
PARAPET_T = 0.30     # parapet wall thickness

PALETTE_HEX = {
    # Deliberate palette extension. The real wall is a dark warm gray; the
    # palette's Toy_ink (3a3530) is near-black and turned the whole building
    # into a silhouette in the first aerial, which is the exact failure mode
    # this asset has to avoid (see REPORT.md). 4a4540 keeps the warmth, keeps
    # the building clearly the darkest thing on its block, and still lets the
    # oak read.
    "Toy_charcoal": "4a4540",
    "Toy_rust": "a86444",     # the oak joinery — the one warm element
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_white": "f7f4ec",    # the 2014 "cool" roof membrane
    "Toy_steel": "9aa0a6",
    "Toy_roofd": "45454a",
    "Toy_ink": "3a3530",
    "Toy_trim": "f3efe6",     # the Kleiner Perkins wordmark and the 101 plate
    "Toy_rust_Glow": "c08a5a",
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
    """Miter offset of the convex CCW footprint; positive d moves outward."""
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

    The width is capped at a third of the object's thinnest dimension: the
    applied panels here are only 60-200 mm thick and a flat 0.12 m bevel on
    those relies entirely on clamp_overlap, which collapses opposing profiles
    into zero-area slivers. The remove_doubles/dissolve_degenerate pass sweeps
    up whatever clamping still pinches shut.
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


def face_panel(name, edge, u_centre, profile, d0, d1, mat):
    """Closed prism of a (u, z) profile lying in the plane of wall `edge`,
    extruded along that wall's outward normal from offset d0 to d1. Negative
    offsets cut INTO the building, which is how the upper ribbon's recess and
    the shopfront reveals are made."""
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


def roof_box(name, u, v, z0, z1, su, sv, mat):
    """Box on the roof, aligned to the building's own grid rather than to the
    world axes: u runs along the South Park front from its northeast end, v
    runs INTO the block (against the front's outward normal)."""
    origin, _l, t, n = poly_edge(EDGE_FRONT)
    cx = origin[0] + t[0] * u - n[0] * v
    cy = origin[1] + t[1] * u - n[1] * v
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=math.atan2(t[1], t[0]))


def lettering(name, edge, u_centre, z_base, text, cap_h, d0, d1, mat, weld_frac=0.09):
    """Extruded letterforms lying in the plane of wall `edge`, standing proud
    from offset d0 to d1.

    Real signage, not a decal: the app has no textures, so a wordmark either
    exists as geometry or it does not exist. `resolution_u = 1` keeps the font
    curves coarse, which is both cheap and correct for the miniature — chunky
    letterforms, no hairline serif detail (style bible s.4).
    """
    curve = bpy.data.curves.new(f"{name}_curve", "FONT")
    curve.body = text
    curve.size = cap_h
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    curve.resolution_u = 1
    weld = cap_h * weld_frac
    curve.offset = 0.0
    ob = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(ob)

    # Text is authored in its own XY plane extruding along +Z. Stand it up in
    # the wall: local +X -> wall tangent, local +Y -> world up, local +Z -> the
    # wall's outward normal.
    a, _length, t, n = poly_edge(edge)
    basis = Matrix(
        (
            (t[0], 0.0, n[0], 0.0),
            (t[1], 0.0, n[1], 0.0),
            (0.0, 1.0, 0.0, 0.0),
            (0.0, 0.0, 0.0, 1.0),
        )
    )
    origin = Vector(
        (
            a[0] + t[0] * u_centre + n[0] * d0,
            a[1] + t[1] * u_centre + n[1] * d0,
            z_base,
        )
    )
    ob.matrix_world = Matrix.Translation(origin) @ basis

    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh = bpy.data.meshes.new_from_object(ob.evaluated_get(depsgraph))
    bpy.data.objects.remove(ob)
    bpy.data.curves.remove(curve)

    solid = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(solid)
    mesh.transform(Matrix.Translation(origin) @ basis)

    # Give the flat glyph outlines real thickness, then close them into solids.
    normal = Vector((n[0], n[1], 0.0))
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    # recalc_face_normals only guarantees CONSISTENCY on an open sheet, not
    # direction. If the glyph faces came out pointing into the wall, extruding
    # along +n would push the letters backwards and leave the finished solid
    # inside-out — which is exactly how the "101" plate failed its signed-volume
    # check the first time. Flip the sheet to face outward before extruding.
    if bm.faces and bm.faces[0].normal.dot(normal) < 0.0:
        bmesh.ops.reverse_faces(bm, faces=list(bm.faces))
    extrude = bmesh.ops.extrude_face_region(bm, geom=list(bm.faces))
    moved = [e for e in extrude["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=moved, vec=normal * (d1 - d0))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    # Font outlines are far denser than a half-metre letter needs, and the cost
    # is driven entirely by the outline vertex count. Welding at a fixed
    # FRACTION of the cap height is the lever that actually reduces it, and
    # keeping it proportional makes the cost scale-invariant — a limited dissolve does not,
    # because a triangulated simple polygon already costs exactly n-2 triangles
    # for n outline vertices.
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=weld)
    bmesh.ops.dissolve_degenerate(bm, dist=weld, edges=list(bm.edges))
    bmesh.ops.triangulate(bm, faces=list(bm.faces))
    slivers = [f for f in bm.faces if f.calc_area() < 1e-7]
    if slivers:
        bmesh.ops.delete(bm, geom=slivers, context="FACES_ONLY")
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    volume = sum(
        f.verts[0].co.dot(f.verts[1].co.cross(f.verts[2].co)) / 6.0 for f in bm.faces
    )
    if volume < 0.0:
        bmesh.ops.reverse_faces(bm, faces=list(bm.faces))
    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(mat)
    mesh.shade_flat()
    return solid


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


def oak_bay(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None, base=0.0):
    """A shopfront bay: a chunky oak frame ring standing proud of the wall with
    the glass proud again inside it. The frame is deliberately fat (0.28 m read)
    — it is the only warm element on the building and it has to survive at
    thumbnail size (style bible s.7, s.22). `base` is the offset of the wall
    surface the bay sits on."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), base, base + 0.14, frame_mat)
    inset = 0.28
    face_panel(
        f"{tag}_fill",
        edge,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        base,
        base + 0.20,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.40
        face_panel(
            f"{tag}_glow",
            edge,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            base + 0.16,
            base + 0.24,
            glow_mat,
        )


def flank_bay(tag, edge, u, w, z0, z1, frame_mat, fill_mat):
    """A plain opening on a secondary elevation: a dark border ring with the
    glass standing proud inside it. No frame colour — the flanks stay quiet so
    the front's oak row keeps its monopoly on warmth.

    Note the direction of travel. Everything here is a union of closed solids;
    there are no booleans, so an opening cannot be cut out of the wall. The
    first build authored these as panels sunk INTO the body, which simply filled
    the wall with more wall and left the flanks blank in the render. Openings
    are made by standing proud, and depth is faked by what stands proud around
    them (see the front's ribbon surround)."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, 0.07, frame_mat)
    face_panel(
        f"{tag}_fill",
        edge,
        u,
        rect_profile(w - 0.22, z0 + 0.11, z1 - 0.11),
        0.0, 0.13,
        fill_mat,
    )


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    charcoal = material("Toy_charcoal")
    trim = material("Toy_trim")
    oak = material("Toy_rust")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    white = material("Toy_white")
    steel = material("Toy_steel")
    roofd = material("Toy_roofd")
    ink = material("Toy_ink")
    oglow = material("Toy_rust_Glow")
    gglow = material("Toy_glass_Glow")

    # --- body: one charcoal volume, its top cap IS the cool roof deck -------
    prism("body", FOOTPRINT, 0.0, Z_DECK, charcoal, mat_caps=white)

    # --- parapet ring + steel coping ---------------------------------------
    # The coping is what keeps the parapet ring legible from the app's downward
    # camera against a near-white deck.
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET - 0.14, -PARAPET_T, 0.0, charcoal)
    ring_band("coping", FOOTPRINT, Z_PARAPET - 0.14, Z_PARAPET, -PARAPET_T - 0.06, 0.06, steel)

    len_front = poly_edge(EDGE_FRONT)[1]

    # --- South Park front: the proud skin that MAKES the ribbon recess -------
    # There are no booleans here — every part is a closed solid and the union is
    # the building. So the upper storey's half-metre reveal is not cut out of
    # the wall; it is what is left over when the rest of the front is built
    # proud of it. Four panels form a picture frame (sill, header, two end
    # piers) standing RECESS clear of the body, and the ribbon glass sits back
    # near the body plane inside that frame. The shadow this throws is the whole
    # upper half of the elevation.
    pier_w = (len_front - RIBBON_W) / 2.0
    face_panel(
        "front_skin_sill", EDGE_FRONT, len_front / 2.0,
        rect_profile(len_front, 0.0, Z_UWIN0), 0.0, RECESS, charcoal,
    )
    face_panel(
        "front_skin_header", EDGE_FRONT, len_front / 2.0,
        rect_profile(len_front, Z_UWIN1, Z_PARAPET - 0.14), 0.0, RECESS, charcoal,
    )
    # the front's own coping, carried out to the skin face so the parapet line
    # does not disappear behind it
    face_panel(
        "front_coping", EDGE_FRONT, len_front / 2.0,
        rect_profile(len_front + 0.12, Z_PARAPET - 0.14, Z_PARAPET), 0.0, RECESS + 0.06, steel,
    )
    for tag, u in (("ne", pier_w / 2.0), ("sw", len_front - pier_w / 2.0)):
        face_panel(
            f"front_skin_pier_{tag}", EDGE_FRONT, u,
            rect_profile(pier_w, Z_UWIN0, Z_UWIN1), 0.0, RECESS, charcoal,
        )
    face_panel(
        "ribbon_glass", EDGE_FRONT, len_front / 2.0,
        rect_profile(RIBBON_W, Z_UWIN0, Z_UWIN1), 0.0, 0.13, glass,
    )
    # slim mullions so the band is not one blank rectangle
    for u in (4.55, 8.25):
        face_panel(
            f"ribbon_mullion_{int(u * 100)}", EDGE_FRONT, u,
            rect_profile(0.16, Z_UWIN0, Z_UWIN1), 0.0, 0.20, ink,
        )
    # three lit lights at night, not the whole band
    for i, u in enumerate((3.10, 6.40, 9.05)):
        face_panel(
            f"ribbon_glow{i}", EDGE_FRONT, u,
            rect_profile(1.75, Z_UWIN0 + 0.28, Z_UWIN1 - 0.28), 0.13, 0.19, gglow,
        )

    # --- South Park front, ground floor: the oak row ------------------------
    # u = 0 at the northeast corner of the front, which is the entrance end.
    # These sit on the proud sill skin, so every depth is measured from RECESS.
    oak_bay("door", EDGE_FRONT, 1.35, 1.55, 0.0, Z_DOOR1, oak, ink, oglow, base=RECESS)
    # Pale glazing, not the navy Toy_glass used everywhere else: the real
    # shopfront lights are frosted/shaded and read almost white from the street,
    # and the first aerial proved that navy behind a thin oak frame collapses
    # into one dark hole. Toy_glassl gives the oak something to sit against,
    # which is the whole job of this row.
    for i, u in enumerate((3.55, 5.75, 7.95, 10.15)):
        oak_bay(f"gbay{i}", EDGE_FRONT, u, 1.90, Z_GWIN0, Z_GWIN1, oak, glassl, oglow,
                base=RECESS)
    # --- the Kleiner Perkins identity ---------------------------------------
    # The building's tenant is the reason anyone points at it, and with no
    # textures in this pipeline a wordmark has to be geometry or nothing.
    #
    # Faithful to: SF permit 2018 records exactly ONE single-faced,
    # NON-ILLUMINATED wall sign reading "kleiner perkins", and KP's published
    # brand assets are monochrome wordmarks with no brand colour — so the sign
    # is off-white on charcoal and does not glow.
    #
    # Exaggerated: the real sign is a small plaque beside the entrance, which at
    # city scale is well under a pixel. It is moved up onto the header band
    # between the ribbon and the parapet and scaled to a 0.5 m cap height so it
    # reads from the app's downward camera. Semantic exaggeration of an identity
    # feature in AUTHORING is exactly what AGENTS rule 5 and style bible s.22
    # allow; the building is not moved or rescaled.
    lettering(
        "wordmark", EDGE_FRONT, len_front / 2.0, 9.20,
        "Kleiner Perkins", 0.75, RECESS, RECESS + 0.09, trim,
    )
    # the street number over the entrance, at its real position and size
    lettering("plate_101", EDGE_FRONT, 1.35, 3.34, "101", 0.30, RECESS, RECESS + 0.05, trim)

    # --- Jack London Alley flank: quiet, regular, genuinely visible ---------
    for i in range(6):
        u = 3.0 + i * 4.40
        flank_bay(f"ne_g{i}", EDGE_NE, u, 1.60, 1.00, 3.60, ink, glass)
        flank_bay(f"ne_u{i}", EDGE_NE, u, 1.60, Z_UWIN0 - 0.10, Z_UWIN1 - 0.20, ink, glass)

    # --- southwest flank: party wall with 117 South Park, blank -------------
    # Intentionally no openings and no relief. The first build put two shallow
    # pilaster strips here to break up 29.6 m of flat wall; they did not read at
    # all in the aerial and they are not on the real building, so they are gone.
    # A blank party wall against an attached neighbour is the honest answer, and
    # the style bible's "design every surface" is about the roof, which this
    # asset does spend its budget on.

    # --- rear: service elevation --------------------------------------------
    len_rear = poly_edge(EDGE_REAR)[1]
    face_panel(
        "rear_door", EDGE_REAR, 3.2, rect_profile(2.4, 0.0, 3.0), 0.0, 0.10, roofd
    )
    for i, u in enumerate((7.0, 9.8)):
        flank_bay(f"rear_g{i}", EDGE_REAR, u, 1.30, 1.20, 3.40, ink, glass)
    for i, u in enumerate((4.0, 7.0, 9.8)):
        flank_bay(f"rear_u{i}", EDGE_REAR, u, 1.30, Z_UWIN0, Z_UWIN1 - 0.40, ink, glass)
    del len_rear

    # --- roof: the surface the app's camera sees most ------------------------
    # u runs along the South Park front from its NE end, v goes into the block.
    # The 2026 satellite shows the skylight/mechanical density concentrated in
    # the front third with a thinner scatter down the length — that asymmetry is
    # what makes the roof read as a real roof rather than a decorated tray.
    for i, (u, v) in enumerate(
        ((3.2, 4.2), (6.6, 4.2), (9.9, 4.2), (5.1, 15.6), (8.9, 20.2), (4.2, 25.0))
    ):
        roof_box(f"skylight_kerb{i}", u, v, Z_DECK, Z_DECK + 0.20, 2.5, 1.8, steel)
        roof_box(f"skylight{i}", u, v, Z_DECK + 0.16, Z_DECK + 0.42, 2.2, 1.5, glassl)
    roof_box("hvac_a", 4.2, 8.2, Z_DECK, Z_DECK + 1.00, 2.2, 1.6, steel)
    roof_box("hvac_b", 7.6, 8.6, Z_DECK, Z_DECK + 0.80, 1.6, 1.2, steel)
    roof_box("duct", 6.0, 10.6, Z_DECK + 0.22, Z_DECK + 0.52, 0.7, 2.0, steel)
    roof_box("penthouse", 3.7, 12.4, Z_DECK, Z_CREST, 3.2, 2.6, roofd)
    roof_box("roof_hatch", 9.5, 12.8, Z_DECK, Z_DECK + 0.45, 1.4, 1.1, roofd)
    roof_box("hvac_c", 7.4, 25.4, Z_DECK, Z_DECK + 0.70, 1.6, 1.2, steel)
    roof_box("vent_a", 10.3, 24.2, Z_DECK, Z_DECK + 1.05, 0.70, 0.70, steel)
    roof_box("vent_b", 2.6, 19.6, Z_DECK, Z_DECK + 0.85, 0.60, 0.60, steel)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.12/2. Applied window panels are small and numerous — their frames
    # get a token 1-segment softening and the fills/glow shells none at all,
    # which is what keeps this well under the 9,000-triangle cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")):
            continue
        if obj.name.endswith(("_frame", "_reveal", "_glass")) or "_mullion_" in obj.name:
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
    print("[build] anchor lon/lat: -122.3937582 37.7812624 (footprint OBB centre)")
    print("[build] South Park front heading: 318.3 deg true (NW)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "101-south-park.blend")
    glb = os.path.join(out, "101-south-park.glb")
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
