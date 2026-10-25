"""Deterministic Blender build of the SF-SIM miniature 555 Market Street (Market Center).

    blender -b --python build_555_market_street.py -- [--out DIR]

555 Market Street (Hertzka & Knowles, 1964; Standard Oil Building No. 3, later the
Chevron Towers): the shorter of the two Market Center towers, a 22-storey slab clad
in white precast panels that form tight, deep vertical ribs over dark glass, on a
granite base, next to a landscaped plaza shared with 575 Market. Recognition cues:
the crisp white vertical pinstripe and the plain flat top. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "555-market-street"
CENTER = (-122.3999256, 37.7900032)  # OSM way 32946577, OBB centre
H_TOP = 94.8                          # published roof 94.79 m (Wikipedia); LiDAR majority 96.4, max 96.8
H_BASE = 7.0
H_SHAFT = 91.0
L, W = 42.6, 26.4                     # OSM OBB 42.8 x 26.5
YAW = math.radians(90 - 45.1)         # local +x along Market (bearing 45.1); +y = NW face


def build():
    plan = tk.xform(tk.rect(L, W), YAW)
    # granite base: a recessed glass lobby behind a granite frame
    lobby = tk.offset_poly(plan, -1.5)
    tk.prism("lobby", lobby, 0.0, H_BASE, "glassd")
    tk.glow_ring("lobby_lit", lobby, 0.6, H_BASE - 1.4, 0.06, "sand_Glow")
    tk.pier_grid("base_piers", tk.offset_poly(plan, -0.8), 0.0, H_BASE, 5.3, 0.9, 0.8, "granite")
    tk.prism("base_fascia", plan, H_BASE - 0.01, H_BASE + 1.0, "granite", bev=0.12)
    # shaft: white precast ribs over dark glass; 21 storeys of 3.9 m
    tk.shaft("shaft", plan, H_BASE + 1.0, H_SHAFT, (H_SHAFT - H_BASE - 1.0) / 21, glass="glassd", band="white",
             band_h=1.1, band_out=0.15, fins=(1.6, 0.45, 0.45, "white"), lit=0.28, seed=7.0, lit_spacing=1.6)
    # top: a plain white attic band round the roof, plant behind it
    tk.ring_band("attic", tk.offset_poly(plan, -0.2), H_SHAFT, H_TOP, 0.45, "white")
    tk.prism("roof_deck", tk.offset_poly(plan, -0.3), H_SHAFT - 0.3, H_SHAFT + 0.05, "roofd")
    tk.prism("penthouse", tk.xform(tk.rect(18.0, 11.0, 2.0, 0.0), YAW), H_SHAFT, H_TOP - 0.8, "white", bev=0.15)
    tk.hvac_cluster("roof_plant", *tk.rot2((-13.0, 0.0), YAW), H_SHAFT, YAW, 10.0, 14.0, seed=3.0, hmax=2.6)
    tk.glow_ring("crown_light", plan, H_TOP - 2.4, H_TOP - 1.6, 0.5, "white_Glow")
    # the Market Center plaza shared with 575 Market lies to the SW (local -x): a strip
    # of it with a few trees
    tk.plinth("plaza", plan, h=0.3, out=3.0, mat="granite")
    p0, p1 = tk.xform([(-L / 2 - 6.5, -W / 2 + 3), (-L / 2 - 6.5, W / 2 - 3)], YAW)
    tk.prism("plaza_sw", tk.xform(tk.rect(10.0, W + 6.0, -L / 2 - 5.0, 0.0), YAW), 0.0, 0.25, "stone")
    tk.tree_row("plaza_trees", p0, p1, 0.25, 4, h=6.0, seed=2.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
