"""Contract check for the exported street kit (.agents/skills/sf-asset-check).

    blender -b --python validate_streetkit.py -- [--kit DIR] [--json OUT]

Every GLB is re-imported into a *fresh* scene, so what is checked is the file
that ships, not the builder's in-memory state. Prints a PASS/FAIL table and
exits non-zero on any FAIL.
"""

import json
import os
import struct
import sys

import bpy
from mathutils import Vector

# Vehicle-class props stay under 300; the three pieces that are really small
# buildings get 500, per the layer 2 plan.
BUDGET = {"muni_shelter": 500, "market_stall": 500, "parklet": 500}
DEFAULT_BUDGET = 300
# Only these surfaces are allowed to be lights at night.
GLOW_ALLOWED = {
    "sl_standard",
    "sl_pathofgold",
    "sl_residential",
    "traffic_signal",
    "muni_shelter",
}
MAX_DIM = 10.0  # nothing in a furniture kit is taller than a mast-arm lamp


def gltf_json(path):
    """The GLB's JSON chunk. Blender's importer normalises a lot away; the app
    reads these fields, so the file's own declarations are what get checked."""
    with open(path, "rb") as fh:
        blob = fh.read()
    magic, _, _ = struct.unpack_from("<III", blob, 0)
    assert magic == 0x46546C67, path
    length, kind = struct.unpack_from("<II", blob, 12)
    assert kind == 0x4E4F534A, path
    return json.loads(blob[20 : 20 + length].decode("utf8"))


def inspect(path, piece_id):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)

    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    other = [o.type for o in bpy.data.objects if o.type not in ("MESH", "EMPTY")]

    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    tris = 0
    mats = {}
    for o in meshes:
        me = o.data
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for m in me.materials:
            if m:
                mats[m.name] = m
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    dims = [mx[i] - mn[i] for i in range(3)]

    gltf = gltf_json(path)
    textured = sorted(set(gltf.get("images", []) and ["<image>"] or []))
    transparent = []
    rough = []
    for gm in gltf.get("materials", []):
        pbr = gm.get("pbrMetallicRoughness", {})
        if gm.get("alphaMode", "OPAQUE") != "OPAQUE" or pbr.get("baseColorFactor", [1, 1, 1, 1])[3] < 0.999:
            transparent.append(gm.get("name", "?"))
        if any(k.endswith("Texture") for k in list(pbr) + list(gm)):
            textured.append(gm.get("name", "?"))
        rough.append((gm.get("name", "?"), round(pbr.get("roughnessFactor", 1.0), 3)))

    checks = []
    checks.append(("units_metres", max(dims) <= MAX_DIM and max(dims) > 0.3, f"max dim {max(dims):.2f} m"))
    checks.append(("origin_on_ground", abs(mn.z) < 1e-3, f"min z {mn.z:.4f}"))
    checks.append(
        (
            "origin_centred",
            abs(mn.x + mx.x) < 2e-3 and abs(mn.y + mx.y) < 2e-3,
            f"centre ({(mn.x + mx.x) / 2:.4f}, {(mn.y + mx.y) / 2:.4f})",
        )
    )
    budget = BUDGET.get(piece_id, DEFAULT_BUDGET)
    checks.append(("tri_budget", tris <= budget, f"{tris} / {budget}"))
    bad_names = [n for n in mats if not n.startswith("Toy_")]
    checks.append(("materials_toy", not bad_names, ",".join(sorted(mats)) or "none"))
    checks.append(("no_textures", not textured, ",".join(sorted(set(textured))) or "none"))
    checks.append(("opaque", not transparent, ",".join(sorted(set(transparent))) or "none"))
    checks.append(
        (
            "roughness",
            bool(rough) and all(abs(r - 0.85) < 0.06 for _, r in rough),
            f"{min(r for _, r in rough)}-{max(r for _, r in rough)}" if rough else "none",
        )
    )
    glow = sorted(n for n in mats if n.endswith("_Glow"))
    checks.append(
        (
            "glow_only_where_lit",
            (not glow) or piece_id in GLOW_ALLOWED,
            ",".join(glow) or "none",
        )
    )
    extra = other + [f"gltf:{k}" for k in ("cameras", "animations", "skins") if gltf.get(k)]
    checks.append(("no_cameras_lights", not extra, ",".join(sorted(set(extra))) or "none"))
    checks.append(("no_animation", not bpy.data.actions, f"{len(bpy.data.actions)} actions"))
    checks.append(
        ("no_skinning", all(not o.vertex_groups for o in meshes), "no vertex groups")
    )

    return {
        "id": piece_id,
        "tris": tris,
        "dims": [round(d, 3) for d in dims],
        "materials": sorted(mats),
        "glow": glow,
        "checks": [{"name": n, "pass": bool(ok), "detail": d} for n, ok, d in checks],
        "pass": all(ok for _, ok, _ in checks),
    }


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    kit = arg(
        "--kit",
        os.path.abspath(os.path.join(here, "..", "..", "app", "public", "sf-assets", "streetkit")),
    )
    out_json = arg("--json", os.path.join(here, "streetkit-contract.json"))
    with open(os.path.join(kit, "streetkit_index.json"), encoding="utf8") as fh:
        index = json.load(fh)

    results = []
    for piece in index["pieces"]:
        r = inspect(os.path.join(kit, piece["file"]), piece["id"])
        # The index is what the app trusts before it has parsed a mesh, so it
        # has to agree with the file to a tenth of a metre.
        claimed = piece["dims"]
        agree = all(abs(claimed[i] - r["dims"][i]) < 0.1 for i in range(3)) and piece["tris"] == r["tris"]
        r["checks"].append({"name": "index_agrees", "pass": agree, "detail": f"index {claimed} / {piece['tris']}"})
        r["pass"] = r["pass"] and agree
        results.append(r)

    width = max(len(r["id"]) for r in results)
    names = [c["name"] for c in results[0]["checks"]]
    print("\n[contract] piece".ljust(width + 12) + "  ".join(n[:9].rjust(9) for n in names))
    for r in results:
        row = "  ".join(("PASS" if c["pass"] else "FAIL").rjust(9) for c in r["checks"])
        print(f"[contract] {r['id'].ljust(width)}  {row}   {'PASS' if r['pass'] else 'FAIL'}")
        for c in r["checks"]:
            if not c["pass"]:
                print(f"[contract]   ! {r['id']}.{c['name']}: {c['detail']}")

    with open(out_json, "w", encoding="utf8") as fh:
        json.dump({"pieces": results}, fh, indent=1)
        fh.write("\n")
    failed = [r["id"] for r in results if not r["pass"]]
    print(f"[contract] {len(results) - len(failed)}/{len(results)} pass -> {out_json}")
    if failed:
        print(f"[contract] FAILED: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
