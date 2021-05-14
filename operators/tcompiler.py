import bpy
import re
import os

from .utils.strips import *

def compiletitle(titleclip: bpy.types.TextSequence):
    titlecontent = titleclip.text
    newclip = replacetemplate(titleclip, "t")
    if not newclip:
        return

    newclip.text = titlecontent[2:]
    newclip["pcontent"] = titlecontent

class PROCEDITOR_OT_compiler(bpy.types.Operator):
    bl_idname = "proceditor.compile"
    bl_label = "compile text"

    def execute(self, context):
        selectedclips = []
        for i in bpy.context.scene.sequence_editor.sequences_all:
            if i.select:
                selectedclips.append(i)
        titlesequences = getrawsequences(regex='^t\..*')
        colorsequences = getrawsequences(regex='^c\..*')
        compiledsequences = getrawsequences(compiled = True)
        bpy.ops.sequencer.select(deselect_all=True)

        for i in titlesequences:
            compiletitle(i)

        for i in colorsequences:
            replacetemplate(i, "c")

        for i in compiledsequences:
            adjustkeyframes(i)
        
        for i in selectedclips:
            i.select = True
        return {'FINISHED'}
