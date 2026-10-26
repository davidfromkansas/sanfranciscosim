"""Deterministic Blender build of the SF-SIM miniature Park Tower at Transbay.

    blender -b --python build_park_tower.py -- [--out DIR]

250 Howard Street (Goettsch Partners / SCB, 2018): a 43-storey blue-glass
office tower on a low podium beside Salesforce Park. Recognition cues: the
crisp blue prism, the stacks of open-air terraces carved out of its east and
west corners (the street grid's "SE" and "NW" corners) in the upper third, and a glass screen crown that carries the silhouette to
183 m above the 168 m roof. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "park-tower"
CENTER = (-122.394279, 37.790436)   # OSM way 611390934, OBB centre
H_TOP = 183.0                        # architectural (605 ft)
H_ROOF = 168.0                       # roof (550 ft)
H_POD = 17.0
H_NOTCH = 116.0                      # terrace stacks start here (photo: ~2/3 up)
W, D = 44.0, 35.0
PW, PD = 54.0, 50.0                  # podium (OSM OBB 56.7 x 54.9)
YAW = math.radians(45.0)
NOTCH = 11.0                         # terrace bay size carved from each corner
# Local +X runs along Howard St (bearing 45). With YAW = 45 deg the local
# (+X, -Y) corner is true EAST (Howard x Main side) and (-X, +Y) is true WEST.
# The Commons photo (taken from across Howard, looking NW at the Howard face)
# shows the terrace stack on the right-hand (east) corner and the far-left
# (west) corner cut back; Wikipedia: terraces "on both the northwest and
# southeast corners" (grid directions).
CORNERS = ((1, -1), (-1, 1))


def P(poly):
    return tk.xform(poly, YAW)


def notched():
    hw, hd, n = W / 2, D / 2, NOTCH
    return [(-hw, -hd), (hw - n, -hd), (hw - n, -hd + n), (hw, -hd + n), (hw, hd),
            (-hw + n, hd), (-hw + n, hd - n), (-hw, hd - n)]


def bay_at(sx, sy):
    hw, hd, n = W / 2, D / 2, NOTCH
    x0, x1 = sorted((sx * hw, sx * (hw - n)))
    y0, y1 = sorted((sy * hd, sy * (hd - n)))
    return P([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def build():
    tower = P(tk.rect(W, D))
    pod = P(tk.rect(PW, PD))
    # podium: glass base with a stone band and a planted roof edge
    tk.prism("podium", tk.offset_poly(pod, -1.0), 0.0, H_POD - 1.5, "glassl")
    tk.glow_ring("podium_lit", tk.offset_poly(pod, -1.0), 0.8, H_POD - 2.5, 0.06, "sand_Glow")
    tk.prism("podium_roof", pod, H_POD - 1.5, H_POD, "stone", bev=0.15)
    tk.pier_grid("podium_cols", tk.offset_poly(pod, -0.6), 0.0, H_POD - 1.5, 6.0, 0.9, 0.9, "trim")
    # roof garden on the podium around the tower
    p0 = P([(-PW / 2 + 3, -PD / 2 + 3)])[0]
    p1 = P([(PW / 2 - 3, -PD / 2 + 3)])[0]
    tk.tree_row("pod_trees_s", p0, p1, H_POD, 4, h=5.0, r=2.0, seed=3.0)
    # main shaft (full plan), then the notched top
    kw = dict(glass="glassl", band="glass", band_h=0.7, band_out=0.15,
              fins=(3.0, 0.3, 0.3, "steel"), lit_spacing=3.0)
    tk.shaft("shaft", tower, H_POD, H_NOTCH, 7.8, lit=0.3, seed=1.0, **kw)
    top = P(notched())
    tk.shaft("upper", top, H_NOTCH, H_ROOF, 7.8, lit=0.4, seed=2.0, **kw)
    # terraces: slabs and planters in each carved corner, every two floors
    for ci, (sx, sy) in enumerate(CORNERS):
        bay = bay_at(sx, sy)
        c = (sum(p[0] for p in bay) / 4, sum(p[1] for p in bay) / 4)
        z = H_NOTCH
        k = 0
        while z < H_ROOF - 1:
            tk.prism(f"terrace_{ci}_{k}", bay, z, z + 0.7, "trim")
            tk.tree(f"terrace_tree_{ci}_{k}", c[0], c[1], z + 0.7, h=3.4, r=1.5,
                    mat="leaf" if (k + ci) % 2 else "leafd")
            tk.glow_cap(f"terrace_lamp_{ci}_{k}", tk.scale_poly(bay, 0.3, *c), z + 0.72, "sand_Glow")
            z += 7.8
            k += 1
        tk.prism(f"terrace_roof_{ci}", bay, H_ROOF - 0.7, H_ROOF, "trim")
    # roof + glass screen crown to 183 m, on the notched plan (the photo shows
    # the screen rising over the slab only, not over the terrace corners)
    tk.roof_kit("roof", top, H_ROOF, seed=6.0, parapet=0.8, plant_frac=0.4, yaw=YAW)
    tk.ring_band("crown_screen", tk.offset_poly(top, -0.5), H_ROOF, H_TOP - 0.8, 0.5, "glassl")
    tk.ring_band("crown_cap", tk.offset_poly(top, -0.6), H_TOP - 0.8, H_TOP, 0.7, "white")
    tk.glow_ring("crown_light", top, H_ROOF + 1.0, H_TOP - 1.5, 0.08, "white_Glow")
    tk.plinth("plaza", pod, h=0.3, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
