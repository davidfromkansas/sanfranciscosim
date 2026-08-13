"""Deterministic Blender build of the SF-SIM miniature 362 Brannan Street.

    blender -b --python build_362_brannan.py -- [--out DIR]

Writes 362-brannan.blend and 362-brannan.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint OBB centre (anchor lon -122.3937450,
lat 37.7808430), min Z = 0, ridge of the front bay's sloped roof exactly 8.6 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured DataSF LiDAR footprint (mblr SF3775018) reduced to its convex
  hull, a 7-gon of 489.3 m2 against the survey's 486.9, sitting ~45 deg off the
  world axes like the whole SoMa grid. It is a through lot: Brannan Street at
  the SE, Varney Place at the NW, party walls on both flanks;
* the massing is the point of this building and the thing OSM's height=6 misses:
  a long ONE-storey block covering the whole lot at 5.6 m (the LiDAR median),
  with a TWO-storey bay on the southwest end of the Brannan frontage whose
  low-pitched roof slopes up away from the street, from a 7.1 m front parapet to
  the 8.6 m ridge (the LiDAR max) set back inside the block;
* the identity is one colour pair, cream stucco and dark bottle green, carried by
  four features: the steel-sash factory window band on the bay, the two green
  diamond lozenges in the frieze above it, the green water table running the
  whole frontage, and three green roll-up freight doors on the Varney back;
* night state: four lit lights scattered in the window band plus the entrance
  sign panel. This is a working sheet-metal shop, not an office floor — the
  restraint is the point. Glow surfaces are thin shells proud of the opaque
  glazing (the app renders _Glow in a separate layer that is ~12% alpha by day —
  never author a primary surface as glow);
* a designed roof for the app's downward camera: the sloped metal bay roof that
  tells the two-height story from straight overhead, a parapet ring under a sand
  coping, two rows of skylight boxes, a gridded skylight, a mechanical pair, a
  hatch and two vent stubs.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF building footprint SF3775018 projected with the app's tangent
# projection, recentred on the OBB centre, and reduced to its convex hull. CCW.
# Edges 1 and 3 are sub-1.2 m survey jogs at the south and east corners, kept so
# the model stays honest to the survey.
FOOTPRINT = [
    (-15.870, 1.705),    # west corner
    (1.102, -15.100),
    (2.037, -15.118),    # south corner
    (15.392, -2.180),    # east corner
    (14.815, -1.242),
    (6.729, 7.498),
    (-1.735, 15.745),    # north corner
]

# Edge index -> elevation. Outward normals verified against the survey.
EDGE_SW = 0      # 23.88 m, faces SW 224.7 deg — party wall to 370 Brannan
EDGE_FRONT = 2   # 18.59 m, faces SE 135.9 deg — Brannan Street
EDGE_NE_A = 4    # 11.91 m, faces NE  47.2 deg — party wall to 358 Brannan
EDGE_NE_B = 5    # 11.82 m, faces NE  44.3 deg
EDGE_REAR = 6    # 19.92 m, faces NW 315.2 deg — Varney Place

Z_DECK = 5.6         # one-storey roof deck (DataSF LiDAR hgt_median 5.63)
Z_PARAPET = 5.95     # low-block parapet crest (inferred: deck + 0.35)
Z_EAVE = 7.1         # two-storey bay's street parapet (inferred, photogrammetric)
Z_CREST = 8.6        # bay roof ridge = LiDAR hgt_max 8.58 -> the bbox top
Z_WIN0, Z_WIN1 = 4.2, 6.0    # steel-sash window band on the bay
Z_FRIEZE0, Z_FRIEZE1 = 6.2, 7.0
Z_WATER0, Z_WATER1 = 1.2, 1.8   # the green water table, full frontage
Z_SLOT0, Z_SLOT1 = 3.4, 3.9     # slot windows high in the low wall

# The two-storey bay, in the front edge's own frame: u runs along Brannan from
# its SW end, v runs INTO the block. Both numbers are *inferred* (plan 2.3) —
# LiDAR area statistics put the bay at 8-20% of the roof, photography at rather
# under half the frontage; 9.0 x 8.5 m = 76 m2 = 16% sits where those agree.
BAY_U0, BAY_U1 = 0.15, 9.15
BAY_DEPTH = 8.5
BAY_PROUD = 0.04    # see build(): keeps the bay's front face off the body's

SKIN = 0.10          # applied-panel thickness on the wall faces
PARAPET_T = 0.30

PALETTE_HEX = {
    "Toy_cream": "f2ede3",
    "Toy_sand": "ece4d4",
    # Deliberate palette extension — see REPORT.md. The palette's Toy_verdigris
    # (9fb8a8) is a pale sage; the real joinery is a dark bottle green, and the
    # green-against-cream contrast IS this building. Rendered in verdigris the
    # window band, the diamonds, the water table and the freight doors all
    # dissolve into the stucco and nothing is left.
    "Toy_bottle": "2f4f3f",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_trim": "f3efe6",
    "Toy_steel": "9aa0a6",
    "Toy_roofd": "45454a",
    "Toy_ink": "3a3530",
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


def diamond_profile(size, zc):
    a = size / 2.0
    return [(0.0, zc - a), (a, zc), (0.0, zc + a), (-a, zc)]


def front_pt(u, v):
    """World XY at (u along the Brannan edge from its SW end, v into the block)."""
    a, _length, t, n = poly_edge(EDGE_FRONT)
    return (a[0] + t[0] * u - n[0] * v, a[1] + t[1] * u - n[1] * v)


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
    """Miniature-style edge softening (style bible s.4), clamped to a third of
    the object's thinnest dimension so the thin applied panels here do not
    collapse into zero-area slivers under clamp_overlap."""
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
    """Box on the roof, aligned to the building's own grid: u along the Brannan
    edge from its SW end, v INTO the block."""
    _a, _l, t, _n = poly_edge(EDGE_FRONT)
    cx, cy = front_pt(u, v)
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=math.atan2(t[1], t[0]))


def sloped_solid(name, u0, u1, v0, v1, z_base, z_front, z_back, mat, mat_top=None):
    """Closed solid over the (u, v) rectangle whose top face is a single plane
    rising from z_front at v0 to z_back at v1 — the bay's shed roof."""
    quad = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
    tops = [z_front, z_front, z_back, z_back]
    verts = [(*front_pt(u, v), z_base) for u, v in quad]
    verts += [(*front_pt(u, v), z) for (u, v), z in zip(quad, tops)]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    face_mats = [0, 1 if mat_top else 0, 0, 0, 0, 0]
    mats = [mat, mat_top] if mat_top else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


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


def rect_opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None, skin=SKIN):
    """Frame panel + a smaller fill that protrudes further, so the frame reads as
    a border ring around a recessed opening. No booleans, all closed solids."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, skin + 0.06, frame_mat)
    inset = 0.16
    face_panel(
        f"{tag}_fill",
        edge,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        0.0,
        skin + 0.13,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.30
        face_panel(
            f"{tag}_glow",
            edge,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            skin + 0.10,
            skin + 0.17,
            glow_mat,
        )


def sash_unit(tag, edge, u, w, z0, z1, frame_mat, glass_mat, bar_mat, cols, rows, glow_mat=None):
    """One steel-sash window unit: a bottle-green perimeter frame, a recessed
    glazed field, and a light grid of pale glazing bars. The grid is 4 x 3 —
    the real sash is nearer 6 x 5 and is sub-pixel from the app's camera."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, SKIN + 0.08, frame_mat)
    inset = 0.14
    gw, gz0, gz1 = w - 2 * inset, z0 + inset, z1 - inset
    face_panel(f"{tag}_glass", edge, u, rect_profile(gw, gz0, gz1), 0.0, SKIN + 0.13, glass_mat)
    bar = 0.055
    for c in range(1, cols):
        du = -gw / 2.0 + gw * c / cols
        face_panel(
            f"{tag}_barv{c}", edge, u + du, rect_profile(bar, gz0, gz1),
            SKIN + 0.11, SKIN + 0.155, bar_mat,
        )
    for r in range(1, rows):
        z = gz0 + (gz1 - gz0) * r / rows
        face_panel(
            f"{tag}_barh{r}", edge, u, rect_profile(gw, z - bar / 2, z + bar / 2),
            SKIN + 0.11, SKIN + 0.155, bar_mat,
        )
    if glow_mat is not None:
        # One lit pane, bottom-left of the unit — a shop with a light on, not a
        # lit floor plate. A thin shell proud of the opaque glazing.
        pw, ph = gw / cols, (gz1 - gz0) / rows
        face_panel(
            f"{tag}_glow", edge, u - gw / 2 + pw / 2 + bar,
            rect_profile(pw - 2 * bar, gz0 + bar, gz0 + ph - bar),
            SKIN + 0.135, SKIN + 0.175, glow_mat,
        )


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    cream = material("Toy_cream")
    sand = material("Toy_sand")
    bottle = material("Toy_bottle")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    trim = material("Toy_trim")
    steel = material("Toy_steel")
    roofd = material("Toy_roofd")
    ink = material("Toy_ink")
    gglow = material("Toy_glass_Glow")
    tglow = material("Toy_trim_Glow")

    len_f = poly_edge(EDGE_FRONT)[1]
    len_r = poly_edge(EDGE_REAR)[1]

    # --- the one-storey block: the whole lot, its top cap IS the roof deck ---
    prism("body", FOOTPRINT, 0.0, Z_DECK, cream, mat_caps=roofd)

    # --- low-block parapet ring + sand coping -------------------------------
    # The coping keeps the ring legible from the app's downward camera against
    # the darker deck.
    # Both rings stop 20 mm INSIDE the wall plane. The two-storey bay rises to
    # 7.1 m across the southwest end of the Brannan frontage, so a parapet flush
    # with the wall (or a coping oversailing it) would either z-fight with the
    # bay's front face or draw a wrong horizontal ledge across it at 5.95 m. The
    # coping earns its read from its material and its inward overhang over the
    # dark deck instead, which is the only place it is seen from.
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET - 0.14, -PARAPET_T, -0.02, cream)
    ring_band("coping", FOOTPRINT, Z_PARAPET - 0.14, Z_PARAPET, -PARAPET_T - 0.06, -0.02, sand)

    # --- the two-storey bay and its shed roof -------------------------------
    # The roof plane rises away from the street: this is what makes the crest
    # (8.6 m) sit behind and above the street parapet (7.1 m), and it is the one
    # cue that tells the two-height story from straight overhead.
    # The bay stands 40 mm PROUD of the street wall (v starts at -BAY_PROUD).
    # Flush, its front face is exactly coplanar with the one-storey block's front
    # face over the same 9 m, and the first Cycles aerial showed the resulting
    # z-fight as a soft X across the stucco under the window band — the two quads
    # triangulate differently, so the seam is diagonal. 40 mm also gives the step
    # at u = BAY_U1 a real reveal, which the building has.
    sloped_solid(
        "bay", BAY_U0, BAY_U1, -BAY_PROUD, BAY_DEPTH, 0.0, Z_EAVE, Z_CREST, cream, mat_top=steel
    )
    # A thin sand fascia along the bay's street edge, so the parapet line reads.
    face_panel(
        "bay_fascia", EDGE_FRONT, (BAY_U0 + BAY_U1) / 2.0,
        rect_profile(BAY_U1 - BAY_U0, Z_EAVE - 0.22, Z_EAVE), 0.0, SKIN + 0.05, sand,
    )
    # Ribs up the slope. The real roof is ribbed galvanized sheet, and without
    # them the roof plane is the largest unmodulated surface on the model —
    # a pale slab that reads as a lid rather than as a roof (style bible s.10:
    # every surface the camera looks down on is designed).
    for i in range(7):
        u = BAY_U0 + (BAY_U1 - BAY_U0) * (i + 0.5) / 7.0
        sloped_solid(
            f"bay_rib{i}", u - 0.10, u + 0.10, 0.25, BAY_DEPTH - 0.25,
            Z_EAVE - 0.30, Z_EAVE + 0.07, Z_CREST + 0.07, steel,
        )
    # Ridge cap and two verge trims, so the plane ends in an edge rather than a
    # cut. The ridge cap tops out below Z_CREST — the ribs set the crest.
    roof_box(
        "bay_ridge", (BAY_U0 + BAY_U1) / 2.0, BAY_DEPTH - 0.12,
        Z_CREST - 0.10, Z_CREST + 0.04, BAY_U1 - BAY_U0 + 0.16, 0.34, sand,
    )

    # --- the steel-sash factory window band on the bay ----------------------
    # Three units inside a bottle-green frame system, the building's loudest
    # feature. LIT picks the units that carry a lit pane at night.
    LIT = {0, 2}
    unit_w, gap = 2.42, 0.42
    span = 3 * unit_w + 2 * gap
    u_start = (BAY_U0 + BAY_U1) / 2.0 - span / 2.0 + unit_w / 2.0
    for i in range(3):
        sash_unit(
            f"sash{i}", EDGE_FRONT, u_start + i * (unit_w + gap), unit_w, Z_WIN0, Z_WIN1,
            bottle, glass, trim, 4, 3, gglow if i in LIT else None,
        )

    # --- the frieze and its two green diamonds ------------------------------
    for i, u in enumerate((BAY_U0 + (BAY_U1 - BAY_U0) / 3.0, BAY_U0 + 2 * (BAY_U1 - BAY_U0) / 3.0)):
        face_panel(
            f"diamond{i}", EDGE_FRONT, u,
            diamond_profile(0.92, (Z_FRIEZE0 + Z_FRIEZE1) / 2.0), 0.0, SKIN + 0.06, bottle,
        )

    # --- the low wall: entrance, then four slot windows ---------------------
    # The entrance sits on the low wall just past the step, not straddling it:
    # placed 0.85 m past BAY_U1 its 2.3 m reveal ran back under the two-storey
    # bay, which is not where the door is.
    U_DOOR = BAY_U1 + 1.45
    DOOR_W = 2.30

    # --- the green water table, full frontage but broken at the entrance ----
    # Run unbroken it drew a green line straight across the doorway. It stops
    # 0.15 m short on each side, which is what the building does.
    for tag, (u0, u1) in (
        ("sw", (0.10, U_DOOR - DOOR_W / 2.0 - 0.15)),
        ("ne", (U_DOOR + DOOR_W / 2.0 + 0.15, len_f - 0.10)),
    ):
        face_panel(
            f"water_table_{tag}", EDGE_FRONT, (u0 + u1) / 2.0,
            rect_profile(u1 - u0, Z_WATER0, Z_WATER1), 0.0, SKIN + 0.07, bottle,
        )

    face_panel(
        "door_reveal", EDGE_FRONT, U_DOOR, rect_profile(DOOR_W, 0.0, 3.25), 0.0, SKIN + 0.05, sand
    )
    face_panel(
        "door_glass", EDGE_FRONT, U_DOOR, rect_profile(1.72, 0.12, 2.66), 0.0, SKIN + 0.11, glass
    )
    face_panel(
        "door_frame", EDGE_FRONT, U_DOOR, rect_profile(1.90, 0.0, 2.80), SKIN + 0.02, SKIN + 0.09, trim
    )
    face_panel(
        "sign", EDGE_FRONT, U_DOOR, rect_profile(1.60, 2.86, 3.16), 0.0, SKIN + 0.13, trim
    )
    face_panel(
        "sign_glow", EDGE_FRONT, U_DOOR, rect_profile(1.40, 2.92, 3.10), SKIN + 0.10, SKIN + 0.17, tglow
    )
    slot_u0 = U_DOOR + 1.9
    slot_gap = (len_f - 1.0 - slot_u0) / 3.0
    for i in range(4):
        rect_opening(
            f"slot{i}", EDGE_FRONT, slot_u0 + i * slot_gap, 1.35, Z_SLOT0, Z_SLOT1, sand, ink
        )

    # --- Varney Place back: three roll-up freight doors + a clad panel ------
    for i, (u, mat) in enumerate(((4.0, bottle), (9.2, bottle), (14.4, steel))):
        face_panel(
            f"roll{i}_reveal", EDGE_REAR, u, rect_profile(3.44, 0.0, 4.00), 0.0, SKIN + 0.05, sand
        )
        face_panel(
            f"roll{i}_door", EDGE_REAR, u, rect_profile(3.20, 0.0, 3.80), 0.0, SKIN + 0.11, mat
        )
    face_panel(
        "rear_panel", EDGE_REAR, 17.6, rect_profile(2.00, 0.0, 3.80), 0.0, SKIN + 0.09, bottle
    )
    # The real rear parapet steps very slightly along its length. A 0.22 m raised
    # strip was tried for it and rendered as a thin white blade floating over the
    # Varney parapet — at the app's camera distance a step that shallow is noise,
    # not information. The back is left as the plain wall it reads as.

    # --- roof furniture: the surface the app's camera sees most --------------
    # u along the Brannan edge from its SW end, v back into the block. Everything
    # sits on the low deck, clear of the bay (u < 9.15, v < 8.5).
    for i, (u, v) in enumerate(((3.2, 12.4), (6.6, 12.4), (10.0, 12.4),
                                (4.4, 17.0), (7.8, 17.0), (11.2, 17.0))):
        roof_box(f"skylight_kerb{i}", u, v, Z_DECK, Z_DECK + 0.18, 2.5, 1.6, sand)
        roof_box(f"skylight{i}", u, v, Z_DECK + 0.14, Z_DECK + 0.36, 2.2, 1.3, glassl)
    roof_box("monitor_kerb", 13.6, 5.0, Z_DECK, Z_DECK + 0.22, 3.6, 2.6, sand)
    roof_box("monitor", 13.6, 5.0, Z_DECK + 0.18, Z_DECK + 0.52, 3.3, 2.3, glassl)
    roof_box("hvac_a", 15.4, 11.6, Z_DECK, Z_DECK + 0.90, 2.0, 1.4, steel)
    roof_box("hvac_b", 15.6, 14.4, Z_DECK, Z_DECK + 0.70, 1.4, 1.0, steel)
    roof_box("duct", 14.2, 13.0, Z_DECK + 0.20, Z_DECK + 0.48, 0.6, 1.8, steel)
    # The Varney end of the deck was an empty third of the roof in the first
    # review render. A stair bulkhead, the hatch and two vent stubs give it
    # something to be, without competing with the bay.
    roof_box("bulkhead", 6.2, 20.4, Z_DECK, Z_DECK + 1.35, 2.8, 2.2, roofd)
    # Steel, not sand: from straight overhead the cap is all you see of the
    # bulkhead, and in cream it read as a bright slab competing with the
    # skylight field for the eye.
    roof_box("bulkhead_cap", 6.2, 20.4, Z_DECK + 1.30, Z_DECK + 1.44, 3.0, 2.4, steel)
    roof_box("roof_hatch", 2.6, 17.4, Z_DECK, Z_DECK + 0.50, 1.5, 1.2, roofd)
    roof_box("vent_a", 10.4, 20.8, Z_DECK, Z_DECK + 1.00, 0.55, 0.55, steel)
    roof_box("vent_b", 13.2, 19.4, Z_DECK, Z_DECK + 0.80, 0.45, 0.45, steel)
    roof_box("vent_c", 2.4, 12.0, Z_DECK, Z_DECK + 0.75, 0.45, 0.45, steel)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.12/2. The applied facade panels are small and numerous — frames get
    # a token 1-segment softening, fills, glazing bars and glow shells none at
    # all, which is what keeps this under the 8,000-triangle cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow", "_glass", "_door")) or "_bar" in obj.name:
            continue
        if obj.name.endswith(("_frame", "_reveal")) or obj.name.startswith("diamond"):
            bevel(obj, width=0.05, segments=1)
        else:
            bevel(obj, width=0.12, segments=2)

    normalize_height()
    return scene


def normalize_height():
    """Land the bounding-box top exactly on Z_CREST.

    The 0.12 m bevel rounds the ridge edge of the bay roof and takes ~21 mm off
    the apex, so the raw build tops out at 8.579 and the loader's
    targetHeightM / measuredHeight would come out at 1.0025 rather than 1.0.
    A uniform Z-only scale about z=0 fixes it: min Z stays 0, the footprint stays
    exactly on the survey (a uniform XYZ scale would move it ~80 mm, which is
    real-world placement accuracy and belongs to AGENTS rule 5), and 0.25% in Z
    is far below the bevel radius it is correcting for.
    """
    top = max(
        (o.matrix_world @ v.co).z
        for o in bpy.data.objects
        if o.type == "MESH"
        for v in o.data.vertices
    )
    k = Z_CREST / top
    for me in bpy.data.meshes:
        for v in me.vertices:
            v.co.z *= k
    print(f"[build] height normalization: top {top:.4f} -> {Z_CREST} (z scale {k:.6f})")


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
    print("[build] anchor lon/lat: -122.3937450 37.7808430 (footprint OBB centre)")
    print("[build] Brannan front heading: 135.9 deg true (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "362-brannan.blend")
    glb = os.path.join(out, "362-brannan.glb")
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
