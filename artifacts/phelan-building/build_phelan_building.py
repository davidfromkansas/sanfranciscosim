"""Deterministic Blender build of the SF-SIM miniature Phelan Building.

    blender -b --python build_phelan_building.py -- [--out DIR]

760 Market Street (William Curlett, 1907-08; SF Landmark 156): James D.
Phelan's eleven-storey flatiron at the meeting of Market, O'Farrell and Grant,
clad in cream glazed terra cotta. A dark shopfront storey, a tall cream shaft
of closely spaced windows, a top storey of arched windows, a deep cornice and
balustrade, and a rounded prow at the eastern tip. At its western end a low
arcaded wing continues along Market. Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "phelan-building"
CENTER = (-122.4054146, 37.7863882)  # OSM relation 1547962 (outer ring), OBB centre
H_TOP = 47.0                          # DataSF 2010 LiDAR median of ring 201006.0000308 (measured; merged ring)
YAW = tk.bearing_to_yaw(81.4)         # local +x = east (prow), +y = north (O'Farrell St)
# OSM outer ring in local street-grid metres: O'Farrell edge, rounded prow, Market edge, west end
PROW = [(41.1, 31.2), (45.1, 31.1), (46.2, 30.2), (46.0, 28.8), (44.6, 27.3)]  # 12 OSM nodes thinned
XW = -30.0                            # west end of the tall flatiron (low arcaded wing beyond; inferred)


def market_y(x):
    """Market St edge from the prow (44.6, 27.3) to (-36.3, -31.2)."""
    return 27.3 + (x - 44.6) * (27.3 + 31.2) / (44.6 + 36.3)


def L(poly):
    return tk.xform(poly, YAW)


def build():
    tall = L([(XW, 31.1)] + PROW + [(XW, market_y(XW))])
    wing = L([(-36.3, -31.2), (XW, market_y(XW)), (XW, 31.1), (-46.3, 31.1), (-45.9, 12.4), (-38.3, 12.5),
              (-38.5, 8.3), (-36.6, 8.3)])
    # dark shopfront storey with lit windows
    tk.prism("shops", tall, 0.0, 5.2, "ink")
    tk.lit_windows("shops_lit", tall, [(0.4, 4.6)], 4.0, 0.85, seed=1.0, out=0.08, margin=0.2, gap=0.8,
                   edge_filter=lambda ei, p0, p1, n: tk.rot2(n, -YAW)[0] > -0.9)
    tk.ring_band("shop_cap", tall, 5.2, 5.8, 0.3, "cream")
    # cream terracotta shaft: 9 storeys of 3.8 m (the west face is hidden by the wing for the first two)
    west = lambda ei, p0, p1, n: tk.rot2(n, -YAW)[0] > -0.9  # noqa: E731
    tk.punched_block("shaft_lo", tall, 5.8, 13.4, 3.8, wall="cream", win="glassd", spacing=3.1, gap=1.1,
                     margin=0.8, lit=0.3, seed=4.0, bev=0.0, edge_filter=west)
    tk.punched_block("shaft", tall, 13.4, 40.0, 3.8, wall="cream", win="glassd", spacing=3.1, gap=1.1,
                     margin=0.8, lit=0.3, seed=5.0, bev=0.15)
    tk.ring_band("frieze", tall, 40.0, 40.6, 0.25, "trim")
    tk.prism("top", tall, 40.6, 44.2, "cream")
    tk.arched_panes("top_arches", tall, 41.0, 43.8, 3.1, 1.7, mat="glassd", seg=3)
    tk.ring_band("cornice", tall, 44.2, 45.6, 0.9, "trim")
    tk.prism("roof", tk.offset_poly(tall, -0.4), 45.3, 45.7, "roofd")
    tk.ring_band("balustrade", tk.offset_poly(tall, 0.2), 45.6, H_TOP, 0.3, "cream")
    ph = L(tk.rect(9.0, 8.0, 26.0, 20.0))
    tk.prism("penthouse", ph, 45.7, 46.9, "cream", bev=0.1)
    tk.hvac_cluster("plant", *tk.rot2((0.0, 12.0), YAW), 45.7, YAW, 14.0, 8.0, seed=3.0, hmax=1.1, fans=False)
    # low arcaded wing at the west end (Market side)
    tk.prism("wing", wing, 0.0, 11.0, "cream", bev=0.12)
    tk.arched_panes("wing_arches", wing, 0.6, 9.0, 3.6, 2.6, mat="glassd",
                    edge_filter=lambda ei, p0, p1, n: tk.rot2(n, -YAW)[1] < -0.3)
    tk.ring_band("wing_cornice", wing, 11.0, 11.7, 0.4, "trim")
    tk.prism("wing_roof", tk.offset_poly(wing, -0.3), 11.3, 11.75, "roofd")
    tk.prism("sidewalk", L([(-48.0, 34.0), (48.5, 34.0), (48.5, 26.0), (-38.0, -34.5), (-48.0, -34.5)]),
             0.0, 0.15, "concrete")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
