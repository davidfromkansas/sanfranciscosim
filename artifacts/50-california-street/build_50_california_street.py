"""Deterministic Blender build of the SF-SIM miniature 50 California Street.

    blender -b --python build_50_california_street.py -- [--out DIR]

50 California Street (Welton Becket & Associates, 1972; Union Bank Building):
a 37-storey pale grey slab at the foot of California Street. Every face is a
close comb of deep precast vertical fins over dark glass, framed by broad
solid corner piers and capped by a plain white band - a crisp ribbed box
over a plaza. A low pavilion fills the east side of the lot. Helpers in
tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "50-california-street"
CENTER = (-122.397383, 37.7940826)    # OSM way 32612484, OBB centre
H_TOP = 148.44                         # published roof (Wikipedia 148.44 m); LiDAR 153.71 (rooftop plant)
H_LOBBY = 7.0                          # INFERRED
H_FINS = 141.0                         # INFERRED: fins stop under a ~7 m solid white cap (photo)
H_PAVILION = 7.0                       # INFERRED: low pavilion on the east part of the lot
YAW = tk.bearing_to_yaw(81.0)          # local +x = bearing 81.0 (street grid), +y = 351.0

# Local plans (x ~ east, y ~ north) from the 11-node OSM outline: the tower is the
# 31.7 x 61 m rectangle, the eastern bump the low pavilion.
TOWER = tk.rect(31.7, 60.9, -5.15, 0.0)
PAVILION = [(10.7, -22.4), (20.9, -22.4), (20.9, 13.3), (10.7, 13.3)]
CORNER = 2.6


def build():
    plan = tk.xform(TOWER, YAW)
    tk.prism("lobby", tk.offset_poly(plan, -2.0), 0.0, H_LOBBY, "glassd")
    tk.glow_ring("lobby_lit", tk.offset_poly(plan, -2.0), 0.8, H_LOBBY - 1.5, 0.06, "sand_Glow")
    tk.prism("transfer", plan, H_LOBBY, H_LOBBY + 1.0, "concrete")
    # dark glass behind the fin comb, solid corner piers, white cap
    tk.prism("shaft", tk.offset_poly(plan, -0.6), H_LOBBY + 1.0, H_FINS, "glassd")
    for k, (sx, sy) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1))):
        cx, cy = tk.rot2((-5.15 + sx * (31.7 / 2 - CORNER / 2), sy * (60.9 / 2 - CORNER / 2)), YAW)
        tk.box(f"corner{k}", cx, cy, 0.0, H_FINS, CORNER, CORNER, "white", yaw=YAW, bottom=False)
    # the fin comb on every face (the end fins disappear into the corner piers)
    tk.pier_grid("fins", tk.offset_poly(plan, -0.6), H_LOBBY + 1.0, H_FINS, 1.5, 0.4, 0.6, "concrete",
                 skip_short=3.0, corners=False)
    tk.prism("cap", plan, H_FINS, H_TOP - 1.0, "white", bev=0.2)
    tk.ring_band("parapet", tk.offset_poly(plan, -0.5), H_TOP - 1.0, H_TOP, 0.5, "white")
    tk.prism("roof_deck", tk.offset_poly(plan, -0.5), H_TOP - 1.3, H_TOP - 0.9, "roofd")
    tk.hvac_cluster("plant", *tk.rot2((-5.15, 0.0), YAW), H_TOP - 0.9, YAW, 18.0, 36.0, seed=3.0, hmax=0.85,
                    fans=False)
    bands = tk.floors(H_LOBBY + 1.0, H_FINS, 7.3889)      # 18 two-storey groups
    tk.lit_windows("shaft_win", tk.offset_poly(plan, -0.6), bands, 3.0, 0.3, seed=6.0, out=0.7, margin=0.8,
                   gap=0.5)
    tk.glow_ring("crown_light", plan, H_FINS + 1.5, H_FINS + 2.3, 0.3, "white_Glow")
    # low pavilion and the plaza
    pav = tk.ccw(tk.xform(PAVILION, YAW))
    tk.prism("pavilion", pav, 0.0, H_PAVILION, "concrete", bev=0.15)
    tk.panes("pavilion", pav, [(0.6, H_PAVILION - 1.6)], 4.0, mat="glassd", out=0.06, margin=0.0, gap=0.8)
    tk.lit_windows("pavilion_win", pav, [(0.6, H_PAVILION - 1.6)], 4.0, 0.7, seed=1.0, out=0.12, margin=0.3,
                   gap=1.0)
    tk.prism("pavilion_roof", tk.offset_poly(pav, -0.4), H_PAVILION, H_PAVILION + 0.4, "roofd")
    tk.plinth("plaza", tk.xform(tk.rect(41.9, 60.9, 0.0, 0.0), YAW), h=0.3, out=2.5)
    p0, p1 = tk.xform([(-24.0, -26.0), (-24.0, 26.0)], YAW)
    tk.tree_row("trees", p0, p1, 0.3, 4, h=6.0, seed=2.4)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
