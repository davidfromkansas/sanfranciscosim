"""Deterministic build of the 551 Third Street (Shell station) miniature.

Run headless:
    blender -b --python build_551_third.py -- --out 551-third.glb

Everything is authored in the site-aligned (u, v) frame of the asset plan
(docs/asset-plans/551-third.md 2.3) and rotated into true world axes on the way
into Blender, so the exported GLB has +Y = true north and +X = east and drops
into the city at its real heading.  z is metres above the apron underside; the
apron's own top sits at APRON_T so nothing floats.

    u  positive toward bearing 315 (north-west, along 3rd Street)
    v  positive toward bearing  45 (north-east, into the lot from the street)

Origin (u, v) = (0, 0) is the parcel centroid, which is the manifest anchor.
"""

import argparse
import math
import sys

import bmesh
import bpy

# --- site constants (metres; all measured, see the plan's 2.1 and 2.3) --------

LOT_U0, LOT_U1 = -21.1, 18.6
LOT_V0, LOT_V1 = -11.4, 9.0

APRON_T = 0.14  # apron slab top; the forecourt ground plane

OCT_R = 5.40  # octagon circumradius
OCT_U = 2.10  # both umbrellas share this u
OCT_FLAT = OCT_R * math.cos(math.radians(22.5))  # centre -> flat side
OCT_V = (2.24, -7.74)  # tangent pair straddling v = -2.75

CANOPY_UNDER = 4.30  # soffit
CANOPY_DECK = 5.00  # deck slab top, before ribs
CANOPY_TOP = 5.10  # rib top == the deck top quoted in the plan
CREST = 6.60  # pecten crown top == targetHeightM

KIOSK_U0, KIOSK_U1 = -21.1, -14.3
KIOSK_V0, KIOSK_V1 = -5.0, 8.0
KIOSK_TOP = 3.91

LANES = (5.40, -2.75, -10.60)
CURB_CUTS = ((5.0, 13.0), (-10.0, -2.0))  # u ranges left open in the 3rd St kerb

GLOW_GAP = 0.02  # how far a _Glow shell stands off the surface it lights

# --- palette (sf-asset-check SKILL.md step 7), sRGB hex ----------------------

PALETTE = {
    "Toy_cream": "f2ede3",
    "Toy_trim": "f3efe6",
    "Toy_teal": "3fa8a0",
    "Toy_mustard": "d9a441",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_ink": "3a3530",
    "Toy_roofd": "45454a",
    "Toy_stone": "d9d2c2",
    "Toy_red": "c4453c",
    "Toy_steel": "9aa0a6",
    "Toy_white": "f7f4ec",
}
GLOWS = ("Toy_trim_Glow", "Toy_mustard_Glow", "Toy_glassl_Glow")


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def material(name):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    base = name[:-5] if name.endswith("_Glow") else name
    hexv = PALETTE[base]
    rgb = tuple(srgb_to_linear(int(hexv[i : i + 2], 16) / 255.0) for i in (0, 2, 4))
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.85
    bsdf.inputs["Metallic"].default_value = 0.0
    return mat


# --- geometry helpers --------------------------------------------------------

COS45 = math.sqrt(0.5)


def world(u, v, z):
    """Site-aligned (u, v) -> Blender world (x=east, y=north, z=up)."""
    return (-COS45 * u + COS45 * v, COS45 * u + COS45 * v, z)


def prism(name, ring_uv, z0, z1, mat, bevel=0.06, segments=2):
    """Extrude a closed (u, v) ring between two heights into a solid."""
    mesh = bpy.data.meshes.new(name)
    verts = [world(u, v, z0) for u, v in ring_uv] + [world(u, v, z1) for u, v in ring_uv]
    n = len(ring_uv)
    faces = [list(range(n - 1, -1, -1)), list(range(n, 2 * n))]
    faces += [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
    mesh.from_pydata(verts, [], faces)
    mesh.validate()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(material(mat))
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if bevel > 0:
        bmesh.ops.bevel(
            bm,
            geom=list(bm.edges) + list(bm.verts),
            offset=bevel,
            segments=segments,
            profile=0.5,
            affect="EDGES",
            clamp_overlap=True,
        )
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    return obj


def box(name, u0, u1, v0, v1, z0, z1, mat, bevel=0.06, segments=2):
    return prism(
        name, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], z0, z1, mat, bevel, segments
    )


def octagon(cu, cv, r):
    return [
        (
            cu + r * math.cos(math.radians(22.5 + 45 * k)),
            cv + r * math.sin(math.radians(22.5 + 45 * k)),
        )
        for k in range(8)
    ]


def ngon(cu, cv, r, n, phase=0.0):
    return [
        (
            cu + r * math.cos(math.radians(phase + 360 * k / n)),
            cv + r * math.sin(math.radians(phase + 360 * k / n)),
        )
        for k in range(n)
    ]


def scallop(cu, cv, r_out, r_in, lobes=12):
    ring = []
    for k in range(lobes * 2):
        a = math.radians(360 * k / (lobes * 2))
        r = r_out if k % 2 == 0 else r_in
        ring.append((cu + r * math.cos(a), cv + r * math.sin(a)))
    return ring


def plate_uv(name, ring_uv, z0, z1, mat):
    """A thin shell: no bevel, so it stays a clean closed slab."""
    return prism(name, ring_uv, z0, z1, mat, bevel=0.0)


def upright(name, ring_uv, z0, z1, mat, axis="v", offset=0.0):
    """Build a vertical plate standing in the u/z or v/z plane.

    ring_uv is given as (along, z) pairs; `offset` is the fixed coordinate on the
    other site axis.  Used for the pecten, which faces -v.
    """
    mesh = bpy.data.meshes.new(name)
    verts = []
    for along, zz in ring_uv:
        if axis == "v":
            verts.append(world(along, offset, zz))
        else:
            verts.append(world(offset, along, zz))
    n = len(ring_uv)
    for along, zz in ring_uv:
        if axis == "v":
            verts.append(world(along, offset + (z1 - z0), zz))
        else:
            verts.append(world(offset + (z1 - z0), along, zz))
    faces = [list(range(n - 1, -1, -1)), list(range(n, 2 * n))]
    faces += [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
    mesh.from_pydata(verts, [], faces)
    mesh.validate()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(material(mat))
    bpy.context.scene.collection.objects.link(obj)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    return obj


def capsule(name, cu, cv, r, z0, z1, mat, segments=8):
    return prism(name, ngon(cu, cv, r, segments), z0, z1, mat, bevel=r * 0.45, segments=2)


# --- the model ---------------------------------------------------------------


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def build_apron():
    box(
        "apron",
        LOT_U0,
        LOT_U1,
        LOT_V0,
        LOT_V1,
        0.0,
        APRON_T,
        "Toy_roofd",
        bevel=0.04,
        segments=1,
    )

    # perimeter kerb, broken by the two 3rd Street curb cuts
    k = 0.30
    kt = APRON_T + 0.18
    box("kerb_ne", LOT_U0, LOT_U1, LOT_V1 - k, LOT_V1, APRON_T, kt, "Toy_stone", 0.04, 1)
    box("kerb_nw", LOT_U1 - k, LOT_U1, LOT_V0, LOT_V1, APRON_T, kt, "Toy_stone", 0.04, 1)
    box("kerb_se", LOT_U0, LOT_U0 + k, LOT_V0, LOT_V1, APRON_T, kt, "Toy_stone", 0.04, 1)
    spans, cursor = [], LOT_U0
    for cut0, cut1 in sorted(CURB_CUTS):
        spans.append((cursor, cut0))
        cursor = cut1
    spans.append((cursor, LOT_U1))
    for i, (a, b) in enumerate(spans):
        if b - a > 0.2:
            box(
                f"kerb_sw_{i}", a, b, LOT_V0, LOT_V0 + k, APRON_T, kt, "Toy_stone", 0.04, 1
            )

    # painted edge line just inside the kerb — keeps the open apron from reading
    # as a bare parking lot without adding clutter (style bible §10)
    e0, e1 = LOT_U0 + 1.0, LOT_U1 - 1.0
    f0, f1 = LOT_V0 + 1.0, LOT_V1 - 1.0
    for nm, a, b, c, d_ in (
        ("edge_ne", e0, e1, f1 - 0.11, f1 + 0.11),
        ("edge_sw", e0, e1, f0 - 0.11, f0 + 0.11),
        ("edge_nw", e1 - 0.11, e1 + 0.11, f0, f1),
        ("edge_se", e0 - 0.11, e0 + 0.11, f0, f1),
    ):
        plate_uv(nm, [(a, c), (b, c), (b, d_), (a, d_)], APRON_T, APRON_T + 0.015, "Toy_trim")

    # a chevron at each curb cut, pointing into the forecourt
    for i, (c0, c1) in enumerate(CURB_CUTS):
        cu = (c0 + c1) / 2
        for j, off in enumerate((0.0, 1.1)):
            base = LOT_V0 + 1.9 + off
            plate_uv(
                f"chev_{i}_{j}",
                [(cu - 1.5, base), (cu, base + 0.85), (cu + 1.5, base),
                 (cu + 1.5, base + 0.36), (cu, base + 1.21), (cu - 1.5, base + 0.36)],
                APRON_T,
                APRON_T + 0.015,
                "Toy_trim",
            )

    for i, v in enumerate(LANES):
        plate_uv(
            f"lane_{i}",
            [
                (LOT_U0 + 1.5, v - 0.125),
                (LOT_U1 - 1.5, v - 0.125),
                (LOT_U1 - 1.5, v + 0.125),
                (LOT_U0 + 1.5, v + 0.125),
            ],
            APRON_T,
            APRON_T + 0.015,
            "Toy_trim",
        )


def build_umbrella(idx, cv):
    tag = f"umb{idx}"
    deck = octagon(OCT_U, cv, OCT_R)

    prism(f"{tag}_deck", deck, CANOPY_UNDER, CANOPY_DECK, "Toy_stone", 0.08, 2)

    # eight ribs from the column to each vertex
    for k, (vu, vv) in enumerate(deck):
        du, dv = vu - OCT_U, vv - cv
        L = math.hypot(du, dv)
        nu, nv = du / L, dv / L
        pu, pv = -nv * 0.175, nu * 0.175
        ring = [
            (OCT_U + pu, cv + pv),
            (OCT_U + nu * (L - 0.15) + pu, cv + nv * (L - 0.15) + pv),
            (OCT_U + nu * (L - 0.15) - pu, cv + nv * (L - 0.15) - pv),
            (OCT_U - pu, cv - pv),
        ]
        prism(f"{tag}_rib{k}", ring, CANOPY_DECK, CANOPY_TOP, "Toy_white", 0.03, 1)

    # fascia: eight slabs, skipping the side shared with the other umbrella
    shared = 6 if cv > -2.75 else 2  # edge whose midpoint faces the waist
    outer = octagon(OCT_U, cv, OCT_R + 0.12)
    for k in range(8):
        if k == shared:
            continue
        a, b = deck[k], deck[(k + 1) % 8]
        oa, ob = outer[k], outer[(k + 1) % 8]
        ring = [a, b, ob, oa]
        prism(f"{tag}_fascia_lo{k}", ring, CANOPY_UNDER, CANOPY_UNDER + 0.45, "Toy_mustard", 0.03, 1)
        prism(f"{tag}_fascia_hi{k}", ring, CANOPY_UNDER + 0.45, CANOPY_TOP, "Toy_red", 0.03, 1)
        # the 2003-04 LED lightbar: a thin glow shell standing off the yellow band
        glow = octagon(OCT_U, cv, OCT_R + 0.12 + GLOW_GAP)
        ga, gb = glow[k], glow[(k + 1) % 8]
        plate_uv(
            f"{tag}_lightbar{k}",
            [oa, ob, gb, ga],
            CANOPY_UNDER + 0.10,
            CANOPY_UNDER + 0.40,
            "Toy_mustard_Glow",
        )

    # lit soffit: opaque white is the primary surface, the glow shell hangs below
    plate_uv(
        f"{tag}_soffit_glow",
        octagon(OCT_U, cv, OCT_R - 0.20),
        CANOPY_UNDER - GLOW_GAP - 0.03,
        CANOPY_UNDER - GLOW_GAP,
        "Toy_trim_Glow",
    )

    # central column with a flared capital
    box(f"{tag}_col", OCT_U - 0.275, OCT_U + 0.275, cv - 0.275, cv + 0.275, APRON_T, 4.00, "Toy_steel", 0.05, 2)
    prism(
        f"{tag}_capital",
        [(OCT_U - 0.7, cv - 0.7), (OCT_U + 0.7, cv - 0.7), (OCT_U + 0.7, cv + 0.7), (OCT_U - 0.7, cv + 0.7)],
        4.00,
        CANOPY_UNDER,
        "Toy_steel",
        0.06,
        2,
    )

    # island, dispensers, bollards
    it = APRON_T + 0.20
    box(f"{tag}_island", OCT_U - 3.5, OCT_U + 3.5, cv - 0.6, cv + 0.6, APRON_T, it, "Toy_stone", 0.05, 2)
    for s, du in ((0, -1.9), (1, 1.9)):
        box(f"{tag}_disp{s}", OCT_U + du - 0.55, OCT_U + du + 0.55, cv - 0.35, cv + 0.35, it, it + 1.90, "Toy_trim", 0.06, 2)
        for face, dv in ((0, -0.35), (1, 0.35)):
            sign = -1 if dv < 0 else 1
            box(
                f"{tag}_disp{s}_face{face}",
                OCT_U + du - 0.42,
                OCT_U + du + 0.42,
                cv + dv,
                cv + dv + sign * 0.06,
                it + 0.75,
                it + 1.55,
                "Toy_ink",
                0.03,
                1,
            )
            box(
                f"{tag}_disp{s}_hose{face}",
                OCT_U + du + sign * 0.30,
                OCT_U + du + sign * 0.44,
                cv + dv,
                cv + dv + sign * 0.22,
                it + 0.45,
                it + 1.35,
                "Toy_ink",
                0.05,
                1,
            )
        box(f"{tag}_disp{s}_cap", OCT_U + du - 0.58, OCT_U + du + 0.58, cv - 0.38, cv + 0.38, it + 1.90, it + 2.06, "Toy_red", 0.05, 2)
    for s, du in ((0, -3.7), (1, 3.7)):
        capsule(f"{tag}_boll{s}", OCT_U + du, cv, 0.11, APRON_T, APRON_T + 1.0, "Toy_mustard")


def build_pecten():
    """Scalloped disc on the umbrella that faces 3rd Street. Sets the crest."""
    cv = OCT_V[1]
    face_v = cv - OCT_FLAT - 0.12  # outer face of that umbrella's fascia
    cz = CREST - 0.90
    back = scallop(OCT_U, cz, 1.00, 1.00, lobes=6)  # a plain 12-gon backing ring
    upright("pecten_back", back, face_v, face_v - 0.12, "Toy_red", axis="v", offset=face_v)
    disc = scallop(OCT_U, cz, 0.90, 0.70, lobes=12)
    upright("pecten_face", disc, face_v - 0.12, face_v - 0.37, "Toy_mustard", axis="v", offset=face_v - 0.12)
    glow = scallop(OCT_U, cz, 0.88, 0.68, lobes=12)
    upright(
        "pecten_glow",
        glow,
        face_v - 0.37 - GLOW_GAP,
        face_v - 0.37 - GLOW_GAP - 0.03,
        "Toy_mustard_Glow",
        axis="v",
        offset=face_v - 0.37 - GLOW_GAP,
    )
    box("pecten_stem", OCT_U - 0.12, OCT_U + 0.12, face_v - 0.10, face_v + 0.02, CANOPY_TOP - 0.4, cz, "Toy_steel", 0.03, 1)


def build_kiosk():
    cap = 0.35
    box("kiosk_body", KIOSK_U0, KIOSK_U1, KIOSK_V0, KIOSK_V1, APRON_T, KIOSK_TOP - cap, "Toy_cream", 0.08, 2)
    cw = 0.34  # parapet cap is a RING, not a lid: the roof has to read from above
    box("kiosk_cap_nw", KIOSK_U1 - cw, KIOSK_U1 + 0.12, KIOSK_V0 - 0.12, KIOSK_V1 + 0.12, KIOSK_TOP - cap, KIOSK_TOP, "Toy_ink", 0.05, 2)
    box("kiosk_cap_se", KIOSK_U0 - 0.12, KIOSK_U0 + cw, KIOSK_V0 - 0.12, KIOSK_V1 + 0.12, KIOSK_TOP - cap, KIOSK_TOP, "Toy_ink", 0.05, 2)
    box("kiosk_cap_ne", KIOSK_U0 + cw, KIOSK_U1 - cw, KIOSK_V1 - cw, KIOSK_V1 + 0.12, KIOSK_TOP - cap, KIOSK_TOP, "Toy_ink", 0.05, 2)
    box("kiosk_cap_sw", KIOSK_U0 + cw, KIOSK_U1 - cw, KIOSK_V0 - 0.12, KIOSK_V0 + cw, KIOSK_TOP - cap, KIOSK_TOP, "Toy_ink", 0.05, 2)
    box("kiosk_roof", KIOSK_U0 + 0.2, KIOSK_U1 - 0.2, KIOSK_V0 + 0.2, KIOSK_V1 - 0.2, KIOSK_TOP - cap - 0.06, KIOSK_TOP - 0.10, "Toy_stone", 0.03, 1)
    box("kiosk_plant", KIOSK_U0 + 2.6, KIOSK_U0 + 4.2, KIOSK_V0 + 5.2, KIOSK_V0 + 6.6, KIOSK_TOP - 0.10, KIOSK_TOP + 0.65, "Toy_roofd", 0.05, 2)

    # shopfront on the north-west face, looking back at the umbrellas
    f = KIOSK_U1
    box("kiosk_glass", f - 0.10, f + 0.06, KIOSK_V0 + 1.1, KIOSK_V1 - 1.1, 1.00, 2.60, "Toy_glass", 0.03, 1)
    plate_uv(
        "kiosk_glass_glow",
        [
            (f + 0.06, KIOSK_V0 + 1.25),
            (f + 0.06 + GLOW_GAP + 0.03, KIOSK_V0 + 1.25),
            (f + 0.06 + GLOW_GAP + 0.03, KIOSK_V1 - 1.25),
            (f + 0.06, KIOSK_V1 - 1.25),
        ],
        1.10,
        2.50,
        "Toy_glassl_Glow",
    )
    for i, v in enumerate((KIOSK_V0 + 1.1, KIOSK_V1 - 1.1)):
        box(f"kiosk_mull{i}", f - 0.12, f + 0.10, v - 0.11, v + 0.11, APRON_T, 2.72, "Toy_ink", 0.03, 1)
    box("kiosk_head", f - 0.12, f + 0.10, KIOSK_V0 + 1.0, KIOSK_V1 - 1.0, 2.60, 2.72, "Toy_ink", 0.03, 1)
    box("kiosk_door", f - 0.12, f + 0.08, KIOSK_V0 + 2.2, KIOSK_V0 + 3.3, APRON_T, 2.20, "Toy_ink", 0.03, 1)
    box("kiosk_sign", f - 0.14, f + 0.12, KIOSK_V0 + 4.0, KIOSK_V1 - 2.0, 2.85, 3.45, "Toy_red", 0.05, 2)


def build_furniture():
    box("air_water", 7.4, 8.1, 3.9, 4.4, APRON_T, APRON_T + 1.30, "Toy_teal", 0.06, 2)
    box("bin_a", 13.6, 14.2, 1.2, 1.8, APRON_T, APRON_T + 1.05, "Toy_ink", 0.05, 2)
    box("vac", 13.2, 14.0, 5.6, 6.2, APRON_T, APRON_T + 1.25, "Toy_teal", 0.06, 2)
    for i in range(3):
        capsule(f"nw_boll_{i}", 16.9, LOT_V0 + 3.4 + i * 2.6, 0.11, APRON_T, APRON_T + 1.0, "Toy_mustard")
    box("bin_b", 10.5, 11.1, -6.0, -5.4, APRON_T, APRON_T + 1.05, "Toy_ink", 0.05, 2)
    for i, (u, v) in enumerate(((-2.6, 2.24), (-2.6, -7.74))):
        box(f"squeegee_{i}", u - 0.28, u + 0.28, v - 0.22, v + 0.22, APRON_T, APRON_T + 1.15, "Toy_steel", 0.05, 2)
    for i in range(6):
        capsule(f"kerb_boll_{i}", LOT_U0 + 4.0 + i * 5.6, LOT_V0 + 0.75, 0.11, APRON_T, APRON_T + 1.0, "Toy_mustard")


def normalize_and_export(path):
    objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    mn = [1e9] * 3
    mx = [-1e9] * 3
    for o in objs:
        for corner in o.bound_box:
            w = o.matrix_world @ __import__("mathutils").Vector(corner)
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    # base to z=0, XY centre to the origin, crest exactly on CREST
    dz = -mn[2]
    dx = -(mn[0] + mx[0]) / 2
    dy = -(mn[1] + mx[1]) / 2
    for o in objs:
        o.location = (o.location[0] + dx, o.location[1] + dy, o.location[2] + dz)
    bpy.context.view_layer.update()
    top = mx[2] + dz
    if abs(top - CREST) > 1e-6:
        s = CREST / top
        for o in objs:
            o.scale = (s, s, s)
            o.location = (o.location[0] * s, o.location[1] * s, o.location[2] * s)
    bpy.context.view_layer.update()
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.ops.export_scene.gltf(
        filepath=path,
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_yup=True,
        export_cameras=False,
        export_lights=False,
        export_animations=False,
    )


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="551-third.glb")
    ap.add_argument("--blend", default="")
    args = ap.parse_args(argv)

    clear_scene()
    build_apron()
    for i, cv in enumerate(OCT_V):
        build_umbrella(i, cv)
    build_pecten()
    build_kiosk()
    build_furniture()
    normalize_and_export(args.out)
    if args.blend:
        bpy.ops.wm.save_as_mainfile(filepath=args.blend)

    tris = 0
    for o in bpy.context.scene.objects:
        if o.type == "MESH":
            o.data.calc_loop_triangles()
            tris += len(o.data.loop_triangles)
    print(f"[build] objects={len(bpy.context.scene.objects)} tris={tris} -> {args.out}")


if __name__ == "__main__":
    main()
