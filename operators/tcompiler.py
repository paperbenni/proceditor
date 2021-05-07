import bpy
import re
import os

from .utils.strips import *

class PROCEDITOR_OT_compiler(bpy.types.Operator):
    bl_idname = "proceditor.compile"
    bl_label = "compile text"
    
    # titles

    def execute(self, context):
        tpattern = re.compile('^h\..*')
        sequences = getsequences()
        bpy.ops.sequencer.select(deselect_all=True)
        for i in sequences:
            if type(i) == bpy.types.TextSequence:
                if tpattern.match(i.text):
                    i.select = True
        bpy.ops.sequencer.delete()
            
        return {'FINISHED'}

