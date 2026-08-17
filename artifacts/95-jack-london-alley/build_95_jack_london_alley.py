"""Deterministic Blender build of the SF-SIM miniature 95 Jack London Alley
(Gran Oriente Filipino Masonic Temple, 1951).

    blender -b --python build_95_jack_london_alley.py -- [--out DIR]

Writes 95-jack-london-alley.blend and 95-jack-london-alley.glb next to this file
(or into --out). Geometry is authored directly in world space in metres, Z up,
+X east, +Y north, so the model drops into the city at its real-world heading —
the loader applies no rotation. Origin = DataSF LiDAR footprint area centroid
(anchor lon -122.3934430, lat 37.7813460), min Z = 0, facade parapet crest
exactly 8.40 m.

Design (see REFERENCE.md for the sources behind every number):

* the footprint is the DataSF LiDAR polygon (sf16_bldgid 201006.0108499),
  8.60 m of frontage on Jack London Alley running back 13.70 m, at 45.9 deg like
  the whole SoMa grid. OSM way/71211338 traces the same building 6.6 m deeper and
  is WRONG — DataSF assigns that strip to 41-43 South Park and Bing z20 shows a
  tree in a yard there. See the plan's 2.3;
* a two-storey blush-pink stucco box with a parapet all round, stepping up
  0.25 m at the alley end to carry the DEDICATED TO THE SUPREME ARCHITECT OF THE
  UNIVERSE course. Three of the four elevations are essentially blank, which is
  true and is itself a cue: this is a hall, not a house;
* the identity feature, and the reason this asset exists: the MOORISH ENTRANCE.
  A real recess (the only boolean in the build) 2.60 m wide and 0.75 m deep with
  a two-centre pointed arch, a trilobed glazed transom inside it, the gold
  square-and-compass on the centre lobe, and two free-standing white columns
  capped with spheres — Jachin and Boaz. At the app's distance it collapses to a
  dark notch with two bright dots either side, which is still unmistakable;
* the north-west flank is NOT a party wall (designation report: stucco on "the
  façade and north elevation") and carries a dentilled parapet band, the only
  ornament on the building besides the doorway;
* night state: the emblem is the hero, the two globes are the supporting accent,
  and a thin spill lights the recess. Nothing else lights — category 8 is night
  profile 3 (dark) and a lodge that meets a few evenings a month should be one of
  the quietest things in the night city. Glow shells are small and closed: closed
  shells read ~23% alpha by day rather than 12%, which is why every one of them
  here sits over opaque geometry of the SAME colour and covers under 1 m2;
* a designed roof for the app's downward camera: charcoal deck, bright coping
  ring, the facade parapet reading as a thicker brighter bar at the alley end,
  the dentil band down one long side only, and three small boxes.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF LiDAR footprint 201006.0108499, reduced to its min-area oriented box
# and recentred on the polygon's area centroid. CCW, +X east, +Y north.
HALF_LONG = 6.85    # 13.70 m depth, running back at 45.9 deg
HALF_SHORT = 4.30   # 8.60 m frontage on Jack London Alley
HEADING = math.radians(45.87)

_L = (math.sin(HEADING), math.cos(HEADING))                    # toward the rear (NE)
_S = (math.sin(HEADING + math.pi / 2), math.cos(HEADING + math.pi / 2))  # toward the SE


def _corner(sl, ss):
    return (
        sl * HALF_LONG * _L[0] + ss * HALF_SHORT * _S[0],
        sl * HALF_LONG * _L[1] + ss * HALF_SHORT * _S[1],
    )


FOOTPRINT = [
    _corner(-1, -1),   # 0  alley / north-west corner
    _corner(-1, +1),   # 1  alley / south-east corner
    _corner(+1, +1),   # 2  rear  / south-east corner
    _corner(+1, -1),   # 3  rear  / north-west corner
]

EDGE_FACADE = 0   # 8.60 m, faces SW 225.9 deg — Jack London Alley, the public face
EDGE_SE = 1       # 13.70 m, faces SE 135.9 deg — toward the warehouse
EDGE_REAR = 2     # 8.60 m, faces NE  45.9 deg — the yard
EDGE_NW = 3       # 13.70 m, faces NW 315.9 deg — toward 45-49 South Park

Z_DECK = 7.84        # roof deck (LiDAR median 7.84, majority 7.76)
Z_PAR = 8.05         # side/rear parapet wall top
Z_PAR_COPE = 8.15    # side/rear coping crest
Z_FAC_PAR = 8.30     # facade parapet wall top
Z_CREST = 8.40       # facade coping crest = the bbox top

PARAPET_T = 0.22
FRONTAGE = 2.0 * HALF_SHORT
DEPTH = 2.0 * HALF_LONG

# Entrance: two-centre pointed arch. Half-width a, arc centres at +-ARC_D on the
# springing line, so the apex lands at Z_SPRING + sqrt((a+d)^2 - d^2).
ENT_W = 2.60
ENT_HALF = ENT_W / 2.0
ENT_SPRING = 1.75
ARC_D = 0.40
ENT_APEX = ENT_SPRING + math.sqrt((ENT_HALF + ARC_D) ** 2 - ARC_D ** 2)  # 3.40 m
ENT_DEPTH = 0.75

SKIN = 0.0

PALETTE_HEX = {
    # Toy_peach and Toy_coral carry adjusted hexes under the style bible's SF
    # exception for tinted facades, the same convention 165 South Park used for
    # Toy_steel: the palette KEY is kept so the contract check stays meaningful,
    # the value moves to the building's real colour. This building is pink in a
    # block of gray, white and olive, and that is recognition cue #2.
    "Toy_peach": "e8cdc9",
    "Toy_coral": "d9a189",
    "Toy_trim": "f3efe6",
    "Toy_stone": "d9d2c2",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_ink": "3a3530",
    "Toy_gold": "caa64a",
    "Toy_roofd": "45454a",
    "Toy_rust": "a86444",
    "Toy_steel": "9aa0a6",
    "Toy_gold_Glow": "e6c46a",
    "Toy_trim_Glow": "f6e6c4",
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


def edge_point(edge, u, d):
    """World XY of the point u metres along `edge` and d metres outward of it."""
    a, _length, t, n = poly_edge(edge)
    return (a[0] + t[0] * u + n[0] * d, a[1] + t[1] * u + n[1] * d)


def offset_polygon(poly, d):
    """Miter offset of the CCW footprint; positive d moves outward."""
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


def pointed_profile(w, z0, z_spring, arc_d, seg=7):
    """Closed (u, z) profile: jambs to the springing, then a two-centre pointed
    arch. arc_d > 0 puts the arc centres outside the opening, which is what makes
    the head come to a point instead of a semicircle."""
    a = w / 2.0
    r = a + arc_d
    apex = z_spring + math.sqrt(r * r - arc_d * arc_d)
    pts = [(-a, z0), (a, z0), (a, z_spring)]
    # right-hand arc, centre (-arc_d, z_spring): from the right springing up to
    # the apex; then mirror for the left-hand arc.
    th0 = math.atan2(0.0, a + arc_d)
    th1 = math.atan2(apex - z_spring, arc_d)
    for k in range(1, seg + 1):
        th = th0 + (th1 - th0) * k / seg
        pts.append((-arc_d + r * math.cos(th), z_spring + r * math.sin(th)))
    for k in range(seg - 1, -1, -1):
        th = th0 + (th1 - th0) * k / seg
        pts.append((arc_d - r * math.cos(th), z_spring + r * math.sin(th)))
    # k == 0 already lands exactly on (-a, z_spring); appending it again closed
    # the profile on a duplicate vertex and produced four zero-area triangles in
    # recess_back, the one object that never goes through the bevel pass (whose
    # remove_doubles had been quietly hiding the same bug in the arch cutter).
    return pts


def trilobe_profile(w, z0, z_spring, rise, seg=5):
    """Closed (u, z) profile: a rectangle whose head is three tangent lobes.

    This is how the plan's 2.6 asks the tripartite arcade to be carried — one
    glazed panel cut to a trilobe silhouette, not three modelled arches.
    """
    a = w / 2.0
    half = w / 6.0
    pts = [(-a, z0), (a, z0), (a, z_spring)]
    for j in range(3):
        c = a - (2 * j + 1) * half
        for k in range(1, seg + 1):
            th = math.pi * k / seg
            pts.append((c + half * math.cos(th), z_spring + rise * math.sin(th)))
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


def bevel(obj, width=0.08, segments=2):
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
    extruded from offset d0 to d1 along that wall's outward normal."""
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


def cylinder(name, cx, cy, z0, z1, radius, mat, seg=10):
    ring = [
        (cx + radius * math.cos(2 * math.pi * k / seg), cy + radius * math.sin(2 * math.pi * k / seg))
        for k in range(seg)
    ]
    return prism(name, ring, z0, z1, mat)


def sphere(name, cx, cy, cz, radius, mat, seg=10, rings=5):
    """Closed low-poly UV sphere (style bible s.4: chunky, few segments)."""
    verts = [(cx, cy, cz - radius)]
    for r in range(1, rings):
        phi = math.pi * r / rings
        z = cz - radius * math.cos(phi)
        rr = radius * math.sin(phi)
        for k in range(seg):
            th = 2 * math.pi * k / seg
            verts.append((cx + rr * math.cos(th), cy + rr * math.sin(th), z))
    verts.append((cx, cy, cz + radius))
    top = len(verts) - 1
    faces = []
    for k in range(seg):
        faces.append((0, 1 + (k + 1) % seg, 1 + k))
    for r in range(rings - 2):
        a0 = 1 + r * seg
        b0 = a0 + seg
        for k in range(seg):
            k2 = (k + 1) % seg
            faces.append((a0 + k, a0 + k2, b0 + k2, b0 + k))
    a0 = 1 + (rings - 2) * seg
    for k in range(seg):
        faces.append((top, a0 + k, a0 + (k + 1) % seg))
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
    """Applied frame + proud fill, the repo's standard no-boolean opening."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, SKIN + 0.07, frame_mat)
    inset = 0.14
    face_panel(
        f"{tag}_fill",
        edge,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        0.0,
        SKIN + 0.13,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.24
        face_panel(
            f"{tag}_glow",
            edge,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            SKIN + 0.10,
            SKIN + 0.17,
            glow_mat,
        )


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    peach = material("Toy_peach")
    coral = material("Toy_coral")
    trim = material("Toy_trim")
    stone = material("Toy_stone")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    ink = material("Toy_ink")
    gold = material("Toy_gold")
    roofd = material("Toy_roofd")
    rust = material("Toy_rust")
    steel = material("Toy_steel")
    gold_glow = material("Toy_gold_Glow")
    trim_glow = material("Toy_trim_Glow")

    uc = FRONTAGE / 2.0          # facade centreline, measured from the NW corner
    ur = DEPTH / 2.0             # midpoint of a long flank
    ue = FRONTAGE / 2.0          # midpoint of the rear wall

    # --- stucco body; its top cap IS the dark roof deck ---------------------
    body = prism("body", FOOTPRINT, 0.0, Z_DECK, peach, mat_caps=roofd)

    # --- THE ENTRANCE RECESS: the only boolean in the build -----------------
    # A real 0.75 m recess, because the whole asset rests on this notch reading
    # from the app's camera. The cutter carries Toy_coral so the jambs, soffit
    # and back plane come out of the difference already in the warmer colour the
    # photographs show inside the opening.
    cutter = face_panel(
        "entrance_cut",
        EDGE_FACADE,
        uc,
        pointed_profile(ENT_W, -0.30, ENT_SPRING, ARC_D),
        -ENT_DEPTH,
        0.35,
        coral,
    )
    bpy.context.view_layer.objects.active = body
    mod = body.modifiers.new("entrance", "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.object = cutter
    mod.solver = "EXACT"
    bpy.ops.object.modifier_apply(modifier="entrance")
    bpy.data.objects.remove(cutter, do_unlink=True)

    # --- parapet: three sides low, the alley end 0.25 m higher --------------
    # Revision 2 (see REPORT.md). The first pass carried a continuous coping ring
    # right round at 8.15 and then stacked the facade parapet on top of it, which
    # from square-on read as a fussy TRIPLE cornice the real building does not
    # have — its alley parapet is one flat plane with a single thin cap and the
    # dedication course incised into it. The ring now stops at the two front
    # corners and the facade parapet runs flush with the wall below it.
    # Revision 3: the flanks were extended 0.145 m past both their ends so the
    # corners would close, which left two coping stubs poking out either side of
    # the taller facade cap like door handles. Only the REAR panel oversails now
    # (it has two ordinary corners to close); the flanks stop dead on the front
    # corners, which is exactly where the real parapet steps up.
    for tag, edge, span, over in (
        ("se", EDGE_SE, DEPTH, 0.0),
        ("rear", EDGE_REAR, FRONTAGE, 0.44),
        ("nw", EDGE_NW, DEPTH, 0.0),
    ):
        mid = span / 2.0
        face_panel(f"parapet_{tag}", edge, mid, rect_profile(span + over, Z_DECK, Z_PAR),
                   -PARAPET_T, 0.0, peach)
        face_panel(f"coping_{tag}", edge, mid,
                   rect_profile(span + (0.72 if over else 0.0), Z_PAR, Z_PAR_COPE),
                   -PARAPET_T - 0.07, 0.07, trim)
    face_panel(
        "facade_parapet",
        EDGE_FACADE,
        uc,
        rect_profile(FRONTAGE, Z_DECK, Z_FAC_PAR),
        -PARAPET_T,
        0.0,
        peach,
    )
    face_panel(
        "facade_coping",
        EDGE_FACADE,
        uc,
        rect_profile(FRONTAGE + 0.14, Z_FAC_PAR, Z_CREST),
        -PARAPET_T - 0.07,
        0.07,
        trim,
    )

    # --- the dentil band, north-west flank only -----------------------------
    # The designation report's "cornice", and the only ornament on the building
    # besides the doorway. Individual teeth are far below a pixel in the app, so
    # it is one band with the bevel doing the shadow (plan 2.6).
    face_panel(
        "dentil_nw",
        EDGE_NW,
        ur,
        rect_profile(DEPTH - 0.10, Z_DECK + 0.06, Z_DECK + 0.26),
        0.0,
        0.07,
        trim,
    )

    # --- alley facade: the two incised text courses -------------------------
    # Bands of a marginally different value, applied proud rather than incised —
    # the repo builds openings and bands this way throughout, and at 8.6 m across
    # the reading is identical. NO GLYPHS, at any scale.
    # Revision 2: the name course was a 6.00 x 1.02 m Toy_stone slab and read as
    # an applied sign panel — the real thing is text cut into pink stucco with no
    # panel behind it at all. It is now Toy_peach, so the bevel's shadow line is
    # the whole of it, which is what incised text looks like from 150 m up. The
    # dedication course keeps a light value because the photograph really does
    # show a lighter incised band under the coping, and it is thinner now.
    face_panel(
        "text_dedicated",
        EDGE_FACADE,
        uc,
        rect_profile(FRONTAGE - 1.20, 8.02, 8.22),
        0.0,
        0.02,
        stone,
    )
    face_panel(
        "text_name",
        EDGE_FACADE,
        uc,
        rect_profile(5.60, 3.66, 4.51),
        0.0,
        0.035,
        peach,
    )

    # --- alley facade: openings ---------------------------------------------
    # The second-floor window is HORIZONTAL — a vertical one there mis-reads the
    # building as a house. Toy_glassl rather than Toy_glass because the real one
    # is filled with an amber grille and reads light, not dark.
    rect_opening("f2_win", EDGE_FACADE, uc, 1.80, 5.35, 6.30, trim, glassl)
    # Flanking windows, built SYMMETRIC at +-2.85 m. The one square-on photograph
    # hints they are not (see the plan's 2.15 risk 3 and REPORT.md); with the
    # evidence inconclusive, the plan's own fallback is symmetry, because a wrong
    # asymmetry looks deliberate and gets copied forward.
    for tag, du in (("nw", -2.85), ("se", +2.85)):
        rect_opening(f"fg_{tag}", EDGE_FACADE, uc + du, 0.95, 1.35, 2.40, trim, glass)

    # --- inside the recess ---------------------------------------------------
    back = -ENT_DEPTH
    # Revision 3. The cutter was given Toy_coral on the assumption that Blender's
    # exact boolean would carry the operand material onto the new faces; it does
    # not, and the whole recess came out of the difference in Toy_peach. The
    # tympanum is therefore an explicit coral plane at the back of the opening —
    # which is also where the warmth actually shows in the reference photograph
    # (the arch reveal itself really is the same stucco as the facade).
    face_panel(
        "recess_back",
        EDGE_FACADE,
        uc,
        pointed_profile(ENT_W - 0.03, 0.0, ENT_SPRING, ARC_D),
        back - 0.02,
        back + 0.02,
        coral,
    )
    face_panel(
        "doors",
        EDGE_FACADE,
        uc,
        rect_profile(1.62, 0.0, 2.10),
        back,
        back + 0.06,
        ink,
    )
    face_panel(
        "door_reveal",
        EDGE_FACADE,
        uc,
        rect_profile(0.05, 0.10, 2.00),
        back + 0.06,
        back + 0.08,
        trim,
    )
    # The tripartite transom, carried as ONE trilobed glazed panel (plan 2.6).
    face_panel(
        "transom",
        EDGE_FACADE,
        uc,
        trilobe_profile(2.32, 2.10, 2.36, 0.50),
        back + 0.02,
        back + 0.08,
        glass,
    )
    for k, du in enumerate((-0.387, 0.387)):
        face_panel(
            f"transom_mull{k}",
            EDGE_FACADE,
            uc + du,
            rect_profile(0.09, 2.10, 2.42),
            back + 0.08,
            back + 0.14,
            trim,
        )
    # The gold square-and-compass with the letter G, on the centre lobe.
    face_panel(
        "emblem",
        EDGE_FACADE,
        uc,
        rect_profile(0.46, 2.30, 2.76),
        back + 0.08,
        back + 0.10,
        gold,
    )
    face_panel(
        "emblem_glow",
        EDGE_FACADE,
        uc,
        rect_profile(0.44, 2.31, 2.75),
        back + 0.10,
        back + 0.12,
        gold_glow,
    )
    # Thin warm spill across the floor of the recess: at night this is what says
    # the notch is a doorway rather than a hole.
    face_panel(
        "recess_spill",
        EDGE_FACADE,
        uc,
        rect_profile(1.75, 0.02, 0.14),
        back + 0.10,
        back + 0.16,
        trim_glow,
    )

    # --- Jachin and Boaz -----------------------------------------------------
    # Free-standing in the recess, 0.45 m proud of the door plane. At thumbnail
    # size the whole entrance reduces to a dark notch with these two bright dots
    # either side, which is recognition cue #3 and the reason they get spheres
    # rather than a cheaper cap.
    for tag, du in (("nw", -0.95), ("se", +0.95)):
        cx, cy = edge_point(EDGE_FACADE, uc + du, back + 0.45)
        box(f"col_{tag}_plinth", cx, cy, 0.0, 0.14, 0.34, 0.34, trim,
            yaw=math.atan2(poly_edge(EDGE_FACADE)[2][1], poly_edge(EDGE_FACADE)[2][0]))
        cylinder(f"col_{tag}_shaft", cx, cy, 0.14, 2.14, 0.11, trim, seg=10)
        sphere(f"col_{tag}_globe", cx, cy, 2.30, 0.16, trim, seg=10, rings=5)
        # Glow shell over an opaque globe of the SAME colour: a closed shell is
        # two alpha layers (~23% by day, not 12%), so it may only ever sit over
        # matching geometry and must stay small. 0.07 m2 each, near-white on
        # near-white — invisible by day, two warm points at night.
        sphere(f"col_{tag}_globe_glow", cx, cy, 2.30, 0.185, trim_glow, seg=10, rings=5)

    # --- the three plain elevations -----------------------------------------
    # Assumed, not observed: no photograph of the south-east flank or the rear
    # was located. A lodge hall's back walls are genuinely plain, so this is one
    # service door and two small openings and nothing else (plan 2.4, 2.15 risk 4).
    rect_opening("rear_door", EDGE_REAR, ue - 1.60, 1.10, 0.0, 2.10, trim, ink)
    rect_opening("rear_win", EDGE_REAR, ue + 1.90, 0.70, 5.20, 5.90, trim, glass)
    rect_opening("se_win", EDGE_SE, ur - 2.40, 0.70, 5.20, 5.90, trim, glass)
    # Revision 4: the north-west flank was left completely blank, and it is the
    # one secondary elevation there IS a photograph of — the 2016 oblique shows a
    # small opening near the alley end and a projecting element above it. Both
    # are here now, at the alley end (u -> DEPTH on this edge).
    rect_opening("nw_win", EDGE_NW, DEPTH - 2.60, 0.70, 5.20, 5.90, trim, glass)
    face_panel(
        "nw_flue",
        EDGE_NW,
        DEPTH - 1.30,
        rect_profile(0.45, 3.10, Z_DECK + 0.55),
        0.0,
        0.22,
        peach,
    )

    # --- roof furniture ------------------------------------------------------
    # Bing z20 shows a light patch near the north-west edge and two small
    # reddish boxes near the alley end. No PV, no bulkhead, no plant. Resist
    # inventing more (plan 2.9).
    yaw = math.atan2(_L[1], _L[0])
    cx, cy = edge_point(EDGE_NW, ur + 3.1, -1.7)
    box("roof_hatch", cx, cy, Z_DECK, Z_DECK + 0.45, 1.20, 0.90, stone, yaw=yaw)
    for k, du in enumerate((-1.15, 0.30)):
        cx, cy = edge_point(EDGE_FACADE, uc + du, -2.35)
        box(f"roof_vent{k}", cx, cy, Z_DECK, Z_DECK + 0.35, 0.55, 0.55, rust, yaw=yaw)
    # The lighter membrane patch the Bing aerial shows along the north-west half
    # of the deck. A 20 mm inlay, not a raised object: it gives the roof plane a
    # composition without inventing plant that is demonstrably not there.
    cx, cy = edge_point(EDGE_NW, ur + 0.9, -2.3)
    box("roof_patch", cx, cy, Z_DECK, Z_DECK + 0.02, 3.00, 2.20, steel, yaw=yaw)

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.08/2. Applied panels get a token softening on frames only; fills, glow
    # shells and the small entrance parts get none, which is what keeps this
    # under the 6,000-triangle cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if name.endswith(("_fill", "_glow", "_mull0", "_mull1")) or name in {
            "emblem",
            "emblem_glow",
            "recess_spill",
            "transom",
            "recess_back",
            "doors",
            "door_reveal",
            "text_dedicated",
            "roof_patch",
        }:
            continue
        if name.endswith("_frame"):
            bevel(obj, width=0.04, segments=1)
        elif "_globe" in name or "_shaft" in name:
            bevel(obj, width=0.02, segments=1)
        else:
            bevel(obj, width=0.08, segments=2)

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
    print("[build] anchor lon/lat: -122.3934430 37.7813460 (DataSF LiDAR area centroid)")
    print(f"[build] alley facade heading: 225.9 deg true (SW); entrance apex {ENT_APEX:.3f} m")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "95-jack-london-alley.blend")
    glb = os.path.join(out, "95-jack-london-alley.glb")
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
