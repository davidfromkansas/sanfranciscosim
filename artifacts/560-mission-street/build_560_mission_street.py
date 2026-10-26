"""Deterministic Blender build of the SF-SIM miniature JPMorgan Chase Building (560 Mission Street).

    blender -b --python build_560_mission_street.py -- [--out DIR]

560 Mission Street (Cesar Pelli & Associates, 2002): a 31-storey "minimalist
tower wrapped in black steel" - a clean rectangular slab of pale glass behind
a crisp black steel grid of mullions and floor lines, a slim ledge partway up,
the grid running up past the roof as an open steel crown frame, and a tall
black-columned base opening onto a landscaped plaza with George Rickey's ring
sculpture. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "560-mission-street"
CENTER = (-122.3994826, 37.7887773)   # OSM way 79377216, OBB centre
H_TOP = 128.02                         # 128.02 m (published, Wikipedia); LiDAR 127.81
H_ROOF = 122.0                         # roof deck; the steel frame runs on to the crest (inferred)
H_BASE = 9.0
H_LEDGE = 46.0                         # slim ledge seen in the photo (about floor 11)
L, W = 54.6, 37.6                      # OSM 54.9 x 37.9
YAW = math.radians(90 - 134.3)         # local +x = bearing 134.3 (SE), +y = 44.3 (NE)


def build():
    plan = tk.xform(tk.rect(L, W), YAW)
    # tall colonnaded base: recessed dark lobby glass behind black columns
    tk.prism("lobby", tk.offset_poly(plan, -1.8), 0.0, H_BASE, "glassd")
    tk.glow_ring("lobby_lit", tk.offset_poly(plan, -1.8), 0.6, H_BASE - 2.0, 0.06, "sand_Glow")
    tk.pier_grid("columns", tk.offset_poly(plan, -0.9), 0.0, H_BASE, 9.0, 0.9, 0.9, "ink")
    tk.prism("transfer", plan, H_BASE, H_BASE + 0.6, "ink")
    # shaft: pale glass behind a black steel grid
    n1 = 9
    p = (H_ROOF - H_BASE - 0.6) / 28
    z_ledge = H_BASE + 0.6 + n1 * p
    tk.shaft("low", plan, H_BASE + 0.6, z_ledge, p, glass="glassl", band="ink", band_h=0.45, band_out=0.2,
             fins=(4.1, 0.3, 0.35, "ink"), lit=0.3, seed=2.0, lit_spacing=4.1)
    tk.ring_band("ledge", plan, z_ledge, z_ledge + 0.5, 0.7, "ink")
    tk.shaft("high", plan, z_ledge + 0.5, H_ROOF, (H_ROOF - z_ledge - 0.5) / (28 - n1), glass="glassl",
             band="ink", band_h=0.45, band_out=0.2, fins=(4.1, 0.3, 0.35, "ink"), lit=0.3, seed=3.0,
             lit_spacing=4.1)
    # open steel crown frame round the roof
    tk.prism("roof_deck", tk.offset_poly(plan, -0.5), H_ROOF - 0.2, H_ROOF + 0.1, "roofd")
    tk.pier_grid("crown_posts", tk.offset_poly(plan, -0.2), H_ROOF, H_TOP - 0.8, 6.2, 0.3, 0.55, "ink")
    tk.ring_band("crown_frame", tk.offset_poly(plan, -0.2), H_TOP - 0.8, H_TOP, 0.55, "ink")
    tk.ring_band("crown_rail", tk.offset_poly(plan, -0.2), H_ROOF + 2.6, H_ROOF + 3.0, 0.55, "ink")
    tk.hvac_cluster("roof_plant", 0, 0, H_ROOF + 0.1, YAW, 30.0, 20.0, seed=4.0, hmax=4.0)
    tk.glow_ring("crown_light", tk.offset_poly(plan, -0.5), H_ROOF + 0.4, H_ROOF + 1.6, 0.05, "white_Glow")
    # plaza on the NW (Stevenson Place) side, inferred: paving, bamboo, the Rickey ring sculpture
    plaza = tk.xform(tk.rect(L + 6.0, W + 6.0, 0.0, 0.0), YAW)
    tk.plinth("sidewalk", plaza, h=0.25, out=0.0)
    ext = tk.xform(tk.rect(16.0, W + 6.0, -L / 2 - 11.0, 0.0), YAW)
    tk.prism("plaza", ext, 0.0, 0.3, "stone", bev=0.08)
    pool = tk.xform(tk.rect(6.0, 14.0, -L / 2 - 10.0, -4.0), YAW)
    tk.prism("pool", pool, 0.3, 0.4, "sky")
    c = tk.rot2((-L / 2 - 10.0, -4.0), YAW)
    tk.ring_band("eclipse", tk.ellipse(2.6, 2.6, 12, c[0], c[1]), 5.0, 5.4, 0.35, "steel")
    tk.cylinder("eclipse_post", c[0], c[1], 0.4, 5.0, 0.18, "steel", seg=6)
    p0, p1 = tk.xform([(-L / 2 - 6.0, 10.0), (-L / 2 - 6.0, W / 2 + 1.0)], YAW)
    tk.tree_row("bamboo", p0, p1, 0.3, 3, h=5.0, r=1.4, seed=2.2)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
