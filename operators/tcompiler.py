import bpy
import re
import os

from .utils.strips import *


def compiletitle(titleclip: bpy.types.TextSequence):
    titlecontent = titleclip.text[2:]
    newclip = replacetemplate(titleclip, "h")
    newclip.text = titlecontent


class PROCEDITOR_OT_compiler(bpy.types.Operator):
    bl_idname = "proceditor.compile"
    bl_label = "compile text"
    
    # titles

    def execute(self, context):
        tpattern = re.compile('^h\..*')
        sequences = getsequences()
        titlesequences = []
        bpy.ops.sequencer.select(deselect_all=True)
        for i in sequences:
            if type(i) == bpy.types.TextSequence:
                if tpattern.match(i.text):
                    titlesequences.append(i)
        for i in titlesequences:
            compiletitle(i)
            
        return {'FINISHED'}

