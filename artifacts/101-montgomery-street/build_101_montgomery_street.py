"""Deterministic Blender build of the SF-SIM miniature 101 Montgomery (Schwab Building).

    blender -b --python build_101_montgomery_street.py -- [--out DIR]

101 Montgomery Street (1984): a slender 28-storey slab, 64 x 17 m, running north-south
along Montgomery Street, clad in pale cream stone with rows of curved, bay-like windows
that make the long faces ripple. It stands on a colonnaded ground storey and ends in a
plain, slightly set-back top. Recognition cues: the thin cream blade and its fine
window grid. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "101-montgomery-street"
CENTER = (-122.4024903, 37.7903646)  # OSM way 132125159, OBB centre
H_TOP = 123.1                         # published roof 404 ft (Wikipedia); LiDAR crest 124.67 m
H_LOBBY = 8.0
H_SHAFT = 119.0
# OSM footprint in metres about CENTER (+x east, +y north); long axis bearing 170.9
PTS = [(3.37, 33.02), (11.17, -16.39), (13.41, -30.44), (-3.32, -33.07), (-5.54, -19.19),
       (-8.88, 1.71), (-13.49, 30.43)]
YAW = math.radians(90 - 170.9)


def build():
    plan = tk.ccw(PTS)
    # colonnaded ground storey: dark glass set back behind cream piers
    tk.prism("lobby", tk.offset_poly(plan, -1.5), 0.0, H_LOBBY, "glassd")
    tk.glow_ring("lobby_lit", tk.offset_poly(plan, -1.5), 0.6, H_LOBBY - 1.5, 0.06, "sand_Glow")
    tk.pier_grid("colonnade", tk.offset_poly(plan, -0.9), 0.0, H_LOBBY, 6.4, 1.0, 0.9, "cream")
    tk.prism("lobby_soffit", plan, H_LOBBY - 0.01, H_LOBBY + 1.2, "cream", bev=0.15)
    # shaft: cream stone with deep sills (bands) and fine piers = the window grid; 27 storeys
    tk.shaft("shaft", plan, H_LOBBY + 1.2, H_SHAFT, (H_SHAFT - H_LOBBY - 1.2) / 27, glass="glassd", band="cream",
             band_h=1.9, band_out=0.3, fins=(3.2, 0.9, 0.3, "cream"), lit=0.3, seed=3.0, lit_spacing=3.2)
    # top: a set-back cream crown wall hiding the roof plant, with a light line
    top = tk.offset_poly(plan, -0.8)
    tk.ring_band("crown", tk.offset_poly(top, -0.6), H_SHAFT, H_TOP - 0.4, 0.6, "cream")
    tk.ring_band("crown_cap", top, H_TOP - 0.4, H_TOP, 0.3, "white")
    tk.glow_ring("crown_light", top, H_TOP - 2.6, H_TOP - 1.6, 0.06, "white_Glow")
    tk.prism("roof_deck", tk.offset_poly(top, -0.5), H_SHAFT - 0.3, H_SHAFT + 0.6, "roofd")
    tk.hvac_cluster("roof_plant", 0.0, 0.0, H_SHAFT + 0.6, YAW, 36.0, 10.0, seed=5.0, hmax=3.0)
    tk.plinth("sidewalk", plan, h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
