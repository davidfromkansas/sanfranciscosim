"""Deterministic Blender build of the SF-SIM miniature White House building.

    blender -b --python build_white_house_building.py -- [--out DIR]

The White House (Raphael Weill & Co.) department store, Sutter x Grant (255 Sutter /
256 Grant), Albert Pissis, 1908, clad in white terra cotta: a five-storey palazzo
with a sweeping rounded corner at Sutter and Grant, a tall glazed shop base, three
storeys of windows under a heavy cornice, an attic storey and a roof balustrade.
The store closed in 1965; the upper floors are a parking garage and Banana
Republic has the ground floor. Recognition cue: the white curved corner. Helpers
in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "white-house-building"
CENTER = (-122.4047871, 37.7894368)   # OSM way 333827281, OBB centre
H_TOP = 32.1                           # measured: DataSF LiDAR median roof (balustrade/roof deck)
A = math.radians(9.0)                  # street grid: u = bearing 81 (E), v = bearing 351 (N)
U0, U1, V0, V1, R = -42.2, 42.0, -21.2, 21.2, 10.0


def G(poly):
    return tk.xform(poly, A)


def street(ei, p0, p1, n):
    """Sutter (N), Grant (W) and the rounded corner between them."""
    gu = n[0] * math.cos(A) + n[1] * math.sin(A)
    gv = -n[0] * math.sin(A) + n[1] * math.cos(A)
    return gv > 0.3 or gu < -0.3


def build():
    arc = [(U0 + R - R * math.sin(math.radians(a)), V1 - R + R * math.cos(math.radians(a))) for a in
           (0, 18, 36, 54, 72, 90)]
    plan = G([(U0, V0), (U1, V0), (U1, V1)] + arc)
    # shop base: big dark display windows on the street faces, lit at night
    tk.prism("base", plan, 0.0, 9.5, "white", bev=0.15)
    tk.panes("shopfronts", plan, [(0.4, 8.6)], 4.6, mat="glassd", gap=1.1, margin=0.3, edge_filter=street)
    tk.lit_windows("shop_lit", plan, [(0.4, 5.6)], 4.6, 0.95, seed=1.0, out=0.1, margin=0.4, gap=1.5,
                   edge_filter=street)
    tk.ring_band("base_band", plan, 9.5, 10.3, 0.35, "cream")
    # three storeys of paired windows
    tk.punched_block("body", plan, 10.3, 24.5, 4.73, wall="white", win="glassd", spacing=3.0, gap=1.2, margin=0.9,
                     lit=0.3, seed=2.0, edge_filter=street)
    tk.cornice("cornice", plan, 24.5, h=1.8, out=1.2, mat="cream")
    # attic storey and roof balustrade (garage deck behind)
    tk.punched_block("attic", tk.offset_poly(plan, -0.3), 26.3, 30.6, 4.3, wall="white", win="glassd", spacing=3.0,
                     gap=1.4, margin=1.0, lit=0.25, seed=3.0, edge_filter=street)
    tk.ring_band("balustrade", tk.offset_poly(plan, -0.3), 30.6, H_TOP, 0.0, "cream", inset=-0.5)
    tk.prism("deck", tk.offset_poly(plan, -1.0), 30.4, 30.7, "roofd")
    # rooftop parking deck (the upper floors are a garage): bay stripes, lift/stair house, lamps
    for row, v in enumerate((-9.0, 7.0)):
        for k in range(16):
            x, y = G([(-28.0 + k * 3.6, v)])[0]
            tk.box(f"stripe_{row}_{k}", x, y, 30.7, 30.75, 0.2, 5.0, "white", yaw=A)
    sh = G(tk.rect(9.0, 6.0, 33.0, -14.0))
    tk.prism("stair_house", sh, 30.7, 31.9, "cream", bev=0.1)
    for k, u in enumerate((-24.0, -4.0, 16.0)):
        tk.glow_cap(f"lamp_{k}", G(tk.rect(10.0, 1.2, u, -1.0)), 30.72, "sand_Glow")
    tk.plinth("sidewalk", plan, h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
