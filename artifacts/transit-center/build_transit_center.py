"""Deterministic Blender build of the SF-SIM miniature Salesforce Transit Center.

    blender -b --python build_transit_center.py -- [--out DIR]

Salesforce Transit Center (Pelli Clarke Pelli, 2018): a 440 m long bus
terminal between Minna and Natoma Streets wrapped in a rippling white
perforated-aluminium skin, with Salesforce Park - a 2.2 ha garden with a
central lawn, a path loop, an amphitheatre and pavilions - on its roof, and
the glass "light column" funnelling daylight down into the Grand Hall.

The footprint is OSM way 542375290 simplified to 64 points; it already
traces the skin's scallops, so lofting it gives the undulating facade for
free. Recognition cues, ranked: the long green roof, the white wavy skin,
the light column. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "transit-center"
CENTER = (-122.3968766, 37.7891071)  # OSM way 542375290, OBB centre
H_TOP = 30.0                         # OSM height 30 m (ESTIMATED; pavilion tops)
H_PARK = 21.3                        # park level ~70 ft above the street (published)
H_SKIN = 23.2                        # skin parapet just above the park
YAW = math.radians(45.3)             # long axis bearing 45.3

# OSM way 542375290, Douglas-Peucker 1.5 m, metres east/north of CENTER
PLAN = [(126.4, 161.3), (130.9, 167.4), (140.5, 167.4), (151.8, 151.3), (168.3, 140.0), (167.3, 131.6),
        (133.6, 99.3), (129.8, 92.0), (98.4, 65.1), (91.9, 54.3), (80.7, 48.0), (74.0, 36.0), (61.7, 27.6),
        (54.1, 16.0), (42.1, 7.7), (34.5, -4.1), (22.9, -12.1), (16.6, -22.5), (5.1, -29.9), (-2.3, -40.9),
        (-13.1, -48.1), (-20.3, -58.9), (-31.6, -66.3), (-39.0, -77.4), (-52.5, -87.5), (-57.0, -95.2),
        (-69.5, -103.5), (-77.0, -114.6), (-87.4, -121.0), (-93.9, -131.6), (-108.2, -140.5),
        (-133.6, -166.6), (-141.2, -164.6), (-146.6, -155.9), (-149.5, -158.9), (-160.4, -148.3),
        (-157.3, -145.2), (-167.8, -136.6), (-166.6, -128.6), (-137.0, -100.4), (-133.1, -93.8),
        (-122.0, -86.3), (-114.7, -75.1), (-104.0, -67.6), (-96.7, -56.7), (-85.2, -49.5), (-77.8, -38.2),
        (-67.3, -32.4), (-59.6, -20.5), (-48.4, -13.5), (-40.9, -2.4), (-29.5, 5.2), (-22.4, 15.6),
        (-11.4, 22.3), (-4.0, 34.0), (8.2, 40.6), (16.4, 54.2), (27.8, 61.6), (35.6, 73.7), (48.3, 81.5),
        (53.6, 91.9), (64.9, 99.6), (91.9, 129.0), (102.3, 136.0)]


def A(u, v):
    """Point at u metres along the building's long axis (NE +), v across (NW +)."""
    return tk.rot2((u, v), YAW)


def build():
    p = tk.ccw(PLAN)
    # glazed street level and the bus-deck body behind the skin
    tk.prism("street_glass", tk.offset_poly(p, -3.5), 0.0, 6.0, "glassl")
    tk.glow_ring("street_lit", tk.offset_poly(p, -3.5), 0.8, 5.2, 0.06, "sand_Glow")
    tk.prism("body", tk.offset_poly(p, -2.6), 6.0, H_PARK - 0.6, "glassd", top=False)
    # the rippling white skin: a thin wall on the scalloped outline, lifted off the street
    tk.ring_band("skin", p, 4.5, H_SKIN, 0.0, "white", inset=-0.7)
    # perforation read as rows of pale slots, lit cool at night (the skin glows)
    tk.panes("skin_slots", p, [(7.0, 9.0), (12.0, 14.0), (17.0, 19.0)], 6.0, mat="steel", gap=2.2,
             margin=0.0, out=0.04)
    tk.lit_windows("skin_light", p, [(6.5, 20.5)], 6.0, 0.7, seed=3.0, out=0.1, margin=0.0,
                   mat="white_Glow", gap=0.8)
    # Salesforce Park: lawn deck, path loop, tree rows
    deck = tk.offset_poly(p, -0.8)
    tk.prism("park_soil", deck, H_PARK - 0.6, H_PARK, "leaf", bottom=True)
    # lawns: a few oval greens set into darker planting, not one carpet
    for k, (u, a_, b_) in enumerate(((-55.0, 26.0, 9.0), (20.0, 30.0, 10.0), (110.0, 22.0, 8.0))):
        tk.prism(f"lawn_{k}", tk.xform(tk.ellipse(a_, b_, 14), YAW, *A(u, 0.0)), H_PARK, H_PARK + 0.25, "mint")
    # the path loop: a meandering walk down each side, as short chunky segments
    for side in (-1, 1):
        pts = [A(u, side * (12.5 + 3.0 * math.sin(u / 22.0 + side))) for u in range(-175, 176, 14)]
        for k in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[k], pts[k + 1]
            L = math.hypot(x1 - x0, y1 - y0)
            tk.box(f"path_{side}_{k}", (x0 + x1) / 2, (y0 + y1) / 2, H_PARK, H_PARK + 0.3, L + 0.8, 3.0,
                   "stone", yaw=math.atan2(y1 - y0, x1 - x0))
        tk.tree_row(f"trees_{side}", A(-180, side * 19.0), A(180, side * 19.0), H_PARK, 22,
                    h=6.5, r=2.3, seed=1.0 + side)
    # tree clumps in the planting beds between the lawns
    for k, u in enumerate((-135.0, -15.0, 60.0, 135.0)):
        for j, (du, dv) in enumerate(((0, 0), (5, 4), (-4, 5), (3, -5))):
            x, y = A(u + du, dv)
            tk.tree(f"clump_{k}_{j}", x, y, H_PARK, h=5.5 + j % 2, r=2.2, mat="leaf" if j % 2 else "leafd")
    # the light column: a glass oculus ringed in white over the Grand Hall
    oc = A(-20.0, 0.0)
    ell = tk.xform(tk.ellipse(14.0, 8.0, 16), YAW, *oc)
    tk.ring_band("oculus_rim", ell, H_PARK, H_PARK + 1.0, 1.2, "white")
    tk.prism("oculus_glass", tk.offset_poly(ell, -0.2), H_PARK - 0.2, H_PARK + 0.6, "glassl")
    tk.glow_cap("oculus_light", tk.offset_poly(ell, -0.4), H_PARK + 0.62, "white_Glow")
    # amphitheatre: stepped half-ellipse terraces near the west end
    am = A(-110.0, 0.0)
    for k in range(4):
        e = tk.xform([(x, y) for x, y in tk.ellipse(16.0 - 3 * k, 9.0 - 1.8 * k, 12) if y <= 0.01], YAW, *am)
        tk.prism(f"amphi_{k}", e, H_PARK, H_PARK + 0.5 * (k + 1), "stone")
    # pavilions: the cafe and the gondola head house (the park's tallest objects)
    cafe = A(75.0, 0.0)
    tk.box("cafe", cafe[0], cafe[1], H_PARK, H_PARK + 4.5, 18.0, 9.0, "glassl", yaw=YAW)
    tk.box("cafe_roof", cafe[0], cafe[1], H_PARK + 4.5, H_PARK + 5.3, 21.0, 11.0, "white", yaw=YAW, bev=0.2)
    tk.glow_ring("cafe_lit", tk.xform(tk.rect(18.0, 9.0), YAW, *cafe), H_PARK + 0.6, H_PARK + 4.0, 0.06, "sand_Glow")
    g = A(150.0, 0.0)
    tk.box("gondola_house", g[0], g[1], H_PARK, H_TOP - 1.0, 10.0, 8.0, "glassl", yaw=YAW)
    tk.box("gondola_roof", g[0], g[1], H_TOP - 1.0, H_TOP, 12.0, 10.0, "white", yaw=YAW, bev=0.2)
    tk.plinth("sidewalk", p, h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
