"""Deterministic Blender build of the SF-SIM miniature 350 Mission (Salesforce East).

    blender -b --python build_350_mission.py -- [--out DIR]

350 Mission Street (SOM, 2015): a 30-storey blue glass prism whose facade
panels are canted to make a shimmering pixel pattern, standing on a 17 m tall
transparent lobby with a giant LED media wall behind the glass. Recognition
cues: the see-through base and the faceted blue shaft. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "350-mission"
CENTER = (-122.396720, 37.790872)   # OSM way 226514310, OBB centre
H_TOP = 129.0                        # roof, 424 ft
H_LOBBY = 17.0
L, W = 38.5, 36.5                   # OSM OBB 39.4 x 37.2
YAW = math.radians(90 - 135.0)


def build():
    plan = tk.xform(tk.rect(L, W), YAW)
    # the glass lobby: tall, clear, with the LED wall and a hovering shaft above
    tk.prism("lobby_glass", tk.offset_poly(plan, -1.2), 0.0, H_LOBBY, "glassl")
    tk.glow_ring("lobby_lit", tk.offset_poly(plan, -1.2), 0.8, H_LOBBY - 1.0, 0.06, "sand_Glow")
    tk.pier_grid("lobby_mullions", tk.offset_poly(plan, -1.0), 0.0, H_LOBBY, 4.5, 0.25, 0.3, "steel")
    # LED media wall facing Mission (NW): a sky-blue slab that glows at night
    a, b = tk.xform([(-L / 2 + 6, W / 2 - 1.6), (L / 2 - 6, W / 2 - 1.6)], YAW)
    nx, ny = tk.rot2((0, 1), YAW)
    tk.box("led_wall", (a[0] + b[0]) / 2 - nx * 0.6, (a[1] + b[1]) / 2 - ny * 0.6, 3.0, H_LOBBY - 2.5,
           L - 12, 0.8, "sky", yaw=YAW)
    tk.flat_quad("led_wall_glow", a, b, 3.2, H_LOBBY - 2.7, -0.15, "sky_Glow", (nx, ny))
    tk.prism("transfer", plan, H_LOBBY, H_LOBBY + 1.2, "steel", bev=0.15)
    # shaft: two-tone blue bands read as the canted pixel panels
    tk.shaft("shaft", plan, H_LOBBY + 1.2, H_TOP - 4.5, 4.2, glass="glass", band="glassl", band_h=1.6,
             band_out=0.25, fins=(4.6, 0.25, 0.3, "glassl"), lit=0.3, seed=9.0, lit_spacing=3.0)
    tk.ring_band("crown_screen", tk.offset_poly(plan, -0.3), H_TOP - 4.5, H_TOP, 0.3, "glass")
    tk.prism("roof_deck", tk.offset_poly(plan, -0.4), H_TOP - 4.8, H_TOP - 4.4, "roofd")
    tk.hvac_cluster("roof_plant", 0, 0, H_TOP - 4.4, YAW, L * 0.6, W * 0.5, seed=4.0, hmax=4.0)
    tk.glow_ring("crown_light", plan, H_TOP - 3.5, H_TOP - 1.0, 0.36, "white_Glow")
    # Salesforce cloud by the corner, semantically enlarged
    for k, (dx, w, h, dz) in enumerate(((-2.6, 3.6, 2.6, 0.0), (0.0, 5.0, 3.8, 0.5), (2.6, 3.2, 2.4, 0.1))):
        cx, cy = tk.rot2((dx - 10, W / 2 + 0.4), YAW)
        tk.box(f"cloud_{k}", cx, cy, 22.0 + dz, 22.0 + dz + h, w, 0.8, "sky", yaw=YAW, bev=0.3)
    tk.plinth("plaza", plan, h=0.3, out=3.0)
    p0, p1 = tk.xform([(-L / 2 + 4, W / 2 + 2.2), (L / 2 - 4, W / 2 + 2.2)], YAW)
    tk.tree_row("trees", p0, p1, 0.3, 3, h=6.0, seed=3.3)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
