"""Deterministic Blender build of the SF-SIM miniature 334 Brannan Street.

    blender -b --python build_334_brannan.py -- [--out DIR]

Writes 334-brannan.blend and 334-brannan.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint centroid (anchor lon -122.3930344,
lat 37.7814147), min Z = 0, pier-cap crest exactly 13.40 m.

Design (see REFERENCE.md for the sources behind every number):

* the surveyed parcel polygon 3775101 (identical to OSM way 71211341), a
  near-perfect 21.08 x 21.13 m SQUARE standing on a corner at ~45 deg off the
  world axes like the whole SoMa grid, covering its entire lot;
* a three-storey REINFORCED-CONCRETE box (1929, "Sherman and Clay", a
  contributor to the South End Historic District) — not the brick of the older
  buildings further southwest;
* the identity feature: the GILDED CREST — a band of gold frieze ornament across
  the top of every bay and a gold capital block on the head of every pier. It is
  the only gold on this block face and the reason the building is a contributor;
* the two-tone paint: a WARM GREIGE structural frame (piers, bands, surrounds)
  with SAGE-GREEN recessed panels, parapet field, roll-up leaf and entry tower.
  Reversing those two turns the building into a green box and loses it among its
  neighbours — the first aerial review render of this asset did exactly that;
* six bays of tall steel industrial sash over a very wide roll-up freight door;
* an ENTRY TOWER at the northeast end carrying a round-headed portal, the
  vertical 334 plate and two pale-pink Deco panels under their own gilt caps;
* an EXPOSED northeast flank — 326 Brannan next door is a one-storey building set
  back from the street, so this elevation reads from the sidewalk, with the JAX
  Vineyards garden's living wall against its base;
* night state: the gold frieze lit as the hero, a restrained scatter of lit
  windows and a warm lamp over the portal. Glow surfaces are thin shells proud of
  the opaque surface behind them (the app renders _Glow in a separate layer that
  is ~12% alpha by day — never author a primary surface as glow);
* a designed roof for the app's downward camera: a light membrane deck, the USED
  roof deck the leasing copy sells (tables, planters), a low stair bulkhead,
  skylights and mechanical clutter — all of it kept BELOW the 13.10 m parapet,
  which is why no street photograph shows any of it.

Documented deviation from docs/asset-plans/334-brannan.md §2.7: the plan called
for a full-width greige "Brannan skin" panel with sage recesses cut into it. A
recess cannot be cut out of an applied skin without booleans, so the BODY carries
the greige and the sage recesses are applied flush on it, with the piers and
bands standing proud between them. Same photographed result, fewer parts. The
northeast flank, which is genuinely painted sage, gets its own applied skin.
See REPORT.md.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF parcel polygon 3775101 (== OSM way 71211341) projected with the app's
# tangent projection and recentred on the footprint centroid. CCW, starting at
# the SOUTH corner so edge 0 runs S -> E along Brannan Street. A fifth surveyed
# vertex at (7.30, 7.66) lies 0.03 m off the straight N->E edge and is dropped
# as survey noise.
FOOTPRINT = [
    (-0.04, -15.17),   # S corner  — southwest end of the Brannan frontage
    (14.89, -0.28),    # E corner  — northeast end of the Brannan frontage
    (0.04, 15.17),     # N corner
    (-14.88, 0.22),    # W corner
]

# Edge index -> elevation. Outward normals verified against the survey.
EDGE_FRONT = 0   # 21.08 m, faces SE 135.1 deg — Brannan Street, the hero
EDGE_NE = 1      # 21.43 m, faces NE  46.1 deg — exposed flank over 326's garden
EDGE_NW = 2      # 21.12 m, faces NW 314.9 deg — rear, block interior
EDGE_SW = 3      # 21.38 m, faces SW 226.1 deg — party wall against 340, blind

Z_DECK = 12.15       # roof deck / top of the body (LiDAR median 12.14)
Z_FRIEZE_A = 12.30   # gold frieze band, bottom
Z_FRIEZE_B = 12.95   # gold frieze band, top = parapet coping underside
Z_PARAPET = 13.10    # parapet coping crest (inferred: deck + 0.95 m)
Z_CREST = 13.40      # gold pier caps = the bbox top
Z_G_TOP = 4.20       # head of the roll-up freight door
Z_BAND_A = 4.30      # ground-floor lintel band
Z_BAND_B = 4.75
Z_W2A, Z_W2B = 5.10, 8.10    # middle-floor window band
Z_W3A, Z_W3B = 8.60, 11.60   # top-floor window band (taller sill-to-head reveal)

SKIN = 0.10          # applied-panel standoff from the wall plane
PARAPET_T = 0.35     # parapet wall thickness

# Brannan frontage layout, u measured from the SOUTHWEST end of edge 0.
MAIN_END = 16.50               # main block / entry tower division
BAY_U = [1.75, 4.45, 7.15, 9.85, 12.55, 15.25]     # six bay centres, pitch 2.70
PIER_U = [0.40, 3.10, 5.80, 8.50, 11.20, 13.90, 16.60]  # seven piers
TOWER_U = 18.79                # entry tower centre
TOWER_W = 4.58
PINK_U = [17.85, 19.73]        # the two pale-pink Deco panels / their gilt caps

PALETTE_HEX = {
    # The painted concrete. The recessed field is the sage; the applied frame
    # is the warm greige. Photographed May 2025, both tones repainted.
    "Toy_sage": "8f9b86",
    "Toy_stone": "d9d2c2",   # piers, bands, surrounds — the applied frame
    "Toy_cream": "f2ede3",   # roof membrane (re-roofed 2010), bulkhead
    "Toy_trim": "f3efe6",    # parapet coping, skylight kerbs, deck tables, plate
    "Toy_gold": "c9a227",    # THE IDENTITY: frieze band and pier caps
    "Toy_pink": "e8b3ae",    # the two entry-tower accent panels
    "Toy_glass": "2a4d73",   # steel-sash windows
    "Toy_glassl": "6f95b8",  # skylights
    "Toy_ink": "3a3530",     # window frames, portal, door reveals
    "Toy_roofd": "45454a",   # service door, roof hatch, roll-up door leaf
    "Toy_steel": "9aa0a6",   # mechanical block and duct
    "Toy_leaf": "5b7347",    # living wall on the NE flank, roof planters
    # Glow colours are the LIT appearance and must equal the day colour of the
    # non-glow neighbour behind them, or the night pass reads as a hole.
    "Toy_gold_Glow": "c9a227",
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


def arch_profile(w, z0, z_spring, rise, seg=5):
    """Closed (u, z) profile: rectangle with a segmental arched head."""
    a = w / 2.0
    pts = [(-a, z0), (a, z0), (a, z_spring)]
    if rise > 1e-4:
        radius = (a * a + rise * rise) / (2.0 * rise)
        cz = z_spring + rise - radius
        th0 = math.atan2(z_spring - cz, a)
        th1 = math.pi - th0
        for k in range(1, seg):
            th = th0 + (th1 - th0) * k / seg
            pts.append((radius * math.cos(th), cz + radius * math.sin(th)))
    pts.append((-a, z_spring))
    return pts


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
    """Miniature-style edge softening on the chunky solids (style bible s.4).

    Width is capped at a third of the object's thinnest dimension; the applied
    panels here are 60-280 mm thick and a flat 0.12 m bevel on those relies
    entirely on clamp_overlap, which collapses opposing profiles into zero-area
    slivers. remove_doubles/dissolve_degenerate at 1 mm sweeps up whatever
    clamping still pinches shut (same tolerance the optimize pass welds at).
    """
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
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-3)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-3, edges=list(bm.edges))
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


def roof_box(name, u, v, z0, z1, su, sv, mat):
    """Box on the roof, aligned to the building's own grid rather than to the
    world axes: u runs along the Brannan edge from its SW end, v runs INTO the
    block (against the outward normal)."""
    origin, _l, t, n = poly_edge(EDGE_FRONT)
    cx = origin[0] + t[0] * u - n[0] * v
    cy = origin[1] + t[1] * u - n[1] * v
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=math.atan2(t[1], t[0]))


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
    as a border ring around a recessed opening. No booleans, all closed solids.
    `base` lifts both off the wall when the opening sits on an applied panel."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), base, base + SKIN + 0.04, frame_mat)
    inset = 0.17
    face_panel(
        f"{tag}_fill",
        edge,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        base,
        base + SKIN + 0.11,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.31
        face_panel(
            f"{tag}_glow",
            edge,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            base + SKIN + 0.08,
            base + SKIN + 0.15,
            glow_mat,
        )


def arched_opening(tag, edge, u, w, z0, z_spring, rise, frame_mat, fill_mat, base=0.0):
    face_panel(
        f"{tag}_frame", edge, u, arch_profile(w, z0, z_spring, rise),
        base, base + SKIN + 0.06, frame_mat,
    )
    inset = 0.26
    face_panel(
        f"{tag}_fill",
        edge,
        u,
        arch_profile(w - 2 * inset, z0 + inset, z_spring, max(rise - 0.08, 0.0)),
        base,
        base + SKIN + 0.14,
        fill_mat,
    )


# Which upper-floor bays are lit at night. Restrained: five windows across two
# floors of the one elevation that faces a street.
LIT_MID = {1, 4}
LIT_TOP = {0, 3, 5}


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    sage = material("Toy_sage")
    stone = material("Toy_stone")
    cream = material("Toy_cream")
    trim = material("Toy_trim")
    gold = material("Toy_gold")
    pink = material("Toy_pink")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    ink = material("Toy_ink")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    leaf = material("Toy_leaf")
    gold_glow = material("Toy_gold_Glow")
    glass_glow = material("Toy_glass_Glow")

    len_f = poly_edge(EDGE_FRONT)[1]
    len_ne = poly_edge(EDGE_NE)[1]
    len_nw = poly_edge(EDGE_NW)[1]

    # --- painted concrete body; its top cap IS the roof membrane ------------
    # GREIGE is the structural frame and therefore the body colour; the SAGE
    # recessed panels are applied flush on top of it and the frame elements
    # (piers, bands, surrounds) stand proud between them. Reversing the two
    # loses the building among its neighbours (see the module docstring).
    prism("body", FOOTPRINT, 0.0, Z_DECK, stone, mat_caps=cream)

    # --- parapet ring + coping ---------------------------------------------
    # The parapet field is the sage the gold frieze sits on.
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_FRIEZE_B, -PARAPET_T, 0.0, sage)
    ring_band("coping", FOOTPRINT, Z_FRIEZE_B, Z_PARAPET, -PARAPET_T - 0.07, 0.07, stone)

    # === BRANNAN STREET (SE) — the hero elevation ===========================

    # --- the applied greige frame: seven piers and three horizontal bands ---
    # the recessed sage field of each bay, flush on the wall; the proud piers
    # and bands on either side are what make it read as a recess
    for i, u in enumerate(BAY_U):
        face_panel(f"recess{i}", EDGE_FRONT, u,
                   rect_profile(1.98, Z_BAND_B, Z_DECK), 0.0, 0.035, sage)
    for i, u in enumerate(PIER_U):
        face_panel(f"pier{i}", EDGE_FRONT, u, rect_profile(0.95, 0.0, Z_FRIEZE_A),
                   0.0, SKIN + 0.03, stone)
    # ground-floor lintel band, spandrel band between the two window floors,
    # and the band that carries the frieze; all stop at the entry tower.
    for tag, z0, z1, d in (
        ("band_grd", Z_BAND_A, Z_BAND_B, SKIN + 0.04),
        ("band_span", Z_W2B + 0.10, Z_W3A - 0.10, SKIN + 0.05),
        ("band_frieze", Z_DECK - 0.20, Z_FRIEZE_A, SKIN + 0.02),
    ):
        face_panel(tag, EDGE_FRONT, MAIN_END / 2.0,
                   rect_profile(MAIN_END - 0.10, z0, z1), 0.0, d, stone)
    # base plinth: the darker painted skirt the photographs show
    face_panel("plinth", EDGE_FRONT, MAIN_END / 2.0,
               rect_profile(MAIN_END - 0.10, 0.0, 0.45), 0.0, SKIN + 0.06, roofd)

    # --- six bays of steel industrial sash ----------------------------------
    for i, u in enumerate(BAY_U):
        rect_opening(f"fmid{i}", EDGE_FRONT, u, 2.15, Z_W2A, Z_W2B, ink, glass,
                     glass_glow if i in LIT_MID else None)
        rect_opening(f"ftop{i}", EDGE_FRONT, u, 2.15, Z_W3A, Z_W3B, ink, glass,
                     glass_glow if i in LIT_TOP else None)

    # --- ground floor: the wide roll-up freight door + two sash windows -----
    face_panel("rollup_surround", EDGE_FRONT, 5.90,
               rect_profile(11.10, 0.0, Z_G_TOP + 0.18), 0.0, SKIN + 0.06, stone)
    face_panel("rollup_leaf", EDGE_FRONT, 5.90,
               rect_profile(10.50, 0.10, Z_G_TOP), 0.0, SKIN + 0.13, sage)
    for i, u in enumerate((12.55, 15.25)):
        rect_opening(f"fgrd{i}", EDGE_FRONT, u, 1.85, 1.50, 3.90, ink, glass)

    # --- THE IDENTITY: the gilded crest -------------------------------------
    # One frieze panel per bay plus a gold capital block on every pier. The caps
    # set the bounding-box top and must land exactly on Z_CREST.
    for i, u in enumerate(BAY_U):
        face_panel(f"frieze{i}", EDGE_FRONT, u,
                   rect_profile(2.34, Z_FRIEZE_A, Z_FRIEZE_B), 0.0, 0.13, gold)
        # thin glow plate proud of the gold, never the gold itself
        face_panel(f"frieze{i}_glow", EDGE_FRONT, u,
                   rect_profile(2.20, Z_FRIEZE_A + 0.09, Z_FRIEZE_B - 0.09),
                   0.11, 0.17, gold_glow)
    for i, u in enumerate(PIER_U):
        face_panel(f"cap{i}", EDGE_FRONT, u,
                   rect_profile(1.02, Z_FRIEZE_B - 0.06, Z_CREST),
                   -PARAPET_T - 0.05, 0.26, gold)

    # === THE ENTRY TOWER (northeast end of the Brannan front) ===============
    face_panel("tower", EDGE_FRONT, TOWER_U,
               rect_profile(TOWER_W, 0.0, Z_CREST), -PARAPET_T - 0.05, 0.34, sage)
    face_panel("tower_coping", EDGE_FRONT, TOWER_U,
               rect_profile(TOWER_W + 0.16, Z_PARAPET - 0.18, Z_PARAPET),
               -PARAPET_T - 0.12, 0.42, stone)
    arched_opening("portal", EDGE_FRONT, TOWER_U + 0.55, 2.30, 0.0, 3.20, 0.38,
                   stone, ink, base=0.34)
    # warm lamp over the entrance: the only glow that is not gold frieze or sash
    face_panel("portal_lamp", EDGE_FRONT, TOWER_U + 0.55,
               rect_profile(1.40, 3.62, 3.88), 0.48, 0.55, gold_glow)
    # the vertical 334 plate, beside the portal
    face_panel("plate334", EDGE_FRONT, TOWER_U - 1.35,
               rect_profile(0.50, 2.30, 4.20), 0.34, 0.42, trim)
    for i, u in enumerate(PINK_U):
        face_panel(f"pink{i}", EDGE_FRONT, u,
                   rect_profile(0.58, 10.90, 12.70), 0.34, 0.42, pink)
        face_panel(f"pinkcap{i}", EDGE_FRONT, u,
                   rect_profile(0.78, 12.70, Z_CREST), 0.26, 0.44, gold)

    # === NORTHEAST FLANK — exposed over the 326 Brannan garden ==============
    # A plain painted wall (already sage) with the garden's living wall at its
    # base. No window rhythm is visible in any reference and none is invented.
    face_panel("ne_skin", EDGE_NE, len_ne / 2.0,
               rect_profile(len_ne - 0.20, 0.0, Z_DECK), 0.0, 0.04, sage)
    face_panel("living_wall", EDGE_NE, len_ne / 2.0 - 0.60,
               rect_profile(15.40, 0.40, 3.30), 0.04, 0.16, leaf)
    face_panel("ne_plinth", EDGE_NE, len_ne / 2.0,
               rect_profile(len_ne - 0.30, 0.0, 0.40), 0.0, SKIN, roofd)

    # === NORTHWEST REAR — block interior, no public vantage =================
    rect_opening("nwdoor", EDGE_NW, 4.00, 2.30, 0.0, 3.00, ink, roofd)
    face_panel("nw_band", EDGE_NW, len_nw / 2.0,
               rect_profile(len_nw - 0.30, Z_BAND_A, Z_BAND_B), 0.0, SKIN - 0.03, stone)

    # === ROOF — the surface the app's camera sees most ======================
    # u runs along the Brannan edge from its SW end, v goes back into the block
    # (the block is ~21.1 m deep). NOTHING here may exceed Z_PARAPET: the real
    # parapet hides all of it, which is why no street photograph shows a
    # bulkhead. The USED deck (tables + planters) sits in the Brannan half.
    # the deck: two tables with their chairs, read as one furnished group
    for i, (u, v) in enumerate(((6.60, 4.60), (10.90, 4.60))):
        roof_box(f"deck_table{i}", u, v, Z_DECK, Z_DECK + 0.74, 1.30, 1.30, trim)
        roof_box(f"deck_chair{i}a", u - 1.15, v, Z_DECK, Z_DECK + 0.48, 0.55, 0.55, steel)
        roof_box(f"deck_chair{i}b", u + 1.15, v, Z_DECK, Z_DECK + 0.48, 0.55, 0.55, steel)
    for i, u in enumerate((4.40, 8.75, 13.10)):
        roof_box(f"planter{i}", u, 7.30, Z_DECK, Z_DECK + 0.75, 1.70, 0.80, leaf)
    roof_box("bulkhead", 7.40, 16.10, Z_DECK, Z_DECK + 0.95, 4.20, 3.20, cream)
    for i, v in enumerate((11.40, 14.60)):
        roof_box(f"skylight_kerb{i}", 14.90, v, Z_DECK, Z_DECK + 0.20, 2.60, 1.60, trim)
        roof_box(f"skylight{i}", 14.90, v, Z_DECK + 0.16, Z_DECK + 0.42, 2.30, 1.30, glassl)
    roof_box("hvac", 12.20, 17.60, Z_DECK, Z_DECK + 1.00, 2.20, 1.60, steel)
    roof_box("duct", 10.10, 16.40, Z_DECK + 0.25, Z_DECK + 0.55, 0.70, 1.90, steel)
    roof_box("roof_hatch", 3.60, 12.60, Z_DECK, Z_DECK + 0.50, 1.50, 1.20, roofd)
    roof_box("vent_a", 3.20, 15.40, Z_DECK, Z_DECK + 0.90, 0.55, 0.55, steel)
    roof_box("vent_b", 17.30, 8.20, Z_DECK, Z_DECK + 0.85, 0.50, 0.50, steel)

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.12/2. Applied panels are small and numerous — frames get a token
    # 1-segment softening, fills and glow shells none, which is what keeps this
    # under the 9,000-triangle cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")):
            continue
        if obj.name.endswith("_frame") or obj.name.startswith(
            ("frieze", "cap", "pink", "band_", "pier", "plate", "portal_lamp", "recess", "ne_skin", "living_wall")
        ):
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
    print("[build] anchor lon/lat: -122.3930344 37.7814147 (footprint centroid)")
    print("[build] Brannan front heading: 135.1 deg true (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "334-brannan.blend")
    glb = os.path.join(out, "334-brannan.glb")
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
