"""Deterministic Blender build of the SF-SIM miniature 370 Brannan Street.

    blender -b --python build_370_brannan.py -- [--out DIR]

Writes 370-brannan.blend and 370-brannan.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint centre (anchor lon -122.3938572,
lat 37.7807602), min Z = 0, parapet crest exactly 7.63 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured DataSF LiDAR footprint (mblr SF3775020), a clean 7.00 x 23.83 m
  rectangle sitting at 45 deg off the world axes like the whole SoMa grid. Four
  sub-600 mm survey-noise segments in the published ring are dropped — the tile
  bake simplifies at 0.6 m anyway;
* a two-storey stucco-over-wood-frame slab, 3.4x as deep as it is wide and
  LOWER than both its neighbours (7.63 m against 8.80 and 8.58). The proportion
  IS the recognition — this building has no other monumental quality;
* the identity feature: the framed front panel. A raised flat border — a
  pilaster at each end and a wide mid-band across the middle — enclosing the
  Brannan elevation, with the cobalt-blue door as the single saturated accent;
* a black steel-sash upper window band, deeply recessed, simplified from a
  ~4x3 pane grid to one panel with two mullions;
* blank flanks. Both long sides are party walls built hard against taller
  neighbours; inventing a window grid on them would be a straightforward lie;
* night state: the upper band lit as ONE continuous panel (on a 7 m frontage a
  scatter of lit windows is indistinguishable mush, and one lit loft floor over
  a dark shopfront is what the street actually looks like), plus a narrow spill
  at the door. Glow shells are thin and proud of the opaque glazing — the app
  renders _Glow in a separate layer that is ~12% alpha by day;
* a deliberately quiet roof for the app's downward camera: a parapet ring, two
  square skylights with tapered glass caps, one small roof light and a hatch.
  No HVAC, no penthouse, no masts — this is a small wood-frame building and its
  real roof is empty. The two skylights are what has to carry it.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF building footprint SF3775020 projected with the app's tangent
# projection and recentred on the footprint centre. CCW.
FOOTPRINT = [
    (-10.946, 5.907),
    (5.999, -10.863),
    (10.941, -5.901),
    (-5.994, 10.857),
]

# Edge index -> elevation. Outward normals verified against the survey.
EDGE_SW = 0      # 23.84 m, faces SW 224.7 deg — party wall, 372-374 Brannan
EDGE_FRONT = 1   # 7.00 m, faces SE 134.9 deg — Brannan Street
EDGE_NE = 2      # 23.82 m, faces NE  44.7 deg — party wall, 362-366 Brannan
EDGE_REAR = 3    # 7.00 m, faces NW 315.0 deg — Varney Place

Z_DECK = 7.05        # roof deck / top of the body (LiDAR median 7.07)
Z_CREST = 7.63       # parapet crest = LiDAR max 7.63 -> the bbox top
Z_BAND0, Z_BAND1 = 3.40, 4.50    # the framed mid-band that carries "370"
Z_WIN0, Z_WIN1 = 4.60, 6.45      # upper steel-sash band

FRAME_D = 0.10       # how far the raised front frame stands proud of the wall
FRAME_W = 0.55       # width of the frame's pilasters
PARAPET_T = 0.30     # parapet wall thickness

# Two deliberate palette extensions, both WARN-not-FAIL under the contract and
# both forced by the first render pass (see REPORT.md):
#   Toy_greige — the real wall is a mid warm gray. In palette Toy_stone the whole
#     building rendered as a cream slab with the Toy_trim frame invisible against
#     it, which loses the one composition this building has.
#   Toy_cobalt — palette Toy_navy (2c4a70) is within two points of Toy_glass
#     (2a4d73), so the door vanished into the storefront beside it. The real door
#     is a bright cobalt and it is this building's only saturated colour.
PALETTE_HEX = {
    "Toy_greige": "b0aa9e",
    "Toy_cobalt": "2f5fb0",
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_roofd": "45454a",
    "Toy_ink": "3a3530",
    "Toy_glass_Glow": "6f95b8",
    "Toy_cobalt_Glow": "6db3d9",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def poly_edge(i):
    """Edge i of FOOTPRINT: (origin, length, tangent unit, outward normal)."""
    a = FOOTPRINT[i]
    b = FOOTPRINT[(i + 1) % len(FOOTPRINT)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def offset_polygon(poly, d):
    """Miter offset of the convex CCW footprint; positive d moves outward."""
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
    """Miniature-style edge softening (style bible s.4). Width is capped at a
    third of the object's thinnest dimension: the applied frame panels here are
    only 100-160 mm thick and a flat 0.12 m bevel on those collapses opposing
    profiles into zero-area slivers even with clamp_overlap."""
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


def face_panel(name, edge, u_centre, profile, d0, d1, mat):
    """Closed prism of a (u, z) profile lying in the plane of wall `edge`,
    extruded outward from offset d0 to d1 along that wall's normal."""
    a, _length, t, n = poly_edge(edge)
    verts = []
    for d in (d0, d1):
        for du, z in profile:
            px = a[0] + t[0] * (u_centre + du) + n[0] * d
            py = a[1] + t[1] * (u_centre + du) + n[1] * d
            verts.append((px, py, z))
    npts = len(profile)
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0):
    """Box with local +x along yaw and local +y 90 deg ccw of it."""
    c, s = math.cos(yaw), math.sin(yaw)
    corners = []
    for lx, ly in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)):
        corners.append((cx + lx * c - ly * s, cy + lx * s + ly * c))
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


def tapered_box(name, cx, cy, z0, z1, sx, sy, inset, mat, yaw=0.0):
    """Box whose top face is `inset` smaller on every side — the skylight cap.
    A real pyramid would set the crest on a 12-triangle spike nobody can see at
    city scale; a shallow frustum reads as glazing from the app's camera."""
    c, s = math.cos(yaw), math.sin(yaw)

    def quad(hx, hy):
        out = []
        for lx, ly in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)):
            out.append((cx + lx * c - ly * s, cy + lx * s + ly * c))
        return out

    lo = quad(sx / 2, sy / 2)
    hi = quad(max(sx / 2 - inset, 0.05), max(sy / 2 - inset, 0.05))
    verts = [(x, y, z0) for x, y in lo] + [(x, y, z1) for x, y in hi]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


def roof_box(name, u, v, z0, z1, su, sv, mat, taper=None):
    """Box on the roof, aligned to the building's own grid rather than to the
    world axes: u runs along the Brannan edge from its SW end, v runs INTO the
    block (against the outward normal)."""
    origin, _l, t, n = poly_edge(EDGE_FRONT)
    cx = origin[0] + t[0] * u - n[0] * v
    cy = origin[1] + t[1] * u - n[1] * v
    yaw = math.atan2(t[1], t[0])
    if taper is None:
        return box(name, cx, cy, z0, z1, su, sv, mat, yaw=yaw)
    return tapered_box(name, cx, cy, z0, z1, su, sv, taper, mat, yaw=yaw)


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


def rect_opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None, base=0.0):
    """Frame panel + a smaller fill that protrudes further, so the frame reads
    as a border ring around a recessed opening. No booleans, all closed solids."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), base, base + 0.07, frame_mat)
    inset = 0.16
    face_panel(
        f"{tag}_fill",
        edge,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        base,
        base + 0.13,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.28
        face_panel(
            f"{tag}_glow",
            edge,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            base + 0.10,
            base + 0.17,
            glow_mat,
        )


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    greige = material("Toy_greige")
    stone = material("Toy_stone")
    trim = material("Toy_trim")
    cobalt = material("Toy_cobalt")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    roofd = material("Toy_roofd")
    ink = material("Toy_ink")
    gglow = material("Toy_glass_Glow")
    nglow = material("Toy_cobalt_Glow")

    # --- stucco body: its top cap IS the roof deck --------------------------
    prism("body", FOOTPRINT, 0.0, Z_DECK, greige, mat_caps=roofd)

    # --- parapet ring -------------------------------------------------------
    # Plain, no coping course: the real parapet is a bare stucco upstand and
    # adding a cap band would give this building an ornament it does not have.
    # This ring sets the 7.63 m crest and therefore the loader's scale.
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_CREST, -PARAPET_T, 0.0, greige)

    # --- the framed front panel: the whole identity of the building ---------
    _a_f, len_f, _t_f, _n_f = poly_edge(EDGE_FRONT)
    for tag, u in (("sw", FRAME_W / 2.0), ("ne", len_f - FRAME_W / 2.0)):
        face_panel(
            f"frame_pier_{tag}",
            EDGE_FRONT,
            u,
            rect_profile(FRAME_W, 0.0, Z_DECK),
            0.0,
            FRAME_D,
            trim,
        )
    face_panel(
        "frame_band",
        EDGE_FRONT,
        len_f / 2.0,
        rect_profile(len_f, Z_BAND0, Z_BAND1),
        0.0,
        FRAME_D,
        trim,
    )
    # The painted "370" numerals on the band's SW end are NOT modelled: the
    # contract forbids textures and glyph geometry at 7 m frontage is sub-pixel
    # noise. The band that carries them is the cue that survives (plan 2.6).

    # --- Brannan front, ground floor ---------------------------------------
    # The cobalt door is the only saturated colour on this block face and the
    # single strongest cue at thumbnail size — it gets its own trim surround so
    # it does not dissolve into the dark storefront beside it.
    rect_opening("door", EDGE_FRONT, 1.32, 1.05, 0.0, 2.75, trim, cobalt, nglow)
    rect_opening("store", EDGE_FRONT, 4.40, 3.90, 0.35, 3.20, ink, glass)

    # --- Brannan front, upper floor: one steel-sash band, two mullions ------
    rect_opening("upper", EDGE_FRONT, 3.50, 5.30, Z_WIN0, Z_WIN1, ink, glass, gglow)
    for i, du in enumerate((-1.60, 0.0, 1.60)):
        face_panel(
            f"mullion{i}",
            EDGE_FRONT,
            3.50 + du,
            rect_profile(0.10, Z_WIN0 + 0.16, Z_WIN1 - 0.16),
            0.0,
            0.20,
            ink,
        )

    # --- Varney Place rear: INFERRED (no imagery found — see REPORT.md) ------
    # Kept to the minimum a 1937 wood-frame back wall must have, so that if the
    # real elevation ever surfaces the correction is small.
    rect_opening("rdoor", EDGE_REAR, 1.60, 1.10, 0.0, 2.30, greige, roofd)
    for i, u in enumerate((3.60, 5.40)):
        rect_opening(f"rwin{i}", EDGE_REAR, u, 0.90, 4.90, 5.80, greige, glass)

    # --- flanks: blank. Both are party walls against taller neighbours. -----

    # --- roof: quiet by nature, so the two skylights have to carry it -------
    # u runs along the Brannan edge from its SW end, v goes back into the block.
    roof_box("rooflight", 3.50, 5.20, Z_DECK, Z_DECK + 0.25, 1.60, 1.00, glassl)
    for i, v in enumerate((8.40, 14.60)):
        roof_box(f"skylight_kerb{i}", 3.50, v, Z_DECK, Z_DECK + 0.20, 2.60, 2.60, stone)
        roof_box(
            f"skylight{i}", 3.50, v, Z_DECK + 0.16, Z_DECK + 0.50, 2.40, 2.40, glassl, taper=0.45
        )
    roof_box("roof_hatch", 2.20, 17.00, Z_DECK, Z_DECK + 0.45, 1.10, 0.90, roofd)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.12/2. Applied panels are thin — their frames get a token 1-segment
    # softening and the fills/glow shells none at all.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")) or obj.name.startswith("mullion"):
            continue
        if obj.name.endswith("_frame") or obj.name.startswith("frame_"):
            bevel(obj, width=0.05, segments=1)
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
    print("[build] anchor lon/lat: -122.3938572 37.7807602 (footprint centre)")
    print("[build] Brannan front heading: 134.9 deg true (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "370-brannan.blend")
    glb = os.path.join(out, "370-brannan.glb")
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
