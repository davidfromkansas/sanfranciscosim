"""Deterministic Blender build of the SF-SIM miniature 150 California Street.

    blender -b --python build_150_california_street.py -- [--out DIR]

150 California Street (HOK, 2000): a 24-storey office tower at California x
Front. A warm grey granite grid of square punched windows over a five-storey
base of larger windows, an open trellis frame along the roof line, and the one
memorable gesture: a column of stacked, faceted blue glass bays with a ledge
at every other floor that climbs the Front St corner and rises above the roof
as a glass lantern. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "150-california-street"
CENTER = (-122.3985185, 37.7936973)   # OSM way 1279447597, OBB centre
H_TOP = 100.6                          # published roof 100.59 m (Wikipedia / Emporis); glass bay crest
H_ROOF = 97.0                          # LiDAR roof plane (DataSF majority 96.9 m)
H_POD = 22.0                           # five-storey base (photo; estimated)
YAW = tk.bearing_to_yaw(80.4)         # local +x = east along California St, +y = north (toward Sacramento)
# OSM footprint in that local frame (m): a 41 x 29 block with a 13 x 12 wing at the NE
FOOT = [(-20.5, -20.4), (20.6, -20.5), (20.5, 20.4), (7.4, 20.5), (7.4, 8.7), (-20.5, 8.9)]
TOWER = (-20.5, -20.4, 11.5, 2.0)     # x0, y0, x1, y1: the tower over the SW (corner) part, inferred
BAY = 7.0                             # glass bay column at the California x Front corner


def build():
    foot = tk.ccw(tk.xform(FOOT, YAW))
    x0, y0, x1, y1 = TOWER
    tower = tk.xform(tk.rect(x1 - x0, y1 - y0, (x0 + x1) / 2, (y0 + y1) / 2), YAW)
    # five-storey base with large windows
    tk.prism("podium", foot, 0.0, H_POD, "concrete", bev=0.12)
    pod = tk.floors(1.0, H_POD - 0.8, 4.2)
    tk.panes("podium_win", foot, pod, 4.0, mat="glassd", margin=0.7, gap=1.3)
    tk.lit_windows("podium_lit", foot, pod, 4.0, 0.4, seed=1.3, out=0.1, margin=0.8, gap=1.4)
    tk.prism("podium_roof", tk.offset_poly(foot, -0.3), H_POD - 0.2, H_POD + 0.6, "concrete")
    # the tower: granite grid of square punched windows
    floors = tk.floors(H_POD, H_ROOF, 3.95)
    tk.prism("tower", tower, H_POD, H_ROOF, "concrete", bev=0.12)
    tk.panes("tower_win", tower, floors, 3.45, mat="glassd", margin=0.9, gap=1.3)
    tk.lit_windows("tower_lit", tower, floors, 3.45, 0.3, seed=4.2, out=0.1, margin=0.95, gap=1.4)
    # roof-line trellis frame on slim posts over a dark roof deck
    tk.prism("roof_deck", tk.offset_poly(tower, -0.3), H_ROOF - 0.3, H_ROOF + 0.2, "roofd")
    tk.pier_grid("trellis_posts", tk.offset_poly(tower, -0.5), H_ROOF, H_ROOF + 2.4, 5.0, 0.35, 0.35, "concrete")
    tk.ring_band("trellis", tk.offset_poly(tower, -0.4), H_ROOF + 2.4, H_ROOF + 3.0, 1.2, "concrete")
    c = tk.rot2(((x0 + x1) / 2 + 4.0, (y0 + y1) / 2 + 2.0), YAW)
    tk.hvac_cluster("plant", c[0], c[1], H_ROOF + 0.2, YAW, 12.0, 8.0, seed=6.0, hmax=2.2)
    # the glass bay column on the SW corner: chamfered outward corner, ledges every other floor
    bx, by = x0, y0

    def bay(z, off):
        pts = [(bx - 1.6, by + BAY - 1.0), (bx - 1.6, by + 1.2), (bx + 1.2, by - 1.6),
               (bx + BAY - 1.0, by - 1.6), (bx + BAY - 1.0, by + BAY - 1.0)]
        return tk.offset_poly(tk.xform(pts, YAW), off)
    tk.banded_loft("glass_bay", bay, 4.5, H_TOP - 1.4, 7.9, 0.45, 0.45, tk.material("glassl"),
                   tk.material("steel"), glass_in=0.0)
    tk.prism("glass_bay_cap", bay(0, 0.2), H_TOP - 1.4, H_TOP, "steel")
    tk.lit_loop_windows("glass_bay_win", bay, tk.floors(4.5, H_TOP - 1.4, 3.95), 0.45, seed=2.7, out=0.55,
                        margin=0.6, subdiv=1)
    tk.glow_ring("glass_bay_crown", bay(0, 0.0), H_ROOF + 0.6, H_TOP - 1.8, 0.55, "sky_Glow")
    tk.plinth("sidewalk", foot, h=0.25, out=2.5)
    p0, p1 = tk.xform([(x0 + 9.0, y0 - 2.2), (x1 + 6.0, y0 - 2.2)], YAW)
    tk.tree_row("trees", p0, p1, 0.25, 3, h=6.0, seed=8.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
