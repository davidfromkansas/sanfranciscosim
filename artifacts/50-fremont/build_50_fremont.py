"""Deterministic Blender build of the SF-SIM miniature 50 Fremont (Salesforce West).

    blender -b --python build_50_fremont.py -- [--out DIR]

50 Fremont Center (SOM, 1985), now Salesforce West: a 43-storey tower of
pale grey precast with a tight grid of punched square windows, serrated
(notched) corners and a stepped top. The blue Salesforce cloud on the lower
facade is the street identity. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "50-fremont"
CENTER = (-122.397241, 37.790510)   # OSM way 288716396, OBB centre
H_TOP = 183.0
H_BASE = 11.0
L, W = 50.0, 36.5                   # OSM OBB 52.1 x 38.2 (serrated edges)
YAW = math.radians(90 - 134.9)
STEPS = [(158.0, 0.0), (168.0, 2.5), (176.0, 5.5)]  # (z top, inset)


def plan(inset=0.0, notch=4.0):
    return tk.xform(tk.notch_rect(L - 2 * inset, W - 2 * inset, notch), YAW)


def build():
    base = plan()
    # base: recessed glass arcade under a granite band
    tk.prism("base_glass", plan(1.5), 0.0, H_BASE, "glass")
    tk.glow_ring("base_lit", plan(1.5), 0.8, H_BASE - 1.5, 0.06, "sand_Glow")
    tk.pier_grid("base_piers", tk.offset_poly(base, -0.3), 0.0, H_BASE, 5.0, 1.4, 1.2, "granite",
                 skip_short=3.5)
    tk.ring_band("base_band", base, H_BASE - 1.6, H_BASE, 0.3, "granite")
    z = H_BASE
    for i, (zt, inset) in enumerate(STEPS):
        p = plan(inset)
        tk.punched_block(f"shaft{i}", p, z, zt, 4.1, wall="stone", win="glass", spacing=3.4,
                         gap=1.1, margin=0.9, lit=0.3, seed=1.0 + i, bev=0.2)
        if i:
            tk.ring_band(f"step_cornice{i}", p, z - 0.6, z, 0.35, "trim")
        z = zt
    # crown: dark louvred mechanical band and a flat cap
    top = plan(7.5, notch=3.0)
    tk.prism("crown", top, z, H_TOP - 1.2, "glass")
    tk.pier_grid("crown_louvres", top, z, H_TOP - 1.2, 2.2, 0.4, 0.4, "steel", skip_short=2.5)
    tk.prism("crown_cap", tk.offset_poly(top, 0.4), H_TOP - 1.2, H_TOP, "trim", bev=0.2)
    tk.glow_ring("crown_light", top, z + 0.8, H_TOP - 2.0, 0.5, "white_Glow")
    tk.roof_kit("roof_lo", plan(STEPS[-1][1]), z, seed=3.0, parapet=0.9, plant_frac=0.2, yaw=YAW)
    # Orientation: local +y faces 45 deg = Fremont St (NE, the long entrance face); local +x
    # faces 135 deg = Mission St (SE). The Salesforce cloud goes on the Fremont face,
    # semantically enlarged.
    nx, ny = tk.rot2((0, 1), YAW)
    for k, (dx, w, h, dz) in enumerate(((-3.5, 5.0, 3.6, 0.0), (0.0, 7.0, 5.2, 0.6), (3.6, 4.4, 3.2, 0.2))):
        cx, cy = tk.rot2((dx, W / 2 + 0.5), YAW)
        tk.box(f"cloud_{k}", cx, cy, 24.0 + dz, 24.0 + dz + h, w, 1.0, "sky", yaw=YAW, bev=0.4)
    tk.flat_quad("cloud_glow", tk.rot2((6.2, W / 2 + 1.05), YAW), tk.rot2((-6.2, W / 2 + 1.05), YAW),
                 24.4, 28.8, 0.0, "sky_Glow", (nx, ny))
    tk.plinth("plaza", base, h=0.3, out=3.0)
    p0, p1 = tk.xform([(-L / 2 + 4, W / 2 + 2.2), (L / 2 - 4, W / 2 + 2.2)], YAW)  # Fremont
    tk.tree_row("trees", p0, p1, 0.3, 3, h=6.0, seed=1.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
