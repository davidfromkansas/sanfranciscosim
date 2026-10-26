"""Deterministic Blender build of the SF-SIM miniature Adam Grant Building.

    blender -b --python build_100_sansome_street.py -- [--out DIR]

114 Sansome Street at Bush (1908): a fourteen-storey post-fire office block
filling most of its lot around an interior light court. The miniature is an
Edwardian commercial palazzo: a two-storey stone base, a light brick shaft
of punched windows, a top storey under a projecting cornice, and the light
court shown as a dark well in the roof. Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "100-sansome-street"
CENTER = (-122.4004726, 37.7915113)  # OSM way 260282389, OBB centre
H_TOP = 58.2                          # DataSF 2010 LiDAR median of ring 201006.0002228 (measured; majority 58.1)
YAW = tk.bearing_to_yaw(81.3)         # local +x = east, +y = north
# OSM outline in local street-grid metres, light-court hole and its slit removed
OUTLINE = [(-21.9, -20.8), (22.0, -20.8), (22.0, -7.9), (17.1, -7.9), (17.1, 20.5), (2.0, 20.5), (2.0, 17.2),
           (-9.6, 17.2), (-9.6, 20.8), (-21.9, 20.8)]
COURT = [(-6.3, -7.5), (4.8, -7.5), (4.8, 8.6), (-6.3, 8.6)]   # OSM light court


def L(poly):
    return tk.xform(poly, YAW)


def build():
    plan = L(OUTLINE)
    tk.prism("base", plan, 0.0, 8.6, "stone", bev=0.15)
    tk.panes("base_win", plan, [(0.0, 8.6)], 3.8, mat="glassd", gap=1.1, margin=0.9)
    tk.lit_windows("base_lit", plan, [(0.0, 4.6)], 3.8, 0.7, seed=1.0, out=0.1, margin=0.6, gap=1.2)
    tk.ring_band("base_cornice", plan, 8.6, 9.4, 0.4, "stone")
    tk.punched_block("shaft", plan, 9.4, 51.4, 3.82, wall="sand", win="glassd", spacing=3.4, gap=1.6,
                     margin=0.9, lit=0.3, seed=6.0, bev=0.12)
    tk.ring_band("band", plan, 51.4, 52.1, 0.3, "stone")
    tk.punched_block("attic", plan, 52.1, 55.6, 3.5, wall="sand", win="glassd", spacing=2.9, gap=1.6,
                     margin=0.8, lit=0.35, seed=7.0, bev=0.1)
    tk.cornice("cornice", plan, 55.6, h=1.6, out=1.2, mat="stone")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.2), 57.2, H_TOP, 0.3, "sand")
    tk.prism("roof", tk.offset_poly(plan, -0.4), 56.9, 57.3, "roofd")
    court = L(COURT)
    tk.ring_band("court_rim", court, 57.3, 57.9, 0.4, "sand")
    tk.glow_cap("court_well", court, 57.34, "ink")
    tk.hvac_cluster("plant", *tk.rot2((10.0, 8.0), YAW), 57.3, YAW, 10.0, 16.0, seed=3.0, hmax=0.85, fans=False)
    tk.box("tank", *tk.rot2((-15.0, -14.0), YAW), 57.3, 58.1, 4.0, 4.0, "rust", yaw=YAW, bev=0.1)
    tk.prism("sidewalk", L(tk.rect(48.0, 45.0, 0.0, 0.0)), 0.0, 0.15, "concrete")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
