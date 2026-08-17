"""Deterministic Blender build of the SF-SIM miniature 156 South Park Street.

    blender -b --python build_156_south_park.py -- [--out DIR]

Writes 156-south-park.blend and 156-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading - the
loader applies no rotation. Origin = footprint area centroid (anchor
lon -122.3948748, lat 37.7813535), min Z = 0, front parapet crest exactly 8.70 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured DataSF LiDAR footprint (mblr SF3775066), a 32.3 m through lot
  running east-south-east to South Park Street and west-north-west to the Taber
  Place alley, at ~117.3 deg. It is a tapering strip: 5.93 m wide at the street,
  9.8 m at its widest two thirds back, and a 7.94 m end wall on Taber Place cut
  ~19 deg off square;
* two masses, which is the whole point of the building: a tall two-storey street
  bar (parapet crest 8.70 m, the LiDAR maximum) in front of a long single-storey
  top-lit shed (roof 5.45 m, the LiDAR modal cell at 5.66 m less its parapet).
  The step between them is what the app's downward camera reads first;
* one colour. A 1924 reinforced-concrete warehouse for a drayage firm was built
  without ornament and the 2023 studio conversion painted everything - wall,
  sash, glazing bars, sills, door, parapet cap - the same slate blue-grey. The
  2009 Page & Turnbull survey found this the only unaltered contributor of the
  district's twenty-three. Its plainness IS its identity, so the model carries
  no base course, no cornice and no contrasting shopfront;
* the two stacked fields of small steel-sash panes, which are the only openings
  on the street elevation and therefore carry it entirely. The pane grid is
  modelled as relieved bars over one flat glass field, not as 50 glazed panes;
* the identity details, small on purpose: the pale entrance canopy, the 156
  numerals, two stacked black sconces on the pier, and the two X-shaped steel
  star tie anchors high on the parapet (the visible ends of the 1990 parapet
  reinforcing permit);
* the skylight monitor run down the shed roof, aligned to the lot's long axis
  with its glazing facing north-north-east - the roof's only event, and the
  reason this asset is worth more than a box from the aerial camera;
* night state: warm interior light behind the two street sash fields (this is an
  architecture studio, lit late), with a dimmer cool spill from the monitors as
  the supporting accent. Nothing else glows. Glow surfaces are thin shells proud
  of the opaque glazing - the app renders _Glow in a separate layer that is ~12%
  alpha by day, so a primary surface must never be authored as glow.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# The lot's own frame. +v points east-south-east along the lot toward South Park
# Street (the measured front normal, bearing 117.3 deg true); +u points
# south-south-west across it, toward 158 - 160 South Park. The pair is a proper
# rotation, so counter-clockwise in (u, v) is counter-clockwise in world.
FRONT_BEARING_DEG = 117.3

_TH = math.radians(FRONT_BEARING_DEG)
V_HAT = (math.sin(_TH), math.cos(_TH))
U_HAT = (V_HAT[1], -V_HAT[0])


def to_world(u, v):
    """Lot frame -> world (east, north) metres, both centred on the anchor."""
    return (u * U_HAT[0] + v * V_HAT[0], u * U_HAT[1] + v * V_HAT[1])


# Survey footprint in (u, v), recentred on the anchor. Derived from the DataSF
# ring for mblr SF3775066; the raw vertices are listed in REFERENCE.md. Two
# simplifications, both recorded in REPORT.md: the 0.15 m sliver at the
# north-east street corner and the 1.05 m sliver at the Taber Place corner are
# dropped, because they are sub-metre artefacts of the parcel line that cost
# triangles the window grids need.
V_SPLIT = 10.00        # where the two-storey bar meets the single-storey shed

FRONT_UV = [
    (-2.40, V_SPLIT),   # junction, north-east side
    (4.82, V_SPLIT),    # junction, south-west side
    (3.25, 16.44),      # South Park corner, south-west (party wall, 158 - 160)
    (-2.68, 16.44),     # South Park corner, north-east (party wall, 150)
]

REAR_UV = [
    (-2.40, V_SPLIT),   # junction, north-east side
    (-2.11, 3.41),      # survey vertex: north-east wall kink
    (-4.79, -2.63),     # survey vertex: north-east wall steps out
    (-7.92, -13.27),    # Taber Place corner, north-east
    (-0.41, -15.86),    # Taber Place corner, south-west
    (6.84, 1.74),       # survey vertex: south-west wall, widest point
    (4.82, V_SPLIT),    # junction, south-west side
]

# Heights. Z_CREST is the one number that must land exactly: the loader scales
# by targetHeightM / measuredHeight and 8.70 must give 1.0.
Z_SHED = 5.45          # shed roof deck
Z_SHED_PAR = 5.70      # shed parapet crest (LiDAR modal cell, 566 cm)
Z_MON0, Z_MON1 = 5.30, 6.28   # skylight monitor body
Z_SILL, Z_HEAD = 1.05, 4.05   # ground-floor sash field
Z_FLOOR2 = 4.55        # second-floor line
Z_SILL2, Z_HEAD2 = 5.30, 7.55  # upper sash ribbon
Z_BAR = 8.34           # front bar roof deck
Z_CREST = 8.70         # front parapet crest -> the bbox top, must land exactly

SKIN = 0.10            # applied panels stand proud of the wall by this much
PARAPET_T = 0.28

PALETTE_HEX = {
    # The building's one colour, read off the Jan 2025 pano: a desaturated
    # blue-grey, distinctly bluer than black and much darker than any stucco on
    # the oval. Deliberate palette extension, documented as a WARN in REPORT.md
    # the same way 380 Brannan's Toy_slate and 155 South Park's Toy_peach were -
    # nothing in the existing palette reads as "painted grey concrete".
    "Toy_slate": "77828e",
    "Toy_roofd": "444a54",
    "Toy_trim": "ddd7c9",
    "Toy_ink": "26262a",
    "Toy_glass": "22394f",
    "Toy_glassl": "6f95b8",
    "Toy_gold": "caa64a",
    "Toy_warm": "cbbb96",
    "Toy_warm_Glow": "cbbb96",
    "Toy_glass_Glow": "6f95b8",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


# --------------------------------------------------------------- 2D helpers


def signed_area(poly):
    s = 0.0
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        s += a[0] * b[1] - b[0] * a[1]
    return s / 2.0


def ccw(poly):
    return poly if signed_area(poly) > 0 else list(reversed(poly))


def poly_edge(poly, i):
    """Edge i of poly: (origin, length, tangent unit, outward normal)."""
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def edge_facing(poly, bearing_deg):
    """Index of the edge whose outward normal is closest to a compass bearing."""
    target = math.radians(bearing_deg)
    tx, ty = math.sin(target), math.cos(target)
    best, best_dot = 0, -2.0
    for i in range(len(poly)):
        _a, _l, _t, n = poly_edge(poly, i)
        d = n[0] * tx + n[1] * ty
        if d > best_dot:
            best, best_dot = i, d
    return best


def offset_polygon(poly, d):
    """Miter offset of a CCW footprint by intersecting adjacent offset lines;
    positive d moves outward. Handles the one re-entrant vertex on the shed."""
    npts = len(poly)
    normals = []
    for i in range(npts):
        a, b = poly[i], poly[(i + 1) % npts]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1.0
        normals.append((dy / length, -dx / length))
    out = []
    for i in range(npts):
        n1, n2 = normals[i - 1], normals[i]
        v = poly[i]
        det = n1[0] * n2[1] - n1[1] * n2[0]
        if abs(det) < 1e-6:
            out.append((v[0] + n2[0] * d, v[1] + n2[1] * d))
            continue
        c1 = v[0] * n1[0] + v[1] * n1[1] + d
        c2 = v[0] * n2[0] + v[1] * n2[1] + d
        out.append(((c1 * n2[1] - c2 * n1[1]) / det, (c2 * n1[0] - c1 * n2[0]) / det))
    return out


def rect_profile(w, z0, z1):
    a = w / 2.0
    return [(-a, z0), (a, z0), (a, z1), (-a, z1)]


def star_profile(size, zc):
    """Closed (u, z) eight-pointed star washer - the one piece of ornament the
    1990 parapet reinforcing left on the facade."""
    pts = []
    for k in range(8):
        ang = math.radians(22.5 + k * 45.0)
        r = size / 2.0 if k % 2 == 0 else size / 5.2
        pts.append((r * math.cos(ang), zc + r * math.sin(ang)))
    return pts


# -------------------------------------------------------------- mesh helpers


def new_mesh(name, verts, faces, materials, face_mats=None):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(v) for v in verts], [], faces)
    for m in materials:
        mesh.materials.append(m)
    if face_mats:
        for poly, mi in zip(mesh.polygons, face_mats):
            poly.material_index = mi
    mesh.validate()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.shade_flat()
    return obj


def bevel(obj, width=0.12, segments=2):
    """Miniature-style edge softening (style bible s.4), width capped at a third
    of the object's thinnest dimension so thin applied panels do not collapse."""
    thin = min((d for d in obj.dimensions if d > 1e-6), default=width)
    offset = min(width, thin * 0.30)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.bevel(
        bm,
        geom=list(bm.verts) + list(bm.edges),
        offset=offset,
        segments=segments,
        profile=0.5,
        affect="EDGES",
        clamp_overlap=True,
    )
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-4)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-4, edges=list(bm.edges))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def prism(name, poly, z0, z1, mat, mat_caps=None):
    """Closed extrusion of a CCW polygon (walls + both caps)."""
    npts = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces, face_mats = [], []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
        face_mats.append(0)
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    face_mats += [1 if mat_caps else 0] * 2
    mats = [mat, mat_caps] if mat_caps else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def ring_band(name, poly, z0, z1, off_in, off_out, mat):
    """Closed band following a footprint: 4 loops, quads between."""
    lo_in = offset_polygon(poly, off_in)
    lo_out = offset_polygon(poly, off_out)
    npts = len(lo_in)
    verts = []
    for loop, z in ((lo_in, z0), (lo_out, z0), (lo_out, z1), (lo_in, z1)):
        verts.extend([(x, y, z) for x, y in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * npts, ((k + 1) % 4) * npts
        for i in range(npts):
            j = (i + 1) % npts
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])


def face_panel(name, poly, edge, s_centre, profile, d0, d1, mat):
    """Closed prism of an (s, z) profile lying in the plane of wall `edge`,
    extruded outward from offset d0 to d1 along that wall's normal. `s` runs
    along the edge from its first vertex."""
    a, _length, t, n = poly_edge(poly, edge)
    verts = []
    for d in (d0, d1):
        for ds, z in profile:
            px = a[0] + t[0] * (s_centre + ds) + n[0] * d
            py = a[1] + t[1] * (s_centre + ds) + n[1] * d
            verts.append((px, py, z))
    npts = len(profile)
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def uv_box(name, u, v, z0, z1, su, sv, mat):
    """Box on the lot's own grid: centre at (u, v), su across the lot, sv along."""
    corners = [
        to_world(u - su / 2, v - sv / 2),
        to_world(u + su / 2, v - sv / 2),
        to_world(u + su / 2, v + sv / 2),
        to_world(u - su / 2, v + sv / 2),
    ]
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


def material(name):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    rgb = PALETTE[name]
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.85
    bsdf.inputs["Metallic"].default_value = 0.0
    if name.endswith("_Glow"):
        # Flagged for the app's night pass; emission is off in the day asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# --------------------------------------------------------------------- parts


def opening(tag, poly, edge, s0, s1, z0, z1, wall, fill_mat, jamb=0.17, depth=0.22):
    """A recessed opening built without booleans, the way 155 South Park's
    rect_opening does it: the fill sits just proud of the wall face and a ring
    of four wall-coloured jambs stands proud of the fill, so the eye reads a
    reveal. Modelling the fill *behind* the wall plane instead hides it
    completely - there is no hole in the wall to see it through."""
    w = s1 - s0
    sc = (s0 + s1) / 2.0
    # side jambs are clamped to the pavement: an opening that starts at z = 0
    # would otherwise carry its jambs below it and break the min-Z contract
    zj = max(z0 - jamb, 0.0)
    face_panel(f"{tag}_fill", poly, edge, sc, rect_profile(w, z0, z1), 0.0, 0.04, fill_mat)
    face_panel(
        f"{tag}_jl", poly, edge, s0 - jamb / 2, rect_profile(jamb, zj, z1 + jamb),
        0.0, depth, wall,
    )
    face_panel(
        f"{tag}_jr", poly, edge, s1 + jamb / 2, rect_profile(jamb, zj, z1 + jamb),
        0.0, depth, wall,
    )
    face_panel(
        f"{tag}_jt", poly, edge, sc, rect_profile(w, z1, z1 + jamb), 0.0, depth, wall,
    )
    if z0 > jamb:
        # skipped for openings that start at the pavement - a bottom jamb there
        # would push geometry below z = 0 and break the contract's min-Z check
        face_panel(
            f"{tag}_jb", poly, edge, sc, rect_profile(w, z0 - jamb, z0), 0.0, depth + 0.06, wall,
        )
    return w, sc


def sash_field(tag, poly, edge, s0, s1, z0, z1, cols, rows, wall, glass, glow=None):
    """One field of industrial steel sash. The mullion grid is modelled as
    relieved bars in the wall colour standing proud of one flat glass plane -
    that is what makes the field read as many small panes at thumbnail size.
    The panes themselves are never modelled."""
    w, sc = opening(tag, poly, edge, s0, s1, z0, z1, wall, glass)
    if glow:
        # The shell covers the lower band of the field only. Two things drive
        # that: a studio's light actually reads at desk height, and the app's
        # day pass leaves a closed shell at ~23% (two alpha layers, not one), so
        # a shell over the whole field tints the entire window by day. Verified
        # by rendering the same GLB with the shells deleted.
        gz1 = z0 + (z1 - z0) * 0.46
        face_panel(
            f"{tag}_glow", poly, edge, sc, rect_profile(w - 0.80, z0 + 0.10, gz1),
            0.044, 0.050, glow,
        )
    bar = 0.09
    for k in range(1, cols):
        s = s0 + w * k / cols
        face_panel(
            f"{tag}_mv{k}", poly, edge, s, rect_profile(bar, z0, z1), 0.052, 0.13, wall,
        )
    for k in range(1, rows):
        z = z0 + (z1 - z0) * k / rows
        face_panel(
            f"{tag}_mh{k}", poly, edge, sc,
            rect_profile(w, z - bar / 2, z + bar / 2), 0.052, 0.13, wall,
        )


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0

    wall = material("Toy_slate")
    roofd = material("Toy_roofd")
    trim = material("Toy_trim")
    ink = material("Toy_ink")
    glass = material("Toy_glass")
    glow_warm = material("Toy_warm_Glow")
    glow_cool = material("Toy_glass_Glow")

    front = ccw([to_world(u, v) for u, v in FRONT_UV])
    rear = ccw([to_world(u, v) for u, v in REAR_UV])

    # ------------------------------------------------ the two masses
    prism("shed", rear, 0.0, Z_SHED, wall, roofd)
    ring_band("shed_parapet", rear, Z_SHED, Z_SHED_PAR, -PARAPET_T, 0.03, wall)

    prism("bar", front, 0.0, Z_BAR, wall, roofd)
    ring_band("bar_parapet", front, Z_BAR, Z_CREST - 0.09, -PARAPET_T, 0.03, wall)
    # the parapet cap: a thin band standing slightly proud, and the only thing
    # that reaches Z_CREST
    ring_band("bar_cap", front, Z_CREST - 0.09, Z_CREST, -PARAPET_T - 0.05, 0.08, wall)

    # ------------------------------------------------ the street elevation
    e = edge_facing(front, FRONT_BEARING_DEG)
    _a, span, _t, _n = poly_edge(front, e)
    # s runs from the south-west (158 - 160) end toward the north-east (150) end
    assert 5.5 < span < 6.3, f"street edge {span:.2f} m - check the footprint"

    # entrance bay: recessed door under a small flat pale canopy
    opening("door", front, e, 0.58, 1.62, 0.0, 2.62, wall, ink, jamb=0.16, depth=0.30)
    opening("dslot", front, e, 0.18, 0.44, 1.70, 3.28, wall, glass, jamb=0.11, depth=0.20)
    face_panel("canopy", front, e, 1.06, rect_profile(1.94, 2.98, 3.16), 0.0, 0.56, trim)
    face_panel("numerals", front, e, 2.22, rect_profile(0.56, 3.30, 3.60), 0.0, 0.06, trim)

    # the pier between door bay and window, with two stacked black sconces
    for k, z in enumerate((2.35, 3.05)):
        face_panel(f"sconce{k}", front, e, 2.25, rect_profile(0.16, z, z + 0.34), 0.0, 0.20, ink)

    # the two sash fields - the whole facade
    sash_field("w1", front, e, 2.52, span - 0.16, Z_SILL, Z_HEAD, 6, 5, wall, glass, glow_warm)
    sash_field("w2", front, e, 0.26, span - 0.26, Z_SILL2, Z_HEAD2, 8, 4, wall, glass, glow_warm)

    # the 1990 parapet tie anchors
    for k, s in enumerate((1.30, span - 1.35)):
        face_panel(f"anchor{k}", front, e, s, star_profile(0.46, Z_BAR - 0.34), 0.0, 0.07, ink)

    # ------------------------------------------------ the Taber Place end
    er = edge_facing(rear, (FRONT_BEARING_DEG + 180.0) % 360.0)
    _ar, span_r, _tr, _nr = poly_edge(rear, er)
    sr = span_r / 2.0
    opening("veh", rear, er, sr - 1.75, sr + 1.75, 0.0, 3.45, wall, roofd, jamb=0.20, depth=0.24)

    # ------------------------------------------------ the shed roof monitors
    # A regular run stepping away from the street down the lot's long axis, with
    # the glazed face turned north-north-east. Regular spacing is deliberate: a
    # ragged run reads as noise from the app's downward camera, a regular one
    # reads as architecture.
    for k in range(7):
        v = 7.4 - k * 3.15
        u = 1.55 + (v - 7.4) * 0.2436       # the lot's drifting centreline
        uv_box(f"mon{k}", u, v, Z_MON0, Z_MON1, 4.20, 1.40, wall)
        uv_box(f"mon{k}_glass", u - 2.10, v, Z_MON0 + 0.20, Z_MON1 - 0.09, 0.18, 1.18, glass)
        uv_box(f"mon{k}_glow", u - 2.21, v, Z_MON0 + 0.26, Z_MON1 - 0.15, 0.04, 0.94, glow_cool)

    # a single restrained plant box near the step, where the real roof has it
    uv_box("plant", 4.55, 6.05, Z_SHED, Z_SHED + 0.62, 1.45, 1.00, wall)

    # Bevel budget: the two masses and the parapets carry the miniature read and
    # get the full 0.12/2. The mullion bars and glow shells are small, numerous
    # and would triple the triangle count for nothing at thumbnail size.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        n = obj.name
        if n.endswith(("_glow", "_fill")) or "_mv" in n or "_mh" in n:
            continue
        if n.startswith(("sconce", "anchor", "numerals", "canopy")) or n.endswith(
            ("_jl", "_jr", "_jt", "_jb", "_glass")
        ):
            bevel(obj, width=0.04, segments=1)
        else:
            bevel(obj, width=0.12, segments=2)

    return scene


def report():
    dg = bpy.context.evaluated_depsgraph_get()
    tris = 0
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    for o in objs:
        me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    print("[build] anchor lon/lat: -122.3948748 37.7813535 (footprint area centroid)")
    print(f"[build] South Park front heading: {FRONT_BEARING_DEG} deg true (ESE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "156-south-park.blend")
    glb = os.path.join(out, "156-south-park.glb")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    bpy.ops.export_scene.gltf(
        filepath=glb,
        export_format="GLB",
        export_apply=True,
        export_yup=True,
        use_selection=False,
        export_cameras=False,
        export_lights=False,
        export_animations=False,
        export_skins=False,
        export_morph=False,
        export_materials="EXPORT",
        export_image_format="NONE",
    )
    print(f"[build] wrote {blend}")
    print(f"[build] wrote {glb}")


if __name__ == "__main__":
    main()
