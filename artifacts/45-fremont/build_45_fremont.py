"""Deterministic Blender build of the SF-SIM miniature 45 Fremont Street.

    blender -b --python build_45_fremont.py -- [--out DIR]

45 Fremont (SOM, 1978): a 34-storey cream precast tower wrapped in
continuous horizontal ribbon windows, with chamfered corners and a flat top.
Recognition cue: the strong cream/dark horizontal striping. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "45-fremont"
CENTER = (-122.397149, 37.791231)   # OSM way 32946535, OBB centre
H_TOP = 145.0                        # roof, 476 ft (DataSF LiDAR crest 146.0)
H_BASE = 8.0
L, W = 45.5, 36.5                   # OSM OBB 46.8 x 37.5
YAW = math.radians(90 - 134.4)


def plan(off=0.0):
    return tk.xform(tk.offset_poly(tk.chamfer_rect(L, W, 4.5), off), YAW)


def build():
    p = plan()
    tk.prism("base_glass", plan(-2.5), 0.0, H_BASE, "glass")
    tk.glow_ring("base_lit", plan(-2.5), 0.8, H_BASE - 1.2, 0.06, "sand_Glow")
    tk.pier_grid("base_cols", plan(-0.5), 0.0, H_BASE, 7.0, 1.4, 1.4, "cream", skip_short=5.0)
    # ribbon windows: cream spandrels proud of a dark glass core, one per floor
    tk.shaft("shaft", p, H_BASE, H_TOP - 3.0, 4.0, glass="glassd", band="cream", band_h=2.3,
             band_out=0.45, fins=None, lit=0.3, seed=2.4, lit_spacing=3.2)
    tk.prism("roof_band", tk.offset_poly(p, 0.45), H_TOP - 3.0, H_TOP - 0.6, "cream", bev=0.2)
    tk.roof_kit("roof", tk.offset_poly(p, -0.2), H_TOP - 0.6, seed=8.0, parapet=0.6, plant_frac=0.45,
                yaw=YAW)
    tk.plinth("plaza", p, h=0.3, out=3.0)
    p0, p1 = tk.xform([(-L / 2 + 4, -W / 2 - 2.2), (L / 2 - 4, -W / 2 - 2.2)], YAW)
    tk.tree_row("trees", p0, p1, 0.3, 3, h=6.0, seed=5.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
