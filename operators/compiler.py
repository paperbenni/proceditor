import bpy
import re
import os

from .utils.strips import *
from .utils.mrkp import *
from .utils.audio import *


def compilemarkupclip(clip: bpy.types.TextSequence):
    query = mrkpquery(clip.text)
    if not query.valid:
        return False

    newtemplate = replacetemplate(clip, query.name);
    if newtemplate == None:
        return False
    
    compiletemplate(newtemplate)

def compiletemplate(clip: bpy.types.MetaSequence):

    if clip["pcontent"] == None:
        return False
    placeholders = get_placeholders(clip)

    query = mrkpquery(clip["pcontent"])
    if not query.valid:
        return False

    for i in placeholders:
        compileplaceholder(i, query.arguments[placeholders.index(i)])
    
    adjustkeyframes(clip)
    return True


def compileplaceholder(clip: bpy.types.Sequence, param):
    cliptype = type(clip)
    # param as content for text clip
    if cliptype == bpy.types.TextSequence:
        clip.text = param
    # multiple choice metaclips, delete all except with name choice.param
    elif cliptype == bpy.types.MetaSequence:
        choices = clip.sequences.values()
        for i in choices:
            if i.name.startswith('choice.'):
                if i.name.removeprefix('choice.') != param:
                    removeclip(i)


def get_placeholders(clip: bpy.types.MetaSequence):
    placeholders = []
    placeholderregex = re.compile('^:[0-9][0-9]*:')
    counter = 0

    for i in clip.sequences.values():
        if placeholderregex.match(i.name):
            if int(i.name[1]) <= counter:
                placeholders.append(i)
                counter += 1
    return placeholders


def rgbtocolor(rgbcode):
    if not re.compile('^#[0-f][0-f][0-f][0-f][0-f][0-f]').match(rgbcode):
        return None

    colorcode = rgbcode.removeprefix('#').lower()
    colortuple = tuple(int(colorcode[i:i+2], 16) for i in (0, 2, 4))
    retcolor = Color((
        float(colortuple[0]) / 255,
        float(colortuple[1]) / 255,
        float(colortuple[2]) / 255
    ))
    return retcolor


# def compileaudio(clip: bpy.types.TextSequence):
#     params = mrkpquery(clip.text).getparams()
#     filepath = downloadclip(params[0])
#     if not filepath:
#         return False
#     startframe = clip.frame_start
#     endframe = clip.frame_final_end
#     channel = clip.channel
#     bpy.context.scene.sequence_editor.sequences.remove(clip)
#     os.system('notify-send "' + filepath + '"')
#     bpy.context.scene.sequence_editor.sequences.new_sound(
#         "proceditor audio", filepath, channel, startframe)


class PROCEDITOR_OT_compiler(bpy.types.Operator):
    bl_idname = "proceditor.compile"
    bl_label = "compile text"

    def execute(self, context):
        selectedclips = saveselection()

        rawsequences = getmarkupsequences()

        for i in rawsequences:
            compilemarkupclip(i)

        bpy.ops.sequencer.select(deselect_all=True)

        for i in selectedclips:
            i.select = True
        return {'FINISHED'}
