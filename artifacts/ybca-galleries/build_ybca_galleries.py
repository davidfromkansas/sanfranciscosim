"""Deterministic Blender build of the SF-SIM miniature YBCA Galleries.

    blender -b --python build_ybca_galleries.py -- [--out DIR]

Yerba Buena Center for the Arts, Galleries and Forum building (Fumihiko
Maki, 1993), on Mission Street at Yerba Buena Gardens: a long, low,
precise box of silver-grey aluminium panels and tall glazed walls. On the
gardens side a full-height glass wall is crossed by a broad diagonal
aluminium band - the grand stair rising inside - and a thin flat canopy
marks the entrance; a raised skylit hall lifts above the gallery roof.
Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "ybca-galleries"
CENTER = (-122.4019824, 37.7855827)   # OSM way 24563073, OBB centre
H_TOP = 17.3                           # LiDAR max 17.26 m (DataSF 2010, parcel 3723115); OSM "28 m" rejected
H_GAL = 12.0                           # gallery block roof (LiDAR median 10.3 m over the whole footprint)
H_FORUM = 9.0                          # forum wing roof (inferred)
YAW = tk.bearing_to_yaw(135.1)         # local +x = bearing 135.1 (SE, away from Mission), +y = 45.1 (NE)

# OSM outline (19 nodes) in local metres, simplified to two masses:
# the gallery block along Mission (x < 5) and the forum wing to the SE.
GALLERY = [(-40.9, -35.6), (4.6, -35.6), (4.6, -7.2), (5.1, -7.2), (5.1, 31.0), (-23.8, 31.0), (-23.8, 35.5), (-43.8, 35.5),
           (-43.9, 27.8), (-40.9, 27.8)]
FORUM = [(4.6, -35.6), (38.5, -35.5), (38.5, -31.5), (43.8, -31.4), (43.9, -26.3), (38.8, -26.3),
         (39.0, -7.0), (4.6, -7.2)]
HALL = [(-30.0, -18.0), (-6.0, -18.0), (-6.0, 14.0), (-30.0, 14.0)]   # raised skylit hall (inferred)


def L(poly):
    return tk.ccw(tk.xform(poly, YAW))


def shared(p0, p1):
    """The party wall where the forum wing abuts the gallery block (x = 4.6, y < -7.2)."""
    m = tk.rot2(((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2), -YAW)
    return abs(m[0] - 4.6) < 0.3 and m[1] < -7.0


def facing(dx, dy):
    def f(ei, p0, p1, nrm):
        lx, ly = tk.rot2(nrm, -YAW)
        return lx * dx + ly * dy > 0.7 and not shared(p0, p1)
    return f


def exposed(ei, p0, p1, nrm):
    return not shared(p0, p1)


def build():
    gal, forum, hall = L(GALLERY), L(FORUM), L(HALL)
    # aluminium-panel volumes with a dark glass ground storey band
    tk.prism("gallery", gal, 0.0, H_GAL, "steel", bev=0.15)
    tk.prism("forum", forum, 0.0, H_FORUM, "steel", bev=0.15)
    for name, poly, h in (("gallery", gal, H_GAL), ("forum", forum, H_FORUM)):
        tk.ring_band(name + "_coping", poly, h - 0.5, h + 0.35, 0.15, "white")
        tk.panes(name + "_glaze", poly, [(0.0, 4.2)], 3.0, mat="glassd", gap=0.3, margin=0.15,
                 edge_filter=exposed)
        tk.lit_windows(name + "_lit", poly, [(0.0, 4.2)], 3.0, 0.6, seed=len(name), out=0.1, margin=0.4,
                       gap=0.5, edge_filter=exposed)
    # the gardens face (local +x side of the gallery block): full-height glass
    # with the diagonal stair band crossing it
    tk.panes("garden_glass", gal, [(4.4, H_GAL - 0.8)], 3.2, mat="sky", gap=0.25, margin=0.1,
             edge_filter=facing(1, 0))
    tk.lit_windows("garden_lit", gal, [(4.4, H_GAL - 0.8)], 3.2, 0.5, seed=4.0, out=0.12, margin=0.3,
                   gap=0.4, edge_filter=facing(1, 0))
    a, b = (5.25, 27.0, 2.2), (5.25, -4.0, H_GAL - 2.0)
    pa, pb = tk.rot2(a[:2], YAW), tk.rot2(b[:2], YAW)
    tk.tube("stair_band", (pa[0], pa[1], a[2]), (pb[0], pb[1], b[2]), 2.8, 0.6, tk.rot2((1.0, 0.0), YAW), "white")
    # entrance canopy on the forum wing's NE face
    c = tk.rot2((22.0, -5.4), YAW)
    tk.box("canopy", c[0], c[1], 4.4, 4.8, 12.0, 3.6, "white", yaw=YAW, bev=0.05)
    # raised skylit hall and its lit clerestory
    tk.prism("hall", hall, H_GAL - 0.2, H_TOP - 0.4, "white", bev=0.12)
    tk.prism("hall_roof", tk.offset_poly(hall, 0.4), H_TOP - 0.4, H_TOP, "steel")
    tk.panes("clerestory", hall, [(H_GAL + 0.6, H_TOP - 1.2)], 2.4, mat="glassl", gap=0.3, margin=0.1)
    tk.lit_windows("clerestory_lit", hall, [(H_GAL + 0.6, H_TOP - 1.2)], 2.4, 0.9, seed=2.0, out=0.1,
                   margin=0.3, gap=0.4)
    # flat roofs, a little plant on the forum
    tk.prism("gal_roof", tk.offset_poly(gal, -0.3), H_GAL - 0.1, H_GAL + 0.12, "roofd")
    tk.prism("forum_roof", tk.offset_poly(forum, -0.3), H_FORUM - 0.1, H_FORUM + 0.12, "roofd")
    c = tk.rot2((24.0, -21.0), YAW)
    tk.hvac_cluster("plant", c[0], c[1], H_FORUM + 0.12, YAW, 12.0, 8.0, seed=5.0, hmax=2.0, fans=False)
    # gardens-side apron (the photo's street trees are left to the city's tree layer)
    # (no bevel: the miter offset of the notched plans leaves slivers)
    tk.prism("plaza", tk.offset_poly(gal, 1.5), 0.0, 0.25, "stone")
    tk.prism("plaza_f", tk.offset_poly(forum, 1.5), 0.0, 0.2, "stone")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
