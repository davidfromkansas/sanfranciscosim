"""Deterministic Blender build of the SF-SIM miniature 501 Third Street.

    blender -b --python build_501_third.py -- [--out DIR]

Writes 501-third.blend and 501-third.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint vertex centroid (anchor lon -122.3954601,
lat 37.7813246), min Z = 0, rooftop bulkhead crest exactly 16.40 m.

Design (see REFERENCE.md for the sources behind every number):

* the OSM rhombus (way/147689541) extruded as a three-storey painted-masonry
  industrial loft on the 45° SoMa grid — a diamond, not a rectangle. The
  building fills its lot, so only the 3rd Street face (NE, 25.09 m) is a true
  street front; the other three faces are plainer party/rear walls;
* the identity is the WINDOW GRID: two upper bands of large recessed industrial
  windows on the 3rd Street face, the SoMa loft type — walls that are more
  window than wall;
* the two-tone base/body split: a dark (Toy_ink) storefront ground floor under
  a warm-sand painted upper block — the single strongest value contrast;
* the one silhouette event is the ROOFTOP BULKHEAD, a 4 × 3 m box at the crest
  (16.4 m) — the stair/elevator head converted to a mechanical room (2011),
  corroborated by the LiDAR hgt_max of 16.42 m;
* the roof is a pale grey membrane field with the bulkhead, a smaller
  accessories box (2010 permit), a roof deck guardrail (2006 permit), and one
  mechanical unit (2019 VRF);
* night state is restrained: the storefront uplight plus two lit upper windows.
  A working SoMa loft reads as quietly lit, not as a beacon. Glow surfaces are
  thin shells proud of opaque glazing — the app renders _Glow in a separate
  layer at ~12% alpha by day, so a primary surface must never be authored as
  glow.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way/147689541 projected with the app's tangent projection
# (LON0 -122.4375, LAT0 37.77) and recentred on the vertex centroid.
# CCW, (x east, y north). A true rhombus (parallelogram): 23.6 x 25.05 m, 592 m2.
FOOTPRINT = [
    (+0.354, -17.175),   # 0  S  south corner  (SE party / SW party)
    (+17.267, -0.660),   # 1  E  east corner   (SE party / 3rd St front)
    (-0.385, +17.170),   # 2  N  north corner  (3rd St front / NW party)
    (-17.236, +0.666),   # 3  W  west corner   (NW party / SW party)
]
# Edge roles CORRECTED 18 August 2026 against the bake's own street centrelines
# (pipeline/data/streets_datasf.geojson) and the neighbouring DataSF footprints.
# The plan and the first build had this 180 deg out: they put the 3rd Street
# elevation on the NE face, which is the mid-block PARTY wall. Measured
# perpendicular offsets from this anchor, and the method reproduces shipped
# 500 Third's documented orientation exactly as a control:
#
#     3rd Street     bearing 225.2 deg, 24.1 m   -> the SW face
#     Bryant Street  bearing 315.2 deg, 23.5 m   -> the NW face
#     Taber Place    bearing 135.1 deg, 17.0 m   -> the SE face (alley)
#     NE face        no street; DataSF SF3775075 (h 14.90 m) abuts, centroid
#                    bearing 42 deg at 21.8 m    -> the party wall
#
# So this is a CORNER building on 3rd and Bryant with an alley flank, not a
# one-street building with three party walls. See REFERENCE.md "Orientation".
E_THIRD = (3, 0)   # SW face, 25.05 m, outward normal 225.4 deg — 3rd STREET front
E_BRYANT = (2, 3)  # NW face, 23.59 m, outward normal 315.6 deg — BRYANT STREET
E_TABER = (0, 1)   # SE face, 23.64 m, outward normal 135.7 deg — TABER PLACE alley
E_PARTY = (1, 2)   # NE face, 25.09 m, outward normal 45.3 deg — blind party wall

L_THIRD = 25.05
L_BRYANT = 23.59
L_TABER = 23.64
L_PARTY = 25.09

H_WALL = 13.80   # top of the wall shell / underside of the parapet
H_ROOF = 13.90   # roof membrane surface (LiDAR median 13.73 m)
H_PAR = 13.90    # parapet base
H_PAR_CAP = 14.00  # parapet coping top = main parapet height
H_BULK = 16.40   # bulkhead crest = target height / bbox top

# Three storeys: tall ground floor (storefront/gallery) + two upper office floors
Z_SHOP_SILL = 0.20
Z_SHOP_HEAD = 3.60
Z_FASCIA_TOP = 4.50
Z_F2_SILL = 5.30
Z_F2_HEAD = 8.80
Z_F3_SILL = 9.80
Z_F3_HEAD = 13.00

BEVEL_W = 0.10
BEVEL_SEG = 2

PALETTE_HEX = {
    "Toy_sand": "ece4d4",
    "Toy_ink": "3a3530",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_trim": "f3efe6",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_white_Glow": "f7f4ec",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def poly_edge(edge):
    """(a, b, length, tangent unit, outward normal) for a CCW footprint edge."""
    a, b = FOOTPRINT[edge[0]], FOOTPRINT[edge[1]]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> this points outward
    return a, b, length, t, n


def offset_polygon(poly, d):
    """Miter offset of a CCW polygon; positive d moves outward."""
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


# The building's own axes: U runs along the 3rd Street face from the west corner
# toward the south corner, W runs along the Taber Place face from the south
# corner toward the east corner. Roof objects are laid out in this frame.
def _axes():
    _, _, _, t_third, _ = poly_edge(E_THIRD)
    _, _, _, t_taber, _ = poly_edge(E_TABER)
    return t_third, t_taber


U, W = _axes()


def uw(u, w):
    return (U[0] * u + W[0] * w, U[1] * u + W[1] * w)


def uw_rect(u, w, su, sw):
    """Four CCW plan corners of a rectangle in the building frame."""
    return [
        uw(u - su / 2, w - sw / 2),
        uw(u + su / 2, w - sw / 2),
        uw(u + su / 2, w + sw / 2),
        uw(u - su / 2, w + sw / 2),
    ]


def signed_area(poly):
    n = len(poly)
    return sum(
        poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1]
        for i in range(n)
    ) / 2.0


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


def bevel(obj, width=BEVEL_W, segments=BEVEL_SEG):
    """Miniature-style edge softening on the chunky solids (style bible s.4)."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.bevel(
        bm,
        geom=list(bm.verts) + list(bm.edges),
        offset=width,
        segments=segments,
        profile=0.5,
        affect="EDGES",
        clamp_overlap=True,
    )
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


def ring_band(name, z0, z1, off_in, off_out, mat, poly=None):
    """Closed band following a polygon: 4 loops, quads between."""
    base = poly if poly is not None else FOOTPRINT
    lo_in = offset_polygon(base, off_in)
    lo_out = offset_polygon(base, off_out)
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


def quad_box(name, corners, z0, z1, mat):
    """Closed box from four CCW plan corners."""
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


def wall_box(name, edge, s0, s1, z0, z1, d_in, d_out, mat):
    """Box hung on a facade: s along the edge from its first vertex, d measured
    along the outward normal (negative = recessed into the wall)."""
    a, _, _, t, n = poly_edge(edge)

    def p(s, d):
        return (a[0] + t[0] * s + n[0] * d, a[1] + t[1] * s + n[1] * d)

    return quad_box(name, [p(s0, d_in), p(s1, d_in), p(s1, d_out), p(s0, d_out)], z0, z1, mat)


def uw_box(name, u, w, z0, z1, su, sw, mat):
    """Box centred at (u, w) in the building frame, su along U, sw along W."""
    return quad_box(name, uw_rect(u, w, su, sw), z0, z1, mat)


# ------------------------------------------------------------------- the build


def materials():
    mats = {}
    for name, rgb in PALETTE.items():
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        bsdf = m.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.85
        bsdf.inputs["Metallic"].default_value = 0.0
        if name.endswith("_Glow"):
            bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 0.0
        mats[name] = m
    return mats


def punched_window(tag, edge, s0, s1, z0, z1, mats, lit=False):
    """Upper-storey opening: a Toy_trim reveal with a Toy_glass pane set into it.
    Built PROUD of the wall — the shell is a solid prism with no cut openings, so
    anything at negative depth is buried inside it and invisible. The apparent
    recess comes from the reveal standing 0.10 m out in front of the pane (style
    bible s.5: windows are graphical elements before they are literal openings)."""
    wall_box(f"{tag}_reveal", edge, s0, s1, z0, z1, 0.0, 0.10, mats["Toy_trim"])
    wall_box(f"{tag}_glass", edge, s0 + 0.14, s1 - 0.14, z0 + 0.14, z1 - 0.14,
             0.06, 0.14, mats["Toy_glass"])
    if lit:
        wall_box(f"{tag}_glow", edge, s0 + 0.20, s1 - 0.20, z0 + 0.20, z1 - 0.20,
                 0.145, 0.165, mats["Toy_white_Glow"])


def shopfront(tag, edge, s0, s1, mats, bays, lit_bays=None):
    """A run of the dark storefront base: recessed glazing under a proud Toy_ink
    fascia. `lit_bays` is the set of bay indices that carry night glow; the rest
    stay dark glass. Default: every bay."""
    wall_box(f"{tag}_back", edge, s0, s1, 0.0, Z_FASCIA_TOP, 0.0, 0.04, mats["Toy_ink"])
    bevel(wall_box(f"{tag}_fascia", edge, s0, s1, Z_SHOP_HEAD + 0.14, Z_FASCIA_TOP,
                   0.0, 0.20, mats["Toy_ink"]), width=0.04)
    wall_box(f"{tag}_glass", edge, s0 + 0.10, s1 - 0.10, Z_SHOP_SILL, Z_SHOP_HEAD,
             0.03, 0.11, mats["Toy_glass"])
    span = s1 - s0
    for k in range(1, bays):
        s = s0 + span * k / bays
        wall_box(f"{tag}_mull{k}", edge, s - 0.07, s + 0.07, Z_SHOP_SILL, Z_SHOP_HEAD,
                 0.10, 0.17, mats["Toy_ink"])
    lit = range(bays) if lit_bays is None else lit_bays
    for k in lit:
        g0 = s0 + span * k / bays + 0.45
        g1 = s0 + span * (k + 1) / bays - 0.45
        wall_box(f"{tag}_glow{k}", edge, g0, g1, Z_SHOP_SILL + 0.55,
                 Z_SHOP_HEAD - 0.45, 0.115, 0.135, mats["Toy_white_Glow"])


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    mats = materials()

    sand = mats["Toy_sand"]
    ink = mats["Toy_ink"]
    glass = mats["Toy_glass"]
    glassl = mats["Toy_glassl"]
    trim = mats["Toy_trim"]
    roofd = mats["Toy_roofd"]
    steel = mats["Toy_steel"]

    # ---- 1. body prism: the rhombus extruded to the parapet ---------------- #
    bevel(prism("body", FOOTPRINT, 0.0, H_WALL, sand), width=0.12)

    # ---- 2. roof field ----------------------------------------------------- #
    # Toy_steel (9aa0a6), NOT Toy_roofd (45454a): an up-facing Toy_roofd plane
    # measures rgb(9,9,12) in the running app at 1 PM -- black -- while the same
    # asset's Toy_steel reads rgb(94,103,112) in the same frame (measured on
    # 92 South Park, 2026-08-17). The dossier calls this roof a PALE grey
    # membrane; Toy_roofd stays on the small dark rooftop props only.
    prism("roof_field", offset_polygon(FOOTPRINT, -0.30), H_WALL, H_ROOF, steel)

    # ---- 3. parapet -------------------------------------------------------- #
    bevel(ring_band("parapet", H_WALL, H_PAR, -0.30, 0.0, sand), width=0.05)
    bevel(ring_band("parapet_cap", H_PAR, H_PAR_CAP, -0.38, 0.08, ink), width=0.04)

    # ---- 4. storefront base, wrapping the 3rd/Bryant corner --------------- #
    # The dark ground-floor band. A 1920 corner loft carries its shopfront round
    # the corner onto the secondary street, so the band runs the full 3rd Street
    # face (5 bays, the gallery front) and continues along Bryant (4 bays), with
    # the pier between them left solid so the corner reads as masonry.
    # Night restraint (style bible: hero glow + supporting accents, not a
    # beacon). The gallery front on 3rd Street is the hero and lights all five
    # bays; Bryant keeps the same shopfront band but lights only the two bays
    # nearest the corner, so the corner reads lit and the secondary street
    # tails off into dark glass. E_BRYANT runs north corner -> west corner, so
    # bays 2 and 3 are the ones at the 3rd Street corner.
    shopfront("shop_t", E_THIRD, 1.20, L_THIRD - 1.20, mats, bays=5)
    shopfront("shop_b", E_BRYANT, 1.20, L_BRYANT - 1.20, mats, bays=4,
              lit_bays=(2, 3))
    # the recessed entry door, on 3rd Street (the address face) only
    ent_s = L_THIRD * 0.45
    wall_box("ent_door", E_THIRD, ent_s, ent_s + 1.30, 0.0, 2.60, 0.02, 0.09, glass)
    bevel(wall_box("ent_jamb0", E_THIRD, ent_s - 0.16, ent_s, 0.0, 2.80, 0.02, 0.18, ink),
          width=0.04)
    bevel(wall_box("ent_jamb1", E_THIRD, ent_s + 1.30, ent_s + 1.46, 0.0, 2.80, 0.02, 0.18, ink),
          width=0.04)

    # ---- 5. upper window grid on the two street elevations ---------------- #
    # The identity: two bands of large steel-sash industrial windows. 5 bays on
    # 3rd Street (25.05 m) and 4 on Bryant (23.59 m), at a near-identical bay
    # pitch, so the grid turns the corner instead of stopping at it. One lit
    # window per street at night.
    for tag, edge, length, nbays, lit2, lit3 in (
        ("t", E_THIRD, L_THIRD, 5, 2, None),
        ("b", E_BRYANT, L_BRYANT, 4, None, 3),
    ):
        pitch = (length - 2.40) / nbays
        bay_w = min(3.20, pitch - 1.30)
        for k in range(nbays):
            s0 = 1.20 + k * pitch + (pitch - bay_w) / 2
            punched_window(f"{tag}_f2_{k}", edge, s0, s0 + bay_w, Z_F2_SILL, Z_F2_HEAD,
                           mats, lit=(k == lit2))
            punched_window(f"{tag}_f3_{k}", edge, s0, s0 + bay_w, Z_F3_SILL, Z_F3_HEAD,
                           mats, lit=(k == lit3))

    # ---- 6. Taber Place: the alley flank ---------------------------------- #
    # Exposed to a 12 m alley, not to a street: no shopfront, punched windows
    # only, and this is where the stair/elevator shaft shows (the 2011 permit
    # re-surfaced it from outside, which an alley allows and a party wall does
    # not).
    for k, s0 in enumerate((3.0, 9.0, 15.0, 20.2)):
        punched_window(f"tb_f2_{k}", E_TABER, s0, s0 + 2.20, Z_F2_SILL, Z_F2_HEAD, mats)
        punched_window(f"tb_f3_{k}", E_TABER, s0, s0 + 2.20, Z_F3_SILL, Z_F3_HEAD, mats)

    # ---- 7. stair/elevator shaft bump on the Taber Place flank ------------- #
    # A slight projection (re-surfaced 2011) — one small box proud of the wall
    wall_box("shaft_bump", E_TABER, 12.6, 16.6, 0.0, H_WALL, 0.0, 0.50, sand)

    # ---- 7b. the NE party wall stays blind -------------------------------- #
    # DataSF SF3775075 (14.90 m) abuts this face and the building fills its lot,
    # so anything modelled here would be buried inside the neighbour up to 14.9 m
    # of a 13.8 m wall. Blind painted masonry is both the truth and free.

    # ---- 8. the working roof ----------------------------------------------- #
    # The bulkhead: the crest at 16.4 m. Its coping is four thin bars around the
    # top edge, NOT a lid: a full-plan cap box reads from directly above as a
    # black hole punched in the roof.
    bevel(uw_box("bulkhead", -3.0, 2.0, H_ROOF, H_BULK - 0.15, 4.00, 3.00, roofd),
          width=0.08)
    for k, (du, dw, su, sw) in enumerate(((0, -1.47, 4.16, 0.16), (0, 1.47, 4.16, 0.16),
                                          (-2.08, 0, 0.16, 2.72), (2.08, 0, 0.16, 2.72))):
        bevel(uw_box(f"bulk_cope{k}", -3.0 + du, 2.0 + dw, H_BULK - 0.15,
                     H_BULK, su, sw, ink), width=0.04)

    # The accessories box (2010 permit): a smaller rooftop structure
    bevel(uw_box("access_box", 5.0, -4.0, H_ROOF, H_ROOF + 1.50, 3.00, 2.00, roofd),
          width=0.06)

    # Roof deck guardrail (2006 permit): a low steel rail along the SE roof edge
    rail_off = offset_polygon(FOOTPRINT, -1.20)
    npts = len(rail_off)
    rail_verts = []
    for loop, z in ((rail_off, H_ROOF), (rail_off, H_ROOF + 1.10)):
        rail_verts.extend([(x, y, z) for x, y in loop])
    rail_faces = []
    for i in range(npts):
        j = (i + 1) % npts
        rail_faces.append((i, j, npts + j, npts + i))
    new_mesh("guardrail", rail_verts, rail_faces, [steel])

    # One mechanical unit (2019 VRF system)
    bevel(uw_box("mech_unit", 6.0, 4.0, H_ROOF, H_ROOF + 0.80, 1.50, 1.00, steel),
          width=0.05)

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
        o.evaluated_get(dg).to_mesh_clear()
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] footprint area={abs(signed_area(FOOTPRINT)):.1f} m2")
    print("[build] anchor lon/lat: -122.3954601 37.7813246 (vertex centroid)")
    print("[build] 3rd Street front normal 225.4 deg true (SW face);"
          " Bryant 315.6, Taber Place 135.7, party wall 45.3")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "501-third.blend")
    glb = os.path.join(out, "501-third.glb")
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
