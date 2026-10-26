"""Deterministic Blender build of the SF-SIM miniature 199 Fremont Street.

    blender -b --python build_199_fremont_street.py -- [--out DIR]

199 Fremont Street / 300 Howard Street (KMD Architects, 2000): a 27-storey office
tower clad in pale granite with a regular grid of paired blue windows, a full-height
blue glass slot at its street corner, and a top two storeys stepped back behind a
granite parapet. Recognition cues: the light stone grid and the glazed corner slot.
Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "199-fremont-street"
CENTER = (-122.3948627, 37.7899805)  # OSM way 192883913, OBB centre
H_TOP = 110.9                         # published roof (Wikipedia 110.9 m); LiDAR max 111.31 m
H_BASE = 8.0
H_SHAFT = 102.6
YAW = math.radians(90 - 133.9)
# OSM way 192883913 in metres about CENTER (+x east, +y north)
PTS = [(-7.34, 33.06), (-34.38, 5.39), (-16.94, -11.41), (-13.88, -8.21), (6.65, -27.98), (7.93, -26.68),
       (9.54, -28.23), (14.96, -22.68), (16.33, -23.98), (26.39, -13.68), (25.03, -12.37), (30.66, -6.6),
       (29.05, -5.05), (31.47, -2.58), (-0.82, 28.54), (-1.7, 27.63)]


def build():
    plan = tk.ccw(PTS)
    # base: tall storefront glass in the granite
    tk.prism("base", plan, 0.0, H_BASE, "stone", bev=0.15)
    tk.panes("base_glass", plan, [(0.3, H_BASE - 1.2)], 5.0, mat="glass", gap=1.0, margin=0.0)
    tk.lit_windows("base_lit", plan, [(0.3, H_BASE - 1.8)], 5.0, 0.85, seed=2.0, out=0.1, margin=0.3, gap=1.4)
    tk.ring_band("base_band", plan, H_BASE, H_BASE + 0.8, 0.3, "stone")
    # shaft: granite with paired windows; 24 storeys of 3.9 m
    tk.punched_block("shaft", plan, H_BASE + 0.8, H_SHAFT, (H_SHAFT - H_BASE - 0.8) / 24, wall="stone",
                     win="glass", spacing=4.6, gap=1.3, margin=0.8, lit=0.28, seed=5.0, bev=0.12)
    # the glazed corner slot on the west (Fremont) corner: a full-height glass column
    # standing proud of the granite (the photo's cue; corner choice inferred)
    d = tk.rot2((1.3, 1.3), YAW)
    c = (PTS[1][0] + d[0], PTS[1][1] + d[1])
    tk.box("corner_glass", c[0], c[1], H_BASE, H_SHAFT + 0.8, 4.0, 4.0, "glass", yaw=YAW)
    tk.lit_windows("corner_lit", tk.xform(tk.rect(4.0, 4.0), YAW, c[0], c[1]),
                   tk.floors(H_BASE + 0.8, H_SHAFT, (H_SHAFT - H_BASE - 0.8) / 24), 2.0, 0.35, seed=9.0,
                   out=0.08, margin=0.5, gap=0.3)
    # stepped top: two storeys set back, then a granite parapet hiding the plant
    tk.cornice("shaft_cornice", plan, H_SHAFT, h=0.8, out=0.4, mat="stone")
    top = tk.xform(tk.chamfer_rect(49.0, 31.0, 4.0), YAW)
    tk.prism("top_floors", top, H_SHAFT + 0.8, H_TOP - 2.6, "glass")
    tk.pier_grid("top_piers", top, H_SHAFT + 0.8, H_TOP - 2.6, 4.6, 0.9, 0.4, "stone")
    tk.lit_windows("top_lit", top, [(H_SHAFT + 0.8, H_TOP - 2.6)], 4.6, 0.4, seed=12.0, out=0.45, margin=1.0, gap=1.4)
    tk.ring_band("parapet", tk.offset_poly(top, -0.4), H_TOP - 2.6, H_TOP, 0.8, "stone")
    tk.prism("roof_deck", tk.offset_poly(top, -0.4), H_TOP - 2.9, H_TOP - 2.55, "roofd")
    tk.hvac_cluster("roof_plant", 0.0, 0.0, H_TOP - 2.55, YAW, 24.0, 14.0, seed=6.0, hmax=2.3)
    tk.glow_ring("crown_light", top, H_TOP - 1.6, H_TOP - 0.8, 0.45, "white_Glow")
    tk.plinth("sidewalk", plan, h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
