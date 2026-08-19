"""Deterministic Blender build of the SF-SIM miniature 434 Brannan Street.

    blender -b --python build_434_brannan.py -- [--out DIR]

Writes 434-brannan.blend and 434-brannan.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint axis-aligned bbox centre (anchor
lon -122.3954103, lat 37.7796003), min Z = 0, rooftop penthouse crest exactly
13.79 m.

Design (see REFERENCE.md and docs/asset-plans/434-brannan.md for the sources
behind every number):

* the measured DataSF LiDAR footprint (mblr SF3776151), reduced to its four real
  corners — a clean 22.70 x 33.85 m parallelogram at the 45 deg SoMa heading,
  763.6 m2 against the survey ring's 764.8;
* a 1929 ART DECO REINFORCED-CONCRETE LOFT (SF Planning DPR 523A, Page &
  Turnbull, Eastern Neighborhoods SoMa Survey). Three storeys; the LiDAR deck at
  11.46 m is the best-pinned number in the dossier (mode 11.43, median 11.46,
  sd 0.92 over 3,086 cells) and everything above it is inferred;
* the identity feature, and the only thing on this block face that has one:
  SIX FLUTED PILASTERS dividing the Brannan front into FIVE BAYS, each pilaster
  stepping up through the parapet into a plain projecting CAP, so the roofline
  reads as a row of teeth from the app's downward camera. Under the caps, five
  SALMON DECO FRIEZE panels — the one saturated accent on an otherwise neutral
  building;
* the second identity feature: CONCRETE FRONT, CORRUGATED-METAL BACK. The rear
  (NW) elevation is blue-grey ribbed metal over its own car park and the rear
  8.05 m of the Zoe flank is terracotta ribbed metal. A modeller who clads it in
  concrete all round loses the building's whole logic;
* two finished street elevations (Brannan SE 5 bays, Zoe SW 6 bays), one visible
  rear, and one blind party flank (NE, against 426 Brannan at 5.75 m for the
  21.9 m nearest Brannan — this building stands 5.7 m proud of it there and the
  rear 11.8 m is fully open, so the flank is modelled as a finished quiet plane
  with floor-line score marks and no invented windows);
* night state: the five frieze panels as an uplit crown (hero glow), the recessed
  main entry, and a restrained scatter of lit sash. Glow surfaces are thin shells
  proud of the opaque geometry — the app renders _Glow in a separate layer that
  is ~12% alpha PER LAYER by day, so never author a primary surface as glow and
  never wrap one in a closed shell;
* a designed roof: the parapet ring, the six caps, the mechanical penthouse that
  sets the 13.79 m crest (~6.6 m in from the NE parapet, two thirds of the way
  back — measured off nadir imagery against the footprint ring), the duct run
  along the NE side, a skylight, a hatch, three small units and the antenna
  ballast pad. The roof deck is Toy_steel, NOT Toy_roofd: 45454a measures
  rgb(9,9,12) on a deck in the running app and reads as a black hole.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF building footprint SF3776151 projected with the app's tangent
# projection and recentred on the axis-aligned bbox centre (which is what the
# loader's base-centre origin convention needs). Listed CCW, so the outward
# normal of edge i is (t.y, -t.x) — derived from the winding, never from the
# centroid, because a centroid-derived "outward" folds on non-convex corners.
FOOTPRINT = [
    (-19.816, 4.182),    # W corner — rear x Zoe
    (3.812, -20.052),    # S corner — Brannan x Zoe
    (19.816, -3.952),    # E corner — Brannan x 426 party wall
    (-3.837, 20.052),    # N corner — rear x 426 party wall
]

EDGE_ZOE = 0     # 33.85 m, faces SW 224.8 deg — Zoe Street flank
EDGE_FRONT = 1   # 22.70 m, faces SE 134.8 deg — Brannan Street, the dressed face
EDGE_NE = 2      # 33.70 m, faces NE  44.8 deg — party flank, blind
EDGE_REAR = 3    # 22.52 m, faces NW 314.8 deg — corrugated rear over the car park

TAG = {EDGE_ZOE: "z", EDGE_FRONT: "f", EDGE_NE: "ne", EDGE_REAR: "r"}

Z_DECK = 11.46     # roof deck / top of the body — DataSF LiDAR median, MEASURED
Z_FRIEZE0 = 11.05  # bottom of the Deco frieze band on Brannan
Z_PARAPET = 12.22  # top of the parapet wall / bottom of the coping (inferred)
Z_COPING = 12.40   # parapet crest (inferred: deck + 0.94)
Z_CAP0 = 12.05     # bottom of the pilaster caps
Z_CAP = 13.05      # pilaster cap top (inferred; 0.65 m clear of the coping so
                   # the roofline is serrated from the app's downward camera)
Z_CREST = 13.79    # penthouse AHU top = LiDAR max 13.79 -> the bbox top

# Floor-to-floor 4.20 / 3.63 / 3.63 sums to the measured 11.46 m deck.
Z_W = ((1.35, 3.60), (5.10, 7.35), (8.73, 10.90))
Z_FLOORLINE = (4.20, 7.83)  # scored reveals on the blind NE flank

Z_PLINTH = 0.55    # light plinth on Brannan
Z_DADO = 1.15      # painted mid-grey dado on the Zoe concrete portion; kept
                   # BELOW the 1.35 m ground-floor sills so the band reads as a
                   # base course instead of slicing the windows in half

SKIN = 0.10        # applied-panel standoff from the wall plane
PARAPET_T = 0.35   # parapet wall thickness
CLAD = 0.06        # corrugated cladding standoff
PIL_D = 0.26       # pilaster projection

# Brannan: 6 pilasters of 1.15 m and 5 openings of 3.16 m across 22.70 m.
PIL_W = 1.15
BAY_W = 3.16
PIL_U = [PIL_W / 2 + i * (PIL_W + BAY_W) for i in range(6)]
BAY_U = [PIL_W + BAY_W / 2 + i * (PIL_W + BAY_W) for i in range(5)]
WIN_F = 2.85

# Zoe: the rear 8.05 m is corrugated; the remaining 25.80 m carries 6 bays of
# 3.65 m between 0.55 m piers. u runs from the REAR corner toward Brannan.
Z_CLAD_U = 8.05
ZOE_PIER = 0.55
ZOE_BAY = 3.65
ZOE_U = [Z_CLAD_U + ZOE_PIER + ZOE_BAY / 2 + i * (ZOE_PIER + ZOE_BAY) for i in range(6)]
WIN_Z = 3.30

# Rear: six punched openings in two columns of three.
REAR_U = [5.20, 11.26, 17.32]
REAR_W, REAR_H = 1.30, 1.50

# Restrained night scatter: ten lit sash across three floors and three faces.
LIT_F = {0: set(), 1: {1, 3}, 2: {0, 4}}
LIT_Z = {0: {4}, 1: {1, 5}, 2: {2}}
LIT_R = {(1, 1), (2, 2)}

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",   # the concrete body, pilasters, parapet, penthouse
    "Toy_trim": "f3efe6",    # plinth, coping, pilaster caps, frames, frieze motif
    "Toy_coral": "e8735a",   # the five Deco frieze panels — the one saturated accent
    "Toy_glass": "2a4d73",   # all sash glazing and the skylight
    "Toy_ink": "3a3530",     # entry reveal, scored floor-line reveals
    "Toy_steel": "9aa0a6",   # roof deck, rear cladding, Zoe dado, duct, small units
    "Toy_rust": "a86444",    # the terracotta corrugated section on the Zoe flank
    "Toy_roofd": "45454a",   # the rooftop air-handling unit and the hatch ONLY
    # Glow colours are the LIT appearance, not a lighting effect: the app draws
    # _Glow as an unlit overlay at the material's own baked colour, so the base
    # colour IS the night look. The frieze glows in its own coral so the day
    # tint of the 12% shell over the identical opaque panel is invisible.
    "Toy_coral_Glow": "e8735a",
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


def offset_polygon(poly, d):
    return offset_polygon_per_edge(poly, [d] * len(poly))


def rect_profile(w, z0, z1):
    a = w / 2.0
    return [(-a, z0), (a, z0), (a, z1), (-a, z1)]


def ziggurat_profile(w, z0, z1, steps=3):
    """A symmetric stepped pyramid — the miniature's read of the frieze's
    stylised Deco palmette. A simple CCW (u, z) outline, so it goes straight
    into face_panel with no booleans: bottom edge, up the stepped right side,
    across the plateau, down the stepped left side."""
    a = w / 2.0
    dz = (z1 - z0) / steps
    xs = [a * (1.0 - k / float(steps)) for k in range(steps + 1)]
    xs[-1] = a * 0.14  # a small plateau, not a point: a point duplicates a vertex
    right = []
    for k in range(steps):
        right.append((xs[k], z0 + (k + 1) * dz))
        right.append((xs[k + 1], z0 + (k + 1) * dz))
    left = [(-x, z) for x, z in reversed(right)]
    return [(-a, z0), (a, z0)] + right + left


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
    """Miniature edge softening (style bible s.4), clamped to a third of the
    object's thinnest dimension so applied panels do not collapse into zero-area
    slivers whose averaged vertex normals fail the contract validator."""
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
    extruded outward from offset d0 to d1 along that wall's outward normal."""
    a, _length, t, n = poly_edge(edge, poly)
    verts = []
    for d in (d0, d1):
        for du, z in profile:
            verts.append(
                (
                    a[0] + t[0] * (u_centre + du) + n[0] * d,
                    a[1] + t[1] * (u_centre + du) + n[1] * d,
                    z,
                )
            )
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


def roof_uv(u, v):
    """Roof-grid coordinates: u runs along the Brannan edge from its south
    (Zoe) corner toward the northeast party corner, v runs INTO the block. The
    footprint is 22.70 (u) x 33.85 (v) in this frame."""
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
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    # Workbench's MATERIAL colour mode reads diffuse_color, not the BSDF, and
    # Workbench is the engine this rig falls back to under machine contention.
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# --------------------------------------------------------------------- parts


def rect_opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None, poly=None):
    """Frame panel + a smaller fill that protrudes further, so the frame reads
    as a border ring around a recessed opening. No booleans, all closed solids."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, SKIN - 0.02,
               frame_mat, poly)
    inset = 0.16
    face_panel(f"{tag}_fill", edge, u,
               rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
               0.0, SKIN + 0.04, fill_mat, poly)
    if glow_mat is not None:
        g = 0.30
        face_panel(f"{tag}_glow", edge, u,
                   rect_profile(w - 2 * g, z0 + g, z1 - g),
                   SKIN + 0.02, SKIN + 0.08, glow_mat, poly)


def ribbed_cladding(tag, edge, u0, u1, z0, z1, mat, ribs):
    """A corrugated-metal panel: one flat plate plus a few proud strips. Never
    rib by rib — at the app's camera four grooves and forty read identically,
    and forty cost 480 triangles."""
    w = u1 - u0
    face_panel(f"clad_{tag}", edge, (u0 + u1) / 2.0, rect_profile(w, z0, z1),
               0.0, CLAD, mat)
    for i in range(ribs):
        u = u0 + w * (i + 0.5) / ribs
        face_panel(f"clad_{tag}_rib{i}", edge, u, rect_profile(0.22, z0 + 0.05, z1 - 0.05),
                   CLAD, CLAD + 0.05, mat)


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials, bpy.data.curves):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    stone = material("Toy_stone")
    trim = material("Toy_trim")
    coral = material("Toy_coral")
    glass = material("Toy_glass")
    ink = material("Toy_ink")
    steel = material("Toy_steel")
    rust = material("Toy_rust")
    roofd = material("Toy_roofd")
    cglow = material("Toy_coral_Glow")
    gglow = material("Toy_glass_Glow")
    tglow = material("Toy_trim_Glow")

    len_front = poly_edge(EDGE_FRONT)[1]
    len_zoe = poly_edge(EDGE_ZOE)[1]
    len_ne = poly_edge(EDGE_NE)[1]
    len_rear = poly_edge(EDGE_REAR)[1]

    # --- masses -------------------------------------------------------------
    # One volume. The roof deck cap is Toy_steel, not Toy_roofd: 45454a measures
    # rgb(9,9,12) on a deck in the running app.
    prism("body", FOOTPRINT, 0.0, Z_DECK, stone, mat_caps=steel)

    # --- parapet ring + light coping ---------------------------------------
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET, -PARAPET_T, 0.0, stone)
    # The coping is concrete like the wall; the CAPS are the lighter trim, so
    # the teeth read against the parapet instead of merging into one white rim.
    ring_band("coping", FOOTPRINT, Z_PARAPET, Z_COPING, -PARAPET_T - 0.07, 0.07, stone)

    # --- corrugated metal: the rear elevation and the rear end of Zoe -------
    ribbed_cladding("rear", EDGE_REAR, 0.10, len_rear - 0.10, 0.0, Z_PARAPET, steel, 5)
    ribbed_cladding("zoe", EDGE_ZOE, 0.10, Z_CLAD_U, 0.0, Z_PARAPET, rust, 4)

    # --- Brannan: plinth, six pilasters, five frieze bays, six caps ---------
    face_panel("plinth_f", EDGE_FRONT, len_front / 2.0,
               rect_profile(len_front, 0.0, Z_PLINTH), 0.0, 0.08, trim)

    for i, u in enumerate(PIL_U):
        face_panel(f"pilaster{i}", EDGE_FRONT, u,
                   rect_profile(PIL_W, Z_PLINTH, Z_CAP0), 0.0, PIL_D, stone)
        # three shallow flutes, read as lines not as solids -> no bevel, 12 tris
        for k, du in enumerate((-0.32, 0.0, 0.32)):
            face_panel(f"flute{i}{k}", EDGE_FRONT, u + du,
                       rect_profile(0.12, Z_PLINTH + 0.20, Z_CAP0 - 0.10),
                       PIL_D, PIL_D + 0.04, stone)
        # THE TEETH: caps projecting past the pilaster and past the coping, so
        # the roofline is serrated from the app's downward camera. Deliberately
        # thicker and deeper than life — the plan's one spent exaggeration.
        face_panel(f"cap{i}", EDGE_FRONT, u,
                   rect_profile(PIL_W + 0.44, Z_CAP0, Z_CAP), -0.10, PIL_D + 0.26, trim)

    for i, u in enumerate(BAY_U):
        # Pale ground, SALMON ornament — that is the way round the real frieze
        # is, and it keeps the accent to the motif instead of flooding the bay.
        face_panel(f"frieze{i}", EDGE_FRONT, u,
                   rect_profile(BAY_W, Z_FRIEZE0, Z_PARAPET), 0.0, CLAD, trim)
        face_panel(f"friezefan{i}", EDGE_FRONT, u,
                   ziggurat_profile(2.60, Z_FRIEZE0 + 0.16, Z_PARAPET - 0.16),
                   CLAD, CLAD + 0.05, coral)
        # hero night glow: the crown, uplit. Thin single shell, the same coral
        # as the ornament under it, so the 12% day layer is invisible.
        face_panel(f"friezeglow{i}", EDGE_FRONT, u,
                   ziggurat_profile(2.32, Z_FRIEZE0 + 0.26, Z_PARAPET - 0.26),
                   CLAD + 0.05, CLAD + 0.09, cglow)

    # --- Brannan bays: sash on all three floors, entry in the NE-most bay ---
    for f, (z0, z1) in enumerate(Z_W):
        for i, u in enumerate(BAY_U):
            if f == 0 and i == len(BAY_U) - 1:
                continue  # replaced by the main entry
            rect_opening(f"fw{f}{i}", EDGE_FRONT, u, WIN_F, z0, z1, trim, glass,
                         gglow if i in LIT_F[f] else None)
            face_panel(f"fm{f}{i}", EDGE_FRONT, u,
                       rect_profile(WIN_F - 0.34, (z0 + z1) / 2 - 0.05,
                                    (z0 + z1) / 2 + 0.05),
                       SKIN + 0.02, SKIN + 0.07, trim)

    # The recessed main entry, northeast-most bay: a dark reveal with a glazed
    # leaf, a big flat disc on its back wall (the circular graphic that is on the
    # real one), and a warm glow shell for the night pass.
    # Built as APPLIED panels stacking outward, not as a recess. There are no
    # booleans in this script, so a "recessed" reveal modelled as a solid prism
    # sunk into the wall simply swallows the door and the glow shell inside
    # itself — which is exactly what the first night render showed: a dead black
    # rectangle where the lit entrance should be. A dark panel with the leaf,
    # the disc and the glow stacked proud of it reads as a deep portal from the
    # app's camera and actually lights at night.
    u_entry = BAY_U[-1]
    face_panel("entry_reveal", EDGE_FRONT, u_entry,
               rect_profile(3.00, 0.0, 4.00), 0.0, 0.05, ink)
    disc = [
        (0.80 * math.cos(2 * math.pi * k / 14), 3.25 + 0.80 * math.sin(2 * math.pi * k / 14))
        for k in range(14)
    ]
    face_panel("entry_disc", EDGE_FRONT, u_entry, disc, 0.05, 0.09, stone)
    face_panel("entry_door", EDGE_FRONT, u_entry,
               rect_profile(2.20, 0.0, 2.90), 0.05, 0.11, glass)
    face_panel("entry_glow", EDGE_FRONT, u_entry,
               rect_profile(2.40, 0.25, 2.70), 0.11, 0.16, tglow)

    # --- Zoe Street flank: dado + 6 bays of sash on three floors ------------
    face_panel("dado_z", EDGE_ZOE, (Z_CLAD_U + len_zoe) / 2.0,
               rect_profile(len_zoe - Z_CLAD_U, 0.0, Z_DADO), 0.0, 0.05, steel)
    for f, (z0, z1) in enumerate(Z_W):
        for i, u in enumerate(ZOE_U):
            rect_opening(f"zw{f}{i}", EDGE_ZOE, u, WIN_Z, z0, z1, trim, glass,
                         gglow if i in LIT_Z[f] else None)
            # the same single horizontal division the Brannan sash gets: the
            # real windows are two-light industrial sash on every elevation
            face_panel(f"zm{f}{i}", EDGE_ZOE, u,
                       rect_profile(WIN_Z - 0.34, (z0 + z1) / 2 - 0.05,
                                    (z0 + z1) / 2 + 0.05),
                       SKIN + 0.02, SKIN + 0.07, trim)

    # --- rear openings ------------------------------------------------------
    for f, (z0, z1) in enumerate(Z_W):
        zc = (z0 + z1) / 2.0
        for i, u in enumerate(REAR_U):
            rect_opening(f"rw{f}{i}", EDGE_REAR, u, REAR_W,
                         zc - REAR_H / 2, zc + REAR_H / 2, trim, glass,
                         gglow if (f, i) in LIT_R else None)

    # --- northeast party flank: finished, quiet, no invented windows --------
    for z in Z_FLOORLINE:
        face_panel(f"reveal_ne_{z:.0f}", EDGE_NE, len_ne / 2.0,
                   rect_profile(len_ne - 0.30, z, z + 0.10), -0.05, 0.02, ink)

    # --- roof: the surface the app's camera sees most -----------------------
    # Penthouse at u 16.4, v 25.9 — 6.3 m in from the NE parapet and two thirds
    # of the way back, which is where the nadir imagery puts it.
    roof_box("penthouse", 16.40, 25.90, Z_DECK, Z_DECK + 0.45, 5.20, 4.00, stone)
    roof_box("penthouse_ahu", 16.40, 25.90, Z_DECK + 0.45, Z_CREST, 3.40, 2.40, roofd)

    # the duct run heading southeast toward Brannan, 4.5 m inside the NE parapet
    roof_box("duct", 18.20, 20.00, Z_DECK, Z_DECK + 0.50, 0.75, 9.00, steel)
    roof_box("duct_riser", 17.20, 24.40, Z_DECK, Z_DECK + 0.80, 0.50, 0.50, steel)

    # skylight, hatch and the small cluster near the Brannan end
    roof_box("skylight_kerb", 18.60, 11.20, Z_DECK, Z_DECK + 0.25, 2.40, 2.40, trim)
    roof_box("skylight", 18.60, 11.20, Z_DECK + 0.20, Z_DECK + 0.48, 2.05, 2.05, glass)
    roof_box("roof_hatch", 14.00, 10.10, Z_DECK, Z_DECK + 0.50, 1.30, 1.00, roofd)
    # Toy_stone, not Toy_steel: small units the same colour as the deck vanish
    # from the nadir view, which is the view this roof exists for.
    roof_box("vent_a", 11.60, 8.20, Z_DECK, Z_DECK + 0.80, 1.60, 1.20, stone)
    roof_box("vent_b", 9.20, 9.60, Z_DECK, Z_DECK + 0.60, 1.20, 1.00, stone)
    roof_box("vent_c", 13.10, 6.40, Z_DECK, Z_DECK + 1.00, 0.90, 0.90, stone)

    # the antenna guy-wire ballast pad — the wire itself is not modellable here
    roof_box("ballast_pad", 2.34, 17.57, Z_DECK, Z_DECK + 0.25, 1.40, 1.40, stone)

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.12/2. Frames, caps and roof props get a token 1-segment softening.
    # Hairline strips (flutes, mullions, reveals, ribs) read as lines, not as
    # solids: a bevel costs ~96 triangles apiece and buys nothing at city scale.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if name.endswith(("_fill", "_glow")) or name.startswith(("friezefan", "entry_disc")):
            continue
        if name.startswith(("flute", "fm", "zm", "reveal_")) or "_rib" in name:
            continue
        if name.endswith("_frame") or name.startswith(
            ("cap", "vent_", "roof_hatch", "skylight", "duct_riser", "ballast_pad",
             "penthouse_ahu", "entry_", "frieze", "plinth_", "dado_", "clad_")
        ):
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
    print("[build] anchor lon/lat: -122.3954103 37.7796003 (footprint bbox centre)")
    print("[build] Brannan front heading: 134.8 deg true (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "434-brannan.blend")
    glb = os.path.join(out, "434-brannan.glb")
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
