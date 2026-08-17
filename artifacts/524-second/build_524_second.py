"""Deterministic Blender build of the SF-SIM miniature 524 Second Street.

    blender -b --python build_524_second.py -- [--out DIR]

Writes 524-second.blend and 524-second.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint OBB centre (anchor lon -122.3934330,
lat 37.7825731), min Z = 0, merlon tops exactly 9.90 m.

Design (see REFERENCE.md for the sources behind every number):

* the OSM footprint (way 112926337) reduced to its minimum-area rectangle —
  20.92 m of Second Street frontage running 29.63 m back through the lot, at
  45.6 deg off the world axes. Three footprint sources disagree by 12% (DataSF
  LiDAR 570 m2, OSM 620 m2, parcel 639 m2); OSM is used because it sits exactly
  where a lot-line wall sits, inset ~0.3 m per side from the property line, and
  the LiDAR polygon is short specifically on the Second Street edge where a
  19.7 m neighbour across a 6 m alley shadows the scan. This is the OPPOSITE
  call from 358-brannan, where OSM was wrong — reconcile all three every time;
* the recognition cue is the CRENELLATED PARAPET: nine chunky square merlon
  blocks standing 0.58 m proud of a plain brick parapet along the Second Street
  elevation, returning three blocks around the Taber Place corner. Nothing else
  on this block face has it, and on a building with a dead-flat roof it is the
  only silhouette there is. That lift is the one place semantic exaggeration is
  spent;
* the second cue is LOWNESS: a measured 8.96 m roof membrane (DataSF LiDAR
  hgt_median over 2,293 cells, std 0.95 m — a flat roof) between 512 Second at
  19.71 m and 544 Second at 12.83 m. Never raise it to make the facade compose;
* TWO public elevations, not one. This is a corner lot: Taber Place runs the
  full 29.63 m northwest flank ~2.9 m off the wall, so that side gets the same
  brick-pier-and-steel-sash rhythm as the front, nine bays to the front's six.
  The southeast and southwest walls are party walls and stay blind brick;
* a two-tone facade on a hard horizontal line: grey painted ground floor under
  bare red brick. The paint line at 4.05 m on the front and 1.55 m on Taber
  Place is the strongest horizontal in the asset;
* night state: three lit second-floor windows on Second Street and two on
  Taber Place lead, with the entrance bay's sign panel as the single warm
  accent — SF permit 2012-03-27 is an electric single-faced door/window sign
  at this address. The asset plan called the sign the hero; the first night
  review reversed that, because a 1923 office conversion tenanted by a venture
  firm has lit desks, not a marquee. An office with people still in it, not a
  lit-up box. Glow
  surfaces are thin shells proud of the opaque surface behind them (the app
  renders _Glow in a separate layer that is ~12% alpha by day — never author a
  primary surface as glow);
* the roof membrane is Toy_sand, the palest thing on the asset. The Vexcel
  aerial shows a near-white sheet; Toy_roofd and then Toy_steel were both tried
  and both read too dark from the app's downward camera against the baked
  neighbours (measured in the live scene, see REPORT.md s.4).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way 112926337 projected with the app's tangent projection, reduced to its
# minimum-area OBB and recentred on the OBB centre. CCW in (x=east, y=north).
FOOTPRINT = [
    (3.240, 17.813),    # north corner  (Second St x Taber Pl)
    (-17.929, -2.918),  # west corner
    (-3.240, -17.813),  # south corner
    (17.929, 2.918),    # east corner
]

# Edge index -> elevation. Outward normals verified against the survey.
EDGE_TABER = 0   # 29.63 m, faces NW 315.4 deg — Taber Place, a public elevation
EDGE_REAR = 1    # 20.92 m, faces SW 225.6 deg — rear, to the 10 South Park block
EDGE_SE = 2      # 29.63 m, faces SE 135.4 deg — party wall to 544 Second Street
EDGE_FRONT = 3   # 20.92 m, faces NE  45.6 deg — Second Street

# Levels below the deck are photogrammetric: the May 2025 Second Street
# panorama rectified against the measured 20.92 m frontage and a 2.35 m camera
# height derived from the same image. The first build placed the floors ~1 m
# high (glazing at 1.10/5.55) and the aerial review showed a second storey
# riding too close to the parapet; these are the re-measured values.
Z_DECK = 8.96          # roof membrane (DataSF LiDAR hgt_median 8.96 — measured)
Z_PARAPET = 9.32       # parapet coping top (photogrammetric, estimated)
Z_CREST = 9.90         # merlon tops = the bbox top (photogrammetric, estimated)

Z_PAINT = 4.05         # the front's grey/brick paint line
Z_TABER_BASE = 1.55    # the alley base band
Z_G0, Z_G1 = 0.80, 3.75    # ground-floor glazing, Second Street
Z_TG0, Z_TG1 = 1.55, 3.75  # ground-floor glazing, Taber Place
Z_U0, Z_U1 = 4.70, 7.75    # second-floor glazing, both elevations
Z_CORBEL0, Z_CORBEL1 = 8.10, 8.34   # the shallow band under the parapet
Z_DOOR_TOP = 3.20      # the recessed double doors
Z_BAY_TOP = 4.45       # the projecting entrance bay

SKIN = 0.06            # painted base band, proud of the brick shell
PARAPET_T = 0.35
COPING_H = 0.12
BAY_PROJ = 0.45

FRONT_BAYS = 6
TABER_BAYS = 9
FRONT_OPEN_W = 2.50
TABER_OPEN_W = 2.30

# The first aerial review read the merlons as a faint dotted line — fatal for
# the one cue this building has. Widened 0.85 -> 1.00, deepened 0.40 -> 0.48,
# and the coping dropped from 9.45 to 9.32 so the blocks stand 0.58 m proud
# instead of 0.45. This is the semantic exaggeration the style bible allows,
# spent in the one place it is worth spending.
MERLON_W = 1.00
MERLON_H = Z_CREST - Z_PARAPET
MERLON_D0, MERLON_D1 = -0.34, 0.14   # straddles the 0.35 m parapet, 0.14 m proud

PALETTE_HEX = {
    "Toy_brick": "c96f4a",
    # The real ground-floor paint is a warm mid-grey, greyer than Toy_stone and
    # lighter than Toy_steel. Toy_stone is used because the asset's job at
    # distance is a LIGHT base under dark brick, and Toy_steel would read as
    # metal next to the rooftop plant. 358-brannan splits stone/brick
    # front-to-back; here the split is horizontal, which is what keeps the two
    # SoMa warehouses from reading as one building twice.
    "Toy_stone": "d9d2c2",
    # The roof membrane. Toy_steel (#9aa0a6) was tried first, following
    # 358-brannan's log; in the LIVE SCENE at the app's downward camera the lit
    # deck measured (90,98,107) against (146,133,104) on the baked neighbours —
    # 27% darker and cooler, the darkest roof on the block. The Vexcel aerial
    # shows this roof as a near-WHITE membrane, so Toy_sand is both truer and
    # the better top-down read, and it lets the brick parapet ring carry the
    # roof edge instead of fighting a mid-grey deck.
    "Toy_sand": "ece4d4",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_roofd": "45454a",
    # Toy_steel doubles as the light roof membrane (see module docstring).
    "Toy_steel": "9aa0a6",
    "Toy_ink": "3a3530",
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

# --------------------------------------------------------------- 2D helpers


def edge_frame(poly, i):
    """Edge i of a CCW polygon: (origin, length, tangent unit, outward normal)."""
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def poly_edge(i):
    return edge_frame(FOOTPRINT, i)


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


def bay_centres(edge, count):
    """Structural bay centres along an edge, in that edge's u coordinate."""
    _a, length, _t, _n = poly_edge(edge)
    pitch = length / count
    return [(i + 0.5) * pitch for i in range(count)]


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
    """Miniature-style edge softening (style bible s.4). Width is capped at a
    third of the object's thinnest dimension: the applied panels here are only
    60-200 mm thick, and a flat bevel on those relies entirely on clamp_overlap,
    which collapses opposing profiles into zero-area slivers."""
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


def wall_panel(name, frame, u_centre, profile, d0, d1, mat):
    """Closed prism of a (u, z) profile lying in a wall plane, extruded outward
    from offset d0 to d1 along that wall's normal. `frame` is (origin, t, n)."""
    a, t, n = frame
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


def edge_wall(edge):
    a, _length, t, n = poly_edge(edge)
    return (a, t, n)


def face_panel(name, edge, u_centre, profile, d0, d1, mat):
    return wall_panel(name, edge_wall(edge), u_centre, profile, d0, d1, mat)


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


def roof_box(name, u, v, z0, z1, su, sv, mat):
    """Box on the roof, aligned to the building's own grid: u runs along the
    Second Street edge from its southeast (544) end, v runs INTO the block."""
    origin, _l, t, n = poly_edge(EDGE_FRONT)
    cx = origin[0] + t[0] * u - n[0] * v
    cy = origin[1] + t[1] * u - n[1] * v
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=math.atan2(t[1], t[0]))


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


def rect_opening(tag, frame, u, w, z0, z1, frame_mat, fill_mat, base_d, glow_mat=None):
    """Frame panel + a smaller fill that protrudes further, so the frame reads
    as a border ring around a recessed opening. No booleans, all closed solids."""
    wall_panel(f"{tag}_frame", frame, u, rect_profile(w, z0, z1), 0.0, base_d + 0.06, frame_mat)
    inset = 0.16
    wall_panel(
        f"{tag}_fill",
        frame,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        0.0,
        base_d + 0.13,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.30
        wall_panel(
            f"{tag}_glow",
            frame,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            base_d + 0.10,
            base_d + 0.17,
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
    glassl = material("Toy_glassl")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    sand = material("Toy_sand")
    ink = material("Toy_ink")
    gold_glow = material("Toy_gold_Glow")
    glass_glow = material("Toy_glass_Glow")

    _a_f, len_f, _t_f, _n_f = poly_edge(EDGE_FRONT)
    _a_t, len_t, _t_t, _n_t = poly_edge(EDGE_TABER)
    front = edge_wall(EDGE_FRONT)
    taber = edge_wall(EDGE_TABER)

    # --- shell: red brick body, its cap IS the pale roof membrane -----------
    prism("body", FOOTPRINT, 0.0, Z_DECK, brick, mat_caps=sand)

    # --- parapet ring and coping, continuous on all four sides --------------
    # The coping is BRICK, not stone. Authored pale first, it swallowed the
    # merlons: nine Toy_stone blocks sitting on a continuous Toy_stone band read
    # as one lumpy ledge from the aerial camera. A brick parapet with pale
    # blocks on it is both what the panorama shows and the higher-contrast
    # reading of the only cue this building has.
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET - COPING_H, -PARAPET_T, 0.0, brick)
    ring_band(
        "coping", FOOTPRINT, Z_PARAPET - COPING_H, Z_PARAPET, -PARAPET_T - 0.06, 0.06, brick
    )

    # --- THE identity cue: the crenellated parapet --------------------------
    # Nine blocks across the 20.92 m Second Street frontage at 2.509 m centres,
    # the outermost pair landing on the corners; three continue around the
    # Taber Place corner on the same pitch. Their tops set the bbox crest.
    step = (len_f - MERLON_W) / 8.0
    for i in range(9):
        wall_panel(
            f"merlon_f{i}",
            front,
            MERLON_W / 2.0 + step * i,
            rect_profile(MERLON_W, Z_PARAPET, Z_CREST),
            MERLON_D0,
            MERLON_D1,
            stone,
        )
    # EDGE_TABER starts AT the Second Street corner (FOOTPRINT[0]), so u is
    # already measured from the street — the first build subtracted it from the
    # edge length and put the return 22 m away at the rear corner.
    for i, u in enumerate((1.70, 4.21, 6.72)):
        wall_panel(
            f"merlon_t{i}",
            taber,
            u,
            rect_profile(MERLON_W, Z_PARAPET, Z_CREST),
            MERLON_D0,
            MERLON_D1,
            stone,
        )

    # --- the shallow brick band under the parapet, both public elevations ---
    for tag, edge, ln in (("f", EDGE_FRONT, len_f), ("t", EDGE_TABER, len_t)):
        face_panel(
            f"corbel_{tag}",
            edge,
            ln / 2.0,
            rect_profile(ln - 0.20, Z_CORBEL0, Z_CORBEL1),
            0.0,
            0.10,
            brick,
        )

    # --- Second Street: the grey painted base under bare brick --------------
    face_panel(
        "front_base", EDGE_FRONT, len_f / 2.0, rect_profile(len_f, 0.0, Z_PAINT), 0.0, SKIN, stone
    )
    face_panel(
        "front_paintline",
        EDGE_FRONT,
        len_f / 2.0,
        rect_profile(len_f, Z_PAINT - 0.15, Z_PAINT),
        0.0,
        SKIN + 0.06,
        stone,
    )

    fbays = bay_centres(EDGE_FRONT, FRONT_BAYS)
    # Ground floor: storefront glazing in five bays, the recessed dark double
    # doors in the second bay from the 544 end (photographed at u ~ 5.2 m).
    DOOR_BAY = 1
    for i, u in enumerate(fbays):
        if i == DOOR_BAY:
            rect_opening("front_door", front, u, 2.20, 0.0, Z_DOOR_TOP, stone, ink, SKIN)
        else:
            rect_opening(
                f"front_g{i}", front, u, FRONT_OPEN_W, Z_G0, Z_G1, stone, glass, SKIN
            )
    # Second floor: six bays of dark steel sash; three lit at night.
    for i, u in enumerate(fbays):
        rect_opening(
            f"front_u{i}",
            front,
            u,
            FRONT_OPEN_W,
            Z_U0,
            Z_U1,
            roofd,
            glass,
            0.0,
            glass_glow if i in (1, 3, 5) else None,
        )

    # --- the projecting grey entrance bay, dead centre on the front ---------
    # Photographed centred on the facade, straddling the pier between bays 2
    # and 3; it overlaps the neighbouring frames by ~0.45 m, which is fine —
    # these are independent closed solids, not a boolean union.
    uc = len_f / 2.0
    wall_panel(
        "entry_bay", front, uc, rect_profile(2.40, 0.0, Z_BAY_TOP), 0.0, SKIN + BAY_PROJ, stone
    )
    wall_panel(
        "entry_cap",
        front,
        uc,
        rect_profile(2.62, Z_BAY_TOP - 0.22, Z_BAY_TOP),
        0.0,
        SKIN + BAY_PROJ + 0.12,
        stone,
    )
    wall_panel(
        "entry_glass",
        front,
        uc,
        rect_profile(1.60, 1.05, 3.25),
        SKIN + BAY_PROJ - 0.02,
        SKIN + BAY_PROJ + 0.05,
        glass,
    )
    # the night hero: the 2012-permitted electric door sign, a thin shell proud
    # of the opaque bay behind it
    wall_panel(
        "entry_sign",
        front,
        uc,
        rect_profile(2.16, 3.39, 4.05),
        SKIN + BAY_PROJ,
        SKIN + BAY_PROJ + 0.07,
        ink,
    )
    wall_panel(
        "entry_sign_glow",
        front,
        uc,
        rect_profile(1.90, 3.51, 3.95),
        SKIN + BAY_PROJ + 0.05,
        SKIN + BAY_PROJ + 0.12,
        gold_glow,
    )

    # --- Taber Place: the second public elevation ---------------------------
    face_panel(
        "taber_base",
        EDGE_TABER,
        len_t / 2.0,
        rect_profile(len_t, 0.0, Z_TABER_BASE),
        0.0,
        SKIN,
        stone,
    )
    tbays = bay_centres(EDGE_TABER, TABER_BAYS)
    for i, u in enumerate(tbays):
        rect_opening(f"taber_g{i}", taber, u, TABER_OPEN_W, Z_TG0, Z_TG1, roofd, glass, SKIN)
        rect_opening(
            f"taber_u{i}",
            taber,
            u,
            TABER_OPEN_W,
            Z_U0,
            Z_U1,
            roofd,
            glass,
            0.0,
            glass_glow if i in (2, 6) else None,
        )

    # --- roof: 620 m2 of flat membrane, and the camera looks straight at it --
    # u runs along the Second Street edge from its southeast (544) end
    # (0 .. 20.92); v runs back into the block from that edge (0 .. 29.63).
    # The plant is grouped toward the street third so the middle stays open;
    # the skylights read as a loose diagonal, matching the Vexcel aerial.
    for i, (u, v) in enumerate(((7.0, 11.0), (10.5, 14.6), (14.0, 18.2))):
        roof_box(f"skylight_kerb{i}", u, v, Z_DECK, Z_DECK + 0.16, 2.30, 1.70, stone)
        roof_box(f"skylight{i}", u, v, Z_DECK + 0.12, Z_DECK + 0.34, 2.02, 1.44, glassl)
    # No plant may out-top the merlons: the crest must be the identity cue, and
    # the street-level panorama confirms nothing shows above the parapet line.
    # 0.85 m is therefore the ceiling here (Z_DECK + 0.85 = 9.81 < Z_CREST).
    roof_box("rtu0", 6.2, 5.4, Z_DECK, Z_DECK + 0.85, 1.80, 1.40, steel)
    roof_box("rtu1", 9.6, 4.4, Z_DECK, Z_DECK + 0.72, 1.40, 1.20, steel)
    roof_box("condenser", 13.1, 6.0, Z_DECK, Z_DECK + 0.64, 1.10, 1.10, steel)
    # The Vexcel aerial shows a straight diagonal run of small fixtures crossing
    # the deck; five vents on that line keep the rear half from reading dead
    # without adding anything the imagery does not show.
    for i, (u, v) in enumerate(
        ((4.2, 9.2), (5.4, 16.4), (16.2, 12.1), (8.0, 21.4), (11.4, 25.0))
    ):
        roof_box(f"exhaust{i}", u, v, Z_DECK, Z_DECK + 0.45, 0.62, 0.62, roofd)
    roof_box("roof_hatch", 17.4, 22.3, Z_DECK, Z_DECK + 0.40, 1.20, 1.00, roofd)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.10/2. Applied panels are small and numerous — their frames get a
    # token 1-segment softening and the fills/glow shells none at all. The
    # merlons get the full bevel: they ARE the silhouette.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")):
            continue
        if obj.name.endswith("_frame") or obj.name.startswith(
            ("corbel", "front_paintline", "entry_sign", "entry_cap", "entry_glass")
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
    print("[build] anchor lon/lat: -122.3934330 37.7825731 (footprint OBB centre)")
    print("[build] Second Street front heading: 45.6 deg true (NE)")
    print("[build] Taber Place flank heading: 315.4 deg true (NW)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "524-second.blend")
    glb = os.path.join(out, "524-second.glb")
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
