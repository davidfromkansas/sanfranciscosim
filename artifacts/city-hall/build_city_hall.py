"""Deterministically build the SF-SIM San Francisco City Hall miniature.

Usage:
    blender -b --python build_city_hall.py -- [--out DIR]

Authored in true-world orientation: +X east, +Y north, +Z up. The building's
measured long-axis heading is 350.4 degrees true, so all local geometry is
rotated 9.62 degrees counter-clockwise about +Z before the transforms are
applied and the parts are joined per material.
"""

import math
import os
import sys

import bmesh
import bpy

ROT = math.radians(9.62)
HEIGHT = 93.73

# Storey stack, in metres above the terrace datum.
BASE_TOP = 8.5
ORDER_TOP = 26.0
ENTAB_TOP = 28.2
CORNICE_TOP = 30.6
ROOF_TOP = 34.4
CROSSING_TOP = 41.0

# Plan half-extents of the main block, plus portico and stair projections.
HX = 43.0
HY = 61.0
PORTICO_E = 51.0
PORTICO_W = -50.0
STAIR_OUT = 58.6

PALETTE = {
    "Toy_cream": (0.8879, 0.8469, 0.7696),
    "Toy_sand": (0.8398, 0.7758, 0.6584),
    "Toy_trim": (0.8963, 0.8632, 0.7977),
    "Toy_glass": (0.0232, 0.0742, 0.1714),
    "Toy_stone": (0.6939, 0.6445, 0.5356),
    "Toy_roofd": (0.0595, 0.0595, 0.0685),
    "Toy_roofc": (0.2470, 0.3916, 0.3813),
    "Toy_gold": (0.5906, 0.3813, 0.0685),
}
MATS = {}


def material(name):
    if name in MATS:
        return MATS[name]
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    rgb = PALETTE[name]
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.84
    bsdf.inputs["Metallic"].default_value = 0.2 if name == "Toy_gold" else 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.84
    MATS[name] = mat
    return mat


def finish_object(obj, mat_name, bevel=0.0):
    if not obj.data.materials:
        obj.data.materials.append(material(mat_name))
    if bevel >= 0.12:
        mod = obj.modifiers.new("soft toy edges", "BEVEL")
        mod.width = bevel
        mod.segments = 2
        mod.limit_method = "ANGLE"
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
    x, y = obj.location.x, obj.location.y
    obj.location.x = math.cos(ROT) * x - math.sin(ROT) * y
    obj.location.y = math.sin(ROT) * x + math.cos(ROT) * y
    obj.rotation_euler.z += ROT
    return obj


def add_box(name, loc, size, mat_name="Toy_cream", bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish_object(obj, mat_name, bevel)


def add_cylinder(name, loc, radius, depth, mat_name="Toy_cream", vertices=10, bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    obj = bpy.context.object
    obj.name = name
    return finish_object(obj, mat_name, bevel)


def add_sphere(name, loc, scale, mat_name, segments=10, rings=5):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish_object(obj, mat_name)


def add_mesh(name, verts, faces, loc, mat_name, bevel=0.0):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.validate()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    bm = bmesh.new(); bm.from_mesh(mesh); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(mesh); bm.free()
    return finish_object(obj, mat_name, bevel)


def add_frustum(name, loc, lower, upper, height, mat_name, bevel=0.0):
    lx, ly = lower[0] / 2, lower[1] / 2
    ux, uy = upper[0] / 2, upper[1] / 2
    z0, z1 = -height / 2, height / 2
    verts = [(-lx, -ly, z0), (lx, -ly, z0), (lx, ly, z0), (-lx, ly, z0),
             (-ux, -uy, z1), (ux, -uy, z1), (ux, uy, z1), (-ux, uy, z1)]
    faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return add_mesh(name, verts, faces, loc, mat_name, bevel)


def add_pediment(name, loc, width, depth, rise, along_y, mat_name="Toy_trim"):
    """Triangular gable; along_y=True means the gable faces east/west."""
    if along_y:
        sx, sy = depth / 2, width / 2
        verts = [(-sx, -sy, 0), (-sx, sy, 0), (-sx, 0, rise), (sx, -sy, 0), (sx, sy, 0), (sx, 0, rise)]
        faces = [(0, 2, 1), (3, 4, 5), (0, 1, 4, 3), (1, 2, 5, 4), (2, 0, 3, 5)]
    else:
        sx, sy = width / 2, depth / 2
        verts = [(-sx, -sy, 0), (sx, -sy, 0), (0, -sy, rise), (-sx, sy, 0), (sx, sy, 0), (0, sy, rise)]
        faces = [(0, 1, 2), (3, 5, 4), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]
    return add_mesh(name, verts, faces, loc, mat_name)


def add_column(name, loc, height, radius, capital=True):
    add_cylinder(name, (loc[0], loc[1], loc[2] + height / 2), radius, height, "Toy_trim", 8)
    add_box(name + "_plinth", (loc[0], loc[1], loc[2] + 0.4), (radius * 2.7, radius * 2.7, 0.8), "Toy_trim")
    if capital:
        add_box(name + "_capital", (loc[0], loc[1], loc[2] + height - 0.5), (radius * 2.9, radius * 2.9, 1.0), "Toy_trim")


# --------------------------------------------------------------------------- massing


def add_massing():
    add_box("terrace", (0, 0, 0.6), (100, 128, 1.2), "Toy_stone", 0.4)
    add_box("rusticated_base", (0, 0, BASE_TOP / 2 + 0.6), (2 * HX + 3, 2 * HY + 3, BASE_TOP), "Toy_stone", 0.5)
    add_box("main_block", (0, 0, (BASE_TOP + CORNICE_TOP) / 2), (2 * HX, 2 * HY, CORNICE_TOP - BASE_TOP), "Toy_cream", 0.5)

    # Slightly projecting terminal pavilions anchor all four corners.
    for sx in (-1, 1):
        for sy in (-1, 1):
            add_box(f"corner_pavilion_{sx}_{sy}", (sx * (HX - 6.5), sy * (HY - 7.0), (BASE_TOP + ENTAB_TOP) / 2),
                    (16.5, 17.0, ENTAB_TOP - BASE_TOP + 1.6), "Toy_cream", 0.45)

    # Continuous entablature, attic storey, and crowning cornice.
    add_box("entablature", (0, 0, (ORDER_TOP + ENTAB_TOP) / 2 + 0.1), (2 * HX + 2.4, 2 * HY + 2.4, ENTAB_TOP - ORDER_TOP), "Toy_trim", 0.2)
    add_box("attic", (0, 0, (ENTAB_TOP + CORNICE_TOP) / 2), (2 * HX + 0.6, 2 * HY + 0.6, CORNICE_TOP - ENTAB_TOP), "Toy_cream", 0.25)
    add_box("cornice", (0, 0, CORNICE_TOP + 0.45), (2 * HX + 3.4, 2 * HY + 3.4, 1.5), "Toy_trim", 0.25)


def add_roofscape():
    band = 15.0
    inner_x = HX - band
    inner_y = HY - band
    top = ROOF_TOP - CORNICE_TOP
    add_frustum("roof_band_east", ((HX + inner_x) / 2, 0, CORNICE_TOP + top / 2 + 0.9),
                (band, 2 * HY), (band - 5, 2 * HY - 6), top, "Toy_roofc", 0.2)
    add_frustum("roof_band_west", (-(HX + inner_x) / 2, 0, CORNICE_TOP + top / 2 + 0.9),
                (band, 2 * HY), (band - 5, 2 * HY - 6), top, "Toy_roofc", 0.2)
    add_frustum("roof_band_north", (0, (HY + inner_y) / 2, CORNICE_TOP + top / 2 + 0.9),
                (2 * inner_x, band), (2 * inner_x - 6, band - 5), top, "Toy_roofc", 0.2)
    add_frustum("roof_band_south", (0, -(HY + inner_y) / 2, CORNICE_TOP + top / 2 + 0.9),
                (2 * inner_x, band), (2 * inner_x - 6, band - 5), top, "Toy_roofc", 0.2)

    # Flat deck inside the metal band, shaped around the two inner light courts.
    deck_z = CORNICE_TOP + 0.7
    for sx in (-1, 1):
        add_box(f"roof_deck_side_{sx}", (sx * 22.0, 0, deck_z), (14.0, 2 * inner_y, 1.0), "Toy_sand", 0.15)
    for sy in (-1, 1):
        add_box(f"roof_deck_end_{sy}", (0, sy * 42.0, deck_z), (30.0, 8.0, 1.0), "Toy_sand", 0.15)
        add_box(f"court_rim_{sy}", (0, sy * 30.0, deck_z + 0.5), (32.0, 28.0, 0.5), "Toy_trim", 0.12)
        add_box(f"court_void_{sy}", (0, sy * 30.0, deck_z + 0.55), (28.0, 24.0, 0.5), "Toy_roofd")
        for k in range(4):
            add_box(f"court_skylight_{sy}_{k}", (0, sy * (23.0 + k * 4.6), deck_z + 0.9), (26.0, 2.6, 0.4), "Toy_glass")
        # Rooftop solar arrays sit on the court rims, as on the real building.
        for i in (-1, 0, 1):
            add_box(f"solar_{sy}_{i}", (i * 9.0, sy * 43.5, deck_z + 0.9), (7.4, 5.0, 0.35), "Toy_roofd")

    # Raised crossing mass and the four pavilions that surround the dome base.
    add_box("crossing_block", (0, 0, (CORNICE_TOP + CROSSING_TOP) / 2), (46, 42, CROSSING_TOP - CORNICE_TOP), "Toy_cream", 0.5)
    add_box("crossing_cornice", (0, 0, CROSSING_TOP + 0.5), (48.5, 44.5, 1.4), "Toy_trim", 0.2)
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * 26.5, sy * 25.0
            add_box(f"dome_pavilion_{sx}_{sy}", (x, y, CORNICE_TOP + 3.4), (13.0, 13.0, 7.5), "Toy_cream", 0.3)
            add_frustum(f"dome_pavilion_roof_{sx}_{sy}", (x, y, CORNICE_TOP + 9.1), (14.0, 14.0), (4.0, 4.0), 4.0, "Toy_roofd", 0.2)


# --------------------------------------------------------------------------- facades


def add_long_facade(side, sign):
    """East/west elevations: the long walls that run north-south."""
    x_wall = sign * HX
    face = sign * 0.28
    for i in range(19):
        y = -54.0 + i * 6.0
        if abs(y) < 19.0:
            continue
        add_box(f"{side}_pilaster_{i}", (x_wall + face, y, (BASE_TOP + ORDER_TOP) / 2),
                (1.7, 2.0, ORDER_TOP - BASE_TOP), "Toy_trim")
        yw = y + 3.0
        if abs(yw) < 19.0 or abs(yw) > 57.0:
            continue
        add_box(f"{side}_order_window_{i}", (x_wall + face * 0.5, yw, 17.4), (0.8, 3.4, 11.0), "Toy_glass")
        add_box(f"{side}_order_sill_{i}", (x_wall + face, yw, 11.5), (1.0, 4.4, 0.5), "Toy_trim")
        add_box(f"{side}_base_window_{i}", (x_wall + 1.6 * face, yw, 4.6), (0.9, 2.8, 3.4), "Toy_glass")
        add_box(f"{side}_attic_window_{i}", (x_wall + face, yw, 29.2), (0.8, 2.6, 1.9), "Toy_glass")

    # Corner pavilion faces get their own bay group and a small crowning pediment.
    for sy in (-1, 1):
        px = sign * (HX + 0.25)
        for k, dy in enumerate((-5.4, 0.0, 5.4)):
            y = sy * (HY - 7.0) + dy
            add_box(f"{side}_pav_window_{sy}_{k}", (px, y, 17.4), (0.9, 3.2, 10.4), "Toy_glass")
            add_box(f"{side}_pav_base_window_{sy}_{k}", (px + 0.6 * sign, y, 4.6), (0.9, 2.6, 3.4), "Toy_glass")
            add_box(f"{side}_pav_column_{sy}_{k}", (px + 0.5 * sign, y - 3.0, (BASE_TOP + ORDER_TOP) / 2),
                    (1.6, 1.6, ORDER_TOP - BASE_TOP), "Toy_trim")
        add_pediment(f"{side}_pav_pediment_{sy}", (sign * (HX - 6.0), sy * (HY - 7.0), ENTAB_TOP + 1.7),
                     17.0, 3.0, 4.6, True)


def add_portico(side, sign, half_width, projection, columns, portal_span):
    """Giant-order pedimented portico: rusticated arcaded podium, free-standing
    column screen in front of a recessed wall, entablature and gable."""
    front = sign * projection
    mid = sign * (HX + projection) / 2
    depth = projection - HX

    add_box(f"{side}_portico_podium", (mid, 0, BASE_TOP / 2 + 0.6),
            (depth, 2 * half_width + 1.0, BASE_TOP), "Toy_stone", 0.35)
    # Ceremonial arched portals in the podium, reached by the grand stair.
    for i, y in enumerate(portal_span):
        add_box(f"{side}_portal_{i}", (front, y, 4.6), (1.0, 4.6, 6.4), "Toy_glass")
        add_box(f"{side}_portal_arch_{i}", (front - sign * 0.1, y, 8.1), (1.3, 5.4, 0.9), "Toy_gold")

    # Antae (solid end piers) frame the colonnade; wall behind is recessed.
    for sy in (-1, 1):
        add_box(f"{side}_anta_{sy}", (mid, sy * (half_width - 1.4), (BASE_TOP + ENTAB_TOP) / 2),
                (depth, 3.4, ENTAB_TOP - BASE_TOP), "Toy_cream", 0.3)
    step = (2 * half_width - 8.0) / (columns - 1)
    for i in range(columns):
        y = -half_width + 4.0 + i * step
        add_column(f"{side}_column_{i}", (front - sign * 1.9, y, BASE_TOP), ORDER_TOP - BASE_TOP, 1.18)

    add_box(f"{side}_portico_entablature", (mid, 0, (ORDER_TOP + ENTAB_TOP) / 2 + 0.7),
            (depth + 1.6, 2 * half_width + 2.4, ENTAB_TOP - ORDER_TOP + 1.4), "Toy_trim", 0.25)
    add_pediment(f"{side}_pediment", (mid, 0, ENTAB_TOP + 1.5),
                 2 * half_width + 2.4, depth + 1.6, 8.8, True)

    # Tall glazed bays on the recessed wall, read between the columns.
    for i, y in enumerate(portal_span):
        add_box(f"{side}_tall_window_{i}", (sign * (HX + 0.35), y, 17.6), (0.9, 4.8, 12.4), "Toy_glass")
    add_box(f"{side}_gold_frieze", (sign * (HX + 0.35), 0, 24.6), (0.9, 2 * half_width - 8.0, 0.9), "Toy_gold")


def add_short_facade(side, sign):
    """North/south elevations: the short walls, with a modest central accent."""
    y_wall = sign * HY
    face = sign * 0.28
    for i in range(13):
        x = -36.0 + i * 6.0
        add_box(f"{side}_pilaster_{i}", (x, y_wall + face, (BASE_TOP + ORDER_TOP) / 2),
                (2.0, 1.7, ORDER_TOP - BASE_TOP), "Toy_trim")
        xw = x + 3.0
        if xw > 38.0:
            continue
        add_box(f"{side}_order_window_{i}", (xw, y_wall + face * 0.5, 17.4), (3.4, 0.8, 11.0), "Toy_glass")
        add_box(f"{side}_order_sill_{i}", (xw, y_wall + face, 11.5), (4.4, 1.0, 0.5), "Toy_trim")
        add_box(f"{side}_base_window_{i}", (xw, y_wall + 1.6 * face, 4.6), (2.8, 0.9, 3.4), "Toy_glass")
        add_box(f"{side}_attic_window_{i}", (xw, y_wall + face, 29.2), (2.6, 0.8, 1.9), "Toy_glass")

    py = sign * (HY + 2.6)
    add_box(f"{side}_center_mass", (0, sign * (HY + 1.3), (0.6 + ENTAB_TOP) / 2), (30.0, 2.6, ENTAB_TOP - 0.6), "Toy_cream", 0.35)
    for i, x in enumerate((-11.0, -3.7, 3.7, 11.0)):
        add_column(f"{side}_column_{i}", (x, py - sign * 0.6, BASE_TOP), ORDER_TOP - BASE_TOP, 1.0)
    for i, x in enumerate((-7.4, 0.0, 7.4)):
        add_box(f"{side}_center_window_{i}", (x, py - sign * 1.4, 17.4), (3.8, 1.0, 11.0), "Toy_glass")
        add_box(f"{side}_center_door_{i}", (x, py - sign * 1.4, 4.9), (3.4, 1.0, 5.6), "Toy_glass")
    add_box(f"{side}_center_entablature", (0, py - sign * 1.0, (ORDER_TOP + ENTAB_TOP) / 2 + 0.3),
            (31.0, 3.4, ENTAB_TOP - ORDER_TOP + 1.4), "Toy_trim", 0.22)
    add_pediment(f"{side}_center_pediment", (0, py - sign * 1.2, ENTAB_TOP + 1.2), 31.0, 4.4, 5.4, False)


def add_stairs_and_balustrade():
    # Grand plaza-facing approach on the east front.
    steps = 9
    for i in range(steps):
        x_front = STAIR_OUT - i * 0.84
        add_box(f"east_step_{i}", ((x_front + PORTICO_E) / 2, 0, 0.4 + i * 0.52),
                (x_front - PORTICO_E, 40.0 - i * 0.7, 0.62), "Toy_stone")
    add_box("east_stair_landing", (PORTICO_E + 0.9, 0, 5.0), (5.0, 34.0, 0.8), "Toy_trim", 0.14)
    for sy in (-1, 1):
        add_box(f"east_stair_cheek_{sy}", ((STAIR_OUT + PORTICO_E) / 2, sy * 20.6, 2.4),
                (STAIR_OUT - PORTICO_E, 2.6, 4.0), "Toy_stone", 0.2)
        add_box(f"east_stair_plinth_{sy}", (STAIR_OUT - 1.2, sy * 20.6, 4.9), (3.4, 3.6, 1.2), "Toy_trim", 0.15)

    # Low balustraded terrace edge, opened where the grand stair lands.
    for sy in (-1, 1):
        add_box(f"terrace_rail_east_{sy}", (49.6, sy * 40.0, 1.9), (1.6, 38.0, 1.6), "Toy_trim", 0.15)
    for sy in (-1, 1):
        add_box(f"terrace_rail_west_{sy}", (-49.6, sy * 40.0, 1.9), (1.6, 38.0, 1.6), "Toy_trim", 0.15)
    for sy in (-1, 1):
        add_box(f"terrace_rail_{sy}", (0, sy * 63.6, 1.9), (98.0, 1.6, 1.6), "Toy_trim", 0.15)
    for sx in (-1, 1):
        for sy in (-1, 1):
            add_box(f"terrace_post_{sx}_{sy}", (sx * 49.6, sy * 63.6, 2.1), (2.6, 2.6, 2.2), "Toy_trim", 0.2)


# --------------------------------------------------------------------------- dome


def add_dome():
    add_frustum("dome_transition", (0, 0, CROSSING_TOP + 2.6), (42, 40), (36, 36), 3.2, "Toy_trim", 0.3)
    add_cylinder("drum_plinth", (0, 0, CROSSING_TOP + 5.6), 17.8, 3.0, "Toy_trim", 32, 0.15)
    add_cylinder("drum_body", (0, 0, 53.6), 16.4, 12.0, "Toy_cream", 32, 0.15)
    add_cylinder("drum_entablature", (0, 0, 60.4), 17.6, 2.2, "Toy_trim", 32, 0.2)
    add_cylinder("drum_crown", (0, 0, 62.2), 16.9, 1.8, "Toy_stone", 32, 0.15)

    # Sixteen-bay drum: dark openings alternating with paired columns and urns.
    for i in range(16):
        a = 2 * math.pi * i / 16
        r = 16.6
        bpy.ops.mesh.primitive_cube_add(location=(r * math.cos(a), r * math.sin(a), 53.4))
        window = bpy.context.object
        window.name = f"drum_window_{i}"
        window.dimensions = (0.9, 3.9, 8.4)
        window.rotation_euler.z = a
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        finish_object(window, "Toy_glass")
        for offset in (-1, 1):
            ca = a + offset * math.pi / 16 * 0.62
            add_cylinder(f"drum_column_{i}_{offset}", (17.1 * math.cos(ca), 17.1 * math.sin(ca), 53.4),
                         0.62, 12.6, "Toy_trim", 8)
        ua = a + math.pi / 16
        add_box(f"drum_urn_{i}", (17.4 * math.cos(ua), 17.4 * math.sin(ua), 63.6), (1.5, 1.5, 2.4), "Toy_trim")

    # Revolved dome shell: stilted, ribbed, and deliberately oversized.
    profile = [(16.1, 62.9), (16.0, 65.4), (15.4, 68.6), (14.3, 71.8), (12.7, 74.8),
               (10.4, 77.6), (7.5, 79.9), (4.2, 81.4), (2.6, 81.9)]
    segments = 32
    verts = []
    for radius, z in profile:
        for i in range(segments):
            a = 2 * math.pi * i / segments
            verts.append((radius * math.cos(a), radius * math.sin(a), z))
    faces = []
    for j in range(len(profile) - 1):
        for i in range(segments):
            ni = (i + 1) % segments
            faces.append((j * segments + i, j * segments + ni, (j + 1) * segments + ni, (j + 1) * segments + i))
    add_mesh("dome_shell", verts, faces, (0, 0, 0), "Toy_roofd")

    # Gilded meridian ribs and ornament, the dome's strongest colour cue.
    for i in range(16):
        a = 2 * math.pi * i / 16
        curve = bpy.data.curves.new(f"dome_rib_{i}_curve", "CURVE")
        curve.dimensions = "3D"
        curve.resolution_u = 1
        curve.bevel_depth = 0.24
        curve.bevel_resolution = 0
        spline = curve.splines.new("POLY")
        spline.points.add(len(profile) - 1)
        for point, (radius, z) in zip(spline.points, profile):
            point.co = ((radius + 0.12) * math.cos(a), (radius + 0.12) * math.sin(a), z, 1.0)
        obj = bpy.data.objects.new(f"dome_rib_{i}", curve)
        bpy.context.collection.objects.link(obj)
        curve.materials.append(material("Toy_gold"))
        obj.rotation_euler.z = ROT
    add_cylinder("dome_gold_ring", (0, 0, 63.4), 16.3, 1.2, "Toy_gold", 32)
    for i in range(8):
        a = 2 * math.pi * i / 8 + math.pi / 8
        add_sphere(f"dome_medallion_{i}", (13.9 * math.cos(a), 13.9 * math.sin(a), 71.0), (1.0, 1.0, 1.3), "Toy_gold")

    # Tiered open lantern with a dark spire cap and gold finial.
    add_cylinder("lantern_balcony", (0, 0, 82.3), 4.6, 1.1, "Toy_gold", 16, 0.12)
    add_cylinder("lantern_base", (0, 0, 83.2), 3.7, 0.9, "Toy_trim", 16)
    for i in range(8):
        a = 2 * math.pi * i / 8
        add_cylinder(f"lantern_column_{i}", (3.1 * math.cos(a), 3.1 * math.sin(a), 86.4), 0.34, 5.6, "Toy_gold", 6)
    add_cylinder("lantern_core", (0, 0, 86.4), 2.1, 5.4, "Toy_glass", 12)
    add_cylinder("lantern_cornice", (0, 0, 89.5), 3.9, 0.9, "Toy_gold", 16, 0.12)
    add_frustum("lantern_spire", (0, 0, 91.2), (4.4, 4.4), (0.9, 0.9), 2.6, "Toy_roofd", 0.15)
    add_cylinder("finial", (0, 0, 92.9), 0.22, 1.4, "Toy_gold", 6)
    add_sphere("finial_ball", (0, 0, HEIGHT - 0.3), (0.32, 0.32, 0.32), "Toy_gold")


# --------------------------------------------------------------------------- export


def apply_and_join_by_material():
    for obj in list(bpy.data.objects):
        if obj.type == "CURVE":
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.convert(target="MESH")
            obj.select_set(False)

    meshes = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    bpy.ops.object.select_all(action="DESELECT")
    for obj in meshes:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.select_all(action="DESELECT")

    for mat_name in PALETTE:
        group = [obj for obj in bpy.data.objects
                 if obj.type == "MESH" and obj.data.materials and obj.data.materials[0].name == mat_name]
        if not group:
            continue
        for obj in group:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = group[0]
        bpy.ops.object.join()
        group[0].name = mat_name.replace("Toy_", "CityHall_")
        bpy.ops.object.select_all(action="DESELECT")

    for obj in [o for o in bpy.data.objects if o.type == "MESH"]:
        bm = bmesh.new(); bm.from_mesh(obj.data)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(obj.data); bm.free()
        obj.data.validate(clean_customdata=False)
        obj.data.shade_flat()
        obj.location = (0, 0, 0)
        obj.rotation_euler = (0, 0, 0)
        obj.scale = (1, 1, 1)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))
    out = argv[argv.index("--out") + 1] if "--out" in argv else here
    os.makedirs(out, exist_ok=True)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"
    scene.unit_settings.scale_length = 1.0

    for name in PALETTE:
        material(name)
    add_massing()
    add_long_facade("east", 1)
    add_long_facade("west", -1)
    add_short_facade("north", 1)
    add_short_facade("south", -1)
    add_portico("east", 1, 18.0, PORTICO_E, 8, (-9.4, 0.0, 9.4))
    add_portico("west", -1, 15.0, -PORTICO_W, 6, (-8.0, 0.0, 8.0))
    add_stairs_and_balustrade()
    add_roofscape()
    add_dome()
    apply_and_join_by_material()

    blend = os.path.join(out, "city-hall.blend")
    glb = os.path.join(out, "city-hall.glb")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    bpy.ops.export_scene.gltf(
        filepath=glb,
        export_format="GLB",
        export_apply=True,
        use_selection=False,
        export_cameras=False,
        export_lights=False,
        export_animations=False,
        export_skins=False,
        export_morph=False,
        export_materials="EXPORT",
        export_image_format="NONE",
    )
    print(f"[city-hall] wrote {blend}")
    print(f"[city-hall] wrote {glb}")


if __name__ == "__main__":
    main()
