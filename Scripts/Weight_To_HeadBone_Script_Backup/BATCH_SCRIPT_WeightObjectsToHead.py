bl_info = {
    "name": "Weight Objects to Head Bone",
    "author": "OpenAI",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object > Weight Objects to Head Bone",
    "description": "Weights all objects except 'BBody' to the head bone with 100% influence",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}

import bpy

class OBJECT_OT_weight_objects_to_head_bone(bpy.types.Operator):
    bl_idname = "object.weight_objects_to_head_bone"
    bl_label = "Weight Objects to Head Bone"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Find the base mesh object "BBody"
        base_mesh_obj = bpy.data.objects.get("BBody")

        if not base_mesh_obj:
            self.report({'ERROR'}, "Base mesh object 'BBody' not found in the scene")
            return {'CANCELLED'}

        # Check if the base mesh object has an armature modifier
        armature_modifier = None
        for modifier in base_mesh_obj.modifiers:
            if modifier.type == 'ARMATURE':
                armature_modifier = modifier
                break

        if not armature_modifier:
            self.report({'ERROR'}, "Base mesh object must have an Armature modifier")
            return {'CANCELLED'}

        # Get the armature object from the modifier
        armature_obj = armature_modifier.object

        # Make sure armature is selected
        bpy.ops.object.select_all(action='DESELECT')
        armature_obj.select_set(True)
        context.view_layer.objects.active = armature_obj

        # Set armature to Pose mode
        bpy.ops.object.mode_set(mode='POSE')

        # Find the head bone
        head_bone = None
        for bone in armature_obj.pose.bones:
            if bone.name == 'Head_bind':  # Replace 'head_bone_name' with the actual head bone name
                head_bone = bone
                break

        if not head_bone:
            self.report({'ERROR'}, "Head bone not found in armature")
            return {'CANCELLED'}

        # Iterate through all objects in the scene
        for obj in bpy.data.objects:
            # Check if the object is a mesh and not the base mesh object "BBody"
            if obj.type == 'MESH' and obj != base_mesh_obj:
                # Add an armature modifier to the object, if not present
                armature_modifier = None
                for modifier in obj.modifiers:
                    if modifier.type == 'ARMATURE':
                        armature_modifier = modifier
                        break

                if not armature_modifier:
                    armature_modifier = obj.modifiers.new('Armature', 'ARMATURE')

                # Set the armature object in the object's modifier
                armature_modifier.object = armature_obj

                # Add a new vertex group to the object and assign it to the head bone
                vertex_group = obj.vertex_groups.new(name=head_bone.name)
                vertices = [v.index for v in obj.data.vertices]
                vertex_group.add(vertices, 1.0, 'REPLACE')  # 100% weight

        # Set armature back to Object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, "Weighted objects to head bone successfully")

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_weight_objects_to_head_bone.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_weight_objects_to_head_bone)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_weight_objects_to_head_bone)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()
