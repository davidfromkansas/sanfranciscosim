"""Deterministic Blender build of the SF-SIM miniature 100 Pine Center.

    blender -b --python build_100_pine_center.py -- [--out DIR]

100 Pine Center (Hertzka & Knowles, 1972), at the north-west corner of Pine
and Front streets: a 33-storey box of continuous horizontal bands, cream
metal spandrels alternating with dark bronze-tinted ribbon windows, its
corners notched back in steps (read straight off OSM). A plain flat top
with a screened plant. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

# ---------------------------------------------- lean facade helpers (local)
# Flat outward quads (2 tris each) instead of extruded bands: the FiDi batch
# shares one vertex cap, so window graphics are skins over a solid prism.


def bays(name, poly, bands, spacing, frac, mat, out=0.06, density=1.01, seed=0.0, suffix="_panes",
         edge_min=2.0, efilter=None, end=0.0):
    """Per edge: cut into round(L/spacing) bays (one bay if spacing is None),
    put a quad `frac` of the bay wide in each, for every (z0, z1) band.
    `density` < 1 keeps a hashed subset (night lights)."""
    verts, faces = [], []
    for ei, (p0, p1, L, n) in enumerate(tk.edges(poly)):
        if L < edge_min or (efilter and not efilter(ei, p0, p1, n)):
            continue
        ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
        e = min(end, L * 0.25)
        cnt = 1 if spacing is None else max(1, int(round((L - 2 * e) / spacing)))
        step = (L - 2 * e) / cnt
        w = step * frac
        for bi, (z0, z1) in enumerate(bands):
            for i in range(cnt):
                if density < 1.0 and tk.hash01(seed + ei * 71.3 + bi * 13.7 + i * 3.11) > density:
                    continue
                c = e + (i + 0.5) * step
                a, b = c - w / 2, c + w / 2
                pa = (p0[0] + ux * a + n[0] * out, p0[1] + uy * a + n[1] * out)
                pb = (p0[0] + ux * b + n[0] * out, p0[1] + uy * b + n[1] * out)
                k = len(verts)
                verts += [(pa[0], pa[1], z0), (pb[0], pb[1], z0), (pb[0], pb[1], z1), (pa[0], pa[1], z1)]
                faces.append((k, k + 1, k + 2, k + 3))
    if not faces:
        return None
    return tk.new_mesh(name + suffix, verts, faces, [mat], recalc=False)


def lit(name, poly, bands, spacing, frac, density, seed, mat="sand_Glow", out=0.12, **kw):
    """Night skin aligned with `bays` (same bay maths), a hashed subset lit."""
    return bays(name, poly, bands, spacing, frac, mat, out=out, density=density, seed=seed,
                suffix="_glow", **kw)


def storeys(z0, z1, n, margin=0.0):
    """n equal storey bands between z0 and z1 (no sliver), trimmed by margin."""
    h = (z1 - z0) / n
    return [(z0 + i * h + margin, z0 + (i + 1) * h - margin) for i in range(n)]


def clean_poly(poly, tol=0.35):
    """Drop OSM vertices that sit on a straight edge (collinear within tol m)."""
    pts = list(poly)
    changed = True
    while changed and len(pts) > 3:
        changed = False
        for i in range(len(pts)):
            a, b, c = pts[i - 1], pts[i], pts[(i + 1) % len(pts)]
            L = math.dist(a, c)
            if L < 1e-6:
                continue
            d = abs((c[0] - a[0]) * (a[1] - b[1]) - (a[0] - b[0]) * (c[1] - a[1])) / L
            if d < tol:
                pts.pop(i)
                changed = True
                break
    return tk.ccw(pts)

SLUG = "100-pine-center"
CENTER = (-122.3990096, 37.7926517)  # OSM way 944025918, OBB centre
H_TOP = 145.0                         # published 476 ft roof (Wikipedia 145.09 m); LiDAR 144.4
H_LOBBY = 8.0
Z_ROOF = 141.0                         # top of the banded shaft; parapet/screen above
N_FL = 32                              # office storeys above the lobby (4.16 m, no sliver)
YAW = math.radians(90.0 - 170.5)

# OSM way 944025918 (m about CENTER, +x east, +y north): notched corners
PTS = [(8.0, 21.9), (8.2, 20.9), (9.4, 13.5), (13.4, 14.2), (13.8, 11.8), (17.4, 12.4), (22.0, -14.7),
       (18.1, -15.3), (18.5, -17.5), (-11.8, -22.6), (-12.2, -20.5), (-16.0, -21.1), (-20.3, 4.8),
       (-20.6, 6.3), (-22.4, 16.9), (-13.8, 18.3)]


def build():
    plan = clean_poly(PTS)
    lob = tk.offset_poly(plan, -1.5)
    tk.prism("lobby", lob, 0.0, H_LOBBY, "glassd")
    tk.glow_ring("lobby_lit", lob, 0.5, H_LOBBY - 1.2, 0.05, "sand_Glow")
    tk.pier_grid("columns", tk.offset_poly(plan, -0.6), 0.0, H_LOBBY, 6.0, 0.8, 0.8, "cream", skip_short=3.0)
    # banded shaft: cream body, one dark ribbon window per storey per face
    tk.prism("shaft", plan, H_LOBBY, Z_ROOF, "cream", bev=0.2)
    fl = storeys(H_LOBBY, Z_ROOF - 0.5, N_FL)
    ribbons = [(a + 1.5, b - 0.25) for a, b in fl]
    bays("ribbons", plan, ribbons, None, 1.0, "bronze", out=0.05, edge_min=1.5, end=0.35)
    lit("shaft", plan, ribbons, 3.4, 0.82, 0.27, 4.0, edge_min=3.0, end=0.35)
    # roof: cream parapet / screen, deck, plant, crown line
    tk.ring_band("screen", tk.offset_poly(plan, -0.3), Z_ROOF, H_TOP, 0.3, "cream")
    tk.prism("deck", tk.offset_poly(plan, -0.4), Z_ROOF - 0.3, Z_ROOF + 0.05, "roofd")
    tk.hvac_cluster("plant", 0.0, -1.0, Z_ROOF + 0.05, YAW, 24.0, 20.0, seed=11.0, hmax=3.6)
    tk.glow_ring("crown", plan, Z_ROOF + 1.0, Z_ROOF + 2.4, 0.32, "white_Glow")
    tk.plinth("apron", plan, h=0.25, out=2.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
