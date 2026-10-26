"""Deterministic Blender build of the SF-SIM miniature 77 Beale Street (PG&E Building).

    blender -b --python build_77_beale.py -- [--out DIR]

77 Beale (Hertzka & Knowles, 1971), PG&E's headquarters tower: a 34-storey
slab of grey granite, finely ribbed by deep vertical piers between punched
windows, with blank notched corners and a crenellated crown where the piers
rise past the roof. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "77-beale"
CENTER = (-122.395754, 37.791782)   # OSM way 260291405, OBB centre
H_TOP = 150.0                        # 149.96 m published height
H_ROOF = 145.0                       # DataSF LiDAR majority roof plane 144.7 m
H_BASE = 10.0
L, W = 56.0, 41.0                   # OSM OBB 58.4 x 42.4
YAW = math.radians(45.0)


def plan(off=0.0):
    return tk.xform(tk.offset_poly(tk.notch_rect(L, W, 3.0), off), YAW)


def build():
    p = plan()
    tk.prism("base_glass", plan(-2.0), 0.0, H_BASE, "glassd")
    tk.glow_ring("base_lit", plan(-2.0), 0.8, H_BASE - 1.5, 0.06, "sand_Glow")
    tk.pier_grid("base_piers", plan(-0.3), 0.0, H_BASE, 5.5, 1.5, 1.5, "concrete", skip_short=3.5)
    tk.ring_band("base_head", p, H_BASE - 1.4, H_BASE, 0.2, "concrete")
    tk.punched_block("shaft", p, H_BASE, H_ROOF, 3.95, wall="concrete", win="glassd", spacing=2.9,
                     gap=1.6, margin=1.0, lit=0.3, seed=2.2, bev=0.2)
    # deep vertical ribs: the piers stand proud and run on past the roof
    tk.pier_grid("ribs", tk.offset_poly(p, 0.0), H_BASE, H_ROOF, 2.9, 0.7, 0.55, "concrete",
                 skip_short=3.5, corners=False)
    # crenellated crown: a solid screen wall above the roof, slotted between the piers
    tk.ring_band("crown", tk.offset_poly(p, -1.2), H_ROOF, H_TOP, 1.75, "concrete")
    tk.panes("crown_slots", tk.offset_poly(p, 0.55), [(H_ROOF + 0.6, H_TOP - 0.4)], 2.9, mat="ink",
             gap=2.0, margin=0.0)
    tk.prism("roof", tk.offset_poly(p, -1.0), H_ROOF - 0.2, H_ROOF + 0.2, "roofd")
    tk.hvac_cluster("plant", 0, 0, H_ROOF + 0.2, YAW, L * 0.45, W * 0.4, seed=4.0, hmax=H_TOP - H_ROOF - 0.5)
    tk.plinth("plaza", p, h=0.3, out=3.5)
    p0, p1 = tk.xform([(-L / 2 + 4, -W / 2 - 2.5), (L / 2 - 4, -W / 2 - 2.5)], YAW)
    tk.tree_row("trees", p0, p1, 0.3, 4, h=6.0, seed=2.9)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
