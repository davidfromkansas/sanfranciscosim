"""Deterministic Blender build of the SF-SIM miniature 135 South Park.

    blender -b --python build_135_south_park.py -- [--out DIR]

Writes 135-south-park.blend and 135-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = footprint area centroid (anchor
lon -122.3940203, lat 37.7811030), min Z = 0, roof-monitor crest exactly 8.5 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured OSM footprint (way/113545684): an L, 19.71 m of frontage on
  South Park running back only 13.9 m, past which only a 7.75 m strip along the
  party wall continues another 14.8 m to the rear. The missing ~14.8 x 12.0 m
  rectangle is a re-entrant rear yard and is left as a true void. 45 deg off the
  world axes like the whole SoMa grid;
* a two-storey brick box: Toy_rust masonry on all four elevations, because
  unlike 380 Brannan one block away there is no evidence of a painted front —
  and no evidence against one either. See REPORT.md;
* the north-east elevation is a PARTY WALL shared with 123 South Park along its
  whole 28.65 m. It carries no openings at all. That is the one facade fact in
  this dossier that is measured rather than inferred, so it is honoured exactly;
* the identity feature, and the reason this asset exists: a raised glazed ROOF
  MONITOR running along the deep wing, parallel to the party wall, from the
  7.0 m deck up to the 8.5 m crest, under a bright Toy_trim lid that ties it
  into the coping ring and keeps it legible from directly overhead. It is what
  the 2010 LiDAR maximum of 8.52 m over a 7.06 m deck is measuring, and what the
  Esri aerial shows as a lighter raised plane with its own shadow;
* night state: the monitor is the hero glow — a lit lantern on a dark roof,
  legible from the app's aerial camera in a way an 8.5 m brick box never is —
  plus four lit windows on the front. Glow surfaces are thin shells proud of
  the opaque glazing (the app renders _Glow in a separate layer that is ~12%
  alpha by day — never author a primary surface as glow);
* a designed roof for the app's downward camera: dark deck, bright Toy_trim
  coping ring, the monitor as its spine, a mechanical pair and hatch at the
  rear, one round vent cowl on the front half.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way/113545684 projected with the app's tangent projection and recentred on
# the polygon's area centroid. CCW, +X east, +Y north.
FOOTPRINT = [
    (-2.133, 13.562),    # 0  front / party-wall corner
    (-16.178, -0.267),   # 1  front / south-west corner
    (-6.331, -10.127),   # 2  south-west flank -> rear of the front block
    (-0.180, -4.070),    # 3  jog
    (-1.456, -2.798),    # 4  jog
    (0.920, -0.455),     # 5  head of the deep wing's south-west flank
    (11.550, -11.089),   # 6
    (12.685, -12.227),   # 7  survey chamfer
    (18.114, -6.700),    # 8  rear / party-wall corner
    (1.457, 9.969),      # 9  party wall, intermediate vertex
]

# Edge index -> elevation. Outward normals verified against the survey.
EDGE_FRONT = 0    # 19.71 m, faces NW 315.4 deg — South Park
EDGE_SW = 1       # 13.93 m, faces SW 225.0 deg — gap to 147 South Park
EDGE_BACK_W = 2   # 8.63 m,  faces SE 135.4 deg — rear of the front block
EDGE_WING_SW = 5  # 15.04 m, faces SW 225.0 deg — deep wing, onto the rear yard
EDGE_REAR = 7     # 7.75 m,  faces SE 134.5 deg — rear, onto the courtyard
EDGE_PARTY = 8    # 23.57 m, faces NE  45.0 deg — PARTY WALL, no openings
EDGE_PARTY2 = 9   # 5.08 m,  faces NE  45.0 deg — same wall, front return

Z_DECK = 7.0         # roof deck (LiDAR mode 7.06, median 6.95)
Z_PARAPET = 7.9      # parapet crest (inferred: deck + 0.9 m)
Z_CREST = 8.5        # roof-monitor top = LiDAR max 8.52 -> the bbox top
Z_GROUND_TOP = 4.0   # ground-floor ceiling
Z_WIN0, Z_WIN1 = 4.4, 6.4   # upper-floor window band

SKIN = 0.0           # no applied front skin: one masonry material everywhere
PARAPET_T = 0.35     # parapet wall thickness
COPING = 0.15        # coping band height

PALETTE_HEX = {
    # Toy_rust rather than the palette's Toy_brick for the masonry, the same
    # swap 380 Brannan made 55 m away: c96f4a is saturated enough that a whole
    # building of it reads as an accent, and the style bible s.7 reserves
    # saturation for identity. Here the identity is the monitor, not the walls.
    "Toy_rust": "a86444",
    "Toy_trim": "f3efe6",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_ink": "3a3530",
    "Toy_glassl_Glow": "6f95b8",
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
    """Miter offset of the CCW footprint; positive d moves outward.

    Solved as the intersection of the two offset edge lines at each vertex, so
    it is correct at the reflex corners of this L as well as the convex ones —
    which matters, because two of the ten vertices are reflex and a naive
    normal-averaging offset would fold the parapet ring inside out there.
    """
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


def arch_profile(w, z0, z_spring, rise, seg=4):
    """Closed (u, z) profile: rectangle with a segmental-arched head."""
    a = w / 2.0
    pts = [(-a, z0), (a, z0), (a, z_spring)]
    if rise > 1e-4:
        radius = (a * a + rise * rise) / (2.0 * rise)
        cz = z_spring + rise - radius
        th0 = math.atan2(z_spring - cz, a)
        th1 = math.pi - th0
        for k in range(1, seg):
            th = th0 + (th1 - th0) * k / seg
            pts.append((radius * math.cos(th), cz + radius * math.sin(th)))
    pts.append((-a, z_spring))
    return pts


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
    """Miniature-style edge softening on the chunky solids (style bible s.4).

    Width is capped at a third of the object's thinnest dimension: the applied
    window panels here are 90-220 mm thick and a flat 0.12 m bevel on those
    relies entirely on clamp_overlap, which collapses opposing profiles into
    zero-area slivers. The remove_doubles/dissolve_degenerate pass sweeps up
    whatever clamping still pinches shut.
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
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-4)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-4, edges=list(bm.edges))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def prism(name, poly, z0, z1, mat, mat_caps=None):
    """Closed extrusion of a CCW polygon (walls + both caps).

    The caps are concave n-gons here; Blender tessellates them correctly on
    export, which the validator re-checks by signed volume on the re-import.
    """
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


def cylinder(name, cx, cy, z0, z1, radius, mat, seg=10):
    """Low-segment cylinder (style bible s.4: 8-14 segments)."""
    ring = [
        (cx + radius * math.cos(2 * math.pi * k / seg), cy + radius * math.sin(2 * math.pi * k / seg))
        for k in range(seg)
    ]
    return prism(name, ring, z0, z1, mat)


# Building-local frame: u runs along the party wall from the REAR corner
# (vertex 8) towards the front, v runs into the block away from that wall.
# Every roof position below is expressed in it, so the roof composition is
# described relative to the building rather than to the world axes.
_PA, _PL, _PT, _PN = poly_edge(EDGE_PARTY)


def uv_to_world(u, v):
    return (_PA[0] + _PT[0] * u - _PN[0] * v, _PA[1] + _PT[1] * u - _PN[1] * v)


def roof_box(name, u, v, z0, z1, su, sv, mat):
    cx, cy = uv_to_world(u, v)
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=math.atan2(_PT[1], _PT[0]))


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


def arched_opening(tag, edge, u, w, z0, z_spring, rise, frame_mat, fill_mat, glow_mat=None):
    """Frame panel + a smaller fill that protrudes further, so the frame reads
    as a border ring around a recessed opening. No booleans, all closed solids."""
    face_panel(
        f"{tag}_frame", edge, u, arch_profile(w, z0, z_spring, rise), 0.0, SKIN + 0.06, frame_mat
    )
    inset = 0.20
    face_panel(
        f"{tag}_fill",
        edge,
        u,
        arch_profile(w - 2 * inset, z0 + inset, z_spring, max(rise - 0.08, 0.0)),
        0.0,
        SKIN + 0.13,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.34
        face_panel(
            f"{tag}_glow",
            edge,
            u,
            arch_profile(w - 2 * g, z0 + g, z_spring - 0.12, max(rise - 0.16, 0.0)),
            SKIN + 0.10,
            SKIN + 0.17,
            glow_mat,
        )


def rect_opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None):
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, SKIN + 0.06, frame_mat)
    inset = 0.18
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
        g = 0.32
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

    brick = material("Toy_rust")
    trim = material("Toy_trim")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    ink = material("Toy_ink")
    gglow = material("Toy_glass_Glow")
    mglow = material("Toy_glassl_Glow")

    # --- masonry body: the L, its top cap IS the dark roof deck ------------
    prism("body", FOOTPRINT, 0.0, Z_DECK, brick, mat_caps=roofd)

    # --- parapet ring + coping ---------------------------------------------
    # The bright coping carried right round is what makes the ring read as a
    # ring from the app's downward camera, and what stops the dark deck reading
    # as an open tray. It also traces the re-entrant yard, which is the
    # silhouette this building is recognised by.
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET - COPING, -PARAPET_T, 0.0, brick)
    ring_band(
        "coping", FOOTPRINT, Z_PARAPET - COPING, Z_PARAPET, -PARAPET_T - 0.07, 0.07, trim
    )

    # --- South Park front (NW), 19.71 m -------------------------------------
    # Ground floor: the wide opening toward the SW end, the pedestrian entrance
    # with its canopy, two windows. All INFERRED — see the plan's 2.15.
    arched_opening("fr_freight", EDGE_FRONT, 15.2, 4.0, 0.0, 3.0, 0.45, trim, roofd)
    rect_opening("fr_door", EDGE_FRONT, 10.7, 1.7, 0.0, 3.0, trim, ink)
    face_panel(
        "fr_canopy", EDGE_FRONT, 10.7, rect_profile(2.6, 3.0, 3.22), 0.0, 1.15, trim
    )
    for k, u in enumerate((3.4, 6.9)):
        arched_opening(f"fr_gw{k}", EDGE_FRONT, u, 1.7, 1.1, 2.9, 0.3, trim, glass)

    # Upper floor: 5 clean bays of tall industrial glazing. Four of them light
    # at night; the fifth stays dark so the row does not read as a switchboard.
    for k, u in enumerate((2.7, 6.0, 9.3, 12.6, 15.9)):
        rect_opening(
            f"fr_up{k}",
            EDGE_FRONT,
            u,
            2.0,
            Z_WIN0,
            Z_WIN1,
            trim,
            glass,
            gglow if k != 2 else None,
        )

    # --- south-west flank of the front block (13.93 m) ----------------------
    for k, u in enumerate((3.6, 7.0, 10.4)):
        rect_opening(f"sw_up{k}", EDGE_SW, u, 1.7, Z_WIN0, Z_WIN1, trim, glass)
    arched_opening("sw_gw0", EDGE_SW, 7.0, 1.6, 1.1, 2.9, 0.3, trim, glass)

    # --- deep wing, south-west flank onto the rear yard (15.04 m) -----------
    for k, u in enumerate((2.6, 6.2, 9.8, 13.0)):
        rect_opening(f"wg_up{k}", EDGE_WING_SW, u, 1.7, Z_WIN0, Z_WIN1, trim, glass)
    for k, u in enumerate((4.4, 11.4)):
        arched_opening(f"wg_gw{k}", EDGE_WING_SW, u, 1.6, 1.1, 2.9, 0.3, trim, glass)

    # --- rear of the front block (8.63 m) and the rear wall (7.75 m) --------
    for k, u in enumerate((2.5, 6.1)):
        rect_opening(f"bw_up{k}", EDGE_BACK_W, u, 1.6, Z_WIN0, Z_WIN1, trim, glass)
    arched_opening("re_door", EDGE_REAR, 4.4, 3.0, 0.0, 2.9, 0.35, trim, roofd)
    rect_opening("re_up0", EDGE_REAR, 4.4, 1.7, Z_WIN0, Z_WIN1, trim, glass)

    # --- NORTH-EAST PARTY WALL: deliberately blank --------------------------
    # 28.65 m shared with 123 South Park, gap 0.0 m. A party wall cannot carry
    # openings, and this is the only facade fact in the dossier that is
    # measured rather than inferred. Do not add windows here.

    # --- the roof monitor: this asset's whole identity ----------------------
    # On the deep wing, long axis along the party wall, centred 7.5 m forward of
    # the rear corner and in the middle of the 7.75 m wing. Its cap sets the
    # bounding-box top and must land exactly on Z_CREST.
    # Revision 2, from the first aerial review (logged in REPORT.md). The first
    # pass capped the monitor in Toy_roofd, so from the app's downward camera it
    # was a dark slab on a dark deck and the identity cue vanished; and at 4.2 m
    # in a 7.75 m wing it read as a container filling the wing rather than as a
    # discrete lantern. Three changes: a BRIGHT Toy_trim lid that ties into the
    # coping ring, a narrower body with real deck margin either side, and glow
    # shells lifted clear of the 7.9 m parapet so the night state is actually
    # visible from outside the building.
    MON_U, MON_V, MON_L, MON_W = 7.6, 3.88, 12.0, 3.6
    LID = 0.20
    roof_box("monitor_kerb", MON_U, MON_V, Z_DECK, Z_DECK + 0.16, MON_L + 0.36, MON_W + 0.36, roofd)
    roof_box("monitor_body", MON_U, MON_V, Z_DECK + 0.16, Z_CREST - LID, MON_L, MON_W, glassl)
    roof_box("monitor_lid", MON_U, MON_V, Z_CREST - LID, Z_CREST, MON_L + 0.34, MON_W + 0.34, trim)
    # Glow shells, proud of the opaque clerestory on all four sides.
    #
    # Revision 3. Rev 2 started the band at 7.95 to clear the 7.9 m parapet,
    # reasoning from a side view — but the app's camera looks DOWN at 30-50 deg
    # and sees over the parapet onto the deck, and the monitor stands in the
    # middle of a 7.75 m wing, well inside the ring. Clipping to the parapet
    # therefore lit only 0.31 m of a 1.14 m clerestory and wasted most of the
    # feature. The band now runs 7.35-8.26 m: the whole of it reads from the
    # aerial, while from street level the parapet still hides its lower half,
    # which is what a real clerestory behind a parapet does.
    GLOW_Z0, GLOW_Z1 = Z_DECK + 0.35, Z_CREST - LID - 0.04
    for side, dv in (("sw", -(MON_W / 2 + 0.05)), ("ne", MON_W / 2 + 0.05)):
        roof_box(
            f"monitor_glow_{side}", MON_U, MON_V + dv, GLOW_Z0, GLOW_Z1, MON_L - 0.6, 0.09, mglow
        )
    for side, du in (("nw", MON_L / 2 + 0.05), ("se", -(MON_L / 2 + 0.05))):
        roof_box(
            f"monitor_glow_{side}", MON_U + du, MON_V, GLOW_Z0, GLOW_Z1, 0.09, MON_W - 0.6, mglow
        )

    # --- roof furniture -----------------------------------------------------
    # Grouped, not scattered (style bible s.10): mechanical pair at the rear of
    # the wing, hatch on the front block, one vent cowl on the front half.
    roof_box("hvac_a", 2.2, 5.9, Z_DECK, Z_DECK + 0.8, 1.8, 1.4, steel)
    roof_box("hvac_b", 3.9, 2.2, Z_DECK, Z_DECK + 0.6, 1.2, 1.0, steel)
    roof_box("roof_hatch", 17.6, 16.4, Z_DECK, Z_DECK + 0.5, 1.3, 1.1, roofd)
    cx, cy = uv_to_world(22.0, 11.5)
    cylinder("vent_cowl", cx, cy, Z_DECK, Z_DECK + 0.55, 0.4, steel)

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.12/2. The many small applied window panels get a token 1-segment
    # softening on their frames and none at all on fills and glow shells, which
    # is what keeps this under the 8,000-triangle cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")) or "_glow_" in obj.name:
            continue
        if obj.name.endswith("_frame"):
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
    print("[build] anchor lon/lat: -122.3940203 37.7811030 (footprint area centroid)")
    print("[build] South Park front heading: 315.4 deg true (NW)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "135-south-park.blend")
    glb = os.path.join(out, "135-south-park.glb")
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
