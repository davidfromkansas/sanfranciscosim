"""Deterministic Blender build of the SF-SIM miniature Salesforce Tower.

    blender -b --python build_salesforce_tower.py -- [--out DIR]

Writes salesforce-tower.blend and salesforce-tower.glb next to this file (or
into --out). Geometry is authored directly in world space in metres, Z up,
+X east, +Y north, origin at the base centre, min Z = 0, so the export needs
no transforms applied after the fact.

Design (see REFERENCE.md for the sources behind every number):

* a slender rounded-square shaft, 55 m across the flats at grade, rotated onto
  the SoMa street grid, tapering gently and then hard in the top third;
* the facade's dominant grain is horizontal: every floor carries a projecting
  perforated sunshade at the spandrel, so the tower reads as fine light ribs
  over dark blue-grey glass. Here they are grouped (one rib per ~3 floors) so
  the rhythm survives the city camera instead of aliasing into mush;
* the hollow perforated topper above the 296 m roof, modelled as open hoops
  converging to a rounded tip at 326 m - the crown and the LED floors behind
  it are the only _Glow surfaces;
* a roof deck designed for the app's downward camera and glimpsed through the
  crown: walkway ring, plant blocks and the window-washing rig;
* a two-storey glazed lobby with a chunky canopy and the blue cloud sign.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

H_ARCH = 326.0  # architectural height, tip of the crown
H_ROOF = 296.0  # occupied roof / parapet level
H_LED = 270.0  # the upper six LED floors sit behind the perforated facade
H_LOBBY = 16.0  # two-storey glazed lobby
H_CANOPY = 1.8  # canopy slab

A_BASE = 27.5  # half-width across the flats at grade (55 m square)
TAPER = 0.20  # fraction of width lost between grade and roof
TAPER_POW = 1.35
F_BASE = 0.46  # corner radius as a fraction of half-width, at grade
F_ROOF = 0.72  # ... at the roof: the plan is nearly round up there

BAND_PITCH = 8.4  # sunshade rhythm: one modelled rib per ~2 real floors
BAND_H = 1.3  # rib face height
BAND_OUT = 0.55  # how far the rib stands proud of the glass line
GLASS_IN = -0.35  # glass sits just behind the structural line
YAW = math.radians(44.13)  # OSM footprint: flats run 45.9 / 135.9 degrees

SEG_FLAT = 5  # resolution of the rounded-square outline (n = 4*(5+7) = 48)
SEG_ARC = 7
CROWN_HOOPS = 6  # broad open hoops abstract the crown's perforated screen

# Project palette from .agents/skills/sf-asset-check (hex, sRGB). Materials are
# authored with the linear equivalents, which is what the shipped kit GLBs hold.
PALETTE_HEX = {
    "Toy_trim": "f3efe6",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_steel": "9aa0a6",
    "Toy_stone": "d9d2c2",
    "Toy_roofd": "45454a",
    "Toy_sky": "6db3d9",
    "Toy_white_Glow": "f7f4ec",
    "Toy_red_Glow": "c4453c",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- plan shapes


def rot2(p, ang):
    c, s = math.cos(ang), math.sin(ang)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def half_width(z):
    t = min(max(z / H_ROOF, 0.0), 1.0)
    return A_BASE * (1.0 - TAPER * t**TAPER_POW)


def corner_fraction(z):
    t = min(max(z / H_ROOF, 0.0), 1.0)
    return F_BASE + (F_ROOF - F_BASE) * t


def outline(z, offset=0.0):
    """High-resolution rounded-square plan at height z, yawed to the grid."""
    a = half_width(z) + offset
    r = min(corner_fraction(z) * half_width(z), a - 0.1)
    s = a - r
    pts = []
    for quad in range(4):
        base = quad * math.pi / 2
        for i in range(SEG_FLAT):
            u = -s + 2 * s * i / SEG_FLAT
            pts.append(rot2((a, u), base))
        for i in range(SEG_ARC):
            ang = (math.pi / 2) * i / SEG_ARC
            pts.append(rot2((s + r * math.cos(ang), s + r * math.sin(ang)), base))
    return [rot2(p, YAW) for p in pts]


def arc_sampler(loop):
    """Return f(u in [0,1)) -> (point, outward unit normal) around a closed loop."""
    n = len(loop)
    seg = []
    total = 0.0
    for i in range(n):
        j = (i + 1) % n
        d = math.dist(loop[i], loop[j])
        seg.append((total, d, i, j))
        total += d

    def f(u):
        target = (u % 1.0) * total
        for start, d, i, j in seg:
            if target <= start + d or (i == n - 1):
                t = (target - start) / d if d else 0.0
                p = (
                    loop[i][0] + (loop[j][0] - loop[i][0]) * t,
                    loop[i][1] + (loop[j][1] - loop[i][1]) * t,
                )
                tx = loop[j][0] - loop[i][0]
                ty = loop[j][1] - loop[i][1]
                m = math.hypot(tx, ty) or 1.0
                nrm = (ty / m, -tx / m)  # loop is CCW -> this points outward
                return p, nrm
        raise RuntimeError("unreachable")

    return f, total



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


def bevel(obj, width=0.15, segments=2):
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


def loft(name, rings, materials, row_mats=None, cap_top=False, cap_bottom=False):
    """Loft equal-length closed plan loops (list of (z, points)) into a tube.

    row_mats gives the material index of each horizontal strip, which is how
    the sunshade banding is produced: alternating glass and rib rows.
    """
    n = len(rings[0][1])
    verts = []
    for z, loop in rings:
        verts.extend([(x, y, z) for x, y in loop])
    faces, face_mats = [], []
    for r in range(len(rings) - 1):
        for i in range(n):
            j = (i + 1) % n
            faces.append((r * n + i, r * n + j, (r + 1) * n + j, (r + 1) * n + i))
            face_mats.append(row_mats[r] if row_mats else 0)
    if cap_bottom:
        faces.append(tuple(range(n - 1, -1, -1)))
        face_mats.append(0)
    if cap_top:
        off = (len(rings) - 1) * n
        faces.append(tuple(range(off, off + n)))
        face_mats.append(0)
    return new_mesh(name, verts, faces, materials, face_mats)


def ring_band(name, z0, z1, inner_off, outer_off, mat, scale0=1.0, scale1=1.0):
    """A closed band standing proud of the shaft: outer wall plus lip faces."""

    def sc(loop, s):
        return [(x * s, y * s) for x, y in loop] if s != 1.0 else loop

    lo_in = sc(outline(z0, inner_off), scale0)
    lo_out = sc(outline(z0, outer_off), scale0)
    hi_out = sc(outline(z1, outer_off), scale1)
    hi_in = sc(outline(z1, inner_off), scale1)
    n = len(lo_in)
    verts = []
    for loop, z in ((lo_in, z0), (lo_out, z0), (hi_out, z1), (hi_in, z1)):
        verts.extend([(x, y, z) for x, y in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * n, ((k + 1) % 4) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])


def disc(name, z, offset, mat, scale=1.0):
    loop = outline(z, offset)
    loop = [(x * scale, y * scale) for x, y in loop]
    verts = [(x, y, z) for x, y in loop]
    return new_mesh(name, verts, [tuple(range(len(loop)))], [mat])


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=YAW):
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


def cylinder(name, cx, cy, z0, z1, radius, mat, seg=10):
    verts = []
    for z in (z0, z1):
        for i in range(seg):
            a = 2 * math.pi * i / seg
            verts.append((cx + radius * math.cos(a), cy + radius * math.sin(a), z))
    faces = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i) for i in range(seg)]
    faces.append(tuple(range(seg - 1, -1, -1)))
    faces.append(tuple(range(seg, 2 * seg)))
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
        # Flagged for the app's night pass; emission is off in the daylight asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    mat.blend_method = "OPAQUE"
    return mat


# --------------------------------------------------------------------- build


def crown_scale(z):
    """Ogive profile of the topper: 1.0 at the roof, closing to a rounded tip."""
    t = min(max((z - H_LED) / (H_ARCH - H_LED), 0.0), 1.0)
    return max(0.0, 1.0 - t**2.5) ** 0.55


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    trim = material("Toy_trim")
    glass = material("Toy_glass")
    steel = material("Toy_steel")
    stone = material("Toy_stone")
    roofd = material("Toy_roofd")
    sky = material("Toy_sky")
    glow = material("Toy_white_Glow")
    red_glow = material("Toy_red_Glow")

    # --- shaft: glass shell ribbed by the horizontal sunshade rhythm -------
    # Each band contributes four rings (glass -> rib underside -> rib face ->
    # rib top -> back to glass), so the ribs are real relief, not painted on.
    z0 = H_LOBBY + H_CANOPY
    rings, rows = [], []
    z = z0
    rings.append((z, outline(z, GLASS_IN)))
    while z + BAND_PITCH < H_ROOF - 1.0:
        zb = z + BAND_PITCH - BAND_H
        led_here = zb >= H_LED
        rib = 2 if led_here else 0
        rings.append((zb, outline(zb, GLASS_IN)))
        rows.append(2 if led_here else 1)  # glass bay (lit at the top)
        rings.append((zb + 0.2, outline(zb + 0.2, BAND_OUT)))
        rows.append(rib)  # underside of the rib
        rings.append((zb + BAND_H, outline(zb + BAND_H, BAND_OUT)))
        rows.append(rib)  # rib face
        z = zb + BAND_H
        rings.append((z + 0.2, outline(z + 0.2, GLASS_IN)))
        rows.append(rib)  # top return
        z += 0.2
    rings.append((H_ROOF, outline(H_ROOF, GLASS_IN)))
    rows.append(2)
    loft("shaft", rings, [trim, glass, glow], rows)

    # --- lobby: recessed glass box, chunky piers and an overhanging canopy --
    lobby_rings = [
        (0.0, outline(0.0, -1.9)),
        (H_LOBBY, outline(H_LOBBY, -1.9)),
    ]
    loft("lobby_glass", lobby_rings, [glass], cap_bottom=True)
    ring_band("lobby_sill", 0.0, 1.4, -2.6, 0.35, stone)
    ring_band("canopy", H_LOBBY, H_LOBBY + H_CANOPY, -2.6, 2.4, trim)

    pier_loop = outline(H_LOBBY / 2, 0.0)
    fp, _ = arc_sampler(pier_loop)
    for i in range(8):
        p, nrm = fp((i + 0.5) / 8)
        bevel(
            box(
                f"pier_{i}",
                p[0] - nrm[0] * 0.4,
                p[1] - nrm[1] * 0.4,
                0.0,
                H_LOBBY,
                1.9,
                1.9,
                trim,
                yaw=math.atan2(nrm[1], nrm[0]),
            ),
            width=0.25,
        )

    # --- entrance and identity on the Mission Street (north-west) face -----
    p, nrm = fp(0.5 / 8 + 0.25)  # centre of the north-west flat
    ang = math.atan2(nrm[1], nrm[0])
    bevel(
        box("entrance", p[0] + nrm[0] * 1.0, p[1] + nrm[1] * 1.0, 0.0, 9.0, 14.0, 3.0,
            glass, yaw=ang),
        width=0.25,
    )
    bevel(
        box("entrance_canopy", p[0] + nrm[0] * 3.4, p[1] + nrm[1] * 3.4, 9.0, 10.0,
            17.0, 8.0, trim, yaw=ang),
        width=0.3,
    )
    # The blue cloud wordmark by the doors: the one-second identity cue at
    # ground level, semantically enlarged (style bible s.8 / s.9).
    sx, sy = p[0] + nrm[0] * 2.6, p[1] + nrm[1] * 2.6
    tx, ty = -nrm[1], nrm[0]
    for k, (dx, w, h) in enumerate(((-2.2, 3.2, 2.2), (0.3, 4.4, 3.0), (2.6, 2.6, 1.8))):
        bevel(
            box(f"sign_cloud_{k}", sx + tx * dx, sy + ty * dx, 10.6, 10.6 + h, w, 1.0,
                sky, yaw=ang),
            width=0.45,
        )

    # --- roof: designed for the app's downward camera -----------------------
    disc("roof_deck", H_ROOF - 0.6, -1.8, roofd)
    ring_band("parapet", H_ROOF - 2.4, H_ROOF, -1.9, -0.3, trim)
    for i, (dx, dy, sx2, sy2, h) in enumerate(
        [
            (-5.5, 4.5, 10.0, 6.5, 4.4),
            (5.5, 3.5, 7.0, 5.5, 3.2),
            (0.0, -6.0, 12.0, 5.0, 2.8),
            (-7.5, -3.5, 4.5, 4.5, 5.0),
        ]
    ):
        cx, cy = rot2((dx, dy), YAW)
        bevel(box(f"plant_{i}", cx, cy, H_ROOF - 0.6, H_ROOF - 0.6 + h, sx2, sy2, steel))
    ring_band("bmu_rail", H_ROOF - 0.6, H_ROOF - 0.1, -5.2, -4.2, steel)
    cx, cy = rot2((half_width(H_ROOF) * 0.42, -half_width(H_ROOF) * 0.34), YAW)
    bevel(box("bmu", cx, cy, H_ROOF - 0.1, H_ROOF + 1.9, 5.5, 2.2, steel))

    # --- crown: hollow perforated topper, open hoops closing to a tip ------
    # Broad hooped screens begin below the occupied roof, as the real tower's
    # upper LED floors sit behind the facade rather than below a separate cap.
    span = H_ARCH - H_LED
    for i in range(CROWN_HOOPS):
        zb = H_LED + span * i / CROWN_HOOPS
        zt = zb + span / CROWN_HOOPS * 0.42  # the gaps are the perforation
        ring_band(
            f"crown_hoop_{i}",
            zb,
            zt,
            GLASS_IN - 0.9,
            BAND_OUT,
            glow,
            scale0=crown_scale(zb),
            scale1=crown_scale(zt),
        )
    cylinder("mast", 0.0, 0.0, H_ROOF, H_ARCH - 1.0, 0.6, steel, seg=8)
    cylinder("beacon", 0.0, 0.0, H_ARCH - 1.0, H_ARCH, 0.9, red_glow, seg=8)

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

    blend = os.path.join(out, "salesforce-tower.blend")
    glb = os.path.join(out, "salesforce-tower.glb")
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
