"""Deterministic Blender build of the SF-SIM miniature 123 Mission Street.

    blender -b --python build_123_mission.py -- [--out DIR]

123 Mission (SOM, 1986): a 29-storey tower of warm cream stone with a dense
grid of deep punched windows, notched corners, and a set-back crown storey.
Recognition cue: the pale, solid, finely gridded prism among glass towers.
Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "123-mission"
CENTER = (-122.394447, 37.791824)   # OSM way 192026933, OBB centre
H_TOP = 124.0                        # roof (DataSF LiDAR crest 127.2 incl. plant)
H_BASE = 10.0
H_SHAFT = 114.0
L, W = 40.5, 33.5                   # OSM OBB 41.6 x 34.2
YAW = math.radians(90 - 134.5)


def plan(inset=0.0, notch=3.2):
    return tk.xform(tk.notch_rect(L - 2 * inset, W - 2 * inset, notch), YAW)


def build():
    p = plan()
    tk.prism("base", plan(1.6), 0.0, H_BASE, "glassd")
    tk.glow_ring("base_lit", plan(1.6), 0.8, H_BASE - 1.5, 0.06, "sand_Glow")
    tk.pier_grid("base_piers", tk.offset_poly(p, -0.3), 0.0, H_BASE, 4.5, 1.6, 1.4, "stone", skip_short=3.0)
    tk.ring_band("base_head", p, H_BASE - 1.4, H_BASE, 0.2, "stone")
    tk.punched_block("shaft", p, H_BASE, H_SHAFT, 3.95, wall="sand", win="glassd", spacing=2.6, gap=1.1,
                     margin=0.9, lit=0.3, seed=3.3, bev=0.2)
    tk.cornice("cornice", p, H_SHAFT, h=0.9, out=0.4, mat="stone")
    top = plan(3.0, 2.4)
    tk.punched_block("crown", top, H_SHAFT + 0.9, H_TOP - 4.0, 3.9, wall="sand", win="glassd",
                     spacing=2.6, gap=1.1, margin=0.9, lit=0.4, seed=4.4)
    tk.prism("roof", tk.offset_poly(p, -0.5), H_SHAFT + 0.7, H_SHAFT + 0.95, "roofd")
    tk.ring_band("crown_parapet", tk.offset_poly(top, -0.4), H_TOP - 4.0, H_TOP - 2.8, 0.4, "stone")
    tk.hvac_cluster("plant", 0, 0, H_TOP - 4.0, YAW, (L - 6) * 0.6, (W - 6) * 0.5, seed=1.0, hmax=4.0)
    tk.plinth("plaza", p, h=0.3, out=3.0)
    p0, p1 = tk.xform([(-L / 2 + 4, W / 2 + 2.2), (L / 2 - 4, W / 2 + 2.2)], YAW)
    tk.tree_row("trees", p0, p1, 0.3, 3, h=6.0, seed=6.6)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
