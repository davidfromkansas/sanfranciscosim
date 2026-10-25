"""Deterministic Blender build of the SF-SIM miniature 60 Spear Street.

    blender -b --python build_60_spear.py -- [--out DIR]

60 Spear ("The Spear"): a 13-storey office block at Spear and Mission,
square to the street grid, crowned by a set-back glazed top floor. Massing
and height are measured (OSM way 32863010; DataSF LiDAR crest 57.93 m, roof
plane 55.4 m); the stone-grid facade with a glass top is INFERRED - no usable
photo was available in this pass (see REFERENCE.md).
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "60-spear"
CENTER = (-122.394585, 37.792566)   # OSM way 32863010, OBB centre
H_TOP = 57.9                         # DataSF LiDAR crest 57.93 m (measured)
H_ROOF = 55.4                        # LiDAR majority roof plane 55.38 m
H_BASE = 6.0
L, W = 39.5, 31.0                   # OSM OBB 40.4 x 31.6
YAW = math.radians(90 - 134.8)


def build():
    p = tk.xform(tk.rect(L, W), YAW)
    tk.prism("base", tk.offset_poly(p, -1.5), 0.0, H_BASE, "glass")
    tk.glow_ring("base_lit", tk.offset_poly(p, -1.5), 0.6, H_BASE - 1.0, 0.06, "sand_Glow")
    tk.pier_grid("base_piers", tk.offset_poly(p, -0.3), 0.0, H_BASE, 4.0, 1.1, 1.1, "stone")
    tk.shaft("shaft", p, H_BASE, H_ROOF - 4.2, (H_ROOF - 4.2 - H_BASE) / 11,  # whole storeys: no sliver band
             glass="glass", band="stone", band_h=1.3,
             band_out=0.3, fins=(4.0, 0.9, 0.45, "stone"), lit=0.3, seed=8.1, lit_spacing=4.0)
    # set-back glass top storey with a terrace ring
    top = tk.offset_poly(p, -2.2)
    tk.prism("terrace", tk.offset_poly(p, 0.3), H_ROOF - 4.2, H_ROOF - 3.6, "stone", bev=0.15)
    tk.prism("top_glass", top, H_ROOF - 3.6, H_ROOF, "glassl")
    tk.glow_ring("top_lit", top, H_ROOF - 3.2, H_ROOF - 0.6, 0.06, "sand_Glow")
    tk.prism("top_roof", tk.offset_poly(top, 0.3), H_ROOF, H_ROOF + 0.3, "roofd")
    tk.ring_band("top_parapet", tk.offset_poly(top, -0.2), H_ROOF, H_ROOF + 0.9, 0.5, "trim")
    tk.hvac_cluster("plant", 0, 0, H_ROOF + 0.3, YAW, L * 0.5, W * 0.45, seed=2.0, hmax=H_TOP - H_ROOF - 0.3)
    for k, (a, b) in enumerate(((-L / 2 + 1.2, -W / 2 + 1.2), (L / 2 - 1.2, W / 2 - 1.2))):
        c = tk.rot2((a, b), YAW)
        tk.tree(f"terrace_tree_{k}", c[0], c[1], H_ROOF - 3.6, h=3.0, r=1.3)
    tk.plinth("plaza", p, h=0.3, out=3.0)
    # street trees on the Spear St (NE, local +y) sidewalk
    p0, p1 = tk.xform([(-L / 2 + 4, W / 2 + 2.2), (L / 2 - 4, W / 2 + 2.2)], YAW)
    tk.tree_row("trees", p0, p1, 0.3, 3, h=6.0, seed=1.1)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
