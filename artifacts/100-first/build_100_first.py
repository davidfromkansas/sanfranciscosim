"""Deterministic Blender build of the SF-SIM miniature 100 First Street (100 First Plaza).

    blender -b --python build_100_first.py -- [--out DIR]

100 First Plaza (SOM, 1988): a 27-storey postmodern tower of cream stone
with blue-glass notched corners that climbs in setbacks to a crown of stepped
gables and a spire at 136.25 m, over a three-storey podium. Recognition cues:
the stepped, gabled crown and the stone/blue-glass two-tone. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "100-first"
CENTER = (-122.3975827, 37.7892919)  # OSM tower part 1410929341, OBB centre
H_TOP = 136.25                       # spire (published); roof 116 m
H_ROOF = 116.0
H_POD = 13.0
L, W = 34.0, 29.5                    # tower part OBB 35.3 x 30.4
YAW = math.radians(90 - 135.3)
TIERS = [(96.0, 0.0), (106.0, 3.0), (H_ROOF, 6.0)]


def plan(inset=0.0, notch=3.4):
    return tk.xform(tk.notch_rect(L - 2 * inset, W - 2 * inset, notch), YAW)


def build():
    # podium: three-storey stone base reaching toward First Street (OSM way 91626348)
    pod = tk.xform(tk.rect(56.0, 44.0, -6.0, 3.0), YAW)
    tk.prism("podium", pod, 0.0, H_POD, "sand", bev=0.2)
    tk.panes("podium_win", pod, tk.floors(1.0, H_POD - 1.0, 4.0), 3.6, mat="glass", gap=1.2, margin=0.6)
    tk.lit_windows("podium_lit", pod, tk.floors(1.0, H_POD - 1.0, 4.0), 3.6, 0.5, seed=2.0, out=0.1,
                   margin=0.6, gap=1.2)
    tk.roof_kit("podium_roof", pod, H_POD, seed=4.0, parapet=0.8, plant_frac=0.3, yaw=YAW)
    z = H_POD
    for i, (zt, inset) in enumerate(TIERS):
        p = plan(inset)
        tk.punched_block(f"tier{i}", p, z, zt, 4.0, wall="sand", win="glass", spacing=2.7, gap=1.0,
                         margin=0.8, lit=0.3, seed=1.0 + i, bev=0.2)
        # blue-glass notched corners: glass prisms filling each notch
        hw, hd, n = (L - 2 * inset) / 2, (W - 2 * inset) / 2, 3.4
        for k, (sx, sy) in enumerate(((1, 1), (-1, 1), (-1, -1), (1, -1))):
            c = tk.rot2((sx * (hw - n / 2), sy * (hd - n / 2)), YAW)
            tk.box(f"corner{i}_{k}", c[0], c[1], z, zt, n, n, "glassl", yaw=YAW)
        if i:
            tk.cornice(f"setback{i}", plan(TIERS[i - 1][1]), z - 0.8, h=0.8, out=0.3, mat="trim")
        z = zt
    # the crown: a gabled pyramid in two steps and the spire
    top = plan(TIERS[-1][1], 2.6)
    tk.cornice("crown_base", top, H_ROOF, h=1.0, out=0.5, mat="trim")
    tk.pyramid("crown_low", tk.offset_poly(top, -0.2), H_ROOF + 1.0, H_ROOF + 10.0, "glass")
    tk.pyramid("crown_top", tk.xform(tk.rect(8.0, 8.0), YAW), H_ROOF + 6.5, H_ROOF + 13.0, "trim")
    tk.cylinder("spire", 0.0, 0.0, H_ROOF + 12.0, H_TOP - 1.2, 0.6, "trim", seg=6, r1=0.2)
    tk.cylinder("spire_tip_glow", 0.0, 0.0, H_TOP - 1.2, H_TOP, 0.4, "red_Glow", seg=6)
    tk.glow_ring("crown_light", top, H_ROOF + 1.2, H_ROOF + 3.0, -0.6, "white_Glow")
    tk.plinth("plaza", pod, h=0.3, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
