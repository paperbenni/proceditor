import bpy
import re
import os

from .utils.strips import *
from .utils.mrkp import *
from .utils.audio import *

colorscheme = {
    ("r", "red") : "#E0527E", 
    ("dr", "red") : "#E0527E", 
    ("g", "green") : "#52DF67", 
    ("b", "blue") : "#5293E1",
    ("bg", "background"): "#292F3A", 
    ("y", "yellow"): "#E09F52"
}

def compiletitle(titleclip: bpy.types.TextSequence):
    titlecontent = titleclip.text
    newclip = replacetemplate(titleclip, "t")
    if not newclip:
        return

    newclip.text = mrkpquery(titlecontent).getparams()[0]
    newclip["pcontent"] = titlecontent

def compilecolor(clip: bpy.types.TextSequence):

    params = mrkpquery(clip.text).getparams()
    newclip = replacetemplate(clip, "c")
    if not newclip:
        return False
    # allow custom color
    if len(params) != 0:
        customcolor = False
        if re.compile('^#[0-f][0-f][0-f][0-f][0-f][0-f]').match(params[0]):
            customcolor = params[0].lstrip("#")
        else:
            for i in colorscheme.keys():
                param = params[0]
                if param in i:
                    customcolor = colorscheme[i].lower().lstrip("#")

        if customcolor:
            colortuple = tuple(int(customcolor[i:i+2], 16) for i in (0, 2, 4))
            newclip.color.r = float(colortuple[0]) / 255
            newclip.color.g = float(colortuple[1]) / 255
            newclip.color.b = float(colortuple[2]) / 255

def compileaudio(clip: bpy.types.TextSequence):
    params = mrkpquery(clip.text).getparams()
    filepath = downloadclip(params[0])
    if not filepath:
        return False
    startframe = clip.frame_start
    endframe = clip.frame_final_end
    channel = clip.channel
    bpy.context.scene.sequence_editor.sequences.remove(clip)
    os.system('notify-send "' + filepath + '"')
    bpy.context.scene.sequence_editor.sequences.new_sound("proceditor audio", filepath, channel, startframe)


compilers = {
    Prefix.TITLE: compiletitle,
    Prefix.COLOR: compilecolor, 
    Prefix.AUDIO: compileaudio
}

class PROCEDITOR_OT_compiler(bpy.types.Operator):
    bl_idname = "proceditor.compile"
    bl_label = "compile text"

    def execute(self, context):
        selectedclips = []
        for i in bpy.context.scene.sequence_editor.sequences_all:
            if i.select:
                selectedclips.append(i)

        rawsequences = getrawsequences()

        for i in rawsequences:
            query = mrkpquery(i.text)
            type = query.gettype()
            if type and type in compilers.keys():
                compilers[type](i)

        bpy.ops.sequencer.select(deselect_all=True)

        compiledsequences = getrawsequences(compiled = True)

        for i in compiledsequences:
            adjustkeyframes(i)
        
        for i in selectedclips:
            i.select = True
        return {'FINISHED'}