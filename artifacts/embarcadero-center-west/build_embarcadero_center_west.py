"""Deterministic Blender build of the SF-SIM miniature Embarcadero Center West (275 Battery Street).

    blender -b --python build_embarcadero_center_west.py -- [--out DIR]

275 Battery Street (John Portman & Associates, 1989; formerly Embarcadero West): a
30-storey near-square office tower of grey-green precast piers and dark glass whose
corners are notched in steps, so every corner reads as a serrated column; at the top
the notches deepen in two more steps into a stepped crown. A rose granite base.
Recognition cues: the dark ribbed shaft and the stepped, notched corners.
Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "embarcadero-center-west"
CENTER = (-122.4004675, 37.7938599)  # OSM way 32947500, OBB centre
H_TOP = 123.1                         # published roof (Wikipedia 123.1 m); LiDAR majority 120.1, max 126.9
H_BASE = 9.0
H_SHAFT = 107.0                       # first crown step (inferred from photos)
L, W = 40.6, 36.0                     # OSM OBB 41.2 x 36.4
YAW = math.radians(90 - 80.8)         # local +x along Battery-Clay grid (bearing 80.8)
N = 3.0                               # corner notch


def P(n, w=L, d=W):
    return tk.xform(tk.notch_rect(w, d, n), YAW)


def build():
    plan = P(N)
    # rose granite base with dark storefront glass
    tk.prism("base", plan, 0.0, H_BASE, "granite", bev=0.15)
    tk.panes("base_glass", plan, [(0.3, H_BASE - 2.0)], 4.0, mat="glassd", gap=0.8, margin=0.0)
    tk.lit_windows("base_lit", plan, [(0.3, H_BASE - 2.6)], 4.0, 0.8, seed=1.0, out=0.1, margin=0.3, gap=1.2)
    # shaft: dark glass, grey-green precast spandrels and deep piers; 13 two-storey groups
    # (a lean loft) with the lit panes still cut per storey
    pitch = (H_SHAFT - H_BASE) / 13
    tk.shaft("shaft", plan, H_BASE, H_SHAFT, pitch, glass="glassd", band="steel", band_h=1.3, band_out=0.25,
             fins=(4.0, 0.7, 0.45, "steel"), lit=0.0)
    tk.lit_windows("shaft_win", tk.offset_poly(plan, -0.2), [b for z0, z1 in tk.floors(H_BASE, H_SHAFT, pitch)
                                                          for b in ((z0 + 1.3, (z0 + z1 + 1.3) / 2),
                                                                    ((z0 + z1 + 1.3) / 2, z1))],
                   4.0, 0.27, seed=6.0, out=0.55, margin=0.4, gap=0.9)
    # stepped crown: the corner notches deepen twice
    z = H_SHAFT
    for k, (n, h) in enumerate(((6.0, 8.0), (9.0, 6.4))):
        p = P(n)
        tk.shaft(f"crown_{k}", p, z, z + h, h, glass="glassd", band="steel", band_h=1.3, band_out=0.25,
                 fins=(4.0, 0.7, 0.45, "steel"), lit=0.0)
        tk.prism(f"crown_{k}_ledge", tk.offset_poly(P(n - 3.0), 0.2), z - 0.3, z + 0.05, "steel")
        z += h
    top = P(9.0)
    tk.ring_band("parapet", tk.offset_poly(top, -0.5), z, H_TOP, 0.75, "steel")
    tk.prism("roof_deck", tk.offset_poly(top, -0.4), z - 0.3, z + 0.05, "roofd")
    tk.hvac_cluster("roof_plant", 0.0, 0.0, z, YAW, 16.0, 13.0, seed=2.0, hmax=H_TOP - z - 0.2)
    tk.glow_ring("crown_light", top, z - 1.1, z - 0.4, 0.75, "white_Glow")
    tk.plinth("sidewalk", plan, h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
