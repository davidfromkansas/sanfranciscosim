"""Deterministic Blender build of the SF-SIM miniature Coit Tower.

    blender -b --python build_coit_tower.py -- [--out DIR]

Writes coit-tower.blend and coit-tower.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east,
+Y true north, origin at the base centre, min Z = 0, so the export needs no
transforms applied after the fact.

Design (see REFERENCE.md for the sources behind every number):

* a two-tier round rotunda base (the mapped 22.4 m footprint) with four flat
  colonnaded bays on the measured cross - the entrance bay faces bearing 346
  degrees, toward the real parking-circle approach (NNW, not the plan's SE);
* a gently tapering shaft carrying 24 crisp concave flutes, ending in a
  dentil course - the count is a documented visual inference, locked to the
  8 crown bays (3 flutes per bay);
* a two-tier arcaded crown: 8 tall round-arched loggia openings with chunky
  toy balustrades over a glowing inner drum, triple slot groups over each
  pier, then a set-back OPEN-TOPPED lantern ring with 8 arches, a flared rim
  and a skylight ring on the well floor for the app's downward camera;
* flat Toy_* materials only; the loggia inner drum and the lantern arch
  reveals are the only _Glow surfaces (the crown is what reads at night).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

H_TOTAL = 64.0        # architectural height above the tower's own terrace
BEARING0 = 346.0      # entrance bay bearing: the measured NNW approach

# rotunda base (OSM footprint: ~22.4 m extent with four flat bays)
ROT_R = 10.4          # main drum radius
BAY_FACE_R = 11.2     # flat bay faces sit on the mapped 22.4 m extent
BAY_W = 7.2           # bay width (chord)
ROT_H = 6.2           # colonnade tier height
CORNICE_H = 0.6
MID_R = 9.3           # second tier drum
MID_TOP = 8.6
STEP_R = 7.9          # narrow step ring under the shaft
STEP_TOP = 9.3

# shaft
SHAFT_R0 = 6.7        # radius at the foot
SHAFT_R1 = 6.15       # radius at the head (gentle taper)
SHAFT_Z0 = STEP_TOP
SHAFT_Z1 = 51.8
FLUTES = 24
FLUTE_DEPTH = 0.38
FLUTE_Z0 = 11.2       # flutes ramp in above a smooth foot band
FLUTE_Z1 = 49.9       # ... and out below a smooth head band

# dentil course under the crown
DENT_Z0, DENT_Z1 = 51.8, 52.3
RING_Z0, RING_Z1 = 52.3, 52.6

# loggia (observation) tier: 8 arched bays + 8 piers, faceted like the original
LOG_R = 6.85
LOG_Z0, LOG_Z1 = 52.6, 59.4
LOG_T = 0.7           # wall thickness
ARCH_W = 2.5
ARCH_SILL = 53.8
ARCH_SPRING = 56.9    # semicircle above -> apex 58.15
BAL_TOP = 54.9

# lantern tier: set back, open top
LAN_R = 4.9
LAN_Z0, LAN_Z1 = 59.4, 63.5
LAN_T = 0.55
LAN_ARCH_W = 1.7
LAN_SILL = 60.1
LAN_SPRING = 62.0
RIM_R = 5.15          # slightly flared rim lip
RIM_Z0, RIM_Z1 = 63.5, H_TOTAL

BAYS = 8
ARC_SEG = 10          # segments in each arch semicircle
PHASE = math.radians(BEARING0)

# Project palette from .agents/skills/sf-asset-check (hex, sRGB). Materials are
# authored with the linear equivalents, which is what the shipped kit GLBs hold.
PALETTE_HEX = {
    "Toy_white": "f7f4ec",
    "Toy_trim": "f3efe6",
    "Toy_stone": "d9d2c2",
    "Toy_glass": "2a4d73",
    "Toy_ink": "3a3530",
    "Toy_white_Glow": "f7f4ec",
    "Toy_gold_Glow": "caa64a",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


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
        # Flagged for the app's night pass; emission is off in the daylight asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    mat.blend_method = "OPAQUE"
    return mat


# -------------------------------------------------------------- mesh helpers


def new_mesh(name, verts, faces, materials, face_mats=None, recalc=True):
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
    if recalc:
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.free()
    mesh.shade_flat()
    return obj


def bevel(obj, width=0.12, segments=2):
    """Miniature-style edge softening on the chunky solids (style bible s.4)."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.bevel(
        bm,
        geom=list(bm.verts) + list(bm.edges),
        offset=width,
        segments=segments,
        profile=0.5,
        affect="EDGES",
        clamp_overlap=True,
    )
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def rot2(p, ang):
    c, s = math.cos(ang), math.sin(ang)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def frame(bearing_deg):
    """Outward direction and right-hand tangent for a compass bearing."""
    b = math.radians(bearing_deg)
    return (math.sin(b), math.cos(b)), (math.cos(b), -math.sin(b))


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0):
    hx, hy = sx / 2, sy / 2
    corners = [rot2(c, yaw) for c in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy))]
    verts = [(cx + x, cy + y, z0) for x, y in corners]
    verts += [(cx + x, cy + y, z1) for x, y in corners]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


def panel_box(name, bearing_deg, radial, along, z0, z1, size_along, thickness, mat):
    """A box on a compass-bearing frame: `radial` = distance of the OUTER face
    from the origin, `along` = sideways offset on the tangent."""
    out, tan = frame(bearing_deg)
    cx = out[0] * (radial - thickness / 2) + tan[0] * along
    cy = out[1] * (radial - thickness / 2) + tan[1] * along
    return box(name, cx, cy, z0, z1, size_along, thickness, mat,
               yaw=-math.radians(bearing_deg))


def ring_pts(r, z, seg, phase=PHASE):
    return [(r * math.sin(phase + 2 * math.pi * i / seg),
             r * math.cos(phase + 2 * math.pi * i / seg), z) for i in range(seg)]


def cyl(name, r, z0, z1, mat, seg=36, cap_top=True, cap_bottom=True):
    verts = ring_pts(r, z0, seg) + ring_pts(r, z1, seg)
    faces = [(i, seg + i, seg + (i + 1) % seg, (i + 1) % seg) for i in range(seg)]
    if cap_bottom:
        faces.append(tuple(range(seg)))
    if cap_top:
        faces.append(tuple(range(2 * seg - 1, seg - 1, -1)))
    return new_mesh(name, verts, faces, [mat])


def tube(name, r, z0, z1, mat, seg=36, t=0.06):
    """A thin closed wall ring - used where a bare cylinder surface would
    leave single-sided geometry (every face in the export must be a solid)."""
    return ring_wall(name, r - t, r, z0, z1, mat, seg=seg)


def annulus(name, r_in, r_out, z, mat, seg=36, t=0.05):
    """A flat ring surface with its top face at z, as a thin closed solid."""
    return ring_wall(name, r_in, r_out, z - t, z, mat, seg=seg)


def ring_wall(name, r_in, r_out, z0, z1, mat, seg=36):
    """A closed band: outer wall, top ring, inner wall, bottom ring."""
    verts = (ring_pts(r_out, z0, seg) + ring_pts(r_out, z1, seg)
             + ring_pts(r_in, z1, seg) + ring_pts(r_in, z0, seg))
    faces = []
    for k in range(4):
        a0, b0 = k * seg, ((k + 1) % 4) * seg
        for i in range(seg):
            j = (i + 1) % seg
            faces.append((a0 + i, b0 + i, b0 + j, a0 + j))
    return new_mesh(name, verts, faces, [mat], recalc=False)


def disc(name, r, z, mat, seg=36, t=0.05):
    """A flat disc with its top face at z, as a thin closed solid."""
    return cyl(name, r, z - t, z, mat, seg=seg)


def arch_wall(name, bearing_deg, radial, width, z0, z1, aw, sill, spring,
              thickness, mat, tunnel_mat=None):
    """A flat wall panel with a through arch opening, standing on a compass
    bearing with its outer face `radial` metres from the origin. Closed solid;
    vertices are pooled so the mesh is manifold and normals recalc cleanly."""
    out, tan = frame(bearing_deg)
    r = aw / 2
    pool = {}
    verts = []
    faces = []
    fmats = []

    def vid(x, z, depth):
        key = (round(x, 5), round(z, 5), round(depth, 5))
        if key not in pool:
            d = radial - depth
            pool[key] = len(verts)
            verts.append((out[0] * d + tan[0] * x, out[1] * d + tan[1] * x, z))
        return pool[key]

    # hole boundary, counter-clockwise in panel space (x right, z up)
    hole = [(-r, sill), (r, sill), (r, spring)]
    for i in range(1, ARC_SEG):
        a = math.pi * i / ARC_SEG
        hole.append((r * math.cos(a), spring + r * math.sin(a)))
    hole.append((-r, spring))

    hw = width / 2
    arc = hole[2:]                # (r, spring) ... over the top ... (-r, spring)
    # Every face below is emitted so that each edge is shared by exactly two
    # faces (no T-junctions): recalc_face_normals then orients the closed
    # solid unambiguously.
    for depth, flip in ((0.0, False), (thickness, True)):
        def quad(p0, p1, p2, p3):
            idx = [vid(x, z, depth) for x, z in (p0, p1, p2, p3)]
            faces.append(tuple(reversed(idx)) if flip else tuple(idx))
            fmats.append(0)

        # bottom band, split at the arch jambs
        quad((-hw, z0), (-r, z0), (-r, sill), (-hw, sill))
        quad((-r, z0), (r, z0), (r, sill), (-r, sill))
        quad((r, z0), (hw, z0), (hw, sill), (r, sill))
        # side columns, split at the spring line
        quad((-hw, sill), (-r, sill), (-r, spring), (-hw, spring))
        quad((-hw, spring), (-r, spring), (-r, z1), (-hw, z1))
        quad((r, sill), (hw, sill), (hw, spring), (r, spring))
        quad((r, spring), (hw, spring), (hw, z1), (r, z1))
        # strips between the arc and the top edge
        for a, b in zip(arc, arc[1:]):
            quad((b[0], b[1]), (a[0], a[1]), (a[0], z1), (b[0], z1))

    # tunnel faces around the hole
    n = len(hole)
    for i in range(n):
        a, b = hole[i], hole[(i + 1) % n]
        ia0, ib0 = vid(*a, 0.0), vid(*b, 0.0)
        ia1, ib1 = vid(*a, thickness), vid(*b, thickness)
        faces.append((ia0, ib0, ib1, ia1))
        fmats.append(1 if tunnel_mat else 0)

    def rim_quad(a, b):
        faces.append((vid(*a, 0.0), vid(*b, 0.0), vid(*b, thickness), vid(*a, thickness)))
        fmats.append(0)

    # outer edge faces, subdivided to match the front/back partitions
    for xa, xb in ((-hw, -r), (-r, r), (r, hw)):                  # bottom
        rim_quad((xa, z0), (xb, z0))
    top_xs = [-hw] + sorted(p[0] for p in arc) + [hw]             # top
    for xa, xb in zip(top_xs, top_xs[1:]):
        rim_quad((xa, z1), (xb, z1))
    for x in (-hw, hw):                                           # sides
        rim_quad((x, z0), (x, sill))
        rim_quad((x, sill), (x, spring))
        rim_quad((x, spring), (x, z1))

    mats = [mat] + ([tunnel_mat] if tunnel_mat else [])
    return new_mesh(name, verts, faces, mats, fmats)


# --------------------------------------------------------------------- build


def shaft_radius(z):
    t = (z - SHAFT_Z0) / (SHAFT_Z1 - SHAFT_Z0)
    return SHAFT_R0 + (SHAFT_R1 - SHAFT_R0) * max(0.0, min(1.0, t))


def shaft_ring(z, fluted):
    """120-point plan ring: 24 sectors of 15 deg, each a shallow concave
    channel between narrow fillets (5 points per sector)."""
    R = shaft_radius(z)
    d = FLUTE_DEPTH if fluted else 0.0
    pts = []
    for k in range(FLUTES):
        a0 = PHASE + math.radians(k * 15.0)
        for da, dr in ((1.8, 0.0), (5.0, d * 0.82), (7.5, d), (10.0, d * 0.82), (13.2, 0.0)):
            a = a0 + math.radians(da)
            pts.append(((R - dr) * math.sin(a), (R - dr) * math.cos(a), z))
    return pts


def build_shaft(white):
    zs = [(SHAFT_Z0 - 0.01, False), (FLUTE_Z0 - 0.55, False), (FLUTE_Z0, True),
          (FLUTE_Z1, True), (FLUTE_Z1 + 0.55, False), (SHAFT_Z1, False)]
    rings = [shaft_ring(z, fl) for z, fl in zs]
    n = len(rings[0])
    verts = [v for ring in rings for v in ring]
    faces = []
    for r in range(len(rings) - 1):
        for i in range(n):
            j = (i + 1) % n
            faces.append((r * n + i, r * n + j, (r + 1) * n + j, (r + 1) * n + i))
    faces.append(tuple(range(n)))                                   # bottom cap
    faces.append(tuple(range(len(rings) * n - 1, (len(rings) - 1) * n - 1, -1)))
    return new_mesh("shaft", verts, faces, [white])


def build_rotunda(white, trim, stone, glass, ink, gold_glow):
    bay_bearings = [BEARING0 + k * 90.0 for k in range(4)]

    tube("rotunda_drum", ROT_R, 0.0, ROT_H + 0.01, white, seg=36)
    ring_wall("rotunda_cornice", ROT_R - 0.4, ROT_R + 0.3, ROT_H, ROT_H + CORNICE_H,
              trim, seg=36)
    annulus("rotunda_roof", MID_R - 0.4, ROT_R - 0.4, ROT_H + CORNICE_H, stone, seg=36)
    tube("mid_drum", MID_R, ROT_H + CORNICE_H - 0.01, MID_TOP + 0.01, white, seg=36)
    annulus("mid_roof", STEP_R - 0.4, MID_R, MID_TOP, stone, seg=36)
    tube("step_ring", STEP_R, MID_TOP - 0.01, STEP_TOP, white, seg=36)
    annulus("step_roof", SHAFT_R0 - 0.3, STEP_R, STEP_TOP, stone, seg=36)

    for bi, bearing in enumerate(bay_bearings):
        is_entrance = bi == 0
        bay = panel_box(f"bay_{bi}", bearing, BAY_FACE_R, 0.0, 0.0, ROT_H - 0.01,
                        BAY_W, BAY_FACE_R - ROT_R + 3.2, white)
        bevel(bay, width=0.12, segments=2)
        cap = panel_box(f"bay_{bi}_cap", bearing, BAY_FACE_R + 0.15, 0.0,
                        ROT_H - 0.01, ROT_H + CORNICE_H - 0.03, BAY_W + 0.3, 1.6, trim)
        bevel(cap, width=0.08, segments=1)
        # four square pilasters across the face
        for k, xo in enumerate((-2.85, -0.95, 0.95, 2.85)):
            p = panel_box(f"bay_{bi}_pier_{k}", bearing, BAY_FACE_R + 0.22, xo,
                          0.0, ROT_H - 0.35, 0.62, 0.5, white)
            bevel(p, width=0.08, segments=1)
        if is_entrance:
            # doorway, phoenix relief panel - the identity face (style bible s.8)
            panel_box("entrance_door", bearing, BAY_FACE_R + 0.06, 0.0,
                      0.0, 3.4, 1.9, 0.28, ink)
            ph = panel_box("entrance_phoenix", bearing, BAY_FACE_R + 0.16, 0.0,
                           3.7, 5.3, 1.7, 0.3, trim)
            panel_box("entrance_lamp", bearing, BAY_FACE_R + 0.18, 0.0,
                      3.44, 3.64, 1.5, 0.06, gold_glow)
            bevel(ph, width=0.07, segments=1)
            for k, xo in enumerate((-1.9, 1.9)):
                panel_box(f"entrance_win_{k}", bearing, BAY_FACE_R + 0.05, xo,
                          0.9, 5.1, 1.25, 0.24, glass)
        else:
            for k, xo in enumerate((-1.9, 0.0, 1.9)):
                panel_box(f"bay_{bi}_win_{k}", bearing, BAY_FACE_R + 0.05, xo,
                          0.9, 5.1, 1.25, 0.24, glass)


def build_dentils(white, trim):
    for k in range(FLUTES):
        a = PHASE + math.radians(k * 15.0 + 7.5)
        x, y = math.sin(a), math.cos(a)
        r = SHAFT_R1 + 0.12
        box(f"dentil_{k}", x * r, y * r, DENT_Z0, DENT_Z1, 0.5, 0.55, white, yaw=-a)
    ring_wall("crown_ring", SHAFT_R1 - 0.3, LOG_R - 0.05, RING_Z0, RING_Z1, trim,
              seg=48)


def build_loggia(white, trim, ink, glow):
    bay_arc, pier_arc = 31.0, 14.0
    annulus("loggia_floor", SHAFT_R1 - 0.6, LOG_R, LOG_Z0 + 0.02, white, seg=36)
    # the glowing inner drum: white by day, the lit gallery ring at night
    tube("loggia_core", LOG_R - LOG_T - 0.25, LOG_Z0 + 0.03, LOG_Z1 - 0.02, white, seg=32)
    # night lamp: a thin glow shell floating between the core and the arch
    # backs - hidden against the white core by day, the lit gallery at night
    tube("loggia_glow_shell", LOG_R - LOG_T - 0.08, ARCH_SILL - 0.2,
         ARCH_SPRING + 1.4, glow, seg=24)
    for k in range(BAYS):
        bearing = BEARING0 + k * 45.0
        bay_w = 2 * LOG_R * math.sin(math.radians(bay_arc / 2)) + 0.16
        arch_wall(f"loggia_bay_{k}", bearing, LOG_R, bay_w,
                  LOG_Z0 - 0.02, LOG_Z1, ARCH_W, ARCH_SILL, ARCH_SPRING, LOG_T, white)
        # chunky toy balustrade across the arch
        sill = panel_box(f"loggia_balsill_{k}", bearing, LOG_R + 0.06, 0.0,
                         ARCH_SILL - 0.25, ARCH_SILL + 0.08, ARCH_W + 0.5, 0.42, trim)
        rail = panel_box(f"loggia_rail_{k}", bearing, LOG_R + 0.06, 0.0,
                         BAL_TOP - 0.22, BAL_TOP, ARCH_W + 0.3, 0.34, trim)
        bevel(sill, width=0.06, segments=1)
        bevel(rail, width=0.06, segments=1)
        for pk, xo in enumerate((-0.8, 0.0, 0.8)):
            panel_box(f"loggia_post_{k}_{pk}", bearing, LOG_R - 0.02, xo,
                      ARCH_SILL - 0.05, BAL_TOP - 0.2, 0.2, 0.2, trim)
        # pier panel between this bay and the next, with the triple slot group
        pier_bearing = bearing + 22.5
        pier_w = 2 * LOG_R * math.sin(math.radians(pier_arc / 2)) + 0.95
        panel_box(f"loggia_pier_{k}", pier_bearing, LOG_R + 0.001, 0.0,
                  LOG_Z0 - 0.02, LOG_Z1, pier_w, LOG_T, white)
        for sk, xo in enumerate((-0.42, 0.0, 0.42)):
            panel_box(f"loggia_slot_{k}_{sk}", pier_bearing, LOG_R + 0.06, xo,
                      57.6, 58.8, 0.3, 0.14, ink)
            panel_box(f"loggia_slotglow_{k}_{sk}", pier_bearing, LOG_R + 0.085, xo,
                      57.68, 58.72, 0.22, 0.03, glow)


def build_lantern(white, trim, stone, glass, glow):
    annulus("loggia_deck", LAN_R - 0.4, LOG_R - 0.25, LOG_Z1 + 0.02, stone, seg=36)
    ring_wall("loggia_parapet", LOG_R - 0.25, LOG_R + 0.1, LOG_Z1 + 0.02, LOG_Z1 + 0.45,
              trim, seg=36)
    for k in range(BAYS):
        bearing = BEARING0 + 22.5 + k * 45.0
        w = 2 * LAN_R * math.sin(math.radians(22.5)) + 0.3
        arch_wall(f"lantern_bay_{k}", bearing, LAN_R, w, LAN_Z0, LAN_Z1,
                  LAN_ARCH_W, LAN_SILL, LAN_SPRING, LAN_T, white)
    # night lamp inside the well: reads through all 8 arches and from above
    tube("lantern_glow_liner", LAN_R - LAN_T - 0.06, LAN_SILL - 0.2, LAN_Z1 - 0.3,
         glow, seg=24)
    # flared rim lip, open in the centre (aerials look straight down the well)
    ring_wall("lantern_rim", LAN_R - LAN_T, RIM_R, RIM_Z0 - 0.02, RIM_Z1, white, seg=36)
    # the well floor: deck, skylight ring, and the small central cap
    disc("well_floor", LAN_R - 0.02, LAN_Z0 + 0.2, stone, seg=36)
    ring_wall("skylight_ring", 2.3, 3.4, LAN_Z0 + 0.21, LAN_Z0 + 0.42, glass, seg=32)
    cyl("well_core", 1.5, LAN_Z0 + 0.21, LAN_Z0 + 1.6, white, seg=24)
    cyl("well_cap", 1.7, LAN_Z0 + 1.59, LAN_Z0 + 1.95, trim, seg=24)


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    white = material("Toy_white")
    trim = material("Toy_trim")
    stone = material("Toy_stone")
    glass = material("Toy_glass")
    ink = material("Toy_ink")
    glow = material("Toy_white_Glow")
    gold_glow = material("Toy_gold_Glow")

    build_rotunda(white, trim, stone, glass, ink, gold_glow)
    build_shaft(white)
    build_dentils(white, trim)
    build_loggia(white, trim, ink, glow)
    build_lantern(white, trim, stone, glass, glow)
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
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "coit-tower.blend")
    glb = os.path.join(out, "coit-tower.glb")
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
