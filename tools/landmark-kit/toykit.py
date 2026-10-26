"""Shared Blender helpers for the Transbay landmark batch (2026-10).

Twenty towers between the Ferry Building and Salesforce Tower were built in one
batch, and most of them are the same handful of problems: a prism on an OSM
footprint, a curtain wall or a pier grid, spandrel bands, a designed roof and a
lit-window night skin. Solving those once here keeps the set looking like one
toy box (style bible s.24, "structure families") and keeps each building's own
build script about its building rather than about bmesh.

Import from a build script with

    sys.path.insert(0, os.path.join(REPO, "tools", "landmark-kit"))
    import toykit as tk

Conventions (the asset contract, .agents/skills/sf-asset-check):
* metres, Z up, +X east, +Y north (true compass), origin at base centre, min Z 0;
* every object is authored in world space (no object transforms);
* flat `Toy_*` materials only, roughness 0.85, `_Glow` on night surfaces;
* glow is a thin skin laid OVER solid body, because the app renders `_Glow`
  nearly transparent by day.
"""

import math
import os

import bmesh
import bpy
from mathutils import Vector

# ------------------------------------------------------------------ palette

PALETTE_HEX = {
    "cream": "f2ede3", "sand": "ece4d4", "trim": "f3efe6", "teal": "3fa8a0",
    "coral": "e8735a", "mustard": "d9a441", "mint": "8fd0a8", "sky": "6db3d9",
    "navy": "2c4a70", "glass": "2a4d73", "glassl": "6f95b8", "ink": "3a3530",
    "roofd": "45454a", "brick": "c96f4a", "stone": "d9d2c2", "red": "c4453c",
    "steel": "9aa0a6", "rust": "a86444", "gold": "caa64a", "ioorange": "c0402a",
    "verdigris": "9fb8a8", "white": "f7f4ec",
}

# Off-palette tones some buildings need (a WARN, not a fail, per the contract).
# Each is documented in the building's REFERENCE.md where it is used.
EXTRA_HEX = {
    "granite": "b9a79a",   # rose/red granite (123 Mission, 333 Market base)
    "bronze": "6b5843",    # bronze-tinted glass and mullions
    "glassg": "8fa9b8",    # pale silvery glass (Salesforce, Park Tower)
    "glassd": "3b4a5a",    # dark grey-green glass
    "leaf": "5fae5a",      # roof-garden foliage
    "leafd": "3f8a4a",
    "concrete": "c9c4b8",
    "terracotta": "e3d3b6",
    "copper": "7f9c8c",
}

ALL_HEX = {**PALETTE_HEX, **EXTRA_HEX}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


def material(key):
    """`material("glass")` -> Toy_glass; `material("white_Glow")` -> Toy_white_Glow."""
    name = "Toy_" + key
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    base = key[:-5] if key.endswith("_Glow") else key
    rgb = srgb_to_linear(ALL_HEX[base])
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.85
    bsdf.inputs["Metallic"].default_value = 0.0
    if key.endswith("_Glow"):
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    return mat


def off_palette(materials):
    return sorted(m for m in materials if m.replace("Toy_", "").replace("_Glow", "") in EXTRA_HEX)


# ----------------------------------------------------------- 2-D plan maths


def rot2(p, ang):
    c, s = math.cos(ang), math.sin(ang)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def bearing_to_yaw(bearing_deg):
    """Compass bearing of a building's local +X axis -> Blender yaw (radians)."""
    return math.radians(90.0 - bearing_deg)


def xform(poly, yaw=0.0, dx=0.0, dy=0.0):
    return [(x + dx, y + dy) for x, y in (rot2(p, yaw) for p in poly)]


def rect(w, d, cx=0.0, cy=0.0):
    hw, hd = w / 2, d / 2
    return [(cx - hw, cy - hd), (cx + hw, cy - hd), (cx + hw, cy + hd), (cx - hw, cy + hd)]


def chamfer_rect(w, d, c, cx=0.0, cy=0.0):
    """Rectangle with 45-degree chamfered corners (c = leg length)."""
    hw, hd = w / 2, d / 2
    return [(cx + x, cy + y) for x, y in [
        (-hw + c, -hd), (hw - c, -hd), (hw, -hd + c), (hw, hd - c),
        (hw - c, hd), (-hw + c, hd), (-hw, hd - c), (-hw, -hd + c)]]


def notch_rect(w, d, n, cx=0.0, cy=0.0):
    """Rectangle with square re-entrant notches of size n at all four corners."""
    hw, hd = w / 2, d / 2
    pts = [(-hw + n, -hd), (hw - n, -hd), (hw - n, -hd + n), (hw, -hd + n),
           (hw, hd - n), (hw - n, hd - n), (hw - n, hd), (-hw + n, hd),
           (-hw + n, hd - n), (-hw, hd - n), (-hw, -hd + n), (-hw + n, -hd + n)]
    return [(cx + x, cy + y) for x, y in pts]


def rounded_rect(w, d, r, seg=4, cx=0.0, cy=0.0):
    hw, hd = w / 2, d / 2
    r = min(r, hw - 0.01, hd - 0.01)
    pts = []
    for (sx, sy, a0) in ((1, -1, -90), (1, 1, 0), (-1, 1, 90), (-1, -1, 180)):
        ccx, ccy = sx * (hw - r), sy * (hd - r)
        for i in range(seg + 1):
            a = math.radians(a0 + 90 * i / seg)
            pts.append((cx + ccx + r * math.cos(a), cy + ccy + r * math.sin(a)))
    return pts


def ellipse(a, b, seg=24, cx=0.0, cy=0.0):
    return [(cx + a * math.cos(2 * math.pi * i / seg), cy + b * math.sin(2 * math.pi * i / seg))
            for i in range(seg)]


def poly_area(poly):
    a = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        a += x1 * y2 - x2 * y1
    return a / 2


def ccw(poly):
    return poly if poly_area(poly) > 0 else list(reversed(poly))


def offset_poly(poly, d):
    """Miter offset of a simple CCW polygon (d > 0 grows it)."""
    poly = ccw(poly)
    n = len(poly)
    out = []
    for i in range(n):
        p0, p1, p2 = poly[i - 1], poly[i], poly[(i + 1) % n]
        e1 = (p1[0] - p0[0], p1[1] - p0[1])
        e2 = (p2[0] - p1[0], p2[1] - p1[1])
        l1 = math.hypot(*e1) or 1
        l2 = math.hypot(*e2) or 1
        n1 = (e1[1] / l1, -e1[0] / l1)
        n2 = (e2[1] / l2, -e2[0] / l2)
        bx, by = n1[0] + n2[0], n1[1] + n2[1]
        bl = math.hypot(bx, by)
        if bl < 1e-6:
            out.append((p1[0] + n1[0] * d, p1[1] + n1[1] * d))
            continue
        bx, by = bx / bl, by / bl
        cosh = bx * n1[0] + by * n1[1]
        k = d / max(cosh, 0.25)
        out.append((p1[0] + bx * k, p1[1] + by * k))
    return out


def scale_poly(poly, s, cx=0.0, cy=0.0):
    return [(cx + (x - cx) * s, cy + (y - cy) * s) for x, y in poly]


def edges(poly):
    """[(p0, p1, length, outward_normal)] for a CCW polygon."""
    poly = ccw(poly)
    out = []
    for i in range(len(poly)):
        p0, p1 = poly[i], poly[(i + 1) % len(poly)]
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dx, dy)
        if L < 1e-6:
            continue
        out.append((p0, p1, L, (dy / L, -dx / L)))
    return out


def hash01(n):
    x = math.sin(n * 12.9898 + 78.233) * 43758.5453
    return x - math.floor(x)


# ------------------------------------------------------------- mesh helpers


def new_mesh(name, verts, faces, mats, face_mats=None, recalc=True):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(v) for v in verts], [], faces)
    for m in mats:
        mesh.materials.append(m if isinstance(m, bpy.types.Material) else material(m))
    if face_mats:
        for poly, mi in zip(mesh.polygons, face_mats):
            poly.material_index = mi
    mesh.validate()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    if recalc:
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.free()
    mesh.shade_flat()
    return obj


def bevel(obj, width=0.15, segments=1, only_vertical=False):
    """Miniature edge softening (style bible s.4). One segment keeps tris low."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    es = list(bm.edges)
    if only_vertical:
        es = [e for e in es if abs(e.verts[0].co.z - e.verts[1].co.z) > 1e-3]
    bmesh.ops.bevel(bm, geom=es, offset=width, segments=segments, profile=0.5,
                    affect="EDGES", clamp_overlap=True)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def prism(name, poly, z0, z1, mat, bev=0.0, top=True, bottom=True):
    """Extrude a plan polygon (concave allowed) from z0 to z1."""
    poly = ccw(poly)
    n = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    if bottom:
        faces.append(tuple(range(n - 1, -1, -1)))
    if top:
        faces.append(tuple(range(n, 2 * n)))
    obj = new_mesh(name, verts, faces, [mat])
    if bev > 0:
        bevel(obj, bev)
    return obj


def frustum(name, poly0, z0, poly1, z1, mat, top=True, bottom=True):
    n = len(poly0)
    verts = [(x, y, z0) for x, y in poly0] + [(x, y, z1) for x, y in poly1]
    faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    if top:
        faces.append(tuple(range(n, 2 * n)))
    if bottom:
        faces.append(tuple(range(n - 1, -1, -1)))
    return new_mesh(name, verts, faces, [mat])


def loft(name, rings, mat, row_mats=None, cap_top=False, mats=None, cap_bottom=False):
    """Loft equal-length loops [(z, loop)]; row_mats indexes into mats per strip."""
    n = len(rings[0][1])
    verts = []
    for z, loop in rings:
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
        fm.append(0)
    if cap_bottom:
        faces.append(tuple(range(n - 1, -1, -1)))
        fm.append(0)
    return new_mesh(name, verts, faces, mats or [mat], fm if mats else None)


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0, bev=0.0, bottom=True):
    poly = xform(rect(sx, sy), yaw, cx, cy)
    return prism(name, poly, z0, z1, mat, bev=bev, bottom=bottom)


def cylinder(name, cx, cy, z0, z1, r, mat, seg=10, top=True, r1=None):
    r1 = r if r1 is None else r1
    p0 = [(cx + r * math.cos(2 * math.pi * i / seg), cy + r * math.sin(2 * math.pi * i / seg)) for i in range(seg)]
    p1 = [(cx + r1 * math.cos(2 * math.pi * i / seg), cy + r1 * math.sin(2 * math.pi * i / seg)) for i in range(seg)]
    return frustum(name, p0, z0, p1, z1, mat, top=top)


def pyramid(name, poly, z0, apex_z, mat, apex=None):
    poly = ccw(poly)
    n = len(poly)
    if apex is None:
        apex = (sum(p[0] for p in poly) / n, sum(p[1] for p in poly) / n)
    verts = [(x, y, z0) for x, y in poly] + [(apex[0], apex[1], apex_z)]
    faces = [(i, (i + 1) % n, n) for i in range(n)]
    return new_mesh(name, verts, faces, [mat])


def join(objs, name):
    """Join objects into one (keeps materials); returns the result."""
    objs = [o for o in objs if o is not None]
    if len(objs) == 1:
        objs[0].name = name
        return objs[0]
    ctx = {"active_object": objs[0], "selected_editable_objects": objs, "object": objs[0]}
    with bpy.context.temp_override(**ctx):
        bpy.ops.object.join()
    objs[0].name = name
    return objs[0]


# ------------------------------------------------------- facade components


def ring_band(name, poly, z0, z1, out, mat, inset=0.0):
    """A band around a plan polygon standing `out` proud of it (solid annulus)."""
    inner = offset_poly(poly, inset) if inset else ccw(poly)
    outer = offset_poly(poly, out)
    n = len(inner)
    verts = []
    for loop, z in ((inner, z0), (outer, z0), (outer, z1), (inner, z1)):
        verts.extend([(x, y, z) for x, y in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * n, ((k + 1) % 4) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])


def banded_loft(name, outline_fn, z0, z1, pitch, band_h, out, glass, band,
                glass_in=0.0, first_band=True):
    """Curtain wall with continuous horizontal bands, as ONE loft.

    outline_fn(z, offset) -> CCW loop (fixed vertex count). Each storey-group
    of height `pitch` gets a proud band of height `band_h` at its base. The
    profile zig-zags (glass line -> band line), which costs 8n tris per band
    and has no hidden inner faces.
    """
    rings, rmats = [], []
    z = z0
    while z < z1 - 1e-6:
        zb = min(z + band_h, z1)
        zt = min(z + pitch, z1)
        rings.append((z, outline_fn(z, glass_in)))
        rings.append((z, outline_fn(z, out)))
        rings.append((zb, outline_fn(zb, out)))
        rings.append((zb, outline_fn(zb, glass_in)))
        rmats += [1, 1, 1, 0]
        if zt > zb + 1e-6:
            pass
        z = zt
    rings.append((z1, outline_fn(z1, glass_in)))
    # row r spans ring r -> r+1; the last appended pattern element covers the glass
    rmats = rmats[:len(rings) - 1]
    return loft(name, rings, None, row_mats=rmats, mats=[glass, band], cap_top=True, cap_bottom=True)


def pier_grid(name, poly, z0, z1, spacing, width, depth, mat, skip_short=4.0, corners=True, min_count=2):
    """Vertical piers (fins) standing on each edge of a plan polygon.

    Piers are evenly distributed so each edge reads as a regular rhythm; one
    joined mesh. Boxes are open at the bottom (sitting on something).
    """
    objs = []
    k = 0
    for p0, p1, L, nrm in edges(poly):
        if L < skip_short:
            continue
        count = max(min_count, int(round(L / spacing)) + 1)
        ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
        yaw = math.atan2(uy, ux)
        for i in range(count):
            if not corners and (i == 0 or i == count - 1):
                continue
            t = (width / 2 + (L - width) * i / (count - 1)) if count > 1 else L / 2
            cx = p0[0] + ux * t + nrm[0] * depth / 2
            cy = p0[1] + uy * t + nrm[1] * depth / 2
            objs.append(box(f"{name}_{k}", cx, cy, z0, z1, width, depth, mat, yaw=yaw))
            k += 1
    return join(objs, name) if objs else None


def spandrels(name, poly, zs, h, out, mat):
    """Horizontal bands (ring_band) at each z in zs."""
    objs = [ring_band(f"{name}_{i}", poly, z, z + h, out, mat) for i, z in enumerate(zs)]
    return join(objs, name) if objs else None


def lit_windows(name, poly, bands, spacing, density, seed=0.0, out=0.08, margin=0.6,
                mat="sand_Glow", gap=0.5, edge_filter=None, suffix="_glow"):
    """Night skin: scattered lit panes laid just outside a facade.

    `bands` = [(z0, z1)] storey bands; each edge is cut into panes of about
    `spacing` metres and a deterministic hash lights roughly `density` of them.
    """
    verts, faces = [], []
    for ei, (p0, p1, L, nrm) in enumerate(edges(poly)):
        if L < spacing * 0.8:
            continue
        if edge_filter and not edge_filter(ei, p0, p1, nrm):
            continue
        cnt = max(1, int(round(L / spacing)))
        step = L / cnt
        ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
        for bi, (z0, z1) in enumerate(bands):
            za, zb = z0 + margin, z1 - margin
            if zb - za < 0.5:
                continue
            for i in range(cnt):
                if hash01(seed + ei * 71.3 + bi * 13.7 + i * 3.11) > density:
                    continue
                a, b = i * step + gap / 2, (i + 1) * step - gap / 2
                pa = (p0[0] + ux * a + nrm[0] * out, p0[1] + uy * a + nrm[1] * out)
                pb = (p0[0] + ux * b + nrm[0] * out, p0[1] + uy * b + nrm[1] * out)
                k = len(verts)
                verts += [(pa[0], pa[1], za), (pb[0], pb[1], za), (pb[0], pb[1], zb), (pa[0], pa[1], zb)]
                faces.append((k, k + 1, k + 2, k + 3))
    if not faces:
        return None
    return new_mesh(name + suffix, verts, faces, [mat], recalc=False)


def panes(name, poly, bands, spacing, mat="glass", out=0.06, margin=0.6, gap=0.6, edge_filter=None):
    """Punched-window graphics: dark outward quads on a solid wall (style s.5)."""
    return lit_windows(name, poly, bands, spacing, 1.01, out=out, margin=margin, mat=mat, gap=gap,
                       edge_filter=edge_filter, suffix="_panes")


def floors(z0, z1, pitch):
    """[(zb, zt)] storey bands of about `pitch` between z0 and z1."""
    n = max(1, int(round((z1 - z0) / pitch)))
    h = (z1 - z0) / n
    return [(z0 + i * h, z0 + (i + 1) * h) for i in range(n)]


def lit_loop_windows(name, outline_fn, bands, density, seed=0.0, out=0.08, margin=0.6,
                     mat="sand_Glow", stride=1, subdiv=1, gap=0.0):
    """Night skin for lofted (curved) shafts: one pane per outline segment."""
    verts, faces = [], []
    for bi, (z0, z1) in enumerate(bands):
        za, zb = z0 + margin, z1 - margin
        if zb - za < 0.5:
            continue
        lo, hi = outline_fn(za, out), outline_fn(zb, out)
        n = len(lo)
        for i in range(0, n, stride):
            j = (i + 1) % n
            for s in range(subdiv):
                if hash01(seed + bi * 131.7 + i * 7.13 + s * 0.71) > density:
                    continue
                t0 = s / subdiv + gap / 2
                t1 = (s + 1) / subdiv - gap / 2

                def lerp(loop, t):
                    return (loop[i][0] + (loop[j][0] - loop[i][0]) * t, loop[i][1] + (loop[j][1] - loop[i][1]) * t)
                a0, a1, b0, b1 = lerp(lo, t0), lerp(lo, t1), lerp(hi, t0), lerp(hi, t1)
                k = len(verts)
                verts += [(a0[0], a0[1], za), (a1[0], a1[1], za), (b1[0], b1[1], zb), (b0[0], b0[1], zb)]
                faces.append((k, k + 1, k + 2, k + 3))
    if not faces:
        return None
    return new_mesh(name + "_glow", verts, faces, [mat], recalc=False)


def flat_quad(name, p0, p1, z0, z1, out, mat, nrm):
    """A single outward-facing vertical quad (signs, glow strips)."""
    a = (p0[0] + nrm[0] * out, p0[1] + nrm[1] * out)
    b = (p1[0] + nrm[0] * out, p1[1] + nrm[1] * out)
    verts = [(a[0], a[1], z0), (b[0], b[1], z0), (b[0], b[1], z1), (a[0], a[1], z1)]
    return new_mesh(name, verts, [(0, 1, 2, 3)], [mat], recalc=False)


def glow_ring(name, poly, z0, z1, out, mat):
    """An outward-facing open band (crown light lines)."""
    loop = offset_poly(poly, out)
    n = len(loop)
    verts = [(x, y, z0) for x, y in loop] + [(x, y, z1) for x, y in loop]
    faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return new_mesh(name + "_glow", verts, faces, [mat], recalc=False)


def glow_cap(name, poly, z, mat):
    """Upward-facing lit plane (lit roof/skylight seen from above)."""
    poly = ccw(poly)
    verts = [(x, y, z) for x, y in poly]
    return new_mesh(name + "_glow", verts, [tuple(range(len(poly)))], [mat], recalc=False)


# --------------------------------------------------------------- roof kit


def hvac_cluster(name, cx, cy, z, yaw, w, d, seed=0.0, mat="steel", mat2="roofd", fans=True, hmax=4.3):
    """A tidy cluster of plant boxes within a w x d footprint (style bible s.10)."""
    objs = []
    cols = max(1, int(w // 6))
    rows = max(1, int(d // 6))
    cw, cd = w / cols, d / rows
    k = 0
    for i in range(cols):
        for j in range(rows):
            hv = hash01(seed + i * 7.1 + j * 3.3)
            if hv < 0.18:
                continue
            bw, bd = cw * (0.6 + 0.25 * hv), cd * (0.55 + 0.3 * hash01(seed + i + j * 9.1))
            h = min(1.6 + 2.2 * hash01(seed * 3 + i * 1.7 + j), hmax - (0.5 if fans else 0.0))
            lx = -w / 2 + cw * (i + 0.5)
            ly = -d / 2 + cd * (j + 0.5)
            px, py = rot2((lx, ly), yaw)
            objs.append(box(f"{name}_{k}", cx + px, cy + py, z, z + h, bw, bd, mat, yaw=yaw, bev=0.12))
            if fans and hv > 0.6:
                objs.append(cylinder(f"{name}_f{k}", cx + px, cy + py, z + h, z + h + 0.5,
                                     min(bw, bd) * 0.3, mat2, seg=8))
            k += 1
    return join(objs, name) if objs else None


def antenna(name, x, y, z0, h, r=0.35, mat="steel", tip_mat="red_Glow"):
    a = cylinder(name, x, y, z0, z0 + h, r, mat, seg=6, r1=r * 0.5)
    b = cylinder(name + "_tip_glow", x, y, z0 + h, z0 + h + 1.2, r * 1.6, tip_mat, seg=6)
    return [a, b]


def helipad(name, cx, cy, z, r, yaw=0.0):
    pad = cylinder(name, cx, cy, z, z + 0.25, r, "roofd", seg=16)
    ring = ring_band(name + "_ring", ellipse(r * 0.78, r * 0.78, 16, cx, cy), z + 0.25, z + 0.3, 0.6, "white")
    h1 = box(name + "_h1", cx + rot2((-r * 0.25, 0), yaw)[0], cy + rot2((-r * 0.25, 0), yaw)[1], z + 0.25, z + 0.32, 0.9, r * 0.9, "white", yaw)
    h2 = box(name + "_h2", cx + rot2((r * 0.25, 0), yaw)[0], cy + rot2((r * 0.25, 0), yaw)[1], z + 0.25, z + 0.32, 0.9, r * 0.9, "white", yaw)
    h3 = box(name + "_h3", cx, cy, z + 0.25, z + 0.32, r * 0.5, 0.9, "white", yaw)
    return join([pad, ring, h1, h2, h3], name)


def tree(name, x, y, z, h=6.0, r=2.4, mat="leaf", seg=7):
    trunk = cylinder(name + "_t", x, y, z, z + h * 0.45, 0.35, "rust", seg=5)
    crown = cylinder(name + "_c", x, y, z + h * 0.35, z + h, r, mat, seg=seg, r1=r * 0.55)
    return join([trunk, crown], name)


def tree_row(name, p0, p1, z, n, h=6.0, r=2.2, seed=0.0):
    objs = []
    for i in range(n):
        t = (i + 0.5) / n
        x = p0[0] + (p1[0] - p0[0]) * t
        y = p0[1] + (p1[1] - p0[1]) * t
        hv = hash01(seed + i)
        objs.append(tree(f"{name}_{i}", x, y, z, h * (0.85 + 0.3 * hv), r * (0.85 + 0.3 * hv),
                         "leaf" if hv > 0.35 else "leafd"))
    return join(objs, name) if objs else None


def plinth(name, poly, h=0.4, out=3.0, mat="stone"):
    """Sidewalk/plaza apron that grounds the model (style bible s.13)."""
    return prism(name, offset_poly(poly, out), 0.0, h, mat, bev=0.1, bottom=True)


# ------------------------------------------------------------------ export


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def recalc_all():
    for o in bpy.data.objects:
        if o.type != "MESH" or o.name.endswith("_glow") or o.name.endswith("_panes"):
            continue
        bm = bmesh.new()
        bm.from_mesh(o.data)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(o.data)
        bm.free()


def bbox():
    mn = Vector((1e12,) * 3)
    mx = Vector((-1e12,) * 3)
    for o in bpy.data.objects:
        if o.type != "MESH":
            continue
        for v in o.data.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    return mn, mx


def recenter_xy():
    """Shift all geometry so the XY bbox centre is at the origin; returns the shift."""
    mn, mx = bbox()
    dx, dy = -(mn.x + mx.x) / 2, -(mn.y + mx.y) / 2
    for o in bpy.data.objects:
        if o.type == "MESH":
            for v in o.data.vertices:
                v.co.x += dx
                v.co.y += dy
    return dx, dy


def tri_count():
    t = 0
    for o in bpy.data.objects:
        if o.type == "MESH":
            o.data.calc_loop_triangles()
            t += len(o.data.loop_triangles)
    return t


def merge_by_material(prefix):
    """Join all non-glow meshes into one object and all glow into another.

    Keeps the export small and the object list readable; the app merges to
    two buffers anyway.
    """
    body = [o for o in bpy.data.objects if o.type == "MESH" and not o.name.endswith("_glow")]
    glow = [o for o in bpy.data.objects if o.type == "MESH" and o.name.endswith("_glow")]
    out = []
    if body:
        out.append(join(body, prefix + "_body"))
    if glow:
        out.append(join(glow, prefix + "_night_glow"))
    return out


def export(slug, outdir):
    """Save <slug>.blend and leak-proof export <slug>.glb (mesh objects only)."""
    for o in bpy.data.objects:
        o.select_set(False)
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    glb = os.path.join(outdir, slug + ".glb")
    bpy.ops.export_scene.gltf(filepath=glb, export_format="GLB", use_selection=True,
                              export_apply=True, export_cameras=False, export_lights=False,
                              export_animations=False, export_yup=True, export_texcoords=False,
                              export_normals=True, export_materials="EXPORT")
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(outdir, slug + ".blend"), compress=True)
    return glb


# --------------------------------------------------------------- harness

KX = 111320.0 * math.cos(math.radians(37.79))  # metres per degree lon at SF
KY = 110540.0                                    # metres per degree lat


def run(slug, build_fn, here, center_lonlat, target_h):
    """Build, recentre on the bbox, export; print the manifest anchor.

    Geometry is authored around `center_lonlat` (the OSM footprint's oriented
    bounding-box centre). Recentring moves the bbox centre to the origin, so the
    anchor the loader needs is that centre shifted back by the same amount.
    """
    import sys
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out = argv[argv.index("--out") + 1] if "--out" in argv else here
    reset()
    build_fn()
    recalc_all()
    merge_by_material(slug)
    dx, dy = recenter_xy()
    mn, mx = bbox()
    if 1e-4 < abs(mx.z - target_h) <= 0.03 * target_h:
        # normalize the crest to the verified height exactly (ADDRESS-TO-ASSET
        # stage 2), so the loader's targetHeightM / measured scale lands at 1.0
        k = target_h / mx.z
        for o in bpy.data.objects:
            if o.type == "MESH":
                for v in o.data.vertices:
                    v.co.z *= k
        print(f"[{slug}] z normalized x{k:.5f}")
        mn, mx = bbox()
    lon = center_lonlat[0] - dx / KX
    lat = center_lonlat[1] - dy / KY
    top = mx.z
    print(f"[{slug}] bbox {tuple(round(v, 3) for v in mn)} {tuple(round(v, 3) for v in mx)}"
          f" tris {tri_count()} anchor [{lon:.7f}, {lat:.7f}]")
    if abs(top - target_h) > 0.02:
        print(f"[{slug}] WARNING top {top:.3f} != target {target_h}")
    export(slug, out)
    return lon, lat


def tube(name, a, b, w, d, nrm2, mat):
    """Rectangular bar from 3-D point a to b: w wide across, d deep along the
    horizontal outward normal nrm2 (a facade brace, a strut, a mast)."""
    A, B = Vector(a), Vector(b)
    u = (B - A).normalized()
    n = Vector((nrm2[0], nrm2[1], 0.0)).normalized()
    side = n.cross(u).normalized()
    n = u.cross(side).normalized()
    verts = []
    for P in (A, B):
        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            verts.append(tuple(P + side * (sx * w / 2) + n * (sy * d / 2)))
    faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return new_mesh(name, verts, faces, [mat])


def loft_fins(name, plan_fn, z0, z1, spacing, w, d, mat, skip_short=4.0, corners=False):
    """Vertical mullion fins that follow a tapering loft (plan_fn(z, off))."""
    lo, hi = ccw(plan_fn(z0, 0.0)), ccw(plan_fn(z1, 0.0))
    objs = []
    n = len(lo)
    for i in range(n):
        a0, a1 = lo[i], lo[(i + 1) % n]
        b0, b1 = hi[i], hi[(i + 1) % n]
        L = math.dist(a0, a1)
        if L < skip_short:
            continue
        cnt = max(1, int(round(L / spacing)))
        nx, ny = (a1[1] - a0[1]) / L, -(a1[0] - a0[0]) / L
        rng = range(0, cnt + 1) if corners else range(1, cnt)
        for k in rng:
            t = k / cnt
            pa = (a0[0] + (a1[0] - a0[0]) * t + nx * d / 2, a0[1] + (a1[1] - a0[1]) * t + ny * d / 2, z0)
            pb = (b0[0] + (b1[0] - b0[0]) * t + nx * d / 2, b0[1] + (b1[1] - b0[1]) * t + ny * d / 2, z1)
            objs.append(tube(f"{name}_{i}_{k}", pa, pb, w, d, (nx, ny), mat))
    return join(objs, name) if objs else None


def shaft(name, plan, z0, z1, pitch, glass="glass", band="trim", band_h=0.9, band_out=0.35,
          fins=None, lit=0.3, seed=0.0, lit_spacing=3.2, lit_mat="sand_Glow", glass_in=-0.2):
    """A straight prism tower section on `plan`: banded curtain wall, optional
    vertical fins (spacing, width, depth, mat), and its lit-window night skin."""
    fn = lambda z, off: offset_poly(plan, off)  # noqa: E731
    banded_loft(name, fn, z0, z1, pitch, band_h, band_out, material(glass), material(band),
                glass_in=glass_in)
    if fins:
        sp, w, d, m = fins
        pier_grid(name + "_fins", offset_poly(plan, glass_in), z0, z1, sp, w, d + abs(glass_in), m,
                  skip_short=sp * 0.9, corners=True)
    if lit:
        bands = [(z + band_h, min(z + pitch, z1)) for z in
                 [z0 + i * pitch for i in range(int((z1 - z0) / pitch + 0.999))]]
        lit_windows(name + "_win", offset_poly(plan, glass_in), bands, lit_spacing, lit, seed=seed,
                    out=0.08 + (fins[2] if fins else 0.0), margin=0.5, mat=lit_mat, gap=0.4)


def punched_block(name, plan, z0, z1, pitch, wall="cream", win="glass", spacing=3.2,
                  gap=1.2, margin=0.9, lit=0.3, seed=0.0, bev=0.15, edge_filter=None):
    """Solid masonry/precast block with punched windows and a night skin."""
    prism(name, plan, z0, z1, wall, bev=bev)
    bands = floors(z0, z1, pitch)
    panes(name, plan, bands, spacing, mat=win, gap=gap, margin=margin, edge_filter=edge_filter)
    if lit:
        lit_windows(name + "_win", plan, bands, spacing, lit, seed=seed, out=0.1, margin=margin,
                    gap=gap, edge_filter=edge_filter)


def roof_kit(name, plan, z, seed=0.0, parapet=1.2, pmat="trim", deck="roofd", plant_frac=0.45,
             yaw=0.0):
    """Designed roof (style s.10): parapet, deck, one tidy plant cluster."""
    prism(name + "_deck", offset_poly(plan, -0.4), z - 0.3, z + 0.05, deck)
    ring_band(name + "_parapet", offset_poly(plan, -0.6), z, z + parapet, 0.6, pmat)
    xs = [p[0] for p in plan]
    ys = [p[1] for p in plan]
    cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
    # plant footprint: a fraction of the roof's inscribed extent along yaw
    us = [rot2((x - cx, y - cy), -yaw) for x, y in plan]
    w = (max(u[0] for u in us) - min(u[0] for u in us)) * plant_frac
    d = (max(u[1] for u in us) - min(u[1] for u in us)) * plant_frac
    hvac_cluster(name + "_plant", cx, cy, z, yaw, w, d, seed=seed)


def arched_panes(name, poly, z0, z1, spacing, width, mat="glass", out=0.06, seg=5, edge_filter=None,
                 suffix="_panes"):
    """Round-headed windows/arches on every edge of a plan: rectangle from z0
    rising to a semicircle that peaks at z1 (an arcade, a top-floor loggia)."""
    verts, faces = [], []
    r = width / 2
    zs = z1 - r
    for ei, (p0, p1, L, nrm) in enumerate(edges(poly)):
        if L < spacing * 0.8 or (edge_filter and not edge_filter(ei, p0, p1, nrm)):
            continue
        cnt = max(1, int(round(L / spacing)))
        step = L / cnt
        ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
        for i in range(cnt):
            c = (i + 0.5) * step
            prof = [(-r, z0), (r, z0)]
            for k in range(seg + 1):
                a = math.pi * k / seg
                prof.append((r * math.cos(a), zs + r * math.sin(a)))
            prof = prof[:2] + prof[2:]
            base = len(verts)
            for u, z in prof:
                t = c + u
                verts.append((p0[0] + ux * t + nrm[0] * out, p0[1] + uy * t + nrm[1] * out, z))
            # (-r,z0) (r,z0) then arc from angle 0 (r,zs) to pi (-r,zs): CCW seen from outside
            faces.append(tuple(range(base, base + len(prof))))
    if not faces:
        return None
    return new_mesh(name + suffix, verts, faces, [mat], recalc=False)


def cornice(name, poly, z, h=1.2, out=1.0, mat="cream"):
    """A projecting cornice: a slab stepping out over a smaller fillet."""
    a = ring_band(name + "_fillet", poly, z, z + h * 0.4, out * 0.45, mat)
    b = prism(name + "_slab", offset_poly(poly, out), z + h * 0.4, z + h, mat, bev=0.12)
    return join([a, b], name)
