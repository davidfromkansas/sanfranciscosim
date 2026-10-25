"""Deterministic Blender build of the SF-SIM miniature Stevenson Place (71 Stevenson).

    blender -b --python build_stevenson_place.py -- [--out DIR]

71 Stevenson Street (1986): a postmodern office tower between Market and Mission.
A five-storey dark rose-granite base under a shaft of cream piers framing rose
granite spandrels and dark windows; the corners step back near the top and the
centre rises into a gabled, hipped crown with a louvred plant opening. Helpers
in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "stevenson-place"
CENTER = (-122.3997359, 37.7893242)   # OSM way 149840694, OBB centre
H_TOP = 103.0                          # 103 m (published, Wikipedia; OSM height); LiDAR 105.97
H_BASE = 19.0                          # five-storey granite base
H_SHAFT = 87.4                         # shaft parapet; corners step back above (inferred)
H_UPPER = 95.0
YAW = math.radians(90 - 134.5)         # local +x = bearing 134.5 (SE), +y = 44.5 (NE)

# OSM footprint in the local frame (stepped cut at the south corner)
LOCAL = [(-21.9, -20.6), (2.4, -20.6), (2.5, -15.4), (11.4, -15.4), (11.4, -8.9), (21.7, -8.9),
         (21.9, 20.6), (-21.6, 20.6), (-21.9, -8.9)]
TOWER = tk.notch_rect(38.0, 28.0, 3.5, 0.0, 5.6)
UPPER = tk.notch_rect(30.0, 24.0, 4.0, 0.0, 5.6)


def build():
    plan = tk.xform(LOCAL, YAW)
    tower = tk.xform(TOWER, YAW)
    upper = tk.xform(UPPER, YAW)
    # base: rose granite, banded with cream, punched windows, lit lobby
    tk.punched_block("base", plan, 0.0, H_BASE, 3.8, wall="granite", win="glassd", spacing=3.6, gap=1.4,
                     margin=0.8, lit=0.45, seed=1.0)
    tk.spandrels("base_bands", plan, [3.6, 7.4, 11.2, 15.0], 0.5, 0.1, "cream")
    tk.prism("base_roof", tk.offset_poly(plan, -0.2), H_BASE - 0.2, H_BASE + 0.1, "roofd")
    # shaft: rose granite body, dark windows, proud cream piers
    tk.prism("shaft", tower, H_BASE, H_SHAFT, "granite", bev=0.1)
    bands = tk.floors(H_BASE, H_SHAFT, 3.9)
    tk.panes("shaft_win", tower, bands, 3.4, mat="glassd", gap=1.3, margin=0.9)
    tk.pier_grid("shaft_piers", tower, H_BASE, H_SHAFT, 3.4, 1.1, 0.35, "cream", skip_short=3.0)
    tk.lit_windows("shaft_lit", tower, bands, 3.4, 0.3, seed=3.0, out=0.12, margin=0.9, gap=1.3)
    tk.ring_band("shaft_cap", tower, H_SHAFT - 0.6, H_SHAFT + 0.2, 0.4, "cream")
    tk.prism("shaft_roof", tk.offset_poly(tower, -0.2), H_SHAFT, H_SHAFT + 0.2, "roofd")
    # stepped upper storeys
    tk.punched_block("upper", upper, H_SHAFT, H_UPPER, 4.0, wall="cream", win="glassd", spacing=3.4,
                     gap=1.3, margin=0.9, lit=0.35, seed=4.0)
    tk.ring_band("upper_cap", upper, H_UPPER - 0.5, H_UPPER + 0.2, 0.4, "cream")
    # gabled hip crown with the dark louvred opening on the long faces
    ridge = tk.xform(tk.rect(2.0, 14.0, 0.0, 5.6), YAW)
    base = tk.xform(tk.rect(18.0, 24.0, 0.0, 5.6), YAW)
    tk.prism("crown_wall", base, H_UPPER, H_UPPER + 3.0, "cream")
    tk.frustum("crown", base, H_UPPER + 3.0, ridge, H_TOP, "cream")
    nx, ny = tk.rot2((1, 0), YAW)
    for s, (x0, x1) in ((1, (9.0, 9.0)), (-1, (-9.0, -9.0))):
        a, b = tk.xform([(x0, 5.6 - 3.0 * s), (x1, 5.6 + 3.0 * s)], YAW)
        tk.flat_quad(f"louvre_{s}", a, b, H_UPPER + 1.1, H_UPPER + 2.8, 0.06, "ink", (nx * s, ny * s))
    tk.glow_ring("crown_light", tk.xform(tk.rect(18.0, 24.0, 0.0, 5.6), YAW), H_UPPER + 0.2, H_UPPER + 0.9,
                 0.1, "white_Glow")
    tk.hvac_cluster("plant", *tk.rot2((0.0, -12.5), YAW), H_BASE + 0.1, YAW, 14.0, 6.0, seed=2.0, hmax=2.5)
    tk.plinth("plaza", plan, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
