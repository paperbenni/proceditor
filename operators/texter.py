import bpy
import os

from .utils.strips import *

class PROCEDITOR_OT_add_text(bpy.types.Operator):
    bl_idname = "proceditor.add_text"
    bl_label = "Add a text clip with a text popup"

    text_content: bpy.props.StringProperty(name="Text yaboiii")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        sequences = getsequences()
        bpy.ops.sequencer.effect_strip_add(type='TEXT', frame_start = bpy.context.scene.frame_current, frame_end = bpy.context.scene.frame_current + 20)
        newclip = getnewsequence(sequences)
        newclip.text = self.text_content
        newclip.align_y = 'CENTER'
        newclip.font_size = 50
        newclip.location[1] = 0.5
        newclip.blend_type = 'ALPHA_OVER'

        # for i in sequences:
        #     if type(i) == bpy.types.TextSequence:
        #         titleclip = i
        #         i.text = self.text_content
        #         break

        # map(lambda x: x.select + False, sequences)
        # titleclip.select = True

        # bpy.context.scene.sequence_editor.active_strip = titleclip
        # bpy.ops.sequencer.duplicate_move(TRANSFORM_OT_seq_slide={"value": (bpy.context.scene.frame_current, 0), "snap": False, "snap_target": 'CLOSEST', "snap_point": (
        #     0, 0, 0), "snap_align": False, "release_confirm": False, "use_accurate": False})

        return {'FINISHED'}
