"""Deterministic Blender build of the SF-SIM miniature 49 Stevenson Street.

    blender -b --python build_49_stevenson_street.py -- [--out DIR]

49 Stevenson Street (1989): a fifteen-storey office building on the alley
block between Market and Mission, fronting Stevenson Street. Its OSM outline
is a 41.6 x 25.7 m slab whose north (Market-side, east) corner is cut into a
saw-tooth of small steps. No photograph was available: the miniature is a
late-1980s granite-and-glass treatment read from the outline and the LiDAR
roof (a 60 m main roof with a 64 m screened plant top) - a two-storey granite
base, ribbon-window shaft with granite spandrels, a stepped corner that runs
the full height, and a screened crown. Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "49-stevenson-street"
CENTER = (-122.3993944, 37.7897092)  # OSM way 149837256, OBB centre
H_TOP = 64.44                         # DataSF 2010 LiDAR max of ring 201006.0003248 (crown screen)
H_ROOF = 60.0                         # LiDAR median (main roof); majority 63.9 = the crown
YAW = tk.bearing_to_yaw(44.9)         # local +x = NE along Stevenson, +y = NW (toward Market)
OUTLINE = [(-20.8, 12.9), (-20.7, -10.3), (-15.7, -10.3), (-15.6, -12.8), (20.8, -12.9), (20.7, 7.2),
           (20.2, 7.2), (20.2, 9.2), (18.3, 9.2), (18.3, 10.4), (17.2, 10.4), (17.2, 12.2), (15.3, 12.2),
           (15.3, 12.9)]


def L(poly):
    return tk.xform(poly, YAW)


def P(x, y):
    return tk.rot2((x, y), YAW)


def build():
    plan = L(OUTLINE)
    # two-storey granite base with a lit lobby
    tk.prism("base", plan, 0.0, 8.6, "granite", bev=0.15)
    tk.panes("base_win", plan, [(0.0, 8.6)], 3.6, mat="glassd", gap=0.9, margin=0.8)
    tk.lit_windows("base_lit", plan, [(0.0, 4.6)], 3.6, 0.7, seed=2.0, out=0.1, margin=0.6, gap=1.0)
    tk.ring_band("base_cap", plan, 8.6, 9.3, 0.3, "stone")
    # ribbon-window shaft: 13 storeys of 3.9 m, granite spandrels
    tk.shaft("shaft", plan, 9.3, 60.0, 3.9, glass="glassd", band="granite", band_h=1.5, band_out=0.25,
             lit=0.3, seed=4.0, lit_spacing=3.6, glass_in=-0.25)
    # parapet, main roof, set-back screened crown over the plant
    tk.ring_band("parapet", plan, H_ROOF, H_ROOF + 1.0, 0.3, "stone")
    tk.prism("roof", tk.offset_poly(plan, -0.4), H_ROOF - 0.2, H_ROOF + 0.15, "roofd")
    crown = L(tk.rect(26.0, 14.0, -1.5, -1.0))
    tk.prism("crown_core", tk.offset_poly(crown, -1.0), H_ROOF + 0.15, 63.6, "steel")
    tk.ring_band("crown_screen", crown, H_ROOF + 0.15, H_TOP, 0.3, "granite")
    tk.prism("crown_deck", tk.offset_poly(crown, -0.2), 63.6, 63.9, "roofd")
    tk.glow_ring("crown_line", tk.offset_poly(crown, 0.3), H_TOP - 0.6, H_TOP - 0.2, 0.05, "white_Glow")
    tk.prism("sidewalk", L(tk.rect(46.0, 30.0, 0.0, -0.5)), 0.0, 0.15, "concrete")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
