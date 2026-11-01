"""
NEUROTWIN AI // Procedural Cybernetic Pedestal Generator (Blender Python API)
-----------------------------------------------------------------------------
Generates a multi-tiered sci-fi holographic platform with glowing cyan emitter
rings and floating data pillars, then exports it directly to GLTF/GLB for Three.js.

Usage (Headless CLI from project root):
    blender --background --python blender_scripts/generate_pedestal.py

Usage (Inside Blender GUI):
    Open in Blender's Scripting workspace and click "Run Script" (Alt + P).
"""

import bpy
import bmesh
import math
from pathlib import Path


def clear_scene():
    """Removes all default meshes, lights, and cameras for a clean export."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)


def create_pbr_material(name, base_color, metallic=0.9, roughness=0.2, emission_color=None, emission_strength=0.0):
    """Creates a GLTF-compatible Principled BSDF material (Blender 3.x & 4.x compatible)."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")

    if bsdf:
        bsdf.inputs["Base Color"].default_value = base_color
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness

        if emission_color and emission_strength > 0:
            # Handle Blender 4.0+ ("Emission Color") and Blender 3.x ("Emission")
            if "Emission Color" in bsdf.inputs:
                bsdf.inputs["Emission Color"].default_value = emission_color
            elif "Emission" in bsdf.inputs:
                bsdf.inputs["Emission"].default_value = emission_color

            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = emission_strength

    return mat


def add_bevel_and_smooth(obj, width=0.03, segments=2):
    """Applies a clean mechanical bevel and auto-smoothing for crisp sci-fi edges."""
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = width
    bevel.segments = segments
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(30)

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()


def build_cyber_pedestal():
    clear_scene()

    # 1. Define Materials
    mat_obsidian_metal = create_pbr_material(
        name="NT_Obsidian_Armor",
        base_color=(0.04, 0.06, 0.12, 1.0),
        metallic=0.92,
        roughness=0.22
    )

    mat_titanium_trim = create_pbr_material(
        name="NT_Titanium_Trim",
        base_color=(0.15, 0.20, 0.28, 1.0),
        metallic=0.85,
        roughness=0.30
    )

    mat_cyan_emissive = create_pbr_material(
        name="NT_Cyan_Synapse_Glow",
        base_color=(0.05, 0.75, 0.95, 1.0),
        metallic=0.1,
        roughness=0.1,
        emission_color=(0.13, 0.83, 0.93, 1.0),
        emission_strength=6.5
    )

    # Create Master Parent Empty for clean Three.js Scene Graph import
    root = bpy.data.objects.new("NeuroTwin_Pedestal_Root", None)
    bpy.context.collection.objects.link(root)

    # 2. Tier 1: Heavy Octagonal Base Plate
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=2.6,
        depth=0.28,
        location=(0, 0, 0.14)
    )
    base_tier = bpy.context.active_object
    base_tier.name = "Pedestal_Base_Tier"
    base_tier.data.materials.append(mat_obsidian_metal)
    add_bevel_and_smooth(base_tier, width=0.04, segments=3)
    base_tier.parent = root

    # 3. Tier 2: Stepped Inner Core Platform
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=2.05,
        depth=0.22,
        location=(0, 0, 0.36)
    )
    mid_tier = bpy.context.active_object
    mid_tier.name = "Pedestal_Mid_Tier"
    mid_tier.data.materials.append(mat_titanium_trim)
    add_bevel_and_smooth(mid_tier, width=0.025, segments=2)
    mid_tier.parent = root

    # 4. Concentric Glowing Emitter Rings
    ring_specs = [
        ("Emitter_Ring_Inner", 1.55, 0.035, 0.48),
        ("Emitter_Ring_Mid",   2.12, 0.028, 0.30),
        ("Emitter_Ring_Outer", 2.65, 0.022, 0.12),
    ]

    for r_name, major_r, minor_r, z_pos in ring_specs:
        bpy.ops.mesh.primitive_torus_add(
            major_radius=major_r,
            minor_radius=minor_r,
            major_segments=64,
            minor_segments=16,
            location=(0, 0, z_pos)
        )
        ring = bpy.context.active_object
        ring.name = r_name
        ring.data.materials.append(mat_cyan_emissive)
        ring.parent = root

    # 5. Radial Cybernetic Data Pillars (8 Symmetrical Fin Anchors)
    num_pillars = 8
    pillar_radius = 2.32
    for i in range(num_pillars):
        angle = (2 * math.pi / num_pillars) * i
        px = math.cos(angle) * pillar_radius
        py = math.sin(angle) * pillar_radius

        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            location=(px, py, 0.34),
            rotation=(0, math.radians(-18), angle)
        )
        pillar = bpy.context.active_object
        pillar.name = f"Synapse_Pylon_{i+1:02d}"
        pillar.scale = (0.36, 0.14, 0.24)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        pillar.data.materials.append(mat_obsidian_metal)
        add_bevel_and_smooth(pillar, width=0.015, segments=2)
        pillar.parent = root

        # Add a glowing energy strip on top of each pylon
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            location=(px * 0.96, py * 0.96, 0.46),
            rotation=(0, math.radians(-18), angle)
        )
        strip = bpy.context.active_object
        strip.name = f"Synapse_Pylon_Glow_{i+1:02d}"
        strip.scale = (0.28, 0.05, 0.04)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        strip.data.materials.append(mat_cyan_emissive)
        strip.parent = root

    # 6. Central Hologram Emitter Lens
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=48,
        radius=1.35,
        depth=0.06,
        location=(0, 0, 0.49)
    )
    lens = bpy.context.active_object
    lens.name = "Central_Holo_Emitter"
    lens.data.materials.append(mat_cyan_emissive)
    lens.parent = root

    print("[NeuroTwin Blender Pipeline] Procedural pedestal mesh generated.")


def export_glb():
    """Exports the generated pedestal directly to frontend/public/assets/models/pedestal.glb."""
    script_dir = Path(__file__).resolve().parent
    output_dir = script_dir.parent / "frontend" / "public" / "assets" / "models"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "pedestal.glb"

    bpy.ops.export_scene.gltf(
        filepath=str(output_file),
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_yup=True  # Converts Blender Z-up to Three.js Y-up automatically
    )
    print(f"[NeuroTwin Blender Pipeline] Successfully exported GLB -> {output_file}")


if __name__ == "__main__":
    build_cyber_pedestal()
    export_glb()