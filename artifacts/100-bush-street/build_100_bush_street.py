"""Deterministic Blender build of the SF-SIM miniature Shell Building (100 Bush Street).

    blender -b --python build_100_bush_street.py -- [--out DIR]

The Shell Building (George W. Kelham, 1929): a 28-storey Art Deco / Gothic
Moderne office tower at Bush and Battery, all pale cream terracotta. A
three-storey base with round-headed windows carries lower wings and a slender
tower of continuous cream piers between dark recessed window strips; the tower
steps back in tiers near the top into a crown with shell-ornament finials.
Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "100-bush-street"
CENTER = (-122.3999801, 37.7915717)   # OSM way 260282390, OBB centre
H_TOP = 115.22                         # 115.22 m (published, Wikipedia; OSM height tag)
H_BASE = 13.5                          # three-storey base (inferred from photo)
H_WING = 76.0                          # side wings (inferred: about floor 20)
H_T0 = 96.0                            # main tower shaft
H_T1 = 104.0
H_T2 = 110.0
L, W = 36.8, 41.4                      # OSM OBB 37.1 x 41.7
YAW = math.radians(90 - 81.3)          # local +x = bearing 81.3 (E), +y = N
TX, TY = 4.0, 5.0                      # tower pushed toward the Bush x Battery corner (NE, inferred)


def facade(name, plan, z0, z1, seed, density=0.28):
    """Cream terracotta block, dark full-height window strips, scattered lit panes."""
    tk.prism(name, plan, z0, z1, "terracotta", bev=0.12)
    tk.panes(name + "_strips", plan, [(z0, z1)], 2.5, mat="glassd", gap=1.35, margin=0.6)
    if density:
        tk.lit_windows(name + "_lit", plan, tk.floors(z0, z1, 3.9), 2.5, density, seed=seed, out=0.1,
                       margin=0.7, gap=1.35)


def build():
    plan = tk.xform(tk.rect(L, W), YAW)
    tower = tk.xform(tk.rect(28.0, 30.0, TX, TY), YAW)
    t1 = tk.xform(tk.chamfer_rect(23.0, 25.0, 2.0, TX, TY), YAW)
    t2 = tk.xform(tk.chamfer_rect(17.0, 19.0, 3.0, TX, TY), YAW)
    t3 = tk.xform(tk.chamfer_rect(10.0, 12.0, 2.5, TX, TY), YAW)
    # base: round-headed upper windows over dark shopfronts
    tk.prism("base", plan, 0.0, H_BASE, "terracotta", bev=0.15)
    tk.panes("shopfronts", plan, [(0.4, 5.6)], 4.6, mat="glassd", gap=1.4, margin=0.2)
    tk.lit_windows("shop_lit", plan, [(0.4, 5.6)], 4.6, 0.85, seed=1.0, out=0.1, margin=0.3, gap=1.6)
    tk.arched_panes("base_arches", plan, 7.4, 12.2, 2.3, 1.3, mat="glassd")
    tk.cornice("base_cornice", plan, H_BASE, h=0.9, out=0.5, mat="cream")
    # wings and tower
    facade("wings", plan, H_BASE + 0.9, H_WING, 2.0)
    tk.ring_band("wing_parapet", tk.offset_poly(plan, -0.5), H_WING, H_WING + 1.4, 0.5, "cream")
    tk.prism("wing_roof", tk.offset_poly(plan, -0.4), H_WING - 0.2, H_WING + 0.1, "roofd")
    facade("tower", tower, H_WING, H_T0, 3.0)
    facade("tier1", t1, H_T0, H_T1, 4.0, 0.35)
    facade("tier2", t2, H_T1, H_T2, 5.0, 0.0)
    # crown lantern and the shell-ornament finials at the setback corners
    tk.prism("lantern", t3, H_T2, H_TOP - 1.2, "cream", bev=0.12)
    tk.panes("lantern_slots", t3, [(H_T2 + 0.8, H_TOP - 2.4)], 2.5, mat="glassd", gap=1.4, margin=0.0)
    tk.prism("lantern_cap", tk.offset_poly(t3, -1.0), H_TOP - 1.2, H_TOP, "terracotta", bev=0.1)
    for k, (poly, z) in enumerate(((tower, H_T0), (t1, H_T1), (t2, H_T2))):
        for i, (x, y) in enumerate(poly):
            if k and i % 2:
                continue
            tk.cylinder(f"finial_{k}_{i}", x, y, z, z + 1.8, 0.8, "cream", seg=6, r1=0.35)
    tk.prism("tier_decks", tk.offset_poly(tower, -0.3), H_T0 - 0.2, H_T0 + 0.05, "roofd")
    # crown floodlight (the terracotta tiers are lit at night)
    tk.glow_ring("crown_light", t1, H_T1 - 2.4, H_T1 - 0.6, 0.18, "sand_Glow")
    tk.glow_ring("crown_light2", t2, H_T2 - 2.0, H_T2 - 0.5, 0.18, "sand_Glow")
    c = tk.rot2((-11.0, -11.0), YAW)
    tk.hvac_cluster("wing_plant", c[0], c[1], H_WING + 0.1, YAW, 10.0, 12.0, seed=6.0, hmax=2.6)
    tk.plinth("sidewalk", plan, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
