"""Deterministic Blender build of the SF-SIM miniature 44 Montgomery Street.

    blender -b --python build_44_montgomery_street.py -- [--out DIR]

44 Montgomery (John Graham & Company, 1967; built for Wells Fargo): a
43-storey slab, the tallest building west of Dallas when it opened. Its whole
skin is a dense comb of slender white vertical fins over dark glass, running
unbroken from the lobby to a crisp flat top where the fins stand proud of the
roof like teeth. A slightly lower second slab steps back to the east along
Sutter Street. Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "44-montgomery-street"
CENTER = (-122.4017284, 37.7896264)   # OSM way 32963370, OBB centre
H_TOP = 172.2                          # published roof (Wikipedia 172.2 m; antenna 180.7 m not modelled)
H_ROOF = 170.6                         # roof deck; the fin tips rise 1.6 m above it to the crest
H_EAST = 150.6                         # INFERRED: east (Sutter) slab ~5 storeys lower, from the photo
H_LOBBY = 9.0
YAW = tk.bearing_to_yaw(80.9)          # local +x = bearing 80.9 (street grid), +y = 350.9

# Local plans (x ~ east, y ~ north) from the 18-node OSM outline.
# West face = Montgomery St, north face = Sutter St, south end = toward Market.
MAIN = [(-25.9, -41.0), (-7.0, -41.0), (-7.0, -8.0), (-1.6, -8.0), (-1.6, 41.0), (-25.9, 41.0)]
EAST = [(-1.6, 20.5), (28.2, 20.5), (28.2, 41.0), (-1.6, 41.0)]


def slab(name, local, z_top, seed):
    plan = tk.ccw(tk.xform(local, YAW))
    tk.prism(name + "_lobby", tk.offset_poly(plan, -1.6), 0.0, H_LOBBY, "glassd")
    tk.glow_ring(name + "_lobby_lit", tk.offset_poly(plan, -1.6), 0.8, H_LOBBY - 1.8, 0.06, "sand_Glow")
    tk.prism(name + "_glass", plan, H_LOBBY, z_top - 1.6, "glassd")
    tk.prism(name + "_deck", tk.offset_poly(plan, -0.2), z_top - 1.9, z_top - 1.5, "roofd")
    # the comb: white fins from the pavement to 1.6 m above the roof
    tk.pier_grid(name + "_fins", plan, 0.0, z_top, 1.65, 0.45, 0.65, "white", skip_short=3.0)
    bands = tk.floors(H_LOBBY, z_top - 1.6, 7.6)
    tk.lit_windows(name + "_win", plan, bands, 3.3, 0.3, seed=seed, out=0.75, margin=0.9, gap=0.4)
    return plan


def build():
    main = slab("main", MAIN, H_TOP, 4.0)
    east = slab("east", EAST, H_EAST, 9.0)
    c = tk.rot2((-13.8, 6.0), YAW)
    tk.hvac_cluster("plant", c[0], c[1], H_ROOF - 1.5 + 0.05, YAW, 16.0, 50.0, seed=2.0, hmax=1.4, fans=False)
    c = tk.rot2((13.0, 30.7), YAW)
    tk.hvac_cluster("plant_e", c[0], c[1], H_EAST - 1.5, YAW, 20.0, 12.0, seed=5.0, hmax=2.5)
    tk.glow_ring("crown_light", main, H_TOP - 1.4, H_TOP - 0.6, 0.7, "white_Glow")
    tk.plinth("plaza", main, h=0.3, out=3.0)
    tk.plinth("plaza_e", east, h=0.25, out=3.0)
    # street trees on Montgomery (west)
    p0, p1 = tk.xform([(-31.0, -36.0), (-31.0, 10.0)], YAW)
    tk.tree_row("trees", p0, p1, 0.3, 3, h=6.0, seed=4.1)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
