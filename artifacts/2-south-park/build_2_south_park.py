"""Deterministic Blender build of the SF-SIM miniature 2 South Park (544 Second Street).

    blender -b --python build_2_south_park.py -- [--out DIR]

Writes 2-south-park.blend and 2-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = DataSF surveyed parcel 3775-005 area
centroid (anchor lon -122.3932364, lat 37.7824236), min Z = 0, roof penthouse
crest exactly 17.72 m.

Design (see REFERENCE.md for the sources behind every number, and REPORT.md for
the corrections this build made to the plan):

* the surveyed footprint: a 29.8 x 20.9 m rectangle filling its corner lot at
  the head of the South Park oval, at bearing 45/225 deg. Three public faces and
  one blind party wall — the corner condition IS the building;
* a 1923 unreinforced-brick Kohler warehouse, three storeys to a 12.83 m roof
  deck, with a pier-and-spandrel grid: proud brick piers, four bays on Second
  Street, six on South Park and six on Taber Place, and light cast-stone bands
  crossing them at every floor line;
* enormous multi-pane steel industrial sash, simplified to one recessed glazed
  panel per bay with a single steel frame ring — the *size* of the opening is
  the cue at the app's camera, not its subdivision;
* a flat roof at 12.83 m behind a 13.60 m parapet, with a set-back stair/lift
  penthouse reaching 17.72 m, one skylight and a tight mechanical group along
  the Taber Place edge. The roof flagpole is deliberately NOT modelled (plan
  2.10): it would put the bounding-box top on a fixture and is sub-pixel;
* night state: the Blue Bottle café wrapping the Second Street x South Park
  corner is the hero glow, plus six scattered lit office windows on the two
  street faces. The Taber Place alley and the party wall stay dark. Glow
  surfaces are thin shells proud of the opaque glazing (the app renders _Glow in
  a separate layer that is ~12% alpha by day — never author a primary surface as
  glow).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF parcel 3775005 reduced to its minimum-area oriented bounding box
# (29.8 x 20.9 m at bearing 45.2 deg), projected with the app's tangent
# projection and recentred on the parcel area centroid (anchor
# lon -122.3932364, lat 37.7824236). CCW, 4 corners.
#
#   N corner = Second Street x Taber Place
#   W corner = Taber Place x the party wall
#   S corner = South Park x the party wall
#   E corner = Second Street x South Park   <- the corner that matters
FOOTPRINT = [
    (3.15, 17.93),     # N
    (-17.93, -3.15),   # W
    (-3.15, -17.93),   # S
    (17.93, 3.15),     # E
]

# Edge index -> elevation. Outward normals verified against the survey (2.3).
EDGE_TABER = 0    # 29.8 m, faces NW 315.2 deg — the service alley
EDGE_PARTY = 1    # 20.9 m, faces SW 225.2 deg — blind party wall
EDGE_PARK = 2     # 29.8 m, faces SE 135.2 deg — South Park front
EDGE_SECOND = 3   # 20.9 m, faces NE  45.2 deg — Second Street front

BAYS = {EDGE_TABER: 6, EDGE_PARK: 6, EDGE_SECOND: 4}
PIER_W = 1.10      # brick pier width
PIER_OUT = 0.12    # how far the piers stand proud of the wall plane
BAY_CLEAR = 0.42   # gap between a pier face and the opening beside it

# Vertical scheme. Three floors of ~4.28 m to a 12.83 m LiDAR-median roof deck;
# parapet derived (plan 2.15), penthouse crest = the LiDAR maximum.
Z_BASE_TOP = 0.35          # dark plinth under the shopfronts
Z_STORE_0, Z_STORE_1 = 0.45, 3.90     # ground-floor shopfront openings
Z_BAND1_0, Z_BAND1_1 = 4.05, 4.30     # cast-stone band capping the ground floor
Z_W2_0, Z_W2_1 = 4.75, 7.90           # second-floor sash
Z_BAND2_0, Z_BAND2_1 = 8.15, 8.45     # cast-stone spandrel band
Z_W3_0, Z_W3_1 = 8.95, 12.10          # third-floor sash
Z_BAND3_0, Z_BAND3_1 = 12.35, 12.65   # cast-stone lintel band
Z_DECK = 12.83             # roof deck (DataSF LiDAR hgt_median 12.83 m)
Z_PARAPET = 13.40          # brick parapet upstand
Z_COPING = 13.58           # stone coping — the parapet line the street sees
Z_PENT_0 = 12.95           # penthouse base, just above the deck slab
Z_PENT_CAP = 17.55         # penthouse wall top
Z_CREST = 17.72            # penthouse cap top = bbox top = targetHeightM

# Roof furniture, on the building's own (u, v) grid: +u north-east toward Second
# Street, +v north-west toward Taber Place. Half-extents 14.9 x 10.45 m.
PENT_U, PENT_V, PENT_SU, PENT_SV = -1.5, 5.45, 7.0, 5.0
SKY_U, SKY_V, SKY_SU, SKY_SV = -1.5, 1.50, 3.0, 2.0

PALETTE_HEX = {
    "Toy_brick": "c96f4a",      # body, piers, parapet, penthouse
    "Toy_stone": "d9d2c2",      # sill/spandrel/lintel bands, coping
    "Toy_glass": "2a4d73",      # industrial sash, shopfronts, skylight
    "Toy_steel": "9aa0a6",      # light roof membrane, entry canopy
    "Toy_roofd": "45454a",      # penthouse cap, roof plant, skylight kerb
    "Toy_ink": "3a3530",        # plinth, steel sash and shopfront frames, fire escape
    "Toy_glass_Glow": "6f95b8", # lit office windows at night
    "Toy_trim_Glow": "f3efe6",  # cafe spill at the Second Street corner
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


# ------------------------------------------------- building-local (u, v) frame
# u runs along the South Park edge (bearing 45.2 deg, north-east positive);
# v runs from that edge into the building (bearing 315.2 deg, toward Taber
# Place). Both are measured from the footprint centre, which is the anchor.

_U_AXIS = poly_edge(EDGE_PARK)[2]
_N_PARK = poly_edge(EDGE_PARK)[3]
_V_AXIS = (-_N_PARK[0], -_N_PARK[1])
_CX = sum(c[0] for c in FOOTPRINT) / len(FOOTPRINT)
_CY = sum(c[1] for c in FOOTPRINT) / len(FOOTPRINT)


def uv(u, v):
    """Building-local (u north-east, v north-west) -> world (x, y)."""
    return (
        _CX + _U_AXIS[0] * u + _V_AXIS[0] * v,
        _CY + _U_AXIS[1] * u + _V_AXIS[1] * v,
    )


def bay_layout(edge):
    """(pier u positions, window u positions, window width) for a public face."""
    length = poly_edge(edge)[1]
    n = BAYS[edge]
    pitch = length / n
    width = pitch - PIER_W - 2 * BAY_CLEAR
    piers = [k * pitch for k in range(1, n)]
    piers = [PIER_W / 2 + 0.2] + piers + [length - PIER_W / 2 - 0.2]
    windows = [(k + 0.5) * pitch for k in range(n)]
    return piers, windows, width


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
    """Miniature-style edge softening on the chunky solids (style bible s.4)."""
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


def uv_box(name, u, v, z0, z1, su, sv, mat):
    """Box on the building's own grid rather than the world axes."""
    corners = []
    for lu, lv in ((-su / 2, -sv / 2), (su / 2, -sv / 2), (su / 2, sv / 2), (-su / 2, sv / 2)):
        corners.append(uv(u + lu, v + lv))
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


def uv_cyl(name, u, v, z0, z1, radius, mat, segments=10):
    poly = []
    for i in range(segments):
        a = 2 * math.pi * i / segments
        poly.append(uv(u + radius * math.cos(a), v + radius * math.sin(a)))
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
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# --------------------------------------------------------------------- parts


def sash(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None):
    """One bay's opening: a frame ring proud of the wall with a glazed fill set
    inside it. No booleans, all closed solids."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, 0.08, frame_mat)
    inset = 0.15
    face_panel(
        f"{tag}_fill",
        edge,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        0.0,
        0.14,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.36
        face_panel(
            f"{tag}_glow",
            edge,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            0.11,
            0.19,
            glow_mat,
        )


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    brick = material("Toy_brick")
    stone = material("Toy_stone")
    glass = material("Toy_glass")
    steel = material("Toy_steel")
    roofd = material("Toy_roofd")
    ink = material("Toy_ink")
    gglow = material("Toy_glass_Glow")
    tglow = material("Toy_trim_Glow")

    # --- body: one brick volume to the roof deck ----------------------------
    prism("body", FOOTPRINT, 0.0, Z_DECK, brick)

    # --- dark base band under the shopfronts --------------------------------
    ring_band("base_band", FOOTPRINT, 0.0, Z_BASE_TOP, -0.02, 0.09, ink)

    # --- cast-stone bands crossing every floor line -------------------------
    # These are the strongest identity carrier on the model (plan 2.5 cue 3):
    # they wrap all four faces, so the party wall reads as part of the building
    # from the air even though it has no openings.
    ring_band("band_ground", FOOTPRINT, Z_BAND1_0, Z_BAND1_1, -0.02, 0.07, stone)
    ring_band("band_spandrel", FOOTPRINT, Z_BAND2_0, Z_BAND2_1, -0.02, 0.07, stone)
    ring_band("band_lintel", FOOTPRINT, Z_BAND3_0, Z_BAND3_1, -0.02, 0.07, stone)

    # --- parapet and coping -------------------------------------------------
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET, -0.02, 0.13, brick)
    ring_band("coping", FOOTPRINT, Z_PARAPET, Z_COPING, -0.04, 0.17, stone)

    # --- brick piers on the three public faces ------------------------------
    for edge, tag in ((EDGE_SECOND, "sec"), (EDGE_PARK, "park"), (EDGE_TABER, "tab")):
        piers, _windows, _w = bay_layout(edge)
        for k, u in enumerate(piers):
            face_panel(
                f"pier_{tag}_{k}",
                edge,
                u,
                rect_profile(PIER_W, 0.0, Z_PARAPET),
                0.0,
                PIER_OUT,
                brick,
            )

    # --- the openings -------------------------------------------------------
    # Second Street (4 bays) and South Park (6 bays) carry shopfronts at the
    # ground floor; Taber Place is an alley, so it gets two service openings and
    # is otherwise plain brick. The party wall gets nothing at all.
    #
    # u=0 on EDGE_SECOND is the E corner (Second x South Park); u=0 on
    # EDGE_PARK is the S corner (South Park x the party wall). So the cafe
    # corner is EDGE_SECOND bay 0 and EDGE_PARK bay 5.
    # (floor, bay) -> lit at night. Bay 1 on South Park is skipped deliberately:
    # the fire escape stands in front of it and a lit window behind a stair run
    # reads as a shard rather than a window.
    lit_second = {(2, 0), (2, 2), (3, 1)}
    lit_park = {(2, 2), (2, 4), (3, 5)}

    for edge, tag in ((EDGE_SECOND, "sec"), (EDGE_PARK, "park"), (EDGE_TABER, "tab")):
        _piers, windows, w = bay_layout(edge)
        for k, u in enumerate(windows):
            # ground floor
            if edge is EDGE_TABER and k not in (1, 4):
                pass  # alley: plain brick between the two service openings
            else:
                cafe = (edge is EDGE_SECOND and k == 0) or (edge is EDGE_PARK and k == 5)
                sash(
                    f"store_{tag}_{k}",
                    edge,
                    u,
                    w + 0.20,
                    Z_STORE_0,
                    Z_STORE_1,
                    ink,
                    glass,
                    tglow if cafe else None,
                )
            # upper floors
            for floor, (z0, z1) in ((2, (Z_W2_0, Z_W2_1)), (3, (Z_W3_0, Z_W3_1))):
                lit = (floor, k) in (lit_second if edge is EDGE_SECOND else lit_park)
                sash(
                    f"sash_{tag}_{floor}_{k}",
                    edge,
                    u,
                    w,
                    z0,
                    z1,
                    ink,
                    glass,
                    gglow if (lit and edge is not EDGE_TABER) else None,
                )

    # --- Second Street: the recessed timber-panelled main entry -------------
    _p, sec_windows, sec_w = bay_layout(EDGE_SECOND)
    entry_u = (sec_windows[1] + sec_windows[2]) / 2
    face_panel(
        "entry", EDGE_SECOND, entry_u, rect_profile(2.0, 0.0, 3.10), 0.0, 0.08, ink
    )
    face_panel(
        "entry_canopy",
        EDGE_SECOND,
        entry_u,
        rect_profile(2.9, 3.14, 3.34),
        0.0,
        0.85,
        steel,
    )

    # --- South Park: the black fire escape near the party-wall end ----------
    _p, park_windows, _w = bay_layout(EDGE_PARK)
    fe_u = park_windows[1]
    for tag, z in (("lo", 4.55), ("hi", 8.75)):
        face_panel(
            f"fe_deck_{tag}", EDGE_PARK, fe_u, rect_profile(3.20, z, z + 0.12), 0.10, 1.15, ink
        )
        face_panel(
            f"fe_rail_{tag}",
            EDGE_PARK,
            fe_u,
            rect_profile(3.20, z + 0.12, z + 1.00),
            1.02,
            1.15,
            ink,
        )
    stair = [(-1.05, 4.95), (1.05, 8.55), (1.05, 8.90), (-1.05, 5.30)]
    face_panel("fe_stair", EDGE_PARK, fe_u, stair, 0.30, 0.98, ink)

    # --- roof ---------------------------------------------------------------
    prism("roof_slab", offset_polygon(FOOTPRINT, -0.16), Z_DECK, Z_DECK + 0.12, steel)

    # Penthouse: the crest, set back from the Taber Place parapet (plan 2.7).
    uv_box("penthouse", PENT_U, PENT_V, Z_PENT_0, Z_PENT_CAP, PENT_SU, PENT_SV, brick)
    uv_box(
        "penthouse_cap",
        PENT_U,
        PENT_V,
        Z_PENT_CAP,
        Z_CREST,
        PENT_SU + 0.36,
        PENT_SV + 0.36,
        roofd,
    )
    # one glazed opening on the penthouse's South Park face
    uv_box(
        "penthouse_glass",
        PENT_U,
        PENT_V - PENT_SV / 2,
        Z_PENT_0 + 1.6,
        Z_PENT_0 + 3.4,
        3.0,
        0.16,
        glass,
    )

    # Skylight beside the penthouse (2017 permit 201709016716).
    uv_box("skylight_kerb", SKY_U, SKY_V, Z_DECK + 0.12, Z_DECK + 0.34, SKY_SU, SKY_SV, roofd)
    uv_box(
        "skylight_glass",
        SKY_U,
        SKY_V,
        Z_DECK + 0.34,
        Z_DECK + 0.62,
        SKY_SU - 0.34,
        SKY_SV - 0.34,
        glass,
    )

    # Mechanical group along the Taber Place edge, away from the clean two
    # thirds of roof the camera reads first (plan 2.9).
    uv_box("mech_a", 5.6, 7.4, Z_DECK + 0.12, Z_DECK + 0.92, 2.0, 1.4, roofd)
    uv_box("mech_b", 8.2, 5.9, Z_DECK + 0.12, Z_DECK + 0.74, 1.6, 1.1, roofd)
    uv_box("mech_c", -8.6, 7.4, Z_DECK + 0.12, Z_DECK + 0.86, 1.8, 1.3, roofd)
    uv_cyl("mech_fan_a", 3.0, 6.4, Z_DECK + 0.12, Z_DECK + 0.66, 0.55, roofd)
    uv_cyl("mech_fan_b", -6.0, 5.6, Z_DECK + 0.12, Z_DECK + 0.60, 0.48, roofd)
    # gas flue, same permit
    uv_cyl("flue", -10.5, 6.2, Z_DECK + 0.12, Z_DECK + 1.70, 0.22, roofd, segments=8)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.12/2. The 44 opening panels are small and numerous — their frames
    # get a token 1-segment softening and the fills and glow shells none at all.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")):
            continue
        if obj.name.startswith("band_") or obj.name == "coping":
            bevel(obj, width=0.03, segments=1)
        elif obj.name.endswith("_frame") or obj.name.startswith(("pier_", "fe_")):
            bevel(obj, width=0.05, segments=1)
        elif obj.name in ("parapet", "base_band", "roof_slab"):
            bevel(obj, width=0.06, segments=1)
        elif obj.name.startswith(("mech_", "skylight_", "flue", "entry")):
            bevel(obj, width=0.06, segments=1)
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
    print("[build] anchor lon/lat: -122.3932364 37.7824236 (DataSF parcel 3775-005 area centroid)")
    print("[build] Second Street front heading: 45.2 deg true (NE); South Park front 135.2 deg (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "2-south-park.blend")
    glb = os.path.join(out, "2-south-park.glb")
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
