"""Deterministic Blender build of the SF-SIM miniature 110 The Embarcadero
(The Commonwealth Club of California).

    blender -b --python build_110_embarcadero.py -- [--out DIR]

Writes 110-embarcadero.blend and 110-embarcadero.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading - the loader applies
no rotation. Origin = model XY bbox centre, min Z = 0, roof fascia crest exactly
17.40 m.

Design (see REFERENCE.md for the sources behind every number):

* a 1910 two-storey ILA union hall on a 41.87 x 13.91 m through-lot, gutted by
  Leddy Maytum Stacy in 2015-17 into the Commonwealth Club's headquarters: the
  rendered Steuart Street front retained and shored, a light-weight glass third
  floor added, and a full-height glass curtain wall hung on the Embarcadero end;
* the recognition rests on the building being TWO BUILDINGS. Three storeys of
  glass at 17.40 m facing The Embarcadero (44.83 deg), a two-storey rendered
  front with a bracketed cornice and a shallow PEDIMENT at 12.60 m facing
  Steuart Street (224.94 deg), and the step between them visible from every
  aerial angle;
* both long sides are literal party walls - the Audiffred Building shares this
  footprint's north-west vertices, the seven-storey office at way/193054135
  shares its south-east ones - so they are flat and blind by design, not by
  laziness;
* the roof is the largest surface the app's camera ever sees of this building
  and it is a designed public terrace: paved deck at the Embarcadero end,
  planted garden through the middle, one penthouse, one skylight, the quiet
  strip behind the historic parapet at the Steuart end. That gradient tells the
  new-end / old-end story in the one view the app actually gives you;
* night state: the curtain wall is ONE lantern, not a scatter - there is an
  auditorium behind it and this is an events building (cat 17, night profile 1).
  The signage band and canopy are the ground cue, the roof skylight and the
  set-back third-floor glazing are the aerial cue, and the rendered 1910 front
  stays dark except its storefront. Glow surfaces are single outward-facing
  quads standing proud of the opaque glazing, never closed shells: the app draws
  _Glow in a separate layer and a closed shell is two alpha layers deep.

Authoring frame: the footprint is a parallelogram at 135.24 deg to the world
axes, so everything is placed through a (u, s) plan frame - u along the long
axis from the Steuart end, s across from the south-east party wall - and through
Face frames on the two street ends. Because the building sits at 45 deg the
axis-aligned XY bounding box is ~40 x 40 m even though the building is
41.87 x 13.91 m. That is expected, not a scale error.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# The project's tangent projection (AGENTS.md), used only to convert the final
# recentring shift back into a lon/lat anchor.
LON0P, LAT0P = -122.4375, 37.77
LON_M = 111320.0 * math.cos(math.radians(LAT0P))
LAT_M = 110540.0

# Footprint centroid - the plan's design anchor, before recentring.
DESIGN_ANCHOR = (-122.3926624, 37.7932325)

# Measured footprint, OSM way/256969674 reprojected and recentred on the
# centroid (metres east, metres north). DataSF parcel 3715002 agrees to <= 1 m.
V_EMB_SE = (19.790, 9.833)     # Embarcadero end, south-east corner
V_STE_SE = (-9.935, -19.648)   # Steuart end, south-east corner
V_STE_NW = (-19.781, -9.821)   # Steuart end, north-west corner
V_EMB_NW = (9.926, 19.637)     # Embarcadero end, north-west corner

# Vertical datums. Every one of these is measured off a rectified 60 px/m
# Street View elevation (REFERENCE.md) unless marked otherwise.
Z_L2 = 4.20          # level 2 floor - head of the recessed Embarcadero lobby
Z_L3 = 11.20         # level 3 floor; also the retained historic roof line
Z_HIST_CORN = 11.60  # Steuart cornice crest (measured 11.5)
Z_HIST_APEX = 12.60  # Steuart pediment apex - EXAGGERATED from the measured
                     # 12.3 m by 0.3 m, the one licensed exaggeration here
Z_SETBACK = 13.90    # top of the set-back glazed third floor at the Steuart end
Z_OVERRUN = 14.80    # stair / lift over-run box at the Steuart end
Z_ROOF = 15.80       # main roof DECK surface of the Embarcadero volume.
                     # STAGE-2 CORRECTION to the plan, which put the deck at
                     # 16.60: 16.90 is the measured parapet / curtain-wall HEAD,
                     # and a publicly accessible terrace needs its walking
                     # surface a guard height (1.10 m) below that, not 0.30 m.
                     # The plan's ladder also had nowhere to put roof planting
                     # without breaking the 17.40 bbox top. See REPORT.md 2.
Z_HEAD = 16.90       # curtain-wall head / main parapet top (measured 16.9)
Z_FASCIA = 17.40     # projecting roof eyebrow - the BBOX TOP, so the loader's
                     # targetHeightM / measuredHeight lands on exactly 1.0

STEP_U = 7.60        # where the block steps down to the historic height,
                     # measured back from the Steuart face
SETBACK_D = 1.60     # how far the new third floor sits back from that face

EMBED = 0.03         # how far every applied band is sunk INTO the surface it
                     # sits on. Nothing here is allowed to have a face exactly
                     # coincident with another solid's: coincident faces make
                     # the first-hit direction of a ray ambiguous and the
                     # contract's normals ray test counts that as a flip.
                     # Overlapping solids are the supported model - the
                     # authoritative normals test is per-object signed volume.

BEVEL_W, BEVEL_SEG = 0.10, 2

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",   # the rendered walls: the 1910 Steuart front, both
                             # party walls, the body of the block. A step darker
                             # than the trim on purpose - 49 South Park's report
                             # records what happens when body and moulding are
                             # both cream (the modelling vanishes).
    "Toy_trim": "f3efe6",    # cornice, pediment, modillions, sill band, window
                             # and storefront frames, curtain-wall mullions and
                             # jambs, signage band, canopy, roof fascia,
                             # penthouse, stair over-run
    "Toy_glass": "2a4d73",   # curtain-wall panes, Steuart upper windows and
                             # storefront, the set-back third floor
    "Toy_glassl": "6f95b8",  # curtain-wall spandrel bands, roof skylight
    "Toy_ink": "3a3530",     # lobby back plane, door recesses, parapet cap
                             # line, fascia soffit, the 110 plate
    "Toy_mint": "8fd0a8",    # roof-garden planting
    "Toy_sand": "ece4d4",    # planter kerbs, roof deck paving
    "Toy_glassl_Glow": "6f95b8",   # the lit curtain wall, the set-back glazing
                             # and the roof skylight. NOT Toy_glass_Glow
                             # (2a4d73): the app draws _Glow unlit, so at night
                             # the surface shows its RAW base colour, and 2a4d73
                             # is the navy of UNLIT glass - it renders as a dark
                             # window pretending to be a lit one.
    "Toy_trim_Glow": "f3efe6",     # the COMMONWEALTH CLUB signage band only.
                             # Near-white is right for a SIGN and wrong for
                             # everything else: the first night pass used it for
                             # the whole lobby band and the Steuart storefront
                             # too, and 13.9 m of f3efe6 blew out to a white
                             # slab brighter than the hero curtain wall above
                             # it. The app shows a _Glow surface's RAW base
                             # colour at night, so the colour IS the brightness.
    "Toy_mustard_Glow": "d9a441",  # the lobby spill and the Steuart storefront.
                             # Warm amber at ground level under the cool lantern
                             # is the composition; it also keeps the two ground
                             # cues clearly subordinate to the curtain wall.
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


# ------------------------------------------------------------- plan geometry


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def _unit(v):
    m = math.hypot(v[0], v[1])
    return (v[0] / m, v[1] / m), m


U_HAT, L_LONG = _unit(_sub(V_EMB_SE, V_STE_SE))    # Steuart end -> Embarcadero
S_HAT, W_WIDE = _unit(_sub(V_STE_NW, V_STE_SE))    # SE party wall -> NW party
ORIGIN_US = V_STE_SE

FOOTPRINT = [V_EMB_SE, V_STE_SE, V_STE_NW, V_EMB_NW]
CX = sum(p[0] for p in FOOTPRINT) / 4.0
CY = sum(p[1] for p in FOOTPRINT) / 4.0


def P(u, s):
    """Plan point: u metres from the Steuart face, s metres from the south-east
    party wall."""
    return (ORIGIN_US[0] + U_HAT[0] * u + S_HAT[0] * s,
            ORIGIN_US[1] + U_HAT[1] * u + S_HAT[1] * s)


def slab(u0, u1, s0, s1):
    """Plan rectangle in the (u, s) frame, as a world-XY polygon."""
    return [P(u0, s0), P(u1, s0), P(u1, s1), P(u0, s1)]


class Face:
    """A local frame on one elevation: t runs along the face from `a` to `b`,
    d runs OUTWARD (away from the footprint centroid), z is world up."""

    def __init__(self, a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        self.a, self.b, self.length = a, b, n
        self.t = (dx / n, dy / n)
        nrm = (-self.t[1], self.t[0])
        if (a[0] + nrm[0] - CX) ** 2 + (a[1] + nrm[1] - CY) ** 2 < (a[0] - CX) ** 2 + (
            a[1] - CY
        ) ** 2:
            nrm = (-nrm[0], -nrm[1])
        self.n = nrm
        self.heading = (math.degrees(math.atan2(nrm[0], nrm[1])) + 360.0) % 360.0

    def xy(self, t, d):
        return (self.a[0] + self.t[0] * t + self.n[0] * d,
                self.a[1] + self.t[1] * t + self.n[1] * d)

    def rect(self, t0, t1, d0, d1):
        return [self.xy(t0, d0), self.xy(t1, d0), self.xy(t1, d1), self.xy(t0, d1)]


# t = 0 at the NORTH-WEST corner on the Embarcadero face, at the SOUTH-EAST
# corner on the Steuart face. Both street faces therefore run "away from the
# Audiffred" as t grows on one and toward it on the other - the entrance side
# and the over-run side are stated in NW/SE terms everywhere below.
EMB = Face(V_EMB_NW, V_EMB_SE)     # The Embarcadero, faces 44.83
SE_PARTY = Face(V_EMB_SE, V_STE_SE)  # party wall, faces 135.24
STE = Face(V_STE_SE, V_STE_NW)     # Steuart Street, faces 224.94
NW_PARTY = Face(V_STE_NW, V_EMB_NW)  # party wall, faces 315.24


# --------------------------------------------------------------- mesh helpers


def new_mesh(name, verts, faces, materials, face_mats=None, recalc=True):
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
    if recalc:
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.free()
    mesh.shade_flat()
    return obj


def prism(name, poly_xy, z0, z1, mat, mat_top=None):
    """Closed extrusion of a world-XY polygon (walls + both caps)."""
    n = len(poly_xy)
    verts = [(x, y, z0) for x, y in poly_xy] + [(x, y, z1) for x, y in poly_xy]
    faces, face_mats = [], []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
        face_mats.append(0)
    faces.append(tuple(range(n - 1, -1, -1)))
    face_mats.append(0)
    faces.append(tuple(range(n, 2 * n)))
    face_mats.append(1 if mat_top else 0)
    mats = [mat, mat_top] if mat_top else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def plate(name, face, pts_tz, d0, d1, mat):
    """Extrude a polygon drawn in a face's (t, z) plane outward from d0 to d1.
    Used for the Steuart pediment, which is the one non-rectangular elevation
    element on the building."""
    lo = [(face.xy(t, d0)[0], face.xy(t, d0)[1], z) for t, z in pts_tz]
    hi = [(face.xy(t, d1)[0], face.xy(t, d1)[1], z) for t, z in pts_tz]
    n = len(pts_tz)
    verts = lo + hi
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    return new_mesh(name, verts, faces, [mat])


def opening(name, face, t0, t1, z0, z1, mats, margin=0.16, glass="Toy_glass"):
    """A glazed opening: a recessed frame plate with the glass standing PROUD of
    it. Built this way round on purpose - the first pass put the frame in front
    of the glass as one solid slab and every window on the Steuart front
    rendered as a blank cream panel. The frame must be the thing behind."""
    prism(f"{name}_frame", face.rect(t0 - margin, t1 + margin, -EMBED, 0.07),
          z0 - margin, z1 + margin, mats["Toy_trim"])
    prism(f"{name}_glass", face.rect(t0, t1, 0.05, 0.13), z0, z1, mats[glass])


def glow_quad(name, face, t0, t1, z0, z1, mat, proud):
    """ONE outward-facing quad, standing `proud` metres off the wall.

    Night glow must never be a closed shell. The app draws _Glow in a separate
    layer that is translucent by day, so a closed box shows its front AND back
    face and reads at roughly twice the intended day alpha - enough to tint a
    whole facade. The winding is set from the face's own outward normal rather
    than recalculated, because a single quad has no inside for recalc to find."""
    p = [face.xy(t0, proud), face.xy(t1, proud)]
    verts = [(p[0][0], p[0][1], z0), (p[1][0], p[1][1], z0),
             (p[1][0], p[1][1], z1), (p[0][0], p[0][1], z1)]
    # normal of the quad as wound = t_hat x z_hat
    nx, ny = face.t[1], -face.t[0]
    order = (0, 1, 2, 3) if (nx * face.n[0] + ny * face.n[1]) > 0.0 else (3, 2, 1, 0)
    return new_mesh(name, verts, [order], [mat], recalc=False)


def glow_roof(name, poly_xy, z, mat):
    """One upward-facing horizontal glow quad (roof skylight)."""
    verts = [(x, y, z) for x, y in poly_xy]
    # ensure counter-clockwise so the single face points up
    s2 = 0.0
    for i in range(len(poly_xy)):
        a, b = poly_xy[i], poly_xy[(i + 1) % len(poly_xy)]
        s2 += a[0] * b[1] - b[0] * a[1]
    idx = tuple(range(len(poly_xy))) if s2 > 0 else tuple(range(len(poly_xy) - 1, -1, -1))
    return new_mesh(name, verts, [idx], [mat], recalc=False)


def bevel(obj, width=BEVEL_W, segments=BEVEL_SEG):
    """Miniature-style edge softening (style bible s.4). The offset is capped at
    a third of the object's thinnest dimension: glazing bands, frames and glow
    shells are only 20-160 mm thick and a full bevel on those collapses opposing
    profiles into zero-area slivers even with clamp_overlap."""
    thin = min((d for d in obj.dimensions if d > 1e-6), default=width)
    offset = min(width, thin * 0.30)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.bevel(bm, geom=list(bm.verts) + list(bm.edges), offset=offset,
                    segments=segments, profile=0.5, affect="EDGES",
                    clamp_overlap=True)
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-4)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-4, edges=list(bm.edges))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def make_material(name):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = PALETTE[name] + (1.0,)
    bsdf.inputs["Roughness"].default_value = 0.85
    if "Metallic" in bsdf.inputs:
        bsdf.inputs["Metallic"].default_value = 0.0
    if name.endswith("_Glow") and "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = PALETTE[name] + (1.0,)
        bsdf.inputs["Emission Strength"].default_value = 1.0
    return mat


# --------------------------------------------------------------------- build


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene
    mats = {k: make_material(k) for k in PALETTE_HEX}

    L, W = L_LONG, W_WIDE
    REC = 0.55                      # Embarcadero ground-floor recess depth

    # ---- 1. the block, in three stacked plates so the ground floor can be
    #         recessed at the Embarcadero end and the Steuart end can step down.
    # The recessed zone at the Embarcadero end has to clear the top of the
    # signage band, not stop at the level-2 slab: with body_mid starting at
    # 4.00 the upper half of the COMMONWEALTH CLUB band and its night glow were
    # buried inside the flush body above them, which the validator's glow ray
    # test caught (19 of 20 faces outward).
    Z_REC_TOP = Z_L2 + 0.75     # top of the recessed lobby zone
    Z_MID0 = Z_L2 + 0.55        # where the flush body starts (0.20 m overlap)
    prism("body_low", slab(0.0, L - REC, 0.0, W), 0.0, Z_REC_TOP,
          mats["Toy_stone"])
    prism("body_mid", slab(0.0, L, 0.0, W), Z_MID0, Z_L3, mats["Toy_stone"])
    prism("body_high", slab(STEP_U, L, 0.0, W), Z_L3 - 0.20, Z_ROOF,
          mats["Toy_stone"], mat_top=mats["Toy_sand"])

    # ---- 2. main parapet, round the Embarcadero volume only. It stops at the
    #         step, where the historic parapet takes over 5.3 m lower down.
    for poly, nm in ((slab(STEP_U, L, -0.02, 0.28), "pl_se"),
                     (slab(STEP_U, L, W - 0.28, W + 0.02), "pl_nw"),
                     (slab(STEP_U - 0.02, STEP_U + 0.28, 0.0, W), "pl_step")):
        prism(f"parapet_{nm}", poly, Z_ROOF - 0.10, Z_HEAD, mats["Toy_stone"])
    # A NARROW cap line. At 0.38 m the first pass read from the app's downward
    # camera as two heavy black rails running the whole length of the roof.
    prism("parapet_cap_se", slab(STEP_U, L, -0.05, 0.13), Z_HEAD, Z_HEAD + 0.07,
          mats["Toy_ink"])
    prism("parapet_cap_nw", slab(STEP_U, L, W - 0.13, W + 0.05), Z_HEAD,
          Z_HEAD + 0.07, mats["Toy_ink"])

    # ---- 3. THE EMBARCADERO END (north-east) - the glass curtain wall.
    #         t = 0 at the north-west (Audiffred) corner.
    tw = EMB.length
    # 3a. recessed lobby: dark back plane and a full-width glazed wall
    prism("lobby_back", EMB.rect(0.30, tw - 0.30, -REC - EMBED, -REC + 0.10),
          0.0, Z_L2 - 0.05, mats["Toy_ink"])
    prism("lobby_glass", EMB.rect(0.55, tw - 0.55, -REC + 0.06, -REC + 0.16),
          0.25, Z_L2 - 0.45, mats["Toy_glass"])
    # entrance doors, toward the north-west (Audiffred) half - measured off the
    # rectified elevation, not centred
    prism("entry_doors", EMB.rect(3.10, 6.00, -REC + 0.14, -REC + 0.22),
          0.0, 3.05, mats["Toy_glass"])
    prism("entry_jambL", EMB.rect(2.92, 3.14, -REC + 0.06, -REC + 0.26),
          0.0, 3.25, mats["Toy_trim"])
    prism("entry_jambR", EMB.rect(5.96, 6.18, -REC + 0.06, -REC + 0.26),
          0.0, 3.25, mats["Toy_trim"])
    # 3b. entrance canopy - a thin flat slab reaching out past the building line
    prism("entry_canopy", EMB.rect(2.40, 6.70, -REC - EMBED, 0.35),
          3.28, 3.48, mats["Toy_trim"])
    prism("entry_canopy_soffit", EMB.rect(2.44, 6.66, -REC + 0.05, 0.31),
          3.22, 3.28, mats["Toy_ink"])
    # 3c. signage band: COMMONWEALTH CLUB reads as one chunky band at city scale
    prism("sign_band", EMB.rect(0.30, tw - 0.30, -REC - EMBED, -REC + 0.16),
          Z_L2 - 0.45, Z_L2 + 0.30, mats["Toy_trim"])
    prism("addr_plate", EMB.rect(6.55, 7.25, -REC + 0.12, -REC + 0.22),
          Z_L2 - 0.30, Z_L2 + 0.06, mats["Toy_ink"])
    # 3d. the curtain wall itself: one glass field, five bays of mullions
    Z_CW0, Z_CW1 = Z_L2 + 0.80, Z_HEAD - 0.30
    prism("cw_glass", EMB.rect(0.62, tw - 0.62, -EMBED, 0.10), Z_CW0, Z_CW1,
          mats["Toy_glass"])
    n_bays = 5
    t_a, t_b = 0.62, tw - 0.62
    for i in range(n_bays + 1):
        t = t_a + (t_b - t_a) * i / n_bays
        prism(f"cw_mull{i}", EMB.rect(t - 0.10, t + 0.10, -EMBED, 0.24),
              Z_CW0 - 0.05, Z_CW1 + 0.05, mats["Toy_trim"])
    # spandrel band at the level-3 floor line - measured at 11.0-12.4 m
    prism("cw_spandrel", EMB.rect(0.62, tw - 0.62, 0.02, 0.16), Z_L3 - 0.20,
          Z_L3 + 0.55, mats["Toy_glassl"])
    # horizontal transoms. Without them the five bays read as one 12 m sheet of
    # glass and the building loses its storeys - the first pass had exactly that
    # problem. Two lines: one through the double-height auditorium volume, one
    # through the third floor, both at the heights the rectified elevation shows.
    for i, z in enumerate((7.90, 13.70)):
        prism(f"cw_transom{i}", EMB.rect(0.62, tw - 0.62, -EMBED, 0.15),
              z, z + 0.14, mats["Toy_trim"])
    # jamb returns closing the curtain wall against both party walls
    prism("cw_jamb_nw", EMB.rect(0.0, 0.66, -EMBED, 0.18), Z_CW0 - 0.15,
          Z_HEAD, mats["Toy_trim"])
    prism("cw_jamb_se", EMB.rect(tw - 0.66, tw, -EMBED, 0.18), Z_CW0 - 0.15,
          Z_HEAD, mats["Toy_trim"])
    prism("cw_head", EMB.rect(0.0, tw, -EMBED, 0.20), Z_CW1, Z_HEAD,
          mats["Toy_trim"])
    # 3e. the projecting roof eyebrow - the top edge of the whole asset, and
    #     thickened well past its real section so it survives at city distance
    prism("roof_fascia", EMB.rect(-0.16, tw + 0.16, -0.40, 0.66),
          Z_HEAD - 0.05, Z_FASCIA, mats["Toy_trim"])
    prism("roof_fascia_soffit", EMB.rect(-0.12, tw + 0.12, 0.16, 0.62),
          Z_HEAD - 0.11, Z_HEAD - 0.05, mats["Toy_ink"])

    # ---- 4. THE STEUART STREET END (south-west) - the restored 1910 front.
    #         t = 0 at the south-east corner.
    ts = STE.length
    tc = ts / 2.0
    # 4a. plinth, sill band, storefront
    prism("ste_plinth", STE.rect(0.0, ts, -EMBED, 0.10), 0.0, 0.55,
          mats["Toy_sand"])
    # t = 0 is the SOUTH-EAST corner of this face. The doorway is at the
    # south-east end and the three storefront bays run north-west from it -
    # that is the order in the Street View frame, read against the seven-storey
    # brick neighbour that stands on the south-east side. The first pass had
    # them the other way round, which put the door against the Audiffred.
    prism("ste_doorfr", STE.rect(0.55, 2.27, -EMBED, 0.07), 0.0, 3.00,
          mats["Toy_trim"])
    prism("ste_door", STE.rect(0.71, 2.11, 0.05, 0.12), 0.0, 2.85,
          mats["Toy_ink"])
    for i, (a, b) in enumerate(((2.75, 6.05), (6.45, 9.75), (10.15, 13.35))):
        opening(f"ste_shop{i}", STE, a, b, 0.85, 4.05, mats, margin=0.15)
    prism("ste_sill_band", STE.rect(0.0, ts, -EMBED, 0.14), 4.85, 5.10,
          mats["Toy_trim"])
    # 4b. upper storey: four tall windows in a 2 + blank centre + 2 rhythm.
    #     The blank centre bay is what makes this face read as 1910 rather than
    #     as a generic punched wall - keep it.
    for i, t in enumerate((2.05, 4.35, 9.55, 11.85)):
        opening(f"ste_win{i}", STE, t - 0.80, t + 0.80, 5.40, 8.10, mats,
                margin=0.17)
        prism(f"ste_pilas{i}", STE.rect(t + 1.08, t + 1.42, -EMBED, 0.13),
              5.10, 9.45, mats["Toy_trim"])
    # 4c. frieze, modillions, cornice, pediment
    prism("ste_frieze_lo", STE.rect(0.0, ts, -EMBED, 0.12), 9.45, 9.62,
          mats["Toy_trim"])
    prism("ste_frieze_hi", STE.rect(0.0, ts, -EMBED, 0.12), 10.62, 10.79,
          mats["Toy_trim"])
    for i in range(6):
        t = 1.30 + i * 2.26
        prism(f"ste_modil{i}", STE.rect(t - 0.18, t + 0.18, -EMBED, 0.30),
              10.65, 11.22, mats["Toy_trim"])
    prism("ste_cornice", STE.rect(-0.10, ts + 0.10, -EMBED, 0.34),
          11.22, Z_HIST_CORN, mats["Toy_trim"])
    prism("ste_cornice_cap", STE.rect(-0.14, ts + 0.14, -EMBED, 0.38),
          Z_HIST_CORN, Z_HIST_CORN + 0.09, mats["Toy_ink"])
    # The pediment is a raking cornice with a recessed tympanum, NOT a filled
    # triangle with a dark cap: the first pass capped it in Toy_ink and it
    # rendered as a black arrowhead sitting on the navy of the set-back glazing
    # behind. The cream raking moulding against the Toy_stone tympanum is what
    # actually reads at city distance.
    half = 4.50
    plate("ste_pediment", STE,
          [(tc - half, Z_HIST_CORN - 0.12), (tc + half, Z_HIST_CORN - 0.12),
           (tc, Z_HIST_APEX)], -EMBED, 0.42, mats["Toy_trim"])
    plate("ste_tympanum", STE,
          [(tc - half + 0.60, Z_HIST_CORN + 0.06), (tc + half - 0.60, Z_HIST_CORN + 0.06),
           (tc, Z_HIST_APEX - 0.42)], 0.16, 0.28, mats["Toy_stone"])

    # ---- 5. the set-back glazed third floor behind the historic front, and the
    #         stair / lift over-run box on the south-east side.
    prism("setback_glass", slab(SETBACK_D, STEP_U + 0.30, 0.35, W - 0.35),
          Z_L3 - 0.10, Z_SETBACK, mats["Toy_glass"], mat_top=mats["Toy_trim"])
    prism("setback_head", slab(SETBACK_D - 0.08, STEP_U + 0.30, 0.27, W - 0.27),
          Z_SETBACK, Z_SETBACK + 0.22, mats["Toy_trim"])
    prism("overrun", slab(SETBACK_D + 0.40, SETBACK_D + 4.00, 0.45, 4.05),
          Z_L3 - 0.10, Z_OVERRUN, mats["Toy_trim"])
    # the quiet strip of roof behind the historic parapet
    prism("ste_roof_strip", slab(0.30, SETBACK_D, 0.30, W - 0.30),
          Z_L3 - 0.10, Z_L3 + 0.06, mats["Toy_sand"])

    # ---- 6. THE ROOF TERRACE. A gradient along the long axis: quiet strip at
    #         the Steuart end, planted garden through the middle, paved public
    #         deck at the Embarcadero end. This is the largest surface the app's
    #         camera ever sees of this building, so it is designed as a plan,
    #         not left as a membrane: the first pass had two 15 m blank
    #         rectangles here and read as a lid.
    prism("roof_field", slab(STEP_U, L - 0.35, 0.35, W - 0.35), Z_ROOF - 0.12,
          Z_ROOF + 0.02, mats["Toy_stone"])
    # 6a. the paved public deck at the Embarcadero end, with joint bands
    prism("roof_deck", slab(26.8, L - 0.55, 0.55, W - 0.55), Z_ROOF + 0.02,
          Z_ROOF + 0.12, mats["Toy_sand"])
    for i in range(5):
        u = 28.4 + i * 2.7
        prism(f"deck_joint{i}", slab(u, u + 0.14, 0.55, W - 0.55),
              Z_ROOF + 0.10, Z_ROOF + 0.15, mats["Toy_stone"])
    # 6b. three planted beds through the middle, split by two cross paths
    for i, (a, b) in enumerate(((13.9, 17.7), (18.5, 22.3), (23.1, 26.2))):
        prism(f"bed_kerb{i}", slab(a, b, 0.80, W - 0.80), Z_ROOF - 0.02,
              Z_ROOF + 0.34, mats["Toy_stone"])
        prism(f"bed{i}", slab(a + 0.22, b - 0.22, 1.02, W - 1.02),
              Z_ROOF + 0.20, Z_ROOF + 0.40, mats["Toy_mint"])
    # shrub masses - the planting has to have HEIGHT or it reads as green paint
    for i, (u, sv, r) in enumerate(((15.1, 4.3, 1.05), (16.6, 9.6, 0.85),
                                    (19.7, 3.6, 0.95), (21.2, 10.1, 1.10),
                                    (24.2, 4.9, 0.90), (25.3, 9.2, 1.00))):
        prism(f"shrub{i}", slab(u - r, u + r, sv - r, sv + r), Z_ROOF + 0.30,
              Z_ROOF + 0.30 + min(r * 1.15, 1.05), mats["Toy_mint"])
    # 6c. planter row along the south-east edge of the deck
    for i in range(4):
        u = 29.0 + i * 2.9
        prism(f"planter{i}", slab(u, u + 1.70, 1.05, 2.05), Z_ROOF + 0.10,
              Z_ROOF + 0.70, mats["Toy_stone"])
        prism(f"planter_top{i}", slab(u + 0.14, u + 1.56, 1.19, 1.91),
              Z_ROOF + 0.62, Z_ROOF + 0.92, mats["Toy_mint"])
    # 6d. a low timber trellis screen down each side of the deck. The first
    #     pass put a 2.55 m pergola here; it stood 1.75 m proud of the roof
    #     fascia and made the bbox top 19.15 m, which would have driven the
    #     loader's scale factor off 1.0. Nothing on this deck is allowed above
    #     17.35 m.
    for i in range(9):
        u = 28.6 + i * 1.45
        prism(f"trellis_se{i}", slab(u, u + 0.13, 0.70, 0.86), Z_ROOF + 0.10,
              Z_ROOF + 1.15, mats["Toy_trim"])
        prism(f"trellis_nw{i}", slab(u, u + 0.13, W - 0.86, W - 0.70),
              Z_ROOF + 0.10, Z_ROOF + 1.15, mats["Toy_trim"])
    prism("trellis_rail_se", slab(28.4, 40.6, 0.70, 0.86), Z_ROOF + 1.03,
          Z_ROOF + 1.19, mats["Toy_trim"])
    prism("trellis_rail_nw", slab(28.4, 40.6, W - 0.86, W - 0.70),
          Z_ROOF + 1.03, Z_ROOF + 1.19, mats["Toy_trim"])

    # 6e. plant enclosure between the step and the garden. There is NO mid-roof
    #     penthouse: the building's only stair / lift over-run is the box at the
    #     Steuart end (section 5), which is what the Street View elevation
    #     actually shows. A second one here was invented in the first pass, and
    #     it both duplicated that box and pushed the bbox top past the fascia.
    prism("plant_screen", slab(8.6, 12.6, 1.10, 5.40), Z_ROOF - 0.10,
          Z_ROOF + 1.40, mats["Toy_trim"], mat_top=mats["Toy_stone"])
    for i, (u, sv) in enumerate(((9.2, 7.2), (10.9, 7.2), (12.2, 9.4))):
        prism(f"plant_box{i}", slab(u, u + 1.20, sv, sv + 1.00),
              Z_ROOF + 0.02, Z_ROOF + 0.85, mats["Toy_stone"])
    # 6f. three roof lights over the deck
    for i in range(3):
        u = 29.3 + i * 3.6
        prism(f"skylight_kerb{i}", slab(u - 0.16, u + 1.96, 5.34, 7.46),
              Z_ROOF + 0.06, Z_ROOF + 0.20, mats["Toy_trim"])
        prism(f"skylight{i}", slab(u, u + 1.80, 5.50, 7.30), Z_ROOF + 0.14,
              Z_ROOF + 0.40, mats["Toy_glassl"])

    # ---- 7. NIGHT. One lantern plus two supports; the 1910 front stays dark.
    glow_quad("cw_glow", EMB, 0.70, tw - 0.70, Z_CW0 + 0.05, Z_CW1 - 0.05,
              mats["Toy_glassl_Glow"], 0.14)
    glow_quad("sign_glow", EMB, 0.36, tw - 0.36, Z_L2 - 0.38, Z_L2 + 0.24,
              mats["Toy_trim_Glow"], -REC + 0.20)
    glow_quad("lobby_glow", EMB, 0.62, tw - 0.62, 0.30, Z_L2 - 0.50,
              mats["Toy_mustard_Glow"], -REC + 0.20)
    for i, (a, b) in enumerate(((2.75, 6.05), (6.45, 9.75), (10.15, 13.35))):
        glow_quad(f"shop{i}_glow", STE, a, b, 0.90, 4.00,
                  mats["Toy_mustard_Glow"], 0.18)
    # aerial cues
    # The set-back third floor glows on its own SOUTH-WEST face, the one that
    # shows above the historic Steuart parapet - that is where the teal band is
    # visible in the photographs. The first pass put this on the NORTH-WEST
    # party wall, using t as if it ran from the Embarcadero end; NW_PARTY's t
    # actually starts at the Steuart corner, so the quad landed buried inside
    # the solid body at the far end of the building. The validator's ray test
    # caught it (19 of 20 glow faces outward). A party wall against the
    # Audiffred could never have shown it anyway.
    glow_quad("setback_glow", STE, 0.70, W_WIDE - 0.70, Z_L3 + 0.20,
              Z_SETBACK - 0.20, mats["Toy_glassl_Glow"], -(SETBACK_D - 0.06))
    for i in range(3):
        u = 29.3 + i * 3.6
        glow_roof(f"skylight{i}_glow", slab(u + 0.05, u + 1.75, 5.55, 7.25),
                  Z_ROOF + 0.44, mats["Toy_glassl_Glow"])

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.10/2. Glazing, frames, mullions, modillions and glow shells are small
    # and numerous - a token softening or none at all is what keeps this under
    # cap and stops thin plates collapsing into slivers.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        n = obj.name
        if n.endswith("_glow"):
            continue
        if n.startswith(("cw_mull", "cw_transom", "ste_modil", "ste_win", "ste_shop",
                         "ste_pilas", "ste_frieze", "ste_door", "entry_",
                         "addr_plate", "skylight_kerb", "deck_joint",
                         "parapet_cap", "roof_fascia_soffit", "trellis_",
                         "bed_kerb", "planter_top",
                         "ste_cornice_cap", "ste_tympanum",
                         "lobby_", "setback_head",
                         "ste_sill_band", "ste_roof_strip")):
            continue
        if n.startswith(("cw_glass", "cw_spandrel", "cw_jamb", "cw_head",
                         "sign_band")):
            bevel(obj, width=0.04, segments=1)
        else:
            bevel(obj)

    recentre()
    return scene


ANCHOR_SHIFT = [0.0, 0.0]


def recentre():
    """Move the model so its XY bbox centre sits on the origin (contract rule 2),
    and record the shift so the manifest anchor can be moved by the same vector
    and the building still lands on its real footprint."""
    mn = Vector((1e9, 1e9))
    mx = Vector((-1e9, -1e9))
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    for o in meshes:
        for v in o.data.vertices:
            for i in range(2):
                mn[i] = min(mn[i], v.co[i])
                mx[i] = max(mx[i], v.co[i])
    cx, cy = (mn[0] + mx[0]) / 2.0, (mn[1] + mx[1]) / 2.0
    ANCHOR_SHIFT[0], ANCHOR_SHIFT[1] = cx, cy
    for o in meshes:
        for v in o.data.vertices:
            v.co.x -= cx
            v.co.y -= cy


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
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    lon = DESIGN_ANCHOR[0] + ANCHOR_SHIFT[0] / LON_M
    lat = DESIGN_ANCHOR[1] + ANCHOR_SHIFT[1] / LAT_M
    print(f"[build] footprint: {L_LONG:.2f} x {W_WIDE:.2f} m = {L_LONG * W_WIDE:.1f} m2")
    print(f"[build] design (footprint centroid) anchor: {DESIGN_ANCHOR}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] Embarcadero faces {EMB.heading:.2f} deg; Steuart {STE.heading:.2f}; "
          f"SE party {SE_PARTY.heading:.2f}; NW party {NW_PARTY.heading:.2f}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "110-embarcadero.blend")
    glb = os.path.join(out, "110-embarcadero.glb")
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
