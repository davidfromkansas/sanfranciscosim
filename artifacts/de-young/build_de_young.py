"""Deterministic Blender build of the SF-SIM miniature de Young Museum.

    blender -b --python build_de_young.py -- [--out DIR]

Writes de-young.blend and de-young.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, origin at the base centre, min Z = 0, so the export needs no
transforms applied after the fact.

Design (see REFERENCE.md for the measured geometry behind every number):

* the long copper band: the measured 153.7 x 76.1 m oriented footprint on the
  Music Concourse grid (long axis bearing 48.2 deg true = local +X yawed
  +41.8 deg CCW), walls in weathered brown copper (Toy_rust) under a green
  patina roof plane (Toy_verdigris) - the dossier's graphic weathering rule:
  every skyward copper surface has turned, every wall face is still brown;
* the angular NE prow: the band's east end cuts diagonally to a sharp tip,
  the education wing's signature wedge;
* four roof voids at their measured positions: two broad garden courts toward
  the concourse side (the eastern one is the open-air entry court) and two
  narrow fern canyons en echelon toward the JFK side;
* horizontal copper banding (Toy_brick) and scattered vertical window slits
  wrap the walls; the entrance is a dark cut-out under a cantilevered roof
  blade on the concourse facade;
* the Hamon Tower at the NE end, JFK side: a 9.4 x 27.9 m slab lofted through
  nine storeys to a wider, shorter 11.2 x 20.4 m top, twisting 42 deg
  clockwise so the observation floor aligns with the city's avenue grid -
  the architects' stated parti, eased so the swing concentrates near the top;
* night state per the dossier: the observation lantern in Toy_white_Glow and
  a warm Toy_gold_Glow entry sequence (entry passage, entry-court liner, the
  window slits, the cafe corner), every glow pane paired with a dark glass
  backing so the day read survives the loader's 12% day opacity; the canyons
  and west court stay dark for contrast.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

YAW = math.radians(41.8)  # local +X (long axis) -> bearing 48.2 true

HALF_U = 76.85  # half-length of the oriented footprint (153.7 m)
HALF_V = 38.05  # half-width (76.1 m)

H_BAND = 12.2  # main copper band, wall top
H_ROOF = 13.0  # roof plane (OSM height=13)
ROOF_OVER = 1.2  # roof plate oversail beyond the walls

H_TOWER = 43.9  # Hamon Tower, 144 ft
TOWER_CX, TOWER_CY = 63.1, 23.95  # measured slab centre (NE end, JFK side)
TOWER_BASE = (4.7, 13.95)  # half-dims: 9.4 x 27.9 m, long axis across the band
TOWER_TOP = (5.6, 10.2)  # 11.2 x 20.4 m: wider and shorter
TWIST = math.radians(-42.0)  # clockwise (viewed from above) to the city grid
LANTERN_H = 3.9  # glazed observation floor at the top

# Prow: the SE edge cuts from (PROW_X0, -HALF_V) to the tip edge at +HALF_U
PROW_X0 = 55.0
PROW_TIP_Y = 10.0

# Roof voids, measured in the grid frame (local x = u, local y = -v):
# (x0, x1, y0, y1, floor material key, depth below roof)
COURTS = [
    (-73.0, -30.0, -20.5, -5.0, "Toy_mint", 3.4),   # west garden court (dark at night)
    (15.0, 52.0, -20.0, -5.0, "Toy_stone", 3.4),    # open-air entry court (plaza)
]
CANYONS = [
    (-70.0, -11.0, 10.0, 16.0, "Toy_mint", 2.8),    # fern canyon 1
    (-3.0, 52.0, 5.0, 11.0, "Toy_mint", 2.8),       # fern canyon 2, en echelon
]

# proud horizontal copper panel bands - four courses, the facade's rhythm
BAND_ZS = ((1.9, 2.55), (4.9, 5.55), (7.9, 8.55), (10.6, 11.25))
BAND_OUT = 0.18

# Vertical window slits (x along each facade, width, height, base z)
SLITS_SE = [(-63.0, 3.6), (-49.0, 5.2), (-36.5, 3.0), (-22.0, 5.8), (-9.0, 3.4),
            (4.5, 5.4), (40.0, 3.2)]
SLITS_NW = [(-58.0, 4.8), (-41.0, 3.2), (-26.0, 5.6), (-8.0, 3.6), (8.0, 5.0),
            (24.0, 3.4), (40.0, 5.6)]

PALETTE_HEX = {
    "Toy_rust": "a86444",
    "Toy_brick": "c96f4a",
    "Toy_verdigris": "9fb8a8",
    "Toy_glass": "2a4d73",
    "Toy_mint": "8fd0a8",
    "Toy_stone": "d9d2c2",
    "Toy_ink": "3a3530",
    "Toy_roofd": "45454a",
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


def rot2(p, ang=None):
    a = YAW if ang is None else ang
    c, s = math.cos(a), math.sin(a)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def new_mesh(name, verts, faces, materials, face_mats=None, smooth=False,
             recalc=True):
    """recalc=False keeps the authored winding - required for OPEN meshes
    (sheets, capless shells), where bmesh's outside-detection flips faces."""
    verts = [(*rot2((v[0], v[1])), v[2]) for v in verts]
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
    if smooth:
        mesh.polygons.foreach_set("use_smooth", [True] * len(mesh.polygons))
    else:
        mesh.shade_flat()
    return obj


def bevel(obj, width=0.15, segments=2):
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


def prism(name, pts, z0, z1, side_mat, top_mat=None, bottom_mat=None,
          cap_top=True, cap_bottom=True):
    """Extrusion of a CCW polygon with per-part materials and optional caps."""
    mats = [side_mat]
    def midx(m):
        if m is None or m == side_mat:
            return 0
        if m not in mats:
            mats.append(m)
        return mats.index(m)
    ti, bi = midx(top_mat), midx(bottom_mat)
    n = len(pts)
    verts = [(x, y, z0) for x, y in pts] + [(x, y, z1) for x, y in pts]
    faces, fm = [], []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
        fm.append(0)
    if cap_bottom:
        faces.append(tuple(range(n - 1, -1, -1)))
        fm.append(bi)
    if cap_top:
        faces.append(tuple(range(n, 2 * n)))
        fm.append(ti)
    return new_mesh(name, verts, faces, mats, fm,
                    recalc=cap_top and cap_bottom)


def roof_top_tiles(name, voids, mat, z):
    """The roof surface at z with real rectangular holes at the voids.

    The rectangular part of the plan is cut into x-strips at every void edge;
    each strip is filled with quads around the voids it crosses. The prow
    wedge (x > PROW_X0, no voids there) is one trapezoid.
    """
    xs = sorted({-HALF_U, PROW_X0} | {v for (x0, x1, *_r) in voids for v in (x0, x1)})
    verts, faces = [], []

    def quad(x0, x1, y0, y1):
        base = len(verts)
        verts.extend([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)])
        faces.append((base, base + 1, base + 2, base + 3))

    for xi in range(len(xs) - 1):
        x0, x1 = xs[xi], xs[xi + 1]
        # strips are minimal intervals between void edges, so any void
        # overlapping this strip spans it fully
        holes = sorted(
            (v[2], v[3]) for v in voids if v[0] <= x0 and v[1] >= x1
        )
        y = -HALF_V
        for h0, h1 in holes:
            if h0 > y:
                quad(x0, x1, y, h0)
            y = h1
        if y < HALF_V:
            quad(x0, x1, y, HALF_V)
    # prow trapezoid
    base = len(verts)
    verts.extend([(PROW_X0, -HALF_V, z), (HALF_U, PROW_TIP_Y, z),
                  (HALF_U, HALF_V, z), (PROW_X0, HALF_V, z)])
    faces.append((base, base + 1, base + 2, base + 3))
    return new_mesh(name, verts, faces, [mat], recalc=False)


def oversail_ring(name, width, z0, z1, side_mat, top_mat):
    """The cantilevered roof-edge ring: outer outline lofted to the wall line."""
    outer = band_outline(width)
    inner = band_outline(0.0)
    n = len(outer)
    verts = ([(x, y, z1) for x, y in outer] + [(x, y, z1) for x, y in inner]
             + [(x, y, z0) for x, y in outer] + [(x, y, z0) for x, y in inner])
    faces, fm = [], []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))          # top annulus
        fm.append(1)
        faces.append((2 * n + j, 2 * n + i, i, j))  # outer wall
        fm.append(0)
        faces.append((3 * n + i, 3 * n + j, 2 * n + j, 2 * n + i))  # underside
        fm.append(0)
        faces.append((n + j, n + i, 3 * n + i, 3 * n + j))  # inner (hidden)
        fm.append(0)
    return new_mesh(name, verts, faces, [side_mat, top_mat], fm)


def box(name, cx, cy, z0, z1, sx, sy, mat, local_yaw=0.0, face_mats=None, mats=None):
    hx, hy = sx / 2, sy / 2
    corners = [rot2(c, local_yaw) for c in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy))]
    verts = [(cx + x, cy + y, z0) for x, y in corners]
    verts += [(cx + x, cy + y, z1) for x, y in corners]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),  # -Y face (index 2 in face list)
        (1, 2, 6, 5),
        (2, 3, 7, 6),  # +Y face (index 4)
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, mats or [mat], face_mats)


def seg_box(name, p0, p1, z0, z1, thick, mat):
    """A thin closed slab following the segment p0->p1 (for banding on any wall)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    length = math.hypot(dx, dy)
    ang = math.atan2(dy, dx)
    cx, cy = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    return box(name, cx, cy, z0, z1, length, thick, mat, local_yaw=ang)


def sphere(name, cx, cy, cz, r, mat, seg=10, rings=6):
    verts, faces = [], []
    for ri in range(1, rings):
        phi = math.pi * ri / rings
        for si in range(seg):
            th = 2 * math.pi * si / seg
            verts.append((cx + r * math.sin(phi) * math.cos(th),
                          cy + r * math.sin(phi) * math.sin(th),
                          cz + r * math.cos(phi)))
    top = len(verts); verts.append((cx, cy, cz + r))
    bot = len(verts); verts.append((cx, cy, cz - r))
    for si in range(seg):
        sj = (si + 1) % seg
        faces.append((top, si, sj))
        faces.append((bot, (rings - 2) * seg + sj, (rings - 2) * seg + si))
        for ri in range(rings - 2):
            a = ri * seg
            faces.append((a + si, a + seg + si, a + seg + sj, a + sj))
    return new_mesh(name, verts, faces, [mat], smooth=True)


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
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    mat.blend_method = "OPAQUE"
    return mat


# --------------------------------------------------------------------- build


def band_outline(off=0.0):
    """The main plan polygon (CCW): rectangle with the angular NE prow cut."""
    return [
        (-HALF_U - off, -HALF_V - off),
        (PROW_X0 + off * 0.4, -HALF_V - off),
        (HALF_U + off, PROW_TIP_Y - off * 0.6),
        (HALF_U + off, HALF_V + off),
        (-HALF_U - off, HALF_V + off),
    ]


def void_pit(name, x0, x1, y0, y1, floor_mat, depth, rust, wall_top):
    """A roof void: four wall slabs with a parapet lip plus a sunken floor."""
    t = 0.45  # wall slab thickness
    lip = 0.4  # parapet above the roof plane
    z_top = wall_top + lip
    z_floor = wall_top - depth
    box(f"{name}_wall_s", (x0 + x1) / 2, y0 + t / 2, z_floor, z_top, x1 - x0, t, rust)
    box(f"{name}_wall_n", (x0 + x1) / 2, y1 - t / 2, z_floor, z_top, x1 - x0, t, rust)
    box(f"{name}_wall_w", x0 + t / 2, (y0 + y1) / 2, z_floor, z_top, t, y1 - y0 - 2 * t, rust)
    box(f"{name}_wall_e", x1 - t / 2, (y0 + y1) / 2, z_floor, z_top, t, y1 - y0 - 2 * t, rust)
    box(f"{name}_floor", (x0 + x1) / 2, (y0 + y1) / 2, z_floor, z_floor + 0.25,
        x1 - x0 - 2 * t, y1 - y0 - 2 * t, floor_mat)
    return z_floor


def glow_pane(name, cx, cy, z0, z1, sx, sy, out_dir, glow, glass, axis="y"):
    """A dark glass slab with a glow face on its outward side (day-safe glow)."""
    fm = [0, 0, 0, 0, 0, 0]
    if axis == "y":
        fm[2 if out_dir < 0 else 4] = 1  # -Y or +Y face carries the glow
    else:
        fm[5 if out_dir < 0 else 3] = 1  # -X or +X face
    box(name, cx, cy, z0, z1, sx, sy, glass, face_mats=fm, mats=[glass, glow])


def ease(t, p=1.9):
    return t ** p


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    rust = material("Toy_rust")
    brick = material("Toy_brick")
    verdi = material("Toy_verdigris")
    glass = material("Toy_glass")
    mint = material("Toy_mint")
    stone = material("Toy_stone")
    ink = material("Toy_ink")
    roofd = material("Toy_roofd")
    wglow = material("Toy_white_Glow")
    gglow = material("Toy_gold_Glow")

    # --- the copper band as a shell, so the roof voids are REAL holes -------
    # sides + bottom (no top cap: the top is tiled around the voids)
    prism("band_shell", band_outline(0.0), 0.0, H_ROOF, rust,
          bottom_mat=rust, cap_top=False)
    roof_top_tiles("roof_top", COURTS + CANYONS, verdi, H_ROOF)
    # cantilevered roof-edge ring, patina on top / copper fascia + soffit
    oversail_ring("roof_edge", ROOF_OVER, H_BAND, H_ROOF, rust, verdi)

    # --- horizontal copper panel bands around every facade ------------------
    wall_pts = band_outline(BAND_OUT / 2)
    for bi, (z0, z1) in enumerate(BAND_ZS):
        for si in range(len(wall_pts)):
            p0, p1 = wall_pts[si], wall_pts[(si + 1) % len(wall_pts)]
            seg_box(f"band_{bi}_{si}", p0, p1, z0, z1, 0.3, brick)

    # --- vertical window slits (gold at night, dark glass by day) -----------
    # (slits stand prouder than the panel bands, so they read as cuts through
    # the banding, the way the real irregular slots interrupt the panels)
    for k, (sx_, h) in enumerate(SLITS_SE):
        glow_pane(f"slit_se_{k}", sx_, -HALF_V + 0.05, 1.6, 1.6 + h, 0.9, 1.0,
                  -1, gglow, glass)
    for k, (sx_, h) in enumerate(SLITS_NW):
        glow_pane(f"slit_nw_{k}", sx_, HALF_V - 0.05, 1.6, 1.6 + h, 0.9, 1.0,
                  +1, gglow, glass)
    for k, (sy_, h) in enumerate(((-21.0, 4.6), (2.0, 3.2), (19.0, 5.4))):
        glow_pane(f"slit_sw_{k}", -HALF_U + 0.05, sy_, 1.6, 1.6 + h, 1.0, 0.9,
                  -1, gglow, glass, axis="x")

    # --- entrance: dark cut-out + cantilevered roof blade (concourse side) --
    box("entry_recess", 28.0, -HALF_V + 0.25, 0.0, 5.6, 13.0, 1.4, ink)
    glow_pane("entry_passage", 28.0, -HALF_V - 0.12, 0.4, 5.2, 11.6, 0.5,
              -1, gglow, glass)
    bevel(box("entry_blade", 28.0, -HALF_V - 2.6, 5.6, 6.25, 17.5, 6.4, rust,
              face_mats=[0, 1, 0, 0, 0, 0], mats=[rust, verdi]), width=0.12)
    for sx_ in (21.5, 34.5):  # slim supports at the blade tips
        box(f"blade_post_{sx_}", sx_, -HALF_V - 5.2, 0.0, 5.6, 0.5, 0.5, ink)

    # --- cafe corner glazing at the SW end ----------------------------------
    glow_pane("cafe_band", -68.0, -HALF_V - 0.1, 0.7, 3.55, 15.0, 0.5,
              -1, gglow, glass)

    # --- roof voids: courts and fern canyons --------------------------------
    for name, (x0, x1, y0, y1, key, depth) in zip(
        ("court_west", "court_entry"), COURTS
    ):
        zf = void_pit(name, x0, x1, y0, y1, material(key), depth, rust, H_ROOF)
        for i, (tx, ty, r) in enumerate(
            ((0.3, 0.3, 1.6), (0.68, 0.62, 1.25), (0.15, 0.72, 1.05))
        ):
            if name == "court_entry" and i == 0:
                continue  # keep the entry plaza open
            sphere(f"{name}_tree_{i}", x0 + (x1 - x0) * tx, y0 + (y1 - y0) * ty,
                   zf + 0.25 + r * 0.75, r, mint)
    # entry-court gold liner on the concourse-side wall (night sequence)
    x0, x1, y0, y1 = COURTS[1][:4]
    glow_pane("court_entry_liner", (x0 + x1) / 2, y0 + 0.62, H_ROOF - 2.4,
              H_ROOF - 0.2, x1 - x0 - 1.6, 0.28, +1, gglow, glass)
    for name, (x0, x1, y0, y1, key, depth) in zip(
        ("canyon_a", "canyon_b"), CANYONS
    ):
        void_pit(name, x0, x1, y0, y1, material(key), depth, rust, H_ROOF)
        # little crossing bridges over the fern canyons
        for bx in (x0 + (x1 - x0) * 0.3, x0 + (x1 - x0) * 0.72):
            box(f"{name}_bridge_{round(bx)}", bx, (y0 + y1) / 2,
                H_ROOF + 0.42, H_ROOF + 0.68, 1.7, y1 - y0 + 1.2, stone)
    # benches on the entry-court plaza
    ex0, ex1, ey0, ey1 = COURTS[1][:4]
    for k, bt in enumerate((0.3, 0.55, 0.8)):
        box(f"court_bench_{k}", ex0 + (ex1 - ex0) * bt, (ey0 + ey1) / 2 - 2.0,
            H_ROOF - 3.15, H_ROOF - 2.75, 2.6, 0.9, stone)

    # --- roof furniture: skylight strips + plant blocks ---------------------
    for k, (x0, x1, yc) in enumerate(((-62.0, -34.0, 25.4), (-18.0, 8.0, 29.2),
                                      (18.0, 44.0, 25.4))):
        box(f"skylight_{k}", (x0 + x1) / 2, yc, H_ROOF, H_ROOF + 0.14,
            x1 - x0, 2.3, ink)
    for k, (cx, cy, sx_, sy_, h) in enumerate(
        ((-72.5, 28.0, 4.5, 3.2, 1.1), (60.0, -20.0, 5.2, 3.4, 1.3))
    ):
        bevel(box(f"vent_{k}", cx, cy, H_ROOF, H_ROOF + h, sx_, sy_, roofd),
              width=0.1)

    # --- the Hamon Tower: nine storeys, twisting to the city grid -----------
    # The shaft is one loft whose rings carry the eased twist; each storey
    # line is a recessed dark-glass window band folded into the same loft, so
    # the glazing follows the warped faces instead of poking through them.
    levels = 9
    shaft_h = H_TOWER - LANTERN_H
    win_h = 1.0  # storey window band height
    step = 0.30  # recess depth

    def tower_ring(z, inset):
        t = min(max(z / shaft_h, 0.0), 1.0)
        hx = TOWER_BASE[0] + (TOWER_TOP[0] - TOWER_BASE[0]) * t - inset
        hy = TOWER_BASE[1] + (TOWER_TOP[1] - TOWER_BASE[1]) * t - inset
        phi = TWIST * ease(t)
        corners = [rot2(c, phi) for c in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy))]
        return [(TOWER_CX + x, TOWER_CY + y, z) for x, y in corners]

    rings, rows = [], []  # rows[i] = material row between ring i and i+1
    rings.append(tower_ring(0.0, 0.0))
    for li in range(1, levels + 1):
        z1 = shaft_h * li / levels
        zb = z1 - win_h
        rings.append(tower_ring(zb, 0.0)); rows.append(0)          # wall
        rings.append(tower_ring(zb + 0.02, step)); rows.append(0)  # step in
        if li == levels:
            rings.append(tower_ring(z1, step)); rows.append(1)     # glass to top
        else:
            rings.append(tower_ring(z1 - 0.02, step)); rows.append(1)  # glass
            rings.append(tower_ring(z1, 0.0)); rows.append(0)      # step out
    verts, faces, fm = [], [], []
    for ring in rings:
        verts.extend(ring)
    for ri in range(len(rings) - 1):
        a = ri * 4
        for i in range(4):
            j = (i + 1) % 4
            faces.append((a + i, a + j, a + 4 + j, a + 4 + i))
            fm.append(rows[ri])
    faces.append((3, 2, 1, 0)); fm.append(0)
    a = (len(rings) - 1) * 4
    faces.append((a, a + 1, a + 2, a + 3)); fm.append(0)
    new_mesh("tower_shaft", verts, faces, [rust, glass], fm)
    # observation lantern: glass drum with a white glow liner, patina cap
    hx, hy = TOWER_TOP
    z0 = H_TOWER - LANTERN_H
    box("lantern_glass", TOWER_CX, TOWER_CY, z0, H_TOWER - 0.5,
        2 * hx, 2 * hy, glass, local_yaw=TWIST)
    box("lantern_glow", TOWER_CX, TOWER_CY, z0 + 0.35, H_TOWER - 0.85,
        2 * hx + 0.14, 2 * hy + 0.14, wglow, local_yaw=TWIST)
    bevel(box("lantern_cap", TOWER_CX, TOWER_CY, H_TOWER - 0.5, H_TOWER,
              2 * hx + 0.6, 2 * hy + 0.6, rust, local_yaw=TWIST,
              face_mats=[0, 1, 0, 0, 0, 0], mats=[rust, verdi]), width=0.12)

    return scene


# Measured footprint centre (REFERENCE.md). The plan polygon is asymmetric
# (prow, tower, blade), so after building, the whole asset is recentred on its
# axis-aligned bounds and the anchor that corresponds to the new origin is
# printed for REPORT.md.
FOOT_LON, FOOT_LAT = -122.46872, 37.77150


def recenter():
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for o in bpy.data.objects:
        if o.type != "MESH":
            continue
        for v in o.data.vertices:
            for i in range(3):
                mn[i] = min(mn[i], v.co[i])
                mx[i] = max(mx[i], v.co[i])
    cx, cy = (mn.x + mx.x) / 2, (mn.y + mx.y) / 2
    for o in bpy.data.objects:
        if o.type != "MESH":
            continue
        for v in o.data.vertices:
            v.co.x -= cx
            v.co.y -= cy
    lon = FOOT_LON + cx / (111320.0 * math.cos(math.radians(FOOT_LAT)))
    lat = FOOT_LAT + cy / 110540.0
    print(f"[build] recentered by ({-cx:.3f}, {-cy:.3f}) m")
    print(f"[build] manifest anchor for the recentered origin: [{lon:.7f}, {lat:.7f}]")


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
    recenter()
    report()

    blend = os.path.join(out, "de-young.blend")
    glb = os.path.join(out, "de-young.glb")
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
