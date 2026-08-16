"""Deterministic Blender build of the SF-SIM miniature 188 South Park.

    blender -b --python build_188_south_park.py -- [--out DIR]

Writes 188-south-park.blend and 188-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = DataSF LiDAR footprint area centroid
(anchor lon -122.3950794, lat 37.7810118), min Z = 0, penthouse crest exactly
15.93 m.

Design (see REFERENCE.md for the sources behind every number, and REPORT.md for
the corrections this build made to the plan):

* the measured footprint: a 23.7 x 16.1 m rectangle on the north rim of the
  South Park oval at bearing 45/225 deg, facing SE onto the park. Wider than it
  is deep — the proportion IS the building;
* four storeys of 2002 live/work loft over a ground-floor commercial base, wood
  frame, the tallest thing on this side of the oval by ~4 m;
* a flat roof at 13.3 m with a penthouse/roof terrace reaching 15.93 m — the
  building's aerial signature. The penthouse sits on the SE third overlooking
  South Park, with a terrace railing;
* the exposed SW and NE flanks carry the building's window rhythm (4 bays each,
  3 floors); the SE end is the address elevation with a storefront; the NW end
  is the service/patio rear with a garage and residential entries;
* night state: a restrained scatter of lit windows on the SW flank plus the
  storefront at the park end. The patio/NW end stays dark. Glow surfaces are
  thin shells proud of the opaque glazing (the app renders _Glow in a separate
  layer that is ~12% alpha by day — never author a primary surface as glow).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way/124884339 OBB, projected with the app's tangent projection and
# recentred on the DataSF LiDAR footprint area centroid (anchor
# lon -122.3950794, lat 37.7810118). CCW, 4 corners.
FOOTPRINT = [
    (-14.110, -2.697),
    (-2.581, -14.132),
    (14.110, 2.697),
    (2.581, 14.132),
]

# Edge index -> elevation. Outward normals verified against the survey.
# Edge 0: 16.1m, faces SW 224.8° — SW flank (long, faces the park oval)
# Edge 1: 23.7m, faces SE 134.8° — South Park front (address elevation)
# Edge 2: 16.1m, faces NE 44.8° — NE flank (faces 166-168 South Park)
# Edge 3: 23.7m, faces NW 314.8° — 3rd St / patio rear (service end)
EDGE_SW = 0      # 16.1 m, faces SW 224.8° — exposed flank toward the park
EDGE_FRONT = 1   # 23.7 m, faces SE 134.8° — South Park front (address)
EDGE_NE = 2      # 16.1 m, faces NE 44.8° — flank toward 166-168 South Park
EDGE_REAR = 3    # 23.7 m, faces NW 314.8° — 3rd St / patio rear

Z_ROOF = 13.30        # main flat roof (LiDAR median 13.34 m)
Z_CREST = 15.93       # penthouse parapet crest (LiDAR max 15.93 m) — bbox top
Z_GROUND_TOP = 4.0    # commercial ground floor ceiling / floor band
Z_PARAPET = 13.50     # parapet upstand above main roof
Z_PENT_BASE = 13.50   # penthouse base = parapet top
Z_PENT_TOP = 15.93    # penthouse crest = target height
Z_W1A, Z_W1B = 4.60, 7.55    # first loft floor window band
Z_W2A, Z_W2B = 8.35, 11.30   # second loft floor window band
Z_W3A, Z_W3B = 11.60, 12.80  # third loft floor window band (shorter, under parapet)

PALETTE_HEX = {
    "Toy_sand": "ece4d4",       # body walls (warm stucco — inferred)
    "Toy_stone": "d9d2c2",      # ground-floor base (stone — inferred)
    "Toy_trim": "f3efe6",       # floor band, parapet, window frames
    "Toy_glass": "2a4d73",      # windows and storefront glazing
    "Toy_roofd": "45454a",      # flat roof slab
    "Toy_steel": "9aa0a6",      # penthouse railing, HVAC, frame bands
    "Toy_ink": "3a3530",        # garage door, door recesses
    "Toy_glass_Glow": "6f95b8", # lit loft windows at night
    "Toy_trim_Glow": "f3efe6",  # storefront spill at the park end
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
# u runs along the long axis (SE edge, bearing 134.8°), v runs across it.
# The SE edge (EDGE_FRONT) is the South Park front.

_A_FRONT, _L_FRONT, _T_FRONT, _N_FRONT = poly_edge(EDGE_FRONT)
U_AXIS = _T_FRONT                      # SE edge runs SW -> NE, bearing 44.8°
# Wait — EDGE_FRONT is edge 1, from corner 1 to corner 2.
# Corner 1 = (-2.581, -14.132), Corner 2 = (14.110, 2.697)
# So the tangent goes from SW to NE. The front faces SE (outward normal = 134.8°).
# u=0 is at corner 1 (the SW end of the front), u=L_FRONT is at corner 2 (NE end).
# v runs from the front (v=0) toward the rear (v=HALF_W_deep).
# Actually, let's use the edge-based frame properly.

# Let's use the FRONT edge as the u-axis, and the inward normal as v.
# u runs along the front (23.7m), v runs from front toward rear (16.1m).
# The front edge's tangent: from corner 1 to corner 2.
# The inward normal (pointing into the building from the front) = -outward normal.
HALF_L = _L_FRONT / 2.0  # half the front length (23.7/2 = 11.85)
# The depth is the perpendicular distance from front to rear.
# We can get it from the SW or NE edge length.
HALF_W = poly_edge(EDGE_SW)[1] / 2.0  # 16.1/2 = 8.05

# Inward normal from the front edge (points into the building, toward NW/rear)
V_AXIS = (-_N_FRONT[0], -_N_FRONT[1])  # negate outward normal = inward

# The center of the footprint in local (u,v) coordinates:
# u_center = L_FRONT/2, v_center = HALF_W (depth/2)
# But we want uv() to map (u=0, v=0) to the front edge center.
# Actually, let's center u on the footprint center.

# Recompute: the footprint center is the average of the 4 corners
_CX = sum(c[0] for c in FOOTPRINT) / 4
_CY = sum(c[1] for c in FOOTPRINT) / 4

# The front edge center
_FC = ((_A_FRONT[0] + FOOTPRINT[(1+1)%4][0]) / 2, (_A_FRONT[1] + FOOTPRINT[(1+1)%4][1]) / 2)

# u-axis direction (along front, from SW to NE)
# v-axis direction (inward, from front toward rear)

def uv(u, v):
    """Building-local (u along the front, v from front toward rear) -> world (x, y).
    u=0 is at the front edge center, v=0 is at the front, v=HALF_W*2 is at the rear.
    Actually: u is centered on the footprint center, v is centered too.
    Let's use: u measured from footprint center along the front direction,
    v measured from footprint center toward the rear."""
    # Map (u, v) to world coordinates relative to the footprint center
    return (_CX + U_AXIS[0] * u + V_AXIS[0] * v,
            _CY + U_AXIS[1] * u + V_AXIS[1] * v)


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


def rect_opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None):
    """Frame panel + a smaller fill that protrudes further, so the frame reads as
    a border ring around a recessed opening. No booleans, all closed solids."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, 0.07, frame_mat)
    inset = 0.16
    face_panel(
        f"{tag}_fill",
        edge,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        0.0,
        0.13,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.30
        face_panel(
            f"{tag}_glow",
            edge,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            0.10,
            0.17,
            glow_mat,
        )


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    sand = material("Toy_sand")
    stone = material("Toy_stone")
    trim = material("Toy_trim")
    steel = material("Toy_steel")
    glass = material("Toy_glass")
    roofd = material("Toy_roofd")
    ink = material("Toy_ink")
    gglow = material("Toy_glass_Glow")
    tglow = material("Toy_trim_Glow")

    len_front = poly_edge(EDGE_FRONT)[1]   # 23.7 m, front and rear
    len_flank = poly_edge(EDGE_SW)[1]      # 16.1 m, both flanks

    # --- body: one plain volume up to the main roof -------------------------
    # Ground floor in stone, upper floors in sand (stucco)
    prism("body_base", FOOTPRINT, 0.0, Z_GROUND_TOP, stone)
    prism("body_upper", FOOTPRINT, Z_GROUND_TOP, Z_ROOF, sand)

    # --- floor band separating the commercial base from the lofts -----------
    ring_band("floor_band", FOOTPRINT, Z_GROUND_TOP, Z_GROUND_TOP + 0.18, -0.02, 0.10, trim)

    # --- parapet at the main roof line --------------------------------------
    ring_band("parapet", FOOTPRINT, Z_ROOF, Z_PARAPET, -0.02, 0.14, trim)

    # --- South Park (SE) front: the address elevation -----------------------
    # Ground: storefront (State Farm office) + recessed entry
    # u is measured along the front edge from its origin (corner 1, SW end)
    # The front edge goes from (-2.581, -14.132) to (14.110, 2.697)
    # u=0 is at the SW end, u=23.7 is at the NE end
    # Center the storefront group around u=8 (SE third overlooking the park)
    rect_opening("store", EDGE_FRONT, 7.5, 6.0, 0.55, 3.45, ink, glass, gglow)
    rect_opening("entry", EDGE_FRONT, 12.5, 1.5, 0.0, 2.75, trim, ink)
    face_panel(
        "entry_canopy", EDGE_FRONT, 12.5, rect_profile(2.3, 2.80, 3.02), 0.0, 0.80, trim
    )
    face_panel(
        "entry_canopy_glow", EDGE_FRONT, 12.5, rect_profile(1.9, 2.81, 2.87), 0.24, 0.74, tglow
    )
    # Upper floors: 4 bays per floor on the 23.7m front
    BAYS_FRONT = 4
    for fi, (za, zb) in enumerate(((Z_W1A, Z_W1B), (Z_W2A, Z_W2B), (Z_W3A, Z_W3B))):
        for i in range(BAYS_FRONT):
            u = len_front / (2.0 * BAYS_FRONT) + i * (len_front / BAYS_FRONT)
            # Light the 2nd bay on the 1st floor and the 3rd bay on the 2nd floor
            glow = gglow if (fi, i) in {(0, 1), (1, 2)} else None
            rect_opening(f"se{fi}_{i}", EDGE_FRONT, u, 3.2, za, zb, steel, glass, glow)

    # --- 3rd St / patio (NW) rear: the service end --------------------------
    rect_opening("garage", EDGE_REAR, 5.0, 3.6, 0.0, 3.3, ink, roofd)
    rect_opening("backdoor", EDGE_REAR, 9.0, 1.2, 0.0, 2.5, trim, ink)
    # Upper floors: 4 bays per floor, plainer
    for fi, (za, zb) in enumerate(((Z_W1A, Z_W1B), (Z_W2A, Z_W2B), (Z_W3A, Z_W3B))):
        for i in range(BAYS_FRONT):
            u = len_front / (2.0 * BAYS_FRONT) + i * (len_front / BAYS_FRONT)
            rect_opening(f"nw{fi}_{i}", EDGE_REAR, u, 2.5, za, zb, steel, glass)

    # --- SW flank: faces the park oval, the most exposed elevation ----------
    # 4 bays per floor on the 16.1m flank
    BAYS_FLANK = 4
    LIT_SW = {(0, 0), (0, 2), (1, 1), (1, 3), (2, 0)}
    for fi, (za, zb) in enumerate(((Z_W1A, Z_W1B), (Z_W2A, Z_W2B), (Z_W3A, Z_W3B))):
        for i in range(BAYS_FLANK):
            u = len_flank / (2.0 * BAYS_FLANK) + i * (len_flank / BAYS_FLANK)
            rect_opening(
                f"sw{fi}_{i}", EDGE_SW, u, 2.4, za, zb, steel, glass,
                gglow if (fi, i) in LIT_SW else None,
            )
    # Ground floor: a couple of small openings
    for i, u in enumerate((4.0, 12.0)):
        rect_opening(f"swg{i}", EDGE_SW, u, 2.0, 0.75, 3.25, steel, glass)

    # --- NE flank: faces 166-168 South Park, similar rhythm -----------------
    for fi, (za, zb) in enumerate(((Z_W1A, Z_W1B), (Z_W2A, Z_W2B), (Z_W3A, Z_W3B))):
        for i in range(BAYS_FLANK):
            u = len_flank / (2.0 * BAYS_FLANK) + i * (len_flank / BAYS_FLANK)
            rect_opening(f"ne{fi}_{i}", EDGE_NE, u, 2.4, za, zb, steel, glass)

    # --- flat roof slab -----------------------------------------------------
    # Thin slab at the main roof level
    roof_poly = offset_polygon(FOOTPRINT, 0.05)
    prism("roof_slab", roof_poly, Z_ROOF - 0.05, Z_ROOF + 0.05, roofd)

    # --- penthouse: the building's aerial signature -------------------------
    # Setback volume on the SE third of the roof, overlooking South Park.
    # In the building's (u, v) frame: u along the front, v from front toward rear.
    # The penthouse sits at u ~ 5.5 (SE third), v ~ -3 (setback from front edge).
    # Dimensions: 7.0m along u, 8.0m along v, from Z_PENT_BASE to Z_PENT_TOP.
    PENT_U = 5.5     # center along the front direction (SE third)
    PENT_V = -3.0    # setback from the front edge toward the rear
    PENT_SU = 7.0    # width along the front
    PENT_SV = 8.0    # depth across the building
    uv_box("penthouse", PENT_U, PENT_V, Z_PENT_BASE, Z_PENT_TOP, PENT_SU, PENT_SV, sand)

    # Penthouse windows: one or two glazed openings on the SE face
    # The SE face of the penthouse faces the park — put a tall window there
    # We'll use face_panel on the front edge, but offset to the penthouse position
    # Actually, let's use a simpler approach: a glass box slightly proud of the penthouse wall
    # The penthouse SE face is at u = PENT_U + PENT_SU/2 in the building frame
    # But face_panel works on the footprint edges, not arbitrary positions.
    # Let's add a simple glass strip on the penthouse using uv_box
    uv_box("pent_glass", PENT_U + PENT_SU/2 - 0.01, PENT_V, Z_PENT_BASE + 0.8, Z_PENT_TOP - 0.3,
           0.06, PENT_SV - 1.0, glass)

    # Penthouse terrace railing: a low lattice around the penthouse perimeter
    # Use a ring_band-like approach but on the penthouse footprint
    pent_footprint = []
    for lu, lv in ((-PENT_SU/2, -PENT_SV/2), (PENT_SU/2, -PENT_SV/2),
                   (PENT_SU/2, PENT_SV/2), (-PENT_SU/2, PENT_SV/2)):
        x, y = uv(PENT_U + lu, PENT_V + lv)
        pent_footprint.append((x, y))
    ring_band("pent_railing", pent_footprint, Z_PENT_BASE, Z_PENT_BASE + 1.0, -0.05, 0.05, steel)

    # --- roof furniture: HVAC units on the NW third -------------------------
    # Grouped away from the penthouse
    uv_box("hvac_a", -6.0, -2.0, Z_PARAPET, Z_PARAPET + 0.9, 2.2, 1.6, steel)
    uv_box("hvac_b", -8.0, 2.0, Z_PARAPET, Z_PARAPET + 0.7, 1.6, 1.2, steel)
    uv_box("vent_a", -4.0, 3.0, Z_PARAPET, Z_PARAPET + 0.5, 0.6, 0.6, steel)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.12/2. The window panels are small and numerous — their frames get a
    # token 1-segment softening and the fills, glow shells none at all.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")):
            continue
        if obj.name.endswith(("_frame",)):
            bevel(obj, width=0.05, segments=1)
        elif obj.name in ("pent_glass", "pent_railing"):
            bevel(obj, width=0.03, segments=1)
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
    print("[build] anchor lon/lat: -122.3950794 37.7810118 (DataSF LiDAR footprint area centroid)")
    print("[build] South Park front heading: 134.8 deg true (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "188-south-park.blend")
    glb = os.path.join(out, "188-south-park.glb")
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
