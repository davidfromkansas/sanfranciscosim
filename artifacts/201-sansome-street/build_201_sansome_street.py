"""Deterministic Blender build of the SF-SIM miniature Royal Insurance Building.

    blender -b --python build_201_sansome_street.py -- [--out DIR]

201 Sansome Street at Pine (Howells & Stokes, 1907; SF Landmark #160): an
eleven-storey office block, now condominiums. A three-storey white marble
base with the Royal coat of arms (lion, unicorn and clock) over the Sansome
entrance, a shaft of dark red-brown brick with white-trimmed paired windows,
and a white terracotta top of two storeys with cartouches under a deep
cornice. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "201-sansome-street"
CENTER = (-122.4012685, 37.7922612)   # OSM way 256067738, OBB centre
H_TOP = 41.3                           # LiDAR median roof (DataSF 2010, parcel 0260017); OSM 41
YAW = tk.bearing_to_yaw(81.5)          # local +x = bearing 81.5 (street grid), +y = 351.5

# OSM outline in local metres: L-shape with a light court notch at the NW
# (inner) corner. East face = Sansome St, south face = Pine St.
LOCAL = [(-13.85, -10.3), (13.8, -10.3), (13.8, 10.25), (2.2, 10.25), (2.2, 4.75), (-13.85, 4.75)]
H_BASE = 12.6      # three marble storeys
H_SHAFT = 32.4     # brick storeys 4-9
H_CORN = 39.6      # white top storeys 10-11, then cornice to the crest


def street(ei, p0, p1, nrm):
    """Only the two street faces (east = Sansome, south = Pine)."""
    lx, ly = tk.rot2(nrm, -YAW)
    return lx > 0.7 or ly < -0.7


def build():
    plan = tk.ccw(tk.xform(LOCAL, YAW))
    # marble base with tall ground-floor openings
    tk.prism("base", plan, 0.0, H_BASE, "stone", bev=0.15)
    tk.panes("base_win", plan, [(0.0, 5.6), (5.6, 9.1), (9.1, H_BASE)], 3.0, mat="glassd", gap=1.1, margin=0.7)
    tk.lit_windows("base_lit", plan, [(0.0, 5.6)], 3.0, 0.8, seed=2.0, out=0.1, margin=0.9, gap=1.3,
                   edge_filter=street)
    tk.cornice("base_cornice", plan, H_BASE, h=0.8, out=0.45, mat="cream")
    # brick shaft with paired windows
    tk.punched_block("shaft", plan, H_BASE + 0.8, H_SHAFT, 3.27, wall="rust", win="glassd", spacing=2.55,
                     gap=1.0, margin=0.8, lit=0.32, seed=5.0, bev=0.12)
    # white quoin piers at the street corner and the far ends of the street faces
    for i, (x, y) in enumerate([(13.8, -10.3), (-13.85, -10.3), (13.8, 10.25)]):
        c = tk.rot2((x, y), YAW)
        tk.box(f"quoin_{i}", c[0], c[1], H_BASE + 0.8, H_SHAFT, 1.6, 1.6, "cream", yaw=YAW, bev=0.1)
    # white terracotta top: band, two storeys with cartouches, deep cornice
    tk.ring_band("top_band", plan, H_SHAFT, H_SHAFT + 0.7, 0.35, "cream")
    tk.punched_block("top", plan, H_SHAFT + 0.7, H_CORN, 3.45, wall="cream", win="glassd", spacing=2.55,
                     gap=1.0, margin=0.8, lit=0.3, seed=8.0, bev=0.12)
    tk.cornice("cornice", plan, H_CORN, h=1.1, out=1.0, mat="cream")
    tk.prism("roof", tk.offset_poly(plan, -0.3), H_CORN + 1.1, H_TOP - 0.25, "roofd")
    tk.ring_band("parapet", tk.offset_poly(plan, 0.2), H_CORN + 1.1, H_TOP, 0.35, "cream")
    # coat of arms over the Sansome entrance (east face, near the Pine corner)
    for k, (x, y, w, h) in enumerate([(14.0, -4.5, 3.8, 3.6), (14.0, 4.0, 2.4, 2.4)][:1]):
        c = tk.rot2((x + 0.25, y), YAW)
        tk.box(f"arms_{k}", c[0], c[1], H_BASE - 4.2, H_BASE - 4.2 + h, 0.5, w, "cream", yaw=YAW, bev=0.1)
    c = tk.rot2((14.55, -4.5), YAW)
    tk.cylinder("clock", c[0], c[1], H_BASE - 2.6, H_BASE - 1.6, 0.6, "gold", seg=8)
    # cartouches on the top storeys of the street faces
    for i, (x, y) in enumerate([(14.05, -6.0), (14.05, 6.0), (-8.0, -10.55), (0.0, -10.55), (8.0, -10.55)]):
        c = tk.rot2((x, y), YAW)
        sx, sy = (0.5, 1.4) if abs(x) > 13 else (1.4, 0.5)
        tk.box(f"cartouche_{i}", c[0], c[1], H_SHAFT + 1.4, H_SHAFT + 3.4, sx, sy, "stone", yaw=YAW, bev=0.1)
    pc = tk.rot2((6.0, -2.0), YAW)
    tk.hvac_cluster("plant", pc[0], pc[1], H_CORN + 1.1, YAW, 10.0, 8.0, seed=3.0, hmax=0.55, fans=False)
    tk.glow_ring("crown_light", plan, H_CORN - 0.6, H_CORN - 0.1, 0.12, "white_Glow")
    tk.plinth("plaza", plan, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
