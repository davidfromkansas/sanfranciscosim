"""Deterministic Blender build of the SF-SIM miniature 27 South Park.

    blender -b --python build_27_south_park.py -- [--out DIR]

Writes 27-south-park.blend and 27-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading - the
loader applies no rotation. Origin = footprint centroid (anchor
lon -122.3931439, lat 37.7817369), min Z = 0, parapet coping crest exactly
10.20 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured OSM footprint (way/112759868), a 12.19 x 33.55 m parallelogram at
  ~45 deg off the world axes, built as ONE mass. This is the CENTRE third of the
  1919 warehouse at 21-29 South Park Street; DataSF traces all three sections as
  a single 1,115 m2 polygon and only OSM splits them, so the OSM ring is the
  geometry and the anchor;
* one public elevation. The building is a party-wall stick: 21 South Park hard
  against the north-east flank, 29 South Park hard against the south-west, a
  service gap at the rear. Everything the city sees is 12.19 m wide;
* the identity, carried hard: SIX SEGMENTAL-ARCHED second-floor windows in dark
  blue-green metal on narrow painted-brick piers. The 2009 DPR form describes
  the district's warehouses as having "jack-arch window and door openings" -
  this is the arcaded one, and it is the only reason the building is worth an
  asset. The arch rise is 0.65 m on a 1.55 m opening, close to the photograph,
  and each head carries a proud Toy_stone archivolt so the arcade separates from
  its own glazing at the app's camera;
* a very tall ground floor - 4.55 m of it, nearly half the facade - in three
  bays, each stacked the same way: transom strip over a recessed panel band over
  a big opening. Bay 1 (north-east) a pair of flush doors, bay 2 the shopfront
  window, bay 3 the MAHOGANY DOUBLE DOOR at the address numeral. That door is
  the single warm accent in a run of dark blue-green joinery and it is what says
  27 rather than 21-29;
* painted brick, not exposed brick. This row is painted a warm off-white and its
  neighbours are not; from the app's downward camera the pale wall IS the
  building. Toy_sand body, Toy_stone bands;
* BOTH party walls finished. The re-bake removes the procedural mass of 21 and
  29 along with this building's own - they share one polygon in the bake input -
  so until those get GLBs both flanks are exposed to the camera. Plain painted
  brick, no openings, parapet carried across;
* night state: the ground-floor bays are the hero glow - Toy_gold_Glow rather
  than the plan's Toy_trim_Glow, which previewed as a blown white slab; warm,
  the office lobby,
  the one genuinely bright thing on this facade after dark - plus two of the six
  arches cool and much smaller in area. Nothing on the flanks, the rear or the
  roof. Glow surfaces are thin plates proud of the opaque glazing (the app
  renders _Glow in a separate layer that reads through by day - never author a
  primary surface as glow);
* a roof the 2026 nadir aerial shows in detail: dark membrane inside a
  continuous painted parapet ring, plant spread through the middle third toward
  the FRONT and the rear third all but bare, two low glazed monitors among it.
  No penthouse, no bulkhead, no roof deck - none exist. Every unit is kept under
  the coping so the crest stays architectural (plan s.2.10, s.2.15). The
  membrane is Toy_roofd rather than the observed light grey: from the app's
  downward camera a pale roof inside pale parapets inside pale walls was one
  flat shape, and the value break is what makes the parapet ring read.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# The lot's own frame. to_world maps (u, v) -> (east, north) by a proper
# rotation, and in that mapping +v sits 90 deg CCW of +u. The building runs
# NW-SE with its front on the NORTH-WEST, so +v must point SE (into the lot,
# away from South Park Street) and +u therefore points SW (toward 29 South
# Park). ROT_DEG = 225.2 gives exactly that, from the measured edge bearings:
# front outward normal 314.79 deg, long axis 134.79/314.79 deg.
ROT_DEG = 225.2

HALF_W = 6.095    # half the 12.19 m frontage
HALF_D = 16.775   # half the 33.55 m depth

# Footprint in (u, v) metres, centred on the anchor. CCW and convex. The OSM
# ring is a parallelogram to within 0.07 m of this rectangle, which is below the
# bake's own 0.6 m simplify tolerance and far below anything the camera sees.
FOOT_UV = [
    (-HALF_W, HALF_D),    # rear, north-east side
    (-HALF_W, -HALF_D),   # front, north-east side
    (HALF_W, -HALF_D),    # front, south-west side
    (HALF_W, HALF_D),     # rear, south-west side
]

# Edge index -> elevation. Outward normals verified against the survey.
E_NE = 0      # 33.55 m party wall, faces NE - 21 South Park, 0.00 m gap. BLANK
E_FRONT = 1   # 12.19 m, faces NW 314.8 deg - South Park. The only public face
E_SW = 2      # 33.55 m party wall, faces SW - 29 South Park, 0.00 m gap. BLANK
E_REAR = 3    # 12.19 m, faces SE - the Brannan service gap. Not observed

FRONT_W = 12.19
DEPTH = 33.55

Z_BASE = 0.35          # painted base band top
Z_OPEN_TOP = 3.30      # ground-floor opening head
Z_PANEL_A, Z_PANEL_B = 3.30, 3.70    # beaded panel band (read as one recess)
Z_TRAN_A, Z_TRAN_B = 3.70, 4.35      # transom strip
Z_SHOP_TOP = 4.55      # top of the joinery
Z_CORN_A, Z_CORN_B = 4.55, 4.85      # ground-floor cornice band
Z_WIN_A = 5.35         # arched window sill
Z_WIN_TRAN = 7.60      # transom bar in the arched windows
Z_SPRING = 7.90        # arch springing line
Z_ARCH_TOP = 8.55      # arch crown (rise 0.65 m)
Z_DECK = 9.60          # roof deck - DataSF LiDAR median over the parcel
Z_PARA = 10.05         # parapet, below its coping
Z_CREST = 10.20        # coping crest -> the bbox top, must land exactly

SKIN = 0.10            # applied panels stand proud of the wall by this much

# Three ground-floor bays on 4.063 m centres, six arches on 2.032 m centres.
# Both rhythms are derived from the measured 12.19 m frontage (plan s.2.15):
# the arch count is what the Jan 2025 photograph shows across this width.
BAY_N = 3
ARCH_N = 6
BAY_W = 3.30
ARCH_W = 1.55
ARCH_SEGS = 6

PALETTE_HEX = {
    "Toy_sand": "ece4d4",
    "Toy_stone": "d9d2c2",
    "Toy_navy": "2c4a70",
    "Toy_glass": "2a4d73",
    "Toy_rust": "a86444",
    "Toy_steel": "9aa0a6",
    "Toy_ink": "3a3530",
    "Toy_trim": "f3efe6",
    "Toy_roofd": "45454a",
    "Toy_glass_Glow": "6f95b8",
    "Toy_gold_Glow": "caa64a",
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


FOOT = [to_world(u, v) for u, v in FOOT_UV]

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


def arch_profile(w, z0, z_spring, rise, segs=ARCH_SEGS):
    """(du, z) outline of a segmental-arched opening: square jambs to the
    springing line, then a circular arc of `rise` over the chord `w`.

    Six segments, not twelve. The arc is the identity of this building and has
    to survive at thumbnail size, but each extra segment costs four triangles
    across six openings plus their frames; at the app's camera a 6-segment
    segmental arch and a 16-segment one are the same picture."""
    a = w / 2.0
    radius = (a * a + rise * rise) / (2.0 * rise)
    cz = z_spring + rise - radius            # arc centre, below the springing
    half = math.asin(a / radius)             # half the subtended angle
    # The arc's own endpoints ARE the springing points, so they are not emitted
    # separately: duplicating them put two zero-area triangles in every cap of
    # every arch element and the validator caught all 96 of them.
    pts = [(-a, z0), (a, z0)]
    for i in range(segs + 1):
        ang = half - 2.0 * half * i / segs   # +half (right jamb) -> -half
        pts.append((radius * math.sin(ang), cz + radius * math.cos(ang)))
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
    """Miniature-style edge softening (style bible s.4). The width is capped at
    a third of the object's thinnest dimension: the applied panels here are
    60-440 mm thick and a flat 0.12 m bevel on those collapses opposing profiles
    into zero-area slivers even with clamp_overlap."""
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
    yaw = math.atan2(_S, _C)
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


def lot_cyl(name, u, v, z0, z1, radius, mat, segs=10):
    """Low-segment cylinder on the lot grid - rooftop fans and condensers."""
    cx, cy = to_world(u, v)
    ring = []
    for i in range(segs):
        a = 2.0 * math.pi * i / segs
        ring.append((cx + radius * math.cos(a), cy + radius * math.sin(a)))
    return prism(name, ring, z0, z1, mat)


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


def arched_window(tag, u, navy, glass, glow_mat=None, stone=None, ink=None):
    """One of the six segmental-arched second-floor lights: a painted-brick
    archivolt, a dark frame following the arch, a Toy_glass fill inside it, and
    one transom bar. No muntin grid - at the app's camera the ARCH is the cue
    and a grid inside the head would cost five times as much for the same
    picture (plan s.2.6).

    The Toy_stone archivolt is the one addition the first aerial forced. Frame
    and glazing are both very dark in reality, so navy-on-Toy_glass collapsed
    into one flat silhouette and the arcade read as six holes rather than six
    arches. A 0.12 m light band around each head separates them and is what the
    proud brick arch does on the building anyway."""
    rise = Z_ARCH_TOP - Z_SPRING
    if stone is not None:
        face_panel(
            f"{tag}_archivolt",
            FOOT,
            E_FRONT,
            u,
            arch_profile(ARCH_W + 0.24, Z_WIN_A - 0.12, Z_SPRING, rise + 0.12),
            0.0,
            SKIN + 0.02,
            stone,
        )
    face_panel(
        f"{tag}_frame",
        FOOT,
        E_FRONT,
        u,
        arch_profile(ARCH_W, Z_WIN_A, Z_SPRING, rise),
        0.0,
        SKIN + 0.08,
        ink if ink is not None else navy,
    )
    inset = 0.14
    face_panel(
        f"{tag}_fill",
        FOOT,
        E_FRONT,
        u,
        arch_profile(ARCH_W - 2 * inset, Z_WIN_A + inset, Z_SPRING, rise - inset),
        0.0,
        SKIN + 0.15,
        glass,
    )
    face_panel(
        f"{tag}_bar",
        FOOT,
        E_FRONT,
        u,
        rect_profile(ARCH_W - 2 * inset, Z_WIN_TRAN - 0.05, Z_WIN_TRAN + 0.05),
        0.0,
        SKIN + 0.19,
        ink if ink is not None else navy,
    )
    if glow_mat is not None:
        g = 0.38
        face_panel(
            f"{tag}_glow",
            FOOT,
            E_FRONT,
            u,
            rect_profile(ARCH_W - 2 * g, Z_WIN_A + g, Z_WIN_TRAN - 0.20),
            SKIN + 0.12,
            SKIN + 0.17,
            glow_mat,
        )


def ground_bay(tag, u, navy, glass, fill_mat, glow_mat=None, mullion=False):
    """One of the three ground-floor bays. Every bay is stacked the same way -
    transom strip / recessed panel band / big opening - and only the opening's
    material and mullion change. That repetition is what the photograph shows
    and it is what keeps the ground floor legible at 12 m of frontage."""
    # the reveal: one recess the full height of the bay
    face_panel(
        f"{tag}_reveal", FOOT, E_FRONT, u, rect_profile(BAY_W, Z_BASE, Z_TRAN_B + 0.10), 0.0, SKIN, navy
    )
    # the opening
    face_panel(
        f"{tag}_open", FOOT, E_FRONT, u, rect_profile(BAY_W - 0.28, Z_BASE + 0.10, Z_OPEN_TOP),
        0.0, SKIN + 0.09, fill_mat,
    )
    if mullion:
        face_panel(
            f"{tag}_mullion", FOOT, E_FRONT, u, rect_profile(0.10, Z_BASE + 0.10, Z_OPEN_TOP),
            0.0, SKIN + 0.14, navy,
        )
    # the beaded panel band, read as one recessed strip (plan s.2.6)
    face_panel(
        f"{tag}_panel", FOOT, E_FRONT, u, rect_profile(BAY_W - 0.28, Z_PANEL_A, Z_PANEL_B),
        0.0, SKIN + 0.04, navy,
    )
    face_panel(
        f"{tag}_stud", FOOT, E_FRONT, u, rect_profile(0.24, Z_PANEL_A + 0.10, Z_PANEL_B - 0.10),
        0.0, SKIN + 0.10, navy,
    )
    # the transom strip
    face_panel(
        f"{tag}_transom", FOOT, E_FRONT, u, rect_profile(BAY_W - 0.28, Z_TRAN_A, Z_TRAN_B),
        0.0, SKIN + 0.09, glass,
    )
    if glow_mat is not None:
        face_panel(
            f"{tag}_glow", FOOT, E_FRONT, u, rect_profile(BAY_W - 1.10, Z_BASE + 0.55, Z_OPEN_TOP - 0.45),
            SKIN + 0.11, SKIN + 0.16, glow_mat,
        )


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    sand = material("Toy_sand")
    stone = material("Toy_stone")
    navy = material("Toy_navy")
    glass = material("Toy_glass")
    rust = material("Toy_rust")
    steel = material("Toy_steel")
    ink = material("Toy_ink")
    trim = material("Toy_trim")
    roofd = material("Toy_roofd")
    wglow = material("Toy_glass_Glow")
    tglow = material("Toy_gold_Glow")

    # --- the one mass --------------------------------------------------------
    prism("body", FOOT, 0.0, Z_DECK, sand, mat_caps=roofd)

    # --- base band -----------------------------------------------------------
    ring_band("base", FOOT, 0.0, Z_BASE, -0.05, 0.06, stone)

    # --- the parapet ring and its coping -------------------------------------
    # Carried around all four faces INCLUDING both party walls: the re-bake
    # removes 21 and 29 with this building, so both flanks are public until they
    # get GLBs of their own (plan s.2.10, s.2.13).
    ring_band("parapet", FOOT, Z_DECK, Z_PARA, -0.30, 0.02, sand)
    # The coping. This sets the bounding-box top and must land exactly on
    # Z_CREST = 10.20 m, Overture's per-ring USGS-LiDAR height for way/112759868.
    ring_band("coping", FOOT, Z_PARA, Z_CREST, -0.36, 0.09, stone)

    # =========================== SOUTH PARK FRONT ============================
    # u runs from the NORTH-EAST end of the frontage (the 21 South Park party
    # wall) to the SOUTH-WEST end (29 South Park), which is left-to-right as the
    # Jan 2025 photograph reads it from the street.

    # bay 1: the pair of flush freight-scale doors, no glazing
    ground_bay("bay_ne", FRONT_W * 0.5 / BAY_N, navy, glass, navy, mullion=True)
    # bay 2: the divided-light shopfront window
    ground_bay("bay_c", FRONT_W * 1.5 / BAY_N, navy, glass, glass, glow_mat=tglow, mullion=True)
    # bay 3: the MAHOGANY DOUBLE DOOR at the address numeral - the one warm
    # accent on the building
    ground_bay("bay_sw", FRONT_W * 2.5 / BAY_N, navy, glass, rust, glow_mat=tglow, mullion=True)
    # the glazed upper half of the mahogany door
    face_panel(
        "entry_light", FOOT, E_FRONT, FRONT_W * 2.5 / BAY_N,
        rect_profile(BAY_W - 0.90, 2.05, Z_OPEN_TOP - 0.16), 0.0, SKIN + 0.14, glass,
    )

    # --- ground-floor cornice band -------------------------------------------
    face_panel(
        "cornice", FOOT, E_FRONT, FRONT_W / 2.0, rect_profile(FRONT_W, Z_CORN_A, Z_CORN_B),
        0.0, SKIN + 0.10, stone,
    )

    # --- the arcade: six segmental-arched lights, the whole identity ---------
    # Two lit at night, not six: an office row with every window on reads as a
    # render. The warm ground floor is the hero.
    for i in range(ARCH_N):
        u = FRONT_W * (i + 0.5) / ARCH_N
        glow = wglow if i in (1, 4) else None
        arched_window(f"arch{i}", u, navy, glass, glow_mat=glow, stone=stone, ink=ink)

    # ======================== NORTH-EAST PARTY WALL ==========================
    # 21 South Park is hard against this wall at a 0.00 m gap. Blind painted
    # brick with the parapet carried across - finished, but no ornament: every
    # triangle spent here is a triangle taken off the arcade.

    # ======================== SOUTH-WEST PARTY WALL ==========================
    # 29 South Park, likewise blind.

    # ============================== REAR FACE ================================
    # Not observed by any source consulted; kept blunt on the strength of the
    # type (REFERENCE.md s.4, plan s.2.15). Two small service windows and
    # nothing else - a loading door would be unsurprising here but nothing
    # establishes one.
    for i, u in enumerate((3.60, 8.60)):
        face_panel(f"rear_win{i}_frame", FOOT, E_REAR, u, rect_profile(1.10, 5.60, 6.70), 0.0, 0.07, navy)
        face_panel(f"rear_win{i}_fill", FOOT, E_REAR, u, rect_profile(0.86, 5.76, 6.54), 0.0, 0.13, glass)

    # ================================= ROOF ==================================
    # The 2026 nadir aerial reads at ~3 cm/px: plant packed into the middle
    # third TOWARD THE FRONT, the rear third bare membrane, two low glazed
    # monitors among it, no penthouse and no bulkhead. v is measured from the
    # centre of the lot, negative toward South Park.
    # No plinth slab: the first aerial put a black rectangle in the middle of
    # the roof that read as a hole. The units sit straight on the membrane, as
    # they do in the photograph.
    for tag, (u, v) in {
        "a": (-3.20, -9.40),
        "b": (-0.60, -7.90),
        "c": (2.90, -6.60),
        "d": (-2.60, -3.60),
        "e": (1.40, -2.10),
        "f": (-3.30, 1.20),
    }.items():
        lot_box(f"mech_{tag}", u, v, Z_DECK, Z_DECK + 0.46, 1.05, 1.55, trim)
        lot_box(f"mech_{tag}_cap", u, v, Z_DECK + 0.44, Z_DECK + 0.50, 1.11, 1.61, steel)
    lot_cyl("fan_a", 3.40, -10.20, Z_DECK, Z_DECK + 0.41, 0.42, steel)
    lot_cyl("fan_b", 0.90, -4.60, Z_DECK, Z_DECK + 0.41, 0.42, steel)
    lot_cyl("fan_c", -1.30, 3.60, Z_DECK, Z_DECK + 0.41, 0.42, steel)
    # Two low glazed monitors. Skylights, not penthouses - the aerial shows a
    # pane grid on both and neither breaks the parapet line.
    for tag, (u, v) in {"a": (2.60, -3.90), "b": (1.90, -12.10)}.items():
        lot_box(f"sky_{tag}_kerb", u, v, Z_DECK, Z_DECK + 0.18, 1.40, 2.20, trim)
        lot_box(f"sky_{tag}", u, v, Z_DECK + 0.14, Z_DECK + 0.34, 1.16, 1.96, glass)
    # A vent pipe on the rear half, the only thing back there.
    lot_cyl("vent", 2.40, 9.60, Z_DECK, Z_DECK + 0.55, 0.16, steel, segs=8)
    lot_cyl("vent_b", -3.90, 6.30, Z_DECK, Z_DECK + 0.48, 0.14, steel, segs=8)

    # Bevel budget: the one chunky mass and the parapet rings carry the
    # miniature read and get the full 0.12/2. Applied panels are small and
    # numerous - frames and reveals get a token 1-segment softening, and the
    # fills, glow plates, mullions and bars none at all.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if (
            name.endswith(("_fill", "_glow", "_open", "_transom", "_bar", "_stud", "_mullion", "_cap", "_archivolt"))
            or name == "entry_light"
        ):
            continue
        if name.endswith(("_frame", "_reveal", "_panel")):
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
    print("[build] anchor lon/lat: -122.3931439 37.7817369 (OSM way/112759868 centroid)")
    print("[build] South Park front heading: 314.8 deg true (NW)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "27-south-park.blend")
    glb = os.path.join(out, "27-south-park.glb")
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
