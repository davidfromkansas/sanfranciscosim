"""Deterministic Blender build of the SF-SIM miniature St. Regis Museum Tower.

    blender -b --python build_3rd_street_tower.py -- [--out DIR]

125 Third Street at Mission (Skidmore, Owings & Merrill, 2005): a 42-storey
hotel and residential tower, published roof 484 ft (147.5 m). A warm limestone
grid of square punched windows, a broad 89 m hotel block wrapped around the
foot of a slimmer residential shaft, a glass-railed penthouse crown, and the
Museum of the African Diaspora in a glassy three-storey base on Mission.
Footprints are the OSM building and building:part ways. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "3rd-street-tower"
CENTER = (-122.401414, 37.7863109)   # OSM way 436648188, OBB centre
H_TOP = 147.5                        # PUBLISHED roof 484 ft (Wikipedia); LiDAR max 144.8
H_WING = 88.4                        # OSM part 79377186 height=89; LiDAR median 88.5 (13 x 6.8 m bands)
H_CROWN0 = 142.8                     # top of the stone shaft (21 x 6.8 m bands)
H_STRIP = 13.0                       # OSM part 1365382602, 3 levels
PITCH = 6.8                          # two storeys per window band (42 storeys / 147.5 m)

# OSM ways, metres relative to CENTER (+x east, +y north)
TOWER = [(-13.2, 8.4), (9.7, -14.9), (27.2, 2.1), (4.3, 25.4)]          # part 436648187, 42 levels
WING = [(32.9, 0.5), (30.9, 2.5), (29.8, 3.5), (2.9, 30.0), (-18.8, 8.3), (-11.3, 0.8),
        (-14.8, -2.7), (-13.8, -3.8), (-27.4, -17.2), (-8.4, -36.0), (-6.0, -38.4),
        (-0.6, -33.0), (13.1, -19.3)]                                     # part 79377186
STRIP = [(-18.8, 8.3), (-21.4, 10.9), (7.1, 37.4), (35.5, 9.1), (33.2, 7.0), (29.8, 3.5),
         (2.9, 30.0)]                                                     # part 1365382602
OUTLINE = [(-27.4, -17.2), (-8.4, -36.0), (-6.0, -38.4), (-0.6, -33.0), (13.1, -19.3),
           (32.9, 0.5), (30.9, 2.5), (29.8, 3.5), (33.2, 7.0), (35.5, 9.2), (7.1, 37.4),
           (-21.4, 10.9), (-18.8, 8.3), (-11.2, 0.8), (-14.8, -2.7), (-13.8, -3.8)]


def off_strip(ei, p0, p1, nrm):
    """Edge filter: skip wing edges that lie against the low strip (buried)."""
    m = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
    for a, b, L, _ in tk.edges(tk.ccw(STRIP)):
        t = max(0.0, min(1.0, ((m[0] - a[0]) * (b[0] - a[0]) + (m[1] - a[1]) * (b[1] - a[1])) / (L * L)))
        if math.dist(m, (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)) < 1.5:
            return False
    return True


def stone_grid(name, plan, z0, z1, seed, spacing=3.6, lit=0.3, edge_filter=None):
    bands = tk.floors(z0, z1, PITCH)
    tk.panes(name, plan, bands, spacing, mat="glassl", gap=1.4, margin=1.4, edge_filter=edge_filter)
    tk.lit_windows(name + "_lit", plan, bands, spacing, lit, seed=seed, out=0.12, margin=1.6, gap=1.6,
                   edge_filter=edge_filter)


def build():
    tower, wing, strip = tk.ccw(TOWER), tk.ccw(WING), tk.ccw(STRIP)

    # low east strip (3 levels)
    tk.prism("strip", strip, 0.0, H_STRIP, "sand", bev=0.1)
    tk.ring_band("strip_cap", strip, H_STRIP - 0.6, H_STRIP, 0.3, "stone")
    tk.roof_kit("strip_roof", tk.offset_poly(strip, -0.5), H_STRIP, seed=3.0, parapet=0.8, plant_frac=0.3)

    # hotel block: glassy museum/lobby base, then the limestone grid to 88.4 m
    tk.prism("wing_base", tk.offset_poly(wing, -0.6), 0.0, 10.2, "glassd")
    tk.lit_windows("wing_base_lit", tk.offset_poly(wing, -0.6), [(0.4, 9.8)], 4.0, 0.75, seed=1.0,
                   out=0.1, margin=0.6, gap=0.8, edge_filter=off_strip)
    tk.prism("wing_transfer", wing, 10.2, 13.6, "sand", bev=0.1)
    tk.prism("wing", wing, 13.6, H_WING, "sand", bev=0.15)
    stone_grid("wing_grid", wing, 13.6, H_WING, seed=11.0)
    tk.ring_band("wing_parapet", tk.offset_poly(wing, -0.5), H_WING, H_WING + 1.2, 0.5, "stone")
    tk.prism("wing_deck", tk.offset_poly(wing, -0.4), H_WING - 0.3, H_WING + 0.2, "roofd")
    tk.hvac_cluster("wing_plant", -12.0, -20.0, H_WING + 0.2, tk.bearing_to_yaw(135.5), 14.0, 8.0, seed=4.0,
                    hmax=3.0)

    # residential shaft rising through the hotel block
    tk.prism("tower", tower, H_WING, H_CROWN0, "sand", bev=0.15)
    stone_grid("tower_grid", tower, H_WING + 0.0, H_CROWN0, seed=21.0, spacing=3.4, lit=0.35)
    # the vertical glass slot and balcony stack on the NE face (photo)
    for p0, p1, L, nrm in tk.edges(tower):
        if nrm[0] > 0.5 and nrm[1] > 0.5:     # NE face
            ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
            c = (p0[0] + ux * L * 0.72 + nrm[0] * 0.6, p0[1] + uy * L * 0.72 + nrm[1] * 0.6)
            tk.box("slot", c[0], c[1], H_WING, H_CROWN0 - 3.4, 3.0, 1.2, "glass", yaw=math.atan2(uy, ux))
            a = (c[0] - ux * 0.8, c[1] - uy * 0.8)
            b = (c[0] + ux * 0.8, c[1] + uy * 0.8)
            tk.flat_quad("slot_glow", a, b, H_WING + 2.0, H_CROWN0 - 6.0, 0.62, "sky_Glow", nrm)
    # glass-railed penthouse crown
    tk.ring_band("crown_cornice", tower, H_CROWN0, H_CROWN0 + 0.8, 0.4, "stone")
    inner = tk.offset_poly(tower, -1.6)
    tk.prism("crown", inner, H_CROWN0 + 0.8, H_TOP - 1.4, "glassl", bev=0.0)
    tk.lit_windows("crown_lit", inner, [(H_CROWN0 + 0.8, H_TOP - 1.4)], 3.0, 0.6, seed=31.0, out=0.08,
                   margin=0.5, gap=0.6)
    tk.ring_band("crown_rail", tk.offset_poly(inner, -0.2), H_TOP - 1.4, H_TOP, 0.2, "glassg")
    tk.prism("crown_deck", tk.offset_poly(inner, -0.3), H_TOP - 1.6, H_TOP - 1.0, "roofd")
    tk.glow_ring("crown_line", inner, H_TOP - 1.4, H_TOP - 1.0, 0.28, "white_Glow")
    tk.hvac_cluster("crown_plant", 7.0, 5.0, H_TOP - 1.0, tk.bearing_to_yaw(135.5), 10.0, 6.0, seed=9.0,
                    hmax=1.0, fans=False)

    tk.plinth("apron", tk.ccw(OUTLINE), h=0.3, out=2.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
