"""Deterministic Blender build of the SF-SIM miniature SFMOMA.

    blender -b --python build_151_3rd_street.py -- [--out DIR]

San Francisco Museum of Modern Art, 151 Third Street. Mario Botta's 1995
museum faces Yerba Buena Gardens across Third Street: symmetric, nearly
windowless blocks of red-orange brick stepping up toward the middle, where a
black-and-white striped cylinder, sliced on the bias, rises to a 130-ft
elliptical skylight (the oculus). Behind it, Snohetta's 2016 expansion runs
from Minna to Howard Street as a tall white mass with rippled horizontal
bands. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "151-3rd-street"
CENTER = (-122.4005921, 37.7857978)  # OSM way 41692824, OBB centre
H_TOP = 60.0                          # ESTIMATED crest of the 2016 Snohetta wing (10 storeys); see REFERENCE.md
H_SNO = 56.0
H_OCULUS = 39.6                       # published: the cylinder's skylight is 130 ft high (Wikipedia / NYT)
YAW = tk.bearing_to_yaw(135.2)        # local +x along Third St (SE), +y away from it (NE)
AXIS = -21.7                          # Botta's symmetry axis (local x)
# Snohetta wing: OSM footprint nodes behind the Botta building (local frame)
SNO = [(54.3, 6.6), (54.0, 33.2), (46.6, 34.0), (34.7, 35.1), (21.4, 36.2), (14.7, 36.9), (3.8, 37.3),
       (-5.1, 37.5), (-5.1, 42.3), (-54.1, 41.8), (-53.9, 6.6)]


def P(poly):
    return tk.xform(poly, YAW)


def box(x0, x1, y0, y1):
    return P([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def striped_cylinder(name, cx, cy, z0, z_front, z_back, r, seg, pitch):
    """Cylinder with alternating black/white bands and a top cut on the bias
    (low toward Third Street, high at the back)."""
    rings, rows = [], []
    nb = max(2, int(round((z_back - z0) / pitch)))
    for k in range(nb + 1):
        t = k / nb
        loop, zs = [], []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            lx, ly = r * math.cos(a), r * math.sin(a)
            zt = z_front + (z_back - z_front) * (ly + r) / (2 * r)
            zs.append(z0 + (zt - z0) * t)
            loop.append(tk.rot2((lx + cx, ly + cy), YAW))
        rings.append((zs, loop))
        if k < nb:
            rows.append(k % 2)
    verts, faces, fm = [], [], []
    for zs, loop in rings:
        verts += [(x, y, z) for (x, y), z in zip(loop, zs)]
    for k in range(nb):
        for i in range(seg):
            j = (i + 1) % seg
            faces.append((k * seg + i, k * seg + j, (k + 1) * seg + j, (k + 1) * seg + i))
            fm.append(rows[k])
    top = list(range(nb * seg, nb * seg + seg))
    faces.append(tuple(top))
    fm.append(2)
    faces.append(tuple(range(seg - 1, -1, -1)))
    fm.append(0)
    obj = tk.new_mesh(name, verts, faces, ["ink", "white", "glassg"], fm)
    # the oculus: a lit ellipse just above the sliced top
    cap = [(x, y, z + 0.08) for (x, y), z in zip(rings[-1][1], rings[-1][0])]
    tk.new_mesh(name + "_oculus_glow", [(x, y, z) for x, y, z in cap], [tuple(range(seg))], ["white_Glow"],
                recalc=False)
    return obj


def build():
    # Botta building: stepped brick blocks, symmetric about the cylinder
    tk.prism("botta_a", box(-54.2, 10.8, -42.3, 6.6), 0.0, 12.0, "brick", bev=0.15)
    tk.prism("botta_b", box(-50.2, 6.8, -36.5, 6.6), 12.0, 20.0, "brick", bev=0.15)
    tk.prism("botta_c", box(-45.2, 1.8, -29.0, 6.6), 20.0, 28.0, "brick", bev=0.15)
    tk.prism("botta_back", box(-32.0, -11.4, -18.0, 5.0), 28.0, 33.5, "ink", bev=0.1)
    # stone string-courses that give the brick its striated look
    tk.ring_band("botta_a_course", box(-54.2, 10.8, -42.3, 6.6), 10.8, 11.4, 0.12, "stone")
    tk.ring_band("botta_b_course", box(-50.2, 6.8, -36.5, 6.6), 18.8, 19.4, 0.12, "stone")
    # the striped, bias-cut cylinder and its oculus
    striped_cylinder("oculus", AXIS, -26.0, 12.0, 33.0, H_OCULUS, 9.5, 14, 1.9)
    # entrance: a striped portal slot on the Third Street face, lit at night
    front = box(AXIS - 4.5, AXIS + 4.5, -43.0, -41.0)
    tk.prism("portal", front, 0.0, 12.6, "white", bev=0.08)
    for k, z in enumerate((2.0, 4.6, 7.2, 9.8, 12.0)):
        tk.prism(f"portal_stripe_{k}", tk.offset_poly(front, 0.06), z, z + 1.0, "ink")
    a, b = P([(AXIS - 2.6, -43.0), (AXIS + 2.6, -43.0)])
    nx, ny = tk.rot2((0.0, -1.0), YAW)
    tk.flat_quad("door_panes", a, b, 0.0, 4.0, 0.08, "glassd", (nx, ny))
    tk.flat_quad("door_glow", a, b, 0.3, 3.6, 0.12, "sand_Glow", (nx, ny))
    # Snohetta wing: white, rippled horizontal bands, a few lit windows
    sno = P(tk.ccw(SNO))
    tk.shaft("sno", sno, 0.0, H_SNO, 5.8, glass="white", band="stone", band_h=1.0, band_out=0.35, lit=0.12,
             seed=3.0, lit_spacing=6.0, glass_in=0.0)
    a, b = P([(54.3, 8.0), (54.3, 32.0)])
    hx, hy = tk.rot2((1.0, 0.0), YAW)
    tk.flat_quad("howard_gallery_panes", a, b, 0.4, 7.2, 0.4, "glassl", (hx, hy))
    tk.flat_quad("howard_gallery_glow", a, b, 0.8, 6.6, 0.45, "sand_Glow", (hx, hy))
    tk.roof_kit("sno_roof", sno, H_SNO, seed=5.0, parapet=0.8, pmat="white", plant_frac=0.35, yaw=YAW)
    tk.prism("botta_roof_a", tk.offset_poly(box(-54.2, 10.8, -42.3, 6.6), -0.3), 11.8, 12.05, "roofd")
    tk.plinth("plaza", box(-54.2, 10.8, -42.3, 6.6), h=0.25, out=3.0)
    tk.plinth("sidewalk_sno", sno, h=0.24, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
