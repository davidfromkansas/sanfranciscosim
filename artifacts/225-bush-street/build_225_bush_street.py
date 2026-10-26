"""Deterministic Blender build of the SF-SIM miniature 225 Bush Street (Standard Oil Building).

    blender -b --python build_225_bush_street.py -- [--out DIR]

225 Bush Street, the Standard Oil Building (George W. Kelham, 1922; 1950s
wing): a 22-storey pale-stone palazzo filling a long block - a two-storey
arcade of round-headed openings, an ornamented band course, a tall shaft of
evenly punched windows, and a colonnaded loggia under a deep cornice at the
top, modelled on the Federal Reserve Bank of New York. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "225-bush-street"
CENTER = (-122.4013094, 37.7908371)   # OSM way 942665601, OBB centre
H_TOP = 100.0                          # 328 ft (published); LiDAR 98.68
H_ARCADE = 9.5
H_MEZZ = 17.0
H_SHAFT = 88.0
H_LOGGIA = 95.0
H_CORNICE = 97.6
L, W = 83.6, 43.0                      # OSM OBB 83.9 x 43.2
YAW = math.radians(90 - 81.2)          # long faces look N and S


def build():
    plan = tk.xform(tk.rect(L, W), YAW)
    # two-storey arcade
    tk.prism("arcade", plan, 0.0, H_ARCADE, "stone", bev=0.15)
    tk.arched_panes("arches", plan, 0.3, H_ARCADE - 0.6, 6.2, 4.2, mat="glassd")
    tk.arched_panes("arches_lit", plan, 0.4, H_ARCADE - 2.6, 6.2, 3.2, mat="sand_Glow", out=0.1, suffix="_glow")
    # mezzanine and ornamented band course
    tk.punched_block("mezz", plan, H_ARCADE, H_MEZZ, 3.75, wall="stone", win="glassd", spacing=4.2, gap=2.0,
                     margin=0.8, lit=0.3, seed=1.0)
    tk.cornice("band", plan, H_MEZZ - 0.6, h=1.0, out=0.45, mat="cream")
    # shaft: 18 storeys of punched windows
    tk.punched_block("shaft", plan, H_MEZZ + 0.4, H_SHAFT, (H_SHAFT - H_MEZZ - 0.4) / 18, wall="stone",
                     win="glassd", spacing=4.6, gap=2.4, margin=1.0, lit=0.25, seed=2.0)
    # colonnaded loggia: dark recess behind a ring of columns
    tk.prism("loggia", tk.offset_poly(plan, -1.2), H_SHAFT, H_LOGGIA, "glassd")
    tk.glow_ring("loggia_lit", tk.offset_poly(plan, -1.2), H_SHAFT + 1.0, H_LOGGIA - 1.6, 0.05, "sand_Glow")
    tk.pier_grid("columns", tk.offset_poly(plan, -1.2), H_SHAFT, H_LOGGIA, 4.2, 1.0, 1.1, "cream")
    tk.ring_band("loggia_sill", plan, H_SHAFT - 0.4, H_SHAFT + 0.3, 0.3, "cream")
    tk.cornice("cornice", plan, H_LOGGIA, h=H_CORNICE - H_LOGGIA, out=1.6, mat="cream")
    tk.prism("roof", tk.offset_poly(plan, 0.6), H_CORNICE - 0.4, H_CORNICE + 0.05, "roofd")
    tk.ring_band("tile_edge", tk.offset_poly(plan, 0.6), H_CORNICE, H_CORNICE + 0.5, 0.35, "terracotta")
    # plant penthouses on the roof (estimated) reach the crest
    for k, x in enumerate((-22.0, 22.0)):
        p = tk.xform(tk.rect(14.0, 12.0, x, 0.0), YAW)
        tk.prism(f"penthouse_{k}", p, H_CORNICE, H_TOP, "stone", bev=0.12)
    tk.hvac_cluster("plant", 0, 0, H_CORNICE + 0.05, YAW, 18.0, 16.0, seed=4.0, hmax=2.0)
    tk.plinth("sidewalk", plan, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
