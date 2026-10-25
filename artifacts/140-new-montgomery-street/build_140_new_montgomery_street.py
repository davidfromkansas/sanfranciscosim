"""Deterministic Blender build of the SF-SIM miniature 140 New Montgomery (Pacific Telephone Building).

    blender -b --python build_140_new_montgomery_street.py -- [--out DIR]

140 New Montgomery Street (Miller & Pflueger, 1925): San Francisco's first
skyscraper south of Market, a 26-storey Art Deco tower of mottled pale grey
terracotta on an L-shaped plan. Unbroken vertical piers run the full height; the shaft
steps in twice, after Saarinen's Tribune Tower entry, to a parapet of pinnacles,
and a small central lantern carries the flagpole. Recognition cues: the pale
ribbed verticality, the stepped shoulders and the lantern. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "140-new-montgomery-street"
CENTER = (-122.4000285, 37.7866218)  # OSM way 80296766, OBB centre
H_TOP = 132.7                         # published architectural top 132.7 m (roof 132.6; tip 140.2 not modelled)
H_STEP1 = 66.0                        # first setback (inferred from the photo)
H_STEP2 = 91.0                        # second setback (inferred from the photo)
H_MAIN = 116.0                        # main roof: DataSF LiDAR majority plane 116.07 m (measured)
YAW = math.radians(90 - 134.7)        # local +x along New Montgomery (bearing 134.7)
# OSM way 80296766 simplified to its L (the small light-court notches dropped)
PTS = [(13.72, -18.45), (19.9, -14.48), (33.13, -1.28), (-1.43, 32.9), (-33.13, 1.28), (-22.71, -9.02),
       (-0.39, 13.24)]


def section(name, poly, z0, z1, groups, seed, cap=True):
    """Pale piers over dark recessed spandrels; lit panes cut per storey (two per group)."""
    pitch = (z1 - z0) / groups
    tk.shaft(name, poly, z0, z1, pitch, glass="glassd", band="stone", band_h=0.8, band_out=-0.05,
             fins=(3.6, 1.1, 0.5, "white"), lit=0.0)
    tk.lit_windows(name + "_win", tk.offset_poly(poly, -0.2),
                   [b for za, zb in tk.floors(z0, z1, pitch)
                    for b in ((za + 0.8, (za + zb + 0.8) / 2), ((za + zb + 0.8) / 2, zb))],
                   3.6, 0.27, seed=seed, out=0.6, margin=0.35, gap=1.6)
    if cap:
        tk.ring_band(name + "_cap", poly, z1, z1 + 0.8, 0.6, "white")
        tk.prism(name + "_roof", tk.offset_poly(poly, -0.4), z1 - 0.2, z1 + 0.1, "roofd")


def build():
    plan = tk.ccw(PTS)
    # base: tall storeys of dark shopfront/lobby glass in pale stone
    tk.prism("base", plan, 0.0, 10.0, "stone", bev=0.15)
    tk.panes("base_glass", plan, [(0.4, 8.6)], 4.2, mat="glassd", gap=1.4, margin=0.0)
    tk.lit_windows("base_lit", plan, [(0.4, 8.0)], 4.2, 0.85, seed=1.0, out=0.1, margin=0.3, gap=1.8)
    tk.ring_band("base_band", plan, 10.0, 11.0, 0.35, "stone")
    # the shaft steps in twice (photo: at about 66 m and 91 m) up to the main parapet
    section("shaft", plan, 11.0, H_STEP1, 7, 4.0)
    mid = tk.offset_poly(plan, -3.0)
    section("upper", mid, H_STEP1 + 0.8, H_STEP2, 3, 6.0)
    top = tk.offset_poly(plan, -4.8)
    section("top", top, H_STEP2 + 0.8, H_MAIN, 3, 8.0, cap=False)
    # parapet of pinnacles round the main roof
    tk.ring_band("parapet", tk.offset_poly(top, -0.5), H_MAIN, H_MAIN + 1.6, 0.7, "white")
    tk.prism("main_roof", tk.offset_poly(top, -0.4), H_MAIN - 0.2, H_MAIN + 0.1, "roofd")
    for k, (p0, p1, Le, nrm) in enumerate(tk.edges(top)):
        n = max(1, int(Le // 7.0))
        for i in range(n + 1):
            t = i / n
            x = p0[0] + (p1[0] - p0[0]) * t + nrm[0] * 0.2
            y = p0[1] + (p1[1] - p0[1]) * t + nrm[1] * 0.2
            tk.box(f"pinnacle_{k}_{i}", x, y, H_MAIN + 1.6, H_MAIN + 3.4, 1.1, 1.1, "white", yaw=YAW)
    # the central lantern over the New Montgomery arm (flagpole to 140.2 m not modelled)
    c = ((PTS[2][0] + PTS[3][0]) / 2 - 0.7071 * 6.5, (PTS[2][1] + PTS[3][1]) / 2 - 0.7071 * 6.5)
    lan = tk.xform(tk.rect(9.0, 8.0), YAW, *c)
    section("lantern", lan, H_MAIN + 0.1, H_TOP - 2.0, 2, 9.0, cap=False)
    tk.ring_band("lantern_crown", tk.offset_poly(lan, -0.3), H_TOP - 2.0, H_TOP, 0.8, "white")
    tk.prism("lantern_roof", tk.offset_poly(lan, -0.2), H_TOP - 2.2, H_TOP - 1.9, "roofd")
    tk.glow_ring("lantern_light", lan, H_TOP - 4.0, H_TOP - 3.0, 0.7, "white_Glow")
    c2 = tk.rot2((-14.0, -10.0), YAW)
    tk.hvac_cluster("roof_plant", c[0] + c2[0], c[1] + c2[1], H_MAIN + 0.1, YAW, 8.0, 6.0, seed=2.0, hmax=2.6)
    tk.plinth("sidewalk", plan, h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
