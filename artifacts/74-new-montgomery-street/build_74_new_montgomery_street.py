"""Deterministic Blender build of the SF-SIM miniature The Montgomery.

    blender -b --python build_74_new_montgomery_street.py -- [--out DIR]

74 New Montgomery Street at Jessie (Reid Brothers, 1914): the San Francisco
Call's headquarters after the 1906 fire, converted to 107 condominiums in
2005. An eight-storey classical block: a charcoal-grey base (tall ground
floor, mezzanine, banded rusticated third storey), four storeys of cream
fluted Corinthian giant pilasters, a deep modillioned cornice and a cream
attic storey of small windows. Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "74-new-montgomery-street"
CENTER = (-122.4013268, 37.7874752)   # OSM way 79377217, OBB centre
H_TOP = 32.7                           # LiDAR median roof (DataSF 2010, parcel 3707064); OSM 33
YAW = tk.bearing_to_yaw(45.0)          # local +x = bearing 45 (parallel to Market), +y = 315

# OSM rectangle 82.1 x 21.3 m. Local +x end (NE) = New Montgomery St (5 bays),
# local +y side (NW) = Jessie St (the long street front); SE/SW are back walls.
L, W = 82.0, 21.3
Z_MEZZ, Z_RUST, Z_PIL, Z_CORN, Z_ATT = 6.0, 10.2, 14.6, 28.0, 29.6


def is_street(nrm):
    lx, ly = tk.rot2(nrm, -YAW)
    return lx > 0.7 or ly > 0.7


def street(ei, p0, p1, nrm):
    return is_street(nrm)


def back(ei, p0, p1, nrm):
    return not is_street(nrm)


def pilasters(name, plan, z0, z1, spacing, w, d, mat):
    """Giant-order pilasters on the street faces only (pier_grid has no filter)."""
    objs = []
    for k, (p0, p1, ln, nrm) in enumerate(tk.edges(plan)):
        if not is_street(nrm):
            continue
        n = int(round(ln / spacing))
        ux, uy = (p1[0] - p0[0]) / ln, (p1[1] - p0[1]) / ln
        for i in range(n + 1):
            t = w / 2 + 0.3 + (ln - w - 0.6) * i / n
            cx, cy = p0[0] + ux * t + nrm[0] * d / 2, p0[1] + uy * t + nrm[1] * d / 2
            objs.append(tk.box(f"{name}_{k}_{i}", cx, cy, z0, z1, w, d, mat, yaw=YAW))
            objs.append(tk.box(f"{name}_cap_{k}_{i}", cx + nrm[0] * 0.1, cy + nrm[1] * 0.1, z1 - 1.0, z1,
                               w + 0.5, d + 0.2, mat, yaw=YAW))
    return tk.join(objs, name)


def build():
    plan = tk.ccw(tk.xform(tk.rect(L, W), YAW))
    # charcoal base: shopfronts, mezzanine, rusticated third storey
    tk.prism("base", plan, 0.0, Z_PIL, "steel", bev=0.15)
    tk.panes("shop", plan, [(0.4, Z_MEZZ - 0.4)], 4.1, mat="glassd", gap=1.4, margin=0.3, edge_filter=street)
    tk.lit_windows("shop_lit", plan, [(0.4, Z_MEZZ - 0.8)], 4.1, 0.75, seed=1.0, out=0.1, margin=0.4, gap=1.6,
                   edge_filter=street)
    tk.panes("base_win", plan, [(Z_MEZZ, Z_RUST), (Z_RUST + 0.6, Z_PIL - 0.6)], 4.1, mat="glassl", gap=1.6,
             margin=0.6)
    for i, z in enumerate([Z_MEZZ - 0.3, Z_RUST + 0.3, Z_RUST + 1.4, Z_RUST + 2.5, Z_PIL - 0.5]):
        tk.ring_band(f"rust_{i}", plan, z, z + 0.45, 0.25 if i else 0.4, "steel")
    # cream upper body: four pilaster storeys, cornice, attic
    tk.prism("upper", plan, Z_PIL, Z_ATT, "cream", bev=0.12)
    bands = tk.floors(Z_PIL, Z_CORN, 3.35)
    tk.panes("upper_win", plan, bands, 4.1, mat="glassl", gap=1.6, margin=0.5)
    tk.lit_windows("upper_lit", plan, bands, 4.1, 0.33, seed=4.0, out=0.1, margin=0.6, gap=1.7)
    pilasters("pilasters", plan, Z_PIL, Z_CORN, 4.1, 1.1, 0.55, "cream")
    tk.cornice("cornice", plan, Z_CORN, h=1.6, out=1.25, mat="cream")
    tk.prism("attic", plan, Z_ATT, H_TOP - 1.7, "cream", bev=0.1)
    tk.panes("attic_win", plan, [(Z_ATT + 0.2, H_TOP - 1.8)], 4.1, mat="glassl", gap=2.0, margin=0.5)
    tk.lit_windows("attic_lit", plan, [(Z_ATT + 0.2, H_TOP - 1.8)], 4.1, 0.3, seed=7.0, out=0.1, margin=0.6,
                   gap=2.1)
    tk.cornice("top_cornice", plan, H_TOP - 1.7, h=0.9, out=0.5, mat="cream")
    # roof: dark deck inside a 0.8 m parapet, one low plant cluster below the parapet line
    tk.prism("roof", tk.offset_poly(plan, -0.3), H_TOP - 0.9, H_TOP - 0.75, "roofd")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.6), H_TOP - 0.8, H_TOP, 0.6, "cream")
    c = tk.rot2((24.0, -3.0), YAW)
    tk.hvac_cluster("plant", c[0], c[1], H_TOP - 0.75, YAW, 12.0, 8.0, seed=3.0, hmax=0.7, fans=False)
    tk.glow_ring("crown_light", plan, Z_CORN - 0.5, Z_CORN - 0.1, 0.12, "white_Glow")
    tk.plinth("plaza", plan, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
