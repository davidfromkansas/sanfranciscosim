"""Deterministic Blender build of the SF-SIM miniature One Front Street.

    blender -b --python build_1_front_street.py -- [--out DIR]

One Front Street (SOM, 1979; formerly Shaklee Terraces / 444 Market): a
38-storey office tower whose white aluminium spandrels run in continuous,
round-nosed horizontal bands between dark ribbon windows, wrapping a plan that
steps down to Market Street in four saw-tooth notches - a deliberate echo of
Fahrenkamp's Shell-Haus in Berlin. Recognition cues: the zebra of white and
dark ribbons and the stepped Market corner. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "1-front-street"
CENTER = (-122.3988329, 37.7917891)   # OSM way 148710877, OBB centre
H_TOP = 164.0                          # published roof (Wikipedia 164 m); LiDAR 158.06 = main roof
H_LOBBY = 8.0
H_ROOF = 158.0                         # LiDAR roof; the white screen rises to 164
YAW = tk.bearing_to_yaw(81.2)          # local +x = bearing 81.2 (street grid), +y = 351.2

# Local plan (x ~ east, y ~ north) simplified from the 29-node OSM outline:
# Front St = west face, the chamfer = Front x Market corner, the four
# saw-tooth steps = the Market St frontage (SE).
LOCAL = [(-21.8, 27.3), (-21.8, -9.9), (-8.6, -27.2), (-2.2, -27.2), (-2.2, -21.9), (3.4, -21.9),
         (3.4, -17.0), (9.4, -17.0), (9.4, -12.4), (15.6, -12.4), (15.6, -7.6), (21.6, -7.6),
         (21.6, 27.3)]


def build():
    plan = tk.ccw(tk.xform(LOCAL, YAW))
    # lobby: recessed dark glass under the white tower, lit at night
    tk.prism("lobby", tk.offset_poly(plan, -1.5), 0.0, H_LOBBY, "glassd")
    tk.glow_ring("lobby_lit", tk.offset_poly(plan, -1.5), 0.8, H_LOBBY - 1.5, 0.06, "sand_Glow")
    tk.pier_grid("lobby_piers", tk.offset_poly(plan, -0.9), 0.0, H_LOBBY, 6.0, 0.9, 0.9, "white",
                 skip_short=3.0)
    # tower: white body, one dark ribbon window per storey on every face = the bands
    bands = tk.floors(H_LOBBY, H_ROOF, 4.05)  # 37 storeys, divides exactly
    tk.prism("tower", plan, H_LOBBY, H_ROOF, "white", bev=0.5)
    ribbons = [(z0 + 2.1, z1 - 0.1) for z0, z1 in bands]  # ~half white, half glass
    tk.panes("tower", plan, ribbons, 6.5, mat="glassd", out=0.08, margin=0.05, gap=0.35)
    tk.lit_windows("tower_win", plan, ribbons, 6.5, 0.3, seed=11.0, out=0.14, margin=0.35, gap=0.6)
    # roof: a white screen ring 158-164 m around a deck and plant
    tk.ring_band("screen", tk.offset_poly(plan, -0.3), H_ROOF, H_TOP, 0.3, "white")
    tk.prism("roof_deck", tk.offset_poly(plan, -0.5), H_ROOF - 0.3, H_ROOF + 0.1, "roofd")
    c = tk.rot2((-2.0, 8.0), YAW)
    tk.hvac_cluster("plant", c[0], c[1], H_ROOF + 0.1, YAW, 24.0, 22.0, seed=3.0, hmax=4.8)
    tk.glow_ring("crown_light", plan, H_TOP - 1.2, H_TOP - 0.4, 0.36, "white_Glow")
    tk.plinth("plaza", plan, h=0.3, out=3.0)
    # street trees on Front St (west)
    p0, p1 = tk.xform([(-26.0, -6.0), (-26.0, 24.0)], YAW)
    tk.tree_row("trees", p0, p1, 0.3, 3, h=6.0, seed=1.7)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
