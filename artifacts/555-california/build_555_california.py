"""Deterministic Blender build of the SF-SIM miniature 555 California Street.

    blender -b --python build_555_california.py -- [--out DIR]

Writes 555-california.blend and 555-california.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, origin at the base centre, min Z = 0, so the export needs no
transforms applied after the fact and the loader's placeGeneric only has to
scale and position it.

Design (every number is sourced in REFERENCE.md):

* the real plate - 74.51 x 44.45 m, long axis 81.23 deg clockwise from true
  north, all four corners chamfered by one bay module. NOTE the raw OSM outline
  way is 84 m long because it includes the one-storey east podium; the tower
  itself is the shorter figure, cross-checked against Vornado's published
  ~30,000 RSF floor plate;
* the signature sawtooth bay-window skin: a granite nose pier at each apex,
  canted granite cheeks, and a recessed glazed valley between them, at the real
  6.21 m pitch and 2.1 m throw, 12 modules per long face and 7 per short end,
  unbroken from the arcade to the parapet. This is the one cue that must be
  right. The real bay glazes its canted flanks instead; moving the glazing into
  the valley keeps the granite dominant at the city camera, which is what makes
  the tower read as the warm stone mass it is (REFERENCE.md s.6);
* the "irregular cutout areas near the top... designed to suggest the Sierra
  Nevada": shallow, deliberately unequal terraces on different sides at each of
  three levels between 196 and 226 m, with the four chamfered corner masses
  running full height through all of them;
* one strong horizontal accent, the mechanical louvre band at ~157 m;
* the blank granite mechanical penthouse between the 226 m main parapet and the
  237.4 m architectural top, its sawtooth continued as solid stone;
* a deep granite entrance arcade at the base, on the low plaza podium;
* night state built for the app's dusk system. The real tower has no facade
  floodlighting and no crown lighting - it is a dark mass with scattered lit
  offices over a warmly lit arcade, plus the red FAA obstruction lights on the
  penthouse. That, and nothing more, is what is modelled.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

H_ARCH = 237.4  # architectural top = mechanical penthouse (CTBUH, 779 ft)
H_ROOF = 225.6  # main roof deck, 740 ft above plaza (USGS 3DEP lidar)
H_PODIUM = 1.6  # raised granite plaza podium
H_ARCADE = 10.0  # top of the entrance arcade
H_SHAFT = 12.0  # shaft springs above the arcade lintel
FLOOR = 3.96  # 13 ft slab-to-slab (Vornado), used by the night skin
PODIUM_COLLAR = 3.2  # how far the podium plinth stands proud of the tower
LOUVRE_Z = (67.4, 114.9)  # the two mechanical floors, 15th and 27th

# Published plan: 243 x 143 ft (SkyscraperPage, Emporis archive), which closes
# exactly as 11 x 20 ft bays plus an 11.5 ft chamfered corner bay at each end.
PLAN_L = 74.07  # 243 ft
PLAN_W = 43.59  # 143 ft
CHAMFER = 3.50  # 45 deg corner cut, 11.5 ft consumed along each face
YAW = math.radians(9.10)  # long axis at bearing 80.9 deg cw from true north

# Bay module: 6.21 m pitch, 2.1 m throw. The real bay glazes its canted flanks;
# the miniature moves the glazing into the valley so the granite reads as the
# dominant material at the city camera (see REFERENCE.md s.6).
MODULE = 6.096  # nominal 20 ft structural/facade module
BAY_DEPTH = 2.2  # ~7 ft, measured off the roof parapet zigzag in nadir aerials
F_NOSE = 0.22  # granite nose pier at the outer apex
F_CHEEK = 0.17  # canted granite cheek down to the valley
F_FACE = 0.44  # recessed glazed valley face

# The Sierra Nevada crown. Shallow, deliberately unequal steps on different
# sides at each level - never a symmetric wedding cake. The four chamfered
# corner masses are built separately and run full height through all of them.
# (z_top, x0, x1, y0, y1)
# "While each of the four corners rises the whole 52 floors, the middle of each
# face is set back on the upper floors" (SFYIMBY). So the crown is built by
# notching the MIDDLE of each face by one bay module, with the notch widening -
# not deepening - at each level, and spanning different runs on every face.
# (z_top, {face: (t0, t1, depth)})
CROWN_BASE = 196.0
NOTCH = 6.1  # one bay module
STAGES = [
    (CROWN_BASE, {}),
    (206.0, {"north": (0.30, 0.62, NOTCH), "south": (0.42, 0.72, NOTCH)}),
    (216.0, {"north": (0.18, 0.74, NOTCH), "south": (0.30, 0.84, NOTCH), "west": (0.25, 0.75, NOTCH)}),
    (H_ROOF, {"north": (0.10, 0.84, NOTCH), "south": (0.18, 0.90, NOTCH),
              "west": (0.14, 0.86, NOTCH), "east": (0.30, 0.70, NOTCH)}),
]
PENTHOUSE_INSET = 11.7  # granite penthouse, ~50.7 x 20.2 m, +40 ft

LIT_DENSITY = 0.15  # fraction of office panes lit at night
LIT_SEED = 5.37

# Project palette from .agents/skills/sf-asset-check (hex, sRGB). Materials are
# authored with the linear equivalents, which is what the shipped kit GLBs hold.
PALETTE_HEX = {
    "Toy_rust": "a86444",  # carnelian granite - nearest palette entry
    "Toy_glass": "2a4d73",
    "Toy_stone": "d9d2c2",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_ink": "3a3530",
    "Toy_sand_Glow": "ece4d4",  # warm office light, matches the baked city
    "Toy_gold_Glow": "caa64a",
    "Toy_red_Glow": "c4453c",  # FAA red obstruction lighting (DOF 06-000484)
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

HL, HW = PLAN_L / 2, PLAN_W / 2


# --------------------------------------------------------------- plan shapes


def rot2(p, ang=YAW):
    c, s = math.cos(ang), math.sin(ang)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def hash01(n):
    """Deterministic 0..1 from a number, so the lit pattern is stable per build."""
    x = math.sin(n * 12.9898) * 43758.5453
    return x - math.floor(x)


def plan_poly(x0=None, x1=None, y0=None, y1=None, inset=0.0, chamfer=CHAMFER, notches=None):
    """Chamfered-rectangle plan, CCW and yawed onto the city grid.

    `notches` maps a face name to (t0, t1, depth): the stretch of that face
    between those fractions steps back by `depth`. Only the four straight faces
    can be notched, never the chamfered corners - which is exactly how the real
    crown works, with the corners running the full 52 floors while the middle of
    each face erodes away above roughly floor 40.
    """
    notches = notches or {}
    x0 = -HL + inset if x0 is None else x0
    x1 = HL - inset if x1 is None else x1
    y0 = -HW + inset if y0 is None else y0
    y1 = HW - inset if y1 is None else y1
    c = max(0.5, min(chamfer, (x1 - x0) * 0.4, (y1 - y0) * 0.4))
    edges = [
        ("south", (x0 + c, y0), (x1 - c, y0)),
        ("se", (x1 - c, y0), (x1, y0 + c)),
        ("east", (x1, y0 + c), (x1, y1 - c)),
        ("ne", (x1, y1 - c), (x1 - c, y1)),
        ("north", (x1 - c, y1), (x0 + c, y1)),
        ("nw", (x0 + c, y1), (x0, y1 - c)),
        ("west", (x0, y1 - c), (x0, y0 + c)),
        ("sw", (x0, y0 + c), (x0 + c, y0)),
    ]
    pts = []
    for name, a, b in edges:
        pts.append(a)
        nt = notches.get(name)
        if not nt:
            continue
        t0, t1, depth = nt
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1.0
        nx, ny = dy / length, -dx / length  # outward for a CCW loop
        for t, off in ((t0, 0.0), (t0, depth), (t1, depth), (t1, 0.0)):
            pts.append((a[0] + dx * t - nx * off, a[1] + dy * t - ny * off))
    return [rot2(p) for p in pts]


def serrate(poly, depth=BAY_DEPTH, solid_edges=(1, 3, 5, 7)):
    """Lay sawtooth bay-window modules around an outline.

    The supplied loop is the OUTER nose plane; granite cheeks cant inward to a
    glazed valley `depth` behind it. Returns (points, seg_kind) where
    seg_kind[i] describes the segment from points[i] to points[i+1]:
    0 = granite (nose or cheek), 1 = glazed valley face.

    Edges listed in `solid_edges` keep their sawtooth relief but are glazed
    nowhere: those are the four chamfered corners, which the photographs show as
    granite-dominant piers running the full height of the tower and anchoring
    the silhouette through every crown terrace.
    """
    pts, kind = [], []
    n = len(poly)
    for i in range(n):
        solid = i in solid_edges
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % n]
        ex, ey = bx - ax, by - ay
        length = math.hypot(ex, ey)
        if length < 0.9:
            continue
        if length < MODULE * 1.15:
            # A notch return wall: too short to carry a bay, so keep it a flat
            # granite reveal rather than letting it sprout a stray fin.
            pts.append((ax, ay))
            kind.append(0)
            continue
        tx, ty = ex / length, ey / length
        nx, ny = ty, -tx  # poly is CCW -> outward
        count = max(1, round(length / MODULE))
        m = length / count
        for k in range(count):
            u = k * m
            spans = (
                (u, 0.0, 0),  # granite nose face, outer apex
                (u + m * F_NOSE, 0.0, 0),  # granite cheek cants inward
                (u + m * (F_NOSE + F_CHEEK), -depth, 0 if solid else 1),  # valley face
                (u + m * (F_NOSE + F_CHEEK + F_FACE), -depth, 0),  # cheek back out
            )
            for su, sd, sk in spans:
                pts.append((ax + tx * su + nx * sd, ay + ty * su + ny * sd))
                kind.append(sk)
    return pts, kind


def offset_poly(poly, offset):
    """Push a convex outline out (or in) by a constant distance."""
    out = []
    n = len(poly)
    for i in range(n):
        px, py = poly[i]
        ax, ay = poly[(i - 1) % n]
        bx, by = poly[(i + 1) % n]
        n1 = _edge_normal(ax, ay, px, py)
        n2 = _edge_normal(px, py, bx, by)
        nx, ny = n1[0] + n2[0], n1[1] + n2[1]
        mag = math.hypot(nx, ny) or 1.0
        cosang = max(0.4, (n1[0] * n2[0] + n1[1] * n2[1] + 1.0) / 2.0) ** 0.5
        out.append((px + nx / mag * offset / cosang, py + ny / mag * offset / cosang))
    return out


def _edge_normal(ax, ay, bx, by):
    ex, ey = bx - ax, by - ay
    m = math.hypot(ex, ey) or 1.0
    return (ey / m, -ex / m)


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


def bevel(obj, width=0.14, segments=2):
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


def prism(name, pts, z0, z1, materials, seg_mats=None, cap_mat=0):
    """Extrude a closed CCW plan loop into a capped solid.

    The caps are filled with bmesh rather than fanned from a centroid. A fan is
    fine for a convex outline but produces slivers on these plans: the crown
    notches run almost radially from the centre, so a fan lays near-degenerate
    triangles along their return walls and the normals there become ambiguous.
    """
    n = len(pts)
    verts = [(x, y, z0) for x, y in pts] + [(x, y, z1) for x, y in pts]
    faces, face_mats = [], []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
        face_mats.append(seg_mats[i] if seg_mats else 0)
    obj = new_mesh(name, verts, faces, materials, face_mats, recalc=False)

    bm = bmesh.new()
    bm.from_mesh(obj.data)
    boundary = [e for e in bm.edges if len(e.link_faces) == 1]
    filled = bmesh.ops.holes_fill(bm, edges=boundary, sides=0)["faces"]
    for f in filled:
        f.material_index = cap_mat
    if filled:
        bmesh.ops.triangulate(bm, faces=filled, quad_method="BEAUTY", ngon_method="BEAUTY")
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def band(name, pts_in, pts_out, z0, z1, mat):
    """A closed ring standing between two plan loops: outer wall plus lip faces."""
    n = len(pts_in)
    verts = []
    for loop, z in ((pts_in, z0), (pts_out, z0), (pts_out, z1), (pts_in, z1)):
        verts.extend([(x, y, z) for x, y in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * n, ((k + 1) % 4) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])


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


# ---------------------------------------------------------------- night skin
#
# The app splits a landmark by material name: `_Glow` faces become a separate
# MeshBasicMaterial buffer whose opacity is driven by `uNight` (0.12 by day,
# ~1 at night). A glow face is therefore nearly transparent in daylight, so the
# lit surfaces are added ON TOP of the solid body rather than carved out of it -
# the daylight silhouette is untouched and only the panes ignite.


def lit_panes(name, stages, mat, density=LIT_DENSITY, seed=LIT_SEED, out=0.07):
    """Scattered warm office panes over the glazed flanks of every stage."""
    verts, faces = [], []
    for si, (pts, kind, z0, z1) in enumerate(stages):
        n = len(pts)
        floors = max(1, int((z1 - z0 - 1.2) // FLOOR))
        for i in range(n):
            if kind[i] != 1:
                continue
            j = (i + 1) % n
            ax, ay = pts[i]
            bx, by = pts[j]
            ex, ey = bx - ax, by - ay
            m = math.hypot(ex, ey) or 1.0
            nx, ny = ey / m * out, -ex / m * out
            inset = 0.12
            p0 = (ax + ex * inset + nx, ay + ey * inset + ny)
            p1 = (ax + ex * (1 - inset) + nx, ay + ey * (1 - inset) + ny)
            for f in range(floors):
                if hash01(seed + si * 71.3 + i * 13.17 + f * 3.71) > density:
                    continue
                za = z0 + 0.8 + f * FLOOR + 0.55
                zb = za + FLOOR - 1.5
                k = len(verts)
                verts.extend(
                    [
                        (p0[0], p0[1], za),
                        (p1[0], p1[1], za),
                        (p1[0], p1[1], zb),
                        (p0[0], p0[1], zb),
                    ]
                )
                faces.append((k, k + 1, k + 2, k + 3))
    if not faces:
        raise RuntimeError(f"{name}: no lit panes")
    return new_mesh(name, verts, faces, [mat], recalc=False)


def glow_ring(name, poly, z0, z1, mat, out=0.06):
    """Thin outward-facing luminous line following a plan loop."""
    ring = offset_poly(poly, out)
    n = len(ring)
    verts = [(x, y, z0) for x, y in ring] + [(x, y, z1) for x, y in ring]
    faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return new_mesh(name, verts, faces, [mat], recalc=False)


# --------------------------------------------------------------------- build


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    rust = material("Toy_rust")
    glass = material("Toy_glass")
    stone = material("Toy_stone")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    ink = material("Toy_ink")
    lit = material("Toy_sand_Glow")
    gold = material("Toy_gold_Glow")
    red = material("Toy_red_Glow")

    # --- plaza podium: the low granite plinth the tower stands on ----------
    bevel(prism("plaza_podium", plan_poly(inset=-PODIUM_COLLAR), 0.0, H_PODIUM, [stone]), width=0.28)

    # --- entrance arcade: deep granite piers, glazing well behind them -----
    base_poly = plan_poly()
    prism("arcade_glass", offset_poly(base_poly, -3.0), H_PODIUM, H_ARCADE, [glass])

    n = len(base_poly)
    idx = 0
    for i in range(n):
        ax, ay = base_poly[i]
        bx, by = base_poly[(i + 1) % n]
        ex, ey = bx - ax, by - ay
        length = math.hypot(ex, ey)
        if length < 1.0:
            continue
        tx, ty = ex / length, ey / length
        count = max(1, round(length / MODULE))
        m = length / count
        for k in range(count):
            u = (k + 0.5) * m
            bevel(
                box(
                    f"arcade_pier_{idx}",
                    ax + tx * u,
                    ay + ty * u,
                    H_PODIUM,
                    H_ARCADE,
                    2.4,
                    2.6,
                    rust,
                    yaw=math.atan2(ty, tx),
                ),
                width=0.18,
            )
            idx += 1

    bevel(band("arcade_sill", offset_poly(base_poly, -3.4), offset_poly(base_poly, 1.0), H_PODIUM, H_PODIUM + 1.0, rust), width=0.16)
    # The second-floor setback the arcade sits beneath.
    bevel(band("arcade_lintel", offset_poly(base_poly, -1.4), offset_poly(base_poly, 1.4), H_ARCADE, H_SHAFT, rust), width=0.2)

    # --- shaft: sawtooth skin, terracing into the Sierra Nevada crown ------
    z = H_SHAFT
    stages = []
    for si, (z_top, notches) in enumerate(STAGES):
        # Stages overlap by 0.6 m so no two solids ever share a plane: coincident
        # faces both z-fight in the app and make ray tests ambiguous.
        if si:
            z -= 0.6
        poly = plan_poly(notches=notches)
        pts, kind = serrate(poly)
        seg_mats = [1 if k == 1 else 0 for k in kind]
        # Granite caps: the terraces are stone ledges and the parapet edge is
        # "crenellated by the bay noses", which the sawtooth cap gives for free.
        prism(f"shaft_{si}", pts, z, z_top, [rust, glass], seg_mats, cap_mat=0)
        stages.append((pts, kind, z, z_top))
        z = z_top

    # The mechanical floor: dark louvre slots recessed just behind the bay noses,
    # the one horizontal accent on an otherwise wholly vertical tower.
    main = plan_poly()
    for i, lz in enumerate(LOUVRE_Z):
        band(f"louvre_band_{i}", offset_poly(main, -BAY_DEPTH), offset_poly(main, -0.6), lz, lz + 4.4, ink)

    # --- penthouse: blank granite box, sawtooth continued as solid stone ----
    ph_poly = plan_poly(inset=PENTHOUSE_INSET, chamfer=2.6)
    ph_pts, _ = serrate(ph_poly, depth=1.2)
    prism("penthouse", ph_pts, H_ROOF - 1.4, H_ARCH, [rust], cap_mat=0)

    # --- roofscape: the camera looks down on this ---------------------------
    # Rings here are generated directly from the notched plan at an inset rather
    # than mitred off it: offset_poly assumes a convex outline and collapses to
    # degenerate faces at a notch's re-entrant corners.
    top_notches = STAGES[-1][1]
    deck_z = H_ROOF - 1.6  # the sawtooth walls stand proud of it as the parapet
    prism("roof_deck", plan_poly(inset=BAY_DEPTH + 1.4, notches=top_notches), deck_z - 0.4, deck_z, [roofd])

    # Masts and dishes cluster at the west end, washing rigs at the east end,
    # arranged around the penthouse where the downward camera actually sees them.
    for i, (dx, dy, h) in enumerate([(-26.5, 4.5, 7.5), (-24.0, -1.0, 5.5), (-28.5, -5.0, 4.5)]):
        cx, cy = rot2((dx, dy))
        bevel(box(f"mast_{i}", cx, cy, deck_z, deck_z + h, 1.0, 1.0, steel), width=0.1)
    for i, (dx, dy, sx, sy, h) in enumerate([(-19.0, 10.0, 7.0, 4.5, 2.4), (-19.5, -10.0, 6.0, 4.0, 1.9), (7.0, 11.0, 8.0, 4.0, 1.6)]):
        cx, cy = rot2((dx, dy))
        bevel(box(f"plant_{i}", cx, cy, deck_z, deck_z + h, sx, sy, roofd), width=0.16)
    for i, (dx, dy) in enumerate([(22.0, 9.5), (22.0, -9.5)]):
        cx, cy = rot2((dx, dy))
        bevel(box(f"bmu_{i}", cx, cy, deck_z, deck_z + 2.0, 6.5, 2.2, steel), width=0.14)
    band(
        "bmu_rail",
        plan_poly(inset=BAY_DEPTH + 4.0, notches=top_notches),
        plan_poly(inset=BAY_DEPTH + 3.4, notches=top_notches),
        deck_z,
        deck_z + 0.4,
        steel,
    )

    # --- night state -------------------------------------------------------
    # No facade floodlighting and no crown lighting: the real tower is a dark
    # mass at night. Only the offices and the lobby carry light.
    lit_panes("windows_office", stages, lit)
    glow_ring("arcade_lantern", offset_poly(base_poly, -3.0), H_PODIUM + 1.4, H_ARCADE - 1.2, gold, out=0.07)
    # Red FAA obstruction lights, confirmed in the Digital Obstacle File
    # (record 06-000484, Lighting = R). They sit on the penthouse, recessed into
    # its cap so nothing rises above the 237.4 m architectural top.
    for i, (dx, dy) in enumerate([(-22.0, 0.0), (22.0, 0.0), (0.0, 9.0), (0.0, -9.0)]):
        cx, cy = rot2((dx, dy))
        bevel(box(f"beacon_{i}", cx, cy, H_ARCH - 1.0, H_ARCH - 0.1, 1.6, 1.6, red), width=0.1)

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

    blend = os.path.join(out, "555-california.blend")
    glb = os.path.join(out, "555-california.glb")
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
