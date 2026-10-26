"""Deterministic Blender build of the SF-SIM miniature 580 California Street.

    blender -b --python build_580_california_street.py -- [--out DIR]

580 California Street (Johnson/Burgee, 1987): a 23-storey postmodern tower in
pale grey granite. Each face has flat granite corner piers with punched
windows framing a run of round glass bay windows; the top storey carries the
twelve hooded, faceless "Corporate Goddesses" (Muriel Castanis), three a side,
under a steep dark metal mansard with corner pavilions and a glass lantern.
Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "580-california-street"
CENTER = (-122.404152, 37.7929843)   # OSM way 148741786, OBB centre
H_TOP = 107.0                         # published roof 107 m / 351 ft (Wikipedia, Emporis)
H_BASE = 7.0
H_SHAFT = 89.0                        # 20 storeys of 4.1 m above the base
H_ATTIC = 95.0                        # goddess storey
H_EAVE = 96.5
L, W = 38.4, 37.2                    # OSM OBB 39.0 x 37.7; local +x = bearing 170.3 (toward California St)
YAW = tk.bearing_to_yaw(170.3)
BAY_W, BAY_D, BAYS, BAY_SP = 3.0, 1.1, 4, 4.6


def bays_for_face(hx, hy, axis, sign):
    """Half-hexagon bay outlines (local) on one face; axis 'x' faces +-x."""
    out = []
    for k in range(BAYS):
        u = (k - (BAYS - 1) / 2) * BAY_SP
        a, c = BAY_W / 2, BAY_W / 4
        if axis == "x":
            x0 = sign * hx
            pts = [(x0, u - a), (x0 + sign * BAY_D, u - c), (x0 + sign * BAY_D, u + c), (x0, u + a)]
        else:
            y0 = sign * hy
            pts = [(u - a, y0), (u - c, y0 + sign * BAY_D), (u + c, y0 + sign * BAY_D), (u + a, y0)]
        out.append(tk.ccw(tk.xform(pts, YAW)))
    return out


def not_back(ei, p0, p1, nrm):
    """Edge filter: skip a bay's back edge, which lies in the wall (its normal faces the core)."""
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    return mx * nrm[0] + my * nrm[1] > 0.0


def build():
    plan = tk.xform(tk.rect(L, W), YAW)
    hx, hy = L / 2, W / 2
    # base: granite with tall arched openings and a warm lit lobby
    tk.prism("base", plan, 0.0, H_BASE, "stone", bev=0.15)
    tk.arched_panes("base_arches", plan, 0.4, H_BASE - 0.9, 4.6, 3.0, mat="glassd")
    tk.arched_panes("base_lit", plan, 0.6, H_BASE - 1.8, 4.6, 2.2, mat="sand_Glow", out=0.1, suffix="_glow")
    tk.ring_band("base_band", plan, H_BASE, H_BASE + 0.6, 0.3, "concrete")
    # shaft: flat granite with punched windows on the corner piers ...
    bands = tk.floors(H_BASE + 0.6, H_SHAFT, 4.1)
    tk.prism("shaft", plan, H_BASE + 0.6, H_SHAFT, "stone", bev=0.12)
    corner = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            corner.append(tk.ccw(tk.xform(tk.rect(7.0, 7.0, sx * (hx - 3.5), sy * (hy - 3.5)), YAW)))
    for i, cp in enumerate(corner):
        # only the outward faces of each corner zone carry windows
        tk.panes(f"corner_{i}", cp, bands, 3.5, mat="glassd", gap=1.6, margin=0.9,
                 edge_filter=lambda ei, p0, p1, nrm, cp=cp: _outer_edge(p0, p1, nrm))
        tk.lit_windows(f"corner_{i}_win", cp, bands, 3.5, 0.25, seed=3.1 + i, out=0.1, margin=0.9, gap=1.6,
                       edge_filter=lambda ei, p0, p1, nrm, cp=cp: _outer_edge(p0, p1, nrm))
    # ... framing four round glass bays per face that run the full shaft
    bays = []
    for axis, sign in (("x", 1), ("x", -1), ("y", 1), ("y", -1)):
        bays += bays_for_face(hx, hy, axis, sign)
    for i, b in enumerate(bays):
        tk.prism(f"bay_{i}", b, H_BASE + 0.6, H_SHAFT, "glassl", bottom=False)
        # granite spandrel strips every other storey: flat outward quads, not rings (tri budget)
        tk.panes(f"bay_{i}_sp", b, [(z - 0.35, z + 0.35) for z, _ in bands[2::2]], 1.2, mat="stone", out=0.06,
                 margin=0.0, gap=0.0, edge_filter=not_back)
    for i, b in enumerate(bays):
        tk.lit_windows(f"bay_{i}_win", b, bands, 1.2, 0.22, seed=11.0 + i * 1.7, out=0.12, margin=0.8, gap=0.2,
                       edge_filter=not_back)
    # the goddess storey: a cornice band, the attic, and three hooded figures per side
    tk.cornice("shaft_cornice", plan, H_SHAFT, h=0.9, out=0.5, mat="concrete")
    tk.prism("attic", tk.offset_poly(plan, -0.6), H_SHAFT + 0.9, H_ATTIC, "stone")
    tk.panes("attic_win", tk.offset_poly(plan, -0.6), [(H_SHAFT + 0.9, H_ATTIC)], 3.2, mat="glassd", gap=1.4, margin=0.9)
    tk.lit_windows("attic_lit", tk.offset_poly(plan, -0.6), [(H_SHAFT + 0.9, H_ATTIC)], 3.2, 0.5, seed=7.7,
                   out=0.1, margin=0.9, gap=1.4)
    for k, (p0, p1, Le, nrm) in enumerate(tk.edges(plan)):
        ux, uy = (p1[0] - p0[0]) / Le, (p1[1] - p0[1]) / Le
        for j, t in enumerate((0.3, 0.5, 0.7)):
            cx = p0[0] + ux * Le * t - nrm[0] * 0.1
            cy = p0[1] + uy * Le * t - nrm[1] * 0.1
            # semantically enlarged (real figures are 3.7 m) so the hooded shapes read from the aerial view
            cx, cy = cx + nrm[0] * 0.5, cy + nrm[1] * 0.5
            tk.cylinder(f"goddess_{k}_{j}", cx, cy, H_SHAFT + 0.9, H_SHAFT + 5.0, 1.3, "white", seg=6, r1=0.7)
            tk.cylinder(f"goddess_head_{k}_{j}", cx, cy, H_SHAFT + 5.0, H_SHAFT + 6.1, 0.75, "white", seg=6, r1=0.15)
    tk.cornice("eave", tk.offset_poly(plan, -0.6), H_ATTIC, h=1.5, out=0.9, mat="concrete")
    # steep dark metal mansard, four corner pavilions and a glass lantern
    m0 = tk.offset_poly(plan, -0.8)
    m1 = tk.xform(tk.rect(L - 14.0, W - 14.0), YAW)
    tk.frustum("mansard", m0, H_EAVE, m1, 103.0, "roofd")
    for sx in (-1, 1):
        for sy in (-1, 1):
            pv = tk.xform(tk.rect(5.0, 5.0, sx * (hx - 3.6), sy * (hy - 3.6)), YAW)
            tk.prism(f"pavilion_{sx}_{sy}", pv, H_EAVE, 101.0, "roofd")
            tk.pyramid(f"pavilion_roof_{sx}_{sy}", pv, 101.0, 103.5, "copper")
    lan = tk.xform(tk.rect(8.0, 8.0), YAW)
    tk.prism("lantern", lan, 103.0, 105.2, "glassl")
    tk.glow_ring("lantern_lit", lan, 103.3, 104.9, 0.06, "white_Glow")
    tk.pyramid("lantern_roof", tk.offset_poly(lan, 0.3), 105.2, H_TOP, "copper")
    tk.plinth("plaza", plan, h=0.3, out=3.0)
    p0, p1 = tk.xform([(hx + 2.2, -hy + 5), (hx + 2.2, hy - 5)], YAW)   # California St trees
    tk.tree_row("trees", p0, p1, 0.3, 3, h=6.0, seed=1.7)


def _outer_edge(p0, p1, nrm):
    """True when an edge of a corner zone lies on the building's outer face."""
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    return mx * nrm[0] + my * nrm[1] > min(L, W) / 2 - 0.5


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
