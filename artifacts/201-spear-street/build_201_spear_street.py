"""Deterministic Blender build of the SF-SIM miniature 201 Spear Street.

    blender -b --python build_201_spear_street.py -- [--out DIR]

201 Spear Street at Howard (1986, 18 storeys, offices): a flat-topped
rectangular tower whose whole perimeter is folded into a fine saw-tooth -
every 2.9 m the wall turns out 1.3 m, so each office gets an angled window
bay and the box reads as finely pleated. A screened mechanical penthouse
sits on the roof. No photograph was available: the pleated plan is from the
OSM outline (123 nodes); materials, glazing and penthouse are inferred.
Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "201-spear-street"
CENTER = (-122.3919788, 37.7912423)   # OSM way 288645263, OBB centre
H_TOP = 79.2                           # LiDAR max 79.22 m = penthouse (DataSF 2010, parcel 3741032)
H_ROOF = 72.4                          # LiDAR median / mode 72.4 m = main roof; 18 storeys (assessor)
YAW = tk.bearing_to_yaw(134.4)         # local +x = bearing 134.4 (along Spear, SE), +y = 44.4 (NE)

HX, HY = 27.95, 15.15    # half extents of the outer tooth line (OSM)
DEPTH = 1.3              # tooth depth (OSM)
PITCH = 2.9              # tooth pitch (OSM)
H_LOBBY = 6.0


def sawtooth():
    """CCW pleated outline: on each side the wall runs back DEPTH over ~70 %
    of a tooth, then snaps out again (the OSM pattern)."""
    corners = [(-HX, -HY), (HX, -HY), (HX, HY), (-HX, HY)]
    pts = []
    for k in range(4):
        a, b = corners[k], corners[(k + 1) % 4]
        ln = abs(b[0] - a[0]) + abs(b[1] - a[1])
        ux, uy = (b[0] - a[0]) / ln, (b[1] - a[1]) / ln
        nx, ny = uy, -ux            # outward normal of a CCW side
        n = max(2, int(round(ln / PITCH)))
        step = ln / n
        for i in range(n):
            t0 = i * step
            pts.append((a[0] + ux * t0, a[1] + uy * t0))
            t1 = t0 + step * 0.7
            pts.append((a[0] + ux * t1 - nx * DEPTH, a[1] + uy * t1 - ny * DEPTH))
    return pts


def long_faces(ei, p0, p1, nrm):
    """The long (window) leg of each tooth: odd edges run from the inner point out."""
    return ei % 2 == 0


def build():
    plan = tk.ccw(tk.xform(sawtooth(), YAW))
    tk.prism("shaft", plan, 0.0, H_ROOF, "stone", bev=0.0, bottom=False)
    # lobby: one dark glass band; office storeys: a window on each tooth's long leg
    tk.panes("lobby", plan, [(0.2, H_LOBBY - 0.6)], 1.6, mat="glassd", gap=0.2, margin=0.0,
             edge_filter=long_faces)
    tk.lit_windows("lobby_lit", plan, [(0.2, H_LOBBY - 0.6)], 1.6, 0.8, seed=1.0, out=0.1, margin=0.4,
                   gap=0.3, edge_filter=long_faces)
    bands = tk.floors(H_LOBBY, H_ROOF - 1.4, 7.7)   # storey pairs: per-storey panes would exceed the 5,000 cap
    tk.panes("win", plan, bands, 1.6, mat="glassd", gap=0.25, margin=0.9, edge_filter=long_faces)
    tk.lit_windows("win_lit", plan, bands, 1.6, 0.3, seed=5.0, out=0.1, margin=1.1, gap=0.4,
                   edge_filter=long_faces)
    # roof: parapet line, deck, screened penthouse
    tk.prism("deck", tk.offset_poly(tk.ccw(tk.xform(tk.rect(2 * HX - 3.0, 2 * HY - 3.0), YAW)), 0.0),
             H_ROOF - 0.1, H_ROOF + 0.1, "roofd")
    ph = tk.ccw(tk.xform(tk.rect(22.0, 13.0), YAW))
    tk.prism("penthouse", ph, H_ROOF, H_TOP - 0.3, "stone", bev=0.15)
    tk.prism("penthouse_roof", tk.offset_poly(ph, 0.3), H_TOP - 0.3, H_TOP, "steel")
    tk.panes("louvres", ph, [(H_ROOF + 1.5, H_TOP - 1.5)], 3.0, mat="steel", gap=0.8, margin=0.0)
    c = tk.rot2((19.0, 0.0), YAW)
    tk.hvac_cluster("plant", c[0], c[1], H_ROOF + 0.1, YAW, 8.0, 14.0, seed=3.0, hmax=2.4, fans=True)
    tk.glow_ring("crown_light", ph, H_TOP - 1.2, H_TOP - 0.6, 0.12, "white_Glow")
    tk.plinth("plaza", tk.ccw(tk.xform(tk.rect(2 * HX, 2 * HY), YAW)), h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
