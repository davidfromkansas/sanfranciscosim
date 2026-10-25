"""Deterministic Blender build of the SF-SIM miniature One Montgomery Tower.

    blender -b --python build_120_kearny_street.py -- [--out DIR]

One Montgomery Tower, 120 Kearny Street (SOM, 1982; formerly Pacific Telesis
Tower): a 38-storey Art Deco Revival office tower at Post and Kearny, part of
the Crocker Galleria complex. Its steel frame is clad in rose-red granite with a
dense grid of square windows (grouped in blocks of four by small squares at
their intersections); the first two floors are black granite. The plan is a
rectangle with clipped corners. Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "120-kearny-street"
CENTER = (-122.4033381, 37.7891918)   # OSM way 148716020, OBB centre
H_TOP = 152.4                          # published roof (500 ft); LiDAR 155.95
H_BASE = 9.0                           # two black-granite storeys (published)
H_SHAFT = 146.0                        # INFERRED: top of the window grid under a solid granite cap
YAW = tk.bearing_to_yaw(80.1)          # local +x = bearing 80.1 (along Post St), +y = 350.1 (along Kearny St)

# Local plan (x ~ east along Post, y ~ north along Kearny) from the 9-node OSM
# outline: a 54.9 x 38 rectangle with ~2.8 m clipped corners.
LOCAL = tk.chamfer_rect(54.9, 38.0, 2.8)


def build():
    plan = tk.xform(LOCAL, YAW)
    # black granite base, lit shop/lobby glass
    tk.prism("base", plan, 0.0, H_BASE, "ink", bev=0.15)
    tk.panes("base", plan, [(0.4, H_BASE - 1.2)], 4.5, mat="glassd", out=0.06, margin=0.0, gap=1.0)
    tk.lit_windows("base_win", plan, [(0.4, H_BASE - 1.2)], 4.5, 0.85, seed=2.0, out=0.12, margin=0.4, gap=1.4)
    # rose-red granite shaft: one square window per bay per storey
    tk.prism("shaft", plan, H_BASE, H_TOP - 1.6, "granite", bev=0.25)
    rows = tk.floors(H_BASE, H_SHAFT, 3.8056)          # 36 storeys
    tk.panes("shaft", plan, [(z0 + 0.7, z1 - 0.7) for z0, z1 in rows], 3.75, mat="glassd", out=0.07,
             margin=0.0, gap=1.35)
    pairs = tk.floors(H_BASE, H_SHAFT, 7.6111)         # night: lit pairs of windows, 2 storeys at a time
    tk.lit_windows("shaft_win", plan, pairs, 7.5, 0.3, seed=9.0, out=0.13, margin=0.9, gap=1.6)
    # solid granite cap with a stepped top and parapet
    tk.ring_band("cap_band", plan, H_SHAFT + 1.0, H_SHAFT + 1.8, 0.35, "granite")
    tk.prism("roof_deck", tk.offset_poly(plan, -0.5), H_TOP - 2.0, H_TOP - 1.5, "roofd")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.5), H_TOP - 1.6, H_TOP, 0.5, "granite")
    step = tk.xform(tk.chamfer_rect(30.0, 20.0, 2.0), YAW)
    tk.prism("penthouse", step, H_TOP - 1.6, H_TOP - 0.2, "granite", bev=0.15)
    c = tk.rot2((-18.0, 0.0), YAW)
    tk.hvac_cluster("plant", c[0], c[1], H_TOP - 1.6, YAW, 10.0, 22.0, seed=4.0, hmax=1.5, fans=False)
    tk.glow_ring("crown_light", plan, H_SHAFT + 2.4, H_SHAFT + 3.2, 0.3, "white_Glow")
    tk.plinth("plaza", plan, h=0.3, out=3.0)
    p0, p1 = tk.xform([(-24.0, -22.0), (24.0, -22.0)], YAW)
    tk.tree_row("trees", p0, p1, 0.3, 4, h=6.0, seed=8.8)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
