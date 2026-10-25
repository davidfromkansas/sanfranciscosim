"""Deterministic Blender build of the SF-SIM miniature 575 Market Street.

    blender -b --python build_575_market_street.py -- [--out DIR]

575 Market Street (Hertzka & Knowles, 1975; Standard Oil Building No. 4,
later Chevron Tower): the taller of the two Market Center towers, a 40-storey
slab standing end-on to Market Street. Its skin is precast terra cotta
panels - a pale wall punched by a tight grid
of tall dark windows - over a granite
base, matched to its 1964 sister 555 Market across the shared plaza.
Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "575-market-street"
CENTER = (-122.4003805, 37.7895456)   # OSM way 32963382, OBB centre
H_TOP = 174.65                         # published roof (Wikipedia 174.65 m); LiDAR 175.39
H_BASE = 9.0                           # granite base (published material, height inferred)
H_SHAFT = 167.4                        # INFERRED: top of the window grid; solid panel band above (photo)
L, W = 45.5, 29.2                      # OSM OBB 45.7 x 29.2
YAW = tk.bearing_to_yaw(135.1)         # local +x = bearing 135.1 (away from Market), -x = Market end


def build():
    plan = tk.xform(tk.rect(L, W), YAW)
    # granite base with a dark recessed lobby
    tk.prism("lobby", tk.offset_poly(plan, -1.8), 0.0, H_BASE, "glassd")
    tk.glow_ring("lobby_lit", tk.offset_poly(plan, -1.8), 0.8, H_BASE - 1.5, 0.06, "sand_Glow")
    tk.pier_grid("base_piers", tk.offset_poly(plan, -1.0), 0.0, H_BASE, 4.6, 1.1, 1.0, "granite")
    tk.ring_band("base_band", plan, H_BASE, H_BASE + 1.4, 0.2, "granite")
    # shaft: pale precast terra cotta wall punched by a tight grid of tall windows
    tk.prism("shaft", plan, H_BASE + 1.4, H_SHAFT, "stone", bev=0.3)
    rows = tk.floors(H_BASE + 1.4, H_SHAFT, 4.0)       # 39 storeys
    tk.panes("shaft", plan, [(z0 + 1.0, z1 - 0.35) for z0, z1 in rows], 3.3, mat="glassd", out=0.07,
             margin=0.0, gap=1.5)
    pairs = tk.floors(H_BASE + 1.4, H_SHAFT, 8.0)
    tk.lit_windows("shaft_win", plan, pairs, 5.8, 0.3, seed=12.0, out=0.13, margin=1.0, gap=1.8)
    # solid top band, roof and plant
    tk.prism("top", plan, H_SHAFT, H_TOP - 1.0, "stone", bev=0.2)
    tk.ring_band("parapet", tk.offset_poly(plan, -0.5), H_TOP - 1.0, H_TOP, 0.5, "stone")
    tk.prism("roof_deck", tk.offset_poly(plan, -0.5), H_TOP - 1.3, H_TOP - 0.9, "roofd")
    tk.hvac_cluster("plant", 0.0, 0.0, H_TOP - 0.9, YAW, L * 0.55, W * 0.5, seed=2.5, hmax=0.85, fans=False)
    tk.glow_ring("crown_light", plan, H_SHAFT + 2.0, H_SHAFT + 2.8, 0.3, "white_Glow")
    tk.plinth("plaza", plan, h=0.3, out=3.5)
    # the landscaped plaza between the towers (SW side, local -y)
    p0, p1 = tk.xform([(-L / 2 + 5, -W / 2 - 6.0), (L / 2 - 5, -W / 2 - 6.0)], YAW)
    tk.tree_row("trees", p0, p1, 0.0, 4, h=6.5, seed=5.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
