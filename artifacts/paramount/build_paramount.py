"""Deterministic Blender build of the SF-SIM miniature The Paramount (680 Mission Street).

    blender -b --python build_paramount.py -- [--out DIR]

The Paramount (Kwan Henmi Architecture/Planning, 2001): a 40-storey rental-apartment
tower at Mission and Third, once the tallest concrete-framed building in
Seismic Zone 4. Pale precast with long ribbon windows; a broad lower block
with stepped shoulders carries a central slab that rises another ten storeys
to a thin, boldly overhanging flat roof cap. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "paramount"
CENTER = (-122.4020234, 37.7867294)   # OSM way 160673823, OBB centre
H_TOP = 128.0                          # 420 ft (published, Wikipedia; OSM height 127)
H_POD = 11.0                           # three-storey retail/lobby podium (estimated)
H_WING = 92.0                          # shoulders: LiDAR 91.67 (the 2010 hit on the lower block)
H_SLAB = 124.6                         # top floor of the central slab
H_CAP = 126.6                          # underside of the overhanging roof cap (estimated)
YAW = math.radians(90 - 45.4)          # local +x = bearing 45.4 (NE), +y = 315.4 (NW) = Mission St; -x (SW) = Third St

# OSM footprint in the local frame: 50.4 x 47.8 m with a notch at the north (+x, +y) corner
LOCAL = [(-25.2, -23.9), (25.2, -23.9), (25.2, 15.7), (12.3, 15.7), (12.3, 23.9), (-25.2, 23.9)]
SLAB = tk.rect(40.0, 24.0, -3.0, -2.0)   # central slab, long axis NE-SW; shoulders on the Mission and rear sides (inferred)


def build():
    plan = tk.xform(LOCAL, YAW)
    slab = tk.xform(SLAB, YAW)
    # podium: retail glass under a stone band
    tk.prism("podium", tk.offset_poly(plan, -0.6), 0.0, H_POD - 1.2, "glassd")
    tk.glow_ring("podium_lit", tk.offset_poly(plan, -0.6), 0.6, H_POD - 3.0, 0.06, "sand_Glow")
    tk.pier_grid("podium_piers", plan, 0.0, H_POD - 1.2, 6.0, 1.0, 0.6, "stone")
    tk.prism("podium_band", plan, H_POD - 1.2, H_POD, "stone", bev=0.1)
    # lower block: 26 storeys of ribbon windows between pale precast bands
    p = (H_WING - H_POD) / 26
    tk.shaft("lower", plan, H_POD, H_WING, p, glass="glass", band="stone", band_h=1.45, band_out=0.15,
             lit=0.3, seed=2.0, lit_spacing=3.6, lit_mat="sand_Glow")
    tk.ring_band("lower_parapet", tk.offset_poly(plan, -0.4), H_WING, H_WING + 1.1, 0.4, "stone")
    tk.prism("lower_roof", tk.offset_poly(plan, -0.3), H_WING - 0.2, H_WING + 0.1, "roofd")
    # central slab: ten more storeys
    tk.shaft("upper", slab, H_WING, H_SLAB, (H_SLAB - H_WING) / 10, glass="glass", band="concrete",
             band_h=1.45, band_out=0.15, lit=0.35, seed=3.0, lit_spacing=3.6)
    # recessed top storey and the overhanging flat roof cap
    tk.prism("loggia", tk.offset_poly(slab, -1.2), H_SLAB, H_CAP, "glassd")
    tk.glow_ring("loggia_lit", tk.offset_poly(slab, -1.2), H_SLAB + 0.3, H_CAP - 0.3, 0.05, "white_Glow")
    tk.prism("cap", tk.offset_poly(slab, 2.4), H_CAP, H_TOP, "concrete", bev=0.15)
    # shoulder roof terraces: planters and plant
    for k, y in enumerate((-19.5, 17.0)):
        c = tk.rot2((-6.0, y), YAW)
        tk.hvac_cluster(f"plant_{k}", c[0], c[1], H_WING + 0.1, YAW, 18.0, 6.0, seed=4.0 + k, hmax=2.2)
    tk.plinth("sidewalk", plan, h=0.25, out=2.5)
    p0, p1 = tk.xform([(-22.0, 26.6), (10.0, 26.6)], YAW)
    tk.tree_row("mission_trees", p0, p1, 0.25, 4, h=6.0, seed=6.1)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
