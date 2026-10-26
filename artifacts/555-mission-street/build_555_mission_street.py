"""Deterministic Blender build of the SF-SIM miniature 555 Mission Street.

    blender -b --python build_555_mission_street.py -- [--out DIR]

555 Mission Street (Kohn Pedersen Fox, 2008): a 33-storey office tower on
the south side of Mission between First and Second. A pale blue glass
prism with a fine grid of silvery vertical mullions and slim spandrels,
notched corners read straight off OSM, a tall glass lobby on the Mission
plaza and a glass screen crown that hides the roof plant. Helpers in
tools/landmark-kit/toykit.py.
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

SLUG = "555-mission-street"
CENTER = (-122.3985526, 37.7885313)  # OSM way 80296761, OBB centre
H_TOP = 147.0                         # published 482 ft (Wikipedia); LiDAR 142.5 = main roof
H_ROOF = 142.5
H_LOBBY = 10.0
N_FL = 32                              # office storeys above the lobby (4.13 m, no sliver)

# OSM footprint (m about CENTER, +x east, +y north). Faces bear 45 / 135 / 225 / 315;
# the NW face (315) is Mission Street.
PLAN = tk.ccw([(2.2, -29.4), (24.4, -8.6), (23.9, -8.0), (29.5, -2.6), (30.1, -3.3), (32.3, -0.8),
               (18.1, 13.5), (16.4, 11.8), (6.4, 21.8), (8.1, 23.5), (-0.8, 32.4), (-32.5, 0.9),
               (-9.1, -22.4), (-7.0, -20.3)])
YAW = math.radians(90.0 - 45.2)


def build():
    lob = tk.offset_poly(PLAN, -1.0)
    tk.prism("lobby", lob, 0.0, H_LOBBY, "glassl")
    tk.glow_ring("lobby_lit", lob, 0.6, H_LOBBY - 1.0, 0.05, "sand_Glow")
    tk.pier_grid("lobby_mullions", tk.offset_poly(PLAN, -0.5), 0.0, H_LOBBY, 4.5, 0.3, 0.4, "white",
                 skip_short=2.0)
    tk.prism("transfer", PLAN, H_LOBBY, H_LOBBY + 0.9, "white", bev=0.12)
    # shaft: silvery glass, a light fin every ~3 m and a slim spandrel at every storey
    z0, z1 = H_LOBBY + 0.9, H_ROOF
    tk.prism("shaft", PLAN, z0, z1, "glassl")
    tk.pier_grid("fins", PLAN, z0, z1, 3.1, 0.18, 0.3, "glassg", skip_short=2.5)
    bands = storeys(z0, z1, N_FL)
    bays("spandrels", PLAN, [(a, a + 0.4) for a, _ in bands[1:]], None, 1.0, "glassg", out=0.05, edge_min=1.0)
    lit("shaft", PLAN, [(a + 0.6, b - 0.3) for a, b in bands], 3.1, 0.82, 0.22, 5.0, out=0.34)
    # crown: glass screen standing above the roof, plant behind it, light line on top
    tk.prism("deck", tk.offset_poly(PLAN, -0.4), H_ROOF - 0.3, H_ROOF + 0.05, "roofd")
    tk.ring_band("screen", tk.offset_poly(PLAN, -0.25), H_ROOF, H_TOP - 0.6, 0.25, "glassl")
    tk.ring_band("screen_cap", tk.offset_poly(PLAN, -0.3), H_TOP - 0.6, H_TOP, 0.35, "white")
    tk.hvac_cluster("plant", 0.0, 0.0, H_ROOF + 0.05, YAW, 26.0, 22.0, seed=6.0, hmax=4.2)
    tk.glow_ring("crown", PLAN, H_TOP - 3.4, H_TOP - 1.2, 0.08, "white_Glow")
    tk.plinth("plaza", PLAN, h=0.25, out=3.0)
    # Mission Street plaza trees along the NW face
    a, b = tk.rot2((-24.0, 24.5), YAW), tk.rot2((20.0, 24.5), YAW)
    tk.tree_row("trees", (a[0], a[1]), (b[0], b[1]), 0.25, 4, h=6.0, seed=2.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
