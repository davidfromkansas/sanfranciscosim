"""Deterministic Blender build of the SF-SIM miniature 234 Van Ness Avenue
(The Kelsey Civic Center).

    blender -b --python build_234_van_ness.py -- [--out DIR]

Writes 234-van-ness.blend and 234-van-ness.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = footprint AABB centre (anchor
lon -122.4193071, lat 37.7780541), min Z = 0, mechanical-penthouse crest exactly
30.12 m.

Design (see REFERENCE.md and docs/asset-plans/234-van-ness.md for the sources
behind every number):

* the footprint is OSM ways 1547771521 + 1547771522 unioned (1,304 m², which
  agrees with the geotechnical report's 13,815 sq ft site to 1.6 %), then
  regularised to a clean rectilinear L in the building's own 80.75° grid — no
  vertex moves more than 0.30 m and the L is what the eye reads;
* every height comes off WRNS Studio's dimensioned SOUTH ELEVATION - TOM
  WADDELL: a 15'-0" ground floor, seven 9'-11" residential floors, roof at
  84'-5" (25.73 m), copper fascia to 87'-11" (26.80 m), mechanical penthouse to
  98'-10" (30.12 m);
* the identity is the open-air courtyard: calm white-and-charcoal striped street
  elevations outside, eight storeys of candy-coloured panel patchwork inside,
  visible only from the app's downward camera — which is the whole point;
* night state: the courtyard glows (floor wash + festoon), a third of the
  apartment bays are lit, the Van Ness lobby is lit. Nothing on the roof.
  Glow surfaces are thin shells proud of the opaque glazing — the app renders
  _Glow in a separate layer at ~12 % alpha by day.

Everything is authored in the building's own (u, v, z) frame — u along the Dr.
Tom Waddell frontage from its west end, v into the block, z up — and rotated to
world once. That makes every wall, bay, fin and planter an axis-aligned box in
(u, v), which is why this script has almost no trigonometry in it.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- geometry

# Building grid: the Civic Center's 80.75° / 170.75° pair.
GRID_DEG = 80.75
_a = math.radians(GRID_DEG)
EU = (math.sin(_a), math.cos(_a))          # +u: ENE along Dr. Tom Waddell Place
EV = (-math.cos(_a), math.sin(_a))         # +v: NNW into the block
UV_ORIGIN = (-25.60, -22.40)               # ring vertex v0, the SW corner

# Regularised L, in (u, v). Outer perimeter, CCW.
BAR_U = 54.06        # Dr. Tom Waddell frontage
BAR_V = 15.47        # depth of the south bar
WING_U0 = 31.70      # west face of the north wing
WING_V = 36.58       # Grove Street frontage line

# The open courtyard.
CY_U0, CY_U1 = 36.60, 52.40
CY_V0, CY_V1 = 12.40, 30.70
PARTY_U0 = CY_U1     # blank east party wall enclosing the court

OUTER = [
    (0.0, 0.0),
    (BAR_U, 0.0),
    (BAR_U, WING_V),
    (WING_U0, WING_V),
    (WING_U0, BAR_V),
    (0.0, BAR_V),
]

# The five solids that make up "L minus courtyard".
SOLIDS = [
    ("bar_west", 0.0, CY_U0, 0.0, BAR_V),
    ("bar_east", CY_U0, BAR_U, 0.0, CY_V0),
    ("gallery_wing", WING_U0, CY_U0, BAR_V, WING_V),
    ("grove_wing", CY_U0, BAR_U, CY_V1, WING_V),
    ("party_wall", PARTY_U0, BAR_U, CY_V0, CY_V1),
]

# ------------------------------------------------------------------ levels

Z_L1 = 4.572          # 15'-0"  top of the concrete base
FLOOR = 3.0226        # 9'-11"
Z_FLOOR = [Z_L1 + FLOOR * i for i in range(7)]   # levels 2..8 floor lines
Z_ROOF = 25.730       # 84'-5"   roof deck
Z_FASCIA = 26.797     # 87'-11"  copper fascia / parapet top
Z_CREST = 30.120      # 98'-10"  mechanical screen — the bbox top

SILL = 0.90           # window sill above the floor line
VISION = 1.75         # vision-glass height
INFILL = 0.42         # opaque glass infill under the vision glass

BASE_PROUD = 0.12     # the concrete plinth stands proud of the panel field

PALETTE_HEX = {
    "Toy_white": "f7f4ec",     # fibre-cement panel field, penthouse
    "Toy_stone": "d9d2c2",     # textured concrete base
    "Toy_sand": "ece4d4",      # canopy slats, benches, courtyard pavers
    "Toy_trim": "f3efe6",      # roof pavers, archivolt
    "Toy_cream": "f2ede3",     # gallery decks, one courtyard stripe
    "Toy_ink": "3a3530",       # window-wall bays, reveals, frames, doors
    "Toy_glass": "2a4d73",     # vision glazing, corner bay
    "Toy_glassl": "6f95b8",    # opaque infill, pale-blue courtyard stripes
    "Toy_rust": "a86444",      # copper-anodized fins, fascia, bay soffit
    "Toy_coral": "e8735a",     # accent panels, coral courtyard stripes
    "Toy_sky": "6db3d9",       # sky-blue courtyard stripes
    "Toy_mustard": "d9a441",   # mustard courtyard stripes, the yellow wall
    "Toy_mint": "8fd0a8",      # olive stripes, planting caps
    "Toy_ioorange": "c0402a",  # gallery end screen
    "Toy_steel": "9aa0a6",     # guardrail, rails, roof plant
    "Toy_roofd": "45454a",     # planters, mechanical screen, coiling door
    "Toy_glassl_Glow": "6f95b8",
    "Toy_trim_Glow": "f3efe6",
}

# Deterministic courtyard colour sequence (style bible §7: every saturated
# colour this asset owns is spent in here).
COURT_SEQ = [
    "Toy_sky", "Toy_cream", "Toy_coral", "Toy_glassl", "Toy_mustard",
    "Toy_white", "Toy_mint", "Toy_sky", "Toy_coral", "Toy_cream",
    "Toy_glassl", "Toy_mint", "Toy_mustard", "Toy_white", "Toy_sky",
    "Toy_coral", "Toy_cream", "Toy_mint", "Toy_glassl", "Toy_white",
]

# Deterministic lit-window scatter: (face key, bay index, floor index).
LIT = {
    ("S", 0, 1), ("S", 0, 5), ("S", 2, 0), ("S", 2, 3), ("S", 3, 6),
    ("S", 5, 2), ("S", 5, 4), ("S", 6, 0), ("S", 7, 5), ("S", 8, 1),
    ("S", 8, 6), ("S", 10, 3), ("W", 0, 2), ("W", 1, 6), ("W", 2, 0),
    ("W", 2, 4), ("N", 1, 1), ("N", 2, 5), ("N", 3, 2), ("N", 4, 6),
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# Recentring: the regularised L's AABB centre, so the exported model is centred
# on the measured anchor. Filled in by _measure_offset().
OFFSET = [0.0, 0.0]


def W(u, v):
    """(u, v) in the building's grid -> world (x, y), recentred."""
    return (
        UV_ORIGIN[0] + EU[0] * u + EV[0] * v - OFFSET[0],
        UV_ORIGIN[1] + EU[1] * u + EV[1] * v - OFFSET[1],
    )


def _measure_offset():
    xs, ys = [], []
    for u, v in OUTER:
        x = UV_ORIGIN[0] + EU[0] * u + EV[0] * v
        y = UV_ORIGIN[1] + EU[1] * u + EV[1] * v
        xs.append(x)
        ys.append(y)
    OFFSET[0] = (min(xs) + max(xs)) / 2.0
    OFFSET[1] = (min(ys) + max(ys)) / 2.0


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


def prism(name, poly_uv, z0, z1, mat, mat_caps=None):
    """Closed extrusion of a CCW (u, v) polygon."""
    n = len(poly_uv)
    pts = [W(u, v) for u, v in poly_uv]
    verts = [(x, y, z0) for x, y in pts] + [(x, y, z1) for x, y in pts]
    faces, fm = [], []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
        fm.append(0)
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    fm += [1 if mat_caps else 0] * 2
    mats = [mat, mat_caps] if mat_caps else [mat]
    return new_mesh(name, verts, faces, mats, face_mats=fm)


def ubox(name, u0, u1, v0, v1, z0, z1, mat, mat_caps=None):
    """Axis-aligned box in the building grid. The workhorse of this script."""
    return prism(name, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], z0, z1, mat, mat_caps)


def arch_prism(name, u_c, half_w, v0, v1, z0, z_spring, crest, mat, seg=6):
    """Segmental-arched profile in the (u, z) plane, extruded along v."""
    prof = [(u_c - half_w, z0), (u_c + half_w, z0), (u_c + half_w, z_spring)]
    rise = crest - z_spring
    radius = (half_w * half_w + rise * rise) / (2.0 * rise)
    cz = z_spring + rise - radius
    th0 = math.atan2(z_spring - cz, half_w)
    th1 = math.pi - th0
    for k in range(1, seg):
        th = th0 + (th1 - th0) * k / seg
        prof.append((u_c + radius * math.cos(th), cz + radius * math.sin(th)))
    prof.append((u_c - half_w, z_spring))

    n = len(prof)
    verts = []
    for v in (v0, v1):
        for u, z in prof:
            x, y = W(u, v)
            verts.append((x, y, z))
    faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    return new_mesh(name, verts, faces, [mat])


def hex_crown(name, u, v, z0, z1, r, mat):
    """A chunky six-sided tree crown — silhouette, not leaves (style bible §12)."""
    ring = [(u + r * math.cos(math.tau * k / 6), v + r * math.sin(math.tau * k / 6))
            for k in range(6)]
    return prism(name, ring, z0, z1, mat)


def bevel(obj, width=0.12, segments=2):
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
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# ------------------------------------------------------------------ facades

# Public street faces, described in the (u, v) frame. Each entry gives the
# constant coordinate, which axis it lies on, the outward sign, the run of the
# face, and how many window bays it carries.
#   key, axis ('v' = face of constant v), const, outward sign, run0, run1, bays
FACES = [
    ("S", "v", 0.0, -1, 0.0, BAR_U, 11),          # Dr. Tom Waddell Place
    ("N", "v", WING_V, +1, WING_U0, BAR_U, 5),    # Grove Street
    ("W", "u", 0.0, -1, 0.0, BAR_V, 3),           # Van Ness Avenue
]

# Party / lot-line faces: the same white panel field, and almost nothing else.
# A full grid here is the "generic office block" failure mode (style bible §27)
# and it is also untrue — these walls are built to a lot line. E abuts 101
# Grove and gets three high openings; X and Y face narrow open lots and get a
# sparse, deliberately irregular scatter on the upper floors only.
#   key, axis, const, sign, run0, run1, columns, floors
PARTY_FACES = [
    ("E", "u", BAR_U, +1, 4.0, WING_V - 4.0, 3, (4, 5, 6)),      # against 101 Grove
    ("X", "u", WING_U0, -1, BAR_V + 2.0, WING_V - 2.0, 3, (2, 3, 4, 5, 6)),
    ("Y", "v", BAR_V, +1, 3.0, WING_U0 - 3.0, 4, (1, 2, 3, 4, 5, 6)),
]

BAY_W = 2.05          # charcoal window-wall bay
FIN_W = 0.18


def face_box(name, face, r0, r1, z0, z1, d0, d1, mat):
    """A slab lying on `face`, spanning [r0, r1] along the face, standing from
    depth d0 to d1 measured outward from the wall plane."""
    _key, axis, const, sign, _a0, _a1, _bays = face
    if axis == "v":
        v0, v1 = const + sign * d0, const + sign * d1
        return ubox(name, r0, r1, min(v0, v1), max(v0, v1), z0, z1, mat)
    u0, u1 = const + sign * d0, const + sign * d1
    return ubox(name, min(u0, u1), max(u0, u1), r0, r1, z0, z1, mat)


def street_facade(face, ink, glass, glassl, rust, coral, glow, coral_bays):
    key, _axis, _const, _sign, a0, a1, bays = face
    pitch = (a1 - a0) / bays
    for b in range(bays):
        c = a0 + pitch * (b + 0.5)
        face_box(f"{key}bay{b}", face, c - BAY_W / 2, c + BAY_W / 2,
                 Z_L1, Z_ROOF, -0.02, 0.05, ink)
        for f, zf in enumerate(Z_FLOOR):
            z0 = zf + SILL
            face_box(f"{key}g{b}_{f}", face, c - BAY_W / 2 + 0.12, c + BAY_W / 2 - 0.12,
                     z0, z0 + VISION, 0.02, 0.16, glass)
            face_box(f"{key}i{b}_{f}", face, c - BAY_W / 2 + 0.12, c + BAY_W / 2 - 0.12,
                     z0 - INFILL - 0.08, z0 - 0.08, 0.02, 0.13, glassl)
            if (key, b, f) in LIT:
                face_box(f"{key}lit{b}_{f}", face, c - BAY_W / 2 + 0.30,
                         c + BAY_W / 2 - 0.30, z0 + 0.18, z0 + VISION - 0.18,
                         0.14, 0.20, glow)
        # copper fins flank every bay, full seven storeys, uninterrupted
        for s, off in ((0, -1), (1, 1)):
            fc = c + off * (BAY_W / 2 + FIN_W / 2 + 0.06)
            face_box(f"{key}fin{b}_{s}", face, fc - FIN_W / 2, fc + FIN_W / 2,
                     Z_L1, Z_ROOF, 0.0, 0.11, rust)
        if b in coral_bays:
            pc = c + pitch / 2
            face_box(f"{key}coral{b}", face, pc - pitch * 0.18, pc + pitch * 0.18,
                     Z_FLOOR[1], Z_FLOOR[4], 0.0, 0.07, coral)


def party_facade(face, ink, glass):
    key, axis, const, sign, a0, a1, cols, floors = face
    plain = (key, axis, const, sign, a0, a1, cols)
    pitch = (a1 - a0) / cols
    for b in range(cols):
        c = a0 + pitch * (b + 0.5)
        for f in floors:
            # stagger every other column by one floor so the scatter never
            # resolves into a grid from the aerial camera
            fi = f - (b % 2)
            if not 0 <= fi < len(Z_FLOOR):
                continue
            z0 = Z_FLOOR[fi] + SILL
            face_box(f"{key}r{b}_{f}", plain, c - 0.85, c + 0.85,
                     z0, z0 + 1.55, -0.02, 0.04, ink)
            face_box(f"{key}q{b}_{f}", plain, c - 0.70, c + 0.70,
                     z0 + 0.12, z0 + 1.43, 0.02, 0.12, glass)


# ---------------------------------------------------------------- the build


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)

    _measure_offset()

    white = material("Toy_white")
    stone = material("Toy_stone")
    sand = material("Toy_sand")
    trim = material("Toy_trim")
    cream = material("Toy_cream")
    ink = material("Toy_ink")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    rust = material("Toy_rust")
    coral = material("Toy_coral")
    mustard = material("Toy_mustard")
    mint = material("Toy_mint")
    ioorange = material("Toy_ioorange")
    steel = material("Toy_steel")
    roofd = material("Toy_roofd")
    gglow = material("Toy_glassl_Glow")
    tglow = material("Toy_trim_Glow")
    court_mats = {k: material(k) for k in set(COURT_SEQ)}

    heavy = []

    # --- base and body -----------------------------------------------------
    for name, u0, u1, v0, v1 in SOLIDS:
        heavy.append(ubox(f"base_{name}", u0 - BASE_PROUD, u1 + BASE_PROUD,
                          v0 - BASE_PROUD, v1 + BASE_PROUD, 0.0, Z_L1, stone))
        # The roof cap is a pale grey membrane, not the deck. Only the amenity
        # zone gets cream pavers, so from the app's camera the deck reads as a
        # designed room on the roof rather than the roof reading as one tray.
        heavy.append(ubox(f"body_{name}", u0, u1, v0, v1, Z_L1, Z_ROOF,
                          white, mat_caps=stone))

    # --- copper fascia lid on every outer face and around the court --------
    F = 0.22
    for i, (u, v) in enumerate(OUTER):
        u2, v2 = OUTER[(i + 1) % len(OUTER)]
        if abs(v - v2) < 1e-6:      # runs along u, face of constant v
            out = -F if v < BAR_V else F
            ubox(f"fascia{i}", min(u, u2), max(u, u2), min(v, v + out),
                 max(v, v + out), Z_ROOF, Z_FASCIA, rust)
        else:                        # runs along v, face of constant u
            out = -F if u < BAR_U / 2 else F
            ubox(f"fascia{i}", min(u, u + out), max(u, u + out), min(v, v2),
                 max(v, v2), Z_ROOF, Z_FASCIA, rust)

    # --- street elevations --------------------------------------------------
    street_facade(FACES[0], ink, glass, glassl, rust, coral, gglow, {1, 4, 8})
    street_facade(FACES[1], ink, glass, glassl, rust, coral, gglow, {2})
    street_facade(FACES[2], ink, glass, glassl, rust, coral, gglow, {0})
    for f in PARTY_FACES:
        party_facade(f, ink, glass)

    # --- the courtyard: the identity ---------------------------------------
    # Four inner faces, each divided into full-height vertical colour stripes.
    court_faces = [
        ("CW", "u", CY_U0, +1, CY_V0, CY_V1),   # gallery wall, faces east
        ("CE", "u", CY_U1, -1, CY_V0, CY_V1),   # blank party wall, faces west
        ("CS", "v", CY_V0, +1, CY_U0, CY_U1),   # faces north
        ("CN", "v", CY_V1, -1, CY_U0, CY_U1),   # faces south
    ]
    seq = 0
    for key, axis, const, sign, a0, a1 in court_faces:
        n = max(3, int(round((a1 - a0) / 1.65)))
        pitch = (a1 - a0) / n
        for b in range(n):
            r0 = a0 + pitch * b + 0.04
            r1 = a0 + pitch * (b + 1) - 0.04
            mat = mustard if key == "CE" and b % 3 == 1 else court_mats[COURT_SEQ[seq % len(COURT_SEQ)]]
            seq += 1
            face = (key, axis, const, sign, a0, a1, n)
            face_box(f"{key}stripe{b}", face, r0, r1, 0.0, Z_ROOF, -0.01, 0.12, mat)
            if key != "CE" and b % 2 == 0:
                for f, zf in enumerate(Z_FLOOR):
                    z0 = zf + SILL
                    face_box(f"{key}w{b}_{f}", face, r0 + 0.22, r1 - 0.22,
                             z0, z0 + 1.55, 0.10, 0.20, glass)

    # open-air access galleries on the west courtyard wall
    for f, zf in enumerate(Z_FLOOR[:6]):
        ubox(f"gallery{f}", CY_U0, CY_U0 + 1.70, CY_V0 + 0.3, CY_V1 - 0.3,
             zf - 0.22, zf, cream)
        ubox(f"gallery_rail{f}", CY_U0 + 1.52, CY_U0 + 1.70, CY_V0 + 0.3, CY_V1 - 0.3,
             zf, zf + 1.02, steel)
    ubox("gallery_screen", CY_U0 + 1.30, CY_U0 + 1.52, CY_V1 - 4.6, CY_V1 - 0.3,
         Z_L1, Z_FLOOR[4], ioorange)

    # the big soft arch into the covered passage under the south bar
    arch_prism("court_arch_recess", (CY_U0 + CY_U1) / 2, 4.0, CY_V0 - 0.05, CY_V0 + 0.55,
               0.0, 4.4, 7.4, ink)
    arch_prism("court_arch_ring", (CY_U0 + CY_U1) / 2, 4.45, CY_V0 + 0.10, CY_V0 + 0.40,
               0.0, 4.6, 7.9, trim)

    # courtyard ground: pavers, planters, three chunky trees, the night wash
    # Two tones: pale plank decking against grey unit pavers, as photographed —
    # and bright, because an 18 m court seen from 25 m up is dark enough already.
    ubox("court_pavers", CY_U0, CY_U1, CY_V0, CY_V1, 0.0, 0.16, trim)
    ubox("court_deck", CY_U0, CY_U0 + 5.4, CY_V0, CY_V1, 0.16, 0.24, sand)
    ubox("court_paverband", CY_U0 + 5.4, CY_U1, CY_V0 + 7.6, CY_V0 + 10.9,
         0.16, 0.22, stone)
    for i, (pu, pv) in enumerate(((39.0, 15.2), (48.6, 15.2), (39.0, 27.4), (48.6, 27.4))):
        ubox(f"court_planter{i}", pu - 1.9, pu + 1.9, pv - 1.3, pv + 1.3, 0.16, 0.72, roofd)
        ubox(f"court_bed{i}", pu - 1.75, pu + 1.75, pv - 1.15, pv + 1.15, 0.66, 0.82, mint)
    for i, (tu, tv) in enumerate(((42.4, 18.4), (46.8, 22.6), (42.0, 26.8))):
        ubox(f"court_trunk{i}", tu - 0.16, tu + 0.16, tv - 0.16, tv + 0.16, 0.16, 2.5, roofd)
        hex_crown(f"court_crown{i}", tu, tv, 2.4, 5.1, 1.7, mint)
    ubox("court_wash", CY_U0 + 0.6, CY_U1 - 0.6, CY_V0 + 0.6, CY_V1 - 0.6,
         0.17, 0.24, tglow)
    for i in range(7):
        cu = CY_U0 + 1.6 + i * 2.1
        ubox(f"court_festoon{i}", cu - 0.14, cu + 0.14, CY_V0 + 5.4, CY_V1 - 5.4,
             6.5, 6.66, tglow)

    # --- Van Ness / Waddell corner: the projecting glazed bay --------------
    # A plain glass box read as a navy billboard bolted to the corner. What
    # makes it a bay window is the frame: pale cheeks at both ends, charcoal
    # mullions splitting each face into lights, and the floor bands between.
    CB_U0, CB_U1, CB_V0, CB_V1 = -0.95, 4.85, -0.95, 2.95
    heavy.append(ubox("corner_bay", CB_U0, CB_U1, CB_V0, CB_V1,
                      Z_FLOOR[0], Z_FLOOR[6] + 2.0, glass, mat_caps=stone))
    ubox("corner_soffit", CB_U0 - 0.15, CB_U1 + 0.15, CB_V0 - 0.15, CB_V1 + 0.15,
         Z_FLOOR[0] - 0.40, Z_FLOOR[0], rust)
    for f, zf in enumerate(Z_FLOOR[1:6]):
        ubox(f"corner_band{f}", CB_U0 - 0.06, CB_U1 + 0.06, CB_V0 - 0.06, CB_V1 + 0.06,
             zf - 0.26, zf + 0.06, ink)
    # pale cheeks: the solid ends of the bay, in the panel material
    ubox("corner_cheek_e", CB_U1 - 0.55, CB_U1 + 0.06, CB_V0 - 0.06, CB_V1 + 0.06,
         Z_FLOOR[0], Z_FLOOR[6] + 2.0, white)
    ubox("corner_cheek_n", CB_U0 - 0.06, CB_U1 + 0.06, CB_V1 - 0.55, CB_V1 + 0.06,
         Z_FLOOR[0], Z_FLOOR[6] + 2.0, white)
    # charcoal mullions, two per visible face
    for i, mu in enumerate((1.15, 2.85)):
        ubox(f"corner_mull_s{i}", mu - 0.09, mu + 0.09, CB_V0 - 0.07, CB_V0 + 0.10,
             Z_FLOOR[0], Z_FLOOR[6] + 2.0, ink)
    for i, mv in enumerate((0.35, 1.75)):
        ubox(f"corner_mull_w{i}", CB_U0 - 0.07, CB_U0 + 0.10, mv - 0.09, mv + 0.09,
             Z_FLOOR[0], Z_FLOOR[6] + 2.0, ink)

    # --- ground floor -------------------------------------------------------
    # glazed lobby and retail on Van Ness and the west half of Waddell
    for b in range(3):
        c = 2.4 + b * 4.6
        face_box(f"Sshop{b}", FACES[0], c - 1.9, c + 1.9, 0.55, Z_L1 - 0.85,
                 BASE_PROUD - 0.02, BASE_PROUD + 0.12, glass)
    for b in range(2):
        c = 4.0 + b * 6.6
        face_box(f"Wshop{b}", FACES[2], c - 2.1, c + 2.1, 0.55, Z_L1 - 0.85,
                 BASE_PROUD - 0.02, BASE_PROUD + 0.12, glass)
        face_box(f"Wlobbyglow{b}", FACES[2], c - 1.8, c + 1.8, 0.80, Z_L1 - 1.10,
                 BASE_PROUD + 0.10, BASE_PROUD + 0.17, tglow)
    # the middle of the 54 m base was a blank concrete band: painted aluminium
    # vents and a pair of recessed panels, which is what the elevation shows
    for i, c in enumerate((19.4, 24.2, 29.0)):
        face_box(f"Svent{i}", FACES[0], c - 1.15, c + 1.15, 2.30, 3.55,
                 BASE_PROUD - 0.02, BASE_PROUD + 0.07, steel)
    for i, c in enumerate((21.8, 26.6)):
        face_box(f"Srecess{i}", FACES[0], c - 0.95, c + 0.95, 0.30, 3.90,
                 BASE_PROUD - 0.06, BASE_PROUD + 0.01, ink)

    # service end of Waddell: coiling door and two hollow-metal doors
    face_box("Sdoor_coil", FACES[0], 44.0, 48.2, 0.0, 3.7, BASE_PROUD - 0.02,
             BASE_PROUD + 0.08, roofd)
    for i, c in enumerate((40.6, 50.4)):
        face_box(f"Sdoor{i}", FACES[0], c - 0.65, c + 0.65, 0.0, 2.4,
                 BASE_PROUD - 0.02, BASE_PROUD + 0.09, ink)

    # wood-slat trellis canopy over the Waddell sidewalk at the corner. It stops
    # at the building line on the west: cantilevering it out over Van Ness as
    # well pushed the bbox 2.6 m south and threw the XY centre off by 1.4 m.
    ubox("canopy_plate", 0.40, 8.40, -1.50, 0.10, Z_L1 - 1.20, Z_L1 - 1.06, ink)
    for i in range(6):
        cu = 0.95 + i * 1.45
        ubox(f"canopy_slat{i}", cu - 0.16, cu + 0.16, -1.50, 0.10,
             Z_L1 - 1.06, Z_L1 - 0.84, sand)
    ubox("canopy_outrig", 0.40, 8.40, -0.30, 0.10, Z_L1 - 1.06, Z_L1 - 0.90, ink)

    # --- the roof: the surface the app's camera sees most --------------------
    # Amenity deck at the west end, looking across Van Ness to City Hall — the
    # only part of the roof that is paved.
    ubox("pavers_deck", 0.35, 22.60, 0.35, BAR_V - 0.35, Z_ROOF, Z_ROOF + 0.20, trim)

    for i, (pu, pv) in enumerate(((5.0, 4.2), (5.0, 11.0), (12.0, 4.2), (12.0, 11.0), (19.0, 7.6))):
        # The planting has to sit PROUD of the rim. Sunk inside a tall rim it
        # read as five black cushions from the aerial; flush with a low rim it
        # read as five green pools. A low dark rim with the planting standing
        # above it gives both the bronze edge and the green mass.
        heavy.append(ubox(f"planter{i}", pu - 2.4, pu + 2.4, pv - 1.5, pv + 1.5,
                          Z_ROOF + 0.18, Z_ROOF + 0.58, roofd))
        ubox(f"planting{i}", pu - 2.05, pu + 2.05, pv - 1.15, pv + 1.15,
             Z_ROOF + 0.44, Z_ROOF + 0.92, mint)
    for i, (bu, bv) in enumerate(((8.5, 7.6), (15.5, 4.2), (15.5, 11.0), (2.0, 7.6))):
        heavy.append(ubox(f"bench{i}", bu - 1.9, bu + 1.9, bv - 0.55, bv + 0.55,
                          Z_ROOF + 0.18, Z_ROOF + 0.66, sand))

    # The membrane roof over the east bar and the Grove wing is not a deck, so
    # it gets what a roof like this really carries: a skylight run over the
    # top-floor corridor and two tight mechanical clusters (style bible §10 —
    # organised clusters, never scatter).
    for i in range(4):
        cu = 44.6 + i * 2.3
        ubox(f"skylight_kerb{i}", cu - 0.85, cu + 0.85, 7.6, 10.4,
             Z_ROOF, Z_ROOF + 0.22, stone)
        ubox(f"skylight{i}", cu - 0.70, cu + 0.70, 7.75, 10.25,
             Z_ROOF + 0.18, Z_ROOF + 0.42, glassl)
    for i in range(3):
        cu = 39.4 + i * 3.0
        ubox(f"wing_kerb{i}", cu - 1.0, cu + 1.0, 32.2, 34.8,
             Z_ROOF, Z_ROOF + 0.20, stone)
        ubox(f"wing_unit{i}", cu - 0.85, cu + 0.85, 32.4, 34.6,
             Z_ROOF + 0.18, Z_ROOF + 1.05, steel)
    ubox("duct_run", 45.0, 51.4, 12.6, 13.4, Z_ROOF + 0.30, Z_ROOF + 0.62, steel)

    # perimeter guardrail on the deck end and around the courtyard rim
    def guardrail(tag, u0, u1, v0, v1):
        ubox(f"{tag}_rail_lo", u0, u1, v0, v1, Z_ROOF + 0.20, Z_ROOF + 0.32, steel)
        ubox(f"{tag}_rail_hi", u0, u1, v0, v1, Z_FASCIA - 0.14, Z_FASCIA, steel)
        span = max(u1 - u0, v1 - v0)
        n = max(2, int(span / 1.10))
        for k in range(n):
            t = (k + 0.5) / n
            if u1 - u0 >= v1 - v0:
                pu = u0 + (u1 - u0) * t
                ubox(f"{tag}_p{k}", pu - 0.05, pu + 0.05, v0, v1,
                     Z_ROOF + 0.30, Z_FASCIA - 0.12, steel)
            else:
                pv = v0 + (v1 - v0) * t
                ubox(f"{tag}_p{k}", u0, u1, pv - 0.05, pv + 0.05,
                     Z_ROOF + 0.30, Z_FASCIA - 0.12, steel)

    guardrail("deck_e", 22.6, 22.78, 0.45, BAR_V - 0.45)
    guardrail("court_s", CY_U0, CY_U1, CY_V0 - 0.18, CY_V0)
    guardrail("court_n", CY_U0, CY_U1, CY_V1, CY_V1 + 0.18)
    guardrail("court_w", CY_U0 - 0.18, CY_U0, CY_V0, CY_V1)

    # mechanical penthouse — the crest
    # The screen is a louvred box around the plant, not a lid over the whole
    # penthouse: at 9.2 x 6.2 m it read from the aerial as one black slab
    # swallowing the roof. Keeping it to 5.8 x 3.4 m lets the pale penthouse
    # read as the mass and the screen as the thing sitting on it — and the
    # screen is still what sets the 30.120 m crest.
    heavy.append(ubox("penthouse", 25.4, 39.0, 2.6, 11.6, Z_ROOF, 28.90, white,
                      mat_caps=stone))
    heavy.append(ubox("mech_screen", 29.0, 34.8, 5.4, 8.8, 28.90, Z_CREST, roofd))
    ubox("mech_unit_a", 41.0, 43.6, 3.4, 6.2, Z_ROOF + 0.18, Z_ROOF + 1.35, steel)
    ubox("mech_unit_b", 41.0, 43.2, 7.6, 10.0, Z_ROOF + 0.18, Z_ROOF + 1.05, steel)
    ubox("roof_hatch", 46.4, 47.8, 5.4, 6.8, Z_ROOF + 0.18, Z_ROOF + 0.70, roofd)

    # --- beveling ------------------------------------------------------------
    # Only the chunky masses carry the miniature read. The applied panels are
    # 60-200 mm thick; a full bevel on those collapses into degenerate slivers.
    heavy_names = {o.name for o in heavy}
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name in heavy_names:
            bevel(obj, width=0.12, segments=2)

    return bpy.context.scene


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
    print("[build] anchor lon/lat: -122.4193071 37.7780541 (footprint AABB centre)")
    print("[build] Van Ness front heading: 261.8 deg true (W)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "234-van-ness.blend")
    glb = os.path.join(out, "234-van-ness.glb")
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
