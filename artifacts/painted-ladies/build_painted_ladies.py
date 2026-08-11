"""Deterministic Blender build of the SF-SIM miniature Painted Ladies.

    blender -b --python build_painted_ladies.py -- [--out DIR]

Writes painted-ladies.blend and painted-ladies.glb. Geometry is authored in
real-world metres with Blender +X east, +Y true north, +Z up. The measured OSM
heading is baked into every vertex: the row runs 350.87 deg / 170.87 deg and the
six front facades look WEST across Steiner Street to Alamo Square Park, outward
normal 260.87 deg (see REFERENCE.md -- the houses stand on the EAST side of
Steiner Street, not the west).

Local authoring frame, before the yaw is applied:
    local +X = away from the street, toward the rear of the lots (bearing 80.87)
    local +Y = along the row toward its north end   (bearing 350.87)
    local  x = 0 is the front wall plane, x = 16 the rear wall plane.
House 0 is 710 Steiner (south end, highest ground); house 5 is 720 Steiner
(north end, lowest ground). The 2.9 m fall of Steiner Street across the row is
baked into the stone base course so the roofline steps, while the whole model
still sits on one flat z = 0 plane.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- measured data

YAW = math.radians(9.13)  # local +Y -> bearing 350.87 deg (true north of the row)

PITCH = 7.00      # centre-to-centre spacing of the six houses, measured on OSM
BODY_W = 6.88     # body width; the 0.12 m reveal is the party-wall shadow line
DEPTH = 16.00     # front wall to rear wall
FRONT_DEPTH = 12.50   # full-height main mass; the rest is the lower rear wing
GRADE_STEP = 0.58     # NED10m fall per house going north (2.90 m over the row)

FLOOR_H = 3.10
BASE_H = 2.20         # raised basement / garage storey
CORNICE_H = 0.60
RIDGE_RISE = 3.50     # each house reaches 12.5 m at its main ridge
GABLE_RISE = 3.25

# number, facade, roof, gable delta, chimney rise, chimney material,
# rear-wing start x, rear-wing eave drop, gable-field material
HOUSES = [
    ("710", "Toy_sand",      "Toy_roofd", 0.00, 0.95, "Toy_brick", 12.30, 0.90, "Toy_gold"),
    ("712", "Toy_sky",       "Toy_roofd", 0.16, 0.62, "Toy_rust",  12.90, 1.35, None),
    ("714", "Toy_cream",     "Toy_rust",  -0.12, 1.05, "Toy_brick", 12.50, 0.75, None),
    ("716", "Toy_mustard",   "Toy_roofd", 0.24, 0.70, "Toy_rust",  13.10, 1.20, "Toy_red"),
    ("718", "Toy_verdigris", "Toy_roofd", 0.04, 0.98, "Toy_brick", 12.40, 1.00, None),
    ("720", "Toy_mint",      "Toy_roofd", 0.14, 0.58, "Toy_rust",  12.80, 1.45, None),
]

PALETTE_HEX = {
    "Toy_cream": "f2ede3",
    "Toy_sand": "ece4d4",
    "Toy_sky": "6db3d9",
    "Toy_coral": "e8735a",
    "Toy_mustard": "d9a441",
    "Toy_verdigris": "9fb8a8",
    "Toy_mint": "8fd0a8",
    "Toy_trim": "f3efe6",
    "Toy_roofd": "45454a",
    "Toy_rust": "a86444",
    "Toy_glass": "2a4d73",
    "Toy_ink": "3a3530",
    "Toy_stone": "d9d2c2",
    "Toy_brick": "c96f4a",
    "Toy_gold": "caa64a",
    "Toy_red": "c4453c",
    "Toy_gold_Glow": "ffd489",  # lamp/window light: read at night from 150 m out
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {name: srgb_to_linear(value) for name, value in PALETTE_HEX.items()}


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


# ------------------------------------------------------------------- primitives


def rot2(x, y):
    c, s = math.cos(YAW), math.sin(YAW)
    return x * c - y * s, x * s + y * c


def world(x, y, z):
    xx, yy = rot2(x, y)
    return (xx, yy, z)


def new_mesh(name, verts, faces, mat, do_bevel=False, bevel_width=0.10, recalc=True):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(v) for v in verts], [], faces)
    mesh.materials.append(mat)
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


BOX_FACES = [
    (3, 2, 1, 0),
    (4, 5, 6, 7),
    (0, 1, 5, 4),
    (1, 2, 6, 5),
    (2, 3, 7, 6),
    (3, 0, 4, 7),
]


def box(name, x0, x1, y0, y1, z0, z1, mat, bevel=False, bevel_width=0.10):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    verts = [world(x, y, z0) for x, y in pts] + [world(x, y, z1) for x, y in pts]
    return new_mesh(name, verts, BOX_FACES, mat, do_bevel=bevel, bevel_width=bevel_width)


def prism_z(name, plan, z0, z1, mat, bevel=False, bevel_width=0.10):
    """Vertical prism over a CCW plan polygon given in local x/y."""
    n = len(plan)
    verts = [world(x, y, z0) for x, y in plan] + [world(x, y, z1) for x, y in plan]
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    faces += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return new_mesh(name, verts, faces, mat, do_bevel=bevel, bevel_width=bevel_width)


def gable_slab(name, x0, x1, yc, half_w, z_base, z_apex, mat, bevel=False, bevel_width=0.08):
    """Triangular prism extruded along local X; the triangle stands in the Y-Z plane."""
    tri = [(yc - half_w, z_base), (yc + half_w, z_base), (yc, z_apex)]
    verts = [world(x0, y, z) for y, z in tri] + [world(x1, y, z) for y, z in tri]
    faces = [(2, 1, 0), (3, 4, 5), (0, 1, 4, 3), (1, 2, 5, 4), (2, 0, 3, 5)]
    return new_mesh(name, verts, faces, mat, do_bevel=bevel, bevel_width=bevel_width)


def hip_roof(name, x0, x1, yc, half_w, z_eave, z_ridge, mat, hip_front=1.1, hip_back=1.6):
    """Roof with the ridge along local X, hipped at both ends, eaves all round."""
    y0, y1 = yc - half_w, yc + half_w
    verts = [
        world(x0, y0, z_eave), world(x1, y0, z_eave),
        world(x1, y1, z_eave), world(x0, y1, z_eave),
        world(x0 + hip_front, yc, z_ridge), world(x1 - hip_back, yc, z_ridge),
    ]
    faces = [(0, 1, 5, 4), (1, 2, 5), (2, 3, 4, 5), (3, 0, 4), (3, 2, 1, 0)]
    return new_mesh(name, verts, faces, mat, do_bevel=True, bevel_width=0.09)


def plate(name, xf, yc, zc, width, height, depth, mat):
    """Thin slab standing proud of the front (west) wall; xf is its outer x."""
    return box(name, xf, xf + depth, yc - width / 2, yc + width / 2,
               zc - height / 2, zc + height / 2, mat)


def rear_plate(name, xr, yc, zc, width, height, depth, mat):
    return box(name, xr - depth, xr, yc - width / 2, yc + width / 2,
               zc - height / 2, zc + height / 2, mat)


def window_front(name, xf, yc, zc, width, height, trim, glass, glow=None):
    plate(name + "_trim", xf - 0.09, yc, zc, width + 0.34, height + 0.34, 0.11, trim)
    plate(name + "_glass", xf - 0.13, yc, zc, width, height, 0.06, glass)
    if glow is not None:
        # Lit pane just proud of the glass; the loader fades it in at dusk.
        plate(name + "_lit", xf - 0.17, yc, zc, width * 0.62, height * 0.66, 0.045, glow)


def window_rear(name, xr, yc, zc, width, height, trim, glass):
    rear_plate(name + "_trim", xr + 0.09, yc, zc, width + 0.30, height + 0.30, 0.11, trim)
    rear_plate(name + "_glass", xr + 0.13, yc, zc, width, height, 0.06, glass)


def cant_window(name, a, b, zc, height, trim, glass):
    """Window set into the canted return of a bay; a,b are the plan edge ends."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    nx, ny = -uy, ux  # outward for the bay plan winding used below

    def band(t0, t1, o0, o1, z0, z1, mat, name_suffix):
        pts = [
            (a[0] + ux * t0 + nx * o0, a[1] + uy * t0 + ny * o0),
            (a[0] + ux * t1 + nx * o0, a[1] + uy * t1 + ny * o0),
            (a[0] + ux * t1 + nx * o1, a[1] + uy * t1 + ny * o1),
            (a[0] + ux * t0 + nx * o1, a[1] + uy * t0 + ny * o1),
        ]
        prism_z(name + name_suffix, pts, z0, z1, mat)

    band(0.18, length - 0.18, -0.02, 0.08, zc - height / 2 - 0.17, zc + height / 2 + 0.17,
         trim, "_trim")
    band(0.33, length - 0.33, 0.04, 0.13, zc - height / 2, zc + height / 2, glass, "_glass")


def window_side(name, ys, sign, xc, zc, width, height, trim, glass):
    """Window on a flank wall (local +/-Y face); only the two end houses need these."""
    y_out = ys + sign * 0.09
    box(name + "_trim", xc - (width + 0.30) / 2, xc + (width + 0.30) / 2,
        min(ys, y_out), max(ys, y_out), zc - (height + 0.30) / 2, zc + (height + 0.30) / 2, trim)
    y_g = ys + sign * 0.15
    box(name + "_glass", xc - width / 2, xc + width / 2,
        min(ys + sign * 0.08, y_g), max(ys + sign * 0.08, y_g),
        zc - height / 2, zc + height / 2, glass)


# ----------------------------------------------------------------------- house


def build_house(index, number, facade_name, roof_name, gable_delta, chimney_extra,
                chimney_name, wing_x, wing_drop, field_name):
    """One Victorian. index 0 = 710 Steiner (south, highest ground)."""
    facade = material(facade_name)
    field = material(field_name) if field_name else facade
    roof = material(roof_name)
    trim = material("Toy_trim")
    glass = material("Toy_glass")
    ink = material("Toy_ink")
    stone = material("Toy_stone")
    brick = material(chimney_name)
    glow = material("Toy_gold_Glow")

    tag = f"h{index}_{number}"
    yc = (index - 2.5) * PITCH            # local +Y is north, so 710 sits south
    g = (5 - index) * GRADE_STEP          # Steiner Street falls 0.58 m per house north
    hw = BODY_W / 2

    base_top = g + BASE_H
    f1_top = base_top + FLOOR_H
    f2_top = f1_top + FLOOR_H
    corn_top = f2_top + CORNICE_H
    ridge = corn_top + RIDGE_RISE
    apex = corn_top + GABLE_RISE + gable_delta
    finial_top = apex + 0.55

    y0, y1 = yc - hw, yc + hw

    # 1. Raised basement: one continuous stone course that steps down the hill.
    box(f"{tag}_base", 0.0, DEPTH, y0, y1, 0.0, base_top, stone, bevel=True, bevel_width=0.10)
    box(f"{tag}_water_table", -0.22, FRONT_DEPTH, y0 - 0.14, y1 + 0.14,
        base_top - 0.34, base_top, trim, bevel=True, bevel_width=0.07)

    # 2. Main mass and the lower rear wing (real rear extensions read from above).
    box(f"{tag}_body", 0.0, wing_x, y0, y1, base_top, f2_top, facade,
        bevel=True, bevel_width=0.11)
    wing_eave = f2_top - wing_drop
    box(f"{tag}_rear_wing", wing_x, DEPTH, y0 + 0.26, y1 - 0.26,
        base_top, wing_eave, facade, bevel=True, bevel_width=0.10)
    box(f"{tag}_rear_roof", wing_x, DEPTH + 0.16, y0 + 0.12, y1 - 0.12,
        wing_eave, wing_eave + 0.26, roof, bevel=True, bevel_width=0.07)
    box(f"{tag}_rear_rail", DEPTH - 0.20, DEPTH + 0.16, y0 + 0.12, y1 - 0.12,
        wing_eave + 0.26, wing_eave + 0.64, trim, bevel=True, bevel_width=0.06)

    # 3. Belt course between the two upper storeys and the heavy main cornice.
    box(f"{tag}_belt", -0.30, wing_x, y0 - 0.16, y1 + 0.16,
        f1_top - 0.16, f1_top + 0.16, trim, bevel=True, bevel_width=0.06)
    box(f"{tag}_cornice", -0.52, wing_x, y0 - 0.30, y1 + 0.30,
        f2_top, corn_top, trim, bevel=True, bevel_width=0.09)
    # Corbel rhythm under the cornice: the row's cheapest, most legible ornament.
    for k in range(7):
        cy = y0 + 0.42 + k * (BODY_W - 0.84) / 6.0
        box(f"{tag}_corbel_{k}", -0.46, -0.02, cy - 0.13, cy + 0.13,
            f2_top - 0.46, f2_top, trim)

    # 4. Hipped main roof, ridge running east-west; six of these make the row's
    #    corrugated top view.
    hip_roof(f"{tag}_roof", 1.05, wing_x + 0.28, yc, hw + 0.24, corn_top, ridge, roof)

    # 5. Steep front gable with bargeboard, recessed shingle field and finial.
    gable_slab(f"{tag}_gable", -0.52, 1.35, yc, hw + 0.30, corn_top - 0.05, apex, trim,
               bevel=True, bevel_width=0.07)
    gable_slab(f"{tag}_gable_field", -0.66, -0.50, yc, hw - 0.16, corn_top + 0.30,
               apex - 0.62, field)
    window_front(f"{tag}_attic", -0.66, yc, corn_top + 1.02, 1.05, 0.58, trim, glass)
    box(f"{tag}_finial", -0.20, 0.28, yc - 0.11, yc + 0.11, apex - 0.15, finial_top, trim)

    # 6. Projecting bay: square bay with canted returns, two storeys tall.
    bay_c = yc - 0.66
    bay_hw, bay_out, cant = 2.30, 1.05, 0.66
    plan = [
        (0.0, bay_c - bay_hw),
        (-bay_out, bay_c - bay_hw + cant),
        (-bay_out, bay_c + bay_hw - cant),
        (0.0, bay_c + bay_hw),
    ]
    prism_z(f"{tag}_bay", plan, base_top, f2_top, facade, bevel=True, bevel_width=0.09)
    for z_band, thick in ((f1_top, 0.17), (f2_top, 0.30)):
        wide = [(0.0, bay_c - bay_hw - 0.14), (-bay_out - 0.14, bay_c - bay_hw + cant - 0.06),
                (-bay_out - 0.14, bay_c + bay_hw - cant + 0.06), (0.0, bay_c + bay_hw + 0.14)]
        prism_z(f"{tag}_bay_band_{int(z_band * 10)}", wide, z_band - thick / 2, z_band + thick / 2,
                trim, bevel=True, bevel_width=0.06)
    for j, zc in enumerate((base_top + 2.00, f1_top + 2.00)):
        window_front(f"{tag}_bay_win_{j}", -bay_out, bay_c, zc, 1.58, 2.25, trim, glass, glow)
        cant_window(f"{tag}_bay_cant_s{j}", plan[0], plan[1], zc, 1.95, trim, glass)
        cant_window(f"{tag}_bay_cant_n{j}", plan[2], plan[3], zc, 1.95, trim, glass)
    for j, yy in enumerate((bay_c - bay_hw + 0.24, bay_c + bay_hw - 0.24)):
        box(f"{tag}_bay_post_{j}", -0.20, 0.10, yy - 0.16, yy + 0.16, base_top, f2_top, trim)

    # 7. Entry bay on the north side: recessed door, hood, balustrade, stoop.
    ent_c = yc + hw - 0.90
    box(f"{tag}_door_case", -0.08, 0.12, ent_c - 0.84, ent_c + 0.84,
        base_top, base_top + 2.64, trim, bevel=True, bevel_width=0.05)
    box(f"{tag}_door", -0.20, 0.24, ent_c - 0.56, ent_c + 0.56,
        base_top + 0.05, base_top + 2.28, ink)
    box(f"{tag}_transom", -0.18, 0.16, ent_c - 0.50, ent_c + 0.50,
        base_top + 2.32, base_top + 2.54, glass)
    box(f"{tag}_lamp", -0.74, -0.46, ent_c - 0.27, ent_c + 0.27,
        base_top + 2.36, base_top + 2.92, glow)
    box(f"{tag}_hood", -1.15, 0.0, ent_c - 1.05, ent_c + 1.05,
        base_top + 2.98, base_top + 3.32, trim, bevel=True, bevel_width=0.07)
    box(f"{tag}_balcony", -1.05, -0.02, ent_c - 0.98, ent_c + 0.98,
        base_top + 3.32, base_top + 3.92, trim, bevel=True, bevel_width=0.07)
    for j, zc in enumerate((f1_top + 1.95,)):
        window_front(f"{tag}_ent_win_{j}", 0.0, ent_c, zc, 1.05, 1.95, trim, glass, glow)

    # Stoop: eight chunky risers out to the sidewalk, solid balustrades.
    risers = 8
    tread = 0.30
    top_x = -0.42
    for s in range(risers):
        z_top = g + (BASE_H / risers) * (risers - s)
        box(f"{tag}_step_{s}", top_x - tread * (s + 1), top_x - tread * s,
            ent_c - 0.78, ent_c + 0.78, g, z_top, stone)
    run = tread * risers
    for j, yy in enumerate((ent_c - 0.90, ent_c + 0.90)):
        rail = [
            (top_x, yy - 0.11), (top_x - run, yy - 0.11),
            (top_x - run, yy + 0.11), (top_x, yy + 0.11),
        ]
        verts = [world(x, y, g) for x, y in rail]
        verts += [world(top_x, yy - 0.11, base_top + 0.95), world(top_x - run, yy - 0.11, g + 1.05),
                  world(top_x - run, yy + 0.11, g + 1.05), world(top_x, yy + 0.11, base_top + 0.95)]
        new_mesh(f"{tag}_rail_{j}", verts, BOX_FACES, trim, do_bevel=True, bevel_width=0.05)

    # 8. Garage opening and basement vents on the street-level wall.
    gar_c = bay_c - 0.10
    box(f"{tag}_garage_case", -0.08, 0.10, gar_c - 1.44, gar_c + 1.44,
        g + 0.05, g + 2.12, trim)
    box(f"{tag}_garage", -0.18, 0.20, gar_c - 1.22, gar_c + 1.22, g + 0.14, g + 1.90, ink)

    # 9. Slender chimney, set on the roof toward the rear.
    cx = 6.4 + (index % 3) * 1.1
    box(f"{tag}_chimney", cx, cx + 0.62, yc + 1.20, yc + 1.82, corn_top - 0.6,
        ridge + chimney_extra, brick, bevel=True, bevel_width=0.06)
    box(f"{tag}_chimney_cap", cx - 0.10, cx + 0.72, yc + 1.10, yc + 1.92,
        ridge + chimney_extra, ridge + chimney_extra + 0.16, trim)

    # 10. Rear elevation: plain but not blank.
    for j, (zc, wdt) in enumerate(((base_top + 1.8, 1.25), (f1_top + 1.75, 1.25))):
        window_rear(f"{tag}_rear_win_{j}", DEPTH, yc - 1.35, zc, wdt, 1.65, trim, glass)
        window_rear(f"{tag}_rear_win_b{j}", DEPTH, yc + 1.35, zc, wdt, 1.65, trim, glass)
    box(f"{tag}_rear_door", DEPTH - 0.22, DEPTH + 0.06, yc + 2.55, yc + 3.35,
        base_top, base_top + 2.1, ink)

    # 11. Flank windows only where a flank is actually exposed (the two end houses).
    if index == 0:
        for j, zc in enumerate((base_top + 1.9, f1_top + 1.9)):
            window_side(f"{tag}_flank_{j}", y0, -1, 4.6, zc, 1.1, 1.7, trim, glass)
            window_side(f"{tag}_flank_b{j}", y0, -1, 9.2, zc, 1.1, 1.7, trim, glass)
    if index == len(HOUSES) - 1:
        for j, zc in enumerate((base_top + 1.9, f1_top + 1.9)):
            window_side(f"{tag}_flank_{j}", y1, 1, 4.6, zc, 1.1, 1.7, trim, glass)
            window_side(f"{tag}_flank_b{j}", y1, 1, 9.2, zc, 1.1, 1.7, trim, glass)


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    for i, spec in enumerate(HOUSES):
        build_house(i, *spec)

    recenter_xy_and_ground()
    return scene


def recenter_xy_and_ground():
    """Origin at base centre: bbox centred in X/Y, minimum geometry Z at 0."""
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    for obj in meshes:
        for vert in obj.data.vertices:
            p = obj.matrix_world @ vert.co
            for i in range(3):
                mn[i] = min(mn[i], p[i])
                mx[i] = max(mx[i], p[i])
    offset = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, mn.z))
    for obj in meshes:
        for vert in obj.data.vertices:
            vert.co -= offset


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
    blend = os.path.join(out, "painted-ladies.blend")
    glb = os.path.join(out, "painted-ladies.glb")
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
