"""Deterministic Blender build of the SF-SIM miniature 345 California Center.

    blender -b --python build_345_california_street.py -- [--out DIR]

345 California Center (SOM, 1986): a 48-storey mid-block tower of grey granite
punched by square windows. Its top 11 floors are a hotel in two towers set at
45 degrees to the slab, joined by a stack of glazed skybridge floors, and each
topped by a square concrete shaft that steps thinner - the "Tweezer Towers".
Recognition cues: the twin shafts and the split, rotated top. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "345-california-street"
CENTER = (-122.4004566, 37.7925878)   # OSM way 588355355, OBB centre
H_TOP = 211.8                          # published architectural top (695 ft, spire tips); LiDAR 212
H_HOTEL_ROOF = 189.0                   # published roof (620 ft)
H_OFFICE = 154.0                       # INFERRED: top of the office slab under the 11 hotel floors
H_BASE = 20.0                          # INFERRED: street-wall podium (lobby + retail floors 2-3)
YAW = tk.bearing_to_yaw(81.2)          # local +x = bearing 81.2 (California St), +y = 351.2

TURRET_X = 17.0                        # INFERRED: hotel tower centres +/- along the slab (photo)
TURRET = 22.0                          # INFERRED: hotel tower side (photo)
SPIRE_X = 6.0                          # INFERRED: the two concrete shafts flank the glass core (photo)
H_SPIRE_STEP = 199.0                   # INFERRED: shafts step thinner about halfway up (photo)


def build():
    site = tk.xform(tk.rect(84.6, 41.4), YAW)
    slab = tk.xform(tk.chamfer_rect(66.0, 36.0, 6.0), YAW)
    # podium on the full mid-block footprint
    tk.punched_block("podium", site, 0.0, H_BASE, 10.0, wall="concrete", win="glassd", spacing=6.0,
                     gap=1.2, margin=0.8, lit=0.5, seed=1.0)
    tk.prism("podium_deck", tk.offset_poly(site, -0.4), H_BASE - 0.3, H_BASE + 0.05, "roofd")
    tk.ring_band("podium_parapet", tk.offset_poly(site, -0.6), H_BASE, H_BASE + 0.9, 0.6, "concrete")
    # office slab: grey granite punched by square windows, 32 storeys
    tk.prism("slab", slab, H_BASE, H_OFFICE, "concrete", bev=0.3)
    rows = tk.floors(H_BASE, H_OFFICE, 4.1875)
    wins = [(z0 + 1.2, z1 - 0.9) for z0, z1 in rows]
    tk.panes("slab", slab, wins, 5.2, mat="glassd", out=0.08, margin=0.0, gap=3.0)
    pairs = tk.floors(H_BASE, H_OFFICE, 8.375)
    tk.lit_windows("slab_win", slab, pairs, 9.0, 0.3, seed=5.0, out=0.14, margin=1.6, gap=2.6)
    tk.prism("slab_roof", tk.offset_poly(slab, -0.4), H_OFFICE - 0.2, H_OFFICE + 0.6, "roofd")
    tk.ring_band("slab_parapet", tk.offset_poly(slab, -0.4), H_OFFICE, H_OFFICE + 1.2, 0.4, "concrete")
    # the twin hotel towers, turned 45 degrees, with a glass core between them
    for k, sx in enumerate((-1, 1)):
        cx, cy = tk.rot2((sx * TURRET_X, 0.0), YAW)
        t = tk.xform(tk.rect(TURRET, TURRET), YAW + math.radians(45), cx, cy)
        tk.prism(f"turret{k}", t, H_OFFICE, H_HOTEL_ROOF, "concrete", bev=0.3)
        hb = [(z0 + 0.9, z1 - 0.8) for z0, z1 in tk.floors(H_OFFICE + 1.2, H_HOTEL_ROOF - 1.0, 3.2)]
        tk.panes(f"turret{k}", t, hb, 4.4, mat="glassd", out=0.08, margin=0.0, gap=2.4)
        tk.lit_windows(f"turret{k}_win", t, hb, 4.4, 0.45, seed=20.0 + k, out=0.14, margin=0.1, gap=2.6)
        tk.prism(f"turret{k}_deck", tk.offset_poly(t, -0.4), H_HOTEL_ROOF - 0.3, H_HOTEL_ROOF + 0.1, "roofd")
        tk.ring_band(f"turret{k}_parapet", tk.offset_poly(t, -0.4), H_HOTEL_ROOF - 0.2, H_HOTEL_ROOF + 1.0, 0.4,
                     "concrete")
        tk.glow_ring(f"turret{k}_crown", t, H_HOTEL_ROOF - 2.4, H_HOTEL_ROOF - 1.6, 0.3, "white_Glow")
        # the tweezer: a square concrete shaft rising from the inner corner, stepping thinner
        px, py = tk.rot2((sx * SPIRE_X, 0.0), YAW)
        tk.box(f"spire{k}_lo", px, py, H_HOTEL_ROOF - 0.5, H_SPIRE_STEP, 4.2, 4.2, "concrete", yaw=YAW, bev=0.1)
        tk.box(f"spire{k}_hi", px, py, H_SPIRE_STEP, H_TOP - 0.6, 2.6, 2.6, "concrete", yaw=YAW, bev=0.1)
        tk.box(f"spire{k}_tip_glow", px, py, H_TOP - 0.6, H_TOP, 1.6, 1.6, "red_Glow", yaw=YAW)
        pc = tk.rot2((sx * (TURRET_X + 3.0), 0.0), YAW)
        tk.hvac_cluster(f"plant{k}", pc[0], pc[1], H_HOTEL_ROOF + 0.1, YAW + math.radians(45), 9.0, 9.0,
                        seed=3.0 + k, hmax=2.5)
    # glass core between the towers: stacked glazed floors (the skybridges)
    tk.box("core_glass", 0.0, 0.0, H_OFFICE + 1.2, H_HOTEL_ROOF - 3.0, 10.0, 8.0, "glassl", yaw=YAW, bev=0.1)
    tk.box("core_base", 0.0, 0.0, H_OFFICE + 0.6, H_OFFICE + 6.0, 14.0, 10.0, "glassd", yaw=YAW, bev=0.1)
    for sy in (-1, 1):
        a, b = tk.xform([(-4.6 * sy, 4.06 * sy), (4.6 * sy, 4.06 * sy)], YAW)
        nx, ny = tk.rot2((0.0, sy), YAW)
        tk.flat_quad(f"core_lit{sy + 1}_glow", a, b, H_OFFICE + 7.0, H_HOTEL_ROOF - 4.0, 0.0, "sand_Glow",
                     (nx, ny))
    tk.plinth("plaza", site, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
