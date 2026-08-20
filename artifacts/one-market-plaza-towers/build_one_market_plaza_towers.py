"""Deterministic Blender build of the SF-SIM miniature One Market Plaza towers.

    blender -b --python build_one_market_plaza_towers.py -- [--out DIR]

Spear Tower (43 storeys, 172 m) and Steuart Tower (27 storeys, 111 m), Welton
Becket Associates 1976, on the six-storey podium they share at 1 Market Street.
The 1916 Southern Pacific Building on the same address is a SEPARATE asset
(artifacts/1-market/) and is deliberately not here; the two abut along the shared
survey edge.

Geometry is authored in world space in metres, Z up, +X east, +Y north, so the
model drops into the city at its real heading. Origin = envelope AABB centre
(anchor lon -122.3941803, lat 37.7933169), min Z = 0, Spear's plant cap top
exactly 177.60 m.

Design:

* both towers are the same building at two sizes — a rectangle with all four
  corners CANTED, wrapped in close-spaced white precast piers over dark window
  slots that run unbroken from the podium to the parapet. No spandrels, no
  banding, no crown. That uniformity is the design;
* because the slots are continuous vertically, the shaft is ONE dark prism with
  white pier strips standing proud of it — no per-storey geometry at all, which
  is why a 172 m tower costs almost nothing here;
* the podium fills the rest of the lot at 27.8 m in the same language at a
  coarser pitch, with a glazed retail band at grade;
* the plaza deck between the shafts carries the circular sunken garden and the
  run of glazed barrel-vault canopies, both located from nadir imagery and
  corrected for the tile's building lean;
* night: a sparse scatter of lit slots up both shafts, thinning with height,
  over a lit podium retail band and lit canopies. Glow sits OUTSIDE the opaque
  glazing — a plate behind opaque glass renders nothing.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ------------------------------------------------------------------ constants

# lot-007 envelope: DataSF podium ring (mblr SF3713007 / 201006.0000212) UNION
# the Spear shaft ring (201006.0001309), shared edge removed, sub-1 m survey
# jogs dropped, recentred on the envelope AABB centre. CCW, (x east, y north).
# 7,521 m2 against the survey's 7,543 m2.
ENVELOPE = [
    (-50.850, 13.450),    # W — shared edge with the Southern Pacific Building
    (-60.350, 4.150),
    (-22.950, -32.650),
    (-18.550, -38.150),
    (6.350, -63.250),     # S — Mission x Spear return
    (31.650, -38.350),
    (25.550, -32.150),
    (35.050, -23.050),
    (60.350, 2.150),      # E — Don Chee Way
    (28.650, 33.150),
    (-1.350, 63.250),     # N — toward Steuart Street
    (-34.750, 29.050),
]

# The downtown grid. A runs along both shafts' long axis (bearing 135.2 deg, SE);
# B is the short axis (bearing 45.2 deg, NE). A bearing t maps to (sin t, cos t).
_A_BRG, _B_BRG = math.radians(135.2), math.radians(45.2)
AXIS_A = (math.sin(_A_BRG), math.cos(_A_BRG))
AXIS_B = (math.sin(_B_BRG), math.cos(_B_BRG))

# Shafts: centre, length along A, width along B. Spear from the DataSF survey;
# Steuart from OSM way/132238431 shifted +1.9, -2.0 into the DataSF frame (it
# has no footprint of its own in the survey).
SPEAR = {"c": (-28.90, -1.75), "a": 52.5, "b": 35.7}
STEUART = {"c": (31.65, 6.18), "a": 43.3, "b": 33.7}
CANT = 4.6            # canted-corner chord, exaggerated ~15% over the survey's 4.05

H_PODIUM = 27.80      # six storeys — DataSF LiDAR median on the podium polygon
H_POD_PAR = 28.80
H_RETAIL = 6.60       # glazed retail band at grade
H_SPEAR = 172.00      # published roof; DataSF LiDAR median 172.41
H_SPEAR_PAR = 173.20
H_SPEAR_CREST = 177.60  # DataSF LiDAR maximum — the export's bounding-box top
H_STEUART = 111.00    # published roof, corroborated by the satellite lean ratio
H_STEUART_PAR = 112.20
H_STEUART_CREST = 115.50   # inferred by analogy with Spear's measured plant

PIER_W = 1.80         # white precast pier width — near-equal to the slot
PIER_D = 0.62         # projection — this is what keeps the vertical grain at 2 km
PIER_PITCH = 3.50     # measured off the nadir imagery
POD_PITCH = 6.20      # the podium runs a coarser rhythm than the shafts
POD_PIER_W = 2.80
POD_PIER_D = 0.55

# plaza features, read off the z20 nadir tile and corrected for the tile's
# building lean (-0.0116, +0.1547) m per metre of height at 27.8 m
GARDEN = {"c": (-7.5, -30.7), "r": 8.9}
CANOPY = {"p0": (2.5, -10.8), "p1": (22.6, -20.1), "w": 11.0, "n": 5}

BEVEL_W = 0.16
BEVEL_SEG = 2

PALETTE_HEX = {
    "Toy_white": "f7f4ec",
    "Toy_cream": "f2ede3",
    "Toy_sand": "ece4d4",
    "Toy_stone": "d9d2c2",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_slate": "6f7883",
    "Toy_steel": "9aa0a6",
    "Toy_mint": "8fd0a8",
    "Toy_roofd": "45454a",
    "Toy_glassl_Glow": "6f95b8",
    "Toy_gold_Glow": "caa64a",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def oct_ring(spec, cant=CANT, inset=0.0):
    """Rectangle with all four corners canted, in the downtown-grid frame.
    Returns 8 CCW vertices in world XY."""
    cx, cy = spec["c"]
    ha = spec["a"] / 2.0 - inset
    hb = spec["b"] / 2.0 - inset
    d = cant / math.sqrt(2.0)
    ab = [
        (ha - d, -hb), (ha, -hb + d), (ha, hb - d), (ha - d, hb),
        (-ha + d, hb), (-ha, hb - d), (-ha, -hb + d), (-ha + d, -hb),
    ]
    pts = [(cx + AXIS_A[0] * a + AXIS_B[0] * b, cy + AXIS_A[1] * a + AXIS_B[1] * b)
           for a, b in ab]
    return pts if signed_area(pts) > 0 else pts[::-1]


def signed_area(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1]
               - poly[(i + 1) % len(poly)][0] * poly[i][1]
               for i in range(len(poly))) / 2.0


def edge_frame(poly, i):
    """(a, length, tangent, outward normal) for edge i of a CCW polygon."""
    a, b = poly[i], poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    return a, length, t, (t[1], -t[0])


def offset_polygon(poly, d):
    npts = len(poly)
    normals = []
    for i in range(npts):
        a, b = poly[i], poly[(i + 1) % npts]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1.0
        normals.append((dy / length, -dx / length))
    out = []
    for i in range(npts):
        n1, n2 = normals[i - 1], normals[i]
        v = poly[i]
        det = n1[0] * n2[1] - n1[1] * n2[0]
        if abs(det) < 1e-6:
            out.append((v[0] + n2[0] * d, v[1] + n2[1] * d))
            continue
        c1 = v[0] * n1[0] + v[1] * n1[1] + d
        c2 = v[0] * n2[0] + v[1] * n2[1] + d
        out.append(((c1 * n2[1] - c2 * n1[1]) / det, (c2 * n1[0] - c1 * n2[0]) / det))
    return out


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


def bevel(obj, width=BEVEL_W, segments=BEVEL_SEG):
    thin = min(obj.dimensions)
    width = min(width, thin * 0.4)
    if width < 1e-4:
        return obj
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.bevel(bm, geom=list(bm.verts) + list(bm.edges), offset=width,
                    segments=segments, profile=0.5, affect="EDGES", clamp_overlap=True)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(target := obj.data)
    bm.free()
    target.shade_flat()
    return obj


def ensure_outward(obj):
    me = obj.data
    me.calc_loop_triangles()
    vol = 0.0
    for tri in me.loop_triangles:
        a, b, c = (obj.matrix_world @ me.vertices[i].co for i in tri.vertices)
        vol += a.dot(b.cross(c)) / 6.0
    if vol > 0.0:
        return obj
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.reverse_faces(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    me.shade_flat()
    return obj


def prism(name, poly, z0, z1, mat, mat_caps=None):
    npts = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces, face_mats = [], []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
        face_mats.append(0)
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    face_mats += [1 if mat_caps else 0] * 2
    mats = [mat, mat_caps] if mat_caps else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def band(name, poly, z0, z1, off_in, off_out, mat):
    lo_in = offset_polygon(poly, off_in)
    lo_out = offset_polygon(poly, off_out)
    npts = len(lo_in)
    verts = []
    for loop, z in ((lo_in, z0), (lo_out, z0), (lo_out, z1), (lo_in, z1)):
        verts.extend([(x, y, z) for x, y in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * npts, ((k + 1) % 4) * npts
        for i in range(npts):
            j = (i + 1) % npts
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])


def quad_box(name, corners, z0, z1, mat):
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_mesh(name, verts, faces, [mat])


def edge_box(name, poly, i, s0, s1, z0, z1, d_in, d_out, mat):
    a, _, t, nrm = edge_frame(poly, i)

    def p(s, d):
        return (a[0] + t[0] * s + nrm[0] * d, a[1] + t[1] * s + nrm[1] * d)

    return quad_box(name, [p(s0, d_in), p(s1, d_in), p(s1, d_out), p(s0, d_out)], z0, z1, mat)


def disc(name, c, r, z0, z1, mat, segs=18):
    pts = [(c[0] + r * math.cos(2 * math.pi * k / segs),
            c[1] + r * math.sin(2 * math.pi * k / segs)) for k in range(segs)]
    return prism(name, pts, z0, z1, mat)


# --------------------------------------------------------------- the build


def materials():
    mats = {}
    for name, rgb in PALETTE.items():
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        bsdf = m.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.85
        bsdf.inputs["Metallic"].default_value = 0.0
        m.diffuse_color = (*rgb, 1.0)
        m.roughness = 0.85
        if name.endswith("_Glow"):
            bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 0.0
        mats[name] = m
    return mats


def pier_run(tag, poly, z0, z1, pitch, pier_w, pier_d, mat):
    """White precast piers along every edge of a polygon, evenly spaced, with one
    at each end of each edge so the canted corners read as corners."""
    made = 0
    for i in range(len(poly)):
        _, length, _, _ = edge_frame(poly, i)
        nbay = max(1, int(round((length - pier_w) / pitch)))
        step = (length - pier_w) / nbay if nbay else 0.0
        for k in range(nbay + 1):
            s0 = k * step
            edge_box(f"{tag}_p{i}_{k}", poly, i, s0, s0 + pier_w, z0, z1, -0.10, pier_d, mat)
            made += 1
    return made


def lit_slots(tag, poly, z0, z1, mats, rows, per_row, seed=1):
    """Night: a sparse scatter of lit window slots, thinning with height. Plates
    sit OUTSIDE the opaque shaft, or they render nothing."""
    rnd = seed
    for r in range(rows):
        f = (r + 0.5) / rows
        zz = z0 + (z1 - z0) * f
        count = max(1, int(round(per_row * (1.0 - 0.65 * f))))
        for k in range(count):
            rnd = (rnd * 1103515245 + 12345) & 0x7FFFFFFF
            i = rnd % len(poly)
            _, length, _, _ = edge_frame(poly, i)
            rnd = (rnd * 1103515245 + 12345) & 0x7FFFFFFF
            s0 = 1.5 + (rnd % 1000) / 1000.0 * max(0.5, length - 4.0)
            edge_box(f"{tag}_lit{r}_{k}", poly, i, s0, s0 + 1.6, zz, zz + 2.4,
                     PIER_D - 0.14, PIER_D - 0.06, mats["Toy_glassl_Glow"])


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    mats = materials()
    white, cream, sand = mats["Toy_white"], mats["Toy_cream"], mats["Toy_sand"]
    stone, glass, glassl = mats["Toy_stone"], mats["Toy_glass"], mats["Toy_glassl"]
    slate, steel, mint = mats["Toy_slate"], mats["Toy_steel"], mats["Toy_mint"]

    # ---- 1. podium ------------------------------------------------------- #
    bevel(prism("podium", ENVELOPE, 0.0, H_PODIUM, glass, mat_caps=sand), width=0.22)
    pier_run("pod", ENVELOPE, 0.0, H_PODIUM, POD_PITCH, POD_PIER_W, POD_PIER_D, white)
    bevel(band("pod_par", ENVELOPE, H_PODIUM, H_POD_PAR, -0.35, POD_PIER_D + 0.30, white),
          width=0.12)
    # glazed retail band at grade, and its night glow just proud of it
    bevel(band("pod_retail", ENVELOPE, 0.9, H_RETAIL, -0.12, POD_PIER_D - 0.18, glassl),
          width=0.10, segments=1)
    band("pod_retail_glow", ENVELOPE, 1.4, H_RETAIL - 0.7, POD_PIER_D - 0.16,
         POD_PIER_D - 0.10, mats["Toy_gold_Glow"])

    # ---- 2. the plaza deck ------------------------------------------------ #
    gpoly = [(GARDEN["c"][0] + GARDEN["r"] * math.cos(2 * math.pi * k / 18),
              GARDEN["c"][1] + GARDEN["r"] * math.sin(2 * math.pi * k / 18)) for k in range(18)]
    # a kerb RING, not a disc — a solid cap would simply bury the planting
    bevel(band("garden_kerb", gpoly, H_PODIUM - 0.10, H_PODIUM + 0.62, -0.05, 0.85, stone),
          width=0.12, segments=1)
    disc("garden", GARDEN["c"], GARDEN["r"], H_PODIUM - 0.40, H_PODIUM + 0.18, mint)
    # the glazed barrel-vault canopies over the retail below
    p0, p1 = CANOPY["p0"], CANOPY["p1"]
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    run = math.hypot(dx, dy)
    ux, uy = dx / run, dy / run
    for k in range(CANOPY["n"]):
        f = (k + 0.5) / CANOPY["n"]
        cxk, cyk = p0[0] + dx * f, p0[1] + dy * f
        seg = run / CANOPY["n"] * 0.62
        half = CANOPY["w"] / 2.0
        corners = [
            (cxk - ux * seg / 2 - (-uy) * half, cyk - uy * seg / 2 - ux * half),
            (cxk + ux * seg / 2 - (-uy) * half, cyk + uy * seg / 2 - ux * half),
            (cxk + ux * seg / 2 + (-uy) * half, cyk + uy * seg / 2 + ux * half),
            (cxk - ux * seg / 2 + (-uy) * half, cyk - uy * seg / 2 + ux * half),
        ]
        bevel(quad_box(f"canopy{k}", corners, H_PODIUM + 0.15, H_PODIUM + 4.10, glassl),
              width=1.55, segments=4)
        inner = [(cxk + (c[0] - cxk) * 0.72, cyk + (c[1] - cyk) * 0.72) for c in corners]
        quad_box(f"canopy_glow{k}", inner, H_PODIUM + 3.95, H_PODIUM + 4.16,
                 mats["Toy_glassl_Glow"])

    # plaza furniture: the camera looks down, so the deck is an elevation too
    # (style bible). A paved apron along the Mission edge, planters flanking the
    # garden, and the stepped edge down toward Mission Street.
    for k, (px_, py_, su, sv) in enumerate((
        (-24.0, -18.0, 9.0, 5.0), (6.0, -34.0, 7.0, 5.0), (14.0, 2.0, 5.0, 9.0),
        (-14.0, 12.0, 6.0, 4.0),
    )):
        corners = [(px_ - su / 2, py_ - sv / 2), (px_ + su / 2, py_ - sv / 2),
                   (px_ + su / 2, py_ + sv / 2), (px_ - su / 2, py_ + sv / 2)]
        bevel(quad_box(f"planter{k}", corners, H_PODIUM - 0.05, H_PODIUM + 0.75, stone),
              width=0.14, segments=1)
        inner = [(px_ + (c[0] - px_) * 0.74, py_ + (c[1] - py_) * 0.74) for c in corners]
        quad_box(f"planting{k}", inner, H_PODIUM + 0.55, H_PODIUM + 1.15, mint)
    for k, (px_, py_, su, sv) in enumerate(((2.0, -46.0, 44.0, 7.0), (44.0, -6.0, 7.0, 30.0))):
        corners = [(px_ - su / 2, py_ - sv / 2), (px_ + su / 2, py_ - sv / 2),
                   (px_ + su / 2, py_ + sv / 2), (px_ - su / 2, py_ + sv / 2)]
        quad_box(f"apron{k}", corners, H_PODIUM - 0.02, H_PODIUM + 0.10, stone)

    # ---- 3. the two shafts ------------------------------------------------ #
    for tag, spec, h_roof, h_par, h_crest, rows, per_row in (
        ("spear", SPEAR, H_SPEAR, H_SPEAR_PAR, H_SPEAR_CREST, 26, 5),
        ("steuart", STEUART, H_STEUART, H_STEUART_PAR, H_STEUART_CREST, 16, 4),
    ):
        ring = oct_ring(spec)
        # ONE dark prism for the whole shaft: the window slots are continuous
        # vertically, so there is no per-storey geometry to build at all.
        bevel(prism(f"{tag}_shaft", ring, H_PODIUM - 1.2, h_roof, glass, mat_caps=slate),
              width=0.20)
        pier_run(tag, ring, H_PODIUM - 1.2, h_roof, PIER_PITCH, PIER_W, PIER_D, white)
        bevel(band(f"{tag}_par", ring, h_roof, h_par, -0.45, PIER_D + 0.22, white), width=0.14)
        # rooftop plant
        pc = spec["c"]
        plant = {"c": pc, "a": spec["a"] * 0.34, "b": spec["b"] * 0.38}
        bevel(prism(f"{tag}_plant", oct_ring(plant, cant=2.2), h_par, h_crest - 0.5, slate),
              width=0.16, segments=1)
        bevel(prism(f"{tag}_plant_cap", oct_ring(plant, cant=2.2, inset=-0.5),
                    h_crest - 0.5, h_crest, steel), width=0.10, segments=1)
        lit_slots(tag, ring, H_PODIUM + 4.0, h_roof - 6.0, mats, rows, per_row,
                  seed=7 if tag == "spear" else 31)

    return scene


def finish():
    for obj in [o for o in bpy.data.objects if o.type == "MESH"]:
        ensure_outward(obj)


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
        o.evaluated_get(dg).to_mesh_clear()
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print("[build] anchor lon/lat: -122.3941803 37.7933169 (envelope AABB centre)")
    print(f"[build] podium {H_PODIUM}; Steuart roof {H_STEUART}; Spear roof {H_SPEAR}; crest {H_SPEAR_CREST}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)
    build()
    finish()
    report()
    blend = os.path.join(out, "one-market-plaza-towers.blend")
    glb = os.path.join(out, "one-market-plaza-towers.glb")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    bpy.ops.export_scene.gltf(
        filepath=glb, export_format="GLB", export_apply=True, export_yup=True,
        use_selection=False, export_cameras=False, export_lights=False,
        export_animations=False, export_skins=False, export_morph=False,
        export_materials="EXPORT", export_image_format="NONE",
    )
    print(f"[build] wrote {blend}")
    print(f"[build] wrote {glb}")


if __name__ == "__main__":
    main()
