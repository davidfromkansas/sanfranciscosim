"""Deterministic Blender build of the SF-SIM miniature Grace Cathedral.

    blender -b --python build_grace_cathedral.py -- [--out DIR]

Writes grace-cathedral.blend and grace-cathedral.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y true
north, so the model drops into the city at its real-world heading; the origin
is the bounding-box centre and min Z = 0 (the east street level at the foot of
the great steps).

Every number is sourced in REFERENCE.md. The skeleton:

* footprint masses traced from OSM way/32946942 (long axis bearing 81.0 deg cw
  from true north, entrance front facing ~east onto Taylor Street);
* the published height trio - twin towers 53 m, nave ridge 39.6 m (derived:
  247 ft cross - 117 ft fleche), verdigris fleche with gold cross to 75.3 m;
* the 7.6 m "Canticle of the Sun" rose (ring + 12 chunky spokes, the
  documented Chartres 12-scheme) over the gold Ghiberti doors;
* 6 aisle bays of engaged stepped buttresses with pinnacle caps per flank
  (photo-verified: no true flying arches), cruciform transepts with unequal
  arms per the footprint, polygonal 5-facet apse with radiating buttresses;
* the 6.1 m podium climbed by full-width east steps;
* glow set per the app's dusk system (thin separate shells, never a primary
  surface): Toy_white_Glow rose tracery, Toy_gold_Glow portal tympanum +
  fleche lantern, Toy_mustard_Glow lit panes behind every window on the
  building - aisles, clerestory, transepts, choir, apse and tower stages.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ------------------------------------------------------------------ site data

# Local frame: u along the nave axis (u+ = the Taylor Street entrance end,
# compass bearing 81.03 deg), v across it (v+ = the north flank). The frame is
# rotated into world axes (+X east, +Y north) at mesh-creation time.
THETA = math.radians(90.0 - 81.03)      # math angle of u+ from +X (CCW)
CT, ST = math.cos(THETA), math.sin(THETA)

# Footprint bbox centre of OSM way/32946942 in WGS84 (build-frame origin).
BLON, BLAT = -122.4134968, 37.7918332
LAT0 = 37.77                            # app projection reference latitude
KX = 111320.0 * math.cos(math.radians(LAT0))
KY = 110540.0

# Key levels (m above the east street; see REFERENCE.md)
ENTRY = 6.1            # podium / entry-floor level (20 ft)
TOWER_TOP = 53.0       # published 174 ft
RIDGE = 39.6           # nave ridge (derived 130 ft)
CROSS_TOP = 75.3       # fleche cross top (published 247 ft)

# Cruciform plan in the local frame (from the OSM outline, metres)
NAVE_U0, NAVE_U1 = -6.8, 35.0           # aisled nave block
FAC_U0, FAC_U1 = 35.0, 45.9             # facade / twin-tower block
AXIS_V = 1.35                           # nave centreline
CORE_V0, CORE_V1 = -5.65, 8.35          # nave core (clerestory) walls
AISLE_VN0, AISLE_VN1 = 8.35, 14.7       # north aisle
AISLE_VS0, AISLE_VS1 = -12.0, -5.65     # south aisle
TRAN_U0, TRAN_U1 = -19.8, -6.7          # transept arms
TRAN_VN, TRAN_VS = 23.8, -19.6          # arm ends (north arm is longer)
CHOIR_U0, CHOIR_U1 = -36.7, -19.8
CHOIR_V0, CHOIR_V1 = -7.45, 10.15
APSE_C = (-39.3, AXIS_V)                # facet-circle centre
APSE_R = 8.8

BAYS = 6
BAY_W = (NAVE_U1 - NAVE_U0) / BAYS

AISLE_PAR = 17.8       # aisle parapet top
CLER_TOP = 32.0        # clerestory wall / nave eave parapet
EAVE = 31.2            # nave roof eave (under the parapet lip)
CHOIR_EAVE, CHOIR_RIDGE = 26.8, 34.5
APSE_WALL = 20.0

# Palette from .agents/skills/sf-asset-check (hex sRGB -> linear at runtime).
# Toy_roofc is a deliberate off-palette WARN: the roofs are photo-verified
# brown-copper standing-seam, not the plan's gray (REFERENCE.md).
PALETTE_HEX = {
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    "Toy_glass": "2a4d73",
    "Toy_ink": "3a3530",
    "Toy_gold": "caa64a",
    "Toy_verdigris": "9fb8a8",
    "Toy_roofc": "7c6553",
    "Toy_rust": "a86444",
    "Toy_white_Glow": "f7f4ec",
    "Toy_gold_Glow": "caa64a",
    "Toy_mustard_Glow": "d9a441",
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
        # Flagged for the app's night pass; emission ships OFF.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    return mat


# -------------------------------------------------------------- mesh plumbing


def W(u, v, z):
    """Local (u, v, z) -> world (x, y, z)."""
    return (u * CT - v * ST, u * ST + v * CT, z)


def new_mesh(name, verts_local, faces, materials, face_mats=None):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(W(*v)) for v in verts_local], [], faces)
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
    """Miniature edge softening on the chunky masses (style bible s.4)."""
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


def box(name, cu, cv, z0, z1, su, sv, mat, yaw=0.0):
    hx, hy = su / 2, sv / 2
    corners = [rot2(c, yaw) for c in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy))]
    verts = [(cu + a, cv + b, z0) for a, b in corners]
    verts += [(cu + a, cv + b, z1) for a, b in corners]
    faces = [
        (3, 2, 1, 0), (4, 5, 6, 7),
        (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


def pyramid(name, cu, cv, z0, base, z1, mat, yaw=0.0):
    h = base / 2
    corners = [rot2(c, yaw) for c in ((-h, -h), (h, -h), (h, h), (-h, h))]
    verts = [(cu + a, cv + b, z0) for a, b in corners] + [(cu, cv, z1)]
    faces = [(3, 2, 1, 0), (0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4)]
    return new_mesh(name, verts, faces, [mat])


def extrude_outline(name, outline_tz, base_uv, ang, depth, mat):
    """A closed slab: `outline_tz` is the face outline in (tangent, z), the
    face plane passes through base_uv with outward normal at local angle
    `ang`; the slab extends `depth` behind the face."""
    n = (math.cos(ang), math.sin(ang))
    t = (-math.sin(ang), math.cos(ang))
    verts = []
    for d in (0.0, -depth):
        for tt, zz in outline_tz:
            verts.append((base_uv[0] + t[0] * tt + n[0] * d,
                          base_uv[1] + t[1] * tt + n[1] * d, zz))
    k = len(outline_tz)
    faces = [tuple(range(k)), tuple(range(2 * k - 1, k - 1, -1))]
    for i in range(k):
        j = (i + 1) % k
        faces.append((i, j, k + j, k + i))
    return new_mesh(name, verts, faces, [mat])


def lancet(name, base_uv, ang, w, sill, apex, proud, depth, mat):
    """A chunky pointed-arch slab standing proud of a wall face. base_uv is a
    point ON the wall face at the lancet's centreline; the front face sits
    `proud` out along `ang`, the back is buried `depth` into the wall."""
    spring = sill + 0.55 * (apex - sill)
    shoulder = spring + 0.72 * (apex - spring)
    h = w / 2
    outline = [
        (-h, sill), (h, sill), (h, spring), (h * 0.45, shoulder),
        (0.0, apex), (-h * 0.45, shoulder), (-h, spring),
    ]
    n = (math.cos(ang), math.sin(ang))
    base = (base_uv[0] + n[0] * proud, base_uv[1] + n[1] * proud)
    return extrude_outline(name, outline, base, ang, depth + proud, mat)


def lit_lancet(name, base_uv, ang, w, sill, apex, proud, depth, glass_mat, glow_mat):
    """A pointed window that lights up at night.

    Two shells: the opaque `Toy_glass` pane (the only thing that carries the
    window by day) and, 5 cm in front of it, a smaller `*_Glow` pane standing
    for the lit interior. The glow pane is inset on all sides so a dark glazed
    reveal frames it, and its back edge is buried inside the wall - the app
    draws glow surfaces at only 12% opacity in daylight, so nothing here may
    depend on the glow shell to read as a window when the sun is up.
    """
    lancet(name, base_uv, ang, w, sill, apex, proud, depth, glass_mat)
    span = apex - sill
    lancet(f"{name}_lit", base_uv, ang, w * 0.72, sill + span * 0.07,
           apex - span * 0.08, proud + 0.05, 0.32, glow_mat)


def vring(name, base_uv, ang, cz, r_in, r_out, depth, mat, seg=24):
    """An annulus in a vertical plane (facing `ang`), as a closed solid."""
    n = (math.cos(ang), math.sin(ang))
    t = (-math.sin(ang), math.cos(ang))
    verts = []
    for d in (0.0, -depth):
        for r in (r_out, r_in):
            for i in range(seg):
                a = 2 * math.pi * i / seg
                tt, zz = r * math.cos(a), cz + r * math.sin(a)
                verts.append((base_uv[0] + t[0] * tt + n[0] * d,
                              base_uv[1] + t[1] * tt + n[1] * d, zz))
    faces = []
    def ring_pair(a0, b0):
        for i in range(seg):
            j = (i + 1) % seg
            faces.append((a0 + i, b0 + i, b0 + j, a0 + j))
    ring_pair(0, seg)                      # front face (outer->inner)
    ring_pair(3 * seg, 2 * seg)            # back face
    ring_pair(2 * seg, 0)                  # outer rim
    ring_pair(seg, 3 * seg)                # inner rim
    return new_mesh(name, verts, faces, [mat])


def vdisc(name, base_uv, ang, cz, r, depth, mat, seg=24):
    """A disc in a vertical plane, as a thin closed cylinder."""
    n = (math.cos(ang), math.sin(ang))
    t = (-math.sin(ang), math.cos(ang))
    verts = []
    for d in (0.0, -depth):
        for i in range(seg):
            a = 2 * math.pi * i / seg
            verts.append((base_uv[0] + t[0] * r * math.cos(a) + n[0] * d,
                          base_uv[1] + t[1] * r * math.cos(a) + n[1] * d,
                          cz + r * math.sin(a)))
    faces = [tuple(range(seg)), tuple(range(2 * seg - 1, seg - 1, -1))]
    for i in range(seg):
        j = (i + 1) % seg
        faces.append((i, j, seg + j, seg + i))
    return new_mesh(name, verts, faces, [mat])


def ring_pts(cu, cv, r, z, seg, phase=0.0):
    return [(cu + r * math.cos(phase + 2 * math.pi * i / seg),
             cv + r * math.sin(phase + 2 * math.pi * i / seg), z)
            for i in range(seg)]


def cyl(name, cu, cv, r, z0, z1, mat, seg=12, phase=0.0):
    verts = ring_pts(cu, cv, r, z0, seg, phase) + ring_pts(cu, cv, r, z1, seg, phase)
    faces = [(i, seg + i, seg + (i + 1) % seg, (i + 1) % seg) for i in range(seg)]
    faces.append(tuple(range(seg)))
    faces.append(tuple(range(2 * seg - 1, seg - 1, -1)))
    return new_mesh(name, verts, faces, [mat])


def cone(name, cu, cv, r0, r1, z0, z1, mat, seg=12, phase=0.0):
    verts = ring_pts(cu, cv, r0, z0, seg, phase) + ring_pts(cu, cv, r1, z1, seg, phase)
    faces = [(i, seg + i, seg + (i + 1) % seg, (i + 1) % seg) for i in range(seg)]
    faces.append(tuple(range(seg)))
    faces.append(tuple(range(2 * seg - 1, seg - 1, -1)))
    return new_mesh(name, verts, faces, [mat])


def hring(name, cu, cv, r_in, r_out, z0, z1, mat, seg=12, phase=0.0):
    """A horizontal closed band (outer wall, top, inner wall, bottom)."""
    verts = (ring_pts(cu, cv, r_out, z0, seg, phase)
             + ring_pts(cu, cv, r_out, z1, seg, phase)
             + ring_pts(cu, cv, r_in, z1, seg, phase)
             + ring_pts(cu, cv, r_in, z0, seg, phase))
    faces = []
    for k in range(4):
        a0, b0 = k * seg, ((k + 1) % 4) * seg
        for i in range(seg):
            j = (i + 1) % seg
            faces.append((a0 + i, b0 + i, b0 + j, a0 + j))
    return new_mesh(name, verts, faces, [mat])


# ------------------------------------------------------------------ the build


def buttress(name, cu, cv, ang, top, pin_top, mat, scale=1.0):
    """An engaged stepped pier with a pinnacle cap, projecting outward from a
    wall face along local angle `ang`. cu, cv is ON the wall face."""
    n = (math.cos(ang), math.sin(ang))
    w = 2.0 * scale
    steps = [(0.0, top * 0.45, 1.5 * scale), (top * 0.45, top * 0.75, 1.0 * scale),
             (top * 0.75, top, 0.6 * scale)]
    for i, (z0, z1, proj) in enumerate(steps):
        box(f"{name}_s{i}", cu + n[0] * (proj / 2 - 0.2), cv + n[1] * (proj / 2 - 0.2),
            z0, z1, *rot_dims(w, proj + 0.2, ang), material("Toy_stone") if mat is None else mat,
            yaw=ang)
    p = 0.85 * scale
    pc_u = cu + n[0] * 0.15
    pc_v = cv + n[1] * 0.15
    box(f"{name}_pin", pc_u, pc_v, top - 0.2, pin_top - 1.1 * scale, p, p,
        material("Toy_stone"), yaw=ang)
    pyramid(f"{name}_cap", pc_u, pc_v, pin_top - 1.1 * scale, p * 1.18, pin_top,
            material("Toy_stone"), yaw=ang)


def rot_dims(w, d, ang):
    # box() with yaw=ang maps su along the projection direction, sv across it
    return (d, w)


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    stone = material("Toy_stone")
    trim = material("Toy_trim")
    glass = material("Toy_glass")
    ink = material("Toy_ink")
    gold = material("Toy_gold")
    verd = material("Toy_verdigris")
    roof = material("Toy_roofc")
    roofa = material("Toy_rust")
    wglow = material("Toy_white_Glow")
    gglow = material("Toy_gold_Glow")
    lit = material("Toy_mustard_Glow")     # warm interior light in the windows

    # ---------------------------------------------------------------- masses
    nave = box("nave_core", (NAVE_U0 + NAVE_U1 + 0.6) / 2, (CORE_V0 + CORE_V1) / 2,
               0, CLER_TOP, NAVE_U1 - NAVE_U0 + 0.6, CORE_V1 - CORE_V0, stone)
    bevel(nave)
    for nm, v0, v1 in (("aisle_n", AISLE_VN0, AISLE_VN1), ("aisle_s", AISLE_VS0, AISLE_VS1)):
        a = box(nm, (NAVE_U0 + NAVE_U1) / 2, (v0 + v1) / 2, 0, AISLE_PAR - 0.9,
                NAVE_U1 - NAVE_U0, v1 - v0, stone)
        bevel(a)
    # aisle parapets + trim coping on the outer edges
    for nm, ve, sgn in (("par_n", AISLE_VN1, 1), ("par_s", AISLE_VS0, -1)):
        box(nm, (NAVE_U0 + NAVE_U1) / 2, ve - sgn * 0.22, 0.0, AISLE_PAR - 0.25,
            NAVE_U1 - NAVE_U0, 0.44, stone)
        box(nm + "_cap", (NAVE_U0 + NAVE_U1) / 2, ve - sgn * 0.22, AISLE_PAR - 0.25,
            AISLE_PAR, NAVE_U1 - NAVE_U0, 0.62, trim)
    # Aisle lean-to roofs, in the darker roof value: from the app's downward
    # camera they read as a deliberate step in tone against the big copper nave
    # roof, instead of the whole roofscape being one uniform brown slab.
    for nm, v_out, v_in in (("aisle_roof_n", AISLE_VN1 - 0.45, CORE_V1),
                            ("aisle_roof_s", AISLE_VS0 + 0.45, CORE_V0)):
        extrude_outline(nm, [(v_out, AISLE_PAR - 1.0), (v_in, AISLE_PAR - 1.0),
                             (v_in, 20.4)][::(1 if v_out < v_in else -1)],
                        (NAVE_U1, 0.0), 0.0, NAVE_U1 - NAVE_U0, roofa)

    # transept arms + crossing core
    for nm, v0, v1 in (("transept_n", CORE_V1, TRAN_VN), ("transept_s", TRAN_VS, CORE_V0)):
        t = box(nm, (TRAN_U0 + TRAN_U1) / 2, (v0 + v1) / 2, 0, CLER_TOP - 0.5,
                TRAN_U1 - TRAN_U0, v1 - v0, stone)
        bevel(t)
    # Crossing: its lid stops BELOW the roof eaves and is capped in copper, so
    # the valleys where the nave and transept slopes meet read as flashed roof
    # instead of a pale stone slab poking through from the aerial camera.
    box("crossing", (TRAN_U0 + TRAN_U1) / 2, (CORE_V0 + CORE_V1) / 2, 0, EAVE - 0.5,
        TRAN_U1 - TRAN_U0, CORE_V1 - CORE_V0, stone)
    box("crossing_deck", (TRAN_U0 + TRAN_U1) / 2, (CORE_V0 + CORE_V1) / 2,
        EAVE - 0.5, EAVE - 0.1, TRAN_U1 - TRAN_U0 + 1.2, CORE_V1 - CORE_V0 + 1.2, roof)

    # choir + apse
    ch = box("choir", (CHOIR_U0 + CHOIR_U1) / 2, (CHOIR_V0 + CHOIR_V1) / 2, 0,
             CHOIR_EAVE + 0.2, CHOIR_U1 - CHOIR_U0, CHOIR_V1 - CHOIR_V0, stone)
    bevel(ch)
    apse_angles = [math.radians(a) for a in (90, 126, 162, 198, 234, 270)]
    sect = [(APSE_C[0] + APSE_R * math.cos(a), APSE_C[1] + APSE_R * math.sin(a))
            for a in apse_angles]
    sect += [(CHOIR_U0 + 0.4, APSE_C[1] - APSE_R), (CHOIR_U0 + 0.4, APSE_C[1] + APSE_R)]
    verts = [(u, v, 0.0) for u, v in sect] + [(u, v, APSE_WALL) for u, v in sect]
    k = len(sect)
    faces = [tuple(range(k)), tuple(range(2 * k - 1, k - 1, -1))]
    for i in range(k):
        j = (i + 1) % k
        faces.append((i, j, k + j, k + i))
    new_mesh("apse", verts, faces, [stone])
    # apse faceted half-cone roof, apex buried in the choir mass
    ring = [(APSE_C[0] + (APSE_R + 0.4) * math.cos(a),
             APSE_C[1] + (APSE_R + 0.4) * math.sin(a), APSE_WALL - 0.2)
            for a in apse_angles]
    ring += [(CHOIR_U0 + 0.5, APSE_C[1] - APSE_R - 0.4, APSE_WALL - 0.2),
             (CHOIR_U0 + 0.5, APSE_C[1] + APSE_R + 0.4, APSE_WALL - 0.2)]
    apex = (CHOIR_U0 + 0.9, AXIS_V, 26.5)
    verts = ring + [apex]
    k = len(ring)
    faces = [tuple(range(k))]
    for i in range(k):
        faces.append((i, (i + 1) % k, k))
    new_mesh("apse_roof", verts, faces, [roof])

    # ------------------------------------------------------------- big roofs
    extrude_outline("nave_roof", [(-7.65, EAVE), (7.65, EAVE), (0.0, RIDGE)],
                    (44.9, AXIS_V), 0.0, 44.9 - (-13.25), roof)
    extrude_outline("transept_roof_n", [(-7.35, EAVE), (7.35, EAVE), (0.0, RIDGE)],
                    (-13.25, TRAN_VN - 0.5), math.radians(90), TRAN_VN - 0.5 - AXIS_V, roof)
    extrude_outline("transept_roof_s", [(-7.35, EAVE), (7.35, EAVE), (0.0, RIDGE)],
                    (-13.25, TRAN_VS + 0.5), math.radians(270), AXIS_V - (TRAN_VS + 0.5), roof)
    extrude_outline("choir_roof", [(-8.9, CHOIR_EAVE), (8.9, CHOIR_EAVE), (0.0, CHOIR_RIDGE)],
                    (-14.5, AXIS_V), 0.0, -14.5 - (CHOIR_U0 - 0.5), roof)

    # Verdigris ridge cresting: real copper roofs are capped at the ridge, and
    # from above these lines are what give the roofscape its drawing - a clear
    # cruciform of ridges tying every slope to the fleche (style bible s.10).
    box("crest_nave", (44.9 + TRAN_U0) / 2, AXIS_V, RIDGE - 0.22, RIDGE + 0.26,
        44.9 - TRAN_U0, 0.62, verd)
    box("crest_transept", -13.25, (TRAN_VS + TRAN_VN) / 2, RIDGE - 0.22, RIDGE + 0.26,
        0.62, TRAN_VN - TRAN_VS - 1.0, verd)
    box("crest_choir", (CHOIR_U0 - 0.5 + -14.5) / 2, AXIS_V, CHOIR_RIDGE - 0.22,
        CHOIR_RIDGE + 0.26, -14.5 - (CHOIR_U0 - 0.5), 0.55, verd)

    # gable end walls (stone pentagons with coping above the roof planes)
    for nm, v_end, sgn in (("tr_gable_n", TRAN_VN, 1), ("tr_gable_s", TRAN_VS, -1)):
        extrude_outline(nm, [(-6.55, CLER_TOP - 0.5), (6.55, CLER_TOP - 0.5),
                             (6.55, EAVE + 0.4), (0.0, RIDGE + 0.5), (-6.55, EAVE + 0.4)],
                        (-13.25, v_end), math.radians(90 if sgn > 0 else 270), 0.9, stone)
    extrude_outline("choir_gable_w", [(-8.9, APSE_WALL - 0.4), (8.9, APSE_WALL - 0.4),
                                      (8.9, CHOIR_EAVE + 0.3), (0.0, CHOIR_RIDGE + 0.5),
                                      (-8.9, CHOIR_EAVE + 0.3)],
                    (CHOIR_U0, AXIS_V), math.radians(180), 0.7, stone)

    # ------------------------------------------------- facade block + towers
    TW = 10.0                                    # tower width across v
    tower_vs = [(AISLE_VN1 - TW, AISLE_VN1), (AISLE_VS0, AISLE_VS0 + TW)]
    CB_V0, CB_V1 = AISLE_VS0 + TW, AISLE_VN1 - TW          # centre bay -2.0 .. 4.7
    # centre bay wall, slightly recessed, rising to the nave gable
    box("facade_bay", (FAC_U0 + FAC_U1 - 0.5) / 2, (CB_V0 + CB_V1) / 2, 0, CLER_TOP + 1.0,
        FAC_U1 - FAC_U0 - 0.5, CB_V1 - CB_V0, stone)
    extrude_outline("facade_gable", [(-(CB_V1 - CB_V0) / 2, CLER_TOP + 1.0),
                                     ((CB_V1 - CB_V0) / 2, CLER_TOP + 1.0),
                                     ((CB_V1 - CB_V0) / 2, 35.6), (0.0, RIDGE + 0.4),
                                     (-(CB_V1 - CB_V0) / 2, 35.6)],
                    (FAC_U1 - 0.5, AXIS_V), 0.0, 2.4, stone)
    for ti, (v0, v1) in enumerate(tower_vs):
        cv = (v0 + v1) / 2
        t = box(f"tower_{ti}", (FAC_U0 + FAC_U1) / 2, cv, 0, TOWER_TOP - 3.85,
                FAC_U1 - FAC_U0, v1 - v0, stone)
        bevel(t)
        # crown parapet + trim coping, with the pierced slots the photos show
        for e_ang, e_u, e_v, sl in (
            (0.0, FAC_U1, cv, TW), (math.pi, FAC_U0, cv, TW),
            (math.pi / 2, (FAC_U0 + FAC_U1) / 2, v1, FAC_U1 - FAC_U0),
            (-math.pi / 2, (FAC_U0 + FAC_U1) / 2, v0, FAC_U1 - FAC_U0),
        ):
            n = (math.cos(e_ang), math.sin(e_ang))
            t_ = (-math.sin(e_ang), math.cos(e_ang))
            deg = round(math.degrees(e_ang))
            box(f"tw{ti}_par_{deg}", e_u - n[0] * 0.3, e_v - n[1] * 0.3,
                TOWER_TOP - 3.6, TOWER_TOP - 1.9,
                *((0.6, sl) if abs(n[0]) > 0.5 else (sl, 0.6)), stone)
            box(f"tw{ti}_cap_{deg}", e_u - n[0] * 0.3, e_v - n[1] * 0.3,
                TOWER_TOP - 1.9, TOWER_TOP - 1.55,
                *((0.85, sl) if abs(n[0]) > 0.5 else (sl, 0.85)), trim)
            for si in range(5):
                so = (si - 2) * (sl - 3.4) / 4
                box(f"tw{ti}_parslot_{deg}_{si}", e_u - n[0] * 0.18 + t_[0] * so,
                    e_v - n[1] * 0.18 + t_[1] * so, TOWER_TOP - 3.2, TOWER_TOP - 2.1,
                    *((0.3, 0.34) if abs(n[0]) > 0.5 else (0.34, 0.3)), ink)
        # designed crown deck: copper roof inset inside the parapet + the stair
        # penthouse (the app's camera looks down on this - style bible s.10)
        box(f"tw{ti}_deck", (FAC_U0 + FAC_U1) / 2, cv, TOWER_TOP - 3.9,
            TOWER_TOP - 3.5, FAC_U1 - FAC_U0 - 1.2, TW - 1.2, roof)
        box(f"tw{ti}_house", (FAC_U0 + FAC_U1) / 2 - 1.6, cv, TOWER_TOP - 3.5,
            TOWER_TOP - 1.6, 2.6, 2.2, stone)
        box(f"tw{ti}_house_cap", (FAC_U0 + FAC_U1) / 2 - 1.6, cv, TOWER_TOP - 1.6,
            TOWER_TOP - 1.35, 3.0, 2.6, trim)
        box(f"tw{ti}_vent", (FAC_U0 + FAC_U1) / 2 + 2.2, cv + 1.6, TOWER_TOP - 3.5,
            TOWER_TOP - 2.6, 1.4, 1.4, roof)
        # corner buttresses (stepped) + crown turrets
        for cu_, cv_ in ((FAC_U0, v0), (FAC_U0, v1), (FAC_U1, v0), (FAC_U1, v1)):
            su = 1 if cu_ == FAC_U0 else -1
            sv = 1 if cv_ == v0 else -1
            for i, (z0, z1, w) in enumerate(((0, 18, 2.3), (18, 33, 1.9), (33, 45, 1.5))):
                box(f"tw{ti}_cb{i}_{round(cu_)}_{round(cv_)}",
                    cu_ + su * (w / 2 - 0.55), cv_ + sv * (w / 2 - 0.55),
                    z0, z1, w, w, stone)
            cyl(f"tw{ti}_tur_{round(cu_)}_{round(cv_)}",
                cu_ + su * 0.62, cv_ + sv * 0.62, 0.95, 44.0, TOWER_TOP - 1.7,
                stone, seg=8)
            hring(f"tw{ti}_turband_{round(cu_)}_{round(cv_)}",
                  cu_ + su * 0.62, cv_ + sv * 0.62, 0.9, 1.12, TOWER_TOP - 1.9,
                  TOWER_TOP - 1.55, trim, seg=8)
            cone(f"tw{ti}_turcap_{round(cu_)}_{round(cv_)}",
                 cu_ + su * 0.62, cv_ + sv * 0.62, 1.05, 0.10, TOWER_TOP - 1.55,
                 TOWER_TOP, stone, seg=8)
        # belfry: trim frame + two deep pointed openings per face
        for f_ang, fu, fv in ((0.0, FAC_U1, cv), (math.pi, FAC_U0, cv),
                              (math.pi / 2, (FAC_U0 + FAC_U1) / 2, v1),
                              (-math.pi / 2, (FAC_U0 + FAC_U1) / 2, v0)):
            n = (math.cos(f_ang), math.sin(f_ang))
            t_ = (-math.sin(f_ang), math.cos(f_ang))
            lancet(f"tw{ti}_belfrytrim_{round(math.degrees(f_ang))}", (fu, fv), f_ang,
                   6.0, 33.8, 48.0, 0.10, 0.5, trim)
            for so in (-1.55, 1.55):
                lancet(f"tw{ti}_belfry_{round(math.degrees(f_ang))}_{so}",
                       (fu + t_[0] * so, fv + t_[1] * so), f_ang,
                       2.05, 35.0, 46.6, 0.22, 0.6, ink)
        # mid-stage paired glass lancets on the east + outer faces
        outer_ang = math.pi / 2 if ti == 0 else -math.pi / 2
        ov = v1 if ti == 0 else v0
        for f_ang, fu, fv in ((0.0, FAC_U1, cv),
                              (outer_ang, (FAC_U0 + FAC_U1) / 2, ov)):
            t_ = (-math.sin(f_ang), math.cos(f_ang))
            for so in (-1.2, 1.2):
                lit_lancet(f"tw{ti}_mid_{round(math.degrees(f_ang))}_{so}",
                           (fu + t_[0] * so, fv + t_[1] * so), f_ang,
                           1.5, 22.5, 29.5, 0.07, 0.4, glass, lit)
        # small side door at the tower base, east face
        lancet(f"tw{ti}_doortrim", (FAC_U1, cv), 0.0, 2.6, ENTRY - 0.3, 11.0, 0.06, 0.4, trim)
        lancet(f"tw{ti}_door", (FAC_U1, cv), 0.0, 1.6, ENTRY, 9.6, 0.14, 0.4, ink)

    # facade string course at the aisle-parapet line, standing proud
    box("facade_course", (FAC_U0 + FAC_U1) / 2, (AISLE_VS0 + AISLE_VN1) / 2,
        17.4, 17.95, FAC_U1 - FAC_U0 + 0.5, AISLE_VN1 - AISLE_VS0 + 0.5, trim)

    # ------------------------------------------------------- the entrance set
    # porch (projecting central portal)
    porch = box("porch", (FAC_U1 + 47.7) / 2, AXIS_V, 0, 14.8, 47.7 - FAC_U1,
                8.0, stone)
    bevel(porch)
    extrude_outline("porch_gable", [(-4.0, 14.8), (4.0, 14.8), (0.0, 17.6)],
                    (47.7, AXIS_V), 0.0, 47.7 - FAC_U1, stone)
    # flanking pinnacled piers
    for sv in (-1, 1):
        pv = AXIS_V + sv * 4.6
        box(f"porch_pier_{sv}", 47.2, pv, 0, 16.2, 1.5, 1.5, stone)
        pyramid(f"porch_pier_cap_{sv}", 47.2, pv, 16.2, 1.75, 18.4, stone)
    # portal: trim surround > ink reveal > gold doors > glow tympanum
    lancet("portal_trim", (47.7, AXIS_V), 0.0, 7.2, ENTRY - 0.4, 16.2, 0.12, 0.5, trim)
    lancet("portal_ink", (47.7, AXIS_V), 0.0, 5.6, ENTRY - 0.1, 14.4, 0.24, 0.5, ink)
    box("portal_doors", 47.7 + 0.34, AXIS_V, ENTRY, 10.9, 0.16, 3.5, gold)
    lancet("portal_tympanum", (47.7 + 0.30, AXIS_V), 0.0, 3.2, 11.2, 13.8, 0.02, 0.14, gglow)

    # Rose window: opaque dark glazing proud of the wall, a thin Toy_white_Glow
    # tracery ring 4 cm in front of it (the app draws _Glow as an unlit overlay
    # at 12% opacity by day, so a glow surface must never BE the primary
    # surface - it rides on top of the glass and the trim spokes silhouette
    # over it), then the ring + 12 chunky spokes + hub (the documented Chartres
    # 12-fold scheme, REFERENCE.md).
    RC_U, RC_Z, RR = FAC_U1 - 0.5, 27.5, 3.8            # wall face u, centre z, radius
    vdisc("rose_glass", (RC_U + 0.22, AXIS_V), 0.0, RC_Z, 3.6, 0.50, glass)
    # glow = thin tracery rings, not a disc: at the app's 12% day opacity a
    # full disc would haze the whole window, while rings read as lit tracery
    vring("rose_glow_outer", (RC_U + 0.27, AXIS_V), 0.0, RC_Z, 3.02, 3.34, 0.06,
          wglow, seg=24)
    vring("rose_glow_inner", (RC_U + 0.27, AXIS_V), 0.0, RC_Z, 1.72, 1.98, 0.06,
          wglow, seg=20)
    vdisc("rose_glow_hub", (RC_U + 0.27, AXIS_V), 0.0, RC_Z, 0.60, 0.06, wglow, seg=12)
    vring("rose_ring", (RC_U + 0.62, AXIS_V), 0.0, RC_Z, 3.42, RR + 0.55, 0.62, trim, seg=28)
    for i in range(12):
        a = math.pi * 2 * i / 12
        c, s = math.cos(a), math.sin(a)
        L, hw = 3.35, 0.15
        outline = [(0.62 * c - hw * -s, RC_Z + 0.62 * s - hw * c),
                   (L * c - hw * -s, RC_Z + L * s - hw * c),
                   (L * c + hw * -s, RC_Z + L * s + hw * c),
                   (0.62 * c + hw * -s, RC_Z + 0.62 * s + hw * c)]
        extrude_outline(f"rose_spoke_{i}", outline, (RC_U + 0.55, AXIS_V), 0.0, 0.42, trim)
    vdisc("rose_hub", (RC_U + 0.60, AXIS_V), 0.0, RC_Z, 0.75, 0.50, trim, seg=16)

    # open arcade gallery band between the towers, above the rose
    box("arcade_band", FAC_U1 - 0.45, AXIS_V, 32.6, 35.4, 0.5, CB_V1 - CB_V0 + 0.2, trim)
    for i in range(9):
        sv = AXIS_V + (i - 4) * 0.68
        lancet(f"arcade_slot_{i}", (FAC_U1 - 0.24, sv), 0.0, 0.44, 33.0, 35.0, 0.30, 0.55, ink)

    # ------------------------------------------------------------ the steps
    STEP_V0, STEP_V1 = AXIS_V - 12.0, AXIS_V + 12.0
    box("terrace", (47.7 + 50.7) / 2, AXIS_V, 0, ENTRY, 3.0, STEP_V1 - STEP_V0, stone)
    rise = ENTRY / 8
    for i in range(4):                                   # upper flight
        u0 = 50.7 + i * 0.95
        box(f"step_a{i}", u0 + 0.475, AXIS_V, 0, ENTRY - rise * (i + 1),
            0.95, STEP_V1 - STEP_V0, stone)
    box("step_landing", (54.5 + 56.1) / 2, AXIS_V, 0, ENTRY - rise * 4,
        1.6, STEP_V1 - STEP_V0, stone)
    for i in range(3):                                   # lower flight
        u0 = 56.1 + i * 0.95
        box(f"step_b{i}", u0 + 0.475, AXIS_V, 0, ENTRY - rise * (5 + i),
            0.95, STEP_V1 - STEP_V0, stone)
    for sv, ve in ((1, STEP_V1), (-1, STEP_V0)):         # cheek walls
        box(f"cheek_hi_{sv}", (50.7 + 55.3) / 2, ve + sv * 0.45, 0, ENTRY + 0.4,
            55.3 - 50.7, 0.9, stone)
        box(f"cheek_lo_{sv}", (55.3 + 59.0) / 2, ve + sv * 0.45, 0, ENTRY - rise * 4 + 0.4,
            59.0 - 55.3, 0.9, stone)

    # ------------------------------------------------- flank window rhythms
    for k in range(BAYS):
        cu_ = NAVE_U0 + BAY_W * (k + 0.5)
        lit_lancet(f"aisle_win_n_{k}", (cu_, AISLE_VN1), math.pi / 2, 2.1, 8.6, 15.9,
                   0.07, 0.5, glass, lit)
        lit_lancet(f"aisle_win_s_{k}", (cu_, AISLE_VS0), -math.pi / 2, 2.1, 8.6, 15.9,
                   0.07, 0.5, glass, lit)
        lit_lancet(f"cler_win_n_{k}", (cu_, CORE_V1), math.pi / 2, 2.3, 24.4, 30.6,
                   0.07, 0.5, glass, lit)
        lit_lancet(f"cler_win_s_{k}", (cu_, CORE_V0), -math.pi / 2, 2.3, 24.4, 30.6,
                   0.07, 0.5, glass, lit)
    # engaged buttresses at the bay lines (both flanks)
    for k in range(BAYS + 1):
        cu_ = NAVE_U0 + BAY_W * k
        buttress(f"but_n_{k}", cu_, AISLE_VN1, math.pi / 2, 20.5, 24.2, None)
        buttress(f"but_s_{k}", cu_, AISLE_VS0, -math.pi / 2, 20.5, 24.2, None)

    # transept ends: great window + corner buttresses
    for nm, v_end, f_ang in (("tr_n", TRAN_VN, math.pi / 2), ("tr_s", TRAN_VS, -math.pi / 2)):
        lancet(f"{nm}_wintrim", (-13.25, v_end), f_ang, 6.6, 12.0, 28.0, 0.08, 0.6, trim)
        lit_lancet(f"{nm}_win", (-13.25, v_end), f_ang, 5.2, 12.6, 26.4, 0.18, 0.6,
                   glass, lit)
        lancet(f"{nm}_door", (-13.25, v_end), f_ang, 2.2, 0.2, 5.0, 0.24, 0.5, ink)
        for cu_ in (TRAN_U0, TRAN_U1):
            su = 1 if cu_ == TRAN_U0 else -1
            buttress(f"{nm}_cb_{round(cu_)}", cu_ + su * 1.0, v_end, f_ang, 26.0, 30.0,
                     None, scale=1.15)
        # The arm's east and west faces rise clear above the aisle roofs and
        # the app's aerial camera looks straight at them - they get the same
        # bay rhythm as the flanks rather than reading as blank slabs.
        v_in = CORE_V1 if v_end > 0 else CORE_V0
        for f2, fu in ((0.0, TRAN_U1), (math.pi, TRAN_U0)):
            box(f"{nm}_course_{round(fu)}", fu, (v_in + v_end) / 2, 20.5, 21.0,
                0.5, abs(v_end - v_in) - 0.8, trim)
            for j in (0.32, 0.68):
                vm = v_in + (v_end - v_in) * j
                lit_lancet(f"{nm}_up_{round(fu)}_{j}", (fu, vm), f2, 2.0, 22.8, 29.6,
                           0.07, 0.5, glass, lit)
                lit_lancet(f"{nm}_lo_{round(fu)}_{j}", (fu, vm), f2, 1.8, 9.0, 16.4,
                           0.07, 0.5, glass, lit)
            for j in (0.05, 1.0):
                vm = v_in + (v_end - v_in) * j
                buttress(f"{nm}_pier_{round(fu)}_{j}", fu, vm, f2, 24.0, 27.4, None, 0.8)

    # choir bays + apse facets
    for k in range(3):
        cu_ = CHOIR_U0 + 2.8 + k * 5.6
        lit_lancet(f"choir_win_n_{k}", (cu_, CHOIR_V1), math.pi / 2, 1.9, 12.0, 22.0,
                   0.07, 0.5, glass, lit)
        lit_lancet(f"choir_win_s_{k}", (cu_, CHOIR_V0), -math.pi / 2, 1.9, 12.0, 22.0,
                   0.07, 0.5, glass, lit)
    for k in range(4):
        cu_ = CHOIR_U0 + 5.6 * (k)
        if k:
            buttress(f"choir_but_n_{k}", cu_ - 2.8 + 2.8, CHOIR_V1, math.pi / 2, 18.5, 21.8, None, 0.9)
            buttress(f"choir_but_s_{k}", cu_ - 2.8 + 2.8, CHOIR_V0, -math.pi / 2, 18.5, 21.8, None, 0.9)
    facet_centers = [math.radians(a) for a in (108, 144, 180, 216, 252)]
    for i, a in enumerate(facet_centers):
        fu = APSE_C[0] + APSE_R * math.cos(a)
        fv = APSE_C[1] + APSE_R * math.sin(a)
        lit_lancet(f"apse_win_{i}", (fu, fv), a, 1.7, 9.5, 17.5, 0.07, 0.5, glass, lit)
    for i, a in enumerate([math.radians(x) for x in (126, 162, 198, 234)]):
        fu = APSE_C[0] + APSE_R * math.cos(a)
        fv = APSE_C[1] + APSE_R * math.sin(a)
        buttress(f"apse_but_{i}", fu, fv, a, 16.5, 20.0, None, 0.85)

    # ------------------------------------------------------------ the fleche
    FL_U, FL_V = -13.25, AXIS_V
    cyl("fleche_drum", FL_U, FL_V, 2.6, 37.0, 44.0, verd, seg=8, phase=math.pi / 8)
    hring("fleche_cornice", FL_U, FL_V, 2.35, 2.95, 44.0, 44.6, verd, seg=8, phase=math.pi / 8)
    for i in range(8):
        a = math.pi / 8 + i * math.pi / 4
        box(f"fleche_post_{i}", FL_U + 2.3 * math.cos(a), FL_V + 2.3 * math.sin(a),
            44.6, 47.9, 0.42, 0.42, verd, yaw=a)
    cyl("fleche_lantern_ink", FL_U, FL_V, 1.65, 44.6, 47.9, ink, seg=8, phase=math.pi / 8)
    hring("fleche_lantern_glow", FL_U, FL_V, 1.86, 2.0, 45.0, 47.6, gglow, seg=8,
          phase=math.pi / 8)
    cone("fleche_capring", FL_U, FL_V, 2.75, 2.1, 47.9, 48.6, verd, seg=8, phase=math.pi / 8)
    cone("fleche_needle", FL_U, FL_V, 2.05, 0.12, 48.6, 72.2, verd, seg=12)
    cyl("fleche_orb", FL_U, FL_V, 0.4, 72.2, 72.95, gold, seg=10)
    box("cross_post", FL_U, FL_V, 72.95, CROSS_TOP, 0.18, 0.18, gold)
    box("cross_arm_u", FL_U, FL_V, 74.15, 74.5, 1.45, 0.16, gold)
    box("cross_arm_v", FL_U, FL_V, 74.15, 74.5, 0.16, 1.45, gold)

    return scene


# ---------------------------------------------------------- centre and export


def recenter_and_report():
    dg = bpy.context.evaluated_depsgraph_get()
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    mn = Vector((1e12, 1e12, 1e12))
    mx = Vector((-1e12, -1e12, -1e12))
    tris = 0
    for o in objs:
        me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
        o.evaluated_get(dg).to_mesh_clear()
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, mn.z))
    for o in objs:
        for v in o.data.vertices:
            v.co.x -= center.x
            v.co.y -= center.y
            v.co.z -= center.z
    anchor_lon = BLON + center.x / KX
    anchor_lat = BLAT + center.y / KY
    dims = [round(mx[i] - mn[i], 3) for i in range(3)]
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] dims={dims}")
    print(f"[build] recentered by {[round(v, 3) for v in center]}")
    print(f"[build] ANCHOR lon/lat = {anchor_lon:.7f}, {anchor_lat:.7f}")
    print(f"[build] heading: long axis 81.03 deg cw from true north (authored world-true)")
    return tris, dims, (anchor_lon, anchor_lat)


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    recenter_and_report()

    blend = os.path.join(out, "grace-cathedral.blend")
    glb = os.path.join(out, "grace-cathedral.glb")
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
