"""Deterministic Blender build of the SF-SIM miniature Federal Reserve Bank of San Francisco.

    blender -b --python build_federal_reserve.py -- [--out DIR]

101 Market Street (SOM, 1983): a long low slab of alternating travertine
spandrels and bronze ribbon glass, lifted over Market Street on a deep
colonnaded arcade whose roof is a terrace lined with planters, with a lower
operations block behind. Recognition cues: the horizontal striping and the
planted arcade along Market. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "federal-reserve"
CENTER = (-122.395520, 37.793002)   # OSM way 32612362, OBB centre
H_TOP = 63.1                         # DataSF LiDAR crest 63.14 m (measured)
H_ARCADE = 9.0
H_SLAB = 60.5                        # LiDAR majority roof plane 60.5 m
YAW = math.radians(45.0)            # local +x along Market (bearing 45), +y = NW
LX = 84.0


def R(w, d, cx=0.0, cy=0.0):
    return tk.xform(tk.rect(w, d, cx, cy), YAW)


def build():
    slab = R(LX, 34.0, 0.0, 14.0)
    back = R(LX - 4, 40.0, 0.0, -21.0)
    # the arcade: piers carrying a planted terrace along Market
    arc = R(LX, 10.0, 0.0, 36.0)
    tk.prism("arcade_roof", arc, H_ARCADE - 1.2, H_ARCADE, "stone", bev=0.2)
    a0, a1 = tk.xform([(-LX / 2 + 1, 40.4), (LX / 2 - 1, 40.4)], YAW)
    for i in range(12):
        t = (i + 0.5) / 12
        x, y = a0[0] + (a1[0] - a0[0]) * t, a0[1] + (a1[1] - a0[1]) * t
        tk.box(f"arcade_pier_{i}", x, y, 0.0, H_ARCADE - 1.2, 1.6, 1.6, "stone", yaw=YAW, bev=0.15)
        if i % 2 == 0:
            tk.box(f"planter_{i}", x, y, H_ARCADE, H_ARCADE + 0.9, 4.0, 2.2, "stone", yaw=YAW, bev=0.15)
            tk.tree(f"terrace_tree_{i}", x, y, H_ARCADE + 0.9, h=3.2, r=1.6, mat="leaf")
    tk.tree_row("market_trees", *tk.xform([(-LX / 2 + 4, 44.0), (LX / 2 - 4, 44.0)], YAW), 0.3, 6,
                h=6.5, r=2.6, seed=3.0)
    # the slab: travertine bands over bronze ribbon glass
    tk.prism("slab_base", tk.offset_poly(slab, -2.0), 0.0, H_ARCADE, "glassd")
    tk.glow_ring("lobby_lit", tk.offset_poly(slab, -2.0), 0.8, H_ARCADE - 1.5, 0.06, "sand_Glow")
    tk.shaft("slab", slab, H_ARCADE, H_SLAB, 4.25, glass="bronze", band="stone", band_h=2.2,
             band_out=0.5, fins=None, lit=0.32, seed=1.7, lit_spacing=3.4)
    tk.roof_kit("slab_roof", slab, H_SLAB, seed=2.0, parapet=0.9, pmat="stone", plant_frac=0.5, yaw=YAW)
    tk.prism("penthouse", R(30, 14, 4.0, 14.0), H_SLAB, H_TOP, "stone", bev=0.2)
    # the lower operations block behind
    tk.shaft("back", back, 0.0, 23.9, 4.6, glass="bronze", band="stone", band_h=2.4, band_out=0.5,
             fins=None, lit=0.22, seed=5.5, lit_spacing=3.4)
    tk.roof_kit("back_roof", back, 23.9, seed=9.0, parapet=0.9, pmat="stone", plant_frac=0.5, yaw=YAW)
    tk.plinth("plaza", R(LX, 92.0, 0.0, 0.0), h=0.3, out=2.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
