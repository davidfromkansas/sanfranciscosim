"""Deterministic Blender build of the SF-SIM miniature Four Seasons Hotel and Residences, 757 Market Street.

    blender -b --python build_757_market_street.py -- [--out DIR]

757 Market Street (Millennium Partners, 2001): a hotel-and-condominium tower over a
block-filling podium of hotel, sports club and shops between Market Street and
Yerba Buena Lane. A 40-storey slab of pale stone and glass rises from the Market
Street half of the site; the podium roof behind it steps down to the lane. No
usable photo was obtained, so the skin is modelled from the general description
(light stone, regular punched windows); see REFERENCE.md. Recognition cues: the
tall pale tower set right on Market with its broad low podium behind. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "757-market-street"
CENTER = (-122.4042838, 37.786245)   # OSM way 149332498, OBB centre
H_TOP = 130.1                         # DataSF 2010 LiDAR max over the site, 130.07 m (measured crest)
H_ROOF = 121.0                        # tower roof: OSM building:part 435591307 height=121 (40 levels)
H_POD = 28.7                          # podium: LiDAR median 28.69 m (OSM height=29)
YAW = math.radians(90 - 45.0)         # local +x along Market (bearing ~45)
# OSM way 149332498 (whole site) and building:part 435591307 (the tower), metres about CENTER
SITE = [(-11.49, 48.13), (-45.14, 15.01), (-40.87, 10.72), (-47.27, 0.06), (-32.97, -14.3), (5.98, -53.39),
        (8.94, -50.48), (15.17, -44.2), (53.68, -6.49), (39.63, 7.6), (34.15, 2.33), (25.48, 11.02),
        (20.35, 16.17), (-5.57, 42.2)]
TOWER = [(-2.97, 7.05), (-32.96, -14.3), (-47.27, 0.06), (-40.86, 10.71), (-5.57, 42.19), (20.36, 16.16),
         (14.01, 10.57), (19.2, 4.23), (11.66, -4.2)]


def build():
    site = tk.ccw(SITE)
    tower = tk.ccw(TOWER)
    # podium: shopfront glass at the street, stone above, a planted roof deck
    tk.prism("podium_base", site, 0.0, 6.0, "sand", bev=0.15)
    tk.panes("podium_shops", site, [(0.3, 5.0)], 5.0, mat="glassd", gap=1.0, margin=0.0)
    tk.lit_windows("podium_lit", site, [(0.3, 4.6)], 5.0, 0.8, seed=1.0, out=0.1, margin=0.3, gap=1.4)
    tk.punched_block("podium", site, 6.0, H_POD, (H_POD - 6.0) / 4, wall="sand", win="glassd", spacing=5.5,
                     gap=1.6, margin=0.9, lit=0.3, seed=2.0, bev=0.12)
    tk.ring_band("podium_parapet", tk.offset_poly(site, -0.5), H_POD, H_POD + 1.0, 0.5, "stone")
    tk.prism("podium_roof", tk.offset_poly(site, -0.3), H_POD - 0.3, H_POD + 0.05, "roofd")
    c = tk.rot2((-10.0, -22.0), YAW)
    tk.prism("podium_garden", tk.xform(tk.rect(26.0, 14.0), YAW, c[0], c[1]), H_POD, H_POD + 0.4, "leafd")
    c = tk.rot2((14.0, -28.0), YAW)
    tk.hvac_cluster("podium_plant", c[0], c[1], H_POD + 0.05, YAW, 12.0, 12.0, seed=3.0, hmax=3.0)
    # tower: pale stone with a regular grid of windows; 23 bands of ~3.97 m (the real
    # floors are ~3 m apart; fewer, taller bands keep the triangle budget), paired panes
    z0 = H_POD + 1.0
    tk.punched_block("tower", tower, z0, H_ROOF, (H_ROOF - z0) / 23, wall="sand", win="glass", spacing=4.8,
                     gap=1.4, margin=0.8, lit=0.32, seed=5.0, bev=0.15)
    tk.cornice("tower_cornice", tower, H_ROOF, h=0.9, out=0.5, mat="stone")
    # crown: a set-back mechanical screen to the LiDAR crest, lit at night
    crown = tk.offset_poly(tower, -4.0)
    tk.ring_band("crown_screen", tk.offset_poly(crown, -0.6), H_ROOF + 0.9, H_TOP, 0.6, "stone")
    tk.prism("tower_roof", tk.offset_poly(tower, -0.3), H_ROOF + 0.5, H_ROOF + 0.95, "roofd")
    tk.glow_ring("crown_light", crown, H_TOP - 2.0, H_TOP - 1.0, 0.06, "white_Glow")
    tk.plinth("sidewalk", site, h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
