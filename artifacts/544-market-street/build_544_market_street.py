"""Deterministic Blender build of the SF-SIM miniature Flatiron Building.

    blender -b --python build_544_market_street.py -- [--out DIR]

The Flatiron Building, 540-544 Market Street at Sutter (Havens & Toepke, 1913;
SF Landmark 155): a ten-storey cream terracotta wedge on the sharp Market x
Sutter corner. Paired windows between tall piers, a stack of bay windows on the
narrow prow, round-arched top-floor windows and a deep bracketed cornice.
Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "544-market-street"
CENTER = (-122.4007731, 37.790027)   # OSM way 132125158, OBB centre
H_TOP = 36.6                          # published roof 36.58 m / 120 ft (Wikipedia, Emporis)
PTS = [[-11.94, 8.89], [-8.78, -12.25], [3.82, -0.01], [9.82, 5.81], [8.71, 12.24]]  # OSM footprint (m)
H_SHOP, H_TOPFLOOR, H_CORNICE, H_ROOF = 5.0, 30.2, 33.4, 35.0


def street_edges(plan):
    """Every edge except the windowless party wall (outward normal ~ west, 261 deg)."""
    out = []
    for p0, p1, L, nrm in tk.edges(plan):
        brg = math.degrees(math.atan2(nrm[0], nrm[1])) % 360
        if not 230 < brg < 290:
            out.append((p0, p1, L, nrm, brg))
    return out


def street(ei, p0, p1, nrm):
    brg = math.degrees(math.atan2(nrm[0], nrm[1])) % 360
    return not 230 < brg < 290


def flat(ei, p0, p1, nrm):
    """Street faces minus the prow, whose windows are on the bay stack."""
    brg = math.degrees(math.atan2(nrm[0], nrm[1])) % 360
    return street(ei, p0, p1, nrm) and not 60 < brg < 100


def build():
    plan = tk.ccw([tuple(p) for p in PTS])
    tk.prism("body", plan, 0.0, H_CORNICE, "terracotta", bev=0.1)
    # storefronts, a belt course, eight office floors, the arched top floor
    tk.panes("shops", plan, [(0.0, H_SHOP - 0.6)], 4.4, mat="glassd", margin=0.4, gap=0.9, edge_filter=street)
    tk.lit_windows("shops_lit", plan, [(0.0, H_SHOP - 0.6)], 4.4, 0.95, seed=1.0, out=0.1, margin=0.6, gap=1.2,
                   edge_filter=street)
    tk.ring_band("belt", plan, H_SHOP, H_SHOP + 0.6, 0.3, "cream")
    bands = tk.floors(H_SHOP + 0.6, H_TOPFLOOR, 3.05)
    tk.panes("windows", plan, bands, 2.2, mat="glassd", margin=0.6, gap=0.7, edge_filter=flat)
    tk.lit_windows("windows_lit", plan, bands, 2.2, 0.3, seed=4.4, out=0.1, margin=0.7, gap=0.8, edge_filter=flat)
    tk.arched_panes("top_arches", plan, H_TOPFLOOR + 0.3, H_CORNICE - 0.2, 4.4, 3.2, mat="glassd",
                    edge_filter=street)
    tk.arched_panes("top_lit", plan, H_TOPFLOOR + 0.5, H_CORNICE - 0.7, 4.4, 2.2, mat="sand_Glow", out=0.1,
                    edge_filter=street, suffix="_glow")
    # tall piers between the window pairs on Market and Sutter
    piers = []
    for k, (p0, p1, L, nrm, brg) in enumerate(street_edges(plan)):
        if L < 7.0:
            continue
        # piers sit in every other gap of the 2.2 m window rhythm, so they never cover a pane
        cnt = max(1, int(round(L / 2.2)))
        step = L / cnt
        ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
        for i in range(0, cnt + 1, 2):
            t = min(max(i * step, 0.4), L - 0.4)
            cx, cy = p0[0] + ux * t + nrm[0] * 0.2, p0[1] + uy * t + nrm[1] * 0.2
            piers.append(tk.box(f"pier_{k}_{i}", cx, cy, H_SHOP + 0.6, H_TOPFLOOR, 0.8, 0.4, "cream",
                                yaw=math.atan2(uy, ux)))
    tk.join(piers, "piers")
    # the prow (east, facing the Market x Sutter point): a stack of bay windows
    for p0, p1, L, nrm, brg in street_edges(plan):
        if 60 < brg < 100:
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            yaw = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
            bay = tk.xform([(-2.2, 0.0), (2.2, 0.0), (1.6, 1.0), (-1.6, 1.0)], yaw, mx, my)
            bay = tk.ccw(bay)
            tk.prism("prow_bay", bay, H_SHOP + 0.6, H_TOPFLOOR, "cream", bottom=False)
            tk.panes("prow_bay_win", bay, bands, 1.4, mat="glassd", margin=0.5, gap=0.3,
                     edge_filter=lambda ei, a, b, n, m=(mx, my): (n[0] * ((a[0] + b[0]) / 2 - m[0]) +
                                                                  n[1] * ((a[1] + b[1]) / 2 - m[1])) > 0.1)
            tk.lit_windows("prow_bay_lit", bay, bands, 1.4, 0.45, seed=8.0, out=0.1, margin=0.5, gap=0.3,
                           edge_filter=lambda ei, a, b, n, m=(mx, my): (n[0] * ((a[0] + b[0]) / 2 - m[0]) +
                                                                        n[1] * ((a[1] + b[1]) / 2 - m[1])) > 0.1)
    # deep bracketed cornice, parapet, roof
    tk.cornice("cornice", plan, H_CORNICE, h=1.6, out=1.3, mat="cream")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.2), H_ROOF, H_TOP, 0.3, "terracotta")
    tk.prism("roof", tk.offset_poly(plan, 0.0), H_ROOF - 0.2, H_ROOF + 0.15, "roofd")
    c = [sum(p[0] for p in plan) / len(plan), sum(p[1] for p in plan) / len(plan)]
    tk.box("stair_house", c[0] - 3.0, c[1] + 1.5, H_ROOF + 0.15, H_TOP + 0.4 - 0.4, 4.0, 3.5, "concrete")
    tk.hvac_cluster("plant", c[0] + 1.5, c[1] - 1.0, H_ROOF + 0.15, math.radians(-9), 6.0, 5.0, seed=2.0,
                    hmax=1.3)
    tk.plinth("sidewalk", plan, h=0.25, out=2.5)
    # Market Street trees on the SE face
    for p0, p1, L, nrm, brg in street_edges(plan):
        if 120 < brg < 150 and L > 15:
            a = (p0[0] + nrm[0] * 2.2, p0[1] + nrm[1] * 2.2)
            b = (p1[0] + nrm[0] * 2.2, p1[1] + nrm[1] * 2.2)
            tk.tree_row("trees", a, b, 0.25, 2, h=6.5, seed=5.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
