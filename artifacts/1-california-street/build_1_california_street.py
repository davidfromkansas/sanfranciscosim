"""Deterministic Blender build of the SF-SIM miniature One California Street.

    blender -b --python build_1_california_street.py -- [--out DIR]

One California (Welton Becket Associates, 1969), where California Street
meets Market and Drumm: a 32-storey square tower with chamfered corners,
tall white piers running unbroken from the base to a solid white crown
band, dark glass strips between them, a recessed glazed lobby, and one of
the few rooftop corporate signs left in the Financial District (shown as a
plain red-and-navy panel). Helpers in tools/landmark-kit/toykit.py.
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

SLUG = "1-california-street"
CENTER = (-122.3971799, 37.7932335)  # OSM way 32612471, OBB centre
H_TOP = 133.5                         # published 438 ft roof (Wikipedia); LiDAR 135.2, OSM 140
H_LOBBY = 9.0
Z_CROWN = 126.0                       # bottom of the solid white crown band
N_FL = 30                              # storeys between lobby and crown (3.9 m, no sliver)

# OSM way 32612471 (m about CENTER): a 44 m square on the FiDi grid (faces bear
# ~80 / 170 / 260 / 350) with chamfered corners
PLAN = tk.ccw([(-18.0, -21.8), (-14.2, -24.4), (21.1, -18.9), (24.1, -14.8), (21.1, 2.9), (18.1, 21.1),
               (13.5, 24.2), (-21.2, 18.9), (-24.0, 14.2)])


def build():
    plan = clean_poly(PLAN)
    lob = tk.offset_poly(plan, -2.0)
    tk.prism("lobby", lob, 0.0, H_LOBBY, "glassd")
    tk.glow_ring("lobby_lit", lob, 0.5, H_LOBBY - 1.2, 0.05, "sand_Glow")
    tk.prism("transfer", plan, H_LOBBY, H_LOBBY + 1.2, "white", bev=0.15)
    # shaft: dark glass strips between deep white piers, unbroken to the crown
    tk.prism("shaft", plan, H_LOBBY + 1.2, Z_CROWN, "glass")
    tk.pier_grid("piers", plan, 0.0, Z_CROWN, 3.6, 1.0, 0.6, "white", skip_short=3.0)
    fl = storeys(H_LOBBY + 1.2, Z_CROWN, N_FL)
    bays("mullions", plan, [(a, a + 0.35) for a, _ in fl[1:]], None, 1.0, "glassd", out=0.04, edge_min=3.0)
    lit("shaft", plan, [(a + 0.5, b - 0.3) for a, b in fl], 3.6, 0.6, 0.27, 6.0, edge_min=3.0, out=0.08)
    # solid white crown band (the plant floors) and the rooftop sign panels
    tk.ring_band("crown", plan, Z_CROWN, H_TOP, 0.6, "white", inset=-1.6)
    tk.prism("deck", tk.offset_poly(plan, -1.6), Z_CROWN, H_TOP - 1.6, "roofd")
    tk.glow_ring("crown", tk.offset_poly(plan, 0.6), Z_CROWN + 0.4, Z_CROWN + 1.2, 0.05, "white_Glow")
    for k, (p0, p1) in enumerate(((PLAN[1], PLAN[2]), (PLAN[3], PLAN[5]))):   # south and east faces
        L = math.dist(p0, p1)
        n = ((p1[1] - p0[1]) / L, -(p1[0] - p0[0]) / L)
        for sign_mat, t0, t1, out in (("red", 0.22, 0.34, 0.65), ("navy", 0.36, 0.72, 0.65)):
            a = (p0[0] + (p1[0] - p0[0]) * t0, p0[1] + (p1[1] - p0[1]) * t0)
            b = (p0[0] + (p1[0] - p0[0]) * t1, p0[1] + (p1[1] - p0[1]) * t1)
            tk.flat_quad(f"sign{k}_{sign_mat}_panes", a, b, H_TOP - 4.6, H_TOP - 1.6, out, sign_mat, n)
            tk.flat_quad(f"sign{k}_{sign_mat}_glow", a, b, H_TOP - 4.4, H_TOP - 1.8, out + 0.05,
                         sign_mat + "_Glow", n)
    tk.hvac_cluster("plant", 0.0, 0.0, H_TOP - 1.6, math.radians(90 - 170.5), 22.0, 20.0, seed=2.0,
                    hmax=1.5)
    tk.plinth("plaza", plan, h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
