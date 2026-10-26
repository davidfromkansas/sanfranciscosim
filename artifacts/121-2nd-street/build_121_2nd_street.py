"""Deterministic Blender build of the SF-SIM miniature Rapp Building.

    blender -b --python build_121_2nd_street.py -- [--out DIR]

The Rapp Building, 121 Second Street (1907, seven storeys): a post-quake
Chicago-school commercial loft in the Second and Howard Streets historic district.
A pale grey-cream front of four bays of paired windows between plain piers, a
darker two-storey base with shopfronts, keystoned window heads on the sixth
floor and a deep bracketed cornice. It stands beside the 101 Second Street tower.
Recognition cue: the cream loft front with its heavy cornice on 2nd Street.
Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "121-2nd-street"
CENTER = (-122.3992013, 37.7878356)   # OSM way 80296751, OBB centre
H_TOP = 27.5                           # measured: DataSF LiDAR median roof 27.46 m (OSM height 27)
A = math.radians(45.0)                 # SoMa grid: u = bearing 45 (NE), v = bearing 315 (NW)


def G(poly):
    return tk.xform(poly, A)


def faces_dir(du, dv):
    def f(ei, p0, p1, n):
        gu = n[0] * math.cos(A) + n[1] * math.sin(A)
        gv = -n[0] * math.sin(A) + n[1] * math.cos(A)
        return gu * du + gv * dv > 0.7
    return f


def build():
    # OSM footprint in the SoMa frame; 2nd Street is the -u face (SW)
    plan = G([(-11.3, -9.0), (11.2, -9.5), (10.7, 9.4), (-11.2, 9.4)])
    front = faces_dir(-1, 0)
    rear = faces_dir(1, 0)
    # darker two-storey base with shopfronts, belt course
    tk.prism("base", plan, 0.0, 8.2, "concrete", bev=0.1)
    tk.panes("shops", plan, [(0.3, 4.2), (4.9, 7.8)], 2.3, mat="glassd", gap=0.7, margin=0.2, edge_filter=front)
    tk.lit_windows("shop_lit", plan, [(0.3, 3.6)], 4.6, 0.9, seed=1.0, out=0.1, margin=0.3, gap=1.0, edge_filter=front)
    tk.ring_band("belt", plan, 8.0, 8.6, 0.3, "cream")
    # five upper storeys of paired windows; sixth-floor heads keyed by a band
    tk.punched_block("upper", plan, 8.6, 25.0, 3.28, wall="cream", win="glassd", spacing=2.3, gap=0.8, margin=0.6,
                     lit=0.3, seed=2.0, edge_filter=front)
    tk.panes("rear_win", plan, tk.floors(8.6, 25.0, 3.28), 3.0, mat="glassd", gap=1.4, margin=0.8, edge_filter=rear)
    tk.ring_band("sill_band", plan, 21.6, 22.1, 0.15, "cream")
    # four bays: piers stand proud of the front
    p0, p1 = G([(-11.3, -9.0), (-11.2, 9.4)])
    for k in range(1, 4):  # at the bay joints, clear of the window panes
        t = k / 4
        x = p0[0] + (p1[0] - p0[0]) * t
        y = p0[1] + (p1[1] - p0[1]) * t
        cx, cy = x + tk.rot2((-0.25, 0.0), A)[0], y + tk.rot2((-0.25, 0.0), A)[1]
        tk.box(f"pier_{k}", cx, cy, 8.6, 25.0, 0.5, 0.7, "cream", yaw=A)
    tk.cornice("cornice", plan, 25.0, h=1.6, out=1.1, mat="cream")
    tk.ring_band("parapet", tk.offset_poly(plan, 0.2), 26.6, H_TOP, 0.0, "cream", inset=-0.5)
    tk.prism("roof", tk.offset_poly(plan, -0.4), 26.4, 26.75, "roofd")
    c = G([(4.0, 0.0)])[0]
    tk.hvac_cluster("plant", c[0], c[1], 26.75, A, 6.0, 6.0, seed=3.0, hmax=0.7, fans=False)
    tk.plinth("sidewalk", plan, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
