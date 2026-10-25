"""Deterministic Blender build of the SF-SIM miniature 333 Market Street.

    blender -b --python build_333_market.py -- [--out DIR]

333 Market (Gin Wong Associates, 1979): a 33-storey tower whose long faces
have serrated corners - a stair of small steps (OSM traces them), clad in
tall pale-bronze piers with dark glass between - a column of fine vertical
pinstripes. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "333-market"
CENTER = (-122.397403, 37.791938)   # OSM way 288505729, OBB centre
H_TOP = 144.0                        # roof (DataSF LiDAR crest 146.1)
H_BASE = 9.0
YAW = math.radians(45.3 - 90 + 90)  # long axis bearing 45.3


def sawtooth(L=46.0, W=37.0, k=3, n=2.6):
    """A rectangle whose four corners are cut into a stair of k re-entrant
    steps of size n (the serrated corners OSM traces on the real tower)."""
    hw, hd = L / 2, W / 2
    ne = []
    for i in range(k):
        ne += [(hw - n * (k - i), hd - n * i), (hw - n * (k - i - 1), hd - n * i)]
    ne.append((hw, hd - n * k))
    # ne runs from the top edge to the right edge; mirror into a closed ring
    se = [(x, -y) for x, y in ne]                 # bottom edge -> right edge
    nw = [(-x, y) for x, y in ne]                 # top edge -> left edge
    sw = [(-x, -y) for x, y in reversed(ne)]      # left edge -> bottom edge
    return tk.ccw(se + list(reversed(ne)) + nw + sw)


def build():
    p = tk.xform(sawtooth(), YAW)
    tk.prism("base_glass", tk.offset_poly(p, -2.0), 0.0, H_BASE, "glassd")
    tk.glow_ring("base_lit", tk.offset_poly(p, -2.0), 0.8, H_BASE - 1.2, 0.06, "sand_Glow")
    tk.pier_grid("base_cols", tk.offset_poly(p, -0.4), 0.0, H_BASE, 5.0, 1.2, 1.2, "granite", skip_short=4.5)
    tk.shaft("shaft", p, H_BASE, H_TOP - 2.0, 4.2, glass="glassd", band="bronze", band_h=0.5,
             band_out=0.15, fins=(1.9, 0.75, 0.5, "terracotta"), lit=0.3, seed=7.1, lit_spacing=1.9)
    tk.prism("cap", tk.offset_poly(p, 0.5), H_TOP - 2.0, H_TOP - 0.8, "terracotta", bev=0.2)
    tk.roof_kit("roof", tk.offset_poly(p, -0.2), H_TOP - 0.8, seed=5.0, parapet=0.8, plant_frac=0.45,
                yaw=YAW)
    tk.plinth("plaza", p, h=0.3, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
