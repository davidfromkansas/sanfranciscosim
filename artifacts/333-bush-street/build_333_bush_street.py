"""Deterministic Blender build of the SF-SIM miniature 333 Bush Street.

    blender -b --python build_333_bush_street.py -- [--out DIR]

333 Bush Street (Skidmore, Owings & Merrill, 1986): a 43-storey rose granite
office and condominium tower. A punched-window granite shaft with greenish
glass on an L-shaped plan whose south-west corner steps back in a staircase
(read straight off OSM), a dark louvred band where the offices end, and a
terraced "ziggurat" top of setback boxes over the seven condominium floors.
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

SLUG = "333-bush-street"
CENTER = (-122.4030673, 37.790554)   # OSM way 132125167, OBB centre
H_TOP = 151.0                         # published 495 ft (Wikipedia); LiDAR 150.45
BEARING = 170.6                       # OBB long axis
YAW = math.radians(90.0 - BEARING)
Z_SHAFT = 117.0                       # top of the full-plan shaft (photo: ~35 storeys)
N_FL = 33                              # storeys between the base and Z_SHAFT

# OSM way 132125167 (m about CENTER, +x east, +y north)
PTS = [(18.6, 29.3), (19.3, 25.1), (20, 20.9), (20.7, 16.7), (21.4, 12.3), (22.2, 7.4), (23.0, 2.9),
       (23.7, -1.5), (24.4, -5.9), (27.1, -21.8), (14.9, -23.8), (14.3, -20.3), (13.0, -12.8), (10.6, -13.2),
       (6.1, -13.9), (-2.6, -15.3), (-7.0, -16.0), (-12.0, -16.9), (-12.8, -12.1), (-17, -12.8), (-17.8, -7.9),
       (-22.0, -8.6), (-22.7, -4.5), (-23.4, -0.2), (-23.7, 1.7), (-24.2, 4.7), (-25.0, 9.2), (-25.7, 13.5),
       (-26.4, 17.6), (-27.1, 21.8), (-22.6, 22.6), (-18.1, 23.3), (-13.5, 24.0), (-9.1, 24.8), (-0.1, 26.2),
       (4.1, 26.9), (8.8, 27.7), (13.7, 28.5)]


def tier(w, d, n, cu, cv):
    """A setback box with square-notched corners, in the tower's own frame."""
    return tk.ccw(tk.xform(tk.notch_rect(w, d, n), YAW, *tk.rot2((cu, cv), YAW)))


def windows(name, plan, z0, z1, nfl, seed, col=2.9):
    """Granite punched windows: glass columns under a granite spandrel quad per storey."""
    fl = storeys(z0, z1, nfl)
    bays(name + "_col", plan, [(z0 + 0.5, z1 - 0.9)], col, 0.48, "glassd", out=0.05, end=0.7)
    bays(name + "_spd", plan, [(a, a + 1.5) for a, _ in fl[1:]], None, 0.995, "granite", out=0.08, end=0.0)
    lit(name, plan, [(a + 1.7, b - 0.3) for a, b in fl], col, 0.44, 0.3, seed, end=0.7, out=0.12)


def build():
    plan = clean_poly(PTS)
    tk.prism("base", plan, 0.0, 9.0, "granite", bev=0.2)
    bays("lobby", plan, [(0.6, 7.4)], 4.4, 0.82, "glassd", end=0.8)
    lit("lobby", plan, [(0.8, 7.2)], 4.4, 0.82, 0.85, 1.0, end=0.8)
    tk.ring_band("base_band", plan, 8.2, 9.0, 0.3, "stone")
    tk.prism("shaft", plan, 9.0, Z_SHAFT, "granite", bev=0.2)
    windows("shaft", plan, 9.0, Z_SHAFT - 4.0, N_FL - 1, 5.0)
    # the dark louvred band where the office floors end
    tk.ring_band("louvres", plan, Z_SHAFT - 4.0, Z_SHAFT, 0.12, "bronze")
    # terraced condominium top: setback boxes over the full-width (Bush Street) half
    # of the plan, clear of the stepped south-west corner
    tiers = [
        (Z_SHAFT, 125.0, tier(30.0, 42.0, 5.0, -10.5, 0.0)),
        (125.0, 133.0, tier(25.0, 34.0, 4.5, -10.5, 1.0)),
        (133.0, 141.0, tier(20.0, 26.0, 4.0, -10.5, 2.0)),
        (141.0, 147.0, tier(14.0, 17.0, 3.0, -10.5, 2.5)),
    ]
    for k, (za, zb, p) in enumerate(tiers):
        tk.prism(f"tier{k}", p, za - 0.3, zb, "granite", bev=0.15)
        n = max(1, int(round((zb - za) / 3.6)))
        windows(f"tier{k}", p, za + 0.3, zb - 0.6, n, 20.0 + k, col=3.2)
        tk.prism(f"tier{k}_deck", tk.offset_poly(p, -0.3), zb - 0.2, zb + 0.05, "roofd")
        tk.ring_band(f"tier{k}_rail", tk.offset_poly(p, -0.35), zb, zb + 0.9, 0.3, "stone")
    tk.prism("shaft_deck", tk.offset_poly(plan, -0.3), Z_SHAFT - 0.2, Z_SHAFT + 0.05, "roofd")
    tk.ring_band("shaft_rail", tk.offset_poly(plan, -0.35), Z_SHAFT, Z_SHAFT + 0.9, 0.3, "stone")
    top = tier(8.0, 9.0, 1.5, -10.5, 2.5)
    tk.prism("crown", top, 147.0, H_TOP, "granite", bev=0.12)
    tk.glow_ring("crown", top, 148.0, 150.2, 0.06, "sand_Glow")
    tk.plinth("apron", plan, h=0.25, out=2.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
