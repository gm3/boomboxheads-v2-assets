import bpy
import os

# Set the working dir to the current dir
dir = os.path.dirname(bpy.data.filepath)
if not dir:
    dir = os.getcwd()
os.chdir(dir)

# Create a subdir called "blender" if it doesn't already exist
if not os.path.exists(os.path.join(dir, "blender")):
    os.mkdir(os.path.join(dir, "blender"))

# Remove all data blocks
for block in bpy.data.meshes:
    bpy.data.meshes.remove(block)
for block in bpy.data.armatures:
    bpy.data.armatures.remove(block)
for block in bpy.data.materials:
    bpy.data.materials.remove(block)
for block in bpy.data.textures:
    bpy.data.textures.remove(block)
for block in bpy.data.collections:
    bpy.data.collections.remove(block)
for block in bpy.data.images:
    bpy.data.images.remove(block)
for block in bpy.data.libraries:
    bpy.data.libraries.remove(block)
for block in bpy.data.node_groups:
    bpy.data.node_groups.remove(block)
for block in bpy.data.shape_keys:
    bpy.data.shape_keys.remove(block)

# Loop through all files in the dir with the .glb extension
for file_name in os.listdir(dir):
    if file_name.endswith(".glb"):
        # Load the glb file
        bpy.ops.import_scene.gltf(filepath=os.path.join(dir, file_name))

        # Select all objects
        bpy.ops.object.select_all(action='SELECT')

        # Get all objects in the scene
        objs = bpy.context.scene.objects
        
        # Iterate through each object and remove shapekeys if it has them
        for obj in objs:
            if obj.type == 'MESH':
                if obj.data.shape_keys:
                    obj.shape_key_clear()


        # Get a list of all mesh objects in the scene
        mesh_objs = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        
        # Loop through each mesh object and make a single user copy of its mesh data
        for obj in mesh_objs:
            # Make a copy of the mesh data and set it as the object's data
            new_mesh = obj.data.copy()
            obj.data = new_mesh
        
            # Make the mesh data single user
            bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True)

        
        # Apply armature modifier
        for mod in bpy.context.active_object.modifiers:
            if mod.type == 'ARMATURE':
                bpy.ops.object.modifier_apply(modifier=mod.name)
       

        # Iterate through all objects in the scene
        for obj in bpy.context.scene.objects:
            # Check if the object has an armature modifier
            arm_mod = [mod for mod in obj.modifiers if mod.type == 'ARMATURE']
            if arm_mod:
                # Apply the armature modifier to the object
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_apply(modifier=arm_mod[0].name)


        # Set armature to active object
        armature_obj = bpy.context.scene.objects.get("Armature")
        if armature_obj:
            bpy.context.view_layer.objects.active = armature_obj
        
            # Select all meshes parented to the armature
            bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')
        
            # Clear and keep transformations for selected objects
            for obj in bpy.context.selected_objects:
                obj.select_set(True)
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
                # Clear parent to keep transformations
                bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
                obj.select_set(False)

        # Select the armature object(s)
        armature_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'ARMATURE']



        # Apply the armature transformation to its child objects
        for armature_obj in armature_objs:
            for child_obj in armature_obj.children:
                child_obj.matrix_world = armature_obj.matrix_world @ child_obj.matrix_local


        # Get all mesh objects in the scene
        mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        
        ## Select all mesh objects
        #for obj in mesh_objects:
        #    obj.select_set(True)
        #
        ## Join all selected objects

	## Select all objects in the scene
	#for obj in bpy.context.scene.objects:
	#    obj.select_set(True)
	#
	## Get the object named "BBody"
	#bbody = bpy.data.objects.get("BBody")
	#
	## Set it as the active object
	#bpy.context.view_layer.objects.active = bbody
	#
	## Join all selected objects to the active object
	#bpy.ops.object.join()

        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')
        
        # Select all objects
        bpy.ops.object.select_all(action='SELECT')
        
        # Get reference to "BBody" object
        bbody = bpy.data.objects.get("BBody")
        
        # Set active object to "BBody"
        bpy.context.view_layer.objects.active = bbody
        
        # Join all selected objects to "BBody"
        bpy.ops.object.join()

        # Select all objects
        bpy.ops.object.select_all(action='SELECT')

        # Get all objects in the scene
        objs = bpy.context.scene.objects
        

        # Get the armature object by name
        armature_obj = bpy.data.objects.get("Armature")
        
        if armature_obj is not None:
            # Remove the armature object from the scene
            bpy.data.objects.remove(armature_obj, do_unlink=True)

        # Clear and keep transforms for layers
        for obj in bpy.context.selected_objects:
            if obj.type == 'EMPTY':
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        # Clear empty objects
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.context.scene.objects:
            if obj.type == 'EMPTY' and not obj.children:
                obj.select_set(True)
        bpy.ops.object.delete()

        # Iterate over all materials
        for mat in bpy.data.materials:
            # Set the specular value
            mat.specular_intensity = 0.043


        # Export the glb file with a new file name
        export_file_name = os.path.splitext(file_name)[0] + '_fixed.glb'
        export_file_path = os.path.join(dir, export_file_name)
        bpy.ops.export_scene.gltf(filepath=export_file_path, export_format='GLB', export_current_frame=True)

        # Remove all data blocks
        for block in bpy.data.meshes:
            bpy.data.meshes.remove(block)
        for block in bpy.data.armatures:
            bpy.data.armatures.remove(block)
        for block in bpy.data.materials:
            bpy.data.materials.remove(block)
        for block in bpy.data.textures:
            bpy.data.textures.remove(block)
        for block in bpy.data.collections:
            bpy.data.collections.remove(block)
        for block in bpy.data.images:
            bpy.data.images.remove(block)
        for block in bpy.data.libraries:
            bpy.data.libraries.remove(block)
        for block in bpy.data.node_groups:
            bpy.data.node_groups.remove(block)
        for block in bpy.data.shape_keys:
            bpy.data.shape_keys.remove(block)

        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')
        
        # Delete all objects in the scene
        bpy.ops.object.delete(use_global=False)
        
        # Remove all materials
        for material in bpy.data.materials:
            bpy.data.materials.remove(material)
        
        # Remove all textures
        for texture in bpy.data.textures:
            bpy.data.textures.remove(texture)
        
        # Remove all images
        for image in bpy.data.images:
            bpy.data.images.remove(image)
