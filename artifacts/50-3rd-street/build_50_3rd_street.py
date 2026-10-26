"""Deterministic Blender build of the SF-SIM miniature 50 Third Street hotel.

    blender -b --python build_50_3rd_street.py -- [--out DIR]

50 Third Street, now the Hyatt Regency San Francisco Downtown SOMA (built
1983 as the ANA Hotel; later Le Meridien, the Argent and Park Central). A
36-storey hotel slab on an elongated hexagonal plan that sits east-west
across a diamond-shaped SoMa lot, with 13-storey triangular wings at
its two ends and a three-storey podium filling the rest of the block
corner at Third and Jessie. Massing taken from the OSM building:parts.
Helpers in tools/landmark-kit/toykit.py.
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

SLUG = "50-3rd-street"
CENTER = (-122.4030999, 37.7865616)  # OSM way 118480404, OBB centre
H_TOP = 114.0                         # published 374 ft (Wikipedia); LiDAR max 118.6 incl. roof plant
H_POD = 13.0                           # 3-storey podium (building:parts 1240818462/463)
H_WING = 46.0                          # 13-storey wings (building:parts 1240818460/461), estimated
N_FL = 32                              # guest floors above the podium

# OSM building:parts, m about CENTER (+x east, +y north)
TOWER = [(-30.1, 9.8), (-20.1, 19.9), (22.1, 19.1), (31.5, 9.8), (22.5, 0.7), (-20.9, 1.0)]
WING_W = [(-20.9, 1.0), (-39.0, 1.0), (-30.1, 9.8)]
WING_E = [(22.5, 0.7), (31.5, 9.8), (40.7, 0.6)]
POD_N = [(-20.1, 19.9), (0.5, 40.4), (22.1, 19.1)]
POD_S = [(-39.0, 1.0), (-33.9, -4.0), (-35.6, -5.7), (-11.8, -29.3), (-0.5, -40.4), (24.6, -15.4),
         (40.7, 0.6), (22.5, 0.7), (-20.9, 1.0)]


def build():
    tower = tk.ccw(TOWER)
    for nm, p in (("pod_n", POD_N), ("pod_s", POD_S)):
        p = tk.ccw(p)
        tk.prism(nm, p, 0.0, H_POD, "stone", bev=0.15)
        bays(nm + "_glass", p, [(0.8, 5.0)], 4.5, 0.8, "glassd", end=0.8)
        bays(nm + "_win", p, [(7.0, 11.4)], 3.2, 0.55, "glass", end=0.8)
        lit(nm, p, [(1.0, 4.8)], 4.5, 0.8, 0.9, 3.0, end=0.8)
        tk.ring_band(nm + "_parapet", tk.offset_poly(p, -0.5), H_POD, H_POD + 0.9, 0.5, "trim")
        tk.prism(nm + "_roof", tk.offset_poly(p, -0.5), H_POD - 0.3, H_POD + 0.05, "steel")
    # the two 13-storey end wings (they rise from the ground behind the podium skin)
    for nm, p in (("wing_w", WING_W), ("wing_e", WING_E)):
        p = tk.ccw(p)
        tk.prism(nm, p, 0.0, H_WING, "sand", bev=0.15)
        wb = storeys(H_POD, H_WING - 1.0, 10)
        bays(nm + "_win", p, [(a + 0.9, b - 0.4) for a, b in wb], 3.0, 0.5, "glass", end=0.8)
        lit(nm, p, [(a + 0.9, b - 0.4) for a, b in wb], 3.0, 0.5, 0.35, 9.0, end=0.8)
        tk.ring_band(nm + "_cap", tk.offset_poly(p, -0.4), H_WING, H_WING + 0.8, 0.4, "trim")
    # tower: precast slab, punched hotel windows in storey rows
    z_roof = H_TOP - 6.0
    tk.prism("tower", tower, 0.0, z_roof, "sand", bev=0.2)
    fl = storeys(H_POD, z_roof - 1.0, N_FL)
    # window columns under one spandrel quad per storey (punched look, few triangles)
    bays("tower_win", tower, [(H_POD + 0.6, z_roof - 1.4)], 2.9, 0.5, "glass", out=0.05, end=0.8)
    bays("tower_spandrel", tower, [(a, a + 1.0) for a, _ in fl[1:]], None, 0.99, "sand", out=0.08,
         end=0.8)
    lit("tower", tower, [(a + 1.2, b - 0.3) for a, b in fl], 2.9, 0.46, 0.33, 13.0, end=0.8, out=0.42)
    # vertical precast piers on the long faces (the slab's dominant grain)
    tk.pier_grid("piers", tower, H_POD, z_roof, 8.7, 0.6, 0.35, "trim", skip_short=13.0)
    # crown: mechanical penthouse, screened, with a light band
    tk.prism("deck", tk.offset_poly(tower, -0.4), z_roof - 0.3, z_roof + 0.05, "roofd")
    tk.ring_band("parapet", tk.offset_poly(tower, -0.5), z_roof, z_roof + 1.2, 0.5, "trim")
    pent = tk.ccw([(-14.0, 5.0), (14.0, 5.0), (14.0, 15.5), (-14.0, 15.5)])
    tk.prism("penthouse", pent, z_roof, H_TOP, "sand", bev=0.15)
    tk.ring_band("pent_cap", pent, H_TOP - 0.8, H_TOP, 0.25, "trim")
    tk.glow_ring("crown", pent, H_TOP - 3.0, H_TOP - 1.2, 0.08, "sand_Glow")
    tk.plinth("apron", tk.ccw(POD_S), h=0.25, out=1.5)
    tk.plinth("apron_n", tk.ccw(POD_N), h=0.25, out=1.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
