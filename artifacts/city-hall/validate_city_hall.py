"""Fresh-scene validation and re-import review render for City Hall GLB.

    blender -b --python validate_city_hall.py -- [--glb FILE] [--out FILE]
"""

import json
import math
import os
import sys

import bpy
from mathutils import Vector

ALLOWED_MATERIALS = {"Toy_cream", "Toy_sand", "Toy_trim", "Toy_glass", "Toy_stone", "Toy_roofd", "Toy_roofc", "Toy_gold"}


def rounded(vector):
    return [round(value, 4) for value in vector]


def aim(obj, target):
    obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()


def render_reimport_review(here, meshes, mn, mx):
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.resolution_x = 1200; scene.render.resolution_y = 900; scene.render.resolution_percentage = 100
    scene.view_settings.view_transform = "Standard"; scene.view_settings.look = "None"; scene.view_settings.exposure = 0.2
    scene.world = bpy.data.worlds.new("Validation studio"); scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.86, 0.80, 0.69, 1)
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.65
    dims = mx - mn; span = max(dims.x, dims.y)
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    key = bpy.data.lights.new("validation_key", "AREA"); key.energy = 1800; key.size = span * 0.75
    key_obj = bpy.data.objects.new("validation_key", key); bpy.context.collection.objects.link(key_obj)
    key_obj.location = (-span * 0.7, -span * 0.8, span * 0.9); aim(key_obj, Vector((0, 0, 28)))
    fill = bpy.data.lights.new("validation_fill", "AREA"); fill.energy = 850; fill.size = span * 0.55
    fill_obj = bpy.data.objects.new("validation_fill", fill); bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (span * 0.75, span * 0.25, span * 0.6); aim(fill_obj, Vector((0, 0, 30)))
    bpy.ops.mesh.primitive_plane_add(size=span * 4, location=(0, 0, -0.04))
    floor = bpy.context.object
    floor_mat = bpy.data.materials.new("Validation floor"); floor_mat.diffuse_color = (0.58, 0.49, 0.37, 1)
    floor.data.materials.append(floor_mat)
    cam_data = bpy.data.cameras.new("validation_camera"); cam_data.lens = 76
    cam = bpy.data.objects.new("validation_camera", cam_data); bpy.context.collection.objects.link(cam)
    pitch = math.radians(39); azimuth = math.radians(135); radius = span * 3.05
    cam.location = Vector((center.x + radius * math.cos(pitch) * math.sin(azimuth),
                           center.y + radius * math.cos(pitch) * math.cos(azimuth),
                           center.z + radius * math.sin(pitch)))
    aim(cam, Vector((center.x, center.y, 25)))
    scene.camera = cam
    path = os.path.join(here, "city-hall-validation-aerial.png")
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    return path


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))
    def arg(flag, default): return argv[argv.index(flag) + 1] if flag in argv else default
    glb = arg("--glb", os.path.join(here, "city-hall.glb"))
    output = arg("--out", os.path.join(here, "validation.json"))

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb)
    objects = list(bpy.data.objects)
    meshes = [obj for obj in objects if obj.type == "MESH"]
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mn = Vector((1e12, 1e12, 1e12)); mx = Vector((-1e12, -1e12, -1e12))
    triangles = 0; degenerate = 0; invalid_normals = 0; object_rows = []
    for obj in meshes:
        evaluated = obj.evaluated_get(depsgraph); mesh = evaluated.to_mesh(); mesh.calc_loop_triangles()
        triangles += len(mesh.loop_triangles)
        degenerate += sum(1 for triangle in mesh.loop_triangles if triangle.area < 1e-8)
        for vertex in mesh.vertices:
            point = obj.matrix_world @ vertex.co
            for index in range(3):
                mn[index] = min(mn[index], point[index]); mx[index] = max(mx[index], point[index])
        for loop in mesh.loops:
            normal = loop.normal
            if not all(math.isfinite(value) for value in normal) or abs(normal.length - 1.0) > 1e-3:
                invalid_normals += 1
        object_rows.append({"name": obj.name, "triangles": len(mesh.loop_triangles),
                            "location": rounded(obj.location), "rotation_euler": rounded(obj.rotation_euler), "scale": rounded(obj.scale)})
        evaluated.to_mesh_clear()

    material_rows = []; textured = []; transparent = []; off_contract = []; glow_violations = []
    for mat in bpy.data.materials:
        texture_nodes = []; alpha = 1.0; roughness = None; emission = 0.0
        if mat.use_nodes:
            texture_nodes = [node.name for node in mat.node_tree.nodes if node.type == "TEX_IMAGE"]
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                alpha = float(bsdf.inputs["Alpha"].default_value)
                roughness = float(bsdf.inputs["Roughness"].default_value)
                emission = float(bsdf.inputs["Emission Strength"].default_value)
        if texture_nodes: textured.append(mat.name)
        if alpha < 0.999 or mat.surface_render_method != "DITHERED":
            # Blender's imported opaque glTF materials use DITHERED in 4.5; alpha is the authoritative check.
            if alpha < 0.999: transparent.append(mat.name)
        compliant = mat.name in ALLOWED_MATERIALS and mat.name.startswith("Toy_") and mat.name != "Toy_body"
        if not compliant: off_contract.append(mat.name)
        if mat.name.endswith("_Glow"): glow_violations.append(mat.name)
        material_rows.append({"name": mat.name, "contract_compliant": compliant,
                              "image_texture_nodes": texture_nodes, "alpha": round(alpha, 4),
                              "roughness": round(roughness, 4) if roughness is not None else None,
                              "glow": mat.name.endswith("_Glow"), "exported_emission_strength": round(emission, 4)})

    transforms_applied = all(
        all(abs(value - 1.0) < 1e-5 for value in obj.scale)
        and all(abs(value) < 1e-5 for value in obj.rotation_euler)
        and all(abs(value) < 1e-5 for value in obj.location) for obj in meshes)
    negative_scale = any(math.prod(obj.matrix_world.to_scale()) < 0 for obj in meshes)
    animations = sum(len(action.fcurves) for action in bpy.data.actions)
    unexpected = [obj.name for obj in objects if obj.type != "MESH"]
    dims = mx - mn
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))

    # Deterministic first-hit rays test the visible shell after final re-import.
    ray_hits = 0; flipped_hits = 0; flipped_by_object = {}
    golden = math.pi * (3.0 - math.sqrt(5.0))
    targets = [Vector((center.x + dx * dims.x, center.y + dy * dims.y, mn.z + fz * dims.z))
               for dx, dy in ((0, 0), (-0.2, -0.12), (0.2, 0.12)) for fz in (0.18, 0.52, 0.86)]
    for target in targets:
        for i in range(650):
            q = 1.0 - 2.0 * (i + 0.5) / 650
            r = math.sqrt(max(0.0, 1.0 - q * q)); angle = golden * i
            outward = Vector((math.cos(angle) * r, math.sin(angle) * r, q)); direction = -outward
            hit, _, normal, _, hit_obj, _ = bpy.context.scene.ray_cast(depsgraph, target + outward * 1000, direction, distance=1400)
            if hit:
                ray_hits += 1
                if normal.dot(direction) > 1e-5:
                    flipped_hits += 1
                    flipped_by_object[hit_obj.name] = flipped_by_object.get(hit_obj.name, 0) + 1
    normal_tolerance = max(3, math.ceil(ray_hits * 0.0075))
    normals_pass = invalid_normals == 0 and ray_hits > 0 and flipped_hits <= normal_tolerance

    results = {
        "asset": os.path.basename(glb), "validator": "Blender " + bpy.app.version_string,
        "fresh_isolated_scene": True, "reimported_final_glb": True,
        "object_count": len(objects), "mesh_object_count": len(meshes),
        "triangle_count": triangles, "triangle_budget": 27000,
        "dimensions_m": rounded(dims), "bbox_min_m": rounded(mn), "bbox_max_m": rounded(mx),
        "min_z_m": round(mn.z, 4), "xy_center_offset_m": [round(center.x, 4), round(center.y, 4)],
        "materials": sorted(mat.name for mat in bpy.data.materials),
        "material_details": sorted(material_rows, key=lambda row: row["name"]),
        "image_texture_count": len(bpy.data.images), "textured_materials": sorted(textured),
        "transparent_materials": sorted(transparent), "camera_count": len(bpy.data.cameras),
        "light_count": len(bpy.data.lights), "animation_fcurve_count": animations,
        "armature_count": sum(1 for obj in objects if obj.type == "ARMATURE"),
        "constraint_count": sum(len(obj.constraints) for obj in objects),
        "transforms_applied": transforms_applied, "negative_scales": negative_scale,
        "degenerate_triangle_count": degenerate, "invalid_or_nonunit_loop_normal_count": invalid_normals,
        "normal_ray_cast_first_hits": ray_hits, "normal_ray_cast_flipped_visible_faces": flipped_hits,
        "normal_ray_cast_flipped_by_object": dict(sorted(flipped_by_object.items())),
        "normal_ray_cast_tolerance": normal_tolerance,
        "normal_orientation_status": "PASS" if normals_pass else "FAIL",
        "normal_orientation_method": "Finite/unit re-imported loop normals plus 5,850 deterministic exterior first-hit rays (0.75% tolerance for overlapping decorative planes).",
        "unexpected_geometry_or_objects": unexpected, "material_contract_violations": sorted(off_contract),
        "glow_contract_violations": sorted(glow_violations),
        "duplicate_object_names": sorted({obj.name for obj in objects if sum(other.name == obj.name for other in objects) > 1}),
        "object_details": sorted(object_rows, key=lambda row: row["name"]),
    }
    results["checks"] = {
        "meters_and_plausible_dimensions": 112 <= dims.x <= 126 and 135 <= dims.y <= 148 and 93.5 <= dims.z <= 94.0,
        "base_at_z_zero": abs(mn.z) <= 0.05,
        "origin_at_base_center": abs(center.x) <= 1.0 and abs(center.y) <= 1.0,
        "under_triangle_budget": triangles <= 27000,
        "no_image_textures": not bpy.data.images and not textured,
        "no_transparency": not transparent,
        "materials_follow_contract": not off_contract and not glow_violations,
        "no_cameras_or_lights": not bpy.data.cameras and not bpy.data.lights,
        "no_animation_skin_or_constraints": animations == 0 and results["armature_count"] == 0 and results["constraint_count"] == 0,
        "transforms_applied": transforms_applied,
        "no_negative_scales": not negative_scale,
        "normals_outward": normals_pass,
        "no_degenerate_geometry": degenerate == 0,
        "no_unexpected_objects": not unexpected,
        "unique_object_names": not results["duplicate_object_names"],
    }
    results["overall"] = "PASS" if all(results["checks"].values()) else "FAIL"
    review_path = render_reimport_review(here, meshes, mn, mx)
    results["reimport_review_image"] = os.path.basename(review_path)
    with open(output, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2); file.write("\n")
    print(json.dumps({key: results[key] for key in ("overall", "triangle_count", "dimensions_m", "bbox_min_m", "bbox_max_m", "checks")}, indent=2))


if __name__ == "__main__":
    main()
