"""Deterministic Blender build of the SF-SIM miniature 50 Beale Street.

    blender -b --python build_50_beale.py -- [--out DIR]

50 Beale (SOM, 1967), the former Bechtel / Blue Shield building: a long
23-storey slab of dark bronze glass in a deep black-anodised grid. The
recognition cue is the colour - the darkest box on the block - and the
heavy, regular grid. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "50-beale"
CENTER = (-122.396486, 37.791257)   # OSM way 256065251, OBB centre
H_TOP = 100.0                        # 328 ft
H_ROOF = 93.0
H_BASE = 7.5
L, W = 70.0, 38.0                   # OSM OBB 71.5 x 39.1
YAW = math.radians(90 - 134.8)


def build():
    plan = tk.xform(tk.rect(L, W), YAW)
    tk.prism("base_glass", tk.offset_poly(plan, -3.0), 0.0, H_BASE, "glassd")
    tk.glow_ring("base_lit", tk.offset_poly(plan, -3.0), 0.8, H_BASE - 1.2, 0.06, "sand_Glow")
    tk.pier_grid("colonnade", tk.offset_poly(plan, -0.7), 0.0, H_BASE, 6.5, 1.3, 1.3, "ink")
    tk.shaft("shaft", plan, H_BASE, H_ROOF, 3.9, glass="bronze", band="ink", band_h=1.2, band_out=0.25,
             fins=(3.3, 0.5, 0.45, "ink"), lit=0.3, seed=6.0, lit_spacing=3.3)
    pent = tk.offset_poly(plan, -4.0)
    tk.prism("penthouse", pent, H_ROOF, H_TOP - 4.0, "ink")
    tk.pier_grid("louvres", pent, H_ROOF, H_TOP - 4.0, 1.8, 0.3, 0.3, "roofd")
    tk.prism("roof_cap", tk.offset_poly(pent, 0.3), H_TOP - 4.0, H_TOP - 3.4, "roofd", bev=0.15)
    tk.hvac_cluster("cap_plant", 0, 0, H_TOP - 3.4, YAW, L * 0.6, W * 0.45, seed=3.0, hmax=3.4)
    tk.prism("roof_deck", plan, H_ROOF - 0.2, H_ROOF + 0.2, "roofd")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.5), H_ROOF, H_ROOF + 1.0, 0.5, "ink")
    # Beale Street plaza: the famous mature trees by the entrance
    tk.plinth("plaza", plan, h=0.3, out=5.0)
    p0, p1 = tk.xform([(-L / 2 + 4, W / 2 + 3.5), (L / 2 - 4, W / 2 + 3.5)], YAW)  # Beale St (NE) face
    tk.tree_row("trees", p0, p1, 0.3, 5, h=7.5, r=3.0, seed=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
