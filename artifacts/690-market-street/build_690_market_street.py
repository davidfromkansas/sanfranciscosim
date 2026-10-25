"""Deterministic Blender build of the SF-SIM miniature Old Chronicle Building.

    blender -b --python build_690_market_street.py -- [--out DIR]

690 Market Street, the Old Chronicle (de Young) Building (Burnham and Root,
1890; rebuilt by Willis Polk after 1906), now the Ritz-Carlton Club and
Residences: San Francisco's first skyscraper, a red-brick Richardsonian
Romanesque block on a rusticated brownstone base with a tall arcade of
round-arched windows, its 1962 aluminium skin stripped off in 2005-07 and
an eight-plus-storey beige residential addition stacked on top in tiers
under deep dark bracketed cornices. Helpers in tools/landmark-kit/toykit.py.
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

SLUG = "690-market-street"
CENTER = (-122.4031917, 37.7882682)  # OSM way 32946675, OBB centre
H_TOP = 95.0                          # published 312 ft roof (Wikipedia); LiDAR max 100.7 / median 96.0
H_BASE = 9.0                          # two rusticated brownstone storeys
H_HIST = 53.0                         # top of the historic brick block (12 storeys)
TIERS = [(H_HIST, 67.0, 0.8), (67.0, 80.5, 1.8), (80.5, H_TOP - 1.6, 2.8)]   # addition: (z0, z1, setback)

# OSM way 32946675 (m about CENTER): Market (SE face), Kearny (W) and Geary (S)
PLAN = tk.ccw([(7.0, 12.0), (20.0, -0.2), (3.4, -16.7), (-2.7, -20.5), (-16.3, -21.9), (-22.1, 12.8),
               (-7.1, 15.5), (-7.6, 18.6), (0.9, 20.2), (2.1, 18.5), (3.6, 16.6)])


def build():
    plan = clean_poly(PLAN)
    # rusticated brownstone base with shopfronts
    tk.prism("base", plan, 0.0, H_BASE, "rust", bev=0.15)
    bays("shops", plan, [(0.6, 5.6)], 4.2, 0.72, "glassd", end=0.8, edge_min=3.0)
    lit("shops", plan, [(0.8, 5.4)], 4.2, 0.72, 0.9, 1.0, end=0.8, edge_min=3.0)
    bays("base_win", plan, [(6.4, 8.4)], 2.6, 0.5, "glassd", end=0.8, edge_min=3.0)
    tk.ring_band("base_band", plan, H_BASE - 0.5, H_BASE + 0.3, 0.3, "terracotta")
    # red brick shaft: punched windows, a tall round-arched arcade, an attic
    tk.prism("brick", plan, H_BASE, H_HIST, "brick", bev=0.15)
    low = storeys(H_BASE + 0.3, 27.0, 4)
    bays("low_win", plan, [(a + 1.2, b - 0.8) for a, b in low], 2.5, 0.48, "glassd", end=0.9, edge_min=3.0)
    lit("low", plan, [(a + 1.2, b - 0.8) for a, b in low], 2.5, 0.44, 0.3, 3.0, end=0.9, edge_min=3.0)
    tk.ring_band("band1", plan, 27.0, 27.8, 0.25, "terracotta")
    tk.arched_panes("arcade", plan, 28.6, 41.5, 5.0, 3.4, mat="glassd", seg=4)
    tk.arched_panes("arcade_lit", plan, 29.2, 39.0, 5.0, 2.6, mat="sand_Glow", out=0.1, seg=4, suffix="_glow")
    tk.ring_band("band2", plan, 42.2, 43.0, 0.25, "terracotta")
    up = storeys(43.0, H_HIST - 1.2, 3)
    bays("up_win", plan, [(a + 0.9, b - 0.6) for a, b in up], 2.5, 0.48, "glassd", end=0.9, edge_min=3.0)
    lit("up", plan, [(a + 0.9, b - 0.6) for a, b in up], 2.5, 0.44, 0.3, 8.0, end=0.9, edge_min=3.0)
    tk.cornice("hist_cornice", plan, H_HIST - 1.2, h=1.2, out=0.7, mat="verdigris")
    # the 2005-07 residential addition: beige tiers under deep dark cornices
    for k, (z0, z1, sb) in enumerate(TIERS):
        p = tk.offset_poly(plan, -sb)
        tk.prism(f"add{k}", p, z0 - 0.3, z1, "sand", bev=0.15)
        n = max(1, int(round((z1 - z0) / 3.4)))
        rows = [(a + 1.0, b - 0.4) for a, b in storeys(z0, z1 - 0.6, n)]
        bays(f"add{k}_win", p, rows, 3.3, 0.6, "glassl", end=0.8, edge_min=3.0)
        lit(f"add{k}", p, rows, 3.3, 0.56, 0.34, 20.0 + k, end=0.8, edge_min=3.0)
        tk.prism(f"add{k}_eave", tk.offset_poly(p, 1.1), z1 - 0.15, z1 + 0.45, "ink", bev=0.08)
    top = tk.offset_poly(plan, -TIERS[-1][2] - 0.4)
    tk.prism("roof", top, H_TOP - 1.6, H_TOP - 0.6, "roofd")
    tk.hvac_cluster("plant", -2.0, -2.0, H_TOP - 0.6, math.radians(90 - 170.6), 14.0, 12.0, seed=5.0,
                    hmax=0.6, fans=False)
    tk.glow_ring("crown", tk.offset_poly(plan, -TIERS[-1][2]), H_TOP - 3.0, H_TOP - 2.0, 0.08, "sand_Glow")
    tk.plinth("apron", plan, h=0.25, out=2.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
