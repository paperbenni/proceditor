import bpy
import re
import os

from .utils.strips import *


def compiletitle(titleclip: bpy.types.TextSequence):
    titlecontent = titleclip.text
    newclip = replacetemplate(titleclip, "t")
    if newclip:
        newclip.text = titlecontent[2:]
        newclip["pcontent"] = titlecontent

class PROCEDITOR_OT_compiler(bpy.types.Operator):
    bl_idname = "proceditor.compile"
    bl_label = "compile text"

    def execute(self, context):
        titlesequences = getrawsequences(regex='^t\..*')
        bpy.ops.sequencer.select(deselect_all=True)

        for i in titlesequences:
            compiletitle(i)
        return {'FINISHED'}
