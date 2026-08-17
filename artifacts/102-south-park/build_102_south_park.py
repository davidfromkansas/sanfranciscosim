"""Deterministic Blender build of the SF-SIM miniature 102 South Park (The Park View).

    blender -b --python build_102_south_park.py -- [--out DIR]

Writes 102-south-park.blend and 102-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = footprint OBB centre (anchor
lon -122.3943678, lat 37.7817707), min Z = 0, front cornice crest exactly 14.0 m.

Design (see REFERENCE.md for the sources behind every number, and REPORT.md for
the corrections this build made to the plan):

* the measured footprint: 7.78 m of South Park frontage running 29.76 m back at
  bearing 135.4 deg, with three light-well notches cut into the SW party-wall
  side where it meets the Gran Oriente Filipino at 106. Four storeys on a 25-foot
  lot — the proportion IS the building;
* a 1913 residential hotel (built as the Hotel Bo-Chow, later the Park View),
  40 SRO rooms over Caffe Centro, rehabilitated 2019-2022 by Mission Housing;
* the front elevation is three bays wide and changes register as it rises: round
  arched windows on floors 2 and 3, plain rectangles on floor 4, all in dusty
  blue-gray on warm greige stucco, under a white two-step cornice;
* the roof deck sits at 12.9 m (LiDAR median) and carries the rehab's solar
  array; the cornice crest at 14.0 m is the bbox top;
* night state: the cafe storefront is the hero glow, with a sparse scatter of lit
  SRO rooms above. Glow surfaces are thin shells proud of the opaque glazing (the
  app renders _Glow in a separate layer that is ~12% alpha by day — never author
  a primary surface as glow).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way/124884353, projected with the app's tangent projection and recentred on
# the footprint OBB centre. The three light wells on the SW side are kept; the
# two collinear segments of the rear wall are merged. CW in this listing, so the
# polygon is reversed once below to give a CCW ring (outward normal = (t.y, -t.x)).
FOOTPRINT_CW = [
    (-7.761, 13.243),    # rear (NW) corner, north side
    (13.296, -7.782),    # park (SE) corner, east side
    (7.761, -13.243),    # park (SE) corner, west side
    (2.376, -7.859),     # --- SW party wall begins
    (4.030, -6.234),     # light well 1: 2.32 m deep
    (2.235, -4.433),
    (0.581, -6.069),
    (-1.936, -3.559),
    (-1.373, -3.007),    # light well 2: 0.79 m deep
    (-3.810, -0.575),
    (-4.373, -1.128),
    (-6.468, 0.962),
    (-4.981, 2.432),     # light well 3: 2.09 m deep
    (-6.644, 4.090),
    (-8.131, 2.620),
    (-13.296, 7.782),    # --- SW party wall ends, rear (NW) corner, south side
]
FOOTPRINT = list(reversed(FOOTPRINT_CW))

# Indices into FOOTPRINT (i.e. into the REVERSED list) for the four elevations.
# Verified by outward normal in report(): 135.4 / 45.0 / 315.4 / 225.0 deg.
EDGE_FRONT = 13       # 7.78 m, faces SE 135.4 deg — South Park
EDGE_NE = 14          # 29.76 m, faces NE 45.0 deg — Jack London Alley side; u=0 at the park end
EDGE_REAR = 15        # 7.77 m, faces NW 315.4 deg — back of the lot, toward Bryant
EDGE_SW = 0           # 7.30 m, faces SW 225.0 deg — rear-end run of the party wall
EDGE_SW_PARK = 12     # 7.61 m, faces SW 225.0 deg — park-end run of the party wall

# The roof furniture must stay clear of the light wells: the deepest notch cuts
# 2.32 m in from the SW wall, i.e. to v = -5.46 measured inward from the NE flank.
V_NOTCH_LIMIT = -5.20

Z_DECK = 12.90        # roof deck — DataSF LiDAR median over this footprint
Z_CREST = 14.00       # front cornice crest — the bbox top
Z_CORNICE_MID = 13.45
Z_PARAPET = 13.40     # plain parapet on the other three sides
Z_BELT_A, Z_BELT_B = 4.00, 4.25   # storefront beltcourse

# Floor plates: ground 4.0 m, then three storeys of 2.967 m to the 12.9 m deck.
Z_F2, Z_F3, Z_F4 = 4.00, 6.97, 9.93

ARCH_SEGS = 7         # enough to read as a curve at diorama scale (plan 2.11)
BAY_W = 1.40          # front window width, widened from ~1.25 m observed (s.9)
BAY_U = (1.945, 3.890, 5.835)     # three bays across the 7.78 m front

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",     # greige stucco body
    "Toy_glassl": "6f95b8",    # THE blue-gray window trim (see REPORT.md)
    "Toy_glass": "2a4d73",     # glazing
    "Toy_trim": "f3efe6",      # cornice, storefront beltcourse
    "Toy_ink": "3a3530",       # shopfront joinery, doors, reveals
    "Toy_awning": "4f7d63",    # the Caffe Centro awning — see REPORT.md s.3
    "Toy_white": "f7f4ec",     # roof deck
    "Toy_navy": "2c4a70",      # roof solar panels
    "Toy_steel": "9aa0a6",     # coping, stair penthouse, vents
    "Toy_mustard_Glow": "d9a441",  # the cafe at night — hero glow
    "Toy_glassl_Glow": "6f95b8",   # lit SRO rooms
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
    """Edge i of the footprint: (origin, length, tangent unit, outward normal)."""
    poly = FOOTPRINT if poly is None else poly
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def rect_profile(w, z0, z1):
    a = w / 2.0
    return [(-a, z0), (a, z0), (a, z1), (-a, z1)]


def arch_profile(w, z_sill, z_spring, segs=ARCH_SEGS):
    """(u, z) profile of a round-arched opening: a rectangle up to the springing
    line, then a semicircle of radius w/2 over it. The crown lands at
    z_spring + w/2, which is what sets the head height in the recipe."""
    r = w / 2.0
    pts = [(-r, z_sill), (r, z_sill), (r, z_spring)]
    for i in range(1, segs):
        a = math.pi * i / segs
        pts.append((r * math.cos(a), z_spring + r * math.sin(a)))
    pts.append((-r, z_spring))
    return pts


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
    Width is capped at a third of the object's thinnest dimension so the thin
    applied panels do not collapse into slivers."""
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


def prism(name, poly, z0, z1, mat):
    """Closed extrusion of a CCW polygon (walls + both caps)."""
    npts = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def offset_polygon(poly, d):
    """Miter offset of a CCW polygon; positive d moves outward. Reflex corners
    (the light wells) are handled by the same intersection formula."""
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


def edge_box(name, edge, u_centre, su, z0, z1, d0, d1, mat):
    """Axis box on a wall's own (u, normal) frame — used for the cornice returns,
    the awning and the storefront pieces."""
    return face_panel(name, edge, u_centre, rect_profile(su, z0, z1), d0, d1, mat)


def uv_box(name, edge, u_centre, v_centre, su, sv, z0, z1, mat):
    """Box on the building's own grid: u along `edge`, v outward from it."""
    a, _length, t, n = poly_edge(edge)
    corners = []
    for du, dv in ((-su / 2, -sv / 2), (su / 2, -sv / 2), (su / 2, sv / 2), (-su / 2, sv / 2)):
        u = u_centre + du
        v = v_centre + dv
        corners.append((a[0] + t[0] * u + n[0] * v, a[1] + t[1] * u + n[1] * v))
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


def rect_opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None):
    """Frame panel + a smaller fill that protrudes further, so the frame reads as
    a border ring around a recessed opening. No booleans, all closed solids."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, 0.07, frame_mat)
    inset = 0.16
    face_panel(
        f"{tag}_fill", edge, u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset), 0.0, 0.13, fill_mat,
    )
    if glow_mat is not None:
        g = 0.28
        face_panel(
            f"{tag}_glow", edge, u,
            rect_profile(w - 2 * g, z0 + g, z1 - g), 0.10, 0.17, glow_mat,
        )


def arch_opening(tag, edge, u, w, z_sill, z_spring, frame_mat, fill_mat, glow_mat=None):
    """The building's signature opening: a round-arched architrave with a keystone
    at the crown. Frame and fill use the same construction as rect_opening, with
    the fill's arch radius shrunk by the same inset so the border stays even."""
    inset = 0.16
    face_panel(
        f"{tag}_frame", edge, u, arch_profile(w, z_sill, z_spring), 0.0, 0.07, frame_mat
    )
    face_panel(
        f"{tag}_fill", edge, u,
        arch_profile(w - 2 * inset, z_sill + inset, z_spring), 0.0, 0.13, fill_mat,
    )
    # keystone: a small block standing proud at the crown, the one piece of
    # ornament the miniature keeps. The arch crown is at z_spring + w/2.
    crown = z_spring + w / 2.0
    face_panel(
        f"{tag}_key", edge, u,
        rect_profile(0.26, crown - 0.20, crown + 0.11), 0.0, 0.13, frame_mat,
    )
    # sill: one projecting band that absorbs the real impost blocks and under-sill
    face_panel(
        f"{tag}_sill", edge, u,
        rect_profile(w + 0.30, z_sill - 0.18, z_sill), 0.0, 0.17, frame_mat,
    )
    if glow_mat is not None:
        g = 0.30
        face_panel(
            f"{tag}_glow", edge, u,
            arch_profile(w - 2 * g, z_sill + g, z_spring), 0.10, 0.17, glow_mat,
        )


def blind_bay(tag, edge, u, w, z0, z1, mat):
    """A recessed panel with no glazing — the SW party wall and the blind stretches
    of the ground floor get articulation rather than a blank slab (style bible s.10)."""
    face_panel(f"{tag}_recess", edge, u, rect_profile(w, z0, z1), -0.09, 0.02, mat)


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    stone = material("Toy_stone")
    glassl = material("Toy_glassl")
    glass = material("Toy_glass")
    trim = material("Toy_trim")
    ink = material("Toy_ink")
    awn = material("Toy_awning")
    white = material("Toy_white")
    navy = material("Toy_navy")
    steel = material("Toy_steel")
    cafe_glow = material("Toy_mustard_Glow")
    room_glow = material("Toy_glassl_Glow")

    len_front = poly_edge(EDGE_FRONT)[1]   # 7.78 m
    len_flank = poly_edge(EDGE_NE)[1]      # 29.76 m

    # --- body: one volume, notches and all, up to the roof deck -------------
    prism("body", FOOTPRINT, 0.0, Z_DECK, stone)

    # --- roof deck: the pale membrane the solar array sits on ---------------
    # Tucked inside the parapet's inner face (-0.28) and standing 50 mm proud of
    # the body cap, so no two faces are coincident.
    prism("roof_deck", offset_polygon(FOOTPRINT, -0.30), Z_DECK - 0.02, Z_DECK + 0.05, white)

    # --- storefront beltcourse: cafe below, hotel above ---------------------
    ring_band("belt", FOOTPRINT, Z_BELT_A, Z_BELT_B, -0.02, 0.10, trim)

    # --- South Park (SE) front ----------------------------------------------
    # Ground: one shopfront, the cafe entrance, and the residential door that
    # serves the 40 rooms above. u runs from the east corner of the front.
    rect_opening("shopfront", EDGE_FRONT, 2.50, 3.60, 0.45, 3.30, ink, glass, cafe_glow)
    rect_opening("cafe_door", EDGE_FRONT, 5.05, 1.15, 0.00, 2.65, ink, ink, cafe_glow)
    rect_opening("sro_door", EDGE_FRONT, 6.85, 1.05, 0.00, 2.55, ink, ink)
    # The awning: deeper and thicker than reality, because it is the only
    # saturated element on a 7.78 m-wide facade (plan 2.6).
    edge_box("awning", EDGE_FRONT, 3.10, 5.40, 3.30, 3.62, 0.02, 1.02, awn)
    edge_box("awning_valance", EDGE_FRONT, 3.10, 5.40, 3.02, 3.34, 0.90, 1.02, awn)

    # Floors 2 and 3: three round-arched windows each — the identity of the
    # building. Sill 0.90 above each floor, springing 2.10 above it, so the crown
    # lands at floor + 2.80 and the head clears the plate by ~0.17 m.
    LIT_ARCH = {(0, 1), (1, 2)}
    for fi, zf in enumerate((Z_F2, Z_F3)):
        for i, u in enumerate(BAY_U):
            arch_opening(
                f"fa{fi}_{i}", EDGE_FRONT, u, BAY_W, zf + 0.90, zf + 2.10,
                glassl, glass, room_glow if (fi, i) in LIT_ARCH else None,
            )

    # Floor 4: the register change — plain rectangles on the same centres.
    for i, u in enumerate(BAY_U):
        rect_opening(
            f"f4_{i}", EDGE_FRONT, u, BAY_W, Z_F4 + 0.97, Z_F4 + 2.52,
            glassl, glass, room_glow if i == 0 else None,
        )

    # --- northeast flank: the exposed elevation toward Jack London Alley -----
    BAYS = 8
    LIT_NE = {(0, 2), (0, 6), (1, 4), (2, 1), (2, 5)}
    for fi, zf in enumerate((Z_F2, Z_F3, Z_F4)):
        for i in range(BAYS):
            u = len_flank / (2.0 * BAYS) + i * (len_flank / BAYS)
            rect_opening(
                f"ne{fi}_{i}", EDGE_NE, u, 1.30, zf + 0.90, zf + 2.40,
                glassl, glass, room_glow if (fi, i) in LIT_NE else None,
            )
    # Ground floor: the cafe's side wall and the hotel's back-of-house. Four
    # blind panels, not an invented shopfront — this face is a yard, not a street.
    for i in range(4):
        u = len_flank / 8.0 + i * (len_flank / 4.0)
        blind_bay(f"neg{i}", EDGE_NE, u, 2.40, 0.80, 3.30, stone)

    # --- rear (NW): service elevation ---------------------------------------
    rect_opening("back_door", EDGE_REAR, 2.10, 1.00, 0.00, 2.40, ink, ink)
    for fi, zf in enumerate((Z_F2, Z_F3, Z_F4)):
        for i, u in enumerate((2.30, 5.30)):
            rect_opening(f"rear{fi}_{i}", EDGE_REAR, u, 0.90, zf + 1.00, zf + 2.50,
                         glassl, glass)

    # --- southwest party wall: blind ----------------------------------------
    # Attached to 106 South Park for its whole length. The light wells in the
    # footprint are the only articulation; the shared plane gets nothing.

    # --- cornice: a front-elevation event, with short returns ----------------
    # Two steps. The upper step's top face is the bounding-box top and must land
    # exactly on Z_CREST, so it is a flat cap and never a bevelled apex.
    edge_box("cornice_lo", EDGE_FRONT, len_front / 2.0, len_front + 0.44,
             Z_DECK, Z_CORNICE_MID, -0.22, 0.22, trim)
    edge_box("cornice_hi", EDGE_FRONT, len_front / 2.0, len_front + 0.84,
             Z_CORNICE_MID, Z_CREST, -0.22, 0.42, trim)
    for side, edge, u0 in (
        ("ne", EDGE_NE, 0.45),
        ("sw", EDGE_SW_PARK, poly_edge(EDGE_SW_PARK)[1] - 0.45),
    ):
        edge_box(f"cornice_ret_{side}_lo", edge, u0, 0.90, Z_DECK, Z_CORNICE_MID,
                 -0.22, 0.22, trim)
        edge_box(f"cornice_ret_{side}_hi", edge, u0, 0.90, Z_CORNICE_MID, Z_CREST,
                 -0.22, 0.42, trim)

    # --- parapet on the other three sides ------------------------------------
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET, -0.28, 0.02, stone)
    ring_band("parapet_coping", FOOTPRINT, Z_PARAPET, Z_PARAPET + 0.10, -0.32, 0.05, steel)

    # --- roof: the 2019-2022 rehab's solar array ----------------------------
    # Two rows of five panels down the long axis, on the NE flank's own (u, v)
    # frame with v measured inward. Two rows, not three: the third would have run
    # over the light wells (V_NOTCH_LIMIT). The park end is left clear so the
    # cornice edge reads from above, which is also what the imagery shows.
    for r, v in enumerate((-2.30, -4.25)):
        for i in range(6):
            u = 5.6 + i * 3.9
            uv_box(f"solar{r}_{i}", EDGE_NE, u, v, 3.40, 1.70,
                   Z_DECK + 0.13, Z_DECK + 0.29, navy)
    uv_box("stair_penthouse", EDGE_NE, 27.0, -3.3, 2.60, 2.20, Z_DECK, 13.90, steel)
    uv_box("vent_a", EDGE_NE, 3.0, -2.3, 0.50, 0.50, Z_DECK, Z_DECK + 0.70, steel)
    uv_box("vent_b", EDGE_NE, 3.0, -4.3, 0.50, 0.50, Z_DECK, Z_DECK + 0.60, steel)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.12/2. The applied window panels are small and numerous — their frames
    # get a token 1-segment softening and the fills, keystones, sills, glow shells
    # and solar panels none at all, which is what keeps this under 9,000 triangles.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if name.endswith(("_fill", "_glow", "_key", "_sill")) or name.startswith("solar"):
            continue
        if name.endswith(("_frame", "_recess")):
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
    for tag, e in (("front", EDGE_FRONT), ("NE", EDGE_NE), ("rear", EDGE_REAR),
                   ("SW-rear-run", EDGE_SW), ("SW-park-run", EDGE_SW_PARK)):
        _a, ln, _t, n = poly_edge(e)
        print(f"[build] edge {tag}: len={ln:.2f} outward normal="
              f"{math.degrees(math.atan2(n[0], n[1])) % 360:.1f} deg")
    print("[build] anchor lon/lat: -122.3943678 37.7817707 (footprint OBB centre)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "102-south-park.blend")
    glb = os.path.join(out, "102-south-park.glb")
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
