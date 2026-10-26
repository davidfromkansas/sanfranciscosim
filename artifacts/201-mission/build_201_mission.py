"""Deterministic Blender build of the SF-SIM miniature 201 Mission Street.

    blender -b --python build_201_mission.py -- [--out DIR]

201 Mission (1981), the former Providian Financial / Pacific Gateway
building: a 30-storey tower on an elongated octagonal plan at the Mission end
of an odd trapezoidal mid-block lot that runs through to Howard, over a
four-storey podium filling the lot. The plan shape and the podium come from
OSM building parts (ways 616813259 / 616813260). Facade from the Commons
infobox photo "201 Mission Street.jpg": pale precast concrete ribbed by dense
full-height piers with slot windows between them, a notched (crenellated)
parapet, a lower ~11-storey wing against one long face, and a grey concrete
podium with terraced planters. The wing's side (Howard/SE) is INFERRED.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "201-mission"
CENTER = (-122.3949072, 37.7910519)  # OSM podium way 616813260, OBB centre
H_TOP = 135.9                        # DataSF LiDAR crest 135.89 m (measured)
H_ROOF = 127.2                       # LiDAR majority roof plane (wiki 417 ft = 127 m)
H_POD = 17.0
WING_C = (13.0, -1.5)                # wing centre, m east/north of CENTER (inferred)
H_WING = 57.0                        # ~11 storeys over the podium, read from the photo (estimated)
# tower part, metres east/north of CENTER (OSM way 616813259)
TOWER_C = ((-122.3950436 + 122.3949072) * tk.KX, (37.791213 - 37.7910519) * tk.KY)
TOWER = [(29.6, -4.3), (11.9, 14.0), (-1.0, 18.2), (-17.3, 16.5), (-30.1, 3.9), (-12.6, -12.5),
         (-0.3, -18.1), (18.3, -15.8)]
PODIUM = [(-15.1, 54.5), (-53.6, 17.7), (-43.1, 6.5), (-29.0, 7.1), (-15.1, -6.3), (0.7, -5.5),
          (13.6, -18.3), (24.1, -17.5), (31.7, -25.0), (46.8, -24.3), (53.6, -17.5)]
YAW = math.radians(90 - 44.6)
TYAW = math.atan2(-4.3 - 3.9, 29.6 + 30.1)    # tower octagon long axis (OSM part), ~ -7.8 deg


def build():
    tower = tk.ccw([(x + TOWER_C[0], y + TOWER_C[1]) for x, y in TOWER])
    pod = tk.ccw(PODIUM)
    # podium: grey concrete with a dark recessed street storey and planted terraces
    tk.prism("podium_glass", tk.offset_poly(pod, -1.5), 0.0, 5.0, "glassd")
    tk.glow_ring("podium_lit", tk.offset_poly(pod, -1.5), 0.8, 4.2, 0.06, "sand_Glow")
    tk.pier_grid("podium_cols", tk.offset_poly(pod, -0.6), 0.0, 5.0, 7.0, 1.0, 1.0, "concrete",
                 skip_short=5.0)
    tk.prism("podium", pod, 5.0, H_POD, "concrete", bev=0.2)
    tk.panes("podium_win", pod, [(7.0, 9.5), (11.0, 13.5)], 4.0, mat="glass", gap=1.4, margin=0.0)
    tk.ring_band("podium_planter", tk.offset_poly(pod, -0.8), H_POD, H_POD + 1.0, 0.8, "concrete")
    tk.prism("podium_deck", tk.offset_poly(pod, -1.0), H_POD - 0.2, H_POD + 0.2, "concrete")
    tk.ring_band("podium_hedge", tk.offset_poly(pod, -2.4), H_POD, H_POD + 0.9, 1.2, "leafd")
    # the tower: pale concrete, dense full-height ribs, slot windows, notched parapet
    body = tk.offset_poly(tower, -0.4)
    tk.prism("tower", body, H_POD, H_ROOF, "stone", bev=0.15)
    bands = tk.floors(H_POD + 0.5, H_ROOF - 1.0, 3.75)
    tk.panes("tower_win", body, bands, 2.7, mat="glassd", out=0.06, margin=0.55, gap=1.3)
    tk.lit_windows("tower_lit", body, bands, 2.7, 0.3, seed=3.9, out=0.1, margin=0.65, gap=1.4)
    tk.pier_grid("tower_ribs", body, H_POD, H_ROOF + 1.8, 2.7, 0.9, 0.55, "white", skip_short=2.0)
    tk.prism("roof_deck", tk.offset_poly(body, -0.2), H_ROOF - 0.2, H_ROOF + 0.4, "roofd")
    # lower ~11-storey wing against the tower's south-east face (side inferred), placed
    # on the podium's wide Howard-side lobe so it stands clear of the octagon
    cx = sum(p[0] for p in tower) / len(tower)
    cy = sum(p[1] for p in tower) / len(tower)
    wing = tk.xform(tk.rect(18.0, 11.0), TYAW, *WING_C)
    tk.prism("wing", wing, H_POD, H_WING, "stone", bev=0.15)
    wb = tk.floors(H_POD + 0.5, H_WING - 1.0, 3.75)
    tk.panes("wing_win", wing, wb, 2.7, mat="glassd", out=0.06, margin=0.55, gap=1.3)
    tk.lit_windows("wing_lit", wing, wb, 2.7, 0.3, seed=7.3, out=0.1, margin=0.65, gap=1.4)
    tk.pier_grid("wing_ribs", wing, H_POD, H_WING + 1.0, 2.7, 0.9, 0.55, "white", skip_short=2.0)
    tk.prism("wing_roof", tk.offset_poly(wing, -0.3), H_WING - 0.2, H_WING + 0.3, "leafd")
    tk.tree_row("wing_trees", *tk.xform([(-5.0, 0.0), (5.0, 0.0)], TYAW, *WING_C), H_WING + 0.3, 3,
                h=3.5, r=1.5, seed=2.2)
    # roof: mechanical penthouse with louvres and a tidy plant cluster
    tk.box("penthouse", cx, cy, H_ROOF, H_TOP - 0.6, 22.0, 12.0, "concrete", yaw=TYAW, bev=0.2)
    tk.pier_grid("louvres", tk.xform(tk.rect(22.0, 12.0), TYAW, cx, cy), H_ROOF + 1.0, H_TOP - 1.6,
                 1.8, 0.3, 0.3, "steel", skip_short=3.0)
    tk.prism("pent_cap", tk.xform(tk.rect(22.6, 12.6), TYAW, cx, cy), H_TOP - 0.6, H_TOP, "trim")
    for k, sx in enumerate((-1, 1)):
        c = tk.rot2((sx * 19.5, 0.0), TYAW)
        tk.hvac_cluster(f"plant_{k}", cx + c[0], cy + c[1], H_ROOF + 0.4, TYAW, 12.0, 12.0, seed=1.2 + k,
                        hmax=3.6)
    # podium roof garden toward Howard
    tk.tree_row("pod_trees", (24.0, -12.0), (44.0, -19.0), H_POD + 0.6, 3, h=4.5, r=1.8, seed=4.0)
    tk.tree_row("pod_trees2", (-24.0, 43.0), (-14.0, 46.0), H_POD + 0.6, 2, h=4.5, r=1.8, seed=5.0)
    tk.plinth("plaza", pod, h=0.3, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
