"""Deterministic Blender build of the SF-SIM miniature One Post Street.

    blender -b --python build_1_post_street.py -- [--out DIR]

One Post Street (Welton Becket & Associates, 1969; formerly McKesson Plaza):
a 38-storey octagonal tower on the Market/Post/Montgomery flatiron site. A
close comb of dark bronze-brown stone piers runs unbroken from a tall glass
lobby to a flat top, over dark glass - Becket's repetitive geometry in natural
stone. The clipped corners make it read as a slim dark octagonal prism. The
plaza holds the two-tier octagonal BART entrance. Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "1-post-street"
CENTER = (-122.4026604, 37.7887819)   # OSM way 32946671, OBB centre
H_TOP = 161.0                          # published roof (Wikipedia 161 m / 529 ft); LiDAR 166.04
H_LOBBY = 8.0                          # INFERRED: double-height glass lobby (photo)
YAW = tk.bearing_to_yaw(81.3)          # local +x = bearing 81.3 (street grid), +y = 351.3

# Local octagon (x ~ east, y ~ north) from the 8-node OSM outline.
LOCAL = [(-17.6, 12.0), (-17.6, -12.3), (-13.6, -16.6), (14.2, -16.6), (17.6, -12.3), (17.6, 12.7),
         (13.6, 16.6), (-13.1, 16.6)]


def build():
    plan = tk.ccw(tk.xform(LOCAL, YAW))
    # tall glass lobby behind the piers
    tk.prism("lobby", tk.offset_poly(plan, -1.6), 0.0, H_LOBBY, "glassl")
    tk.glow_ring("lobby_lit", tk.offset_poly(plan, -1.6), 0.8, H_LOBBY - 1.5, 0.06, "sand_Glow")
    tk.prism("transfer", plan, H_LOBBY, H_LOBBY + 1.2, "bronze")
    # dark glass shaft behind the pier comb; faint spandrel line every 4 storeys
    tk.prism("shaft", tk.offset_poly(plan, -0.3), H_LOBBY + 1.2, H_TOP - 1.2, "glassd")
    tk.pier_grid("piers", tk.offset_poly(plan, -0.3), H_LOBBY, H_TOP, 2.25, 0.8, 0.75, "bronze",
                 skip_short=3.0)
    groups = tk.floors(H_LOBBY + 1.2, H_TOP - 1.2, 15.06)     # 10 groups of ~4 storeys
    tk.panes("spandrels", tk.offset_poly(plan, -0.3), [(z0, z0 + 0.7) for z0, _ in groups[1:]], 2.25,
             mat="ink", out=0.06, margin=0.0, gap=0.0)
    lit = tk.floors(H_LOBBY + 1.2, H_TOP - 1.2, 7.53)
    tk.lit_windows("shaft_win", tk.offset_poly(plan, -0.3), lit, 4.5, 0.3, seed=2.0, out=0.86, margin=0.9,
                   gap=0.6)
    # flat top: deck inside a bronze parapet, small plant
    tk.prism("roof_deck", tk.offset_poly(plan, -0.4), H_TOP - 1.5, H_TOP - 1.1, "roofd")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.4), H_TOP - 1.2, H_TOP, 0.4, "bronze")
    tk.hvac_cluster("plant", 0.0, 0.0, H_TOP - 1.1, YAW, 18.0, 14.0, seed=7.0, hmax=1.0, fans=False)
    tk.glow_ring("crown_light", plan, H_TOP - 3.0, H_TOP - 2.2, 0.9, "white_Glow")
    # plaza with the octagonal BART well and trees (Market side, local south/east)
    tk.plinth("plaza", plan, h=0.3, out=4.0)
    bx, by = tk.rot2((8.0, -24.0), YAW)
    well = tk.xform(tk.chamfer_rect(10.0, 7.0, 2.2), YAW, bx, by)
    tk.ring_band("bart_well", well, 0.0, 1.0, 0.6, "stone")
    tk.prism("bart_floor", well, 0.0, 0.05, "roofd")
    p0, p1 = tk.xform([(-14.0, -22.0), (0.0, -24.0)], YAW)
    tk.tree_row("trees", p0, p1, 0.0, 3, h=6.0, seed=3.9)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
