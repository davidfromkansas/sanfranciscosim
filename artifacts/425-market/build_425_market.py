"""Deterministic Blender build of the SF-SIM miniature 425 Market Street.

    blender -b --python build_425_market.py -- [--out DIR]

425 Market (SOM, 1973): a 38-storey slab of blue-grey glass held in a crisp
silver aluminium grid, flat-topped, on a colonnaded base set back from
Market Street. Recognition cue: the unbroken blue grid prism, one of the
cleanest International Style slabs downtown. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "425-market"
CENTER = (-122.398153, 37.791204)   # OSM way 32946526, OBB centre
H_TOP = 160.0
H_ROOF = 152.0
H_BASE = 9.0
L, W = 60.0, 37.5                   # OSM OBB 61.3 x 38.5
YAW = math.radians(90 - 134.9)


def build():
    plan = tk.xform(tk.rect(L, W), YAW)
    tk.prism("base_glass", tk.offset_poly(plan, -3.0), 0.0, H_BASE, "glass")
    tk.glow_ring("base_lit", tk.offset_poly(plan, -3.0), 0.8, H_BASE - 1.2, 0.06, "sand_Glow")
    tk.pier_grid("colonnade", tk.offset_poly(plan, -0.6), 0.0, H_BASE, 6.0, 1.2, 1.2, "steel")
    tk.shaft("shaft", plan, H_BASE, H_ROOF, 4.1, glass="glass", band="steel", band_h=1.1, band_out=0.12,
             fins=(3.0, 0.35, 0.35, "steel"), lit=0.3, seed=4.2, lit_spacing=3.0)
    # mechanical penthouse band, recessed, then the roof
    pent = tk.offset_poly(plan, -2.0)
    tk.prism("penthouse", pent, H_ROOF, H_TOP - 4.8, "glassd")
    tk.pier_grid("louvres", pent, H_ROOF, H_TOP - 4.8, 1.6, 0.35, 0.35, "steel")
    tk.prism("roof_cap", tk.offset_poly(pent, 0.3), H_TOP - 4.8, H_TOP - 4.0, "steel", bev=0.15)
    tk.hvac_cluster("cap_plant", 0, 0, H_TOP - 4.0, YAW, L * 0.6, W * 0.5, seed=7.0, hmax=4.0)
    tk.prism("roof_parapet_base", plan, H_ROOF - 0.2, H_ROOF + 0.3, "steel")
    tk.hvac_cluster("roof_plant", 0, 0, H_ROOF + 0.3, YAW, L * 0.9, 3.0, seed=2.0, hmax=3.2)
    tk.plinth("plaza", plan, h=0.3, out=4.0)
    # Orientation: local -x faces 315 deg = Market St (NW, short face); local +y faces
    # 45 deg = Fremont St (NE, long face). Street trees along Fremont.
    p0, p1 = tk.xform([(-L / 2 + 5, W / 2 + 3), (L / 2 - 5, W / 2 + 3)], YAW)
    tk.tree_row("trees", p0, p1, 0.3, 4, h=6.0, seed=8.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
