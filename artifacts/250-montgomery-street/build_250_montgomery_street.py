"""Deterministic Blender build of the SF-SIM miniature 250 Montgomery Street.

    blender -b --python build_250_montgomery_street.py -- [--out DIR]

250 Montgomery Street (formerly Continental Center, 1986): a sixteen-storey
office tower on the east side of Montgomery between Bush and Pine, backing on
Petrarch Place. No photograph was available; the miniature is a mid-1980s
downtown-plan treatment read from the outline and the LiDAR roof: a two-storey
rose-granite base with a lit lobby, a pale stone shaft of paired punched
windows in shallow vertical recesses, a two-storey set-back top under a
cornice and a screened roof. Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "250-montgomery-street"
CENTER = (-122.4022951, 37.7917005)  # OSM way 256066242, OBB centre
H_TOP = 69.88                         # DataSF 2010 LiDAR max of ring 201006.0004020 (roof screen)
H_ROOF = 68.0                         # LiDAR median (main roof)
YAW = tk.bearing_to_yaw(80.8)         # local +x = east, +y = north; Montgomery St = west face
W, D = 22.8, 35.2


def L(poly):
    return tk.xform(poly, YAW)


def build():
    plan = L(tk.rect(W, D))
    tk.prism("base", plan, 0.0, 9.0, "granite", bev=0.15)
    tk.panes("base_win", plan, [(0.0, 9.0)], 3.5, mat="glassd", gap=1.0, margin=0.8)
    tk.lit_windows("base_lit", plan, [(0.0, 5.0)], 3.5, 0.75, seed=1.0, out=0.1, margin=0.6, gap=1.2)
    tk.ring_band("base_cap", plan, 9.0, 9.7, 0.35, "stone")
    # shaft: 12 storeys of 4.24 m
    tk.punched_block("shaft", plan, 9.7, 60.6, 4.2417, wall="stone", win="glassd", spacing=2.9, gap=1.0,
                     margin=0.9, lit=0.3, seed=5.0, bev=0.12)
    tk.pier_grid("piers", plan, 9.7, 60.6, 5.8, 0.7, 0.3, "sand", skip_short=8.0)
    tk.cornice("cornice", plan, 60.6, h=1.0, out=0.6, mat="granite")
    top = tk.offset_poly(plan, -1.5)
    tk.punched_block("top", top, 61.6, H_ROOF, 3.2, wall="stone", win="glassd", spacing=2.9, gap=1.2,
                     margin=0.8, lit=0.4, seed=7.0, bev=0.1)
    tk.prism("roof", tk.offset_poly(top, -0.3), H_ROOF - 0.3, H_ROOF + 0.1, "roofd")
    screen = L(tk.rect(12.0, 16.0, 0.0, 2.0))
    tk.ring_band("screen", screen, H_ROOF + 0.1, H_TOP, 0.3, "granite")
    tk.prism("plant_core", tk.offset_poly(screen, -0.8), H_ROOF + 0.1, H_TOP - 0.6, "steel")
    tk.glow_ring("crown", tk.offset_poly(top, 0.0), H_ROOF - 0.7, H_ROOF - 0.4, 0.06, "white_Glow")
    tk.prism("sidewalk", L(tk.rect(W + 5.0, D + 4.0, -0.5, 0.0)), 0.0, 0.15, "concrete")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
