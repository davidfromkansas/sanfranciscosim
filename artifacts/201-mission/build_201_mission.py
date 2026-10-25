"""Deterministic Blender build of the SF-SIM miniature 201 Mission Street.

    blender -b --python build_201_mission.py -- [--out DIR]

201 Mission (1981), the former Providian Financial / Pacific Gateway
building: a 30-storey tower on an elongated octagonal plan at the Mission end
of an odd trapezoidal mid-block lot that runs through to Howard, over a
four-storey podium filling the lot. The plan shape and the podium come from
OSM building parts (ways 616813259 / 616813260); the banded glass-and-stone
facade is INFERRED (no usable photo in this pass - see REFERENCE.md).
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "201-mission"
CENTER = (-122.3949072, 37.7910519)  # OSM podium way 616813260, OBB centre
H_TOP = 135.9                        # DataSF LiDAR crest 135.89 m (measured)
H_ROOF = 127.2                       # LiDAR majority roof plane (wiki 417 ft = 127 m)
H_POD = 17.0
# tower part, metres east/north of CENTER (OSM way 616813259)
TOWER_C = ((-122.3950436 + 122.3949072) * tk.KX, (37.791213 - 37.7910519) * tk.KY)
TOWER = [(29.6, -4.3), (11.9, 14.0), (-1.0, 18.2), (-17.3, 16.5), (-30.1, 3.9), (-12.6, -12.5),
         (-0.3, -18.1), (18.3, -15.8)]
PODIUM = [(-15.1, 54.5), (-53.6, 17.7), (-43.1, 6.5), (-29.0, 7.1), (-15.1, -6.3), (0.7, -5.5),
          (13.6, -18.3), (24.1, -17.5), (31.7, -25.0), (46.8, -24.3), (53.6, -17.5)]
YAW = math.radians(90 - 44.6)


def build():
    tower = tk.ccw([(x + TOWER_C[0], y + TOWER_C[1]) for x, y in TOWER])
    pod = tk.ccw(PODIUM)
    tk.prism("podium_glass", tk.offset_poly(pod, -1.0), 0.0, H_POD - 1.6, "glassd")
    tk.glow_ring("podium_lit", tk.offset_poly(pod, -1.0), 0.8, H_POD - 2.6, 0.06, "sand_Glow")
    tk.prism("podium_roof", pod, H_POD - 1.6, H_POD, "stone", bev=0.15)
    tk.pier_grid("podium_cols", tk.offset_poly(pod, -0.5), 0.0, H_POD - 1.6, 6.0, 1.0, 1.0, "stone",
                 skip_short=5.0)
    tk.shaft("tower", tower, H_POD, H_ROOF, 4.0, glass="glassd", band="stone", band_h=1.5, band_out=0.35,
             fins=None, lit=0.3, seed=3.9, lit_spacing=3.2)
    tk.roof_kit("roof", tower, H_ROOF, seed=1.2, parapet=1.0, pmat="stone", plant_frac=0.4, yaw=YAW)
    cx = sum(p[0] for p in tower) / len(tower)
    cy = sum(p[1] for p in tower) / len(tower)
    tk.box("penthouse", cx, cy, H_ROOF, H_TOP - 0.6, 16.0, 10.0, "stone", yaw=YAW, bev=0.2)
    tk.pier_grid("louvres", tk.xform(tk.rect(16.0, 10.0), YAW, cx, cy), H_ROOF + 1.0, H_TOP - 1.6,
                 1.8, 0.3, 0.3, "steel", skip_short=3.0)
    tk.prism("pent_cap", tk.xform(tk.rect(16.6, 10.6), YAW, cx, cy), H_TOP - 0.6, H_TOP, "trim")
    # podium roof garden toward Howard
    tk.tree_row("pod_trees", (24.0, -12.0), (44.0, -19.0), H_POD, 3, h=4.5, r=1.8, seed=4.0)
    tk.plinth("plaza", pod, h=0.3, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
