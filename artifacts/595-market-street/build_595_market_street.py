"""Deterministic Blender build of the SF-SIM miniature 595 Market Street.

    blender -b --python build_595_market_street.py -- [--out DIR]

595 Market Street (Skidmore, Owings & Merrill, 1979): a 30-storey office tower
at Market and Second, square in plan with deeply chamfered corners, wrapped in
alternating bright aluminium spandrels and dark blue ribbon windows - a crisp
horizontal "striped" tower - capped by a tall pale louvred mechanical screen,
over a low planted podium. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "595-market-street"
CENTER = (-122.4007917, 37.7892292)   # OSM way 941649701, OBB centre
H_TOP = 125.0                          # roof 410 ft (published); LiDAR 128.95 incl. roof plant
H_LOBBY = 8.0
H_SCREEN = 117.0                       # louvred mechanical screen 117-125 (inferred from photo)
S = 41.0                               # OSM square 41.7 x 41.2
CH = 8.0                               # chamfer leg (inferred from photo; OSM traces a plain square)
YAW = math.radians(90 - 135.1)         # square sides parallel to Market (bearing ~45)


def build():
    plan = tk.xform(tk.chamfer_rect(S, S, CH), YAW)
    pod = tk.xform(tk.rect(S + 1.0, S + 1.0), YAW)
    # podium: two storeys of stone with a recessed dark lobby; planted terrace on top
    tk.prism("podium", pod, 0.0, H_LOBBY - 1.5, "stone", bev=0.15)
    tk.panes("podium_win", pod, [(0.5, 5.0)], 4.2, mat="glassd", gap=0.8, margin=0.3)
    tk.lit_windows("podium_lit", pod, [(0.5, 5.0)], 4.2, 0.7, seed=1.0, out=0.1, margin=0.5, gap=1.0)
    tk.prism("podium_deck", tk.offset_poly(pod, -0.3), H_LOBBY - 1.5, H_LOBBY - 1.2, "leafd")
    for k, (x, y) in enumerate(((-17.5, -17.5), (17.5, -17.5), (-17.5, 17.5), (17.5, 17.5))):
        px, py = tk.rot2((x, y), YAW)
        tk.tree(f"terrace_tree_{k}", px, py, H_LOBBY - 1.2, h=4.5, r=1.8, mat="leaf")
    # shaft: 27 striped storeys of bright spandrel + dark blue ribbon glass
    z0 = H_LOBBY - 1.2
    tk.shaft("shaft", plan, z0, H_SCREEN, (H_SCREEN - z0) / 27, glass="glass", band="white", band_h=1.75,
             band_out=0.2, fins=None, lit=0.3, seed=4.0, lit_spacing=3.4)
    # louvred mechanical screen: pale band with fine horizontal louvre lines
    tk.ring_band("screen", tk.offset_poly(plan, -0.6), H_SCREEN, H_TOP, 0.6, "trim")
    tk.spandrels("louvres", plan, [H_SCREEN + 1.4 + 1.6 * i for i in range(4)], 0.25, 0.12, "steel")
    tk.prism("roof_deck", tk.offset_poly(plan, -0.6), H_SCREEN, H_TOP - 2.2, "roofd")
    tk.hvac_cluster("roof_plant", 0, 0, H_TOP - 2.2, YAW, 22.0, 22.0, seed=6.0, hmax=2.0)
    tk.glow_ring("crown_light", plan, H_SCREEN + 0.2, H_SCREEN + 0.9, 0.12, "white_Glow")
    tk.plinth("plaza", pod, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
