"""Deterministic Blender build of the SF-SIM miniature Central Plaza (455 Market Street).

    blender -b --python build_first_and_market_usps.py -- [--out DIR]

Central Plaza, 455 Market Street / 21-29 First Street (Kaplan McLaughlin Diaz,
1987-88): a 23-storey beige stone office tower on First Street between Market
and Stevenson, with a nine-storey wing reaching forward to Market Street. The
tower's corners are cut into sawtooth notches with dark glass corner bays, its
walls are a flat grid of punched windows, and the top storeys step back to a
notched glass crown. The slug keeps the batch list's working name. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "first-and-market-usps"
CENTER = (-122.3984381, 37.7908453)  # OSM way 159280395, OBB centre
H_TOP = 96.9                          # published roof 96.93 m (Wikipedia); LiDAR tower ring majority 96.45 m
H_WING = 36.5                         # LiDAR majority of the Market wing ring (SF3709012), measured
H_BASE = 6.0
H_SHAFT = 88.0
YAW = tk.bearing_to_yaw(135.1)
# OSM footprint about CENTER, split at the DataSF ring boundary into tower (SE) and Market wing (NW)
TOWER = [(-12.7, -12.5), (16.7, -42.0), (42.2, -17.1), (29.5, -4.3), (26.6, -7.1), (12.7, 6.8),
         (7.8, 2.0), (5.0, 4.9)]
WING = [(-42.2, 17.1), (-12.7, -12.5), (5.0, 4.9), (-24.6, 34.5)]


OUTLINE = [(-42.2, 17.1), (-12.7, -12.5), (16.7, -42.0), (42.2, -17.1), (29.5, -4.3), (26.6, -7.1),
           (12.7, 6.8), (7.8, 2.0), (5.0, 4.9), (-24.6, 34.5)]
SE = (0.7071, -0.7071)   # outward normal of the wing's seam face; the tower's seam faces the opposite way


def facing(n, d):
    return n[0] * d[0] + n[1] * d[1] > 0.95


def wing_faces(ei, p0, p1, n):
    return not facing(n, SE)


def tower_low(ei, p0, p1, n):
    """Below the wing roof: skip the seam and the short notch faces."""
    return not facing(n, (-SE[0], -SE[1])) and math.dist(p0, p1) > 7.5


def tower_high(ei, p0, p1, n):
    return math.dist(p0, p1) > 7.5


def build():
    tower = tk.ccw(TOWER)
    wing = tk.ccw(WING)
    # ground floor: dark glass storefront band under a stone fascia, lit lobby
    for nm, pl in (("tower", tower), ("wing", wing)):
        tk.prism(f"{nm}_ground", tk.offset_poly(pl, -0.8), 0.0, H_BASE, "glassd")
        tk.glow_ring(f"{nm}_lobby", tk.offset_poly(pl, -0.8), 0.6, H_BASE - 1.2, 0.05, "sand_Glow")
        tk.pier_grid(f"{nm}_ground_piers", tk.offset_poly(pl, -0.8), 0.0, H_BASE, 6.0, 0.9, 0.8, "sand",
                     skip_short=3.0)
    # Market wing: nine storeys of the same stone grid, roof terrace
    tk.punched_block("wing", wing, H_BASE, H_WING - 1.2, 3.38, wall="sand", win="glassd", spacing=3.6,
                     gap=1.0, margin=0.8, lit=0.3, seed=3.0, bev=0.12, edge_filter=wing_faces)
    tk.ring_band("wing_parapet", tk.offset_poly(wing, -0.4), H_WING - 1.2, H_WING, 0.4, "sand")
    tk.prism("wing_deck", tk.offset_poly(wing, -0.5), H_WING - 1.5, H_WING - 1.1, "roofd")
    tk.hvac_cluster("wing_plant", -26.0, 17.0, H_WING - 1.1, YAW, 12.0, 10.0, seed=1.0, hmax=2.6, fans=False)
    # tower shaft: beige stone grid with punched windows
    tk.punched_block("shaft_low", tower, H_BASE, H_WING, 3.42, wall="sand", win="glassd", spacing=3.6,
                     gap=1.0, margin=0.8, lit=0.3, seed=5.0, bev=0.15, edge_filter=tower_low)
    tk.punched_block("shaft", tower, H_WING, H_SHAFT, 3.79, wall="sand", win="glassd", spacing=3.6,
                     gap=1.0, margin=0.8, lit=0.3, seed=6.0, bev=0.15, edge_filter=tower_high)
    # dark glass corner bays on the short notch faces (the photographed sawtooth corners)
    for k, (p0, p1, L, n) in enumerate(tk.edges(tower)):
        if L < 7.5:
            tk.flat_quad(f"notch_{k}_panes", p0, p1, H_BASE, H_SHAFT, 0.06, "glassd", n)
    # crown: stone parapet ring with a set-back dark glass top
    top = tk.offset_poly(tower, -2.5)
    tk.ring_band("crown_band", tower, H_SHAFT - 0.6, H_SHAFT, 0.3, "stone")
    tk.prism("crown_glass", top, H_SHAFT, H_TOP - 1.4, "glassd", bev=0.1)
    tk.lit_windows("crown_win", top, [(H_SHAFT, H_TOP - 1.4)], 3.3, 0.45, seed=9.0, out=0.08, margin=0.9, gap=0.8)
    tk.ring_band("crown_parapet", tk.offset_poly(top, -0.3), H_TOP - 1.4, H_TOP, 0.4, "sand")
    tk.prism("roof_deck", tk.offset_poly(top, -0.5), H_TOP - 1.7, H_TOP - 1.3, "roofd")
    tk.hvac_cluster("plant", 14.0, -16.0, H_TOP - 1.3, YAW, 18.0, 12.0, seed=4.0, hmax=1.3, fans=False)
    tk.ring_band("roof_terrace", tk.offset_poly(tower, -0.4), H_SHAFT, H_SHAFT + 1.1, 0.4, "sand")
    tk.glow_ring("crown_line", top, H_TOP - 3.2, H_TOP - 2.4, 0.12, "white_Glow")
    tk.plinth("sidewalk", tk.ccw(OUTLINE), h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
