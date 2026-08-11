"""Deterministic Blender build of the SF-SIM streetscape furniture kit.

    blender -b --python build_streetkit.py -- [--out DIR]

Writes one GLB per piece plus streetkit_index.json into --out (default
app/public/sf-assets/streetkit/), and streetkit.blend next to this file.

Everything follows the sf-asset-check contract: metres, Z up, origin at the
base centre with min Z = 0, front facing -Y, flat `Toy_*` palette materials,
`_Glow` only where the piece is a light at night, no textures, no animation.

"Front is -Y" has one meaning across the whole kit: -Y points at the roadway.
A lamp's arm reaches out over -Y, a signal head looks down -Y at the traffic it
stops, a shelter and a bench open onto -Y, and the placement code only has to
yaw a piece so its -Y faces the kerb.

Sizes are the real objects nudged up the way the style bible's semantic scale
asks for (s.9): poles a touch stouter, lamp heads and signal lenses bigger than
scale, so they still read from the 42 degree diorama camera instead of aliasing
into a grey smudge. Triangles are spent on the silhouette — the pole, the arm,
the head — and never on detail that dies at that distance, which is what keeps
every piece inside the 300 tri vehicle-class budget (500 for the shelter, the
stall and the parklet, which are small buildings).
"""

import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

# --------------------------------------------------------------- the palette

PALETTE_HEX = {
    "Toy_cream": "f2ede3",
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    "Toy_ink": "3a3530",
    "Toy_steel": "9aa0a6",
    "Toy_roofd": "45454a",
    "Toy_navy": "2c4a70",
    "Toy_glass": "2a4d73",
    "Toy_teal": "3fa8a0",
    "Toy_coral": "e8735a",
    "Toy_mustard": "d9a441",
    "Toy_mint": "8fd0a8",
    "Toy_red": "c4453c",
    "Toy_rust": "a86444",
    "Toy_gold": "caa64a",
    "Toy_white": "f7f4ec",
    "Toy_verdigris": "9fb8a8",
    # Night surfaces. The lamp family shares one warm sodium glow so a street of
    # mixed lamp types still lights as one instrument at dusk.
    "Toy_gold_Glow": "caa64a",
    "Toy_white_Glow": "f7f4ec",
    "Toy_red_Glow": "c4453c",
    "Toy_mustard_Glow": "d9a441",
    "Toy_mint_Glow": "8fd0a8",
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
        # Flagged for the app's dusk pass; the daylight asset does not emit.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    mat.blend_method = "OPAQUE"
    return mat


# ------------------------------------------------------------------ geometry

PIECES = []  # (id, [objects]) in build order


def new_mesh(name, verts, faces, mat):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(v) for v in verts], [], faces)
    mesh.materials.append(material(mat))
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


def bevel(obj, width=0.012, segments=1):
    """Miniature edge softening (style bible s.4).

    One segment, not two: these are 0.2-1 m props whose whole triangle budget is
    the size of a single beveled box at two segments, and at the camera distance
    they are authored for a single chamfer already catches the light the same way
    the two-segment landmark bevels do.
    """
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


def rot2(x, y, ang):
    c, s = math.cos(ang), math.sin(ang)
    return (x * c - y * s, x * s + y * c)


def box(name, mat, cx, cy, z0, z1, sx, sy, yaw=0.0, chamfer=0.0):
    hx, hy = sx / 2, sy / 2
    corners = [rot2(x, y, yaw) for x, y in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy))]
    verts = [(cx + x, cy + y, z0) for x, y in corners]
    verts += [(cx + x, cy + y, z1) for x, y in corners]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    obj = new_mesh(name, verts, faces, mat)
    if chamfer:
        bevel(obj, chamfer)
    return obj


def frustum(name, mat, cx, cy, z0, z1, sx0, sy0, sx1, sy1):
    """A tapered box: planter tubs, anything with battered sides."""
    lo = ((-sx0 / 2, -sy0 / 2), (sx0 / 2, -sy0 / 2), (sx0 / 2, sy0 / 2), (-sx0 / 2, sy0 / 2))
    hi = ((-sx1 / 2, -sy1 / 2), (sx1 / 2, -sy1 / 2), (sx1 / 2, sy1 / 2), (-sx1 / 2, sy1 / 2))
    verts = [(cx + x, cy + y, z0) for x, y in lo] + [(cx + x, cy + y, z1) for x, y in hi]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_mesh(name, verts, faces, mat)


def wedge(name, mat, cx, cy, z0, z1, sx, sy0, sy1, yaw=0.0):
    """A box whose top face is narrower in Y — awnings, hydrant bonnets, lids."""
    hx = sx / 2
    lo = [rot2(x, y, yaw) for x, y in ((-hx, -sy0 / 2), (hx, -sy0 / 2), (hx, sy0 / 2), (-hx, sy0 / 2))]
    hi = [rot2(x, y, yaw) for x, y in ((-hx, -sy1 / 2), (hx, -sy1 / 2), (hx, sy1 / 2), (-hx, sy1 / 2))]
    verts = [(cx + x, cy + y, z0) for x, y in lo] + [(cx + x, cy + y, z1) for x, y in hi]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_mesh(name, verts, faces, mat)


def cyl(name, mat, cx, cy, z0, z1, r0, r1=None, seg=8, phase=0.0):
    r1 = r0 if r1 is None else r1
    verts = []
    for r, z in ((r0, z0), (r1, z1)):
        for i in range(seg):
            a = 2 * math.pi * i / seg + phase
            verts.append((cx + r * math.cos(a), cy + r * math.sin(a), z))
    faces = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i) for i in range(seg)]
    faces.append(tuple(range(seg - 1, -1, -1)))
    faces.append(tuple(range(seg, 2 * seg)))
    return new_mesh(name, verts, faces, mat)


def cyl_y(name, mat, cx, cy0, cy1, cz, r, seg=6):
    """A cylinder lying along Y: hydrant nozzles and other stubs."""
    obj = cyl(name, mat, 0, 0, 0, cy1 - cy0, r, seg=seg)
    obj.data.transform(Matrix.Translation((cx, cy0, cz)) @ Matrix.Rotation(math.radians(-90), 4, "X"))
    return obj


def dome(name, mat, cx, cy, cz, r, seg=8, rings=3, squash=1.0):
    """Upper half of a sphere; `squash` flattens it into a cap."""
    verts = []
    for j in range(rings):
        t = (j / rings) * (math.pi / 2)
        rr = r * math.cos(t)
        z = cz + r * math.sin(t) * squash
        for i in range(seg):
            a = 2 * math.pi * i / seg
            verts.append((cx + rr * math.cos(a), cy + rr * math.sin(a), z))
    top = len(verts)
    verts.append((cx, cy, cz + r * squash))
    faces = []
    for j in range(rings - 1):
        for i in range(seg):
            a0 = j * seg + i
            a1 = j * seg + (i + 1) % seg
            faces.append((a0, a1, a1 + seg, a0 + seg))
    for i in range(seg):
        faces.append(((rings - 1) * seg + i, (rings - 1) * seg + (i + 1) % seg, top))
    faces.append(tuple(range(seg - 1, -1, -1)))
    return new_mesh(name, verts, faces, mat)


def globe(name, mat, cx, cy, cz, r, seg=8, rings=3):
    """A closed low-segment sphere: the lamp globes and the shrub crowns."""
    verts = []
    for j in range(1, rings + 1):
        t = math.pi * j / (rings + 1)
        rr = r * math.sin(t)
        z = cz + r * math.cos(t)
        for i in range(seg):
            a = 2 * math.pi * i / seg
            verts.append((cx + rr * math.cos(a), cy + rr * math.sin(a), z))
    top = len(verts)
    verts.append((cx, cy, cz + r))
    bottom = top + 1
    verts.append((cx, cy, cz - r))
    faces = []
    for j in range(rings - 1):
        for i in range(seg):
            a0 = j * seg + i
            a1 = j * seg + (i + 1) % seg
            faces.append((a0, a1, a1 + seg, a0 + seg))
    for i in range(seg):
        faces.append((i, top, (i + 1) % seg))
        faces.append(((rings - 1) * seg + i, (rings - 1) * seg + (i + 1) % seg, bottom))
    return new_mesh(name, verts, faces, mat)


def bar(name, mat, p0, p1, w, h, mat_yaw=None):
    """A rectangular bar between two 3D points: lamp arms, mast arms, rails."""
    ax, ay, az = p0
    bx, by, bz = p1
    dx, dy, dz = bx - ax, by - ay, bz - az
    horiz = math.hypot(dx, dy)
    if horiz < 1e-6:
        return cyl(name, mat, ax, ay, min(az, bz), max(az, bz), w / 2, seg=6)
    ux, uy = dx / horiz, dy / horiz  # along, in plan
    nx, ny = -uy, ux  # across, in plan
    # The bar's cross-section stays vertical: it is a chunky miniature part, not
    # a swept tube, and a vertical section keeps the silhouette crisp from above.
    verts = []
    for (px, py, pz) in ((ax, ay, az), (bx, by, bz)):
        for sx, sz in ((-1, 0), (1, 0), (1, 1), (-1, 1)):
            verts.append((px + nx * sx * w / 2, py + ny * sx * w / 2, pz + sz * h))
    faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return new_mesh(name, verts, faces, mat)


# --------------------------------------------------------------- the pieces
#
# Every builder returns the objects it made. Ids and geometry are fixed: the
# script is the asset, so a re-run reproduces the same bytes.


def sl_standard():
    """The default citywide lamp: SF's davit-arm cobra head, semantically fat."""
    o = [
        cyl("base", "Toy_ink", 0, 0, 0, 0.45, 0.30, 0.26, seg=8),
        cyl("pole", "Toy_steel", 0, 0, 0.45, 7.4, 0.19, 0.15, seg=8),
    ]
    # Three chords instead of a swept curve: the davit reads as a curve from any
    # camera that can see this lamp at all, for a fifth of the triangles.
    arm = [(0, 0, 7.4), (0, -0.55, 8.05), (0, -1.5, 8.4), (0, -2.5, 8.5)]
    for i in range(3):
        o.append(bar(f"arm{i}", "Toy_steel", arm[i], arm[i + 1], 0.19, 0.19))
    o.append(box("head", "Toy_ink", 0, -3.00, 8.24, 8.62, 0.62, 1.45, chamfer=0.04))
    # The lens is the light: a slab on the underside, so the glow reads as a
    # lit fixture from the diorama camera and not as a floating bead.
    o.append(box("lens", "Toy_gold_Glow", 0, -3.05, 8.14, 8.26, 0.52, 1.20))
    return o


def sl_pathofgold():
    """Market Street's Path of Gold: fluted column, twin globes on a cross arm."""
    o = [
        box("plinth", "Toy_ink", 0, 0, 0, 0.30, 0.62, 0.62, chamfer=0.03),
        cyl("collar", "Toy_ink", 0, 0, 0.30, 0.62, 0.26, 0.22, seg=8),
        cyl("column", "Toy_verdigris", 0, 0, 0.62, 5.15, 0.17, 0.12, seg=8),
        cyl("capital", "Toy_gold", 0, 0, 5.15, 5.45, 0.20, 0.16, seg=8),
        bar("crossarm", "Toy_verdigris", (-1.15, 0, 5.45), (1.15, 0, 5.45), 0.12, 0.14),
    ]
    for side in (-1, 1):
        o.append(cyl(f"stem{side}", "Toy_gold", side * 1.15, 0, 5.45, 5.72, 0.09, 0.07, seg=6))
        o.append(globe(f"globe{side}", "Toy_gold_Glow", side * 1.15, 0, 6.15, 0.46, seg=8, rings=2))
    o.append(cyl("finial", "Toy_gold", 0, 0, 5.45, 5.95, 0.11, 0.02, seg=6))
    return o


def sl_residential():
    """The short lantern lamp for residential blocks: acorn on a stubby post."""
    o = [
        cyl("base", "Toy_ink", 0, 0, 0, 0.34, 0.22, 0.18, seg=8),
        cyl("pole", "Toy_ink", 0, 0, 0.34, 4.25, 0.11, 0.09, seg=8),
        cyl("collar", "Toy_ink", 0, 0, 4.25, 4.42, 0.17, 0.14, seg=8),
        # Acorn: a short taper up into the glass, then the cap.
        cyl("lantern", "Toy_gold_Glow", 0, 0, 4.42, 5.15, 0.20, 0.30, seg=8),
        cyl("shoulder", "Toy_gold_Glow", 0, 0, 5.15, 5.35, 0.30, 0.22, seg=8),
        dome("cap", "Toy_ink", 0, 0, 5.35, 0.26, seg=8, rings=2, squash=0.75),
    ]
    return o


def traffic_signal():
    """Mast-arm signal: three-lens head over the roadway plus a kerbside ped head."""
    o = [
        box("base", "Toy_ink", 0, 0, 0, 0.30, 0.52, 0.52, chamfer=0.03),
        cyl("pole", "Toy_ink", 0, 0, 0.30, 6.30, 0.15, 0.12, seg=8),
        bar("mast", "Toy_ink", (0, 0, 6.20), (0, -3.30, 6.20), 0.18, 0.18),
        box("head", "Toy_ink", 0, -3.30, 4.40, 6.20, 0.70, 0.52, chamfer=0.04),
    ]
    # Red, amber, green as fat lenses on the -Y face: at diorama scale the lens
    # colour is the only thing that says "signal", so it is oversized (s.9).
    for i, mat in enumerate(("Toy_red_Glow", "Toy_mustard_Glow", "Toy_mint_Glow")):
        z = 5.86 - i * 0.54
        o.append(box(f"lens{i}", mat, 0, -3.60, z, z + 0.42, 0.52, 0.10))
        o.append(box(f"visor{i}", "Toy_ink", 0, -3.72, z + 0.40, z + 0.46, 0.58, 0.28))
    o.append(box("pedbox", "Toy_ink", 0, -0.28, 2.60, 3.36, 0.52, 0.38, chamfer=0.03))
    o.append(box("pedface", "Toy_white_Glow", 0, -0.49, 2.74, 3.22, 0.40, 0.06))
    return o


def hydrant():
    """SF hydrant. High-pressure-system hydrants are colour-coded; this is the
    common mustard-topped coral body, which also happens to be the accent the
    style bible wants at kerbside (s.7)."""
    o = [
        cyl("foot", "Toy_ink", 0, 0, 0, 0.10, 0.26, 0.24, seg=8),
        cyl("body", "Toy_coral", 0, 0, 0.10, 0.62, 0.19, 0.17, seg=8),
        cyl("shoulder", "Toy_coral", 0, 0, 0.62, 0.72, 0.22, 0.19, seg=8),
        dome("bonnet", "Toy_mustard", 0, 0, 0.72, 0.19, seg=8, rings=2, squash=0.85),
        cyl("cap", "Toy_mustard", 0, 0, 0.88, 0.96, 0.07, 0.06, seg=6),
        # The pumper nozzle points at the roadway, which is what fixes the
        # hydrant's facing to the kit's -Y convention.
        cyl_y("nozzle", "Toy_mustard", 0, -0.30, -0.14, 0.44, 0.10),
        cyl_y("portL", "Toy_mustard", -0.21, -0.06, 0.06, 0.40, 0.07),
        cyl_y("portR", "Toy_mustard", 0.21, -0.06, 0.06, 0.40, 0.07),
    ]
    return o


def mailbox():
    """USPS collection box: navy, domed lid, pull handle, two stubby feet."""
    o = [
        box("body", "Toy_navy", 0, 0, 0.16, 1.05, 0.62, 0.50, chamfer=0.02),
        wedge("lid", "Toy_navy", 0, 0.02, 1.05, 1.26, 0.62, 0.50, 0.34),
        box("hatch", "Toy_navy", 0, -0.27, 0.86, 1.10, 0.50, 0.06, chamfer=0.015),
        box("handle", "Toy_steel", 0, -0.32, 0.94, 1.00, 0.26, 0.05),
        box("legL", "Toy_ink", -0.19, 0, 0, 0.16, 0.10, 0.40),
        box("legR", "Toy_ink", 0.19, 0, 0, 0.16, 0.10, 0.40),
    ]
    return o


def muni_shelter():
    """Muni stop: glass back and side, a cantilevered roof, a bench and the lit
    schedule panel that is the piece's only night surface."""
    o = [
        box("roof", "Toy_steel", 0, 0.05, 2.62, 2.76, 4.40, 1.75, chamfer=0.03),
        box("fascia", "Toy_steel", 0, -0.82, 2.46, 2.66, 4.40, 0.10),
        box("back", "Toy_glass", 0, 0.78, 0.35, 2.55, 4.10, 0.08),
        box("endL", "Toy_glass", -2.06, 0.20, 0.35, 2.55, 0.08, 1.25),
        box("endR", "Toy_glass", 2.06, 0.20, 0.35, 2.55, 0.08, 1.25),
        box("postL", "Toy_steel", -2.10, -0.72, 0, 2.62, 0.12, 0.12),
        box("postR", "Toy_steel", 2.10, -0.72, 0, 2.62, 0.12, 0.12),
        box("backpostL", "Toy_steel", -2.10, 0.80, 0, 2.62, 0.12, 0.12),
        box("backpostR", "Toy_steel", 2.10, 0.80, 0, 2.62, 0.12, 0.12),
        box("bench", "Toy_stone", 0, 0.52, 0.44, 0.52, 3.30, 0.44, chamfer=0.02),
        box("benchleg", "Toy_steel", 0, 0.52, 0, 0.44, 0.14, 0.32),
        # The lit panel: timetable at one end, the whole reason a stop reads at
        # night. Small on purpose — a shelter is not a lantern.
        box("panel", "Toy_white_Glow", 1.62, -0.78, 1.05, 2.35, 0.66, 0.05),
    ]
    return o


def bench():
    o = [
        box("seat", "Toy_rust", 0, 0, 0.44, 0.52, 1.85, 0.52, chamfer=0.02),
        box("backrest", "Toy_rust", 0, 0.24, 0.52, 0.94, 1.85, 0.06, chamfer=0.02),
        box("legL", "Toy_ink", -0.72, 0, 0, 0.44, 0.09, 0.46),
        box("legR", "Toy_ink", 0.72, 0, 0, 0.44, 0.09, 0.46),
        box("armL", "Toy_ink", -0.90, 0, 0.44, 0.68, 0.07, 0.48),
        box("armR", "Toy_ink", 0.90, 0, 0.44, 0.68, 0.07, 0.48),
    ]
    return o


def trashcan():
    o = [
        cyl("body", "Toy_ink", 0, 0, 0, 0.86, 0.29, 0.32, seg=10),
        cyl("rim", "Toy_steel", 0, 0, 0.86, 0.94, 0.34, 0.34, seg=10),
        dome("lid", "Toy_steel", 0, 0, 0.94, 0.32, seg=10, rings=2, squash=0.45),
    ]
    return o


def newsboxes():
    """A rack of three: the cluster is the piece, so a kerb gets one instance,
    not three coincident ones."""
    o = []
    colors = ("Toy_teal", "Toy_mustard", "Toy_red")
    for i, mat in enumerate(colors):
        x = (i - 1) * 0.56
        o.append(box(f"body{i}", mat, x, 0, 0.22, 1.02, 0.50, 0.42, chamfer=0.02))
        o.append(wedge(f"hood{i}", mat, x, -0.03, 1.02, 1.20, 0.50, 0.42, 0.30))
        o.append(box(f"window{i}", "Toy_glass", x, -0.22, 0.66, 1.00, 0.38, 0.04))
        o.append(box(f"legs{i}", "Toy_ink", x, 0, 0, 0.22, 0.42, 0.30))
    return o


def planter():
    o = [
        frustum("tub", "Toy_stone", 0, 0, 0, 0.66, 0.84, 0.84, 1.00, 1.00),
        box("soil", "Toy_rust", 0, 0, 0.62, 0.68, 0.94, 0.94),
        globe("shrubA", "Toy_mint", -0.13, 0.05, 0.98, 0.33, seg=8, rings=2),
        globe("shrubB", "Toy_mint", 0.17, -0.09, 0.90, 0.26, seg=8, rings=2),
    ]
    return o


def bikerack():
    """Three inverted-U hoops on a common footing."""
    o = [box("foot", "Toy_stone", 0, 0, 0, 0.06, 2.30, 0.34, chamfer=0.02)]
    for i in (-1, 0, 1):
        x = i * 0.85
        o.append(cyl(f"legA{i}", "Toy_steel", x, -0.30, 0.02, 0.78, 0.045, seg=5))
        o.append(cyl(f"legB{i}", "Toy_steel", x, 0.30, 0.02, 0.78, 0.045, seg=5))
        o.append(bar(f"hoop{i}", "Toy_steel", (x, -0.30, 0.78), (x, 0.30, 0.78), 0.09, 0.09))
    return o


def cafe_set():
    """Two chairs, a table and the umbrella that is the block's colour accent."""
    o = [
        cyl("tablefoot", "Toy_ink", 0, 0, 0, 0.06, 0.34, 0.34, seg=8),
        cyl("tablepost", "Toy_ink", 0, 0, 0.06, 0.72, 0.06, 0.06, seg=6),
        cyl("tabletop", "Toy_trim", 0, 0, 0.72, 0.78, 0.52, 0.52, seg=8),
    ]
    for side in (-1, 1):
        y = side * 0.78
        o.append(box(f"seat{side}", "Toy_teal", 0, y, 0.42, 0.48, 0.46, 0.46, chamfer=0.02))
        o.append(box(f"back{side}", "Toy_teal", 0, y + side * 0.20, 0.48, 0.92, 0.46, 0.05))
        o.append(cyl(f"chairpost{side}", "Toy_ink", 0, y, 0, 0.42, 0.05, 0.07, seg=5))
    # Umbrella: the only saturated mass at this scale, deliberately oversized so
    # a cafe cluster reads as one warm dot from the aerial camera (s.9, s.16).
    o.append(cyl("mast", "Toy_ink", 0, 0, 0.78, 2.18, 0.05, 0.05, seg=6))
    o.append(cyl("canopy", "Toy_coral", 0, 0, 2.02, 2.40, 0.95, 0.10, seg=8))
    return o


def market_stall():
    """A striped-awning stall: four posts, a counter, crates of produce."""
    o = [
        box("counter", "Toy_trim", 0, -0.30, 0.68, 0.80, 2.60, 1.05, chamfer=0.02),
        box("apron", "Toy_stone", 0, -0.30, 0.10, 0.68, 2.50, 0.95),
    ]
    for sx in (-1, 1):
        for sy in (-1, 1):
            o.append(box(f"post{sx}{sy}", "Toy_ink", sx * 1.30, sy * 0.80 - 0.30, 0, 2.40, 0.10, 0.10))
    o.append(bar("beamF", "Toy_ink", (-1.35, -1.10, 2.30), (1.35, -1.10, 2.30), 0.09, 0.10))
    o.append(bar("beamB", "Toy_ink", (-1.35, 0.50, 2.30), (1.35, 0.50, 2.30), 0.09, 0.10))
    # Awning: alternating stripes, slanted forward over the counter.
    for i in range(5):
        mat = "Toy_red" if i % 2 == 0 else "Toy_trim"
        x = -1.44 + i * 0.60
        verts = [
            (x, 0.55, 2.42),
            (x + 0.60, 0.55, 2.42),
            (x + 0.60, -1.35, 2.05),
            (x, -1.35, 2.05),
            (x, 0.55, 2.36),
            (x + 0.60, 0.55, 2.36),
            (x + 0.60, -1.35, 1.99),
            (x, -1.35, 1.99),
        ]
        faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
        o.append(new_mesh(f"awning{i}", verts, faces, mat))
    o.append(box("crateA", "Toy_mustard", -0.75, -0.62, 0.80, 1.02, 0.72, 0.52, chamfer=0.02))
    o.append(box("crateB", "Toy_mint", 0.10, -0.62, 0.80, 0.98, 0.66, 0.52, chamfer=0.02))
    o.append(box("crateC", "Toy_coral", 0.85, -0.62, 0.80, 1.06, 0.62, 0.52, chamfer=0.02))
    return o


def parklet():
    """A curbside parklet on one parking slot: deck, rail, planters, bench.

    Its long axis is X, matching the kerb, and the open side faces +Y (the
    sidewalk) while -Y is the traffic side that carries the rail — the same
    -Y-is-the-road convention as every other piece.
    """
    o = [
        box("deck", "Toy_rust", 0, 0, 0.14, 0.26, 6.00, 2.10, chamfer=0.02),
        box("skirt", "Toy_ink", 0, 0, 0, 0.14, 5.90, 2.00),
    ]
    for x in (-2.85, -0.95, 0.95, 2.85):
        o.append(box(f"post{x}", "Toy_ink", x, -0.98, 0.26, 1.05, 0.10, 0.10))
    o.append(bar("rail", "Toy_ink", (-2.95, -0.98, 0.98), (2.95, -0.98, 0.98), 0.08, 0.09))
    o.append(box("bench", "Toy_rust", -1.20, 0.72, 0.26, 0.72, 2.40, 0.50, chamfer=0.02))
    o.append(box("benchback", "Toy_rust", -1.20, 0.95, 0.72, 1.15, 2.40, 0.06, chamfer=0.02))
    o.append(frustum("tub", "Toy_teal", 2.05, 0.55, 0.26, 0.98, 0.78, 0.78, 0.94, 0.94))
    o.append(globe("shrub", "Toy_mint", 2.05, 0.55, 1.26, 0.40, seg=8, rings=2))
    return o


BUILDERS = [
    ("sl_standard", sl_standard),
    ("sl_pathofgold", sl_pathofgold),
    ("sl_residential", sl_residential),
    ("traffic_signal", traffic_signal),
    ("hydrant", hydrant),
    ("mailbox", mailbox),
    ("muni_shelter", muni_shelter),
    ("bench", bench),
    ("trashcan", trashcan),
    ("newsboxes", newsboxes),
    ("planter", planter),
    ("bikerack", bikerack),
    ("cafe_set", cafe_set),
    ("market_stall", market_stall),
    ("parklet", parklet),
]


# --------------------------------------------------------------------- build


def measure(objs):
    dg = bpy.context.evaluated_depsgraph_get()
    mn = [1e12] * 3
    mx = [-1e12] * 3
    tris = 0
    mats = set()
    for obj in objs:
        ev = obj.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for m in me.materials:
            if m:
                mats.add(m.name)
        for v in me.vertices:
            w = obj.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
        ev.to_mesh_clear()
    return mn, mx, tris, sorted(mats)


def ground_and_centre(objs):
    """Contract rule 2: min z = 0, centred in x/y. Done by moving geometry, not
    the object transforms, so the export needs no applied transforms."""
    mn, mx, _, _ = measure(objs)
    offset = Vector((-(mn[0] + mx[0]) / 2, -(mn[1] + mx[1]) / 2, -mn[2]))
    for obj in objs:
        obj.data.transform(Matrix.Translation(offset))
    return offset


def export(objs, path):
    for scene in bpy.data.scenes:
        for obj in scene.objects:
            obj.select_set(False)
    for obj in objs:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.gltf(
        filepath=path,
        export_format="GLB",
        export_apply=True,
        export_yup=True,
        use_selection=True,
        export_cameras=False,
        export_lights=False,
        export_animations=False,
        export_skins=False,
        export_morph=False,
        export_materials="EXPORT",
        export_image_format="NONE",
    )


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))
    default_out = os.path.abspath(
        os.path.join(here, "..", "..", "app", "public", "sf-assets", "streetkit")
    )
    out = argv[argv.index("--out") + 1] if "--out" in argv else default_out
    os.makedirs(out, exist_ok=True)

    bpy.ops.wm.read_factory_settings(use_empty=True)

    entries = []
    for piece_id, builder in BUILDERS:
        collection = bpy.data.collections.new(piece_id)
        bpy.context.scene.collection.children.link(collection)
        layer = bpy.context.view_layer.layer_collection.children[collection.name]
        bpy.context.view_layer.active_layer_collection = layer

        objs = builder()
        for obj in objs:
            obj.name = f"{piece_id}_{obj.name}"
        ground_and_centre(objs)
        mn, mx, tris, mats = measure(objs)
        dims = [round(mx[i] - mn[i], 3) for i in range(3)]
        path = os.path.join(out, f"{piece_id}.glb")
        export(objs, path)
        entries.append(
            {
                "id": piece_id,
                "file": f"{piece_id}.glb",
                "dims": dims,
                "tris": tris,
                "materials": mats,
                "glow": [m for m in mats if m.endswith("_Glow")],
            }
        )
        print(f"[build] {piece_id:15s} tris={tris:4d} dims={dims} mats={len(mats)}")

    index = {
        "version": 1,
        "note": (
            "Streetscape furniture kit (layer 2). Built by "
            "artifacts/streetkit/build_streetkit.py; every piece is metres, "
            "base-centre origin at z=0, front -Y = the roadway side."
        ),
        "pieces": entries,
    }
    with open(os.path.join(out, "streetkit_index.json"), "w", encoding="utf8") as fh:
        json.dump(index, fh, indent=1)
        fh.write("\n")
    print(f"[build] wrote {out}/streetkit_index.json ({len(entries)} pieces)")

    blend = os.path.join(here, "streetkit.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    print(f"[build] wrote {blend}")


if __name__ == "__main__":
    main()
