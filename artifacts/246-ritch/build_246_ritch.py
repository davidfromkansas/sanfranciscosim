"""Deterministic Blender build of the SF-SIM miniature 246 Ritch Street.

    blender -b --python build_246_ritch.py -- [--out DIR]

Writes 246-ritch.blend and 246-ritch.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint OBB centre (anchor lon -122.3958481,
lat 37.7802253), min Z = 0, roof-penthouse crest exactly 18.76 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured OSM footprint (way/1174904714), reduced to its four real corners
  — the survey's eight vertices lie within 0.05 m of this rectangle, and the two
  sub-metre jogs on the south-east run are noise on a party wall. 16.68 x 22.70 m,
  45 deg off the world axes like the whole SoMa grid. The OSM ring is used rather
  than the DataSF LiDAR ring (395.4 m2) because OSM (378.5 m2) and the surveyed
  lot (383.7 m2) agree with each other, and the LiDAR ring over-reaches at the
  rear (see plan 2.15 risk 2);
* a CREAM STUCCO SLAB with CHARCOAL RECESSED WINDOW BAYS, five storeys, built
  2014 — deliberately not the brick-and-steel loft language of 500 Third across
  the alley and not the low painted timber of 248-250 Ritch next door, which are
  the two easiest mistakes to make on this block;
* the identity feature, carried hard: NINE CANTILEVERED NEAR-BLACK BALCONY BOXES
  on floors 2, 3 and 4 of the Ritch Street front, in a STAGGERED grid — each
  floor skips a different bay, so no two floors line up. Floor 5 carries none, so
  the silhouette ends in a clean band under the parapet;
* the charcoal GROUND-FLOOR BASE BAND at one constant height (3.40 m) across the
  whole frontage, holding the restaurant glazing, the recessed lobby and the
  white sectional garage door — a hard shadow line that separates the pale body
  from the street;
* exactly one fully designed elevation (Ritch NE). The south-east flank stands
  ~8 m proud of 248-250 Ritch (7.95 m) and gets a punched window rank above that;
  the north-west flank is buried against 230/236 Ritch (10.75 m) and stays blind;
  the rear faces a shallow yard and gets windows but no balconies (plan 2.15
  risk 3 — the aerial's rear dark rectangles are unconfirmed);
* night state: the lit restaurant/lobby band inside the dark base as hero glow —
  this building's night identity is a lit restaurant at the bottom of a dark
  alley, the exact inverse of its daytime plinth — plus six scattered lit
  windows. Glow surfaces are thin shells proud of the opaque geometry (the app
  renders _Glow in a separate layer that is ~12% alpha PER LAYER by day, so a
  closed shell reads at ~23%; never author a primary surface as glow);
* a designed roof for the app's downward camera, which on this block face sees
  this roof before any other because it is 5 m higher than anything around it:
  the stair/elevator penthouse that sets the 18.76 m crest (LiDAR max), a
  lightwell/roof-deck recess read graphically as a dark inset inside a low curb,
  and one clean mechanical cluster.

Triangle economy: the primary masses get a 2-segment bevel, the ~60 applied
panels get 1 segment. At 2 segments throughout this model lands near 12k; the
cap is 9,000 and the identity lives in the balcony count, not in bevel profiles.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way/1174904714 projected with the app's tangent projection, recentred on
# the oriented bounding box centre and reduced to four corners.
# CCW, so outward normal = (t.y, -t.x).
FOOTPRINT = [
    (2.18, 13.87),      # north corner
    (-13.98, -2.07),    # west corner
    (-2.19, -13.87),    # south corner
    (13.97, 2.07),      # east corner
]

EDGE_NW = 0      # 22.70 m, faces NW 315.0 deg — party wall against 230/236 Ritch
EDGE_REAR = 1    # 16.68 m, faces SW 225.0 deg — rear, over the yard
EDGE_SE = 2      # 22.70 m, faces SE 135.0 deg — party wall against 248-250 Ritch
EDGE_FRONT = 3   # 16.68 m, faces NE  45.0 deg — RITCH STREET

FRONT_W = 16.68
DEPTH = 22.70

Z_PARAPET = 15.87   # parapet crest = DataSF LiDAR hgt_median 15.87
Z_DECK = 15.12      # roof membrane, 0.75 m below the parapet
Z_CREST = 18.76     # roof penthouse top = LiDAR hgt_max -> the bbox top

Z_BASE = 3.40       # top of the charcoal ground-floor band
FLOOR_H = 3.115     # (15.87 - 3.40) / 4 -> floors 2..5 at 3.40, 6.52, 9.63, 12.75
FLOORS = [Z_BASE + i * FLOOR_H for i in range(4)]   # sill datum of floors 2..5

SKIN = 0.10         # applied-panel standoff from the wall plane
BASE_D = 0.10       # the base band is applied, NOT projecting: every ground-floor
                    # opening layer is dimensioned to sit PROUD of this, so no
                    # frame can ever land in the band's outer plane and z-fight.
PARAPET_T = 0.30

# Ritch Street bays. u runs along the front edge from the EAST corner (where the
# garage is) toward the NORTH corner (where the restaurant is).
N_BAYS = 4
BAY_PITCH = FRONT_W / N_BAYS                       # 4.17 m
BAY_U = [BAY_PITCH * (i + 0.5) for i in range(N_BAYS)]

# The charcoal recesses step sideways floor to floor so the wall reads as an
# interlocking patchwork rather than a grid. Index = floor 2..5.
RECESS_SHIFT = (0.0, 0.55, -0.55, 0.55)

# Balconies: floors 2, 3 and 4 only, three per floor, each floor skipping a
# DIFFERENT bay. This stagger is recognition cue 1 (plan 2.5).
BALCONY_BAYS = {
    0: (0, 1, 3),   # floor 2 — skips bay 2
    1: (0, 2, 3),   # floor 3 — skips bay 1
    2: (1, 2, 3),   # floor 4 — skips bay 0
}

# Restrained night state: six lit windows out of twenty on the front.
LIT_FRONT = {0: {2}, 1: {0}, 2: {1, 3}, 3: {0, 2}}

PALETTE_HEX = {
    # One deliberate palette extension (Toy_slate), a WARN and not a FAIL under
    # the contract, with precedent in 380-brannan and 181-south-park. The repo
    # carries three different Toy_slate values; THIS asset uses 5d646d, chosen so
    # the recesses sit clearly between the cream body and the near-black
    # balconies — Toy_roofd merges with the balconies and kills the patchwork,
    # Toy_steel is too light for the recesses to read as recesses.
    "Toy_slate": "5d646d",
    "Toy_sand": "ece4d4",    # the stucco body, parapet, penthouse walls
    "Toy_trim": "f3efe6",    # window surrounds, garage leaf, shopfront surround
    "Toy_glass": "2a4d73",   # all windows and the ground-floor glazing
    "Toy_steel": "9aa0a6",   # roof membrane, penthouse cap, mechanical blocks
    "Toy_roofd": "45454a",   # parapet coping, screen caps, hatch, plinth — small
                             # dark props only; measured rgb(9,9,12) in the app on
                             # a large up-facing surface (92-south-park)
    "Toy_ink": "3a3530",     # base band, lobby reveal, balcony decks and screens
    "Toy_white": "f7f4ec",   # the "246" numerals
    # Glow colours are the LIT appearance, not the day colour: a night window
    # that glows in its own dark navy reads as a hole.
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
    return offset_polygon_per_edge(poly, [d] * len(poly))


def offset_polygon_per_edge(poly, ds):
    """Miter offset with a separate distance per edge (positive = outward)."""
    npts = len(poly)
    normals = [poly_edge(i, poly)[3] for i in range(npts)]
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
    """Miniature-style edge softening (style bible s.4).

    Width is capped at 30% of the object's thinnest dimension: the applied panels
    here are 70-160 mm thick and an unclamped 0.12 m bevel on those collapses
    opposing profiles into zero-area slivers whose averaged vertex normal is
    zero, which fails the contract validator once gltfpack re-emits them. The
    1 mm remove_doubles/dissolve_degenerate pass sweeps up whatever clamping
    still pinches shut.
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
            verts.append((
                a[0] + t[0] * (u_centre + du) + n[0] * d,
                a[1] + t[1] * (u_centre + du) + n[1] * d,
                z,
            ))
    npts = len(profile)
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def face_box(name, edge, u_centre, z0, z1, w, d0, d1, mat):
    """Axis-in-wall box: w wide along the wall, z0..z1 tall, d0..d1 proud."""
    return face_panel(name, edge, u_centre, rect_profile(w, z0, z1), d0, d1, mat)


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0):
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
    """Roof grid: u along the Ritch front from its EAST corner, v INTO the block
    against the outward normal. The footprint is 16.68 (u) x 22.70 (v)."""
    origin, _l, t, n = poly_edge(EDGE_FRONT)
    return (origin[0] + t[0] * u - n[0] * v, origin[1] + t[1] * u - n[1] * v)


def roof_yaw():
    _o, _l, t, _n = poly_edge(EDGE_FRONT)
    return math.atan2(t[1], t[0])


def roof_box(name, u, v, z0, z1, su, sv, mat):
    cx, cy = roof_uv(u, v)
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=roof_yaw())


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
        # Flagged for the app's night pass; emission is OFF in the day asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# --------------------------------------------------------------------- parts

PANELS = []   # applied panels: 1-segment bevel
MASSES = []   # primary solids: 2-segment bevel


def panel(obj):
    PANELS.append(obj)
    return obj


def mass(obj):
    MASSES.append(obj)
    return obj


def window(tag, edge, u, z_sill, w, h, glass, trim, glow=None, d_base=SKIN):
    """A pale surround with a glass fill proud of it. Two solids, no booleans."""
    panel(face_box(f"{tag}_frame", edge, u, z_sill, z_sill + h, w,
                   0.0, d_base + 0.05, trim))
    inset = 0.14
    panel(face_box(f"{tag}_fill", edge, u, z_sill + inset, z_sill + h - inset,
                   w - 2 * inset, 0.0, d_base + 0.11, glass))
    if glow is not None:
        # A thin shell PROUD of the glazing, and only the lower two thirds of the
        # opening — a lit room reads as light at desk height, and a full-opening
        # shell tints the whole facade by day at ~23% (two alpha layers).
        g = 0.30
        panel(face_box(f"{tag}_glow", edge, u,
                       z_sill + g, z_sill + h * 0.62,
                       w - 2 * g, d_base + 0.08, d_base + 0.14, glow))


def balcony(tag, u, z_floor, ink, roofd):
    """Cantilevered deck + near-black perforated screen, read as a solid panel.

    The real screens are laser-cut with a scatter of short horizontal slots; at
    the app's camera distance that is a fine dark texture, so the model carries
    a solid panel with a lighter cap and lets the value do the work (style
    bible s.4, s.26). Four solids per balcony, nine balconies.
    """
    W = 2.95
    PROJ = 1.05
    panel(face_box(f"{tag}_deck", EDGE_FRONT, u, z_floor - 0.14, z_floor, W,
                   0.0, PROJ, ink))
    panel(face_box(f"{tag}_screen", EDGE_FRONT, u, z_floor, z_floor + 1.28, W,
                   PROJ - 0.08, PROJ, ink))
    for sgn in (-1, 1):
        panel(face_box(f"{tag}_end{sgn}", EDGE_FRONT, u + sgn * (W / 2 - 0.04),
                       z_floor, z_floor + 1.28, 0.08, 0.0, PROJ, ink))
    panel(face_box(f"{tag}_cap", EDGE_FRONT, u, z_floor + 1.28, z_floor + 1.36, W,
                   PROJ - 0.10, PROJ + 0.02, roofd))


def numerals(u, z0, height, depth, mat):
    """The white "246" plate on the pier between the lobby and the restaurant.

    Built from a Blender text object so the digits are real letterforms rather
    than a seven-segment approximation; converted to a mesh immediately so the
    export carries no font dependency.
    """
    a, _l, t, n = poly_edge(EDGE_FRONT)
    bpy.ops.object.text_add(location=(0.0, 0.0, 0.0))
    txt = bpy.context.object
    txt.name = "numerals"
    txt.data.body = "246"
    txt.data.size = height
    txt.data.extrude = 0.05
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
        a[0] + t[0] * u + n[0] * depth,
        a[1] + t[1] * u + n[1] * depth,
        z0 + height / 2.0,
    )
    bpy.context.view_layer.update()
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.select_set(False)
    obj.data.shade_flat()
    return obj


# ---------------------------------------------------------------------- build


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials, bpy.data.curves):
        for item in list(coll):
            coll.remove(item)
    PANELS.clear()
    MASSES.clear()

    sand = material("Toy_sand")
    slate = material("Toy_slate")
    trim = material("Toy_trim")
    glass = material("Toy_glass")
    steel = material("Toy_steel")
    roofd = material("Toy_roofd")
    ink = material("Toy_ink")
    white = material("Toy_white")
    gglow = material("Toy_glass_Glow")
    tglow = material("Toy_trim_Glow")

    # --- masses -------------------------------------------------------------
    # One clean slab filling the lot wall to wall. The body stops at the roof
    # membrane; the parapet is a separate ring so the deck reads as a real tray.
    mass(prism("body", FOOTPRINT, 0.0, Z_DECK, sand, mat_caps=steel))
    mass(ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET, -PARAPET_T, 0.0, sand))
    # The dark coping band under the roof edge — visible in every photograph of
    # this building and what stops the top of the model reading as a bare
    # extrusion. It wraps all four elevations, as the real one does.
    mass(ring_band("coping", FOOTPRINT, Z_PARAPET - 0.40, Z_PARAPET, 0.0, 0.09, roofd))

    # --- ground floor -------------------------------------------------------
    # Applied band, not a projecting plinth: every opening layer below is
    # dimensioned to sit proud of BASE_D, so nothing can land in its outer plane.
    # FRONT and REAR only. Wrapping the band round the footprint put a black bar
    # across both party walls — surfaces that are buried against 7.95 m and
    # 10.75 m neighbours in the city and therefore never seen, but which made the
    # studio elevations read as a building with a plinth on all four sides.
    for edge in (EDGE_FRONT, EDGE_REAR):
        mass(face_box(f"base_band_{edge}", edge, FRONT_W / 2, 0.0, Z_BASE, FRONT_W,
                      0.0, BASE_D, ink))

    # Garage door: white sectional leaf scored into a 3 x 3 grid of square
    # panels. u = 1.1..5.7 from the east corner.
    panel(face_box("garage_leaf", EDGE_FRONT, 3.40, 0.05, 3.05, 4.60,
                   0.0, BASE_D + 0.06, trim))
    for k in (1, 2):
        panel(face_box(f"garage_v{k}", EDGE_FRONT, 3.40 - 2.30 + k * (4.60 / 3),
                       0.10, 3.00, 0.09, 0.0, BASE_D + 0.09, slate))
        panel(face_box(f"garage_h{k}", EDGE_FRONT, 3.40, 0.05 + k * (3.00 / 3),
                       0.05 + k * (3.00 / 3) + 0.09, 4.50, 0.0, BASE_D + 0.09, slate))

    # Lobby: a glazed door set back in a charcoal reveal. u centre 7.60.
    panel(face_box("lobby_reveal", EDGE_FRONT, 7.60, 0.0, 3.05, 2.30,
                   0.0, BASE_D + 0.04, ink))
    panel(face_box("lobby_door", EDGE_FRONT, 7.60, 0.05, 2.85, 1.85,
                   0.0, BASE_D + 0.10, glass))
    panel(face_box("lobby_glow", EDGE_FRONT, 7.60, 0.28, 1.80, 1.35,
                   BASE_D + 0.07, BASE_D + 0.13, tglow))

    # Restaurant shopfront (the old 240 Ritch bakery space, now Wabi-Sabi SF).
    # u = 10.58..15.78 from the east corner.
    panel(face_box("shop_frame", EDGE_FRONT, 13.18, 0.30, 3.05, 5.20,
                   0.0, BASE_D + 0.05, trim))
    panel(face_box("shop_glass", EDGE_FRONT, 13.18, 0.45, 2.90, 4.90,
                   0.0, BASE_D + 0.11, glass))
    # Hero night state: a wide, low, warm band inside the dark base.
    panel(face_box("shop_glow", EDGE_FRONT, 13.18, 0.62, 1.85, 4.10,
                   BASE_D + 0.08, BASE_D + 0.14, tglow))

    numerals(9.55, 2.05, 0.62, BASE_D + 0.03, white)

    # --- Ritch Street front, floors 2-5 -------------------------------------
    # Charcoal recessed bay + window, the recess stepping sideways floor to floor
    # so the wall reads as an interlocking patchwork rather than a grid.
    for fi, z_floor in enumerate(FLOORS):
        shift = RECESS_SHIFT[fi]
        for bi, u0 in enumerate(BAY_U):
            u = u0 + shift
            panel(face_box(f"f{fi}b{bi}_recess", EDGE_FRONT, u,
                           z_floor + 0.10, z_floor + 2.60, 3.10,
                           0.0, SKIN - 0.05, slate))
            window(f"f{fi}b{bi}", EDGE_FRONT, u, z_floor + 0.38, 2.05, 1.92,
                   glass, trim, gglow if bi in LIT_FRONT.get(fi, ()) else None)

    # --- balconies (recognition cue 1) --------------------------------------
    for fi, bays in BALCONY_BAYS.items():
        for bi in bays:
            balcony(f"bal{fi}{bi}", BAY_U[bi], FLOORS[fi] + 0.22, ink, roofd)

    # --- south-east flank ---------------------------------------------------
    # 248-250 Ritch next door is 7.95 m; everything above that is seen from the
    # alley, so floors 4 and 5 get a punched rank and the buried part stays flat.
    for fi in (2, 3):
        for u in (5.70, 11.35, 17.00):
            window(f"se{fi}_{int(u)}", EDGE_SE, u, FLOORS[fi] + 0.42,
                   1.90, 1.95, glass, trim, None)

    # --- rear ---------------------------------------------------------------
    # Over a shallow yard, seen only obliquely from above. Windows, no balconies
    # (plan 2.15 risk 3 — the aerial's rear dark rectangles are unconfirmed).
    for fi in range(4):
        for u in (4.17, 8.34, 12.51):
            window(f"r{fi}_{int(u * 10)}", EDGE_REAR, u, FLOORS[fi] + 0.42,
                   2.00, 2.00, glass, trim, None)

    # --- north-west flank: blind (buried against 230/236 Ritch at 10.75 m) ---

    # --- roof ---------------------------------------------------------------
    # The camera looks down and this roof is 5 m higher than anything on the
    # block, so it is composed rather than furnished (style bible s.10): ONE
    # long dark bar across the middle, ONE block at its east end, and two prop
    # clusters balancing it. The first pass put the penthouse in front of the
    # lightwell from the app's north-east camera and the two read as one
    # confused frame-and-tab shape.

    # Lightwell / roof deck. The MND's 16,442 gsf over five floors is ~305 m2
    # against a 378 m2 footprint, so ~70 m2 of the plan is lightwell; this reads
    # it graphically as a dark inset inside a low curb rather than as a hole.
    LW_U, LW_V, LW_SU, LW_SV = 8.34, 15.00, 10.00, 4.00
    panel(roof_box("deck_slab", LW_U, LW_V, Z_DECK, Z_DECK + 0.07, LW_SU, LW_SV, slate))
    mass(ring_band(
        "deck_curb",
        [roof_uv(LW_U - LW_SU / 2 - 0.02, LW_V - LW_SV / 2 - 0.02),
         roof_uv(LW_U - LW_SU / 2 - 0.02, LW_V + LW_SV / 2 + 0.02),
         roof_uv(LW_U + LW_SU / 2 + 0.02, LW_V + LW_SV / 2 + 0.02),
         roof_uv(LW_U + LW_SU / 2 + 0.02, LW_V - LW_SV / 2 - 0.02)],
        Z_DECK, Z_DECK + 0.22, -0.24, 0.0, sand))

    # The stair/elevator penthouse: the 18.76 m LiDAR maximum, the only break in
    # a dead-flat parapet anywhere on this block face, and the bounding-box top.
    # Sand walls under a dark fascia so it separates from the sand parapet ring;
    # placed clear of the lightwell so neither occludes the other from the NE.
    mass(roof_box("penthouse", 11.80, 8.00, Z_DECK, Z_CREST - 0.42, 4.60, 4.20, sand))
    mass(roof_box("penthouse_fascia", 11.80, 8.00, Z_CREST - 0.42, Z_CREST - 0.10,
                  4.76, 4.36, roofd))
    mass(roof_box("penthouse_cap", 11.80, 8.00, Z_CREST - 0.10, Z_CREST, 4.90, 4.50, trim))

    # Mechanical group on the north-east half, near the street parapet.
    mass(roof_box("mech_plinth", 4.30, 5.20, Z_DECK, Z_DECK + 0.18, 5.30, 2.10, roofd))
    for k, du in enumerate((-1.75, 0.0, 1.75)):
        mass(roof_box(f"mech{k}", 4.30 + du, 5.20, Z_DECK + 0.18, Z_DECK + 1.05,
                      1.50, 1.10, steel))
    # Two vents and a hatch on the rear half, so no quadrant is blank.
    for k, (u, v) in enumerate(((4.10, 19.60), (6.20, 20.30))):
        panel(roof_box(f"vent{k}", u, v, Z_DECK, Z_DECK + 0.60, 1.15, 0.90, steel))
    panel(roof_box("hatch", 14.00, 5.00, Z_DECK, Z_DECK + 0.40, 1.30, 0.95, roofd))

    # --- finishing ----------------------------------------------------------
    for obj in MASSES:
        bevel(obj, width=0.12, segments=2)
    for obj in PANELS:
        bevel(obj, width=0.05, segments=1)

    join_by_material()


def join_by_material():
    """Join every object down to one per material — the loader merges anyway,
    and a 13-object export is what the shipped set looks like."""
    groups = {}
    for obj in list(bpy.data.objects):
        if obj.type != "MESH" or not obj.data.materials:
            continue
        key = tuple(sorted(m.name for m in obj.data.materials if m))
        groups.setdefault(key, []).append(obj)
    for key, objs in groups.items():
        if len(objs) < 2:
            objs[0].name = "part_" + "_".join(key)
            continue
        bpy.ops.object.select_all(action="DESELECT")
        for o in objs:
            o.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]
        bpy.ops.object.join()
        bpy.context.object.name = "part_" + "_".join(key)
        bpy.ops.object.select_all(action="DESELECT")


def report():
    dg = bpy.context.evaluated_depsgraph_get()
    mn = [1e9] * 3
    mx = [-1e9] * 3
    tris = 0
    for o in bpy.data.objects:
        if o.type != "MESH":
            continue
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
        ev.to_mesh_clear()
    print(f"[build] objects={len([o for o in bpy.data.objects if o.type == 'MESH'])} tris={tris}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] min_z={mn[2]:.4f} max_z={mx[2]:.4f} "
          f"center_xy=({(mn[0] + mx[0]) / 2:.3f}, {(mn[1] + mx[1]) / 2:.3f})")
    print(f"[build] materials={sorted(m.name for m in bpy.data.materials)}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "246-ritch.blend")
    glb = os.path.join(out, "246-ritch.glb")
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
