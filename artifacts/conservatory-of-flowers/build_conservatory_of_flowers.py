"""Deterministic Blender build of the SF-SIM miniature Conservatory of Flowers.

    blender -b --python build_conservatory_of_flowers.py -- [--out DIR]

Writes conservatory-of-flowers.blend and conservatory-of-flowers.glb next to
this file (or into --out). Geometry is authored in world space in metres, Z up,
+X east, +Y north, origin at the dome axis (base centre), min Z = 0.

Design (see REFERENCE.md for the sources behind every number):

* the whole model is authored on local axes (u along the wings, v across) and
  yawed +9 deg so the long axis sits on its measured real-world bearing of
  81 deg cw from true north; the south vestibule then faces within 9 deg of -Y;
* a red-brick plinth extruded from a simplified E-plan outline - the raised
  masonry base the conservatory actually stands on;
* two elliptical-vault glass wings with a deliberately fat 1.6 m rib rhythm
  (thin ribs alias at city scale), white paneled knee walls, ridge ventilator
  monitors and Victorian cresting teeth;
* octagonal domed end pavilions with ogee cupolas + finials (the E-plan's
  outer teeth), stepping 4 m south of the wing face;
* the two-tier centre: octagonal drum with pilastered glass bays and a transom
  band, a ribbed skirt roof with three peaked dormers (S/E/W per the NRHP
  nomination), a gallery band, a lattice clerestory, the 16-rib great dome and
  a lantern + finial closing at exactly 18.3 m;
* the gabled south entrance vestibule with a projecting porch;
* a low rear lean-to service range along the north side of each wing;
* night cue: the app renders _Glow surfaces in a separate unlit layer whose
  opacity follows uNight (near-invisible by day), so the glazing itself stays
  opaque Toy_glassl and thin Toy_white_Glow shells ride 3-5 cm proud of the
  rotunda, lantern and end-pavilion domes - at night they ignite into warm
  lit glass with the white ribs silhouetted over them; a Toy_gold_Glow transom
  lights the entrance; the wings stay dark.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

YAW = math.radians(9.0)  # 90 - 81: measured long-axis bearing baked in

H_PLINTH = 1.2
H_KNEE = 3.0
H_WING_EAVE = 4.6
H_WING_RIDGE = 9.0
WING_HALF = 6.2  # wing half-depth (walls at v = +/-6.2)
WING_END_U = 26.5  # vault dies deep inside the end pavilions
WING_START_U = 9.3  # vault dies inside the drum
RIB_PITCH = 1.6
RIB_W = 0.36
RIB_OUT = 0.30

DRUM_R = 11.0  # central octagon circumradius (flats half = 10.16)
H_DRUM_EAVE = 8.35
SKIRT_TOP_R = 7.25  # octagon circumradius at skirt top (flats half = 6.7)
H_SKIRT_TOP = 11.4
CLER_R = 6.85  # clerestory octagon circumradius
H_CLER_TOP = 13.55
DOME_R = 6.9  # great dome base radius (overhangs the clerestory)
H_DOME_SPRING = 13.8
H_ARCH = 18.30  # finial tip - the published ~60 ft; loader scale 1.0

END_R = 8.9  # end pavilion octagon circumradius (flats half = 8.22)
END_U = 29.0  # end pavilion centres at u = +/-29.0
END_V = -2.0  # ... shifted south: the E-plan step
H_END_EAVE = 4.6
H_END_DOME = 10.8

VEST_HALF_W = 3.95
VEST_FRONT_V = -12.4
PORCH_FRONT_V = -14.0

LEAN_V0, LEAN_V1 = 6.2, 10.5  # rear lean-to range
H_LEAN_EAVE = 3.3
LEAN_U0, LEAN_U1 = 10.5, 21.0

OCT = [math.radians(22.5 + 45.0 * k) for k in range(8)]  # flat faces N/S/E/W

# Project palette from .agents/skills/sf-asset-check (hex, sRGB); authored as
# linear, which is what the shipped kit GLBs hold.
PALETTE_HEX = {
    "Toy_white": "f7f4ec",
    "Toy_trim": "f3efe6",
    "Toy_glassl": "6f95b8",
    "Toy_glass": "2a4d73",
    "Toy_brick": "c96f4a",
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


# -------------------------------------------------------------- mesh helpers


def yaw2(p):
    c, s = math.cos(YAW), math.sin(YAW)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def new_mesh(name, verts, faces, materials, face_mats=None):
    """Create an object; every vertex is yawed onto the real-world heading."""
    mesh = bpy.data.meshes.new(name)
    world = []
    for v in verts:
        x, y = yaw2((v[0], v[1]))
        world.append(Vector((x, y, v[2])))
    mesh.from_pydata(world, [], faces)
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


def box(name, cx, cy, z0, z1, sx, sy, mat, ang=0.0):
    hx, hy = sx / 2.0, sy / 2.0
    c, s = math.cos(ang), math.sin(ang)
    corners = [
        (cx + x * c - y * s, cy + x * s + y * c)
        for x, y in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy))
    ]
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


def gable(name, cx, cy, z0, z_eave, z_ridge, sx, sy, mat, ridge_axis="x"):
    """Box with a triangular gable top; ridge runs along ridge_axis."""
    hx, hy = sx / 2.0, sy / 2.0
    b = [
        (cx - hx, cy - hy),
        (cx + hx, cy - hy),
        (cx + hx, cy + hy),
        (cx - hx, cy + hy),
    ]
    verts = [(x, y, z0) for x, y in b] + [(x, y, z_eave) for x, y in b]
    if ridge_axis == "x":
        verts += [(cx - hx, cy, z_ridge), (cx + hx, cy, z_ridge)]
        faces = [
            (3, 2, 1, 0),
            (0, 1, 5, 4),
            (2, 3, 7, 6),
            (1, 2, 6, 5),
            (3, 0, 4, 7),
            (4, 5, 9, 8),
            (6, 7, 8, 9),
            (5, 6, 9),
            (7, 4, 8),
        ]
    else:
        verts += [(cx, cy - hy, z_ridge), (cx, cy + hy, z_ridge)]
        faces = [
            (3, 2, 1, 0),
            (0, 1, 5, 4),
            (2, 3, 7, 6),
            (1, 2, 6, 5),
            (3, 0, 4, 7),
            (4, 5, 8),
            (6, 7, 9),
            (5, 6, 9, 8),
            (7, 4, 8, 9),
        ]
    return new_mesh(name, verts, faces, [mat])


def pyramid(name, cx, cy, z0, h, sx, sy, mat):
    hx, hy = sx / 2.0, sy / 2.0
    verts = [
        (cx - hx, cy - hy, z0),
        (cx + hx, cy - hy, z0),
        (cx + hx, cy + hy, z0),
        (cx - hx, cy + hy, z0),
        (cx, cy, z0 + h),
    ]
    faces = [(3, 2, 1, 0), (0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4)]
    return new_mesh(name, verts, faces, [mat])


def extrude_polygon(name, pts, z0, z1, mat):
    n = len(pts)
    verts = [(x, y, z0) for x, y in pts] + [(x, y, z1) for x, y in pts]
    faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    return new_mesh(name, verts, faces, [mat])


def octagon_pts(r_circ, cx=0.0, cy=0.0, scale=1.0):
    return [
        (cx + r_circ * scale * math.cos(a), cy + r_circ * scale * math.sin(a))
        for a in OCT
    ]


def sweep(name, rings, materials, row_mats=None, cap_top=False):
    """Loft closed loops (list of point lists, equal length) into a shell."""
    n = len(rings[0][0])
    verts = []
    for loop, z in rings:
        verts.extend([(x, y, z) for x, y in loop])
    faces, fm = [], []
    for r in range(len(rings) - 1):
        for i in range(n):
            j = (i + 1) % n
            faces.append((r * n + i, r * n + j, (r + 1) * n + j, (r + 1) * n + i))
            fm.append(row_mats[r] if row_mats else 0)
    if cap_top:
        off = (len(rings) - 1) * n
        faces.append(tuple(range(off, off + n)))
        fm.append(row_mats[-1] if row_mats else 0)
    return new_mesh(name, verts, faces, materials, fm)


def disc(name, r, z, mat, seg=16, th=0.12):
    pts = circle_pts(r, seg=seg)
    verts = [(x, y, z - th) for x, y in pts] + [(x, y, z) for x, y in pts]
    faces = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i) for i in range(seg)]
    faces.append(tuple(range(seg - 1, -1, -1)))
    faces.append(tuple(range(seg, 2 * seg)))
    return new_mesh(name, verts, faces, [mat])


def ring_band(name, loop_fn, r_in, r_out, z0, z1, mat):
    """Closed overhanging band: bottom annulus, outer wall, top annulus."""
    rings = [
        (loop_fn(r_in), z0),
        (loop_fn(r_out), z0),
        (loop_fn(r_out), z1),
        (loop_fn(r_in), z1),
        (loop_fn(r_in), z0),
    ]
    return sweep(name, rings, [mat])


def circle_pts(r, cx=0.0, cy=0.0, seg=16, a0=0.0):
    return [
        (cx + r * math.cos(a0 + 2 * math.pi * i / seg),
         cy + r * math.sin(a0 + 2 * math.pi * i / seg))
        for i in range(seg)
    ]


def slab(name, quad, th, mat):
    """Thin closed prism from four corners; thickness th along the normal."""
    a, b, c, d = (Vector(p) for p in quad)
    n = (b - a).cross(d - a).normalized() * th
    verts = [tuple(p) for p in (a, b, c, d)] + [tuple(p + n) for p in (a, b, c, d)]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
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
        # Flagged for the app's night pass; emission off in the daylight asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    mat.blend_method = "OPAQUE"
    return mat


# ------------------------------------------------------------ wing profiles


def vault_profile(off=0.0, seg=12):
    """Half-elliptical wing vault cross-section in (v, z), south to north."""
    pts = []
    for i in range(seg + 1):
        t = math.pi * i / seg  # 0 = south eave, pi = north eave
        v = -WING_HALF * math.cos(t)
        z = H_WING_EAVE + (H_WING_RIDGE - H_WING_EAVE) * math.sin(t)
        if off:
            # offset along the outward ellipse normal in the (v, z) plane
            nv = -(H_WING_RIDGE - H_WING_EAVE) * math.cos(t)
            nz = WING_HALF * math.sin(t)
            m = math.hypot(nv, nz) or 1.0
            v += nv / m * off
            z += nz / m * off
        pts.append((v, z))
    # fixed anchor points buried inside the eave-wall glass seal the loft's
    # open boundary edge (rays could otherwise slip under the rib overhangs)
    return [(-WING_HALF, 4.40)] + pts + [(WING_HALF, 4.40)]


def wing_vault(name, u0, u1, glass, white):
    """Vault shell lofted along u with proud rib rows every RIB_PITCH."""
    prof0 = vault_profile(0.0)
    prof1 = vault_profile(RIB_OUT)
    rows = [(u0, prof0, 0)]  # (u, profile, material row after this ring)
    u = u0 + 1.2
    while u + RIB_PITCH < u1 - 0.6:
        ur = u + RIB_PITCH - RIB_W
        rows.append((ur, prof0, 0))
        rows.append((ur + 0.06, prof1, 1))
        rows.append((ur + RIB_W, prof1, 1))
        rows.append((ur + RIB_W + 0.06, prof0, 1))
        u = ur + RIB_W + 0.06
    rows.append((u1, prof0, 0))
    n = len(prof0)
    verts = []
    for uu, prof, _ in rows:
        verts.extend([(uu, v, z) for v, z in prof])
    faces, fm = [], []
    for r in range(len(rows) - 1):
        mat_i = rows[r + 1][2]
        for i in range(n - 1):
            faces.append((r * n + i, r * n + i + 1, (r + 1) * n + i + 1, (r + 1) * n + i))
            fm.append(mat_i)
    obj = new_mesh(name, verts, faces, [glass, white], fm)
    # end walls: thin closed prisms (deterministic outward normals)
    for tag, uu, inward in (("a", u0, 0.22), ("b", u1, -0.22)):
        prof = vault_profile(0.0)
        m = len(prof)
        vv = [(uu, v, z) for v, z in prof]
        vv += [(uu + inward, v, z) for v, z in prof]
        vv += [(uu, 0.0, H_WING_EAVE), (uu + inward, 0.0, H_WING_EAVE)]
        ff = [(i, i + 1, 2 * m) for i in range(m - 1)]  # outer fan
        ff += [(m + i + 1, m + i, 2 * m + 1) for i in range(m - 1)]  # inner fan
        ff += [(i + 1, i, m + i, m + i + 1) for i in range(m - 1)]  # arc rim
        ff += [(0, m, 2 * m + 1, 2 * m), (m - 1 + m, m - 1, 2 * m, 2 * m + 1)]
        new_mesh(f"{name}_end_{tag}", vv, ff, [glass])
    return obj


# --------------------------------------------------------------------- build


def dome_profile():
    """Great dome meridian in (r, z): domical, slight overhang, apex 17.15."""
    return [
        (DOME_R, H_DOME_SPRING),
        (6.80, 14.70),
        (6.42, 15.55),
        (5.65, 16.30),
        (4.50, 16.90),
        (3.05, 17.30),
        (1.70, 17.52),
        (0.85, 17.60),
    ]


def end_dome_profile():
    """End pavilion dome meridian (octagonal sweep scale factors on END_R)."""
    return [
        (1.00, H_END_EAVE + 0.22),
        (0.94, 6.6),
        (0.80, 8.4),
        (0.58, 9.8),
        (0.30, 10.6),
        (0.10, H_END_DOME),
    ]


def skirt_profile():
    """Skirt roof scale factors on DRUM_R and heights."""
    return [
        (1.000, H_DRUM_EAVE + 0.03),
        (0.940, 9.55),
        (0.840, 10.45),
        (0.730, 11.05),
        (SKIRT_TOP_R / DRUM_R, H_SKIRT_TOP),
    ]


def meridian_rib(name, profile, ang, width, out, mat, cx=0.0, cy=0.0, rmul=1.0):
    """A proud rib with real thickness following a (r, z) profile at ang."""
    ca, sa = math.cos(ang), math.sin(ang)
    tx, ty = -sa, ca  # tangential direction for rib width
    aI, aO, bO, bI = [], [], [], []
    for r, z in profile:
        ri = max(r * rmul - 0.05, 0.0)
        ro = r * rmul + out
        for line, rr, side in ((aI, ri, -1), (aO, ro, -1), (bO, ro, 1), (bI, ri, 1)):
            line.append(
                (
                    cx + ca * rr + tx * side * width / 2,
                    cy + sa * rr + ty * side * width / 2,
                    z,
                )
            )
    n = len(profile)
    verts = aI + aO + bO + bI
    faces = []
    for k in range(3):  # side A, top, side B
        base = k * n
        for i in range(n - 1):
            faces.append((base + i, base + i + 1, base + n + i + 1, base + n + i))
    obj = new_mesh(name, verts, faces, [mat])
    return obj


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    white = material("Toy_white")
    trim = material("Toy_trim")
    glassl = material("Toy_glassl")
    glass = material("Toy_glass")
    brick = material("Toy_brick")
    glow = material("Toy_white_Glow")
    gold_glow = material("Toy_gold_Glow")

    # --- plinth: the raised masonry base, simplified E-plan ----------------
    south_wing, south_end, south_vest = -7.0, -10.8, -14.6
    plinth_pts = [
        (-38.5, south_end), (-20.4, south_end), (-20.4, south_wing),
        (-11.55, south_wing), (-11.55, south_end), (-VEST_HALF_W - 0.55, south_end),
        (-VEST_HALF_W - 0.55, south_vest), (VEST_HALF_W + 0.55, south_vest),
        (VEST_HALF_W + 0.55, south_end), (11.55, south_end), (11.55, south_wing),
        (20.4, south_wing), (20.4, south_end), (38.5, south_end),
        (38.5, 7.0), (21.55, 7.0), (21.55, 11.05), (-21.55, 11.05),
        (-21.55, 7.0), (-38.5, 7.0),
    ]
    bevel(extrude_polygon("plinth", plinth_pts, 0.0, H_PLINTH, brick), 0.12)

    # --- wings: knee walls, glass walls, mullions, vaults -------------------
    for side, s in (("w", -1), ("e", 1)):
        u_in, u_out = 9.0, 26.0
        cu = s * (u_in + u_out) / 2
        length = u_out - u_in
        for vv, tag in ((-WING_HALF, "s"), (WING_HALF, "n")):
            bevel(box(f"wing_{side}_knee_{tag}", cu, vv, H_PLINTH, H_KNEE,
                      length, 0.55, white), 0.10)
            box(f"wing_{side}_glass_{tag}", cu, vv, H_KNEE - 0.05, H_WING_EAVE,
                length, 0.18, glassl)
            bevel(box(f"wing_{side}_eave_{tag}", cu, vv, H_WING_EAVE - 0.10,
                      H_WING_EAVE + 0.22, length, 0.62, white), 0.08)
            k = 0
            u = u_in + 1.30
            while u < u_out - 0.5:
                box(f"wing_{side}_mullion_{tag}_{k}", s * u, vv, H_KNEE - 0.05,
                    H_WING_EAVE, 0.34, 0.30, white)
                u += RIB_PITCH
                k += 1
        wing_vault(f"wing_{side}_vault", s * WING_START_U if s > 0 else s * WING_END_U,
                   s * WING_END_U if s > 0 else s * WING_START_U, glassl, white)

    # ridge ventilator monitors + cresting teeth on the wing ridges
    for s in (-1, 1):
        for k, um in enumerate((15.2, 19.8)):
            cu = s * um
            box(f"monitor_glass_{s}_{k}", cu, 0.0, H_WING_RIDGE - 0.25,
                H_WING_RIDGE + 0.42, 2.8, 1.05, glassl)
            bevel(box(f"monitor_cap_{s}_{k}", cu, 0.0, H_WING_RIDGE + 0.42,
                      H_WING_RIDGE + 0.66, 3.1, 1.3, white), 0.08)
        for k, ut in enumerate((11.2, 12.6, 17.5, 21.6, 22.6)):
            pyramid(f"crest_{s}_{k}", s * ut, 0.0, H_WING_RIDGE - 0.15, 0.62,
                    0.42, 0.34, trim)

    # --- end pavilions: knee ring, glass ring, dome, cupola, porch ---------
    for side, s in (("w", -1), ("e", 1)):
        cx = s * END_U
        knee = octagon_pts(END_R + 0.18, cx, END_V)
        sweep(f"end_{side}_knee", [(octagon_pts(END_R + 0.30, cx, END_V), H_PLINTH),
                                   (octagon_pts(END_R + 0.30, cx, END_V), H_KNEE)],
              [white], cap_top=True)
        sweep(f"end_{side}_glass", [(octagon_pts(END_R, cx, END_V), H_KNEE - 0.05),
                                    (octagon_pts(END_R, cx, END_V), H_END_EAVE)],
              [glassl], cap_top=True)
        # corner posts on the octagon vertices
        for i, a in enumerate(OCT):
            px = cx + (END_R + 0.10) * math.cos(a)
            py = END_V + (END_R + 0.10) * math.sin(a)
            box(f"end_{side}_post_{i}", px, py, H_PLINTH, H_END_EAVE + 0.05,
                0.42, 0.42, white, ang=a)
        bevel(ring_band(f"end_{side}_eavering",
                        lambda r: octagon_pts(r, cx, END_V), END_R - 0.10,
                        END_R + 0.34, H_END_EAVE - 0.06, H_END_EAVE + 0.26,
                        white), 0.07)
        # octagonal glass dome
        prof = end_dome_profile()
        rings = [(octagon_pts(END_R, cx, END_V, scale=f), z) for f, z in prof]
        sweep(f"end_{side}_dome", rings, [glassl], cap_top=True)
        # hip ribs on vertices + mid-face ribs
        for i in range(8):
            for da, w in ((0.0, 0.30), (math.radians(22.5), 0.26)):
                ang = OCT[i] + da
                rprof = [(END_R * f * (math.cos(math.radians(22.5)) if da else 1.0), z)
                         for f, z in prof]
                meridian_rib(f"end_{side}_rib_{i}_{int(da * 100)}", rprof, ang,
                             w, 0.10, white, cx, END_V)
        gshell = [(octagon_pts(END_R * f + 0.035, cx, END_V),
                   min(z + 0.005, 10.78) if f <= 0.11 else z + 0.005)
                  for f, z in prof]
        gshell[0] = (octagon_pts(END_R + 0.035, cx, END_V), 4.84)
        sweep(f"end_{side}_glow", gshell, [glow], cap_top=True)
        # ogee cupola + finial
        cup = [(1.30, H_END_DOME - 0.1), (1.18, 11.35), (0.82, 11.8),
               (0.38, 12.1), (0.16, 12.42)]
        sweep(f"end_{side}_cupola",
              [(circle_pts(r, cx, END_V, 12), z) for r, z in cup],
              [trim], cap_top=True)
        box(f"end_{side}_finial", cx, END_V, 12.42, 13.35, 0.14, 0.14, trim)
        pyramid(f"end_{side}_finial_tip", cx, END_V, 13.20, 0.30, 0.30, 0.30, trim)
        # cresting teeth around the dome eave ring
        for i, a in enumerate(OCT):
            px = cx + (END_R + 0.2) * math.cos(a)
            py = END_V + (END_R + 0.2) * math.sin(a)
            pyramid(f"end_{side}_crest_{i}", px, py, H_END_EAVE + 0.26, 0.5,
                    0.36, 0.36, trim)
        # secondary entrance porch on the outer face
        px = cx + s * (END_R * math.cos(math.radians(22.5)) + 0.55)
        gable(f"end_{side}_porch", px, END_V, H_PLINTH, 3.1, 4.1, 1.6, 3.4,
              white, ridge_axis="x")

    # --- central drum -------------------------------------------------------
    sweep("drum_knee", [(octagon_pts(DRUM_R + 0.22), H_PLINTH),
                        (octagon_pts(DRUM_R + 0.22), H_KNEE)], [white],
          cap_top=True)
    sweep("drum_glass", [(octagon_pts(DRUM_R), H_KNEE - 0.05),
                         (octagon_pts(DRUM_R), 7.55)], [glassl], cap_top=True)
    ring_band("drum_transom", octagon_pts, DRUM_R - 0.10, DRUM_R + 0.12, 7.55,
              H_DRUM_EAVE - 0.28, white)
    bevel(ring_band("drum_eave", octagon_pts, DRUM_R - 0.10, DRUM_R + 0.30,
                    H_DRUM_EAVE - 0.28, H_DRUM_EAVE + 0.05, white), 0.07)
    for i, a in enumerate(OCT):  # corner pilasters
        px = (DRUM_R + 0.10) * math.cos(a)
        py = (DRUM_R + 0.10) * math.sin(a)
        box(f"drum_post_{i}", px, py, H_PLINTH, H_DRUM_EAVE - 0.2, 0.5, 0.5,
            white, ang=a)
    for i in range(8):  # two mullions per face
        a0, a1 = OCT[i], OCT[(i + 1) % 8]
        for t in (0.36, 0.64):
            ax = math.cos(a0) + (math.cos(a1) - math.cos(a0)) * t
            ay = math.sin(a0) + (math.sin(a1) - math.sin(a0)) * t
            m = math.hypot(ax, ay)
            px, py = DRUM_R * ax / m, DRUM_R * ay / m
            box(f"drum_mullion_{i}_{int(t * 100)}", px, py, H_KNEE - 0.05, 7.55,
                0.30, 0.30, white, ang=math.atan2(ay, ax))

    # --- skirt roof + dormers + gallery -------------------------------------
    sk = skirt_profile()
    sweep("skirt", [(octagon_pts(DRUM_R, scale=f), z) for f, z in sk], [glassl])
    for i in range(8):
        for da, w in ((0.0, 0.34), (math.radians(22.5), 0.30)):
            ang = OCT[i] + da
            rprof = [(DRUM_R * f * (math.cos(math.radians(22.5)) if da else 1.0), z)
                     for f, z in sk]
            meridian_rib(f"skirt_rib_{i}_{int(da * 100)}", rprof, ang, w, 0.10,
                         white)
    # dormers on the south, east and west skirt faces (NRHP)
    for name, ang in (("s", -math.pi / 2), ("e", 0.0), ("w", math.pi)):
        r = DRUM_R * 0.74
        px, py = r * math.cos(ang), r * math.sin(ang)
        gable(f"dormer_{name}", px, py, 9.6, 10.75, 11.4, 2.3, 2.3, white,
              ridge_axis="x" if name in ("e", "w") else "y")
        box(f"dormer_{name}_glass",
            px + 1.24 * math.cos(ang), py + 1.24 * math.sin(ang), 9.85, 10.65,
            1.25 if name == "s" else 0.22, 0.22 if name == "s" else 1.25,
            glassl)
    disc("gallery_deck", SKIRT_TOP_R + 0.35, H_SKIRT_TOP + 0.06, white)
    bevel(ring_band("gallery", lambda r: circle_pts(r, seg=16),
                    SKIRT_TOP_R - 0.60, SKIRT_TOP_R + 0.55, H_SKIRT_TOP,
                    H_SKIRT_TOP + 0.62, white), 0.08)
    for i in range(12):  # gallery cresting
        a = 2 * math.pi * i / 12 + math.pi / 12
        px = (SKIRT_TOP_R + 0.45) * math.cos(a)
        py = (SKIRT_TOP_R + 0.45) * math.sin(a)
        pyramid(f"gallery_crest_{i}", px, py, H_SKIRT_TOP + 0.62, 0.45, 0.32,
                0.32, trim)

    # --- clerestory ----------------------------------------------------------
    sweep("cler_glass", [(octagon_pts(CLER_R), H_SKIRT_TOP + 0.45),
                         (octagon_pts(CLER_R), H_CLER_TOP)], [glassl],
          cap_top=True)
    # night shell: proud of the glass, behind the posts, edges buried in the
    # gallery band and cler_ring solids
    sweep("cler_glow", [(octagon_pts(CLER_R + 0.05), 11.95),
                        (octagon_pts(CLER_R + 0.05), 13.60)], [glow])
    for i, a in enumerate(OCT):
        px, py = (CLER_R + 0.06) * math.cos(a), (CLER_R + 0.06) * math.sin(a)
        box(f"cler_post_{i}", px, py, H_SKIRT_TOP + 0.45, H_CLER_TOP + 0.05,
            0.4, 0.4, white, ang=a)
    for i in range(8):
        a0, a1 = OCT[i], OCT[(i + 1) % 8]
        ax = (math.cos(a0) + math.cos(a1)) / 2
        ay = (math.sin(a0) + math.sin(a1)) / 2
        m = math.hypot(ax, ay)
        box(f"cler_mullion_{i}", CLER_R * ax / m, CLER_R * ay / m,
            H_SKIRT_TOP + 0.45, H_CLER_TOP, 0.26, 0.26, white,
            ang=math.atan2(ay, ax))
    bevel(ring_band("cler_ring", octagon_pts, CLER_R - 0.10, CLER_R + 0.28,
                    H_CLER_TOP, H_CLER_TOP + 0.25, white), 0.07)

    # --- the great dome ------------------------------------------------------
    disc("cler_deck", CLER_R + 0.32, H_CLER_TOP + 0.24, white)
    dp = dome_profile()
    sweep("dome_glass", [(circle_pts(r, seg=16), z) for r, z in dp], [glassl],
          cap_top=True)
    shell = [(6.94, 13.79)] + [(r + 0.035, z + 0.005) for r, z in dp[1:]]
    sweep("dome_glow", [(circle_pts(r, seg=16), z) for r, z in shell], [glow],
          cap_top=True)
    for i in range(16):
        ang = 2 * math.pi * i / 16 + math.pi / 16
        meridian_rib(f"dome_rib_{i}", dp, ang, 0.28, 0.12, white)
    for zr, rr in ((15.55, 6.42), (16.90, 4.50)):  # two horizontal rings
        sweep(f"dome_ring_{int(zr * 10)}",
              [(circle_pts(rr - 0.55, seg=16), zr - 0.11),
               (circle_pts(rr + 0.16, seg=16), zr - 0.11),
               (circle_pts(rr + 0.16, seg=16), zr + 0.11),
               (circle_pts(rr - 0.55, seg=16), zr + 0.11)], [white])
    # lantern + finial: closes at exactly H_ARCH
    sweep("lantern_glass", [(circle_pts(0.80, seg=12), 17.55),
                            (circle_pts(0.80, seg=12), 17.98)], [glassl],
          cap_top=True)
    sweep("lantern_glow", [(circle_pts(0.84, seg=12), 17.56),
                           (circle_pts(0.84, seg=12), 17.97)], [glow],
          cap_top=True)
    sweep("lantern_cap", [(circle_pts(0.94, seg=12), 17.98),
                          (circle_pts(0.52, seg=12), 18.12),
                          (circle_pts(0.15, seg=12), 18.20)], [trim],
          cap_top=True)
    bevel(ring_band("lantern_base", lambda r: circle_pts(r, seg=12), 0.60,
                    0.98, 17.42, 17.60, trim), 0.05)
    box("finial", 0.0, 0.0, 18.16, H_ARCH - 0.10, 0.12, 0.12, trim)
    pyramid("finial_ball", 0.0, 0.0, H_ARCH - 0.16, 0.16, 0.26, 0.26, trim)

    # --- south vestibule + porch --------------------------------------------
    gable("vest", 0.0, -11.2, H_PLINTH, 4.4, 6.9, VEST_HALF_W * 2, 2.5, glassl,
          ridge_axis="y")
    for sx in (-1, 1):  # white corner frames
        box(f"vest_frame_{sx}", sx * (VEST_HALF_W - 0.17), VEST_FRONT_V + 0.05,
            H_PLINTH, 4.4, 0.34, 0.34, white)
    bevel(box("vest_bargeboard", 0.0, VEST_FRONT_V - 0.06, 4.25, 4.75,
              VEST_HALF_W * 2 + 0.3, 0.24, white), 0.06)
    box("vest_gable_frame", 0.0, VEST_FRONT_V - 0.02, 4.75, 6.9, 0.9, 0.2, white)
    box("vest_door", 0.0, VEST_FRONT_V - 0.08, H_PLINTH, 3.6, 2.2, 0.18, glass)
    box("vest_transom_glow", 0.0, VEST_FRONT_V - 0.10, 3.66, 4.12, 2.4, 0.16,
        gold_glow)
    pyramid("vest_finial", 0.0, -11.2, 6.9, 0.6, 0.3, 0.3, trim)
    # projecting porch
    gable("porch", 0.0, -13.2, 3.6, 3.95, 5.15, 3.1, 1.8, white, ridge_axis="y")
    for sx in (-1, 1):
        box(f"porch_post_{sx}", sx * 1.3, PORCH_FRONT_V + 0.35, H_PLINTH, 3.7,
            0.30, 0.30, white)
    pyramid("porch_finial", 0.0, -13.2, 5.15, 0.45, 0.26, 0.26, trim)

    # --- rear lean-to service range -----------------------------------------
    for side, s in (("w", -1), ("e", 1)):
        u0, u1 = s * LEAN_U0, s * LEAN_U1
        lo, hi = min(u0, u1), max(u0, u1)
        cu, ln = (lo + hi) / 2, hi - lo
        bevel(box(f"lean_{side}_knee", cu, LEAN_V1 - 0.25, H_PLINTH, 2.0, ln,
                  0.5, white), 0.08)
        box(f"lean_{side}_glasswall", cu, LEAN_V1 - 0.25, 1.95, H_LEAN_EAVE, ln,
            0.16, glassl)
        # sloped glass roof (thin slab) with three white rafters
        slab(f"lean_{side}_roof",
             [(lo, LEAN_V1 - 0.15, H_LEAN_EAVE), (hi, LEAN_V1 - 0.15, H_LEAN_EAVE),
              (hi, 5.7, 5.45), (lo, 5.7, 5.45)], 0.14, glassl)
        for k, ur in enumerate((lo + 1.5, cu, hi - 1.5)):
            slab(f"lean_{side}_rafter_{k}",
                 [(ur - 0.15, LEAN_V1 - 0.15, H_LEAN_EAVE + 0.04),
                  (ur + 0.15, LEAN_V1 - 0.15, H_LEAN_EAVE + 0.04),
                  (ur + 0.15, 5.75, 5.52), (ur - 0.15, 5.75, 5.52)], 0.14, white)
        for tag, ue in (("in", lo if s > 0 else hi), ("out", hi if s > 0 else lo)):
            box(f"lean_{side}_end_{tag}", ue, (LEAN_V0 + LEAN_V1) / 2 - 0.1,
                H_PLINTH, H_LEAN_EAVE + 0.4, 0.3, LEAN_V1 - LEAN_V0 - 0.2, white)

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

    blend = os.path.join(out, "conservatory-of-flowers.blend")
    glb = os.path.join(out, "conservatory-of-flowers.glb")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    kwargs = dict(
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
    )
    try:
        bpy.ops.export_scene.gltf(**kwargs, export_image_format="NONE")
    except TypeError:
        bpy.ops.export_scene.gltf(**kwargs)
    print(f"[build] wrote {blend}")
    print(f"[build] wrote {glb}")


if __name__ == "__main__":
    main()
