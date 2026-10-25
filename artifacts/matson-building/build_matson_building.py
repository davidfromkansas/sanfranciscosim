"""Deterministic Blender build of the SF-SIM miniature Matson Building.

    blender -b --python build_matson_building.py -- [--out DIR]

215 Market Street (Bliss & Faville, 1922-24; annex 1945-47): the Matson
Navigation Company's sixteen-storey Renaissance Revival headquarters, all
cream terracotta - an ornate arcaded base with a tall central entrance arch,
a plainer shaft, and an ornate top storey of arched windows under a deep
bracketed cornice and roof balustrade: "a column". Twin of the PG&E General
Office Building next door. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "matson-building"
CENTER = (-122.396508, 37.792655)   # OSM way 1279504249, OBB centre
H_TOP = 73.0                         # ESTIMATED: 16 storeys + cornice; see REFERENCE.md
H_BASE = 11.0
H_SHAFT = 62.0
L, W = 43.5, 41.5                   # OSM OBB 44.7 x 42.5
YAW = math.radians(90 - 135.4)


def build():
    base = tk.xform(tk.rect(L, W), YAW)
    tk.prism("base", base, 0.0, H_BASE, "terracotta", bev=0.2)
    tk.arched_panes("arcade", base, 0.6, H_BASE - 1.8, 4.6, 3.0, mat="glassd")
    tk.lit_windows("arcade_lit", base, [(0.6, H_BASE - 3.6)], 4.6, 0.85, seed=5.0, out=0.1, margin=0.4, gap=2.0)
    # the grand entrance arch on Market: the NW face, local -X (local +X is bearing 135.4)
    c = tk.rot2((-L / 2 - 0.5, 0.0), YAW)
    tk.box("portal", c[0], c[1], 0.0, H_BASE + 1.5, 1.2, 9.0, "cream", yaw=YAW, bev=0.2)
    x = -L / 2 - 1.15
    tri = tk.xform([(x, 3.1), (x, -3.1), (x + 6.0, 0.0)], YAW)
    tk.arched_panes("portal_arch", tri, 0.3, H_BASE + 0.6, 7.0, 6.2, mat="glassd", out=0.0,
                    edge_filter=lambda ei, *_: ei == 0)
    tk.arched_panes("portal_lit", tri, 0.3, H_BASE - 1.0, 7.0, 4.4, mat="sand_Glow", out=0.05,
                    edge_filter=lambda ei, *_: ei == 0, suffix="_glow")
    tk.cornice("base_cornice", base, H_BASE, h=1.0, out=0.6, mat="cream")
    tk.punched_block("shaft", base, H_BASE + 1.0, H_SHAFT, 3.85, wall="cream", win="glassd", spacing=2.8,
                     gap=1.2, margin=0.9, lit=0.32, seed=6.0, bev=0.15)
    # ornate top: band course, arched top storey, deep cornice, balustrade
    tk.ring_band("band", base, H_SHAFT - 0.6, H_SHAFT + 0.4, 0.4, "terracotta")
    tk.prism("top", base, H_SHAFT + 0.4, 68.0, "terracotta", bev=0.15)
    tk.arched_panes("top_arches", base, H_SHAFT + 1.0, 67.2, 2.8, 1.9, mat="glassd")
    tk.arched_panes("top_lit", base, H_SHAFT + 1.3, 66.5, 2.8, 1.4, mat="sand_Glow", out=0.1, suffix="_glow")
    tk.cornice("cornice", base, 68.0, h=2.0, out=1.6, mat="cream")
    tk.ring_band("balustrade", tk.offset_poly(base, 0.6), 70.0, 71.4, 0.5, "terracotta")
    tk.prism("roof", tk.offset_poly(base, 0.5), 69.8, 70.2, "roofd")
    # rooftop penthouse: the small arcaded loggia block seen over the Market
    # cornice in the Commons photo (position on the roof inferred)
    ph = tk.xform(tk.rect(10.0, 18.0, -5.0, 0.0), YAW)
    tk.prism("penthouse", ph, 70.2, 72.4, "cream", bev=0.12)
    tk.arched_panes("penthouse_arches", ph, 70.5, 72.1, 2.6, 1.6, mat="glassd")
    tk.arched_panes("penthouse_lit", ph, 70.7, 71.8, 2.6, 1.1, mat="sand_Glow", out=0.1, suffix="_glow")
    tk.cornice("penthouse_cornice", ph, 72.4, h=0.6, out=0.5, mat="terracotta")
    pc = tk.rot2((9.0, 0.0), YAW)
    tk.hvac_cluster("plant", pc[0], pc[1], 70.2, YAW, L * 0.25, W * 0.4, seed=8.0, hmax=1.8)
    tk.plinth("plaza", base, h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
