"""Deterministic Blender build of the SF-SIM miniature 222 Second Street (LinkedIn).

    blender -b --python build_222_2nd_street.py -- [--out DIR]

222 Second Street (Thomas Phifer / Gensler, 2016): a 26-storey dark-glass office
tower at the south corner of Second and Howard. John King: "a form that begins
as a squat 16-story rectangle and concludes as a 10-story square", skinned in
overlapping 6 x 13 ft shingled glass panes; a four-storey glass base whose
shingles fan the other way. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "222-2nd-street"
CENTER = (-122.3982516, 37.786315)   # OSM way 80296717, OBB centre
H_ROOF = 106.7                        # roof 350 ft (published)
H_TOP = 112.8                         # architectural top 370 ft (published): roof screen
H_BASE = 16.4                         # 4 storeys
H_LOW = 65.6                          # 16 storeys
YAW = math.radians(90 - 135.0)        # local +x = bearing 135 (SE), +y = 45 (NE, Second St)

# OSM footprint in the local frame: a 49.8 x 47 m rectangle with a 22.7 x 5.8 m
# notch at the south (+x, -y) corner
LOCAL = [(-24.9, -23.5), (2.1, -23.5), (2.1, -17.7), (24.9, -17.7), (24.9, 23.5), (-24.9, 23.5)]
# upper 10-storey square, flush with the Second St (NE) and SE faces, set back from Howard (NW): inferred
UPPER = tk.rect(36.0, 36.0, 24.9 - 18.0, 23.5 - 18.0)


def build():
    plan = tk.xform(LOCAL, YAW)
    up = tk.xform(UPPER, YAW)
    # glass base: dark lobby glass with a lit ring and close fins (the fanned shingles)
    tk.prism("base_glass", tk.offset_poly(plan, -0.8), 0.0, H_BASE, "glassd")
    tk.glow_ring("base_lit", tk.offset_poly(plan, -0.8), 0.6, 5.0, 0.06, "sand_Glow")
    tk.pier_grid("base_fins", tk.offset_poly(plan, -0.8), 0.0, H_BASE, 3.7, 0.2, 0.5, "glass")
    tk.ring_band("base_band", plan, H_BASE, H_BASE + 0.8, 0.15, "glassl")
    # lower block 16 storeys: 12 above the base, shingled glass = banded loft + fins
    tk.shaft("low", plan, H_BASE + 0.8, H_LOW, (H_LOW - H_BASE - 0.8) / 12, glass="glassd", band="glass",
             band_h=0.5, band_out=0.25, fins=(3.7, 0.15, 0.3, "glassl"), lit=0.28, seed=2.0, lit_spacing=3.7)
    tk.prism("low_roof", tk.offset_poly(plan, -0.3), H_LOW - 0.3, H_LOW + 0.1, "roofd")
    tk.ring_band("low_parapet", tk.offset_poly(plan, -0.5), H_LOW, H_LOW + 1.1, 0.45, "glassd")
    # terrace planting on the setback (Howard side)
    c = tk.rot2((-24.9 + 7.0, 0.0), YAW)
    tk.hvac_cluster("low_plant", c[0], c[1], H_LOW + 0.1, YAW, 8.0, 30.0, seed=3.0, hmax=2.5, fans=False)
    # upper square: 10 storeys
    tk.shaft("up", up, H_LOW, H_ROOF, (H_ROOF - H_LOW) / 10, glass="glassd", band="glass", band_h=0.5,
             band_out=0.25, fins=(3.6, 0.15, 0.3, "glassl"), lit=0.3, seed=5.0, lit_spacing=3.6)
    # glass roof screen to the architectural top, around a deck and plant
    tk.prism("roof_deck", tk.offset_poly(up, -0.4), H_ROOF - 0.3, H_ROOF + 0.05, "roofd")
    tk.ring_band("screen", tk.offset_poly(up, -0.6), H_ROOF, H_TOP, 0.6, "glassd")
    ux, uy = tk.rot2((24.9 - 18.0, 23.5 - 18.0), YAW)
    tk.hvac_cluster("roof_plant", ux, uy, H_ROOF + 0.05, YAW, 22.0, 20.0, seed=7.0, hmax=4.5)
    tk.glow_ring("crown_light", up, H_TOP - 1.2, H_TOP - 0.4, 0.42, "white_Glow")
    # LinkedIn "in" sign at the Second x Howard corner (north, local -x +y), base top
    nx, ny = tk.rot2((0, 1), YAW)
    a, b = tk.xform([(-24.0, 23.5), (-20.4, 23.5)], YAW)
    tk.flat_quad("sign", a, b, H_BASE - 4.0, H_BASE - 0.4, 0.62, "sky", (nx, ny))
    tk.flat_quad("sign_glow", a, b, H_BASE - 3.8, H_BASE - 0.6, 0.68, "sky_Glow", (nx, ny))
    tk.plinth("plaza", plan, h=0.3, out=3.0)
    p0, p1 = tk.xform([(-22.0, 26.0), (22.0, 26.0)], YAW)
    tk.tree_row("trees", p0, p1, 0.3, 4, h=6.0, seed=1.7)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
