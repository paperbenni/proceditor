import bpy
import os

from .utils.strips import *

class PROCEDITOR_OT_add_text(bpy.types.Operator):
    bl_idname = "proceditor.add_text"
    bl_label = "Add a text clip with a text popup"

    text_content: bpy.props.StringProperty(name="text")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        sequences = getsequences()
        bpy.ops.sequencer.effect_strip_add(type='TEXT', frame_start = bpy.context.scene.frame_current, frame_end = bpy.context.scene.frame_current + 20)
        activateselection()
        newclip = bpy.context.scene.sequence_editor.active_strip
        newclip.text = self.text_content
        newclip.align_y = 'CENTER'
        newclip.font_size = 50
        newclip.name = 'procedittext'
        newclip.location[1] = 0.5
        newclip.blend_type = 'ALPHA_OVER'

        return {'FINISHED'}
