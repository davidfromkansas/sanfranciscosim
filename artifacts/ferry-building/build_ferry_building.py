"""Deterministic Blender build of the SF-SIM miniature Ferry Building.

    blender -b --python build_ferry_building.py -- [--out DIR]

Writes ferry-building.blend and ferry-building.glb. Geometry is authored in
real-world metres with Blender +X east, +Y true north, +Z up. The measured OSM
heading is baked into every vertex; local -Y is the Market Street/west front.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# Verified dimensions and true-world orientation (see REFERENCE.md).
LENGTH = 201.0
WIDTH = 56.0
BODY_H = 15.0
ROOF_EAVE = 15.8
ROOF_RIDGE = 21.0
TOWER_H = 74.7
CLOCK_D = 6.7
YAW = math.radians(-53.6)  # local +X (long axis) points southeast, bearing 143.6°

PALETTE_HEX = {
    "Toy_sand": "ece4d4",
    "Toy_trim": "f3efe6",
    "Toy_ink": "3a3530",
    "Toy_glass": "2a4d73",
    "Toy_white_Glow": "f7f4ec",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_gold": "caa64a",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {name: srgb_to_linear(value) for name, value in PALETTE_HEX.items()}


def rot2(x, y):
    c, s = math.cos(YAW), math.sin(YAW)
    return x * c - y * s, x * s + y * c


def world(x, y, z):
    xx, yy = rot2(x, y)
    return (xx, yy, z)


def new_mesh(name, verts, faces, materials, face_mats=None, do_bevel=False, bevel_width=0.12, recalc=True):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(v) for v in verts], [], faces)
    for mat in materials:
        mesh.materials.append(mat)
    if face_mats:
        for poly, idx in zip(mesh.polygons, face_mats):
            poly.material_index = idx
    mesh.validate()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    if recalc:
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if do_bevel:
        bmesh.ops.bevel(
            bm,
            geom=list(bm.verts) + list(bm.edges),
            offset=bevel_width,
            segments=2,
            profile=0.5,
            affect="EDGES",
            clamp_overlap=True,
        )
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.shade_flat()
    return obj


def material(name):
    existing = bpy.data.materials.get(name)
    if existing:
        return existing
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
    mat.surface_render_method = "DITHERED"
    return mat


def box(name, cx, cy, z0, z1, sx, sy, mat, bevel=True, bevel_width=0.12):
    hx, hy = sx / 2, sy / 2
    pts = [(-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)]
    verts = [world(cx + x, cy + y, z0) for x, y in pts]
    verts += [world(cx + x, cy + y, z1) for x, y in pts]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat], do_bevel=bevel, bevel_width=bevel_width)


def cylinder(name, cx, cy, z0, z1, radius, mat, seg=12, bevel=False):
    verts = []
    for z in (z0, z1):
        for i in range(seg):
            a = 2 * math.pi * i / seg
            verts.append(world(cx + radius * math.cos(a), cy + radius * math.sin(a), z))
    faces = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i) for i in range(seg)]
    faces += [tuple(range(seg - 1, -1, -1)), tuple(range(seg, 2 * seg))]
    return new_mesh(name, verts, faces, [mat], do_bevel=bevel, bevel_width=0.08)


def hipped_roof(name, cx, cy, z_eave, z_ridge, sx, sy, mat):
    """Low hipped roof whose ridge runs along local X."""
    hx, hy = sx / 2, sy / 2
    ridge_half = max(0.0, hx - hy * 0.65)
    verts = [
        world(cx - hx, cy - hy, z_eave), world(cx + hx, cy - hy, z_eave),
        world(cx + hx, cy + hy, z_eave), world(cx - hx, cy + hy, z_eave),
        world(cx - ridge_half, cy, z_ridge), world(cx + ridge_half, cy, z_ridge),
    ]
    faces = [(0, 1, 5, 4), (1, 2, 5), (2, 3, 4, 5), (3, 0, 4), (3, 2, 1, 0)]
    return new_mesh(name, verts, faces, [mat], do_bevel=True, bevel_width=0.15)


def gable_prism(name, cx, cy, z0, wall_top, ridge_z, sx, sy, mat):
    """Short-axis end pavilion: roof ridge runs local Y."""
    hx, hy = sx / 2, sy / 2
    verts = [
        world(cx - hx, cy - hy, z0), world(cx + hx, cy - hy, z0),
        world(cx + hx, cy + hy, z0), world(cx - hx, cy + hy, z0),
        world(cx - hx, cy - hy, wall_top), world(cx + hx, cy - hy, wall_top),
        world(cx + hx, cy + hy, wall_top), world(cx - hx, cy + hy, wall_top),
        world(cx, cy - hy, ridge_z), world(cx, cy + hy, ridge_z),
    ]
    faces = [
        (3, 2, 1, 0), (0, 1, 5, 4), (2, 3, 7, 6),
        (0, 4, 8, 5, 1), (3, 2, 6, 9, 7),
        (4, 7, 9, 8), (5, 8, 9, 6),
    ]
    # Explicit winding is required here: automatic recalc chooses the inset
    # prism's interior because the ridge cuts the rectangular shell.
    faces = [tuple(reversed(face)) for face in faces]
    return new_mesh(name, verts, faces, [mat], recalc=False)


def arch_outline(width, spring, total_h, segments=8):
    """CCW local 2D outline, bottom-left first, with semicircular head."""
    r = width / 2
    base_top = total_h - r
    pts = [(-r, 0), (r, 0), (r, base_top)]
    for i in range(1, segments + 1):
        a = i * math.pi / segments
        pts.append((r * math.cos(a), base_top + r * math.sin(a)))
    pts.append((-r, 0))
    return pts[:-1]


def facade_arch(name, center_u, side, z0, width, height, depth, mat, horizontal_axis="x", segments=8):
    """Arch-shaped dark inset plane on a local X or Y facade."""
    pts = arch_outline(width, height - width / 2, height, segments)
    verts = []
    eps = 0.025
    if horizontal_axis == "x":
        y = side
        for u, z in pts:
            verts.append(world(center_u + u, y, z0 + z))
        # reverse winding for north/east-facing plane when needed
        faces = [tuple(range(len(verts))) if side < 0 else tuple(range(len(verts) - 1, -1, -1))]
    else:
        x = side
        for u, z in pts:
            verts.append(world(x, center_u + u, z0 + z))
        faces = [tuple(range(len(verts) - 1, -1, -1)) if side < 0 else tuple(range(len(verts)))]
    return new_mesh(name, verts, faces, [mat], recalc=False)


def facade_rect(name, cx, cy, z0, z1, sx, sy, mat):
    return box(name, cx, cy, z0, z1, sx, sy, mat, bevel=False)


def vertical_disc(name, face, z, radius, mat, segments=20, offset=0.0):
    """Clock disc on one tower side in the local coordinate frame."""
    verts = []
    if face in ("front", "back"):
        y = (-1 if face == "front" else 1) * (7.01 + offset)
        for i in range(segments):
            a = 2 * math.pi * i / segments
            verts.append(world(radius * math.cos(a), y, z + radius * math.sin(a)))
        reverse = face == "back"
    else:
        x = (-1 if face == "left" else 1) * (7.01 + offset)
        for i in range(segments):
            a = 2 * math.pi * i / segments
            verts.append(world(x, radius * math.cos(a), z + radius * math.sin(a)))
        reverse = face == "left"
    face_idx = tuple(range(segments - 1, -1, -1)) if reverse else tuple(range(segments))
    return new_mesh(name, verts, [face_idx], [mat], recalc=False)


def clock_detail(face, z, trim, ink, glow):
    vertical_disc(f"clock_{face}_dial", face, z, CLOCK_D / 2, glow, 24)
    # Projecting surround: 12 tick blocks plus two chunky hands.
    for i in range(12):
        a = 2 * math.pi * i / 12
        tang = 0.34 if i % 3 else 0.55
        rr = CLOCK_D * 0.46
        u = rr * math.cos(a)
        zz = z + rr * math.sin(a)
        if face in ("front", "back"):
            y = (-1 if face == "front" else 1) * 7.06
            box(f"clock_{face}_tick_{i}", u, y, zz - tang / 2, zz + tang / 2,
                0.30 if i % 3 else 0.42, 0.16, ink, bevel=False)
        else:
            x = (-1 if face == "left" else 1) * 7.06
            box(f"clock_{face}_tick_{i}", x, u, zz - tang / 2, zz + tang / 2,
                0.16, 0.30 if i % 3 else 0.42, ink, bevel=False)
    # Hands read around 10:10 from all four views.
    for j, (angle, length, thick) in enumerate(((math.radians(150), 2.35, 0.24), (math.radians(30), 1.75, 0.30))):
        du, dz = math.cos(angle) * length / 2, math.sin(angle) * length / 2
        if face in ("front", "back"):
            y = (-1 if face == "front" else 1) * 7.10
            # Use a thin cuboid rotated in the face plane by creating vertices directly.
            make_face_bar(f"clock_{face}_hand_{j}", face, du, z + dz, length, thick, angle, ink)
        else:
            make_face_bar(f"clock_{face}_hand_{j}", face, du, z + dz, length, thick, angle, ink)


def make_face_bar(name, face, center_u, center_z, length, width, angle, mat):
    du = (math.cos(angle) * length / 2, math.sin(angle) * length / 2)
    dv = (-math.sin(angle) * width / 2, math.cos(angle) * width / 2)
    q = [
        (center_u - du[0] - dv[0], center_z - du[1] - dv[1]),
        (center_u + du[0] - dv[0], center_z + du[1] - dv[1]),
        (center_u + du[0] + dv[0], center_z + du[1] + dv[1]),
        (center_u - du[0] + dv[0], center_z - du[1] + dv[1]),
    ]
    verts = []
    if face in ("front", "back"):
        y = (-1 if face == "front" else 1) * 7.11
        verts = [world(u, y, z) for u, z in q]
        reverse = face == "back"
    else:
        x = (-1 if face == "left" else 1) * 7.11
        verts = [world(x, u, z) for u, z in q]
        reverse = face == "left"
    new_mesh(name, verts, [tuple(range(3, -1, -1)) if reverse else (0, 1, 2, 3)], [mat], recalc=False)


def square_belvedere(name, z0, z1, half, pier, wall, trim):
    box(name + "_floor", 0, 0, z0, z0 + 0.7, half * 2 + 1.2, half * 2 + 1.2, trim)
    positions = []
    for x in (-half, -half / 3, half / 3, half):
        positions += [(x, -half), (x, half)]
    for y in (-half / 3, half / 3):
        positions += [(-half, y), (half, y)]
    for i, (x, y) in enumerate(positions):
        box(f"{name}_pier_{i}", x, y, z0 + 0.7, z1 - 0.7, pier, pier, wall, bevel=True, bevel_width=0.10)
    box(name + "_cap", 0, 0, z1 - 0.7, z1, half * 2 + 1.5, half * 2 + 1.5, trim)


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    sand = material("Toy_sand")
    trim = material("Toy_trim")
    ink = material("Toy_ink")
    glass = material("Toy_glass")
    glow = material("Toy_white_Glow")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    gold = material("Toy_gold")

    # Long arcade body and stronger end/central pavilions.
    box("main_body", 0, 0, 0, BODY_H, LENGTH, WIDTH, sand, bevel=True, bevel_width=0.18)
    box("base_plinth", 0, 0, 0, 1.1, LENGTH + 1.2, WIDTH + 1.2, trim, bevel=True, bevel_width=0.12)
    box("belt_course", 0, 0, 6.7, 7.35, LENGTH + 1.0, WIDTH + 1.0, trim, bevel=True, bevel_width=0.10)
    box("main_cornice", 0, 0, 14.0, 15.8, LENGTH + 2.0, WIDTH + 2.0, trim, bevel=True, bevel_width=0.14)

    # Wing pavilions create a less generic, historically plausible end condition.
    for sign in (-1, 1):
        cx = sign * (LENGTH / 2 - 8.0)
        box(f"end_pavilion_{sign}", cx, 0, 0, 16.5, 16.0, WIDTH + 1.6, sand, bevel=True, bevel_width=0.15)
        box(f"end_cornice_{sign}", cx, 0, 15.0, 16.8, 17.4, WIDTH + 3.0, trim, bevel=True, bevel_width=0.12)

    # Central ceremonial pavilion and three monumental arched entrances.
    box("central_pavilion", 0, -0.55, 0, 18.0, 30.0, WIDTH + 2.0, sand, bevel=True, bevel_width=0.16)
    box("central_entablature", 0, -0.55, 16.1, 18.7, 32.0, WIDTH + 3.2, trim, bevel=True, bevel_width=0.14)
    for side_name, y in (("west", -WIDTH / 2 - 1.58), ("east", WIDTH / 2 + 1.58)):
        for i, x in enumerate((-9.0, 0.0, 9.0)):
            facade_arch(f"central_{side_name}_arch_{i}", x, y, 1.0, 7.2, 12.6, 0.0, glass, "x", 10)
        # Giant paired pilasters frame the central arch group.
        for i, x in enumerate((-14.0, -12.2, 12.2, 14.0)):
            box(f"central_{side_name}_column_{i}", x, y + (0.28 if y < 0 else -0.28), 0.8, 15.8,
                1.15, 1.15, trim, bevel=True, bevel_width=0.11)

    # Long west/east facade rhythm. 14 upper and 12 ground openings per wing.
    for side_name, y in (("west", -WIDTH / 2 - 0.13), ("east", WIDTH / 2 + 0.13)):
        for wing in (-1, 1):
            lo, hi = (-(LENGTH / 2 - 9), -17.5) if wing < 0 else (17.5, LENGTH / 2 - 9)
            for i in range(14):
                x = lo + (hi - lo) * (i + 0.5) / 14
                facade_arch(f"{side_name}_upper_{wing}_{i}", x, y, 7.75, 4.35, 5.45, 0, glass, "x", 8)
            for i in range(12):
                x = lo + (hi - lo) * (i + 0.5) / 12
                facade_arch(f"{side_name}_ground_{wing}_{i}", x, y, 1.05, 4.5, 4.85, 0, ink, "x", 8)

    # End elevations: designed gables with one large and two small arch fields.
    for sign, end_name in ((-1, "northwest"), (1, "southeast")):
        x = sign * (LENGTH / 2 + 0.13)
        facade_arch(f"{end_name}_center_arch", 0, x, 2.0, 12.5, 12.0, 0, glass, "y", 10)
        for i, y in enumerate((-18.0, 18.0)):
            facade_arch(f"{end_name}_side_arch_{i}", y, x, 1.2, 8.0, 8.5, 0, glass, "y", 10)
        # Triangular gable plane above the end pavilion.
        verts = [world(x, -WIDTH / 2 - 0.5, 16.4), world(x, WIDTH / 2 + 0.5, 16.4), world(x, 0, 23.0)]
        new_mesh(f"{end_name}_gable", verts, [(0, 1, 2) if sign > 0 else (2, 1, 0)], [sand], recalc=False)

    # Roof and clerestory are intentionally designed for the aerial camera.
    hipped_roof("main_roof", 0, 0, ROOF_EAVE, ROOF_RIDGE, LENGTH - 3.0, WIDTH - 3.5, roofd)
    gable_prism("clerestory", 0, 0, 18.0, 21.0, 23.6, LENGTH - 18.0, 8.5, trim)
    for wing in (-1, 1):
        lo, hi = (-(LENGTH / 2 - 14), -18.0) if wing < 0 else (18.0, LENGTH / 2 - 14)
        for i in range(7):
            x = lo + (hi - lo) * (i + 0.5) / 7
            facade_arch(f"clerestory_w_{wing}_{i}", x, -4.31, 19.0, 5.0, 3.9, 0, glass, "x", 8)
            facade_arch(f"clerestory_e_{wing}_{i}", x, 4.31, 19.0, 5.0, 3.9, 0, glass, "x", 8)

    # Skylight bands break up the roof slopes for the app's downward camera.
    roof_hy = (WIDTH - 3.5) / 2
    for wing in (-1, 1):
        lo, hi = (-(LENGTH / 2 - 14), -18.0) if wing < 0 else (18.0, LENGTH / 2 - 14)
        for i in range(6):
            x = lo + (hi - lo) * (i + 0.5) / 6
            for y in (-15.5, 15.5):
                z = ROOF_RIDGE - (ROOF_RIDGE - ROOF_EAVE) * abs(y) / roof_hy
                box(f"skylight_{wing}_{i}_{'e' if y > 0 else 'w'}", x, y, z - 0.35, z + 0.5,
                    6.4, 2.6, glass, bevel=True, bevel_width=0.10)

    # Four tidy roof plant clusters; no scattered miniature noise.
    plant_specs = [(-69, 8, 9, 6, 2.5), (-48, -8, 7, 5, 3.0), (48, 9, 10, 6, 2.2), (70, -7, 8, 5, 3.2)]
    for i, (x, y, sx, sy, h) in enumerate(plant_specs):
        box(f"roof_plant_{i}", x, y, 19.0, 19.0 + h, sx, sy, steel, bevel=True, bevel_width=0.12)

    # Clock tower: keep the lower shaft narrow relative to the 201 m body.
    box("tower_lower", 0, 0, 0, 42.0, 14.0, 14.0, sand, bevel=True, bevel_width=0.15)
    box("tower_base_band", 0, 0, 18.0, 20.0, 17.5, 17.5, trim, bevel=True, bevel_width=0.12)
    box("tower_clock_stage", 0, 0, 40.5, 50.0, 14.0, 14.0, sand, bevel=True, bevel_width=0.15)
    box("clock_lower_band", 0, 0, 39.8, 41.2, 15.6, 15.6, trim, bevel=True, bevel_width=0.11)
    box("clock_upper_band", 0, 0, 49.5, 51.0, 16.2, 16.2, trim, bevel=True, bevel_width=0.11)
    for face in ("front", "back", "left", "right"):
        clock_detail(face, 45.2, trim, ink, glow)

    # Perforated frieze represented by dark repeated square recesses.
    for face in ("front", "back"):
        y = -7.08 if face == "front" else 7.08
        for i, x in enumerate((-4.8, -2.4, 0, 2.4, 4.8)):
            box(f"frieze_{face}_{i}", x, y, 51.5, 53.0, 1.25, 0.14, ink, bevel=False)
    for face in ("left", "right"):
        x = -7.08 if face == "left" else 7.08
        for i, y in enumerate((-4.8, -2.4, 0, 2.4, 4.8)):
            box(f"frieze_{face}_{i}", x, y, 51.5, 53.0, 0.14, 1.25, ink, bevel=False)

    # Giralda-derived layered crown: square belvederes, setbacks, circular lantern.
    square_belvedere("belvedere_lower", 53.0, 59.0, 6.0, 0.72, sand, trim)
    box("crown_step_1", 0, 0, 59.0, 60.5, 13.0, 13.0, trim, bevel=True, bevel_width=0.13)
    box("crown_step_2", 0, 0, 60.5, 62.0, 10.8, 10.8, sand, bevel=True, bevel_width=0.12)
    square_belvedere("belvedere_upper", 62.0, 67.0, 4.5, 0.64, sand, trim)
    cylinder("lantern_floor", 0, 0, 67.0, 68.0, 5.2, trim, 16, True)
    for i in range(10):
        a = 2 * math.pi * i / 10
        cylinder(f"lantern_pier_{i}", 4.15 * math.cos(a), 4.15 * math.sin(a), 68.0, 71.1, 0.34, sand, 8)
    cylinder("lantern_cap", 0, 0, 71.0, 71.8, 5.0, trim, 16, True)

    # Low faceted dome and recognizable flagpole.
    verts = []
    rings = [(71.8, 4.0), (72.7, 3.35), (73.35, 2.1), (73.7, 0.7)]
    seg = 16
    for z, r in rings:
        for i in range(seg):
            a = 2 * math.pi * i / seg
            verts.append(world(r * math.cos(a), r * math.sin(a), z))
    faces = []
    for j in range(len(rings) - 1):
        for i in range(seg):
            faces.append((j * seg + i, j * seg + (i + 1) % seg, (j + 1) * seg + (i + 1) % seg, (j + 1) * seg + i))
    faces.append(tuple(range((len(rings) - 1) * seg, len(rings) * seg)))
    new_mesh("crown_dome", verts, faces, [gold])
    cylinder("flagpole", 0, 0, 73.5, TOWER_H, 0.16, steel, 8)

    return scene


def report():
    dg = bpy.context.evaluated_depsgraph_get()
    tris = 0
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    for obj in objs:
        me = obj.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for vert in me.vertices:
            p = obj.matrix_world @ vert.co
            for i in range(3):
                mn[i] = min(mn[i], p[i])
                mx[i] = max(mx[i], p[i])
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
    blend = os.path.join(out, "ferry-building.blend")
    glb = os.path.join(out, "ferry-building.glb")
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
