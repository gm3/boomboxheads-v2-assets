import bpy
import os

# Set the input and output directories
input_dir = bpy.path.abspath("/mnt/c/Users/gamer/Documents/GitHub/glTF-Transform-lod-script/out")
output_dir = bpy.path.abspath("/mnt/c/Users/gamer/Documents/GitHub/glTF-Transform-lod-script/out/output/")

# Make sure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# Loop through all files in the input directory
for file in os.listdir(input_dir):
    if file.endswith(".glb"):
        # Import the glb file
        filepath = os.path.join(input_dir, file)
        bpy.ops.import_scene.gltf(filepath=filepath)

        # Delete any object named "BBody"
        obj = bpy.data.objects.get("BBody")
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)

        # Export all the other meshes separately as glb files
        for obj in bpy.context.scene.objects:
            if obj.type == "MESH":
                export_filename = "out_" + obj.name + "_" + file
                export_path = os.path.join(output_dir, export_filename)
                bpy.ops.export_scene.gltf(filepath=export_path, use_selection=True) 
                bpy.ops.object.select_all(action="DESELECT")
                bpy.data.objects[obj.name].select_set(True)
                bpy.ops.object.delete()

        # Deselect all objects to clear the selection
        bpy.ops.object.select_all(action="DESELECT")
