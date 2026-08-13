"""Deterministic Blender build of the SF-SIM miniature 592 Third Street.

    blender -b --python build_592_third.py -- [--out DIR]

Writes 592-third.blend and 592-third.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint AABB centre (anchor lon -122.3946805,
lat 37.7800910), min Z = 0, parapet crest exactly 8.20 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured DataSF LiDAR footprint (mblr SF3776114), DE-SPIKED: the published
  13-vertex ring's first vertex is a zero-width spike lying on the 3rd Street
  frontage line, which inflates that frontage from its real 21.67 m to 23.90 m.
  The seven intermediate vertices along the NW party wall deviate from the chord
  by at most 0.55 m — under the 0.6 m tolerance the tile bake simplifies at — and
  are dropped as raster-edge noise on a wall nobody can see;
* a 1905 two-storey wood-frame industrial loft holding the WEST corner of 3rd and
  Brannan, filling its lot. Two designed street elevations of nearly equal length
  meeting at a sharp 90 deg east corner, and two blank party walls;
* the identity feature: a continuous near-black shopfront band that turns the
  corner unbroken, under a plain pale stucco upper storey. That value contrast is
  the whole graphic read at city scale;
* it is the LOW corner — 8.20 m against 599 Third's 18.3 m across the street, the
  11.0 m party-wall neighbour and 9.8-13.8 m along Brannan. Getting it lower than
  everything around it is most of the job;
* night state: the shopfront bays lit as one warm band wrapping the corner (a
  cafe and an office on a corner are exactly what is lit at street level), plus
  two faintly lit skylights. The upper floor stays dark. Glow shells are thin and
  proud of the opaque glazing — the app renders _Glow in a separate layer that is
  ~12% alpha by day;
* a genuinely designed roof, because on a near-square 489 m2 plan 8 m up this
  asset is more roof than facade: a parapet ring, five skylights, two hatches and
  a vent cluster in the loose scatter the aerial imagery shows. No penthouse, no
  HVAC plant, no billboard — the aerial shows none, and 599 Third across the
  street already owns the "working roof" role at this intersection.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF building footprint SF3776114, de-spiked, projected with the app's
# tangent projection and recentred on the footprint AABB centre. CCW.
FOOTPRINT = [
    (0.195, 15.815),      # N — 3rd St / NW party wall
    (-15.485, -1.605),    # W — the two party walls meet
    (-0.875, -15.815),    # S — Brannan / SW party wall
    (15.485, 0.455),      # E — 3rd St / Brannan, the hero corner
]

# Edge index -> elevation. Outward normals verified against the survey.
EDGE_NW = 0       # 23.44 m, faces NW 312.0 deg — party wall, the 11 m neighbour
EDGE_SW = 1       # 20.38 m, faces SW 224.2 deg — party wall, 414 Brannan face
EDGE_BRANNAN = 2  # 23.07 m, faces SE 135.2 deg — Brannan Street
EDGE_THIRD = 3    # 21.67 m, faces NE  45.1 deg — 3rd Street

Z_DECK = 7.82        # roof deck / top of the body (LiDAR mode 7.82, median 7.77)
Z_CREST = 8.20       # parapet crest -> the bbox top and the loader's scale
Z_BAND = 3.55        # top of the near-black shopfront field
Z_FAS0, Z_FAS1 = 3.05, 3.60      # the awning fascia band
Z_SILL, Z_HEAD = 4.75, 6.25      # upper-storey punched windows
Z_COND = 4.30                    # centre of the Brannan condenser row

FAS_D = 0.42         # how far the awning fascia stands proud of the wall
BAND_D = 0.04        # the shopfront field is all but flush
PARAPET_T = 0.30     # parapet wall thickness

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_ink": "3a3530",
    "Toy_glass_Glow": "6f95b8",
    "Toy_glassl_Glow": "8fb4d4",
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


def point_inset_ok(px, py, inset):
    """True when (px,py) is at least `inset` inside every footprint edge."""
    for i in range(len(FOOTPRINT)):
        a, _l, _t, n = poly_edge(i)
        if (px - a[0]) * n[0] + (py - a[1]) * n[1] > -inset:
            return False
    return True


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
    """Miniature-style edge softening (style bible s.4). Width is capped at a
    third of the object's thinnest dimension: the applied panels here are only
    40-450 mm thick and a flat 0.12 m bevel collapses opposing profiles into
    zero-area slivers even with clamp_overlap."""
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


def tapered_box(name, cx, cy, z0, z1, sx, sy, inset, mat, yaw=0.0):
    """Box whose top face is `inset` smaller on every side — the skylight cap.
    A real pyramid would put the crest on a spike nobody can see at city scale;
    a shallow frustum reads as glazing from the app's camera."""
    c, s = math.cos(yaw), math.sin(yaw)

    def quad(hx, hy):
        out = []
        for lx, ly in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)):
            out.append((cx + lx * c - ly * s, cy + lx * s + ly * c))
        return out

    lo = quad(sx / 2, sy / 2)
    hi = quad(max(sx / 2 - inset, 0.05), max(sy / 2 - inset, 0.05))
    verts = [(x, y, z0) for x, y in lo] + [(x, y, z1) for x, y in hi]
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
    """Roof coordinates: u runs along the Brannan edge from its SW end, v runs
    INTO the block (against that edge's outward normal)."""
    origin, _l, t, n = poly_edge(EDGE_BRANNAN)
    return (origin[0] + t[0] * u - n[0] * v, origin[1] + t[1] * u - n[1] * v)


def roof_box(name, u, v, z0, z1, su, sv, mat, taper=None):
    cx, cy = roof_uv(u, v)
    _o, _l, t, _n = poly_edge(EDGE_BRANNAN)
    yaw = math.atan2(t[1], t[0])
    if taper is None:
        return box(name, cx, cy, z0, z1, su, sv, mat, yaw=yaw)
    return tapered_box(name, cx, cy, z0, z1, su, sv, taper, mat, yaw=yaw)


def wall_box(name, edge, u, z0, z1, w, depth, mat, d0=0.0):
    """Small box hung on a wall — the Brannan condenser row."""
    a, _l, t, n = poly_edge(edge)
    cx = a[0] + t[0] * u + n[0] * (d0 + depth / 2.0)
    cy = a[1] + t[1] * u + n[1] * (d0 + depth / 2.0)
    return box(name, cx, cy, z0, z1, w, depth, mat, yaw=math.atan2(t[1], t[0]))


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


def shopfront_bay(tag, edge, u, w, glass, ink, roofd, glow):
    """One glazed shopfront bay inside the black band: a dark bulkhead, a glazed
    panel recessed behind the band, and a thin glow shell for the night pass."""
    face_panel(f"{tag}_cill", edge, u, rect_profile(w, 0.0, 0.55), BAND_D, BAND_D + 0.05, roofd)
    face_panel(
        f"{tag}_glass", edge, u, rect_profile(w - 0.30, 0.60, 3.05), BAND_D - 0.14, BAND_D - 0.04, glass
    )
    face_panel(
        f"{tag}_mull", edge, u, rect_profile(0.16, 0.60, 3.05), BAND_D - 0.06, BAND_D + 0.02, ink
    )
    face_panel(
        f"{tag}_glow",
        edge,
        u,
        rect_profile(w - 0.62, 0.76, 2.89),
        BAND_D - 0.06,
        BAND_D + 0.01,
        glow,
    )


def punched_window(tag, edge, u, w, z0, z1, trim, glass):
    """A punched opening with a white surround — the upper storey's only motif.

    The glazing must sit PROUD of its own surround, not recessed behind the wall
    plane: a recessed fill is invisible from every camera the app uses and the
    window reads as a solid white block. Learned the hard way on the first pass
    of this asset (see REPORT.md)."""
    face_panel(f"{tag}_trim", edge, u, rect_profile(w + 0.24, z0 - 0.12, z1 + 0.12), 0.0, 0.05, trim)
    face_panel(f"{tag}_glass", edge, u, rect_profile(w, z0, z1), 0.03, 0.07, glass)
    face_panel(f"{tag}_mull", edge, u, rect_profile(0.10, z0, z1), 0.05, 0.09, trim)


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    stone = material("Toy_stone")
    trim = material("Toy_trim")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    ink = material("Toy_ink")
    gglow = material("Toy_glass_Glow")
    skyglow = material("Toy_glassl_Glow")

    # --- stucco body: its top cap IS the roof deck --------------------------
    prism("body", FOOTPRINT, 0.0, Z_DECK, stone, mat_caps=steel)

    # --- parapet ring -------------------------------------------------------
    # Plain, no coping course: the real parapet is a bare stucco upstand. This
    # ring sets the 8.20 m crest and therefore the loader's scale.
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_CREST, -PARAPET_T, 0.0, stone)

    # --- the wrapped shopfront band: the whole identity of the building ------
    # One near-black field and one awning fascia per street edge, run full
    # length and mitred by overlap at the east corner, so the band reads as
    # continuous around it. That continuity is the recognition cue.
    for edge in (EDGE_BRANNAN, EDGE_THIRD):
        _a, length, _t, _n = poly_edge(edge)
        face_panel(
            f"band{edge}", edge, length / 2.0, rect_profile(length, 0.0, Z_BAND), 0.0, BAND_D, ink
        )
        face_panel(
            f"fascia{edge}",
            edge,
            length / 2.0,
            rect_profile(length, Z_FAS0, Z_FAS1),
            BAND_D,
            BAND_D + FAS_D,
            ink,
        )

    # --- Brannan Street (SE), 23.07 m: garage door + four bays ---------------
    # u runs from the SW party wall toward the east corner.
    # The roll-up door is mid-grey steel, not another black panel: on a black
    # band a dark door is invisible, and a roll-up shutter really is bare metal.
    face_panel(
        "garage", EDGE_BRANNAN, 2.90, rect_profile(3.40, 0.05, 3.30), BAND_D, BAND_D + 0.06, steel
    )
    for i, u in enumerate((7.0, 11.2, 15.4, 19.6)):
        shopfront_bay(f"bbay{i}", EDGE_BRANNAN, u, 3.40, glass, ink, roofd, gglow)
    for i, u in enumerate((4.6, 8.2, 11.8, 15.4, 19.0)):
        punched_window(f"bwin{i}", EDGE_BRANNAN, u, 1.60, Z_SILL, Z_HEAD, trim, glass)
    # The condenser row is small but it is what says "old commercial loft,
    # converted piecemeal" — the one detail that separates this face from a
    # generic stucco box (plan 2.5).
    for i, u in enumerate((6.4, 10.0, 13.6, 17.2)):
        wall_box(
            f"cond{i}", EDGE_BRANNAN, u, Z_COND - 0.28, Z_COND + 0.28, 0.78, 0.46, roofd, d0=0.02
        )

    # --- 3rd Street (NE), 21.67 m: Kinoko, the entry, the cafe, 588 ---------
    # u runs from the east corner toward the NW party wall, so the Kinoko bays
    # (592, nearest the corner) come first — the order the street reads in.
    for i, u in enumerate((2.4, 6.2, 10.0)):
        shopfront_bay(f"tbay{i}", EDGE_THIRD, u, 3.20, glass, ink, roofd, gglow)
    # The entry is a recess in reality; at this scale a recess is a black hole in
    # a black band, so it is modelled as a lit surround with a glazed door — the
    # same information, legible from the app's camera.
    face_panel(
        "entry_trim", EDGE_THIRD, 12.40, rect_profile(1.70, 0.0, 2.95), BAND_D, BAND_D + 0.05, trim
    )
    face_panel(
        "entry_door", EDGE_THIRD, 12.40, rect_profile(1.20, 0.05, 2.70), BAND_D + 0.03, BAND_D + 0.07, glass
    )
    shopfront_bay("tcafe", EDGE_THIRD, 15.60, 3.60, glass, ink, roofd, gglow)
    shopfront_bay("t588", EDGE_THIRD, 19.40, 2.80, glass, ink, roofd, gglow)
    for i, u in enumerate((2.8, 6.0, 9.2, 14.8, 18.2)):
        punched_window(f"twin{i}", EDGE_THIRD, u, 1.60, Z_SILL, Z_HEAD, trim, glass)

    # --- party walls (NW, SW): blank. Both are built hard against taller -----
    # neighbours; inventing openings on them would be a straightforward lie.

    # --- roof: the building's largest visible surface ------------------------
    # Eight skylights, not five: the aerial shows roughly a dozen roof objects on
    # this plan and five left a 489 m2 tray reading empty from the app's camera.
    skylights = (
        (5.5, 5.0), (10.5, 4.0), (15.5, 6.5), (8.0, 11.5),
        (13.5, 13.5), (18.6, 3.6), (6.6, 15.4), (16.4, 9.6),
    )
    for i, (u, v) in enumerate(skylights):
        roof_box(f"sky_kerb{i}", u, v, Z_DECK, Z_DECK + 0.20, 1.70, 1.70, stone)
        roof_box(f"sky{i}", u, v, Z_DECK + 0.16, Z_DECK + 0.33, 1.50, 1.50, glassl, taper=0.28)
        # Only a thin shell glows — never the primary surface. The app draws
        # _Glow in a separate layer at ~12% alpha by day, so a cap authored as
        # glow simply vanishes in daylight and the kerb reads as an empty tray.
        if i in (1, 2):
            roof_box(
                f"sky{i}_glow", u, v, Z_DECK + 0.30, Z_DECK + 0.36, 1.10, 1.10, skyglow, taper=0.20
            )
    for i, (u, v) in enumerate(((4.0, 9.0), (17.5, 10.5))):
        roof_box(f"hatch{i}", u, v, Z_DECK, Z_DECK + 0.35, 1.10, 0.90, stone)
    for i, (u, v) in enumerate(((10.5, 16.5), (7.6, 8.2))):
        roof_box(f"vent{i}", u, v, Z_DECK, Z_DECK + 0.30, 0.50, 0.50, roofd)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.12/2. Applied panels are thin — trims and bands get a token
    # 1-segment softening and the fills/glow shells none at all.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if name.endswith(("_glass", "_glow", "_mull", "_door")) or "_glow" in name:
            continue
        if name.endswith(("_trim", "_cill")) or name.startswith(("band", "fascia", "entry", "sky")):
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
    print("[build] anchor lon/lat: -122.3946805 37.7800910 (footprint AABB centre)")
    print("[build] 3rd Street front heading: 45.1 deg true (NE)")
    print("[build] Brannan Street front heading: 135.2 deg true (SE)")
    # Roof furniture must sit clear of the parapet on a footprint that narrows
    # fast toward its corners — check rather than trust the hand-placed u,v.
    for u, v in ((5.5, 5.0), (10.5, 4.0), (15.5, 6.5), (8.0, 11.5), (13.5, 13.5),
                 (18.6, 3.6), (6.6, 15.4), (16.4, 9.6),
                 (4.0, 9.0), (17.5, 10.5), (10.5, 16.5), (7.6, 8.2)):
        px, py = roof_uv(u, v)
        if not point_inset_ok(px, py, 1.6):
            print(f"[build] WARN roof object at u={u} v={v} is within 1.6 m of a parapet")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "592-third.blend")
    glb = os.path.join(out, "592-third.glb")
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
