"""Deterministic Blender build of the SF-SIM miniature 155 - 157 South Park Street.

    blender -b --python build_155_south_park.py -- [--out DIR]

Writes 155-south-park.blend and 155-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading - the
loader applies no rotation. Origin = footprint OBB centre (anchor
lon -122.3942202, lat 37.7808993), min Z = 0, front parapet crest exactly 10.1 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured DataSF LiDAR footprint (mblr SF3775030), a 8.16 x 31.22 m through
  lot at 41.4 deg off the world axes, split into the two masses the survey
  actually shows: a narrow 6.2 m wide front block on South Park Street and a
  wider, lower 8.2 m rear block on the Varney Place alley;
* three levels on the front: a near-black Toy_ink shopfront under two floors of
  bright white stucco. The value contrast is the whole silhouette at diorama
  scale and no neighbour on the oval has it;
* the identity features, carried hard: two sage-green (Toy_verdigris) three-part
  window groups, one per upper floor, and the pair of cast-plaster lozenges
  flanking the second-floor group, enlarged so they survive at thumbnail size;
* the skewed street edge. South Park Street curves around the oval, so the
  frontage sits ~6 deg off the party walls. Squaring it up is the easiest way to
  make this building look subtly wrong in its row, so the survey skew is built;
* night state: the cafe shopfront is the hero glow - warm gold, the one lit thing
  on a dark residential street - plus two cool lit flat windows above. The rear
  service block does not glow. Glow surfaces are thin shells proud of the opaque
  glazing (the app renders _Glow in a separate layer that is ~12% alpha by day -
  never author a primary surface as glow);
* a roof designed for the app's downward camera without inventing a mechanical
  farm a 1925 flats building never had: a light parapet ring over a dark deck,
  the step down to the rear block, and the rear timber roof deck behind its
  lattice screen.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# The lot's own frame, from the minimum-area oriented bounding box of the DataSF
# footprint SF3775030: u runs across the lot (+u = north-east, toward 147 South
# Park), v runs along it (+v = north-west, toward South Park Street).
ROT_DEG = 41.4

# Footprint in (u, v) metres, recentred on the OBB centre = the anchor. Both
# rings are CCW and convex. The survey's two sub-2 m light-well notches (one per
# party wall) are dropped: they are invisible between party walls and cost
# triangles that the window groups need. Recorded in REPORT.md.
FRONT_UV = [
    (-2.30, 2.95),
    (3.80, 2.95),
    (4.06, 14.68),   # survey vertex 15
    (-2.10, 15.61),  # survey vertex 13
]
REAR_UV = [
    (-2.94, -15.61),  # survey vertex 6
    (4.08, -15.08),   # survey vertex 5
    (4.08, 2.95),
    (-4.08, 2.95),    # survey vertex 8 (-4.08, 2.98)
]

# Edge index -> elevation. Outward normals verified against the survey.
F_JUNCTION = 0   # shared with the rear block, faces SSE
F_NE = 1         # party wall, 147 South Park
F_STREET = 2     # 6.23 m, faces NNW 327.2 deg - South Park Street
F_SW = 3         # party wall, 159 South Park

R_VARNEY = 0     # 7.04 m, faces SSE 147.2 deg - Varney Place
R_NE = 1
R_JUNCTION = 2
R_SW = 3

Z_SHOP_TOP = 3.80     # shopfront head / second-floor line
Z_AWN0, Z_AWN1 = 3.45, 3.80
Z_W2A, Z_W2B = 4.20, 6.55    # second-floor window group
Z_W3A, Z_W3B = 6.90, 9.05    # third-floor window group
Z_DECK = 9.25         # front roof deck (LiDAR modal height cell, 925 cm)
Z_PARAPET = 9.85      # main parapet crest (inferred: deck + 0.6 m)
Z_CREST = 10.10       # raised centre bay -> the bbox top, must land exactly
Z_REAR = 7.00         # rear block roof deck (inferred)
Z_REAR_PAR = 7.35     # rear parapet
Z_SCREEN = 7.95       # lattice screen around the rear roof deck
Z_BULK = 7.90         # rear stair bulkhead

SKIN = 0.10           # applied panels stand proud of the wall by this much
PARAPET_T = 0.30

PALETTE_HEX = {
    "Toy_white": "f7f4ec",
    # Deliberate palette extension. The rear block is a warm salmon; Toy_sand
    # (ece4d4) is too pale to read as a separate mass from the white front and
    # Toy_coral (e8735a) is far too saturated for a whole wall. Documented as a
    # WARN in REPORT.md, exactly as 380 Brannan's Toy_slate was.
    "Toy_peach": "dcb6a0",
    "Toy_trim": "f3efe6",
    "Toy_ink": "3a3530",
    "Toy_gold": "caa64a",
    "Toy_verdigris": "9fb8a8",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_rust": "a86444",
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

_C = math.cos(math.radians(ROT_DEG))
_S = math.sin(math.radians(ROT_DEG))


def to_world(u, v):
    """Lot frame -> world (east, north) metres, both centred on the anchor."""
    return (u * _C - v * _S, u * _S + v * _C)


FRONT = [to_world(u, v) for u, v in FRONT_UV]
REAR = [to_world(u, v) for u, v in REAR_UV]

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


def diamond_profile(size, zc):
    """Closed (u, z) lozenge - the building's one piece of ornament."""
    h = size / 2.0
    return [(0.0, zc - h), (h, zc), (0.0, zc + h), (-h, zc)]


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
    """Miniature-style edge softening (style bible s.4). The width is capped at
    a third of the object's thinnest dimension: most applied panels here are
    90-220 mm thick and a flat 0.12 m bevel on those collapses opposing profiles
    into zero-area slivers even with clamp_overlap. The remove_doubles /
    dissolve_degenerate pass sweeps up whatever clamping still pinches shut."""
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


def lot_box(name, u, v, z0, z1, su, sv, mat):
    """Box on the lot's own grid: centre at (u, v), sides su across the lot and
    sv along it, rotated with the building."""
    cx, cy = to_world(u, v)
    yaw = math.radians(90.0 - ROT_DEG) * 0 + math.atan2(_S, _C)
    c, s = math.cos(yaw), math.sin(yaw)
    corners = []
    for lx, ly in ((-su / 2, -sv / 2), (su / 2, -sv / 2), (su / 2, sv / 2), (-su / 2, sv / 2)):
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
    face_panel(f"{tag}_frame", poly, edge, u, rect_profile(w, z0, z1), 0.0, base + 0.06, frame_mat)
    inset = 0.18
    face_panel(
        f"{tag}_fill",
        poly,
        edge,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        0.0,
        base + 0.13,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.30
        face_panel(
            f"{tag}_glow",
            poly,
            edge,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            base + 0.10,
            base + 0.17,
            glow_mat,
        )


def window_group(tag, u, z0, z1, verdigris, glass, trim, glow_mat=None):
    """The building's signature: a wide fixed centre light flanked by two narrow
    sashes, all in one thick sage-green frame with a sill apron under it. The
    three lights are separate fills inside a single frame panel - three real
    openings would cost triple and read identically at the app's camera."""
    w = 3.60
    face_panel(f"{tag}_frame", FRONT, F_STREET, u, rect_profile(w, z0, z1), 0.0, SKIN + 0.10, verdigris)
    face_panel(
        f"{tag}_sill", FRONT, F_STREET, u, rect_profile(w + 0.30, z0 - 0.16, z0), 0.0, SKIN + 0.20, verdigris
    )
    lights = ((-1.24, 0.72), (0.0, 1.68), (1.24, 0.72))
    for i, (du, lw) in enumerate(lights):
        face_panel(
            f"{tag}_light{i}",
            FRONT,
            F_STREET,
            u + du,
            rect_profile(lw, z0 + 0.22, z1 - 0.22),
            0.0,
            SKIN + 0.16,
            glass,
        )
    if glow_mat is not None:
        for i, (du, lw) in enumerate(lights):
            face_panel(
                f"{tag}_glow{i}",
                FRONT,
                F_STREET,
                u + du,
                rect_profile(lw - 0.22, z0 + 0.34, z1 - 0.34),
                SKIN + 0.13,
                SKIN + 0.20,
                glow_mat,
            )


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    white = material("Toy_white")
    peach = material("Toy_peach")
    trim = material("Toy_trim")
    ink = material("Toy_ink")
    gold = material("Toy_gold")
    verdigris = material("Toy_verdigris")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    rust = material("Toy_rust")
    gglow = material("Toy_gold_Glow")
    wglow = material("Toy_glass_Glow")

    # --- the two masses -----------------------------------------------------
    prism("rear_block", REAR, 0.0, Z_REAR, peach, mat_caps=roofd)
    prism("front_block", FRONT, 0.0, Z_DECK, white, mat_caps=roofd)

    len_st = poly_edge(FRONT, F_STREET)[1]
    len_vy = poly_edge(REAR, R_VARNEY)[1]

    # --- front parapet: light ring over a dark deck, so the ring reads from
    # --- the app's downward camera ------------------------------------------
    ring_band("parapet", FRONT, Z_DECK, Z_PARAPET - 0.14, -PARAPET_T, 0.0, white)
    ring_band("coping", FRONT, Z_PARAPET - 0.14, Z_PARAPET, -PARAPET_T - 0.06, 0.06, trim)
    # The raised centre bay over the middle third of the frontage. This sets the
    # bounding-box top and must land exactly on Z_CREST.
    face_panel(
        "parapet_bay",
        FRONT,
        F_STREET,
        len_st / 2.0,
        rect_profile(len_st * 0.46, Z_PARAPET - 0.10, Z_CREST),
        -PARAPET_T,
        0.08,
        trim,
    )

    # --- South Park Street front, ground floor: the near-black shopfront -----
    face_panel(
        "shopfront", FRONT, F_STREET, len_st / 2.0, rect_profile(len_st, 0.0, Z_SHOP_TOP), 0.0, SKIN, ink
    )
    # u runs from the NE corner (the viewer's left from the street), which is
    # where the residential security gate is.
    rect_opening("gate", FRONT, F_STREET, 1.05, 1.10, 0.0, 3.20, ink, roofd, base=SKIN)
    rect_opening("shopwin", FRONT, F_STREET, 2.55, 1.50, 1.00, 2.90, ink, glass, base=SKIN, glow_mat=gglow)
    # Recessed centre entrance: brass doors under a transom, in a deep ink reveal.
    face_panel(
        "entry_frame", FRONT, F_STREET, 3.95, rect_profile(1.90, 0.0, 2.95), 0.0, SKIN + 0.06, ink
    )
    # Toy_trim, not Toy_gold: the first render put a saturated yellow slab in the
    # shopfront and it became the loudest thing on the building. The real doors
    # are pale curtained glass with brass hardware, so the cream leaves carry the
    # brightness and gold is spent only on the slim centre mullion.
    face_panel(
        "entry_door", FRONT, F_STREET, 3.95, rect_profile(1.42, 0.0, 2.30), 0.0, SKIN + 0.13, trim
    )
    face_panel(
        "entry_mullion", FRONT, F_STREET, 3.95, rect_profile(0.12, 0.0, 2.30), 0.0, SKIN + 0.17, gold
    )
    face_panel(
        "entry_transom", FRONT, F_STREET, 3.95, rect_profile(1.42, 2.38, 2.78), 0.0, SKIN + 0.13, glass
    )
    face_panel(
        "entry_glow", FRONT, F_STREET, 3.95, rect_profile(1.18, 2.42, 2.74), SKIN + 0.10, SKIN + 0.17, gglow
    )
    rect_opening("shopwin2", FRONT, F_STREET, 5.35, 1.05, 1.00, 2.60, ink, glass, base=SKIN, glow_mat=gglow)
    # Awning across the full frontage, with the one surviving copper trim line.
    face_panel(
        "awning", FRONT, F_STREET, len_st / 2.0, rect_profile(len_st, Z_AWN0, Z_AWN1), 0.0, SKIN + 1.05, roofd
    )
    face_panel(
        "awning_trim", FRONT, F_STREET, len_st / 2.0, rect_profile(len_st, Z_AWN0 + 0.04, Z_AWN0 + 0.14),
        SKIN + 1.00, SKIN + 1.09, gold,
    )

    # --- the two upper floors: one window group each -------------------------
    window_group("w2", len_st / 2.0, Z_W2A, Z_W2B, verdigris, glass, trim, glow_mat=wglow)
    window_group("w3", len_st / 2.0, Z_W3A, Z_W3B, verdigris, glass, trim)

    # --- the lozenges: the only ornament, enlarged to survive at thumbnail ----
    for tag, du in (("ne", -2.42), ("sw", 2.42)):
        face_panel(
            f"lozenge_{tag}",
            FRONT,
            F_STREET,
            len_st / 2.0 + du,
            diamond_profile(0.80, (Z_W2A + Z_W2B) / 2.0),
            0.0,
            SKIN + 0.12,
            trim,
        )

    # --- Varney Place rear: blunt, utilitarian, two roll-up doors ------------
    for i, u in enumerate((2.00, 5.00)):
        rect_opening(f"garage{i}", REAR, R_VARNEY, u, 2.40, 0.0, 3.00, peach, steel)
    face_panel(
        "vy_pilaster", REAR, R_VARNEY, 3.50, rect_profile(0.40, 0.0, 3.40), 0.0, 0.12, trim
    )
    for i, u in enumerate((2.20, 4.80)):
        rect_opening(f"vywin{i}", REAR, R_VARNEY, u, 1.20, 4.30, 5.70, peach, glass)
    ring_band("rear_parapet", REAR, Z_REAR, Z_REAR_PAR, -0.26, 0.0, peach)

    # --- flanks: party walls. One service window per side and nothing else;
    # --- the neighbours are hard up against them (dossier 2.4) ---------------
    for tag, poly, edge in (("ne", REAR, R_NE), ("sw", REAR, R_SW)):
        L = poly_edge(poly, edge)[1]
        rect_opening(f"{tag}_flankwin", poly, edge, L * 0.30, 1.00, 4.60, 5.80, peach, glass)

    # --- roofs: the surface the app's camera sees most ------------------------
    # Front roof stays deliberately bare - a 1925 flats building never had a
    # mechanical farm, and inventing one would be a lie about the type.
    lot_box("front_skylight_kerb", 0.30, 11.90, Z_DECK, Z_DECK + 0.20, 2.20, 1.60, trim)
    lot_box("front_skylight", 0.30, 11.90, Z_DECK + 0.16, Z_DECK + 0.42, 1.90, 1.30, glassl)
    lot_box("vent_a", 2.30, 9.20, Z_DECK, Z_DECK + 0.75, 0.50, 0.50, steel)
    lot_box("vent_b", -1.30, 7.60, Z_DECK, Z_DECK + 0.60, 0.42, 0.42, steel)
    lot_box("front_hatch", 1.90, 5.10, Z_DECK, Z_DECK + 0.40, 1.30, 1.00, roofd)

    # Rear roof: the timber deck is what makes the step down read as a USE
    # rather than as a modelling mistake.
    lot_box("deck_boards", 0.60, -11.30, Z_REAR, Z_REAR + 0.08, 4.90, 5.30, rust)
    lot_box("bulkhead", -2.20, -1.60, Z_REAR, Z_BULK, 2.20, 1.60, roofd)
    lot_box("rear_skylight_kerb", 2.10, -1.80, Z_REAR, Z_REAR + 0.20, 1.90, 1.50, trim)
    lot_box("rear_skylight", 2.10, -1.80, Z_REAR + 0.16, Z_REAR + 0.40, 1.65, 1.25, glassl)
    lot_box("rear_vent", -2.90, -5.60, Z_REAR, Z_REAR + 0.55, 0.45, 0.45, steel)

    # Lattice screen around the rear deck: a slab with a coarse cut-out pattern
    # would cost ~350 tris for a detail that is 3 px tall at the app's camera,
    # so it is a plain screen wall with a capped top edge instead (dossier 2.6).
    for tag, u, v, su, sv in (
        ("vy", 0.60, -14.25, 5.80, 0.30),
        ("ne", 3.20, -11.30, 0.30, 6.00),
        ("sw", -2.00, -11.30, 0.30, 6.00),
    ):
        lot_box(f"screen_{tag}", u, v, Z_REAR_PAR, Z_SCREEN, su, sv, trim)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.12/2. Applied panels are small and numerous - frames get a token
    # 1-segment softening and the fills/glow shells none at all, which is what
    # keeps this under the 7,000-triangle cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")) or "_glow" in obj.name or "_light" in obj.name:
            continue
        if obj.name.endswith(("_frame", "_sill", "_door")) or obj.name.startswith("lozenge"):
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
    print("[build] anchor lon/lat: -122.3942202 37.7808993 (footprint OBB centre)")
    print("[build] South Park front heading: 327.2 deg true (NNW)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "155-south-park.blend")
    glb = os.path.join(out, "155-south-park.glb")
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
